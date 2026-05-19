"""Interactive prompts using Rich."""

from __future__ import annotations

from decimal import Decimal

from rich.console import Console
from rich.prompt import FloatPrompt, IntPrompt, Prompt

from investx.cli.validators import validate_age, validate_amount, validate_horizon
from investx.models.user_profile import Objective, RiskProfile, UserProfile
from investx.services.brokerages import get_all_brokerages

console = Console()


def _prompt_amount() -> Decimal:
    while True:
        raw = Prompt.ask(
            "[bold cyan]Qual o valor para investir?[/bold cyan] (ex: 50000)",
            console=console,
        )
        try:
            return validate_amount(raw)
        except ValueError as e:
            console.print(f"[red]{e}[/red]")


def _prompt_objective() -> Objective:
    console.print("\n[bold]Qual seu objetivo?[/bold]")
    options = list(Objective)
    for i, obj in enumerate(options, 1):
        console.print(f"  [cyan]{i}[/cyan]. {obj.label}")

    while True:
        choice = IntPrompt.ask("Escolha", console=console, default=3)
        if 1 <= choice <= len(options):
            return options[choice - 1]
        console.print(f"[red]Escolha entre 1 e {len(options)}[/red]")


def _prompt_risk() -> RiskProfile:
    console.print("\n[bold]Qual seu perfil de risco?[/bold]")
    options = list(RiskProfile)
    for i, rp in enumerate(options, 1):
        console.print(f"  [cyan]{i}[/cyan]. {rp.label}")

    while True:
        choice = IntPrompt.ask("Escolha", console=console, default=2)
        if 1 <= choice <= len(options):
            return options[choice - 1]
        console.print(f"[red]Escolha entre 1 e {len(options)}[/red]")


def _prompt_horizon() -> int:
    while True:
        months = IntPrompt.ask(
            "\n[bold cyan]Horizonte de investimento em meses?[/bold cyan] (ex: 24)",
            console=console,
        )
        try:
            return validate_horizon(months)
        except ValueError as e:
            console.print(f"[red]{e}[/red]")


def _prompt_age() -> int:
    while True:
        age = IntPrompt.ask(
            "\n[bold cyan]Sua idade?[/bold cyan]",
            console=console,
        )
        try:
            return validate_age(age)
        except ValueError as e:
            console.print(f"[red]{e}[/red]")


def _prompt_contribution() -> Decimal:
    raw = Prompt.ask(
        "\n[bold cyan]Aporte mensal?[/bold cyan] (0 se nenhum)",
        default="0",
        console=console,
    )
    try:
        return validate_amount(raw) if raw != "0" else Decimal("0")
    except ValueError:
        return Decimal("0")


def _prompt_brokerage() -> str:
    brokerages = get_all_brokerages()
    console.print("\n[bold]Qual sua corretora?[/bold]")
    for i, b in enumerate(brokerages, 1):
        console.print(f"  [cyan]{i}[/cyan]. {b.name}")
    console.print(f"  [cyan]{len(brokerages) + 1}[/cyan]. Outra / Nao tenho")

    while True:
        choice = IntPrompt.ask("Escolha", console=console, default=len(brokerages) + 1)
        if 1 <= choice <= len(brokerages):
            return brokerages[choice - 1].id
        if choice == len(brokerages) + 1:
            return "generic"
        console.print(f"[red]Escolha entre 1 e {len(brokerages) + 1}[/red]")


def collect_profile_interactive() -> UserProfile:
    """Collect all user inputs interactively."""
    console.print("\n[bold blue]===  InvestX - Analise de Investimentos  ===[/bold blue]\n")

    amount = _prompt_amount()
    objective = _prompt_objective()
    risk = _prompt_risk()
    horizon = _prompt_horizon()
    age = _prompt_age()
    contribution = _prompt_contribution()
    brokerage = _prompt_brokerage()

    return UserProfile(
        amount=amount,
        objective=objective,
        risk_profile=risk,
        horizon_months=horizon,
        age=age,
        monthly_contribution=contribution,
        brokerage=brokerage,
    )
