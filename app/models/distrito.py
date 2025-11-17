# app/models/distrito.py

from sqlalchemy.orm import relationship

from app.database import db


class Distrito(db.Model):
    __tablename__ = "distrito"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(128), nullable=False, unique=True)

    created_at = db.Column(
        db.TIMESTAMP,
        server_default=db.func.current_timestamp(),
        nullable=False,
    )
    updated_at = db.Column(
        db.TIMESTAMP,
        server_default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
        nullable=False,
    )

    # 👇 relación 1–N con Barrio (si la tenés)
    barrios = relationship("Barrio", back_populates="distrito")

    # 👇 ESTA ES LA CLAVE PARA EL ERROR ACTUAL
    domicilios = relationship(
        "Domicilio",
        back_populates="distrito",
    )

    def __repr__(self) -> str:
        return f"<Distrito id={self.id} nombre={self.nombre!r}>"
