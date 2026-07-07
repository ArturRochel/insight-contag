
import locale
import pandas as pd
from datetime import date
from utils.formatter import formatar_timedelta

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

def calcular_metricas_gerais(df: pd.DataFrame) -> dict:
    """
    Calcula as métricas gerais a partir do DataFrame de atendimentos.

    Args:
        df: DataFrame contendo os dados de atendimentos.    

    Returns:
        dict: Dicionário contendo as métricas gerais calculadas.
    """
    quant_atendimentos = df.shape[0]

    # Primeiro e ùltimo registro
    dias_limpos = df["data"].dt.to_period('D') 
    primeiro_dia = dias_limpos.min().strftime("%d/%m/%y")
    ultimo_dia = dias_limpos.max().strftime("%d/%m/%y")

    # Atendimentos por mês
    meses_limpos = df["data"].dt.to_period('M')
    atendimentos_mes = meses_limpos.value_counts().sort_index()
    atendimentos_mes.index = atendimentos_mes.index.strftime("%B/%Y").str.capitalize()
    meses = atendimentos_mes.reset_index()

    # Atendimentos por dia
    atendimentos_dia = dias_limpos.value_counts().sort_index()
    atendimentos_dia.index = atendimentos_dia.index.strftime("%d/%m/%y")
    dias = atendimentos_dia.reset_index()

    # Atendimentos apenas de hoje
    data_atual = date.today()
    atendimentos_hoje = df[df["data"].dt.date == data_atual]
    quant_atendimentos_hoje = len(atendimentos_hoje)

    media_diaria = round(quant_atendimentos / len(atendimentos_dia), 2)
    media_mensal = round(quant_atendimentos / len(atendimentos_mes), 2)

    # Tempo total de atendimento
    tempo_total = df["tempo_decorrido"].sum()
    tempo_total_atendimento = formatar_timedelta(tempo_total)

    # Tempo médio de atendimento
    tempo_medio_atendimento = formatar_timedelta(df["tempo_decorrido"].mean())

    # Tempo médio de espera
    tempo_medio_espera = formatar_timedelta(df["tempo_de_espera"].mean())

    # Tempo médio de atendimento diário
    tempo_medio_diario = formatar_timedelta(tempo_total / len(atendimentos_dia))

    # Tempo médio de atendimento mensal
    tempo_medio_mensal = formatar_timedelta(tempo_total / len(atendimentos_mes))

    # UG Solicitante mais recorrente
    ugs_solicitantes = df["ug_solicitante"].value_counts().reset_index().to_dict(orient="records")

    ug_mais_recorrente = ugs_solicitantes[0]

    # Demanda mais recorrente
    demandas_assuntos = df["demanda_assunto"].value_counts().reset_index().to_dict(orient="records")

    demanda_mais_recorrente = demandas_assuntos[0]
    
    # Quantidade de atendimentos por atendente
    atendimentos_consultores = df["consultor"].value_counts().reset_index().to_dict(orient="records")

    df_atendimentos_consultores = pd.DataFrame(atendimentos_consultores)

    # Atendimentos por Status da Demanda
    status_atendimentos = df["status_da_demanda"].value_counts().reset_index().to_dict(orient="records")

    #df_status_atendimentos = pd.DataFrame(status_atendimentos)

    # Dados inteiros primeiro e DataFrames depois
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
        "meses": meses,
        "dias": dias,
        "primeiro_dia": primeiro_dia,
        "ultimo_dia": ultimo_dia
    }