import locale
import pandas as pd
from utils.formatter import formatar_timedelta
from metrics.base import extrair_intervalo_datas, calcular_frequencia, calcular_tempo_medio_por_grupo

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

def calcular_metricas_por_demanda(df: pd.DataFrame, demanda_selecionada: str = None) -> dict:
    """
    Calcula métricas agregadas de demandas e estatísticas da demanda selecionada.

    Args:
        df: DataFrame contendo os dados brutos de atendimentos.
        demanda_selecionada: Nome da demanda/assunto selecionado para detalhamento.

    Returns:
        dict: Dicionário contendo DataFrames para gráficos e estatísticas da demanda selecionada.
    """
    if df.empty:
        return {
            "df_top_demandas_demoradas": pd.DataFrame(columns=["demanda_assunto", "tempo_medio"]),
            "df_top_demandas_recorrentes": pd.DataFrame(columns=["demanda_assunto", "count"]),
            "metricas_filtradas": {}
        }

    # Top 10 demandas mais demoradas em minutos
    df_top_demandas_demoradas = calcular_tempo_medio_por_grupo(
        df, 
        coluna_grupo="demanda_assunto", 
        coluna_tempo="tempo_decorrido", 
        em_minutos=True, 
        top_n=10
    )

    # Top 10 demandas mais recorrentes
    df_top_demandas_recorrentes = calcular_frequencia(df, "demanda_assunto", top_n=10)

    # Métricas da demanda selecionada (se houver)
    metricas_filtradas = {}
    if demanda_selecionada:
        df_filtrado = df[df["demanda_assunto"] == demanda_selecionada]
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

            # Consultor Especialista (mais frequente na demanda selecionada)
            df_consultores_demanda = calcular_frequencia(df_filtrado, "consultor")
            consultor_especialista = df_consultores_demanda.iloc[0]["consultor"] if not df_consultores_demanda.empty else "N/A"

            # Top 10 UGs mais solicitantes da demanda selecionada
            df_top_ugs_demanda = calcular_frequencia(df_filtrado, "ug_solicitante", top_n=10)

            metricas_filtradas = {
                "quant_atendimentos": quant_atendimentos,
                "media_mensal": media_mensal,
                "media_diaria": media_diaria,
                "tempo_medio_atendimento": tempo_medio_atendimento,
                "tempo_medio_espera": tempo_medio_espera,
                "primeiro_dia": primeiro_dia,
                "ultimo_dia": ultimo_dia,
                "consultor_especialista": consultor_especialista,
                "df_top_ugs_demanda": df_top_ugs_demanda
            }

    return {
        "df_top_demandas_demoradas": df_top_demandas_demoradas,
        "df_top_demandas_recorrentes": df_top_demandas_recorrentes,
        "metricas_filtradas": metricas_filtradas
    }