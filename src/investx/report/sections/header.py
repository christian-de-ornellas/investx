"""Report header: user profile summary and market indicators."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from investx.models.market_data import MarketIndicators
from investx.models.user_profile import UserProfile
from investx.report.formatters import fmt_currency, fmt_months, fmt_pct
from investx.services.brokerages import BrokerageInfo


def render_header(
    console: Console,
    profile: UserProfile,
    indicators: MarketIndicators,
    brokerage_info: BrokerageInfo | None = None,
) -> None:
    # Profile summary
    profile_table = Table(show_header=False, box=None, padding=(0, 2))
    profile_table.add_column("field", style="bold cyan")
    profile_table.add_column("value")

    profile_table.add_row("Valor inicial:", fmt_currency(profile.amount))
    if profile.monthly_contribution > 0:
        profile_table.add_row("Aporte mensal:", fmt_currency(profile.monthly_contribution))
    profile_table.add_row("Objetivo:", profile.objective.label)
    profile_table.add_row("Perfil de risco:", profile.risk_profile.label)
    profile_table.add_row("Horizonte:", fmt_months(profile.horizon_months))
    profile_table.add_row("Idade:", f"{profile.age} anos")
    if brokerage_info and brokerage_info.id != "generic":
        profile_table.add_row("Corretora:", brokerage_info.name)

    console.print(Panel(profile_table, title="[bold]Perfil do Investidor[/bold]", border_style="blue"))

    # Market indicators
    ind_table = Table(show_header=False, box=None, padding=(0, 2))
    ind_table.add_column("indicator", style="bold green")
    ind_table.add_column("value")

    ind_table.add_row("Selic Meta:", fmt_pct(indicators.selic))
    ind_table.add_row("CDI:", fmt_pct(indicators.cdi))
    ind_table.add_row("IPCA (12m):", fmt_pct(indicators.ipca))
    ind_table.add_row("Poupanca:", fmt_pct(indicators.poupanca))
    ind_table.add_row("Retorno Real:", fmt_pct(indicators.real_return))

    fallback_note = ""
    if indicators.is_fallback:
        fallback_note = " [dim](dados estimados - API BCB indisponivel)[/dim]"

    console.print(
        Panel(
            ind_table,
            title=f"[bold]Indicadores de Mercado[/bold]{fallback_note}",
            border_style="green",
        )
    )
