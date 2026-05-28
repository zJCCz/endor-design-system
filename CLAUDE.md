# CLAUDE.md

Instruções operacionais para instâncias de IA (Claude) que vão **gerar
artefatos visuais da Endor Energia** a partir deste design system.

**Você é IA. Leia este arquivo PRIMEIRO. Siga literalmente.**

---

## O que é a Endor

Empresa do setor de energia. Opera 3 concessões de **iluminação pública**
no Sul Fluminense (Luz Imperial – Vassouras; Luz do Vale – Barra do Piraí;
Miguel Pereira Luz). Tem 4 submarcas (Ambiental, Geração Distribuída,
Infraestrutura, Participações). A marca-mãe é "Endor Energia".

## O que é este repo

Sistema operacional da identidade visual. Fonte única para:
- **Tokens** (cores, fontes, espaços) em `tokens/endor.tokens.json`
- **Assets** (logos, símbolo) em `assets/logos/`
- **Builders Python** em `src/endor_docs/` — gera PPTX e XLSX já com a marca
- **Templates e exemplos** em `templates/` e `examples/`
- **Guia oficial em PDF** em `brand/Endor_Guia_Identidade_Visual.pdf`

---

## REGRAS INEGOCIÁVEIS

1. **Tokens são lei.** Nunca hardcode cor (`"#0A1A5C"`), fonte (`"Calibri"`)
   ou tamanho. Sempre via `endor_docs.styles`.
2. **Builders são o caminho.** Para qualquer .pptx/.xlsx, use `EndorPresentation`
   ou `EndorWorkbook`. Não construa python-pptx/openpyxl direto.
3. **Templates e exemplos são gerados, NÃO editados.** Se precisar mudar um
   template, edite `scripts/build_templates.py` e re-rode. Edição manual do
   .pptx/.xlsx é perdida na próxima geração.
4. **Cores: só da paleta.** As 5 cores brand (Endor, Terra, Pôr do Sol,
   Natureza, Tech) + neutros + 4 semânticas. Nada fora.
5. **Tipografia: Calibri em documentos gerados.** Avenir Next LT Pro
   disponível em `assets/fonts/` para peças impressas finais. **Não
   redistribuir** — licença Linotype/Monotype.
6. **Os 6 usos incorretos do logo** (página 16 do guia) são proibidos.
   Use sempre arquivos originais em `assets/logos/`.

Detalhamento: `brand/visual_rules.md`.

---

## ANTES DE QUALQUER TASK

Garantir que o pacote está instalado:

```bash
pip install -e .
```

Validar que carrega:

```python
from endor_docs import EndorPresentation, EndorWorkbook, styles
print(styles.VERSION)  # "0.1.0"
```

---

## RECEITAS COPY-PASTE

### Receita 1: Apresentação corporativa (interno)

```python
from endor_docs import EndorPresentation, styles

deck = EndorPresentation(title="Endor Energia — All-Hands Q2/2026")
deck.add_cover(subtitle="Reunião trimestral", date="Julho 2026")

deck.add_section_divider("Resultados do trimestre", number=1)
deck.add_kpi_slide(
    title="Indicadores Q2/2026",
    kpis=[
        {"label": "Receita", "value": "R$ XX MM", "subtext": "+X% YoY"},
        {"label": "EBITDA", "value": "XX%", "subtext": "+X p.p.", "color": styles.BRAND.natureza},
        {"label": "Atendimentos", "value": "XXX", "subtext": "no trimestre", "color": styles.BRAND.por_do_sol},
        {"label": "SLA", "value": "XX,X%", "subtext": "meta ≥95%", "color": styles.BRAND.terra},
    ],
)

deck.add_content_slide(
    title="Destaques do período",
    bullets=[
        "[Fato 1 — máx 1 linha]",
        "[Fato 2 — máx 1 linha]",
        "[Fato 3 — máx 1 linha]",
    ],
)

deck.add_closing(text="Obrigado.")
deck.save("output.pptx")
```

### Receita 2: Investor Deck

