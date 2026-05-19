"""Report section: liquidity analysis."""

from __future__ import annotations

from decimal import Decimal

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from investx.models.portfolio import Portfolio
from investx.models.products import LiquidityType
from investx.report.formatters import fmt_currency, fmt_pct


_LIQUIDITY_LABELS = {
    LiquidityType.DAILY: ("D+0 / D+1", "green"),
    LiquidityType.SHORT: ("D+2 a D+5", "cyan"),
    LiquidityType.MEDIUM: ("D+30 a D+90", "yellow"),
    LiquidityType.LOW: ("Vencimento / +D+90", "red"),
}


def render_liquidity(console: Console, portfolio: Portfolio) -> None:
    table = Table(title="Analise de Liquidez", show_lines=True)
    table.add_column("Liquidez", style="bold")
    table.add_column("Produtos")
    table.add_column("Valor", justify="right", style="green")
    table.add_column("% Carteira", justify="right", style="cyan")

    groups: dict[LiquidityType, list] = {}
    for alloc in portfolio.allocations:
        liq = alloc.product.liquidity
        groups.setdefault(liq, []).append(alloc)

    total = portfolio.total_amount
    for liq_type in LiquidityType:
        allocs = groups.get(liq_type, [])
        if not allocs:
            continue
        label, style = _LIQUIDITY_LABELS[liq_type]
        names = ", ".join(a.product.name for a in allocs)
        amount = sum(a.amount for a in allocs)
        pct = amount / total * 100 if total else Decimal("0")
        table.add_row(
            f"[{style}]{label}[/{style}]",
            names,
            fmt_currency(amount),
            fmt_pct(pct, 1),
        )

    console.print(Panel(table, border_style="cyan"))

    # Liquidity score
    daily_pct = Decimal("0")
    if total > 0:
        daily_amount = sum(
            a.amount for a in portfolio.allocations
            if a.product.liquidity == LiquidityType.DAILY
        )
        daily_pct = daily_amount / total * 100

    if daily_pct >= 30:
        msg = f"[green]Boa liquidez:[/green] {fmt_pct(daily_pct, 0)} da carteira com resgate imediato"
    elif daily_pct >= 15:
        msg = f"[yellow]Liquidez moderada:[/yellow] {fmt_pct(daily_pct, 0)} com resgate imediato"
    else:
        msg = f"[red]Baixa liquidez:[/red] apenas {fmt_pct(daily_pct, 0)} com resgate imediato"
    console.print(f"  {msg}\n")
