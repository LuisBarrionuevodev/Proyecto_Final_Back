# app/routes/actuacion_routes.py

from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.database import db
from app.models import (
    Actuacion,
    ActuacionComprobacion,
    ActuacionNotificacion,
    OrdenTrabajo,
)
from app.schemas.actuacion import ActuacionBatch, ActuacionUpdate
from app.services.actuacion_service import (
    ActuacionServiceError,
    _get_or_create_inspector,
    crear_actuacion_desde_item,
)

bp = Blueprint("actuaciones", __name__)


# ==========================
#   SERIALIZADORES
# ==========================


def _serializar_actuacion_resumen(actuacion: Actuacion) -> dict:
    """Serializa los campos mínimos para un listado simple de actuaciones."""

    return {
        "id": actuacion.id,
        "fecha_actuacion": actuacion.fecha.isoformat() if actuacion.fecha else None,
        "tipo_actuacion": actuacion.tipo,
        "orden_trabajo_numero": actuacion.orden_trabajo.numero
        if actuacion.orden_trabajo
        else None,
        "domicilio_id": actuacion.domicilio_id,
        "created_at": actuacion.created_at.isoformat()
        if actuacion.created_at
        else None,
        "updated_at": actuacion.updated_at.isoformat()
        if actuacion.updated_at
        else None,
    }


