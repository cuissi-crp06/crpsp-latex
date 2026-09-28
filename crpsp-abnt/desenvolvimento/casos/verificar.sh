#!/bin/sh
# Compila casos.tex com o crpsp-abnt e compara com esperado.txt:
# - as chamadas;
# - as referências, uma por linha, na ordem da lista (a página é larga para
#   cada uma caber numa linha);
# - o número de links: um por obra citada (11, nas dez chamadas), mais os de
#   DOI e URL da lista (3).
# - a árvore de tags (show-pdf-tags), reduzida ao esqueleto: um elemento de
#   estrutura por linha, com o nome mapeado e a profundidade, sem texto nem
#   número de objeto. Compara com arvore.txt.
# Com o veraPDF no PATH ou em ~/verapdf, valida também o PDF/UA-2.
#
#   sh verificar.sh [pasta-de-trabalho]
set -eu
AQUI=$(cd "$(dirname "$0")" && pwd)
PACOTE=$(cd "$AQUI/../.." && pwd)
TMP=${1:-$(mktemp -d)}
mkdir -p "$TMP"
cp "$AQUI/casos.tex" "$AQUI/casos.bib" "$TMP/"
cd "$TMP"
export TEXINPUTS="$PACOTE//:"
lualatex -interaction=nonstopmode casos.tex >/dev/null || true
biber --quiet casos >/dev/null
lualatex -interaction=nonstopmode casos.tex >/dev/null || true
lualatex -interaction=nonstopmode casos.tex >/dev/null
pdftotext -layout casos.pdf - |
  sed -e 's/^ *//' -e 's/ \{2,\}/ /g' -e 's/\. \. \./.../g' -e 's/…/.../g' |
  sed -e 's/ *$//' -e 's/\f//g' |
  awk '/@@chamadas@@/{f=1; next} /@@fim@@/{f=2; next}
       f==2 && /^Referências$/ {next}
       f && NF {print}' > obtido.txt
echo "links: $(grep -c '/Subtype */Link' casos.pdf)" >> obtido.txt
if diff -u "$AQUI/esperado.txt" obtido.txt; then echo "casos: igual"; else echo "casos: DIFERE"; st=1; fi
show-pdf-tags casos.pdf | python3 -c '
import re, sys
for linha in sys.stdin:
    m = re.match(r"^([\s│├└┝━─]*?)[├└]─(.+) \(https?://[^)]*\):$", linha.rstrip())
    if m:
        nome = m.group(2).split(" / ")[-1]
        print("  " * (len(m.group(1)) // 2) + nome)
' > arvore.txt
if diff -u "$AQUI/arvore.txt" arvore.txt; then echo "árvore de tags: igual"; else echo "árvore de tags: DIFERE"; st=1; fi
VERA=$(command -v verapdf || echo "$HOME/verapdf/verapdf")
if [ -x "$VERA" ]; then
  if "$VERA" --flavour ua2 casos.pdf | grep -q 'isCompliant="true"'; then
    echo "veraPDF UA-2: passa"
  else
    echo "veraPDF UA-2: FALHA"; st=1
  fi
fi
exit ${st:-0}