```python
from endor_docs import EndorPresentation, styles, charts

# 1. Gera os charts ANTES de inserir nos slides
chart_growth = charts.line_chart(
    x=["2022", "2023", "2024", "2025", "2026e"],
    y=[42.1, 58.7, 71.2, 89.5, 108.3],
    out_path="/tmp/growth.png",
    ylabel="R$ milhões",
)

# 2. Monta o deck
deck = EndorPresentation(title="Endor Energia")
deck.add_cover(subtitle="Investor Update", date="Q1/2026")

deck.add_section_divider("Tração", number=1)
deck.add_kpi_slide(title="Indicadores Q1/2026", kpis=[
    {"label": "Receita anual", "value": "R$ 108 MM", "subtext": "ann. Q1×4"},
    {"label": "EBITDA margin", "value": "32,1%", "color": styles.BRAND.natureza},
])
deck.add_chart_slide(
    title="Trajetória de receita",
    chart_image=chart_growth,
    caption="CAGR 28,5% no período. Projeção 2026 baseada em pipeline contratado.",
)

deck.add_closing(text="Obrigado.", contact="ri@endor.energia")
deck.save("investor_deck_q1_2026.pptx")
```

### Receita 3: Relatório operacional mensal (estilo Luz Imperial)

```python
from endor_docs import EndorPresentation, styles, charts

# Charts
chart_consumo = charts.bar_chart(
    categories=["mai/25", "jun/25", ..., "mar/26"],  # últimos 11 meses
    values=[126, 158, ..., 198],
    out_path="/tmp/consumo.png",
    ylabel="MWh",
)

deck = EndorPresentation(title="Luz Imperial")
deck.add_cover(
    subtitle="Relatório Mensal — Março 2026",
    date="Abril 2026",
    metadata={
        "Contrato": "PPP 27/2023",
        "Emissão": "Abril 2026",
        "Destinatário": "Prefeitura de Vassouras",
    },
)

deck.add_section_divider("Sumário Executivo", number=1)
deck.add_kpi_slide(title="Visão geral", kpis=[
    {"label": "Atendimentos", "value": 147, "subtext": "em campo"},
    {"label": "Solicitações", "value": 67, "subtext": "abertas", "color": styles.BRAND.por_do_sol},
    {"label": "SLA", "value": "100,0%", "subtext": "atraso: 0,0%", "color": styles.BRAND.natureza},
    {"label": "Consumo", "value": "198 MWh", "subtext": "+6,3%", "color": styles.BRAND.terra},
])

deck.add_section_divider("Operação", number=2)
deck.add_chart_slide(
    title="Consumo de energia",
    chart_image=chart_consumo,
    caption="Fatura Light. 198 MWh em março (+6,3% vs fev). 7.072 pontos no parque (96,5% LED).",
)

deck.add_closing(text="Permanecemos à disposição.", contact="0800 006 1740")
deck.save("luz_imperial_mar2026.pptx")
```

**Quando seguir esta receita:** qualquer relatório mensal das concessionárias.
Modelo de referência completo em `examples/presentations/project_status_example.pptx`.

### Receita 4: Modelo financeiro

```python
from endor_docs import EndorWorkbook, styles

wb = EndorWorkbook(title="Modelo Financeiro — [Projeto]")
wb.add_cover(
    subtitle="[Tipo de projeto]",
    metadata={"Versão": "v1.0", "Período": "10 anos"},
)

prem = wb.add_sheet("Premissas")
prem.column_dimensions["B"].width = 35
prem.column_dimensions["C"].width = 18
wb.write_header_row(prem, row=4, headers=["Premissa", "Valor", "Unidade"], start_col=2)

# Dados
premissas = [
    ("Taxa de desconto (WACC)", 0.118, "% a.a."),
    ("CAPEX inicial",          18_400_000, "BRL"),
    ("OPEX anual",             4_200_000,  "BRL"),
    ("Receita ano 1",          9_800_000,  "BRL"),
    ("Prazo",                  10,         "anos"),
]
for i, (item, val, un) in enumerate(premissas, start=5):
    prem.cell(row=i, column=2, value=item)
    prem.cell(row=i, column=3, value=val)
    prem.cell(row=i, column=4, value=un)

wb.format_percent(prem, "C5:C5")
wb.format_brl(prem, "C6:C8", decimals=False)
wb.format_int(prem, "C9:C9")
wb.apply_zebra(prem, start_row=5, end_row=9, start_col=2, end_col=4)
wb.apply_table_borders(prem, start_row=5, end_row=9, start_col=2, end_col=4)

# Named ranges — fórmulas legíveis em outras abas
wb.define_name("wacc", prem, "$C$5")
wb.define_name("capex_inicial", prem, "$C$6")

wb.save("modelo.xlsx")
```

### Receita 5: Dashboard

