# Briefing de integração: pipeline de normativas × camada `Leg`

> **estado:** levantamento, para decisão
> **escrito em:** 2026-09-17
> **escopo:** o acoplamento entre `cuissi-crp06/normativas-pipeline` (Python) e
> `cuissi-crp06/crpsp-latex` (TeX) — o que já existe, o que está quebrado e o que
> depende de decisão do Angelo.

## 1. Para que serve este documento

O contrato de comandos da camada `Leg` está no cabeçalho do `crpsp-leg.sty` (linhas
17-45) e o briefing fundador está em `briefing-leg-book-acessivel.md`. O que **não**
existia em nenhum dos dois é o mapa do acoplamento: por onde os dois projetos se tocam
hoje, em produção, e quais armadilhas isso cria para quem mexer num lado sem olhar o
outro. É isso que este documento fixa.

Ele foi levantado a partir da pergunta "o Sprint 10 do pipeline está ligado ao
desenvolvimento do `crpsp-latex`?". A resposta curta é **sim, mas por um fio** — e a
resposta longa é que a ligação relevante entre os projetos é outra, e maior.

### ⚠️ Correção de premissa, antes de tudo

O **Sprint 10 não é um sprint de código**. O `ROTEIRO.md` do pipeline o define como
*"O que depende de decisão sua"*, e abre com "Nenhum destes é trabalho de código até você
decidir". Ele tem quatro itens, e só **um** toca o `crpsp-latex`:

| Item do Sprint 10 | Toca o `crpsp-latex`? |
|---|---|
| `\LegAnexo` na camada Leg | **Sim** — é o assunto da seção 4 |
| Avisos de agrupador (código no Sprint 11) | Não |
| Citações ambíguas do LexML (18 chaves) | Não |
| Scraping das históricas do CFP (403 do `atosoficiais`) | Não |

E há uma segunda ressalva: a **frente ativa** do `crpsp-latex` em 17/09 é a linha
`relatorio`, na árvore `crpsp-book/desenvolvimento/v2/`. Essa árvore **não compartilha
código nenhum** com a camada Leg — `crpsp-base.sty` não conhece o `crpsp-leg.sty`, e um
`grep crpsp-leg` em `desenvolvimento/v2/` não devolve nada. Quem chegar aqui esperando
encontrar o Sprint 10 na mesa de trabalho da `relatorio` vai procurar em vão.

A camada Leg é **código vivo mas sem frente ativa**: dependência incondicional da linha
`book`, que está em produção, e prevista como módulo `leg` da linha `livro`, que ainda não
começou.

## 2. O mapa da integração

Um gerador, uma pasta de saída, dois consumidores.

```
  normativas-pipeline (Python)                    crpsp-latex (TeX)
  ────────────────────────────                    ─────────────────
  consolidar.py
      │  JSON canônico
      ▼                                            crpsp-leg.sty  ◄── contrato
  export/normas/<id>.json                          (cabeçalho, l. 17-45)
      │                                                  ▲
      │  latexgen.py                                     │ comandos
      ▼                                                  │
  export/latex/<id>.tex  ─────────┬──────────────────────┘
   (no workbench)                 │
                                  ├──► (a) Manual DH: v1/fragmentos/
                                  │        via build.ps1
                                  │
                                  └──► (b) RÉGUA: verificar.sh faz
                                           ln -s $WORKBENCH/export
```

**A interface é o JSON, não o banco.** O `latexgen.py` consome exclusivamente
`export/normas/<id_arquivo>.json` e **nunca** consulta o SQLite — está escrito no
docstring dele, e é a mesma fonte do viewer HTML.

**O gerador emite 15 comandos `Leg`**, todos definidos no `crpsp-leg.sty`: `LegNorma`
(ambiente), `\LegEpigrafe`, `\LegEmenta`, `\LegPreambulo`, `\LegAgrup`, `\LegArtigo`,
`\LegParagrafo`, `\LegInciso`/`\LegAlinea`/`\LegItem` (com os ambientes-run
`LegIncisos`/`LegAlineas`/`LegItens`), `\LegDisp`, `\LegDispDecimal`, `\LegTermo`,
`\LegAncora`, `\LegRef`, `\LegNotaAlteracao`, `\LegRevogado`, `\LegFecho`, `\LegAssina`.

