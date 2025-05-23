USE sistema_exemplo;
GO

SELECT
    a.cd_registro,
    a.cd_status,
    st.nm_status,
    s.id_pessoa,
    r.nr_categoria,
    r.nm_categoria,
    p.nr_documento,
    p.nm_entidade,
    m.id_movimento,
    m.nr_movimento,
    m.dt_inicio,
    m.dt_fim,
    m.dt_emissao,
    m.dt_criacao,
    m.cd_tipo_contrato,
    tc.nm_tipo_contrato,
    tm.nm_tipo_movimento,
    vl_bruto = it.valor_total,

    FLAG_DIVISAO = 
        CASE 
            WHEN COALESCE(div.participacao, 0)/100 > 0 THEN 'Sim' 
            ELSE 'Nao' 
        END,

    PARTICIPACAO_FORNECEDOR = COALESCE(div.participacao, 0)/100,
    PARTICIPACAO_INTERNA = 1 - COALESCE(div.participacao, 0)/100,
    pc.nm_produto,
    pc.id_item_produto,
    VL_FORNECEDOR = CAST(ROUND(it.valor_total * COALESCE(div.participacao, 0)/100, 2) AS MONEY),
    VL_INTERNO = CAST(ROUND(it.valor_total * (1 - COALESCE(div.participacao, 0)/100), 2) AS MONEY),

    VL_TOTAL_MOVIMENTO = 
        CASE 
            WHEN tm.cd_tipo_movimento IN (2,3) THEN -m.vl_total
            ELSE m.vl_total
        END,

    COMISSAO = 
        CASE 
            WHEN coms.percentual <> 0 THEN coms.percentual
            ELSE m.percentual_divisao
        END,

    corr.*,
    fornec.*,
    it.valor_taxa

FROM tbl_registro a

JOIN tbl_subregistro s ON s.id_registro = a.id_registro

JOIN tbl_movimento m ON m.id_sub = s.id_sub AND m.cd_tipo_movimento IN (0,1,4,2,3)

JOIN tbl_status st ON st.cd_status = a.cd_status AND st.cd_status = 7

JOIN tbl_categoria r ON r.id_categoria = a.id_categoria AND r.nr_categoria IN (100,200)

JOIN tbl_entidade p ON p.id_entidade = s.id_pessoa

JOIN tbl_tipo_contrato tc ON tc.cd_tipo_contrato = ISNULL(m.cd_tipo_contrato, 1)

JOIN tbl_tipo_movimento tm ON tm.cd_tipo_movimento = m.cd_tipo_movimento

JOIN tbl_itens_base ib ON ib.id_movimento = m.id_movimento

JOIN tbl_itens it ON it.id_item = ib.id_item

JOIN tbl_produto_cobertura pc ON pc.id_item_produto = it.id_item_produto

OUTER APPLY (
    SELECT 
        d.id_movimento,
        participacao = SUM(d.participacao)
    FROM tbl_divisao d 
    WHERE d.id_movimento = m.id_movimento
    GROUP BY d.id_movimento
) div

OUTER APPLY (
    SELECT 
        percentual = SUM(sc.percentual)
    FROM tbl_subparceiro sc 
    WHERE sc.id_movimento = m.id_movimento
) coms

OUTER APPLY (
    SELECT TOP 1
        nm_parceiro = c.nm_entidade,
        nm_representante = cr.nm_entidade
    FROM tbl_subparceiro sc
    JOIN tbl_entidade c ON c.id_entidade = sc.id_parceiro
    LEFT JOIN tbl_entidade cr ON cr.id_entidade = c.id_representante
    WHERE sc.id_movimento = m.id_movimento AND sc.cd_tipo_comissao = 2
    ORDER BY sc.flag_lider DESC
) corr

OUTER APPLY (
    SELECT DISTINCT
        f.nm_contrato,
        f.id_contrato
    FROM tbl_item_fornecedor fi
    LEFT JOIN tbl_cobertura_contrato cc ON cc.id_cobertura_contrato = fi.id_cobertura_contrato
    LEFT JOIN tbl_contrato f ON f.id_contrato = cc.id_contrato
    WHERE fi.id_movimento = m.id_movimento
) fornec

WHERE r.nr_categoria IN (100,200)
ORDER BY a.cd_registro;
