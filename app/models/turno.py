from sqlalchemy import Index

from app.database import db


class Turno(db.Model):
    __tablename__ = "turno"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), nullable=False, unique=True)
    hora_desde = db.Column(db.Time, nullable=False)
    hora_hasta = db.Column(db.Time, nullable=False)

    created_at = db.Column(
        db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.TIMESTAMP,
        nullable=False,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    __table_args__ = (Index("idx_turno_horas", "hora_desde", "hora_hasta"),)

    inspectores = db.relationship(
        "Inspector", back_populates="turno", passive_deletes=True
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "hora_desde": self.hora_desde.isoformat() if self.hora_desde else None,
            "hora_hasta": self.hora_hasta.isoformat() if self.hora_hasta else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<Turno id={self.id} nombre={self.nombre!r}>"
