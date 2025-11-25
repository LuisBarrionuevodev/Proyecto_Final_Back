from app.database import db


class RelevamientoSimple(db.Model):
    __tablename__ = "relevamiento_simple"

    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    inspector = db.Column(db.String(150), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    rubro = db.Column(db.String(150), nullable=False)

    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "fecha": self.fecha.isoformat(),
            "inspector": self.inspector,
            "direccion": self.direccion,
            "rubro": self.rubro,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
