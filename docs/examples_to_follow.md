# Exemplos a Seguir

Referência cruzada dos 6 exemplos canônicos em `examples/`. Quando estiver
em dúvida de "como devo estruturar X?", abra o exemplo correspondente.

> **Dados em exemplos são fictícios** mas calibrados em benchmarks reais
> do setor (Luz Imperial Mar/2026 é a referência operacional, valores de
> receita/EBITDA são plausíveis para o estágio descrito). Não usar como
> base para comunicação externa.

---

## Apresentações

### `examples/presentations/project_status_example.pptx`

**Caso:** Relatório mensal operacional de uma concessionária para o
poder concedente.

**Quando seguir este modelo:**
- Reporting mensal de Luz Imperial, Luz do Vale, Miguel Pereira Luz
- Relatórios para prefeituras (poder concedente)
- Qualquer artefato exigido pelo §1.7.5.2 do Anexo 4 do contrato PPP

**Estrutura:**
1. Capa (contrato, emissão, destinatário em metadados)
2. Section divider "Sumário Executivo"
3. KPI slide com 4 indicadores principais (atendimentos, solicitações, SLA, consumo)
4. Slide de "Fatos relevantes" em bullets
5. Section "Operação"
6. 3 chart slides (consumo, origem das solicitações, motivos)
7. Section "Encerramento"
8. Closing com contato

**Builder:** `scripts/build_examples.py::build_project_status_example`

**Inspirado em:** `brand/reference/Relatorio_LuzImperial_Mar2026.pdf` —
peça original feita por designer interno. Os templates Endor seguem
visualmente esse padrão.

---

### `examples/presentations/board_report_example.pptx`

**Caso:** Resultados consolidados das 3 concessões para o Conselho.

**Quando seguir este modelo:**
- Reuniões trimestrais/semestrais do conselho
- Apresentações para acionistas
- Visões consolidadas (cross-concessão)

**Estrutura:**
1. Capa com período YTD
2. Section "Resultados Consolidados" → KPIs financeiros + chart de receita
3. Section "Operacional" → KPIs operacionais + chart por concessionária
4. Section "Próximos Passos" → bullets de pipeline e prioridades
5. Closing

**Decisões de estilo a observar:**
- Mistura de cores secundárias nos KPIs (cada cor categoriza uma dimensão)
- Charts com caption explicando o "so what"
- Bullets curtos (≤1 linha) com fatos diretos

---

### `examples/presentations/investor_deck_example.pptx`

**Caso:** Pitch para investidor / captação Série B.

**Quando seguir este modelo:**
- Investor updates (trimestrais/anuais)
- Decks de captação
- Apresentações para parceiros estratégicos

**Estrutura:**
1. Capa
2. Section "Quem somos" → 1 slide com bullets diretos
3. Section "Mercado e Tração":
   - Chart de TAM
   - KPIs principais
   - Chart de crescimento
4. Section "Próximos passos" → pedido + uso dos recursos + métricas-alvo
5. Closing com contato

**Decisões de estilo a observar:**
- Narrativa "quem somos → tração → pedido"
- Métricas com contexto temporal (sempre comparar com período anterior)
- Charts com projeções marcadas como `e` (2026e, 2027e)

---

## Planilhas

### `examples/spreadsheets/financial_model_example.xlsx`

**Caso:** Modelo financeiro de concessão — 10 anos, com VPL/TIR/Payback.

**Quando seguir este modelo:**
- Avaliação de novas concessões (decisão de participar de edital)
- Refinanciamento ou venda de concessão existente
- Cálculo de bid em concorrências

**Abas:**
- `Capa`
- `Premissas` (com named ranges: `wacc`, `inflacao`, `capex_inicial`, `receita_ano1`)
- `DRE` — 10 anos projetados a partir das premissas
- `Fluxo de Caixa` — CAPEX ano 0 + EBITDA - impostos
- `Resumo` — KPIs VPL/TIR/Payback calculados a partir do FC

**Decisões de estilo a observar:**
- Named ranges em vez de referências absolutas — facilita auditoria
- Cada bloco com header azul Endor + zebra + linha divisória inferior
- Premissas separadas em aba dedicada — mudança em UM lugar propaga
- VPL, TIR e Payback como KPI cards no Resumo

---

### `examples/spreadsheets/kpi_dashboard_example.xlsx`

**Caso:** Dashboard consolidado mensal das 3 concessionárias.

**Quando seguir este modelo:**
- Dashboard executivo mensal
- Acompanhamento de SLAs e indicadores operacionais
- Reporting interno para diretoria

**Abas:**
- `Capa`
- `Dashboard` — KPIs no topo + tabela por concessionária + tabela de tendência

**Decisões de estilo a observar:**
- 4 KPIs em linha (atendimentos, solicitações, SLA, consumo)
- Tabela por dimensão (concessionária) abaixo
- Tabela de tendência (3 meses) com variação calculada
- Larguras de coluna padronizadas em 12

---

### `examples/spreadsheets/concession_model_example.xlsx`

**Caso:** Detalhamento operacional de uma concessão específica.

**Quando seguir este modelo:**
- Reporting detalhado de uma única concessão
- Anexo técnico ao relatório PPT mensal
- Análise causa-raiz de operação

**Abas:**
- `Capa` (contrato, vigência, concessionária)
- `Contrato` — parâmetros contratuais (números, datas, SLAs)
- `Operacional Mar26` — KPIs do mês + tabela por motivo
- `Materiais` — movimentação de materiais (aplicados, retirados, saldo)

**Decisões de estilo a observar:**
- Aba `Contrato` separa parâmetros estáticos dos operacionais
- KPI block aparece em aba específica do mês
- Tabela de motivos com % calculado (não só absolutos)

---

## Quando criar um novo exemplo

Crie um novo exemplo se aparecer um caso de uso recorrente que não está
coberto. Critérios:

1. **Recorrência**: o caso vai aparecer pelo menos 3× por ano
2. **Diferença substancial**: estrutura diferente dos exemplos existentes
3. **Aprovação**: equipe de marca + responsável do design system

Como adicionar:
1. Escreva um builder em `scripts/build_examples.py` (`build_<nome>_example`)
2. Adicione na lista `main()` para regeneração
3. Documente aqui em `examples_to_follow.md`
4. Commit referenciando o caso de uso

## Como regenerar todos os exemplos

```bash
python scripts/build_examples.py
```

Re-roda os 6 builders, sobrescreve os `.pptx`/`.xlsx` em `examples/` e os
charts intermediários em `examples/_charts/`. Commite as mudanças junto
com o que motivou a regeneração (mudança de tokens, novo builder, etc.).
