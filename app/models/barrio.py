from sqlalchemy import ForeignKey, Index

from app.database import db


class Barrio(db.Model):
    __tablename__ = "barrio"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), nullable=False)

    distrito_id = db.Column(
        db.Integer,
        ForeignKey("distrito.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )

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
    distrito = db.relationship("Distrito", back_populates="barrios")
    domicilios = db.relationship(
        "Domicilio",
        back_populates="barrio",
        passive_deletes=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "distrito_id": self.distrito_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    __table_args__ = (Index("idx_barrio_distrito", "distrito_id"),)
