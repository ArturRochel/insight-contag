import locale
import pandas as pd
from utils.formatter import formatar_timedelta
from metrics.base import extrair_intervalo_datas

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

def calcular_metricas_por_consultor(df: pd.DataFrame, consultor: str = None) -> dict:
    """
    Calcula métricas específicas para um consultor a partir do DataFrame fornecido.

    Args:
        df: DataFrame de atendimentos (pode já estar filtrado pelo consultor ou ser o completo).
        consultor: Nome do consultor selecionado (opcional, para filtrar se df for completo).

    Returns:
        dict: Dicionário contendo métricas calculadas e séries de dados para gráficos.
    """
    df_filtrado = df[df["consultor"] == consultor] if consultor is not None else df
    
    if df_filtrado.empty:
        return {
            "quant_atendimentos": 0,
            "media_mensal": 0,
            "media_diaria": 0,
            "tempo_medio_atendimento": "00:00:00",
            "tempo_medio_espera": "00:00:00",
            "primeiro_dia": "N/A",
            "ultimo_dia": "N/A",
            "meses": pd.DataFrame(columns=["data", "count"]),
            "dias": pd.DataFrame(columns=["data", "count"])
        }

    quant_atendimentos = df_filtrado.shape[0]
    primeiro_dia, ultimo_dia = extrair_intervalo_datas(df_filtrado)

    # Atendimentos por mês
    meses_limpos = df_filtrado["data"].dt.to_period('M')
    atendimentos_mes = meses_limpos.value_counts().sort_index()
    atendimentos_mes.index = atendimentos_mes.index.strftime("%B/%Y").str.capitalize()
    meses = atendimentos_mes.reset_index()

    # Atendimentos por dia
    dias_limpos = df_filtrado["data"].dt.to_period('D') 
    atendimentos_dia = dias_limpos.value_counts().sort_index()
    atendimentos_dia.index = atendimentos_dia.index.strftime("%d/%m/%y")
    dias = atendimentos_dia.reset_index()

    media_diaria = round(quant_atendimentos / len(atendimentos_dia), 2) if len(atendimentos_dia) > 0 else 0
    media_mensal = round(quant_atendimentos / len(atendimentos_mes), 2) if len(atendimentos_mes) > 0 else 0

    tempo_medio_atendimento = formatar_timedelta(df_filtrado["tempo_decorrido"].mean())
    tempo_medio_espera = formatar_timedelta(df_filtrado["tempo_de_espera"].mean())

    return {
        "quant_atendimentos": quant_atendimentos,
        "media_mensal": media_mensal,
        "media_diaria": media_diaria,
        "tempo_medio_atendimento": tempo_medio_atendimento,
        "tempo_medio_espera": tempo_medio_espera,
        "primeiro_dia": primeiro_dia,
        "ultimo_dia": ultimo_dia,
        "meses": meses,
        "dias": dias
    }