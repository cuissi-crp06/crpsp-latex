# Ambiente LaTeX reprodutível (podman)

Imagem baseada em `texlive/texlive:latest-small` (TeX Live 2026, atualizado em
abril/2026 — cobre a janela de mudanças no `latex-lab` mencionada no briefing).
Pacotes extras são adicionados ao `Containerfile` via `tlmgr install` conforme
forem necessários; a lista atual cobre o que o briefing
`briefing-crpsp-guia_visual.md` já antecipa.

## Build

```sh
cd editorial/latex_acessivel/desenvolvimento/docker
podman --cgroup-manager=cgroupfs build -t crpsp-latex:dev -f Containerfile .
```

(`--cgroup-manager=cgroupfs` é necessário neste ambiente: rootless podman sem
sessão systemd de usuário/lingering falha com `sd-bus call: Permission denied`
sem essa flag.)

## Compilar um documento

```sh
cd <pasta do .tex>
sh /caminho/para/lualatex-podman.sh arquivo.tex
```

**Importante:** chame sempre com `sh lualatex-podman.sh ...`, nunca
`./lualatex-podman.sh`. A pasta do projeto está montada via `rclone` (FUSE)
por trás do Nextcloud, e esse backend não preserva o bit de execução — o
`chmod +x` não sobrevive, e a execução direta falha com
`bad interpreter: Permission denied`.

## Fontes

Desde 2026-09-13 a **New June não está no git**: é proprietária, e a pasta
`mwe/` guarda só a Lora (OFL). O pacote da linha book a carrega pelo nome do
arquivo (`NEWJUNE-REGULAR.OTF` etc.), sem `Path`, então basta que o motor a
encontre. A origem é `editorial/fonts/NewJune/`, no Nextcloud.

**Linux, motor local** — expor a pasta como fonte do usuário e reindexar:

```sh
mkdir -p ~/.local/share/fonts
ln -s ~/Documentos/trabalho/editorial/fonts ~/.local/share/fonts/crpsp
fc-cache -f ~/.local/share/fonts && luaotfload-tool --update
luaotfload-tool --find NEWJUNE-REGULAR.OTF   # deve responder com o caminho
```

**Windows (MiKTeX)** — instalar os `.OTF` de `editorial\fonts\NewJune\` para o
usuário (botão direito → *Instalar*), e rodar `luaotfload-tool --update`.

**Podman** — a imagem não vê as fontes do usuário. Montar a pasta e apontar o
`OSFONTDIR` para ela (ainda não testado com a imagem, que não está no Fedora):

```sh
podman --cgroup-manager=cgroupfs run --rm \
  -v "$PWD":/work:Z -v ~/Documentos/trabalho/editorial/fonts:/fontes:ro \
  -e OSFONTDIR=/fontes// -w /work crpsp-latex:dev \
  lualatex -interaction=nonstopmode arquivo.tex
```

## Pacote adicional sob demanda

Se um erro apontar pacote faltando:

```sh
podman --cgroup-manager=cgroupfs run --rm crpsp-latex:dev tlmgr install <pacote>
```

Depois de confirmado que resolve, adicionar `<pacote>` à lista no
`Containerfile` e rebuildar, para que fique fixado na imagem.

## Validação feita (Sprint 0)

- `lualatex --version` → LuaHBTeX 1.24.0 (TeX Live 2026).
- `tlmgr --version` → revisão 2026-04-06.
- `\DocumentMetadata{..., testphase={phase-III}}` compila **sem erros e sem
  warning de testphase ignorado** — `tagpdf` gera a estrutura de tags
  normalmente (ParentTree, StructElems, Root etc.). Teste em
  `/tmp/claude-*/scratchpad/phase3test/test.tex` (fora do repo).
- PDF gerado começa com `%PDF-2.0` — confirma `pdfversion=2.0` aplicado.

**Conclusão:** phase-III está funcional neste TeX Live 2026. O Sprint 5
(tagging PDF/UA-2) pode prosseguir sem bloqueio.
