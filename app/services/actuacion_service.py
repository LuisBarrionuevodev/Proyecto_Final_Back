# app/services/actuacion_service.py

from __future__ import annotations

import logging
from typing import Iterable, Optional

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError

from app.database import db
from app.models import (
    ActaClausura,
    ActaComprobacion,
    ActaDecomiso,
    ActaInspeccion,
    Actuacion,
    ActuacionComprobacion,
    ActuacionInspector,
    ActuacionNotificacion,
    Contribuyente,
    DocumentoTipo,
    Domicilio,
    Expediente,
    Inspector,
    MotivoClausura,
    MotivoNotificacion,
    Notificacion,
    NotificacionMotivo,
    Oficio,
    OrdenTrabajo,
    Rubro,
)
from app.schemas.actuacion import ActuacionItem

logger = logging.getLogger(__name__)


class ActuacionServiceError(Exception):
    """Errores de negocio al guardar actuaciones."""


# ==========================
#   HELPERS GENERALES
# ==========================


def _anio_acta(item: ActuacionItem, anio_campo: Optional[int]) -> int:
    """Devuelve el año informado o deriva del año de la actuación."""
    return int(anio_campo or item.fecha_actuacion.year)


def _get_or_create_orden_trabajo(numero: str) -> OrdenTrabajo:
    """
    Busca una OT por número. Si no existe, la crea.
    Esto mantiene la unicidad de orden_trabajo.numero.
    """
    stmt = select(OrdenTrabajo).filter_by(numero=numero)
    existente = db.session.execute(stmt).scalar_one_or_none()
    if existente:
        return existente

    nueva = OrdenTrabajo(numero=numero, descripcion=None)
    db.session.add(nueva)
    db.session.flush()
    return nueva


def _get_or_create_documento_tipo(codigo: str) -> DocumentoTipo:
    """
    Devuelve un tipo de documento. Si no existe, lo crea
    con nombre=código (por ahora simple).
    """
    stmt = select(DocumentoTipo).filter(
        func.upper(DocumentoTipo.codigo) == codigo.upper()
    )
    existente = db.session.execute(stmt).scalar_one_or_none()
    if existente:
        return existente

    nuevo = DocumentoTipo(codigo=codigo.upper(), nombre=codigo.upper())
    db.session.add(nuevo)
    db.session.flush()
    return nuevo


def _get_or_create_contribuyente(
    doc_tipo: DocumentoTipo, doc_nro: str, apellido: str, nombre: Optional[str]
) -> Contribuyente:
    """
    Unicidad por (doc_tipo_id, doc_nro).

    - Si ya existe, actualiza apellido/nombre si vienen valores nuevos.
    - Si no existe, crea uno nuevo.
    """
    stmt = select(Contribuyente).filter_by(doc_tipo_id=doc_tipo.id, doc_nro=doc_nro)
    existente = db.session.execute(stmt).scalar_one_or_none()
    if existente:
        existente.apellido = apellido or existente.apellido
        existente.nombre = nombre or existente.nombre
        return existente

    nuevo = Contribuyente(
        apellido=apellido or "",
        nombre=nombre or "",
        doc_tipo_id=doc_tipo.id,
        doc_nro=doc_nro,
    )
    db.session.add(nuevo)
    db.session.flush()
    return nuevo


def _get_or_create_rubro(nombre: str) -> Rubro:
    """
    Rubro único por nombre (case-insensitive).
    """
    stmt = select(Rubro).filter(func.upper(Rubro.nombre) == nombre.upper())
    existente = db.session.execute(stmt).scalar_one_or_none()
    if existente:
        return existente

    nuevo = Rubro(nombre=nombre.upper())
    db.session.add(nuevo)
    db.session.flush()
    return nuevo


# ==========================
#   DOMICILIO
# ==========================


def _normalizar_calle(calle: str) -> str:
    """Normaliza la calle (trim + mayúsculas) para comparar."""
    return (calle or "").strip().upper()


def _normalizar_numero(numero: Optional[str]) -> Optional[str]:
    """Normaliza el número a string sin espacios; si queda vacío, lo deja en None."""
    if numero is None:
        return None
    s = str(numero).strip()
    return s or None


