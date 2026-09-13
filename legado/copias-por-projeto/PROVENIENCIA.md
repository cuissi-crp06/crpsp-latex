# Cópias por projeto — procedência

Variantes de `livros_crp.sty` que cada projeto carregava antes de haver um pacote
comum. Não são resíduo: a do Manual de Psicologia e Direitos Humanos deu origem
aos comandos `\Leg*` e, por essa via, ao pipeline de normativas, que nasceu em
parte da busca de uma solução para documentos compostos primariamente de leis e
normas.

Cada arquivo declara o próprio nome, e não `livros_crp`, porque nenhum é
implantado — declarar o nome comum faria doze arquivos diferentes disputarem a
mesma identidade de pacote.

## Trazidas de fora do monorepo em 2026-09-04

Conferidas por sha256 contra a origem antes da cópia. O repositório não tem
`.gitattributes`, então os bytes são os da origem.

| arquivo | origem | sha256 (12) |
|---|---|---|
| `livros_crp-cartilha_anticapacitista.sty` | `cuissi-crp06/cartilha_anticapacitista`, raiz | `c366a2e6f188` |
| `livros_crp-apresentacoes_acessiveis.sty` | `cuissi-crp06/apresentacoes_acessiveis`, raiz | `45204b3b3d62` |
| `livros_crp-editoracao_manual.sty` | `cuissi-crp06/editoracao`, `manual/` | `b0ca7505212e` |
| `livros_crp-guia_apresentacoes_acessiveis.sty` | `cuissi-crp06/trabalho`, `production/editorial/publicacoes/acessibilidade/LaTeX/v1/` | `df190dbda53f` |

Duas cópias que pareciam faltar já estavam absorvidas, e a igualdade foi
confirmada por hash, não por tamanho: `editoracao/LaTeX/sty/livros_crp.sty` é
byte a byte `crpsp-memoir/livros_crp_v7.sty` (`ccbe769e457b`), e
`editoracao/LaTeX/sty/livros_crp_comentado.sty` é
`crpsp-memoir/livros_crp_comentado.sty` (`a8dc3788b899`).

`form-sem-logo-pasta.sty` foi removido: era byte a byte idêntico a
`crpsp-forms/form-sem-logo.sty`.

## Trazidas de fora do monorepo em 2026-09-05

Varredura de `cadernoB` e `relatorio_editorial` antes de esses repositórios
saírem do GitHub — o conteúdo deles passa a viver só no Nextcloud, e os pacotes
não podiam sair junto. Dos quinze `.sty` espalhados nos dois, seis já estavam
absorvidos, três eram repetição byte a byte das que vieram, e seis eram versões
inéditas.

A comparação foi pelo corpo do arquivo: hash com a linha `\ProvidesPackage` e os
fins de linha CRLF descartados. Comparar os bytes crus dá falso negativo nos
quinze, porque é exatamente a linha de identidade que se reescreve ao arquivar —
foi o que aconteceu na primeira tentativa desta varredura, que acusou quinze
faltantes onde havia seis.

| arquivo | origem | sha256 (12) |
|---|---|---|
| `crp-cadernoB.sty` | `cuissi-crp06/cadernoB`, `intranet/comunicacao/politica_e_manual/arquivo/` | `388a5088101a` |
| `formularios-relatorio_editorial.sty` | `cuissi-crp06/relatorio_editorial`, raiz | `0dd85ab5e9b4` |
| `livros_crp-politica_e_manual.sty` | `cuissi-crp06/cadernoB`, `intranet/comunicacao/politica_e_manual/arquivo/` | `2456f7450abe` |
| `livros_crp-intranet_relatorio.sty` | `cuissi-crp06/cadernoB`, `intranet/comunicacao/relatorio/` | `9abe25d58db5` |
| `livros_crp-premio_jonatas_salatiel.sty` | `cuissi-crp06/cadernoB`, `redação/premio_jonatas_salatiel/` | `2f2082049f80` |
| `livros_crp-cadernoB_planejamento_estrategico.sty` | `cuissi-crp06/cadernoB`, `revisão/planejamento_estrategico/` | `7754a42e7ca1` |

