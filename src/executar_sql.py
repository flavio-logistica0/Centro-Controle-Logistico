from config import HOST, PORTA, BANCO, USUARIO, SENHA
import psycopg2
import pandas as pd
from pathlib import Path


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================




# ==========================================================
# ARQUIVO SQL
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO_SQL = BASE_DIR / "sql" / "kpis_logisticos.sql"


# ==========================================================
# CONEXÃO
# ==========================================================

conexao = psycopg2.connect(
    host=HOST,
    port=PORTA,
    database=BANCO,
    user=USUARIO,
    password=SENHA
)


# ==========================================================
# LEITURA DO SQL
# ==========================================================

sql = ARQUIVO_SQL.read_text(encoding="utf-8")

consultas = [
    consulta.strip()
    for consulta in sql.split(";")
    if consulta.strip()
]


# ==========================================================
# EXECUÇÃO
# ==========================================================

print("\n==========================================")
print("CENTRO DE CONTROLE LOGÍSTICO")
print("==========================================\n")

for numero, consulta in enumerate(consultas, start=1):

    try:

        df = pd.read_sql_query(
            consulta,
            conexao
        )

        print(f"--- KPI {numero} ---")
        print(df.to_string(index=False))
        print()

    except Exception as erro:

        print(f"Erro no KPI {numero}:")
        print(erro)
        print()


conexao.close()

print("==========================================")
print("ANÁLISE CONCLUÍDA!")
print("==========================================")


