from sqlalchemy import Index, UniqueConstraint

from app.database import db


class Notificacion(db.Model):
    __tablename__ = "notificacion"

    id = db.Column(db.Integer, primary_key=True)
    numero_acta = db.Column(db.String(6), nullable=False)
    anio = db.Column(db.SmallInteger, nullable=False)

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

    # relaciones
    motivos = db.relationship(
        "MotivoNotificacion",
        secondary="notificacion_motivo",
        back_populates="notificaciones",
        passive_deletes=True,
    )

    actuaciones = db.relationship(
        "Actuacion",
        secondary="actuacion_notificacion",
        back_populates="actas_notificacion",
        passive_deletes=True,
    )

    __table_args__ = (
        UniqueConstraint("numero_acta", "anio", name="uq_an_numero_anio"),
        Index("idx_an_numero", "numero_acta"),
        Index("idx_an_anio", "anio"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "numero_acta": self.numero_acta,
            "anio": int(self.anio) if self.anio is not None else None,
            "observaciones": self.observaciones,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
