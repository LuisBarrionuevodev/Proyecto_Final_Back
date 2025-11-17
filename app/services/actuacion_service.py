# app/services/actuacion_service.py

from __future__ import annotations

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


class ActuacionServiceError(Exception):
    """Errores de negocio al guardar actuaciones."""


def _anio_acta(item: ActuacionItem, anio_campo: Optional[int]) -> int:
    """Devuelve el año informado o deriva del año de la actuación."""

    return int(anio_campo or item.fecha_actuacion.year)


def _get_or_create_orden_trabajo(numero: str) -> OrdenTrabajo:
    stmt = select(OrdenTrabajo).filter_by(numero=numero)
    existente = db.session.execute(stmt).scalar_one_or_none()
    if existente:
        return existente

    nueva = OrdenTrabajo(numero=numero, descripcion=None)
    db.session.add(nueva)
    db.session.flush()
    return nueva


def _get_or_create_documento_tipo(codigo: str) -> DocumentoTipo:
    stmt = select(DocumentoTipo).filter(func.upper(DocumentoTipo.codigo) == codigo.upper())
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
    stmt = select(Contribuyente).filter_by(doc_tipo_id=doc_tipo.id, doc_nro=doc_nro)
    existente = db.session.execute(stmt).scalar_one_or_none()
    if existente:
        # actualizamos datos básicos si vienen
        existente.apellido = apellido or existente.apellido
        existente.nombre = nombre or existente.nombre
        return existente

    nuevo = Contribuyente(
        apellido=apellido or "", nombre=nombre or "", doc_tipo_id=doc_tipo.id, doc_nro=doc_nro
    )
    db.session.add(nuevo)
    db.session.flush()
    return nuevo


def _get_or_create_rubro(nombre: str) -> Rubro:
    stmt = select(Rubro).filter(func.upper(Rubro.nombre) == nombre.upper())
    existente = db.session.execute(stmt).scalar_one_or_none()
    if existente:
        return existente

    nuevo = Rubro(nombre=nombre.upper())
    db.session.add(nuevo)
    db.session.flush()
    return nuevo


def _next_inspector_legajo() -> int:
    max_legajo = db.session.query(func.max(Inspector.legajo)).scalar()
    return int(max_legajo or 0) + 1


def _get_or_create_inspector(apellido: str) -> Inspector:
    stmt = select(Inspector).filter(func.upper(Inspector.apellido) == apellido.upper())
    inspector = db.session.execute(stmt).scalar_one_or_none()
    if inspector:
        return inspector

    legajo = _next_inspector_legajo()
    nuevo = Inspector(legajo=legajo, apellido=apellido.upper(), nombre=apellido.upper())
    db.session.add(nuevo)
    db.session.flush()
    return nuevo


def _crear_domicilio(calle: str, numero: str) -> Domicilio:
    domicilio = Domicilio(calle=calle, numero=numero)
    db.session.add(domicilio)
    db.session.flush()
    return domicilio


def _asegurar_actuacion_inspector(actuacion: Actuacion, inspector: Inspector) -> None:
    existe = db.session.execute(
        select(ActuacionInspector).filter_by(
            actuacion_id=actuacion.id, inspector_id=inspector.id
        )
    ).scalar_one_or_none()
    if existe:
        return
    db.session.add(ActuacionInspector(actuacion_id=actuacion.id, inspector_id=inspector.id))


def _crear_actuacion(item: ActuacionItem, ot: OrdenTrabajo, dom: Domicilio) -> Actuacion:
    actuacion = Actuacion(
        fecha=item.fecha_actuacion,
        tipo=item.tipo_actuacion,
        orden_trabajo_id=ot.id,
        establecimiento_domicilio_id=None,
        contraproducencia=item.contraproducencia,
        observaciones=None,
    )
    db.session.add(actuacion)
    db.session.flush()
    return actuacion


def _crear_acta_inspeccion(actuacion: Actuacion, item: ActuacionItem) -> None:
    if not item.acta_inspeccion_num:
        return

    anio = _anio_acta(item, None)
    existente = db.session.execute(
        select(ActaInspeccion).filter_by(numero_acta=item.acta_inspeccion_num, anio=anio)
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
) -> None:
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
            select(MotivoNotificacion).filter(func.upper(MotivoNotificacion.nombre) == motivo_texto.upper())
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


def _vincular_notificacion(
    actuacion: Actuacion, notificacion: Notificacion, contexto: Optional[str]
) -> None:
    existente = db.session.execute(
        select(ActuacionNotificacion).filter_by(
            actuacion_id=actuacion.id, notificacion_id=notificacion.id
        )
    ).scalar_one_or_none()
    if existente:
        existente.contexto = contexto
        return
    db.session.add(
        ActuacionNotificacion(
            actuacion_id=actuacion.id, notificacion_id=notificacion.id, contexto=contexto
        )
    )


