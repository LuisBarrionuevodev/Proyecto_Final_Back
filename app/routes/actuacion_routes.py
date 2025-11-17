# app/routes/actuacion_routes.py

from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.schemas.actuacion import ActuacionItem
from app.services.actuacion_service import (
    ActuacionServiceError,
    guardar_actuacion_desde_item,
)

bp = Blueprint("actuaciones", __name__)


@bp.post("")
def crear_actuacion():
    """
    POST /api/v1/actuaciones

    Recibe UNA actuación (una fila de la grilla del front) y la guarda.
    """
    try:
        payload = request.get_json(force=True)
    except Exception:
        return jsonify({"detail": "JSON inválido o ausente"}), 400

    # 1) Validar con Pydantic
    try:
        item = ActuacionItem.model_validate(payload)
    except ValidationError as e:
        return (
            jsonify(
                {
                    "detail": "Error de validación",
                    "errors": e.errors(),
                }
            ),
            422,
        )

    # 2) Guardar en la base
    try:
        actuacion = guardar_actuacion_desde_item(item)
    except ActuacionServiceError as e:
        return jsonify({"detail": str(e)}), 400
    except Exception as e:
        return (
            jsonify(
                {
                    "detail": "Error interno al guardar la actuación",
                    "error": str(e),
                }
            ),
            500,
        )

    # 3) Respuesta OK
    return (
        jsonify(
            {
                "id": actuacion.id,
                "fecha": actuacion.fecha.isoformat(),
                "tipo": actuacion.tipo,
                "orden_trabajo_id": actuacion.orden_trabajo_id,
            }
        ),
        201,
    )