```python
from endor_docs import EndorWorkbook, styles

wb = EndorWorkbook(title="Dashboard — [Período]")
wb.add_cover(subtitle="[Contexto]", metadata={"Atualização": "[Data]"})

dash = wb.add_sheet("Dashboard")
dash.cell(row=2, column=2, value="[TÍTULO]").font = _h1()  # ver helper

wb.add_kpi_block(dash, start_row=4, kpis=[
    {"label": "[KPI 1]", "value": "[X]", "subtext": "[ctx]"},
    {"label": "[KPI 2]", "value": "[X]", "subtext": "[ctx]", "color": styles.BRAND.natureza},
    {"label": "[KPI 3]", "value": "[X]", "color": styles.BRAND.por_do_sol},
])

wb.write_header_row(dash, row=12, headers=["Item", "Atual", "Anterior"], start_col=2)
# ... preencher linhas ...
wb.apply_zebra(dash, start_row=13, end_row=20, start_col=2, end_col=4)

wb.save("dashboard.xlsx")

def _h1():
    from openpyxl.styles import Font
    return Font(name=styles.FONTS.document, size=styles.SIZES.h1,
                bold=True, color=styles.BRAND.endor.argb)
```

---

## QUANDO USAR CADA TEMPLATE / EXEMPLO

| Caso de uso | Template | Exemplo (referência) |
|--|--|--|
| Apresentação interna, all-hands, kick-off | `templates/pptx/endor_corporate_template.pptx` | `examples/presentations/board_report_example.pptx` |
| Pitch investidor, captação, conselho | `templates/pptx/endor_investor_deck_template.pptx` | `examples/presentations/investor_deck_example.pptx` |
| Relatório mensal de concessão para prefeitura | `templates/pptx/endor_project_report_template.pptx` | `examples/presentations/project_status_example.pptx` |
| Modelo financeiro de concessão | `templates/xlsx/endor_financial_model_template.xlsx` | `examples/spreadsheets/financial_model_example.xlsx` |
| Dashboard de KPI mensal | `templates/xlsx/endor_dashboard_template.xlsx` | `examples/spreadsheets/kpi_dashboard_example.xlsx` |
| Detalhamento operacional de concessão | `templates/xlsx/endor_operational_report_template.xlsx` | `examples/spreadsheets/concession_model_example.xlsx` |

Para abrir um exemplo e copiar a estrutura de código, ver
`scripts/build_examples.py` — cada função `build_*_example` é uma receita
pronta.

---

## PALETA DE CORES — CHEAT SHEET

```python
from endor_docs import styles

# Brand (5 cores institucionais — do guia oficial set/2023)
styles.BRAND.endor       # #0A1A5C  — institucional principal
styles.BRAND.terra       # #0083CA  — azul claro, destaque, h2
styles.BRAND.por_do_sol  # #6C3F99  — roxo, social/comunitário
styles.BRAND.natureza    # #00718A  — teal, ambiental, success
styles.BRAND.tech        # #858A9E  — cinza, dados técnicos

# Neutros (gray-50 a gray-900, derivado de Tech)
styles.NEUTRAL.gray_50   # fundo de card
styles.NEUTRAL.gray_200  # divisores
styles.NEUTRAL.gray_600  # texto secundário
styles.NEUTRAL.gray_800  # texto principal
styles.NEUTRAL.white
styles.NEUTRAL.black

# Semânticas
styles.SEMANTIC.success  # = natureza  → OK, no prazo
styles.SEMANTIC.info     # = terra     → neutro positivo
styles.SEMANTIC.warning  # âmbar       → atenção
styles.SEMANTIC.error    # vermelho    → falha

# Cada cor tem:
c = styles.BRAND.endor
c.hex          # "#0A1A5C"
c.rgb          # (10, 26, 92)
c.argb         # "FF0A1A5C"  (openpyxl)
c.as_pptx()    # RGBColor(10, 26, 92)  (python-pptx)
c.as_matplotlib()  # "#0A1A5C"
```

---

## WORKFLOW PADRÃO

Para qualquer task de "gerar um artefato X":

1. **Identifique o tipo** (apresentação? planilha? dashboard?)
2. **Escolha o builder/receita** acima
3. **Olhe o exemplo mais próximo** em `examples/`
4. **Gere os charts antes** (se for apresentação) — `endor_docs.charts.*`
5. **Construa o objeto** (`EndorPresentation` ou `EndorWorkbook`)
6. **Salve com `.save(path)`**
7. **Valide visualmente** se for entrega final (converter pra PDF e olhar)

Para validação visual:
```bash
soffice --headless --convert-to pdf --outdir /tmp/check output.pptx
```

---

