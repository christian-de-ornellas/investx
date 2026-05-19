"""User profile and risk preference models."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class Objective(str, Enum):
    EMERGENCY = "emergency"       # Reserva de emergencia
    SHORT_TERM = "short_term"     # Curto prazo (<1 ano)
    MIXED = "mixed"               # Medio prazo / misto
    RETIREMENT = "retirement"     # Aposentadoria
    GROWTH = "growth"             # Crescimento patrimonial
    INCOME = "income"             # Renda passiva

    @property
    def label(self) -> str:
        labels = {
            "emergency": "Reserva de Emergencia",
            "short_term": "Curto Prazo",
            "mixed": "Medio Prazo / Misto",
            "retirement": "Aposentadoria",
            "growth": "Crescimento Patrimonial",
            "income": "Renda Passiva",
        }
        return labels[self.value]


class RiskProfile(str, Enum):
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    BOLD = "bold"
    AGGRESSIVE = "aggressive"

    @property
    def label(self) -> str:
        labels = {
            "conservative": "Conservador",
            "moderate": "Moderado",
            "bold": "Arrojado",
            "aggressive": "Agressivo",
        }
        return labels[self.value]

    @property
    def score(self) -> int:
        """Risk score from 1 (conservative) to 4 (aggressive)."""
        scores = {
            "conservative": 1,
            "moderate": 2,
            "bold": 3,
            "aggressive": 4,
        }
        return scores[self.value]


@dataclass
class UserProfile:
    amount: Decimal
    objective: Objective
    risk_profile: RiskProfile
    horizon_months: int
    age: int
    monthly_contribution: Decimal = Decimal("0")

    @property
    def horizon_years(self) -> float:
        return self.horizon_months / 12
