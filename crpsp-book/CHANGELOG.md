# crpsp-book

Linha acessível, sobre a classe `book` com LuaLaTeX, alvo PDF/UA-2.
Convenção de numeração em `editorial/inventario-latex/convencao-versionamento.md`,
no repositório `trabalho`.

O pacote canônico é implantado nos projetos sob o nome `livros_crp_acessivel_book.sty`,
e é esse o nome que ele declara — o nome do arquivo aqui (`book-crpsp_acessivel.sty`)
é do repositório, não da carga.

## 0.5.1 — 2026/08/10

`book-crpsp_acessivel.sty`. Acrescenta o ambiente `NomesDuasColunas`: lista de
nomes em `multicols`, que flui por quantas páginas precisar, no lugar dos pares
de `\parbox{0.49\linewidth}`, que não quebram página e estouram a `\vbox` em
lista longa. Dentro dele `\\` vira `\par`, e cada nome vira um parágrafo próprio
na árvore de tags, na ordem de leitura. No preâmbulo, `\columnsep` de 1em e
`\raggedcolumns`, logo depois da carga do `multicol`, que já existia. Nada foi
removido: o corpo da 0.5.0-beta está inteiro dentro deste.

Trazido em 2026-09-13 da cópia de produção de
`production/editorial/publicacoes/cartilhas/apresentacoes_acessiveis/LaTeX/livros_crp_acessivel_book.sty`,
que é quem escreveu o ambiente, para os créditos institucionais do guia de
apresentações acessíveis. A varredura de 2026-09-12 não a registrou. O corpo é
idêntico verso por verso ao da origem, e só a declaração foi reescrita: a origem
dizia `v0.5.0` de `2026/07/10`, o mesmo rótulo do canônico. A data nova é a da
última gravação do arquivo.

| sha256 (12) da origem | sha256 (12) do blob |
|---|---|
| `d586b3656b4c` | `e37beef89d62` |

**Compila.** O log de 2026-08-14 do guia (MiKTeX, `lualatex`), posterior ao
arquivo, carrega este corpo e usa o ambiente oito vezes: 39 páginas, 1081 objetos
de estrutura, zero erro de tagging. Não foi recompilado no Fedora: o TeX Live da
distribuição não tem `babel-portuges`, `hyphenat`, `xellipsis`, `lastpage`,
`multirow`, `svg` nem `tcolorbox`, e a imagem `crpsp-latex:dev` não está nesta
máquina.

**Sem sufixo de fase**, pelo mesmo motivo do `relatorio-gestao` 0.5.0 em
`crpsp-memoir/`: não está registrado se a edição do guia servida por ele circulou.

### O rótulo `v0.5.0` repetido nas cópias de produção

Havia três corpos declarando `livros_crp_acessivel_book 2026/07/10 v0.5.0`, e o
`\@ifpackagelater` não distingue nenhum deles:

- o canônico, em `editorial/latex_acessivel/` e `editorial/arquivo_latex/crpsp-book/`, que é a 0.5.0-beta daqui;
- o de `manuais/manual_direitos_humanos/v1/` e `gestao/caderno_12_corepsi/editorial/templates/`, **anterior** ao canônico: não tem os dois ramos de `sec-template` por `\@ifpackagelater` de 2026-08-04. Fica fora, porque só está atrás;
- o de `cartilhas/apresentacoes_acessiveis/LaTeX/`, que é esta 0.5.1.

As cópias de produção continuam declarando `v0.5.0`. Corrigir a declaração
delas é mexer no workbench, e fica para quando for decidido.

## 0.5.0-beta — 2026/07/10

`book-crpsp_acessivel.sty`. Variante PDF/UA da linha book, em par com
`crpsp-leg.sty`. Publicações: Caderno 12 CoREPSI e a regeneração do Manual de
Psicologia e Direitos Humanos.

A paleta ainda é fixa no pacote (`crp1`/`crp2`/`crp3`, azul). A direção adotada
daqui em diante é a da linha `desenvolvimento/v2`: paleta definida por
publicação.

### crpsp-leg 0.3.0-beta — 2026/07/13

Camada de legislação acessível. Declarada com `\ProvidesFile`, não
`\ProvidesPackage`, porque é lida via `\input` como módulo-irmão, e não por
`\usepackage`. O argumento opcional é o mesmo nos dois comandos.

## Linha `desenvolvimento/v2` — 0.1.0-alfa

`crpsp-base` (2026/07/03), `guia-crpsp_acessivel` (2026/05/25), `guia-visual`
(2026/07/03), `formulario` (2026/07/03) e `relatorio` (2026/07/29).

`crpsp-base` traz a interface de paleta por publicação: padrões neutros e os
setters `\crpspCorPrincipal`, `\crpspCorSecundaria` e `\crpspCorAcessoria`, com
os apelidos públicos `cor1`, `cor2` e `cor3`. A partir daqui a paleta deixa de
ser propriedade do pacote.

## Etiqueta

A etiqueta `book-v0.5.0` já existe. Depois que esta branch entrar em `main`,
criar as demais sobre o commit de merge:

    git tag book-v0.5.0-beta && git tag leg-v0.3.0-beta
