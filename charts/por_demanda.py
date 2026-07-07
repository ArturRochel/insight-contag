import plotly.express as px

def gerar_graficos_por_demanda(metricas_demanda: dict) -> dict:
    """
    Gera os gráficos de demandas gerais a partir das métricas calculadas.

    Args:
        metricas_demanda: Dicionário contendo as métricas gerais calculadas.

    Returns:
        di
    """

    fig_demandas = px.bar(
        metricas_demanda["df_status_das_demandas"],
        x="status_da_demanda",
        y="count",
        labels={"demanda": "Demanda", "count": "Contagem"},
        title="Atendimentos por Demanda",
        color="status_da_demanda",
        color_discrete_sequence=px.colors.qualitative.T10
    )

    return {
        "fig_demandas": fig_demandas    
    }