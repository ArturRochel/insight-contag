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

    