"""Constants for BCB series codes, tax tables, and fiscal rules."""

from decimal import Decimal

# ---------------------------------------------------------------------------
# BCB SGS series codes
# ---------------------------------------------------------------------------
BCB_SERIES = {
    "selic_meta": 432,
    "cdi_daily": 12,
    "cdi_annual": 4391,
    "ipca_monthly": 433,
    "ipca_annual": 13522,
    "poupanca": 25621,
    "tr": 226,
}

# ---------------------------------------------------------------------------
# IR Regressivo - renda fixa (tabela por dias corridos)
# ---------------------------------------------------------------------------
IR_BRACKETS: list[tuple[int, Decimal]] = [
    (180, Decimal("0.225")),   # ate 180 dias: 22.5%
    (360, Decimal("0.20")),    # 181-360 dias: 20%
    (720, Decimal("0.175")),   # 361-720 dias: 17.5%
    (999999, Decimal("0.15")), # acima de 720 dias: 15%
]

# ---------------------------------------------------------------------------
# IOF regressivo - primeiros 30 dias (% sobre rendimento)
# Dia 1 = 96%, dia 2 = 93%, ..., dia 30 = 0%
# ---------------------------------------------------------------------------
IOF_TABLE: list[int] = [
    96, 93, 90, 86, 83, 80, 76, 73, 70, 66,
    63, 60, 56, 53, 50, 46, 43, 40, 36, 33,
    30, 26, 23, 20, 16, 13, 10, 6, 3, 0,
]

# ---------------------------------------------------------------------------
# Acoes - isencao de IR para vendas ate R$20k/mes
# ---------------------------------------------------------------------------
ACOES_ISENCAO_MENSAL = Decimal("20000")
ACOES_IR_GANHO_CAPITAL = Decimal("0.15")
ACOES_IR_DAYTRADE = Decimal("0.20")

# ---------------------------------------------------------------------------
# FII - dividendos isentos PF, ganho capital 20%
# ---------------------------------------------------------------------------
FII_IR_GANHO_CAPITAL = Decimal("0.20")

# ---------------------------------------------------------------------------
# Poupanca - rendimento regras
# Selic > 8.5%: 0.5% a.m. + TR
# Selic <= 8.5%: 70% da Selic + TR
# ---------------------------------------------------------------------------
POUPANCA_SELIC_THRESHOLD = Decimal("8.5")
POUPANCA_TAXA_FIXA_MENSAL = Decimal("0.005")
POUPANCA_FATOR_SELIC = Decimal("0.70")

# ---------------------------------------------------------------------------
# Limites do sistema
# ---------------------------------------------------------------------------
MIN_INVESTMENT_AMOUNT = Decimal("100")
MAX_INVESTMENT_AMOUNT = Decimal("100000000")
MIN_AGE = 16
MAX_AGE = 100
MIN_HORIZON_MONTHS = 1
MAX_HORIZON_MONTHS = 480  # 40 anos
