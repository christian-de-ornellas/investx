"""Typer CLI application with `analyze` and `rates` commands."""

from __future__ import annotations

from decimal import Decimal
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from investx import __version__

app = typer.Typer(
    name="investx",
    help="InvestX - Sistema de consultoria de investimentos para o mercado brasileiro.",
    no_args_is_help=True,
)
console = Console()


@app.command()
def rates() -> None:
    """Exibe as taxas atuais do mercado (Selic, CDI, IPCA)."""
    from investx.clients.bcb import fetch_market_indicators
    from investx.report.formatters import fmt_pct

    with console.status("[bold green]Buscando dados do Banco Central...[/bold green]"):
        indicators = fetch_market_indicators()

    table = Table(title="Indicadores de Mercado")
    table.add_column("Indicador", style="bold")
    table.add_column("Taxa Anual", justify="right", style="green")
    table.add_column("Taxa Mensal", justify="right", style="cyan")

    table.add_row("Selic Meta", fmt_pct(indicators.selic), fmt_pct(indicators.selic_monthly, 4))
    table.add_row("CDI", fmt_pct(indicators.cdi), fmt_pct(indicators.cdi_monthly, 4))
    table.add_row("IPCA (12m)", fmt_pct(indicators.ipca), "-")
    table.add_row("Poupanca", fmt_pct(indicators.poupanca), "-")
    table.add_row("TR", fmt_pct(indicators.tr), "-")
    table.add_row("Retorno Real", fmt_pct(indicators.real_return), "-")

    console.print()
    console.print(table)

    if indicators.is_fallback:
        console.print("\n[yellow]Dados estimados (API BCB indisponivel)[/yellow]")
    else:
        console.print(f"\n[dim]Dados obtidos em {indicators.fetched_at}[/dim]")


@app.command()
def analyze(
    amount: Optional[float] = typer.Option(None, "--amount", "-a", help="Valor inicial em R$"),
    objective: Optional[str] = typer.Option(None, "--objective", "-o", help="Objetivo: emergency, short_term, mixed, retirement, growth, income"),
    risk: Optional[str] = typer.Option(None, "--risk", "-r", help="Perfil de risco: conservative, moderate, bold, aggressive"),
    horizon: Optional[int] = typer.Option(None, "--horizon", "-h", help="Horizonte em meses"),
    age: Optional[int] = typer.Option(None, "--age", help="Idade do investidor"),
    contribution: float = typer.Option(0, "--contribution", "-c", help="Aporte mensal em R$"),
    no_interactive: bool = typer.Option(False, "--no-interactive", help="Modo nao-interativo (requer todos os parametros)"),
) -> None:
    """Analisa seu perfil e gera recomendacoes de investimento."""
    from investx.clients.bcb import fetch_market_indicators
    from investx.cli.prompts import collect_profile_interactive
    from investx.models.user_profile import Objective as ObjEnum
    from investx.models.user_profile import RiskProfile, UserProfile
    from investx.report.generator import generate_report
    from investx.services.allocation import build_portfolio
    from investx.services.projections import generate_projections

    profile: UserProfile

    if no_interactive:
        # Validate required params
        missing = []
        if amount is None:
            missing.append("--amount")
        if objective is None:
            missing.append("--objective")
        if risk is None:
            missing.append("--risk")
        if horizon is None:
            missing.append("--horizon")
        if age is None:
            missing.append("--age")

        if missing:
            console.print(f"[red]Parametros obrigatorios no modo nao-interativo: {', '.join(missing)}[/red]")
            raise typer.Exit(1)

        try:
            obj_enum = ObjEnum(objective)
        except ValueError:
            valid = ", ".join(o.value for o in ObjEnum)
            console.print(f"[red]Objetivo invalido: '{objective}'. Validos: {valid}[/red]")
            raise typer.Exit(1)

        try:
            risk_enum = RiskProfile(risk)
        except ValueError:
            valid = ", ".join(r.value for r in RiskProfile)
            console.print(f"[red]Perfil de risco invalido: '{risk}'. Validos: {valid}[/red]")
            raise typer.Exit(1)

        profile = UserProfile(
            amount=Decimal(str(amount)),
            objective=obj_enum,
            risk_profile=risk_enum,
            horizon_months=horizon,  # type: ignore[arg-type]
            age=age,  # type: ignore[arg-type]
            monthly_contribution=Decimal(str(contribution)),
        )
    else:
        profile = collect_profile_interactive()

    # Fetch market data
    with console.status("[bold green]Buscando dados do Banco Central...[/bold green]"):
        indicators = fetch_market_indicators()

    # Build portfolio
    portfolio = build_portfolio(profile, indicators)

    # Generate projections
    projection = generate_projections(profile, portfolio, indicators)

    # Render report
    generate_report(console, profile, portfolio, indicators, projection)


@app.command()
def version() -> None:
    """Exibe a versao do InvestX."""
    console.print(f"InvestX v{__version__}")
