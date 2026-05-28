"""
Gera os templates oficiais do design system Endor a partir dos builders.

Roda: ``python scripts/build_templates.py``

Saída:
  templates/pptx/
    endor_corporate_template.pptx
    endor_investor_deck_template.pptx
    endor_project_report_template.pptx
  templates/xlsx/
    endor_financial_model_template.xlsx
    endor_dashboard_template.xlsx
    endor_operational_report_template.xlsx

Estes templates são esqueletos com placeholders ([Título], [Subtítulo],
[Valor]). Para exemplos preenchidos com dados realistas, ver
``scripts/build_examples.py``.

Os arquivos gerados estão commitados no repo. Ao mudar tokens ou builders,
re-rodar este script e commitar os .pptx/.xlsx atualizados.
"""

from __future__ import annotations

from pathlib import Path

from endor_docs import EndorPresentation, EndorWorkbook
from endor_docs import styles

REPO = Path(__file__).resolve().parent.parent
PPTX_DIR = REPO / "templates" / "pptx"
XLSX_DIR = REPO / "templates" / "xlsx"


# ---------------------------------------------------------------------------
# PPTX templates
# ---------------------------------------------------------------------------


def build_corporate_template() -> Path:
    """Template corporativo genérico — apresentações institucionais."""
    deck = EndorPresentation(title="[Título da Apresentação]")
    deck.add_cover(
        subtitle="[Subtítulo descritivo]",
        date="[Mês/Ano]",
        metadata={
            "Autor": "[Nome]",
            "Área": "[Departamento]",
        },
    )

    deck.add_section_divider("[Nome da Seção]", number=1)

    deck.add_content_slide(
        title="[Título do slide]",
        subtitle="[Subtítulo, opcional]",
        bullets=[
            "[Primeiro ponto importante]",
            "[Segundo ponto importante]",
            "[Terceiro ponto importante]",
            "[Adicione mais bullets conforme necessário]",
        ],
    )

    deck.add_kpi_slide(
        title="[Título dos indicadores]",
        kpis=[
            {"label": "[Métrica 1]", "value": "[Valor]", "subtext": "[contexto]"},
            {"label": "[Métrica 2]", "value": "[Valor]", "subtext": "[contexto]", "color": styles.BRAND.por_do_sol},
            {"label": "[Métrica 3]", "value": "[Valor]", "subtext": "[contexto]", "color": styles.BRAND.natureza},
            {"label": "[Métrica 4]", "value": "[Valor]", "subtext": "[contexto]", "color": styles.BRAND.terra},
        ],
    )

    deck.add_content_slide(
        title="[Conclusão / Próximos passos]",
        bullets=[
            "[Ação 1]",
            "[Ação 2]",
            "[Ação 3]",
        ],
    )

    deck.add_closing(text="Obrigado.")

    out = PPTX_DIR / "endor_corporate_template.pptx"
    return deck.save(out)


def build_investor_deck_template() -> Path:
    """Template para pitch deck a investidores/conselho."""
    deck = EndorPresentation(title="[Endor Energia — Update]")
    deck.add_cover(
        subtitle="[Apresentação para Investidores]",
        date="[Q1 2026]",
    )

    deck.add_section_divider("Visão Geral", number=1)
    deck.add_content_slide(
        title="Quem somos",
        bullets=[
            "[1 frase: o que a Endor faz]",
            "[1 frase: nicho específico — iluminação pública via PPPs]",
            "[1 frase: alcance — N municípios, X habitantes atendidos]",
            "[1 frase: ESG / impacto social]",
        ],
    )

    deck.add_section_divider("Mercado e Tração", number=2)
    deck.add_kpi_slide(
        title="Indicadores-chave",
        kpis=[
            {"label": "Receita anual", "value": "[R$ XX MM]", "subtext": "+X% YoY"},
            {"label": "EBITDA margin", "value": "[XX%]", "subtext": "vs [Y%] yr ant", "color": styles.BRAND.natureza},
            {"label": "Concessões ativas", "value": "[N]", "subtext": "em M municípios", "color": styles.BRAND.por_do_sol},
            {"label": "Pontos atendidos", "value": "[XX.XXX]", "subtext": "[XX%] LED", "color": styles.BRAND.terra},
        ],
    )

    deck.add_content_slide(
        title="[Trajetória de crescimento]",
        bullets=[
            "[Marco 1: ano]",
            "[Marco 2: ano]",
            "[Marco 3: ano — atual]",
            "[Próximo marco: previsão]",
        ],
    )

    deck.add_section_divider("Próximos Passos", number=3)
    deck.add_content_slide(
        title="O que estamos buscando",
        bullets=[
            "[Pedido principal — captação / contrato / parceria]",
            "[Uso dos recursos]",
            "[Timeline esperada]",
        ],
    )

    deck.add_closing(text="Obrigado.", contact="ir@endor.energia")

    out = PPTX_DIR / "endor_investor_deck_template.pptx"
    return deck.save(out)


