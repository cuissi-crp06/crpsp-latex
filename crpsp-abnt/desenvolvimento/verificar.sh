#!/bin/sh
# Régua do crpsp-abnt. Rodar depois de mexer no estilo e depois de todo
# `tlmgr update`: o estilo sobrepõe macros internas do abnt.bbx, e o upstream
# pode mudar por baixo (briefing, seção 6).
#
# 1. O corpus da 6023:2025 (trilha, jurisprudência e demais: 287 exemplos) e
#    as 29 chamadas da 10520:2023, medidos por corpus/medir.py com o PDF
#    tagueado e comparados, entrada por entrada, com a linha-base da versão
#    (corpus/medida-crpsp-abnt-<versão>*.tsv) por corpus/comparar.py. Compara
#    texto normalizado, não pixels.
# 2. Cada PDF do corpus no veraPDF UA-2.
# 3. Os casos (casos/verificar.sh): texto, links, árvore de tags e veraPDF.
#
#   sh verificar.sh [pasta-de-trabalho]
#   BASE=0.3.0 sh verificar.sh        # outra linha-base
#
# A versão da linha-base vem do \ProvidesFile do crpsp-abnt.bbx. Sai 1 se
# qualquer texto obtido mudar, se um PDF falhar no veraPDF ou se um caso
# divergir. Melhora também sai 1: a linha-base nova se grava de propósito
# (corpus/DIVERGENCIAS.md, "Régua"). Nada é escrito no repositório.
set -u
AQUI=$(cd "$(dirname "$0")" && pwd)
PACOTE=$(cd "$AQUI/.." && pwd)
C="$AQUI/corpus"
TMP=${1:-$(mktemp -d "${TMPDIR:-/tmp}/crpsp-abnt-regua.XXXXXX")}
mkdir -p "$TMP"
BASE=${BASE:-$(sed -n '1s/.* v\([0-9.]*\)-.*/\1/p' "$PACOTE/crpsp-abnt.bbx")}
export TEXINPUTS="$PACOTE//:"
VERA=$(command -v verapdf || echo "$HOME/verapdf/verapdf")
[ -x "$VERA" ] || echo "veraPDF ausente: o PDF/UA-2 não será validado"
echo "linha-base: $BASE; trabalho em $TMP"
st=0

# medir RÓTULO BIB SUFIXO [opções do medir.py]
medir() {
  rot=$1; bib=$2; base="$C/medida-crpsp-abnt-$BASE$3.tsv"; shift 3
  if ! python3 "$C/medir.py" "$C/$bib" --estilo crpsp-abnt --tagueado \
       --pasta "$TMP/$rot" "$@" > "$TMP/$rot.tsv" 2> "$TMP/$rot.err"; then
    echo "$rot: a medida falhou (ver $TMP/$rot.err)"; st=1; return
  fi
  if [ -f "$base" ]; then
    python3 "$C/comparar.py" "$base" "$TMP/$rot.tsv" --rotulo "$rot" || st=1
  else
    echo "$rot: sem linha-base ($base)"; st=1
  fi
  if [ -x "$VERA" ]; then
    if "$VERA" --flavour ua2 "$TMP/$rot/medir.pdf" | grep -q 'isCompliant="true"'; then
      echo "$rot: veraPDF UA-2 passa"
    else
      echo "$rot: veraPDF UA-2 FALHA"; st=1
    fi
  fi
}

medir trilha trilha-6023.bib ""
medir jurisprudencia jurisprudencia-6023.bib -jurisprudencia
medir demais demais-6023.bib -demais
medir chamadas trilha-10520.bib -chamadas --chamadas "$C/chamadas-10520.tsv"
sh "$AQUI/casos/verificar.sh" "$TMP/casos" || st=1

[ $st -eq 0 ] && echo "régua: igual à linha-base" || echo "régua: DIFERE"
exit $st
