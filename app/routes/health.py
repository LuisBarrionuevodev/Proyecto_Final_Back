# app/routes/health.py

from flask import Blueprint, jsonify

bp = Blueprint("health", __name__)


@bp.get("")
def health_check():
    """
    GET /api/v1/health
    Respuesta simple para verificar que la API está viva.
    """
    return jsonify({"status": "ok"}), 200
