# Gráficos — Diretrizes de Uso

Como escolher e construir gráficos para artefatos Endor. Use sempre as
fábricas em `endor_docs.charts` — paleta, eixos, tipografia e
proporções já vêm padronizados.

## Qual gráfico para qual dado?

| Tipo de dado | Gráfico recomendado | Função |
|--|--|--|
| Série temporal contínua (5+ pontos) | Linha | `charts.line_chart` |
| Série temporal curta (≤4 pontos) ou comparação de magnitudes | Barras verticais | `charts.bar_chart` |
| Comparação de 2–4 categorias × 2–3 séries | Barras agrupadas | `charts.grouped_bar_chart` |
| Composição de UM total (4–6 categorias) | Donut/pizza | `charts.pie_chart` |
| Ranking de N categorias (nomes longos) | Barras horizontais | `charts.horizontal_bar_chart` |
| Decomposição sequencial (ganhos/perdas) | Cascata | `charts.waterfall_chart` |
| Distribuição geográfica | Mapa (Leaflet, externo) | — |

## Paleta de cores

A paleta categórica canônica está em `color.chart.categorical` do tokens:

| Ordem | Cor | Quando usar |
|--|--|--|
| 1 | Endor (azul institucional) | Série principal, valor agregado |
| 2 | Terra (azul claro) | Segunda série, secundário |
| 3 | Pôr do Sol (roxo) | Categoria social/comunitária |
| 4 | Natureza (teal) | ESG, ambiental, indicador positivo |
| 5 | Tech (cinza) | Categoria técnica, residual, "outros" |
| 6 | Warning (âmbar) | Atenção, valor próximo do limite |
| 7 | Error (vermelho) | Falha, atraso |

A fábrica `charts.*` aplica essa ordem automaticamente. Para sobrescrever
com uma cor específica, passe `color=styles.BRAND.natureza.hex`.

### Sequencial (escala única)

Para heatmaps, choropleths e dados ordinais, use `color.chart.sequential-blue`:
gradação `gray-100 → terra → endor` (claro → escuro).

## Regras de eixos e formatação

Aplicadas automaticamente pelas fábricas:

- **Eixos**: linha cinza-300, espessura 0.8pt
- **Top e right spines**: ocultos (eixo aberto)
- **Ticks**: cinza-600, 8pt
- **Grid**: apenas horizontal (Y), cinza-200, 0.6pt
- **Título**: azul Endor, 12pt, bold, alinhado à esquerda (omitido se usado
  como `chart_image` num slide — o título do slide é suficiente)
- **Background**: branco
- **DPI**: 150 (suficiente para PPT/PDF impresso até A3)

## Padrões de uso

### Linha com 1 série

```python
charts.line_chart(
    x=["2022", "2023", "2024", "2025"],
    y=[42.1, 58.7, 71.2, 89.5],
    out_path="receita.png",
    ylabel="R$ milhões",
)
```

### Barras agrupadas (2 séries, comparativo)

```python
charts.grouped_bar_chart(
    categories=["Luz Imperial", "Luz do Vale", "Miguel Pereira"],
    series={
        "Q4/2025": [142, 89, 67],
        "Q1/2026": [147, 95, 71],
    },
    out_path="atendimentos.png",
    ylabel="Atendimentos/mês",
)
```

### Donut

```python
charts.pie_chart(
    labels=["LED", "Vapor metálico", "Vapor de sódio", "Outros"],
    values=[96.5, 1.9, 1.1, 0.5],
    out_path="composicao.png",
)
```

## Quando NÃO usar cada gráfico

| Gráfico | Evitar quando |
|--|--|
| Linha | Categorias discretas sem ordem natural (ex: bairros) |
| Pizza/donut | 7+ categorias (vira ilegível). Use barras horizontais |
| Barras verticais | Categorias com nomes longos (5+ palavras) — use horizontais |
| Cascata | Mais de ~6 passos (vira ruído visual) |
| Mapa | Para 3 pontos ou menos (lista é mais clara) |

## Embedding em PPTX/PDF

`add_chart_slide` do `EndorPresentation` aceita o `Path` que as fábricas
retornam:

```python
img_path = charts.bar_chart(...)
deck.add_chart_slide(title="Consumo de energia", chart_image=img_path, caption="...")
```

O builder calcula automaticamente o tamanho preservando aspect ratio.
Width default: largura do slide menos margens. Height máximo: 11.5cm
(deixa espaço para título + caption + footer).

## Charts em planilhas (Excel)

Para gráficos **dentro do Excel** (que reagem a edição dos dados), use
charts nativos do `openpyxl.chart`:

```python
from openpyxl.chart import BarChart, Reference

chart = BarChart()
chart.style = 13  # estilo neutro
data = Reference(ws, min_col=2, min_row=1, max_col=3, max_row=10)
chart.add_data(data, titles_from_data=True)
ws.add_chart(chart, "E2")
```

> Os charts nativos do Excel **não usam a paleta Endor por padrão** —
> precisam ser estilizados manualmente célula a célula ou via XML.
> Esse helper ainda não está implementado no `EndorWorkbook` v0.1.0.
> Para visual consistente, prefira embedding de PNG via `endor_docs.charts`
> nas planilhas que serão exportadas em PDF — perde a interatividade mas
> mantém a identidade.

## Anti-padrões a evitar

- ❌ 3D em qualquer gráfico (distorce percepção de magnitude)
- ❌ Pizza com >6 fatias (ilegível)
- ❌ Cores fora da paleta Endor
- ❌ Múltiplas séries em pizza (use barras agrupadas)
- ❌ Eixo Y começando em valor diferente de 0 (exceto justificado em caption)
- ❌ Gráficos sem caption explicando o "so what"
- ❌ Mistura de unidades no mesmo eixo (kWh + R$)

## Referências

- Charts dos exemplos: `examples/_charts/*.png`
- Fábricas: `src/endor_docs/charts.py`
- Paleta: `tokens/endor.tokens.json` → `color.chart.categorical`
