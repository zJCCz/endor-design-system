"""
EndorPresentation — gera arquivos .pptx aplicando a identidade Endor.

Uso típico:

    from endor_docs import EndorPresentation

    deck = EndorPresentation(title="Resultados Q1/2026")
    deck.add_cover(subtitle="Apresentação para o Conselho", date="Abril 2026")
    deck.add_section_divider("1. Mercado", number=1)
    deck.add_content_slide(
        title="Crescimento da carteira",
        bullets=["3 novas concessões em 2025", "MWh +18% YoY"],
    )
    deck.add_chart_slide(
        title="Evolução de consumo",
        chart_image="path/to/chart.png",
    )
    deck.add_closing(text="Obrigado.")
    deck.save("output.pptx")
"""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Cm, Emu, Pt

from endor_docs import styles


# Dimensões do slide (16:9 widescreen)
SLIDE_W_CM = 33.867
SLIDE_H_CM = 19.05

# Padrão de margem interna
MARGIN_CM = 2.0


def _set_text(
    text_frame,
    text: str,
    *,
    size: float,
    color: styles.Color,
    bold: bool = False,
    font_name: str | None = None,
    align: PP_ALIGN | None = None,
):
    """Preenche um text_frame com um único parágrafo de texto formatado."""
    text_frame.clear()
    p = text_frame.paragraphs[0]
    if align is not None:
        p.alignment = align
    run = p.add_run()
    run.text = text
    f = run.font
    f.name = font_name or styles.FONTS.document
    f.size = Pt(size)
    f.bold = bold
    f.color.rgb = color.as_pptx()


def _add_textbox(slide, left, top, width, height) -> "TextFrame":
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.margin_left = Emu(0)
    tf.margin_right = Emu(0)
    tf.margin_top = Emu(0)
    tf.margin_bottom = Emu(0)
    tf.word_wrap = True
    return tf


