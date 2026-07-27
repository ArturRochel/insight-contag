import plotly.express as px
import pandas as pd

def gerar_graficos_encadeadas(metricas: dict) -> dict:
    """
    Gera os gráficos Plotly de evolução temporal e distribuição por demanda e status
    para os dados filtrados em Métricas Encadeadas.
    """
    df_evolucao = metricas.get("df_evolucao_temporal", pd.DataFrame())
    df_demanda = metricas.get("df_distribuicao_demanda", pd.DataFrame())
    df_status = metricas.get("df_distribuicao_status", pd.DataFrame())

    # 1. Gráfico de Evolução Temporal
    if not df_evolucao.empty:
        fig_evolucao = px.line(
            df_evolucao,
            x="data",
            y="count",
            labels={"data": "Data", "count": "Atendimentos"},
            title="Evolução Diária dos Atendimentos Filtrados",
            markers=True
        )
        fig_evolucao.update_traces(line_color="#1f77b4", line_width=3)
    else:
        fig_evolucao = None

    # 2. Gráfico de Distribuição por Demanda (Top 10)
    if not df_demanda.empty:
        fig_demanda = px.bar(
            df_demanda,
            x="demanda_assunto",
            y="count",
            labels={"demanda_assunto": "Demanda/Assunto", "count": "Quantidade"},
            title="Distribuição por Demanda/Assunto (Top 10)",
            color="demanda_assunto",
            color_discrete_sequence=px.colors.qualitative.T10
        )
        fig_demanda.update_layout(showlegend=False)
    else:
        fig_demanda = None

    # 3. Gráfico de Distribuição por Status
    if not df_status.empty:
        fig_status = px.bar(
            df_status,
            x="status_da_demanda",
            y="count",
            labels={"status_da_demanda": "Status", "count": "Quantidade"},
            title="Distribuição por Status do Atendimento",
            color="status_da_demanda",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_status.update_layout(showlegend=False)
    else:
        fig_status = None

    return {
        "fig_evolucao": fig_evolucao,
        "fig_demanda": fig_demanda,
        "fig_status": fig_status
    }