def build_project_report_template() -> Path:
    """Template para relatório operacional (estilo Luz Imperial Mar/26)."""
    deck = EndorPresentation(title="[Relatório de Atividades]")
    deck.add_cover(
        subtitle="[Período: Mês/Ano]",
        date="[Mês/Ano]",
        metadata={
            "Contrato": "[N° XX/AAAA]",
            "Emissão": "[Mês AAAA]",
            "Destinatário": "[Poder Concedente]",
        },
    )

    deck.add_section_divider("Sumário Executivo", number=1)
    deck.add_kpi_slide(
        title="Visão geral do período",
        kpis=[
            {"label": "Atendimentos", "value": "[NNN]", "subtext": "em campo"},
            {"label": "Solicitações", "value": "[NN]", "subtext": "abertas", "color": styles.BRAND.por_do_sol},
            {"label": "SLA no prazo", "value": "[XX%]", "subtext": "em atraso: [Y%]", "color": styles.BRAND.natureza},
            {"label": "Consumo", "value": "[XXX MWh]", "subtext": "[±X%] vs ant.", "color": styles.BRAND.terra},
        ],
    )

    deck.add_section_divider("Indicadores Operacionais", number=2)
    deck.add_content_slide(
        title="[Tópico operacional 1]",
        bullets=[
            "[Fato 1]",
            "[Fato 2]",
            "[Fato 3]",
        ],
    )
    deck.add_content_slide(
        title="[Tópico operacional 2]",
        bullets=[
            "[Análise]",
            "[Causa raiz]",
            "[Ação corretiva]",
        ],
    )

    deck.add_section_divider("Encerramento", number=3)
    deck.add_closing(text="[Encerramento]", contact="[contato@empresa.com.br]")

    out = PPTX_DIR / "endor_project_report_template.pptx"
    return deck.save(out)


# ---------------------------------------------------------------------------
# XLSX templates
# ---------------------------------------------------------------------------


