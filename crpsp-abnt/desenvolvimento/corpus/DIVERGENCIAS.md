# Divergências do biblatex-abnt 4.0 e do crpsp-abnt

> **medido em:** 2026-09-28, TeX Live 2026 (`biblatex-abnt` 4.0, 2024-07-04), opções padrão
> **corpus:** `trilha-6023.bib` (107 exemplos da 6023:2025) e `chamadas-10520.tsv`
> (29 chamadas da 10520:2023), nas seções que o guia usa (briefing, seção 5); desde o
> Sprint 6, também `jurisprudencia-6023.bib` (5) e `demais-6023.bib` (175), o corpus completo
> **medida bruta:** `medida-abnt-4.0.tsv` e `medida-abnt-4.0-chamadas.tsv`

Refazer:

```sh
python3 medir.py trilha-6023.bib > medida-abnt-4.0.tsv
python3 medir.py trilha-10520.bib --chamadas chamadas-10520.tsv > medida-abnt-4.0-chamadas.tsv
```

⚠️ Desde o Sprint 1 o corpus usa os campos `ementa` e `complementos` do `crpsp-abnt` nas 15
entradas `@legislation`/`@legal`, onde antes havia `titleaddon` e `addendum`. O upstream
descarta esses campos. A medida dele vale para o corpus do Sprint 0, o do commit `c42352d`,
e refazê-la sobre o corpus atual dá números menores.

## Medida do `crpsp-abnt`

```sh
export TEXINPUTS="$(cd ../.. && pwd)//:"
python3 medir.py trilha-6023.bib --estilo crpsp-abnt > medida-crpsp-abnt-0.2.1.tsv
python3 medir.py trilha-10520.bib --chamadas chamadas-10520.tsv --estilo crpsp-abnt > medida-crpsp-abnt-0.2.1-chamadas.tsv
```

| Versão | Referências iguais | Chamadas iguais | Linhas fechadas |
|---|---:|---:|---|
| upstream 4.0 | 44/107 | 22/29 | — |
| 0.1.0-alfa (Sprint 1) | 53/107 | 22/29 | 4 e 5 |
| 0.2.0-alfa (Sprint 2) | 85/107 | 27/29 | 1, 2, 3, 6, 9, 11, 12 e 21 |
| 0.2.1-alfa (Sprint 3) | 85/107 | 27/29 | 22, 23, 24 e 25 |
| 0.3.0-alfa (Sprint 5) | 85/107 | 27/29 | 26 (fora da trilha) |

No Sprint 1, nove referências passaram a sair iguais à norma, e nenhuma das que já
saíam iguais passou a divergir. As chamadas continuam as do upstream. Nas seções
7.11, quatro exemplos ainda divergem, todos pelas linhas 1 e 3: 7.11.1:3, 7.11.5:1,
7.11.5:3 e 7.11.5:5.

No Sprint 2, mais 32 referências e 5 chamadas passaram a sair iguais, de novo sem
regressão. Os 15 exemplos das seções 7.11 saem todos iguais. As 22 referências que
ainda divergem são das linhas 13 a 20, deixadas para depois da entrega, da linha 7
(`Spring/Summer`) ou de defeito de extração. As duas chamadas que divergem são da
linha 10, e o `et al.` foi escolhido.

No Sprint 3, a medida não muda. As linhas 22 a 25 vieram da composição do guia, e
nenhum exemplo do corpus passava por elas: as teses traziam `eventdate` como contorno.
Ele saiu das seis teses, que seguem iguais pelo mapa novo. Os casos das quatro linhas
estão em `../casos/`.

No Sprint 5, a medida da trilha não muda: `@jurisdiction` não está nas seções do
guia. A jurisprudência é medida à parte, na seção seguinte.

⚠️ No Sprint 2, os DOIs de 7.7.6:7 e 7.7.6:8 passaram a ser escritos no corpus como a
norma os imprime, com o resolvedor. A forma do DOI é do dado (linha 6).

