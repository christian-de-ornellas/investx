"""Report generator - orchestrates all report sections."""

from __future__ import annotations

from rich.console import Console
from rich.rule import Rule
from rich.text import Text

from investx.models.market_data import MarketIndicators
from investx.models.portfolio import Portfolio
from investx.models.user_profile import UserProfile
from investx.report.sections.action_plan import render_action_plan
from investx.report.sections.allocation import render_allocation
from investx.report.sections.header import render_header
from investx.report.sections.liquidity import render_liquidity
from investx.report.sections.products import render_products
from investx.report.sections.projections import render_projections
from investx.report.sections.risk_analysis import render_risk_analysis
from investx.report.sections.tax import render_tax
from investx.services.projections import ProjectionResult


def generate_report(
    console: Console,
    profile: UserProfile,
    portfolio: Portfolio,
    indicators: MarketIndicators,
    projection: ProjectionResult,
) -> None:
    """Render the full investment report to the console."""
    console.print()
    console.print(
        Rule("[bold blue]InvestX - Relatorio de Investimentos[/bold blue]")
    )
    console.print()

    # 1. Header: profile + market indicators
    render_header(console, profile, indicators)
    console.print()

    # 2. Allocation table
    console.print(Rule("[bold]Alocacao[/bold]"))
    render_allocation(console, portfolio)
    console.print()

    # 3. Product details
    console.print(Rule("[bold]Produtos[/bold]"))
    render_products(console, portfolio, indicators)
    console.print()

    # 4. Projections
    console.print(Rule("[bold]Projecoes[/bold]"))
    render_projections(console, projection)
    console.print()

    # 5. Risk analysis
    console.print(Rule("[bold]Risco[/bold]"))
    render_risk_analysis(console, profile, portfolio)
    console.print()

    # 6. Liquidity analysis
    console.print(Rule("[bold]Liquidez[/bold]"))
    render_liquidity(console, portfolio)
    console.print()

    # 7. Tax considerations
    console.print(Rule("[bold]Tributacao[/bold]"))
    render_tax(console, profile, portfolio)
    console.print()

    # 8. Action plan
    console.print(Rule("[bold]Plano de Acao[/bold]"))
    render_action_plan(console, profile, portfolio, indicators)
    console.print()

    # Footer
    console.print(
        Rule("[dim]Este relatorio e apenas informativo e nao constitui recomendacao de investimento[/dim]")
    )
    console.print()
