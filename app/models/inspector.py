# app/models/inspector.py
from sqlalchemy import ForeignKey, Index

from app.database import db


class Inspector(db.Model):
    __tablename__ = "inspector"

    id = db.Column(db.Integer, primary_key=True)

    # si tu legajo es numérico podés usar Integer, acá lo dejamos como string flexible
    legajo = db.Column(db.Integer, nullable=False, unique=True)

    apellido = db.Column(db.String(128), nullable=False)
    nombre = db.Column(db.String(128), nullable=False)

    turno_id = db.Column(
        db.Integer,
        ForeignKey("turno.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )

    email = db.Column(db.String(150))
    telefono = db.Column(db.String(50))

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
        Index("idx_inspector_apellido", "apellido"),
        Index("idx_inspector_turno", "turno_id"),
        Index("idx_inspector_apynom", "apellido", "nombre"),
    )

    turno = db.relationship("Turno", back_populates="inspectores")
    # en app/models/inspector.py
    actuaciones = db.relationship(
        "Actuacion",
        secondary="actuacion_inspector",
        back_populates="inspectores",
        passive_deletes=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "legajo": self.legajo,
            "apellido": self.apellido,
            "nombre": self.nombre,
            "turno_id": self.turno_id,
            "email": self.email,
            "telefono": self.telefono,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return (
            f"<Inspector id={self.id} legajo={self.legajo!r} "
            f"apynom={self.apellido!r}, {self.nombre!r}>"
        )
