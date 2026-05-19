"""Client for the BCB SGS API."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

import httpx

from investx.clients.fallback import get_fallback_indicators
from investx.config.constants import BCB_SERIES
from investx.config.settings import settings
from investx.models.market_data import MarketIndicators


def _fetch_series(code: int, n: int = 1) -> Decimal | None:
    """Fetch the last *n* values of a BCB SGS series and return the latest."""
    url = f"{settings.bcb_base_url}.{code}/dados/ultimos/{n}?formato=json"
    try:
        resp = httpx.get(url, timeout=settings.bcb_timeout_seconds)
        resp.raise_for_status()
        data = resp.json()
        if data:
            return Decimal(str(data[-1]["valor"]).replace(",", "."))
    except (httpx.HTTPError, KeyError, IndexError, ValueError):
        pass
    return None


def _annualize_cdi_daily(daily_rate: Decimal) -> Decimal:
    """Convert a daily CDI rate (e.g. 0.052%) to annual."""
    factor = 1 + float(daily_rate) / 100
    annual = (factor ** 252 - 1) * 100
    return Decimal(str(round(annual, 2)))


def _annualize_cdi_monthly(monthly_rate: Decimal) -> Decimal:
    """Convert a monthly CDI rate to annual."""
    factor = 1 + float(monthly_rate) / 100
    annual = (factor ** 12 - 1) * 100
    return Decimal(str(round(annual, 2)))


def fetch_market_indicators() -> MarketIndicators:
    """Fetch current market indicators from BCB, falling back on error."""
    selic = _fetch_series(BCB_SERIES["selic_meta"])
    cdi_daily = _fetch_series(BCB_SERIES["cdi_daily"])
    cdi_monthly = _fetch_series(BCB_SERIES["cdi_annual"])  # 4391 is monthly
    ipca = _fetch_series(BCB_SERIES["ipca_annual"])
    poupanca = _fetch_series(BCB_SERIES["poupanca"])
    tr = _fetch_series(BCB_SERIES["tr"])

    # Annualize CDI: prefer daily rate (more precise), fallback to monthly
    cdi: Decimal | None = None
    if cdi_daily is not None:
        cdi = _annualize_cdi_daily(cdi_daily)
    elif cdi_monthly is not None:
        cdi = _annualize_cdi_monthly(cdi_monthly)

    # If any critical indicator is missing, use full fallback
    if any(v is None for v in [selic, cdi, ipca]):
        return get_fallback_indicators()

    # Poupanca estimation if unavailable
    if poupanca is None:
        assert selic is not None
        from investx.config.constants import (
            POUPANCA_FATOR_SELIC,
            POUPANCA_SELIC_THRESHOLD,
            POUPANCA_TAXA_FIXA_MENSAL,
        )

        if selic > POUPANCA_SELIC_THRESHOLD:
            poupanca = ((1 + float(POUPANCA_TAXA_FIXA_MENSAL)) ** 12 - 1) * 100
            poupanca = Decimal(str(round(poupanca, 2)))
        else:
            poupanca = (selic * POUPANCA_FATOR_SELIC).quantize(Decimal("0.01"))

    return MarketIndicators(
        selic=selic,  # type: ignore[arg-type]
        cdi=cdi,  # type: ignore[arg-type]
        ipca=ipca,  # type: ignore[arg-type]
        poupanca=poupanca,
        tr=tr or Decimal("0.0"),
        fetched_at=date.today(),
        is_fallback=False,
    )
