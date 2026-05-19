"""Report section: brokerage-specific investment tips."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from investx.models.portfolio import Portfolio
from investx.services.brokerages import BrokerageInfo


def render_brokerage(
    console: Console,
    portfolio: Portfolio,
    brokerage: BrokerageInfo,
) -> None:
    """Render brokerage-specific tips for each allocated product."""
    # Product tips table
    table = Table(
        title=f"[bold]Onde Encontrar na {brokerage.name}[/bold]",
        show_lines=True,
    )
    table.add_column("Produto", style="bold cyan", ratio=1)
    table.add_column("Como Investir na Plataforma", ratio=2)

    for alloc in portfolio.allocations:
        tip = brokerage.product_tips.get(
            alloc.product.name,
            "Busque na area de investimentos da sua corretora.",
        )
        table.add_row(alloc.product.name, tip)

    console.print(table)

    # Highlights and caveats
    lines: list[str] = []
    if brokerage.highlights:
        lines.append("[bold green]Destaques:[/bold green]")
        for h in brokerage.highlights:
            lines.append(f"  [green]+[/green] {h}")

    if brokerage.caveats:
        if lines:
            lines.append("")
        lines.append("[bold yellow]Pontos de Atencao:[/bold yellow]")
        for c in brokerage.caveats:
            lines.append(f"  [yellow]![/yellow] {c}")

    if lines:
        console.print()
        console.print(
            Panel(
                "\n".join(lines),
                title=f"[bold]{brokerage.name}[/bold]",
                border_style="cyan",
                padding=(1, 2),
            )
        )
