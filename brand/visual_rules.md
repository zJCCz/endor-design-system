# Regras Visuais — Endor Energia

Regras duras de aplicação da marca. Extraídas do
`Endor_Guia_Identidade_Visual.pdf` (set/2023). Em caso de conflito entre
este arquivo e o PDF, **o PDF prevalece** — abra um issue para sincronizar.

Quem gera artefatos automaticamente (builders Python, IAs, scripts) usa
estas regras como contrato. Quem revisa manualmente usa como checklist.

---

## 1. Paleta de cores

### Cor principal

| Token | Hex | RGB | Pantone | Uso |
|--|--|--|--|--|
| `color.brand.endor` | `#0A1A5C` | 10, 26, 92 | 287C | Cor institucional. Fundos primários, títulos, elemento âncora da marca. |

### Cores secundárias

| Token | Hex | RGB | Pantone | Uso |
|--|--|--|--|--|
| `color.brand.terra` | `#0083CA` | 0, 131, 202 | 299C | Destaques, links, títulos secundários (h2), categorização. |
| `color.brand.por-do-sol` | `#6C3F99` | 108, 63, 153 | 265C | Tags de seção, dados sociais/comunitários, contrastes pontuais. |
| `color.brand.natureza` | `#00718A` | 0, 113, 138 | 326C | Dados ambientais, ESG, indicadores positivos (success). |
| `color.brand.tech` | `#858A9E` | 133, 138, 158 | 429C | Texto auxiliar, dados técnicos, eixos de gráfico. |

### Regra de aplicação de cores em peças

- Toda peça tem **uma cor primária** (Endor) e **no máximo duas secundárias**
  como destaque. Mais que isso pollui.
- Cores secundárias **categorizam**, não decoram. Cada uma representa um
  contexto (Natureza → ambiental, Tech → técnico, Pôr do Sol → social, etc.).
- Para gráficos com múltiplas séries, usar a sequência canônica de
  `color.chart.categorical` — não inventar a ordem.

### Combinações proibidas

- ❌ Texto Pôr do Sol sobre fundo Natureza (contraste insuficiente)
- ❌ Texto Terra sobre fundo Endor (azul sobre azul — ilegível em corpo pequeno)
- ❌ Quatro ou mais cores da paleta em uma mesma peça
- ❌ Cores fora da paleta para representar dados de marca (gradientes,
  esverdeados, magentas, laranjas que não estejam definidos como
  `color.semantic.warning`)

---

## 2. Logotipo

### Variantes (escolha por fundo)

| Variante | Quando usar | Pasta |
|--|--|--|
| **Principal** (com brilho/efeito) | Fundos brancos ou muito claros. Versão mais expressiva. | `assets/logos/fundo-branco/*/vetor/` |
| **Simplificada** (sem brilho) | Quando a versão principal é tecnicamente inviável: impressão monocromática, baixa resolução, materiais promocionais com restrição de cor. | `assets/logos/*/simplificada/` |
| **Monocromática** | Cor única. Branca em fundo escuro, preta em fundo claro. | `assets/logos/monocromatica/` |
| **Sobre fundo azul** | Fundo azul institucional Endor. Tipografia em branco. | `assets/logos/fundo-azul/` |

### Fundos permitidos

- ✅ Branco e tons de cinza muito claros (até 10% de saturação)
- ✅ Azul institucional Endor (`#0A1A5C`) — usar variante "fundo-azul"
- ✅ Cores secundárias da paleta — usar variante monocromática branca
- ✅ Imagens com áreas limpas e baixa interferência ao redor do logotipo

### Fundos a evitar

- ❌ Cores fora da paleta
- ❌ Imagens com alta densidade visual atrás do logo
- ❌ Gradientes que cruzam o logotipo

### Área de proteção

A área mínima ao redor do logotipo é equivalente à **altura da letra "O"** do
logotipo. Aplicar em todas as direções. Nada (texto, imagem, borda) deve
invadir essa área.

### Redução mínima

| Meio | Tamanho mínimo |
|--|--|
| Impressão | **20 mm** de largura |
| Digital | **200 px** de largura |

Abaixo desse tamanho, usar o **símbolo isolado** (`assets/logos/*/simbolo/`)
em vez do logotipo completo.

### Os 6 usos incorretos do logotipo

Extraídos da página 16 do Guia. **Nunca**:

1. ❌ Alterar as cores da marca
2. ❌ Alterar a relação de hierarquia entre símbolo e tipografia
3. ❌ Alterar a orientação dos elementos (rotação, espelho)
4. ❌ Alterar a proporção (esticar horizontalmente ou verticalmente)
5. ❌ Alterar a tipografia da marca (substituir a fonte do logotipo)
6. ❌ Utilizar a marca em versão "traço" (apenas contorno)

> **Regra de ouro**: nunca reconstrua a marca. Use sempre os arquivos
> originais em `assets/logos/`.

---

## 3. Tipografia

### Famílias

