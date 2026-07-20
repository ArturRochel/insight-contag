import locale
import pandas as pd
from metrics.base import extrair_intervalo_datas

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

def calcular_metricas_temporais(df: pd.DataFrame) -> dict:
    """
    Calcula métricas de análise de tempo e sazonalidade de atendimentos.

    Args:
        df: DataFrame de atendimentos.

    Returns:
        dict: Dicionário contendo estatísticas por horário, dia da semana e mês.
    """
    if df.empty:
        return {
            "primeiro_dia": "N/A",
            "ultimo_dia": "N/A",
            "atendimentos_hora": pd.DataFrame(columns=["hora", "count"]),
            "atendimentos_dia_semana": pd.DataFrame(columns=["dia_semana", "count"])
        }

    primeiro_dia, ultimo_dia = extrair_intervalo_datas(df)

    # Extração de horas do contato
    df_temp = df.copy()
    df_temp["hora"] = df_temp["hora_do_contato"].dt.components["hours"] if "hora_do_contato" in df_temp.columns else 0
    atendimentos_hora = df_temp["hora"].value_counts().reset_index().sort_values(by="hora")

    # Extração por dia da semana
    df_temp["dia_semana"] = df_temp["data"].dt.day_name(locale="pt_BR.UTF-8")
    atendimentos_dia_semana = df_temp["dia_semana"].value_counts().reset_index()

    return {
        "primeiro_dia": primeiro_dia,
        "ultimo_dia": ultimo_dia,
        "atendimentos_hora": atendimentos_hora,
        "atendimentos_dia_semana": atendimentos_dia_semana
    }