def build_financial_model_template() -> Path:
    """Template de modelo financeiro com Premissas, DRE e Fluxo de Caixa."""
    wb = EndorWorkbook(title="[Modelo Financeiro]")
    wb.add_cover(
        subtitle="[Projeto / Concessão]",
        metadata={
            "Versão": "[v0.1]",
            "Período": "[10 anos]",
            "Moeda": "BRL",
        },
    )

    # --- Premissas ---
    prem = wb.add_sheet("Premissas")
    prem.column_dimensions["B"].width = 35
    prem.column_dimensions["C"].width = 18
    prem.column_dimensions["D"].width = 12

    prem.cell(row=2, column=2, value="PREMISSAS DO MODELO").font = styles_font_h2()
    wb.write_header_row(prem, row=4, headers=["Premissa", "Valor", "Unidade"], start_col=2)

    premissas = [
        ("Taxa de desconto (WACC)", 0.12, "% a.a."),
        ("Inflação anual projetada", 0.045, "% a.a."),
        ("CAPEX total inicial", 0, "BRL"),
        ("OPEX anual base", 0, "BRL"),
        ("Receita anual ano 1", 0, "BRL"),
        ("Crescimento receita a.a.", 0.05, "% a.a."),
        ("Prazo contratual", 10, "anos"),
        ("Imposto sobre lucro", 0.34, "%"),
    ]
    for i, (item, val, un) in enumerate(premissas, start=5):
        prem.cell(row=i, column=2, value=item)
        prem.cell(row=i, column=3, value=val)
        prem.cell(row=i, column=4, value=un)

    wb.format_percent(prem, "C5:C6")
    wb.format_brl(prem, "C7:C9")
    wb.format_percent(prem, "C10:C10")
    wb.format_int(prem, "C11:C11")
    wb.format_percent(prem, "C12:C12")
    wb.apply_zebra(prem, start_row=5, end_row=12, start_col=2, end_col=4)
    wb.apply_table_borders(prem, start_row=5, end_row=12, start_col=2, end_col=4)

    # Named ranges para uso nas outras abas
    wb.define_name("wacc", prem, "$C$5")
    wb.define_name("inflacao", prem, "$C$6")
    wb.define_name("capex_inicial", prem, "$C$7")
    wb.define_name("opex_anual_base", prem, "$C$8")
    wb.define_name("receita_ano1", prem, "$C$9")
    wb.define_name("crescimento_receita", prem, "$C$10")
    wb.define_name("prazo_anos", prem, "$C$11")
    wb.define_name("aliquota_ir", prem, "$C$12")

    # --- DRE ---
    dre = wb.add_sheet("DRE")
    dre.column_dimensions["B"].width = 28
    for col in range(3, 13):
        dre.column_dimensions[chr(64 + col)].width = 14

    dre.cell(row=2, column=2, value="DRE PROJETADA (R$)").font = styles_font_h2()
    headers = ["Item"] + [f"Ano {i}" for i in range(1, 11)]
    wb.write_header_row(dre, row=4, headers=headers, start_col=2)

    linhas_dre = [
        "Receita Bruta",
        "(-) Impostos sobre receita",
        "= Receita Líquida",
        "(-) OPEX",
        "= EBITDA",
        "(-) Depreciação",
        "= EBIT",
        "(-) IR/CSLL",
        "= Lucro Líquido",
    ]
    for i, item in enumerate(linhas_dre, start=5):
        dre.cell(row=i, column=2, value=item)
    wb.format_brl(dre, f"C5:L{4 + len(linhas_dre)}", decimals=False)
    wb.apply_zebra(dre, start_row=5, end_row=4 + len(linhas_dre), start_col=2, end_col=12)
    wb.apply_table_borders(dre, start_row=5, end_row=4 + len(linhas_dre), start_col=2, end_col=12)

    # --- Fluxo de Caixa ---
    fc = wb.add_sheet("Fluxo de Caixa")
    fc.column_dimensions["B"].width = 28
    for col in range(3, 13):
        fc.column_dimensions[chr(64 + col)].width = 14

    fc.cell(row=2, column=2, value="FLUXO DE CAIXA LIVRE (R$)").font = styles_font_h2()
    wb.write_header_row(fc, row=4, headers=["Item"] + [f"Ano {i}" for i in range(0, 11)], start_col=2)

    linhas_fc = [
        "EBITDA",
        "(-) CAPEX",
        "(-) Variação capital de giro",
        "(-) Impostos",
        "= Fluxo de Caixa Livre",
        "Fluxo Acumulado",
    ]
    for i, item in enumerate(linhas_fc, start=5):
        fc.cell(row=i, column=2, value=item)
    wb.format_brl(fc, f"C5:M{4 + len(linhas_fc)}", decimals=False)
    wb.apply_zebra(fc, start_row=5, end_row=4 + len(linhas_fc), start_col=2, end_col=13)
    wb.apply_table_borders(fc, start_row=5, end_row=4 + len(linhas_fc), start_col=2, end_col=13)

    # --- Resumo / Outputs ---
    res = wb.add_sheet("Resumo")
    res.column_dimensions["B"].width = 22
    res.column_dimensions["C"].width = 18

    res.cell(row=2, column=2, value="RESULTADOS DO MODELO").font = styles_font_h2()
    wb.add_kpi_block(
        res,
        start_row=4,
        kpis=[
            {"label": "VPL", "value": "[calcular]", "subtext": "valor presente líquido"},
            {"label": "TIR", "value": "[calcular]", "subtext": "taxa interna de retorno", "color": styles.BRAND.natureza},
            {"label": "Payback", "value": "[calcular]", "subtext": "anos", "color": styles.BRAND.por_do_sol},
        ],
    )

    out = XLSX_DIR / "endor_financial_model_template.xlsx"
    return wb.save(out)


