-- ==========================================================
-- CENTRO DE CONTROLE LOGÍSTICO
-- KPIs OPERACIONAIS
-- ==========================================================


-- ==========================================================
-- 1. VISÃO GERAL DOS PEDIDOS
-- ==========================================================

SELECT
    COUNT(*) AS total_pedidos,

    COUNT(*) FILTER (
        WHERE status = 'Entregue'
    ) AS pedidos_entregues,

    COUNT(*) FILTER (
        WHERE status = 'Em transporte'
    ) AS pedidos_em_transporte,

    COUNT(*) FILTER (
        WHERE status = 'Pendente'
    ) AS pedidos_pendentes,

    COUNT(*) FILTER (
        WHERE status = 'Cancelado'
    ) AS pedidos_cancelados

FROM pedidos;


-- ==========================================================
-- 2. ATRASOS
-- ==========================================================

SELECT
    COUNT(*) AS total_entregas,

    COUNT(*) FILTER (
        WHERE data_entrega > data_prometida
    ) AS entregas_atrasadas,

    ROUND(
        COUNT(*) FILTER (
            WHERE data_entrega > data_prometida
        ) * 100.0 / COUNT(*),
        2
    ) AS taxa_atraso

FROM entregas;


-- ==========================================================
-- 3. LEAD TIME MÉDIO
-- ==========================================================

SELECT
    ROUND(
        AVG(
            data_entrega - data_prometida
        ),
        2
    ) AS atraso_medio_dias

FROM entregas;


-- ==========================================================
-- 4. OTIF
-- Entrega no prazo E quantidade completa
-- ==========================================================

SELECT
    COUNT(*) AS total_entregas,

    COUNT(*) FILTER (
        WHERE data_entrega <= data_prometida
        AND quantidade_entregue >= quantidade_pedida
    ) AS entregas_otif,

    ROUND(
        COUNT(*) FILTER (
            WHERE data_entrega <= data_prometida
            AND quantidade_entregue >= quantidade_pedida
        ) * 100.0 / COUNT(*),
        2
    ) AS otif_percentual

FROM entregas;


-- ==========================================================
-- 5. CUSTO MÉDIO POR ENTREGA
-- ==========================================================

SELECT
    ROUND(
        AVG(custo_entrega)::numeric,
        2
    ) AS custo_medio_entrega,

    ROUND(
        SUM(custo_entrega)::numeric,
        2
    ) AS custo_total_transporte

FROM entregas;


-- ==========================================================
-- 6. PERFORMANCE DAS TRANSPORTADORAS
-- ==========================================================

SELECT
    t.transportadora,

    COUNT(e.entrega_id) AS entregas,

    ROUND(
        AVG(e.custo_entrega)::numeric,
        2
    ) AS custo_medio,

    ROUND(
        COUNT(*) FILTER (
            WHERE e.data_entrega <= e.data_prometida
        ) * 100.0 / COUNT(*),
        2
    ) AS otd_percentual,

    ROUND(
        COUNT(*) FILTER (
            WHERE e.data_entrega <= e.data_prometida
            AND e.quantidade_entregue >= e.quantidade_pedida
        ) * 100.0 / COUNT(*),
        2
    ) AS otif_percentual

FROM entregas e

JOIN transportadoras t
    ON e.transportadora_id = t.transportadora_id

GROUP BY t.transportadora

ORDER BY otif_percentual DESC;


-- ==========================================================
-- 7. RUPTURA DE ESTOQUE
-- ==========================================================

SELECT
    COUNT(*) AS total_itens,

    COUNT(*) FILTER (
        WHERE quantidade_estoque <= estoque_minimo
    ) AS itens_criticos,

    ROUND(
        COUNT(*) FILTER (
            WHERE quantidade_estoque <= estoque_minimo
        ) * 100.0 / COUNT(*),
        2
    ) AS percentual_critico

FROM estoque;


-- ==========================================================
-- 8. ESTOQUE PARADO
-- Mais de 90 dias sem movimentação
-- ==========================================================

SELECT

    COUNT(*) FILTER (
        WHERE dias_sem_movimentacao > 90
    ) AS itens_parados,

    ROUND(
        COUNT(*) FILTER (
            WHERE dias_sem_movimentacao > 90
        ) * 100.0 / COUNT(*),
        2
    ) AS percentual_estoque_parado

FROM estoque;


-- ==========================================================
-- 9. PRODUTIVIDADE DO ARMAZÉM
-- ==========================================================

SELECT

    SUM(pedidos_separados) AS pedidos_separados,

    SUM(erros_picking) AS erros_picking,

    SUM(avarias) AS avarias,

    ROUND(
        SUM(erros_picking) * 100.0 /
        NULLIF(SUM(pedidos_separados), 0),
        2
    ) AS taxa_erro_picking

FROM armazem;


-- ==========================================================
-- 10. PERFORMANCE GERAL DO ARMAZÉM
-- ==========================================================

SELECT

    COUNT(*) AS operacoes,

    ROUND(
        AVG(pedidos_separados),
        2
    ) AS produtividade_media,

    ROUND(
        AVG(erros_picking),
        2
    ) AS erros_medios,

    ROUND(
        AVG(avarias),
        2
    ) AS avarias_medias

FROM armazem;