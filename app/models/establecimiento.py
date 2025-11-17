# app/models/establecimiento.py

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app.database import db


class Establecimiento(db.Model):
    __tablename__ = "establecimiento"

    id = db.Column(db.Integer, primary_key=True)

    contribuyente_id = db.Column(
        db.Integer,
        ForeignKey("contribuyente.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )
    nombre = db.Column(db.String(200), nullable=False)

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
    contribuyente = relationship("Contribuyente", back_populates="establecimientos")

    domicilios = relationship(
        "EstablecimientoDomicilio",
        back_populates="establecimiento",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Establecimiento id={self.id} nombre={self.nombre!r}>"
