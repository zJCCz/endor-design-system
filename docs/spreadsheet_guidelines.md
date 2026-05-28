# Planilhas Excel — Diretrizes de Uso

Guia para criar planilhas Endor a partir dos templates ou builders Python.

## Qual template usar?

| Template | Quando usar | Estrutura |
|--|--|--|
| `templates/xlsx/endor_financial_model_template.xlsx` | Modelos financeiros de concessão, valuation de projetos, análise de TIR/VPL/payback. Tem named ranges (`wacc`, `capex_inicial`, etc.) prontos para fórmulas. | Capa · Premissas · DRE · Fluxo de Caixa · Resumo |
| `templates/xlsx/endor_dashboard_template.xlsx` | Dashboards operacionais e gerenciais. KPI cards + tabela detalhada. Atualização periódica. | Capa · Dashboard (KPIs + tabelas) |
| `templates/xlsx/endor_operational_report_template.xlsx` | Acompanhamento operacional mensal (estilo Luz Imperial). Reporting para poder concedente. | Capa · Resumo do mês · Atendimentos · Materiais |

## Convenções globais

### Visual

- Aba **Capa** sempre primeiro, fundo azul Endor, sem gridlines
- Demais abas com gridlines desligadas (`sheet_view.showGridLines = False`)
- Headers de tabela em azul Endor (`color.brand.endor`) com texto branco
- Linhas pares com fundo cinza-50 (`color.neutral.gray-50`) — zebra sutil
- Divisor inferior cinza-200 em cada linha de tabela
- Fonte: **Calibri** em todo o workbook
- Tamanhos: H1 28pt (título de página), H2 18pt (título de bloco), body 10pt

### Formato numérico brasileiro

Use os helpers `format_*` do `EndorWorkbook`, não format strings manuais:

```python
wb.format_brl(ws, "B2:B20")        # R$ X.XXX,XX
wb.format_brl(ws, "B2:B20", decimals=False)  # R$ X.XXX (inteiro)
wb.format_int(ws, "C2:C20")        # X.XXX
wb.format_decimal(ws, "D2:D20")    # X.XXX,XX
wb.format_percent(ws, "E2:E20")    # X,X%
wb.format_percent(ws, "E2:E20", decimals=2)  # X,XX%
wb.format_kwh(ws, "F2:F20")        # X.XXX kWh
wb.format_mwh(ws, "F2:F20")        # X.XXX MWh
wb.format_date(ws, "G2:G20")       # DD/MM/AAAA
```

Os format codes usam padrão Excel-locale. Em Excel com locale pt-BR
renderizam com `.` como separador de milhar e `,` como decimal —
correto para o Brasil. Em locale US renderizam com `,` e `.` —
mas o número subjacente é idêntico.

### Layout de células

- Coluna A: largura 2 (margem visual esquerda)
- Coluna B em diante: conteúdo
- Headers de tabela: altura de linha 24
- KPI values (`add_kpi_block`): altura de linha 40
- Texto de título (h1/h2): nunca em célula mesclada — use `font` na célula raiz

### Named ranges (modelos financeiros)

Use `define_name()` para inputs reutilizáveis:

```python
wb.define_name("wacc", premissas_ws, "$C$5")
wb.define_name("capex_inicial", premissas_ws, "$C$7")

# Depois, em outras abas:
dre_ws["C5"] = "=receita_ano1*(1+crescimento_receita)^A5"
```

Vantagens:
- Fórmulas legíveis (`=wacc*100` em vez de `=Premissas!$C$5*100`)
- Auditoria mais fácil pelo poder concedente
- Mudança de premissa em UM lugar atualiza todo o modelo

## Estrutura recomendada por tipo

### Modelo financeiro de concessão

```
Capa            — Identificação do projeto (CONTRATO, CONCESSIONÁRIA, PERÍODO)
Premissas       — Inputs com named ranges: WACC, CAPEX, OPEX base, receita ano 1,
                   crescimento, prazo, alíquota IR
DRE             — Receita bruta → Receita líquida → EBITDA → EBIT → Lucro líquido,
                   por ano (até prazo contratual)
Fluxo de Caixa  — CAPEX (ano 0) + EBITDA - impostos por ano. Acumulado pra payback.
Resumo          — VPL, TIR, Payback como KPI cards
```

### Dashboard

```
Capa     — período de referência, atualização, frequência
Dashboard — KPI cards (até 4) + tabela detalhada por dimensão + tendência
```

### Relatório operacional

```
Capa           — contrato, concessão, município
Resumo do mês  — KPI cards principais
Atendimentos   — Tabela motivos × quantidade × %
Materiais      — Tabela família × aplicados × retirados × saldo
```

## Como gerar via código

```python
from endor_docs import EndorWorkbook, styles

wb = EndorWorkbook(title="Modelo — Luz Imperial 2026")
wb.add_cover(
    subtitle="PPP de Iluminação Pública",
    metadata={"Contrato": "27/2023", "Período": "10 anos"},
)

prem = wb.add_sheet("Premissas")
prem.column_dimensions["B"].width = 35
wb.write_header_row(prem, row=4, headers=["Premissa", "Valor", "Un."], start_col=2)

prem.cell(row=5, column=2, value="WACC")
prem.cell(row=5, column=3, value=0.118)
prem.cell(row=5, column=4, value="% a.a.")
wb.format_percent(prem, "C5:C5")
wb.apply_zebra(prem, start_row=5, end_row=10, start_col=2, end_col=4)
wb.define_name("wacc", prem, "$C$5")

wb.save("modelo.xlsx")
```

## Como gerar a partir do template (sem código)

1. Copie o template:
   ```bash
   cp templates/xlsx/endor_financial_model_template.xlsx meu_modelo.xlsx
   ```
2. Abra no Excel
3. Preencha as células com `[Placeholder]`
4. Mantenha named ranges intactos — eles são referenciados em outras abas
5. **Não altere** cabeçalhos, cores, layout — só conteúdo

## Do's e Don'ts

### ✅ Faça
- Use named ranges para inputs importantes
- Mantenha 1 aba = 1 propósito (não misture premissas com outputs)
- Insira notas técnicas em texto (não como comments do Excel — não exportam)
- Use os formatadores BR para qualquer número monetário ou percentual
- Numere abas que tenham ordem lógica ("1. Premissas", "2. DRE", "3. FC")

### ❌ Não faça
- Format strings ad-hoc (`'R$ 0.00'`) — use `wb.format_brl()`
- Cores fora da paleta — use `BRAND` e `NEUTRAL` do `styles`
- Mesclar (`merge_cells`) sem necessidade — quebra filtros e ordenação
- Mais de 4 KPI cards em uma linha — fica apertado em A4 retrato impresso
- Editar manualmente um arquivo que será re-gerado por script

## Referências

- Exemplo de modelo financeiro: `examples/spreadsheets/financial_model_example.xlsx`
- Exemplo de dashboard: `examples/spreadsheets/kpi_dashboard_example.xlsx`
- Exemplo de modelo de concessão: `examples/spreadsheets/concession_model_example.xlsx`
- API do builder: `src/endor_docs/xlsx_builder.py`
- Regras visuais inegociáveis: `brand/visual_rules.md`
