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

## Linha `desenvolvimento/v2` — `crpsp-timbrado` e `crpsp-revisao` 0.1.0-beta — 2026/10/19

Promoção de fase, sem mudança de número nem de corpo: só a declaração de
`crpsp-timbrado.cls` e `crpsp-revisao.sty` passa de `-alfa` a `-beta`; as datas de
autoria (2026/10/15 e 2026/10/19) ficam. **Beta** porque o PDF de revisão de
`resposta_rvnd` (cartilha da Lei nº 13.935/2019), composto na classe com o
pacote, foi enviado em 2026-10-19 (decisão do Angelo: "podemos considerar o
`sty` em beta"). `crpsp-base.sty` não foi tocado: é compartilhado por quatro
linhas e tem fase própria (`0.2.0-alfa`).

Na mesma data o `embrulho-revisao.tex` do repositório `scripts` (PR #31, #32) fez o
`##` abrir página nova e igualou o espaço entre esse título e o parágrafo seguinte
ao espaço entre parágrafos. É ajuste do embrulho (`\patchcmd` no `\subsection`), não da
classe: o corpo de `crpsp-timbrado.cls` continua o de 2026/10/15.

## Linha `desenvolvimento/v2` — `crpsp-revisao` 0.1.0-alfa — 2026/10/19

`crpsp-revisao.sty`, pacote novo que marca como **em revisão** o documento
composto na classe `crpsp-timbrado`. Serve ao PDF que circula para aprovação
enquanto o texto ainda muda (o `docx` para o designer sai por outro caminho); a
versão final sai sem o pacote. `-alfa`: nenhum documento circulou com ele.

- **Uso:** `\documentclass{crpsp-timbrado}` seguido de
  `\usepackage{crpsp-revisao}` ou `\usepackage[marcadagua]{crpsp-revisao}`.
  Exige a classe (erro claro sem ela).
- **Cabeçalho:** "USO INTERNO" em NewJune negrito, à direita, na margem oposta
  à do logo e com o topo das maiúsculas alinhado ao de "Conselho", no texto do
  logo (5,1 mm abaixo do topo do símbolo); o "Página X de Y" do timbrado fica
  empilhado logo abaixo e continua só aparecendo com mais de uma página.
  `\revisaoRotulo{<texto>}` troca o rótulo.
- **Marca d'água, opcional** (`marcadagua`, desligada por padrão): "EM REVISÃO"
  em NewJune negrito, vermelho `C00000`, girada a 45°, **centrada no bloco de
  texto** (e não na folha, que tem margens assimétricas) e composta atrás de
  tudo. O corpo da fonte se ajusta ao texto, então `\revisaoMarcaDagua{<texto>}`
  também serve. A transparência vem do canal alfa da cor na fonte (fontspec
  `Color=RRGGBBTT`), sem pacote extra; `opacidade=<0 a 100>`, padrão 10. A 10% o
  texto preto fica a **16,1:1** do fundo da marca (19,4:1 no papel), medido no
  PDF rasterizado.
- **Artefato, como o resto do papel.** Cabeçalho e marca d'água ficam fora da
  árvore de estrutura (a marca usa o par `\tagstop`/`\tagmcbegin{artifact}` do
  `relatorio`, com `eso-pic`). ⚠️ **Quem lê por tecnologia assistiva não ouve
  "USO INTERNO" nem "EM REVISÃO"**; por decisão de 19/10 só há marcação visual,
  sem aviso no corpo. O status deve constar também do nome do arquivo e do
  e-mail que encaminha o PDF. É marcação, não proteção: nada impede de
  remover a marca do PDF.
- Verificado: PDF/UA-2 sem falha no veraPDF 1.30 (1.727 regras) nos dois
  exemplos, zero erro de tagging, zero caractere ausente, nenhum `P` nem
  `Figure` vindo do cabeçalho ou da marca. `exemplo-revisao.tex` (com a marca,
  3 páginas, 94 objetos) e `exemplo-revisao-simples.tex` (sem a marca, 1 página,
  11 objetos) entraram na linha-base; `exemplo-timbrado.tex` não mudou (104).

## Linha `desenvolvimento/v2` — `crpsp-timbrado` 0.1.0-alfa — 2026/10/15

`crpsp-timbrado.cls`, classe nova para documentos sobre o papel timbrado
(ofícios, memorandos, pareceres), sobre `article` e `crpsp-base`. Data de
autoria; nenhuma publicação circulou, daí `-alfa`.

- **Origem:** `Papelaria Institucional/2026/papelCartaCRPSP_4x0_A4_sede.docx`
  (Comunicação, Nextcloud corporativo). Margens e posição do logo vêm dele:
  corpo a 48 mm do topo, 25 mm à esquerda, logo de 68,6 x 25,8 mm a 12,5 mm da
  borda. A margem direita é **37 mm, e não os 30 do modelo**: com 30 mm a linha
  cheia tem 83 caracteres em Atkinson 12 pt, acima do teto de 80 do WCAG 1.4.8
  (medido por `\crpspMedida`).
- **Títulos 1 a 5** são `\section` a `\subparagraph`, todos em linha própria
  (na `article` os dois últimos são embutidos). Saem como H1 a H5 na árvore de
  tags. Sem numeração por padrão; a opção `numerado` numera os cinco níveis.
- **Fontes:** corpo em Atkinson Hyperlegible Next, títulos e rodapé em NewJune,
  as duas declaradas por arquivo e com erro claro se faltarem, como no
  `relatorio`. ⚠️ O `.docx` não usa NewJune em estilo algum: todos os estilos
  são Arial. A NewJune só aparece no endereço do rodapé, que no modelo está
  convertido em curvas.
- **Rodapé em texto.** No `.docx` o endereço é imagem (PNG + SVG de curvas):
  não seleciona nem pesquisa. Aqui é texto em NewJune itálica. A sede é o
  padrão; `\timbradoRodape` troca para uma subsede (os endereços das outras
  doze versões do papel não foram trazidos).
- **Cabeçalho e rodapé são artefato** sob `tagging=on`, o que é o tratamento
  certo para elemento repetido e deixa o logo e o endereço fora da ordem de
  leitura. O remetente precisa estar no corpo do texto.
- **A arte não vem no repositório.** O logo esperado é o PDF **vetorial** do
  kit de marca (`CRP_LogoPreferencial_Horizontal_Positivo_COR.pdf`, em
  `editorial/logos/marca-2023/positiva-cor/` no workbench), copiado ao lado do
  documento como `crpsp-timbrado-logo.pdf`. O PDF do kit traz margem de
  proteção embutida (o desenho ocupa 87% da largura); o padrão a corta com
  `trim`/`clip` e o logo cai a 25,0 mm da esquerda e 12,7 mm do topo, com
  68,7 x 25,8 mm, a menos de 0,2 mm do papel original (medido sobre o PDF
  rasterizado a 300 dpi). `\timbradoLogo[<opções>]{<arquivo>}` aponta outro
  arquivo: sem opções só fixa a largura (serve para o PNG do kit, que é rente
  ao desenho, 1545 px). Sem arquivo algum o cabeçalho cai para o nome do
  Conselho em texto, com **aviso no log** (uma vez, no início do documento).
  Versão anterior desta mesma entrada usava o PNG de 189 ppi extraído do
  `.docx`.
- Não carrega `fancyhdr` nem `titlesec`: o estilo de página é `\ps@timbrado`.
- Verificado: PDF/UA-2 sem falha no veraPDF 1.30 (1.727 regras), zero erro de
  tagging, zero caractere ausente. `exemplo-timbrado.tex` entrou na linha-base.

## Linha `desenvolvimento/v2` — `relatorio` 0.3.0-alfa — 2026/09/28

`crpsp-relatorio` e `relatorio` de `0.2.0-alfa` para `0.3.0-alfa`; o
`crpsp-base` não mudou. Sprint 2 do plano de créditos do `plan-est_2026`
(`2.diagramando/plano_creditos_sprints.md` no workbench): o que o `pe26` fez no
seu `comum.tex` e marcou CANDIDATO À CLASSE vai para a classe, para que o
gerador de créditos do `normativas-pipeline` escreva contra macros estáveis.
Continua `-alfa`: não há registro de que o `pe26` tenha circulado, e a
convenção manda `-alfa` quando não se sabe.

**`relatorio` §12, Créditos (novo).** Veio do `comum.tex` §5 do `pe26`, com os
internos renomeados de `\crpsp@…` para `\crpsprel@…` e o módulo de mensagem
para `relatorio`; o comportamento é o mesmo. Títulos `\creditosoculto`
(nível 1, com tag e sem impressão), `\creditosgrupo` (nível 2, com fio como
artefato), `\creditossub` e `\creditos` (ficha técnica); nomes
`\NomeNosCreditos{nome}{registro}[nota]`, com o registro num `Span` e alias
deprecado para a forma de um argumento, e `\CargoNosCreditos[registro]{nome}{cargo}`,
com os cargos alinhados; ambientes `CreditoInstitucional` e `NomesDuasColunas`.
Carrega `needspace`, `multicol` e `pdfrender`. O `multicol` estava na lista do
que a classe não carrega: a exceção fica registrada na `crpsp-relatorio.cls` §3,
restrita à lista de nomes.

**`relatorio` §11, folha de rosto (nova variante da capa tipográfica).** Do
`comum.tex` §6: `\relRosto{logotipo}{alt}` no preâmbulo troca a capa
tipográfica por título no centro e logotipo no pé, sem fio, autor e data. O
logotipo é imagem com `alt` obrigatório, não artefato. `\crpspRostoTitulo`
(padrão `\@title`) deixa o documento quebrar a linha sem mexer nos metadados.
Sem `\relRosto`, a capa tipográfica é a de antes.

**`relatorio` §4, regra do nome próprio.** Registrada em comentário: sob
tagging, a primeira chamada de `\@startsection{<nome>}` congela o estilo de
todas as seguintes com o mesmo nome. Foi o que pôs em 1 pt os títulos do `pe26`
na quarta revisão (25/09). Título com estilo próprio usa nome próprio.

**Régua.** `linha-base.tsv` regravada: `exemplo-relatorio-externo` de 2 para 3
páginas e de 80 para 162 objetos (ganhou uma página de créditos e a ficha
técnica, com 12 `Span`, um por pessoa com registro), e `exemplo-relatorio-rosto`
é novo, com 2 páginas e 16 objetos (um `Figure`, o logotipo). Os outros
arquivos saíram idênticos, inclusive o `exemplo-relatorio` interno (3 páginas,
151 objetos). veraPDF **PASS em ua2** nos dois exemplos.
`mwe/mwe_creditos_titulo_invisivel.tex` fica como registro do experimento:
as definições dele colidem com as da classe, e o cabeçalho diz como compilá-lo
contra a 0.2.0-alfa.

## Linha `desenvolvimento/v2` — 0.2.0-alfa — 2026/09/17

`crpsp-base`, `crpsp-relatorio` e `relatorio`, todos de `0.1.0-alfa` para
`0.2.0-alfa`. É geração nova, não correção: aplica as decisões de 17/09/2026
(ver `briefings/decisoes-2026-09-17.md`) e abre a variante `externo`.
Permanecem em `-alfa` — o relatório do Jornal Psi, única publicação servida por
esta linha, é interno e não circulou fora do CRP-SP.

**`crpsp-base`.** Ganha três coisas, todas **opt-in**, porque o pacote é
compartilhado por quatro linhas e efeito colateral aqui tiraria da linha-base
quem não decidiu nada:

- `\crpspTipografiaWCAG` — o WCAG 1.4.8 inteiro: espaço entre parágrafos de
  1,5 × entrelinha, alinhamento à esquerda sem hifenação, e a compensação do
  `\@afterheading` que impede o título de ficar mais longe do próprio texto do
  que os parágrafos ficam entre si. Usa o `\raggedright` do kernel, não o
  `\RaggedRight` do ragged2e: além do esticamento infinito, que é o que evita
  transbordo com a hifenação desligada, é ele que marca `/Layout /TextAlign
  /Start` na árvore de tags. Com o ragged2e o PDF saía alinhado à esquerda aos
  olhos e **justificado** para quem lê o atributo — 9 parágrafos assim no
  exemplo do `externo` antes da correção, 0 depois. O ragged2e sai do orçamento
  de pacotes.
- `\crpspMedida{<teto>}` — régua de medida: registra no log os caracteres da
  linha cheia, medidos no motor com kerning sobre a mesma amostra de
  `desenvolvimento/medida/amostra-pt.tex`, e avisa se passarem do teto.
- `\crpspExigeFonte` e `\crpspSondaGlifos` — fonte declarada por arquivo com
  erro claro quando falta, e registro em log da face que não tenha o glifo
  U+0060.

A paleta padrão passa do cinza neutro para o **roxo institucional `#422C73`**.

**`crpsp-relatorio`.** Opções em chave-valor por `\DeclareKeys`, no lugar do
`\DeclareOption` legado: `interno` (padrão) e `externo`, mutuamente exclusivas,
mais o `semtoc` que já existia. Corpo de **11 pt para 12 pt** — a Lora em 11 pt
tinha altura-x de 1,933 mm, abaixo do mínimo de 2,0 mm da RNIB, e a linha não
cumpria o critério que o próprio sistema adota. O `pdfpages` entra na lista de
incompatíveis com tagging.

**`relatorio`.** Margem de **35 mm nos quatro lados** (mancha de 140 mm, 75
caracteres medidos no motor, 35 linhas por página). Atkinson Hyperlegible Next
no corpo e NEWJUNE nos títulos, ambas declaradas por arquivo **e com o
diretório fixado**. `\tracinglostchars = 3`. A variante `externo` traz
`\relDecoracao`, `\relCapaArte` e `\relCapa`, com a arte marcada como artefato
(`\tagstop` + `\tagmcbegin{artifact}`) e fallback tipográfico quando o arquivo
falta.

**Duas armadilhas encontradas ao escrever isto, registradas nos arquivos:**

- **Duas Atkinson na mesma máquina.** O Fedora tinha a do pacote `atkinson` do
  TeX Live e a do pacote de fontes da distribuição, com md5 diferentes. Com a
  fonte declarada só pelo *nome do arquivo*, o luaotfload resolvia Regular e
  Bold por uma cópia e o **itálico** pela outra — dois builds da mesma família
  no mesmo PDF. Pior: só a do TeX Live não tem o glifo U+0060, então o defeito
  das aspas da convenção do TeX **depende da máquina**. O `Path` agora é
  resolvido pelo kpathsea, e os oito cortes vêm do mesmo build.
- **`\newif` dentro de bloco condicional.** Ao pular o `\ifcrpsp@rel@externo`, o
  TeX não reconhece como condicional um `\if...` ainda indefinido, mas conta o
  `\fi` correspondente: o bloco fecha cedo e o erro sai dezenas de linhas
  adiante, como `Too many }'s`. Todo `\newif` de bloco opcional nasce antes
  dele.

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
