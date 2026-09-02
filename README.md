# Olist Intelligent Marketplace

Consultoria de IA agêntica para a Olist (Tech Challenge). Foco em análise de negócio e visão estratégica.

## Dados

Dataset: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

Os CSVs **não entram no git**. Baixe o conjunto no Kaggle e coloque os arquivos em `data/raw/`. Lista e nomes esperados: [data/raw/README.md](data/raw/README.md).

## Como rodar a análise

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python notebooks/01_analise_exploratoria.py
```

Gráficos em `outputs/figuras/`. O notebook equivalente é gerado com `python scripts/gerar_notebook.py` (a fonte da análise é o `.py`).

## Estrutura do repositório

```
.
├── README.md
├── requirements.txt
├── data/
│   ├── raw/           # CSVs originais (fora do git)
│   └── processed/     # tabelas intermediárias (fora do git)
├── notebooks/         # exploração (fonte: 01_analise_exploratoria.py)
├── scripts/           # jobs (ex.: gerar o notebook)
├── src/               # código reutilizável (ainda vazio)
├── outputs/           # figuras e outros artefatos gerados
└── docs/
    ├── edital/        # enunciado do curso
    ├── fases.md       # o que cada fase pede
    └── ...            # peças da consultoria
```

O documento principal da Fase 1 é o [relatório executivo](docs/relatorio_executivo.md).
