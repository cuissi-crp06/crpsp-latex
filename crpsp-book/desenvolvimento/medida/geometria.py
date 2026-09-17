#!/usr/bin/env python3
"""Geometria das classes a partir das medidas do motor.

Lê medidas-fontes.tsv (produzido por medir-fontes.tex) e aplica os critérios
decididos em 17/09/2026 — ver ../../briefings/decisoes-2026-09-17.md.

Escreve geometria.md. Nada de rede, nada fora desta pasta.

    python3 geometria.py
"""

import csv
import pathlib

MM_POR_PT = 25.4 / 72.27
PT_POR_MM = 1 / MM_POR_PT

ENTRELINHA_PT = 18.0          # 12 pt x 1,5 — a entrelinha do WCAG 1.4.8
CORPO = "12.00"

# Critérios de 17/09. A margem interna é o piso de encadernação; a externa é o
# que sobra, e precisa ser MAIOR que a interna em manual e cartilha, para os
# artefatos decorativos.
CLASSES = {
    "cartilha": dict(
        papel=(148, 210), interna=15, vertical=18,
        teto=60, piso=None,        # sem listas aninhadas: não há piso
        candidatos=[60, 55, 50, 45, 40],
        nota="A5. Sem Leg e sem listas aninhadas, o piso deixa de existir.",
    ),
    "manual": dict(
        papel=(210, 297), interna=20, vertical=22,
        teto=80, piso=45,          # linha flexível de 45 a 80
        candidatos=[80, 70, 65, 60, 50, 45],
        nota="A4. Linha flexível de 45 a 80 caracteres.",
    ),
    "relatorio": dict(
        papel=(210, 297), interna=None, vertical=35,
        teto=80, piso=None,
        candidatos=[80, 75, 70, 65],
        nota="A4. Decoração nas margens superior e inferior: margem vertical "
             "de 35 mm de cada lado, e a lateral fica simétrica.",
    ),
}


def carregar(caminho="medidas-fontes.tsv"):
    """Devolve {fonte: mm por caractere} para o corpo de 12 pt."""
    with open(caminho, encoding="utf-8") as f:
        linhas = list(csv.DictReader(f, delimiter="\t"))
    return {
        l["fonte"]: (float(l["mm_por_car"]), float(l["altura_x_mm"]), l["rnib"])
        for l in linhas
        if l["corpo_pt"] == CORPO
    }


def linhas_por_pagina(altura_mm, vertical_mm):
    util_pt = (altura_mm - 2 * vertical_mm) * PT_POR_MM
    return int(util_pt // ENTRELINHA_PT)


def tabela_por_classe(nome, cfg, fontes):
    largura, altura = cfg["papel"]
    out = [f"### `{nome}`", "", cfg["nota"], ""]
    out.append(
        f"Papel {largura}×{altura} mm · margem vertical {cfg['vertical']} mm · "
        f"{linhas_por_pagina(altura, cfg['vertical'])} linhas por página "
        f"(entrelinha de {ENTRELINHA_PT:.0f} pt)."
    )
    out.append("")

    if cfg["interna"] is None:
        cab = "| Linha | " + " | ".join(
            f"{f}<br>mancha / margem por lado" for f in fontes) + " |"
    else:
        cab = "| Linha | " + " | ".join(
            f"{f}<br>mancha / **externa**" for f in fontes) + " |"
    out.append(cab)
    out.append("|---" * (len(fontes) + 1) + "|")

    for car in cfg["candidatos"]:
        celulas = []
        for f in fontes:
            mancha = fontes[f][0] * car
            sobra = largura - mancha
            if cfg["interna"] is None:
                lado = sobra / 2
                celulas.append(f"{mancha:.0f} mm / {lado:.0f} mm")
            else:
                externa = sobra - cfg["interna"]
                marca = "" if externa > cfg["interna"] else " ⚠️"
                celulas.append(f"{mancha:.0f} mm / **{externa:.0f} mm**{marca}")
        out.append(f"| {car} car. | " + " | ".join(celulas) + " |")
    out.append("")
    if cfg["interna"] is not None:
        out.append(
            f"Margem interna fixa em {cfg['interna']} mm. ⚠️ marca a linha em "
            f"que a margem externa deixa de ser maior que a interna — abaixo "
            f"dela o critério da decoração não se cumpre."
        )
        out.append("")
    return out


def main():
    fontes = carregar()
    ordem = ["Luciole", "NEWJUNE-Regular", "NEWJUNE-Serif", "Atkinson", "Lora"]
    fontes = {f: fontes[f] for f in ordem if f in fontes}

    doc = [
        "<!-- Gerado por geometria.py a partir de medidas-fontes.tsv.",
        "     Não editar à mão: rodar `python3 geometria.py`. -->",
        "",
        "# Geometria das classes, pelos critérios de 17/09",
        "",
        "Aplica as [decisões de 17/09](../../briefings/decisoes-2026-09-17.md)",
        "às medidas do motor. Corpo de 12 pt e entrelinha de 18 pt em todas as",
        "linhas, como decidido.",
        "",
        "## As fontes em disputa",
        "",
        "| Fonte | mm/car. | Altura-x | RNIB | Largura relativa |",
        "|---|---|---|---|---|",
    ]
    base = fontes["Luciole"][0]
    for f, (porcar, xh, rnib) in fontes.items():
        rel = (porcar / base - 1) * 100
        rel_txt = "—" if abs(rel) < 0.05 else f"{rel:+.1f}%"
        doc.append(f"| {f} | {porcar:.4f} | {xh:.3f} mm | {rnib} | {rel_txt} |")
    doc += [
        "",
        "Largura relativa à Luciole. **Fonte mais estreita = mais margem "
        "externa com o mesmo número de caracteres** — que é exatamente o que "
        "o critério da decoração pede.",
        "",
        "## Por classe",
        "",
    ]
    for nome, cfg in CLASSES.items():
        doc += tabela_por_classe(nome, cfg, fontes)

    pathlib.Path("geometria.md").write_text("\n".join(doc) + "\n", encoding="utf-8")
    print("geometria.md gravado")


if __name__ == "__main__":
    main()
