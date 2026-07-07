import locale
import pandas as pd
from datetime import date
from utils.formatter import formatar_timedelta

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

def calcular_metricas_por_demanda(demanda: str) -> dict:
    df = st.session_state["df"]
    df_filtrado = df[df["consultor"] == demanda]
    
    quant_atendimentos = df_filtrado.shape[0]

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

    media_diaria = round(quant_atendimentos / len(atendimentos_dia), 2)
    media_mensal = round(quant_atendimentos / len(atendimentos_mes), 2)

    return {
        "quant_atendimentos": quant_atendimentos,
        "media_mensal": media_mensal,
        "media_diaria": media_diaria
    }