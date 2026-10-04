# Centro de Controle Logístico

Projeto de análise e controle logístico desenvolvido com Python, SQL e PostgreSQL.

## 🎯 Objetivo

Simular o cenário de uma empresa que recebe dados operacionais exportados de sistemas como ERP e transforma esses dados em informações úteis para tomada de decisão.

O projeto realiza:

- Geração de dados logísticos simulados
- Tratamento e limpeza dos dados
- Processo ETL com Python
- Armazenamento no PostgreSQL
- Análise com SQL
- Cálculo de indicadores logísticos
- Análise de transportadoras
- Identificação de problemas operacionais
- Geração automática de relatório executivo em PDF

## 🏗️ Arquitetura

CSV → Python / ETL → PostgreSQL → SQL / KPIs → Análise → Relatório Executivo

## 🛠️ Tecnologias

- Python
- Pandas
- NumPy
- PostgreSQL
- SQL
- SQLAlchemy
- Psycopg2
- Python-dotenv
- ReportLab
- Git / GitHub

## 📊 Indicadores analisados

### Transporte

- OTIF
- Taxa de atraso
- Custo médio por entrega
- Performance das transportadoras

### Estoque

- Produtos críticos
- Estoque parado
- Ruptura / risco de estoque

### Armazém

- Pedidos separados
- Erros de picking
- Taxa de erro
- Avarias

### Pedidos

- Total de pedidos
- Pedidos pendentes
- Pedidos cancelados

## 🔎 Principais resultados da simulação

O conjunto de dados utilizado contém:

- 30.000 pedidos
- 30.000 entregas
- 500 produtos
- 10 transportadoras
- 500 registros de estoque
- 10.000 operações de armazém

Entre os principais resultados encontrados:

- OTIF abaixo da meta operacional
- Elevada taxa de entregas atrasadas
- Alto volume de estoque parado
- Produtos em situação crítica
- Erros de picking identificados
- Avarias identificadas

A análise das transportadoras permite verificar se o problema está concentrado em uma transportadora específica ou se representa um problema estrutural da operação.

## 📁 Estrutura

```text
Centro-Controle-Logistico/
│
├── data/
│   └── arquivos CSV
│
├── src/
│   ├── gerar_dados.py
│   ├── etl.py
│   ├── config.py
│   ├── carregar_postgres.py
│   ├── executar_sql.py
│   ├── centro_controle.py
│   ├── analise_transportadoras.py
│   └── gerar_relatorio.py
│
├── sql/
│   └── kpis_logisticos.sql
│
├── reports/
│   └── relatorio_executivo_logistico.pdf
│
├── tests/
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md