| Família | Quando usar | Tokens |
|--|--|--|
| **Avenir Next LT Pro** | Peças institucionais finais (impressos premium, sinalização, banners, materiais distribuídos pela diretoria de marca). Arquivos em `assets/fonts/`. Licença Linotype/Monotype — **NÃO redistribuir**. | `font.family.primary` |
| **Calibri** | Documentos abertos: .pptx, .xlsx, .docx, e-mails formatados, todos os artefatos gerados pelos builders Python. Embutida no Microsoft Office. | `font.family.document` |

> Documentos de trabalho diários **usam Calibri**. Avenir Next LT Pro é
> reservada para peças institucionais finais e requer aprovação da equipe
> de marca para uso.

### Pesos disponíveis

- Avenir Next LT Pro: Ultra Light (200), Regular (400), Medium (500),
  Demi/Semibold (600), Bold (700), Heavy (900) — todos com variante
  Condensed para Ultra Light, Medium, Demi e Heavy. Ver `assets/fonts/README.md`.
- Calibri: Regular (400), Bold (700)

### Hierarquia tipográfica (Calibri, em pt)

| Nível | Tamanho | Peso | Cor | Uso |
|--|--|--|--|--|
| display | 60 | Bold | endor | Capa: título principal |
| h1 | 28 | Bold | endor | Início de seção numerada |
| h2 | 18 | Bold | terra | Subtítulo de seção |
| h3 | 14 | Bold | endor | Título de bloco/card |
| body | 10 | Regular | gray-800 | Texto corrido |
| small | 9 | Regular | gray-600 | Caption, footer, notas |
| tiny | 8 | Regular | gray-500 | Paginação, créditos mínimos |
| kpi-value | 36 | Bold | endor (ou cor da tag) | Número grande em cards |
| kpi-label | 9 | Regular | gray-600 | Label acima do número |

### Alinhamento

- Texto corrido: **alinhar à esquerda** (não justificar — gera "rios" e
  espaçamentos irregulares).
- Números em tabela: **alinhar à direita** (preserva leitura de magnitude).
- Cabeçalhos de coluna em tabela: **alinhar com o tipo de dado da coluna**.

---

## 4. Espaçamento e layout

### Grid de 4pt

Todo espaçamento (margens, paddings, gaps) usa múltiplos de 4pt. Valores
nominais em `space.*` do tokens.json. Não inventar valores intermediários
(7pt, 13pt — proibidos).

### Margens de página

Padrão A4: **18 mm** em todas as bordas. Slides 16:9: **20 mm** lateral
e superior, **15 mm** inferior (acomoda footer).

### Hierarquia visual

- **Capa**: respiro generoso (`space.7` ou `space.8`). Um título dominante.
- **Página interna**: margem consistente, headers de seção destacados, body
  com line-height `font.lineHeight.normal` (1.4).
- **Cards**: padding `space.4` (16pt), border-radius `radius.md` (8pt).

---

## 5. Aplicação em documentos gerados

Quando builders Python produzem PPTX/XLSX:

- **Logo no canto**: sempre `assets/logos/fundo-branco/energia/digital/EndorEnergia.png`
  (ou variante apropriada ao fundo do slide) no canto superior esquerdo, com
  altura proporcional a ~5% da altura do slide.
- **Footer com paginação**: `font.size.tiny` (8pt) em `color.neutral.gray-500`,
  rodapé direito.
- **Cores de fundo**: branco padrão. Slides de divisor de seção podem usar
  `color.brand.endor` com tipografia branca.
- **Tabelas**: header em `color.brand.endor` com texto branco; linhas
  alternadas em `color.neutral.gray-50` (zebra sutil); divisor inferior em
  `color.neutral.gray-200`.
- **Gráficos**: usar sempre `endor_docs.charts` — paleta, eixos e formatação
  já vêm padronizados.

---

## 6. Casos especiais

### Concessionárias

Cada concessionária herda a estrutura "símbolo Endor + nome próprio".
Exemplos válidos:

- `Luz Imperial — ILUMINAÇÃO PÚBLICA — Vassouras`
- `Luz do Vale — ILUMINAÇÃO PÚBLICA — Barra do Piraí`
- `Miguel Pereira Luz — ILUMINAÇÃO PÚBLICA`

Em peças destinadas exclusivamente à concessionária, a marca da concessionária
pode aparecer **isolada** (sem o "Endor Energia" co-presente). Em peças de
governança corporativa (relatórios consolidados), a marca Endor Energia tem
precedência hierárquica.

### Cobrança de identidade em parcerias

Em peças com co-branding (parceiros, prefeituras, fornecedores), a marca Endor
fica **à esquerda** ou **acima** do parceiro, em tamanho igual ou superior,
com separador claro entre as marcas (linha vertical de 1pt em
`color.neutral.gray-300`, ou espaçamento equivalente a 2× a área de proteção).

---

## 7. Versões e atualizações

Este documento reflete o guia de **setembro/2023**. Atualizações ao guia
master devem:

1. Atualizar `brand/Endor_Guia_Identidade_Visual.pdf` (substituindo o arquivo)
2. Sincronizar este `visual_rules.md` com as mudanças
3. Atualizar `tokens/endor.tokens.json` se cores/fontes mudarem
4. Rodar `scripts/build_templates.py` e `scripts/build_examples.py` para
   regenerar artefatos
5. Bump da versão em `tokens/endor.tokens.json` ($metadata.version)
