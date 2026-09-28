# CRP SP LaTeX

**Rastreamento de desenvolvimento dos pacotes e classes LaTeX customizados do CRP-SP.**

Este repositório acompanha a genealogia e a evolução dos estilos — não é onde
os arquivos usados em produção residem; esses continuam localmente na
máquina de trabalho.

## Seções

[crpsp-book](/crpsp-book/)

Pacote `book-crpsp_acessivel.sty` — variante acessível (PDF/UA-2) da linha
editorial de livros, incluindo estado atual e monitoramento de dependências
CTAN.

Em `desenvolvimento/v2/` mora a linha seguinte, que não é só `book`:
`crpsp-base.sty` (paleta por publicação) e as linhas `guia`, `guia_visual`,
`formulario` e `relatorio`. Desde 2026-09-16 o desenvolvimento se concentra em
`relatorio`, `livro` (cartilha/manual) e `formulario`, todas acessíveis; a
linha `guia_visual` foi cancelada (o 16:9 migra para GitHub Pages) e o `guia`
não consta do escopo ativo. O `formulario` de lá é o candidato a formulário
acessível, e não se confunde com os de `crpsp-forms/`, que são `memoir`. Ficou
dentro de `crpsp-book/` porque o workbench espelha esta pasta
(`editorial/arquivo_latex/crpsp-book/`); mover quebra esse caminho.

[crpsp-abnt](/crpsp-abnt/)

Estilo biblatex que estende o `biblatex-abnt` para a NBR 6023:2018 e a
NBR 10520:2023 (documento jurídico, citação acessível, mídia). Em
planejamento: ver `crpsp-abnt/briefings/briefing-crpsp-abnt.md`.

[crpsp-forms](/crpsp-forms/)

Pacotes de formulários (`formularios.sty`, `form-sem-logo.sty`).

[crpsp-memoir](/crpsp-memoir/)

Linhagem `livros_crp*.sty` baseada em `memoir` — base histórica da linha
`book` antes da migração para a classe `book`, e ainda linha ativa:
`relatorio-gestao.sty` 0.5.0 serve o Relatório de Gestão.

[formularios](/formularios/)

Fontes `.tex` dos formulários e documentos institucionais em uso.

[legado](/legado/)

Variantes e cópias históricas fora do monorepo, preservadas para
proveniência (`legado/copias-por-projeto/PROVENIENCIA.md`).

[CONVENCAO-VERSIONAMENTO.md](/CONVENCAO-VERSIONAMENTO.md)

Como numerar versão, data, fase e nome declarado — e por que dois corpos nunca
podem compartilhar a mesma declaração.

**O que não fica aqui.** Conteúdo de publicação (a antiga pasta `publicacoes/`,
removida em 2026-09-13; cópia em `editorial/arquivo_latex/publicacoes/` no
Nextcloud) e a fonte institucional New June, que é proprietária
(`editorial/fonts/NewJune/` no Nextcloud). Os dois continuam recuperáveis pelo
histórico do git, mas não voltam para a árvore.

[ferramentas](/ferramentas/)

`comparar-corpo.py` — diz se um `.sty`/`.cls` já está em algum commit
comparando pelo corpo (sem a declaração `\Provides*` inteira, sem CR, sem as
quebras finais). É o teste antes de trazer qualquer cópia de produção:

    python3 ferramentas/comparar-corpo.py ~/Documentos/trabalho --repo .

[ANALISE-VARIANTES.md](/ANALISE-VARIANTES.md)

Levantamento mecânico de divergências entre variantes `.sty` — evidência
para decisões de consolidação, fechadas na seção "Resolução — 2026-09-04".

## Linguagem por repositório

Norma de 17/09/2026, para que a mesma travessia não tenha dois caminhos.

| Repositório | Linguagem |
|---|---|
| `crpsp-latex` | **TeX e Lua** |
| `normativas-pipeline` | **Python** |

Uma travessia que atravessa os dois — o gerador de créditos institucionais é o
primeiro caso — é escrita na linguagem **do repositório onde mora**, não na do
destino. O gerador vive no `normativas-pipeline`: sai em Python, ao lado do
`latexgen.py`, que já faz JSON → LaTeX. Lua fica para o que roda dentro das
classes, aqui.

A regra existe porque um `texlua` no pipeline não compartilharia ambiente
virtual, dependências nem testes com o resto dele — e porque dois caminhos
diferentes para a mesma conversão, no mesmo repositório, é dívida técnica
nascendo pronta.
