---
tipo: briefing
dominio: editorial
projeto: crpsp-book
estado: pronto-para-execucao
criado: 2026-07-11
executor: a definir (Claude Opus 4.8 / GPT 5.6 Sol / Kimi 2.7-code)
---

# Briefing — Acabamento visual e de acessibilidade do Manual de DH v1

## Objetivo

Fechar as pendências visuais do manual regenerado
(`production/editorial/publicacoes/manual_direitos_humanos/v1/`) mantendo a
conformidade PDF/UA-2 (veraPDF PASS é critério inegociável em TODA tarefa abaixo).

## Leituras obrigatórias

1. `v1/README.md` — arquitetura, build (2× lualatex-dev) e as 4 armadilhas.
2. `editorial/latex_acessivel/book-crpsp_acessivel.sty` (v0.5.0) — seções 2 (eso-pic)
   e 4 (headings/spans); comentários explicam CADA workaround do phase-III.
3. `editorial/latex_acessivel/crpsp-leg.sty` — histórico do bug \list (seção C).
4. Manual publicado de referência: `~/git/editoracao/manual/manpsidh.tex`
   (SOMENTE LEITURA) — `\backgroundsetup` com `fundo_impar.png`/`fundo_par.png`
   alternados por `\ifodd\value{page}`.

## Tarefas

### ~~1. Fundos de página~~ [CONCLUÍDA 2026-07-13]

Implementado no `manual_dh.tex` (do sumário em diante, como no original;
o 1º TODO era `contents={}` vazio — nada a fazer). PNGs copiados de
`~/git/editoracao/manual/` para `v1/`. **Achado do MWE
(`mwe_fundo_esopic.tex`)**: `alt={}` NÃO basta — vira `<Figure>` com Alt
vazio (veraPDF até passa, mas é conteúdo na árvore). O padrão correto é
`\tagstop` + `\tagmcbegin{artifact}` … `\tagmcend` + `\tagstart` em volta
do `\includegraphics` (sem `alt`): zero `<Figure>` na árvore, imagem
dentro de bloco `/Artifact` no stream (verificado com pikepdf), veraPDF
UA-2 PASS no MWE e no manual (395 pp). Original A4 com PNG em tamanho
natural → aqui `width/height=\paperwidth/\paperheight` (mesma proporção).
O exemplo com `alt={}` documentado na seção 2 do book-crpsp_acessivel.sty
segue válido p/ arte decorativa POSICIONADA NO FLUXO; para shipout
background, usar o padrão artifact acima.

### (histórico) 1. Fundos de página (os dois `% TODO fundo eso-pic` no `manual_dh.tex`)

Reproduzir os fundos decorativos do publicado com **eso-pic** (o pacote `background`
é legado/proibido; eso-pic já é carregado pelo pacote na seção 2). Requisitos UA:
- O fundo é DECORATIVO: precisa entrar como **Artifact** na árvore de tags, nunca
  como conteúdo. Com tagging ativo, `\AddToShipoutPictureBG` pode precisar de
  `\tagmcbegin{artifact}`/`\tagmcend` (ou o equivalente do tagpdf da distribuição —
  verificar a API vigente; testar num MWE pequeno ANTES de tocar o manual).
- Imagens: copiar `fundo_impar.png`/`fundo_par.png` do manual publicado para `v1/`.
- Alternância ímpar/par via `\ifodd\value{page}` como no original.
- Validar: veraPDF UA-2 PASS + abrir a árvore de tags e confirmar que o fundo não
  virou `<Figure>` sem alt.

### ~~2. `\LegEmenta` — última minipage da camada Leg~~ [CONCLUÍDA 2026-07-13]

`crpsp-leg.sty` v0.3.0: parágrafo com `\leftskip=6cm` (largura idêntica:
`\boxementa` = `\textwidth-6cm`). Detalhe que morde: `\justifying`
(ragged2e) ZERA `\leftskip` — o `\setlength` tem de vir depois. Par de
.sty recopiado aos 2 deploys; `mwe_leg_completo` (78 pp) e manual
(395 pp) recompilados, veraPDF UA-2 PASS em ambos, visual conferido
(bloco direito idêntico). A camada Leg está SEM minipages.

