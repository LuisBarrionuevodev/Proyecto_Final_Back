def to_upper_trim(valor: str | None):
    if valor is None:
        return None
    return str(valor).strip().upper()


def acta_6(valor: str | int | None):
    if valor is None:
        return None
    s = str(valor).strip()

    if not s:
        return None
    if s.isdigit():
        return s.zfill(6)
    else:
        return s
