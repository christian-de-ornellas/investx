"""Investment product models."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum


class ProductCategory(str, Enum):
    RENDA_FIXA = "renda_fixa"
    RENDA_VARIAVEL = "renda_variavel"
    MULTIMERCADO = "multimercado"
    CAMBIAL = "cambial"


class TaxType(str, Enum):
    IR_REGRESSIVO = "ir_regressivo"  # CDB, Tesouro, fundos RF
    ISENTO = "isento"                # LCI, LCA, debentures incentivadas
    FII = "fii"                      # dividendos isentos, GC 20%
    ACOES = "acoes"                  # 15% GC, isencao <20k/mes
    POUPANCA = "poupanca"            # isento


class LiquidityType(str, Enum):
    DAILY = "daily"       # D+0 ou D+1
    SHORT = "short"       # ate D+5
    MEDIUM = "medium"     # D+30 a D+90
    LOW = "low"           # vencimento fixo ou >D+90


@dataclass
class InvestmentProduct:
    name: str
    category: ProductCategory
    tax_type: TaxType
    liquidity: LiquidityType
    risk_score: int                          # 1-10
    min_investment: Decimal = Decimal("0")
    benchmark: str = "CDI"
    expected_return_pct_cdi: Decimal | None = None  # % do CDI (e.g. 100 = 100%)
    expected_return_fixed: Decimal | None = None     # taxa fixa anual
    expected_return_ipca_plus: Decimal | None = None # IPCA + X%
    description: str = ""
    tags: list[str] = field(default_factory=list)
