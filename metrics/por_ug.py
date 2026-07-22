import locale
import pandas as pd
from utils.formatter import formatar_timedelta
from metrics.base import extrair_intervalo_datas, calcular_frequencia

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

def calcular_metricas_por_ug(df: pd.DataFrame, ug_selecionada: str = None) -> dict:
    """
    Calcula as métricas de atendimentos agrupadas por Unidade Gestora (UG).

    Args:
        df: DataFrame de atendimentos.
        ug_selecionada: Nome da UG selecionada para filtro.

    Returns:
        dict: Dicionário contendo DataFrames calculados e métricas por UG.
    """
    if df.empty:
        return {
            "df_ugs_solicitantes": pd.DataFrame(columns=["ug_solicitante", "count"]),
            "df_ugs_recorrentes": pd.DataFrame(columns=["ug_solicitante", "count"]),
            "df_ugs_tempo_total": pd.DataFrame(columns=["ug_solicitante", "tempo_total_horas"]),
            "metricas_filtradas": {}
        }

    df_ugs_solicitantes = calcular_frequencia(df, "ug_solicitante")
    df_ugs_recorrentes = calcular_frequencia(df, "ug_solicitante", top_n=10)

    # Top 10 UGs em tempo total de atendimento em horas
    temp_df = df.copy()
    temp_df["tempo_horas"] = temp_df["tempo_decorrido"].dt.total_seconds() / 3600.0
    df_ugs_tempo_total = (
        temp_df.groupby("ug_solicitante")["tempo_horas"]
        .sum()
        .reset_index()
        .rename(columns={"tempo_horas": "tempo_total_horas"})
        .sort_values(by="tempo_total_horas", ascending=False)
        .head(10)
    )
    df_ugs_tempo_total["tempo_total_horas"] = df_ugs_tempo_total["tempo_total_horas"].round(2)

    metricas_filtradas = {}
    if ug_selecionada:
        df_filtrado = df[df["ug_solicitante"] == ug_selecionada]
        if not df_filtrado.empty:
            quant_atendimentos = df_filtrado.shape[0]
            primeiro_dia, ultimo_dia = extrair_intervalo_datas(df_filtrado)
            
            meses_limpos = df_filtrado["data"].dt.to_period('M')
            atendimentos_mes = meses_limpos.value_counts()
            dias_limpos = df_filtrado["data"].dt.to_period('D')
            atendimentos_dia = dias_limpos.value_counts()

            media_diaria = round(quant_atendimentos / len(atendimentos_dia), 2) if len(atendimentos_dia) > 0 else 0
            media_mensal = round(quant_atendimentos / len(atendimentos_mes), 2) if len(atendimentos_mes) > 0 else 0

            tempo_medio_atendimento = formatar_timedelta(df_filtrado["tempo_decorrido"].mean())
            tempo_medio_espera = formatar_timedelta(df_filtrado["tempo_de_espera"].mean())

            # Consultor especialista (mais frequente para esta UG)
            df_consultores_ug = calcular_frequencia(df_filtrado, "consultor")
            consultor_especialista = df_consultores_ug.iloc[0]["consultor"] if not df_consultores_ug.empty else "N/A"

            # Top 10 demandas da UG selecionada
            df_top_demandas_ug = calcular_frequencia(df_filtrado, "demanda_assunto", top_n=10)

            metricas_filtradas = {
                "quant_atendimentos": quant_atendimentos,
                "media_mensal": media_mensal,
                "media_diaria": media_diaria,
                "tempo_medio_atendimento": tempo_medio_atendimento,
                "tempo_medio_espera": tempo_medio_espera,
                "primeiro_dia": primeiro_dia,
                "ultimo_dia": ultimo_dia,
                "consultor_especialista": consultor_especialista,
                "df_top_demandas_ug": df_top_demandas_ug
            }

    return {
        "df_ugs_solicitantes": df_ugs_solicitantes,
        "df_ugs_recorrentes": df_ugs_recorrentes,
        "df_ugs_tempo_total": df_ugs_tempo_total,
        "metricas_filtradas": metricas_filtradas
    }
