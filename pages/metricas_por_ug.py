import streamlit as st
import pandas as pd
from metrics import calcular_metricas_por_ug
from charts import gerar_graficos_por_ug, gerar_grafico_demandas_por_ug

def Metricas_UG():
    """
    Função que exibe a página de métricas por Unidade Gestora (UG).
    Exibe os gráficos consolidados (Top 10 mais recorrentes e Top 10 tempo total)
    e permite detalhar os indicadores e o gráfico de barras de demandas ao escolher uma UG.
    """

    st.title("Métricas por UG")
    st.write("Dados consolidados a partir das Unidades Gestoras da consultoria")

    df = st.session_state["df"]

    metricas = calcular_metricas_por_ug(df)
    graficos = gerar_graficos_por_ug(metricas)

    with st.container(border=True):
        st.subheader("Atendimentos por UG", help="As 10 Unidades Gestoras mais recorrentes em quantidade de atendimentos.")
        st.plotly_chart(figure_or_data=graficos["fig_ugs_recorrentes"], width="stretch")

    with st.container(border=True):
        st.subheader("Tempo Total de Atendimento por UG", help="As 10 Unidades Gestoras com maior tempo total acumulado de atendimento (em horas).")
        st.plotly_chart(figure_or_data=graficos["fig_ugs_tempo_total"], width="stretch")

    lista_ugs = metricas.get("lista_todas_ugs", [])

    st.markdown("---")

    ug_selecionada = st.selectbox(
        "Selecione uma Unidade Gestora:",
        lista_ugs,
        index=None,
        placeholder="Escolha uma Unidade Gestora...",
        help="Selecione uma Unidade Gestora para visualizar os indicadores e as demandas específicas"
    )

    if ug_selecionada is None:
        st.info("Por favor, selecione uma Unidade Gestora acima para visualizar seus indicadores e demandas específicas.")
    else:
        metricas_detalhadas = calcular_metricas_por_ug(df, ug_selecionada=ug_selecionada)
        m_filtradas = metricas_detalhadas["metricas_filtradas"]

        if m_filtradas:
            st.badge(f"Primeiro Dia: {m_filtradas['primeiro_dia']}", icon="📅", color="red")
            st.badge(f"Último Dia: {m_filtradas['ultimo_dia']}", icon="📅", color="red")

            a, b, c = st.columns(3)
            d, e, f = st.columns(3)

            a.metric(
                label="Total de Atendimentos",
                value=m_filtradas["quant_atendimentos"],
                help=f"Quantidade total de atendimentos realizados para a UG {ug_selecionada}",
                border=True
            )
            b.metric(
                label="Média Mensal de Atendimentos",
                value=m_filtradas["media_mensal"],
                help=f"Média mensal de atendimentos da UG {ug_selecionada}",
                border=True
            )
            c.metric(
                label="Média Diária de Atendimentos",
                value=m_filtradas["media_diaria"],
                help=f"Média diária de atendimentos da UG {ug_selecionada}",
                border=True
            )

            d.metric(
                label="Tempo Médio de Atendimento",
                value=m_filtradas["tempo_medio_atendimento"],
                help=f"Duração média dos atendimentos realizados para a UG {ug_selecionada}",
                border=True
            )
            e.metric(
                label="Tempo Médio de Espera",
                value=m_filtradas["tempo_medio_espera"],
                help=f"Tempo médio de espera dos atendimentos da UG {ug_selecionada}",
                border=True
            )
            f.metric(
                label="Consultor Especialista",
                value=m_filtradas["consultor_especialista"],
                help=f"{m_filtradas['consultor_especialista']} tem a maior quantidade de atendimentos na UG {ug_selecionada}",
                border=True
            )

            # Gráfico de barras convencional das demandas solicitadas pela UG selecionada
            fig_demandas_ug = gerar_grafico_demandas_por_ug(m_filtradas.get("df_top_demandas_ug"))
            if fig_demandas_ug is not None:
                with st.container(border=True):
                    st.subheader("Top 10 Demandas Solicitadas", help=f"As 10 demandas mais solicitadas pela UG {ug_selecionada}")
                    st.plotly_chart(figure_or_data=fig_demandas_ug, width="stretch")