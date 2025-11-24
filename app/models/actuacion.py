from sqlalchemy import Index, UniqueConstraint

from app.database import db


class Actuacion(db.Model):
    __tablename__ = "actuacion"

    id = db.Column(db.Integer, primary_key=True)

    fecha = db.Column(db.Date, nullable=False)

    tipo = db.Column(db.String(20), nullable=False)

    orden_trabajo_id = db.Column(
        db.Integer,
        db.ForeignKey("orden_trabajo.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )

    establecimiento_domicilio_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "establecimiento_domicilio.id", ondelete="SET NULL", onupdate="CASCADE"
        ),
        nullable=True,
    )

    contraproducencia = db.Column(db.Text, nullable=True)
    observaciones = db.Column(db.Text, nullable=True)

    created_at = db.Column(
        db.DateTime, nullable=False, server_default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    # Relaciones
    orden_trabajo = db.relationship("OrdenTrabajo", back_populates="actuacion")
    inspectores = db.relationship(
        "Inspector",
        secondary="actuacion_inspector",
        back_populates="actuaciones",
        passive_deletes=True,
    )
    # en app/models/actuacion.py (debajo de inspectores=...)
    actas_comprobacion = db.relationship(
        "ActaComprobacion",
        secondary="actuacion_comprobacion",
        back_populates="actuaciones",
        passive_deletes=True,
    )
    # en app/models/actuacion.py
    actas_notificacion = db.relationship(
        "Notificacion",
        secondary="actuacion_notificacion",
        back_populates="actuaciones",
        passive_deletes=True,
    )
    expediente = db.relationship(
        "Expediente",
        back_populates="actuacion",
        uselist=False,
        passive_deletes=True,
    )
    acta_inspeccion = db.relationship(
        "ActaInspeccion",
        back_populates="actuacion",
        uselist=False,
        passive_deletes=True,
    )
    acta_clausura = db.relationship(
        "ActaClausura",
        back_populates="actuacion",
        uselist=False,
        passive_deletes=True,
    )

    acta_decomiso = db.relationship(
        "ActaDecomiso",
        back_populates="actuacion",
        uselist=False,
        passive_deletes=True,
    )

    __table_args__ = (
        UniqueConstraint("orden_trabajo_id", name="uq_act_ot"),
        Index("idx_act_fecha", "fecha"),
        Index("idx_act_est_dom", "establecimiento_domicilio_id"),
        Index("idx_act_tipo", "tipo"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "tipo": self.tipo,
            "orden_trabajo_id": self.orden_trabajo_id,
            "establecimiento_domicilio_id": self.establecimiento_domicilio_id,
            "contraproducencia": self.contraproducencia,
            "observaciones": self.observaciones,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
