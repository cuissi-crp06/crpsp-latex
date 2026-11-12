#!/usr/bin/env python3
"""Compara uma rodada do verificar.sh com a linha-base, só nas linhas da rodada.

Uso:
    comparar-linha-base.py RODADA.tsv LINHA-BASE.tsv

Cada arquivo da RODADA precisa existir na linha-base e ter as mesmas colunas
motor, paginas, objetos, erros_tagging, faltantes e fatais (a coluna
primeiro_erro é só texto e fica de fora). Arquivo da linha-base que a rodada
não compilou é ignorado: o CI compila só um subconjunto (os que não dependem
das fontes proprietárias). Código de saída 1 se houver diferença, linha ausente
da linha-base ou rodada vazia.
"""

import csv
import sys

COLUNAS = ["motor", "paginas", "objetos", "erros_tagging", "faltantes", "fatais"]


def ler(caminho):
    with open(caminho, newline="", encoding="utf-8") as f:
        return {linha["arquivo"]: linha for linha in csv.DictReader(f, delimiter="\t")}


def main(argv):
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2
    rodada, base = ler(argv[1]), ler(argv[2])
    if not rodada:
        print("ERRO: a rodada não tem nenhuma linha.")
        return 1
    erros = 0
    for arquivo, linha in rodada.items():
        if arquivo not in base:
            print(f"ERRO: {arquivo}: ausente da linha-base")
            erros += 1
            continue
        for col in COLUNAS:
            if linha[col] != base[arquivo][col]:
                print(
                    f"ERRO: {arquivo}: {col} = {linha[col]!r}, linha-base {base[arquivo][col]!r}"
                    + (f" ({linha['primeiro_erro']})" if linha["primeiro_erro"] else "")
                )
                erros += 1
    if erros:
        print(f"{erros} diferença(s) em relação à linha-base.")
        return 1
    print(f"{len(rodada)} arquivo(s) iguais à linha-base.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
