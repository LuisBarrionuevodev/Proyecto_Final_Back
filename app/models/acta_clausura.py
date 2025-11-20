from sqlalchemy import Index, UniqueConstraint

from app.database import db


class ActaClausura(db.Model):
    __tablename__ = "acta_clausura"

    id = db.Column(db.Integer, primary_key=True)

    numero_acta = db.Column(
        db.String(6), nullable=False
    )  # 6 dígitos (string para ceros a izq.)
    anio = db.Column(db.SmallInteger, nullable=False)

    # Relación 0..1 con Actuacion (FK única)
    actuacion_id = db.Column(
        db.Integer,
        db.ForeignKey("actuacion.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        unique=True,
    )

    # Catálogo: un (1) motivo por clausura (FK en la tabla clausura, como pediste)
    motivo_id = db.Column(
        db.Integer,
        db.ForeignKey("motivo_clausura.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
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

    # relaciones
    actuacion = db.relationship(
        "Actuacion",
        back_populates="acta_clausura",
        passive_deletes=True,
        uselist=False,
    )
    motivo = db.relationship("MotivoClausura")

    __table_args__ = (
        UniqueConstraint("numero_acta", "anio", name="uq_ac_numero_anio"),
        Index("idx_ac_numero", "numero_acta"),
        Index("idx_ac_anio", "anio"),
        Index("idx_ac_motivo", "motivo_id"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "numero_acta": self.numero_acta,
            "anio": int(self.anio) if self.anio is not None else None,
            "actuacion_id": self.actuacion_id,
            "motivo_id": self.motivo_id,
            "observaciones": self.observaciones,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
