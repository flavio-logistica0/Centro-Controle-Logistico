from config import HOST, PORTA, BANCO, USUARIO, SENHA
import psycopg2





conexao = psycopg2.connect(
    host=HOST,
    port=PORTA,
    database=BANCO,
    user=USUARIO,
    password=SENHA
)

cursor = conexao.cursor()

cursor.execute("""
SELECT
    t.transportadora,

    COUNT(*) AS entregas,

    ROUND(
        COUNT(*) FILTER (
            WHERE e.data_entrega <= e.data_prometida
            AND e.quantidade_entregue >= e.quantidade_pedida
        ) * 100.0 / COUNT(*),
        2
    ) AS otif,

    ROUND(
        COUNT(*) FILTER (
            WHERE e.data_entrega > e.data_prometida
        ) * 100.0 / COUNT(*),
        2
    ) AS atraso,

    ROUND(
        AVG(e.custo_entrega)::numeric,
        2
    ) AS custo_medio

FROM entregas e

JOIN transportadoras t
    ON e.transportadora_id = t.transportadora_id

GROUP BY t.transportadora

ORDER BY otif ASC;
""")

resultados = cursor.fetchall()

print()
print("======================================================")
print("       PERFORMANCE DAS TRANSPORTADORAS")
print("======================================================")
print()
print(
    f"{'Transportadora':<20}"
    f"{'Entregas':>10}"
    f"{'OTIF':>10}"
    f"{'Atraso':>10}"
    f"{'Custo':>12}"
)
print("-" * 62)

for transportadora, entregas, otif, atraso, custo in resultados:

    print(
        f"{transportadora:<20}"
        f"{entregas:>10}"
        f"{otif:>9.2f}%"
        f"{atraso:>9.2f}%"
        f" R$ {custo:>8.2f}"
    )

print()
print("======================================================")

cursor.close()
conexao.close()


