# Arquitetura e Referencia Tecnica — InvestX

## Sumario

1. [Visao Geral](#visao-geral)
2. [Stack Tecnologica](#stack-tecnologica)
3. [Estrutura do Projeto](#estrutura-do-projeto)
4. [Modulos](#modulos)
   - [Config](#config)
   - [Models](#models)
   - [Clients](#clients)
   - [Services](#services)
   - [Report](#report)
   - [CLI](#cli)
5. [Fluxo de Execucao](#fluxo-de-execucao)
6. [API do Banco Central](#api-do-banco-central)
7. [Regras Fiscais](#regras-fiscais)
8. [Motor de Alocacao](#motor-de-alocacao)
9. [Projecoes Financeiras](#projecoes-financeiras)
10. [Configuracao e Extensibilidade](#configuracao-e-extensibilidade)

---

## Visao Geral

O InvestX e um sistema CLI que:

1. Coleta o perfil do investidor (valor, objetivo, risco, horizonte, idade)
2. Busca indicadores de mercado em tempo real da API do Banco Central
3. Constroi uma carteira otimizada com base em templates de alocacao
4. Calcula projecoes de retorno com juros compostos
5. Gera um relatorio completo formatado no terminal

```
                    ┌─────────────┐
                    │   Usuario   │
                    └──────┬──────┘
                           │ inputs
                    ┌──────▼──────┐
                    │  CLI (Typer)│
                    └──────┬──────┘
                           │ UserProfile
              ┌────────────┼────────────┐
              │            │            │
      ┌───────▼──────┐ ┌──▼────┐ ┌─────▼──────┐
      │  BCB Client  │ │ Risk  │ │ Allocation │
      └───────┬──────┘ └──┬────┘ └─────┬──────┘
              │            │            │
      MarketIndicators  MaxRisk     Portfolio
              │            │            │
              └────────────┼────────────┘
                           │
                    ┌──────▼──────┐
                    │ Projections │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   Report    │
                    │  Generator  │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Terminal   │
                    │  (Rich)    │
                    └─────────────┘
```

---

## Stack Tecnologica

| Tecnologia         | Versao   | Uso                                  |
|--------------------|----------|--------------------------------------|
| Python             | 3.10+    | Linguagem principal                  |
| uv                 | latest   | Gerenciamento de pacotes e ambientes |
| Typer              | 0.15+    | Framework CLI                        |
| Rich               | 13+      | Formatacao e tabelas no terminal     |
| httpx              | 0.28+    | Requisicoes HTTP (API BCB)           |
| Pydantic           | 2.0+     | Validacao de dados                   |
| Pydantic Settings  | 2.0+     | Configuracao via variaveis de ambiente |
| Decimal (stdlib)   | —        | Precisao em calculos financeiros     |

---

## Estrutura do Projeto

```
investx/
├── pyproject.toml                 # Dependencias e configuracao do projeto
├── README.md                      # Documentacao principal
├── docs/
│   ├── guia-de-uso.md             # Guia de uso completo
│   └── arquitetura.md             # Este documento
└── src/investx/
    ├── __init__.py                # Versao do pacote
    ├── __main__.py                # Ponto de entrada `python -m investx`
    ├── config/
    │   ├── constants.py           # Series BCB, tabelas IR/IOF, limites
    │   └── settings.py            # Pydantic Settings (URLs, fallbacks)
    ├── models/
    │   ├── user_profile.py        # UserProfile, Objective, RiskProfile
    │   ├── products.py            # InvestmentProduct, categorias, taxacao
    │   ├── market_data.py         # MarketIndicators (Selic, CDI, IPCA)
    │   └── portfolio.py           # Portfolio, AssetAllocation
    ├── clients/
    │   ├── bcb.py                 # Cliente API BCB (Selic, CDI, IPCA, TR)
    │   └── fallback.py            # Valores fallback quando API indisponivel
    ├── services/
    │   ├── products_catalog.py    # Catalogo de 17 produtos brasileiros
    │   ├── tax.py                 # IR regressivo, IOF, isencoes
    │   ├── risk.py                # Score de risco, ajustes
    │   ├── allocation.py          # Motor de alocacao (24 templates)
    │   └── projections.py         # Juros compostos, projecoes
    ├── cli/
    │   ├── app.py                 # Typer app: comandos analyze/rates/version
    │   ├── prompts.py             # Prompts interativos com Rich
    │   └── validators.py          # Validacao de inputs
    └── report/
        ├── formatters.py          # fmt_currency, fmt_pct, fmt_months
        ├── generator.py           # Orquestrador do relatorio
        └── sections/
            ├── header.py          # Perfil + indicadores de mercado
            ├── allocation.py      # Tabela de alocacao
            ├── products.py        # Detalhes dos produtos
            ├── projections.py     # Projecoes de retorno
            ├── risk_analysis.py   # Analise de risco
            ├── liquidity.py       # Analise de liquidez
            ├── tax.py             # Consideracoes fiscais
            └── action_plan.py     # Plano de acao passo-a-passo
```

Total: **29 arquivos Python** organizados em 7 pacotes.

---

## Modulos

### Config

#### `config/constants.py`

Define todas as constantes do sistema:

- **`BCB_SERIES`** — codigos das series da API SGS do Banco Central
- **`IR_BRACKETS`** — tabela do IR regressivo (22,5% a 15%)
- **`IOF_TABLE`** — tabela de IOF dos primeiros 30 dias (96% a 0%)
- **Regras de acoes** — isencao para vendas < R$ 20k/mes, aliquota de 15%
- **Regras de FII** — dividendos isentos, ganho de capital 20%
- **Regras de poupanca** — formula baseada na Selic (threshold de 8,5%)
- **Limites** — valor minimo/maximo, idade, horizonte

#### `config/settings.py`

Classe `Settings` (Pydantic Settings) com configuracoes ajustaveis via variaveis de ambiente com prefixo `INVESTX_`:

- URL base da API BCB
- Timeout e retries para requisicoes HTTP
- Valores fallback para cada indicador

---

### Models

#### `models/user_profile.py`

- **`Objective`** (Enum) — 6 objetivos: emergency, short_term, mixed, retirement, growth, income
- **`RiskProfile`** (Enum) — 4 perfis: conservative, moderate, bold, aggressive
- **`UserProfile`** (dataclass) — agrega todos os inputs do usuario

#### `models/products.py`

- **`ProductCategory`** — renda_fixa, renda_variavel, multimercado, cambial
- **`TaxType`** — ir_regressivo, isento, fii, acoes, poupanca
- **`LiquidityType`** — daily, short, medium, low
- **`InvestmentProduct`** — modelo completo de produto com retorno esperado, risco e tags

#### `models/market_data.py`

- **`MarketIndicators`** — Selic, CDI, IPCA, Poupanca, TR
- Propriedades calculadas: `cdi_monthly`, `selic_monthly`, `real_return`

#### `models/portfolio.py`

- **`AssetAllocation`** — produto + peso + valor alocado
- **`Portfolio`** — lista de alocacoes com calculo de totais, media de risco e distribuicao

---

### Clients

#### `clients/bcb.py`

Cliente para a API SGS do Banco Central:

- **`_fetch_series(code, n)`** — busca os ultimos `n` valores de uma serie
- **`_annualize_cdi_daily(rate)`** — converte CDI diario para anual (252 dias uteis)
- **`_annualize_cdi_monthly(rate)`** — converte CDI mensal para anual
- **`fetch_market_indicators()`** — orquestra todas as buscas e retorna `MarketIndicators`

Tratamento de erros: qualquer falha HTTP, timeout ou dado invalido resulta em uso dos valores fallback.

#### `clients/fallback.py`

Retorna `MarketIndicators` com valores configurados nas variaveis de ambiente, marcados com `is_fallback=True`.

---

### Services

#### `services/products_catalog.py`

Catalogo de 17 produtos do mercado brasileiro:

- 11 produtos de renda fixa (Tesouro Selic, CDBs, LCI, LCA, Debentures, Fundos RF)
- 4 produtos de renda variavel (ETF BOVA11, ETF IVVB11, Acoes, FIIs)
- 1 fundo multimercado
- 1 poupanca (referencia)

Cada produto tem: nome, categoria, tipo de imposto, liquidez, score de risco (1-10), investimento minimo, retorno esperado e tags.

Funcoes auxiliares: `get_all_products()`, `get_products_by_category()`, `get_products_by_risk()`, `get_products_by_tag()`.

#### `services/tax.py`

Implementa as regras fiscais brasileiras:

- **`ir_rate(days)`** — retorna a aliquota de IR para o periodo
- **`iof_rate(days)`** — retorna a aliquota de IOF para os primeiros 30 dias
- **`net_return_fixed_income(gross, days, tax_type)`** — calcula retorno liquido apos IOF + IR
- **`equivalent_cdi_gross(net_pct, days)`** — calcula equivalencia de produto isento vs tributado
- **`fii_tax(gain, is_dividend)`** — imposto de FII
- **`acoes_tax(gain, monthly_sales)`** — imposto de acoes com isencao de R$ 20k

#### `services/risk.py`

Calculo do score maximo de risco:

1. Parte do score base do perfil declarado (conservador=3, moderado=5, arrojado=7, agressivo=10)
2. Aplica ajustes por objetivo (-2 a +1)
3. Aplica ajustes por idade (-2 a +1)
4. Aplica ajustes por horizonte (-2 a +1)
5. Limita ao intervalo 1-10

#### `services/allocation.py`

Motor de alocacao com 24 templates (6 objetivos x 4 perfis de risco).

Cada template mapeia tags de categoria para pesos percentuais. Exemplo para mixed/moderate:

```python
{
    "pos_fixado_liquido": 20%,
    "tesouro_ipca": 25%,
    "renda_fixa_isento": 20%,
    "fii": 15%,
    "multimercado": 10%,
    "acoes_etf": 10%,
}
```

O motor:
1. Seleciona o template baseado em (objetivo, perfil)
2. Mapeia cada tag para um produto concreto do catalogo
3. Filtra produtos que excedem o score maximo de risco
4. Filtra produtos com investimento minimo acima do valor disponivel
5. Renormaliza os pesos para somar 100%
6. Distribui o valor total entre as alocacoes

#### `services/projections.py`

Calcula projecoes de retorno com juros compostos:

1. Estima o retorno anual ponderado da carteira (baseado nos retornos de cada produto)
2. Converte para taxa mensal equivalente
3. Simula mes a mes: `saldo = saldo * (1 + taxa_mensal) + aporte`
4. Calcula imposto medio ponderado nos marcos temporais
5. Compara com poupanca no mesmo periodo

Marcos: a cada 6 meses nos primeiros 2 anos, depois anualmente.

---

### Report

#### `report/formatters.py`

Formatadores para o padrao brasileiro:

- **`fmt_currency(value)`** — `R$ 1.234,56` (ponto como separador de milhar, virgula como decimal)
- **`fmt_pct(value, decimals)`** — `14,25%`
- **`fmt_months(months)`** — `2 anos e 6 meses`

#### `report/generator.py`

Orquestra a renderizacao do relatorio completo chamando as 8 secoes em ordem, com separadores visuais (`Rule`) entre elas.

#### `report/sections/`

8 secoes independentes, cada uma recebendo `Console` + dados relevantes:

| Secao             | Dados de entrada                           |
|-------------------|--------------------------------------------|
| `header.py`       | UserProfile, MarketIndicators              |
| `allocation.py`   | Portfolio                                  |
| `products.py`     | Portfolio, MarketIndicators                |
| `projections.py`  | ProjectionResult                           |
| `risk_analysis.py`| UserProfile, Portfolio                     |
| `liquidity.py`    | Portfolio                                  |
| `tax.py`          | UserProfile, Portfolio                     |
| `action_plan.py`  | UserProfile, Portfolio, MarketIndicators   |

---

### CLI

#### `cli/app.py`

Aplicacao Typer com 3 comandos:

- **`rates`** — busca e exibe indicadores de mercado
- **`analyze`** — fluxo completo (interativo ou via parametros)
- **`version`** — exibe versao

O comando `analyze` aceita modo interativo (padrao) e nao-interativo (`--no-interactive`).

#### `cli/prompts.py`

Prompts interativos usando `rich.prompt`:

- Cada input tem validacao com loop de retry
- Opcoes enumeradas para escolhas categoricas

#### `cli/validators.py`

Validacao de inputs:

- **`validate_amount(value)`** — aceita formatos `50000`, `50.000,00`, `R$ 50.000,00`
- **`validate_age(value)`** — intervalo 16-100
- **`validate_horizon(value)`** — intervalo 1-480 meses

---

## Fluxo de Execucao

```
1. CLI recebe inputs (interativo ou parametros)
       │
2. Constroi UserProfile
       │
3. fetch_market_indicators() ──────► API BCB ──► MarketIndicators
       │                               │
       │                          (fallback se erro)
       │
4. max_risk_score(profile) ──────► score maximo ajustado
       │
5. build_portfolio(profile, indicators) ──────► Portfolio
       │   - Seleciona template de alocacao
       │   - Mapeia tags → produtos
       │   - Filtra por risco e valor minimo
       │   - Renormaliza pesos
       │   - Distribui valor
       │
6. generate_projections(profile, portfolio, indicators)
       │   - Calcula retorno ponderado
       │   - Simula juros compostos mes a mes
       │   - Calcula impostos estimados
       │
7. generate_report(console, profile, portfolio, indicators, projection)
       │   - Renderiza 8 secoes no terminal
       │
8. Output formatado no terminal
```

---

## API do Banco Central

O sistema utiliza a API SGS (Sistema Gerenciador de Series Temporais) do Banco Central:

**URL base:** `https://api.bcb.gov.br/dados/serie/bcdata.sgs.{code}/dados/ultimos/{n}?formato=json`

### Series utilizadas

| Indicador    | Codigo | Tipo                        |
|-------------|:------:|-----------------------------|
| Selic Meta   |   432  | Taxa anual (%)              |
| CDI Diario   |    12  | Taxa diaria (%)             |
| CDI Mensal   |  4391  | Acumulado no mes (%)        |
| IPCA Mensal  |   433  | Variacao mensal (%)         |
| IPCA 12m     | 13522  | Acumulado 12 meses (%)      |
| Poupanca     | 25621  | Rendimento mensal (%)       |
| TR           |   226  | Taxa referencial (%)        |

### Tratamento do CDI

O CDI anual nao e publicado diretamente. O sistema:

1. Busca o CDI diario (serie 12)
2. Anualiza: `annual = ((1 + daily/100) ^ 252 - 1) * 100`
3. Se indisponivel, busca o CDI mensal (serie 4391) e anualiza: `annual = ((1 + monthly/100) ^ 12 - 1) * 100`

### Tratamento de falhas

- Timeout configuravel (padrao: 10 segundos)
- Qualquer erro HTTP, parse ou dado ausente resulta em fallback
- Indicadores criticos (Selic, CDI, IPCA): se qualquer um falhar, usa fallback completo
- Poupanca: se indisponivel, estimada a partir da Selic

---

## Regras Fiscais

### IR Regressivo (Renda Fixa)

Aplicado sobre o rendimento. A aliquota diminui com o tempo:

| Periodo          | Aliquota |
|------------------|:--------:|
| Ate 180 dias     |  22,50%  |
| 181 a 360 dias   |  20,00%  |
| 361 a 720 dias   |  17,50%  |
| Acima de 720 dias|  15,00%  |

### IOF Regressivo

Aplicado sobre o rendimento nos primeiros 30 dias, **antes** do IR:

| Dia | IOF  | Dia | IOF  | Dia | IOF  |
|:---:|:----:|:---:|:----:|:---:|:----:|
|  1  |  96% |  11 |  63% |  21 |  30% |
|  2  |  93% |  12 |  60% |  22 |  26% |
|  3  |  90% |  13 |  56% |  23 |  23% |
|  4  |  86% |  14 |  53% |  24 |  20% |
|  5  |  83% |  15 |  50% |  25 |  16% |
|  6  |  80% |  16 |  46% |  26 |  13% |
|  7  |  76% |  17 |  43% |  27 |  10% |
|  8  |  73% |  18 |  40% |  28 |   6% |
|  9  |  70% |  19 |  36% |  29 |   3% |
| 10  |  66% |  20 |  33% |  30 |   0% |

### Produtos Isentos

- **LCI/LCA** — isentos de IR para pessoa fisica (FGC ate R$ 250k)
- **Debentures Incentivadas** — isentas de IR (Lei 12.431/2011)
- **Poupanca** — isenta de IR

### FII (Fundos Imobiliarios)

- **Dividendos** — isentos de IR para pessoa fisica
- **Ganho de capital** — 20% sobre o lucro na venda de cotas

### Acoes

- **Ganho de capital** — 15% (operacoes normais), 20% (day trade)
- **Isencao** — vendas totais no mes inferiores a R$ 20.000,00

### Equivalencia de Produtos Isentos

Formula para calcular a taxa bruta equivalente de um produto isento:

```
taxa_bruta_equivalente = taxa_isenta / (1 - aliquota_IR)
```

Exemplo: LCI a 93% do CDI com IR de 15%:
```
93% / (1 - 0,15) = 109,4% do CDI
```

---

## Motor de Alocacao

### Templates

O sistema possui 24 templates de alocacao (6 objetivos x 4 perfis de risco). Cada template define pesos para categorias de investimento.

### Categorias de alocacao (tags)

| Tag                    | Produto padrao                        |
|------------------------|---------------------------------------|
| `pos_fixado_liquido`   | Tesouro Selic                        |
| `renda_fixa_isento`    | LCI                                  |
| `renda_fixa_credito`   | Fundo RF Credito Privado             |
| `tesouro_ipca`         | Tesouro IPCA+ 2035                   |
| `tesouro_ipca_juros`   | Tesouro IPCA+ com Juros Semestrais   |
| `fii`                  | Fundos Imobiliarios (FIIs)           |
| `multimercado`         | Fundo Multimercado                   |
| `acoes_etf`            | ETF BOVA11 (Ibovespa)               |
| `acoes_intl`           | ETF IVVB11 (S&P 500)               |
| `acoes_stock`          | Acoes (carteira diversificada)       |
| `debentures`           | Debentures Incentivadas              |
| `prefixado`            | Tesouro Prefixado (2029)            |

### Processo de construcao

1. Busca o template para (objetivo, perfil_de_risco)
2. Para cada tag no template, seleciona o produto correspondente
3. Remove produtos com risco acima do score maximo ajustado
4. Remove produtos com investimento minimo acima do valor disponivel
5. Renormaliza os pesos restantes para somar 100%
6. Calcula o valor monetario de cada alocacao

---

## Projecoes Financeiras

### Formula base

Juros compostos com aportes mensais:

```
saldo[m] = saldo[m-1] * (1 + taxa_mensal) + aporte
```

### Estimativa de retorno por tipo de produto

| Tipo de retorno        | Formula                               |
|------------------------|---------------------------------------|
| % do CDI               | CDI * (pct_cdi / 100)                |
| Prefixado              | taxa fixa informada                  |
| IPCA+                  | IPCA + spread                        |
| Poupanca               | taxa da poupanca                     |
| Acoes                  | IPCA + 6% (estimativa longo prazo)   |
| FII                    | CDI + 1% (dividendos + valorizacao)  |

### Calculo de impostos nas projecoes

O imposto estimado e calculado como media ponderada das aliquotas por tipo de produto:

- **IR Regressivo**: aliquota baseada nos dias corridos
- **Isento/Poupanca**: 0%
- **Acoes**: 15% do ganho
- **FII**: 5% (estimativa conservadora - apenas ganho de capital)

---

## Configuracao e Extensibilidade

### Adicionar um novo produto

Edite `services/products_catalog.py` e adicione um novo `InvestmentProduct` na lista `PRODUCTS`:

```python
InvestmentProduct(
    name="Novo Produto",
    category=ProductCategory.RENDA_FIXA,
    tax_type=TaxType.IR_REGRESSIVO,
    liquidity=LiquidityType.DAILY,
    risk_score=3,
    min_investment=Decimal("100"),
    expected_return_pct_cdi=Decimal("110"),
    description="Descricao do produto",
    tags=["tag1", "tag2"],
)
```

### Adicionar um novo template de alocacao

Edite `services/allocation.py` e adicione uma entrada em `ALLOCATION_TEMPLATES` e o mapeamento de tag para produto em `_pick_product()`.

### Adicionar uma nova secao ao relatorio

1. Crie um arquivo em `report/sections/nova_secao.py` com uma funcao `render_nova_secao(console, ...)`
2. Importe e chame a funcao em `report/generator.py`

### Alterar valores fallback

Via variaveis de ambiente:

```bash
export INVESTX_FALLBACK_SELIC=13.75
export INVESTX_FALLBACK_CDI=13.65
uv run investx rates
```
