import pandas as pd
import plotly.express as px
import locale

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

def processar_dados(data_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Essa função realiza a limpeza e padronização de dados recebidos do loader.

    Args:
        data_raw: Dataframe bruto com os dados extraídos da planilha.

    Returns:
        Retorna um DataFrame limpo e padronizado com os dados extraídos, e o número de linhas descartadas.
    """
    # Remove a primeira coluna vazia
    df = data_raw.drop(columns="Unnamed: 0")

    # Quantidade de linhas antes da limpeza
    linhas_antes = df.shape[0]

    # Remove espaços nos nomes das colunas
    df.columns = df.columns.str.strip()

    # Renomeia as colunas para padronizar os nomes
    df = df.rename(columns={
        "Data": "data",
        "Hora do Contato": "hora_do_contato",
        "Hora Início": "hora_inicio",
        "Hora Fim": "hora_fim",
        "Tempo Decorrido": "tempo_decorrido",
        "Demanda/Assunto": "demanda_assunto",
        "Consultor": "consultor",
        "Nome do Servidor UG": "nome_do_servidor_ug",
        "UG do Solicitante": "ug_solicitante",
        "Status da Demanda": "status_da_demanda",
        "Observação": "observacao"
    })

    # Remove a coluna de observação por falta de utilidade no projeto
    df = df.drop(columns="observacao")

    # Padroniza os tipos de dados de acordo com a coluna
    df["data"] = pd.to_datetime(df["data"].str.strip(), format="%d/%m/%Y", errors="coerce")
    df[["hora_do_contato", "hora_inicio", "hora_fim", "tempo_decorrido"]] = df[["hora_do_contato", "hora_inicio", "hora_fim", "tempo_decorrido"]].apply(lambda x: pd.to_timedelta(x, errors="coerce"))

    # Calcula o tempo decorrido de atendimento
    df["tempo_decorrido"] = df["hora_fim"] - df["hora_inicio"]

    # Adiciona a coluna que calcula o tempo de espera
    df["tempo_de_espera"] = pd.to_timedelta(df["hora_inicio"] - df["hora_do_contato"])

    # Padroniza labels de atendimento
    df[["demanda_assunto", "status_da_demanda"]] = df[["demanda_assunto", "status_da_demanda"]].apply(lambda x: x.str.strip().str.capitalize())
    df[["consultor", "ug_solicitante"]] = df[["consultor", "ug_solicitante"]].apply(lambda x: x.str.strip())

    # Limpeza de linhas inválidas
    # Essa limpeza é feita de acordo com os parâmetros que foram escolhidos como indispensáveis para a análise
    df = df.dropna(subset=["data", "hora_do_contato", "status_da_demanda", "consultor", "ug_solicitante"])

    # Quantidade de linhas descartadas após a limpeza
    linhas_invalidas = linhas_antes - df.shape[0]

    return df, linhas_invalidas


if __name__ == "__main__":
    from data.loader import carregar_dados

    URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS6iPvFOVToRP1TXQ8FxzEgEuw_ryVqdi8B50sZE5H7el4kbSd2BFr5akuI8S8_V2yn7JjEP4EQog0X/pub?output=csv"

    df_raw = carregar_dados(URL)

    df, linhas = processar_dados(df_raw)

    resultado = df.groupby('demanda_assunto')['tempo_decorrido'].mean().reset_index().sort_values('tempo_decorrido', ascending=False)

    print(resultado)
