import plotly.express as px

def gerar_graficos_por_ug(metricas_ug: dict) -> dict:
    """
    Gera os gráficos para a visão por Unidade Gestora.
    """
    df_ugs = metricas_ug.get("df_ugs_solicitantes")
    fig_ugs = px.bar(
        df_ugs,
        x="ug_solicitante",
        y="count",
        labels={"ug_solicitante": "Unidade Gestora", "count": "Atendimentos"},
        title="Atendimentos por Unidade Gestora",
        color="ug_solicitante",
        color_discrete_sequence=px.colors.qualitative.Prism
    )
    fig_ugs.update_layout(showlegend=False)

    return {
        "fig_ugs": fig_ugs
    }
