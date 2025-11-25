from sqlalchemy import Index, func, text

from app.database import db


class Rubro(db.Model):
    __tablename__ = "rubro"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), nullable=False, unique=True)
    activo = db.Column(db.Boolean, nullable=False, server_default=text("1"))
    created_at = db.Column(
        db.TIMESTAMP, nullable=False, server_default=func.current_timestamp()
    )
    updated_at = db.Column(
        db.TIMESTAMP,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    # 🔁 NUEVO: 1 rubro → N domicilios
    domicilios = db.relationship(
        "Domicilio",
        back_populates="rubro",
        lazy="selectin",
    )

    def __repr__(self):
        return f"<Rubro id={self.id} nombre={self.nombre!r} activo={self.activo}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "activo": bool(self.activo),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


Index("idx_rubro_nombre", Rubro.nombre)
Index("idx_rubro_activo", Rubro.activo)
