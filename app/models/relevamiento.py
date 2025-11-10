from sqlalchemy import UniqueConstraint

from app.database import db


class Relevamiento(db.Model):
    __tablename__ = "relevamiento"

    id = db.Column(db.Integer, primary_key=True)

    domicilio_id = db.Column(
        db.Integer,
        db.ForeignKey("domicilio.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        unique=True,  # 1:1 -> cada domicilio puede tener a lo sumo un relevamiento
    )
    rubro_id = db.Column(
        db.Integer,
        db.ForeignKey("rubro.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
        unique=True,  # 1:1 -> cada rubro puede tener a lo sumo un relevamiento
    )

    created_at = db.Column(
        db.DateTime, nullable=False, server_default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    # Relaciones 1:1 (lado inverso marcado con uselist=False)
    domicilio = db.relationship(
        "Domicilio", back_populates="relevamiento", uselist=False
    )
    rubro = db.relationship("Rubro", back_populates="relevamiento", uselist=False)

    # (opcional) si quisieras además impedir duplicidad por la combinación:
    __table_args__ = (
        UniqueConstraint("domicilio_id", "rubro_id", name="uq_rel_dom_rubro"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "domicilio_id": self.domicilio_id,
            "rubro_id": self.rubro_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
