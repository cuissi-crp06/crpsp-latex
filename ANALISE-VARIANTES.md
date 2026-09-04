# Análise das variantes `.sty` — o que precisa de decisão

> Levantamento mecânico de 03/09/2026. **Nada foi consolidado**: as comparações
> abaixo são a evidência; qual versão é canônica é julgamento de Angelo. Fecha
> perguntas que `editorial/inventario-latex/latex-sistema.md` deixou em aberto
> desde junho, marcadas como *"verificar se divergiu"*.

Eram **21 arquivos `.sty`** espalhados, e **11 deles não estavam em git nenhum**
— existiam só no disco desta máquina desde a migração de julho/2026.

## 1. A revisão do Claude foi incorporada à base? — **Não, e a base a superou**

`crpsp-memoir/livros_crp-rev_cld.sty` × `crpsp-memoir/crpsp-memoir.sty`
(o antigo `sty/livros_crp.sty`, v0.2 de 06/04/2025).

O diff bruto dá 1022 linhas, mas **é fim de linha**: ignorando CRLF, são
**36 linhas** reais.

A diferença que decide: a base **removeu o pacote `changes`** e deixou o
motivo escrito no próprio arquivo — marcação de revisão não deve sair no PDF
de entrega, e `changes` colide com `\comment` definido por outros pacotes do
pipeline. A `rev_cld` ainda o carrega, com autor registrado.

**Logo a base é a mais nova**: contém uma decisão tomada *depois* da rev_cld,
rejeitando deliberadamente um recurso dela. A rev_cld traz uma melhoria isolada
que talvez valha portar — `urlbreaks` na opção do `xurl`.

**Decisão pendente:** portar `urlbreaks` para a base e aposentar a rev_cld, ou
revisar as outras 35 linhas antes.

## 2. `book` × `book_old` — **não é "velho", é outra identidade visual**

`legado/book-variantes/livros_crp_acessivel_book.sty` ×
`..._book_old.sty` — 109 linhas de diferença, ambos v0.3 de 09/04/2026.

Não é sucessão: são **paletas diferentes**.

| | `book` | `book_old` |
|---|---|---|
| `crp1` | RGB 66,44,115 — púrpura escuro | RGB 4,88,110 — azul escuro |
| `crp2` | RGB 165,93,166 — púrpura médio | RGB 25,159,175 — azul médio |
| margem inferior | 46.667mm | 32.889mm |

O `_old` também tem um `\let\oldhyperchapter\Hy@org@chapter` que o outro não tem.

**Decisão pendente:** qual paleta é a identidade corrente do CRP-SP? O sufixo
`_old` sugere que o púrpura venceu, mas o nome não é prova — e a diferença de
margem é substantiva.

> Nenhum dos dois é o canônico atual: esse é
> `crpsp-book/book-crpsp_acessivel.sty` (v0.5.0), que veio do repositório
> `latex_acessivel` e viaja em par com `crpsp-leg.sty`.

## 3. `formularios.sty` — três versões, diferença menor do que parecia

| Arquivo | Linhas |
|---|---|
| `crpsp-forms/formularios.sty` (era `sty/`) | 105 |
| `legado/copias-por-projeto/formularios-pasta.sty` | 104 |
| `legado/copias-por-projeto/formularios-raiz.sty` | 81 |

65 e 74 linhas de diferença contra a de `sty/` — mas boa parte é **indentação**
no bloco de `UprightFont`/`BoldFont`. A de 81 linhas é a mais enxuta e
provavelmente a mais antiga.

`form-sem-logo.sty` tinha 2 cópias **byte a byte idênticas** — resolvido, ficou uma.

**Decisão pendente:** confirmar que a de 105 linhas é a canônica e descartar as
outras duas, ou conferir as 74 linhas antes.

## 4. `livros_crp.sty` — 7 cópias, 6 versões