def _crear_acta_comprobacion(
    actuacion: Actuacion, numero: str, anio: int, contexto: str, marcada_doble: bool
) -> ActaComprobacion:
    acta = db.session.execute(
        select(ActaComprobacion).filter_by(numero_acta=numero, anio=anio)
    ).scalar_one_or_none()
    if not acta:
        acta = ActaComprobacion(
            numero_acta=numero, anio=anio, actuada_dos_veces=marcada_doble
        )
        db.session.add(acta)
        db.session.flush()
    elif marcada_doble:
        acta.actuada_dos_veces = True

    _vincular_comprobacion(actuacion, acta, contexto)
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
        existente.contexto = contexto
        return
    db.session.add(
        ActuacionComprobacion(
            actuacion_id=actuacion.id, acta_comprobacion_id=acta.id, contexto=contexto
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
        select(MotivoClausura).filter(func.upper(MotivoClausura.nombre) == motivo_nombre.upper())
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
    if not item.expediente_numero or item.expediente_anio is None:
        return

    existente = db.session.execute(
        select(Expediente).filter_by(
            actuacion_id=actuacion.id,
            numero=item.expediente_numero,
            anio=item.expediente_anio,
        )
    ).scalar_one_or_none()
    if existente:
        return

    db.session.add(
        Expediente(
            numero=item.expediente_numero,
            anio=item.expediente_anio,
            actuacion_id=actuacion.id,
        )
    )


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


def _procesar_actas_inspeccion(actuacion: Actuacion, item: ActuacionItem) -> None:
    _crear_acta_inspeccion(actuacion, item)

    if item.acta_notificacion_num:
        anio = _anio_acta(item, None)
        motivos = [item.notificacion_motivo_1, item.notificacion_motivo_2, item.notificacion_motivo_3]
        _crear_notificacion(actuacion, item.acta_notificacion_num, anio, motivos, "DIA")

    if item.acta_comprobacion_num:
        anio = _anio_acta(item, None)
        acta = _crear_acta_comprobacion(actuacion, item.acta_comprobacion_num, anio, "DIA", False)
        _crear_oficio(acta, item)

    _crear_acta_clausura(actuacion, item)
    _crear_acta_decomiso(actuacion, item)
    _crear_expediente(actuacion, item)


def _procesar_actas_reinspeccion(actuacion: Actuacion, item: ActuacionItem) -> None:
    _procesar_actas_inspeccion(actuacion, item)

    if item.notificacion_previa_num:
        anio = _anio_acta(item, None)
        notificacion = db.session.execute(
            select(Notificacion).filter_by(numero_acta=item.notificacion_previa_num, anio=anio)
        ).scalar_one_or_none()
        if notificacion:
            _vincular_notificacion(actuacion, notificacion, "PREVIA")
        else:
            _crear_notificacion(actuacion, item.notificacion_previa_num, anio, [], "PREVIA")

    if item.comprobacion_previa_num:
        anio = _anio_acta(item, None)
        _crear_acta_comprobacion(actuacion, item.comprobacion_previa_num, anio, "PREVIA", True)


def _procesar_actas_ratificacion(actuacion: Actuacion, item: ActuacionItem) -> None:
    _procesar_actas_inspeccion(actuacion, item)

    if item.acta_comprobacion_num:
        anio = _anio_acta(item, None)
        acta = _crear_acta_comprobacion(actuacion, item.acta_comprobacion_num, anio, "RATIFICA", True)
        _crear_oficio(acta, item)

    # Clausura previa: se registra como clausura actual pero respetando unicidad
    if item.acta_clausura_num:
        _crear_acta_clausura(actuacion, item)


def _procesar_actas_verificar(actuacion: Actuacion, item: ActuacionItem) -> None:
    _procesar_actas_inspeccion(actuacion, item)

    if item.comprobacion_previa_num:
        anio = _anio_acta(item, None)
        _crear_acta_comprobacion(actuacion, item.comprobacion_previa_num, anio, "PREVIA", True)


def crear_actuacion_desde_item(item: ActuacionItem) -> Actuacion:
    try:
        ot = _get_or_create_orden_trabajo(item.orden_trabajo_numero)
        doc_tipo = _get_or_create_documento_tipo(item.doc_tipo_codigo)
        contrib = _get_or_create_contribuyente(doc_tipo, item.doc_nro, item.contrib_apellido, item.contrib_nombre)
        domicilio = _crear_domicilio(item.calle, item.numero)
        _get_or_create_rubro(item.rubro_nombre)

        actuacion = _crear_actuacion(item, ot, domicilio)

        for inspector_nombre in item.inspectores:
            inspector = _get_or_create_inspector(inspector_nombre)
            _asegurar_actuacion_inspector(actuacion, inspector)

        tipo = item.tipo_actuacion
        if tipo == "INSPECCION":
            _procesar_actas_inspeccion(actuacion, item)
        elif tipo == "REINSPECCION":
            _procesar_actas_reinspeccion(actuacion, item)
        elif tipo == "RATIFICACION":
            _procesar_actas_ratificacion(actuacion, item)
        elif tipo == "VERIFICAR E INFORMAR":
            _procesar_actas_verificar(actuacion, item)
        else:
            raise ActuacionServiceError(f"Tipo de actuación no soportado: {tipo}")

        return actuacion
    except IntegrityError as exc:
        raise ActuacionServiceError("Error de integridad al persistir la actuación") from exc
