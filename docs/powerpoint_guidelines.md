# PowerPoint — Diretrizes de Uso

Guia para criar apresentações Endor a partir dos templates ou builders Python.

## Qual template usar?

| Template | Quando usar | Não usar para |
|--|--|--|
| `templates/pptx/endor_corporate_template.pptx` | Comunicação interna, all-hands, atualizações de área, kick-offs. Conteúdo institucional genérico. | Materiais para fora da empresa, decks de investidor (use o específico). |
| `templates/pptx/endor_investor_deck_template.pptx` | Pitch para investidores, conselho, board meetings, materiais para captação. Estrutura otimizada para narrativa "quem somos → tração → pedido". | Operacional, técnico, treinamento. |
| `templates/pptx/endor_project_report_template.pptx` | Relatórios mensais de operação, status reports de concessões, reporting para poder concedente (estilo Luz Imperial). | Pitch externo, comunicação corporativa ampla. |

## Anatomia de um slide Endor

Todo slide gerado segue esta estrutura:

```
┌──────────────────────────────────────────────┐
│ [faixa gradient azul→roxo no topo]           │
│                                              │
│  [logo Endor]                                │
│                                              │
│  Título do slide  (h1, azul Endor, bold)    │
│  Subtítulo opcional (h2, azul Terra)        │
│                                              │
│  [conteúdo principal: bullets, KPIs, chart]  │
│                                              │
│                                              │
│  Endor Energia                  Página X/Y  │
└──────────────────────────────────────────────┘
```

Slides de **divisor de seção** e **closing** quebram esse padrão — fundo
azul institucional, sem footer.

## Tipos de slide disponíveis

### Capa (`add_cover`)
- Lado esquerdo azul institucional, lado direito reserva para imagem/conteúdo
- Logo no topo, título grande no meio, subtítulo, data, metadados em rodapé
- Use UMA capa por apresentação

### Divisor de seção (`add_section_divider`)
- Slide cheio azul Endor
- Número da seção em azul Terra grande (canto sup esq)
- Nome da seção em branco grande
- Use entre blocos lógicos (3–6 seções por deck)

### Slide de conteúdo (`add_content_slide`)
- Título + opcional subtítulo + bullets ou body livre
- Limite: **5 bullets por slide**. Se ultrapassar, divida em 2 slides
- Cada bullet ≤ 1 linha. Frase telegráfica > parágrafo

### Slide de KPI (`add_kpi_slide`)
- Até **4 cards** lado a lado
- Cada card: label (caixa alta pequena), valor grande, subtexto
- Use cores diferentes pra categorizar (default Terra, ou Natureza/Pôr do Sol/Tech)

### Slide de gráfico (`add_chart_slide`)
- Título + uma imagem de gráfico (gerada por `endor_docs.charts`)
- Caption pequeno opcional embaixo
- Não tente colocar 2 charts no mesmo slide — gera ruído

### Closing (`add_closing`)
- Fundo azul, logo grande, mensagem de encerramento
- Opcional: linha de contato (e-mail/telefone/site)

## Estrutura recomendada por tipo de deck

### Corporativo / interno (8–12 slides)
1. Capa
2. Visão geral / agenda
3. (Conteúdo: 4–6 slides distribuídos em 1–2 seções)
4. Próximos passos / decisões
5. Closing

### Investor deck (10–15 slides)
1. Capa
2. Section "Quem somos" → 1 slide
3. Section "Mercado" → 1 chart + 1 slide
4. Section "Tração" → 1 KPI + 1 chart
5. Section "Próximos passos" → 1 slide
6. Closing

### Project report mensal (10–14 slides, formato Luz Imperial)
1. Capa com contrato/emissão/destinatário
2. Section "Sumário Executivo"
3. Slide de KPIs (4 indicadores principais)
4. Slide de fatos relevantes (bullets)
5. Section "Operacional"
6. Charts (2–4 slides)
7. Section "Encerramento"
8. Closing

## Como gerar via código

```python
from endor_docs import EndorPresentation
from endor_docs import charts, styles

# 1. Cria o deck
deck = EndorPresentation(title="Endor Energia — Atualização Q1/2026")
deck.add_cover(subtitle="Conselho", date="Abril 2026")

# 2. Section + KPIs
deck.add_section_divider("Resultados", number=1)
deck.add_kpi_slide(
    title="Indicadores Q1",
    kpis=[
        {"label": "Receita", "value": "R$ 28,4 MM", "subtext": "+21% YoY"},
        {"label": "EBITDA", "value": "32,1%", "subtext": "+3,4 p.p.",
         "color": styles.BRAND.natureza},
    ],
)

# 3. Chart slide (precisa gerar o PNG antes)
chart_png = charts.line_chart(
    x=["2022", "2023", "2024", "2025"],
    y=[42.1, 58.7, 71.2, 89.5],
    out_path="/tmp/receita.png",
    ylabel="R$ MM",
)
deck.add_chart_slide(
    title="Trajetória de receita",
    chart_image=chart_png,
    caption="CAGR 28,5% no período.",
)

# 4. Fim
deck.add_closing(text="Obrigado.", contact="ri@endor.energia")
deck.save("output/q1_2026.pptx")
```

## Como gerar a partir do template (sem código)

1. Copie o template:
   ```bash
   cp templates/pptx/endor_corporate_template.pptx meu_deck.pptx
   ```
2. Abra no PowerPoint/Keynote/LibreOffice
3. Substitua os placeholders `[Título]`, `[Subtítulo]`, etc. pelos textos reais
4. **Não altere** cores, fontes, logo ou layout — apenas o conteúdo textual
5. Adicione/remova slides usando os layouts existentes

> Para mudanças estruturais (novo tipo de slide, nova paleta), edite o
> **builder Python** e re-gere o template — não edite manualmente.

## Do's e Don'ts

### ✅ Faça
- Um título dominante por slide
- Use ≤ 5 bullets por slide
- Capitalize palavras-chave com bold (sparingly)
- Use as cores secundárias para categorizar (cada cor = um contexto)
- Comece cada bullet com verbo ou número
- Inclua caption nos gráficos explicando o "so what"

### ❌ Não faça
- Mais de 4 KPIs em um único slide (cards ficam pequenos demais)
- Mistura de fontes (use só Calibri ou só Avenir Next, nunca ambas)
- Texto sobre imagens sem máscara/fundo
- Cores fora da paleta (consulte `tokens/endor.tokens.json`)
- Bullets de mais de 2 linhas (se precisar de mais, é body, não bullet)
- Edição manual em templates que serão regenerados via script

## Referências

- Exemplo completo de project report: `examples/presentations/project_status_example.pptx`
- Exemplo de investor deck: `examples/presentations/investor_deck_example.pptx`
- Exemplo de board report: `examples/presentations/board_report_example.pptx`
- API dos builders: `src/endor_docs/ppt_builder.py`
- Regras visuais inegociáveis: `brand/visual_rules.md`
