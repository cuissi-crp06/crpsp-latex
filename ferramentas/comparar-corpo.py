#!/usr/bin/env python3
"""Compara .sty/.cls pelo corpo, e diz se cada um já está no histórico do repositório.

O corpo é o arquivo sem CR, sem as quebras de linha finais e sem a declaração
\\ProvidesPackage, \\ProvidesFile ou \\ProvidesClass inteira — do comando até o
']' que fecha o argumento opcional, mesmo que ele ocupe mais de uma linha. É a
declaração que se reescreve ao arquivar, então comparar bytes crus dá falso
"inédito".

Uso:
    comparar-corpo.py CAMINHO... [--repo DIR]

CAMINHO é arquivo ou pasta (varrida recursivamente, sem .git). Com --repo, cada
corpo é procurado em todos os blobs .sty/.cls de todos os commits daquele
repositório; sem --repo, só agrupa os caminhos dados por corpo igual.
"""

import argparse
import hashlib
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

EXTENSOES = {".sty", ".cls"}

# \ProvidesX{nome} seguido, opcionalmente, de [ ... ] em uma ou mais linhas,
# e do fim de linha que sobra depois da declaração.
DECLARACAO = re.compile(
    r"^[ \t]*\\Provides(?:Package|File|Class)\{[^}]*\}(?:[ \t]*\[[^\]]*\])?[^\n]*\n?",
    re.MULTILINE,
)


def corpo(dados: bytes) -> str:
    texto = dados.decode("utf-8", errors="replace").replace("\r", "")
    texto = DECLARACAO.sub("", texto, count=1)
    # Arquivo sem quebra de linha final não é outro corpo.
    texto = texto.rstrip("\n") + "\n"
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()[:12]


def arquivos(caminhos):
    for c in map(Path, caminhos):
        if c.is_file():
            yield c
        elif c.is_dir():
            for p in sorted(c.rglob("*")):
                if p.suffix.lower() in EXTENSOES and p.is_file() and ".git" not in p.parts:
                    yield p
        else:
            print(f"aviso: {c} não existe", file=sys.stderr)


def corpos_do_historico(repo: Path):
    """corpo -> primeiro caminho (e commit) em que aparece, varrendo todos os blobs."""
    git = ["git", "-C", str(repo)]
    listagem = subprocess.run(
        git + ["rev-list", "--all", "--objects"], capture_output=True, text=True, check=True
    ).stdout
    vistos, achados = set(), {}
    for linha in listagem.splitlines():
        partes = linha.split(" ", 1)
        if len(partes) != 2 or Path(partes[1]).suffix.lower() not in EXTENSOES:
            continue
        blob, caminho = partes
        if blob in vistos:
            continue
        vistos.add(blob)
        dados = subprocess.run(git + ["cat-file", "blob", blob], capture_output=True, check=True).stdout
        achados.setdefault(corpo(dados), caminho)
    return achados


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("caminhos", nargs="+")
    ap.add_argument("--repo", type=Path, help="repositório git cujo histórico serve de referência")
    args = ap.parse_args()

    grupos = defaultdict(list)
    for p in arquivos(args.caminhos):
        grupos[corpo(p.read_bytes())].append(p)

    historico = corpos_do_historico(args.repo) if args.repo else None
    ineditos = 0
    for h, ps in sorted(grupos.items(), key=lambda kv: str(kv[1][0])):
        if historico is None:
            estado = ""
        elif h in historico:
            estado = f"  absorvido: {historico[h]}"
        else:
            estado = "  INÉDITO"
            ineditos += 1
        print(f"{h}{estado}")
        for p in ps:
            print(f"    {p}")

    print(f"\n{len(grupos)} corpos distintos", end="")
    print(f", {ineditos} fora do histórico" if historico is not None else "")


if __name__ == "__main__":
    main()