## Jurisprudência (fora da trilha)

As seções 7.11.3 e 7.11.4 não estão no guia e têm corpus próprio,
`jurisprudencia-6023.bib`, com os 5 exemplos da 6023:2025. Ele entra no corpus
completo do Sprint 6.

```sh
python3 medir.py jurisprudencia-6023.bib --estilo abnt > medida-abnt-4.0-jurisprudencia.tsv
python3 medir.py jurisprudencia-6023.bib --estilo crpsp-abnt > medida-crpsp-abnt-0.3.0-jurisprudencia.tsv
```

| Versão | Referências iguais |
|---|---:|
| upstream 4.0 | 0/5 |
| 0.3.0-alfa (Sprint 5) | 5/5 |

Como na legislação, o corpus já usa os campos do `crpsp-abnt` (`orgao`, `ementa`,
`partes`, `relator`), que o upstream descarta. A medida do upstream mostra o que se
perde, não o que ele faria com um `.bib` escrito para ele.

## Corpus completo (Sprint 6)

`demais-6023.bib` tem os 175 exemplos da 6023:2025 que não estão na trilha nem na
jurisprudência. Com os dois, o corpus cobre 287 das 289 referências de `nbr6023.tsv`.
As duas que ficam fora são defeito de extração: 9.1:1b junta duas referências numa linha,
e 8.7.1:8 (`3 DVD (60 min)`) é fragmento classificado como referência. Os 40 fragmentos
(8.4.1, 8.6.1.3, 8.7.1, 9.2) não são referências e não entram.

```sh
python3 medir.py demais-6023.bib --estilo abnt > medida-abnt-4.0-demais.tsv
python3 medir.py demais-6023.bib --estilo crpsp-abnt > medida-crpsp-abnt-0.3.0-demais.tsv
```

| Corpus | Upstream 4.0 | 0.3.0-alfa |
|---|---:|---:|
| Trilha (107) | 44 | 85 |
| Jurisprudência (5) | 0 | 5 |
| Demais (175) | 82 | 107 |
| **Referências (287)** | **126** | **197** |
| Chamadas (29) | 22 | 27 |

A medida do upstream na trilha é a do corpus do Sprint 0 (ver o aviso no topo). Nos
demais, o `crpsp-abnt` acerta 25 exemplos a mais, e nenhum que o upstream acertava passa
a divergir. As 68 divergências que restam são todas herdadas do upstream, que erra do
mesmo jeito. Estão nas linhas 13, 15, 17, 18, 20 e 27 a 33 da tabela, e em "O que não é
do estilo".

A codificação segue a regra da trilha, e onde o biblatex não tem campo, a do teste do
upstream (cabeçalho de `demais-6023.bib`). Filme, vídeo, som, imagem, obra de arte e
correspondência não têm driver no upstream nem no `crpsp-abnt`. Caem no de `@misc`, que
os imprime, com o aviso `No driver for …` na compilação. Das 39 entradas desses tipos,
31 saem iguais.

⚠️ No LuaTeX, o `-{}-` do teste do upstream não impede a ligadura: `[18-{}-]` sai
`[18–]`. O corpus escreve `[18-\/-]`. Vale para o `.bib` de qualquer publicação.

## Régua

`../verificar.sh` roda tudo e compara com a linha-base da versão (os
`medida-crpsp-abnt-<versão>*.tsv`, com a versão lida do `\ProvidesFile` do `.bbx`):

1. os três corpora da 6023 e as chamadas da 10520, medidos com o PDF tagueado
   (`medir.py --tagueado`), e comparados entrada por entrada por `comparar.py`;
2. cada PDF do corpus no veraPDF UA-2;
3. os casos: texto, links, esqueleto da árvore de tags (`show-pdf-tags`) e veraPDF.

