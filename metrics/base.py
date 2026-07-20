import pandas as pd

def converter_timedelta_para_minutos(series: pd.Series) -> pd.Series:
    """
    Converte uma Series de Timedelta para minutos (float).
    """
    return series.dt.total_seconds() / 60.0

def calcular_frequencia(df: pd.DataFrame, coluna: str, top_n: int = None) -> pd.DataFrame:
    """
    Gera um DataFrame com a contagem de ocorrências de uma coluna ordenada de forma decrescente.
    """
    if df.empty or coluna not in df.columns:
        return pd.DataFrame(columns=[coluna, "count"])
    
    resultado = df[coluna].value_counts().reset_index()
    if top_n:
        resultado = resultado.head(top_n)
    return resultado

def calcular_tempo_medio_por_grupo(
    df: pd.DataFrame, 
    coluna_grupo: str, 
    coluna_tempo: str = "tempo_decorrido", 
    em_minutos: bool = True, 
    top_n: int = None
) -> pd.DataFrame:
    """
    Calcula a média de um campo de tempo agrupado por outra coluna, ordenando do maior para o menor.
    """
    if df.empty or coluna_grupo not in df.columns or coluna_tempo not in df.columns:
        return pd.DataFrame(columns=[coluna_grupo, "tempo_medio"])
    
    temp_df = df.copy()
    if em_minutos:
        temp_df["tempo_calculo"] = converter_timedelta_para_minutos(temp_df[coluna_tempo])
    else:
        temp_df["tempo_calculo"] = temp_df[coluna_tempo]
        
    resultado = (
        temp_df.groupby(coluna_grupo)["tempo_calculo"]
        .mean()
        .reset_index()
        .rename(columns={"tempo_calculo": "tempo_medio"})
        .sort_values(by="tempo_medio", ascending=False)
    )
    
    if top_n:
        resultado = resultado.head(top_n)
        
    return resultado

def extrair_intervalo_datas(df: pd.DataFrame, coluna_data: str = "data") -> tuple[str, str]:
    """
    Retorna o primeiro e o último dia formatados no padrão dd/mm/yy.
    """
    if df.empty or coluna_data not in df.columns:
        return "N/A", "N/A"
        
    dias_limpos = df[coluna_data].dt.to_period("D")
    primeiro_dia = dias_limpos.min().strftime("%d/%m/%y")
    ultimo_dia = dias_limpos.max().strftime("%d/%m/%y")
    return primeiro_dia, ultimo_dia
