#!/bin/sh
# Régua de compilação (verificar.sh) dentro da imagem podman.
#
# Para máquina sem TeX Live nativo (WSL pessoal, CRP8057): roda o verificar.sh
# dentro de crpsp-latex:rodada-20261031 e repassa os argumentos. A saída é a
# mesma TSV do verificar.sh, em stdout; o resto vai para stderr.
#
# Uso (de qualquer pasta; chamar com sh, nunca ./):
#   sh crpsp-book/desenvolvimento/verificar-podman.sh > rodada.tsv
#   sh crpsp-book/desenvolvimento/verificar-podman.sh mwe/mwe_minimal.tex v2/exemplo-relatorio.tex
#   IMAGEM=crpsp-latex:dev TEMPO=300 sh crpsp-book/desenvolvimento/verificar-podman.sh
#
# Variáveis:
#   IMAGEM     imagem a usar (padrão crpsp-latex:rodada-20261031)
#   FONTES     fontes do Nextcloud, montadas só para leitura em /fonts, com
#              OSFONTDIR=/fonts// (padrão ~/nextcloud/editorial/fonts)
#   MANUAL_DH  pasta do Manual DH de onde sai o fundo do mwe_fundo_esopic
#              (padrão ~/nextcloud/production/editorial/publicacoes/manuais/
#              manual_direitos_humanos/v1); só fundo_impar.png e fundo_par.png
#              são copiados
#   WORKBENCH  workbench mínimo em ext4 (padrão ~/.cache/crpsp-verificar/workbench),
#              remontado a cada execução e montado só para leitura. Nunca se
#              monta o mount rclone como volume de trabalho: o podman tem defeito
#              com volumes dele. As fontes são a exceção (somente leitura).
#   TEMPO      limite por passada, em segundos (repassado ao verificar.sh)
#
# Sem export/ no WORKBENCH: mwe_leg_completo e mwe_leg_glossario fazem
# \input{export/latex/...} e saem com erro fatal ("File not found") nesta
# máquina. Ficam na TSV, mas fora da comparação com a linha-base.
#
# O repositório entra em /repo:ro e o verificar.sh o copia para uma pasta
# temporária do container, então nada é escrito nele. Como o container não
# enxerga o .git (um worktree aponta para fora), a raiz vai pela variável RAIZ.
set -eu

IMAGEM=${IMAGEM:-crpsp-latex:rodada-20261031}
FONTES=${FONTES:-$HOME/nextcloud/editorial/fonts}
MANUAL_DH=${MANUAL_DH:-$HOME/nextcloud/production/editorial/publicacoes/manuais/manual_direitos_humanos/v1}
WORKBENCH=${WORKBENCH:-$HOME/.cache/crpsp-verificar/workbench}

RAIZ=$(git -C "$(dirname "$0")" rev-parse --show-toplevel)

[ -d "$FONTES/NewJune" ] || { echo "verificar-podman: sem $FONTES/NewJune" >&2; exit 1; }

# Workbench mínimo: o fundo do Manual DH, copiado para ext4. Lê por Python
# porque cp/ls no mount às vezes devolvem Input/output error (cache).
DESTINO="$WORKBENCH/production/editorial/publicacoes/manuais/manual_direitos_humanos/v1"
rm -rf "$WORKBENCH/production"
mkdir -p "$DESTINO"
for f in fundo_impar.png fundo_par.png; do
    python3 -c 'import pathlib, sys; pathlib.Path(sys.argv[2]).write_bytes(pathlib.Path(sys.argv[1]).read_bytes())' \
        "$MANUAL_DH/$f" "$DESTINO/$f" \
        || { echo "verificar-podman: não consegui copiar $f de $MANUAL_DH" >&2; exit 1; }
done

exec podman --cgroup-manager=cgroupfs run --rm \
    -v "$RAIZ":/repo:ro \
    -v "$FONTES":/fonts:ro \
    -v "$WORKBENCH":/workbench:ro \
    -e OSFONTDIR=/fonts// -e RAIZ=/repo -e WORKBENCH=/workbench \
    -e TEMPO="${TEMPO:-180}" \
    -w /tmp "$IMAGEM" \
    sh /repo/crpsp-book/desenvolvimento/verificar.sh "$@"
