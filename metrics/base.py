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

def calcular_variacao_mensal(df: pd.DataFrame) -> dict:
    """
    Calcula as variações de volume de atendimentos e tempos médios entre o mês mais recente
    e o mês imediatamente anterior na base de dados.
    """
    if df.empty or "data" not in df.columns:
        return {
            "delta_atendimentos": None,
            "delta_tempo_espera": None,
            "delta_tempo_atendimento": None
        }

    temp_df = df.copy()
    temp_df["periodo"] = temp_df["data"].dt.to_period("M")
    periodos_ordenados = sorted(temp_df["periodo"].unique())

    if len(periodos_ordenados) < 2:
        return {
            "delta_atendimentos": None,
            "delta_tempo_espera": None,
            "delta_tempo_atendimento": None
        }

    periodo_atual = periodos_ordenados[-1]
    periodo_anterior = periodos_ordenados[-2]

    df_atual = temp_df[temp_df["periodo"] == periodo_atual]
    df_anterior = temp_df[temp_df["periodo"] == periodo_anterior]

    # Variação de volume de atendimentos
    vol_atual = len(df_atual)
    vol_anterior = len(df_anterior)
    if vol_anterior > 0:
        pct_vol = round(((vol_atual - vol_anterior) / vol_anterior) * 100, 1)
        sign = "+" if pct_vol > 0 else ""
        delta_atendimentos = f"{sign}{pct_vol}% vs mês anterior"
    else:
        delta_atendimentos = None

    # Variação de tempo de espera (em minutos)
    espera_atual_min = converter_timedelta_para_minutos(df_atual["tempo_de_espera"]).mean() if "tempo_de_espera" in df_atual.columns else 0
    espera_anterior_min = converter_timedelta_para_minutos(df_anterior["tempo_de_espera"]).mean() if "tempo_de_espera" in df_anterior.columns else 0
    diff_espera = round(espera_atual_min - espera_anterior_min, 1)
    sign_espera = "+" if diff_espera > 0 else ""
    delta_tempo_espera = f"{sign_espera}{diff_espera} min vs mês anterior" if not pd.isna(diff_espera) else None

    # Variação de tempo de atendimento (em minutos)
    atend_atual_min = converter_timedelta_para_minutos(df_atual["tempo_decorrido"]).mean() if "tempo_decorrido" in df_atual.columns else 0
    atend_anterior_min = converter_timedelta_para_minutos(df_anterior["tempo_decorrido"]).mean() if "tempo_decorrido" in df_anterior.columns else 0
    diff_atend = round(atend_atual_min - atend_anterior_min, 1)
    sign_atend = "+" if diff_atend > 0 else ""
    delta_tempo_atendimento = f"{sign_atend}{diff_atend} min vs mês anterior" if not pd.isna(diff_atend) else None

    return {
        "delta_atendimentos": delta_atendimentos,
        "delta_tempo_espera": delta_tempo_espera,
        "delta_tempo_atendimento": delta_tempo_atendimento
    }