### As cinco obrigações que o `.sty` atribui ao gerador

Estão nos comentários do `crpsp-leg.sty` e são o que quebra silenciosamente se alguém
mexer num lado só:

1. **Rótulo completo, sem prefixo automático** (l. 226-232) — o `.sty` não escreve "Art.";
   o gerador emite o rótulo como está no banco. Difere do `livros_crp.sty` do memoir, que
   prefixava.
2. **Profundidade normalizada e saturada em 4** (l. 131-136) — quem normaliza é o gerador
   (`profundidades_normalizadas_detalhe`, `latexgen.py:245`), para nunca passar de `<H6>`.
3. **A marca textual "(Revogado)" é do gerador** (l. 407) — o `\LegRevogado` só acinzenta
   (`crplegcinza`, ≥4,5:1) e **nunca** tacha. Cor sozinha não informa.
4. **`\LegNotaAlteracao`: os parênteses já vêm do banco** (l. 387) — `#1` é o `texto_tag`
   com parênteses; `#2` é a urn-alvo ou vazio.
5. **Glossário em fragmento separado** (l. 342-344) — `<id>-glossario.tex`, que o mestre
   posiciona ao final. O gerador decide por `--termos-no-corpo`.

## 3. ⚠️ A armadilha da régua (leia antes de medir qualquer coisa)

**A saída do pipeline é insumo da linha-base do LaTeX.** O `verificar.sh` monta a cópia de
teste e liga o workbench dentro dela:

```sh
[ -d "$WORKBENCH/export" ] && ln -s "$WORKBENCH/export" "$TMP/export"
```

Três dos 23 arquivos da régua dependem disso:

| Arquivo da régua | Depende de |
|---|---|
| `mwe/mwe_leg_completo.tex` | `export/latex/{dudh,lei15263,lei13146}.tex` |
| `mwe/mwe_leg_glossario.tex` | `export/latex/*-glossario.tex` |
| `mwe/mwe_fundo_esopic.tex` | `fundo_impar.png` do Manual DH |

E o `TEXINPUTS` do `verificar.sh` inclui a pasta `v1/` do Manual DH.

**O problema:** esses fragmentos estão defasados em relação ao banco.

| | dispositivos |
|---|---|
| `export/latex/lei13146.tex`, gravado em **11/09 18:59** | **459** |
| doc 2232 (Lei 13.146) no banco de trabalho hoje, `fonte_texto=planalto` | **463** |

A `linha-base.tsv` foi regravada em **17/09** com `mwe_leg_completo` em 78 páginas e 1.863
objetos — medidos sobre fragmentos de 11/09, anteriores ao **PR B do Sprint 7** (14/09),
que atualizou o texto de 30 leis federais no lugar.

> **Regra, então:** antes de creditar ao LaTeX qualquer mudança em `mwe_leg_completo` ou
> `mwe_leg_glossario`, conferir a data de `export/latex/`. Um `consolidar` + `latexgen`
> move a linha-base sem que uma linha de TeX tenha mudado. E quando a regeneração vier,
> **regravar a linha-base no mesmo movimento** — nunca em commit separado, ou o próximo
> a rodar a régua vai caçar uma regressão de tagging que não existe.

## 4. A decisão do Sprint 10: o `\LegAnexo`

### O que o roteiro diz hoje

> O `latexgen` avisa e não emite: **193 blocos de anexo** hoje. Adiado por decisão sua até
> surgir a necessidade.

O código correspondente está em `latexgen.py:713-720`, e o motivo do adiamento está
escrito ali, corretamente:

```python
# anexos ficam FORA do fragmento: a camada Leg ainda não tem \LegAnexo e
# inventar marcação aqui produziria PDF/UA-2 sem estrutura de heading
# correspondente. O aviso entra na curadoria (T2) para não passar batido.
```

### O que a medição mostra

"193 blocos" lê-se como uma fila de corpus. Não é. Medido no banco de trabalho, só
leitura:

| Medida | Valor |
|---|---|
| Documentos com anexo **em todo o corpus** | **1** |
| Anexos (objetos) | **1** |
| Blocos | **193** |

