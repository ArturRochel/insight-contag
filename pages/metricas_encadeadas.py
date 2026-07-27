import streamlit as st
import pandas as pd
from metrics import calcular_metricas_encadeadas
from charts import gerar_graficos_encadeadas

def Metricas_Encadeadas():
    """
    Exibe a página de Métricas Encadeadas com filtros cruzados reativos dispostos
    em um expander no topo, cards de métricas, gráficos e tabela detalhada.
    """
    st.title("Métricas Encadeadas")
    st.write("Análise granular dos atendimentos através de filtros cruzados reativos")

    df = st.session_state["df"]

    if df.empty:
        st.warning("⚠️ Nenhum registro de atendimento encontrado na base de dados.")
        st.stop()

    # Leitura prévia para obter opções iniciais de filtros
    metricas_iniciais = calcular_metricas_encadeadas(df)

    min_date = df["data"].min().date()
    max_date = df["data"].max().date()

    with st.expander("🔍 Filtros de Atendimento Encadeados", expanded=True):
        col1, col2, col3 = st.columns(3)
        col4, col5, col6 = st.columns(3)

        with col1:
            mes_selecionado = st.selectbox(
                "Mês:",
                ["Todos"] + metricas_iniciais["opcoes_meses"],
                index=0,
                help="Filtre por um mês específico do histórico"
            )

        with col2:
            data_inicio = st.date_input(
                "Data Inicial:",
                value=min_date,
                min_value=min_date,
                max_value=max_date,
                help="Data de início do período"
            )

        with col3:
            data_fim = st.date_input(
                "Data Final:",
                value=max_date,
                min_value=min_date,
                max_value=max_date,
                help="Data final do período"
            )

        with col4:
            # Recalcula opções com base no filtro prévio para garantir reatividade
            temp_metricas = calcular_metricas_encadeadas(
                df, 
                mes_selecionado=mes_selecionado, 
                data_inicio=data_inicio, 
                data_fim=data_fim
            )
            demanda_selecionada = st.selectbox(
                "Demanda / Assunto:",
                ["Todas"] + temp_metricas["opcoes_demandas"],
                index=0,
                help="Filtre por tipo de demanda ou assunto"
            )

        with col5:
            temp_metricas_c = calcular_metricas_encadeadas(
                df, 
                mes_selecionado=mes_selecionado, 
                data_inicio=data_inicio, 
                data_fim=data_fim, 
                demanda_selecionada=demanda_selecionada
            )
            consultor_selecionado = st.selectbox(
                "Consultor:",
                ["Todos"] + temp_metricas_c["opcoes_consultores"],
                index=0,
                help="Filtre pelo consultor responsável"
            )

        with col6:
            temp_metricas_u = calcular_metricas_encadeadas(
                df, 
                mes_selecionado=mes_selecionado, 
                data_inicio=data_inicio, 
                data_fim=data_fim, 
                demanda_selecionada=demanda_selecionada,
                consultor_selecionado=consultor_selecionado
            )
            ug_selecionada = st.selectbox(
                "Unidade Gestora (UG):",
                ["Todas"] + temp_metricas_u["opcoes_ugs"],
                index=0,
                help="Filtre pela Unidade Gestora solicitante"
            )

        # Filtro de Status
        temp_metricas_s = calcular_metricas_encadeadas(
            df, 
            mes_selecionado=mes_selecionado, 
            data_inicio=data_inicio, 
            data_fim=data_fim, 
            demanda_selecionada=demanda_selecionada,
            consultor_selecionado=consultor_selecionado,
            ug_selecionada=ug_selecionada
        )
        status_selecionado = st.selectbox(
            "Status do Atendimento:",
            ["Todos"] + temp_metricas_s["opcoes_status"],
            index=0,
            help="Filtre pelo status do atendimento"
        )

    # Cálculo final das métricas com todos os filtros ativos
    metricas = calcular_metricas_encadeadas(
        df,
        mes_selecionado=mes_selecionado,
        data_inicio=data_inicio,
        data_fim=data_fim,
        demanda_selecionada=demanda_selecionada,
        consultor_selecionado=consultor_selecionado,
        ug_selecionada=ug_selecionada,
        status_selecionado=status_selecionado
    )

    graficos = gerar_graficos_encadeadas(metricas)

    # Exibição das Badges de Período
    st.badge(f"Primeiro Dia: {metricas['primeiro_dia']}", icon="📅", color="red")
    st.badge(f"Último Dia: {metricas['ultimo_dia']}", icon="📅", color="red")

    # Cards de Métricas Solicitados
    m1, m2, m3 = st.columns(3)

    m1.metric(
        label="Total de Atendimentos",
        value=metricas["quant_atendimentos"],
        help="Quantidade total de atendimentos de acordo com a combinação de filtros selecionada",
        border=True
    )
    m2.metric(
        label="Tempo Médio de Atendimento",
        value=metricas["tempo_medio_atendimento"],
        help="Duração média dos atendimentos no subconjunto filtrado",
        border=True
    )
    m3.metric(
        label="Tempo Médio de Espera",
        value=metricas["tempo_medio_espera"],
        help="Tempo médio de espera dos atendimentos no subconjunto filtrado",
        border=True
    )

    st.markdown("---")

    # Gráficos (Opção C)
    st.header("Indicadores Gráficos")

    if graficos.get("fig_evolucao"):
        with st.container(border=True):
            st.plotly_chart(figure_or_data=graficos["fig_evolucao"], width="stretch")

    col_g1, col_g2 = st.columns(2)
    if graficos.get("fig_demanda"):
        with col_g1:
            with st.container(border=True):
                st.plotly_chart(figure_or_data=graficos["fig_demanda"], width="stretch")

    if graficos.get("fig_status"):
        with col_g2:
            with st.container(border=True):
                st.plotly_chart(figure_or_data=graficos["fig_status"], width="stretch")

    st.markdown("---")

    # Tabela Detalhada dos Atendimentos (Opção C)
    st.header("Tabela Detalhada dos Atendimentos Filtrados")
    
    df_tabela = metricas.get("df_tabela_detalhada")

    if df_tabela is not None and not df_tabela.empty:
        st.dataframe(df_tabela, width="stretch", hide_index=True)
    else:
        st.info("Nenhum registro encontrado para a combinação de filtros selecionada.")
