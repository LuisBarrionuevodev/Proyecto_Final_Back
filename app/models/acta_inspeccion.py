from sqlalchemy import Index, UniqueConstraint

from app.database import db


class ActaInspeccion(db.Model):
    __tablename__ = "acta_inspeccion"

    id = db.Column(db.Integer, primary_key=True)

    numero_acta = db.Column(db.String(6), nullable=False)
    anio = db.Column(db.SmallInteger, nullable=False)

    observaciones = db.Column(db.Text, nullable=True)

    actuacion_id = db.Column(
        db.Integer,
        db.ForeignKey("actuacion.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        unique=True,
    )

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
    actuacion = db.relationship(
        "Actuacion",
        back_populates="acta_inspeccion",
        passive_deletes=True,
        uselist=False,
    )

    __table_args__ = (
        UniqueConstraint("numero_acta", "anio", name="uq_ai_numero_anio"),
        Index("idx_ai_numero", "numero_acta"),
        Index("idx_ai_anio", "anio"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "numero_acta": self.numero_acta,
            "anio": int(self.anio) if self.anio is not None else None,
            "actuacion_id": self.actuacion_id,
            "observaciones": self.observaciones,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
