from app.database import db


class ActuacionNotificacion(db.Model):
    __tablename__ = "actuacion_notificacion"

    actuacion_id = db.Column(
        db.Integer,
        db.ForeignKey("actuacion.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    notificacion_id = db.Column(
        db.Integer,
        db.ForeignKey("notificacion.id", ondelete="RESTRICT", onupdate="CASCADE"),
        primary_key=True,
    )

    # contexto: INSPECCION / REINSPECCION / RATIF_* / VERIF_INFORMAR
    contexto = db.Column(db.String(20), nullable=True)

    def to_dict(self):
        return {
            "actuacion_id": self.actuacion_id,
            "notificacion_id": self.notificacion_id,
            "contexto": self.contexto,
        }
