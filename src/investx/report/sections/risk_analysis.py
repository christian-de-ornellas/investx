"""Report section: risk analysis."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from investx.models.portfolio import Portfolio
from investx.models.user_profile import UserProfile
from investx.services.risk import max_risk_score, risk_label


def render_risk_analysis(
    console: Console,
    profile: UserProfile,
    portfolio: Portfolio,
) -> None:
    max_score = max_risk_score(profile)
    avg_score = float(portfolio.avg_risk_score)

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("metric", style="bold")
    table.add_column("value")

    table.add_row("Perfil declarado:", profile.risk_profile.label)
    table.add_row("Score maximo ajustado:", f"{max_score}/10 ({risk_label(max_score)})")
    table.add_row("Score medio da carteira:", f"{avg_score:.1f}/10 ({risk_label(int(avg_score))})")

    # Risk distribution
    low = sum(1 for a in portfolio.allocations if a.product.risk_score <= 3)
    med = sum(1 for a in portfolio.allocations if 4 <= a.product.risk_score <= 6)
    high = sum(1 for a in portfolio.allocations if a.product.risk_score >= 7)

    table.add_row("", "")
    table.add_row("Ativos baixo risco (1-3):", f"{low} ativos")
    table.add_row("Ativos medio risco (4-6):", f"{med} ativos")
    table.add_row("Ativos alto risco (7-10):", f"{high} ativos")

    # Warnings
    warnings: list[str] = []
    if profile.age >= 55 and any(a.product.risk_score >= 7 for a in portfolio.allocations):
        warnings.append("Atencao: idade acima de 55 com ativos de alto risco")
    if profile.horizon_months <= 12 and any(a.product.risk_score >= 5 for a in portfolio.allocations):
        warnings.append("Atencao: horizonte curto com ativos de risco moderado/alto")
    if not warnings:
        warnings.append("Carteira dentro dos parametros de risco adequados")

    table.add_row("", "")
    for w in warnings:
        style = "yellow" if "Atencao" in w else "green"
        table.add_row("", f"[{style}]{w}[/{style}]")

    console.print(Panel(table, title="[bold]Analise de Risco[/bold]", border_style="yellow"))
