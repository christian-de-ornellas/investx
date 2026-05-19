"""Tax calculations: IR regressivo, IOF, FII, LCI/LCA, acoes."""

from __future__ import annotations

from decimal import Decimal

from investx.config.constants import (
    ACOES_IR_GANHO_CAPITAL,
    ACOES_ISENCAO_MENSAL,
    FII_IR_GANHO_CAPITAL,
    IOF_TABLE,
    IR_BRACKETS,
)
from investx.models.products import TaxType


def ir_rate(days: int) -> Decimal:
    """Return the IR rate for a given holding period in days."""
    for max_days, rate in IR_BRACKETS:
        if days <= max_days:
            return rate
    return IR_BRACKETS[-1][1]


def iof_rate(days: int) -> Decimal:
    """Return the IOF rate (fraction, not %) for a given holding period."""
    if days <= 0:
        return Decimal("0.96")
    if days > 30:
        return Decimal("0")
    return Decimal(str(IOF_TABLE[days - 1])) / Decimal("100")


def net_return_fixed_income(
    gross_return: Decimal,
    days: int,
    tax_type: TaxType,
) -> Decimal:
    """Calculate net return after IOF and IR for fixed income products."""
    if tax_type in (TaxType.ISENTO, TaxType.POUPANCA):
        return gross_return

    after_iof = gross_return
    if days <= 30:
        iof = gross_return * iof_rate(days)
        after_iof = gross_return - iof

    ir = after_iof * ir_rate(days)
    return after_iof - ir


def equivalent_cdi_gross(
    net_pct_cdi: Decimal,
    days: int,
) -> Decimal:
    """Calculate gross CDI % equivalent for an exempt product.

    E.g. LCI paying 93% CDI net = equivalent to CDB paying ~116% CDI gross
    at 15% IR (>720 days).
    """
    ir = ir_rate(days)
    return (net_pct_cdi / (Decimal("1") - ir)).quantize(Decimal("0.01"))


def fii_tax(gain: Decimal, is_dividend: bool = True) -> Decimal:
    """Calculate FII tax. Dividends are exempt for individuals."""
    if is_dividend:
        return Decimal("0")
    return gain * FII_IR_GANHO_CAPITAL


def acoes_tax(gain: Decimal, monthly_sales: Decimal) -> Decimal:
    """Calculate stock tax (simplified)."""
    if monthly_sales <= ACOES_ISENCAO_MENSAL:
        return Decimal("0")
    return gain * ACOES_IR_GANHO_CAPITAL
