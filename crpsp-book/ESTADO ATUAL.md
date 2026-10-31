# Estado atual — ecossistema CRP acessível

Situação das linhas editoriais LaTeX do CRP-SP e pendências abertas que
atravessam mais de uma linha. Para a análise detalhada da linha `book`, ver
`README.md`; para os contornos de tagging com os MWEs que os reproduzem, ver
`.agents/skills/latex-dev/references/workarounds.md`.

**Última atualização:** 2026-10-31

---

## RODADA 2026-10-31 — rodada autônoma (régua por podman, crpsp-abnt, formulário, #35 e pendência 4)

Rodada sem o editor presente, no CRP8057, com um PR por tarefa a partir da
`main`. **Mesclados:** #48, #49 e #50. **Abertos, à espera do Angelo:** #51 e #52.

- **Régua por podman (PR #48).** `desenvolvimento/verificar-podman.sh` roda o
  `verificar.sh` dentro da imagem fixa `crpsp-latex:rodada-20261031`, com
  `editorial/fonts` montado só para leitura e o fundo do Manual DH copiado para
  ext4. A base é `desenvolvimento/linha-base-podman.tsv`: **a `linha-base.tsv`
  continua sendo a do Fedora e as duas não se misturam.** A imagem traz LaTeX
  `2026-11-01`, núcleo de teste `dev pre-release-3`, `latex-lab` 80868 e
  `tagpdf` 1.0h. A régua inteira leva 92 s; duas rodadas deram saída idêntica
  por `cmp`.
- **Por que a linha-base do podman difere da do Fedora.** Todas as diferenças
  vêm do upstream, não de mudança no código: `mwe_book_tagging` 72 → 68
  objetos; `mwe_tabelas_phase3` 48 → 24 erros de tagging (o WA-08 continua
  reproduzido, com menos erros); `mwe_acessivel_book` 126 → 125 objetos.
  ⚠️ `mwe_acessivel` agora é **fatal**: o KOMA novo recusa `\DocumentMetadata`
  (`Fatal Class scrbook Error: \DocumentMetadata not supported!`).
- **Fora da comparação ou fatais em qualquer máquina.** `mwe_leg_completo` e
  `mwe_leg_glossario` precisam de `export/latex/`, que o `verificar-podman.sh`
  não monta (regra do script, não defeito). ⚠️ `mwe_creditos_titulo_invisivel`
  falha **em qualquer máquina**: `crpsp-relatorio.cls` está em `v2/`, fora do
  `TEXINPUTS` da régua. A linha tem 28 arquivos; o `exemplo-formulario-aceite`
  (PR #49) foi acrescentado a ela depois, pelo PR de documentação.
- **Formulário (PR #49).** A lista de aceite do `briefing-crpsp-formulario.md`
  (§10) foi medida: **5 de 7 critérios** passam e 2 ficam abertos (a margem da
  `\campolinha`, que termina antes da margem direita porque a classe usa
  `2\campogap` onde o briefing diz 1×; e o preenchimento em leitor de PDF, não
  verificado). A classe não foi tocada; a régua só ganhou o arquivo novo.
  Achados: o ramo NewJune do `formulario.sty` é código morto (o nome de
  família que testa não casa com o das fontes); `\campodata{id}` repetido
  duplica o `name=` do campo.
- **Formulário, fase 2** (cópia do `exemplo-formulario.tex` com
  `\DocumentMetadata{lang=pt-BR, pdfversion=2.0, pdfstandard=ua-2, tagging=on}`,
  só experimento, fora do PR): compila em 1 página, 0 erro, 47 objetos de
  estrutura, 20 campos (17 `Tx`, 3 `Btn`), e o veraPDF `ua2` **passa**.
  ⚠️ **O PASS não prova o que importa:** a árvore de tags tem 0 elemento `Form`
  e os 20 widgets não têm `/StructParent` nem `/TU`; o veraPDF 1.30.2 não cobra
  isso, e um leitor de tela pode não anunciar o rótulo de cada campo. **Não
  testado com NVDA/JAWS.** Com tagging o `/Rect` do widget fica na largura pedida
  (sem tagging, 2,07 bp mais largo e 4,6 bp mais alto).
- **`crpsp-abnt` (PR #50).** Imagem derivada `crpsp-latex:rodada-20261031-abnt`
  (biblatex-abnt, poppler, `show-pdf-tags`). As versões 0.3.0 e 0.4.0 saem
  iguais à linha-base nos 4 corpora e o veraPDF passa. Só `casos/esperado.txt`
  foi regravado: IBGE 2010 antes de 2011, efeito pretendido da ordenação. A
  entrada `BRASIL` passa a sair em ordem cronológica (medido com 9 entradas
  reconstruídas do README). ⚠️ **Lacuna:** nenhum caso prova que `nameaddon` não
  pesa; falta um caso BRASIL + órgão.
- **PR #51 (aberto, Refs #35): `book-crpsp_acessivel.sty` 0.6.0-alfa**, com as
  opções `web` e `print` (e `crpsp-leg.sty` 0.3.1-alfa). `web`: 17 páginas,
  `print`: 23 páginas, veraPDF `ua2` PASS nos dois. A régua do podman na branch
  é a linha-base mais os dois MWEs novos. ⚠️ O `geometry` relê `twoside`, por
  isso as opções entram por `PassOptionsToPackage`; e os `Lora-*.ttf` ficam,
  porque as variantes legadas os exigem.
- **Ensaio do guia de apresentações com o #51**, em cópia ext4 (nada gravado no
  mount): com a `.sty` nova e a opção `web`, o preâmbulo do `.tex` cai de 286
  para 135 linhas. O guia dá **66 e 62 páginas antes e depois** na imagem nova,
  com texto idêntico em todas as páginas (`pdftotext`), 2019 e 1750 objetos
  iguais, 7 `Span` com `/Lang`, veraPDF `ua2` PASS. As 67 páginas do `LEIA.md`
  são da imagem antiga (`crpsp-latex:guia`): o upstream novo move uma linha na
  p. 11 e a variante padrão perde uma página. Diferenças explicadas: o
  `\raggedright` agora vale desde o início (a folha de rosto sobe 1 pt e
  `TextAlign Justify` vai de 2 a 0). **Não explicado:** deslocamento de até
  0,09 pt nas tabelas `tabelaguia`. A proposta de `.tex` enxuto não foi
  aplicada à publicação.
- **PR #52 (aberto): pendência 4** (`sec-template`), `book` 0.5.3-alfa. A
  premissa deste arquivo, **3 chaves** do `\EditInstance`, não se sustentou na
  medida: **ficam 6** (`after-penalty-vspace` 50 contra 60 pt muda 5 de 11
  páginas; `number-format`/`text` valem com `secnumdepth` ≥ 0). Régua
  igual à linha-base; pixel a pixel igual em 8 MWEs. ⚠️ **Escolha de desenho
  para o Angelo:** o módulo antigo (v0.9b, MiKTeX desatualizado) deixa de ter a
  identidade visual, porque antes tinha ramo próprio e agora só recebe aviso.
  Conflito esperado entre #51 e #52 na linha 1 da `.sty` e no topo do `CHANGELOG`.
- ⚠️ **Sem `\DocumentMetadata`, o `geometry` entra em laço com o pacote `book`.**
  Já é assim na `main`, não foi introduzido por PR da rodada.
- **Não verificado nesta rodada:** MiKTeX (nenhuma comparação), NVDA/JAWS (o
  formulário e a troca de voz do `\estrangeirismo`), e a opção padrão sem `web`
  nem `print`, que o #51 deixa para decisão do editor.

---

## RODADA 2026-10-19 — papel timbrado, PDF de revisão e a fase `-beta` na linha `v2`

Detalhe da numeração em `CHANGELOG.md` (entradas de 2026/10/15 e 2026/10/19).

- **Linha nova, em `desenvolvimento/v2/`:** `crpsp-timbrado.cls` (papel timbrado A4 sobre `article`, 2026/10/15) e `crpsp-revisao.sty` (cabeçalho "USO INTERNO" e marca d'água "EM REVISÃO" opcional, PR #45), ambas sobre `crpsp-base.sty`. O PDF de revisão acessível (PDF/UA-2) sai do repositório `scripts`: `md2docx_abnt.sh --pdf-revisao … [--marcadagua]`, com `embrulho-revisao.tex` (o `##` abre página nova e o título fica a um `\parskip` do parágrafo seguinte; o ajuste é do embrulho, não da classe).
- **Fase `-beta` (PR #46):** o PDF de revisão da cartilha da Lei nº 13.935/2019 foi enviado em 2026-10-19, então `crpsp-timbrado` e `crpsp-revisao` (0.1.0) e `crpsp-base` (0.2.0) passaram de `-alfa` a `-beta`. Só a declaração mudou. Pela convenção, a fase é da publicação: sobe o corpo que a serviu. `crpsp-relatorio`, `relatorio`, `guia-visual` e `formulario` também carregam a base, mas seguem `-alfa`. O pacote do guia de apresentações (`livros_crp_acessivel_book`, 0.5.2-beta) já era beta; a aprovação vale para a publicação, não para o projeto editorial.
- **Cópias de produção:** `editorial/arquivo_latex/…/v2/` recebeu as declarações novas (conferido por `cmp` contra o repositório).
- **Pendências:** (1) a cópia de `crpsp-base.sty` em `cartilhas/servicos_online/3.acessivel/` tem outro corpo (base v0.1, 2026/07/03, já absorvida no histórico) e foi deixada como está; (2) a cópia de `crpsp-leg.sty` na pasta do guia de apresentações declara `v0.3.0` sem fase, e o repositório tem `0.3.0-beta` (regra 5 da convenção; pasta de publicação aprovada, não alterada); (3) ainda não há etiquetas `<linha>-v<versão>` para a linha `v2`.

---

## RODADA 2026-10-01 — issue #35: o guia de apresentações andou à frente da classe `book`

A revisão 2 do *Guia de boas práticas para apresentações acessíveis*
(`production/editorial/publicacoes/cartilhas/apresentacoes_acessiveis/revisao_2/LaTeX/`)
reuniu em 30/09 e 01/10 uma série de soluções que **vivem só no `.tex` da
publicação**. A cópia da `.sty` que o guia carrega
(`cartilhas/apresentacoes_acessiveis/LaTeX/livros_crp_acessivel_book.sty`) tem o
corpo idêntico ao de `book-crpsp_acessivel.sty` 0.5.2-beta (diferença: um
travessão na linha `\ProvidesPackage`). Nada do que segue está na classe, e a
próxima publicação `book` não herda.

**Issue aberta:** [#35](https://github.com/cuissi-crp06/crpsp-latex/issues/35) —
adotar as mudanças como padrão da linha `book` e criar as opções `web` e `print`.
Detalhe e critérios de aceite estão lá; aqui fica o resumo.

- **A adotar** (decisão do editor, 01/10): corpo em Atkinson com `Path` do
  kpathsea; `\tracinglostchars=3`; hifenização desligada, inclusive no gancho
  `para/begin`; órfãs e viúvas proibidas (`\clubpenalty`, `\widowpenalty` e
  `\@clubpenalty` em 10000); `\raggedbottom` com `\topskip` rígido de 11 pt;
  `\raggedright` do kernel; `\estrangeirismo` (`Span` com `/Lang`); `tabelaguia`
  com `colortbl`; capa e fundos como `artifact`; `\iniciotextual`; colofão;
  `\DocumentMetadata` só com `tagging=on`.
- **Fora, por decisão do editor:** os ajustes do sumário (`\l@chapter` com
  `plus 4em`, `\setstretch{1.1}` e `\EditInstance{heading}{chapter}{after-vspace=18pt}`).
  ⚠️ **Dependência:** o `plus 4em` existe *porque* a hifenização está desligada.
  Se ela virar padrão da classe, uma entrada longa do sumário volta a bater no
  número da página; a `.sty` precisa de outra solução.
- **Opções propostas:** `web` (`openany`, referências sem citação no texto, fundo
  só `bg-impar`; `oneside` **a confirmar**) e `print` (`openright`, citação
  autor-data, e o que a gráfica exigir). **Os itens de `print` não existem nem
  estão especificados:** escala de cinza, marcas de corte, sangria, PDF/X.
  Perguntas abertas: PDF/UA-2 e PDF/X convivem no mesmo arquivo? A conversão para
  cinza preserva a árvore de tags? A gráfica quer um PDF ou dois?
- **Não verificado:** a troca de voz do `\estrangeirismo` em NVDA + Acrobat Reader
  (o veraPDF não cobra idioma de trecho). A mecânica do `\@clubpenalty` e a
  necessidade do gancho `para/begin` estão como o `.tex` do guia as descreve; não
  foram reproduzidas aqui. Vale conferir se o gancho `begindocument/end` da
  `crpsp-base.sty` (linhas 191–197) tem o mesmo defeito.
- **Código a rever na `.sty` depois da adoção:** `pdfpages` (linha 193), exemplo com
  `alt={}` no comentário (linhas 151–157), Lora como fonte principal e
  `\usepackage[shortcuts]{extdash}` no guia, sem uso no corpo.

---

## RODADA 2026-09-28 — `relatorio` 0.3.0-alfa: créditos e folha de rosto na classe

Sprint 2 do plano de créditos do `plan-est_2026`. Detalhe no `CHANGELOG.md`.

- Os macros de créditos e a folha de rosto saíram do `comum.tex` do `pe26` para a
  `relatorio.sty` (§12 e §11). São a interface que o gerador do
  `normativas-pipeline` (Sprint 3 do plano, Sprint 13 do ROTEIRO) vai escrever.
- **Pendente no workbench, depois do merge:** o `pe26` compila contra a cópia da
  classe em `editorial/arquivo_latex/crpsp-book/desenvolvimento/v2/`, e o
  `comum.tex` dele ainda define os mesmos macros, o que dá erro de "already defined"
  contra a 0.3.0-alfa. Os dois passos andam juntos: atualizar a cópia e tirar os
  §§ 5 e 6 do `comum.tex`. A saída tem de ser igual, com o mesmo texto por página e o
  mesmo número de `Span`. O editor mexe no `pe26.tex`: conferir o hash antes.
- Fora do escopo, registrado no briefing dos créditos: levar o módulo para a linha
  `book`; e os §§ 1–4 e 7 do `comum.tex` (títulos com `\Needspace`, `longtable`
  depois de título, tabelas, sumário, `\irparaimpar`), que também são candidatos
  à classe.

---

## RODADA 2026-09-17 (2) — `relatorio` 0.2.0-alfa, com a variante `externo`

As decisões de 17/09 aplicadas ao código, mais a camada que espera o designer.
Detalhe no `CHANGELOG.md`; aqui fica o que muda a operação.

**A linha `relatorio` não compila mais sem as fontes do Nextcloud.** Decisão do
Angelo: os títulos são NEWJUNE, que é proprietária, e a classe emite **erro
claro** em vez de substituir a face. Isso liga esta linha à pendência C (o WSL
doméstico, que não compila) por um motivo novo: lá falta também a fonte. Quem
precisar compilar fora do Fedora tem de receber `editorial/fonts/NewJune/`
antes.

⚠️ **Havia duas Atkinson Hyperlegible Next nesta máquina**, com md5 diferentes:
a do pacote `atkinson` do TeX Live e a do pacote de fontes do Fedora, em
`/usr/share/fonts`. Declarar a fonte pelo nome do arquivo **não bastava**: o
luaotfload resolvia Regular e Bold por uma cópia e o itálico pela outra, dois
builds da mesma família no mesmo PDF. E só a do TeX Live não tem o glifo
U+0060, de modo que o defeito das aspas da convenção do TeX **dependia de qual
máquina compilava**. O `Path` agora é resolvido pelo kpathsea e fixa o
diretório. **Vale conferir o mesmo nas outras linhas**, que declaram fontes por
nome.

⚠️ **O atributo `TextAlign` mentia.** O `\RaggedRight` do ragged2e muda o
espacejamento mas não passa pela instância `para/raggedright` do latex-lab: o
PDF saía alinhado à esquerda aos olhos e marcado `/Layout /TextAlign /Justify`
na árvore de tags — 9 parágrafos assim, num exemplo que dava veraPDF **PASS**.
O `\raggedright` do kernel resolve os dois lados de uma vez, e o ragged2e sai do
orçamento de pacotes. **Também vale conferir na linha `book`.**

**A régua ganhou dois arquivos** e a `linha-base.tsv` foi regravada: 23 linhas.
Só as do `relatorio` mudaram — `exemplo-relatorio` de 2 para 3 páginas e de 149
para 151 objetos (corpo de 12 pt e o espaço entre parágrafos do WCAG), e
`exemplo-relatorio-externo` é novo, com 2 páginas e 80 objetos. Os outros 20
arquivos saíram idênticos, conferidos um a um.

**Critério de aceitação, cumprido nos dois exemplos:** zero erro, zero erro de
tagging, zero `Missing character`, zero transbordo, veraPDF **PASS em ua2** e
**zero nó `Figure`** vindo da decoração.

⚠️ **Ao contar `Figure` na árvore, casar o nó** (`grep -cE '─Figure \('`), não a
palavra: o exemplo do `externo` escreve "Figure" na prosa e numa célula, e um
`grep -c Figure` devolve 3 com a árvore limpa. O falso positivo já custou uma
investigação.

**O `\tracinglostchars = 3` não vira `! `.** Ele acrescenta contexto de erro à
mensagem `Missing character`, mas a linha do log não começa com `!` — quem pega
é a coluna `faltantes` da régua, não `fatais`.

---

## RODADA 2026-09-17 — o Fedora alinhado ao upstream

**Motivo:** escrever a `crpsp-livro.cls` e revisar a `crpsp-relatorio.cls` exige
a máquina habilitada em qualquer circunstância. O detalhe está em
`briefings/preparo-ambiente-2026-09-17.md`; aqui fica o que muda a operação.

**Documentação e fontes passam a existir.** O TeX Live estava com
`docfiles = 0` e `srcfiles = 0` — 4,8 GB de runtime e 8,2 MB de doc. Agora são
11 GB, com **4,9 GB de documentação e 471 MB de fontes**. `texdoc tagpdf` e
`texdoc latex-lab-sec-template` abrem local, e os `.dtx` estão em
`texmf-dist/source/latex/latex-lab/`.

**Núcleo dev na pre-release 2** (`latex-base-dev` e `latex-lab-dev`, 79901 →
80282), com `tlmgr update --all --backup` — o backup é o caminho de volta.

⚠️ **A linha-base foi regravada, e a mudança é benigna.** Os **11** arquivos que
rodam em `lualatex-dev` perderam de 1 a 5 objetos de estrutura; os **10** em
`lualatex` não mudaram em nada. Páginas, erros de tagging, fatais e faltantes
idênticos em todos os 21. É simplificação do upstream, não regressão.

**veraPDF 1.30.2 em `~/verapdf`**, fora do workbench. O `mwe_acessivel_book.pdf`
dá **PASS em `ua2`** — primeira linha-base de conformidade desta máquina. O
critério de aceitação do briefing do Manual de DH deixa de ser inverificável
aqui:

```sh
~/verapdf/verapdf --format text --flavour ua2 <arquivo>.pdf
```

**Duas ferramentas novas do upstream entram no fluxo:**

- `texlua $(kpsewhich --progname=texlua show-pdf-tags.lua) --tree <pdf>` — árvore
  de tags legível, com papel, namespace e atributos. Enxerga o que os contadores
  de `grep` da régua não enxergam.
- `check-tagging-status = listfiles` no `\DocumentMetadata` — relatório do
  estado de tagging de cada pacote do documento, com dado do upstream.

**Orçamento de pacotes das classes novas.** Incompatíveis: `tabularray`,
`titlesec` e — achado novo — **`pdfpages`**, por onde entra a capa do Guia de
Apresentações Acessíveis. Parciais: `tcolorbox`, `eso-pic`, `hyperref`, `svg`,
`ragged2e`, `tikz`. O `enumitem` não conta: sob `tagging=on` o latex-lab o
substitui pela emulação.

---

## RODADA 2026-09-16 — WSL doméstico, e o que não viaja junto

Primeira sessão no **WSL da máquina doméstica**, reproduzido a partir do
levantamento de 2026-08-18 feito sobre a máquina de referência do trabalho
(WSL2, Debian 13). A reprodução pegou o que estava documentado — os dois
mounts rclone, o `wsl.conf` sandboxed, os settings do Claude Code — e por isso
herdou também os defeitos do original. **As três pendências abaixo são para
resolver no notebook corporativo**, que é onde as origens estão.

**Genealogia encerrada.** `editorial/latex_acessivel/` — o repositório local sem
remote, aposentado em 03/09 quando virou `crpsp-book/` neste monorepo — foi
**removida em 2026-09-16**. Conferido arquivo a arquivo antes: as cinco
modificações não commitadas que restavam lá ou eram bit a bit idênticas ao que
já estava aqui, ou eram subconjunto do que o monorepo levou adiante (o `.sty`
local era 0.5.1-alfa contra a 0.5.2-beta daqui). O clone de trabalho passa a ser
`editorial/arquivo_latex/`, e é o único.

### Pendência A — as skills do workspace não existem em lugar nenhum que viaje

O `CLAUDE.md` documenta seis skills em `skills/` — `latex-dev`,
`linguagem-simples`, `normativas-cfp`, `normativas-crp-sp`,
`extrair-ato-convenio`, `extrair-edital`. Procuradas nesta máquina: **não estão
no Nextcloud** (não há pasta `skills/` nem `.agents/` na raiz montada), **não
estão em nenhum dos três repositórios** (`crpsp-latex`, `scripts`,
`normativas-pipeline`) e **não estão entre as skills sincronizadas da conta**
(chegam 11, todas genéricas: `pandoc`, `my-writing-style`,
`classificar-processos-sei`, `docx`, `pdf`, `pptx`, `xlsx`, `learn`, `docs`,
`mcp-builder`, `skill-creator`).

Pesa nesta linha em particular: o cabeçalho deste arquivo manda ler
`.agents/skills/latex-dev/references/workarounds.md`, e a `latex-dev` é a skill
que carrega os workarounds de tagging (WA-01 a WA-10). Num ambiente novo, a
referência aponta para o vazio e os workarounds precisam ser redescobertos.

- [x] No corporativo, publicar as seis onde viajem. **Conferido em 2026-10-31
      no CRP8057:** estão em `~/repos/claude-memory/skills/` (repositório
      versionado), com symlink em `~/.claude/skills/` (as seis mais
      `dossie-subsede`, `goose-recipes` e `rodada-autonoma`); o `CLAUDE.md` do
      workspace já descreve esse lugar.
- [ ] Corrigir os caminhos que **este arquivo** ainda cita (`.agents/skills/…`
      no cabeçalho, na pendência A acima e na seção "Controle de versão"):
      continuam apontando para um lugar que não existe.

### Pendência B — o mount de escopo Claude Code não entrega o `CLAUDE.md`

O `rclone-crpsp.service` monta o Nextcloud filtrado para o escopo do agente:
libera oito diretórios e fecha com `- **`. O `- **` também nega os **arquivos**
da raiz, e nenhuma regra os recupera — então `CLAUDE.md` **não chega em
`~/crpsp`**. O mount desenhado para o Claude Code é justamente o único onde ele
roda sem as instruções do projeto; esta sessão só as teve porque rodou em
`~/nextcloud`, o mount completo.

Não é defeito local: a unidade é cópia literal da do host de referência, e lá
vale o mesmo.

- [ ] Acrescentar `--filter "+ /CLAUDE.md"` **antes** do `- **`, nas duas
      máquinas. Enquanto isso, abrir o agente em `~/nextcloud`. **Aberta,
      conferida em 2026-10-31 no CRP8057:** o `rclone-crpsp.service` não tem a
      regra (e ainda libera `skills/`) e `~/crpsp` não lista `CLAUDE.md`. Na
      outra máquina: não conferido.
- [ ] Decidir sobre a sobreposição dos dois mounts (`~/nextcloud` completo e
      `~/crpsp` filtrado, mesmo remote), já registrada como pendência conhecida
      no levantamento de 18/08.

### Pendência C — esta máquina não compila

Sem `podman` e sem `pandoc` instalados, e ambos exigem `sudo` com senha
interativa. Enquanto não forem instalados, o WSL doméstico serve para ler,
editar e versionar, **não** para rodar `verificar.sh` nem para conferir a régua
de `linha-base.tsv`: qualquer alteração feita aqui atravessa sem prova de
compilação.

- [x] Instalar `podman` e construir a imagem `crpsp-latex:dev`, ou assumir a
      máquina como somente de edição e sempre compilar no Fedora. **Conferido
      em 2026-10-31 no CRP8057:** `podman` 5.4.2 e `pandoc` instalados, e a
      régua inteira roda aqui pela imagem `crpsp-latex:rodada-20261031` (ver a
      rodada de 2026-10-31). **No WSL doméstico: registrado** (o `podman` entrou
      em 2026-10-01, segundo a memória do projeto), **não conferido** aqui.

### Fora do escopo deste arquivo

Dois achados da mesma varredura pertencem ao `SINCRONIA.md`, que vive no clone
do `normativas-pipeline` e não existe nesta máquina — **transcrever de lá,
quando estiver no corporativo**: (1) o ambiente do pipeline não existe aqui
(nem `~/repos/`, nem `~/venv-normativas`, nem `~/normativas-run`, nem
`~/.config/crpsp/key.env`, nem as variáveis `NORMATIVAS_*`); (2) o `scripts/` do
Nextcloud está defasado do repositório `cuissi-crp06/scripts` — lá existem
`assessoria/`, `editorial/`, `jornal_psi/`, `pesquisa/`, `relatorio_eventos/`,
`transcricao/` e `verificar_chaves.py`, que aqui não existem, e aqui há ~35
arquivos soltos na raiz que lá foram para `arquivo/`. Não mexido de propósito: é
o vaivém que o `ESPELHO.md` registra ter custado trabalho três vezes, e pede
conferência item a item.

---

## RODADA 2026-09-13 — Fedora como máquina de desenvolvimento, e a régua

**Motor.** O Fedora passa a ser a máquina de desenvolvimento, com **TeX Live
upstream** em `~/texlive/2026` (`scheme-full`, `tlmgr`), à frente do TeX Live da
distribuição pelo `~/.bashrc.d/texlive.sh`. Kernel `LaTeX2e <2026-11-01>
pre-release-1` no `lualatex-dev`. Fontes do Nextcloud expostas por
`~/.local/share/fonts/crpsp` (ver `desenvolvimento/docker/README.md`).

⚠️ **O TeX Live do Fedora não serve para esta linha.** O `texlive-latex-lab` da
distribuição (svn76739, fim de 2025) não traz `latex-lab-testphase-sec-template`
nem o `latex-base-dev`: o `lualatex-dev` dele carrega o kernel `2025-11-01`. Sem o
módulo, o `\@ifpackagelater{latex-lab-testphase-sec-template}{2026/05/25}` do
pacote book cai no ramo antigo, que pede o template `display`, também inexistente
ali — `The template 'display' of type 'heading' is unknown`. O pacote supõe dois
estados do upstream (antes e depois de 2026/05/25), e há um terceiro: **módulo
ausente**. Ver a pendência 4.

**A régua.** `desenvolvimento/verificar.sh` compila cada MWE e exemplo v2 duas
vezes, numa cópia temporária, e imprime TSV. A primeira rodada virou
`desenvolvimento/linha-base.tsv` — 21 arquivos em 58 s. Com o pacote book
**0.5.2-beta**:

- `mwe_acessivel_book`: 11 páginas, 131 objetos, zero erro;
- `mwe_leg_completo`: 78 páginas, 1866 objetos, zero erro; `mwe_leg_glossario`: 9 páginas, 99 objetos — as mesmas 9 páginas de 2026-07-13;
- os cinco exemplos v2 compilam sem erro (`exemplo-relatorio`: 149 objetos; `exemplo-guia-visual`: 75).

**Erros esperados na linha-base** — não são regressão:

| arquivo | por quê |
|---|---|
| `mwe_list_pagebreak_bug` | reprodução do bug de `\hsize` em lista × quebra de página; `Too deeply nested` é o sintoma |
| `mwe_tabelas_phase3` | a variante `tblr` do `tabularray` reproduz o WA-08 (48 erros de tagging) |
| `mwe_acessivel` | testa `legado/book-variantes/livros_crp_acessivel.sty` v0.2, variante arquivada |

Sem contagem de objetos (`-`): `crpsp-v2-doc` (`ltxdoc`), `exemplo-formulario` e
`guia-exemplo`, que não declaram `\DocumentMetadata` com tagging.

**Uso na pendência 1.** Antes de trocar `testphase` por `tagging=on` numa linha,
rodar `sh crpsp-book/desenvolvimento/verificar.sh > rodada.tsv` e comparar com a
linha-base: mesmo número de objetos, nenhum erro novo.

---

## PENDÊNCIA 4 — o ramo do `sec-template` supõe que o módulo existe

**Prioridade: baixa**, porque MiKTeX e TeX Live atualizados trazem o módulo.
Mas um motor sem ele (TeX Live de distribuição, MiKTeX desatualizado) falha com
erro fatal em vez de cair num padrão. Conferir `\@ifpackageloaded` antes do
`\@ifpackagelater` e decidir o que fazer no terceiro estado: aviso e formato
padrão do `latex-lab`, ou erro com mensagem clara pedindo atualização.

**Verificado em 17/09/2026:** com o pacote ausente, o `\@ifpackagelater` entrega
o **ramo falso** — "versão antiga" e "módulo ausente" são indistinguíveis por
ele. O terceiro estado é real.

**E metade da pendência some pelo desenho.** O manual do `sec-template` (52
páginas, agora instalado) documenta `\EditInstance` para mudar só as chaves que
interessam. Das treze chaves que o `book-crpsp_acessivel.sty:425-470` declara,
**só três diferem do upstream** — `heading-decls`, `number-decls` e
`title-decls`. As outras dez repetem o padrão, e é essa repetição que obriga a
classe a acompanhar renomeação de chave: foi o que criou o ramo duplo do
`\@ifpackagelater{...}{2026/05/25}`.

Com `\EditInstance` nomeando as três, o ramo duplo deixa de ser necessário e
resta só o `\@ifpackageloaded` em volta de um bloco curto. Ver
`briefings/preparo-ambiente-2026-09-17.md`.

---

## RODADA 2026-08-04 — upstream se mexeu

`monitor_ctan.py` acusou `latex-lab 2025-11-01a → 2026-06-01a`, `tagpdf
1.0b → 1.0d` e `latex-base-dev pre-release 0 (2026-11-01)`. A imagem
`crpsp-latex:dev` está com `latex-lab 2026-06-01a` (igual ao CTAN) e
`tagpdf 1.0c` (uma atrás). O que isso mudou:

**Corrigido na classe (linha `book`):**

- **Chaves do `sec-template` renomeadas** — o bloco `\DeclareInstance{heading}{chapter}`
  escrito para a v0.9b falhava com 4 erros por capítulo na v0.9g, e a
  identidade visual do capítulo era ignorada em silêncio. `book-crpsp_acessivel.sty`
  agora traz os dois ramos, por `\@ifpackagelater{...}{2026/05/25}`. Ver WA-01.
- **`\TOCAcessivel` virou alias deprecado** — o bug do `latex-lab-testphase-toc`
  foi corrigido upstream (v0.85k, 2026-04-28); `\tableofcontents` emite
  `/T (Sumário)` limpo. Ver WA-02.
- **`alt={}` não marca mais artefato** — virou WA-10; a chave é `artifact`.
  Corrigido em `guia_apresentacoes_acessiveis.tex` (27 avisos → 0).

**Continua ativo:** `titlesec` (WA-03) e `tabularray` (WA-08), ambos
reconferidos com MWE nesta data.

**Pendente de conferência visual:** `tcolorbox` inline (WA-09) não emite
mais erro de tagging; falta ver se ainda força `\par`.

~~**Não migrar:** … o `\LegArtigo` por `\hangindent` … contorna o bug de
`\hsize` na quebra de página.~~

⚠️ **Corrigido em 17/09/2026: não há bug de `\hsize`.** A issue
[latex3/tagging-project#1484](https://github.com/latex3/tagging-project/issues/1484)
foi **fechada em 08/08/2026**, e o veredito é outro. Frank Mittelbach: *"for me
`\description ... \enddescription` without appropriate grouping is (and always
was) unsupported usage"*. David Carlisle: *"If I add the missing group then it
runs without error and no overfull box warnings"*.

É uso não suportado, não defeito do tagging, e o conserto suportado é
acrescentar o grupo. Isso **reabre a possibilidade de simplificar o
`crpsp-leg.sty`**: o `\hangindent` do `\LegArtigo` pode não ser mais
necessário. Conferir antes de mexer.

Regra dura para as classes novas, que já valia e agora tem a razão registrada:
**nunca invocar ambiente por csname.**

---

## Linhas e situação

| Linha | Arquivos | Formato | Situação |
| --- | --- | --- | --- |
| `book` | `book-crpsp_acessivel.sty` | A5 livro | Produção |
| `guia` | `crpsp_acessivel.cls` + `guia-crpsp_acessivel.sty` | A5 | Desenvolvimento |
| `guia_visual` | `crpsp-guia_visual.cls` + `guia-visual.sty` | 16:9 | Implementada 2026-07-03 |
| `formulario` | `crpsp-formulario.cls` + `formulario.sty` | A4 AcroForm | Implementada |
| `relatorio` | `crpsp-relatorio.cls` + `relatorio.sty` | A4 retrato | **0.3.0-alfa (2026-09-28)**, com `interno`/`externo`, créditos e folha de rosto |
| `livro` | — | — | Não iniciada |

Infraestrutura comum: `crpsp-base.sty` (verificação de engine, fontspec
condicional, paleta `cor1`/`cor2`/`cor3`). Compilação via podman, imagem
`crpsp-latex:dev` — ver `desenvolvimento/docker/README.md`.

---

## PENDÊNCIA 1 — migrar `testphase` para `tagging = on`

**Prioridade: alta.** É a única pendência que toca todas as linhas.

### O que aconteceu

Em resposta à issue que abrimos ([latex3/tagging-project#1484](https://github.com/latex3/tagging-project/issues/1484),
2026-07-14), David Carlisle:

> "you should not use the `testphase` key which was an earlier syntax
> predating the introduction of `tagging=on`"

A chave `testphase={phase-III,...}` — usada em praticamente todo o código e
toda a documentação deste workspace — é **sintaxe legada**.

### O que já foi verificado

Na imagem `crpsp-latex:dev` (TeX Live 2026), as duas sintaxes produzem
resultado **idêntico**: o relatório do Jornal Psi compila com as mesmas 12
páginas, os mesmos ~843 objetos de estrutura e zero erro de tagging com
`tagging=on` no lugar de `testphase={phase-III, table, firstaid}`.

Verificou-se também que o defeito do `tabularray` (WA-08) é igual nas duas
sintaxes — **não era artefato da chave legada**. Isso enfraquece a hipótese
de que outros workarounds do workspace sejam efeito colateral do `testphase`,
mas não a elimina para os workarounds que dependem de módulos nomeados.

### O que falta

- [ ] **Linha `book`** — a mais delicada. WA-01 e WA-02 dependem de módulos
      `latex-lab-testphase-sec-template` e `latex-lab-testphase-toc`
      **nomeados**; não se sabe se `tagging=on` os carrega sob outro nome.
      Agrava: o motor de referência histórico dessa linha é o `lualatex-dev`
      do MiKTeX/Windows, e a equivalência acima foi medida só no podman.
      **Recompilar nos dois motores e comparar a árvore de tags antes de
      migrar.** [2026-08-04] Parcialmente andado: o `guia_apresentacoes_acessiveis.tex`
      já usa `tagging=on` **e** `testphase={phase-III,table,firstaid}` no mesmo
      `\DocumentMetadata` e compila limpo no podman (0 erros, 670 objetos);
      o `\TOCAcessivel` deixou de ser necessário. Falta rodar no MiKTeX e
      tirar a chave legada. [2026-10-01] A revisão 2 do guia já saiu da chave
      legada: o `\DocumentMetadata` dela tem só `tagging=on`, e compila no podman
      com 0 erro e veraPDF ua2 PASS (LEIA.md da revisão). Falta o MiKTeX e a
      comparação da árvore de tags; a classe (`.sty`) ainda documenta `testphase`
      (ver a issue #35). [2026-10-31] O PR #51 (aberto, Refs #35) tira
      `testphase` da documentação da `.sty` e passa a pedir só `tagging=on`; a
      régua do podman na branch fecha igual à linha-base (mais os 2 MWEs
      novos). **Segue pendente o MiKTeX**, e a
      pendência só fecha para a `book` depois do merge do #51.
- [ ] **Linha `guia`** (`crpsp_acessivel.cls`) — migrar e recompilar
      `guia-exemplo.tex`.
- [ ] **Linha `guia_visual`** — migrar e recompilar `exemplo-guia-visual.tex`.
      Atenção à navbar: ela depende de `\SuspendTagging`/`\ResumeTagging` e
      da pré-medição fora do `tikzpicture`; conferir se o comportamento se
      mantém.
- [ ] **Linha `formulario`** — migrar e recompilar `exemplo-formulario.tex`.
      Conferir os campos AcroForm, que interagem com o tagging.
      [2026-10-31] Fase 2 medida em cópia (`tagging=on`, sem tocar na classe):
      compila, 20 campos preservados e veraPDF `ua2` PASS, **mas 0 elemento
      `Form` na árvore e widgets sem `/StructParent` nem `/TU`**; o veraPDF não
      cobra isso. Falta decidir como declarar cada campo e testar com leitor de
      tela. Não migrada.
- [ ] **Documentos de produção** em `production/editorial/publicacoes/*` que
      tragam o bloco antigo.
- [x] **Linha `relatorio`** — migrada em 2026-07-29 (commit `e9417f9`).
- [x] Documentação de referência (`SKILL.md`, `pdfua-checklist.md`,
      `workarounds.md`, `CLAUDE.md`) — atualizada com a ressalva de que a
      linha `book` ainda não foi reconferida.

### Como verificar cada migração

Trocar o bloco e recompilar duas vezes, comparando **antes e depois**:

```sh
# contagem de objetos de estrutura e erros de tagging
grep -oE "~[0-9]+ structure objects" <arquivo>.log | tail -1
grep -cE "not allowed|text-unit|^! |differ|open structure" <arquivo>.log
```

Resultado esperado: mesmo número de objetos de estrutura, zero erro. Qualquer
divergência é sinal de que a linha depende de um módulo `testphase-*`
específico — nesse caso, **parar e registrar aqui** em vez de forçar.

---

## PENDÊNCIA 2 — `tabularray` carregado em duas classes

**Prioridade: média.** Risco latente, não defeito ativo.

`crpsp_acessivel.cls` e `crpsp-guia_visual.cls` carregam `tabularray`, que
emite relações de tag inválidas no fecho de toda tabela (WA-08). Nenhuma
publicação daquelas linhas exercitou tabelas sob tagging até agora; a
primeira que exercitar vai esbarrar nisso sem aviso claro.

- [ ] Substituir por `tabular`/`longtable` + `\rowcolor`, como em
      `relatorio.sty` §7, ou remover a carga se as linhas não usarem tabelas.

---

## PENDÊNCIA 3 — cargas mortas e workarounds possivelmente vencidos

**Prioridade: baixa.** Higiene.

- [ ] `guia-visual.sty` carrega `tcolorbox[skins]` sem usar: a implementação
      migrou para `\parbox` justamente porque o `tcolorbox` não fica inline
      sob tagging. Manter a carga é risco sem contrapartida.
- [x] O workaround "`enumitem` é proibido" está **vencido em parte**
      (testado 2026-08-04): `description` com `align`/`leftmargin`/
      `labelwidth`/`labelsep`, `itemize[nosep]` e `enumerate[label=]` passam
      limpos pela emulação `latex-lab-enumitem`; só `leftmargin=*` falha.
      Não implica reverter o `\LegArtigo` — ver a nota no `workarounds.md`.
      Fica em aberto só o fato de `crpsp_acessivel.cls` carregar o `enumitem`
      real, o que agora é menos grave.
- [x] `monitor_ctan.py` rodado em 2026-08-04: `latex-lab 2026-06-01a`,
      `tagpdf 1.0d`, `latex-base-dev pre-release 0`. Rodar de novo antes de
      qualquer decisão sobre workarounds de tagging: `python3 monitor_ctan.py`

---

## Controle de versão

Esta pasta foi um repositório git próprio de 2026-07-29 (commit inicial
`c9d1450`) a 2026-09-03, quando entrou no monorepo `cuissi-crp06/crpsp-latex`
como `crpsp-book/`, com o histórico preservado (`940a787`). A pasta antiga
(`editorial/latex_acessivel/`) foi removida em 2026-09-16 — ver a rodada daquela
data. O monorepo acompanha a genealogia; as cópias de produção continuam no
workbench.
O restante do workspace — inclusive `production/` e `.agents/skills/` — **não é
versionado**: alterações lá não têm histórico.

Consequência prática: o relatório do Jornal Psi
(`production/jornal/analise/latex/`) e a documentação em `.agents/skills/latex-dev/`
estão fora deste repositório, ainda que sejam parte do mesmo trabalho.
