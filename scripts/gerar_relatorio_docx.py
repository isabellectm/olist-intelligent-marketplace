"""Gera a versão Word do relatório executivo."""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.shared import Inches, Pt
from htmldocx import HtmlToDocx
from markdown import markdown

ROOT = Path(__file__).resolve().parents[1]
MD_PATH = ROOT / "docs" / "relatorio_executivo.md"
OUT_PATH = ROOT / "docs" / "relatorio_executivo.docx"


def _abs_image(match: re.Match[str]) -> str:
    alt, src = match.group(1), match.group(2)
    path = (MD_PATH.parent / src).resolve()
    return f"![{alt}]({path.as_posix()})"


def _mermaid_note(match: re.Match[str]) -> str:
    code = match.group(1).strip()
    return (
        "\n\n**Diagrama (Mermaid — o desenho renderiza no Markdown/GitHub).** "
        "Segue o texto do fluxo para referência:\n\n"
        f"```\n{code}\n```\n"
    )


def build() -> Path:
    text = MD_PATH.read_text(encoding="utf-8")
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", _abs_image, text)
    text = re.sub(r"```mermaid\n(.*?)```", _mermaid_note, text, flags=re.S)

    html = markdown(text, extensions=["tables", "fenced_code", "nl2br", "sane_lists"])

    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)
    style.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")

    parser = HtmlToDocx()
    parser.table_style = "Table Grid"
    parser.add_html_to_document(html, doc)

    for shape in doc.inline_shapes:
        try:
            shape.width = Inches(6.2)
        except Exception:
            pass

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT_PATH)
    return OUT_PATH


if __name__ == "__main__":
    path = build()
    print(f"Gerado: {path}")