def _get_or_create_domicilio(
    contribuyente: Contribuyente,
    rubro: Rubro,
    calle: str,
    numero: Optional[str],
) -> Domicilio:
    """
    Crea (si hace falta) un domicilio comercial asociado al contribuyente
    para un rubro determinado.

    Por ahora tomamos como 'clave natural':
    (contribuyente_id, rubro_id, calle, numero).
    """
    calle_std = _normalizar_calle(calle)
    numero_std = _normalizar_numero(numero)

    stmt = select(Domicilio).filter(
        func.upper(Domicilio.calle) == calle_std,
        Domicilio.numero == numero_std,
        Domicilio.contribuyente_id == contribuyente.id,
        Domicilio.rubro_id == rubro.id,
    )
    existente = db.session.execute(stmt).scalar_one_or_none()
    if existente:
        return existente

    domicilio = Domicilio(
        calle=calle_std,
        numero=numero_std,
        contribuyente_id=contribuyente.id,
        rubro_id=rubro.id,
    )
    db.session.add(domicilio)
    db.session.flush()
    return domicilio


# ==========================
#   INSPECTORES
# ==========================


def _next_inspector_legajo() -> int:
    max_legajo = db.session.query(func.max(Inspector.legajo)).scalar()
    return int(max_legajo or 0) + 1


def _get_or_create_inspector(apellido: str) -> Inspector:
    """
    Busca inspector por apellido (case-insensitive).
    Si no existe, lo crea con legajo incremental y nombre=apellido.
    """
    stmt = select(Inspector).filter(func.upper(Inspector.apellido) == apellido.upper())
    inspector = db.session.execute(stmt).scalar_one_or_none()
    if inspector:
        return inspector

    legajo = _next_inspector_legajo()
    nuevo = Inspector(legajo=legajo, apellido=apellido.upper(), nombre=apellido.upper())
    db.session.add(nuevo)
    db.session.flush()
    return nuevo


def _asegurar_actuacion_inspector(actuacion: Actuacion, inspector: Inspector) -> None:
    """
    Asegura el vínculo en la tabla puente actuacion_inspector.
    Si ya existe (actuacion_id, inspector_id), no duplica.
    """
    existe = db.session.execute(
        select(ActuacionInspector).filter_by(
            actuacion_id=actuacion.id, inspector_id=inspector.id
        )
    ).scalar_one_or_none()
    if existe:
        return
    db.session.add(
        ActuacionInspector(actuacion_id=actuacion.id, inspector_id=inspector.id)
    )


# ==========================
#   ACTUACIÓN
# ==========================


def _crear_actuacion(
    item: ActuacionItem,
    ot: OrdenTrabajo,
    domicilio: Domicilio,
) -> Actuacion:
    """
    Crea la actuación principal, apuntando DIRECTO a domicilio_id
    (nuevo modelo, sin tablas establecimiento_*).
    """
    actuacion = Actuacion(
        fecha=item.fecha_actuacion,
        tipo=item.tipo_actuacion,
        orden_trabajo_id=ot.id,
        domicilio_id=domicilio.id,
        contraproducencia=item.contraproducencia,
        observaciones=None,
    )
    db.session.add(actuacion)
    db.session.flush()
    return actuacion


# ==========================
#   ACTAS / NOTIFICACIONES
# ==========================


def _crear_acta_inspeccion(actuacion: Actuacion, item: ActuacionItem) -> None:
    if not item.acta_inspeccion_num:
        return

    anio = _anio_acta(item, None)
    existente = db.session.execute(
        select(ActaInspeccion).filter_by(
            numero_acta=item.acta_inspeccion_num, anio=anio
        )
    ).scalar_one_or_none()
    if existente and existente.actuacion_id != actuacion.id:
        raise ActuacionServiceError(
            "El acta de inspección indicada ya está asociada a otra actuación"
        )
    if existente:
        existente.actuacion_id = actuacion.id
        return

    db.session.add(
        ActaInspeccion(
            numero_acta=item.acta_inspeccion_num, anio=anio, actuacion_id=actuacion.id
        )
    )


