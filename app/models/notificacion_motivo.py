from sqlalchemy import UniqueConstraint

from app.database import db


class NotificacionMotivo(db.Model):
    __tablename__ = "notificacion_motivo"

    notificacion_id = db.Column(
        db.Integer,
        db.ForeignKey("notificacion.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    motivo_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "motivo_notificacion.id", ondelete="RESTRICT", onupdate="CASCADE"
        ),
        primary_key=True,
    )

    # si querés guardar el orden (1,2,3) de selección de motivos en el front
    orden = db.Column(db.SmallInteger, nullable=True)

    __table_args__ = (
        UniqueConstraint("notificacion_id", "motivo_id", name="uq_notif_motivo"),
    )

    def to_dict(self):
        return {
            "notificacion_id": self.notificacion_id,
            "motivo_id": self.motivo_id,
            "orden": int(self.orden) if self.orden is not None else None,
        }
