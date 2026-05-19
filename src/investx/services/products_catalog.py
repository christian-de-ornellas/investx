"""Catalog of Brazilian investment products."""

from __future__ import annotations

from decimal import Decimal

from investx.models.products import (
    InvestmentProduct,
    LiquidityType,
    ProductCategory,
    TaxType,
)

PRODUCTS: list[InvestmentProduct] = [
    # --- Renda Fixa - Pos-fixado ---
    InvestmentProduct(
        name="Tesouro Selic",
        category=ProductCategory.RENDA_FIXA,
        tax_type=TaxType.IR_REGRESSIVO,
        liquidity=LiquidityType.DAILY,
        risk_score=1,
        min_investment=Decimal("30"),
        benchmark="Selic",
        expected_return_pct_cdi=Decimal("100"),
        description="Titulo publico pos-fixado, ideal para reserva de emergencia",
        tags=["reserva", "pos-fixado", "governo"],
    ),
    InvestmentProduct(
        name="CDB Liquidez Diaria",
        category=ProductCategory.RENDA_FIXA,
        tax_type=TaxType.IR_REGRESSIVO,
        liquidity=LiquidityType.DAILY,
        risk_score=2,
        min_investment=Decimal("1"),
        expected_return_pct_cdi=Decimal("100"),
        description="CDB com resgate a qualquer momento, bancos digitais oferecem 100% CDI",
        tags=["reserva", "pos-fixado", "fgc"],
    ),
    InvestmentProduct(
        name="CDB Prefixado (2 anos)",
        category=ProductCategory.RENDA_FIXA,
        tax_type=TaxType.IR_REGRESSIVO,
        liquidity=LiquidityType.LOW,
        risk_score=3,
        min_investment=Decimal("1000"),
        expected_return_fixed=Decimal("14.50"),
        description="CDB com taxa fixa, ideal quando juros devem cair",
        tags=["prefixado", "fgc"],
    ),
    InvestmentProduct(
        name="CDB IPCA+ (3 anos)",
        category=ProductCategory.RENDA_FIXA,
        tax_type=TaxType.IR_REGRESSIVO,
        liquidity=LiquidityType.LOW,
        risk_score=3,
        min_investment=Decimal("1000"),
        expected_return_ipca_plus=Decimal("7.0"),
        description="CDB indexado a inflacao, protege poder de compra",
        tags=["inflacao", "fgc"],
    ),
    # --- Renda Fixa - Isentos ---
    InvestmentProduct(
        name="LCI",
        category=ProductCategory.RENDA_FIXA,
        tax_type=TaxType.ISENTO,
        liquidity=LiquidityType.MEDIUM,
        risk_score=2,
        min_investment=Decimal("1000"),
        expected_return_pct_cdi=Decimal("93"),
        description="Letra de Credito Imobiliario, isenta de IR para PF",
        tags=["isento", "fgc", "imobiliario"],
    ),
    InvestmentProduct(
        name="LCA",
        category=ProductCategory.RENDA_FIXA,
        tax_type=TaxType.ISENTO,
        liquidity=LiquidityType.MEDIUM,
        risk_score=2,
        min_investment=Decimal("1000"),
        expected_return_pct_cdi=Decimal("93"),
        description="Letra de Credito do Agronegocio, isenta de IR para PF",
        tags=["isento", "fgc", "agro"],
    ),
    InvestmentProduct(
        name="Debentures Incentivadas",
        category=ProductCategory.RENDA_FIXA,
        tax_type=TaxType.ISENTO,
        liquidity=LiquidityType.LOW,
        risk_score=4,
        min_investment=Decimal("1000"),
        expected_return_ipca_plus=Decimal("7.5"),
        description="Debentures de infraestrutura, isentas de IR (Lei 12.431)",
        tags=["isento", "infraestrutura", "credito_privado"],
    ),
    # --- Renda Fixa - Tesouro Direto ---
    InvestmentProduct(
        name="Tesouro Prefixado (2029)",
        category=ProductCategory.RENDA_FIXA,
        tax_type=TaxType.IR_REGRESSIVO,
        liquidity=LiquidityType.DAILY,
        risk_score=3,
        min_investment=Decimal("30"),
        expected_return_fixed=Decimal("14.80"),
        description="Titulo prefixado do governo, voce sabe exatamente quanto vai receber",
        tags=["prefixado", "governo"],
    ),
    InvestmentProduct(
        name="Tesouro IPCA+ 2035",
        category=ProductCategory.RENDA_FIXA,
        tax_type=TaxType.IR_REGRESSIVO,
        liquidity=LiquidityType.DAILY,
        risk_score=3,
        min_investment=Decimal("30"),
        expected_return_ipca_plus=Decimal("7.2"),
        description="Titulo publico que protege da inflacao, ideal para longo prazo",
        tags=["inflacao", "governo", "longo_prazo"],
    ),
    InvestmentProduct(
        name="Tesouro IPCA+ com Juros Semestrais",
        category=ProductCategory.RENDA_FIXA,
        tax_type=TaxType.IR_REGRESSIVO,
        liquidity=LiquidityType.DAILY,
        risk_score=3,
        min_investment=Decimal("30"),
        expected_return_ipca_plus=Decimal("7.0"),
        description="Tesouro IPCA+ que paga cupons semestrais, bom para renda",
        tags=["inflacao", "governo", "renda", "cupom"],
    ),
    # --- Renda Fixa - Credito Privado ---
    InvestmentProduct(
        name="Fundo RF Credito Privado",
        category=ProductCategory.RENDA_FIXA,
        tax_type=TaxType.IR_REGRESSIVO,
        liquidity=LiquidityType.SHORT,
        risk_score=4,
        min_investment=Decimal("500"),
        expected_return_pct_cdi=Decimal("115"),
        description="Fundo de credito privado, busca retorno acima do CDI",
        tags=["credito_privado", "fundo"],
    ),
    # --- Renda Variavel ---
    InvestmentProduct(
        name="ETF BOVA11 (Ibovespa)",
        category=ProductCategory.RENDA_VARIAVEL,
        tax_type=TaxType.ACOES,
        liquidity=LiquidityType.DAILY,
        risk_score=7,
        min_investment=Decimal("100"),
        description="ETF que replica o Ibovespa, diversificacao instantanea em acoes",
        tags=["acoes", "etf", "ibovespa"],
    ),
    InvestmentProduct(
        name="ETF IVVB11 (S&P 500)",
        category=ProductCategory.RENDA_VARIAVEL,
        tax_type=TaxType.ACOES,
        liquidity=LiquidityType.DAILY,
        risk_score=8,
        min_investment=Decimal("100"),
        description="ETF que replica o S&P 500 em reais, exposicao internacional",
        tags=["acoes", "etf", "internacional", "dolar"],
    ),
    InvestmentProduct(
        name="Acoes (carteira diversificada)",
        category=ProductCategory.RENDA_VARIAVEL,
        tax_type=TaxType.ACOES,
        liquidity=LiquidityType.DAILY,
        risk_score=8,
        min_investment=Decimal("500"),
        description="Carteira diversificada de acoes brasileiras",
        tags=["acoes", "stock_picking"],
    ),
    InvestmentProduct(
        name="Fundos Imobiliarios (FIIs)",
        category=ProductCategory.RENDA_VARIAVEL,
        tax_type=TaxType.FII,
        liquidity=LiquidityType.DAILY,
        risk_score=5,
        min_investment=Decimal("100"),
        expected_return_pct_cdi=Decimal("110"),
        description="Fundos imobiliarios, dividendos mensais isentos de IR",
        tags=["fii", "renda", "imobiliario", "dividendos"],
    ),
    # --- Multimercado ---
    InvestmentProduct(
        name="Fundo Multimercado",
        category=ProductCategory.MULTIMERCADO,
        tax_type=TaxType.IR_REGRESSIVO,
        liquidity=LiquidityType.SHORT,
        risk_score=6,
        min_investment=Decimal("500"),
        expected_return_pct_cdi=Decimal("120"),
        description="Fundo com liberdade para investir em diversas classes",
        tags=["fundo", "diversificacao"],
    ),
    # --- Poupanca (referencia) ---
    InvestmentProduct(
        name="Poupanca",
        category=ProductCategory.RENDA_FIXA,
        tax_type=TaxType.POUPANCA,
        liquidity=LiquidityType.DAILY,
        risk_score=1,
        min_investment=Decimal("1"),
        description="Caderneta de poupanca, isenta mas com rendimento baixo",
        tags=["poupanca", "isento", "fgc"],
    ),
]


def get_all_products() -> list[InvestmentProduct]:
    return PRODUCTS.copy()


def get_products_by_category(
    category: ProductCategory,
) -> list[InvestmentProduct]:
    return [p for p in PRODUCTS if p.category == category]


def get_products_by_risk(max_risk: int) -> list[InvestmentProduct]:
    return [p for p in PRODUCTS if p.risk_score <= max_risk]


def get_products_by_tag(tag: str) -> list[InvestmentProduct]:
    return [p for p in PRODUCTS if tag in p.tags]
