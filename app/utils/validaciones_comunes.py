from datetime import datetime


# este validator nos sirve para ver si no esta vacio el campo
# metemos los valores con tipo str
def validar_no_vacio(valor: str, campo: str) -> str:
    s = str(valor).strip()
    if not s:
        raise ValueError(f"El campo {campo} no puede estar vacio")


def validar_tipo(valor, campo: str, dato_correcto):
    if not isinstance(valor, dato_correcto):
        raise TypeError(f"El campo {campo} de ser de tipo {dato_correcto.__name__}")
    return valor


def validar_longitud(valor, max_length, campo):
    s = str(valor)
    if len(s) > max_length:
        raise ValueError(
            f"La longitud del campo {campo} debe contener {max_length} caracteres "
        )
    return s


def validar_documento(valor: str):
    s = str(valor)
    if len(s) < 6 or len(s) > 11 or s.isdigit():
        raise ValueError("El cuit debe contener 11 digitos")


def validar_fecha(fecha, formato="%Y-%m-%d"):
    try:
        return datetime.strptime(fecha, formato)
    except Exception:
        raise ValueError(
            f"La fecha {fecha} no es valida o no tiene el formato {formato}"
        )


def validar_opcion_en_lista(valor, opciones_validas, campo):
    if valor not in opciones_validas:
        raise ValueError(
            f"El campo '{campo}' debe ser uno de los siguientes: {', '.join(opciones_validas)}"
        )
