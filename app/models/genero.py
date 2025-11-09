from sqlalchemy import func, text

from app.database import db


class Genero(db.Model):
    __tablename__ = "genero"

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(10), nullable=False, unique=True)
    nombre = db.Column(db.String(50), nullable=False)
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

    def __repr__(self) -> str:
        return f"<Genero id={self.id} codigo={self.codigo!r}>"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "activo": bool(self.activo),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
