#!/usr/bin/env python3
"""Compara o relatório JSON do veraPDF (--flavour ua2) com as reprovações esperadas.

Uso:
    comparar-verapdf.py RELATORIO.json ESPERADO.txt LISTA.txt [--resumo ARQ.md]

RELATORIO.json  saída de `verapdf --flavour ua2 --format json` sobre os PDFs que o
                verificar.sh gravou em SAIDA_PDF (nome = caminho do .tex sem
                extensão, com "/" trocado por "_": mwe/mwe_minimal.tex vira
                mwe_mwe_minimal.pdf).
ESPERADO.txt    ci-verapdf-esperado.txt: uma linha por documento que NÃO passa em
                ua2 por motivo conhecido, `arquivo<TAB>regras<TAB>motivo`, com as
                regras separadas por vírgula no formato `cláusula#teste`
                (8.11.1#1). Documento ausente da lista tem de passar sem reprovação.
LISTA.txt       ci-sem-fontes.txt: os documentos que o CI compila.

Falha (código 1) se, em qualquer documento, o conjunto de regras reprovadas for
diferente do esperado, nos dois sentidos: regra nova é regressão; regra esperada
que passou é melhoria e exige tirar a exceção da lista, para a lista não mentir.
Também falha se faltar PDF no relatório, se o veraPDF não terminar normalmente
um documento ou se a lista de exceções citar documento fora de LISTA.txt.
"""

import json
import sys
from pathlib import Path


def nome_pdf(rel):
    return rel.removesuffix(".tex").replace("/", "_") + ".pdf"


def linhas_uteis(caminho):
    for numero, linha in enumerate(Path(caminho).read_text(encoding="utf-8").splitlines(), 1):
        if linha.strip() and not linha.lstrip().startswith("#"):
            yield numero, linha


def ler_lista(caminho):
    return [linha.strip() for _, linha in linhas_uteis(caminho)]


def ler_esperado(caminho, lista):
    esperado, erros = {}, []
    for numero, linha in linhas_uteis(caminho):
        campos = linha.split("\t")
        if len(campos) != 3 or not all(c.strip() for c in campos):
            erros.append(f"ERRO: esperado linha {numero}: use arquivo<TAB>regras<TAB>motivo")
            continue
        rel, regras, _motivo = (c.strip() for c in campos)
        if rel not in lista:
            erros.append(f"ERRO: esperado linha {numero}: {rel} não está na lista de MWEs do CI")
        elif rel in esperado:
            erros.append(f"ERRO: esperado linha {numero}: {rel} repetido")
        else:
            esperado[rel] = {r.strip() for r in regras.split(",") if r.strip()}
    return esperado, erros


def ler_relatorio(caminho):
    """Devolve {nome do PDF: (conjunto de regras reprovadas, jobEndStatus)}."""
    dados = json.loads(Path(caminho).read_text(encoding="utf-8"))
    resultado = {}
    for job in dados["report"]["jobs"]:
        nome = Path(job["itemDetails"]["name"]).name
        validacao = job["validationResult"][0] if job.get("validationResult") else {}
        status = validacao.get("jobEndStatus", "sem resultado")
        regras = {
            f"{r['clause']}#{r['testNumber']}"
            for r in validacao.get("details", {}).get("ruleSummaries", [])
            if r.get("status") == "failed" or r.get("ruleStatus") == "FAILED"
        }
        resultado[nome] = (regras, status)
    return resultado


def main(argv):
    resumo = None
    if "--resumo" in argv:
        i = argv.index("--resumo")
        resumo = argv[i + 1]
        argv = argv[:i] + argv[i + 2 :]
    if len(argv) != 4:
        print(__doc__, file=sys.stderr)
        return 2
    lista = ler_lista(argv[3])
    esperado, erros = ler_esperado(argv[2], lista)
    try:
        obtido = ler_relatorio(argv[1])
    except (OSError, ValueError, KeyError, IndexError) as e:
        print(f"ERRO: relatório do veraPDF ilegível ({type(e).__name__}: {e})")
        return 1
    if not lista:
        erros.append("ERRO: a lista de MWEs está vazia")

    tabela = []
    passou = reprovou_esperado = 0
    for rel in lista:
        nome = nome_pdf(rel)
        if nome not in obtido:
            erros.append(f"ERRO: {rel}: sem PDF no relatório do veraPDF ({nome})")
            tabela.append((rel, "ERRO", "sem PDF no relatório", ""))
            continue
        regras, status = obtido[nome]
        if status != "normal":
            erros.append(f"ERRO: {rel}: o veraPDF terminou com jobEndStatus={status!r}")
            tabela.append((rel, "ERRO", f"jobEndStatus {status}", ""))
            continue
        previsto = esperado.get(rel, set())
        novas, sumidas = sorted(regras - previsto), sorted(previsto - regras)
        if novas:
            erros.append(f"ERRO: {rel}: reprova regra não esperada: {', '.join(novas)}")
        if sumidas:
            erros.append(
                f"ERRO: {rel}: regra esperada passou ({', '.join(sumidas)}); "
                "tire-a de ci-verapdf-esperado.txt"
            )
        if novas or sumidas:
            situacao = "DIVERGE"
        elif regras:
            situacao, reprovou_esperado = "FAIL esperado", reprovou_esperado + 1
        else:
            situacao, passou = "PASS", passou + 1
        tabela.append((rel, situacao, ", ".join(sorted(regras)), ", ".join(sorted(previsto))))
    for nome in sorted(set(obtido) - {nome_pdf(r) for r in lista}):
        erros.append(f"ERRO: {nome}: PDF no relatório que não está na lista de MWEs")

    divergentes = len(lista) - passou - reprovou_esperado
    cabecalho = (
        f"PDF/UA-2 (veraPDF): {passou} PASS, {reprovou_esperado} FAIL esperado, "
        f"{divergentes} divergente(s), de {len(lista)} documento(s)."
    )
    for rel, situacao, regras, _ in tabela:
        print(f"{situacao:13} {rel}  {regras}")
    print(cabecalho)
    for e in erros:
        print(e)
    if resumo:
        linhas = [f"### {cabecalho}", "", "| Documento | Resultado | Regras reprovadas |", "|---|---|---|"]
        linhas += [f"| `{rel}` | {sit} | {regras or '-'} |" for rel, sit, regras, _ in tabela]
        if erros:
            linhas += ["", *(f"- {e}" for e in erros)]
        Path(resumo).write_text("\n".join(linhas) + "\n", encoding="utf-8")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