def _serializar_actuacion(actuacion: Actuacion) -> dict:
    """
    Convierte el modelo en un dict listo para el front,
    incluyendo toda la info 'planchada' que necesitás en la tabla de gestión.
    """

    # Inspectores: concatenar apellido + nombre si están
    inspectores = []
    for inspector in actuacion.inspectores:
        nombre = f"{inspector.apellido or ''} {inspector.nombre or ''}".strip()
        if nombre:
            inspectores.append(nombre)

    # Nuevo modelo: actuacion -> domicilio -> (contribuyente, rubro)
    domicilio = getattr(actuacion, "domicilio", None)
    contrib = getattr(domicilio, "contribuyente", None) if domicilio else None
    rubro = getattr(domicilio, "rubro", None) if domicilio else None
    rubro_nombre = rubro.nombre if rubro else None

    # NOTIFICACIONES (actual y previa) usando la tabla puente actuacion_notificacion
    notificaciones_por_id = {n.id: n for n in actuacion.actas_notificacion}
    links_notif = ActuacionNotificacion.query.filter_by(actuacion_id=actuacion.id).all()
    notificacion_previa = None
    notificacion_actual = None
    for link in links_notif:
        notif = notificaciones_por_id.get(link.notificacion_id)
        if not notif:
            continue
        contexto = link.contexto or ""
        if "PREVIA" in contexto and not notificacion_previa:
            notificacion_previa = notif
        if "PREVIA" not in contexto and notificacion_actual is None:
            notificacion_actual = notif
    if not notificacion_actual and links_notif:
        notificacion_actual = notificaciones_por_id.get(links_notif[0].notificacion_id)

    motivos_notificacion = [
        m.nombre for m in (notificacion_actual.motivos if notificacion_actual else [])
    ]

    # COMPROBACIONES (actual y previa) usando la tabla puente actuacion_comprobacion
    comprobaciones_por_id = {c.id: c for c in actuacion.actas_comprobacion}
    links_comp = ActuacionComprobacion.query.filter_by(actuacion_id=actuacion.id).all()
    comprobacion_previa = None
    comprobacion_actual = None
    for link in links_comp:
        comp = comprobaciones_por_id.get(link.acta_comprobacion_id)
        if not comp:
            continue
        contexto = link.contexto or ""
        if "PREVIA" in contexto and not comprobacion_previa:
            comprobacion_previa = comp
        if "PREVIA" not in contexto and comprobacion_actual is None:
            comprobacion_actual = comp
    if not comprobacion_actual and links_comp:
        comprobacion_actual = comprobaciones_por_id.get(
            links_comp[0].acta_comprobacion_id
        )

    # Oficio (si existe) asociado a la comprobación actual
    oficio = (
        comprobacion_actual.oficios[0]
        if comprobacion_actual and getattr(comprobacion_actual, "oficios", None)
        else None
    )

    return {
        "id": actuacion.id,
        "orden_trabajo_numero": actuacion.orden_trabajo.numero
        if actuacion.orden_trabajo
        else None,
        "fecha_actuacion": actuacion.fecha.isoformat() if actuacion.fecha else None,
        "rubro_nombre": rubro_nombre,
        "inspectores": inspectores,
        "calle": domicilio.calle if domicilio else None,
        "numero": domicilio.numero if domicilio else None,
        "tipo_actuacion": actuacion.tipo,
        "contraproducencia": actuacion.contraproducencia,
        "doc_tipo_codigo": contrib.doc_tipo.codigo
        if contrib and contrib.doc_tipo
        else None,
        "doc_nro": contrib.doc_nro if contrib else None,
        "contrib_apellido": contrib.apellido if contrib else None,
        "contrib_nombre": contrib.nombre if contrib else None,
        "acta_inspeccion_num": actuacion.acta_inspeccion.numero_acta
        if actuacion.acta_inspeccion
        else None,
        "acta_notificacion_num": notificacion_actual.numero_acta
        if notificacion_actual
        else None,
        "notificacion_motivo_1": motivos_notificacion[0]
        if len(motivos_notificacion) > 0
        else None,
        "notificacion_motivo_2": motivos_notificacion[1]
        if len(motivos_notificacion) > 1
        else None,
        "notificacion_motivo_3": motivos_notificacion[2]
        if len(motivos_notificacion) > 2
        else None,
        "acta_comprobacion_num": comprobacion_actual.numero_acta
        if comprobacion_actual
        else None,
        "comprobacion_motivo": comprobacion_actual.observaciones
        if comprobacion_actual
        else None,
        "acta_clausura_num": actuacion.acta_clausura.numero_acta
        if actuacion.acta_clausura
        else None,
        "clausura_motivo": actuacion.acta_clausura.observaciones
        if actuacion.acta_clausura
        else None,
        "acta_decomiso_num": actuacion.acta_decomiso.numero_acta
        if actuacion.acta_decomiso
        else None,
        "decomiso_kilos_total": float(actuacion.acta_decomiso.cantidad)
        if actuacion.acta_decomiso and actuacion.acta_decomiso.cantidad is not None
        else None,
        "expediente_numero": actuacion.expediente.numero_expediente
        if actuacion.expediente
        else None,
        "expediente_anio": int(actuacion.expediente.anio)
        if actuacion.expediente
        else None,
        "oficio_numero": oficio.numero_oficio if oficio else None,
        "oficio_anio": int(oficio.anio) if oficio else None,
        "oficio_causa": oficio.causa if oficio else None,
        "notificacion_previa_num": notificacion_previa.numero_acta
        if notificacion_previa
        else None,
        "comprobacion_previa_num": comprobacion_previa.numero_acta
        if comprobacion_previa
        else None,
        "domicilio_id": actuacion.domicilio_id,
        "created_at": actuacion.created_at.isoformat()
        if actuacion.created_at
        else None,
        "updated_at": actuacion.updated_at.isoformat()
        if actuacion.updated_at
        else None,
    }


# ==========================
#   RUTAS
# ==========================


@bp.get("")
def listar_actuaciones():
    """GET /api/v1/actuaciones: lista todas las actuaciones (vista completa)."""
    actuaciones = Actuacion.query.all()
    return jsonify([_serializar_actuacion(a) for a in actuaciones]), 200


@bp.delete("/<int:actuacion_id>")
def eliminar_actuacion(actuacion_id: int):
    """DELETE /api/v1/actuaciones/<id>: elimina una actuación.

    - 204 si se eliminó bien
    - 404 si no existe
    - 409 si hay error de integridad (FK)
    - 500 para otros errores inesperados
    """
    actuacion = Actuacion.query.get(actuacion_id)
    if not actuacion:
        return jsonify({"detail": "Actuación no encontrada"}), 404

    try:
        db.session.delete(actuacion)
        db.session.commit()
        return "", 204

    except IntegrityError as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "detail": "No se pudo eliminar la actuación porque tiene registros relacionados (actas, expedientes, etc.)",
                    "error": str(e),
                }
            ),
            409,
        )

    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "detail": "Error interno al intentar eliminar la actuación",
                    "error": str(e),
                }
            ),
            500,
        )


