"""Input validation for CLI."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation

from investx.config.constants import (
    MAX_AGE,
    MAX_HORIZON_MONTHS,
    MAX_INVESTMENT_AMOUNT,
    MIN_AGE,
    MIN_HORIZON_MONTHS,
    MIN_INVESTMENT_AMOUNT,
)


def validate_amount(value: str) -> Decimal:
    """Parse and validate an investment amount string."""
    cleaned = value.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
    try:
        amount = Decimal(cleaned)
    except InvalidOperation:
        raise ValueError(f"Valor invalido: '{value}'. Use formato numerico (ex: 50000 ou 50.000,00)")

    if amount < MIN_INVESTMENT_AMOUNT:
        raise ValueError(f"Valor minimo: R$ {MIN_INVESTMENT_AMOUNT}")
    if amount > MAX_INVESTMENT_AMOUNT:
        raise ValueError(f"Valor maximo: R$ {MAX_INVESTMENT_AMOUNT}")
    return amount


def validate_age(value: int) -> int:
    if value < MIN_AGE or value > MAX_AGE:
        raise ValueError(f"Idade deve estar entre {MIN_AGE} e {MAX_AGE} anos")
    return value


def validate_horizon(value: int) -> int:
    if value < MIN_HORIZON_MONTHS or value > MAX_HORIZON_MONTHS:
        raise ValueError(f"Horizonte deve estar entre {MIN_HORIZON_MONTHS} e {MAX_HORIZON_MONTHS} meses")
    return value
