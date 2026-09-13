#!/bin/sh
# Régua de compilação da linha book e da v2.
#
# Copia crpsp-book/ e legado/book-variantes/ da árvore de trabalho para uma
# pasta temporária, compila cada .tex duas vezes com o motor que ele declara
# (% !TeX program = ...; sem declaração, lualatex) e imprime uma linha TSV por
# arquivo: páginas, objetos de estrutura, erros de tagging e erros fatais.
#
# Uso (de qualquer pasta do repositório):
#   sh crpsp-book/desenvolvimento/verificar.sh                 # MWEs e exemplos v2
#   sh crpsp-book/desenvolvimento/verificar.sh mwe/mwe_minimal.tex v2/exemplo-relatorio.tex
#   TEMPO=300 sh crpsp-book/desenvolvimento/verificar.sh > rodada.tsv
#
# Os caminhos são relativos a crpsp-book/desenvolvimento/. Compara-se uma
# rodada com a linha-base (linha-base.tsv) antes e depois de mexer no tagging:
# mesmo número de objetos e nenhum erro novo. Nada é escrito no repositório.
#
# Requer as fontes do Nextcloud instaladas (ver docker/README.md, "Fontes").
#
# Três MWEs dependem do workbench (WORKBENCH, padrão ~/Documentos/trabalho):
# mwe_leg_completo e mwe_leg_glossario fazem \input{../../../../export/latex/...},
# caminho escrito quando moravam em editorial/latex_acessivel/desenvolvimento/mwe/;
# mwe_fundo_esopic usa o fundo_impar.png do Manual DH. A cópia é montada numa
# altura em que esse caminho relativo resolve, com export/ ligado ao workbench.
set -u

RAIZ=$(git -C "$(dirname "$0")" rev-parse --show-toplevel) || exit 1
TEMPO=${TEMPO:-180}
WORKBENCH=${WORKBENCH:-$HOME/Documentos/trabalho}
TMP=$(mktemp -d "${TMPDIR:-/tmp}/crpsp-verificar.XXXXXX")
trap 'rm -rf "$TMP"' EXIT

# $TMP/r/crpsp-book/desenvolvimento/mwe/../../../../ = $TMP
mkdir -p "$TMP/r/legado" "$TMP/carga"
cp -r "$RAIZ/crpsp-book" "$TMP/r/"
cp -r "$RAIZ/legado/book-variantes" "$TMP/r/legado/"
[ -d "$WORKBENCH/export" ] && ln -s "$WORKBENCH/export" "$TMP/export"
# Nome de carga do pacote canônico, como nos projetos de produção.
cp "$RAIZ/crpsp-book/book-crpsp_acessivel.sty" "$TMP/carga/livros_crp_acessivel_book.sty"
cp "$RAIZ/crpsp-book/crpsp-leg.sty" "$TMP/carga/"
TEXINPUTS=".:$TMP/carga//:$TMP/r/legado/book-variantes//:$WORKBENCH/production/editorial/publicacoes/manuais/manual_direitos_humanos/v1:${TEXINPUTS:-}"
export TEXINPUTS

DEV="$TMP/r/crpsp-book/desenvolvimento"
if [ $# -eq 0 ]; then
    set -- $(cd "$DEV" && ls mwe/*.tex v2/*.tex)
fi

printf 'arquivo\tmotor\tpaginas\tobjetos\terros_tagging\tfatais\tprimeiro_erro\n'
for rel in "$@"; do
    tex="$DEV/$rel"
    if [ ! -f "$tex" ]; then
        printf '%s\t-\t-\t-\t-\t-\tarquivo inexistente\n' "$rel"
        continue
    fi
    dir=$(dirname "$tex"); base=$(basename "$tex" .tex)
    motor=$(grep -m1 -oiE '^%[[:space:]]*!TeX[[:space:]]+program[[:space:]]*=[[:space:]]*[a-z-]+' "$tex" | sed -E 's/.*=[[:space:]]*//')
    motor=${motor:-lualatex}
    estado=""
    for passada in 1 2; do
        ( cd "$dir" && timeout "$TEMPO" "$motor" -interaction=nonstopmode "$base.tex" >/dev/null 2>&1 )
        [ $? -eq 124 ] && estado="tempo esgotado (${TEMPO}s) na passada $passada" && break
    done
    log="$dir/$base.log"
    pags=$(grep -oE 'Output written on .*\(([0-9]+) pages?' "$log" 2>/dev/null | grep -oE '\(([0-9]+)' | tr -d '(')
    objs=$(grep -oE '[0-9]+ structure objects' "$log" 2>/dev/null | tail -1 | grep -oE '^[0-9]+')
    errt=$(grep -cE 'not allowed|text-unit|differ|open structure' "$log" 2>/dev/null)
    fatais=$(grep -c '^! ' "$log" 2>/dev/null)
    prim=${estado:-$(grep -m1 '^! ' "$log" 2>/dev/null | cut -c1-90)}
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$rel" "$motor" "${pags:--}" "${objs:--}" "${errt:-0}" "${fatais:-0}" "$prim"
done
