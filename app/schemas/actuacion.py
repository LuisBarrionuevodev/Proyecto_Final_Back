from datetime import date, datetime
from typing import List, Optional

from pydantic import (
    BaseModel,
    confloat,
    conint,
    constr,
    field_validator,
    model_validator,
)

from app.utils.normalizers import acta_6, to_upper_trim
from app.utils.validaciones_comunes import (
    validar_no_vacio,
    validar_opcion_en_lista,
)

ActaNumero6 = constr(strip_whitespace=True, min_length=1, max_length=6)
Anio2 = conint(ge=0, le=99)

TipoActuacionStr = constr(strip_whitespace=True, min_length=3, max_length=50)


class ActuacionItem(BaseModel):
    orden_trabajo_numero: ActaNumero6
    fecha_actuacion: date
    inspectores: List[str]

    calle: str
    numero: str
    rubro_nombre: str

    tipo_actuacion: TipoActuacionStr
    contraproducencia: Optional[str] = None

    doc_tipo_codigo: str
    doc_nro: str
    contrib_apellido: Optional[str] = None
    contrib_nombre: Optional[str] = None

    acta_inspeccion_num: Optional[ActaNumero6] = None

    acta_notificacion_num: Optional[ActaNumero6] = None
    notificacion_motivo_1: Optional[str] = None
    notificacion_motivo_2: Optional[str] = None
    notificacion_motivo_3: Optional[str] = None

    acta_comprobacion_num: Optional[ActaNumero6] = None
    comprobacion_motivo: Optional[str] = None

    acta_clausura_num: Optional[ActaNumero6] = None
    clausura_motivo: Optional[str] = None

    acta_decomiso_num: Optional[ActaNumero6] = None
    decomiso_kilos_total: Optional[confloat(gt=0)] = None

    expediente_numero: Optional[str] = None
    expediente_anio: Optional[Anio2] = None

    oficio_numero: Optional[str] = None
    oficio_anio: Optional[Anio2] = None
    oficio_causa: Optional[int] = None

    notificacion_previa_num: Optional[ActaNumero6] = None
    comprobacion_previa_num: Optional[ActaNumero6] = None

    @field_validator(
        "orden_trabajo_numero",
        "calle",
        "rubro_nombre",
        "doc_tipo_codigo",
        "doc_nro",
        "contrib_apellido",
        mode="before",
    )
    @classmethod
    def _strip_upper_noempty(cls, v, info):
        campo = info.field_name
        s = to_upper_trim(v)
        validar_no_vacio(s, campo)
        return s
    @field_validator("fecha_actuacion", mode="before")
    @classmethod
    def _parse_fecha(cls, v):
        """
        Acepta:
        - date (ya parseado)
        - strings tipo 'DD/MM/AA', 'DD/MM/AAAA' o 'YYYY-MM-DD'
        """
        if isinstance(v, date):
            return v
        if v is None:
            raise ValueError("fecha_actuacion es obligatoria")

        s = str(v).strip()
        for fmt in ("%d/%m/%y", "%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(s, fmt).date()
            except ValueError:
                continue

        raise ValueError("fecha_actuacion debe tener formato DD/MM/AA")


    @field_validator("contrib_nombre", mode="before")
    @classmethod
    def _strip_upper_optional(cls, v):
        if v is not None:
            return to_upper_trim(v)
        else:
            return None

    @field_validator("numero", mode="before")
    @classmethod
    def _numero_calle(cls, v):
        if v is not None:
            return str(v).strip()
        else:
            return " "

    @field_validator("inspectores", mode="before")
    @classmethod
    def _inspectores_list(cls, v):
        """
        Aseguramos que inspectores sea lista de 1 a 4 strings,
        normalizados y sin vacíos.
        """
        if v is None:
            raise ValueError("Debe indicar al menos un inspector")

        if isinstance(v, str):
            items = [i.strip() for i in v.split(",") if i.strip()]
        else:
            items = [str(i).strip() for i in v if str(i).strip()]

        if not (1 <= len(items) <= 4):
            raise ValueError("inspectores debe tener entre 1 y 4 nombres/apellidos")

        return [to_upper_trim(i) for i in items]

    @field_validator("tipo_actuacion", mode="before")
    @classmethod
    def _tipo_actuacion_val(cls, v):
        s = to_upper_trim(v)
        opciones = [
            "INSPECCION",
            "REINSPECCION",
            "RATIFICACION",
            "VERIFICAR E INFORMAR",
        ]
        validar_opcion_en_lista(s, opciones, "tipo_actuacion")
        return s

    # --- Actas: normalizar a 6 dígitos si vienen ---

    @field_validator(
        "acta_inspeccion_num",
        "acta_notificacion_num",
        "acta_comprobacion_num",
        "acta_clausura_num",
        "acta_decomiso_num",
        "notificacion_previa_num",
        "comprobacion_previa_num",
        mode="before",
    )
    @classmethod
    def _norm_acta_6(cls, v):
        if v in (None, "", " "):
            return None
        return acta_6(v)

    # ================== VALIDADOR A NIVEL MODELO ==================

    @model_validator(mode="after")
    def _reglas_cruzadas_basicas(self):
        """
        Reglas entre campos (versión simple por ahora).

        Más adelante acá podemos poner cosas como:
        - Si tipo_actuacion == REINSPECCION -> exigir acta_notificacion_num o acta_comprobacion_num (previa)
        - Si viene decomiso_kilos_total -> debe venir acta_decomiso_num
        - etc.
        """
        # Ejemplo sencillo: si hay decomiso_kilos_total, debe haber acta_decomiso_num
        if self.decomiso_kilos_total is not None and self.acta_decomiso_num is None:
            raise ValueError(
                "Si se informa 'decomiso_kilos_total' debe informarse 'acta_decomiso_num'."
            )

        return self


class ActuacionBatch(BaseModel):
    """
    Payload completo:
    {
      "items": [ { ...fila1... }, { ...fila2... }, ... ]
    }
    """

    items: List[ActuacionItem]

    @model_validator(mode="after")
    def _no_items_vacia(self):
        if not self.items:
            raise ValueError("Debe enviar al menos una actuación en 'items'")
        return self
