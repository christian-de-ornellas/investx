"""Report section: return projections table."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from investx.report.formatters import fmt_currency, fmt_pct
from investx.services.projections import ProjectionResult


def render_projections(console: Console, result: ProjectionResult) -> None:
    table = Table(title="Projecao de Retorno", show_lines=True)
    table.add_column("Periodo", style="bold")
    table.add_column("Investido", justify="right")
    table.add_column("Saldo Bruto", justify="right", style="cyan")
    table.add_column("Saldo Liquido", justify="right", style="green")
    table.add_column("Ganho Liquido", justify="right", style="bold green")
    table.add_column("Poupanca", justify="right", style="dim")

    for row in result.rows:
        gain = row.net_balance - row.invested
        gain_style = "green" if gain >= 0 else "red"
        table.add_row(
            row.label,
            fmt_currency(row.invested),
            fmt_currency(row.gross_balance),
            fmt_currency(row.net_balance),
            f"[{gain_style}]{fmt_currency(gain)}[/{gain_style}]",
            fmt_currency(row.poupanca_balance),
        )

    console.print(Panel(table, border_style="green"))

    # Summary
    advantage = result.final_net - result.final_poupanca
    console.print(
        f"\n  [bold]Resumo Final:[/bold]"
        f"\n  Total investido:       {fmt_currency(result.total_invested)}"
        f"\n  Saldo bruto:           {fmt_currency(result.final_gross)}"
        f"\n  Impostos estimados:    {fmt_currency(result.total_tax_paid)}"
        f"\n  [bold green]Saldo liquido:       {fmt_currency(result.final_net)}[/bold green]"
        f"\n  Retorno liquido:       {fmt_pct(result.real_return_pct)}"
        f"\n  Poupanca (comparacao): {fmt_currency(result.final_poupanca)}"
        f"\n  [bold cyan]Vantagem vs poupanca:{fmt_currency(advantage)}[/bold cyan]\n"
    )
