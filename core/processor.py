import pandas as pd
import unicodedata

def _normalizar_coluna(col: str) -> str:
    col_str = str(col).strip().lower()
    col_str = "".join(c for c in unicodedata.normalize("NFD", col_str) if unicodedata.category(c) != "Mn")
    if col_str == "data":
        return "data"
    elif "contato" in col_str:
        return "hora_do_contato"
    elif "inicio" in col_str:
        return "hora_inicio"
    elif "fim" in col_str:
        return "hora_fim"
    elif "tempo decorrido" in col_str:
        return "tempo_decorrido"
    elif "demanda" in col_str and ("assunto" in col_str or "/" in col_str):
        return "demanda_assunto"
    elif "consultor" in col_str:
        return "consultor"
    elif "servidor" in col_str:
        return "nome_do_servidor_ug"
    elif "ug" in col_str and "solicitante" in col_str:
        return "ug_solicitante"
    elif "status" in col_str:
        return "status_da_demanda"
    elif "observa" in col_str:
        return "observacao"
    return str(col).strip()

def processar_dados(data_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Essa função realiza a limpeza e padronização de dados recebidos do loader.

    Args:
        data_raw: Dataframe bruto com os dados extraídos da planilha.

    Returns:
        Retorna um DataFrame limpo e padronizado com os dados extraídos, e o número de linhas descartadas.
    """
    # Remove a primeira coluna vazia se existir
    cols_to_drop = [col for col in data_raw.columns if pd.isna(col) or str(col).startswith("Unnamed:") or str(col).strip() == ""]
    df = data_raw.drop(columns=cols_to_drop, errors="ignore").copy()

    # Quantidade de linhas antes da limpeza
    linhas_antes = df.shape[0]

    # Renomeia as colunas de forma robusta e tolerante a variações
    df.columns = [_normalizar_coluna(col) for col in df.columns]

    # Remove a coluna de observação por falta de utilidade no projeto
    df = df.drop(columns="observacao", errors="ignore")

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
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from data.loader import carregar_dados

    URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS6iPvFOVToRP1TXQ8FxzEgEuw_ryVqdi8B50sZE5H7el4kbSd2BFr5akuI8S8_V2yn7JjEP4EQog0X/pub?output=csv"

    df_raw = carregar_dados(URL)

    df, linhas = processar_dados(df_raw)

    resultado = df.groupby('demanda_assunto')['tempo_decorrido'].mean().reset_index().sort_values('tempo_decorrido', ascending=False)

    print(resultado)
