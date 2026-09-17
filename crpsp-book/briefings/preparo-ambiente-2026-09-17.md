---
tipo: preparo
dominio: editorial
projeto: crpsp-book
criado: 2026-09-17
---

# Preparo do ambiente para escrever as classes

Sessão de 17/09/2026, no Fedora. Alinha a máquina ao estado atual do LaTeX e
registra o que a consulta à documentação e às issues do upstream muda no
desenho da `crpsp-livro.cls` e da revisão da `crpsp-relatorio.cls`.

## 1. O que faltava na máquina

| Lacuna | Situação |
|---|---|
| `docfiles = 0` e `srcfiles = 0` | Nenhum manual e nenhum `.dtx` instalados: 4,8 GB de runtime contra 8,2 MB de doc. Escrever classe tagueada assim é trabalhar de memória |
| 37 pacotes atrasados | Incluindo todo o núcleo dev, da pre-release 1 para a 2 |
| veraPDF ausente | O critério de aceitação do briefing do Manual de DH era inverificável aqui |
| Duas ferramentas novas ignoradas | `latex-tagging-status` e `show-pdf-tags`, instaladas e desconhecidas do projeto |

Corrigido nesta sessão: `docfiles` e `srcfiles` ligados e o `scheme-full`
reinstalado com ambos; `tlmgr update --all --backup` (o backup é o caminho de
volta); **veraPDF 1.30.2** em `~/verapdf`, fora do workbench, com o perfil
`ua2`.

## 2. A issue #1484 derruba uma premissa nossa

Fechada em **08/08/2026**. David Carlisle e Frank Mittelbach, sobre o
`\description` … `\enddescription` sem grupo:

> "for me `\description ... \enddescription` without appropriate grouping is
> (and always was) unsupported usage"

> "If I add the missing group then it runs without error and no overfull box
> warnings"

⚠️ **O `ESTADO ATUAL.md` registra o contrário** — que o `\LegArtigo` usa
`\hangindent` porque "contorna o bug de `\hsize` na quebra de página". **Não há
bug.** Há uso não suportado, e o conserto suportado é acrescentar o grupo. A
nota precisa ser corrigida, e isso reabre a possibilidade de simplificar o
`crpsp-leg.sty`.

O `mwe_list_pagebreak_bug.tex` da régua é a reprodução disso, hoje listado como
"erro esperado".

Da mesma issue vem a frase que originou a pendência 1: *"you should not use the
`testphase` key which was an earlier syntax predating the introduction of
`tagging=on`"*.

## 3. `\EditInstance` em vez de `\DeclareInstance` — o achado de desenho

A issue **#1494** (fechada em 25/07/2026) usa `\EditInstance{heading}{section}`
para mudar só as chaves que interessam. O `\EditInstance` está no kernel
(`latex.ltx`).

O `book-crpsp_acessivel.sty:425-470` faz o oposto: **redeclara a instância
inteira**, repetindo chaves que são puro padrão do upstream. Comparando com o
que o `latex-lab-testphase-sec-template.sty` já define:

| Chave | Upstream | A nossa |
|---|---|---|
| `name`, `level`, `placement` | define | **repete igual** |
| `after-penalty-vspace`, `after-vspace` | define | **repete igual** |
| `mark-cmd`, `contents-extra` | define | **repete igual** |
| `prefix` | `\@chapapp` | não usa — junta tudo em `number-format` |
| `number-format` | `\thechapter` | `\@chapapp\space\thechapter` |
| `heading-decls` | `\raggedright\parindent0pt\bfseries\huge` | acrescenta `\sffamily` |
| `number-decls`, `title-decls` | define | muda a cor |

**Só três chaves mudam de fato.** Repetir as outras é o que obriga a classe a
acompanhar renomeação de chave do upstream — e é exatamente a causa do ramo
duplo do `\@ifpackagelater{...}{2026/05/25}`.

