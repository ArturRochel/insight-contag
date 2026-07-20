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
            "metricas_filtradas": {}
        }

    df_ugs_solicitantes = calcular_frequencia(df, "ug_solicitante")

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

            metricas_filtradas = {
                "quant_atendimentos": quant_atendimentos,
                "media_mensal": media_mensal,
                "media_diaria": media_diaria,
                "tempo_medio_atendimento": tempo_medio_atendimento,
                "tempo_medio_espera": tempo_medio_espera,
                "primeiro_dia": primeiro_dia,
                "ultimo_dia": ultimo_dia
            }

    return {
        "df_ugs_solicitantes": df_ugs_solicitantes,
        "metricas_filtradas": metricas_filtradas
    }
