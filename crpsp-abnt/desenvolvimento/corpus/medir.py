#!/usr/bin/env python3
"""Mede um estilo biblatex contra o corpus: uma linha TSV por exemplo.

Dois modos:

- referências (padrão): para cada entrada do .bib cuja chave é um id do TSV do
  corpus, compõe a referência na lista (sorting=none, na ordem do .bib) e
  compara com o exemplo da norma;
- chamadas (--chamadas TSV): para cada linha do TSV (id, comando, esperado),
  compõe o comando de citação e compara com a chamada esperada.

Sai em stdout:

    id  estado  esperado  obtido  diferenca

- estado: igual, difere ou ausente (o id não saiu no PDF);
- diferenca: diff de palavras, com [-norma-] e {+estilo+}.

A página é larga o bastante para cada exemplo caber numa linha, sem
hifenização: a quebra de linha não vira espaço no meio de URL. A comparação
ignora só espaço repetido e reticências compostas ([\\ldots] sai como
". . ."); caixa, pontuação e travessão contam.

Uso:
    python3 medir.py trilha-6023.bib [--tsv nbr6023.tsv]
    python3 medir.py trilha-10520.bib --chamadas chamadas-10520.tsv
    opções comuns: [--estilo abnt] [--opcao OPÇÃO ...] [--pasta DIR]

--estilo é o style= do biblatex (abnt, o upstream; crpsp-abnt, quando houver,
com a pasta do pacote no TEXINPUTS). --pasta guarda o .tex, o .pdf e o log.
Nada é escrito no repositório.
"""
import argparse
import csv
import difflib
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RE_CHAVE = re.compile(r"^@\w+\{([^,\s]+),", re.M)

TEX = r"""\documentclass{article}
\usepackage[paperwidth=500cm, paperheight=%(altura)dcm, margin=1cm]{geometry}
\usepackage[brazilian]{babel}
\usepackage{csquotes}
\usepackage[style=%(estilo)s, backend=biber, sorting=none%(opcoes)s]{biblatex}
\addbibresource{corpus.bib}
\AtEveryBibitem{\printtext{@@\thefield{entrykey}@@ }}
\hyphenpenalty=10000 \exhyphenpenalty=10000
\hbadness=10000 \parindent=0pt \raggedright
\pagestyle{empty}
\begin{document}
%(corpo)s
@@fim@@
\end{document}
"""


def normalizar(texto):
    texto = re.sub(r"\.\s\.\s\.", "...", texto)
    texto = texto.replace("…", "...")
    return re.sub(r"\s+", " ", texto).strip()


def diff_palavras(a, b):
    sa, sb = a.split(" "), b.split(" ")
    saida = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, sa, sb, autojunk=False).get_opcodes():
        if op == "equal":
            continue
        if i2 > i1:
            saida.append("[-" + " ".join(sa[i1:i2]) + "-]")
        if j2 > j1:
            saida.append("{+" + " ".join(sb[j1:j2]) + "+}")
    return " ".join(saida)


def compor(bib, corpo, linhas, estilo, opcoes, pasta):
    shutil.copy(bib, pasta / "corpus.bib")
    (pasta / "medir.tex").write_text(TEX % {
        "estilo": estilo, "opcoes": "".join(", " + o for o in opcoes),
        "corpo": corpo, "altura": max(30, 2 * linhas + 10)}, encoding="utf-8")
    passos = [["lualatex", "-interaction=nonstopmode", "medir.tex"],
              ["biber", "--quiet", "medir"],
              ["lualatex", "-interaction=nonstopmode", "medir.tex"]]
    for passo in passos:
        r = subprocess.run(passo, cwd=pasta, capture_output=True, text=True)
        if r.returncode != 0 and not (pasta / "medir.pdf").exists():
            sys.exit(f"falhou: {' '.join(passo)} (ver {pasta}/medir.log)")
    subprocess.run(["pdftotext", "-enc", "UTF-8", "medir.pdf", "medir.txt"],
                   cwd=pasta, check=True)
    texto = (pasta / "medir.txt").read_text(encoding="utf-8")
    partes = re.split(r"@@(.+?)@@", texto)
    return {partes[i]: normalizar(partes[i + 1]) for i in range(1, len(partes) - 1, 2)}


def ler_tsv(caminho):
    with open(caminho, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("bib", type=Path)
    ap.add_argument("--tsv", type=Path, default=AQUI / "nbr6023.tsv")
    ap.add_argument("--chamadas", type=Path)
    ap.add_argument("--estilo", default="abnt")
    ap.add_argument("--opcao", action="append", default=[],
                    help="opção a mais do biblatex (repetível), ex. slashdaterange")
    ap.add_argument("--pasta", type=Path)
    args = ap.parse_args()
    bib = args.bib.resolve()

    if args.chamadas:
        casos = ler_tsv(args.chamadas)
        esperado = {l["id"]: l["esperado"] for l in casos}
        ids = [l["id"] for l in casos]
        corpo = "\n".join(f"@@{l['id']}@@ {l['comando']}\\par" for l in casos)
    else:
        esperado = {l["id"]: l["texto"] for l in ler_tsv(args.tsv)}
        ids = [c for c in RE_CHAVE.findall(bib.read_text(encoding="utf-8")) if c in esperado]
        if not ids:
            sys.exit("nenhuma chave do .bib é id do corpus")
        corpo = "\\nocite{" + ",".join(ids) + "}\n\\printbibliography[heading=none]"

    if args.pasta:
        args.pasta.mkdir(parents=True, exist_ok=True)
        obtido = compor(bib, corpo, len(ids), args.estilo, args.opcao, args.pasta)
    else:
        with tempfile.TemporaryDirectory(prefix="crpsp-abnt-medir.") as tmp:
            obtido = compor(bib, corpo, len(ids), args.estilo, args.opcao, Path(tmp))

    conta = {"igual": 0, "difere": 0, "ausente": 0}
    w = csv.writer(sys.stdout, delimiter="\t", lineterminator="\n")
    w.writerow(["id", "estado", "esperado", "obtido", "diferenca"])
    for i in ids:
        e = normalizar(esperado[i])
        o = obtido.get(i)
        if o is None:
            estado, o, d = "ausente", "", ""
        elif o == e:
            estado, d = "igual", ""
        else:
            estado, d = "difere", diff_palavras(e, o)
        conta[estado] += 1
        w.writerow([i, estado, e, o, d])
    print(" ".join(f"{k}={v}" for k, v in conta.items()), file=sys.stderr)


if __name__ == "__main__":
    main()
