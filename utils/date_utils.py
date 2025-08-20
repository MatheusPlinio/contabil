from datetime import datetime

MONTH_MAP = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}


def get_prev_month():
    today = datetime.today()
    prev_month = today.month - 1 or 12
    year = today.year
    month_name = MONTH_MAP[prev_month]
    return prev_month, year, month_name