A de `sty/` (511 linhas, v0.2) é a base da linha memoir e virou
`crpsp-memoir/crpsp-memoir.sty`. As outras seis, de 184 a 224 linhas, são
**arquivos diferentes com o mesmo nome**, cada uma dentro de um projeto
(`manual_dh/`, `publicacoes/PE2025/`, `publicacoes/politica/`…), agora em
`legado/copias-por-projeto/`.

Duas são idênticas entre si (`manual_dh` e `publicacoes/carta_de_servicos`).

**Decisão pendente:** essas cópias por projeto são customizações que ainda
importam para recompilar aqueles documentos, ou lixo de quando não havia um
pacote comum? Se forem lixo, saem; se não, precisam virar opções do
`crpsp-memoir`.

## 5. `livros_crp_v7.sty` × `livros_crp_comentado.sty`

Ambos v7.0 de 26/09/2025, "Reengenharia do Carregador de Fontes" — 202 e 330
linhas. O `comentado` é a versão anotada do mesmo trabalho.

**Decisão pendente:** o v7 entra na linha memoir como sucessor da v0.2, ou é
uma linha paralela abandonada? O inventário não decide.

---

## O que fazer com o que está em `legado/`

O git guarda o histórico: uma variante pode ser **apagada** num commit e
continuar recuperável. `legado/` existe para o intervalo entre "não sei se
presta" e "decidi" — não é destino permanente. Depois da decisão, o que não
for canônico sai da árvore, com a justificativa na mensagem do commit.

---

# Resolução — 2026-09-04

As cinco perguntas acima foram fechadas, e o levantamento que as originou foi
ampliado: ele varreu o disco de uma máquina, e faltavam os outros repositórios
do GitHub. Contando-os, a linhagem `livros_crp` tem quinze conteúdos distintos,
não sete cópias em seis versões.

**1. A revisão do Claude.** Confirmada: a base é posterior, e `livros_crp-rev_cld.sty`
fica como variante arquivada, com nome de pacote próprio. Segue valendo portar o
`urlbreaks` do `xurl`.

**2. `book` × `book_old`.** O canônico `book-crpsp_acessivel.sty` 0.5.0 fixa a
paleta azul (RGB 4, 88, 110) — a mesma de `book_old.sty`. O sufixo `_old` engana:
o ramo não seguido é o púrpura. A pergunta, porém, deixou de valer para a linha
nova: `crpsp-base.sty` define a paleta por publicação, com padrões neutros e os
setters `\crpspCorPrincipal`, `\crpspCorSecundaria` e `\crpspCorAcessoria`. A
partir dali a paleta não é propriedade do pacote.

**3. `formularios.sty`.** A de 105 linhas segue como canônica em `crpsp-forms/`;
as outras duas ficam arquivadas com nome próprio. A segunda cópia de
`form-sem-logo.sty` era byte a byte idêntica e foi removida.

**4. As cópias por projeto.** Não são lixo. A do Manual de Direitos Humanos deu
origem aos comandos `\Leg*` e ao pipeline de normativas. Ficam, com procedência
registrada em `legado/copias-por-projeto/PROVENIENCIA.md`.

**5. `livros_crp_v7` × `livros_crp_comentado`.** O v7 entra na linha memoir como
0.4.0-beta: é a geração das primeiras tentativas de PDF acessível. O rótulo
`v7.0` vinha de outro esquema e não se ordenava com a série `0.x`, embora sua
data (2025/09/26) fosse posterior à da base `v0.2` (2025/04/06). O `comentado` é
a versão anotada do mesmo trabalho.

## O defeito que o levantamento não tinha visto

Não era a ausência de versão, era o rótulo repetido. Três arquivos de conteúdo
distinto declaravam `v7.0` de 2025/09/26 e três declaravam `v0.5.0` de
2026/07/10. Como `\@ifpackagelater` compara a data declarada, e não o conteúdo,
eram indistinguíveis para o LaTeX.

A correção tem duas partes: o pacote implantado mantém o nome sob o qual é
carregado (`livros_crp`, `livros_crp_acessivel_book`, `formularios`), e toda
variante que não é implantada passa a declarar o próprio nome de arquivo. Feito
isso, nenhum nome declarado se repete no repositório.
