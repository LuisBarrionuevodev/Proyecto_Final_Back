# app/models/establecimiento.py
from sqlalchemy import ForeignKey, Index

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
        db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.TIMESTAMP,
        nullable=False,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    __table_args__ = (
        Index("idx_est_contrib", "contribuyente_id"),
        Index("idx_est_nombre", "nombre"),
    )

    contribuyente = db.relationship("Contribuyente", back_populates="establecimientos")
    domicilios = db.relationship(
        "Domicilio",
        secondary="establecimiento_domicilio",
        back_populates="establecimientos",
        viewonly=True,
    )
    rubros = db.relationship(
        "Rubro",
        secondary="establecimiento_rubro",
        back_populates="establecimientos",
        viewonly=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "contribuyente_id": self.contribuyente_id,
            "nombre": self.nombre,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<Establecimiento id={self.id} nombre={self.nombre!r}>"
