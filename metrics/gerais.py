import locale
import pandas as pd
from datetime import date
from utils.formatter import formatar_timedelta
from metrics.base import extrair_intervalo_datas, calcular_frequencia

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

def calcular_metricas_gerais(df: pd.DataFrame) -> dict:
    """
    Calcula as métricas gerais a partir do DataFrame de atendimentos.

    Args:
        df: DataFrame contendo os dados de atendimentos.    

    Returns:
        dict: Dicionário contendo as métricas gerais calculadas.
    """
    if df.empty:
        return {}

    quant_atendimentos = df.shape[0]

    # Primeiro e último registro
    primeiro_dia, ultimo_dia = extrair_intervalo_datas(df)

    # Atendimentos por mês
    meses_limpos = df["data"].dt.to_period('M')
    atendimentos_mes = meses_limpos.value_counts().sort_index()
    atendimentos_mes.index = atendimentos_mes.index.strftime("%B/%Y").str.capitalize()
    meses = atendimentos_mes.reset_index()

    # Atendimentos por dia
    dias_limpos = df["data"].dt.to_period('D')
    atendimentos_dia = dias_limpos.value_counts().sort_index()
    atendimentos_dia.index = atendimentos_dia.index.strftime("%d/%m/%y")
    dias = atendimentos_dia.reset_index()

    # Atendimentos apenas de hoje
    data_atual = date.today()
    atendimentos_hoje = df[df["data"].dt.date == data_atual]
    quant_atendimentos_hoje = len(atendimentos_hoje)

    media_diaria = round(quant_atendimentos / len(atendimentos_dia), 2) if len(atendimentos_dia) > 0 else 0
    media_mensal = round(quant_atendimentos / len(atendimentos_mes), 2) if len(atendimentos_mes) > 0 else 0

    # Tempo total de atendimento
    tempo_total = df["tempo_decorrido"].sum()
    tempo_total_atendimento = formatar_timedelta(tempo_total)

    # Tempo médio de atendimento
    tempo_medio_atendimento = formatar_timedelta(df["tempo_decorrido"].mean())

    # Tempo médio de espera
    tempo_medio_espera = formatar_timedelta(df["tempo_de_espera"].mean())

    # Tempo médio de atendimento diário
    tempo_medio_diario = formatar_timedelta(tempo_total / len(atendimentos_dia)) if len(atendimentos_dia) > 0 else "00:00:00"

    # Tempo médio de atendimento mensal
    tempo_medio_mensal = formatar_timedelta(tempo_total / len(atendimentos_mes)) if len(atendimentos_mes) > 0 else "00:00:00"

    # UGs solicitantes e UG mais recorrente
    df_ugs_solicitantes = calcular_frequencia(df, "ug_solicitante")
    ugs_solicitantes = df_ugs_solicitantes.to_dict(orient="records")
    ug_mais_recorrente = ugs_solicitantes[0] if ugs_solicitantes else {"ug_solicitante": "N/A", "count": 0}

    # Demandas e Demanda mais recorrente
    df_demandas_assuntos = calcular_frequencia(df, "demanda_assunto")
    demandas_assuntos = df_demandas_assuntos.to_dict(orient="records")
    demanda_mais_recorrente = demandas_assuntos[0] if demandas_assuntos else {"demanda_assunto": "N/A", "count": 0}

    # Atendimentos por atendente
    df_atendimentos_consultores = calcular_frequencia(df, "consultor")

    # Atendimentos por Status do atendimento
    df_status_atendimentos = calcular_frequencia(df, "status_da_demanda")
    status_atendimentos = df_status_atendimentos.to_dict(orient="records")

    return {
        "quant_atendimentos": quant_atendimentos,
        "quant_atendimentos_hoje": quant_atendimentos_hoje,
        "media_diaria": media_diaria,
        "media_mensal": media_mensal,
        "tempo_total_atendimento": tempo_total_atendimento,
        "tempo_medio_atendimento": tempo_medio_atendimento,
        "tempo_medio_espera": tempo_medio_espera,
        "tempo_medio_diario": tempo_medio_diario,
        "tempo_medio_mensal": tempo_medio_mensal,
        "ug_mais_recorrente": ug_mais_recorrente,
        "demanda_mais_recorrente": demanda_mais_recorrente, 
        "atendimentos_consultores": df_atendimentos_consultores,
        "status_das_demandas": status_atendimentos,
        "df_status_das_demandas": df_status_atendimentos,
        "df_demandas_assuntos": df_demandas_assuntos,
        "df_ugs_solicitantes": df_ugs_solicitantes,
        "meses": meses,
        "dias": dias,
        "primeiro_dia": primeiro_dia,
        "ultimo_dia": ultimo_dia
    }