def _crear_notificacion(
    actuacion: Actuacion,
    numero: str,
    anio: int,
    motivos: Iterable[str],
    contexto: str,
) -> Notificacion:
    notificacion = db.session.execute(
        select(Notificacion).filter_by(numero_acta=numero, anio=anio)
    ).scalar_one_or_none()

    if not notificacion:
        notificacion = Notificacion(numero_acta=numero, anio=anio)
        db.session.add(notificacion)
        db.session.flush()

    for idx, motivo_texto in enumerate(motivos, start=1):
        if not motivo_texto:
            continue
        motivo = db.session.execute(
            select(MotivoNotificacion).filter(
                func.upper(MotivoNotificacion.nombre) == motivo_texto.upper()
            )
        ).scalar_one_or_none()
        if not motivo:
            motivo = MotivoNotificacion(nombre=motivo_texto.upper())
            db.session.add(motivo)
            db.session.flush()
        existe_motivo = db.session.execute(
            select(NotificacionMotivo).filter_by(
                notificacion_id=notificacion.id, motivo_id=motivo.id
            )
        ).scalar_one_or_none()
        if not existe_motivo:
            db.session.add(
                NotificacionMotivo(
                    notificacion_id=notificacion.id, motivo_id=motivo.id, orden=idx
                )
            )

    _vincular_notificacion(actuacion, notificacion, contexto)
    return notificacion


def _merge_contexto(actual: Optional[str], nuevo: Optional[str]) -> Optional[str]:
    if not nuevo:
        return actual
    if not actual:
        return nuevo
    valores = {c.strip() for c in actual.split("|") if c.strip()}
    valores.add(nuevo)
    return "|".join(sorted(valores))


def _vincular_notificacion(
    actuacion: Actuacion, notificacion: Notificacion, contexto: Optional[str]
) -> None:
    existente = db.session.execute(
        select(ActuacionNotificacion).filter_by(
            actuacion_id=actuacion.id, notificacion_id=notificacion.id
        )
    ).scalar_one_or_none()
    if existente:
        existente.contexto = _merge_contexto(existente.contexto, contexto)
        return
    db.session.add(
        ActuacionNotificacion(
            actuacion_id=actuacion.id,
            notificacion_id=notificacion.id,
            contexto=_merge_contexto(None, contexto),
        )
    )


def _crear_acta_comprobacion(
    actuacion: Actuacion,
    numero: str,
    anio: int,
    contexto: str,
    marcada_doble: bool,
    observaciones: Optional[str],
) -> ActaComprobacion:
    acta = db.session.execute(
        select(ActaComprobacion).filter_by(numero_acta=numero, anio=anio)
    ).scalar_one_or_none()
    if not acta:
        acta = ActaComprobacion(
            numero_acta=numero,
            anio=anio,
            actuada_dos_veces=marcada_doble,
            observaciones=observaciones,
        )
        db.session.add(acta)
        db.session.flush()
    else:
        if marcada_doble:
            acta.actuada_dos_veces = True
        if observaciones:
            acta.observaciones = observaciones

    _vincular_comprobacion(actuacion, acta, contexto)
    if marcada_doble and not acta.actuada_dos_veces:
        acta.actuada_dos_veces = True
    return acta


def _vincular_comprobacion(
    actuacion: Actuacion, acta: ActaComprobacion, contexto: Optional[str]
) -> None:
    existente = db.session.execute(
        select(ActuacionComprobacion).filter_by(
            actuacion_id=actuacion.id, acta_comprobacion_id=acta.id
        )
    ).scalar_one_or_none()
    if existente:
        existente.contexto = _merge_contexto(existente.contexto, contexto)
        return
    db.session.add(
        ActuacionComprobacion(
            actuacion_id=actuacion.id,
            acta_comprobacion_id=acta.id,
            contexto=_merge_contexto(None, contexto),
        )
    )


def _crear_acta_clausura(actuacion: Actuacion, item: ActuacionItem) -> None:
    if not item.acta_clausura_num:
        return
    anio = _anio_acta(item, None)
    acta = db.session.execute(
        select(ActaClausura).filter_by(numero_acta=item.acta_clausura_num, anio=anio)
    ).scalar_one_or_none()
    if acta and acta.actuacion_id != actuacion.id:
        raise ActuacionServiceError(
            "El acta de clausura indicada ya está vinculada a otra actuación"
        )

    motivo_nombre = item.clausura_motivo or "SIN MOTIVO"
    motivo = db.session.execute(
        select(MotivoClausura).filter(
            func.upper(MotivoClausura.nombre) == motivo_nombre.upper()
        )
    ).scalar_one_or_none()
    if not motivo:
        motivo = MotivoClausura(nombre=motivo_nombre.upper())
        db.session.add(motivo)
        db.session.flush()

    if acta:
        acta.actuacion_id = actuacion.id
        acta.motivo_id = motivo.id
        return

    db.session.add(
        ActaClausura(
            numero_acta=item.acta_clausura_num,
            anio=anio,
            actuacion_id=actuacion.id,
            motivo_id=motivo.id,
            observaciones=None,
        )
    )