O documento é o **doc 2929 — Decreto 12.002/2024**, *"Estabelece normas para elaboração,
redação, alteração e consolidação de atos normativos"*. O anexo é o questionário "QUESTÕES
A SEREM AVALIADAS PREVIAMENTE À ELABORAÇÃO DE ATOS NORMATIVOS NO ÂMBITO DO PODER EXECUTIVO
FEDERAL".

E a forma é **regular** — nenhuma tabela, figura ou lista aninhada:

- **174 blocos `paragrafo`** (`{tipo, texto}`), **todos** com numeração decimal no início.
  Profundidade 1–4, distribuída em 19 / 96 / 57 / 2;
- **19 blocos `titulo`** (`{tipo, nivel, texto}`), **todos** em `nivel 4`.

⚠️ **A camada Leg já tem comando para essa forma.** O `\LegDispDecimal{número}{texto}`
(l. 322) é precisamente o item decimal, com `\leftskip` proporcional ao número de pontos; e
o `\LegAgrup[prof]{tipo}{rótulo}{nome}` já cobre título em profundidade 4. O que falta é o
**invólucro** do anexo — rótulo e título como heading — e não a marcação do conteúdo.

### Que não bloqueia publicação nenhuma

O único consumidor vivo da camada Leg é o **Manual de Direitos Humanos**
(`production/editorial/publicacoes/manuais/manual_direitos_humanos/v1/`): 20 URNs em
`normas_do_manual.txt`, 20 fragmentos em `fragmentos/`. Nenhuma das 20 é o Decreto 12.002
— e, como só **um** documento do corpus inteiro tem anexo, **nenhuma norma do manual tem
anexo**. O `briefing-manual-dh-normas-restantes.md:38` já registrava isso:
*"Falso alarme do briefing: os 'ANEXO' dos blocos eram menções em prosa — nenhuma norma
tinha anexo no estático."*

`\LegAnexo` nunca existiu: `git log -S "LegAnexo"` neste repositório não devolve nada.

### As três saídas

| Saída | Custo | Onde |
|---|---|---|
| **(a)** Anexo como componente próprio, `;anexo.N` na URN | Nenhum LaTeX novo | `_componente_anexo`, `ingerir.py:46` — já existe |
| **(b)** `\LegAnexo` como invólucro, reusando `\LegAgrup` + `\LegDispDecimal` | Um comando + um `mwe_leg_anexo.tex` na régua | `crpsp-leg.sty` |
| **(c)** Seguir adiado | Zero | — |

A escolha entre (a) e (b) já estava escrita como decisão pendente em
`briefing-manual-dh-normas-restantes.md:115-117`: *"decida: ingerir como componente
(`;anexo.N` na URN) ou manter o anexo estático com TODO próprio. Não invente estrutura
nova sem necessidade."*

### Recomendação

**Seguir adiado — mas trocar o motivo do adiamento.** Hoje o roteiro adia "até surgir a
necessidade", o que soma com os "193 blocos" para dar a impressão de dívida grande
esperando. O roteiro deveria dizer, em vez disso: é **um** anexo, de **um** documento, fora
de qualquer publicação, e há duas saídas mais baratas que um comando novo — uma delas sem
LaTeX nenhum. Se um dia entrar, é um invólucro e um MWE, não um projeto.

⚠️ **E registrar por que o caso é menos banal do que o número sugere.** O anexo preso é
justamente o do decreto de **técnica legislativa** — o texto que normatiza como se redige
ato normativo no Executivo federal. Para quem desenha a própria camada Leg, é o anexo de
maior valor de consulta do corpus. Isso é argumento a favor de priorizar, apesar de ser um
documento só, e a decisão é do Angelo.

## 5. O que está quebrado

### Três ponteiros para uma pasta que não existe mais

A pasta `editorial/latex_acessivel/` foi **removida do workbench em 16/09**. Três lugares
ainda apontam para ela ou para caminhos antigos:

