# app/routes/actuacion_routes.py

from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.database import db
from app.models import Actuacion
from app.schemas.actuacion import ActuacionBatch
from app.services.actuacion_service import ActuacionServiceError, crear_actuacion_desde_item

bp = Blueprint("actuaciones", __name__)


def _serializar_actuacion(actuacion: Actuacion) -> dict:
    """Convierte el modelo en un dict listo para el front."""

    inspectores = [i.apellido for i in actuacion.inspectores]
    notificaciones = [
        {
            "numero": n.numero_acta,
            "anio": int(n.anio),
            "motivos": [m.nombre for m in n.motivos],
        }
        for n in actuacion.actas_notificacion
    ]
    comprobaciones = [
        {"numero": c.numero_acta, "anio": int(c.anio)} for c in actuacion.actas_comprobacion
    ]

    return {
        "id": actuacion.id,
        "orden_trabajo_numero": actuacion.orden_trabajo.numero if actuacion.orden_trabajo else None,
        "fecha_actuacion": actuacion.fecha.isoformat() if actuacion.fecha else None,
        "rubro_nombre": "",
        "inspectores": inspectores,
        "calle": actuacion.establecimiento_domicilio.domicilio.calle
        if getattr(actuacion, "establecimiento_domicilio", None)
        and actuacion.establecimiento_domicilio.domicilio
        else "",
        "numero": actuacion.establecimiento_domicilio.domicilio.numero
        if getattr(actuacion, "establecimiento_domicilio", None)
        and actuacion.establecimiento_domicilio.domicilio
        else "",
        "tipo_actuacion": actuacion.tipo,
        "doc_tipo_codigo": None,
        "doc_nro": None,
        "contrib_apellido": None,
        "contrib_nombre": None,
        "acta_inspeccion_num": actuacion.acta_inspeccion.numero_acta
        if actuacion.acta_inspeccion
        else None,
        "acta_notificacion_num": notificaciones[0]["numero"] if notificaciones else None,
        "acta_comprobacion_num": comprobaciones[0]["numero"] if comprobaciones else None,
        "acta_clausura_num": actuacion.acta_clausura.numero_acta
        if actuacion.acta_clausura
        else None,
        "acta_decomiso_num": actuacion.acta_decomiso.numero_acta
        if actuacion.acta_decomiso
        else None,
    }


@bp.get("")
def listar_actuaciones():
    actuaciones = Actuacion.query.all()
    return jsonify([_serializar_actuacion(a) for a in actuaciones]), 200


@bp.post("")
def crear_actuaciones():
    """POST /api/v1/actuaciones: recibe un batch de actuaciones y las persiste."""

    try:
        payload = request.get_json(force=True)
    except Exception:
        return jsonify({"detail": "JSON inválido o ausente"}), 400

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
                respuesta["rubro_nombre"] = item.rubro_nombre
                respuesta["calle"] = item.calle
                respuesta["numero"] = item.numero
                respuesta["inspectores"] = item.inspectores
                actuaciones_creadas.append(respuesta)

        return jsonify(actuaciones_creadas if len(actuaciones_creadas) > 1 else actuaciones_creadas[0]), 201
    except ActuacionServiceError as e:
        db.session.rollback()
        return jsonify({"detail": str(e)}), 400
    except Exception as e:  # pragma: no cover - log interno
        db.session.rollback()
        return (
            jsonify({"detail": "Error interno al guardar la actuación", "error": str(e)}),
            500,
        )