`crp-cadernoB.sty` é o único que não declarava pacote nenhum na origem: ali a
linha foi acrescentada, não reescrita. São 711 bytes — `fontspec` com NewJune,
`geometry`, um `\makepagestyle{crp}` e uma lista de tarefas —, o ancestral mais
simples do conjunto. Aparece três vezes no `cadernoB`, byte a byte idênticas:
em `politica_e_manual/arquivo/` e nas duas de `revisão/202407/politica_de_ti/`.

`livros_crp-cadernoB_planejamento_estrategico.sty` não é o mesmo arquivo que
`livros_crp-publicacoes-PE2025.sty`, embora os dois sirvam ao planejamento
estratégico: os corpos divergem.

### Equivalências que dispensaram cópia

Confirmadas por hash do corpo, com a ressalva de que nenhuma é igualdade de
bytes — as três são variantes de fim de linha e de linha de identidade sobre o
mesmo conteúdo:

- `relatorio_editorial/livros_crp.sty` (`e2000ed8827a`) tem o corpo de
  `crpsp-memoir/livros_crp_v7.sty`. É uma terceira variante do mesmo conteúdo:
  o v7 do monorepo veio de `editoracao/LaTeX/sty/` (`ccbe769e457b`).
- `cadernoB/intranet/comunicacao/relatorio/formularios.sty` (`c7cb2e429d40`) tem
  o corpo do `formularios-relatorio_editorial.sty` trazido acima.
- `apresentacoes_acessiveis/livros_crp.sty`, `cartilha_anticapacitista/livros_crp.sty`
  e `editoracao/manual/livros_crp.sty` já estavam aqui desde 2026-09-04.

## Trazida de fora do monorepo em 2026-09-12

Varredura dos `.sty` do workbench durante o encerramento da máquina Windows
doméstica. Dos 46 corpos distintos que o workbench carrega, 44 já estavam
absorvidos — a comparação foi pelo corpo, como na varredura de 2026-09-05, e
incluiu `\ProvidesFile` na declaração descartada, que a primeira tentativa
esquecera. Sem isso o `crpsp-leg.sty` aparecia como inédito, quando é o mesmo
arquivo de `crpsp-book/` linha por linha.

| arquivo | origem | sha256 (12) da origem | sha256 (12) do blob |
|---|---|---|---|
| `requerimento.sty` | `trabalho`, `production/editorial/formularios/requerimentos/` | `703e6d939e1e` | `50e12421cf86` |

Duas colunas porque os dois números são diferentes, e a razão está na seção
seguinte.

**Nenhum documento o carrega.** Os sete `.tex` daquela pasta são `abntex2` e
declaram os próprios pacotes com `\usepackage` linha a linha; nenhum tem
`\usepackage{requerimento}`. Por isso ele vem para cá, e não para
`crpsp-forms/`: é pacote escrito e não implantado, que é exatamente o que esta
pasta guarda. Compartilha 6 dos 104 versos de corpo com o `crpsp-forms/formularios.sty`,
então também não é variante dele.

A origem declarava só `\ProvidesPackage{requerimento}`, sem data nem versão. Em
2026-09-13 a declaração ganhou `[2024/07/19 v0.1.0-alfa …]`: a data é a da última
gravação do arquivo de origem, e `alfa` porque nunca foi implantado. O corpo não
mudou, mas o blob sim: passa de `50e12421cf86` para `479f6669d0c7`.

Mantém o nome `requerimento`, que já é o seu e que ninguém mais disputa. A regra
de renomear vale para os doze `livros_crp`, que disputavam a mesma identidade.

Os dois `.tex` que faltavam da mesma pasta foram para `formularios/`, onde os
outros cinco já estavam:

| arquivo | sha256 (12) da origem | sha256 (12) do blob |
|---|---|---|
| `requerimento.tex` | `0f999ec78c99` | `b161e0b1d78f` |
| `requerimento_interativo.tex` | `32b6b238fcbf` | `5d55e476ab28` |

### Correção: os bytes **não** são os da origem

