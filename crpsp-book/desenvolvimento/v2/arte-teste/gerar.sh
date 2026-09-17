#!/bin/sh
# Regera a arte de teste da variante `externo`. Ver o cabeçalho de
# gerar-arte-teste.tex. Exige o TeX Live upstream no PATH.
set -eu
cd "$(dirname "$0")"
for arte in topo pe capa; do
    lualatex -interaction=nonstopmode -jobname="saida-$arte" \
        "\\def\\ARTE{$arte}\\input{gerar-arte-teste.tex}" >/dev/null
done
mv saida-topo.pdf faixa-topo.pdf
mv saida-pe.pdf   faixa-pe.pdf
mv saida-capa.pdf capa.pdf
rm -f saida-*.aux saida-*.log
echo "arte de teste regerada:"
for f in faixa-topo.pdf faixa-pe.pdf capa.pdf; do
    printf '  %-16s %s\n' "$f" "$(pdfinfo "$f" | sed -n 's/^Page size: *//p')"
done
