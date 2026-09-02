"""Gera a apresentação widescreen do vídeo executivo (estilo Pós Tech / FIAP)."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "apresentacao_video.pptx"

# Paleta extraída do CSS de postech.fiap.com.br (html/body #000, CTAs #ed145b).
BLACK = RGBColor(0x00, 0x00, 0x00)
CARD = RGBColor(0x11, 0x11, 0x11)
MAGENTA = RGBColor(0xED, 0x14, 0x5B)
MAGENTA_DARK = RGBColor(0xD3, 0x0F, 0x59)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY = RGBColor(0xB3, 0xB3, 0xB3)
LINE = RGBColor(0x2A, 0x2A, 0x2A)

FONT = "Arial"
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
MARGIN_L = Inches(0.55)
MARGIN_R = Inches(0.55)


def rgb(shape_fill, color: RGBColor) -> None:
    shape_fill.solid()
    shape_fill.fore_color.rgb = color


def _set_run(run, text, size, color, bold=False, italic=False) -> None:
    run.text = text
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.italic = italic
    run.font.name = FONT


def add_text(
    slide,
    left,
    top,
    width,
    height,
    text,
    size=18,
    color=WHITE,
    bold=False,
    italic=False,
    align=PP_ALIGN.LEFT,
    anchor=MSO_ANCHOR.TOP,
    font_name=FONT,
) -> None:
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    try:
        tf._txBody.bodyPr.set("anchor", {MSO_ANCHOR.TOP: "t", MSO_ANCHOR.MIDDLE: "ctr", MSO_ANCHOR.BOTTOM: "b"}[anchor])
    except Exception:
        pass
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    _set_run(run, text, size, color, bold, italic)
    run.font.name = font_name
    return box


def add_multiline(
    slide,
    left,
    top,
    width,
    height,
    lines: list[tuple],
    align=PP_ALIGN.LEFT,
    anchor=MSO_ANCHOR.TOP,
) -> None:
    """lines: (text, size, color, bold, space_after_pt)."""
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    try:
        tf._txBody.bodyPr.set("anchor", {MSO_ANCHOR.TOP: "t", MSO_ANCHOR.MIDDLE: "ctr", MSO_ANCHOR.BOTTOM: "b"}[anchor])
    except Exception:
        pass
    for i, item in enumerate(lines):
        text, size, color, bold = item[:4]
        space_after = item[4] if len(item) > 4 else 6
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = Pt(space_after)
        run = p.add_run()
        _set_run(run, text, size, color, bold)
    return box


def add_rect(slide, left, top, width, height, fill, line=None, line_w=Pt(1.25)):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    rgb(shp.fill, fill)
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = line_w
    shp.shadow.inherit = False
    return shp


def add_round(slide, left, top, width, height, fill, line=None, line_w=Pt(1.25)):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    rgb(shp.fill, fill)
    # Menos arredondado (site é angular).
    try:
        shp.adjustments[0] = 0.04
    except Exception:
        pass
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = line_w
    shp.shadow.inherit = False
    return shp


def add_notes(slide, text: str) -> None:
    slide.notes_slide.notes_text_frame.text = text


def chrome(slide, number: str, total: int = 7) -> None:
    """Barra magenta, número de seção, rodapé."""
    add_rect(slide, Inches(0), Inches(0), Inches(0.12), SLIDE_H, MAGENTA)
    add_text(
        slide,
        Inches(11.7),
        Inches(0.22),
        Inches(1.15),
        Inches(0.4),
        number,
        size=22,
        color=MAGENTA,
        bold=True,
        align=PP_ALIGN.RIGHT,
    )
    add_rect(slide, MARGIN_L, Inches(7.12), Inches(12.2), Pt(0.75), LINE)
    add_text(
        slide,
        MARGIN_L,
        Inches(7.16),
        Inches(6),
        Inches(0.28),
        "OLIST  ·  FASE 1",
        size=10,
        color=GRAY,
        bold=True,
    )
    add_text(
        slide,
        Inches(10.4),
        Inches(7.16),
        Inches(2.35),
        Inches(0.28),
        f"{int(number)} / {total}",
        size=10,
        color=GRAY,
        bold=True,
        align=PP_ALIGN.RIGHT,
    )


def label(slide, text: str, top=Inches(0.28)) -> None:
    add_text(slide, MARGIN_L, top, Inches(8), Inches(0.28), text, size=11, color=MAGENTA, bold=True)


def blank_slide(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = BLACK
    # Garante fundo preto no XML (alguns leitores ignoram background.fill).
    bg = slide.background._element
    return slide


def card_text(slide, left, top, width, height, kicker, headline, body) -> None:
    add_round(slide, left, top, width, height, CARD, LINE)
    add_rect(slide, left, top, Inches(0.08), height, MAGENTA)
    add_text(slide, left + Inches(0.22), top + Inches(0.18), width - Inches(0.36), Inches(0.28), kicker, size=11, color=MAGENTA, bold=True)
    add_text(slide, left + Inches(0.22), top + Inches(0.48), width - Inches(0.36), Inches(0.7), headline, size=28, color=WHITE, bold=True)
    add_text(slide, left + Inches(0.22), top + Inches(1.22), width - Inches(0.36), height - Inches(1.4), body, size=13, color=GRAY)


def agent_card(slide, left, top, width, height, idx, title, owner, line) -> None:
    add_round(slide, left, top, width, height, CARD, LINE)
    add_rect(slide, left, top, width, Pt(3), MAGENTA)
    add_text(slide, left + Inches(0.16), top + Inches(0.14), width - Inches(0.28), Inches(0.24), f"0{idx}", size=12, color=MAGENTA, bold=True)
    add_text(slide, left + Inches(0.16), top + Inches(0.4), width - Inches(0.28), Inches(0.65), title, size=14, color=WHITE, bold=True)
    add_text(slide, left + Inches(0.16), top + Inches(1.08), width - Inches(0.28), Inches(0.24), owner, size=11, color=MAGENTA, bold=True)
    add_text(slide, left + Inches(0.16), top + Inches(1.34), width - Inches(0.28), Inches(0.75), line, size=12, color=GRAY)


def chevron(slide, left, top) -> None:
    shp = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, left, top, Inches(0.32), Inches(0.16))
    rgb(shp.fill, MAGENTA)
    shp.line.fill.background()


def build() -> Path:
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    # --- 01 Capa ---
    s = blank_slide(prs)
    chrome(s, "01")
    add_text(s, MARGIN_L, Inches(1.55), Inches(11), Inches(0.35), "FIAP  |  PÓS TECH", size=16, color=MAGENTA, bold=True)
    add_multiline(
        s,
        MARGIN_L,
        Inches(2.05),
        Inches(12.2),
        Inches(2.4),
        [
            ("OLIST INTELLIGENT", 44, WHITE, True, 0),
            ("MARKETPLACE", 44, WHITE, True, 12),
        ],
    )
    add_rect(s, MARGIN_L, Inches(4.55), Inches(1.4), Pt(4), MAGENTA)
    add_text(
        s,
        MARGIN_L,
        Inches(4.75),
        Inches(11),
        Inches(0.7),
        "Consultoria de IA agêntica  ·  Fase 1  ·  Diretoria Olist",
        size=18,
        color=GRAY,
    )
    add_notes(
        s,
        "Capa institucional. Apresente-se em uma frase e passe para a pergunta da fase.\n"
        "Não leia o título por extenso — deixe o slide falar a marca.",
    )

    # --- 02 Abertura ---
    s = blank_slide(prs)
    chrome(s, "02")
    label(s, "ABERTURA")
    add_multiline(
        s,
        MARGIN_L,
        Inches(0.85),
        Inches(12.1),
        Inches(2.2),
        [
            ("Como a Olist usa IA generativa", 32, WHITE, True, 4),
            ("e agentes para melhorar operação", 32, WHITE, True, 4),
            ("e indicadores.", 32, WHITE, True, 0),
        ],
    )
    add_rect(s, MARGIN_L, Inches(4.15), Inches(0.9), Pt(4), MAGENTA)
    add_text(
        s,
        MARGIN_L,
        Inches(4.4),
        Inches(11.5),
        Inches(1.6),
        "Análise de negócio — não um projeto de TI pesado.\nAssistente de decisão para logística, CX e CRM.",
        size=18,
        color=GRAY,
    )
    add_notes(
        s,
        "0:00–0:30 — Abertura\n"
        "Somos a consultoria de IA agêntica. A pergunta desta fase é simples: como a Olist usa IA "
        "generativa e agentes para melhorar operação e indicadores — com análise de negócio, "
        "não com um projeto de TI pesado.",
    )

    # --- 03 Três números ---
    s = blank_slide(prs)
    chrome(s, "03")
    label(s, "TRÊS NÚMEROS QUE MUDAM A CONVERSA")
    add_text(s, MARGIN_L, Inches(0.58), Inches(11), Inches(0.45), "O dado já está na operação. O que falta é decisão.", size=20, color=WHITE, bold=True)
    gap = Inches(0.22)
    card_w = Inches(3.92)
    y = Inches(1.25)
    h = Inches(5.45)
    card_text(
        s,
        MARGIN_L,
        y,
        card_w,
        h,
        "01  ·  LOGÍSTICA",
        "6,8%",
        "dos pedidos atrasam — e nesses a nota cai de 4,3 para 2,6.\n\n"
        "Mais da metade dos atrasados dá nota 1 ou 2.\n\n"
        "Dói mais no RJ e no Nordeste.",
    )
    card_text(
        s,
        MARGIN_L + card_w + gap,
        y,
        card_w,
        h,
        "02  ·  VOZ DO CLIENTE",
        "15%",
        "das avaliações são ruins.\n\n"
        "4 em 10 vêm com texto.\n\n"
        "Oitiva gratuita do cliente, hoje pouco usada em escala.",
    )
    card_text(
        s,
        MARGIN_L + 2 * (card_w + gap),
        y,
        card_w,
        h,
        "03  ·  RELACIONAMENTO",
        "97%",
        "dos clientes compram uma vez.\n\n"
        "Crescimento está quase todo em cliente novo, não em relação.",
    )
    add_notes(
        s,
        "0:30–1:20 — Três números\n"
        "1. Quase 97% dos pedidos são entregues, mas 6,8% atrasam — e nesses a nota média cai de 4,3 "
        "para 2,6. Mais da metade dos atrasados dá nota 1 ou 2.\n"
        "2. 15% das avaliações são ruins; 4 em 10 vêm com texto. Isso é oitiva gratuita do cliente, "
        "hoje pouco usada em escala.\n"
        "3. 97% dos clientes compram uma vez. Crescimento está quase todo em cliente novo, não em relação.",
    )

    # --- 04 Significado ---
    s = blank_slide(prs)
    chrome(s, "04")
    label(s, "O QUE ISSO SIGNIFICA")
    add_text(
        s,
        MARGIN_L,
        Inches(0.58),
        Inches(12),
        Inches(0.7),
        "O problema não é falta de dado.",
        size=28,
        color=WHITE,
        bold=True,
    )
    axes = [
        ("01", "Prazo percebido", "Atraso é minoria. Quando acontece, a nota desaba."),
        ("02", "Aprendizado com review", "O cliente já escreve a causa. Isso não vira ação padronizada."),
        ("03", "Relacionamento", "Quase não há segunda compra. Falta critério de contato."),
    ]
    w = Inches(3.92)
    for i, (n, t, b) in enumerate(axes):
        x = MARGIN_L + i * (w + Inches(0.22))
        add_round(s, x, Inches(1.55), w, Inches(3.15), CARD, LINE)
        add_text(s, x + Inches(0.22), Inches(1.75), w - Inches(0.4), Inches(0.35), n, size=18, color=MAGENTA, bold=True)
        add_text(s, x + Inches(0.22), Inches(2.2), w - Inches(0.4), Inches(0.9), t, size=20, color=WHITE, bold=True)
        add_text(s, x + Inches(0.22), Inches(3.2), w - Inches(0.4), Inches(1.2), b, size=14, color=GRAY)
    add_rect(s, MARGIN_L, Inches(5.05), Inches(12.2), Inches(1.7), CARD, MAGENTA_DARK)
    add_text(
        s,
        MARGIN_L + Inches(0.35),
        Inches(5.35),
        Inches(11.5),
        Inches(1.15),
        "IA aqui não é um chatbot genérico: é um assistente de decisão para logística, CX e CRM.",
        size=20,
        color=WHITE,
        bold=True,
    )
    add_notes(
        s,
        "1:20–2:00 — O que isso significa\n"
        "O problema não é “falta de dado”. É prazo percebido, aprendizado com review e relacionamento. "
        "IA aqui não é um chatbot genérico: é um assistente de decisão para logística, CX e CRM.",
    )

    # --- 05 Quatro agentes ---
    s = blank_slide(prs)
    chrome(s, "05")
    label(s, "QUATRO AGENTES")
    add_text(s, MARGIN_L, Inches(0.55), Inches(12), Inches(0.4), "Eles se falam. Pessoa executa.", size=22, color=WHITE, bold=True)
    aw = Inches(2.92)
    agents = [
        ("1", "Acompanhamento de Prazo", "LOGÍSTICA", "Risco de atraso e uma ação. Dói mais no RJ e no Nordeste."),
        ("2", "Inteligência de Avaliações", "CX", "Lê a nota e o texto, classifica a causa, rascunha resposta."),
        ("3", "Relacionamento e Recompra", "CRM", "Só convoca quem teve boa entrega e boa nota."),
        ("4", "Exceções Operacionais", "OPERAÇÕES", "Cancelado, indisponível, parado. Humano no financeiro."),
    ]
    for i, a in enumerate(agents):
        x = MARGIN_L + i * (aw + Inches(0.18))
        agent_card(s, x, Inches(1.1), aw, Inches(2.25), *a)

    # Fluxo
    add_text(s, MARGIN_L, Inches(3.55), Inches(12), Inches(0.3), "COMO ELES SE FALAM", size=11, color=MAGENTA, bold=True)

    def flow_box(left, top, w, h, title, sub):
        add_round(s, left, top, w, h, CARD, LINE)
        add_text(s, left + Inches(0.12), top + Inches(0.12), w - Inches(0.2), Inches(0.45), title, size=13, color=WHITE, bold=True)
        add_text(s, left + Inches(0.12), top + Inches(0.55), w - Inches(0.2), Inches(0.4), sub, size=11, color=GRAY)

    flow_box(MARGIN_L, Inches(3.95), Inches(2.7), Inches(1.1), "Avaliações", "tema atraso")
    chevron(s, Inches(3.4), Inches(4.4))
    add_text(s, Inches(3.15), Inches(4.62), Inches(0.9), Inches(0.25), "chama", size=9, color=MAGENTA, align=PP_ALIGN.CENTER)
    flow_box(Inches(3.85), Inches(3.95), Inches(2.7), Inches(1.1), "Prazo / Logística", "atraso grave")
    chevron(s, Inches(6.7), Inches(4.4))
    add_text(s, Inches(6.45), Inches(4.62), Inches(0.9), Inches(0.25), "chama", size=9, color=MAGENTA, align=PP_ALIGN.CENTER)
    flow_box(Inches(7.15), Inches(3.95), Inches(2.7), Inches(1.1), "Exceções", "fila priorizada")

    add_round(s, Inches(10.05), Inches(3.95), Inches(2.7), Inches(1.1), CARD, MAGENTA_DARK)
    add_text(s, Inches(10.17), Inches(4.07), Inches(2.46), Inches(0.45), "Recompra", size=13, color=WHITE, bold=True)
    add_text(s, Inches(10.17), Inches(4.5), Inches(2.46), Inches(0.45), "só boa entrega e nota 4–5", size=11, color=GRAY)

    add_text(
        s,
        MARGIN_L,
        Inches(5.3),
        Inches(12.1),
        Inches(1.4),
        "Review de atraso chama logística. Recompra não fala com quem foi mal atendido.",
        size=18,
        color=WHITE,
        bold=True,
    )
    add_notes(
        s,
        "2:00–3:40 — Quatro agentes (30s cada)\n"
        "Acompanhamento de Prazo: risco de atraso e uma ação. Dói mais no RJ e no Nordeste.\n"
        "Inteligência de Avaliações: lê a nota e o texto, classifica a causa, rascunha resposta.\n"
        "Relacionamento e Recompra: só convoca quem teve boa entrega e boa nota.\n"
        "Exceções Operacionais: cancelado, indisponível, pedido parado — fila priorizada, humano no financeiro.\n"
        "Frase: Eles se falam: review de atraso chama logística; recompra não fala com quem foi mal atendido.",
    )

    # --- 06 Impacto e riscos ---
    s = blank_slide(prs)
    chrome(s, "06")
    label(s, "IMPACTO ESPERADO E RISCOS")
    add_text(s, MARGIN_L, Inches(0.55), Inches(12), Inches(0.4), "Ganho com régua. Risco com dono.", size=22, color=WHITE, bold=True)

    add_round(s, MARGIN_L, Inches(1.15), Inches(6.0), Inches(5.55), CARD, LINE)
    add_text(s, MARGIN_L + Inches(0.3), Inches(1.35), Inches(5.4), Inches(0.35), "IMPACTO", size=14, color=MAGENTA, bold=True)
    impacts = [
        "Menos nota 1 ligada a prazo",
        "Reviews virando causa raiz",
        "Início de segunda compra",
        "Fila de exceção mais curta",
    ]
    for i, t in enumerate(impacts):
        y = Inches(1.9) + i * Inches(1.05)
        add_rect(s, MARGIN_L + Inches(0.3), y, Inches(0.08), Inches(0.7), MAGENTA)
        add_text(s, MARGIN_L + Inches(0.55), y, Inches(5.1), Inches(0.7), t, size=18, color=WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)

    add_round(s, Inches(6.8), Inches(1.15), Inches(6.0), Inches(5.55), CARD, LINE)
    add_text(s, Inches(7.1), Inches(1.35), Inches(5.4), Inches(0.35), "RISCOS", size=14, color=MAGENTA, bold=True)
    risks = [
        "Alarme falso de atraso",
        "Resposta automática em caso grave",
        "Oferta para cliente irritado",
    ]
    for i, t in enumerate(risks):
        y = Inches(1.9) + i * Inches(0.85)
        add_text(s, Inches(7.1), y, Inches(5.4), Inches(0.7), t, size=16, color=WHITE, bold=True)

    add_round(s, Inches(7.1), Inches(4.55), Inches(5.4), Inches(1.8), BLACK, MAGENTA)
    add_text(
        s,
        Inches(7.3),
        Inches(4.75),
        Inches(5.0),
        Inches(1.4),
        "Por isso o agente recomenda.\nA pessoa executa.",
        size=18,
        color=WHITE,
        bold=True,
    )
    add_notes(
        s,
        "3:40–4:20 — Impacto esperado e riscos\n"
        "Impacto: menos nota 1 por prazo; reviews virando causa raiz; início de segunda compra; "
        "fila de exceção mais curta.\n"
        "Riscos: alarme falso, resposta automática em caso grave, oferta para cliente irritado. "
        "Por isso o agente recomenda; a pessoa executa.",
    )

    # --- 07 Pedido ---
    s = blank_slide(prs)
    chrome(s, "07")
    label(s, "PEDIDO À DIRETORIA")
    add_text(
        s,
        MARGIN_L,
        Inches(0.55),
        Inches(12),
        Inches(0.85),
        "Validar estes quatro agentes\ncomo visão da Fase 1.",
        size=28,
        color=WHITE,
        bold=True,
    )
    asks = [
        ("PRÓXIMA FASE", "Detalhar casos de uso e donos."),
        ("AGORA", "Sem investir em plataforma grande."),
        ("RÉGUA", "IA agêntica = clareza de problema, dono e instrução."),
    ]
    w = Inches(3.92)
    for i, (k, b) in enumerate(asks):
        x = MARGIN_L + i * (w + Inches(0.22))
        add_round(s, x, Inches(1.7), w, Inches(2.15), CARD, LINE)
        add_rect(s, x, Inches(1.7), Inches(0.08), Inches(2.15), MAGENTA)
        add_text(s, x + Inches(0.28), Inches(1.9), w - Inches(0.45), Inches(0.35), k, size=12, color=MAGENTA, bold=True)
        add_text(s, x + Inches(0.28), Inches(2.35), w - Inches(0.45), Inches(1.2), b, size=18, color=WHITE, bold=True)

    add_rect(s, MARGIN_L, Inches(4.2), Inches(1.4), Pt(4), MAGENTA)
    add_text(
        s,
        MARGIN_L,
        Inches(4.45),
        Inches(12.1),
        Inches(2.2),
        "Os dados da Olist já mostram por onde começar:\nprazo, voz do cliente e recompra.",
        size=22,
        color=WHITE,
        bold=True,
    )
    add_notes(
        s,
        "4:20–5:00 — Pedido e fechamento\n"
        "Validar estes quatro agentes como visão da Fase 1. Próxima fase: detalhar casos de uso e donos. "
        "Sem investir agora em plataforma grande.\n"
        "IA agêntica, nesta fase, é clareza de problema, dono e instrução. Os dados da Olist já mostram "
        "por onde começar: prazo, voz do cliente e recompra.",
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)
    return OUT


if __name__ == "__main__":
    path = build()
    print(f"Gerado: {path}")
