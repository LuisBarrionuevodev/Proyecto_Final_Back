# app/services/actuacion_service.py

from __future__ import annotations

from sqlalchemy import select

from app.database import db
from app.models import Actuacion, OrdenTrabajo
from app.schemas.actuacion import ActuacionItem


class ActuacionServiceError(Exception):
    """Errores de negocio al guardar actuaciones."""


def _map_tipo_actuacion(tipo_str: str, item: ActuacionItem) -> str:
    """
    Mapea el tipo del formulario (Pydantic) al tipo interno de la tabla `actuacion.tipo`.

    En el modelo definimos:
    # INSPECCION | REINSPECCION | RATIF_CLAUSURA | RATIF_DECOMISO | VERIF_INFORMAR
    """
    s = tipo_str.upper()
    if s == "INSPECCION":
        return "INSPECCION"
    if s == "REINSPECCION":
        return "REINSPECCION"
    if s == "RATIFICACION":
        # distinguimos según qué acta viene
        if item.acta_clausura_num:
            return "RATIF_CLAUSURA"
        if item.acta_decomiso_num:
            return "RATIF_DECOMISO"
        # fallback genérico
        return "RATIF_CLAUSURA"
    if s == "VERIFICAR E INFORMAR":
        return "VERIF_INFORMAR"

    raise ActuacionServiceError(f"Tipo de actuación no soportado: {tipo_str}")


def _get_or_create_orden_trabajo(numero: str) -> OrdenTrabajo:
    """
    Busca una orden de trabajo por `numero`. Si no existe, la crea.
    Usa el modelo:

    class OrdenTrabajo(db.Model):
        __tablename__ = "orden_trabajo"
        id = db.Column(db.Integer, primary_key=True)
        numero = db.Column(db.String(6), nullable=False, index=True)
        descripcion = db.Column(db.String(255), nullable=True)
        ...
    """
    stmt = select(OrdenTrabajo).filter_by(numero=numero)
    ot = db.session.execute(stmt).scalar_one_or_none()
    if ot is not None:
        return ot

    ot = OrdenTrabajo(
        numero=numero,
        descripcion=None,  # si querés, podés poner algo por defecto acá
    )
    db.session.add(ot)
    db.session.flush()
    return ot


def guardar_actuacion_desde_item(item: ActuacionItem) -> Actuacion:
    """
    Orquesta el guardado de UNA actuación:

    - Valida el tipo de actuación y lo mapea al enum interno.
    - Busca/crea OrdenTrabajo por número.
    - Crea la Actuacion con campos básicos.

    Más adelante enchufamos:
    - inspectores
    - contribuyente
    - domicilio/establecimiento
    - actas, etc.
    """
    try:
        ot = _get_or_create_orden_trabajo(item.orden_trabajo_numero)
        tipo_interno = _map_tipo_actuacion(item.tipo_actuacion, item)

        actuacion = Actuacion(
            fecha=item.fecha_actuacion,
            tipo=tipo_interno,
            orden_trabajo_id=ot.id,
            # inspector_id, domicilio_id, contribuyente_id, prev_actuacion_id quedan en NULL por ahora
            contraproducencia=item.contraproducencia,
            observaciones=None,
        )
        db.session.add(actuacion)
        db.session.flush()  # para tener actuacion.id

        db.session.commit()
        return actuacion

    except ActuacionServiceError:
        db.session.rollback()
        raise
    except Exception:
        db.session.rollback()
        raise
