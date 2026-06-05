import pandas as pd

def processar_dados(data_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Essa função realiza a limpeza e padronização de dados.

    Args:
        data_raw: Dataframe bruto com os dados extraídos da planilha.

    Returns:
        Retorna um DataFrame limpo e padronizado com os dados extraídos.
    """
    df = data_raw.drop(columns=0)

    # Renomeia as colunas 
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

    # Padroniza os tipos de dados de acordo com a coluna
    df["data"] = pd.to_datetime(df["data"], dayfirst=True, errors="coerce")
    df[["hora_do_contato", "hora_inicio", "hora_fim", "tempo_decorrido"]] = df[["hora_do_contato", "hora_inicio", "hora_fim", "tempo_decorrido"]].apply(lambda x: pd.to_timedelta(x, errors="coerce"))

    # Adiciona a coluna que calcula o tempo de espera
    df["tempo_de_espera"] = df["hora_inicio"] - df["hora_do_contato"]

    # Padroniza labels de atendimento
    # todo - Utilizar o applu: lambda para padronizar todos os campos de label
    df["demanda_assunto"] = df["demanda_assunto"].str.strip().str.capitalize()
    df["status"] = df["status"].str.strip().str.capitalize()

    # Limpeza de linhas
    df = df.dropna(subset=[["hora_do_contato", "hora_inicio", "hora_fim"]])