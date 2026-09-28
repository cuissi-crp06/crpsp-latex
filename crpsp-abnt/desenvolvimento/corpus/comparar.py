#!/usr/bin/env python3
"""Compara uma medida do medir.py com a linha-base, entrada por entrada.

A régua não mede pixels: compara o texto obtido de cada exemplo, já
normalizado pelo medir.py. Qualquer mudança nele conta, porque o que se
procura é o upstream (ou o próprio estilo) mudando por baixo:

- piora: era igual à norma e deixou de ser (ou sumiu do PDF);
- melhora: passou a sair igual à norma;
- muda: continua diferente da norma, mas o texto obtido mudou;
- novo / saiu: o id está só na medida nova, ou só na linha-base.

Sai em stdout uma linha por id que mudou (tipo, id, diff de palavras entre
o obtido antes e o obtido agora) e, por último, o resumo. O código de saída
é 1 se algo mudou: melhora também pede linha-base nova, gravada de propósito.

Uso:
    python3 comparar.py medida-crpsp-abnt-0.3.0.tsv nova.tsv [--rotulo trilha]
"""
import argparse
import csv
import sys
from pathlib import Path

from medir import diff_palavras


def ler(caminho):
    with open(caminho, encoding="utf-8", newline="") as f:
        return {l["id"]: l for l in csv.DictReader(f, delimiter="\t")}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("base", type=Path)
    ap.add_argument("nova", type=Path)
    ap.add_argument("--rotulo", default="")
    args = ap.parse_args()
    base, nova = ler(args.base), ler(args.nova)

    mudancas = []
    for i in list(base) + [i for i in nova if i not in base]:
        a, b = base.get(i), nova.get(i)
        if a is None:
            mudancas.append(("novo", i, b["estado"]))
        elif b is None:
            mudancas.append(("saiu", i, a["estado"]))
        elif a["obtido"] != b["obtido"] or a["estado"] != b["estado"]:
            if a["estado"] == "igual":
                tipo = "piora"
            elif b["estado"] == "igual":
                tipo = "melhora"
            else:
                tipo = "muda"
            mudancas.append((tipo, i, diff_palavras(a["obtido"], b["obtido"])))

    for m in mudancas:
        print("\t".join(m))
    iguais = sum(1 for l in nova.values() if l["estado"] == "igual")
    conta = {t: sum(1 for m in mudancas if m[0] == t)
             for t in ("piora", "melhora", "muda", "novo", "saiu")}
    rotulo = f"{args.rotulo}: " if args.rotulo else ""
    print(f"{rotulo}{iguais}/{len(nova)} iguais à norma; "
          + ", ".join(f"{k} {v}" for k, v in conta.items()))
    sys.exit(1 if mudancas else 0)


if __name__ == "__main__":
    main()
