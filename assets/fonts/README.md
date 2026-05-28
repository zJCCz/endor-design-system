# Avenir Next LT Pro — Fontes Institucionais

10 estilos da família **Avenir Next LT Pro**, licenciada Linotype/Monotype.
São a tipografia INSTITUCIONAL da Endor Energia (Guia de Identidade,
páginas 14 e 15).

## ⚠️ Licenciamento

**Estas fontes são PROPRIETÁRIAS da Linotype/Monotype.**

- Endor Energia possui licença de uso interno.
- **NÃO redistribuir** fora da organização.
- **NÃO commitar** para repositórios públicos.
- **NÃO embedar** em arquivos enviados a terceiros sem revisar o EULA da
  licença (embedding "editable" geralmente NÃO é permitido; "view-only" /
  "print & preview" geralmente é).
- Em caso de dúvida, consulte o contrato de licença com a Linotype antes
  de uso fora dos canais aprovados.

Se este repositório for tornar-se público em algum momento, **estas fontes
devem ser removidas antes** e movidas para um sistema interno de
distribuição (intranet, OneDrive, repositório privado dedicado).

## Inventário

| Arquivo | Estilo | Weight CSS | Uso |
|--|--|--:|--|
| `AvenirNextLTProUltLt.ttf` | Ultra Light | 200 | Quase nunca — apenas peças decorativas grandes |
| `AvenirNextLTProUltLtCn.ttf` | Ultra Light Condensed | 200 | Idem, em espaços estreitos |
| `AvenirNextLTProRegular.ttf` | Regular | 400 | Body text padrão |
| `AvenirNextLTProMedium.ttf` | Medium | 500 | Sub-headers, ênfase leve |
| `AvenirNextLTProMediumCn.ttf` | Medium Condensed | 500 | Idem, em espaços estreitos |
| `AvenirNextLTProDemi.ttf` | Demi (Semibold) | 600 | Ênfase em body, sub-headers fortes |
| `AvenirNextLTProDemiCn.ttf` | Demi Condensed | 600 | Idem |
| `AvenirNextLTProBold.ttf` | Bold | 700 | Headers, ênfase principal |
| `AvenirNextLTProHeavy.ttf` | Heavy | 900 | Display, capas, títulos dominantes |
| `AvenirNextLTProHeavyCn.ttf` | Heavy Condensed | 900 | Display em espaços estreitos |

Family name registrada (CSS / Office): **`Avenir Next LT Pro`**

## Instalação

### macOS / Windows
Duplo-clique nos `.ttf` → "Install Font" / "Instalar fonte". Reinicie o
PowerPoint/Excel/Word para o sistema reconhecer.

### Linux
```bash
mkdir -p ~/.local/share/fonts
cp assets/fonts/*.ttf ~/.local/share/fonts/
fc-cache -f -v
```

### Web (CSS)
```css
@font-face {
  font-family: "Avenir Next LT Pro";
  font-weight: 400;
  src: url("/fonts/AvenirNextLTProRegular.ttf") format("truetype");
}
/* ... uma regra por weight ... */
```

> Para web pública, prefira hospedar via Adobe Fonts / Monotype Fonts com
> licença web ativa — não servir os `.ttf` diretamente, pois isso
> redistribui o arquivo para todo visitante.

## Quando usar Avenir Next vs Calibri

Decisão do Guia (página 15) reforçada neste design system:

| Cenário | Fonte | Por quê |
|--|--|--|
| Peças impressas finais (banners, relatórios encadernados, sinalização, materiais de marketing) | **Avenir Next LT Pro** | Tipografia institucional. Pipeline controlado pela equipe de marca. |
| Documentos abertos (.pptx, .xlsx, .docx) | **Calibri** | Compatibilidade Office universal — recipiente não precisa ter Avenir Next instalada. |
| E-mails formatados | **Calibri** | Idem. |
| Apresentações de marca (capas premium, materiais de eventos) | **Avenir Next LT Pro** com embedding | Equipe de marca exporta o `.pptx` com fontes embutidas e distribui o resultado, não o arquivo editável. |

Os builders Python (`EndorPresentation`, `EndorWorkbook`) usam **Calibri por
padrão**. Para forçar Avenir Next em uma peça específica:

```python
from endor_docs import EndorPresentation, styles

# styles.FONTS.primary devolve "Avenir Next LT Pro"
# A fonte precisa estar instalada na máquina onde o PPT será aberto.
```

> Em v0.1.0 os builders não trocam de fonte automaticamente. Para usar
> Avenir Next em PPTX gerado por código, edite manualmente após geração
> ou faça monkey-patch em `styles.FONTS.document = styles.FONTS.primary`
> antes de instanciar `EndorPresentation`. Em v0.2.0 isso virará
> parâmetro do construtor.
