# Endor Design System

Sistema operacional da identidade visual da **Endor Energia**.

Este repositório é a fonte única de verdade para qualquer artefato visual da
empresa — apresentações, relatórios, planilhas, e-mails formatados, materiais
impressos. Ele combina:

- **Tokens** versionados (`tokens/endor.tokens.json`) — cores, tipografia,
  espaçamento e demais decisões visuais
- **Assets** vetoriais e raster (`assets/logos/`) — variantes oficiais do
  logotipo, submarcas e concessionárias
- **Builders Python** (`src/endor_docs/`) — geração programática de PPTX, XLSX
  e charts já com a marca aplicada
- **Templates e exemplos** (`templates/`, `examples/`) — pontos de partida
  prontos para os casos de uso mais comuns
- **Guia oficial em PDF** (`brand/Endor_Guia_Identidade_Visual.pdf`) —
  documento mestre aprovado pela diretoria de marca em setembro/2023

## Para quem é este sistema

| Persona | O que usar |
|--|--|
| **Outras instâncias de IA gerando documentos** | `CLAUDE.md` → invoca os builders em `src/endor_docs/` |
| **Analistas e gestores** (criando decks/relatórios sem código) | `templates/` (.pptx e .xlsx) — abre no Office e edita |
| **Designers** (peças customizadas) | `assets/logos/*/vetor/*.ai` + `brand/Endor_Guia_Identidade_Visual.pdf` |
| **Desenvolvedores** (integrando em outros sistemas) | `tokens/endor.tokens.json` — consumir via Style Dictionary, ou Python via `src/endor_docs/styles.py` |

## Princípios

### 1. Tokens são lei

Nenhuma cor, fonte ou tamanho fica hardcoded em código. Tudo vem do
`tokens/endor.tokens.json`. Mudou um token → roda os builders → templates
e exemplos se atualizam. Esse loop é o que mantém o sistema vivo.

### 2. Templates e exemplos são gerados, não desenhados

Os arquivos `.pptx` e `.xlsx` em `templates/` e `examples/` são produzidos
pelos scripts em `scripts/`. Editar manualmente no PowerPoint/Excel é uma
operação descartável — a próxima geração sobrescreve. Quando o template
precisar evoluir, mude o **builder** ou os **tokens**, não o arquivo final.

### 3. Hierarquia de marca acima de criatividade isolada

A Endor opera em três níveis de marca (ver abaixo). Toda peça respeita o
nível ao qual pertence. Misturas (logo Endor + cor de concessionária)
exigem aprovação formal.

### 4. Compatibilidade Office > esteticismo tipográfico

Documentos editáveis (.pptx, .xlsx, .docx) usam **Calibri** — fonte embutida
no Office, garantindo que qualquer pessoa abra o arquivo sem fonte faltando.
**Avenir Next** fica reservada para peças impressas finais onde a equipe de
marca controla o pipeline de exportação.

## Hierarquia de marca

```
Endor Energia (holding institucional)
│
├── Endor Ambiental
├── Endor Geração Distribuída     ← Submarcas (4 áreas de atuação)
├── Endor Infraestrutura
├── Endor Participações
│
├── Luz do Vale (Barra do Piraí)
├── Luz Imperial (Vassouras)        ← Concessionárias (PPPs municipais)
└── Miguel Pereira Luz
```

### Endor Energia (holding)

Marca institucional. Aparece em comunicação corporativa, relatórios para
investidores, materiais ESG agregados, sinalização de sede.

Tagline: nenhuma — usar apenas "Endor Energia" como assinatura.

### Submarcas

Endor Ambiental, Endor Geração Distribuída, Endor Infraestrutura,
Endor Participações. Identificam áreas de atuação do grupo. Usar quando
o material é específico de um setor.

Construção: logo Endor + nome do setor em Avenir Next Regular na cor Tech
(#858A9E). Alinhamento à esquerda do logotipo.

### Concessionárias

Operações de iluminação pública municipal. Hoje: Luz do Vale, Luz Imperial,
Miguel Pereira Luz. Cada uma tem nome próprio + tagline "ILUMINAÇÃO PÚBLICA"
+ identificação do município.

Construção: símbolo Endor + nome próprio em Avenir Next Bold + "ILUMINAÇÃO
PÚBLICA" em pequeno + nome do município (quando aplicável).

Novas concessionárias devem seguir o mesmo padrão e ser registradas em
`assets/logos/*/concessionarias/<slug>/`.

## Estrutura do repositório

```
endor-design-system/
├── brand/                            Documentação humana de marca
│   ├── Endor_Guia_Identidade_Visual.pdf  Guia oficial (set/2023) — mestre
│   ├── endor_design_system.md            Este arquivo
│   ├── visual_rules.md                   Regras duras (do/don't)
│   └── reference/                        Peças de referência feitas por designers
│
├── tokens/
│   └── endor.tokens.json             Fonte da verdade — cores, fontes, espaços
│
├── assets/
│   ├── logos/
│   │   ├── fundo-branco/             Logos para fundo claro (versão completa, com brilho)
│   │   ├── fundo-azul/               Logos sobre fundo azul institucional
│   │   └── monocromatica/            Logos em cor única (preto/branco/azul)
│   │       └── (cada uma com: energia/, concessionarias/, submarcas/, simbolo/)
│   └── MANIFEST.txt                  Mapa origem → destino dos assets
│
├── src/endor_docs/                   Builders Python
│   ├── styles.py                     Carrega tokens, expõe constantes
│   ├── charts.py                     Fábricas de gráficos com paleta Endor
│   ├── ppt_builder.py                EndorPresentation
│   └── xlsx_builder.py               EndorWorkbook
│
├── templates/                        Templates gerados (entrada de uso direto)
│   ├── pptx/  (corporate, investor, project-report)
│   └── xlsx/  (financial-model, dashboard, operational-report)
│
├── examples/                         Exemplos preenchidos (referência de uso)
│
├── docs/                             Guias de uso humano
│   ├── powerpoint_guidelines.md
│   ├── spreadsheet_guidelines.md
│   ├── chart_guidelines.md
│   └── examples_to_follow.md
│
├── scripts/                          Scripts de manutenção
│   ├── organize_assets.py            Reorganização inicial dos assets brutos
│   ├── build_templates.py            Regenera templates a partir dos builders
│   └── build_examples.py             Regenera exemplos a partir dos builders
│
├── CLAUDE.md                         Instrução operacional para IAs
└── README.md                         Quickstart para humanos
```

## Versionamento

- **v0.1.0** (atual) — bootstrap. Tokens, assets, builders mínimos viáveis.
- Versões `0.x` mantêm a flexibilidade de mudar APIs sem aviso. A partir de
  `1.0.0` qualquer breaking change vai em changelog.

## Referências

- `brand/Endor_Guia_Identidade_Visual.pdf` — Guia oficial de identidade visual
  (Endor Brasil, setembro 2023). Documento mestre.
- `brand/visual_rules.md` — Regras operacionais extraídas do guia, em formato
  consultável por IA e humanos.
- `brand/reference/Relatorio_LuzImperial_Mar2026.pdf` — Exemplo de relatório
  mensal feito por designer interno. Base de estilo para os templates de
  relatório operacional.
