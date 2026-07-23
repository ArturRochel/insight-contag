import pandas as pd
import streamlit as st
from data.loader import carregar_dados
from core.processor import processar_dados
from pages import Metricas_Gerais, Metricas_Consultor, Metricas_Demandas, Metricas_Temporais, Metricas_UG
from components.footer import redenrizar_footer

def check_password():
    """Retorna True se o usuário digitou a senha correta."""
    
    def password_entered():
        """Checa se a senha digitada é igual à configurada nos secrets."""
        if st.session_state["password"] == st.secrets["APP_PASSWORD"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    st.title("🔒 Acesso Restrito")
    st.text_input(
        "Digite a senha para acessar o projeto:", 
        type="password", 
        on_change=password_entered, 
        key="password"
    )
    
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("😕 Senha incorreta. Tente novamente.")
        
    return False


if not check_password():
    st.stop()

st.set_page_config(
    page_title="Insight Contag", 
    page_icon="🧮", 
    layout="wide"
)

#! Atualizado dia 07/07/2026
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS6iPvFOVToRP1TXQ8FxzEgEuw_ryVqdi8B50sZE5H7el4kbSd2BFr5akuI8S8_V2yn7JjEP4EQog0X/pub?output=csv"

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