## ERROS COMUNS A EVITAR

### Erro: Hardcode de cor
❌ `cell.font = Font(color="0A1A5C")`
✅ `cell.font = Font(color=styles.BRAND.endor.argb)`

### Erro: Hardcode de fonte
❌ `Font(name="Calibri")`
✅ `Font(name=styles.FONTS.document)`

### Erro: Editar template manualmente
❌ Abrir `templates/pptx/endor_corporate_template.pptx` no PowerPoint e salvar
✅ Editar `scripts/build_templates.py` e re-rodar

### Erro: Mais de 4 KPIs em uma linha
❌ `deck.add_kpi_slide(title=..., kpis=[k1, k2, k3, k4, k5, k6])`
✅ Distribuir em 2 slides KPI, ou usar uma tabela

### Erro: Pizza com 8 categorias
❌ Pizza pra distribuição categórica grande
✅ `charts.horizontal_bar_chart` — barras horizontais com nomes longos

### Erro: Texto longo em KPI value
❌ `{"label": "Atendimentos", "value": "147 em campo no mês de março"}`
✅ `{"label": "Atendimentos", "value": "147", "subtext": "em campo no mês"}`

### Erro: Builder importado errado
❌ `from pptx import Presentation; deck = Presentation()`
✅ `from endor_docs import EndorPresentation; deck = EndorPresentation(...)`

### Erro: Format string ad-hoc
❌ `cell.number_format = "R$ 0.00"`
✅ `wb.format_brl(ws, "B2:B20")`

### Erro: Logo modificado
❌ Esticar, recolorir, rotar, traçar o logo
✅ Usar sempre os arquivos em `assets/logos/`

### Erro: Calibri fora de documentos
❌ Usar Calibri em peças impressas finais
✅ Calibri em .pptx/.xlsx/.docx | Avenir Next em peças finais

### Erro: Fundos não-permitidos
❌ Logo sobre imagem com alta densidade visual
✅ Posicionar em áreas limpas (ver `brand/visual_rules.md` §2)

---

## INVENTÁRIO

```
brand/
  Endor_Guia_Identidade_Visual.pdf      Mestre oficial (set/2023). NÃO EDITAR.
  endor_design_system.md                Visão geral em PT-BR
  visual_rules.md                       REGRAS DURAS (ler antes de qualquer task)
  reference/Relatorio_LuzImperial...pdf Referência de estilo (designer interno)

tokens/
  endor.tokens.json                     Fonte da verdade — W3C Design Tokens

assets/logos/
  {fundo-branco,fundo-azul,monocromatica}/
    {energia, concessionarias/*, submarcas, simbolo}/
      {digital, vetor, simplificada}/   PDF, AI, PNG, JPG

src/endor_docs/
  styles.py                             Carrega tokens. SINGLE SOURCE OF TRUTH.
  charts.py                             Fábricas de gráficos matplotlib
  ppt_builder.py                        EndorPresentation
  xlsx_builder.py                       EndorWorkbook

templates/{pptx,xlsx}/                  6 templates gerados (NÃO editar manualmente)

examples/
  presentations/                        3 PPTX preenchidos (referência)
  spreadsheets/                         3 XLSX preenchidos (referência)
  _charts/                              PNGs intermediários dos charts (regeneráveis)

scripts/
  organize_assets.py                    Re-organização inicial dos assets (one-shot)
  build_templates.py                    Gera os 6 templates
  build_examples.py                     Gera os 6 exemplos

docs/
  powerpoint_guidelines.md              Guia humano de PPT
  spreadsheet_guidelines.md             Guia humano de XLSX
  chart_guidelines.md                   Guia humano de gráficos
  examples_to_follow.md                 Referência cruzada dos exemplos
```

---

## SE ALGO PARECE AMBÍGUO

1. Leia `brand/visual_rules.md` — regras duras
2. Leia o exemplo mais próximo em `examples/`
3. Olhe `brand/Endor_Guia_Identidade_Visual.pdf` (páginas relevantes)
4. **Não invente**: pergunte ao humano antes de fazer escolha não-prescrita

Se a task pede algo que conflita com este arquivo (ex: "use a fonte X"
quando X não é Calibri nem Avenir Next), avise sobre o conflito e
sugira alternativa dentro do sistema.

---

## VERSÃO

Design system v0.1.0 (Mai/2026). Tokens em `tokens/endor.tokens.json`
`$metadata.version`. Versões 0.x podem ter breaking changes — confira
o git log antes de assumir que uma API existe.
