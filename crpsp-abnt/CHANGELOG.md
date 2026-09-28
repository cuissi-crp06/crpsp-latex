# Changelog do crpsp-abnt

Versões conforme `CONVENCAO-VERSIONAMENTO.md`, na raiz do repositório.

## 0.2.1-alfa — 2026-09-28

Sprint 3 da trilha do piloto: os quatro defeitos achados ao compor o guia
(linhas 22 a 25 de `DIVERGENCIAS.md`). Só o `.bbx` muda; `.cbx` e `.dbx` seguem na
0.2.0-alfa.

- `@online` com driver próprio: `Local: Editora, data.` antes do endereço, com
  `organization` no lugar da editora quando não há `publisher`. O driver do
  `standard.bbx` descartava `location` e `publisher`.
- A chamada não usa mais a data de acesso: página sem data saía
  `(Deaf Services Unlimited, 2026)` com a referência sem ano. Agora sai `s.d.`, com
  aviso na compilação pedindo o ano entre colchetes (6023, 8.6.1.3).
- Páginas com letra: `p. E16-E18`, não `e16-e18`. O upstream passava o campo por
  `\MakeLowercase` e só punha `p.` em numeral.
- Trabalho acadêmico com o ano da defesa no fim (7.1.2): sem `eventdate`, o mapa copia
  o ano de `date` ou `year`. O corpus tirou o `eventdate` das seis teses, onde era
  contorno.
- `desenvolvimento/casos/`: sete entradas novas: uma por defeito, o `eid` e o `@online` só com local.
- Medida: 85/107 referências e 27/29 chamadas, iguais às da 0.2.0, sem regressão.
  Nenhum exemplo do corpus passava por esses caminhos.

## 0.2.0-alfa — 2026-09-28

Sprint 2 da trilha do piloto: sigla como entrada e chamada.

- Sigla como entrada: `IBGE — INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA.`, com
  a chamada `(IBGE, 2011)` e a lista ordenada pela sigla. O sinal é automático: a
  entrada precisa ter `shortauthor` e um `author` só, entre chaves duplas.
- Um link por obra citada: `\parencite` com um link sobre `IBGE, 2011`, e
  `\textcite` com o link no nome.
- Chamada por título da 10520:2023: `(A flor [...], 1995)`.
- Referência: páginas com hífen, `Anais [...].` com o ponto, qualificador em caixa
  alta e baixa, folhas (`82 f.`), editora no `@manual` e artigo com a palavra seguinte
  na entrada pelo título (`A FLOR prometida`). O DOI sai como está no `.bib`, com
  link. Fecha as linhas 1, 2, 3, 6, 9, 11 e 12 de `DIVERGENCIAS.md`.
- Opções fixadas: `maxbibnames=20`, `minbibnames=20`, `maxcitenames=3`,
  `mincitenames=1` e `slashdaterange`.
- `desenvolvimento/casos/`: casos próprios (sigla, ordenação, links), com o
  `verificar.sh`, que também passa o PDF no veraPDF UA-2.
- Medida: 85 de 107 referências (0.1.0: 53) e 27 de 29 chamadas (antes: 22), sem
  regressão. As duas chamadas que faltam são o `et al.` de quatro ou mais autores, que
  foi uma escolha.

## 0.1.0-alfa — 2026-09-28

Sprint 1 da trilha do piloto: legislação e ato normativo.

- `crpsp-abnt.bbx`: driver próprio para `@legislation` e `@legal`. O upstream os
  mandava para o driver de `@article`. Com ele saem `local: editora` sem diário
  oficial, a edição, `Organizado por` e `In:` (linhas 4 e 5 de
  `desenvolvimento/corpus/DIVERGENCIAS.md`).
- `crpsp-abnt.dbx`: campos `ementa` e `complementos`. O corpus passou a usá-los
  no lugar de `titleaddon` e `addendum`.
- `crpsp-abnt.cbx`: só carrega o `abnt.cbx`.
- Medida: 53 de 107 referências iguais à norma (upstream: 44), sem regressão;
  chamadas inalteradas, 22 de 29. Uma amostra das seções 7.11 sob
  `tagging=on` passa no veraPDF UA-2.
