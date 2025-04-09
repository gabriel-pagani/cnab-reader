def cnpj_format(cnpj: str) -> str:
    try:
        return f"{cnpj[0:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:14]}"
    except Exception:
        return None


def date_format(date: str) -> str:
    try:
        return f"{date[4:8]}-{date[2:4]}-{date[0:2]}"
    except Exception:
        None


def value_format(value: str) -> float:
    try:
        return float(value) / 100
    except Exception:
        return None


def code_format(code: str) -> str:
    try:
        return str(int(code))
    except Exception:
        return None