def _crear_acta_decomiso(actuacion: Actuacion, item: ActuacionItem) -> None:
    if not item.acta_decomiso_num:
        return
    anio = _anio_acta(item, None)
    acta = db.session.execute(
        select(ActaDecomiso).filter_by(numero_acta=item.acta_decomiso_num, anio=anio)
    ).scalar_one_or_none()
    if acta and acta.actuacion_id != actuacion.id:
        raise ActuacionServiceError(
            "El acta de decomiso indicada ya está vinculada a otra actuación"
        )

    cantidad = item.decomiso_kilos_total or 0
    if acta:
        acta.actuacion_id = actuacion.id
        acta.cantidad = cantidad
        acta.unidad = acta.unidad or "KG"
        return

    db.session.add(
        ActaDecomiso(
            numero_acta=item.acta_decomiso_num,
            anio=anio,
            cantidad=cantidad,
            unidad="KG",
            actuacion_id=actuacion.id,
        )
    )


def _crear_expediente(actuacion: Actuacion, item: ActuacionItem) -> None:
    """
    Crea (si no existe) el expediente vinculado a la actuación.
    1:1 con actuacion (en el schema nuevo el UNIQUE está sobre actuacion_id).
    """
    numero_expediente = (item.expediente_numero or "").strip()
    anio = item.expediente_anio

    if not numero_expediente or anio is None:
        return

    anio_int = int(anio)

    existente = db.session.execute(
        select(Expediente).filter_by(
            actuacion_id=actuacion.id,
            numero_expediente=numero_expediente,
            anio=anio_int,
        )
    ).scalar_one_or_none()

    if existente:
        return

    exp = Expediente(
        numero_expediente=numero_expediente,
        anio=anio_int,
        actuacion_id=actuacion.id,
        observaciones=None,
    )
    db.session.add(exp)
    db.session.flush()


def _crear_oficio(acta: ActaComprobacion, item: ActuacionItem) -> None:
    if not item.oficio_numero or item.oficio_anio is None:
        return

    existente = db.session.execute(
        select(Oficio).filter_by(
            numero_oficio=item.oficio_numero,
            anio=item.oficio_anio,
            acta_comprobacion_id=acta.id,
        )
    ).scalar_one_or_none()
    if existente:
        return

    db.session.add(
        Oficio(
            numero_oficio=item.oficio_numero,
            anio=item.oficio_anio,
            causa=item.oficio_causa,
            acta_comprobacion_id=acta.id,
        )
    )


# ==========================
#   FLUJOS SEGÚN TIPO
# ==========================


def _procesar_actas_base(
    actuacion: Actuacion,
    item: ActuacionItem,
    incluir_comprobacion: bool = True,
) -> Optional[ActaComprobacion]:
    _crear_acta_inspeccion(actuacion, item)

    if item.acta_notificacion_num:
        anio = _anio_acta(item, None)
        motivos = [
            item.notificacion_motivo_1,
            item.notificacion_motivo_2,
            item.notificacion_motivo_3,
        ]
        _crear_notificacion(actuacion, item.acta_notificacion_num, anio, motivos, "DIA")

    acta_comp_creada: Optional[ActaComprobacion] = None
    if incluir_comprobacion and item.acta_comprobacion_num:
        anio = _anio_acta(item, None)
        acta_comp_creada = _crear_acta_comprobacion(
            actuacion,
            item.acta_comprobacion_num,
            anio,
            "DIA",
            False,
            item.comprobacion_motivo,
        )
        _crear_oficio(acta_comp_creada, item)

    _crear_acta_clausura(actuacion, item)
    _crear_acta_decomiso(actuacion, item)
    return acta_comp_creada


def _procesar_actas_reinspeccion(actuacion: Actuacion, item: ActuacionItem) -> None:
    # Actas "del día" igual que inspección
    _procesar_actas_base(actuacion, item)

    # SOLO maneja NOTIFICACIÓN PREVIA, no comprobación
    if item.notificacion_previa_num:
        anio = _anio_acta(item, None)
        notificacion = db.session.execute(
            select(Notificacion).filter_by(
                numero_acta=item.notificacion_previa_num,
                anio=anio,
            )
        ).scalar_one_or_none()

        if not notificacion:
            # Crear acta notificación sin motivos, contexto PREVIA
            notificacion = _crear_notificacion(
                actuacion,
                item.notificacion_previa_num,
                anio,
                [],
                "PREVIA",
            )
        else:
            # Vincularla como PREVIA
            _vincular_notificacion(actuacion, notificacion, "PREVIA")

        # Y también marcar que se "actúa de nuevo" en esta actuación
        _vincular_notificacion(actuacion, notificacion, "DIA")


