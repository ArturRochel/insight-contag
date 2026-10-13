import pandas as pd

def carregar_dados(url: str) -> pd.DataFrame:
    """
    Essa função extrai os dados da planilha pública.
    Detecta dinamicamente a linha de cabeçalho para garantir compatibilidade
    caso haja ou não linhas de título no início da planilha.

    Args:
        url: URL pública de acesso a planilha no Google Sheets no formato CSV.

    Returns:
        Retorna um DataFrame bruto com os dados extraídos
    """
    df_raw = pd.read_csv(url, dtype=str)

    cols_clean = [str(col).strip().lower() for col in df_raw.columns]
    if "data" not in cols_clean:
        for idx, row in df_raw.head(10).iterrows():
            row_vals = [str(val).strip().lower() for val in row.values if pd.notna(val)]
            if "data" in row_vals and any(c in row_vals for c in ["hora do contato", "consultor", "demanda/assunto"]):
                df_raw.columns = df_raw.iloc[idx]
                df_raw = df_raw.iloc[idx + 1:].reset_index(drop=True)
                break

    return df_raw