import locale
import pandas as pd
from utils.formatter import formatar_timedelta
from metrics.base import extrair_intervalo_datas, calcular_frequencia

locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")

def calcular_metricas_encadeadas(
    df: pd.DataFrame,
    mes_selecionado: str = None,
    data_inicio = None,
    data_fim = None,
    demanda_selecionada: str = None,
    consultor_selecionado: str = None,
    ug_selecionada: str = None,
    status_selecionado: str = None
) -> dict:
    """
    Calcula as métricas, opções válidas de seletores, gráficos e tabela detalhada 
    com base em filtros encadeados reativos aplicados ao DataFrame.
    """
    if df.empty:
        return {
            "opcoes_meses": [],
            "opcoes_demandas": [],
            "opcoes_consultores": [],
            "opcoes_ugs": [],
            "opcoes_status": [],
            "quant_atendimentos": 0,
            "tempo_medio_atendimento": "0h 0m",
            "tempo_medio_espera": "0h 0m",
            "primeiro_dia": "N/A",
            "ultimo_dia": "N/A",
            "df_evolucao_temporal": pd.DataFrame(columns=["data", "count"]),
            "df_distribuicao_demanda": pd.DataFrame(columns=["demanda_assunto", "count"]),
            "df_distribuicao_status": pd.DataFrame(columns=["status_da_demanda", "count"]),
            "df_tabela_detalhada": pd.DataFrame()
        }

    # DataFrame temporário para manipular meses formatados
    temp_df = df.copy()
    temp_df["mes_fmt"] = temp_df["data"].dt.to_period("M").dt.strftime("%B/%Y").str.capitalize()

    # Aplicação sequencial dos filtros fornecidos
    df_filtrado = temp_df.copy()

    if mes_selecionado and mes_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["mes_fmt"] == mes_selecionado]

    if data_inicio is not None:
        df_filtrado = df_filtrado[df_filtrado["data"].dt.date >= data_inicio]

    if data_fim is not None:
        df_filtrado = df_filtrado[df_filtrado["data"].dt.date <= data_fim]

    if demanda_selecionada and demanda_selecionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado["demanda_assunto"] == demanda_selecionada]

    if consultor_selecionado and consultor_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["consultor"] == consultor_selecionado]

    if ug_selecionada and ug_selecionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado["ug_solicitante"] == ug_selecionada]

    if status_selecionado and status_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["status_da_demanda"] == status_selecionado]

    # Opções válidas atualizadas para os seletores (baseadas no df_filtrado)
    opcoes_meses = sorted(df["data"].dt.to_period("M").dt.strftime("%B/%Y").str.capitalize().dropna().unique().tolist())
    opcoes_demandas = sorted(df_filtrado["demanda_assunto"].dropna().unique().tolist())
    opcoes_consultores = sorted(df_filtrado["consultor"].dropna().unique().tolist())
    opcoes_ugs = sorted(df_filtrado["ug_solicitante"].dropna().unique().tolist())
    opcoes_status = sorted(df_filtrado["status_da_demanda"].dropna().unique().tolist())

    # Indicadores Numéricos
    quant_atendimentos = df_filtrado.shape[0]
    
    if not df_filtrado.empty:
        primeiro_dia, ultimo_dia = extrair_intervalo_datas(df_filtrado)
        tempo_medio_atendimento = formatar_timedelta(df_filtrado["tempo_decorrido"].mean())
        tempo_medio_espera = formatar_timedelta(df_filtrado["tempo_de_espera"].mean())

        # Evolução temporal diária
        df_evolucao_temporal = (
            df_filtrado.groupby(df_filtrado["data"].dt.date)
            .size()
            .reset_index(name="count")
            .rename(columns={"data": "data"})
            .sort_values(by="data")
        )

        # Distribuição por demanda e status
        df_distribuicao_demanda = calcular_frequencia(df_filtrado, "demanda_assunto", top_n=10)
        df_distribuicao_status = calcular_frequencia(df_filtrado, "status_da_demanda")

        # Tabela detalhada tratada para apresentação
        df_tabela_detalhada = df_filtrado.copy()
        df_tabela_detalhada["data"] = df_tabela_detalhada["data"].dt.strftime("%d/%m/%Y")
        if "tempo_decorrido" in df_tabela_detalhada.columns:
            df_tabela_detalhada["tempo_decorrido"] = df_tabela_detalhada["tempo_decorrido"].apply(
                lambda x: formatar_timedelta(x) if pd.notna(x) else "N/A"
            )
        if "tempo_de_espera" in df_tabela_detalhada.columns:
            df_tabela_detalhada["tempo_de_espera"] = df_tabela_detalhada["tempo_de_espera"].apply(
                lambda x: formatar_timedelta(x) if pd.notna(x) else "N/A"
            )
        
        # Renomear colunas da tabela para rótulos legíveis
        df_tabela_detalhada = df_tabela_detalhada.drop(columns=["mes_fmt"], errors="ignore").rename(columns={
            "data": "Data",
            "hora_do_contato": "Hora do Contato",
            "hora_inicio": "Hora Início",
            "hora_fim": "Hora Fim",
            "tempo_decorrido": "Duração do Atendimento",
            "tempo_de_espera": "Tempo de Espera",
            "demanda_assunto": "Demanda/Assunto",
            "consultor": "Consultor",
            "nome_do_servidor_ug": "Servidor da UG",
            "ug_solicitante": "UG Solicitante",
            "status_da_demanda": "Status"
        })
    else:
        primeiro_dia, ultimo_dia = "N/A", "N/A"
        tempo_medio_atendimento = "0h 0m"
        tempo_medio_espera = "0h 0m"
        df_evolucao_temporal = pd.DataFrame(columns=["data", "count"])
        df_distribuicao_demanda = pd.DataFrame(columns=["demanda_assunto", "count"])
        df_distribuicao_status = pd.DataFrame(columns=["status_da_demanda", "count"])
        df_tabela_detalhada = pd.DataFrame()

    return {
        "opcoes_meses": opcoes_meses,
        "opcoes_demandas": opcoes_demandas,
        "opcoes_consultores": opcoes_consultores,
        "opcoes_ugs": opcoes_ugs,
        "opcoes_status": opcoes_status,
        "quant_atendimentos": quant_atendimentos,
        "tempo_medio_atendimento": tempo_medio_atendimento,
        "tempo_medio_espera": tempo_medio_espera,
        "primeiro_dia": primeiro_dia,
        "ultimo_dia": ultimo_dia,
        "df_evolucao_temporal": df_evolucao_temporal,
        "df_distribuicao_demanda": df_distribuicao_demanda,
        "df_distribuicao_status": df_distribuicao_status,
        "df_tabela_detalhada": df_tabela_detalhada
    }