def _add_filled_rect(slide, left, top, width, height, color: styles.Color, line_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color.as_pptx()
    if line_color is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line_color.as_pptx()
    shape.shadow.inherit = False
    return shape


def _add_logo(slide, *, on_dark: bool = False):
    """Insere o logo Endor no canto superior esquerdo do slide."""
    path = styles.LOGOS.fundo_azul_png if on_dark else styles.LOGOS.fundo_branco_png
    if not path.exists():
        return None
    # Logo com ~1.8cm de altura (proporcional, ~5% da altura do slide)
    return slide.shapes.add_picture(
        str(path),
        left=Cm(1.2),
        top=Cm(0.9),
        height=Cm(1.4),
    )


def _add_footer(slide, page_num: int, total: int, *, on_dark: bool = False):
    color = styles.NEUTRAL.white if on_dark else styles.NEUTRAL.gray_500
    # Footer right: paginação
    tf = _add_textbox(slide, Cm(SLIDE_W_CM - 4.0), Cm(SLIDE_H_CM - 1.2), Cm(3.0), Cm(0.6))
    _set_text(
        tf,
        f"Página {page_num} de {total}",
        size=styles.SIZES.tiny,
        color=color,
        align=PP_ALIGN.RIGHT,
    )
    # Footer left: marca
    tf2 = _add_textbox(slide, Cm(1.2), Cm(SLIDE_H_CM - 1.2), Cm(10.0), Cm(0.6))
    _set_text(
        tf2,
        "Endor Energia",
        size=styles.SIZES.tiny,
        color=color,
        align=PP_ALIGN.LEFT,
    )


class EndorPresentation:
    """Builder de apresentações .pptx com identidade Endor aplicada.

    Os slides são gerados em formato 16:9. Cada método ``add_*`` retorna
    o slide criado para permitir customização adicional se necessário,
    embora o uso recomendado seja chamar apenas os métodos sem mexer no
    objeto python-pptx por baixo.
    """

    def __init__(self, title: str = "", author: str = "Endor Energia"):
        self.prs = Presentation()
        self.prs.slide_width = Cm(SLIDE_W_CM)
        self.prs.slide_height = Cm(SLIDE_H_CM)
        self._title = title
        self._author = author
        self._slides: list = []  # tracker de slides + flags para repaginação

    # -----------------------------------------------------------------
    # Slides primários
    # -----------------------------------------------------------------

    def add_cover(
        self,
        subtitle: str = "",
        date: str = "",
        metadata: dict[str, str] | None = None,
    ):
        """Capa estilo Luz Imperial: lado esquerdo azul Endor com texto branco."""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])

        # Fundo Endor cobrindo o slide inteiro
        _add_filled_rect(slide, 0, 0, self.prs.slide_width, self.prs.slide_height, styles.BRAND.endor)

        # Faixa decorativa gradient (Terra → Pôr do Sol) no topo
        # python-pptx não suporta gradientes diretos via API simples — usamos
        # duas faixas adjacentes como aproximação visual.
        strip_h = Cm(0.4)
        half_w = self.prs.slide_width // 2
        _add_filled_rect(slide, 0, 0, half_w, strip_h, styles.BRAND.terra)
        _add_filled_rect(slide, half_w, 0, half_w, strip_h, styles.BRAND.por_do_sol)

        # Logo no topo esquerdo (versão fundo azul)
        if styles.LOGOS.fundo_azul_png.exists():
            slide.shapes.add_picture(
                str(styles.LOGOS.fundo_azul_png),
                left=Cm(2.0),
                top=Cm(2.0),
                height=Cm(2.4),
            )

        # Título grande
        title_tf = _add_textbox(slide, Cm(2.0), Cm(7.0), Cm(20.0), Cm(5.0))
        _set_text(
            title_tf,
            self._title,
            size=styles.SIZES.display,
            color=styles.NEUTRAL.white,
            bold=True,
        )

        # Subtítulo
        if subtitle:
            sub_tf = _add_textbox(slide, Cm(2.0), Cm(12.5), Cm(20.0), Cm(1.5))
            _set_text(
                sub_tf,
                subtitle,
                size=styles.SIZES.h2,
                color=styles.NEUTRAL.white,
            )

        # Data
        if date:
            date_tf = _add_textbox(slide, Cm(2.0), Cm(14.5), Cm(15.0), Cm(0.8))
            _set_text(
                date_tf,
                date,
                size=styles.SIZES.body,
                color=styles.BRAND.terra,
            )

        # Metadados (CONTRATO, EMISSÃO, etc) — opcionais
        if metadata:
            y = Cm(16.0)
            x = Cm(2.0)
            for key, val in metadata.items():
                lbl_tf = _add_textbox(slide, x, y, Cm(8.0), Cm(0.4))
                _set_text(lbl_tf, key.upper(), size=styles.SIZES.tiny, color=styles.NEUTRAL.gray_300)
                val_tf = _add_textbox(slide, x, y + Cm(0.4), Cm(8.0), Cm(0.5))
                _set_text(val_tf, val, size=styles.SIZES.small, color=styles.NEUTRAL.white)
                x += Cm(8.5)

        self._slides.append(("cover", slide))
        return slide

    def add_section_divider(self, label: str, number: int | None = None):
        """Slide divisor de seção: fundo Endor, número grande + label."""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        _add_filled_rect(slide, 0, 0, self.prs.slide_width, self.prs.slide_height, styles.BRAND.endor)

        # Faixa gradient no topo
        strip_h = Cm(0.4)
        half_w = self.prs.slide_width // 2
        _add_filled_rect(slide, 0, 0, half_w, strip_h, styles.BRAND.terra)
        _add_filled_rect(slide, half_w, 0, half_w, strip_h, styles.BRAND.por_do_sol)

        # Logo
        if styles.LOGOS.fundo_azul_png.exists():
            slide.shapes.add_picture(
                str(styles.LOGOS.fundo_azul_png),
                left=Cm(SLIDE_W_CM - 6.0),
                top=Cm(SLIDE_H_CM - 3.0),
                height=Cm(1.6),
            )

        # Número grande
        if number is not None:
            num_tf = _add_textbox(slide, Cm(2.0), Cm(5.0), Cm(10.0), Cm(6.0))
            _set_text(
                num_tf,
                str(number).zfill(2),
                size=140,
                color=styles.BRAND.terra,
                bold=True,
            )

        # Label
        label_tf = _add_textbox(slide, Cm(2.0), Cm(11.5), Cm(28.0), Cm(3.0))
        _set_text(
            label_tf,
            label,
            size=styles.SIZES.display,
            color=styles.NEUTRAL.white,
            bold=True,
        )

        self._slides.append(("divider", slide))
        return slide

    def add_content_slide(
        self,
        title: str,
        bullets: list[str] | None = None,
        body: str | None = None,
        subtitle: str | None = None,
    ):
        """Slide de conteúdo padrão: título + opcional subtítulo + bullets ou body."""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])

        # Faixa gradient sutil no topo
        strip_h = Cm(0.3)
        _add_filled_rect(slide, 0, 0, self.prs.slide_width, strip_h, styles.BRAND.terra)

        _add_logo(slide)

        # Título da seção (h1, azul Endor)
        title_tf = _add_textbox(slide, Cm(MARGIN_CM), Cm(3.0), Cm(SLIDE_W_CM - 2 * MARGIN_CM), Cm(1.5))
        _set_text(title_tf, title, size=styles.SIZES.h1, color=styles.BRAND.endor, bold=True)

        # Subtítulo (h2, Terra)
        cursor_y = 4.6
        if subtitle:
            sub_tf = _add_textbox(slide, Cm(MARGIN_CM), Cm(cursor_y), Cm(SLIDE_W_CM - 2 * MARGIN_CM), Cm(1.2))
            _set_text(sub_tf, subtitle, size=styles.SIZES.h2, color=styles.BRAND.terra, bold=True)
            cursor_y += 1.3

        # Bullets
        if bullets:
            body_tf = _add_textbox(
                slide,
                Cm(MARGIN_CM),
                Cm(cursor_y),
                Cm(SLIDE_W_CM - 2 * MARGIN_CM),
                Cm(SLIDE_H_CM - cursor_y - 2.0),
            )
            body_tf.clear()
            for i, item in enumerate(bullets):
                p = body_tf.paragraphs[0] if i == 0 else body_tf.add_paragraph()
                p.alignment = PP_ALIGN.LEFT
                run = p.add_run()
                run.text = f"•  {item}"
                f = run.font
                f.name = styles.FONTS.document
                f.size = Pt(styles.SIZES.body + 2)  # body+2 dá legibilidade em slide
                f.color.rgb = styles.NEUTRAL.gray_800.as_pptx()
                p.space_after = Pt(8)

        # Body livre
        elif body:
            body_tf = _add_textbox(
                slide,
                Cm(MARGIN_CM),
                Cm(cursor_y),
                Cm(SLIDE_W_CM - 2 * MARGIN_CM),
                Cm(SLIDE_H_CM - cursor_y - 2.0),
            )
            _set_text(body_tf, body, size=styles.SIZES.body + 2, color=styles.NEUTRAL.gray_800)

        self._slides.append(("content", slide))
        return slide

    def add_chart_slide(self, title: str, chart_image: str | Path, caption: str | None = None):
        """Slide com gráfico ocupando a área principal."""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])

        strip_h = Cm(0.3)
        _add_filled_rect(slide, 0, 0, self.prs.slide_width, strip_h, styles.BRAND.terra)

        _add_logo(slide)

        title_tf = _add_textbox(slide, Cm(MARGIN_CM), Cm(3.0), Cm(SLIDE_W_CM - 2 * MARGIN_CM), Cm(1.5))
        _set_text(title_tf, title, size=styles.SIZES.h1, color=styles.BRAND.endor, bold=True)

        # Imagem do gráfico
        chart_path = Path(chart_image)
        if chart_path.exists():
            slide.shapes.add_picture(
                str(chart_path),
                left=Cm(MARGIN_CM),
                top=Cm(5.0),
                width=Cm(SLIDE_W_CM - 2 * MARGIN_CM),
            )

        if caption:
            cap_tf = _add_textbox(slide, Cm(MARGIN_CM), Cm(SLIDE_H_CM - 2.2), Cm(SLIDE_W_CM - 2 * MARGIN_CM), Cm(0.6))
            _set_text(cap_tf, caption, size=styles.SIZES.small, color=styles.NEUTRAL.gray_600)

        self._slides.append(("chart", slide))
        return slide

    def add_kpi_slide(self, title: str, kpis: list[dict]):
        """Slide com até 4 cards de KPI horizontal.

        Cada KPI é um dict: ``{"label": "...", "value": "...", "subtext": "...", "color": Color}``.
        ``color`` é opcional — default é Terra. Use cores secundárias da paleta para categorizar.
        """
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])

        strip_h = Cm(0.3)
        _add_filled_rect(slide, 0, 0, self.prs.slide_width, strip_h, styles.BRAND.terra)

        _add_logo(slide)

        title_tf = _add_textbox(slide, Cm(MARGIN_CM), Cm(3.0), Cm(SLIDE_W_CM - 2 * MARGIN_CM), Cm(1.5))
        _set_text(title_tf, title, size=styles.SIZES.h1, color=styles.BRAND.endor, bold=True)

        # Cards de KPI distribuídos horizontalmente
        kpis = kpis[:4]  # máximo 4 por slide
        n = len(kpis)
        if n == 0:
            return slide

        card_h = Cm(5.0)
        total_w = SLIDE_W_CM - 2 * MARGIN_CM
        gap = 0.5
        card_w = (total_w - gap * (n - 1)) / n
        y = Cm(7.0)
        for i, kpi in enumerate(kpis):
            x = Cm(MARGIN_CM + i * (card_w + gap))
            color = kpi.get("color", styles.BRAND.terra)

            # Card body
            _add_filled_rect(slide, x, y, Cm(card_w), card_h, styles.NEUTRAL.gray_50)
            # Tag colorida no topo
            _add_filled_rect(slide, x, y, Cm(card_w), Cm(0.25), color)

            inner_x = x + Cm(0.4)
            inner_w = Cm(card_w - 0.8)

            # Label
            lbl_tf = _add_textbox(slide, inner_x, y + Cm(0.6), inner_w, Cm(0.6))
            _set_text(
                lbl_tf,
                kpi["label"].upper(),
                size=styles.SIZES.kpi_label,
                color=styles.NEUTRAL.gray_600,
                bold=True,
            )

            # Value
            val_tf = _add_textbox(slide, inner_x, y + Cm(1.4), inner_w, Cm(2.0))
            _set_text(
                val_tf,
                str(kpi["value"]),
                size=styles.SIZES.kpi_value,
                color=styles.BRAND.endor,
                bold=True,
            )

            # Subtext
            if kpi.get("subtext"):
                sub_tf = _add_textbox(slide, inner_x, y + Cm(3.8), inner_w, Cm(0.6))
                _set_text(
                    sub_tf,
                    kpi["subtext"],
                    size=styles.SIZES.small,
                    color=styles.NEUTRAL.gray_600,
                )

        self._slides.append(("kpi", slide))
        return slide

    def add_closing(self, text: str = "Obrigado.", contact: str | None = None):
        """Slide de encerramento — fundo Endor, texto centralizado."""
        slide = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        _add_filled_rect(slide, 0, 0, self.prs.slide_width, self.prs.slide_height, styles.BRAND.endor)

        # Logo grande centralizado-alto
        if styles.LOGOS.fundo_azul_png.exists():
            slide.shapes.add_picture(
                str(styles.LOGOS.fundo_azul_png),
                left=Cm(SLIDE_W_CM / 2 - 4),
                top=Cm(5.0),
                height=Cm(3.5),
            )

        text_tf = _add_textbox(slide, Cm(2.0), Cm(10.5), Cm(SLIDE_W_CM - 4.0), Cm(2.0))
        _set_text(text_tf, text, size=styles.SIZES.display, color=styles.NEUTRAL.white, bold=True, align=PP_ALIGN.CENTER)

        if contact:
            c_tf = _add_textbox(slide, Cm(2.0), Cm(13.5), Cm(SLIDE_W_CM - 4.0), Cm(0.8))
            _set_text(c_tf, contact, size=styles.SIZES.body, color=styles.BRAND.terra, align=PP_ALIGN.CENTER)

        self._slides.append(("closing", slide))
        return slide

    # -----------------------------------------------------------------
    # Paginação + save
    # -----------------------------------------------------------------

    def _apply_footers(self):
        """Adiciona footer e paginação a todos os slides não-capa/divisor/closing."""
        total = len(self._slides)
        for i, (kind, slide) in enumerate(self._slides, start=1):
            if kind in ("content", "chart", "kpi"):
                _add_footer(slide, page_num=i, total=total, on_dark=False)

    def save(self, path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self._apply_footers()
        self.prs.save(str(path))
        return path
