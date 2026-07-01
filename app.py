import pandas as pd
import streamlit as st
from data.loader import carregar_dados
from core.processor import processar_dados
from pages import Metricas_Gerais, Metricas_Consultor, Metricas_Demandas, Metricas_Temporais, Metricas_UG
from components.footer import redenrizar_footer

st.set_page_config(
    page_title="Insight Contag", 
    page_icon="🧮", 
    layout="wide"
)

URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRQuV0BuETouydsDkAJJKSXBs_vJFxCsD8zrDndHFhuKgffHIlSC-fALfsZVdQwT7erZj4sX0ZwHaVr/pub?output=csv"

@st.cache_data(ttl=300)
def carregar_dados_cached() -> pd.DataFrame:
    return carregar_dados(URL)

df_raw = carregar_dados_cached()
df, linhas = processar_dados(df_raw) # Retorna o Dataframe limpo e número de linhas excluídas

if "df" not in st.session_state:
    st.session_state["df"] = df

paginas = st.navigation(
    [
        st.Page(Metricas_Gerais, title="Métricas Gerais", icon=":material/home:"),
        st.Page(Metricas_Consultor, title="Métricas por Consultor", icon=":material/person:"),
        st.Page(Metricas_Demandas, title="Métricas por Demanda", icon=":material/subject:"),
        st.Page(Metricas_UG, title="Métricas por UG", icon=":material/corporate_fare:"),
        st.Page(Metricas_Temporais, title="Métricas por Tempo", icon=":material/calendar_clock:")
    ]
)

paginas.run()
redenrizar_footer()