from config import HOST, PORTA, BANCO, USUARIO, SENHA
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from pathlib import Path


# ==========================================================
# CONFIGURAÇÃO DO POSTGRESQL
# ==========================================================




# ==========================================================
# PASTA DOS DADOS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


# ==========================================================
# CONEXÃO
# ==========================================================

print("Conectando ao PostgreSQL...")

conexao = psycopg2.connect(
    host=HOST,
    port=PORTA,
    database=BANCO,
    user=USUARIO,
    password=SENHA
)

engine = create_engine(
    "postgresql+psycopg2://",
    creator=lambda: conexao
)

print("Conexão realizada com sucesso!\n")


# ==========================================================
# TABELAS
# ==========================================================

tabelas = {
    "pedidos": "pedidos_clean.csv",
    "produtos": "produtos_clean.csv",
    "entregas": "entregas_clean.csv",
    "transportadoras": "transportadoras_clean.csv",
    "estoque": "estoque_clean.csv",
    "armazem": "armazem_clean.csv"
}


# ==========================================================
# CARREGAMENTO
# ==========================================================

print("Carregando dados no PostgreSQL...\n")

for tabela, arquivo in tabelas.items():

    caminho = DATA_DIR / arquivo

    df = pd.read_csv(caminho)

    df.to_sql(
        tabela,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"{tabela:<20} {len(df):>8,} registros")


# ==========================================================
# FINALIZAÇÃO
# ==========================================================

conexao.close()

print("\n==========================================")
print("DADOS CARREGADOS COM SUCESSO!")
print("==========================================")


