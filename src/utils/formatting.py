def cnpj_format(cnpj: str) -> str:
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"


def date_format(date: str) -> str:
    return f"{date[:2]}/{date[2:4]}/{date[4:]}"


def value_format(value: str) -> float:
    return float(value) / 100
