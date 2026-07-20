from .gerais import gerar_graficos_gerais
from .por_consultor import gerar_graficos_por_consultor
from .por_demanda import gerar_graficos_por_demanda, gerar_grafico_ugs_por_demanda
from .por_ug import gerar_graficos_por_ug
from .temporais import gerar_graficos_temporais

__all__ = [
    "gerar_graficos_gerais",
    "gerar_graficos_por_consultor",
    "gerar_graficos_por_demanda",
    "gerar_grafico_ugs_por_demanda",
    "gerar_graficos_por_ug",
    "gerar_graficos_temporais"
]