| # | Arquivo | Problema |
|---|---|---|
| 1 | `scripts/normativas/latexgen.py:8` | O docstring aponta o contrato para `editorial/latex_acessivel/briefings/briefing-leg-book-acessivel.md`. O briefing vive hoje em `crpsp-book/briefings/` **neste** repositório. |
| 2 | `manual_direitos_humanos/v1/README.md` | Cita a mesma pasta como *"a fonte canônica"*, na seção "Armadilhas conhecidas". |
| 3 | `manual_direitos_humanos/v1/build.ps1:35` | Usa `production/editorial/publicacoes/manual_direitos_humanos/…`, **sem o segmento `manuais/`**. |

O terceiro não é cosmético: o caminho não existe, e `latexgen._resolver_urns`
(`latexgen.py:775`) faz `caminho.read_text()` sem guarda. **O build do manual falha no
passo 1 com `FileNotFoundError`, em qualquer plataforma.**

### O build do manual não roda na máquina ativa

`build.ps1` é PowerShell e pede `lualatex-dev` do MiKTeX; não existe `build.sh`. A máquina
ativa é o Fedora desde 12/09.

**A boa notícia é que o ferramental está todo lá** — o que falta é só o porte do script:

| Peça | Estado no Fedora |
|---|---|
| `lualatex-dev` | ✔ `~/texlive/2026/bin/x86_64-linux/lualatex-dev` |
| `tagpdf` | ✔ no TeX Live 2026 upstream |
| veraPDF | ✔ `~/verapdf/bin/cli-1.30.2.jar` — é **jar, sem wrapper**: `java -jar` |

⚠️ Um shell aberto antes de 13/09 precisa de
`export PATH="$HOME/texlive/2026/bin/x86_64-linux:$PATH"` — o TeX Live do Fedora não serve
para a linha `book`.

## 6. O que **não** é dívida (conferido, para não repetir a conferência)

A genealogia das cópias `.sty` deployadas no Manual DH foi conferida com a ferramenta
oficial, como manda o `CLAUDE.md`:

```sh
python3 ferramentas/comparar-corpo.py \
    ~/Documentos/trabalho/production/editorial/publicacoes/manuais/manual_direitos_humanos/v1 \
    --repo ~/repos/crpsp-latex
# → 2 corpos distintos, 0 fora do histórico
```

| Cópia no Manual DH | Declara | Situação |
|---|---|---|
| `crpsp-leg.sty` | `v0.3.0` (2026/07/13) | Corpo **idêntico** ao do repositório |
| `livros_crp_acessivel_book.sty` | `v0.5.0-alfa` (2026/07/10) | Absorvido no blob `f7e879cef661`; o repositório já está em `v0.5.2-beta` (2026/08/10) |

**Nada sobe para o `crpsp-latex`**: as duas cópias só estão *atrás*, e a regra é que uma
cópia que apenas ficou atrás do que o repositório já registra não é trazida.

Duas observações menores, sem ação nesta rodada:

- A cópia do manual declara `crpsp-leg.sty` **`v0.3.0` sem fase**, enquanto o repositório
  declara `v0.3.0-beta`. A correção de declaração de 13/09 não alcançou esta cópia.
- Atualizar o manual para o `v0.5.2-beta` é decisão de produção, não de genealogia — e
  **repaginaria** o PDF, como a `relatorio` repaginou de 12 para 18 páginas em 17/09.

## 7. Dívidas herdadas que caem na camada Leg

### ⚠️ O `TextAlign` mentiroso alcança a Leg

O achado 2 de 17/09 (`crpsp-book/ESTADO ATUAL.md`): o `\RaggedRight` do ragged2e não passa
pela instância `para/raggedright` do latex-lab, e o PDF sai marcado
`/Layout /TextAlign /Justify` na árvore de tags — num exemplo que dava veraPDF **PASS**. O
registro diz *"Conferir também na linha `book`"*.

A camada Leg está no escopo: **`\LegEmenta` (l. 105) chama `\justifying`, do ragged2e.**

E a consequência é concreta: o Manual DH deu veraPDF **PASS em 11/07**, mas o defeito é
**invisível ao veraPDF**. A afirmação de acessibilidade do manual precisa ser reconferida
na árvore de tags, não no validador.

### As outras

- A linha `book`/Leg **não** migrou de `testphase=` para `tagging=on` puro (pendência de
  prioridade alta no `ESTADO ATUAL.md`), ao contrário da `crpsp-relatorio.cls`.