A comparação é de texto normalizado, não de pixels. Qualquer mudança no texto obtido faz
a régua sair com 1, inclusive a melhora: a linha-base nova se grava de propósito, com a
versão nova. O texto do PDF tagueado é o mesmo do PDF sem tags, e por isso as medidas
antigas servem de linha-base.

Rodar depois de todo `tlmgr update` (briefing, seção 6). Em 28/09/2026, com o TeX Live
2026 atualizado, a régua sai igual à linha-base 0.3.0 em 32 s, e os cinco PDFs passam no
veraPDF 1.30.2.

## Resultado

| Corpus | Igual | Difere |
|---|---:|---:|
| Referências (6023) | 44 | 63 |
| Chamadas (10520) | 22 | 7 |

Uma referência pode ter mais de uma divergência, e por isso a soma da coluna
"casos" passa de 63. As chamadas de autor, de pessoa jurídica, de sigla
(`(IBGE, 2011, p. 3)`), de várias obras e com localizador saem certas. O que
quebra é a chamada por título.

A premissa da sigla como entrada (`IBGE — INSTITUTO…`) não está na norma e não
tem exemplo no corpus. Os casos de teste dela são nossos, em `../casos/`.

## Divergências do estilo

"Guia" diz se o tipo de referência aparece nas ~57 do guia (briefing, seção 5).

