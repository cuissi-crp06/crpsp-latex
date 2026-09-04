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

## Limite

A fase de duas delas não está determinada. O `livros_crp-editoracao_manual.sty`
serve o Manual de Direitos Humanos e o `livros_crp-apresentacoes_acessiveis.sty`
o repositório homônimo; em nenhum dos dois casos o repositório registra se a
publicação circulou fora da casa. Ficaram sem sufixo de fase.

O mesmo limite aparece dentro do monorepo: `livros_crp-manual_dh.sty` e
`livros_crp-publicacoes-carta_de_servicos.sty` são byte a byte o mesmo arquivo,
servindo uma publicação que circulou e outra que não. A fase é propriedade da
publicação, não do arquivo, e por isso as cópias arquivadas não a carregam.
