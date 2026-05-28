"""
Gera os exemplos canônicos do design system Endor com DADOS FICTÍCIOS mas
PLAUSÍVEIS para o setor de energia (iluminação pública, concessões PPP,
modelo financeiro de concessão).

Roda: ``python scripts/build_examples.py``

Saída:
  examples/presentations/
    board_report_example.pptx
    investor_deck_example.pptx
    project_status_example.pptx
  examples/spreadsheets/
    financial_model_example.xlsx
    kpi_dashboard_example.xlsx
    concession_model_example.xlsx

Os números são CALIBRADOS para serem realistas (a partir da referência
Luz Imperial Mar/2026 e benchmarks do setor de IP no Brasil), MAS NÃO
REPRESENTAM DADOS OPERACIONAIS REAIS DA ENDOR ENERGIA. Não usar como base
para decisões ou comunicação externa.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from endor_docs import EndorPresentation, EndorWorkbook, styles
from endor_docs import charts

REPO = Path(__file__).resolve().parent.parent
PPTX_DIR = REPO / "examples" / "presentations"
XLSX_DIR = REPO / "examples" / "spreadsheets"
CHART_DIR = REPO / "examples" / "_charts"  # imagens intermediárias, regeneráveis


# ---------------------------------------------------------------------------
# Exemplos PPTX
# ---------------------------------------------------------------------------


def build_board_report_example() -> Path:
    """Relatório para o Conselho — visão consolidada da operação."""
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    # Charts
    chart_receita = charts.line_chart(
        x=["2022", "2023", "2024", "2025", "2026e"],
        y=[42.1, 58.7, 71.2, 89.5, 108.3],
        out_path=CHART_DIR / "board_receita.png",
        ylabel="R$ milhões",
    )
    chart_atendimentos = charts.grouped_bar_chart(
        categories=["Luz Imperial", "Luz do Vale", "Miguel Pereira"],
        series={
            "Q4/2025": [142, 89, 67],
            "Q1/2026": [147, 95, 71],
        },
        out_path=CHART_DIR / "board_atendimentos.png",
        ylabel="Atendimentos/mês",
    )

    deck = EndorPresentation(title="Endor Energia")
    deck.add_cover(
        subtitle="Reunião do Conselho — Resultados Q1/2026",
        date="Abril de 2026",
        metadata={"Período": "Jan–Mar 2026", "Próxima reunião": "Jul 2026"},
    )

    deck.add_section_divider("1. Resultados Consolidados", number=1)
    deck.add_kpi_slide(
        title="Indicadores financeiros — YTD",
        kpis=[
            {"label": "Receita YTD", "value": "R$ 28,4 MM", "subtext": "+21% vs Q1/2025"},
            {"label": "EBITDA Margin", "value": "32,1%", "subtext": "+3,4 p.p.", "color": styles.BRAND.natureza},
            {"label": "Caixa", "value": "R$ 47 MM", "subtext": "+18% YoY", "color": styles.BRAND.por_do_sol},
            {"label": "ROIC", "value": "14,2%", "subtext": "vs 12,8% Q1/25", "color": styles.BRAND.terra},
        ],
    )
    deck.add_chart_slide(
        title="Trajetória de receita 2022–2026e",
        chart_image=chart_receita,
        caption="Inclui projeção 2026 baseada em pipeline contratado. CAGR 2022–2025: 28,5%.",
    )

    deck.add_section_divider("2. Operacional", number=2)
    deck.add_kpi_slide(
        title="Operação consolidada Q1/2026",
        kpis=[
            {"label": "Atendimentos", "value": "939", "subtext": "+8% QoQ"},
            {"label": "SLA no prazo", "value": "98,7%", "subtext": "meta: ≥95%", "color": styles.BRAND.natureza},
            {"label": "% LED", "value": "94,2%", "subtext": "+2,1 p.p.", "color": styles.BRAND.por_do_sol},
            {"label": "Consumo", "value": "612 MWh", "subtext": "−4,8% vs Q4/25", "color": styles.BRAND.terra},
        ],
    )
    deck.add_chart_slide(
        title="Atendimentos por concessionária",
        chart_image=chart_atendimentos,
        caption="Luz Imperial mantém volume mais alto — base instalada maior. Crescimento consistente nos três contratos.",
    )

    deck.add_section_divider("3. Próximos Passos", number=3)
    deck.add_content_slide(
        title="Pipeline e prioridades 2026",
        bullets=[
            "Conclusão da modernização LED em Vassouras até Set/26 (96,5% → 100%)",
            "Participação em 2 novos editais de PPP (Sudeste) — decisão Q3",
            "Estruturação de submarca Endor Geração Distribuída para portfólio FV",
            "Captação Série B em discussão preliminar — Q4 alvo",
        ],
    )

    deck.add_closing(text="Obrigado.", contact="ri@endor.energia")

    out = PPTX_DIR / "board_report_example.pptx"
    return deck.save(out)


def build_investor_deck_example() -> Path:
    """Investor Update Q1/2026 — pitch para investidor."""
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    chart_market = charts.bar_chart(
        categories=["RJ", "MG", "SP", "ES", "PR"],
        values=[1.8, 2.4, 5.2, 0.9, 1.6],
        out_path=CHART_DIR / "investor_market.png",
        ylabel="R$ bilhões",
    )
    chart_growth = charts.line_chart(
        x=["2021", "2022", "2023", "2024", "2025", "2026e", "2027e"],
        y=[18, 42, 58, 71, 89, 108, 138],
        out_path=CHART_DIR / "investor_growth.png",
        ylabel="R$ milhões",
    )

    deck = EndorPresentation(title="Endor Energia")
    deck.add_cover(
        subtitle="Investor Update — Q1/2026",
        date="Abril 2026",
    )

    deck.add_section_divider("Quem somos", number=1)
    deck.add_content_slide(
        title="Endor Energia em 30 segundos",
        bullets=[
            "Concessionária de iluminação pública especializada em PPPs municipais",
            "3 concessões ativas no Sul Fluminense — 25.870 pontos sob operação",
            "94,2% do parque modernizado em tecnologia LED (vs. 78% benchmark setorial)",
            "Atende 320 mil habitantes em 3 municípios da região",
            "Tração: receita 5,1× em 4 anos. EBITDA margin de 32% no Q1/26",
        ],
    )

    deck.add_section_divider("Mercado e Tração", number=2)
    deck.add_chart_slide(
        title="Tamanho de mercado endereçável",
        chart_image=chart_market,
        caption="Apenas SE+S movimenta R$ 11,9 bi/ano em IP. Penetração de PPPs <15% — runway significativo.",
    )

    deck.add_kpi_slide(
        title="Indicadores Q1/2026",
        kpis=[
            {"label": "Receita anual", "value": "R$ 108 MM", "subtext": "ann. Q1×4"},
            {"label": "EBITDA margin", "value": "32,1%", "subtext": "vs 28,7% Q1/25", "color": styles.BRAND.natureza},
            {"label": "Concessões", "value": "3", "subtext": "+2 em pipeline", "color": styles.BRAND.por_do_sol},
            {"label": "Habitantes atendidos", "value": "320k", "subtext": "via 25.870 pontos", "color": styles.BRAND.terra},
        ],
    )

    deck.add_chart_slide(
        title="Trajetória de crescimento",
        chart_image=chart_growth,
        caption="CAGR 2022–2025: 28,5%. Projeção 2026e considera duas concessões em pipeline com decisão Q3.",
    )

    deck.add_section_divider("Próximos passos", number=3)
    deck.add_content_slide(
        title="O que estamos buscando",
        bullets=[
            "Captação Série B — R$ 80–120 MM",
            "Uso: aquisição de 2–3 concessões adicionais + CAPEX de modernização LED",
            "Timeline: due diligence Q2–Q3, fechamento Q4/2026",
            "Métricas-alvo 2028: receita R$ 250 MM, EBITDA margin >35%, 7 concessões ativas",
        ],
    )

    deck.add_closing(text="Obrigado.", contact="ri@endor.energia")

    out = PPTX_DIR / "investor_deck_example.pptx"
    return deck.save(out)


def build_project_status_example() -> Path:
    """Relatório operacional mensal — estilo Luz Imperial."""
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    chart_consumo = charts.bar_chart(
        categories=[
            "mai/25", "jun/25", "jul/25", "ago/25", "set/25", "out/25",
            "nov/25", "dez/25", "jan/26", "fev/26", "mar/26",
        ],
        values=[126, 158, 162, 159, 152, 154, 153, 144, 141, 183, 198],
        out_path=CHART_DIR / "luz_imperial_consumo.png",
        ylabel="MWh",
    )
    chart_origem = charts.horizontal_bar_chart(
        categories=["App", "Ronda própria", "Prefeitura", "Chatbot"],
        values=[24, 24, 18, 1],
        out_path=CHART_DIR / "luz_imperial_origem.png",
    )
    chart_motivos = charts.pie_chart(
        labels=["Manutenção corretiva", "MOD - Modernizado", "Conexão danif.", "LED danif.", "Outros"],
        values=[88, 12, 9, 8, 30],
        out_path=CHART_DIR / "luz_imperial_motivos.png",
    )

    deck = EndorPresentation(title="Luz Imperial")
    deck.add_cover(
        subtitle="Relatório Mensal de Atividades — Março 2026",
        date="Abril de 2026",
        metadata={
            "Contrato": "PPP 27/2023",
            "Emissão": "Abril 2026",
            "Destinatário": "Prefeitura de Vassouras",
        },
    )

    deck.add_section_divider("1. Sumário Executivo", number=1)
    deck.add_kpi_slide(
        title="Visão geral de março",
        kpis=[
            {"label": "Atendimentos", "value": "147", "subtext": "em campo, no mês"},
            {"label": "Solicitações", "value": "67", "subtext": "abertas no mês", "color": styles.BRAND.por_do_sol},
            {"label": "SLA no prazo", "value": "100,0%", "subtext": "atraso: 0,0%", "color": styles.BRAND.natureza},
            {"label": "Consumo", "value": "198 MWh", "subtext": "+6,3% vs fev/26", "color": styles.BRAND.terra},
        ],
    )
    deck.add_content_slide(
        title="Fatos relevantes do mês",
        bullets=[
            "Volume executado supera reativo em 2,2× — 78 atendimentos vinculados a protocolo + 69 sem origem definida",
            "App consolida-se como canal predominante — 36% das solicitações (24/67)",
            "Quatro causas concentram 80% dos atendimentos — manutenção corretiva lidera com 60%",
            "Execução 100% corretiva — baixa visibilidade de preventiva por ausência de coleta estruturada",
        ],
    )

    deck.add_section_divider("2. Operação", number=2)
    deck.add_chart_slide(
        title="Consumo de energia",
        chart_image=chart_consumo,
        caption="Fatura Light. 198 MWh em março, +6,3% vs mês anterior. 7.072 pontos no parque (96,5% LED).",
    )
    deck.add_chart_slide(
        title="Origem das solicitações",
        chart_image=chart_origem,
        caption="App e Ronda própria respondem juntos por 72% das aberturas. Chatbot ainda em adoção inicial.",
    )
    deck.add_chart_slide(
        title="Motivos identificados",
        chart_image=chart_motivos,
        caption="Manutenção corretiva (60%) lidera. Modernização (8,8%) e conexões danificadas (6,6%) completam o top 4.",
    )

    deck.add_section_divider("3. Encerramento", number=3)
    deck.add_closing(text="Permanecemos à disposição.", contact="0800 006 1740 — luzimperial.cidadeiluminada.com.br")

    out = PPTX_DIR / "project_status_example.pptx"
    return deck.save(out)


# ---------------------------------------------------------------------------
# Exemplos XLSX
# ---------------------------------------------------------------------------


def build_financial_model_example() -> Path:
    """Modelo financeiro de concessão — Luz Imperial / 10 anos."""
    wb = EndorWorkbook(title="Modelo Financeiro — Luz Imperial")
    wb.add_cover(
        subtitle="PPP de Iluminação Pública — Vassouras",
        metadata={"Versão": "v1.2", "Período": "2024–2033", "Concessão": "27/2023"},
    )

    # Premissas
    prem = wb.add_sheet("Premissas")
    prem.column_dimensions["B"].width = 38
    prem.column_dimensions["C"].width = 18
    prem.column_dimensions["D"].width = 14
    prem.cell(row=2, column=2, value="PREMISSAS DO MODELO").font = _h2()
    wb.write_header_row(prem, row=4, headers=["Premissa", "Valor", "Unidade"], start_col=2)
    premissas = [
        ("Taxa de desconto (WACC)", 0.118, "% a.a."),
        ("Inflação anual projetada", 0.045, "% a.a."),
        ("CAPEX total inicial (LED + sistemas)", 18_400_000, "BRL"),
        ("OPEX anual base", 4_200_000, "BRL"),
        ("Receita anual ano 1 (CAP IP)", 9_800_000, "BRL"),
        ("Crescimento receita a.a.", 0.06, "% a.a."),
        ("Prazo contratual", 10, "anos"),
        ("Imposto sobre lucro", 0.34, "%"),
    ]
    for i, (item, val, un) in enumerate(premissas, start=5):
        prem.cell(row=i, column=2, value=item)
        prem.cell(row=i, column=3, value=val)
        prem.cell(row=i, column=4, value=un)
    wb.format_percent(prem, "C5:C6")
    wb.format_brl(prem, "C7:C9", decimals=False)
    wb.format_percent(prem, "C10:C10")
    wb.format_int(prem, "C11:C11")
    wb.format_percent(prem, "C12:C12")
    wb.apply_zebra(prem, start_row=5, end_row=12, start_col=2, end_col=4)
    wb.apply_table_borders(prem, start_row=5, end_row=12, start_col=2, end_col=4)
    wb.define_name("wacc", prem, "$C$5")
    wb.define_name("inflacao", prem, "$C$6")
    wb.define_name("capex_inicial", prem, "$C$7")
    wb.define_name("receita_ano1", prem, "$C$9")

    # DRE projetada
    dre = wb.add_sheet("DRE")
    dre.column_dimensions["B"].width = 30
    for col in "CDEFGHIJKL":
        dre.column_dimensions[col].width = 14
    dre.cell(row=2, column=2, value="DRE PROJETADA — R$").font = _h2()
    headers = ["Item"] + [f"Ano {i}" for i in range(1, 11)]
    wb.write_header_row(dre, row=4, headers=headers, start_col=2)

    receita_base = 9_800_000
    cresc = 1.06
    receita = [receita_base * (cresc ** i) for i in range(10)]
    impostos_receita = [r * 0.0925 for r in receita]
    receita_liq = [r - i for r, i in zip(receita, impostos_receita)]
    opex_base = 4_200_000
    inflacao = 1.045
    opex = [opex_base * (inflacao ** i) for i in range(10)]
    ebitda = [r - o for r, o in zip(receita_liq, opex)]
    depreciacao = [18_400_000 / 10] * 10
    ebit = [e - d for e, d in zip(ebitda, depreciacao)]
    ir = [max(0, e) * 0.34 for e in ebit]
    lucro_liq = [e - i for e, i in zip(ebit, ir)]

    dados_dre = [
        ("Receita Bruta", receita),
        ("(-) Impostos sobre receita", [-i for i in impostos_receita]),
        ("= Receita Líquida", receita_liq),
        ("(-) OPEX", [-o for o in opex]),
        ("= EBITDA", ebitda),
        ("(-) Depreciação", [-d for d in depreciacao]),
        ("= EBIT", ebit),
        ("(-) IR/CSLL", [-i for i in ir]),
        ("= Lucro Líquido", lucro_liq),
    ]
    for i, (item, vals) in enumerate(dados_dre, start=5):
        dre.cell(row=i, column=2, value=item)
        for j, v in enumerate(vals):
            dre.cell(row=i, column=3 + j, value=round(v, 0))
    wb.format_brl(dre, "C5:L13", decimals=False)
    wb.apply_zebra(dre, start_row=5, end_row=13, start_col=2, end_col=12)
    wb.apply_table_borders(dre, start_row=5, end_row=13, start_col=2, end_col=12)

    # Fluxo de Caixa
    fc = wb.add_sheet("Fluxo de Caixa")
    fc.column_dimensions["B"].width = 30
    for col in "CDEFGHIJKLM":
        fc.column_dimensions[col].width = 14
    fc.cell(row=2, column=2, value="FLUXO DE CAIXA LIVRE — R$").font = _h2()
    headers_fc = ["Item"] + [f"Ano {i}" for i in range(0, 11)]
    wb.write_header_row(fc, row=4, headers=headers_fc, start_col=2)

    capex_ano0 = [-18_400_000] + [0] * 10
    fc_dados = [
        ("CAPEX", capex_ano0),
        ("EBITDA", [0] + ebitda),
        ("(-) Impostos", [0] + [-i for i in ir]),
        ("= FCL", [-18_400_000] + [e - i for e, i in zip(ebitda, ir)]),
    ]
    for i, (item, vals) in enumerate(fc_dados, start=5):
        fc.cell(row=i, column=2, value=item)
        for j, v in enumerate(vals):
            fc.cell(row=i, column=3 + j, value=round(v, 0))

    # Acumulado
    fcl_serie = fc_dados[3][1]
    acumulado = []
    s = 0
    for v in fcl_serie:
        s += v
        acumulado.append(s)
    fc.cell(row=9, column=2, value="Fluxo Acumulado")
    for j, v in enumerate(acumulado):
        fc.cell(row=9, column=3 + j, value=round(v, 0))

    wb.format_brl(fc, "C5:M9", decimals=False)
    wb.apply_zebra(fc, start_row=5, end_row=9, start_col=2, end_col=13)
    wb.apply_table_borders(fc, start_row=5, end_row=9, start_col=2, end_col=13)

    # Resumo
    res = wb.add_sheet("Resumo")
    res.column_dimensions["B"].width = 22
    res.cell(row=2, column=2, value="RESULTADOS DO MODELO").font = _h2()

    # Cálculo de VPL, TIR e payback (simplificado)
    def npv(rate, flows):
        return sum(f / ((1 + rate) ** i) for i, f in enumerate(flows))

    def irr(flows, guess=0.1):
        x = guess
        for _ in range(100):
            f = npv(x, flows)
            df = sum(-i * fl / ((1 + x) ** (i + 1)) for i, fl in enumerate(flows))
            if abs(df) < 1e-9:
                break
            x_new = x - f / df
            if abs(x_new - x) < 1e-7:
                return x_new
            x = x_new
        return x

    vpl = npv(0.118, fcl_serie)
    tir = irr(fcl_serie)
    payback_idx = next((i for i, a in enumerate(acumulado) if a >= 0), -1)
    payback = f"{payback_idx} anos" if payback_idx >= 0 else "n/a"

    wb.add_kpi_block(
        res,
        start_row=4,
        kpis=[
            {"label": "VPL @ 11,8%", "value": f"R$ {vpl/1_000_000:,.1f} MM", "subtext": "valor presente líquido"},
            {"label": "TIR", "value": f"{tir*100:.1f}%", "subtext": "taxa interna de retorno", "color": styles.BRAND.natureza},
            {"label": "Payback", "value": payback, "subtext": "fluxo acumulado ≥ 0", "color": styles.BRAND.por_do_sol},
        ],
    )

    out = XLSX_DIR / "financial_model_example.xlsx"
    return wb.save(out)


def build_kpi_dashboard_example() -> Path:
    """Dashboard KPI consolidado — visão das 3 concessionárias."""
    wb = EndorWorkbook(title="Dashboard Consolidado — Endor Energia")
    wb.add_cover(
        subtitle="Operação consolidada — Março 2026",
        metadata={"Período": "Mar/2026", "Frequência": "Mensal", "Versão": "v3.4"},
    )

    dash = wb.add_sheet("Dashboard")
    dash.column_dimensions["A"].width = 2
    for col in "BCDEFGHIJ":
        dash.column_dimensions[col].width = 12
    dash.cell(row=2, column=2, value="OPERAÇÃO CONSOLIDADA — MARÇO 2026").font = _h1()

    wb.add_kpi_block(
        dash,
        start_row=5,
        kpis=[
            {"label": "Atendimentos", "value": "313", "subtext": "mar/26 (3 concessões)"},
            {"label": "Solicitações", "value": "147", "subtext": "abertas no mês", "color": styles.BRAND.por_do_sol},
            {"label": "SLA no prazo", "value": "99,3%", "subtext": "meta ≥95%", "color": styles.BRAND.natureza},
            {"label": "Consumo", "value": "498 MWh", "subtext": "+3,2% vs fev", "color": styles.BRAND.terra},
        ],
        start_col=2,
    )

    # Por concessionária
    dash.cell(row=12, column=2, value="POR CONCESSIONÁRIA").font = _h2()
    wb.write_header_row(
        dash,
        row=14,
        headers=["Concessionária", "Pontos", "% LED", "Atendimentos", "SLA", "Consumo MWh"],
        start_col=2,
    )
    rows = [
        ("Luz Imperial (Vassouras)", 7072, 0.965, 147, 1.000, 198),
        ("Luz do Vale (Barra do Piraí)", 12480, 0.942, 95, 0.989, 234),
        ("Miguel Pereira Luz", 6318, 0.918, 71, 0.972, 66),
    ]
    for i, (nome, pontos, led, at, sla, mwh) in enumerate(rows, start=15):
        dash.cell(row=i, column=2, value=nome)
        dash.cell(row=i, column=3, value=pontos)
        dash.cell(row=i, column=4, value=led)
        dash.cell(row=i, column=5, value=at)
        dash.cell(row=i, column=6, value=sla)
        dash.cell(row=i, column=7, value=mwh)
    wb.format_int(dash, "C15:C17")
    wb.format_percent(dash, "D15:D17")
    wb.format_int(dash, "E15:E17")
    wb.format_percent(dash, "F15:F17", decimals=2)
    wb.format_int(dash, "G15:G17")
    wb.apply_zebra(dash, start_row=15, end_row=17, start_col=2, end_col=7)
    wb.apply_table_borders(dash, start_row=15, end_row=17, start_col=2, end_col=7)

    # Tendência - últimos 3 meses
    dash.cell(row=20, column=2, value="TENDÊNCIA — ÚLTIMOS 3 MESES").font = _h2()
    wb.write_header_row(dash, row=22, headers=["Métrica", "Jan/26", "Fev/26", "Mar/26", "Δ"], start_col=2)
    tend = [
        ("Atendimentos totais", 287, 304, 313, "+3,0%"),
        ("Consumo MWh", 451, 483, 498, "+3,1%"),
        ("SLA médio", 0.987, 0.991, 0.993, "+0,2 p.p."),
        ("% LED consolidado", 0.943, 0.945, 0.943, "−0,2 p.p."),
    ]
    for i, (met, j, f, m, d) in enumerate(tend, start=23):
        dash.cell(row=i, column=2, value=met)
        dash.cell(row=i, column=3, value=j)
        dash.cell(row=i, column=4, value=f)
        dash.cell(row=i, column=5, value=m)
        dash.cell(row=i, column=6, value=d)
    wb.format_int(dash, "C23:E24")
    wb.format_percent(dash, "C25:E26", decimals=2)
    wb.apply_zebra(dash, start_row=23, end_row=26, start_col=2, end_col=6)
    wb.apply_table_borders(dash, start_row=23, end_row=26, start_col=2, end_col=6)

    out = XLSX_DIR / "kpi_dashboard_example.xlsx"
    return wb.save(out)


def build_concession_model_example() -> Path:
    """Modelo de concessão específica — operação Luz Imperial."""
    wb = EndorWorkbook(title="Modelo de Concessão — Luz Imperial")
    wb.add_cover(
        subtitle="PPP de IP — Vassouras (RJ)",
        metadata={
            "Contrato": "27/2023",
            "Vigência": "20/Jan/2020 – 19/Jan/2030",
            "Concessionária": "CCIP de Vassouras S.A.",
        },
    )

    # Inputs do contrato
    inp = wb.add_sheet("Contrato")
    inp.column_dimensions["B"].width = 35
    inp.column_dimensions["C"].width = 22
    inp.cell(row=2, column=2, value="PARÂMETROS CONTRATUAIS").font = _h2()
    wb.write_header_row(inp, row=4, headers=["Item", "Valor"], start_col=2)
    contrato = [
        ("Número do contrato", "27/2023"),
        ("Concessionária", "CCIP de Vassouras S.A."),
        ("Município", "Vassouras (RJ)"),
        ("Vigência", "20/01/2020 a 19/01/2030"),
        ("CNPJ", "50.766.761/0001-27"),
        ("Pontos no parque (Mar/26)", 7072),
        ("Potência instalada (kW)", 466),
        ("% LED atual", 0.965),
        ("SLA contratual emergencial", "24h"),
        ("SLA contratual não emergencial", "48h"),
    ]
    for i, (item, val) in enumerate(contrato, start=5):
        inp.cell(row=i, column=2, value=item)
        inp.cell(row=i, column=3, value=val)
    wb.format_int(inp, "C10:C11")
    wb.format_percent(inp, "C12:C12")
    wb.apply_zebra(inp, start_row=5, end_row=14, start_col=2, end_col=3)
    wb.apply_table_borders(inp, start_row=5, end_row=14, start_col=2, end_col=3)

    # Operacional Mar/26
    op = wb.add_sheet("Operacional Mar26")
    op.column_dimensions["B"].width = 35
    op.column_dimensions["C"].width = 14
    op.column_dimensions["D"].width = 14

    op.cell(row=2, column=2, value="EXECUÇÃO — MARÇO 2026").font = _h2()
    wb.add_kpi_block(
        op,
        start_row=4,
        kpis=[
            {"label": "Atendimentos", "value": 147, "subtext": "em campo"},
            {"label": "Solicitações", "value": 67, "subtext": "abertas", "color": styles.BRAND.por_do_sol},
            {"label": "SLA", "value": "100%", "subtext": "67 de 67", "color": styles.BRAND.natureza},
        ],
    )

    op.cell(row=11, column=2, value="POR MOTIVO IDENTIFICADO").font = _h2()
    wb.write_header_row(op, row=13, headers=["Motivo", "Quantidade", "%"], start_col=2)
    motivos = [
        ("Manutenção corretiva", 88, 0.642),
        ("MOD - Modernizado", 12, 0.088),
        ("Conexão danificada", 9, 0.066),
        ("LED danificado", 8, 0.058),
        ("Relé danificado", 7, 0.051),
        ("Presença de abelhas/marimbondos", 6, 0.044),
        ("Condições climáticas desfavoráveis", 5, 0.036),
        ("Furto", 1, 0.007),
        ("Acesso impedido", 1, 0.007),
    ]
    for i, (m, q, p) in enumerate(motivos, start=14):
        op.cell(row=i, column=2, value=m)
        op.cell(row=i, column=3, value=q)
        op.cell(row=i, column=4, value=p)
    wb.format_int(op, "C14:C22")
    wb.format_percent(op, "D14:D22")
    wb.apply_zebra(op, start_row=14, end_row=22, start_col=2, end_col=4)
    wb.apply_table_borders(op, start_row=14, end_row=22, start_col=2, end_col=4)

    # Materiais
    mat = wb.add_sheet("Materiais")
    mat.column_dimensions["B"].width = 30
    for col in "CDE":
        mat.column_dimensions[col].width = 14
    mat.cell(row=2, column=2, value="MOVIMENTAÇÃO DE MATERIAIS — MARÇO 2026").font = _h2()
    wb.write_header_row(mat, row=4, headers=["Família", "Aplicados", "Retirados", "Saldo"], start_col=2)
    fam = [
        ("Cabo/Conexão", 230, 0, 230),
        ("Lâmpada LED", 76, 58, 18),
        ("Relé", 52, 45, 7),
        ("Outros", 30, 6, 24),
        ("Poste", 12, 0, 12),
        ("Braço", 4, 0, 4),
        ("Globo/Difusor", 3, 0, 3),
    ]
    for i, (f, a, r, s) in enumerate(fam, start=5):
        mat.cell(row=i, column=2, value=f)
        mat.cell(row=i, column=3, value=a)
        mat.cell(row=i, column=4, value=r)
        mat.cell(row=i, column=5, value=s)
    wb.format_int(mat, "C5:E11")
    wb.apply_zebra(mat, start_row=5, end_row=11, start_col=2, end_col=5)
    wb.apply_table_borders(mat, start_row=5, end_row=11, start_col=2, end_col=5)

    out = XLSX_DIR / "concession_model_example.xlsx"
    return wb.save(out)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _h1():
    from openpyxl.styles import Font
    return Font(name=styles.FONTS.document, size=styles.SIZES.h1, bold=True, color=styles.BRAND.endor.argb)


def _h2():
    from openpyxl.styles import Font
    return Font(name=styles.FONTS.document, size=styles.SIZES.h2, bold=True, color=styles.BRAND.terra.argb)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    builders = [
        build_board_report_example,
        build_investor_deck_example,
        build_project_status_example,
        build_financial_model_example,
        build_kpi_dashboard_example,
        build_concession_model_example,
    ]
    for fn in builders:
        out = fn()
        size = out.stat().st_size
        print(f"  {str(out.relative_to(REPO)):60} {size:>10,} bytes")


if __name__ == "__main__":
    main()
