"""Financial projections: compound interest, monthly/annual tables."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal

from investx.models.market_data import MarketIndicators
from investx.models.portfolio import Portfolio
from investx.models.products import TaxType
from investx.models.user_profile import UserProfile
from investx.services.tax import ir_rate, net_return_fixed_income


@dataclass
class ProjectionRow:
    period: int              # mes ou ano
    label: str               # "Mes 6", "Ano 1", etc.
    invested: Decimal        # total investido (aportes + inicial)
    gross_balance: Decimal   # saldo bruto
    net_balance: Decimal     # saldo liquido (apos impostos)
    gross_return: Decimal    # rendimento bruto acumulado
    net_return: Decimal      # rendimento liquido acumulado
    poupanca_balance: Decimal  # comparativo poupanca


@dataclass
class ProjectionResult:
    rows: list[ProjectionRow] = field(default_factory=list)
    final_gross: Decimal = Decimal("0")
    final_net: Decimal = Decimal("0")
    final_poupanca: Decimal = Decimal("0")
    total_invested: Decimal = Decimal("0")
    total_tax_paid: Decimal = Decimal("0")
    real_return_pct: Decimal = Decimal("0")


def _estimate_portfolio_annual_return(
    portfolio: Portfolio,
    indicators: MarketIndicators,
) -> Decimal:
    """Estimate the weighted average gross annual return of the portfolio."""
    if not portfolio.allocations:
        return indicators.cdi

    cdi = indicators.cdi
    ipca = indicators.ipca

    total_return = Decimal("0")
    for alloc in portfolio.allocations:
        p = alloc.product
        if p.expected_return_pct_cdi is not None:
            ret = cdi * p.expected_return_pct_cdi / Decimal("100")
        elif p.expected_return_fixed is not None:
            ret = p.expected_return_fixed
        elif p.expected_return_ipca_plus is not None:
            ret = ipca + p.expected_return_ipca_plus
        elif p.tax_type == TaxType.POUPANCA:
            ret = indicators.poupanca
        elif p.tax_type == TaxType.ACOES:
            # Estimate: IPCA + 6% for equities long-term
            ret = ipca + Decimal("6")
        elif p.tax_type == TaxType.FII:
            # Estimate: CDI + 1% (dividends + appreciation)
            ret = cdi + Decimal("1")
        else:
            ret = cdi

        total_return += ret * alloc.weight_fraction

    return total_return.quantize(Decimal("0.01"))


def _estimate_portfolio_avg_tax(
    portfolio: Portfolio,
    days: int,
) -> Decimal:
    """Estimate weighted average tax rate for the portfolio."""
    total_tax = Decimal("0")
    for alloc in portfolio.allocations:
        p = alloc.product
        if p.tax_type == TaxType.IR_REGRESSIVO:
            total_tax += ir_rate(days) * alloc.weight_fraction
        elif p.tax_type in (TaxType.ISENTO, TaxType.POUPANCA):
            pass  # 0% tax
        elif p.tax_type == TaxType.ACOES:
            total_tax += Decimal("0.15") * alloc.weight_fraction
        elif p.tax_type == TaxType.FII:
            # Only capital gains taxed, dividends exempt
            total_tax += Decimal("0.05") * alloc.weight_fraction
    return total_tax.quantize(Decimal("0.0001"))


def generate_projections(
    profile: UserProfile,
    portfolio: Portfolio,
    indicators: MarketIndicators,
) -> ProjectionResult:
    """Generate monthly projection rows for key milestones."""
    annual_return = _estimate_portfolio_annual_return(portfolio, indicators)
    monthly_rate = Decimal(
        str(round((1 + float(annual_return) / 100) ** (1 / 12) - 1, 8))
    )
    poupanca_monthly = Decimal(
        str(round((1 + float(indicators.poupanca) / 100) ** (1 / 12) - 1, 8))
    )

    total_months = profile.horizon_months
    contribution = profile.monthly_contribution

    # Milestones to report
    milestones: list[int] = []
    # Every 6 months for first 2 years
    for m in range(6, min(total_months + 1, 25), 6):
        milestones.append(m)
    # Every year after that
    for y in range(3, total_months // 12 + 1):
        milestones.append(y * 12)
    # Always include final month
    if total_months not in milestones:
        milestones.append(total_months)
    milestones = sorted(set(milestones))

    rows: list[ProjectionRow] = []
    gross_balance = profile.amount
    poupanca_balance = profile.amount

    for month in range(1, total_months + 1):
        # Compound growth
        gross_balance = gross_balance * (1 + monthly_rate) + contribution
        poupanca_balance = poupanca_balance * (1 + poupanca_monthly) + contribution

        if month in milestones:
            invested = profile.amount + contribution * month
            gross_return = gross_balance - invested
            days = month * 30
            avg_tax = _estimate_portfolio_avg_tax(portfolio, days)
            net_return = gross_return * (1 - avg_tax)
            net_balance = invested + net_return

            if month <= 24:
                label = f"Mes {month}"
            else:
                label = f"Ano {month // 12}"

            rows.append(
                ProjectionRow(
                    period=month,
                    label=label,
                    invested=invested.quantize(Decimal("0.01")),
                    gross_balance=gross_balance.quantize(Decimal("0.01")),
                    net_balance=net_balance.quantize(Decimal("0.01")),
                    gross_return=gross_return.quantize(Decimal("0.01")),
                    net_return=net_return.quantize(Decimal("0.01")),
                    poupanca_balance=poupanca_balance.quantize(Decimal("0.01")),
                )
            )

    # Final summary
    final_invested = profile.amount + contribution * total_months
    final_gross_return = gross_balance - final_invested
    final_days = total_months * 30
    final_avg_tax = _estimate_portfolio_avg_tax(portfolio, final_days)
    final_tax_paid = final_gross_return * final_avg_tax
    final_net = gross_balance - final_tax_paid

    real_return_pct = Decimal("0")
    if final_invested > 0:
        real_return_pct = (
            (final_net - final_invested) / final_invested * 100
        ).quantize(Decimal("0.01"))

    return ProjectionResult(
        rows=rows,
        final_gross=gross_balance.quantize(Decimal("0.01")),
        final_net=final_net.quantize(Decimal("0.01")),
        final_poupanca=poupanca_balance.quantize(Decimal("0.01")),
        total_invested=final_invested.quantize(Decimal("0.01")),
        total_tax_paid=final_tax_paid.quantize(Decimal("0.01")),
        real_return_pct=real_return_pct,
    )
