from sqlalchemy import Index, UniqueConstraint

from app.database import db


class Articulo(db.Model):
    __tablename__ = "articulo"

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), nullable=False)  # admite "12 bis", etc.
    descripcion = db.Column(db.Text, nullable=False)

    created_at = db.Column(
        db.DateTime, nullable=False, server_default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    # relaciones
    actas_comprobacion = db.relationship("ActaComprobacion", back_populates="articulo")

    __table_args__ = (
        UniqueConstraint("numero", name="uq_articulo_numero"),
        Index("idx_art_numero", "numero"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "numero": self.numero,
            "descripcion": self.descripcion,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
