import pandas as pd
import plotly.express as px

def gerar_graficos_por_ug(metricas_ug: dict) -> dict:
    """
    Gera os gráficos consolidados para a visão por Unidade Gestora.

    Args:
        metricas_ug: Dicionário contendo os DataFrames de métricas por UG.

    Returns:
        dict: Dicionário com as figuras Plotly (`fig_ugs_recorrentes` e `fig_ugs_tempo_total`).
    """
    df_recorrentes = metricas_ug.get("df_ugs_recorrentes")
    df_tempo_total = metricas_ug.get("df_ugs_tempo_total")

    fig_ugs_recorrentes = px.bar(
        df_recorrentes,
        x="ug_solicitante",
        y="count",
        labels={"ug_solicitante": "Unidade Gestora", "count": "Quantidade de Atendimentos"},
        title="Top 10 UGs em Atendimentos",
        color="ug_solicitante",
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig_ugs_recorrentes.update_layout(showlegend=False)

    fig_ugs_tempo_total = px.bar(
        df_tempo_total,
        x="ug_solicitante",
        y="tempo_total_horas",
        labels={"ug_solicitante": "Unidade Gestora", "tempo_total_horas": "Tempo Total (Horas)"},
        title="Top 10 UGs em Tempo Total de Atendimento",
        color="ug_solicitante",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_ugs_tempo_total.update_layout(showlegend=False)

    return {
        "fig_ugs_recorrentes": fig_ugs_recorrentes,
        "fig_ugs_tempo_total": fig_ugs_tempo_total
    }

def gerar_grafico_demandas_por_ug(df_top_demandas: pd.DataFrame):
    """
    Gera o gráfico de barras Plotly para as Top 10 demandas de uma UG específica.

    Args:
        df_top_demandas: DataFrame com as demandas e frequências da UG selecionada.

    Returns:
        plotly.graph_objects.Figure: Figura de barras Plotly ou None se o DataFrame for vazio.
    """
    if df_top_demandas is None or df_top_demandas.empty:
        return None

    fig = px.bar(
        df_top_demandas,
        x="demanda_assunto",
        y="count",
        labels={"demanda_assunto": "Demanda", "count": "Quantidade de Atendimentos"},
        title="Top 10 Demandas Solicitadas",
        color="demanda_assunto",
        color_discrete_sequence=px.colors.qualitative.T10
    )
    fig.update_layout(showlegend=False)
    return fig


