from config import HOST, PORTA, BANCO, USUARIO, SENHA
import psycopg2
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================




BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

PDF = REPORTS_DIR / "relatorio_executivo_logistico.pdf"


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


def consultar(sql):
    cursor.execute(sql)
    return cursor.fetchone()


# ==========================================================
# KPIs
# ==========================================================

total_pedidos, pendentes, cancelados = consultar("""
SELECT
    COUNT(*),
    COUNT(*) FILTER (WHERE status = 'Pendente'),
    COUNT(*) FILTER (WHERE status = 'Cancelado')
FROM pedidos;
""")


total_entregas, otif_entregas = consultar("""
SELECT
    COUNT(*),
    COUNT(*) FILTER (
        WHERE data_entrega <= data_prometida
        AND quantidade_entregue >= quantidade_pedida
    )
FROM entregas;
""")

otif = otif_entregas / total_entregas * 100

atrasadas = consultar("""
SELECT COUNT(*)
FROM entregas
WHERE data_entrega > data_prometida;
""")[0]

taxa_atraso = atrasadas / total_entregas * 100

custo_medio = consultar("""
SELECT AVG(custo_entrega)
FROM entregas;
""")[0]

rupturas = consultar("""
SELECT COUNT(*)
FROM estoque
WHERE quantidade_estoque <= estoque_minimo;
""")[0]

estoque_parado = consultar("""
SELECT COUNT(*)
FROM estoque
WHERE dias_sem_movimentacao > 90;
""")[0]

pedidos_separados, erros_picking, avarias = consultar("""
SELECT
    SUM(pedidos_separados),
    SUM(erros_picking),
    SUM(avarias)
FROM armazem;
""")

taxa_erro = erros_picking / pedidos_separados * 100


# ==========================================================
# TRANSPORTADORA CRÍTICA
# ==========================================================

transportadora = consultar("""
SELECT
    t.transportadora,
    ROUND(
        COUNT(*) FILTER (
            WHERE e.data_entrega <= e.data_prometida
            AND e.quantidade_entregue >= e.quantidade_pedida
        ) * 100.0 / COUNT(*),
        2
    ) AS otif
FROM entregas e
JOIN transportadoras t
    ON e.transportadora_id = t.transportadora_id
GROUP BY t.transportadora
ORDER BY otif ASC
LIMIT 1;
""")

nome_transportadora, otif_transportadora = transportadora


# ==========================================================
# PDF
# ==========================================================

styles = getSampleStyleSheet()

titulo = styles["Title"]
subtitulo = styles["Heading2"]
normal = styles["BodyText"]

documento = SimpleDocTemplate(
    str(PDF),
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40
)

elementos = []

elementos.append(
    Paragraph(
        "CENTRO DE CONTROLE LOGÍSTICO",
        titulo
    )
)

elementos.append(
    Paragraph(
        "Relatório Executivo de Performance Operacional",
        normal
    )
)

elementos.append(Spacer(1, 20))


# ----------------------------------------------------------
# VISÃO GERAL
# ----------------------------------------------------------

elementos.append(
    Paragraph("1. Visão Geral", subtitulo)
)

dados = [
    ["Indicador", "Resultado"],
    ["Total de pedidos", f"{total_pedidos:,}"],
    ["Pedidos pendentes", f"{pendentes:,}"],
    ["Pedidos cancelados", f"{cancelados:,}"],
    ["OTIF", f"{otif:.2f}%"],
    ["Entregas atrasadas", f"{atrasadas:,}"],
    ["Taxa de atraso", f"{taxa_atraso:.2f}%"],
    ["Custo médio por entrega", f"R$ {custo_medio:.2f}"],
    ["Produtos críticos", f"{rupturas:,}"],
    ["Estoque parado", f"{estoque_parado:,}"],
    ["Taxa de erro picking", f"{taxa_erro:.2f}%"],
    ["Avarias", f"{avarias:,}"],
]

tabela = Table(dados, colWidths=[280, 150])

tabela.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 7),
    ])
)

elementos.append(tabela)

elementos.append(Spacer(1, 20))


# ----------------------------------------------------------
# DIAGNÓSTICO
# ----------------------------------------------------------

elementos.append(
    Paragraph("2. Diagnóstico Automático", subtitulo)
)

problemas = []

if otif < 95:
    problemas.append(
        f"OTIF abaixo da meta: {otif:.2f}%."
    )

if taxa_atraso > 10:
    problemas.append(
        f"Taxa de atraso elevada: {taxa_atraso:.2f}%."
    )

if estoque_parado > 100:
    problemas.append(
        f"Alto volume de estoque parado: {estoque_parado} itens."
    )

if rupturas > 100:
    problemas.append(
        f"Quantidade elevada de produtos críticos: {rupturas}."
    )

if taxa_erro > 1:
    problemas.append(
        f"Taxa de erro de picking acima de 1%: {taxa_erro:.2f}%."
    )

for problema in problemas:
    elementos.append(
        Paragraph("• " + problema, normal)
    )

elementos.append(Spacer(1, 15))


# ----------------------------------------------------------
# TRANSPORTADORA
# ----------------------------------------------------------

elementos.append(
    Paragraph("3. Principal Transportadora em Risco", subtitulo)
)

elementos.append(
    Paragraph(
        f"{nome_transportadora} apresentou o menor OTIF entre as "
        f"transportadoras analisadas: {otif_transportadora:.2f}%.",
        normal
    )
)

elementos.append(Spacer(1, 15))


# ----------------------------------------------------------
# RECOMENDAÇÕES
# ----------------------------------------------------------

elementos.append(
    Paragraph("4. Recomendações", subtitulo)
)

recomendacoes = [
    "Investigar as causas dos atrasos e do baixo OTIF.",
    "Avaliar a performance das transportadoras antes de redistribuir rotas.",
    "Priorizar produtos com estoque abaixo do nível mínimo.",
    "Criar plano de redução do estoque parado.",
    "Acompanhar diariamente erros de picking e avarias.",
    "Estabelecer metas de OTIF, atraso e produtividade."
]

for recomendacao in recomendacoes:
    elementos.append(
        Paragraph("• " + recomendacao, normal)
    )


documento.build(elementos)

cursor.close()
conexao.close()

print()
print("==========================================")
print("RELATÓRIO EXECUTIVO GERADO!")
print("==========================================")
print(f"PDF: {PDF}")


