import plotly.express as px

def gerar_graficos_gerais(metricas_gerais: dict) -> dict:
    """
    Gera os gráficos de demandas gerais a partir das métricas calculadas.

    Args:
        metricas_gerais: Dicionário contendo as métricas gerais calculadas.

    Returns:
        dict[str, go.Figure]: Dicionário com os gráficos do Plotly.
    """

    fig_atendimentos_consultores = px.bar(
        metricas_gerais["atendimentos_consultores"],
        x="consultor",
        y="count",
        labels={"consultor": "Consultor", "count": "Atendimentos"},
        title="Atendimentos por Consultor",
        color="consultor",
        color_discrete_sequence=px.colors.qualitative.T10
    )

    fig_atendimentos_mes = px.bar(
        metricas_gerais["meses"],
        x="data",
        y="count",
        labels={"data": "Meses", "count": "Atendimentos"},
        title="Atendimentos por Mês",
        color="data",
        color_discrete_sequence=px.colors.qualitative.D3
    )

    fig_atendimentos_dia = px.bar(
        metricas_gerais["dias"],
        x="data",
        y="count",
        labels={"data": "Dias", "count": "Atendimentos"},
        title="Atendimentos por Dia"
    )

    return {
        "fig_atendimentos_consultores": fig_atendimentos_consultores,
        "fig_atendimentos_mes": fig_atendimentos_mes,
        "fig_atendimentos_dia": fig_atendimentos_dia    
    }