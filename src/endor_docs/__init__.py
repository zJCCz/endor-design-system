"""
endor_docs — Builders Python para artefatos visuais da Endor Energia.

Uso típico:

    from endor_docs import EndorPresentation, EndorWorkbook
    from endor_docs.styles import COLORS, FONTS, SIZES

    deck = EndorPresentation(title="Relatório Q1/2026")
    deck.add_cover(subtitle="Apresentação de Resultados")
    deck.add_content_slide(title="Mercado", bullets=["..."])
    deck.save("output.pptx")

A fonte da verdade visual está em ``tokens/endor.tokens.json``.
Os builders carregam esses tokens via ``endor_docs.styles``.
"""

from endor_docs.ppt_builder import EndorPresentation
from endor_docs.xlsx_builder import EndorWorkbook

__version__ = "0.1.0"

__all__ = [
    "EndorPresentation",
    "EndorWorkbook",
    "__version__",
]
