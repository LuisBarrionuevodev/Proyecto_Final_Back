from sqlalchemy import Index, UniqueConstraint

from app.database import db


class ActaDecomiso(db.Model):
    __tablename__ = "acta_decomiso"

    id = db.Column(db.Integer, primary_key=True)

    numero_acta = db.Column(db.String(6), nullable=False)  # 6 dígitos
    anio = db.Column(db.SmallInteger, nullable=False)

    # cantidad decomisada (usamos decimal para kg/litros/etc.)
    cantidad = db.Column(db.Numeric(12, 3), nullable=False)
    unidad = db.Column(db.String(20), nullable=True)  # opcional: "kg", "l", "u", etc.

    # Relación 0..1 con Actuacion (FK única)
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

    # relaciones
    actuacion = db.relationship(
        "Actuacion",
        back_populates="acta_decomiso",
        passive_deletes=True,
        uselist=False,
    )

    __table_args__ = (
        UniqueConstraint("numero_acta", "anio", name="uq_ad_numero_anio"),
        Index("idx_ad_numero", "numero_acta"),
        Index("idx_ad_anio", "anio"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "numero_acta": self.numero_acta,
            "anio": int(self.anio) if self.anio is not None else None,
            "cantidad": float(self.cantidad) if self.cantidad is not None else None,
            "unidad": self.unidad,
            "actuacion_id": self.actuacion_id,
            "observaciones": self.observaciones,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
