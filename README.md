# Insight Contag

Sistema de análise de atendimentos e geração de indicadores operacionais para a CONTAG, desenvolvido em Python com visualização interativa através de Streamlit.

## Sobre o Projeto

O Insight Contag tem como objetivo transformar os dados de atendimentos registrados em planilhas do Google Sheets em informações estratégicas para apoio à tomada de decisão.

A aplicação realiza a extração, tratamento e análise dos dados, disponibilizando dashboards interativos com métricas operacionais, produtividade da equipe e indicadores de atendimento.

## Principais Funcionalidades

* Leitura automática de dados a partir do Google Sheets
* Tratamento e padronização das informações
* Geração de métricas operacionais
* Dashboard interativo com filtros dinâmicos
* Visualização de indicadores de produtividade
* Identificação de gargalos e padrões de atendimento

## Tecnologias

| Tecnologia    | Finalidade                    |
| ------------- | ----------------------------- |
| Python 3.12   | Linguagem principal           |
| Pandas        | Tratamento e análise de dados |
| Plotly        | Visualização gráfica          |
| Streamlit     | Interface web                 |
| Google Sheets | Fonte de dados                |
| MkDocs        | Documentação técnica          |

## Arquitetura Simplificada

```text
Google Sheets
      │
      ▼
   Loader
      │
      ▼
 Processamento
      │
      ▼
   Métricas
      │
      ▼
 Dashboard Streamlit
```

## Métricas Disponíveis

### Gerais

* Total de atendimentos
* Média diária e mensal
* Tempo médio de atendimento
* Tempo médio de espera
* Demandas mais recorrentes
* UGs mais atendidas

### Operacionais

* Produtividade por consultor
* Distribuição de demandas
* Horários de pico
* Evolução temporal dos atendimentos
* Indicadores por Unidade Gestora

## Objetivos

* Automatizar a análise dos atendimentos
* Reduzir o esforço manual de consolidação de dados
* Melhorar a visibilidade operacional
* Apoiar a tomada de decisão da gestão
* Criar uma base para futuras evoluções de BI

## Roadmap

* Integração com PostgreSQL
* APIs com FastAPI
* Exportação de relatórios PDF e Excel
* Atualização em tempo real
* Recursos de Inteligência Artificial
* Evolução para sistema completo de gestão de atendimentos

## Documentação

A documentação completa do projeto está disponível através do MkDocs e contém informações sobre:

* Arquitetura
* Regras de negócio
* Processo de tratamento dos dados
* Métricas e indicadores
* Manual de utilização
* Guia para desenvolvedores
