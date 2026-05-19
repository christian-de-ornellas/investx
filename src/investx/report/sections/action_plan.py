"""Report section: step-by-step action plan."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from investx.models.market_data import MarketIndicators
from investx.models.portfolio import Portfolio
from investx.models.products import LiquidityType, ProductCategory
from investx.models.user_profile import Objective, UserProfile
from investx.report.formatters import fmt_currency


def render_action_plan(
    console: Console,
    profile: UserProfile,
    portfolio: Portfolio,
    indicators: MarketIndicators,
) -> None:
    steps: list[str] = []
    step = 0

    # Step 1: Open brokerage
    step += 1
    steps.append(
        f"[bold cyan]{step}.[/bold cyan] Abra conta em uma corretora de confianca "
        "(ex: XP, Rico, NuInvest, BTG, Inter). Prefira corretoras com taxa zero "
        "para Tesouro Direto e boas opcoes de renda fixa."
    )

    # Step 2: Emergency reserve check
    has_emergency = any(
        "reserva" in a.product.tags for a in portfolio.allocations
    )
    if has_emergency or profile.objective == Objective.EMERGENCY:
        step += 1
        steps.append(
            f"[bold cyan]{step}.[/bold cyan] Monte sua reserva de emergencia primeiro. "
            "Recomendamos 6 meses de gastos mensais em Tesouro Selic ou CDB com "
            "liquidez diaria (100% CDI)."
        )

    # Step 3: Invest in order of priority
    step += 1
    order_lines: list[str] = []
    # Sort: liquid first, then medium, then low
    priority = {LiquidityType.DAILY: 0, LiquidityType.SHORT: 1, LiquidityType.MEDIUM: 2, LiquidityType.LOW: 3}
    sorted_allocs = sorted(portfolio.allocations, key=lambda a: priority.get(a.product.liquidity, 9))

    for alloc in sorted_allocs:
        order_lines.append(
            f"   - {alloc.product.name}: {fmt_currency(alloc.amount)}"
        )
    steps.append(
        f"[bold cyan]{step}.[/bold cyan] Realize os investimentos na seguinte ordem "
        "(priorizando liquidez):\n" + "\n".join(order_lines)
    )

    # Step 4: Contributions
    if profile.monthly_contribution > 0:
        step += 1
        steps.append(
            f"[bold cyan]{step}.[/bold cyan] Configure aportes mensais de "
            f"{fmt_currency(profile.monthly_contribution)}. "
            "Mantenha as mesmas proporcoes da carteira recomendada ou "
            "rebalanceie trimestralmente."
        )

    # Step 5: Rebalancing
    step += 1
    steps.append(
        f"[bold cyan]{step}.[/bold cyan] Rebalanceie a carteira a cada 3-6 meses. "
        "Quando uma classe de ativo ultrapassar 5 pontos percentuais da alocacao "
        "alvo, ajuste vendendo o excedente e comprando o deficitario."
    )

    # Step 6: Tax optimization
    has_taxable = any(
        a.product.tax_type.value == "ir_regressivo"
        for a in portfolio.allocations
    )
    if has_taxable:
        step += 1
        steps.append(
            f"[bold cyan]{step}.[/bold cyan] Otimize impostos: mantenha renda fixa "
            "por mais de 720 dias para pagar a menor aliquota de IR (15%). "
            "Evite resgates nos primeiros 30 dias (incide IOF)."
        )

    # Step 7: Review
    step += 1
    steps.append(
        f"[bold cyan]{step}.[/bold cyan] Revise sua estrategia anualmente ou quando "
        "houver mudancas significativas na sua vida (novo emprego, casamento, "
        "filhos) ou no cenario economico (mudancas na Selic, inflacao)."
    )

    content = "\n\n".join(steps)
    console.print(
        Panel(
            content,
            title="[bold]Plano de Acao Passo-a-Passo[/bold]",
            border_style="magenta",
            padding=(1, 2),
        )
    )
