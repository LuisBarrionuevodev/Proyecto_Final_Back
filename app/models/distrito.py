from app.database import db


class Distrito(db.Model):
    __tablename__ = "distrito"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), nullable=False)

    # Polígono en WKT (texto). Ej: "POLYGON((lon lat, lon lat, ...))"
    geom_wkt = db.Column(db.Text, nullable=True)

    created_at = db.Column(
        db.TIMESTAMP, nullable=False, server_default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.TIMESTAMP,
        nullable=False,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    # Relaciones
    barrios = db.relationship(
        "Barrio",
        back_populates="distrito",
        passive_deletes=True,  # respetar ondelete en DB
    )


def to_dict(self):
    return {
        "id": self.id,
        "nombre": self.nombre,
        "geom_wkt": self.geom_wkt,
        "created_at": self.created_at.isoformat() if self.created_at else None,
        "updated_at": self.updated_at.isoformat() if self.updated_at else None,
    }
