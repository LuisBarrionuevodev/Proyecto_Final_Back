from sqlalchemy import Index

from app.database import db


class Oficio(db.Model):
    __tablename__ = "oficio"

    id = db.Column(db.Integer, primary_key=True)

    numero_oficio = db.Column(db.String(30), nullable=False)
    anio = db.Column(db.SmallInteger, nullable=False)  # sin fecha, solo año

    causa = db.Column(
        db.Integer, nullable=True
    )  # si luego puede tener letras, cambia a String

    acta_comprobacion_id = db.Column(
        db.Integer,
        db.ForeignKey("acta_comprobacion.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False,
    )

    observaciones = db.Column(db.Text, nullable=True)

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
    acta_comprobacion = db.relationship(
        "ActaComprobacion", backref=db.backref("oficios", passive_deletes=True)
    )

    __table_args__ = (
        # activa si sabés que es único globalmente
        # UniqueConstraint("numero_oficio", "anio", name="uq_ofi_num_anio"),
        Index("idx_ofi_acta", "acta_comprobacion_id"),
        Index("idx_ofi_num", "numero_oficio"),
        Index("idx_ofi_anio", "anio"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "numero_oficio": self.numero_oficio,
            "anio": int(self.anio) if self.anio is not None else None,
            "causa": self.causa,
            "acta_comprobacion_id": self.acta_comprobacion_id,
            "observaciones": self.observaciones,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