def build_dashboard_template() -> Path:
    """Template de dashboard KPI."""
    wb = EndorWorkbook(title="[Dashboard KPI]")
    wb.add_cover(
        subtitle="[Período de referência]",
        metadata={"Atualização": "[Data]", "Frequência": "[Mensal / Trimestral]"},
    )

    dash = wb.add_sheet("Dashboard")
    for col, w in zip("BCDEFGHIJ", [3, 12, 12, 12, 3, 12, 12, 12, 3]):
        dash.column_dimensions[col].width = w

    dash.cell(row=2, column=2, value="[TÍTULO DO DASHBOARD]").font = styles_font_h1()

    # KPI block (4 indicadores)
    wb.add_kpi_block(
        dash,
        start_row=5,
        kpis=[
            {"label": "[KPI 1]", "value": "[Valor]", "subtext": "[contexto]"},
            {"label": "[KPI 2]", "value": "[Valor]", "subtext": "[contexto]", "color": styles.BRAND.natureza},
            {"label": "[KPI 3]", "value": "[Valor]", "subtext": "[contexto]", "color": styles.BRAND.por_do_sol},
        ],
        start_col=2,
    )

    # Tabela detalhada
    wb.write_header_row(dash, row=12, headers=["Item", "Atual", "Anterior", "Var %"], start_col=2)
    for i in range(3):
        dash.cell(row=13 + i, column=2, value=f"[Item {i+1}]")
    wb.apply_zebra(dash, start_row=13, end_row=15, start_col=2, end_col=5)
    wb.apply_table_borders(dash, start_row=13, end_row=15, start_col=2, end_col=5)

    out = XLSX_DIR / "endor_dashboard_template.xlsx"
    return wb.save(out)


def build_operational_report_template() -> Path:
    """Template de relatório operacional (XLSX equivalente ao Luz Imperial)."""
    wb = EndorWorkbook(title="[Relatório Operacional]")
    wb.add_cover(
        subtitle="[Período: Mês/Ano]",
        metadata={
            "Contrato": "[N°/AAAA]",
            "Concessão": "[Nome]",
            "Município": "[Cidade]",
        },
    )

    # Resumo
    res = wb.add_sheet("Resumo do mês")
    res.cell(row=2, column=2, value="SUMÁRIO EXECUTIVO").font = styles_font_h2()
    wb.add_kpi_block(
        res,
        start_row=4,
        kpis=[
            {"label": "Atendimentos", "value": "[NNN]", "subtext": "em campo"},
            {"label": "Solicitações", "value": "[NN]", "subtext": "abertas", "color": styles.BRAND.por_do_sol},
            {"label": "SLA no prazo", "value": "[XX%]", "subtext": "no prazo", "color": styles.BRAND.natureza},
            {"label": "Consumo", "value": "[XXX MWh]", "subtext": "[±X%]", "color": styles.BRAND.terra},
        ],
    )

    # Atendimentos
    at = wb.add_sheet("Atendimentos")
    at.cell(row=2, column=2, value="DETALHE DE ATENDIMENTOS").font = styles_font_h2()
    wb.write_header_row(at, row=4, headers=["Motivo", "Quantidade", "%"], start_col=2)
    for i in range(5):
        at.cell(row=5 + i, column=2, value=f"[Motivo {i+1}]")
    wb.format_int(at, "C5:C10")
    wb.format_percent(at, "D5:D10")
    wb.apply_zebra(at, start_row=5, end_row=10, start_col=2, end_col=4)
    wb.apply_table_borders(at, start_row=5, end_row=10, start_col=2, end_col=4)

    # Materiais
    mat = wb.add_sheet("Materiais")
    mat.cell(row=2, column=2, value="MATERIAIS APLICADOS E RETIRADOS").font = styles_font_h2()
    wb.write_header_row(mat, row=4, headers=["Família", "Aplicados", "Retirados", "Saldo"], start_col=2)
    for i in range(7):
        mat.cell(row=5 + i, column=2, value=f"[Família {i+1}]")
    wb.format_int(mat, "C5:E12")
    wb.apply_zebra(mat, start_row=5, end_row=12, start_col=2, end_col=5)
    wb.apply_table_borders(mat, start_row=5, end_row=12, start_col=2, end_col=5)

    out = XLSX_DIR / "endor_operational_report_template.xlsx"
    return wb.save(out)


# ---------------------------------------------------------------------------
# Helpers (fontes pré-formatadas usadas nos templates xlsx)
# ---------------------------------------------------------------------------


def styles_font_h1():
    from openpyxl.styles import Font
    return Font(name=styles.FONTS.document, size=styles.SIZES.h1, bold=True, color=styles.BRAND.endor.argb)


def styles_font_h2():
    from openpyxl.styles import Font
    return Font(name=styles.FONTS.document, size=styles.SIZES.h2, bold=True, color=styles.BRAND.terra.argb)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    builders = [
        build_corporate_template,
        build_investor_deck_template,
        build_project_report_template,
        build_financial_model_template,
        build_dashboard_template,
        build_operational_report_template,
    ]
    for fn in builders:
        out = fn()
        size = out.stat().st_size
        print(f"  {str(out.relative_to(REPO)):60} {size:>10,} bytes")


if __name__ == "__main__":
    main()
