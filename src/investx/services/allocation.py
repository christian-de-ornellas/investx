"""Allocation engine - core algorithm for portfolio construction."""

from __future__ import annotations

from decimal import Decimal

from investx.models.market_data import MarketIndicators
from investx.models.portfolio import AssetAllocation, Portfolio
from investx.models.products import InvestmentProduct, LiquidityType
from investx.models.user_profile import Objective, RiskProfile, UserProfile
from investx.services.products_catalog import get_all_products
from investx.services.risk import max_risk_score

# Allocation templates: (Objective, RiskProfile) -> dict[category_tag, weight%]
# Tags map to product selection logic, not 1:1 to products.
ALLOCATION_TEMPLATES: dict[
    tuple[Objective, RiskProfile],
    dict[str, Decimal],
] = {
    # Emergency fund - always very conservative
    (Objective.EMERGENCY, RiskProfile.CONSERVATIVE): {
        "pos_fixado_liquido": Decimal("100"),
    },
    (Objective.EMERGENCY, RiskProfile.MODERATE): {
        "pos_fixado_liquido": Decimal("100"),
    },
    (Objective.EMERGENCY, RiskProfile.BOLD): {
        "pos_fixado_liquido": Decimal("100"),
    },
    (Objective.EMERGENCY, RiskProfile.AGGRESSIVE): {
        "pos_fixado_liquido": Decimal("100"),
    },
    # Short-term
    (Objective.SHORT_TERM, RiskProfile.CONSERVATIVE): {
        "pos_fixado_liquido": Decimal("70"),
        "renda_fixa_isento": Decimal("30"),
    },
    (Objective.SHORT_TERM, RiskProfile.MODERATE): {
        "pos_fixado_liquido": Decimal("50"),
        "renda_fixa_isento": Decimal("30"),
        "renda_fixa_credito": Decimal("20"),
    },
    (Objective.SHORT_TERM, RiskProfile.BOLD): {
        "pos_fixado_liquido": Decimal("40"),
        "renda_fixa_isento": Decimal("30"),
        "renda_fixa_credito": Decimal("20"),
        "multimercado": Decimal("10"),
    },
    (Objective.SHORT_TERM, RiskProfile.AGGRESSIVE): {
        "pos_fixado_liquido": Decimal("30"),
        "renda_fixa_isento": Decimal("25"),
        "renda_fixa_credito": Decimal("20"),
        "multimercado": Decimal("15"),
        "fii": Decimal("10"),
    },
    # Mixed / medium-term
    (Objective.MIXED, RiskProfile.CONSERVATIVE): {
        "pos_fixado_liquido": Decimal("30"),
        "tesouro_ipca": Decimal("30"),
        "renda_fixa_isento": Decimal("25"),
        "fii": Decimal("15"),
    },
    (Objective.MIXED, RiskProfile.MODERATE): {
        "pos_fixado_liquido": Decimal("20"),
        "tesouro_ipca": Decimal("25"),
        "renda_fixa_isento": Decimal("20"),
        "fii": Decimal("15"),
        "multimercado": Decimal("10"),
        "acoes_etf": Decimal("10"),
    },
    (Objective.MIXED, RiskProfile.BOLD): {
        "pos_fixado_liquido": Decimal("10"),
        "tesouro_ipca": Decimal("20"),
        "renda_fixa_isento": Decimal("15"),
        "fii": Decimal("15"),
        "multimercado": Decimal("15"),
        "acoes_etf": Decimal("15"),
        "acoes_intl": Decimal("10"),
    },
    (Objective.MIXED, RiskProfile.AGGRESSIVE): {
        "pos_fixado_liquido": Decimal("5"),
        "tesouro_ipca": Decimal("10"),
        "renda_fixa_isento": Decimal("10"),
        "fii": Decimal("15"),
        "multimercado": Decimal("15"),
        "acoes_etf": Decimal("20"),
        "acoes_intl": Decimal("15"),
        "acoes_stock": Decimal("10"),
    },
    # Retirement
    (Objective.RETIREMENT, RiskProfile.CONSERVATIVE): {
        "tesouro_ipca": Decimal("40"),
        "pos_fixado_liquido": Decimal("20"),
        "renda_fixa_isento": Decimal("20"),
        "fii": Decimal("20"),
    },
    (Objective.RETIREMENT, RiskProfile.MODERATE): {
        "tesouro_ipca": Decimal("30"),
        "pos_fixado_liquido": Decimal("10"),
        "renda_fixa_isento": Decimal("15"),
        "fii": Decimal("15"),
        "acoes_etf": Decimal("15"),
        "acoes_intl": Decimal("15"),
    },
    (Objective.RETIREMENT, RiskProfile.BOLD): {
        "tesouro_ipca": Decimal("20"),
        "pos_fixado_liquido": Decimal("5"),
        "renda_fixa_isento": Decimal("10"),
        "fii": Decimal("15"),
        "acoes_etf": Decimal("20"),
        "acoes_intl": Decimal("15"),
        "multimercado": Decimal("15"),
    },
    (Objective.RETIREMENT, RiskProfile.AGGRESSIVE): {
        "tesouro_ipca": Decimal("15"),
        "fii": Decimal("10"),
        "acoes_etf": Decimal("25"),
        "acoes_intl": Decimal("20"),
        "acoes_stock": Decimal("15"),
        "multimercado": Decimal("15"),
    },
    # Growth
    (Objective.GROWTH, RiskProfile.CONSERVATIVE): {
        "tesouro_ipca": Decimal("30"),
        "pos_fixado_liquido": Decimal("20"),
        "renda_fixa_isento": Decimal("20"),
        "fii": Decimal("15"),
        "acoes_etf": Decimal("15"),
    },
    (Objective.GROWTH, RiskProfile.MODERATE): {
        "tesouro_ipca": Decimal("20"),
        "pos_fixado_liquido": Decimal("10"),
        "renda_fixa_isento": Decimal("10"),
        "fii": Decimal("15"),
        "acoes_etf": Decimal("20"),
        "acoes_intl": Decimal("15"),
        "multimercado": Decimal("10"),
    },
    (Objective.GROWTH, RiskProfile.BOLD): {
        "tesouro_ipca": Decimal("10"),
        "fii": Decimal("10"),
        "acoes_etf": Decimal("25"),
        "acoes_intl": Decimal("20"),
        "acoes_stock": Decimal("15"),
        "multimercado": Decimal("15"),
        "debentures": Decimal("5"),
    },
    (Objective.GROWTH, RiskProfile.AGGRESSIVE): {
        "acoes_etf": Decimal("25"),
        "acoes_intl": Decimal("25"),
        "acoes_stock": Decimal("20"),
        "multimercado": Decimal("15"),
        "fii": Decimal("10"),
        "debentures": Decimal("5"),
    },
    # Income
    (Objective.INCOME, RiskProfile.CONSERVATIVE): {
        "fii": Decimal("30"),
        "tesouro_ipca_juros": Decimal("30"),
        "renda_fixa_isento": Decimal("20"),
        "pos_fixado_liquido": Decimal("20"),
    },
    (Objective.INCOME, RiskProfile.MODERATE): {
        "fii": Decimal("35"),
        "tesouro_ipca_juros": Decimal("25"),
        "renda_fixa_isento": Decimal("15"),
        "debentures": Decimal("10"),
        "pos_fixado_liquido": Decimal("15"),
    },
    (Objective.INCOME, RiskProfile.BOLD): {
        "fii": Decimal("35"),
        "tesouro_ipca_juros": Decimal("15"),
        "debentures": Decimal("15"),
        "acoes_etf": Decimal("15"),
        "renda_fixa_isento": Decimal("10"),
        "pos_fixado_liquido": Decimal("10"),
    },
    (Objective.INCOME, RiskProfile.AGGRESSIVE): {
        "fii": Decimal("30"),
        "acoes_etf": Decimal("20"),
        "acoes_stock": Decimal("15"),
        "debentures": Decimal("15"),
        "tesouro_ipca_juros": Decimal("10"),
        "multimercado": Decimal("10"),
    },
}