- **Duas decisões do briefing Leg seguem herdadas em aberto** pelo futuro módulo `leg`
  (registradas em `plano-2026-09-16-linhas-ativas.md`): agrupadores (`cap`/`tit`/`sec`)
  entram na árvore de headings ou são parágrafos destacados? `\LegTitulo` continua como
  alias de `\LegEpigrafe`?
- O `\hangindent` do `\LegArtigo` contornava um "bug de `\hsize`" que a issue
  [latex3/tagging-project#1484](https://github.com/latex3/tagging-project/issues/1484)
  mostrou **não existir** (uso não suportado de `\description` sem agrupamento). Isso
  reabre a simplificação do `crpsp-leg.sty` — **conferir antes de mexer**.
- ⚠️ `crpsp-book/README.md`, seção 5, **está desatualizado sobre a Leg**: ainda descreve o
  estado pré-extração da v0.4.2 (`\LegArtigo` via `description`, minipages em `\LegEmenta`
  e `\LegParagrafo`). Nada disso corresponde ao `crpsp-leg.sty` v0.3.0, que não tem
  `description` nem minipages desde 13/07.
- O gerador **não emite corpo de prosa**, e por isso duas Notas Técnicas do Manual DH
  continuam estáticas (`briefing-manual-dh-normas-restantes.md:32-35`). Decisão pendente.

## 8. Retomada

Para não depender da conversa em que este documento foi escrito.

1. ⚠️ **Primeiro, no Fedora: `git fetch` nos quatro clones de `~/repos/`.** O clone do
   `normativas-pipeline` está em `main` = `5653667` (PR #39) com `FETCH_HEAD` de **14/09**,
   mas a sessão de 16/09 registrou o repositório já no **PR #58**. Os PRs #40–#58 foram
   feitos no notebook corporativo e **não têm registro no `ESTADO_ATUAL.md`**, que não tem
   sessão de 15/09. Descobrir o que fizeram — provavelmente o **C2 do Sprint 7** — e
   registrar.
2. Conferir o estado deste PR (`gh pr view --json state`) antes de qualquer commit: o
   Angelo mescla no meio da sessão.
3. Só então decidir o Sprint 10, com a seção 4 na mão.
4. Sem decisão do Angelo, **nada** do Sprint 10 vira código — é a definição do sprint.

### Anotações de ambiente, achadas de passagem

- `~/normativas-run/` ainda tem `ensaio-sprint7/` e `ensaio-sprint7c/`, que o
  `ESTADO_ATUAL.md` autorizava apagar depois dos merges (#32 e #33, ambos mesclados).
- `~/normativas-run/export/` **não existe**: o `export/` que a régua liga é o do
  workbench, em `~/Documentos/trabalho/export/`.

## Fontes desta apuração

Tudo verificado nesta máquina, em leitura. Nada foi inferido de registro anterior.

| Afirmação | Como conferir |
|---|---|
| 1 documento, 1 anexo, 193 blocos | Varredura de `documentos.metadados_json` no banco de trabalho, chave `anexos` |
| 459 × 463 dispositivos | `ls -l export/latex/lei13146.tex` × `SELECT count(*) FROM dispositivos WHERE doc_id=2232` |
| Genealogia sem dívida | `ferramentas/comparar-corpo.py` (seção 6) |
| `build.ps1` quebrado | `ls production/editorial/publicacoes/manual_direitos_humanos` → não existe; o real tem `manuais/` |
| Ferramental do Fedora | `which lualatex-dev`, `kpsewhich tagpdf.sty`, `ls ~/verapdf/bin/` |
| `\LegAnexo` nunca existiu | `git log -S "LegAnexo" --all` |

## Relacionados

- `briefing-leg-book-acessivel.md` — o contrato fundador da camada (10/07)
- `briefing-manual-dh-normas-restantes.md` — as decisões de anexo e prosa
- `briefing-manual-dh-acabamento.md` — a remoção das minipages e o veraPDF do manual
- `plano-2026-09-16-linhas-ativas.md` — o lugar da Leg entre as linhas
- `ROTEIRO.md` do `normativas-pipeline`, Sprints 10 e 11