Com `\EditInstance` nomeando só `heading-decls`, `number-decls` e `title-decls`:

- some a dependência das chaves renomeadas, e com ela **metade da pendência 4**;
- melhorias do upstream chegam sozinhas;
- o `prefix = \@chapapp` volta a ser usado como chave própria, que é o padrão
  semântico atual — hoje a nossa classe funde prefixo e número num campo só.

⚠️ O terceiro estado continua necessário: sem o módulo, não há instância para
editar. Mas passa a ser **um** `\@ifpackageloaded` em volta de um bloco curto,
em vez de dois blocos de vinte linhas.

## 4. O orçamento de pacotes das classes

Do `latex-tagging-status`, dado do upstream:

| Estado | Pacotes |
|---|---|
| **Incompatível** | `tabularray`, `titlesec`, **`pdfpages`** |
| Parcial | `tcolorbox`, `enumitem`, `eso-pic`, `hyperref`, `svg`, `ragged2e` |
| Compatível | `fancyhdr`, `geometry`, `fontspec`, `xcolor`, `graphicx`, `setspace`, `longtable`, `booktabs`, `microtype`, `hyphenat`, `extdash`, `xurl` |
| Não verificado | `babel` |

Três consequências:

- **`pdfpages` é incompatível e ninguém tinha notado.** A capa do Guia de
  Apresentações Acessíveis entra por `\includepdf[pages=1]{Capa_baixa.pdf}`. As
  classes novas precisam de outro caminho para capa em PDF.
- `eso-pic` é parcial, e é o mecanismo da decoração de fundo que `manual` e
  `cartilha` vão usar nas margens.
- `ragged2e` é parcial, e acabou de entrar por decisão de alinhamento.

A chave `check-tagging-status = listfiles` no `\DocumentMetadata` emite esse
relatório por documento. Entra no desenvolvimento das classes.

## 5. O manual do `sec-template`, que não existia nesta máquina

52 páginas, agora em `texdoc latex-lab-sec-template`. Dois trechos decidem o
desenho das classes.

**A via documentada é editar, não redeclarar:**

> "It is possible to change heading commands by editing the instance they use."

**E `\@startsection` cai numa camada de compatibilidade.** O pacote `book` define
as seções por `\@startsection` (`livros_crp_acessivel_book.sty:579`). O manual
diz que esses comandos passam a criar instâncias em tempo de execução, com nome
`<arg>-@startsection`, e que isso traz duas limitações: só dá para editá-las
**depois do primeiro uso** do comando, e **não é possível ter dois comandos de
mesmo nível**, porque exigiriam duas instâncias de mesmo nome.

Para classes novas isso é escolha de partida: definir os títulos pela interface
nova, não por `\@startsection`.

**O procedimento de trabalho** que o manual documenta:

```latex
\section{test}          % preciso, para a instância existir
\ShowInstanceValues{heading}{section-@startsection}
\ShowInstanceValues{headformat}{section-@startsection}
```

Despeja no log os valores correntes da instância. É como descobrir o que editar
sem copiar o bloco inteiro do upstream.

**Uma justificativa nossa venceu.** O `changes.txt` do `latex-lab` registra em
**2026-05-23**: *"latex-lab-sec-template.dtx: remove `\normalcolor` from heading
templates (tagging/1215)"*. O `book-crpsp_acessivel.sty:393-405` traz um
comentário longo explicando por que a cor tem de ir em `title-decls` e não em
`decls` — porque o `headformat/display` executava `\normalfont \normalcolor` e
resetava a cor. **Esse `\normalcolor` saiu.** A restrição precisa ser
reconferida antes de virar regra nas classes novas.

## 6. Resultado da atualização, medido

`tlmgr update --self`, `update --all --backup` e reinstalação com doc e fonte:
as três etapas com saída 0. O TeX Live foi de 4,8 GB para 11 GB — 4,9 GB de
documentação e 471 MB de fontes que antes não existiam aqui.

