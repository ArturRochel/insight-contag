import locale
import pandas as pd
from utils.formatter import formatar_timedelta
from metrics.base import extrair_intervalo_datas, calcular_frequencia

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

DIAS_SEMANA_MAP = {
    0: "Segunda-feira",
    1: "Terça-feira",
    2: "Quarta-feira",
    3: "Quinta-feira",
    4: "Sexta-feira",
    5: "Sábado",
    6: "Domingo"
}

MESES_MAP = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

def calcular_metricas_temporais(df: pd.DataFrame, data_inicio=None, data_fim=None) -> dict:
    """
    Calcula métricas de análise de tempo e sazonalidade dos atendimentos.

    Args:
        df: DataFrame de atendimentos.
        data_inicio: Data inicial para filtragem (opcional).
        data_fim: Data final para filtragem (opcional).

    Returns:
        dict: Estatísticas gerais da base e métricas detalhadas do período filtrado.
    """
    if df.empty:
        return {
            "horario_pico_geral": "N/A",
            "dia_mais_movimentado_geral": "N/A",
            "mes_pico_geral": "N/A",
            "df_curva_dia_geral": pd.DataFrame(columns=["hora_str", "media_atendimentos"]),
            "metricas_filtradas": {}
        }

    df_base = df.copy()
    primeiro_dia_geral, ultimo_dia_geral = extrair_intervalo_datas(df_base)

    if "hora_do_contato" in df_base.columns:
        df_base["hora"] = df_base["hora_do_contato"].dt.components["hours"]
    else:
        df_base["hora"] = 0

    total_dias_base = df_base["data"].dt.to_period("D").nunique()
    total_dias_base = max(total_dias_base, 1)

    # 1. Horário de Pico Geral
    atendimentos_por_hora = df_base["hora"].value_counts()
    if not atendimentos_por_hora.empty:
        hora_pico = atendimentos_por_hora.idxmax()
        horario_pico_geral = f"{hora_pico:02d}h:00 - {hora_pico+1:02d}h:00"
    else:
        horario_pico_geral = "N/A"

    # 2. Dia Mais Movimentado Geral (Segunda a Sexta)
    df_base["dayofweek"] = df_base["data"].dt.dayofweek
    df_dias_uteis = df_base[df_base["dayofweek"].isin([0, 1, 2, 3, 4])]
    if not df_dias_uteis.empty:
        top_day_code = df_dias_uteis["dayofweek"].value_counts().idxmax()
        dia_mais_movimentado_geral = DIAS_SEMANA_MAP.get(top_day_code, "N/A")
    else:
        dia_mais_movimentado_geral = "N/A"

    # 3. Mês de Pico Geral
    df_base["mes_num"] = df_base["data"].dt.month
    top_mes_code = df_base["mes_num"].value_counts().idxmax() if not df_base["mes_num"].empty else 1
    mes_pico_geral = MESES_MAP.get(top_mes_code, "N/A")

    # 4. DataFrame Curva do Dia Geral (7h às 18h)
    horas_range = list(range(7, 19))
    curva_dados = []
    for h in horas_range:
        qtd = (df_base["hora"] == h).sum()
        media_h = round(qtd / total_dias_base, 2)
        curva_dados.append({"hora_str": f"{h:02d}:00", "media_atendimentos": media_h})
    df_curva_dia_geral = pd.DataFrame(curva_dados)

    # 5. Filtragem por Intervalo de Datas
    df_filtrado = df.copy()
    if data_inicio is not None:
        df_filtrado = df_filtrado[df_filtrado["data"].dt.date >= data_inicio]
    if data_fim is not None:
        df_filtrado = df_filtrado[df_filtrado["data"].dt.date <= data_fim]

    metricas_filtradas = {}
    if not df_filtrado.empty:
        primeiro_dia, ultimo_dia = extrair_intervalo_datas(df_filtrado)
        quant_atendimentos = len(df_filtrado)

        dias_unicos = df_filtrado["data"].dt.to_period("D").nunique()
        meses_unicos = df_filtrado["data"].dt.to_period("M").nunique()

        media_diaria = round(quant_atendimentos / dias_unicos, 2) if dias_unicos > 0 else 0
        media_mensal = round(quant_atendimentos / meses_unicos, 2) if meses_unicos > 0 else 0

        tempo_medio_espera = formatar_timedelta(df_filtrado["tempo_de_espera"].mean())
        tempo_medio_atendimento = formatar_timedelta(df_filtrado["tempo_decorrido"].mean())
        tempo_total_atendimento = formatar_timedelta(df_filtrado["tempo_decorrido"].sum())

        df_ug = calcular_frequencia(df_filtrado, "ug_solicitante")
        ug_mais_recorrente = df_ug.iloc[0]["ug_solicitante"] if not df_ug.empty else "N/A"

        df_demanda = calcular_frequencia(df_filtrado, "demanda_assunto")
        demanda_mais_recorrente = df_demanda.iloc[0]["demanda_assunto"] if not df_demanda.empty else "N/A"

        df_consultor = calcular_frequencia(df_filtrado, "consultor")
        consultor_mais_atendimentos = df_consultor.iloc[0]["consultor"] if not df_consultor.empty else "N/A"

        # Volume diário para o gráfico de linha no período filtrado
        df_volume_diario = (
            df_filtrado.groupby(df_filtrado["data"].dt.date)
            .size()
            .reset_index(name="count")
            .rename(columns={"data": "data"})
            .sort_values(by="data")
        )

        metricas_filtradas = {
            "primeiro_dia": primeiro_dia,
            "ultimo_dia": ultimo_dia,
            "quant_atendimentos": quant_atendimentos,
            "media_diaria": media_diaria,
            "media_mensal": media_mensal,
            "tempo_medio_espera": tempo_medio_espera,
            "tempo_medio_atendimento": tempo_medio_atendimento,
            "tempo_total_atendimento": tempo_total_atendimento,
            "ug_mais_recorrente": ug_mais_recorrente,
            "demanda_mais_recorrente": demanda_mais_recorrente,
            "consultor_mais_atendimentos": consultor_mais_atendimentos,
            "df_volume_diario": df_volume_diario
        }

    return {
        "primeiro_dia": primeiro_dia_geral,
        "ultimo_dia": ultimo_dia_geral,
        "horario_pico_geral": horario_pico_geral,
        "dia_mais_movimentado_geral": dia_mais_movimentado_geral,
        "mes_pico_geral": mes_pico_geral,
        "df_curva_dia_geral": df_curva_dia_geral,
        "metricas_filtradas": metricas_filtradas
    }

