from sqlalchemy import Index, UniqueConstraint

from app.database import db


class MotivoNotificacion(db.Model):
    __tablename__ = "motivo_notificacion"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)

    created_at = db.Column(
        db.DateTime, nullable=False, server_default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    # relaciones inversas
    notificaciones = db.relationship(
        "Notificacion",
        secondary="notificacion_motivo",
        back_populates="motivos",
        passive_deletes=True,
    )

    __table_args__ = (
        UniqueConstraint("nombre", name="uq_motivo_notif_nombre"),
        Index("idx_motivo_notif_nombre", "nombre"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
