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

## Limite

A fase de duas delas não está determinada. O `livros_crp-editoracao_manual.sty`
serve o Manual de Direitos Humanos e o `livros_crp-apresentacoes_acessiveis.sty`
o repositório homônimo; em nenhum dos dois casos o repositório registra se a
publicação circulou fora da casa. Ficaram sem sufixo de fase.

O mesmo limite aparece dentro do monorepo: `livros_crp-manual_dh.sty` e
`livros_crp-publicacoes-carta_de_servicos.sty` são byte a byte o mesmo arquivo,
servindo uma publicação que circulou e outra que não. A fase é propriedade da
publicação, não do arquivo, e por isso as cópias arquivadas não a carregam.
