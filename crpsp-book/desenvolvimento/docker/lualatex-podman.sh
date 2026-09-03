#!/bin/sh
# Compila um .tex dentro do container crpsp-latex:dev.
# Uso: ./lualatex-podman.sh <arquivo.tex> [-- <args extras de lualatex>]
# O diretorio atual (onde o script eh chamado) eh montado em /work.
set -eu
exec podman --cgroup-manager=cgroupfs run --rm -v "$PWD":/work:Z -w /work crpsp-latex:dev \
  lualatex -interaction=nonstopmode -halt-on-error "$@"
