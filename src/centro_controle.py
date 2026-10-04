from config import HOST, PORTA, BANCO, USUARIO, SENHA
import psycopg2
from pathlib import Path


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================




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

cursor = conexao.cursor()


# ==========================================================
# PEDIDOS
# ==========================================================

cursor.execute("""
SELECT
    COUNT(*) AS total,
    COUNT(*) FILTER (WHERE status = 'Pendente') AS pendentes,
    COUNT(*) FILTER (WHERE status = 'Cancelado') AS cancelados
FROM pedidos;
""")

total_pedidos, pendentes, cancelados = cursor.fetchone()


# ==========================================================
# TRANSPORTE / OTIF
# ==========================================================

cursor.execute("""
SELECT
    COUNT(*),
    COUNT(*) FILTER (
        WHERE data_entrega <= data_prometida
        AND quantidade_entregue >= quantidade_pedida
    )
FROM entregas;
""")

total_entregas, entregas_otif = cursor.fetchone()

otif = (entregas_otif / total_entregas) * 100


# ==========================================================
# ATRASOS
# ==========================================================

cursor.execute("""
SELECT COUNT(*)
FROM entregas
WHERE data_entrega > data_prometida;
""")

atrasadas = cursor.fetchone()[0]

taxa_atraso = (atrasadas / total_entregas) * 100


# ==========================================================
# CUSTO
# ==========================================================

cursor.execute("""
SELECT AVG(custo_entrega)
FROM entregas;
""")

custo_medio = cursor.fetchone()[0]


# ==========================================================
# ESTOQUE
# ==========================================================

cursor.execute("""
SELECT
    COUNT(*) FILTER (
        WHERE quantidade_estoque <= estoque_minimo
    ),
    COUNT(*) FILTER (
        WHERE dias_sem_movimentacao > 90
    )
FROM estoque;
""")

rupturas, estoque_parado = cursor.fetchone()


# ==========================================================
# ARMAZÉM
# ==========================================================

cursor.execute("""
SELECT
    SUM(pedidos_separados),
    SUM(erros_picking),
    SUM(avarias)
FROM armazem;
""")

pedidos_separados, erros_picking, avarias = cursor.fetchone()

taxa_erro = (erros_picking / pedidos_separados) * 100


# ==========================================================
# CENTRO DE CONTROLE
# ==========================================================

print()
print("╔══════════════════════════════════════════╗")
print("║       CENTRO DE CONTROLE LOGÍSTICO       ║")
print("╚══════════════════════════════════════════╝")

print()
print("📦 PEDIDOS")
print(f"Total:              {total_pedidos:,}")
print(f"Pendentes:          {pendentes:,}")
print(f"Cancelados:         {cancelados:,}")

print()
print("🚚 TRANSPORTE")
print(f"OTIF:               {otif:.2f}%")
print(f"Entregas atrasadas: {atrasadas:,}")
print(f"Taxa de atraso:     {taxa_atraso:.2f}%")
print(f"Custo/entrega:      R$ {custo_medio:.2f}")

print()
print("📦 ESTOQUE")
print(f"Produtos críticos:  {rupturas:,}")
print(f"Estoque parado:     {estoque_parado:,}")

print()
print("🏭 ARMAZÉM")
print(f"Pedidos separados:  {pedidos_separados:,}")
print(f"Erros de picking:   {erros_picking:,}")
print(f"Taxa de erro:       {taxa_erro:.2f}%")
print(f"Avarias:            {avarias:,}")

print()
print("🚨 PRINCIPAIS PONTOS DE ATENÇÃO")

if otif < 95:
    print("🔴 OTIF abaixo da meta de 95%")

if taxa_atraso > 10:
    print("🔴 Taxa de atraso elevada")

if rupturas > 100:
    print("🔴 Muitos produtos em nível crítico")

if estoque_parado > 100:
    print("🔴 Alto volume de estoque parado")

if taxa_erro > 1:
    print("🔴 Taxa de erro de picking acima de 1%")

print()
print("==========================================")
print("ANÁLISE CONCLUÍDA")
print("==========================================")

cursor.close()
conexao.close()


