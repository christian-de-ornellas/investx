"""Formatting utilities for Brazilian currency and percentages."""

from __future__ import annotations

from decimal import Decimal


def fmt_currency(value: Decimal | float | int) -> str:
    """Format as Brazilian Real: R$ 1.234,56"""
    v = float(value)
    if v < 0:
        return f"-R$ {abs(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_pct(value: Decimal | float, decimals: int = 2) -> str:
    """Format as percentage: 14,25%"""
    v = float(value)
    formatted = f"{v:.{decimals}f}".replace(".", ",")
    return f"{formatted}%"


def fmt_months(months: int) -> str:
    """Format months into a readable string."""
    if months < 12:
        return f"{months} {'mes' if months == 1 else 'meses'}"
    years = months // 12
    remaining = months % 12
    parts = [f"{years} {'ano' if years == 1 else 'anos'}"]
    if remaining:
        parts.append(f"{remaining} {'mes' if remaining == 1 else 'meses'}")
    return " e ".join(parts)
