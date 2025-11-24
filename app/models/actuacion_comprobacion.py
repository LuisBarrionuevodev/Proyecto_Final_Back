from app.database import db


class ActuacionComprobacion(db.Model):
    __tablename__ = "actuacion_comprobacion"

    actuacion_id = db.Column(
        db.Integer,
        db.ForeignKey("actuacion.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    acta_comprobacion_id = db.Column(
        db.Integer,
        db.ForeignKey("acta_comprobacion.id", ondelete="RESTRICT", onupdate="CASCADE"),
        primary_key=True,
    )

    # contexto de esta asociación: INSPECCION / REINSPECCION / RATIF_* / VERIF_INFORMAR
    contexto = db.Column(db.String(20), nullable=True)

    def to_dict(self):
        return {
            "actuacion_id": self.actuacion_id,
            "acta_comprobacion_id": self.acta_comprobacion_id,
            "contexto": self.contexto,
        }
