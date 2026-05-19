"""Portfolio and allocation models."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal

from investx.models.products import InvestmentProduct


@dataclass
class AssetAllocation:
    product: InvestmentProduct
    weight: Decimal                 # 0-100 (percentual)
    amount: Decimal = Decimal("0")  # valor alocado em R$

    @property
    def weight_fraction(self) -> Decimal:
        return self.weight / Decimal("100")


@dataclass
class Portfolio:
    allocations: list[AssetAllocation] = field(default_factory=list)

    @property
    def total_amount(self) -> Decimal:
        return sum((a.amount for a in self.allocations), Decimal("0"))

    @property
    def total_weight(self) -> Decimal:
        return sum((a.weight for a in self.allocations), Decimal("0"))

    @property
    def avg_risk_score(self) -> Decimal:
        if not self.allocations:
            return Decimal("0")
        weighted = sum(
            a.weight_fraction * a.product.risk_score
            for a in self.allocations
        )
        return Decimal(str(round(float(weighted), 2)))

    def distribute(self, total: Decimal) -> None:
        """Set each allocation's amount based on weight."""
        for alloc in self.allocations:
            alloc.amount = (total * alloc.weight / Decimal("100")).quantize(
                Decimal("0.01")
            )
        # Ajustar rounding diff no ultimo item
        diff = total - sum(a.amount for a in self.allocations)
        if self.allocations and diff:
            self.allocations[-1].amount += diff
