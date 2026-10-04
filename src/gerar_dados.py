import pandas as pd
import numpy as np
from faker import Faker
from pathlib import Path

fake = Faker("pt_BR")
np.random.seed(42)

# Pasta onde os arquivos serão salvos
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# Quantidades
TOTAL_PEDIDOS = 30000
TOTAL_PRODUTOS = 500
TOTAL_TRANSPORTADORAS = 10
TOTAL_REGISTROS_ESTOQUE = 500
TOTAL_REGISTROS_ARMAZEM = 10000

print("Gerando dados logísticos...")

# ==========================================================
# 1. PRODUTOS
# ==========================================================

categorias = [
    "Eletrônicos",
    "Alimentos",
    "Bebidas",
    "Higiene",
    "Limpeza",
    "Vestuário",
    "Casa",
    "Automotivo"
]

produtos = pd.DataFrame({
    "produto_id": range(1, TOTAL_PRODUTOS + 1),
    "produto": [
        f"Produto {i:04d}"
        for i in range(1, TOTAL_PRODUTOS + 1)
    ],
    "categoria": np.random.choice(categorias, TOTAL_PRODUTOS),
    "preco": np.round(np.random.uniform(10, 2000, TOTAL_PRODUTOS), 2),
    "estoque_minimo": np.random.randint(10, 100, TOTAL_PRODUTOS)
})

produtos.to_csv(DATA_DIR / "produtos.csv", index=False, encoding="utf-8-sig")

# ==========================================================
# 2. TRANSPORTADORAS
# ==========================================================

transportadoras = pd.DataFrame({
    "transportadora_id": range(1, TOTAL_TRANSPORTADORAS + 1),
    "transportadora": [
        f"Transportadora {chr(65 + i)}"
        for i in range(TOTAL_TRANSPORTADORAS)
    ]
})

transportadoras.to_csv(
    DATA_DIR / "transportadoras.csv",
    index=False,
    encoding="utf-8-sig"
)

# ==========================================================
# 3. PEDIDOS
# ==========================================================

data_inicio = pd.Timestamp("2025-01-01")
data_fim = pd.Timestamp("2026-09-30")

datas = pd.to_datetime(
    np.random.randint(
        data_inicio.value // 10**9,
        data_fim.value // 10**9,
        TOTAL_PEDIDOS
    ),
    unit="s"
)

pedidos = pd.DataFrame({
    "pedido_id": range(1, TOTAL_PEDIDOS + 1),
    "cliente_id": np.random.randint(1, 10001, TOTAL_PEDIDOS),
    "produto_id": np.random.randint(1, TOTAL_PRODUTOS + 1, TOTAL_PEDIDOS),
    "data_pedido": datas,
    "quantidade": np.random.randint(1, 20, TOTAL_PEDIDOS),
    "valor_pedido": np.round(
        np.random.uniform(50, 5000, TOTAL_PEDIDOS),
        2
    ),
    "status": np.random.choice(
        ["Entregue", "Em transporte", "Pendente", "Cancelado"],
        TOTAL_PEDIDOS,
        p=[0.70, 0.15, 0.10, 0.05]
    )
})

pedidos.to_csv(
    DATA_DIR / "pedidos.csv",
    index=False,
    encoding="utf-8-sig"
)

# ==========================================================
# 4. ENTREGAS
# ==========================================================

data_pedido = pedidos["data_pedido"]

prazo_dias = np.random.randint(2, 8, TOTAL_PEDIDOS)

data_prometida = data_pedido + pd.to_timedelta(
    prazo_dias,
    unit="D"
)

atrasos = np.random.choice(
    [0, 1, 2, 3, 5, 10],
    TOTAL_PEDIDOS,
    p=[0.65, 0.12, 0.10, 0.06, 0.05, 0.02]
)

data_entrega = data_prometida + pd.to_timedelta(
    atrasos,
    unit="D"
)

quantidade_pedida = pedidos["quantidade"]

quantidade_entregue = np.maximum(
    quantidade_pedida - np.random.choice(
        [0, 0, 0, 1],
        TOTAL_PEDIDOS
    ),
    0
)

entregas = pd.DataFrame({
    "entrega_id": range(1, TOTAL_PEDIDOS + 1),
    "pedido_id": pedidos["pedido_id"],
    "transportadora_id": np.random.randint(
        1,
        TOTAL_TRANSPORTADORAS + 1,
        TOTAL_PEDIDOS
    ),
    "data_prometida": data_prometida,
    "data_entrega": data_entrega,
    "quantidade_pedida": quantidade_pedida,
    "quantidade_entregue": quantidade_entregue,
    "custo_entrega": np.round(
        np.random.uniform(15, 150, TOTAL_PEDIDOS),
        2
    )
})

entregas.to_csv(
    DATA_DIR / "entregas.csv",
    index=False,
    encoding="utf-8-sig"
)

# ==========================================================
# 5. ESTOQUE
# ==========================================================

estoque = pd.DataFrame({
    "estoque_id": range(1, TOTAL_REGISTROS_ESTOQUE + 1),
    "produto_id": np.random.randint(
        1,
        TOTAL_PRODUTOS + 1,
        TOTAL_REGISTROS_ESTOQUE
    ),
    "quantidade_estoque": np.random.randint(
        0,
        1000,
        TOTAL_REGISTROS_ESTOQUE
    ),
    "estoque_minimo": np.random.randint(
        20,
        150,
        TOTAL_REGISTROS_ESTOQUE
    ),
    "dias_sem_movimentacao": np.random.randint(
        0,
        365,
        TOTAL_REGISTROS_ESTOQUE
    )
})

estoque.to_csv(
    DATA_DIR / "estoque.csv",
    index=False,
    encoding="utf-8-sig"
)

# ==========================================================
# 6. ARMAZÉM
# ==========================================================

armazem = pd.DataFrame({
    "operacao_id": range(1, TOTAL_REGISTROS_ARMAZEM + 1),
    "funcionario_id": np.random.randint(
        1,
        101,
        TOTAL_REGISTROS_ARMAZEM
    ),
    "data_operacao": pd.to_datetime(
        np.random.randint(
            data_inicio.value // 10**9,
            data_fim.value // 10**9,
            TOTAL_REGISTROS_ARMAZEM
        ),
        unit="s"
    ),
    "pedidos_separados": np.random.randint(
        20,
        200,
        TOTAL_REGISTROS_ARMAZEM
    ),
    "erros_picking": np.random.choice(
        [0, 0, 0, 1, 2, 3],
        TOTAL_REGISTROS_ARMAZEM
    ),
    "avarias": np.random.choice(
        [0, 0, 0, 0, 1, 2],
        TOTAL_REGISTROS_ARMAZEM
    )
})

armazem.to_csv(
    DATA_DIR / "armazem.csv",
    index=False,
    encoding="utf-8-sig"
)

print()
print("==========================================")
print("DADOS LOGÍSTICOS GERADOS COM SUCESSO")
print("==========================================")
print(f"Pedidos:           {len(pedidos):,}")
print(f"Produtos:          {len(produtos):,}")
print(f"Entregas:          {len(entregas):,}")
print(f"Transportadoras:   {len(transportadoras):,}")
print(f"Estoque:           {len(estoque):,}")
print(f"Operações armazém: {len(armazem):,}")
print()
print("Arquivos salvos em: data/")