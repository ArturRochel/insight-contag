import pandas as pd

def formatar_timedelta(timeDelta: pd.Timedelta) -> str:
    horas = (timeDelta.days * 24) + timeDelta.components.hours
    minutos = timeDelta.components.minutes
    return f"{horas}h {minutos}m"