| # | Divergência | Casos | A norma pede | O upstream produz | Sprint | Guia |
|---|---|---:|---|---|---|---|
| 1 | ✅ Intervalo de páginas com meia-risca | 20 | `p. 1-74` | `p. 1–74` | 2 | sim: artigos, capítulos |
| 2 | ✅ Reticências de título de evento engolem o ponto | 9 | `Anais [...]. São Paulo` | `Anais [...] São Paulo` | 2 | sim: 1 evento |
| 3 | ✅ Qualificador de pessoa jurídica em caixa alta | 11 | `INSTITUTO NACIONAL DO CÂNCER (Brasil).` | `… (BRASIL).` | 2 | provável |
| 4 | ✅ Legislação e ato sem publicação oficial: `local, editora` | 8 | `Brasília, DF: Presidência da República, [2016]` | `Brasília, DF, Presidência da República, [2016]` | 1 | sim: leis e resoluções online |
| 5 | ✅ Legislação em monografia perde elementos | 3 | edição, `Organizado por`, `In: VADE mecum.` | edição e `In:` somem; editora antes do local e `320 p.` antes da data | 1 | não |
| 6 | ✅ DOI sem o resolvedor | 2 | `DOI: https://doi.org/10.1590/…` | `DOI: 10.1590/…` | 2 | sim: artigos |
| 7 | ✅ Intervalo de meses com meia-risca | 5 | `jul./ago. 2009` | `jul.–ago. 2009` | opção | sim: artigos |
| 8 | ✅ Mais de três autores viram `et al.` | 4 | todos, ou o primeiro e `et al.` (8.1.1.2) | `et al.` | opção | sim: artigos |
| 9 | ✅ Chamada por título | 5 | `(Inglês, 2012)`, `(A flor [...], 1995)` | `(INGLÊS..., 2012)`, `(A..., 1995)` | 2 | sim: 4 entradas pelo título, se ficarem |
| 10 | ⏸ Chamada com mais de três autores | 2 | `Maciel, Brum, Del Bianco e Costa (2019)` | `Maciel et al. (2019)` | opção | a ver |
| 11 | ✅ Folhas impressas como páginas | 2 | `82 f.`, `f. 19-20` | `82 p.`, `p. 19–20` | 2 | sim: 2 trabalhos acadêmicos |
| 12 | ✅ `@manual` descarta a editora | 1 | `Rio de Janeiro: ABNT, 2011.` | `Rio de Janeiro, 2011.` | 2 | se houver NBR citada |
| 13 | Sem editora, insere `[s. n.]` (e `[S. l.]`) | 1 + 8 | `[Florianópolis: UFSC], 2012.` | `[Florianópolis: UFSC]: [s. n.], 2012.` | depois | não |
| 14 | URL com acento sai codificada | 1 | `…/Relatório-de-Atividades…` | `…/Relat%C3%B3rio-de-Atividades…` | depois | a ver |
| 15 | Várias editoras em vários locais | 2 + 1 | `Rio de Janeiro: UFRJ; São Paulo: CRUESP` | `Rio de Janeiro e São Paulo: UFRJ e CRUESP` | depois | não |
| 16 | `et al.` some da lista de tradutores | 1 | `Tradução Vera da Costa e Silva et al.` | `Tradução: Vera da Costa e Silva.` | depois | não |
| 17 | Campos que o estilo não imprime | 2 + 1 | `Título original: …`, `Ilustrações de …` | nada | depois | não |
| 18 | Ordem de elementos complementares | 7 + 22 | ordem da norma | dimensão, série, nota, páginas e edição fora do lugar | depois | não |
| 19 | Separata | 1 | `Separata de:` | `In:` | depois | não |
| 20 | Mês em inglês em minúscula (ou abreviado) | 1 + 1 | `Nov. 2009` | `nov. 2009` | depois | a ver |
| 21 | ✅ Entrada pelo título com artigo: só o artigo em maiúsculas | — | `A FLOR prometida` (8.2.1) | `A flor prometida` | 2 | sim: `THE EVIDENCE underlying…` |
| 22 | ✅ `@online` descarta local e editora | — | `Washington, DC: ASAN, [2016?].` | `[2016?].` | 3 | sim: 4 páginas com editora |
| 23 | ✅ Página sem data: a chamada leva o ano do acesso | — | a mesma data na chamada e na referência | `(Deaf Services Unlimited, 2026)`, referência sem ano | 3 | sim: 4 páginas sem data |
| 24 | ✅ Páginas com letra saem em minúscula e sem `p.` | — | `p. E16-E18` | `e16-e18` | 3 | sim: 1 artigo |
| 25 | ✅ Trabalho acadêmico sem o ano da defesa | — | `– Universidade …, Natal, 2023.` (7.1.2) | `– Universidade …, Natal.` | 3 | sim: 2 trabalhos acadêmicos |
| 26 | ✅ Jurisprudência sem driver | 5 | `(2. Turma)`, ementa, partes, `Relatora: …, julgado em 29 nov. 2005`, `Brasília, DF: Superior Tribunal de Justiça, [2006]` | driver de artigo: sem órgão julgador, ementa, partes e julgamento; `Brasília, DF, …` | 5 | não |
| 27 | Coleção de periódico: intervalo com barra | 14 | `1939- .`, `1929-1975` | `1939/.`, `1929/1975` (o upstream: `1939–.`) | depois | não |
| 28 | Fascículo (`@periodical`) sem volume e número | 5 | `v. 38, n. 9, set. 1984` | `set. 1984` | depois | não |
| 29 | Várias editoras no mesmo local | 4 | `São Paulo: Delta: Estadão` (8.5.3) | `São Paulo: Delta e Estadão` | depois | a ver |
| 30 | Pontuação da descrição física | 12 | `267 p., il.`, `[46] p.`, `(2 p.).` | `267 p. il.`, `[46].`, `(2 p.)` | depois | não |
| 31 | Número de volumes não sai | 3 | `4 v.` | nada | depois | não |
| 32 | Data com semestre ou com hora | 2 | `2. sem. 1996`; `19 jun. 2013, 23:09` e o acesso com hora | `S2`, sem tradução; a data e o acesso somem | depois | não |
| 33 | Versão de programa não sai | 1 | `Versão 10.11.6.` | nada | 4 | não |

Os casos de cada linha, por id do corpus:

