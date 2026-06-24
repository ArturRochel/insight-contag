import locale
import pandas as pd
from datetime import date
import plotly.express as px
import plotly.graph_objects as go
from utils.formatter import formatar_timedelta

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

def graficos_gerais(df: pd.DataFrame) -> dict:
    """
    Essa função cálcula as métricas e renderiza os gráficos de demandas gerais.

    Args:
        df: Dataframe limpo com os dados padronizados.

    Returns:
        dict[str, go.Figure]: Dicionário com os gráficos do Plotly.
        Retorna múltiplos gráficos do Plotly com as demandas gerais. Os gráficos retornados serão: Quantidade total de atendimentos, Quantidade total de atendimentos por mês, Quantidade total de atendimentos por dia, Média diária de atendimentos, Média mensal de atendimentos, Tempo médio de espera e Tempo total de atendimento.
    """
    # Quantidade de linhas = Quantidade de atendimentos válidos
    quant_atendimentos = df.shape[0]

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

    media_diaria = round(quant_atendimentos / len(atendimentos_dia), 2)
    media_mensal = round(quant_atendimentos / len(atendimentos_mes), 2)

    # Tempo total de atendimento
    tempo_total = df["tempo_decorrido"].sum()
    tempo_total_formatado = formatar_timedelta(tempo_total)

    # Tempo médio de atendimento
    tempo_medio_atendimento = formatar_timedelta(df["tempo_decorrido"].mean())

    # Tempo médio de espera
    tempo_medio_de_espera = formatar_timedelta(df["tempo_de_espera"].mean())

    # Tempo médio de atendimento diário
    tempo_medio_diario = formatar_timedelta(tempo_total / len(atendimentos_dia))

    # Tempo médio de atendimento mensal
    tempo_medio_mensal = formatar_timedelta(tempo_total / len(atendimentos_mes))

    # UG Solicitante mais recorrente
    ugs_solicitantes = df["ug_solicitante"].value_counts().reset_index().to_dict(orient="records")

    ug_mais_recorrente = ugs_solicitantes[0]

    demandas_assuntos = df["demanda_assunto"].value_counts().reset_index().to_dict(orient="records")

    demanda_mais_recorrente = demandas_assuntos[0]
    
    fig_atendimentos_mes = px.bar(
        meses,
        x="data",
        y="count",
        labels={"data": "Meses", "count": "Atendimentos"},
        title="Atendimentos por Mês"
    )

    fig_atendimentos_dia = px.bar(
        dias,
        x="data",
        y="count",
        labels={"data": "Dias", "count": "Atendimentos"},
        title="Atendimentos por Dia"
    )

    dados_exibicao = {
        "graficos": {
            "atendimentos_mes": fig_atendimentos_mes,
            "atendimentos_dia": fig_atendimentos_dia
        },
        "cards": {
            "quant_atendimentos": quant_atendimentos,
            "quant_atendimentos_hoje": quant_atendimentos_hoje,
            "media_diaria": media_diaria,
            "media_mensal": media_mensal,
            "tempo_total": tempo_total_formatado,
            "tempo_medio_atendimento": tempo_medio_atendimento,
            "tempo_medio_espera": tempo_medio_de_espera,
            "tempo_medio_diario": tempo_medio_diario,
            "tempo_medio_mensal": tempo_medio_mensal
        }
    }

    return dados_exibicao

def graficos_por_atendente():
    pass

def graficos_por_demanda():
    pass

def graficos_por_ug():
    pass

def graficos_temporais():
    pass