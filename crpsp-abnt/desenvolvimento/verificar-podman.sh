#!/bin/sh
# Régua do crpsp-abnt (verificar.sh) dentro da imagem podman.
#
# Para máquina sem TeX Live nativo (WSL pessoal, CRP8057): roda o verificar.sh
# dentro de crpsp-latex:rodada-20261031-abnt e repassa os argumentos. Imagem:
# docker/Containerfile (a fixa da rodada, mais biblatex-abnt, pdftotext e o
# show-pdf-tags).
#
# Uso (de qualquer pasta; chamar com sh, nunca ./):
#   sh crpsp-abnt/desenvolvimento/verificar-podman.sh
#   BASE=0.3.0 sh crpsp-abnt/desenvolvimento/verificar-podman.sh
#   SAIDA=$HOME/abnt-saida sh crpsp-abnt/desenvolvimento/verificar-podman.sh
#
# Variáveis:
#   IMAGEM   imagem a usar (padrão crpsp-latex:rodada-20261031-abnt)
#   VERAPDF  instalação do veraPDF, montada só para leitura (padrão ~/verapdf);
#            o Java vem da imagem
#   RAIZ     raiz do repositório a medir (padrão: a deste script); serve para
#            medir uma versão antiga extraída com `git archive`
#   SAIDA    pasta do host onde ficam os PDFs, TSVs e logs da passada (padrão:
#            só o container, descartada); o verificar.sh sai 1 se a régua diferir
#   BASE     linha-base (repassada ao verificar.sh; padrão, a versão do .bbx)
#
# O repositório entra em /repo:ro e nada é escrito nele.
set -eu

IMAGEM=${IMAGEM:-crpsp-latex:rodada-20261031-abnt}
VERAPDF=${VERAPDF:-$HOME/verapdf}
RAIZ=${RAIZ:-$(git -C "$(dirname "$0")" rev-parse --show-toplevel)}

[ -d "$VERAPDF/bin" ] || echo "verificar-podman: sem $VERAPDF; o PDF/UA-2 não será validado" >&2

SAIDA_OPC=""
if [ -n "${SAIDA:-}" ]; then
    mkdir -p "$SAIDA"
    SAIDA_OPC="-v $SAIDA:/saida"
    set -- /saida/trabalho
fi
[ -z "${BASE:-}" ] || BASE_OPC="-e BASE=$BASE"

# shellcheck disable=SC2086
exec podman --cgroup-manager=cgroupfs run --rm \
    -v "$RAIZ":/repo:ro \
    -v "$VERAPDF":/root/verapdf:ro \
    $SAIDA_OPC ${BASE_OPC:-} \
    -w /tmp "$IMAGEM" \
    sh /repo/crpsp-abnt/desenvolvimento/verificar.sh "$@"
