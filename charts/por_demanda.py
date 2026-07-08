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
        metricas_demanda["df_demandas_assuntos"],
        x="demanda_assunto",
        y="count",
        labels={"demanda_assunto": "Demanda", "count": "Contagem"},
        title="Atendimentos por Demanda",
        color="demanda_assunto",
        color_discrete_sequence=px.colors.qualitative.T10
    )

    return {
        "fig_demandas": fig_demandas    
    }