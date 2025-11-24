from sqlalchemy import Index

from app.database import db


class OrdenTrabajo(db.Model):
    __tablename__ = "orden_trabajo"

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(6), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)

    created_at = db.Column(
        db.DateTime, nullable=False, server_default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    actuacion = db.relationship(
        "Actuacion",
        back_populates="orden_trabajo",
        uselist=False,
        passive_deletes=True,
    )

    __table_args__ = (Index("idx_ot_numero", "numero"),)

    def to_dict(self):
        return {
            "id": self.id,
            "numero": self.numero,
            "descripcion": self.descripcion,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