@bp.put("/<int:actuacion_id>")
def actualizar_actuacion(actuacion_id: int):
    """
    PUT /api/v1/actuaciones/<id>

    Actualiza campos básicos de la actuación:
      - fecha_actuacion
      - tipo_actuacion
      - domicilio_id (nuevo modelo)
      - contraproducencia
      - inspectores
      - orden_trabajo_numero
    """
    try:
        payload = request.get_json(force=True)
    except Exception:
        return jsonify({"detail": "JSON inválido o ausente"}), 400

    try:
        dto = ActuacionUpdate.model_validate(payload)
    except ValidationError as e:
        return jsonify({"detail": "Error de validación", "errors": e.errors()}), 422

    actuacion = Actuacion.query.get(actuacion_id)
    if not actuacion:
        return jsonify({"detail": "Actuación no encontrada"}), 404

    try:
        if dto.fecha_actuacion is not None:
            actuacion.fecha = dto.fecha_actuacion
        if dto.tipo_actuacion is not None:
            actuacion.tipo = dto.tipo_actuacion

        # Nuevo: permitir cambiar el domicilio_id
        if "domicilio_id" in payload:
            actuacion.domicilio_id = dto.domicilio_id

        if dto.contraproducencia is not None:
            actuacion.contraproducencia = dto.contraproducencia

        if dto.inspectores is not None:
            nuevos_inspectores = []
            for inspector_nombre in dto.inspectores:
                inspector = _get_or_create_inspector(inspector_nombre)
                nuevos_inspectores.append(inspector)
            actuacion.inspectores = nuevos_inspectores

        # Cambio de orden de trabajo (puede ser None)
        if "orden_trabajo_numero" in payload:
            if dto.orden_trabajo_numero is None:
                actuacion.orden_trabajo_id = None
            else:
                orden_trabajo = db.session.execute(
                    select(OrdenTrabajo).filter_by(numero=dto.orden_trabajo_numero)
                ).scalar_one_or_none()
                if not orden_trabajo:
                    orden_trabajo = OrdenTrabajo(
                        numero=dto.orden_trabajo_numero, descripcion=None
                    )
                    db.session.add(orden_trabajo)
                    db.session.flush()

                actuacion.orden_trabajo_id = orden_trabajo.id

        db.session.commit()
        db.session.refresh(actuacion)
    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "detail": "Error interno al actualizar la actuación",
                    "error": str(e),
                }
            ),
            500,
        )

    # TODO: permitir actualizar rubro, domicilio (datos finos) y actas relacionadas de manera granular.
    return jsonify(_serializar_actuacion(actuacion)), 200


@bp.post("")
def crear_actuaciones():
    """POST /api/v1/actuaciones: recibe un batch de actuaciones y las persiste."""

    try:
        payload = request.get_json(force=True)
    except Exception:
        return jsonify({"detail": "JSON inválido o ausente"}), 400

    # Permitimos que venga un solo objeto o {"items": [...]}
    if isinstance(payload, dict) and "items" not in payload:
        payload = {"items": [payload]}

    try:
        batch = ActuacionBatch.model_validate(payload)
    except ValidationError as e:
        return (
            jsonify({"detail": "Error de validación", "errors": e.errors()}),
            422,
        )

    try:
        actuaciones_creadas = []
        with db.session.begin():
            for item in batch.items:
                actuacion = crear_actuacion_desde_item(item)
                respuesta = _serializar_actuacion(actuacion)

                # Estos campos DEBERÍAN matchear ya con lo que hay en DB,
                # pero los dejamos por si querés ver exactamente lo que se mandó.
                respuesta["rubro_nombre"] = item.rubro_nombre
                respuesta["calle"] = item.calle
                respuesta["numero"] = item.numero
                respuesta["inspectores"] = item.inspectores

                actuaciones_creadas.append(respuesta)

        return jsonify(
            actuaciones_creadas
            if len(actuaciones_creadas) > 1
            else actuaciones_creadas[0]
        ), 201
    except ActuacionServiceError as e:
        db.session.rollback()
        return jsonify({"detail": str(e)}), 400
    except Exception as e:  # pragma: no cover - log interno
        db.session.rollback()
        return (
            jsonify(
                {"detail": "Error interno al guardar la actuación", "error": str(e)}
            ),
            500,
        )
