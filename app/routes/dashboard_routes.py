from flask import Blueprint, jsonify

from app.database import db

bp = Blueprint("dashboard", __name__, url_prefix="/api/v1/dashboard")


@bp.get("/resumen")
def resumen_dashboard():
    try:
        # Total actuaciones
        total_act = db.session.execute(
            db.text("SELECT COUNT(*) AS total FROM actuacion")
        ).scalar()

        # Total relevamientos
        total_rel = db.session.execute(
            db.text("SELECT COUNT(*) AS total FROM relevamiento_simple")
        ).scalar()

        # Pendientes (no tienen PREVIA)
        pendientes = db.session.execute(
            db.text("""
                SELECT COUNT(*) AS pendientes
                FROM (
                SELECT notificacion_id
                FROM actuacion_notificacion
                GROUP BY notificacion_id
                HAVING COUNT(*) = 1
                AND SUM(contexto LIKE '%PREVIA%') = 0
                ) AS t;

            """)
        ).scalar()

        # Completadas (sí tienen PREVIA)
        completadas = db.session.execute(
            db.text("""
                SELECT COUNT(*) AS completadas
                FROM (
                SELECT notificacion_id
                FROM actuacion_notificacion
                GROUP BY notificacion_id
                HAVING COUNT(*) = 2
                AND SUM(contexto LIKE '%PREVIA%') = 1
                ) AS t;
    
            """)
        ).scalar()

        return jsonify(
            {
                "actuaciones": total_act,
                "relevamientos": total_rel,
                "pendientes": pendientes,
                "completadas": completadas,
            }
        )

    except Exception as e:
        return jsonify({"detail": "Error al obtener dashboard", "error": str(e)}), 500
