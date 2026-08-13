import streamlit as st
import pandas as pd
from metrics import calcular_metricas_por_consultor
from charts import gerar_graficos_por_consultor

def Metricas_Consultor():
    """
    Função que exibe a página de métricas por consultor no aplicativo Streamlit.
    """
    df = st.session_state["df"]

    valores_consultores = df["consultor"].value_counts().reset_index().to_dict(orient="records")
    consultores = [item["consultor"] for item in valores_consultores]

    st.title("Métricas por Consultor")
    st.write("Métricas consolidadas por consultor")

    # Filtro para seleção de consultor
    consultor_selecionado = st.segmented_control(
        "Selecione um consultor:",
        consultores,
        help="Selecione um dos consultores para filtrar as métricas dos atendimentos",
        required=True
    )   

    if consultor_selecionado is not None:
        df_filtrado = df[df["consultor"] == consultor_selecionado]
        metricas = calcular_metricas_por_consultor(df_filtrado)
        graficos = gerar_graficos_por_consultor(metricas)

        st.badge(f"Primeiro Dia: {metricas['primeiro_dia']}", icon="📅", color="red")
        st.badge(f"Último Dia: {metricas['ultimo_dia']}", icon="📅", color="red")

        a, b, c = st.columns(3)
        d, e = st.columns(2)
        f, g = st.columns(2)

        a.metric(label="Total de Atendimentos", value=metricas["quant_atendimentos"], help=f"Quantidade total de atendimentos realizados por {consultor_selecionado}", border=True)
        b.metric(label="Média Mensal de Atendimentos", value=metricas["media_mensal"], help=f"Média mensal de atendimentos de {consultor_selecionado}", border=True)
        c.metric(label="Média Diária de Atendimento", value=metricas["media_diaria"], help=f"Média diária de atendimentos de {consultor_selecionado}", border=True)

        d.metric(label="Tempo Médio de Atendimento", value=metricas["tempo_medio_atendimento"], help=f"Duração média dos atendimentos realizados por {consultor_selecionado}", border=True)
        e.metric(label="Tempo Médio de Espera", value=metricas["tempo_medio_espera"], help=f"Tempo médio de espera dos atendimentos realizados por {consultor_selecionado}", border=True)

        f.metric(label="UG mais Atendida", value=metricas["ug_mais_atendida"], help=f"Unidade Gestora mais atendida por {consultor_selecionado}", border=True)
        g.metric(label="Demanda mais Atendida", value=metricas["demanda_mais_atendida"], help=f"Demanda/assunto mais atendido por {consultor_selecionado}", border=True)

        st.markdown("---")
        st.header("Indicadores Gráficos")

        st.plotly_chart(figure_or_data=graficos["fig_atendimentos_mes"], width="stretch")
        st.plotly_chart(figure_or_data=graficos["fig_atendimentos_dia"], width="stretch")
