from app.models.relevamiento_simple import RelevamientoSimple

from app.database import db


def crear_relevamiento_simple(data):
    rel = RelevamientoSimple(
        fecha=data.fecha,
        inspector=data.inspector,
        direccion=data.direccion,
        rubro=data.rubro,
    )
    db.session.add(rel)
    db.session.commit()
    return rel
