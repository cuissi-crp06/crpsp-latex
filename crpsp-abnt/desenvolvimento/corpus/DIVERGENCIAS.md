# Divergências do biblatex-abnt 4.0 nas seções da trilha do piloto

> **medido em:** 2026-09-28, TeX Live 2026 (`biblatex-abnt` 4.0, 2024-07-04), opções padrão
> **corpus:** `trilha-6023.bib` (107 exemplos da 6023:2025) e `chamadas-10520.tsv`
> (29 chamadas da 10520:2023), nas seções que o guia usa (briefing, seção 5)
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

⚠️ No Sprint 2, os DOIs de 7.7.6:7 e 7.7.6:8 passaram a ser escritos no corpus como a
norma os imprime, com o resolvedor. A forma do DOI é do dado (linha 6).

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
| 13 | Sem editora, insere `[s. n.]` | 1 | `[Florianópolis: UFSC], 2012.` | `[Florianópolis: UFSC]: [s. n.], 2012.` | depois | não |
| 14 | URL com acento sai codificada | 1 | `…/Relatório-de-Atividades…` | `…/Relat%C3%B3rio-de-Atividades…` | depois | a ver |
| 15 | Várias editoras em vários locais | 2 | `Rio de Janeiro: UFRJ; São Paulo: CRUESP` | `Rio de Janeiro e São Paulo: UFRJ e CRUESP` | depois | não |
| 16 | `et al.` some da lista de tradutores | 1 | `Tradução Vera da Costa e Silva et al.` | `Tradução: Vera da Costa e Silva.` | depois | não |
| 17 | Campos que o estilo não imprime | 2 | `Título original: …`, `Ilustrações de …` | nada | depois | não |
| 18 | Ordem de elementos complementares | 7 | ordem da norma | dimensão, série, nota, páginas e edição fora do lugar | depois | não |
| 19 | Separata | 1 | `Separata de:` | `In:` | depois | não |
| 20 | Mês em inglês em minúscula | 1 | `Nov. 2009` | `nov. 2009` | depois | a ver |
| 21 | ✅ Entrada pelo título com artigo: só o artigo em maiúsculas | — | `A FLOR prometida` (8.2.1) | `A flor prometida` | 2 | sim: `THE EVIDENCE underlying…` |
| 22 | ✅ `@online` descarta local e editora | — | `Washington, DC: ASAN, [2016?].` | `[2016?].` | 3 | sim: 4 páginas com editora |
| 23 | ✅ Página sem data: a chamada leva o ano do acesso | — | a mesma data na chamada e na referência | `(Deaf Services Unlimited, 2026)`, referência sem ano | 3 | sim: 4 páginas sem data |
| 24 | ✅ Páginas com letra saem em minúscula e sem `p.` | — | `p. E16-E18` | `e16-e18` | 3 | sim: 1 artigo |
| 25 | ✅ Trabalho acadêmico sem o ano da defesa | — | `– Universidade …, Natal, 2023.` (7.1.2) | `– Universidade …, Natal.` | 3 | sim: 2 trabalhos acadêmicos |

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
13. 8.1.2.4:1.
14. 8.1.2.4:1.
15. 7.8.5:2, 8.1.2.1:1.
16. 8.1.1.6:2.
17. 7.1.1:2b (`origtitle`), 8.1.1.6:1 (`illustrator`).
18. 7.1.1:1b, 7.2.2:1b, 7.3:5 (`v. 1.` por `v. 1,`), 7.7.5:5 (`ed. 943`), 7.8.4.1:3,
    7.8.5:4, 8.1.3:2.1.
19. 7.3:4.
20. 7.7.6:5.
21. Casos próprios (`../casos/`).
22–25. Achadas ao compor o guia (`checagem_referencias.md`, no workbench) e guardadas
    em `../casos/`. A 25 aparecia no corpus, mas o `eventdate` das teses a escondia. A 23
    não tem saída certa só no estilo: a 6023 pede um ano entre colchetes (8.6.1.3), que é
    do dado. O estilo tira o acesso da chamada, que passa a sair com `s.d.`, e avisa na
    compilação.

## O que não é do estilo

- **Defeitos de extração do PDF da norma** (briefing, seção 6): 7.2.2:1a (`http ://`,
  `2011..`) e 7.7.6:8 (espaços dentro da URL). O estilo sai certo; o corpus é que está
  errado.
- **A norma se contradiz:**
  - `Tradução:` com dois-pontos em 7.1.1:2b, e `Tradução` sem eles em 7.1.1:3b, 8.1.1.4:3
    e 8.1.1.6:2. O upstream põe dois-pontos, e a diferença entra na medida como divergência
    de três casos;
  - em 8.1.3:2.2 o ano do evento vem seguido de ponto (`2014. Kuala Lumpur`), e em todos os
    outros eventos, de vírgula.
- **Fora do modelo de datas:** 7.7.6:6 (`26 Tishrei 5766 = 29 out. 2005`).
- **Sem campo no biblatex**, e por isso codificado em `titleaddon`: orientador (7.1.2:3b,
  8.1.1.6:3), entrevistadores (7.7.5:6), psicografia (8.1.1.7:1), adaptação (8.1.1.8:1),
  entrevista (8.1.1.9:1). Saem certos. Se o `crpsp-abnt` ganhar campos para eles, entram
  aqui como caso novo.

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