def _pick_product(tag: str, products: list[InvestmentProduct]) -> InvestmentProduct:
    """Select a product for a given allocation tag."""
    by_name: dict[str, InvestmentProduct] = {p.name: p for p in products}
    mapping: dict[str, str] = {
        "pos_fixado_liquido": "Tesouro Selic",
        "renda_fixa_isento": "LCI",
        "renda_fixa_credito": "Fundo RF Credito Privado",
        "tesouro_ipca": "Tesouro IPCA+ 2035",
        "tesouro_ipca_juros": "Tesouro IPCA+ com Juros Semestrais",
        "fii": "Fundos Imobiliarios (FIIs)",
        "multimercado": "Fundo Multimercado",
        "acoes_etf": "ETF BOVA11 (Ibovespa)",
        "acoes_intl": "ETF IVVB11 (S&P 500)",
        "acoes_stock": "Acoes (carteira diversificada)",
        "debentures": "Debentures Incentivadas",
        "prefixado": "Tesouro Prefixado (2029)",
        "cdb_ipca": "CDB IPCA+ (3 anos)",
        "lca": "LCA",
        "poupanca": "Poupanca",
    }
    name = mapping.get(tag)
    if name and name in by_name:
        return by_name[name]
    # Fallback: return first product with matching tag
    for p in products:
        if tag in p.tags:
            return p
    return by_name["Tesouro Selic"]


def build_portfolio(
    profile: UserProfile,
    indicators: MarketIndicators,
) -> Portfolio:
    """Build a portfolio based on user profile and market conditions."""
    products = get_all_products()
    risk_max = max_risk_score(profile)
    key = (profile.objective, profile.risk_profile)
    template = ALLOCATION_TEMPLATES.get(key)

    if template is None:
        # Default to mixed/moderate
        template = ALLOCATION_TEMPLATES[(Objective.MIXED, RiskProfile.MODERATE)]

    allocations: list[AssetAllocation] = []
    for tag, weight in template.items():
        product = _pick_product(tag, products)
        # Skip if product exceeds risk tolerance
        if product.risk_score > risk_max:
            continue
        # Skip if min investment exceeds amount
        if product.min_investment > profile.amount:
            continue
        allocations.append(AssetAllocation(product=product, weight=weight))

    # Re-normalize weights if some products were filtered out
    total_w = sum(a.weight for a in allocations)
    if total_w > Decimal("0") and total_w != Decimal("100"):
        for a in allocations:
            a.weight = (a.weight * Decimal("100") / total_w).quantize(Decimal("0.1"))
        # Fix rounding
        diff = Decimal("100") - sum(a.weight for a in allocations)
        if allocations:
            allocations[0].weight += diff

    portfolio = Portfolio(allocations=allocations)
    portfolio.distribute(profile.amount)
    return portfolio
