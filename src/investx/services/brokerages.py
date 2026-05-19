"""Brokerage catalog with platform-specific product tips."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class BrokerageInfo:
    id: str
    name: str
    url: str
    product_tips: dict[str, str] = field(default_factory=dict)
    highlights: list[str] = field(default_factory=list)
    caveats: list[str] = field(default_factory=list)


_BROKERAGES: dict[str, BrokerageInfo] = {
    "nubank": BrokerageInfo(
        id="nubank",
        name="Nubank / NuInvest",
        url="https://nubank.com.br",
        product_tips={
            "Tesouro Selic": "App Nubank > Investimentos > Tesouro Direto. Taxa zero de custodia ate R$10k.",
            "CDB Liquidez Diaria": "App Nubank > Nu Caixinha (RDB 100% CDI, resgate D+0). Tambem ha CDBs em Investimentos > Renda Fixa.",
            "CDB Prefixado (2 anos)": "App NuInvest > Renda Fixa > CDB. Filtre por 'Prefixado'.",
            "CDB IPCA+ (3 anos)": "App NuInvest > Renda Fixa > CDB. Filtre por 'IPCA+'.",
            "LCI": "App NuInvest > Renda Fixa > LCI. Disponibilidade varia.",
            "LCA": "App NuInvest > Renda Fixa > LCA. Disponibilidade varia.",
            "Debentures Incentivadas": "NuInvest > Renda Fixa > Debentures.",
            "Tesouro Prefixado (2029)": "App Nubank > Investimentos > Tesouro Direto > Prefixado.",
            "Tesouro IPCA+ 2035": "App Nubank > Investimentos > Tesouro Direto > IPCA+.",
            "Tesouro IPCA+ com Juros Semestrais": "App Nubank > Investimentos > Tesouro Direto > IPCA+ com Juros.",
            "Fundo RF Credito Privado": "NuInvest > Fundos > Renda Fixa.",
            "ETF BOVA11 (Ibovespa)": "NuInvest > Bolsa > busque 'BOVA11'.",
            "ETF IVVB11 (S&P 500)": "NuInvest > Bolsa > busque 'IVVB11'.",
            "Acoes (carteira diversificada)": "NuInvest > Bolsa > Acoes.",
            "Fundos Imobiliarios (FIIs)": "NuInvest > Bolsa > Fundos Imobiliarios.",
            "Fundo Multimercado": "NuInvest > Fundos > Multimercado.",
        },
        highlights=[
            "Nu Caixinha rende 100% CDI com resgate instantaneo (D+0)",
            "Tesouro Direto com taxa zero de custodia ate R$10.000",
            "Interface simples e intuitiva no app",
            "Sem taxa de corretagem para acoes e FIIs na NuInvest",
        ],
        caveats=[
            "Menor variedade de CDBs e LCIs comparado a corretoras maiores",
            "Plataforma NuInvest separada do app Nubank para alguns produtos",
            "Analises e ferramentas de renda variavel mais basicas",
        ],
    ),
    "xp": BrokerageInfo(
        id="xp",
        name="XP Investimentos",
        url="https://www.xpi.com.br",
        product_tips={
            "Tesouro Selic": "Portal XP > Renda Fixa > Tesouro Direto. Taxa zero.",
            "CDB Liquidez Diaria": "Portal XP > Renda Fixa > CDB > filtre 'Liquidez Diaria'.",
            "CDB Prefixado (2 anos)": "Portal XP > Renda Fixa > CDB > filtre 'Prefixado'.",
            "CDB IPCA+ (3 anos)": "Portal XP > Renda Fixa > CDB > filtre 'IPCA+'.",
            "LCI": "Portal XP > Renda Fixa > LCI. Ampla selecao de emissores.",
            "LCA": "Portal XP > Renda Fixa > LCA. Ampla selecao de emissores.",
            "Debentures Incentivadas": "Portal XP > Renda Fixa > Debentures > filtre 'Incentivada'.",
            "Tesouro Prefixado (2029)": "Portal XP > Renda Fixa > Tesouro Direto > Prefixado.",
            "Tesouro IPCA+ 2035": "Portal XP > Renda Fixa > Tesouro Direto > IPCA+.",
            "Tesouro IPCA+ com Juros Semestrais": "Portal XP > Renda Fixa > Tesouro Direto > IPCA+ com Juros.",
            "Fundo RF Credito Privado": "Portal XP > Fundos de Investimento > Renda Fixa.",
            "ETF BOVA11 (Ibovespa)": "Portal XP > Bolsa > busque 'BOVA11'. Corretagem zero para ETFs.",
            "ETF IVVB11 (S&P 500)": "Portal XP > Bolsa > busque 'IVVB11'.",
            "Acoes (carteira diversificada)": "Portal XP > Bolsa > Acoes. Confira as carteiras recomendadas.",
            "Fundos Imobiliarios (FIIs)": "Portal XP > Fundos Imobiliarios. Veja a lista de FIIs recomendados.",
            "Fundo Multimercado": "Portal XP > Fundos de Investimento > Multimercado.",
        },
        highlights=[
            "Maior variedade de produtos de renda fixa do mercado",
            "Carteiras recomendadas por analistas para acoes e FIIs",
            "Tesouro Direto com taxa zero",
            "Plataforma completa com home broker profissional",
        ],
        caveats=[
            "Alguns fundos possuem taxa de administracao elevada",
            "Interface pode ser complexa para iniciantes",
            "CDBs de liquidez diaria nem sempre tem as melhores taxas",
        ],
    ),
    "btg": BrokerageInfo(
        id="btg",
        name="BTG Pactual",
        url="https://www.btgpactual.com",
        product_tips={
            "Tesouro Selic": "App BTG > Investir > Renda Fixa > Tesouro Direto. Taxa zero.",
            "CDB Liquidez Diaria": "App BTG > Investir > Renda Fixa > CDB. Veja o 'CDB BTG' com liquidez diaria.",
            "CDB Prefixado (2 anos)": "App BTG > Investir > Renda Fixa > CDB > Prefixado.",
            "CDB IPCA+ (3 anos)": "App BTG > Investir > Renda Fixa > CDB > IPCA+.",
            "LCI": "App BTG > Investir > Renda Fixa > LCI.",
            "LCA": "App BTG > Investir > Renda Fixa > LCA.",
            "Debentures Incentivadas": "App BTG > Investir > Renda Fixa > Debentures.",
            "Tesouro Prefixado (2029)": "App BTG > Investir > Renda Fixa > Tesouro Direto > Prefixado.",
            "Tesouro IPCA+ 2035": "App BTG > Investir > Renda Fixa > Tesouro Direto > IPCA+.",
            "Tesouro IPCA+ com Juros Semestrais": "App BTG > Investir > Renda Fixa > Tesouro Direto > IPCA+ com Juros.",
            "Fundo RF Credito Privado": "App BTG > Investir > Fundos > Renda Fixa.",
            "ETF BOVA11 (Ibovespa)": "App BTG > Investir > Renda Variavel > busque 'BOVA11'.",
            "ETF IVVB11 (S&P 500)": "App BTG > Investir > Renda Variavel > busque 'IVVB11'.",
            "Acoes (carteira diversificada)": "App BTG > Investir > Renda Variavel > Acoes.",
            "Fundos Imobiliarios (FIIs)": "App BTG > Investir > Renda Variavel > Fundos Imobiliarios.",
            "Fundo Multimercado": "App BTG > Investir > Fundos > Multimercado.",
        },
        highlights=[
            "CDB BTG proprio com taxas competitivas e liquidez diaria",
            "Tesouro Direto com taxa zero",
            "Acesso a fundos exclusivos BTG",
            "Plataforma robusta para todos os perfis",
        ],
        caveats=[
            "Investimento minimo em alguns fundos pode ser elevado",
            "App pode parecer complexo para iniciantes",
            "Atendimento premium focado em clientes de alta renda",
        ],
    ),
    "inter": BrokerageInfo(
        id="inter",
        name="Banco Inter",
        url="https://www.bancointer.com.br",
        product_tips={
            "Tesouro Selic": "App Inter > Investimentos > Renda Fixa > Tesouro Direto. Taxa zero.",
            "CDB Liquidez Diaria": "App Inter > Investimentos > Renda Fixa > CDB. Veja tambem os 'Cofrinhos' para reserva.",
            "CDB Prefixado (2 anos)": "App Inter > Investimentos > Renda Fixa > CDB > Prefixado.",
            "CDB IPCA+ (3 anos)": "App Inter > Investimentos > Renda Fixa > CDB > IPCA+.",
            "LCI": "App Inter > Investimentos > Renda Fixa > LCI.",
            "LCA": "App Inter > Investimentos > Renda Fixa > LCA.",
            "Debentures Incentivadas": "App Inter > Investimentos > Renda Fixa > Debentures.",
            "Tesouro Prefixado (2029)": "App Inter > Investimentos > Renda Fixa > Tesouro Direto > Prefixado.",
            "Tesouro IPCA+ 2035": "App Inter > Investimentos > Renda Fixa > Tesouro Direto > IPCA+.",
            "Tesouro IPCA+ com Juros Semestrais": "App Inter > Investimentos > Renda Fixa > Tesouro Direto > IPCA+ com Juros.",
            "Fundo RF Credito Privado": "App Inter > Investimentos > Fundos > Renda Fixa.",
            "ETF BOVA11 (Ibovespa)": "App Inter > Investimentos > Renda Variavel > busque 'BOVA11'.",
            "ETF IVVB11 (S&P 500)": "App Inter > Investimentos > Renda Variavel > busque 'IVVB11'.",
            "Acoes (carteira diversificada)": "App Inter > Investimentos > Renda Variavel > Acoes.",
            "Fundos Imobiliarios (FIIs)": "App Inter > Investimentos > Renda Variavel > Fundos Imobiliarios.",
            "Fundo Multimercado": "App Inter > Investimentos > Fundos > Multimercado.",
        },
        highlights=[
            "Cofrinhos: reserva automatica com rendimento de 100% CDI",
            "Tesouro Direto com taxa zero",
            "Super app com conta, cartao, investimentos e shopping",
            "Cashback em compras que pode ser investido automaticamente",
        ],
        caveats=[
            "Variedade de renda fixa menor que corretoras especializadas",
            "Home broker mais simples que plataformas dedicadas",
            "Algumas funcionalidades requerem plano pago (Inter Black)",
        ],
    ),
    "rico": BrokerageInfo(
        id="rico",
        name="Rico Investimentos",
        url="https://www.rico.com.vc",
        product_tips={
            "Tesouro Selic": "Portal Rico > Renda Fixa > Tesouro Direto. Taxa zero.",
            "CDB Liquidez Diaria": "Portal Rico > Renda Fixa > CDB > filtre 'Liquidez Diaria'.",
            "CDB Prefixado (2 anos)": "Portal Rico > Renda Fixa > CDB > filtre 'Prefixado'.",
            "CDB IPCA+ (3 anos)": "Portal Rico > Renda Fixa > CDB > filtre 'IPCA+'.",
            "LCI": "Portal Rico > Renda Fixa > LCI.",
            "LCA": "Portal Rico > Renda Fixa > LCA.",
            "Debentures Incentivadas": "Portal Rico > Renda Fixa > Debentures.",
            "Tesouro Prefixado (2029)": "Portal Rico > Renda Fixa > Tesouro Direto > Prefixado.",
            "Tesouro IPCA+ 2035": "Portal Rico > Renda Fixa > Tesouro Direto > IPCA+.",
            "Tesouro IPCA+ com Juros Semestrais": "Portal Rico > Renda Fixa > Tesouro Direto > IPCA+ com Juros.",
            "Fundo RF Credito Privado": "Portal Rico > Fundos de Investimento > Renda Fixa.",
            "ETF BOVA11 (Ibovespa)": "Portal Rico > Bolsa > busque 'BOVA11'.",
            "ETF IVVB11 (S&P 500)": "Portal Rico > Bolsa > busque 'IVVB11'.",
            "Acoes (carteira diversificada)": "Portal Rico > Bolsa > Acoes. Confira a 'Carteira Rico'.",
            "Fundos Imobiliarios (FIIs)": "Portal Rico > Fundos Imobiliarios.",
            "Fundo Multimercado": "Portal Rico > Fundos de Investimento > Multimercado.",
        },
        highlights=[
            "Interface simplificada e amigavel para iniciantes",
            "Carteira Rico com sugestoes prontas de investimento",
            "Tesouro Direto com taxa zero",
            "Mesma plataforma XP com acesso aos mesmos produtos",
        ],
        caveats=[
            "Mesma base de produtos da XP, porem com menos destaque em analises",
            "Conteudo educacional menor que o da XP",
            "Migracao de ativos pode ser necessaria se ja tiver conta na XP",
        ],
    ),
    "generic": BrokerageInfo(
        id="generic",
        name="Corretora Generica",
        url="",
        product_tips={},
        highlights=[],
        caveats=[],
    ),
}


def get_brokerage(brokerage_id: str) -> BrokerageInfo | None:
    """Return brokerage info by id, or None if not found."""
    return _BROKERAGES.get(brokerage_id.lower())


def get_all_brokerages() -> list[BrokerageInfo]:
    """Return all brokerages (excluding generic)."""
    return [b for b in _BROKERAGES.values() if b.id != "generic"]