1. 7.3:1–5, 7.7.5:2–8, 7.7.6:7, 7.8.4.1:1–2, 7.8.5:4, 7.11.1:3, 7.11.5:3, 7.11.5:5.
2. 7.8.4.1:1–3, 7.8.5:1–2, 7.8.5:4, 8.1.3:1.1, 8.1.3:2.1–2.2. Contorno no dado:
   `Anais [\ldots]\@`. O `.bib` de teste do upstream usa `[\ldots]` e cai no mesmo defeito.
3. 7.4:1, 7.4:4, 7.11.5:1, 7.11.5:3, 8.1.1.7:1, 8.1.2.1:1, 8.1.2.2:1, 8.1.2.3:1,
   8.1.2.5:1a–1b, 8.5.4:1. Contorno no dado: `{Instituto Nacional do Câncer \NoCaseChange{(Brasil)}}`.
   A unidade subordinada em `nameaddon` já sai certa (`BANCO CENTRAL DO BRASIL. Diretoria
   Colegiada.`); em `bookauthor` não há `nameaddon`, e 7.4:4 fica errada.
4. 7.11.1:1, 7.11.2:1–3, 7.11.5:6, 7.11.6:1–2, 8.1.2.3:2. É o alias para o driver de artigo
   (briefing, 2.2). Com publicação oficial (7.11.1:3, 7.11.5:2 e 5:4) sai certa, desde que o
   ano do diário venha como `volume = {ano 139}`, a convenção do upstream. O contrato de
   campos do Sprint 1 decide se fica assim.
5. 7.11.1:1 (edição), 7.11.1:2 (organizador e ordem), 7.11.2:3 (`In:`).
6. 7.7.6:7–8. A 2025 dá o DOI como URL (briefing, 2.5), mas não em todo exemplo: 7.2.2:6
   e 7.7.2 trazem o DOI sem resolvedor, e 7.7.6:7 traz `http://dx.doi.org/`. A norma não
   fixa a forma. Desde a 0.2.0, o estilo imprime o `doi` como está no `.bib`, e o corpus
   escreve cada um como a norma o imprime.
7. 7.7.5:1, 7.7.5:4, 7.7.5:6, 7.7.6:7, 8.1.1.9:1. O `crpsp-abnt` fixa a opção
   `slashdaterange` do upstream, que resolve os meses. 7.7.5:4 (`Spring/Summer`) ainda sai
   traduzida, como `primavera/verão`.
8. 7.7.5:2, 7.7.6:8, 7.8.4.1:2, 8.1.1.2:2. O `crpsp-abnt` fixa `maxbibnames=20` e
   `minbibnames=20`.
9. 10520:6.1.1.4:a.1–d.1, 7.1.4:3.
10. 10520:6.1.2:2 e 6.1.4:2. A 10520 admite as duas formas. O `crpsp-abnt` escolheu a
    curta (`maxcitenames=3`, `mincitenames=1`), e por isso os dois casos seguem
    divergindo da forma longa do exemplo.
11. 7.1.2:3b, 8.1.1.6:3 (`bookpagination = {leaf}`; o `.lbx` não tem `leaftotal`), e 7.3:2.
12. 8.1.2:1.
13. 8.1.2.4:1. No corpus completo: correspondência (7.5:1a–1b, 7.5:2, 7.6:1), programa e
    jogo (7.20:1, 7.20:3), coleção de periódico sem editora (8.2.5:1) e trabalho não
    publicado (8.11:3, `[S. l.]`). A norma omite a editora quando ela não se aplica, e o
    estilo a completa. Na correspondência, `options = {noslsn}` não serve: 7.5:2 pede o
    `[S. l.]` e não o `[s. n.]`. Entra no Sprint 4, com a escolha do `[S. l.]` online.
14. 8.1.2.4:1.
15. 7.8.5:2, 8.1.2.1:1. No corpus completo: 8.5.2:1.
16. 8.1.1.6:2.
17. 7.1.1:2b (`origtitle`), 8.1.1.6:1 (`illustrator`). No corpus completo: 8.11.1:1
    (`origtitle`).
