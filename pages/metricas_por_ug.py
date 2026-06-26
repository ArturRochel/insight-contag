import streamlit as st

def Metricas_UG():

    """
    Função que exibe a página de métricas por Unidade Gestora. Nessa página serão exibidos os dados a partir da escolha de uma Unidade Gestora. Exemplo: Demandas mais frequentes, demandas mais demoradas e tempo médio de cada Unidade Gestora.

    Args:
        None
    Returns:
        None
    """

    st.title("Métricas por UG")
    st.write("Nessa tela uma Unidade Gestora será escolhida em um filtro e as métricas serão calculadas com base nessa UG escolhida.")