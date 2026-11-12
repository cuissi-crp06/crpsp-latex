#!/usr/bin/env python3
"""Verificações baratas de coerência do repositório (as do CI; sem TeX, sem fontes).

Uso:
    verificar-coerencia.py [--raiz DIR] [--base REF]

Verifica, em todos os arquivos de texto rastreados (ou, fora de um repositório
git, encontrados sob a raiz):

1. Marcadores de conflito de merge (`<<<<<<<`, `>>>>>>>`).
2. Regra zero da CONVENCAO-VERSIONAMENTO.md: dois .sty/.cls que declaram o mesmo
   nome (`\\ProvidesPackage{nome}`) com corpos diferentes são erro. O corpo é o
   arquivo sem CR, sem a declaração `\\Provides*` inteira e sem as quebras de
   linha finais, o mesmo critério de `ferramentas/comparar-corpo.py`.
3. Com --base REF (o CI passa a base do pull request): arquivo cujo corpo mudou
   em relação a REF precisa mudar de data E de versão, e nenhuma das duas pode
   regredir. Mudar só a declaração não exige nada.
4. Versão do CHANGELOG mais recente de cada linha igual à do arquivo principal
   da linha (tabela LINHAS abaixo). Data diferente é só aviso: o CHANGELOG
   registra a data da passagem, a declaração a da autoria do corpo.

Saída: uma linha por achado, `ERRO:` (falha, código 1) ou `AVISO:`. Dentro do
GitHub Actions, as linhas saem também como anotações (`::error`/`::warning`).
Só biblioteca padrão do Python 3.
"""

import argparse
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

# Mesmo critério de ferramentas/comparar-corpo.py.
DECLARACAO = re.compile(
    r"^[ \t]*\\Provides(?:Package|File|Class)\{[^}]*\}(?:[ \t]*\[[^\]]*\])?[^\n]*\n?",
    re.MULTILINE,
)
# Primeira linha da declaração: nome, data, versão (a descrição não interessa).
CABECALHO = re.compile(
    r"^[ \t]*\\Provides(?:Package|File|Class)\{(?P<nome>[^}]*)\}[ \t]*"
    r"\[[ \t]*(?P<data>\d{4}/\d{2}/\d{2})[ \t]+v(?P<versao>\d+(?:\.\d+)*(?:-[A-Za-z]+)?)",
    re.MULTILINE,
)
VERSAO = re.compile(r"^(\d+(?:\.\d+)*)(?:-([A-Za-z]+))?$")
# Título de versão no CHANGELOG: `## 0.5.3-alfa — 2026/10/31` (ou com hífens).
TITULO_VERSAO = re.compile(
    r"^##[ \t]+(?P<versao>\d+\.\d+\.\d+(?:-[A-Za-z]+)?)[ \t]+[—–-][ \t]+"
    r"(?P<data>\d{4}[/-]\d{2}[/-]\d{2})",
    re.MULTILINE,
)
EXTENSOES = {".sty", ".cls"}
BINARIOS = {".pdf", ".png", ".jpg", ".jpeg", ".eps", ".otf", ".ttf", ".docx", ".odt", ".zip"}
FASES = {"alfa": 0, "beta": 1, None: 2}  # a ordem do semver: alfa < beta < estável

# CHANGELOG -> arquivo principal da linha cuja declaração ele acompanha.
LINHAS = {
    "crpsp-book/CHANGELOG.md": "crpsp-book/book-crpsp_acessivel.sty",
    "crpsp-forms/CHANGELOG.md": "crpsp-forms/formularios.sty",
    "crpsp-memoir/CHANGELOG.md": "crpsp-memoir/relatorio-gestao.sty",
    "crpsp-abnt/CHANGELOG.md": "crpsp-abnt/crpsp-abnt.bbx",
}


class Relato:
    def __init__(self):
        self.erros = 0

    def emitir(self, nivel, arquivo, msg):
        print(f"{nivel}: {arquivo}: {msg}")
        if os.environ.get("GITHUB_ACTIONS"):
            comando = "error" if nivel == "ERRO" else "warning"
            print(f"::{comando} file={arquivo}::{msg}")
        if nivel == "ERRO":
            self.erros += 1

    def erro(self, arquivo, msg):
        self.emitir("ERRO", arquivo, msg)

    def aviso(self, arquivo, msg):
        self.emitir("AVISO", arquivo, msg)


def corpo(texto):
    texto = texto.replace("\r", "")
    texto = DECLARACAO.sub("", texto, count=1)
    return texto.rstrip("\n") + "\n"


def declaracao(texto):
    """(nome, data, versão) ou None."""
    m = CABECALHO.search(texto.replace("\r", ""))
    return (m["nome"], m["data"], m["versao"]) if m else None


def chave_versao(versao):
    """Chave de ordenação: números, depois a fase (alfa < beta < estável)."""
    m = VERSAO.match(versao)
    partes = [int(n) for n in m[1].split(".")]
    partes += [0] * (3 - len(partes))
    fase = m[2].lower() if m[2] else None
    return tuple(partes), FASES.get(fase, -1)


def git(raiz, *args):
    return subprocess.run(["git", "-C", str(raiz), *args], capture_output=True, text=True)


def listar(raiz):
    """Caminhos relativos (str, com /) dos arquivos de texto do repositório."""
    r = git(raiz, "ls-files", "-z")
    if r.returncode == 0:
        nomes = [n for n in r.stdout.split("\0") if n]
    else:  # fora de um repositório git: varre a pasta
        nomes = [
            p.relative_to(raiz).as_posix()
            for p in sorted(Path(raiz).rglob("*"))
            if p.is_file() and ".git" not in p.relative_to(raiz).parts
        ]
    return [n for n in nomes if Path(n).suffix.lower() not in BINARIOS and (Path(raiz) / n).is_file()]


