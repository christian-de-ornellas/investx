"""Report section: detailed product descriptions."""

from __future__ import annotations

from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel
from rich.text import Text

from investx.models.market_data import MarketIndicators
from investx.models.portfolio import Portfolio
from investx.report.formatters import fmt_currency, fmt_pct


def _product_panel(alloc, indicators: MarketIndicators) -> Panel:
    p = alloc.product
    lines: list[str] = []
    lines.append(f"[dim]{p.description}[/dim]")
    lines.append("")
    lines.append(f"[bold]Valor alocado:[/bold] {fmt_currency(alloc.amount)}")
    lines.append(f"[bold]Peso:[/bold] {fmt_pct(alloc.weight, 1)}")

    # Return info
    if p.expected_return_pct_cdi is not None:
        ret = indicators.cdi * p.expected_return_pct_cdi / 100
        lines.append(f"[bold]Retorno estimado:[/bold] {fmt_pct(p.expected_return_pct_cdi, 0)} do CDI (~{fmt_pct(ret)} a.a.)")
    elif p.expected_return_fixed is not None:
        lines.append(f"[bold]Retorno estimado:[/bold] {fmt_pct(p.expected_return_fixed)} a.a. (prefixado)")
    elif p.expected_return_ipca_plus is not None:
        total = indicators.ipca + p.expected_return_ipca_plus
        lines.append(f"[bold]Retorno estimado:[/bold] IPCA + {fmt_pct(p.expected_return_ipca_plus)} (~{fmt_pct(total)} a.a.)")

    liquidity_labels = {
        "daily": "D+0/D+1 (diaria)",
        "short": "D+2 a D+5",
        "medium": "D+30 a D+90",
        "low": "Vencimento / +D+90",
    }
    lines.append(f"[bold]Liquidez:[/bold] {liquidity_labels.get(p.liquidity.value, p.liquidity.value)}")

    tax_labels = {
        "ir_regressivo": "IR Regressivo (22,5% a 15%)",
        "isento": "Isento de IR",
        "fii": "Dividendos isentos / GC 20%",
        "acoes": "15% sobre ganho de capital",
        "poupanca": "Isento",
    }
    lines.append(f"[bold]Tributacao:[/bold] {tax_labels.get(p.tax_type.value, p.tax_type.value)}")

    return Panel(
        "\n".join(lines),
        title=f"[bold]{p.name}[/bold]",
        border_style="cyan",
        width=60,
    )


def render_products(
    console: Console,
    portfolio: Portfolio,
    indicators: MarketIndicators,
) -> None:
    console.print("\n[bold underline]Detalhes dos Produtos Recomendados[/bold underline]\n")
    for alloc in portfolio.allocations:
        console.print(_product_panel(alloc, indicators))
