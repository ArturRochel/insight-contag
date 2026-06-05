import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def graficos_gerais(df: pd.DataFrame) -> dict[str, go.Figure]:
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

    # Atendimentos por dia
    dias_limpos = df["data"].dt.to_period('D')
    atendimentos_dia = dias_limpos.value_counts().sort_index()

    media_dia = quant_atendimentos / len(atendimentos_dia)
    media_mes = quant_atendimentos / len(atendimentos_mes)

def graficos_por_atendente():
    pass

def graficos_por_demanda():
    pass

def graficos_por_ug():
    pass

def graficos_temporais():
    pass