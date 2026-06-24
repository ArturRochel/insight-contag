import pandas as pd
import streamlit as st
from data.loader import carregar_dados
from core.processor import processar_dados
from ui.charts import graficos_gerais

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
graficos = graficos_gerais(df=df)

st.title("Insights Consultória CONTAG")

# Métricas
st.metric(label="Total de Atendimentos",value=graficos["cards"]["quant_atendimentos"], help="Total de atendimentos desde o início da base de dados")
st.metric(label="Média de Atendimentos Diários",value=graficos["cards"]["media_diaria"], help="Média de atendimentos diários realizados")
st.metric(label="Média de Atendimentos Mensal", value=graficos["cards"]["media_mensal"])
st.metric(label="Tempo Médio de Espera", value=graficos["cards"]["tempo_medio_espera"])
st.metric(label="Tempo Médio de Atendimento", value=graficos["cards"]["tempo_medio_atendimento"])

# Gráficos
st.plotly_chart(figure_or_data=graficos["graficos"]["atendimentos_mes"])
st.plotly_chart(figure_or_data=graficos["graficos"]["atendimentos_dia"])