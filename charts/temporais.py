import pandas as pd
import plotly.express as px

def gerar_grafico_curva_dia_geral(df_curva_dia: pd.DataFrame):
    """
    Gera o gráfico de linha suave (spline) da média de atendimentos ao longo do dia (07h às 18h).
    """
    if df_curva_dia is None or df_curva_dia.empty:
        return None

    fig = px.line(
        df_curva_dia,
        x="hora_str",
        y="media_atendimentos",
        labels={"hora_str": "Hora do Dia", "media_atendimentos": "Média de Atendimentos"},
        title="Fluxo Médio de Atendimentos ao Longo do Dia (07h às 18h)",
        markers=True,
        line_shape="spline"
    )
    fig.update_traces(line_color="#1E3A8A", line_width=3)
    return fig

def gerar_grafico_volume_diario(df_volume_diario: pd.DataFrame):
    """
    Gera o gráfico de linha do volume diário de atendimentos dentro do período selecionado.
    """
    if df_volume_diario is None or df_volume_diario.empty:
        return None

    fig = px.line(
        df_volume_diario,
        x="data",
        y="count",
        labels={"data": "Data", "count": "Quantidade de Atendimentos"},
        title="Evolução Diária de Atendimentos no Período Selecionado",
        markers=True
    )
    fig.update_traces(line_color="#059669", line_width=2.5)
    return fig

def gerar_graficos_temporais(metricas_temporais: dict) -> dict:
    """
    Gera os gráficos para a visão temporal.
    """
    df_curva = metricas_temporais.get("df_curva_dia_geral")
    m_filtradas = metricas_temporais.get("metricas_filtradas", {})
    df_volume = m_filtradas.get("df_volume_diario") if isinstance(m_filtradas, dict) else None

    return {
        "fig_curva_dia": gerar_grafico_curva_dia_geral(df_curva),
        "fig_volume_diario": gerar_grafico_volume_diario(df_volume)
    }

