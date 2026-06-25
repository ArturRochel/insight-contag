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

st.title("Análise de Dados")

a, b, c = st.columns(3)
d, e, f = st.columns(3)
g, h = st.columns(2)

# Métricas
a.metric(label="Total de Atendimentos",value=graficos["cards"]["quant_atendimentos"], help="Total de atendimentos desde o início da base de dados", border=True)

b.metric(label="Média de Atendimentos Diários",value=graficos["cards"]["media_diaria"], help="Média de atendimentos diários realizados", border=True)

c.metric(label="Média de Atendimentos Mensal", value=graficos["cards"]["media_mensal"], help="Média de atendimentos contabilizados ao longo dos meses", border=True)

d.metric(label="Tempo Médio de Espera", value=graficos["cards"]["tempo_medio_espera"], help="Tempo médio de espera pelos atendimentos", border=True)

e.metric(label="Tempo Médio de Atendimento", value=graficos["cards"]["tempo_medio_atendimento"], help="Durtação média dos atendimentos", border=True)

f.metric(label="Tempo Total de Atendimento", value=graficos["cards"]["tempo_total"], help="Soma do tempo de todos os atendimentos", border=True)

g.metric(label="UG mais Recorrente", value=graficos["cards"]["ug_mais_recorrente"]["ug_solicitante"], help="Unidade Gestora que mais recorre a consultoria", border=True)

h.metric(label="Demanda mais Recorrente", value=graficos["cards"]["demanda_mais_recorrente"]["demanda_assunto"], help="Demanda mais presente nos atendimentos", border=True)

st.markdown("---")

st.header("Indicadores Gráficos")

# Gráficos
st.plotly_chart(figure_or_data=graficos["graficos"]["atendimentos_consultores"])
st.plotly_chart(figure_or_data=graficos["graficos"]["atendimentos_mes"])
st.plotly_chart(figure_or_data=graficos["graficos"]["atendimentos_dia"])
