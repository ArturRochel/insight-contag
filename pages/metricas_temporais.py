import streamlit as st

def Metricas_Temporais():

    """
    Função que exibe a página de métricas temporais. Nessa página serão exibidos os dados a partir da escolha de um período de tempo. Exemplo: Horário de pico, dias mais movimentados e filtros de seleção por período.

    Args:
        None
    Returns:
        None
    """

    st.title("Métricas por Período")
    st.write("Nessa tela serão exibidas métricas específica de tempo, como horário de pico, dias mais movimentados ou filtros de seleção por perído.")