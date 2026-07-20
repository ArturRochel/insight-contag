import pandas as pd
import plotly.express as px

def gerar_grafico_ugs_por_demanda(df_top_ugs: pd.DataFrame):
    """
    Gera o gráfico de barras Plotly para as Top 10 UGs de uma demanda específica.
    """
    if df_top_ugs is None or df_top_ugs.empty:
        return None

    fig = px.bar(
        df_top_ugs,
        x="ug_solicitante",
        y="count",
        labels={"ug_solicitante": "Unidade Gestora", "count": "Quantidade de Atendimentos"},
        title="Top 10 UGs Solicitantes",
        color="ug_solicitante",
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig.update_layout(showlegend=False)
    return fig

def gerar_graficos_por_demanda(metricas_demanda: dict) -> dict:
    """
    Gera os gráficos para a visão por demanda a partir das métricas calculadas.

    Args:
        metricas_demanda: Dicionário contendo os DataFrames de métricas por demanda.

    Returns:
        dict: Dicionário com os objetos de figura Plotly (`fig_demandas_demoradas` e `fig_demandas_recorrentes`).
    """
    df_demoradas = metricas_demanda.get("df_top_demandas_demoradas")
    df_recorrentes = metricas_demanda.get("df_top_demandas_recorrentes")

    fig_demandas_demoradas = px.bar(
        df_demoradas,
        x="demanda_assunto",
        y="tempo_medio",
        labels={"demanda_assunto": "Demanda", "tempo_medio": "Tempo Médio (min)"},
        title="Tempo Médio de Atendimento por Demanda",
        color="demanda_assunto",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_demandas_demoradas.update_layout(showlegend=False)

    fig_demandas_recorrentes = px.bar(
        df_recorrentes,
        x="demanda_assunto",
        y="count",
        labels={"demanda_assunto": "Demanda", "count": "Contagem"},
        title="Atendimentos por Demanda",
        color="demanda_assunto",
        color_discrete_sequence=px.colors.qualitative.T10
    )
    fig_demandas_recorrentes.update_layout(showlegend=False)

    return {
        "fig_demandas_demoradas": fig_demandas_demoradas,
        "fig_demandas_recorrentes": fig_demandas_recorrentes
    }