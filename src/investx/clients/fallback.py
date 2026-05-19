"""Fallback market data when BCB API is unavailable."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from investx.config.settings import settings
from investx.models.market_data import MarketIndicators


def get_fallback_indicators() -> MarketIndicators:
    return MarketIndicators(
        selic=Decimal(str(settings.fallback_selic)),
        cdi=Decimal(str(settings.fallback_cdi)),
        ipca=Decimal(str(settings.fallback_ipca)),
        poupanca=Decimal(str(settings.fallback_poupanca)),
        tr=Decimal(str(settings.fallback_tr)),
        fetched_at=date.today(),
        is_fallback=True,
    )
