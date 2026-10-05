#!/bin/sh
# TeX Live enxuto para as classes crpsp-*: infraestrutura + só os pacotes que o
# workspace usa (inventário de 2026-10-05). Sem sudo: instala em $HOME/texlive.
# Uso: sh instalar-texlive-crpsp.sh   (TL_PREFIX=/outro/caminho para mudar o destino)
# Pré-requisitos do sistema: curl, perl, tar, xz. Opcionais: inkscape (pacote
# svg), ghostscript (epstopdf), poppler-utils e veraPDF (verificar.sh).
# Fora do TeX Live, instalar à parte e expor por fontconfig: NEWJUNE e
# Atkinson Hyperlegible Next. Sem elas, relatorio/leg param com erro de fonte.
# Testado em Debian limpo (2026-10-05): ~263 MB; MWEs de book e formulario compilam.
set -eu
PREFIX="${TL_PREFIX:-$HOME/texlive}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

curl -fsSL https://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz | tar -xz -C "$TMP" --strip-components=1
TEXLIVE_INSTALL_PREFIX="$PREFIX" perl "$TMP/install-tl" --scheme=infraonly \
  --no-interaction --no-doc-install --no-src-install

TLBIN="$(echo "$PREFIX"/20*/bin/*)"
PATH="$TLBIN:$PATH"; export PATH
tlmgr option docfiles 0; tlmgr option srcfiles 0

tlmgr install \
  latex latex-bin latex-lab tagpdf luatex lualibs luaotfload luatexbase lua-uni-algos \
  unicode-data l3kernel l3packages tools graphics graphics-def graphics-cfg \
  amsmath amsfonts lm tex-gyre lora fontspec babel babel-portuges hyphen-portuguese \
  hyperref hyperxmp url xurl xcolor colortbl booktabs tabularray tcolorbox tikzfill \
  pgf pgfplots fancyhdr etoolbox geometry eso-pic iftex hyphenat enumitem setspace \
  ragged2e xhfill framed microtype lastpage standalone luatex85 xellipsis svg catchfile \
  multirow pdfcol ncctools titlesec tikz-bpmn adjustbox pdfpages pdflscape needspace \
  pdfrender tocvsec2 ulem siunitx textpos float fancyvrb epstopdf-pkg csquotes \
  biblatex biber abntex2 background sectionbreak colophon changes acronym \
  glossaries-extra fbb gillius flowchart lipsum memoir koma-script tufte-latex xtufte \
  makeindex hypdoc pdftexcmds kvsetkeys kvdefinekeys etexcmds infwarerr ltxcmds

echo
echo "Pronto. Acrescente ao ~/.bashrc:"
echo "  export PATH=\"$TLBIN:\$PATH\""
