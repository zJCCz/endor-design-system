"""
Organiza os assets brutos de identidade visual da Endor para a estrutura
canônica do design system.

Lê de: /tmp/endor-assets/Marca_Endor vF/
Escreve em: <repo>/assets/logos/ e <repo>/brand/

Idempotente: usar shutil.copy2 mantém metadados e sobrescreve se já existir.
Roda uma única vez na configuração inicial. Os assets reorganizados são o
artefato de verdade no repo — não re-rodar a cada commit.
"""
from __future__ import annotations

import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = Path("/tmp/endor-assets/Marca_Endor vF")
ASSETS = REPO / "assets" / "logos"
BRAND = REPO / "brand"


VARIANT_MAP = {
    "1_Endor_Principal_Fundo_Branco": "fundo-branco",
    "2_Endor_Fundo_Azul": "fundo-azul",
    "3_Endor_Monocromatica": "monocromatica",
}

SUBDIR_MAP = {
    "Digital_Imagens": "digital",
    "Impressao_Vetores": "vetor",
    "Sem_Efeito_Uso_Restrito": "simplificada",
}

CONCESSIONARIA_SLUG = {
    "Luz_Do_Vale": "luz-do-vale",
    "Luz_Imperial": "luz-imperial",
    "Miguel_Pereira_Luz": "miguel-pereira-luz",
}


def copy_leaf(src_dir: Path, dst_dir: Path, manifest: list) -> None:
    if not src_dir.exists():
        return
    dst_dir.mkdir(parents=True, exist_ok=True)
    for f in sorted(src_dir.iterdir()):
        if f.is_file():
            dst = dst_dir / f.name
            shutil.copy2(f, dst)
            manifest.append((str(f.relative_to(SRC)), str(dst.relative_to(REPO))))


def copy_category(src_cat: Path, dst_cat: Path, manifest: list) -> None:
    """Copia uma categoria com as 3 subpastas (digital/vetor/simplificada)."""
    for src_sub, dst_sub in SUBDIR_MAP.items():
        copy_leaf(src_cat / src_sub, dst_cat / dst_sub, manifest)


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"Source not found: {SRC}")

    manifest: list[tuple[str, str]] = []

    BRAND.mkdir(parents=True, exist_ok=True)
    guia = SRC / "Endor_Guia_Identidade_Visual.pdf"
    if guia.exists():
        dst = BRAND / "Endor_Guia_Identidade_Visual.pdf"
        shutil.copy2(guia, dst)
        manifest.append((guia.name, str(dst.relative_to(REPO))))

    for src_variant, dst_variant in VARIANT_MAP.items():
        v_src = SRC / src_variant
        v_dst = ASSETS / dst_variant
        if not v_src.exists():
            continue

        copy_category(v_src / "1_Principal_Energia", v_dst / "energia", manifest)

        conc_src = v_src / "2_Concessionarias"
        if conc_src.exists():
            for sub in sorted(conc_src.iterdir()):
                if sub.is_dir():
                    slug = CONCESSIONARIA_SLUG.get(sub.name, sub.name.lower().replace("_", "-"))
                    copy_category(sub, v_dst / "concessionarias" / slug, manifest)

        copy_category(v_src / "3_Submarcas", v_dst / "submarcas", manifest)

        simbolo_src = v_src / "4_Simbolo_Avatar"
        if simbolo_src.exists():
            copy_leaf(simbolo_src, v_dst / "simbolo", manifest)

    manifest_path = REPO / "assets" / "MANIFEST.txt"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("w", encoding="utf-8") as fh:
        fh.write("# Manifest de organização dos assets\n")
        fh.write(f"# Origem: {SRC}\n")
        fh.write(f"# Total de arquivos: {len(manifest)}\n\n")
        for src_rel, dst_rel in sorted(manifest, key=lambda x: x[1]):
            fh.write(f"{dst_rel}\n    <- {src_rel}\n")

    print(f"{len(manifest)} arquivos organizados.")
    print(f"Manifest: {manifest_path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
