# Endor Design System

Sistema operacional da identidade visual da **Endor Energia**. Gere
apresentações, planilhas, relatórios e qualquer artefato visual da empresa
aplicando a marca de forma consistente — via Python ou via templates Office.

## O que tem aqui

```
brand/              Documentação humana (PDF guia + MDs)
tokens/             Cores, fontes, espaços (W3C Design Tokens)
assets/             Logos oficiais (3 variantes × 4 categorias)
src/endor_docs/     Builders Python (EndorPresentation, EndorWorkbook)
templates/          6 templates prontos (3 .pptx + 3 .xlsx)
examples/           6 exemplos preenchidos com dados realistas
docs/               Guias de uso
scripts/            Scripts de manutenção e regeneração
CLAUDE.md           Instruções para IAs operarem o sistema
```

## Instalação

Python 3.10+ requerido.

```bash
git clone <repo>
cd endor-design-system
pip install -e .
```

Para gerar gráficos via matplotlib:

```bash
pip install -e ".[charts]"
```

## Quickstart — Apresentação em 30 segundos

```python
from endor_docs import EndorPresentation, styles

deck = EndorPresentation(title="Endor Energia — Q1/2026")
deck.add_cover(subtitle="Resultados do trimestre", date="Abril 2026")

deck.add_section_divider("Indicadores", number=1)
deck.add_kpi_slide(
    title="Q1/2026",
    kpis=[
        {"label": "Receita", "value": "R$ 28 MM", "subtext": "+21% YoY"},
        {"label": "EBITDA", "value": "32,1%", "color": styles.BRAND.natureza},
        {"label": "SLA", "value": "98,7%", "color": styles.BRAND.por_do_sol},
        {"label": "Concessões", "value": "3", "color": styles.BRAND.terra},
    ],
)

deck.add_closing(text="Obrigado.", contact="ri@endor.energia")
deck.save("q1_2026.pptx")
```

Resultado: arquivo `.pptx` com capa, divisor de seção, slide de KPI e
closing, todos com a marca Endor aplicada (logo, paleta, tipografia,
faixas decorativas, paginação).

## Quickstart — Planilha em 30 segundos

```python
from endor_docs import EndorWorkbook, styles

wb = EndorWorkbook(title="Modelo Financeiro — Luz Imperial")
wb.add_cover(
    subtitle="PPP de Iluminação Pública",
    metadata={"Contrato": "27/2023", "Vigência": "2020–2030"},
)

prem = wb.add_sheet("Premissas")
wb.write_header_row(prem, row=4, headers=["Premissa", "Valor", "Unidade"], start_col=2)
prem.cell(row=5, column=2, value="Taxa de desconto")
prem.cell(row=5, column=3, value=0.118)
prem.cell(row=5, column=4, value="% a.a.")
wb.format_percent(prem, "C5:C5")
wb.apply_zebra(prem, start_row=5, end_row=5, start_col=2, end_col=4)
wb.define_name("wacc", prem, "$C$5")

wb.save("modelo.xlsx")
```

## Sem código — usar os templates

```bash
cp templates/pptx/endor_project_report_template.pptx meu_relatorio.pptx
```

Abre no PowerPoint/Keynote/LibreOffice, substitui os `[Placeholders]`,
salva. Não mexa em cores, fontes ou layout — apenas no conteúdo textual.

## Regenerar tudo

```bash
python scripts/build_templates.py   # 6 templates
python scripts/build_examples.py    # 6 exemplos
```

Ambos lêem `tokens/endor.tokens.json` + `src/endor_docs/*` e produzem os
artefatos. Sempre que mudar tokens ou builders, re-rode e commite.

## Documentação por papel

| Você é... | Comece por |
|--|--|
| **IA (Claude) gerando artefatos** | [`CLAUDE.md`](CLAUDE.md) |
| **Desenvolvedor integrando ao seu sistema** | [`docs/`](docs/) + [`src/endor_docs/`](src/endor_docs/) |
| **Analista usando os templates** | [`docs/powerpoint_guidelines.md`](docs/powerpoint_guidelines.md) e [`docs/spreadsheet_guidelines.md`](docs/spreadsheet_guidelines.md) |
| **Designer criando peças customizadas** | [`brand/Endor_Guia_Identidade_Visual.pdf`](brand/Endor_Guia_Identidade_Visual.pdf) + [`assets/logos/*/vetor/*.ai`](assets/logos/) |
| **Marketing / equipe de marca** | [`brand/endor_design_system.md`](brand/endor_design_system.md) + [`brand/visual_rules.md`](brand/visual_rules.md) |

## Paleta — visão rápida

| Token | Hex | Uso |
|--|--|--|
| `BRAND.endor` | `#0A1A5C` | Cor institucional |
| `BRAND.terra` | `#0083CA` | Destaques, h2 |
| `BRAND.por_do_sol` | `#6C3F99` | Social, comunitário |
| `BRAND.natureza` | `#00718A` | ESG, ambiental, success |
| `BRAND.tech` | `#858A9E` | Técnico, auxiliar |

Tipografia: **Calibri** em documentos Office (default dos builders).
**Avenir Next LT Pro** institucional para peças impressas finais — arquivos
em `assets/fonts/`, licença Linotype/Monotype (**não redistribuir**).

## Estrutura de marca

- **Endor Energia** (holding)
  - 4 Submarcas: Ambiental, Geração Distribuída, Infraestrutura, Participações
  - 3 Concessionárias: Luz do Vale, Luz Imperial, Miguel Pereira Luz

## Versão

`v0.1.0` — bootstrap inicial. Mudanças em `0.x` podem quebrar API. A partir
de `1.0.0`, breaking changes irão pra CHANGELOG.

## Princípios

1. **Tokens são lei** — toda decisão visual vem do `tokens/endor.tokens.json`
2. **Templates são gerados, não desenhados** — edição manual é descartável
3. **A marca tem hierarquia** — Endor > Submarcas > Concessionárias

## Licença

Proprietary. Uso interno da Endor Energia. Reprodução parcial ou total
sem autorização expressa proibida.
