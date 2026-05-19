# InvestX

Sistema CLI de consultoria de investimentos para o mercado brasileiro.

Recebe seu perfil de investidor (valor, objetivo, risco, horizonte, idade) e gera um relatorio completo com alocacao de carteira, projecoes de retorno, analise de risco, tributacao e plano de acao — tudo com dados reais do Banco Central.

## Requisitos

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (gerenciador de pacotes)

## Instalacao

```bash
# Clone o repositorio
git clone <repo-url>
cd investx

# Instale as dependencias
uv sync
```

## Uso Rapido

```bash
# Ver taxas atuais do mercado (Selic, CDI, IPCA)
uv run investx rates

# Analise interativa (responda as perguntas no terminal)
uv run investx analyze

# Analise direta (modo nao-interativo)
uv run investx analyze \
  --amount 50000 \
  --objective mixed \
  --risk moderate \
  --horizon 24 \
  --age 32 \
  --contribution 2000 \
  --no-interactive
```

## Documentacao

- [Guia de Uso Completo](docs/guia-de-uso.md) — comandos, parametros, exemplos por perfil
- [Arquitetura e Referencia Tecnica](docs/arquitetura.md) — estrutura do projeto, modulos, regras fiscais, API BCB

## Licenca

MIT
