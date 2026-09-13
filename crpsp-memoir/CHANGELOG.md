# crpsp-memoir

Linha memoir. O pacote canônico é implantado sob o nome `livros_crp.sty`, e é
esse o nome que `crpsp-memoir.sty` declara. As demais variantes desta pasta
declaram o próprio nome de arquivo: nenhuma é implantada, e sem isso quatro
arquivos diferentes disputariam o mesmo nome de pacote.

## 0.5.0-beta — 2026/06/16

`relatorio-gestao.sty`, trazido de fora do monorepo em 2026-09-12 — procedência e
somas de verificação em `legado/copias-por-projeto/PROVENIENCIA.md`. É a linha do
Relatório de Gestão: `memoir`, carregado por
`\usepackage{relatorio-gestao}` pelo documento de `3.editoracao/`, com
`tabularray` para as tabelas de dados e `pdflscape` para os anexos em paisagem.

**Não confundir com a linha `relatorio` de `crpsp-book/desenvolvimento/v2/`.**
São duas respostas ao mesmo problema, em bases diferentes: esta é `memoir` e de
junho; aquela é `book`, de 2026/07/29, e declara `v0.1.0-alfa`. Dos 251 versos de
corpo desta, 5 aparecem na `livros_crp_v7.sty`, que foi o vizinho mais próximo que
o repositório tinha — ou seja, quase nada. É código novo, não variante.

### Sobre o remapeamento

A origem declarava `v0.2`, e esse rótulo não se ordena com a série `0.x` daqui: a
`0.2.0-alfa` desta pasta é de 2025/04/06, catorze meses antes. É o mesmo caso do
`v7.0` abaixo — numeração de outro esquema, herdada do projeto. O remapeamento
para 0.5.0 o põe depois da `0.4.0-beta`, que é a ordem em que foram escritos.

A declaração do arquivo foi reescrita para `v0.5.0` (hoje `v0.5.0-beta`), como nos demais desta pasta,
e a data de autoria (2026/06/16) ficou. **O corpo é idêntico verso por verso ao da
origem**: só a linha de identidade mudou.

**Beta**, porque o Relatório de Gestão circulou fora do CRP SP. Até 2026-09-13
esta entrada se chamava 0.5.0, sem sufixo, porque a circulação não estava
registrada quando a cópia foi tirada — a cópia era de uma edição em revisão
diagramada. Pela [convenção](../CONVENCAO-VERSIONAMENTO.md), a ausência de
sufixo fica reservada para versão estável.

## 0.4.0-beta — 2025/09/26

`livros_crp_v7.sty`, antes rotulado `v7.0`. Reengenharia do carregador de fontes.
É a geração das primeiras tentativas de PDF acessível — a princípio só com mais
atenção ao `hyperref` —, e por isso fecha o segundo dígito em 0.4. As
publicações da geração são a cartilha anticapacitista e o guia de boas práticas
para apresentações acessíveis, ambas de circulação externa; daí o `beta`.

`livros_crp_comentado.sty` é a versão anotada do mesmo trabalho, na mesma versão.

### Sobre o remapeamento

O rótulo `v7.0` vinha de um esquema anterior e não se ordenava com a série `0.x`:
declarado em 2025/09/26, era posterior à base `v0.2` de 2025/04/06, mas o número
sugeria o contrário. O remapeamento para 0.4.0 põe as duas na mesma ordem em que
foram escritas.

## 0.2.0-alfa — 2025/04/06

`crpsp-memoir.sty`, a base "Pacote editorial CRP-SP".

`livros_crp-rev_cld.sty` é uma variante revisada da mesma base, na mesma data.
Mantém o pacote `changes`, que a base removeu deliberadamente — marcação de
revisão não deve sair no PDF de entrega, e `changes` colide com `\comment`
definido por outros pacotes do pipeline. A base é, portanto, posterior. Da
variante vale portar o `urlbreaks` na opção do `xurl`.

## 0.1.0-alfa

`livros_crp_memoir_original.sty`, a base memoir original. A data declarada
(2026/09/04) é a desta passagem de versionamento: o arquivo não trazia data e o
histórico do git não a tem, porque entrou no repositório na consolidação de
2026-09-03.
