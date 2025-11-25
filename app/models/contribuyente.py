from sqlalchemy import ForeignKey, Index, func, text

from app.database import db


class Contribuyente(db.Model):
    __tablename__ = "contribuyente"

    id = db.Column(db.Integer, primary_key=True)
    apellido = db.Column(db.String(128), nullable=False)
    nombre = db.Column(db.String(128), nullable=False)

    doc_tipo_id = db.Column(
        db.Integer,
        ForeignKey("documento_tipo.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )
    genero_id = db.Column(
        db.Integer,
        ForeignKey("genero.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True,
    )
    doc_nro = db.Column(db.String(20), nullable=True)

    telefono = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(128), nullable=True)

    activo = db.Column(db.Boolean, nullable=False, server_default=text("1"))
    created_at = db.Column(
        db.TIMESTAMP, nullable=False, server_default=func.current_timestamp()
    )
    updated_at = db.Column(
        db.TIMESTAMP,
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    doc_tipo = db.relationship("DocumentoTipo", lazy="joined", passive_deletes=True)
    genero = db.relationship("Genero", lazy="joined", passive_deletes=True)

    # 🔁 NUEVO: 1 contribuyente → N domicilios
    domicilios = db.relationship(
        "Domicilio",
        back_populates="contribuyente",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    # ❌ ANTES: establecimientos = ...
    # Esa relación ya no se usa con el nuevo modelo.

    def __repr__(self):
        return f"<Contribuyente id={self.id} {self.apellido}, {self.nombre}>"

    def to_dict(self):
        return {
            "id": self.id,
            "apellido": self.apellido,
            "nombre": self.nombre,
            "doc_tipo_id": self.doc_tipo_id,
            "doc_tipo_codigo": self.doc_tipo.codigo if self.doc_tipo else None,
            "genero_id": self.genero_id,
            "genero_codigo": self.genero.codigo if self.genero else None,
            "doc_nro": self.doc_nro,
            "telefono": self.telefono,
            "email": self.email,
            "activo": bool(self.activo),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    __table_args__ = (
        db.UniqueConstraint("doc_tipo_id", "doc_nro", name="uq_contrib_doc"),
        Index("idx_contrib_apellido_nombre", "apellido", "nombre"),
        Index("idx_contrib_doc_std", "doc_tipo_id", "doc_nro"),
    )