def _procesar_actas_ratificacion(actuacion: Actuacion, item: ActuacionItem) -> None:
    _procesar_actas_base(actuacion, item, incluir_comprobacion=False)

    if item.acta_comprobacion_num:
        anio = _anio_acta(item, None)
        acta = _crear_acta_comprobacion(
            actuacion,
            item.acta_comprobacion_num,
            anio,
            "RATIFICA",
            True,
            item.comprobacion_motivo,
        )
        _vincular_comprobacion(actuacion, acta, "PREVIA")
        _crear_oficio(acta, item)

    if item.acta_clausura_num:
        _crear_acta_clausura(actuacion, item)


def _procesar_actas_verificar(actuacion: Actuacion, item: ActuacionItem) -> None:
    _procesar_actas_base(actuacion, item)

    if item.comprobacion_previa_num:
        anio = _anio_acta(item, None)
        acta = _crear_acta_comprobacion(
            actuacion,
            item.comprobacion_previa_num,
            anio,
            "PREVIA",
            True,
            item.comprobacion_motivo,
        )
        _vincular_comprobacion(actuacion, acta, "VERIFICAR")


# ==========================
#   PUNTO DE ENTRADA PÚBLICO
# ==========================


def crear_actuacion_desde_item(item: ActuacionItem) -> Actuacion:
    """
    Orquesta todo el flujo de alta de una actuación:
      - OT
      - contribuyente + tipo doc
      - rubro
      - domicilio (contribuyente + rubro)
      - actuación
      - inspectores
      - actas (según tipo)
      - expediente
    """
    # Debug útil cuando algo no se persiste como esperás
    print("DEBUG ITEM >>>")
    print("  calle:", repr(item.calle))
    print("  numero:", repr(item.numero))
    print("  doc_tipo_codigo:", repr(item.doc_tipo_codigo))
    print("  doc_nro:", repr(item.doc_nro))
    print("  contrib_apellido:", repr(item.contrib_apellido))
    print("  contrib_nombre:", repr(item.contrib_nombre))
    print("  inspectores:", repr(item.inspectores))
    print("  rubro_nombre:", repr(item.rubro_nombre))
    print("<<< FIN DEBUG")

    try:
        # 1) Orden de trabajo
        ot = _get_or_create_orden_trabajo(item.orden_trabajo_numero)

        # 2) Contribuyente
        doc_tipo = _get_or_create_documento_tipo(item.doc_tipo_codigo)
        contrib = _get_or_create_contribuyente(
            doc_tipo,
            item.doc_nro,
            item.contrib_apellido,
            item.contrib_nombre,
        )

        # 3) Rubro
        rubro = _get_or_create_rubro(item.rubro_nombre)

        # 4) Domicilio (ya vinculado a contribuyente y rubro)
        domicilio = _get_or_create_domicilio(
            contribuyente=contrib,
            rubro=rubro,
            calle=item.calle,
            numero=item.numero,
        )

        # 5) Crear actuación apuntando a domicilio_id
        actuacion = _crear_actuacion(item, ot, domicilio)

        # 6) Inspectores
        for inspector_nombre in item.inspectores:
            inspector = _get_or_create_inspector(inspector_nombre)
            _asegurar_actuacion_inspector(actuacion, inspector)

        # 7) Actas según tipo de actuación
        tipo = item.tipo_actuacion
        if tipo == "INSPECCION":
            _procesar_actas_base(actuacion, item)
        elif tipo == "REINSPECCION":
            _procesar_actas_reinspeccion(actuacion, item)
        elif tipo == "RATIFICACION":
            _procesar_actas_ratificacion(actuacion, item)
        elif tipo == "VERIFICAR E INFORMAR":
            _procesar_actas_verificar(actuacion, item)
        else:
            raise ActuacionServiceError(f"Tipo de actuación no soportado: {tipo}")

        # 8) Crear expediente (si viene)
        _crear_expediente(actuacion, item)

        return actuacion

    except IntegrityError as exc:
        detalle_db = str(getattr(exc, "orig", exc))
        raise ActuacionServiceError(
            f"Error de integridad al persistir la actuación: {detalle_db}"
        ) from exc