18. 7.1.1:1b, 7.2.2:1b, 7.3:5 (`v. 1.` por `v. 1,`), 7.7.5:5 (`ed. 943`), 7.8.4.1:3,
    7.8.5:4, 8.1.3:2.1. No corpus completo, três padrões:
    - o `addendum` sai depois do endereço eletrônico, e a norma põe a nota antes do
      `Disponível em:` (7.7.8:2, 7.10:1, 7.18:1, 7.18:3–6, 7.20:5);
    - a nota sai antes da data e da série, e a norma a põe no fim: ISSN antes da
      periodicidade (7.7.1:1b, 7.7.1:3, 7.7.2:1b, 7.7.4:5), `8.7.3:6` como 7.2.2:1b,
      folhas (7.15:6), ISBN depois da nota (8.5:1, 8.11.3:1), evento em periódico
      (7.8.2:1–2);
    - na rede social, o perfil (`Twitter: @biblioufal`) sai antes do local e da data
      (7.20:4, 7.20:6, 8.7.3:2, 8.7.3:5). É do driver `@online` da 0.2.1, e entra no
      Sprint 4.
19. 7.3:4.
20. 7.7.6:5. No corpus completo: 7.16:1 (`1 June 2010`, com `langid = {english}`).
27. Coleção: 7.7.1:1a–1b, 7.7.1:2–3, 7.7.2:1a–1b, 7.7.2:2, 7.7.3:1, 8.2.3:1, 8.2.4:1,
    8.2.5:1, 8.6.1.5:1, 8.6.1.6:1; em livro, 8.6.1.4:1 (`1926-1940`). O corpus usa o
    intervalo do biblatex (`date = {1939/}`); o teste do upstream escreve
    `year = {1939-\nopunct}`, que é texto e não data.
28. 7.7.4:1–5.
29. 7.2.1:1, 8.2.2:2, 8.5.3:1, 8.10:1. `publisher = {Delta and Estadão}`.
30. Vírgula antes de ilustração e dimensão: 8.5:1, 8.8:1–3, 8.9:1–2, 8.11.2:1,
    8.11.3:1–2; paginação entre colchetes: 8.7.2.5:1; ponto final depois de `p.)`:
    8.7.2:3, 8.7.3:6. Ilustração e dimensão vão em `note`, que é o que o biblatex tem.
31. 8.4.2:1, 8.6.1.4:1, 8.7.2.2:1 (`volumes`).
32. 8.6.2.1:2 (`date = {1996-41}`, a divisão de ano do biblatex; falta a string
    `S2` no `.lbx`) e 8.6.3:2 (`date = {2013-06-19T23:09}`; a data com hora não sai, e o
    acesso some junto).
33. 7.20:1 (`version`). A editora igual ao autor, que a Emenda 1 tirou (`Apple`), fica fora
    do `.bib`; o `[s. n.]` que o estilo põe no lugar é da linha 13.
21. Casos próprios (`../casos/`).
22–25. Achadas ao compor o guia (`checagem_referencias.md`, no workbench) e guardadas
    em `../casos/`. A 25 aparecia no corpus, mas o `eventdate` das teses a escondia. A 23
    não tem saída certa só no estilo: a 6023 pede um ano entre colchetes (8.6.1.3), que é
    do dado. O estilo tira o acesso da chamada, que passa a sair com `s.d.`, e avisa na
    compilação.
26. 7.11.3:1–2, 7.11.4:1–3, em `jurisprudencia-6023.bib`, fora da trilha. Os casos que a
    norma não traz (relator sem `relatortype`, julgamento sem relator) estão em `../casos/`.

## O que não é do estilo

