# app/models/domicilio.py

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app.database import db


class Domicilio(db.Model):
    __tablename__ = "domicilio"

    id = db.Column(db.Integer, primary_key=True)

    calle = db.Column(db.String(128), nullable=False)
    numero = db.Column(db.String(20), nullable=True)
    local = db.Column(db.String(128), nullable=True)
    cp = db.Column(db.String(10), nullable=True)

    barrio_id = db.Column(
        db.Integer,
        ForeignKey("barrio.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )

    distrito_id = db.Column(
        db.Integer,
        ForeignKey("distrito.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )

    lat = db.Column(db.Numeric(9, 6), nullable=True)
    lon = db.Column(db.Numeric(9, 6), nullable=True)

    created_at = db.Column(
        db.TIMESTAMP,
        server_default=db.func.current_timestamp(),
        nullable=False,
    )
    updated_at = db.Column(
        db.TIMESTAMP,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
        nullable=False,
    )

    # relaciones
    barrio = relationship("Barrio", back_populates="domicilios")
    distrito = relationship("Distrito", back_populates="domicilios")
    relevamiento = db.relationship("Relevamiento", back_populates="domicilio",)
    # 👇 relación con la tabla puente establecimiento_domicilio
    establecimientos = relationship(
        "EstablecimientoDomicilio",
        back_populates="domicilio",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Domicilio id={self.id} calle={self.calle!r} numero={self.numero!r}>"
