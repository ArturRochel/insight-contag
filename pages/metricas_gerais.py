import streamlit as st
from metrics import calcular_metricas_gerais
from charts import gerar_graficos_gerais

def Metricas_Gerais():
    df = st.session_state["df"]
    metricas = calcular_metricas_gerais(df=df)
    graficos = gerar_graficos_gerais(metricas_gerais=metricas)


    st.title("Métricas Gerais")
    st.write("Visão consolidada e geral dos atendimentos registrados")


    st.badge(f"Primeiro Dia: {metricas['primeiro_dia']}", icon="📅", color="red")
    st.badge(f"Último Dia: {metricas['ultimo_dia']}", icon="📅", color="red")

    a, b, c = st.columns(3)
    d, e, f = st.columns(3)
    g, h = st.columns(2)

    # Métricas
    a.metric(label="Total de Atendimentos",value=metricas["quant_atendimentos"], help="Total de atendimentos desde o início da base de dados", border=True)

    b.metric(label="Média de Atendimentos Diários",value=metricas["media_diaria"], help="Média de atendimentos diários realizados", border=True)

    c.metric(label="Média de Atendimentos Mensal", value=metricas["media_mensal"], help="Média de atendimentos contabilizados ao longo dos meses", border=True)

    d.metric(label="Tempo Médio de Espera", value=metricas["tempo_medio_espera"], help="Tempo médio de espera pelos atendimentos", border=True)

    e.metric(label="Tempo Médio de Atendimento", value=metricas["tempo_medio_atendimento"], help="Durtação média dos atendimentos", border=True)

    f.metric(label="Tempo Total de Atendimento", value=metricas["tempo_total_atendimento"], help="Soma do tempo de todos os atendimentos", border=True)

    g.metric(label="UG mais Recorrente", value=metricas["ug_mais_recorrente"]["ug_solicitante"], help="Unidade Gestora que mais recorre a consultoria", border=True)

    h.metric(label="Demanda mais Recorrente", value=metricas    ["demanda_mais_recorrente"]["demanda_assunto"], help="Demanda mais presente nos atendimentos", border=True)

    st.markdown("---")

    st.header("Indicadores Gráficos")

    # Gráficos
    st.plotly_chart(figure_or_data=graficos["fig_atendimentos_consultores"])
    st.plotly_chart(figure_or_data=graficos["fig_atendimentos_mes"])
    st.plotly_chart(figure_or_data=graficos["fig_atendimentos_dia"])

