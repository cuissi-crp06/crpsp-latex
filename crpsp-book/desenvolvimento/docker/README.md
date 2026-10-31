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
`OSFONTDIR` para ela (testado em 2026-10-19 no Fedora, com a `crpsp-latex:guia`: `luaotfload-tool --find NEWJUNE-REGULAR.OTF` acha o arquivo em `/fontes/NewJune/`; a imagem não vem de registro, então construa-a antes pelo `Containerfile` desta pasta):

```sh
podman --cgroup-manager=cgroupfs run --rm \
  -v "$PWD":/work:Z -v ~/Documentos/trabalho/editorial/fonts:/fontes:ro \
  -e OSFONTDIR=/fontes// -w /work crpsp-latex:dev \
  lualatex -interaction=nonstopmode arquivo.tex
```

## Régua dentro da imagem (`verificar-podman.sh`)

Em máquina sem TeX Live nativo (WSL pessoal, CRP8057) a régua roda dentro da
imagem, com `sh crpsp-book/desenvolvimento/verificar-podman.sh > rodada.tsv`
(argumentos e `TEMPO` seguem para o `verificar.sh`; variáveis `IMAGEM`,
`FONTES`, `MANUAL_DH` e `WORKBENCH` no cabeçalho do script). O fundo do
Manual DH vai para um workbench mínimo em ext4
(`~/.cache/crpsp-verificar/workbench`), as fontes entram em `/fonts:ro` e o
repositório em `/repo:ro`.

`linha-base-podman.tsv` é a linha de base **desta** forma de compilar, gravada em
2026-10-31 sobre a `main` (96c07ca) com a imagem `crpsp-latex:rodada-20261031`
(`podman --cgroup-manager=cgroupfs build -t crpsp-latex:rodada-20261031 -f Containerfile .`,
base `texlive/texlive:latest-small` seguida de `tlmgr update --all`):

| componente | versão |
|---|---|
| LuaHBTeX | 1.24.0 (TeX Live 2026) |
| kernel `lualatex` | LaTeX2e 2026-11-01 (`\fmtversion` 2026-11-01) |
| kernel `lualatex-dev` | LaTeX2e 2026-11-01 pre-release-3 (develop 2026-10-31) |
| `latex-lab` | 2026-06-01a (rev. 80868) |
| `tagpdf` | 1.0h (rev. 80868) |
| `latex-base-dev` | pre-release 3 (rev. 80703) |
| `tlmgr` | rev. 80687 (2026-10-18) |

Duas rodadas seguidas saíram byte a byte idênticas (cerca de 92 s cada).

**Fora da comparação nesta máquina:** `mwe_leg_completo` e `mwe_leg_glossario`
fazem `\input` de `export/latex/` (saída do pipeline de normativas), que não
existe aqui; terminam com erro fatal "File not found" e ficam na TSV só como
registro. `mwe_creditos_titulo_invisivel` também sai com erro fatal
(`crpsp-relatorio.cls` não encontrada) porque o `verificar.sh` não põe
`v2/` no `TEXINPUTS` dos MWEs; é independente da máquina.
Compare a rodada com `linha-base-podman.tsv`, **não** com `linha-base.tsv`
(Fedora, outro `latex-lab`/`tagpdf`): a troca de linha-base é por máquina.

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
