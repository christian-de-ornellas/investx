<div align="center">

# 📈 InvestX

**Sistema CLI de consultoria de investimentos para o mercado brasileiro**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/Licença-MIT-22c55e?style=flat-square)](LICENSE)
[![BCB](https://img.shields.io/badge/Dados-Banco%20Central%20do%20Brasil-003087?style=flat-square)](https://api.bcb.gov.br)

---

*Informe seu perfil de investidor e receba um relatório completo com alocação de carteira, projeções de retorno, análise de risco, tributação e plano de ação — com dados reais do Banco Central.*

</div>

---

## ✨ Funcionalidades

- **Análise personalizada** por valor, objetivo, risco, horizonte e idade
- **Alocação de carteira** com projeções de retorno detalhadas
- **Análise de risco e tributação** baseada na legislação brasileira
- **Dados em tempo real** via API do Banco Central (Selic, CDI, IPCA)
- **Recomendações por corretora** com localização dos produtos na plataforma

---

## 🏦 Corretoras Suportadas

| Corretora | Parâmetro |
|---|---|
| Nubank / NuInvest | `nubank` |
| XP Investimentos | `xp` |
| BTG Pactual | `btg` |
| Banco Inter | `inter` |
| Rico | `rico` |

---

## ⚙️ Requisitos

- **Python** 3.10+
- **[uv](https://docs.astral.sh/uv/)** — gerenciador de pacotes moderno

---

## 🚀 Instalação

```bash
# Clone o repositório
git clone <repo-url>
cd investx

# Instale as dependências
uv sync
```

---

## 📖 Uso

### Ver taxas atuais do mercado

```bash
uv run investx rates
```

### Análise interativa

```bash
# Responda as perguntas no terminal
uv run investx analyze
```

### Análise direta (modo não-interativo)

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

### Análise com dicas da sua corretora

```bash
uv run investx analyze \
  --amount 50000 \
  --objective mixed \
  --risk moderate \
  --horizon 24 \
  --age 32 \
  --contribution 2000 \
  --brokerage nubank \
  --no-interactive
```

> No modo interativo, a corretora é selecionada via menu. No modo não-interativo, use `--brokerage` / `-b`.

---

## 📚 Documentação

| Documento | Descrição |
|---|---|
| [Guia de Uso Completo](docs/guia-de-uso.md) | Comandos, parâmetros e exemplos por perfil |
| [Arquitetura e Referência Técnica](docs/arquitetura.md) | Estrutura do projeto, módulos, regras fiscais e API BCB |

---

## 📄 Licença

Distribuído sob a licença **MIT**. Veja [LICENSE](LICENSE) para mais detalhes.
