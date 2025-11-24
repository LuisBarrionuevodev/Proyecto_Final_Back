from sqlalchemy import Index, UniqueConstraint

from app.database import db


class Expediente(db.Model):
    __tablename__ = "expediente"

    id = db.Column(db.Integer, primary_key=True)

    numero_expediente = db.Column(db.String(30), nullable=False)

    anio = db.Column(db.SmallInteger, nullable=False)

    actuacion_id = db.Column(
        db.Integer,
        db.ForeignKey("actuacion.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        unique=True,
    )

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
    actuacion = db.relationship(
        "Actuacion",
        back_populates="expediente",
        passive_deletes=True,
        uselist=False,  # <-- 1:1 del lado de Actuacion
    )

    __table_args__ = (
        UniqueConstraint("numero_expediente", "anio", name="uq_exp_numero_anio"),
        Index("idx_exp_numero", "numero_expediente"),
        Index("idx_exp_anio", "anio"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "numero_expediente": self.numero_expediente,
            "anio": int(self.anio) if self.anio is not None else None,
            "actuacion_id": self.actuacion_id,
            "observaciones": self.observaciones,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