def ler(raiz, rel):
    try:
        return (Path(raiz) / rel).read_bytes().decode("utf-8")
    except UnicodeDecodeError:
        return None  # binário disfarçado: fora das verificações de texto


def verificar_conflitos(raiz, nomes, relato):
    ini = re.compile(r"^(<{7}|>{7})([ \t].*)?$", re.MULTILINE)
    meio = re.compile(r"^={7}$", re.MULTILINE)
    for rel in nomes:
        texto = ler(raiz, rel)
        if texto is None:
            continue
        texto = texto.replace("\r", "")
        achou = ini.search(texto)
        if achou:
            linha = texto.count("\n", 0, achou.start()) + 1
            extra = " (e '=======')" if meio.search(texto) else ""
            relato.erro(rel, f"marcador de conflito de merge na linha {linha}{extra}")


def verificar_regra_zero(raiz, nomes, relato):
    por_nome = defaultdict(list)  # nome declarado -> [(rel, data, versão, corpo)]
    for rel in nomes:
        if Path(rel).suffix.lower() not in EXTENSOES:
            continue
        texto = ler(raiz, rel)
        if texto is None:
            continue
        d = declaracao(texto)
        if d is None:
            relato.aviso(rel, "sem \\Provides* com nome, data e versão no formato da convenção")
            continue
        por_nome[d[0]].append((rel, d[1], d[2], corpo(texto)))
    for nome, itens in sorted(por_nome.items()):
        if len({c for *_, c in itens}) < 2:
            continue
        lista = "; ".join(f"{rel} ({data} v{versao})" for rel, data, versao, _ in itens)
        datas = len({data for _, data, _, _ in itens}) < len(itens)
        versoes = len({v for _, _, v, _ in itens}) < len(itens)
        motivo = ""
        if datas or versoes:
            partilhado = " e ".join(x for x, ok in (("data", datas), ("versão", versoes)) if ok)
            motivo = f" e ainda compartilham {partilhado}"
        for rel, *_ in itens:
            relato.erro(
                rel,
                f"regra zero: o nome declarado '{nome}' aparece com corpos diferentes{motivo}: {lista}",
            )


def verificar_base(raiz, nomes, base, relato):
    for rel in nomes:
        if Path(rel).suffix.lower() not in EXTENSOES:
            continue
        antigo = git(raiz, "show", f"{base}:{rel}")
        atual = ler(raiz, rel)
        if antigo.returncode != 0 or atual is None:
            continue  # arquivo novo na mudança: nada a comparar
        if corpo(antigo.stdout) == corpo(atual):
            continue
        d_novo, d_velho = declaracao(atual), declaracao(antigo.stdout)
        if d_novo is None or d_velho is None:
            continue  # já avisado pela regra zero
        _, data_n, versao_n = d_novo
        _, data_v, versao_v = d_velho
        if data_n == data_v:
            relato.erro(rel, f"corpo mudou em relação a {base}, mas a data continua {data_v}")
        elif data_n < data_v:
            relato.erro(rel, f"data regrediu: {data_v} em {base}, {data_n} agora")
        if versao_n == versao_v:
            relato.erro(rel, f"corpo mudou em relação a {base}, mas a versão continua v{versao_v}")
        elif chave_versao(versao_n) < chave_versao(versao_v):
            relato.erro(rel, f"versão regrediu: v{versao_v} em {base}, v{versao_n} agora")


def verificar_changelogs(raiz, relato):
    for log, principal in LINHAS.items():
        caminho_log, caminho_pkg = Path(raiz) / log, Path(raiz) / principal
        if not caminho_log.is_file():
            continue  # linha ausente (caso de teste ou linha removida)
        if not caminho_pkg.is_file():
            relato.erro(log, f"arquivo principal da linha não existe: {principal}")
            continue
        m = TITULO_VERSAO.search(caminho_log.read_text(encoding="utf-8").replace("\r", ""))
        d = declaracao(caminho_pkg.read_text(encoding="utf-8"))
        if not m:
            relato.erro(log, "nenhum título '## X.Y.Z-fase — AAAA/MM/DD' encontrado")
            continue
        if d is None:
            relato.erro(principal, "sem declaração \\Provides* no formato da convenção")
            continue
        _, data_pkg, versao_pkg = d
        if m["versao"] != versao_pkg:
            relato.erro(
                log,
                f"versão mais recente do CHANGELOG é {m['versao']}, mas {principal} declara v{versao_pkg}",
            )
        elif m["data"].replace("-", "/") != data_pkg:
            relato.aviso(
                log,
                f"mesma versão ({versao_pkg}), datas diferentes: CHANGELOG {m['data']}, {principal} {data_pkg}",
            )


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--raiz", default=".", help="raiz do repositório (padrão: pasta atual)")
    ap.add_argument("--base", help="referência git da base (ex.: origin/main) para a verificação 3")
    args = ap.parse_args(argv)
    raiz = Path(args.raiz).resolve()
    relato = Relato()
    nomes = listar(raiz)
    verificar_conflitos(raiz, nomes, relato)
    verificar_regra_zero(raiz, nomes, relato)
    if args.base:
        verificar_base(raiz, nomes, args.base, relato)
    verificar_changelogs(raiz, relato)
    if relato.erros:
        print(f"{relato.erros} erro(s).")
        return 1
    print("Coerência ok.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
