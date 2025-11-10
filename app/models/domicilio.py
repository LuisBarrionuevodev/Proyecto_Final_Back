from sqlalchemy import ForeignKey, Index

from app.database import db


class Domicilio(db.Model):
    __tablename__ = "domicilio"

    id = db.Column(db.Integer, primary_key=True)

    calle = db.Column(db.String(128), nullable=False)
    numero = db.Column(db.String(20), nullable=True)
    local = db.Column(db.String(128), nullable=True)
    cp = db.Column(db.String(10), nullable=True)

    barrio_id = db.Column(
        db.Integer,
        ForeignKey("barrio.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )
    # opcional directo a distrito (mientras falten barrios cargados)
    distrito_id = db.Column(
        db.Integer,
        ForeignKey("distrito.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )

    lat = db.Column(db.Numeric(9, 6), nullable=True)
    lon = db.Column(db.Numeric(9, 6), nullable=True)

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
    barrio = db.relationship("Barrio", back_populates="domicilios")
    distrito = db.relationship("Distrito")
    relevamiento = db.relationship(
        "Relevamiento",
        back_populates="domicilio",
        uselist=False,  # 1:1
        passive_deletes=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "calle": self.calle,
            "numero": self.numero,
            "local": self.local,
            "cp": self.cp,
            "barrio_id": self.barrio_id,
            "distrito_id": self.distrito_id,
            "lat": float(self.lat) if self.lat is not None else None,
            "lon": float(self.lon) if self.lon is not None else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    __table_args__ = (
        Index("idx_dom_barrio", "barrio_id"),
        Index("idx_dom_distrito", "distrito_id"),
        Index("idx_dom_cp", "cp"),
        Index("idx_dom_busqueda", "calle", "numero"),
        Index("idx_dom_geo", "lat", "lon"),
    )