| Pacote | Antes | Depois |
|---|---|---|
| `latex-base-dev`, `latex-lab-dev` | pre-release 1 (79901) | **pre-release 2 (80282)** |
| `latex-tagging-status` | 80187 | 80289 |
| `show-pdf-tags` | 1.5 (77604) | **1.6 (80250)** |
| `latex-lab`, `tagpdf` | 2026-06-01a, 1.0e | sem mudança |

### A régua mudou, e a mudança é benigna

| | Objetos antes | Depois | Δ |
|---|---|---|---|
| `mwe_acessivel_book` | 131 | 126 | −5 |
| `mwe_leg_completo` | 1866 | 1863 | −3 |
| `mwe_leg_glossario` | 99 | 97 | −2 |
| `mwe_leg_headings` | 45 | 43 | −2 |
| `mwe_leg_listas` | 91 | 90 | −1 |
| `mwe_fundo_esopic` | 14 | 13 | −1 |
| `mwe_list_pagebreak_bug` | 189 | 188 | −1 |
| `mwe_minimal`, `mwe_sty_manual`, `mwe_sty_minimal`, `mwe_sty_notitlesec` | 21/27/19/19 | 18/24/16/16 | −3 cada |

**Os 11 arquivos que mudaram são exatamente os que rodam em `lualatex-dev`; os
10 em `lualatex` não mudaram em nada.** O efeito é inteiramente do núcleo dev.
Páginas, erros de tagging, fatais e faltantes **idênticos** em todos.

Menos objetos de estrutura para o mesmo conteúdo — o `changes.txt` do dev
registra várias remoções de código não usado entre junho e setembro. Não é
regressão: é simplificação upstream. A `linha-base.tsv` foi regravada.

O `mwe_list_pagebreak_bug` **continua com os mesmos 24 erros**, o que é coerente
com o veredito da issue #1484: não havia bug para corrigir, e o MWE segue
reproduzindo o uso não suportado.

### Conformidade, pela primeira vez verificada aqui

```
PASS mwe_acessivel_book.pdf ua2
```

veraPDF 1.30.2, perfil `ua2`. É a primeira linha-base de conformidade desta
máquina, e vale com o núcleo dev atualizado.

### As duas ferramentas novas funcionam

**`show-pdf-tags --tree`** sobre o mesmo PDF: 297 linhas de árvore legível, com
papel, namespace, atributos e título por nó — `Document` → `semantic-para/Part`
→ `Title` → `text-block/P`, `Sect` → `chapter/H1`, `TOC`/`TOCI`/`Reference`. É
muito mais do que os contadores de `grep` da régua enxergam, e deve virar passo
de verificação das classes.

**`check-tagging-status`** sobre um MWE com tudo o que as linhas carregam:

```
book.cls is compatible
1. Unsupported          NONE
2. Currently incompatible  NONE
3. Partially compatible  ragged2e, eso-pic, svg, pgfrcs, tcolorbox, tikz,
                         verbatim, hyperref, nameref, amsmath, amsbsy
4. Compatible            fontspec, fontenc, brazilian.ldf, xcolor, graphicx,
                         fancyhdr, setspace, hyphenat, extdash, xurl, longtable,
                         booktabs, microtype, array, …
```

Duas leituras:

- **`brazilian.ldf` é compatível** — fecha o "babel não verificado" da consulta
  estática.
- **`enumitem` não aparece na lista.** Sob `tagging=on` o latex-lab **substitui**
  o pacote pela emulação `latex-lab-enumitem.sty`, e o `enumitem.sty` real nunca
  é carregado. O "parcial" da tabela estática é sobre o pacote real, que os
  nossos documentos não usam.
- As categorias 1 e 2 saem vazias porque este MWE **não** carrega `tabularray`,
  `titlesec` nem `pdfpages` — os três que a tabela estática marca como
  incompatíveis.
