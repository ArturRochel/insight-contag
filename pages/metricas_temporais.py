import streamlit as st
import pandas as pd
from metrics import calcular_metricas_temporais
from charts import gerar_grafico_curva_dia_geral, gerar_grafico_volume_diario

def Metricas_Temporais():
    """
    Função que exibe a página de métricas temporais / por período.
    """
    st.title("Métricas Temporais")
    st.write("Análise temporal da consultoria: visão geral dos horários de pico e detalhamento por período selecionado")

    df = st.session_state["df"]

    # 1. Visão Geral da Base Completa (Fixo no Topo)
    metricas_gerais = calcular_metricas_temporais(df)

    st.badge(f"Primeiro Dia: {metricas_gerais['primeiro_dia']}", icon="📅", color="red")
    st.badge(f"Último Dia: {metricas_gerais['ultimo_dia']}", icon="📅", color="red")

    a, b, c = st.columns(3)
    a.metric(
        label="Horário de Pico",
        value=metricas_gerais["horario_pico_geral"],
        help="Faixa de horário com a maior média de atendimentos na base histórica",
        border=True
    )
    b.metric(
        label="Dia Mais Movimentado",
        value=metricas_gerais["dia_mais_movimentado_geral"],
        help="Dia útil da semana (Segunda a Sexta) com a maior média de atendimentos na base histórica",
        border=True
    )
    c.metric(
        label="Mês de Pico",
        value=metricas_gerais["mes_pico_geral"],
        help="Mês com a maior quantidade total de atendimentos na base histórica",
        border=True
    )

    fig_curva = gerar_grafico_curva_dia_geral(metricas_gerais["df_curva_dia_geral"])
    if fig_curva is not None:
        with st.container(border=True):
            st.subheader("Fluxo de Atendimentos ao Longo do Dia", help="Média diária de atendimentos por hora no expediente (07h às 18h) em todo o período histórico")
            st.plotly_chart(figure_or_data=fig_curva, width="stretch")

    st.markdown("---")

    # 2. Painel de Filtro Temporal
    st.subheader("Filtro por Período Temporal")

    min_date = df["data"].min().date()
    max_date = df["data"].max().date()

    opcao_periodo = st.segmented_control(
        "Selecione o período de análise:",
        ["Todas as Datas", "Último Mês", "Último Trimestre", "Último Semestre", "Ano Atual", "Personalizado"],
        default="Todas as Datas",
        help="Escolha um atalho de período ou selecione Personalizado para definir datas customizadas",
        required=True
    )

    data_inicio = min_date
    data_fim = max_date

    if opcao_periodo == "Último Mês":
        data_inicio = max_date - pd.Timedelta(days=30)
    elif opcao_periodo == "Último Trimestre":
        data_inicio = max_date - pd.Timedelta(days=90)
    elif opcao_periodo == "Último Semestre":
        data_inicio = max_date - pd.Timedelta(days=180)
    elif opcao_periodo == "Ano Atual":
        data_inicio = pd.Timestamp(year=max_date.year, month=1, day=1).date()
    elif opcao_periodo == "Personalizado":
        col_d1, col_d2 = st.columns(2)
        data_inicio = col_d1.date_input("Data Inicial", value=min_date, min_value=min_date, max_value=max_date)
        data_fim = col_d2.date_input("Data Final", value=max_date, min_value=min_date, max_value=max_date)

    # 3. Seção Inferior Filtrada
    metricas_periodo = calcular_metricas_temporais(df, data_inicio=data_inicio, data_fim=data_fim)
    m_filtradas = metricas_periodo.get("metricas_filtradas", {})

    if m_filtradas:
        st.badge(f"Primeiro Dia: {m_filtradas['primeiro_dia']}", icon="📅", color="red")
        st.badge(f"Último Dia: {m_filtradas['ultimo_dia']}", icon="📅", color="red")

        # Grid de 9 Cards (3x3)
        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)
        col7, col8, col9 = st.columns(3)

        col1.metric(
            label="Total de Atendimentos",
            value=m_filtradas["quant_atendimentos"],
            help="Quantidade total de atendimentos realizados no período selecionado",
            border=True
        )
        col2.metric(
            label="Média de Atendimentos Diários",
            value=m_filtradas["media_diaria"],
            help="Média diária de atendimentos realizados no período selecionado",
            border=True
        )
        col3.metric(
            label="Média de Atendimentos Mensal",
            value=m_filtradas["media_mensal"],
            help="Média mensal de atendimentos computados no período selecionado",
            border=True
        )

        col4.metric(
            label="Tempo Médio de Espera",
            value=m_filtradas["tempo_medio_espera"],
            help="Tempo médio de espera dos atendimentos no período selecionado",
            border=True
        )
        col5.metric(
            label="Tempo Médio de Atendimento",
            value=m_filtradas["tempo_medio_atendimento"],
            help="Duração média dos atendimentos no período selecionado",
            border=True
        )
        col6.metric(
            label="Tempo Total de Atendimento",
            value=m_filtradas["tempo_total_atendimento"],
            help="Soma total acumulada do tempo de todos os atendimentos no período selecionado",
            border=True
        )

        col7.metric(
            label="UG mais Recorrente",
            value=m_filtradas["ug_mais_recorrente"],
            help="Unidade Gestora com a maior quantidade de solicitações no período selecionado",
            border=True
        )
        col8.metric(
            label="Demanda mais Recorrente",
            value=m_filtradas["demanda_mais_recorrente"],
            help="Assunto ou demanda mais frequente no período selecionado",
            border=True
        )
        col9.metric(
            label="Consultor com mais Atendimentos",
            value=m_filtradas["consultor_mais_atendimentos"],
            help="Consultor responsável pelo maior volume de atendimentos no período selecionado",
            border=True
        )

        # Gráfico Diário no período filtrado
        fig_volume = gerar_grafico_volume_diario(m_filtradas.get("df_volume_diario"))
        if fig_volume is not None:
            with st.container(border=True):
                st.subheader("Evolução Diária de Atendimentos", help="Quantidade diária de atendimentos registrados ao longo das datas do período selecionado")
                st.plotly_chart(figure_or_data=fig_volume, width="stretch")