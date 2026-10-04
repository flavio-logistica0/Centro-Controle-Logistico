import pandas as pd
from pathlib import Path

DATA = Path("data")

arquivos = {
    "pedidos": "pedidos.csv",
    "produtos": "produtos.csv",
    "entregas": "entregas.csv",
    "transportadoras": "transportadoras.csv",
    "estoque": "estoque.csv",
    "armazem": "armazem.csv"
}

print("Iniciando ETL...\n")

for nome, arquivo in arquivos.items():

    caminho = DATA / arquivo

    df = pd.read_csv(caminho)

    antes = len(df)

    # Remove duplicidades
    df = df.drop_duplicates()

    # Converte datas quando existirem
    for coluna in df.columns:
        if "data" in coluna:
            df[coluna] = pd.to_datetime(
                df[coluna],
                errors="coerce"
            )

    # Remove linhas completamente vazias
    df = df.dropna(how="all")

    saida = DATA / f"{nome}_clean.csv"

    df.to_csv(
        saida,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"{nome:<18} "
        f"{antes:>7} → {len(df):>7} registros"
    )

print("\nETL concluído com sucesso!")