A seção de 2026-09-04 afirma que, por não haver `.gitattributes`, os bytes
gravados são os da origem. **Isso está errado**, e quem tentar conferir as
tabelas antigas vai tropeçar nisso: este clone tem `core.autocrlf=true`, que
normaliza CRLF para LF **ao gravar no índice**, independentemente de
`.gitattributes`. O que a configuração faz é justamente o que a ausência do
arquivo não impede.

Dos quatro trazidos hoje, três estavam em CRLF na origem e foram normalizados. O
quarto, `relatorio-gestao.sty`, já era LF e escapou da conversão — mas o blob dele
também difere da origem, por outro motivo: a linha de identidade foi reescrita ao
arquivar, de `v0.2` para `v0.5.0`, como manda a série de `crpsp-memoir/`.

| arquivo | destino | sha256 (12) da origem | sha256 (12) do blob |
|---|---|---|---|
| `relatorio-gestao.sty` | `crpsp-memoir/` | `712b68c08530` | `3445eb889e84` |

Nesse o corpo é idêntico verso por verso ao da origem; a diferença é só a
declaração. É o mesmo caso descrito na varredura de 2026-09-05, em que a linha de
identidade é justamente o que se reescreve ao arquivar.

Por isso as entradas de hoje trazem os dois números: o da origem, que é o que se
confere contra o workbench, e o do blob, que é o que `git show` devolve.

As tabelas anteriores trazem um número só, e não foi reconferido qual dos dois
é — quem precisar auditá-las deve considerar as duas possibilidades.

### Correção de 2026-09-13: eram 42, não 44

Refeita com `ferramentas/comparar-corpo.py --repo .`, que procura cada corpo em
todos os blobs do histórico, a varredura dá os mesmos 46 corpos distintos, mas
**quatro** fora do repositório antes do PR #3, e não dois:

- `relatorio-gestao.sty` e `requerimento.sty`, trazidos acima;
- a cópia de `livros_crp_acessivel_book.sty` em `production/editorial/publicacoes/cartilhas/apresentacoes_acessiveis/LaTeX/`, que é o canônico da linha `book` com o ambiente `NomesDuasColunas` a mais. Entrou em `crpsp-book/` como 0.5.1, e procedência e somas estão em `crpsp-book/CHANGELOG.md`, porque não é cópia por projeto;
- `production/editorial/publicacoes/gestao/caderno_12_corepsi/v2/livros_crp.sty` (gravado em 2026-04-09), variante da `crpsp-memoir/livros_crp-rev_cld.sty`: acrescenta `epstopdf`, tira o `urlbreaks` do `xurl` e o `\fontebook` das listas de cargos e nomes, e põe `\sffamily` num bloco. É a tentativa `memoir` do Caderno 12, que depois saiu pela linha `book` 0.5.0. **Não foi trazida**: pelo precedente de 2026-09-05 caberia aqui como cópia por projeto, e fica para decisão.

Uma segunda armadilha de comparação apareceu na mesma conferência. Descartar só a
**linha** do `\Provides*` não basta quando a declaração ocupa duas:
`crpsp-base.sty` e `relatorio.sty` do workbench trazem `[2026/07/03 v0.1` numa
linha e a descrição na seguinte. Com o filtro por linha, a continuação sobra no
corpo, e os dois parecem diferentes dos daqui sem ser. É preciso descartar a
declaração inteira, do `\Provides` até o `]` que a fecha.

## Limite

A fase de duas delas não está determinada. O `livros_crp-editoracao_manual.sty`
serve o Manual de Direitos Humanos e o `livros_crp-apresentacoes_acessiveis.sty`
o repositório homônimo; em nenhum dos dois casos o repositório registra se a
publicação circulou fora da casa. Ficaram sem sufixo de fase.

O mesmo limite aparece dentro do monorepo: `livros_crp-manual_dh.sty` e
`livros_crp-publicacoes-carta_de_servicos.sty` são byte a byte o mesmo arquivo,
servindo uma publicação que circulou e outra que não. A fase é propriedade da
publicação, não do arquivo, e por isso as cópias arquivadas não a carregam.
