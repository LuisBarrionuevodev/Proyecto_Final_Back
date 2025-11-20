from sqlalchemy import Index, UniqueConstraint
from werkzeug.security import check_password_hash, generate_password_hash

from app.database import db


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(120), nullable=False, unique=True)

    # guardamos el HASH, no la contraseña en claro
    password_hash = db.Column(db.String(255), nullable=False)

    created_at = db.Column(
        db.DateTime, nullable=False, server_default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    __table_args__ = (
        UniqueConstraint("usuario", name="uq_usuario_usuario"),
        Index("idx_usuario_usuario", "usuario"),
    )

    # ---- API de conveniencia ----
    def set_password(self, raw_password: str) -> None:
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)

    def to_dict(self):
        # Nunca exponemos password_hash
        return {
            "id": self.id,
            "usuario": self.usuario,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
