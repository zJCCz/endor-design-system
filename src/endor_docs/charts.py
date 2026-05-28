"""
Fábricas de gráficos com identidade Endor aplicada.

Geram figuras matplotlib, salvam como PNG em tamanho/DPI adequado para
embedding em PPTX/PDF, e devolvem o ``Path`` do arquivo.

Para uso em planilhas Excel, prefira charts nativos via ``openpyxl.chart``
(ver ``endor_docs.xlsx_builder.EndorWorkbook.add_chart``) — eles atualizam
automaticamente quando o usuário edita os dados.
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from endor_docs import styles


def _ensure_matplotlib():
    try:
        import matplotlib
    except ImportError as e:  # pragma: no cover
        raise RuntimeError(
            "matplotlib não está instalado. Instale com: pip install 'endor-docs[charts]'"
        ) from e

    matplotlib.use("Agg")  # backend sem display para servidores/scripts
    return matplotlib


def _new_figure(figsize=(8, 4.5), dpi=150):
    mpl = _ensure_matplotlib()
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    fig.patch.set_facecolor(styles.NEUTRAL.white.hex)
    ax.set_facecolor(styles.NEUTRAL.white.hex)

    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(styles.NEUTRAL.gray_300.hex)
        ax.spines[spine].set_linewidth(0.8)

    ax.tick_params(colors=styles.NEUTRAL.gray_600.hex, labelsize=8)
    ax.title.set_color(styles.BRAND.endor.hex)
    ax.title.set_fontsize(12)
    ax.title.set_fontweight("bold")

    return fig, ax


def _save(fig, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    import matplotlib.pyplot as plt

    plt.close(fig)
    return out_path


def _palette(n: int) -> list[str]:
    pal = [c.hex for c in styles.CHART_CATEGORICAL]
    if n <= len(pal):
        return pal[:n]
    # Repete a paleta — gráficos com mais séries que a paleta são raros
    return (pal * (n // len(pal) + 1))[:n]


def bar_chart(
    categories: Sequence[str],
    values: Sequence[float],
    out_path: Path,
    title: str = "",
    ylabel: str = "",
    color: str | None = None,
    figsize: tuple[float, float] = (8, 4.5),
) -> Path:
    """Gráfico de barras verticais simples."""
    fig, ax = _new_figure(figsize=figsize)
    color = color or styles.BRAND.terra.hex
    ax.bar(list(categories), list(values), color=color, edgecolor="none")
    if title:
        ax.set_title(title, loc="left", pad=12)
    if ylabel:
        ax.set_ylabel(ylabel, color=styles.NEUTRAL.gray_700.hex)
    ax.grid(axis="y", color=styles.NEUTRAL.gray_200.hex, linewidth=0.6)
    ax.set_axisbelow(True)
    return _save(fig, out_path)


def grouped_bar_chart(
    categories: Sequence[str],
    series: dict[str, Sequence[float]],
    out_path: Path,
    title: str = "",
    ylabel: str = "",
    figsize: tuple[float, float] = (9, 4.5),
) -> Path:
    """Múltiplas séries lado a lado."""
    import numpy as np

    fig, ax = _new_figure(figsize=figsize)
    cats = list(categories)
    n_series = len(series)
    colors = _palette(n_series)
    x = np.arange(len(cats))
    width = 0.8 / n_series

    for i, (label, vals) in enumerate(series.items()):
        offset = (i - (n_series - 1) / 2) * width
        ax.bar(x + offset, list(vals), width=width, label=label, color=colors[i], edgecolor="none")

    ax.set_xticks(x)
    ax.set_xticklabels(cats)
    if title:
        ax.set_title(title, loc="left", pad=12)
    if ylabel:
        ax.set_ylabel(ylabel, color=styles.NEUTRAL.gray_700.hex)
    ax.grid(axis="y", color=styles.NEUTRAL.gray_200.hex, linewidth=0.6)
    ax.set_axisbelow(True)
    legend = ax.legend(loc="upper left", frameon=False, fontsize=8, labelcolor=styles.NEUTRAL.gray_700.hex)
    for text in legend.get_texts():
        text.set_color(styles.NEUTRAL.gray_700.hex)
    return _save(fig, out_path)


def line_chart(
    x: Sequence,
    y: Sequence[float],
    out_path: Path,
    title: str = "",
    ylabel: str = "",
    color: str | None = None,
    figsize: tuple[float, float] = (8, 4.5),
) -> Path:
    """Linha simples."""
    fig, ax = _new_figure(figsize=figsize)
    color = color or styles.BRAND.terra.hex
    ax.plot(list(x), list(y), color=color, linewidth=2.4, marker="o", markersize=5)
    if title:
        ax.set_title(title, loc="left", pad=12)
    if ylabel:
        ax.set_ylabel(ylabel, color=styles.NEUTRAL.gray_700.hex)
    ax.grid(axis="y", color=styles.NEUTRAL.gray_200.hex, linewidth=0.6)
    ax.set_axisbelow(True)
    return _save(fig, out_path)


def pie_chart(
    labels: Sequence[str],
    values: Sequence[float],
    out_path: Path,
    title: str = "",
    figsize: tuple[float, float] = (6, 4.5),
) -> Path:
    """Pizza/donut. Use só pra ≤6 categorias — acima disso vira ilegível."""
    fig, ax = _new_figure(figsize=figsize)
    colors = _palette(len(values))
    wedges, texts, autotexts = ax.pie(
        list(values),
        labels=list(labels),
        colors=colors,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"width": 0.35, "edgecolor": styles.NEUTRAL.white.hex, "linewidth": 2},
        textprops={"color": styles.NEUTRAL.gray_700.hex, "fontsize": 9},
    )
    for at in autotexts:
        at.set_color(styles.NEUTRAL.white.hex)
        at.set_fontweight("bold")
    ax.set_aspect("equal")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    if title:
        ax.set_title(title, loc="left", pad=12)
    return _save(fig, out_path)


def horizontal_bar_chart(
    categories: Sequence[str],
    values: Sequence[float],
    out_path: Path,
    title: str = "",
    color: str | None = None,
    figsize: tuple[float, float] = (8, 4.5),
) -> Path:
    """Barras horizontais — bom pra rankings com nomes longos."""
    fig, ax = _new_figure(figsize=figsize)
    color = color or styles.BRAND.terra.hex
    cats = list(categories)
    ax.barh(cats, list(values), color=color, edgecolor="none")
    ax.invert_yaxis()  # categoria de maior valor no topo
    if title:
        ax.set_title(title, loc="left", pad=12)
    ax.grid(axis="x", color=styles.NEUTRAL.gray_200.hex, linewidth=0.6)
    ax.set_axisbelow(True)
    return _save(fig, out_path)


def waterfall_chart(
    categories: Sequence[str],
    values: Sequence[float],
    out_path: Path,
    title: str = "",
    figsize: tuple[float, float] = (9, 4.5),
) -> Path:
    """Cascata: ganhos/perdas sequenciais. Valor negativo desce, positivo sobe."""
    fig, ax = _new_figure(figsize=figsize)
    cats = list(categories)
    vals = list(values)
    cumulative = 0.0
    for i, v in enumerate(vals):
        color = styles.SEMANTIC.success.hex if v >= 0 else styles.SEMANTIC.error.hex
        # Total bars: primeiro e último são totais (não incrementais)
        if i in (0, len(vals) - 1):
            color = styles.BRAND.endor.hex
            ax.bar(cats[i], v, color=color, edgecolor="none")
            cumulative = v if i == 0 else cumulative
        else:
            ax.bar(cats[i], v, bottom=cumulative, color=color, edgecolor="none")
            cumulative += v
    if title:
        ax.set_title(title, loc="left", pad=12)
    ax.grid(axis="y", color=styles.NEUTRAL.gray_200.hex, linewidth=0.6)
    ax.set_axisbelow(True)
    return _save(fig, out_path)
