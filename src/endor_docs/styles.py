"""
Carrega ``tokens/endor.tokens.json`` e expõe os valores como constantes Python.

Este módulo é a ÚNICA fonte de cores, fontes e dimensões para os builders.
Nada em ``ppt_builder.py``, ``xlsx_builder.py`` ou ``charts.py`` deve ter
literal de cor, fonte ou tamanho — sempre via ``styles.COLORS``, ``styles.FONTS``,
``styles.SIZES`` etc.

Quando ``tokens/endor.tokens.json`` muda, basta reimportar este módulo
(ou re-rodar os builders) e tudo se atualiza.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from typing import Any


_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOKENS_PATH = _REPO_ROOT / "tokens" / "endor.tokens.json"
ASSETS_PATH = _REPO_ROOT / "assets"
BRAND_PATH = _REPO_ROOT / "brand"


@dataclass(frozen=True)
class Color:
    """Cor da marca. Expõe múltiplos formatos pra diferentes libs."""

    hex: str
    rgb: tuple[int, int, int]
    name: str = ""
    description: str = ""

    @property
    def hex_no_hash(self) -> str:
        return self.hex.lstrip("#")

    @property
    def argb(self) -> str:
        """openpyxl quer 'FFRRGGBB' (alpha + RGB, sem #)."""
        return f"FF{self.hex_no_hash.upper()}"

    def as_pptx(self):
        """python-pptx quer ``RGBColor(r, g, b)``."""
        from pptx.dml.color import RGBColor

        return RGBColor(*self.rgb)

    def as_matplotlib(self) -> str:
        """matplotlib aceita string hex direto."""
        return self.hex

    def __str__(self) -> str:  # pragma: no cover - convenience
        return self.hex


def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _resolve_alias(value: Any, root: dict) -> Any:
    """Resolve referências W3C do tipo ``{color.brand.endor}``."""
    if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
        path = value[1:-1].split(".")
        cur: Any = root
        for part in path:
            cur = cur[part]
        return _resolve_alias(cur.get("$value"), root)
    if isinstance(value, list):
        return [_resolve_alias(v, root) for v in value]
    return value


def _load_tokens() -> dict:
    with TOKENS_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def _color(node: dict, root: dict, name: str = "") -> Color:
    resolved_hex = _resolve_alias(node["$value"], root)
    return Color(
        hex=resolved_hex,
        rgb=_hex_to_rgb(resolved_hex),
        name=name,
        description=node.get("$description", ""),
    )


_TOKENS = _load_tokens()


# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------

_brand = _TOKENS["color"]["brand"]
_neutral = _TOKENS["color"]["neutral"]
_semantic = _TOKENS["color"]["semantic"]

BRAND = SimpleNamespace(
    endor=_color(_brand["endor"], _TOKENS, "endor"),
    terra=_color(_brand["terra"], _TOKENS, "terra"),
    por_do_sol=_color(_brand["por-do-sol"], _TOKENS, "por-do-sol"),
    natureza=_color(_brand["natureza"], _TOKENS, "natureza"),
    tech=_color(_brand["tech"], _TOKENS, "tech"),
)

NEUTRAL = SimpleNamespace(
    gray_50=_color(_neutral["gray-50"], _TOKENS, "gray-50"),
    gray_100=_color(_neutral["gray-100"], _TOKENS, "gray-100"),
    gray_200=_color(_neutral["gray-200"], _TOKENS, "gray-200"),
    gray_300=_color(_neutral["gray-300"], _TOKENS, "gray-300"),
    gray_400=_color(_neutral["gray-400"], _TOKENS, "gray-400"),
    gray_500=_color(_neutral["gray-500"], _TOKENS, "gray-500"),
    gray_600=_color(_neutral["gray-600"], _TOKENS, "gray-600"),
    gray_700=_color(_neutral["gray-700"], _TOKENS, "gray-700"),
    gray_800=_color(_neutral["gray-800"], _TOKENS, "gray-800"),
    gray_900=_color(_neutral["gray-900"], _TOKENS, "gray-900"),
    white=_color(_neutral["white"], _TOKENS, "white"),
    black=_color(_neutral["black"], _TOKENS, "black"),
)

SEMANTIC = SimpleNamespace(
    success=_color(_semantic["success"], _TOKENS, "success"),
    info=_color(_semantic["info"], _TOKENS, "info"),
    warning=_color(_semantic["warning"], _TOKENS, "warning"),
    error=_color(_semantic["error"], _TOKENS, "error"),
)

# Paleta categórica resolvida para uso direto em gráficos
CHART_CATEGORICAL: list[Color] = [
    _color({"$value": v}, _TOKENS) for v in _resolve_alias(_TOKENS["color"]["chart"]["categorical"]["$value"], _TOKENS)
]

CHART_SEQUENTIAL_BLUE: list[Color] = [
    _color({"$value": v}, _TOKENS) for v in _TOKENS["color"]["chart"]["sequential-blue"]["$value"]
]


# Atalho top-level com tudo agrupado
COLORS = SimpleNamespace(
    brand=BRAND,
    neutral=NEUTRAL,
    semantic=SEMANTIC,
    chart_categorical=CHART_CATEGORICAL,
    chart_sequential_blue=CHART_SEQUENTIAL_BLUE,
)


# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------

_font = _TOKENS["font"]

FONTS = SimpleNamespace(
    primary=_font["family"]["primary"]["$value"],
    document=_font["family"]["document"]["$value"],
    primary_fallback=_font["family"]["primary"]["$extensions"]["br.endor.fallback"],
    document_fallback=_font["family"]["document"]["$extensions"]["br.endor.fallback"],
)

WEIGHTS = SimpleNamespace(
    ultra_light=_font["weight"]["ultra-light"]["$value"],
    regular=_font["weight"]["regular"]["$value"],
    medium=_font["weight"]["medium"]["$value"],
    demi=_font["weight"]["demi"]["$value"],
    bold=_font["weight"]["bold"]["$value"],
    heavy=_font["weight"]["heavy"]["$value"],
)

SIZES = SimpleNamespace(
    display=_font["size"]["display"]["$value"],
    h1=_font["size"]["h1"]["$value"],
    h2=_font["size"]["h2"]["$value"],
    h3=_font["size"]["h3"]["$value"],
    body=_font["size"]["body"]["$value"],
    small=_font["size"]["small"]["$value"],
    tiny=_font["size"]["tiny"]["$value"],
    kpi_value=_font["size"]["kpi-value"]["$value"],
    kpi_label=_font["size"]["kpi-label"]["$value"],
)

LINE_HEIGHT = SimpleNamespace(
    tight=_font["lineHeight"]["tight"]["$value"],
    normal=_font["lineHeight"]["normal"]["$value"],
    relaxed=_font["lineHeight"]["relaxed"]["$value"],
)


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

SPACE = SimpleNamespace(
    s0=_TOKENS["space"]["0"]["$value"],
    s1=_TOKENS["space"]["1"]["$value"],
    s2=_TOKENS["space"]["2"]["$value"],
    s3=_TOKENS["space"]["3"]["$value"],
    s4=_TOKENS["space"]["4"]["$value"],
    s5=_TOKENS["space"]["5"]["$value"],
    s6=_TOKENS["space"]["6"]["$value"],
    s7=_TOKENS["space"]["7"]["$value"],
    s8=_TOKENS["space"]["8"]["$value"],
)

RADIUS = SimpleNamespace(
    none=_TOKENS["radius"]["none"]["$value"],
    sm=_TOKENS["radius"]["sm"]["$value"],
    md=_TOKENS["radius"]["md"]["$value"],
    lg=_TOKENS["radius"]["lg"]["$value"],
    pill=_TOKENS["radius"]["pill"]["$value"],
)


# ---------------------------------------------------------------------------
# Logo paths — resolvidos uma vez aqui, builders usam.
# ---------------------------------------------------------------------------

LOGOS = SimpleNamespace(
    # Para uso em fundos claros (default em PPT/XLSX)
    fundo_branco_png=ASSETS_PATH / "logos/fundo-branco/energia/digital/EndorEnergia.png",
    fundo_branco_pdf=ASSETS_PATH / "logos/fundo-branco/energia/vetor/EndorEnergia.pdf",
    fundo_branco_simplificada_pdf=ASSETS_PATH
    / "logos/fundo-branco/energia/simplificada/EndorEnergia_UsoRestrito.pdf",
    # Para uso em fundos azuis institucionais
    fundo_azul_png=ASSETS_PATH / "logos/fundo-azul/energia/digital/EndorEnergia.png",
    fundo_azul_pdf=ASSETS_PATH / "logos/fundo-azul/energia/vetor/EndorEnergia.pdf",
    # Símbolo isolado (avatar, favicon, peças pequenas)
    simbolo_branco_png=ASSETS_PATH / "logos/fundo-branco/simbolo/EndorEnergia_SimboloBranco.png",
    simbolo_azul_png=ASSETS_PATH / "logos/fundo-azul/simbolo/EndorEnergia_SimboloAzul.png",
    simbolo_transparente_png=ASSETS_PATH / "logos/fundo-branco/simbolo/EndorEnergia_SimboloSemfundo.png",
)


# ---------------------------------------------------------------------------
# Metadata
# ---------------------------------------------------------------------------

VERSION = _TOKENS["$metadata"]["version"]
TOKENS_RAW = _TOKENS


def all_colors() -> dict[str, Color]:
    """Devolve todas as cores nomeadas — útil para debug e diagnósticos."""
    out = {}
    for ns, prefix in [(BRAND, "brand"), (NEUTRAL, "neutral"), (SEMANTIC, "semantic")]:
        for key, val in vars(ns).items():
            if isinstance(val, Color):
                out[f"{prefix}.{key}"] = val
    return out
