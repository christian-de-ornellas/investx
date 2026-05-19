"""Report section: tax considerations."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from investx.models.portfolio import Portfolio
from investx.models.products import TaxType
from investx.models.user_profile import UserProfile
from investx.report.formatters import fmt_currency, fmt_pct
from investx.services.tax import equivalent_cdi_gross, ir_rate


def render_tax(
    console: Console,
    profile: UserProfile,
    portfolio: Portfolio,
) -> None:
    table = Table(title="Consideracoes Fiscais", show_lines=True)
    table.add_column("Produto", style="bold")
    table.add_column("Regime Tributario")
    table.add_column("Aliquota Estimada", justify="right", style="yellow")
    table.add_column("Observacao", style="dim")

    days = profile.horizon_months * 30

    for alloc in portfolio.allocations:
        p = alloc.product

        if p.tax_type == TaxType.IR_REGRESSIVO:
            rate = ir_rate(days)
            table.add_row(
                p.name,
                "IR Regressivo",
                fmt_pct(rate * 100),
                f"Para {profile.horizon_months} meses ({days}d)",
            )
        elif p.tax_type == TaxType.ISENTO:
            equiv = ""
            if p.expected_return_pct_cdi is not None:
                gross_eq = equivalent_cdi_gross(p.expected_return_pct_cdi, days)
                equiv = f"Equivale a {fmt_pct(gross_eq, 0)} do CDI com IR"
            table.add_row(p.name, "Isento de IR", "0,00%", equiv)
        elif p.tax_type == TaxType.POUPANCA:
            table.add_row(p.name, "Isento", "0,00%", "Rendimento isento de IR")
        elif p.tax_type == TaxType.FII:
            table.add_row(
                p.name,
                "FII",
                "Dividendos: 0%",
                "Ganho de capital: 20%",
            )
        elif p.tax_type == TaxType.ACOES:
            table.add_row(
                p.name,
                "Acoes",
                "15%",
                "Isento se vendas < R$20k/mes",
            )

    console.print(Panel(table, border_style="yellow"))

    # IOF note
    if profile.horizon_months <= 1:
        console.print(
            "  [bold yellow]Atencao:[/bold yellow] Para resgates em menos de 30 dias, "
            "incide IOF regressivo (96% a 0%) sobre o rendimento.\n"
        )
    # IR tip
    if days <= 720:
        target_days = 721
        target_rate = ir_rate(target_days)
        console.print(
            f"  [dim]Dica: Mantendo por mais de 720 dias (2 anos), "
            f"a aliquota de IR cai para {fmt_pct(target_rate * 100)}.[/dim]\n"
        )
