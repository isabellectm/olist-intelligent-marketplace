# Scripts

Jobs e geradores. Não é exploração (fica em `notebooks/`) nem biblioteca (fica em `src/` quando existir).

| Script | O que faz |
| --- | --- |
| `gerar_notebook.py` | Gera `notebooks/01_analise_exploratoria.ipynb` a partir do gerador |
| `gerar_apresentacao.py` | Gera `docs/apresentacao_video.pptx` (7 slides, estilo Pós Tech) |
| `gerar_relatorio_docx.py` | Gera `docs/relatorio_executivo.docx` a partir do Markdown |

```bash
python scripts/gerar_notebook.py
python scripts/gerar_apresentacao.py
python scripts/gerar_relatorio_docx.py
```
