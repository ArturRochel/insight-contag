import plotly.express as px

def gerar_graficos_temporais(metricas_temporais: dict) -> dict:
    """
    Gera os gráficos temporais por hora do contato e dia da semana.
    """
    df_hora = metricas_temporais.get("atendimentos_hora")
    df_dia = metricas_temporais.get("atendimentos_dia_semana")

    fig_hora = px.bar(
        df_hora,
        x="hora",
        y="count",
        labels={"hora": "Hora do Dia", "count": "Atendimentos"},
        title="Volume de Atendimentos por Hora do Dia"
    )

    fig_dia_semana = px.bar(
        df_dia,
        x="dia_semana",
        y="count",
        labels={"dia_semana": "Dia da Semana", "count": "Atendimentos"},
        title="Volume de Atendimentos por Dia da Semana"
    )

    return {
        "fig_hora": fig_hora,
        "fig_dia_semana": fig_dia_semana
    }
