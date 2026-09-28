#!/usr/bin/env python3
"""Extrai os exemplos da ABNT NBR 6023:2018 e da NBR 10520:2023 como corpus de teste.

Lê os JSON que o normativas-pipeline grava em export/normas/ (no workbench) e
escreve um TSV por norma, uma linha por referência de exemplo:

    id  secao  exemplo  rotulo  classe  texto  origem

- id: <norma>:<seção>:<exemplo><letra>, ex. 6023:7.11.1:3 ou 6023:7.12:1b
  (a letra só aparece quando um exemplo traz mais de uma referência). Onde a
  numeração recomeça dentro da seção, o exemplo leva a série antes:
  6023:8.1.1.3:b.2 (item b da enumeração), 6023:8.1.3:2.1 (segunda série);
- rotulo: essenciais, complementares ou vazio (a norma nem sempre rotula);
- classe: referencia, fragmento (8.4.1, 8.6.1.3, 8.7.1, 9.2) ou citacao (10520);
- origem: json, ou Er1/Er2 quando o texto veio de uma errata.

O texto das normas não entra no repositório; os exemplos, sim (ver a seção 6
do briefing). O JSON tem quatro defeitos do parser que este script remenda:

1. toda linha que começa por número vira nó novo (o "11.262" no meio de um
   exemplo de 7.11.4, o segundo "7.13.3" que é o resto de 7.13.5): um nó cujo
   número não pode suceder o anterior é colado nele;
2. o título de seção de primeiro nível ("9 Ordenação…", "8 Notas") cola no
   fim do nó anterior: cortado;
3. anexos e índice colam no último nó: cortados;
4. as erratas de 2020 não estão aplicadas, embora a ementa diga que estão:
   aplicadas a partir de erratas-6023.json.

O que nenhuma regra resolve (uma frase de regra grudada num exemplo) vai em
ajustes-6023.json, que falha se o trecho a remover deixar de existir.

Uso:
    python3 extrair.py [--normas DIR] [--saida DIR]

DIR padrão: $WORKBENCH/export/normas (WORKBENCH padrão ~/Documentos/trabalho)
e a pasta deste script.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
NORMAS = {
    "6023": "abnt-nbr-6023-2018.json",
    "10520": "abnt-nbr-10520-2023.json",
}

RE_EXEMPLO = re.compile(r"^EXEMPLOS?(?:\s+(\d+))?\s*$")
RE_ROTULO = re.compile(r"^Elementos\s+(essenciais|complementares)\s*$")
RE_TRACO = re.compile(r"^[—–-]\s*$")
RE_NOTA = re.compile(r"^NOTAS?\b")
RE_ENUM = re.compile(r"^([a-z])\)\s*(.*)$")
# Título de seção de primeiro nível colado no texto: "9\t Ordenação das referências".
RE_TITULO_1 = re.compile(r"^\d{1,2}\t")
RE_ANEXO = re.compile(r"^(Anexo [A-Z]|Índice|Bibliografia)\s*$")
# Início provável de referência: palavra em caixa alta (sobrenome, entidade,
# primeira palavra do título) seguida de vírgula, ponto, espaço ou dois-pontos.
# O artigo de uma letra conta com a palavra seguinte: "O QUE", "A GAME".
RE_INICIO_REF = re.compile(r"^(?:\d+ )?(?:[AOÀ] )?[A-ZÀ-Ý][A-ZÀ-Ý'’\-]+(?:[ ,.:;(]|$)")
LARGURA_CHEIA = 88  # linhas de referência quebram perto de 95-105 caracteres


def numero(s):
    return tuple(int(x) for x in s.split(".")) if re.fullmatch(r"\d+(\.\d+)*", s) else None


def sucede(ant, novo):
    """novo pode vir depois de ant na numeração progressiva? Rejeita o número
    que volta (7.13.5 → 7.13.3) ou que salta mais de dois (7.11.6 → 11.262).
    Salto de dois é legítimo: a 6023 não tem nó para a seção 5, só título."""
    if ant is None or novo is None:
        return novo is not None
    if novo <= ant:
        return False
    for a, b in zip(ant, novo):
        if a != b:
            return b - a <= 2
    return True  # filho de ant


def termina_frase(texto):
    linhas = [ln for ln in texto.split("\n") if ln.strip()]
    return not linhas or linhas[-1].rstrip().endswith((".", "]", ")"))


def nos_reparados(dados):
    planos = []

    def walk(n):
        planos.append(n)
        for c in n["filhos"]:
            walk(c)

    for n in dados["estrutura"]:
        walk(n)

    saida = []
    for n in planos:
        if n["tipo"] == "termo":  # o glossário da seção 3 não tem exemplos
            continue
        num = numero(n["numero"])
        if saida and not sucede(numero(saida[-1]["numero"]), num):
            # Defeito 1: a linha "<número> resto" era continuação de um nó
            # anterior. Nem sempre do imediatamente anterior: o "11.262" vem
            # depois de 7.11.6, mas continua 7.11.4, que termina em "Leis
            # 10.927/91 e". Vai para o último nó que termina no meio da frase.
            alvo = next((m for m in reversed(saida) if not termina_frase(m["texto"])), saida[-1])
            alvo["texto"] += "\n" + n["numero"] + " " + n["texto"]
            continue
        saida.append({"numero": n["numero"], "texto": n["texto"]})

    for n in saida:
        linhas = []
        for ln in n["texto"].split("\n"):
            if RE_TITULO_1.match(ln) or RE_ANEXO.match(ln.strip()):
                break  # defeitos 2 e 3
            linhas.append(ln)
        n["texto"] = "\n".join(linhas)
    return saida


def juntar(linhas):
    """Junta linhas quebradas do PDF numa referência só."""
    out = ""
    for ln in linhas:
        ln = re.sub(r"\s+", " ", ln).strip()
        if not ln:
            continue
        if not out:
            out = ln
            continue
        ultimo = out.split(" ")[-1]
        url_aberta = ("://" in ultimo or ultimo.startswith("www.")) and not ln.startswith("Acesso")
        if url_aberta or (out.endswith("-") and not out.endswith(" -")):
            out += ln
        else:
            out += " " + ln
    return out


def separar_referencias(linhas):
    """Um exemplo pode trazer mais de uma referência (9.1, 7.12). Corta quando
    uma linha curta que fecha em ponto é seguida de início de referência."""
    refs, atual = [], []
    visiveis = [ln for ln in linhas if ln.strip()]
    for i, ln in enumerate(visiveis):
        atual.append(ln)
        prox = visiveis[i + 1] if i + 1 < len(visiveis) else None
        if prox is None:
            break
        curta = len(ln.rstrip()) < LARGURA_CHEIA
        fecha = ln.rstrip().endswith((".", "]"))
        if curta and fecha and RE_INICIO_REF.match(prox.strip()):
            refs.append(atual)
            atual = []
    if atual:
        refs.append(atual)
    return refs


def exemplos(no):
    """Gera [serie, exemplo, rotulo, linhas] a partir do texto de um nó.

    A numeração dos exemplos recomeça dentro da mesma seção: a cada item de
    enumeração (8.1.1.3, "a) sobrenomes hispânicos:") ou depois de um
    parágrafo de regra (8.1.3). Cada recomeço abre uma série; a série é a
    letra do item, quando há, ou o número de ordem."""
    blocos, n_ex, serie, n_series, em_nota, enum_aberta = [], None, "", 0, False, False
    for ln in no["texto"].split("\n"):
        s = ln.strip()
        m = RE_EXEMPLO.match(s)
        e = RE_ENUM.match(s)
        if m:
            novo = int(m.group(1) or 1)
            if n_ex is None or novo <= n_ex:
                n_series += 1
                if not serie or not serie.isalpha() or (blocos and blocos[-1][0] == serie):
                    serie = str(n_series)
            n_ex, em_nota, enum_aberta = novo, False, False
            blocos.append([serie, str(n_ex), None, []])
        elif e:
            # Item de enumeração: nomeia a próxima série e não entra no texto.
            serie, n_ex, enum_aberta = e.group(1), None, not e.group(2).strip()
        elif enum_aberta and s.endswith(":"):
            enum_aberta = False  # " c)" com o título na linha seguinte
        elif blocos:
            r = RE_ROTULO.match(s)
            if RE_NOTA.match(s):
                em_nota = True  # a nota vai até o próximo exemplo ou rótulo
            elif RE_TRACO.match(s):
                em_nota = False
            elif em_nota:
                pass
            elif r:
                em_nota = False
                if blocos[-1][3]:  # rótulo novo no meio do exemplo (7.12)
                    blocos.append([blocos[-1][0], blocos[-1][1], None, []])
                blocos[-1][2] = r.group(1)
            else:
                blocos[-1][3].append(ln)
    if len({b[0] for b in blocos}) == 1:
        for b in blocos:
            b[0] = ""
    return blocos


def classe(texto):
    """referencia, ou fragmento: os exemplos de local (8.4.1), data (8.6.1.3)
    e descrição física (8.7.1) mostram um elemento só, e o de 9.2 é o sistema
    numérico, fora do escopo autor-data."""
    return "referencia" if RE_INICIO_REF.match(texto) else "fragmento"


def extrair_6023(dados, erratas, ajustes):
    por_exemplo = {}
    for no in nos_reparados(dados):
        for serie, n_ex, rotulo, corpo in exemplos(no):
            por_exemplo.setdefault((no["numero"], serie, n_ex), []).extend(
                (rotulo, juntar(r)) for r in separar_referencias(corpo)
            )
    linhas_tsv, indice = [], {}
    for (secao, serie, n_ex), refs in por_exemplo.items():
        for k, (rotulo, texto) in enumerate(refs):
            letra = "abcdefghijklmnopqrstuvwxyz"[k] if len(refs) > 1 else ""
            exemplo = f"{serie}.{n_ex}" if serie else n_ex
            linha = [f"6023:{secao}:{exemplo}{letra}", secao, exemplo, rotulo or "", "", texto, "json"]
            linhas_tsv.append(linha)
            indice[(secao, exemplo, letra)] = linha

    for e in erratas["exemplos"]:
        chave = (e["secao"], e["exemplo"], e.get("referencia", ""))
        if chave not in indice:
            sys.exit(f"errata sem exemplo correspondente: {chave}")
        alvo = indice[chave]
        if "rotulo" in e:
            alvo[3] = e["rotulo"]
        if "texto" in e:
            alvo[5] = e["texto"]
        alvo[6] = e["fonte"]
    aplicar_ajustes(linhas_tsv, ajustes)
    for linha in linhas_tsv:
        linha[4] = classe(linha[5])
    return linhas_tsv


def aplicar_ajustes(linhas_tsv, ajustes):
    por_id = {l[0]: l for l in linhas_tsv}
    for a in ajustes["ajustes"]:
        alvo = por_id.get(a["id"])
        if alvo is None or a["remover"] not in alvo[5]:
            sys.exit(f"ajuste não se aplica: {a['id']}")
        alvo[5] = alvo[5].replace(a["remover"], "").strip()


def extrair_10520(dados):
    """Os exemplos da 10520 são trechos de texto com chamadas; saem inteiros.
    Quais chamadas testar, e com que comando, fica no .tex do corpus."""
    linhas_tsv = []
    for no in nos_reparados(dados):
        for serie, n_ex, rotulo, corpo in exemplos(no):
            texto = juntar(corpo)
            exemplo = f"{serie}.{n_ex}" if serie else n_ex
            if texto:
                linhas_tsv.append([f"10520:{no['numero']}:{exemplo}", no["numero"], exemplo,
                                   rotulo or "", "citacao", texto, "json"])
    return linhas_tsv


def main():
    wb = Path(os.environ.get("WORKBENCH", Path.home() / "Documentos/trabalho"))
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--normas", type=Path, default=wb / "export/normas")
    ap.add_argument("--saida", type=Path, default=AQUI)
    a = ap.parse_args()

    ler = lambda p: json.loads(p.read_text(encoding="utf-8"))
    tabelas = {
        "6023": extrair_6023(ler(a.normas / NORMAS["6023"]), ler(AQUI / "erratas-6023.json"), ler(AQUI / "ajustes-6023.json")),
        "10520": extrair_10520(ler(a.normas / NORMAS["10520"])),
    }
    for norma, linhas in tabelas.items():
        destino = a.saida / f"nbr{norma}.tsv"
        # TSV sem aspas nem escape: juntar() já tirou tabulações e quebras.
        with destino.open("w", encoding="utf-8", newline="\n") as f:
            for campos in [["id", "secao", "exemplo", "rotulo", "classe", "texto", "origem"], *linhas]:
                assert not any(c in x for x in campos for c in "\t\n"), campos
                f.write("\t".join(campos) + "\n")
        print(f"{destino.name}: {len(linhas)} linhas", file=sys.stderr)


if __name__ == "__main__":
    main()
