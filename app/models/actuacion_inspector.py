from app.database import db


class ActuacionInspector(db.Model):
    __tablename__ = "actuacion_inspector"

    actuacion_id = db.Column(
        db.Integer,
        db.ForeignKey("actuacion.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True,
    )
    inspector_id = db.Column(
        db.Integer,
        db.ForeignKey("inspector.id", ondelete="RESTRICT", onupdate="CASCADE"),
        primary_key=True,
    )

    rol = db.Column(db.String(20), nullable=True)  # RESPONSABLE / APOYO (opcional)
    asignado_en = db.Column(
        db.DateTime, nullable=False, server_default=db.func.current_timestamp()
    )

    # Relaciones inversas declaradas en Actuacion e Inspector (back_populates)
    actuacion = db.relationship(
        "Actuacion", backref=db.backref("actuacion_inspectores", passive_deletes=True)
    )
    inspector = db.relationship(
        "Inspector", backref=db.backref("actuacion_inspectores", passive_deletes=True)
    )

    def to_dict(self):
        return {
            "actuacion_id": self.actuacion_id,
            "inspector_id": self.inspector_id,
            "rol": self.rol,
            "asignado_en": self.asignado_en.isoformat() if self.asignado_en else None,
        }
