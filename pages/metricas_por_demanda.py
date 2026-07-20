import streamlit as st
import pandas as pd
from metrics import calcular_metricas_por_demanda
from charts import gerar_graficos_por_demanda, gerar_grafico_ugs_por_demanda

def Metricas_Demandas():
    """
    Função que exibe a página de métricas por demanda.
    Exibe os gráficos consolidados (Top 10 mais demoradas e Top 10 mais recorrentes)
    e permite detalhar os indicadores ao escolher uma Demanda/Assunto.
    """

    st.title("Métricas por Demanda")
    st.write("Dados consolidados a partir das demandas da consultoria")

    df = st.session_state["df"]
    lista_demandas = df["demanda_assunto"].value_counts().reset_index().to_dict(orient="records")

    metricas = calcular_metricas_por_demanda(df)
    graficos_demandas = gerar_graficos_por_demanda(metricas)

    with st.container(border=True):
        st.subheader("Atendimentos por Demanda", help="As 10 demandas mais recorrentes.")
        st.plotly_chart(figure_or_data=graficos_demandas["fig_demandas_recorrentes"], width="stretch")

    with st.container(border=True):
        st.subheader("Tempo Médio de Atendimento por Demanda", help="As 10 demandas com tempo de atendimento mais longo.")
        st.plotly_chart(figure_or_data=graficos_demandas["fig_demandas_demoradas"], width="stretch")

    demandas = [item["demanda_assunto"] for item in lista_demandas][:10]

    st.markdown("---")

    demanda_selecionada = st.segmented_control(
        "Selecione uma demanda:",
        demandas,
        help="Selecione uma das 5 demandas mais recorrentes para visualizar os gráficos",
        required=True
    )  

    if demanda_selecionada is not None:
        metricas_detalhadas = calcular_metricas_por_demanda(df, demanda_selecionada=demanda_selecionada)
        m_filtradas = metricas_detalhadas["metricas_filtradas"]

        if m_filtradas:
            st.badge(f"Primeiro Dia: {m_filtradas['primeiro_dia']}", icon="📅", color="red")
            st.badge(f"Último Dia: {m_filtradas['ultimo_dia']}", icon="📅", color="red")

            a, b, c = st.columns(3)
            d, e, f = st.columns(3)

            a.metric(label="Total de Atendimentos", value=m_filtradas["quant_atendimentos"], help=f"Quantidade total de atendimentos realizados por {demanda_selecionada}", border=True)
            b.metric(label="Média Mensal de Atendimentos", value=m_filtradas["media_mensal"], help=f"Média mensal de atendimentos de {demanda_selecionada}", border=True)
            c.metric(label="Média Diária de Atendimento", value=m_filtradas["media_diaria"], help=f"Média diária de atendimentos de {demanda_selecionada}", border=True)

            d.metric(label="Tempo Médio de Atendimento", value=m_filtradas["tempo_medio_atendimento"], help=f"Duração média dos atendimentos realizados por {demanda_selecionada}", border=True)
            e.metric(label="Tempo Médio de Espera", value=m_filtradas["tempo_medio_espera"], help=f"Tempo médio de espera dos atendimentos realizados por {demanda_selecionada}", border=True)
            f.metric(
                label="Consultor Especialista", 
                value=m_filtradas["consultor_especialista"], 
                help=f"{m_filtradas['consultor_especialista']} tem a maior quantidade de atendimento na demanda {demanda_selecionada}", 
                border=True
            )

            # Gráfico de Top 10 UGs Solicitantes para a demanda selecionada
            fig_ugs_demanda = gerar_grafico_ugs_por_demanda(m_filtradas.get("df_top_ugs_demanda"))
            if fig_ugs_demanda is not None:
                with st.container(border=True):
                    st.subheader("Top 10 UGs Solicitantes", help=f"As 10 Unidades Gestoras que mais solicitaram a demanda {demanda_selecionada}")
                    st.plotly_chart(figure_or_data=fig_ugs_demanda, width="stretch")