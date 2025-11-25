from flask import Blueprint, jsonify, request

from app.schemas.relevamiento import RelevamientoSimpleCreate
from app.services.relevamiento_service import crear_relevamiento_simple

bp = Blueprint("relevamiento", __name__, url_prefix="/api/v1/relevamientos")


@bp.post("")
def crear_rel():
    try:
        payload = RelevamientoSimpleCreate(**request.json)
        nuevo = crear_relevamiento_simple(payload)
        return jsonify(nuevo.to_dict()), 201

    except Exception as e:
        return jsonify(
            {
                "detail": "Error al crear relevamiento",
                "error": str(e),
            }
        ), 400
