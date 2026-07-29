---
tipo: issue-draft
destino: https://github.com/latex3/tagging-project/issues/1484
estado: "PUBLICADA em 2026-07-14 (issue #1484, conta cuissi-crp06, aprovação de Angelo) — acompanhar respostas"
criado: 2026-07-13
mwe: editorial/latex_acessivel/desenvolvimento/mwe/mwe_list_pagebreak_bug.tex
---

# Rascunho de issue (inglês, formato do repositório)

**Title:** `\hsize` corruption after page break inside list item when the
environment is invoked via csname form (`\description`…`\enddescription`)
with tagging enabled

## Issue body

### Brief outline of the bug

With `tagging = on` (`testphase = {phase-III}`), a `description`
environment invoked through the **csname form** (`\description` …
`\enddescription`, e.g. from inside a macro) typesets apparently fine
until a **page break falls in the middle of an item's paragraph**. From
that point on, `\hsize` of the continuation lines is corrupted: nearly
every word is typeset as an isolated overfull `\hbox` (one word per
line), and the page total balloons (~10×) with mostly-empty pages until
the end of the document.

The same document with the identical list written as
`\begin{description}` … `\end{description}` typesets normally, so the
trigger appears to be that the env hooks (`env/description/begin` etc.)
the list-tagging code relies on do not fire in the csname form, leaving
the tagging state unbalanced across the page break.

If the csname invocation of environments is considered out of contract
under tagging, a documented error/warning would still be preferable to
the current silent corruption — the failure surfaces far from its cause
(we hit it via a macro wrapping single-item `description`s for statute
articles; the document inflated from ~395 to 3614 pages).

### Minimal example showing the bug

```latex
\DocumentMetadata{
    lang        = en,
    testphase   = {phase-III},
    tagging     = on,
}
\documentclass{book}

\newcommand\filler{Lorem ipsum dolor sit amet, consectetur adipiscing
elit, sed do eiusmod tempor incididunt ut labore et dolore magna
aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
laboris nisi ut aliquip ex ea commodo consequat. }

\begin{document}
\chapter*{List item crossing a page break under tagging}

\newcount\artn
\artn=1
\loop
    \description
    \item[Article \the\artn.] \filler\filler\filler
    \enddescription
    \advance\artn by 1
\ifnum\artn<31 \repeat

\end{document}
```

**Observed:** 75 pages, 3228 `Overfull \hbox` warnings (LuaHBTeX; see
log excerpt below). **Expected:** ~8 pages, no overfulls — which is
what the same document produces if the loop body uses
`\begin{description}` … `\end{description}`, or if `\DocumentMetadata`
is removed.

### Log excerpt (signature)

```
Overfull \hbox (…pt too wide) in paragraph at lines 36--36
Overfull \hbox (…pt too wide) in paragraph at lines 36--36
…  (one warning per word after the first mid-item page break)
```

### Versions

- LaTeX2e <2026-06-01> pre-release-1 (develop 2026-7-10 branch)
- tagpdf 2026-04-24 v1.0b
- LuaHBTeX 1.24.0 (MiKTeX 26.2), `lualatex-dev`
- OS: Windows 11

---

# Notas internas (não copiar para a issue)

- Bissecção de 2026-07-13 (sessão Claude): o gatilho NÃO é `\list` +
  quebra de página em si (como registrado em 11/07), e sim a forma
  csname. `\begin{description}` idêntico é saudável; `\list` cru dentro
  de `\newenvironment` próprio (LegIncisos/LegAlineas/LegItens) também
  (validado com 8 incisos longos atravessando quebras + manual 395 pp).
- Reproduções desta máquina: `mwe_list_pagebreak_bug.tex` (mínimo,
  75 pp/3228 overfull) e `_repro_*`(descartados) com o pacote CRP
  (85 pp/3234 overfull na forma csname; 10 pp/2 na forma \begin).
- Antes de postar: reproduzir também em TeX Live atual se possível
  (o repositório costuma pedir; MiKTeX develop pre-release já basta
  para abrir, mas mencionar a distribuição).