### (histórico) 2. `\LegEmenta` — última minipage da camada Leg

A ementa ainda usa minipage dupla (offset 6cm) com nota de risco de ordem de
leitura herdada. Trocar por parágrafo com `\leftskip=6cm` (mesma técnica já aplicada
a `\LegParagrafo` — ver seção C do crpsp-leg.sty), preservando o visual (sans,
footnotesize, justificado no bloco direito). Editar a FONTE CANÔNICA
(`editorial/latex_acessivel/crpsp-leg.sty`) e recopiar o par de .sty para os dois
deploys (`v1/` e `caderno_12_corepsi/editorial/templates/`). Recompilar e validar
o manual E o `mwe_leg_completo.tex` (em `editorial/latex_acessivel/desenvolvimento/mwe/`).

### ~~3. Investigar o bug \list × quebra de página~~ [MWE PRONTO 2026-07-13 — issue AGUARDA APROVAÇÃO]

**Causa isolada em MWE mínimo** (`mwe_list_pagebreak_bug.tex`, só book +
`\DocumentMetadata` + description): o gatilho NÃO é `\list` + quebra em
si — é a invocação do ambiente POR CSNAME (`\description`…
`\enddescription`, como fazia o `\LegArtigo` antigo), que pula os env
hooks do tagueamento. Números: csname = 75 pp/3228 overfull; mesmo doc
com `\begin{description}` = ~8 pp/0; sem tagging = ~8 pp/0. `\list` cru
dentro de `\newenvironment` próprio (LegIncisos etc.) é SAUDÁVEL
(testado com itens longos atravessando quebras) — risco rebaixado nos
comentários do .sty. Rascunho de issue pronto em
`briefings/issue-draft-list-csname-tagging.md` — **abrir em
latex3/tagging-project SÓ com aprovação de Angelo**.

### (histórico) 3. Investigar/reportar o bug \list × quebra de página (upstream)

Reproduzível: `mwe_leg_listas.tex` + itens suficientemente longos para a quebra cair
no meio do parágrafo de um item (a versão description do `\LegArtigo` quebrava a
partir do 13º artigo da DUDH — ver comentário na seção C do crpsp-leg.sty).
Produzir um MWE MÍNIMO sem o pacote CRP (só book + \DocumentMetadata + description)
e, se o bug se confirmar em TeX Live/MiKTeX atual, abrir issue no repositório
`latex3/tagging-project` (ou latex2e, conforme orientação lá) com o MWE. Enquanto
não houver correção upstream, `LegIncisos/LegAlineas/LegItens` permanecem com
`\list` — monitorar contagem de páginas em documentos com itens longos.

### 4. Revisão visual sistemática contra o publicado

Página a página (amostragem: capa/paratextos, TOC, um capítulo de prosa, cap. 5
DUDH, CFP 18/2002, créditos): comparar com o PDF publicado e listar divergências
em `v1/revisao-visual.md` com veredicto (aceitar/corrigir). Diferenças JÁ aceitas:
tipografia da camada Leg (hangindent em vez de description), epígrafe adicionada,
ausência de fundos (até a tarefa 1). Ferramenta: `pymupdf` renderiza páginas
(`page.get_pixmap(dpi=110).save(...)`).

## Armadilhas (além das do v1/README.md)

- `\DocumentMetadata` SEMPRE antes de `\documentclass`; `\hypersetup{pdftitle=…}`
  obrigatório (veraPDF 8.11.1-t1 falha sem dc:title).
- O `book-crpsp_acessivel.sty` alterna catcode de `@` por seção (`\makeatletter`/
  `\makeatother` no meio do arquivo) — código novo com `@` interno precisa estar
  entre um par correto.
- Compilar sempre da pasta do documento (fontes com `Path=./`).
- Nada de `git commit` sem pedido explícito do Angelo.

## Critérios de aceitação

veraPDF UA-2 PASS após CADA tarefa; manual visualmente aprovado por Angelo
(tarefa 4 gera a lista de decisão); nenhum warning novo de estrutura no log.
