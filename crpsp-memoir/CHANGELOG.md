# crpsp-memoir

Linha memoir. O pacote canônico é implantado sob o nome `livros_crp.sty`, e é
esse o nome que `crpsp-memoir.sty` declara. As demais variantes desta pasta
declaram o próprio nome de arquivo: nenhuma é implantada, e sem isso quatro
arquivos diferentes disputariam o mesmo nome de pacote.

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
