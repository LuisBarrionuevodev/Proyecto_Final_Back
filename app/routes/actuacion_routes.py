# app/routes/actuacion_routes.py

# Ejemplo de payload válido para POST /api/v1/actuaciones
# {
#   "items": [
#     {
#       "orden_trabajo_numero": "000123",
#       "fecha_actuacion": "2024-05-10",
#       "inspectores": ["INSPECTOR UNO", "INSPECTOR DOS"],
#       "calle": "AV SARMIENTO",
#       "numero": "1234",
#       "rubro_nombre": "ALIMENTOS",
#       "tipo_actuacion": "INSPECCION",
#       "contraproducencia": "SIN OBSERVACIONES",
#       "doc_tipo_codigo": "DNI",
#       "doc_nro": "12345678",
#       "contrib_apellido": "PEREZ",
#       "contrib_nombre": "JUAN",
#       "acta_inspeccion_num": "000111",
#       "acta_notificacion_num": "000222",
#       "notificacion_motivo_1": "FALTA DE HIGIENE",
#       "notificacion_motivo_2": "VENTILACION DEFECTUOSA",
#       "notificacion_motivo_3": "OTRO MOTIVO",
#       "acta_comprobacion_num": "000333",
#       "comprobacion_motivo": "INCUMPLIMIENTO PLAZO",
#       "acta_clausura_num": "000444",
#       "clausura_motivo": "RIESGO SANITARIO",
#       "acta_decomiso_num": "000555",
#       "decomiso_kilos_total": 12.5,
#       "expediente_numero": "EXP-2024-001",
#       "expediente_anio": 24,
#       "oficio_numero": "OF-77",
#       "oficio_anio": 24,
#       "oficio_causa": 987,
#       "notificacion_previa_num": "000666",
#       "comprobacion_previa_num": "000777"
#     }
#   ]
# }

from flask import Blueprint, jsonify, request
from pydantic import ValidationError

from app.database import db
from app.models import Actuacion, ActuacionComprobacion, ActuacionNotificacion
from app.schemas.actuacion import ActuacionBatch
from app.services.actuacion_service import (
    ActuacionServiceError,
    crear_actuacion_desde_item,
)

bp = Blueprint("actuaciones", __name__)


def _serializar_actuacion(actuacion: Actuacion) -> dict:
    """Convierte el modelo en un dict listo para el front."""

    inspectores = [
        f"{i.apellido} {i.nombre}".strip() if i.apellido or i.nombre else i.apellido
        for i in actuacion.inspectores
    ]

    est_dom = getattr(actuacion, "establecimiento_domicilio", None)
    domicilio = est_dom.domicilio if est_dom else None
    establecimiento = est_dom.establecimiento if est_dom else None
    contrib = establecimiento.contribuyente if establecimiento else None

    rubro_nombre = None
    if establecimiento and getattr(establecimiento, "establecimiento_rubros", None):
        rubros = establecimiento.establecimiento_rubros
        if rubros:
            rubro_vigente = next((er for er in rubros if er.fecha_hasta is None), None)
            rubro_nombre = (rubro_vigente or rubros[0]).rubro.nombre

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
        "calle": domicilio.calle if domicilio else "",
        "numero": domicilio.numero if domicilio else "",
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
