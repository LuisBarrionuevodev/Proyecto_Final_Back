# app/routes/actuacion_routes.py

from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.database import db
from app.schemas.actuacion import ActuacionBatch
from app.services.actuacion_service import ActuacionServiceError, crear_actuacion_desde_item

bp = Blueprint("actuaciones", __name__)


@bp.post("")
def crear_actuaciones():
    """POST /api/v1/actuaciones: recibe un batch de actuaciones y las persiste."""

    try:
        payload = request.get_json(force=True)
    except Exception:
        return jsonify({"detail": "JSON inválido o ausente"}), 400

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
                actuaciones_creadas.append(
                    {
                        "id": actuacion.id,
                        "fecha": actuacion.fecha.isoformat(),
                        "tipo": actuacion.tipo,
                        "orden_trabajo_id": actuacion.orden_trabajo_id,
                    }
                )

        return jsonify(actuaciones_creadas), 201
    except ActuacionServiceError as e:
        db.session.rollback()
        return jsonify({"detail": str(e)}), 400
    except Exception as e:  # pragma: no cover - log interno
        db.session.rollback()
        return (
            jsonify({"detail": "Error interno al guardar la actuación", "error": str(e)}),
            500,
        )
