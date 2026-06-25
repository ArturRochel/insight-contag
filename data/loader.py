import pandas as pd

def carregar_dados(url: str) -> pd.DataFrame:
    """
    Essa função extrai os dados da planilha pública.

    Args:
        url: URL pública de acesso a planilha no Google Sheets no formato CSV.

    Returns:
        Retorna um DataFrame bruto com os dados extraídos
    """
    df_raw = pd.read_csv(url, skiprows=1, dtype=str)
    return df_raw