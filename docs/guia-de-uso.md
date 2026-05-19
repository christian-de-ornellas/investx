# Guia de Uso — InvestX

## Sumario

1. [Instalacao](#instalacao)
2. [Comandos Disponiveis](#comandos-disponiveis)
3. [Comando `rates`](#comando-rates)
4. [Comando `analyze`](#comando-analyze)
   - [Modo Interativo](#modo-interativo)
   - [Modo Nao-Interativo](#modo-nao-interativo)
   - [Parametros](#parametros)
5. [Exemplos por Perfil](#exemplos-por-perfil)
6. [Secoes do Relatorio](#secoes-do-relatorio)
7. [Variaveis de Ambiente](#variaveis-de-ambiente)
8. [Perguntas Frequentes](#perguntas-frequentes)

---

## Instalacao

### Pre-requisitos

- Python 3.10 ou superior
- [uv](https://docs.astral.sh/uv/) — gerenciador de pacotes e ambientes virtuais

### Passo a passo

```bash
# 1. Instale o uv (se ainda nao tiver)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone o repositorio
git clone <repo-url>
cd investx

# 3. Instale as dependencias
uv sync

# 4. Verifique a instalacao
uv run investx version
```

A saida esperada e:

```
InvestX v0.1.0
```

---

## Comandos Disponiveis

| Comando   | Descricao                                        |
|-----------|--------------------------------------------------|
| `rates`   | Exibe as taxas atuais do mercado (Selic, CDI, IPCA, Poupanca, TR) |
| `analyze` | Gera relatorio completo de recomendacao de investimentos |
| `version` | Exibe a versao do InvestX                        |

Para ver a ajuda geral:

```bash
uv run investx --help
```

---

## Comando `rates`

Consulta a API do Banco Central e exibe os indicadores atuais do mercado.

```bash
uv run investx rates
```

Saida esperada:

```
          Indicadores de Mercado
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Indicador    ┃ Taxa Anual ┃ Taxa Mensal ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ Selic Meta   │     14,50% │     1,1348% │
│ CDI          │     14,40% │     1,1274% │
│ IPCA (12m)   │      4,39% │           - │
│ Poupanca     │      6,17% │           - │
│ TR           │      0,17% │           - │
│ Retorno Real │     10,01% │           - │
└──────────────┴────────────┴─────────────┘
```

Se a API do BCB estiver indisponivel, o sistema usa valores fallback e exibe um aviso.

---

## Comando `analyze`

Gera um relatorio completo de recomendacao de investimentos baseado no seu perfil.

### Modo Interativo

Basta executar sem parametros — o sistema faz as perguntas uma a uma:

```bash
uv run investx analyze
```

O fluxo interativo solicita:

1. **Valor para investir** — valor inicial em reais (ex: `50000`)
2. **Objetivo** — escolha numerica entre 6 opcoes
3. **Perfil de risco** — escolha numerica entre 4 opcoes
4. **Horizonte** — em meses (ex: `24`)
5. **Idade** — em anos (ex: `32`)
6. **Aporte mensal** — valor mensal adicional (ex: `2000`, ou `0` para nenhum)

### Modo Nao-Interativo

Passe todos os parametros via linha de comando:

```bash
uv run investx analyze \
  --amount 50000 \
  --objective mixed \
  --risk moderate \
  --horizon 24 \
  --age 32 \
  --contribution 2000 \
  --no-interactive
```

### Parametros

| Parametro         | Atalho | Tipo   | Obrigatorio* | Descricao                          |
|-------------------|--------|--------|:------------:|------------------------------------|
| `--amount`        | `-a`   | float  | Sim          | Valor inicial em R$                |
| `--objective`     | `-o`   | string | Sim          | Objetivo do investimento (ver tabela abaixo) |
| `--risk`          | `-r`   | string | Sim          | Perfil de risco (ver tabela abaixo) |
| `--horizon`       | `-h`   | int    | Sim          | Horizonte em meses (1 a 480)       |
| `--age`           |        | int    | Sim          | Idade do investidor (16 a 100)     |
| `--contribution`  | `-c`   | float  | Nao          | Aporte mensal em R$ (padrao: 0)    |
| `--no-interactive`|        | flag   | Nao          | Desativa modo interativo           |

*Obrigatorio apenas no modo `--no-interactive`.

#### Valores para `--objective`

| Valor         | Descricao                  |
|---------------|----------------------------|
| `emergency`   | Reserva de Emergencia      |
| `short_term`  | Curto Prazo (< 1 ano)      |
| `mixed`       | Medio Prazo / Misto        |
| `retirement`  | Aposentadoria              |
| `growth`      | Crescimento Patrimonial    |
| `income`      | Renda Passiva              |

#### Valores para `--risk`

| Valor          | Descricao    | Score |
|----------------|-------------|:-----:|
| `conservative` | Conservador |   1   |
| `moderate`     | Moderado    |   2   |
| `bold`         | Arrojado    |   3   |
| `aggressive`   | Agressivo   |   4   |

---

## Exemplos por Perfil

### Reserva de Emergencia

Jovem de 25 anos montando reserva de emergencia com R$ 5.000 e aportes de R$ 1.000/mes:

```bash
uv run investx analyze \
  --amount 5000 \
  --objective emergency \
  --risk conservative \
  --horizon 12 \
  --age 25 \
  --contribution 1000 \
  --no-interactive
```

Resultado esperado: 100% Tesouro Selic (liquidez diaria, risco minimo).

### Medio Prazo Moderado

Investidor de 32 anos com R$ 50.000 para medio prazo:

```bash
uv run investx analyze \
  --amount 50000 \
  --objective mixed \
  --risk moderate \
  --horizon 24 \
  --age 32 \
  --contribution 2000 \
  --no-interactive
```

Resultado esperado: carteira diversificada com Tesouro Selic, Tesouro IPCA+, LCI e FIIs.

### Aposentadoria Arrojado

Investidor de 28 anos pensando em aposentadoria com horizonte de 30 anos:

```bash
uv run investx analyze \
  --amount 100000 \
  --objective retirement \
  --risk bold \
  --horizon 360 \
  --age 28 \
  --contribution 3000 \
  --no-interactive
```

Resultado esperado: carteira com Tesouro IPCA+, FIIs, ETFs de acoes, multimercado e exposicao internacional.

### Crescimento Agressivo

Investidor de 28 anos buscando crescimento maximo em 5 anos:

```bash
uv run investx analyze \
  --amount 100000 \
  --objective growth \
  --risk aggressive \
  --horizon 60 \
  --age 28 \
  --contribution 5000 \
  --no-interactive
```

Resultado esperado: carteira concentrada em ETFs (BOVA11, IVVB11), acoes, multimercado, FIIs e debentures incentivadas.

### Renda Passiva

Investidor de 50 anos buscando renda com R$ 200.000:

```bash
uv run investx analyze \
  --amount 200000 \
  --objective income \
  --risk moderate \
  --horizon 120 \
  --age 50 \
  --contribution 0 \
  --no-interactive
```

Resultado esperado: carteira focada em FIIs (dividendos mensais), Tesouro IPCA+ com Juros Semestrais, LCI/LCA e debentures incentivadas.

---

## Secoes do Relatorio

O relatorio gerado contem 8 secoes:

### 1. Perfil do Investidor

Resume os dados informados: valor, aporte mensal, objetivo, perfil de risco, horizonte e idade.

### 2. Indicadores de Mercado

Exibe as taxas atuais obtidas do Banco Central: Selic, CDI, IPCA (12 meses), Poupanca e Retorno Real. Se os dados forem estimados (API indisponivel), um aviso e exibido.

### 3. Alocacao Recomendada

Tabela com a carteira recomendada contendo:
- Nome do produto
- Categoria (Renda Fixa, Renda Variavel, Multimercado)
- Peso percentual
- Valor alocado em R$
- Score de risco (barra visual de 1 a 10)

### 4. Detalhes dos Produtos

Para cada produto recomendado, exibe:
- Descricao do produto
- Retorno estimado (% do CDI, prefixado, ou IPCA+)
- Tipo de liquidez (D+0 a vencimento)
- Regime tributario

### 5. Projecao de Retorno

Tabela com projecoes em marcos temporais (a cada 6 meses nos primeiros 2 anos, depois anualmente):
- Total investido (aportes acumulados)
- Saldo bruto e liquido
- Ganho liquido
- Comparativo com poupanca

Inclui resumo final com retorno percentual liquido, impostos estimados e vantagem sobre a poupanca.

### 6. Analise de Risco

- Perfil declarado vs score ajustado (ajuste por idade, horizonte, objetivo)
- Score medio da carteira
- Distribuicao por faixa de risco (baixo/medio/alto)
- Alertas contextuais (ex: idade avancada + ativos de alto risco)

### 7. Analise de Liquidez

Agrupa os ativos por tipo de liquidez:
- **D+0 / D+1** — resgate imediato
- **D+2 a D+5** — curto prazo
- **D+30 a D+90** — medio prazo
- **Vencimento / +D+90** — baixa liquidez

Exibe percentual da carteira com resgate imediato e avaliacao qualitativa.

### 8. Consideracoes Fiscais

Para cada produto, detalha:
- Regime tributario (IR Regressivo, Isento, FII, Acoes)
- Aliquota estimada para o horizonte informado
- Equivalencia de produtos isentos (ex: LCI a 93% CDI equivale a CDB a 113% CDI com IR)
- Dicas de otimizacao fiscal (manter >720 dias, evitar resgate <30 dias)

### 9. Plano de Acao

Roteiro passo-a-passo personalizado:
1. Abertura de conta em corretora
2. Montagem de reserva de emergencia (se aplicavel)
3. Ordem de investimento (priorizando liquidez)
4. Configuracao de aportes mensais (se informado)
5. Estrategia de rebalanceamento
6. Otimizacao fiscal
7. Revisao periodica

---

## Variaveis de Ambiente

Todas as configuracoes podem ser ajustadas via variaveis de ambiente com prefixo `INVESTX_`:

| Variavel                    | Padrao                                      | Descricao                        |
|-----------------------------|---------------------------------------------|----------------------------------|
| `INVESTX_BCB_BASE_URL`     | `https://api.bcb.gov.br/dados/serie/bcdata.sgs` | URL base da API BCB         |
| `INVESTX_BCB_TIMEOUT_SECONDS` | `10.0`                                   | Timeout das requisicoes HTTP     |
| `INVESTX_BCB_MAX_RETRIES`  | `2`                                         | Tentativas em caso de falha      |
| `INVESTX_FALLBACK_SELIC`   | `14.25`                                     | Selic fallback (% a.a.)         |
| `INVESTX_FALLBACK_CDI`     | `14.15`                                     | CDI fallback (% a.a.)           |
| `INVESTX_FALLBACK_IPCA`    | `5.49`                                      | IPCA fallback (% 12m)           |
| `INVESTX_FALLBACK_POUPANCA`| `7.40`                                      | Poupanca fallback (% a.a.)      |
| `INVESTX_FALLBACK_TR`      | `0.10`                                      | TR fallback (% a.a.)            |

Exemplo:

```bash
# Usar timeout maior para conexoes lentas
INVESTX_BCB_TIMEOUT_SECONDS=30 uv run investx rates
```

---

## Perguntas Frequentes

### Os dados do mercado sao em tempo real?

Os dados sao obtidos da API SGS do Banco Central do Brasil, que publica as taxas oficiais. A Selic e o CDI sao atualizados diariamente, o IPCA mensalmente. Nao sao dados de mercado em tempo real (como precos de acoes).

### O que acontece se a API do BCB estiver fora do ar?

O sistema utiliza valores fallback configurados nas variaveis de ambiente. Um aviso e exibido no relatorio indicando que os dados sao estimados.

### As projecoes sao garantidas?

Nao. As projecoes sao estimativas baseadas nas taxas atuais e pressupoem que as condicoes de mercado se mantenham constantes. Rendimentos passados nao garantem rendimentos futuros. O relatorio e informativo e nao constitui recomendacao de investimento.

### Como o sistema ajusta o risco por idade?

O score maximo de risco e reduzido para investidores mais velhos:
- **< 25 anos**: +1 ao score base
- **50-59 anos**: -1 ao score base
- **60+ anos**: -2 ao score base

Isso reflete a menor capacidade de recuperacao de perdas conforme a idade avanca.

### Como funciona a equivalencia LCI/LCA?

Produtos isentos de IR (LCI, LCA, debentures incentivadas) parecem render menos, mas como nao ha desconto de imposto, o retorno liquido pode ser superior. O relatorio calcula a equivalencia:

- LCI a 93% do CDI com IR de 15% (>720 dias) equivale a um CDB a ~109% do CDI
- LCI a 93% do CDI com IR de 22.5% (<=180 dias) equivale a um CDB a ~120% do CDI

### Posso usar o InvestX sem internet?

Sim. Se a API do BCB estiver inacessivel, o sistema usa valores fallback. Voce tambem pode configurar as taxas manualmente via variaveis de ambiente.

### Quais produtos estao no catalogo?

O catalogo inclui 17 produtos:

| Produto                          | Categoria       | Risco | Tributacao      |
|----------------------------------|-----------------|:-----:|-----------------|
| Tesouro Selic                    | Renda Fixa      |   1   | IR Regressivo   |
| CDB Liquidez Diaria             | Renda Fixa      |   2   | IR Regressivo   |
| CDB Prefixado (2 anos)          | Renda Fixa      |   3   | IR Regressivo   |
| CDB IPCA+ (3 anos)              | Renda Fixa      |   3   | IR Regressivo   |
| LCI                              | Renda Fixa      |   2   | Isento          |
| LCA                              | Renda Fixa      |   2   | Isento          |
| Debentures Incentivadas          | Renda Fixa      |   4   | Isento          |
| Tesouro Prefixado (2029)        | Renda Fixa      |   3   | IR Regressivo   |
| Tesouro IPCA+ 2035              | Renda Fixa      |   3   | IR Regressivo   |
| Tesouro IPCA+ c/ Juros Semest.  | Renda Fixa      |   3   | IR Regressivo   |
| Fundo RF Credito Privado        | Renda Fixa      |   4   | IR Regressivo   |
| ETF BOVA11 (Ibovespa)           | Renda Variavel  |   7   | Acoes           |
| ETF IVVB11 (S&P 500)            | Renda Variavel  |   8   | Acoes           |
| Acoes (carteira diversificada)  | Renda Variavel  |   8   | Acoes           |
| Fundos Imobiliarios (FIIs)      | Renda Variavel  |   5   | FII             |
| Fundo Multimercado              | Multimercado    |   6   | IR Regressivo   |
| Poupanca                         | Renda Fixa      |   1   | Isento          |
