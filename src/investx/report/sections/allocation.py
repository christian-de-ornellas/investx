"""Report section: portfolio allocation table."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from investx.models.portfolio import Portfolio
from investx.report.formatters import fmt_currency, fmt_pct


def render_allocation(console: Console, portfolio: Portfolio) -> None:
    table = Table(title="Alocacao Recomendada", show_lines=True)
    table.add_column("Produto", style="bold")
    table.add_column("Categoria", style="dim")
    table.add_column("Peso", justify="right", style="cyan")
    table.add_column("Valor", justify="right", style="green")
    table.add_column("Risco", justify="center")

    for alloc in portfolio.allocations:
        risk_score = alloc.product.risk_score
        if risk_score <= 3:
            risk_style = "green"
        elif risk_score <= 6:
            risk_style = "yellow"
        else:
            risk_style = "red"

        risk_bar = "+" * risk_score + "-" * (10 - risk_score)

        table.add_row(
            alloc.product.name,
            alloc.product.category.value.replace("_", " ").title(),
            fmt_pct(alloc.weight, 1),
            fmt_currency(alloc.amount),
            f"[{risk_style}]{risk_bar}[/{risk_style}] ({risk_score}/10)",
        )

    table.add_section()
    table.add_row(
        "[bold]TOTAL[/bold]",
        "",
        fmt_pct(portfolio.total_weight, 1),
        fmt_currency(portfolio.total_amount),
        f"Media: {float(portfolio.avg_risk_score):.1f}/10",
    )

    console.print(Panel(table, border_style="blue"))
