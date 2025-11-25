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

# -------------------------
#  Tipos básicos reutilizables
# -------------------------

ActaNumero6 = constr(strip_whitespace=True, min_length=1, max_length=6)
Anio2 = conint(ge=0, le=99)
TipoActuacionStr = constr(strip_whitespace=True, min_length=3, max_length=50)


# ==========================
#   ALTA DE ACTUACIONES (ITEM)
# ==========================


class ActuacionItem(BaseModel):
    # ---- Datos base de la actuación ----
    orden_trabajo_numero: ActaNumero6
    fecha_actuacion: date
    inspectores: List[str]

    # ---- Domicilio comercial ----
    calle: str
    numero: str
    rubro_nombre: str

    # ---- Tipo y contraproducencia ----
    tipo_actuacion: TipoActuacionStr
    contraproducencia: Optional[str] = None

    # ---- Contribuyente ----
    doc_tipo_codigo: str
    doc_nro: str
    contrib_apellido: Optional[str] = None
    contrib_nombre: Optional[str] = None

    # ---- Acta de inspección ----
    acta_inspeccion_num: Optional[ActaNumero6] = None

    # ---- Notificación del día ----
    acta_notificacion_num: Optional[ActaNumero6] = None
    notificacion_motivo_1: Optional[str] = None
    notificacion_motivo_2: Optional[str] = None
    notificacion_motivo_3: Optional[str] = None

    # ---- Comprobación (día) ----
    acta_comprobacion_num: Optional[ActaNumero6] = None
    comprobacion_motivo: Optional[str] = None

    # ---- Clausura ----
    acta_clausura_num: Optional[ActaNumero6] = None
    clausura_motivo: Optional[str] = None

    # ---- Decomiso ----
    acta_decomiso_num: Optional[ActaNumero6] = None
    decomiso_kilos_total: Optional[confloat(gt=0)] = None

    # ---- Expediente ----
    expediente_numero: Optional[str] = None
    expediente_anio: Optional[Anio2] = None

    # ---- Oficio (ligado a comprobación) ----
    oficio_numero: Optional[str] = None
    oficio_anio: Optional[Anio2] = None
    oficio_causa: Optional[int] = None

    # ---- Actas previas (reinspección / ratificación / verificar) ----
    notificacion_previa_num: Optional[ActaNumero6] = None
    comprobacion_previa_num: Optional[ActaNumero6] = None

    # -------------------------
    #  VALIDADORES POR CAMPO
    # -------------------------

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
        """
        Normaliza a MAYÚSCULAS + trim y exige que no esté vacío.
        Aplica a:
          - orden_trabajo_numero
          - calle
          - rubro_nombre
          - doc_tipo_codigo
          - doc_nro
          - contrib_apellido
        """
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
        """Normaliza contrib_nombre si viene; si no, lo deja en None."""
        if v is not None:
            return to_upper_trim(v)
        return None

    @field_validator("numero", mode="before")
    @classmethod
    def _numero_calle(cls, v):
        """
        Número de calle: lo forzamos a string con trim.
        Si viene None, lo dejamos como string vacío (la BD lo trata aparte).
        """
        if v is not None:
            return str(v).strip()
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
        """
        Normaliza tipo_actuacion y valida que esté dentro del set permitido.
        """
        s = to_upper_trim(v)
        opciones = [
            "INSPECCION",
            "REINSPECCION",
            "RATIFICACION",
            "VERIFICAR E INFORMAR",
        ]
        validar_opcion_en_lista(s, opciones, "tipo_actuacion")
        return s

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
        """
        Normaliza todos los números de acta:
        - Acepta int/str/None.
        - Devuelve None si viene vacío.
        - Usa acta_6 para zfill(6) si es numérico.
        """
        if v in (None, "", " "):
            return None
        return acta_6(v)

    # -------------------------
    #  REGLAS CRUZADAS
    # -------------------------

    @model_validator(mode="after")
    def _reglas_cruzadas_basicas(self):
        """
        Reglas simples entre campos.

        Ejemplo: si viene decomiso_kilos_total -> debe venir acta_decomiso_num.
        (Se puede ampliar más adelante según negocio.)
        """
        if self.decomiso_kilos_total is not None and self.acta_decomiso_num is None:
            raise ValueError(
                "Si se informa 'decomiso_kilos_total' debe informarse 'acta_decomiso_num'."
            )

        return self


# ==========================
#   BATCH DE ACTUACIONES
# ==========================


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


# ==========================
#   UPDATE DE ACTUACIÓN
# ==========================


class ActuacionUpdate(BaseModel):
    """
    Modelo para PUT /api/v1/actuaciones/<id>

    Todos los campos son opcionales:
      - si vienen en el JSON, se intentan aplicar;
      - si no vienen, se dejan como están.
    """

    fecha_actuacion: Optional[date] = None
    tipo_actuacion: Optional[TipoActuacionStr] = None
    orden_trabajo_numero: Optional[ActaNumero6] = None

    # 👇 Nuevo modelo: la actuación apunta directo a domicilio_id
    domicilio_id: Optional[int] = None

    contraproducencia: Optional[str] = None
    inspectores: Optional[List[str]] = None

    @field_validator("fecha_actuacion", mode="before")
    @classmethod
    def _parse_fecha(cls, v):
        """
        Igual lógica que en ActuacionItem, pero permitiendo None.
        """
        if v is None:
            return None
        if isinstance(v, date):
            return v

        s = str(v).strip()
        for fmt in ("%d/%m/%y", "%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(s, fmt).date()
            except ValueError:
                continue
        raise ValueError("fecha_actuacion debe tener formato DD/MM/AA")

    @field_validator("tipo_actuacion", mode="before")
    @classmethod
    def _tipo_actuacion_val(cls, v):
        if v is None:
            return None
        s = to_upper_trim(v)
        opciones = [
            "INSPECCION",
            "REINSPECCION",
            "RATIFICACION",
            "VERIFICAR E INFORMAR",
        ]
        validar_opcion_en_lista(s, opciones, "tipo_actuacion")
        return s

    @field_validator("orden_trabajo_numero", mode="before")
    @classmethod
    def _strip_ot(cls, v):
        """
        Permite limpiar el número de OT o dejarlo en None
        (para “sacar” la OT en el update).
        """
        if v in (None, ""):
            return None
        return acta_6(v)

    @field_validator("inspectores", mode="before")
    @classmethod
    def _inspectores_list(cls, v):
        """
        Igual lógica que en el alta, pero permitiendo None
        (no tocar inspectores si no viene el campo).
        """
        if v is None:
            return None

        if isinstance(v, str):
            items = [i.strip() for i in v.split(",") if i.strip()]
        else:
            items = [str(i).strip() for i in v if str(i).strip()]

        if not (1 <= len(items) <= 4):
            raise ValueError("inspectores debe tener entre 1 y 4 nombres/apellidos")

        return [to_upper_trim(i) for i in items]
