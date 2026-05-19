"""Risk scoring and profile adjustments."""

from __future__ import annotations

from investx.models.user_profile import Objective, RiskProfile, UserProfile


def max_risk_score(profile: UserProfile) -> int:
    """Determine the maximum acceptable risk score (1-10) for the user."""
    base = {
        RiskProfile.CONSERVATIVE: 3,
        RiskProfile.MODERATE: 5,
        RiskProfile.BOLD: 7,
        RiskProfile.AGGRESSIVE: 10,
    }[profile.risk_profile]

    # Objective adjustment
    obj_adj = {
        Objective.EMERGENCY: -2,
        Objective.SHORT_TERM: -1,
        Objective.MIXED: 0,
        Objective.RETIREMENT: 0,
        Objective.GROWTH: 1,
        Objective.INCOME: 0,
    }[profile.objective]

    # Age adjustment: reduce risk for older investors
    age_adj = 0
    if profile.age >= 60:
        age_adj = -2
    elif profile.age >= 50:
        age_adj = -1
    elif profile.age < 25:
        age_adj = 1

    # Horizon adjustment: shorter horizon = less risk
    horizon_adj = 0
    if profile.horizon_months <= 6:
        horizon_adj = -2
    elif profile.horizon_months <= 12:
        horizon_adj = -1
    elif profile.horizon_months >= 120:
        horizon_adj = 1

    score = base + obj_adj + age_adj + horizon_adj
    return max(1, min(10, score))


def risk_label(score: int) -> str:
    if score <= 2:
        return "Muito Baixo"
    if score <= 4:
        return "Baixo"
    if score <= 6:
        return "Moderado"
    if score <= 8:
        return "Alto"
    return "Muito Alto"
