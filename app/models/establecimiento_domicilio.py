# app/models/establecimiento_domicilio.py
from sqlalchemy import ForeignKey, Index, UniqueConstraint

from app.database import db


class EstablecimientoDomicilio(db.Model):
    __tablename__ = "establecimiento_domicilio"

    id = db.Column(db.Integer, primary_key=True)

    establecimiento_id = db.Column(
        db.Integer,
        ForeignKey("establecimiento.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    domicilio_id = db.Column(
        db.Integer,
        ForeignKey("domicilio.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )

    fecha_desde = db.Column(db.Date, nullable=False)
    fecha_hasta = db.Column(db.Date, nullable=True)  # NULL = vigente

    created_at = db.Column(
        db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.TIMESTAMP,
        nullable=False,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    __table_args__ = (
        Index("idx_ed_est", "establecimiento_id"),
        Index("idx_ed_dom", "domicilio_id"),
        Index("idx_ed_vigencia", "fecha_desde", "fecha_hasta"),
        UniqueConstraint(
            "establecimiento_id",
            "domicilio_id",
            "fecha_desde",
            name="uq_ed_est_dom_desde",
        ),
    )

    # Relaciones directas
    establecimiento = db.relationship(
        "Establecimiento", backref="establecimiento_domicilios"
    )
    domicilio = db.relationship("Domicilio", backref="establecimiento_domicilios")

    # --- utilidades ---
    def to_dict(self):
        return {
            "id": self.id,
            "establecimiento_id": self.establecimiento_id,
            "domicilio_id": self.domicilio_id,
            "fecha_desde": self.fecha_desde.isoformat() if self.fecha_desde else None,
            "fecha_hasta": self.fecha_hasta.isoformat() if self.fecha_hasta else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return (
            f"<EstablecimientoDomicilio id={self.id} "
            f"est={self.establecimiento_id} dom={self.domicilio_id} "
            f"desde={self.fecha_desde} hasta={self.fecha_hasta}>"
        )
