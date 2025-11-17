# app/models/establecimiento_domicilio.py

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

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
    fecha_hasta = db.Column(db.Date, nullable=True)

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
    establecimiento = relationship(
        "Establecimiento",
        back_populates="domicilios",
    )
    domicilio = relationship(
        "Domicilio",
        back_populates="establecimientos",
    )

    def __repr__(self) -> str:
        return (
            f"<EstablecimientoDomicilio id={self.id} "
            f"est={self.establecimiento_id} dom={self.domicilio_id}>"
        )
