import plotly.express as px

def gerar_graficos_por_consultor(metricas_consultor: dict) -> dict:
    """
    Gera os gráficos de demandas gerais a partir das métricas calculadas.

    Args:
        metricas_consultor: Dicionário contendo as métricas gerais calculadas.

    Returns:
        di
    """

    fig_atendimentos_mes = px.bar(
        metricas_consultor["meses"],
        x="data",
        y="count",
        labels={"data": "Meses", "count": "Atendimentos"},
        title="Atendimentos por Mês",
        color="data",
        color_discrete_sequence=px.colors.qualitative.D3
    )

    fig_atendimentos_dia = px.bar(
        metricas_consultor["dias"],
        x="data",
        y="count",
        labels={"data": "Dias", "count": "Atendimentos"},
        title="Atendimentos por Dia"
    )

    return {
        "fig_atendimentos_mes": fig_atendimentos_mes,
        "fig_atendimentos_dia": fig_atendimentos_dia    
    }