- **Defeitos de extração do PDF da norma** (briefing, seção 6): 7.2.2:1a (`http ://`,
  `2011..`) e 7.7.6:8 (espaços dentro da URL). O estilo sai certo; o corpus é que está
  errado. No corpus completo: espaços dentro da URL em 7.7.2:1a (`sci_ serial`), 7.10:1,
  7.18:3 e 7.18:6, e `maio/ ago.` em 8.2.6:1. O `.bib` escreve a URL sem os espaços.
  `(coord.) História`, sem ponto, em 8.5.2:1, é da extração ou da norma.
- **A norma se contradiz:**
  - `Tradução:` com dois-pontos em 7.1.1:2b, e `Tradução` sem eles em 7.1.1:3b, 8.1.1.4:3
    e 8.1.1.6:2. O upstream põe dois-pontos, e a diferença entra na medida como divergência
    de três casos;
  - em 8.1.3:2.2 o ano do evento vem seguido de ponto (`2014. Kuala Lumpur`), e em todos os
    outros eventos, de vírgula;
  - `Tradução de` e `Revisão técnica`, sem dois-pontos, na forma antiga, em 8.4.2:1 e
    8.11.2:1;
  - o podcast de 7.13.5:1 traz `[S. l.]: Escriba Café`, e o mesmo exemplo em 8.7.3:1 não
    traz o `[S. l.]`. O `.bib` é o mesmo, e 8.7.3:1 diverge. A escolha é do Sprint 4.
- **Fora do modelo de datas:** 7.7.6:6 e 8.6.1.2:1 (`26 Tishrei 5766 = 29 out. 2005`).
- **Sem campo no biblatex**, e por isso codificado em `titleaddon`: orientador (7.1.2:3b,
  8.1.1.6:3), entrevistadores (7.7.5:6), psicografia (8.1.1.7:1), adaptação (8.1.1.8:1),
  entrevista (8.1.1.9:1). Saem certos. Se o `crpsp-abnt` ganhar campos para eles, entram
  aqui como caso novo. No corpus completo, também vão em `titleaddon` os créditos de
  filme, vídeo, som e partitura, o destinatário da correspondência e o depositante da
  patente, e a maioria sai certa. Três exemplos não têm codificação que saia certa:
  - o evento como entrada de um cartaz (7.16:3): o `author` sai inteiro em maiúsculas,
    inclusive a cidade;
  - o evento publicado em periódico (7.8.2:1–2): o `@proceedings` não tem campo para o
    periódico, e o fascículo colide com o número do evento.

## Leitura para a trilha

- **Sprint 1** (legislação e ato): as linhas 4 e 5, fechadas na 0.1.0-alfa (✅ na tabela).
  A 4 é a que pesava, porque o guia cita as leis e as resoluções pela versão online.
- **Sprint 2** (sigla e chamada): as linhas 1, 2, 3, 6, 9, 11 e 12, e o caso da sigla
  como entrada, que é nosso. A 1 e a 2 são as mais frequentes e as mais baratas.
- **Sprint 2** feito na 0.2.0-alfa: as linhas 1, 2, 3, 6, 9, 11 e 12, mais a 21, achada
  no caso próprio da entrada pelo título. A sigla como entrada tem casos próprios em
  `../casos/`.
- **Opções** (7, 8, 10): fixadas na 0.2.0-alfa e registradas no README.
- **Sprint 3** (piloto), na 0.2.1-alfa: as linhas 22 a 25, que só apareceram ao
  compor o guia.
- **Depois da entrega:** 13 a 20. Nenhuma aparece no guia.
- **Sprint 5** (jurisprudência), na 0.3.0-alfa: a linha 26, medida fora da trilha.
- **Sprint 6** (corpus completo e régua), sem versão nova, porque o estilo não muda: as
  linhas 27 a 33 e os casos novos das 13, 15, 17, 18 e 20. Nenhuma aparece no guia. As
  linhas 13, 18 (rede social) e 33 são do Sprint 4 (mídia e documento online); as outras
  ficam sem sprint.
