from datetime import date, datetime

from pydantic import BaseModel, field_validator


class RelevamientoSimpleCreate(BaseModel):
    fecha: str  # el front envía "YYYY-MM-DD"
    inspector: str  # texto simple
    direccion: str  # texto simple
    rubro: str  # texto simple

    @field_validator("fecha", mode="before")
    @classmethod
    def parse_fecha(cls, v):
        """
        Permite:
        - string "YYYY-MM-DD"
        - objetos datetime.date
        - objetos datetime.datetime
        Convierte SIEMPRE a string "YYYY-MM-DD"
        """
        if isinstance(v, date):
            return v.strftime("%Y-%m-%d")

        if isinstance(v, datetime):
            return v.date().strftime("%Y-%m-%d")

        if isinstance(v, str):
            s = v.strip()
            try:
                # verifica formato
                dt = datetime.strptime(s, "%Y-%m-%d")
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                raise ValueError("Formato de fecha inválido (usar YYYY-MM-DD)")

        raise ValueError("Fecha inválida")

    @field_validator("inspector", "direccion", "rubro", mode="before")
    @classmethod
    def no_vacio(cls, v):
        """
        Todos estos campos son obligatorios.
        Se asegura de que no vengan vacíos o null.
        """
        if v is None:
            raise ValueError("Campo requerido")
        s = str(v).strip()
        if not s:
            raise ValueError("Campo requerido")
        return s
