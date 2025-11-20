from sqlalchemy import Index, UniqueConstraint

from app.database import db


class ActaComprobacion(db.Model):
    __tablename__ = "acta_comprobacion"

    id = db.Column(db.Integer, primary_key=True)
    numero_acta = db.Column(db.String(6), nullable=False)
    anio = db.Column(db.SmallInteger, nullable=False)

    # artículo aplicable (si luego necesitás varios, migraremos a tabla puente)
    articulo_id = db.Column(
        db.Integer,
        db.ForeignKey("articulo.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )

    # flag denormalizado, lo actualiza el service cuando detecta 2+ vínculos
    actuada_dos_veces = db.Column(
        db.Boolean, nullable=False, server_default=db.text("0")
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
    articulo = db.relationship("Articulo", back_populates="actas_comprobacion")
    actuaciones = db.relationship(
        "Actuacion",
        secondary="actuacion_comprobacion",
        back_populates="actas_comprobacion",
        passive_deletes=True,
    )

    __table_args__ = (
        UniqueConstraint("numero_acta", "anio", name="uq_acp_numero_anio"),
        Index("idx_acp_articulo", "articulo_id"),
        Index("idx_acp_flags", "actuada_dos_veces"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "numero_acta": self.numero_acta,
            "anio": int(self.anio) if self.anio is not None else None,
            "articulo_id": self.articulo_id,
            "actuada_dos_veces": bool(self.actuada_dos_veces),
            "observaciones": self.observaciones,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
