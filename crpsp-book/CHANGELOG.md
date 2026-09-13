# crpsp-book

Linha acessível, sobre a classe `book` com LuaLaTeX, alvo PDF/UA-2.
Convenção de numeração em [`CONVENCAO-VERSIONAMENTO.md`](../CONVENCAO-VERSIONAMENTO.md).

O pacote canônico é implantado nos projetos sob o nome `livros_crp_acessivel_book.sty`,
e é esse o nome que ele declara — o nome do arquivo aqui (`book-crpsp_acessivel.sty`)
é do repositório, não da carga.

## Renumeração de 2026-09-13

Três corpos diferentes declaravam `livros_crp_acessivel_book 2026/07/10 v0.5.0`,
e o `\@ifpackagelater`, que só compara a data, não distinguia nenhum deles. Este
repositório piorou o caso: rotulou `0.5.0-beta` o corpo do **meio**, e o PR #4
chamou de 0.5.1 o terceiro. A série agora segue a ordem em que foram escritos,
com a fase dada pela circulação da publicação:

| versão | data | corpo (sha256 12) | primeiro commit | cópias de produção |
|---|---|---|---|---|
| 0.5.0-alfa | 2026/07/10 | `f7e879cef661` | `c9d1450` | `manuais/manual_direitos_humanos/v1/`, `gestao/caderno_12_corepsi/editorial/templates/` |
| 0.5.1-alfa | 2026/08/04 | `4251e7c15c0f` | `c194d1b` | `editorial/latex_acessivel/`, `editorial/arquivo_latex/crpsp-book/` |
| 0.5.2-beta | 2026/08/10 | `1bd79a0134a0` | `76cca00` | `cartilhas/apresentacoes_acessiveis/LaTeX/` |

As cópias de produção tiveram a declaração corrigida no mesmo dia; os corpos
não foram tocados.

## 0.5.2-beta — 2026/08/10

`book-crpsp_acessivel.sty`. Acrescenta o ambiente `NomesDuasColunas`: lista de
nomes em `multicols`, que flui por quantas páginas precisar, no lugar dos pares
de `\parbox{0.49\linewidth}`, que não quebram página e estouram a `\vbox` em
lista longa. Dentro dele `\\` vira `\par`, e cada nome vira um parágrafo próprio
na árvore de tags, na ordem de leitura. No preâmbulo, `\columnsep` de 1em e
`\raggedcolumns`, logo depois da carga do `multicol`, que já existia. Nada foi
removido: o corpo da 0.5.1-alfa está inteiro dentro deste.

Trazido em 2026-09-13 da cópia de produção de
`production/editorial/publicacoes/cartilhas/apresentacoes_acessiveis/LaTeX/livros_crp_acessivel_book.sty`,
que é quem escreveu o ambiente, para os créditos institucionais do guia de
apresentações acessíveis. A varredura de 2026-09-12 não a registrou. O corpo é
idêntico verso por verso ao da origem, e só a declaração foi reescrita.

| sha256 (12) da origem | sha256 (12) do blob |
|---|---|
| `d586b3656b4c` | `618f08928891` |

(O blob do PR #4, com a declaração `v0.5.1`, era `e37beef89d62`.)

**Compila.** O log de 2026-08-14 do guia (MiKTeX, `lualatex`), posterior ao
arquivo, carrega este corpo e usa o ambiente oito vezes: 39 páginas, 1081 objetos
de estrutura, zero erro de tagging.

**Beta** porque o guia circulou fora do CRP SP.

## 0.5.1-alfa — 2026/08/04

A rodada de 2026-08-04 (ver `ESTADO ATUAL.md`), provocada pelo `monitor_ctan.py`:

- **`sec-template`** — o upstream renomeou as chaves do template `heading` na v0.9g (`after-penalty-sep` → `after-penalty-vspace`, `after-sep` → `after-vspace`, `decls` → `heading-decls`, instância `display` → `chapter`). Com as chaves velhas a identidade visual do capítulo era ignorada em silêncio. O pacote passa a trazer os dois ramos, por `\@ifpackagelater{latex-lab-testphase-sec-template}{2026/05/25}`, porque a linha tem dois motores (podman TL 2026 e MiKTeX). Ver WA-01.
- **`\TOCAcessivel`** vira alias deprecado de `\tableofcontents`: o `latex-lab-testphase-toc` v0.85k corrigiu o `/T (Sumário)`. Ver WA-02.

84 versos entram e 21 saem em relação à 0.5.0-alfa. Nenhuma publicação que
tenha circulado é comprovadamente servida por este corpo, e daí o `alfa`.

## 0.5.0-alfa — 2026/07/10

`book-crpsp_acessivel.sty`. Variante PDF/UA da linha book, em par com
`crpsp-leg.sty`. Publicações: Caderno 12 CoREPSI, que está pausado, e a
regeneração do Manual de Psicologia e Direitos Humanos, que não circulou.
Até 2026-09-13 esta entrada se chamava 0.5.0-beta.

A paleta ainda é fixa no pacote (`crp1`/`crp2`/`crp3`, azul). A direção adotada
daqui em diante é a da linha `desenvolvimento/v2`: paleta definida por
publicação.

### crpsp-leg 0.3.0-beta — 2026/07/13

Camada de legislação acessível. Declarada com `\ProvidesFile`, não
`\ProvidesPackage`, porque é lida via `\input` como módulo-irmão, e não por
`\usepackage`. O argumento opcional é o mesmo nos dois comandos. Beta porque o
mesmo corpo serve o guia de apresentações acessíveis, que circulou.

## Linha `desenvolvimento/v2` — 0.1.0-alfa

`crpsp-base` (2026/07/03), `guia-crpsp_acessivel` (2026/05/25), `guia-visual`
(2026/07/03), `formulario` (2026/07/03) e `relatorio` (2026/07/29).

`crpsp-base` traz a interface de paleta por publicação: padrões neutros e os
setters `\crpspCorPrincipal`, `\crpspCorSecundaria` e `\crpspCorAcessoria`, com
os apelidos públicos `cor1`, `cor2` e `cor3`. A partir daqui a paleta deixa de
ser propriedade do pacote.

## Etiquetas

| etiqueta | commit | observação |
|---|---|---|
| `book-v0.5.0` | `273d412` | anterior à renumeração: marca o estado de 2026-09-03, cujo corpo é a **0.5.1-alfa** |
| `book-v0.5.0-alfa` | `940a787` | o arquivo ali ainda declara `v0.5.0` |
| `book-v0.5.1-alfa` | `e2eb35f` | o arquivo ali declara `v0.5.0-beta` |
| `book-v0.5.2-beta` | merge do PR que traz esta renumeração | primeira em que declaração e etiqueta coincidem |
| `leg-v0.3.0-beta` | `e2eb35f` | |

As etiquetas `book-v0.5.0-beta` e `book-v0.5.1`, criadas em 2026-09-13 com a
numeração antiga, foram apagadas no mesmo dia, junto com `memoir-v0.5.0`. Num
clone que as tenha buscado, apagar só essas três: `git tag -d book-v0.5.0-beta book-v0.5.1 memoir-v0.5.0`.
