import streamlit as st
import pandas as pd
from metrics import calcular_metricas_gerais
from charts import gerar_graficos_por_demanda

def Metricas_Demandas():

    """
    Função que exibe a página de métricas por demanda. Nessa página serão exibidos os dados a partir da escolha de uma Demanda/Assunto. Exemplo: Demandas mais frequentes, demandas mais demoradas e tempo médio de cada Demanda/Assunto.

    Args:
        None
    Returns:
        None
    """

    st.title("Métricas por Demanda")
    st.write("Dados consolidados a partir das demandas da consultoria")

    df = st.session_state["df"]
    lista_demandas = df["demanda_assunto"].value_counts().reset_index().to_dict(orient="records")
    metricas = calcular_metricas_gerais(df)
    graficos_demandas = gerar_graficos_por_demanda(metricas)

    st.plotly_chart(figure_or_data=graficos_demandas["fig_demandas"])

    demandas = [item["demanda_assunto"] for item in lista_demandas][:5]

    # Filtro de escolha das 5 demandas mais recorrentes
    demanda_selecionada = st.segmented_control(
    "Selecione uma demanda:",
    demandas,
    help="Selecione uma das 5 demandas mais recorrentes para visualizar os gráficos",
    required=True
    )  

    # Lógica de filtro e exibicação
    if(demanda_selecionada is not None):
        df_filtrado = df[df["demanda_assunto"] == demanda_selecionada]
        metricas_filtradas = calcular_metricas_gerais(df_filtrado)

        st.badge(f"Primeiro Dia: {metricas_filtradas['primeiro_dia']}", icon="📅", color="red")
        st.badge(f"Último Dia: {metricas_filtradas['ultimo_dia']}", icon="📅", color="red")

        a, b, c = st.columns(3)
        d, e = st.columns(2)

        a.metric(label="Total de Atendimentos", value=metricas_filtradas["quant_atendimentos"], help=f"Quantidade total de atendimentos realizados por {demanda_selecionada}", border=True)

        b.metric(label="Média Mensal de Atendimentos", value=metricas_filtradas["media_mensal"], help=f"Média mensal de atendimentos de {demanda_selecionada}", border=True)

        c.metric(label="Média Diária de Atendimento", value=metricas_filtradas["media_diaria"], help=f"Média mensal de atendimentos de {demanda_selecionada}", border=True)

        d.metric(label="Tempo Médio de Atendimento", value=metricas_filtradas["tempo_medio_atendimento"], help=f"Duração média dos atendimentos realizados por {demanda_selecionada}", border=True)
        
        e.metric(label="Tempo Médio de Espera", value=metricas_filtradas["tempo_medio_espera"], help=f"Tempo médio de espera dos atendimentos realizados por {demanda_selecionada}", border=True)