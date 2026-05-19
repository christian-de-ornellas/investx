"""Market indicators from BCB."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass
class MarketIndicators:
    selic: Decimal          # taxa anual (ex: 14.25)
    cdi: Decimal            # taxa anual
    ipca: Decimal           # acumulado 12 meses
    poupanca: Decimal       # rendimento anual
    tr: Decimal             # taxa referencial anual
    fetched_at: date | None = None
    is_fallback: bool = False

    @property
    def cdi_monthly(self) -> Decimal:
        """CDI mensal equivalente (taxa efetiva)."""
        annual = self.cdi / Decimal("100")
        # (1 + annual)^(1/12) - 1
        monthly = (1 + float(annual)) ** (1 / 12) - 1
        return Decimal(str(round(monthly * 100, 4)))

    @property
    def selic_monthly(self) -> Decimal:
        annual = self.selic / Decimal("100")
        monthly = (1 + float(annual)) ** (1 / 12) - 1
        return Decimal(str(round(monthly * 100, 4)))

    @property
    def real_return(self) -> Decimal:
        """Retorno real (CDI - IPCA) simplificado."""
        return self.cdi - self.ipca
