# crpsp-abnt

Estilo biblatex que estende o `biblatex-abnt` para a ABNT NBR 6023:2025 e a
NBR 10520:2023: documento jurídico (legislação, jurisprudência, ato
administrativo), citação autor-data acessível e mídia contemporânea.

**Estado:** `0.3.0-alfa`. O Sprint 3 da trilha do piloto segue em curso, com os defeitos
achados ao compor o guia corrigidos. O Sprint 5 deu driver próprio à jurisprudência.
O plano, a linha de base medida e as decisões estão em
[`briefings/briefing-crpsp-abnt.md`](briefings/briefing-crpsp-abnt.md). As divergências
que faltam fechar estão em
[`desenvolvimento/corpus/DIVERGENCIAS.md`](desenvolvimento/corpus/DIVERGENCIAS.md).

## Uso

```latex
\usepackage[style=crpsp-abnt, backend=biber]{biblatex}
```

O `crpsp-abnt.dbx` é carregado junto com o estilo, sem a opção `datamodel`. Fora
da árvore do TeX, a pasta precisa estar no `TEXINPUTS`.

| Arquivo | Papel |
|---|---|
| `crpsp-abnt.bbx` | carrega o `abnt.bbx`; opções, sigla como entrada, drivers de `@legislation`, `@legal` e `@jurisdiction`, correções de pontuação e caixa |
| `crpsp-abnt.cbx` | carrega o `abnt.cbx`; chamada por título e um link por obra |
| `crpsp-abnt.dbx` | os campos `ementa`, `complementos`, `orgao`, `partes`, `relator` e `relatortype`, e o interno `crpspsigla` |

## Opções fixadas

O estilo fixa estas opções, e cada uma pode ser trocada no `\usepackage`:

| Opção | Efeito | Motivo |
|---|---|---|
| `maxbibnames=20, minbibnames=20` | a referência traz todos os autores, até 20; acima disso, os 20 primeiros e `et al.` | 6023, 8.1.1.2: "convém indicar todos" |
| `maxcitenames=3, mincitenames=1` | a chamada de quatro ou mais autores é o primeiro e `et al.`: `Maciel et al. (2019)` | 10520, 6.1.4, admite as duas formas; a curta pesa menos para quem ouve pelo leitor de tela |
| `slashdaterange` | intervalo de meses com barra: `jul./ago. 2009` | 6023, 7.7.5 |

As duas primeiras são decisões do Angelo, de 28/09/2026.

## Sigla como entrada

Pessoa jurídica com sigla entra pela sigla, com travessão e o nome por extenso, e a
chamada sai com a sigla:

```
IBGE — INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA. Censo demográfico 2010 [...]
(IBGE, 2011, p. 3)
```

A forma não está na 6023. A 8.1.2 admite a entrada da pessoa jurídica "por extenso ou
abreviada", e esta forma combina as duas. Ela veio da orientação de uma especialista
da ABNT, registrada nas notas da revisão 2 do guia de apresentações acessíveis, e é o
padrão do pacote (decisão 3 do briefing).

O sinal é automático: a entrada vira sigla quando tem `shortauthor` e o `author` é um
nome só, inteiro entre chaves duplas.

```bibtex
author      = {{Instituto Brasileiro de Geografia e Estatística}},
shortauthor = {{IBGE}},
```

- A lista é ordenada pela sigla, porque é por ela que o leitor procura, vindo da
  chamada. Um `sortname` na entrada tem precedência.
- Pessoa física com `shortauthor` não vira sigla, porque tem prenome. Também não vira
  sigla a entrada com mais de um autor.
- Sem `shortauthor`, a pessoa jurídica entra por extenso, como no upstream.
- O qualificador fica em caixa alta e baixa, na sigla e fora dela:
  `INCA — INSTITUTO NACIONAL DO CÂNCER (Brasil).`
- No `In:` de capítulo, o `bookauthor` continua por extenso.

## Chamada

- **Um link por obra.** Em `\cite` e `\parencite`, o link cobre `IBGE, 2011`, e o
  localizador fica fora dele. Em `\textcite`, o link fica no nome. A segunda obra do
  mesmo autor, comprimida (`IBGE, 2010, 2011`), tem o link no ano. O upstream fazia
  dois links por chamada, e o leitor de tela lia os dois em separado.
- **Chamada por título** (10520, 6.1.1.4). Título de uma palavra sai inteiro:
  `(Inglês, 2012)`. Com mais palavras, sai a primeira e `[...]`: `(Anteprojeto [...],
  1987)`. Se a primeira é artigo ou monossílabo, saem as duas primeiras:
  `(A flor [...], 1995)`. O monossílabo é reconhecido por uma lista, que não é
  exaustiva. Onde a regra errar, o `shorttitle` tem precedência e sai como está
  escrito, inclusive o `[\ldots]`.

## Correções da referência

| O que | A norma pede | Campo |
|---|---|---|
| Intervalo de páginas | `p. 1-74`, com hífen | `pages` |
| Evento com reticências | `Anais [...]. São Paulo` | `booktitle = {Anais [\ldots]}` |
| Qualificador | `SÃO PAULO (Estado). Secretaria do Meio Ambiente.` | o nome, entre chaves duplas |
| Folhas | `82 f.`, `f. 19-20` | `bookpagination = {leaf}` |
| `@manual` com editora | `Rio de Janeiro: ABNT, 2011.` | `publisher` |
| Entrada pelo título com artigo | `A FLOR prometida.`, `THE EVIDENCE underlying` | `title` (8.2.1) |
| Documento online com editora | `Washington, DC: ASAN, [2016?].` | `location`, `publisher` ou `organization` |
| Páginas com letra | `p. E16-E18` | `pages`; número de artigo (`e03304`) vai em `eid` |
| Trabalho acadêmico | `– Universidade …, Natal, 2023.` (7.1.2) | o ano vem de `date`; `eventdate` só se a defesa for noutro ano |

**Documento sem data.** A data de acesso não é data do documento, e o estilo não a usa
na chamada: sem data, a chamada sai com `s.d.`, e a compilação avisa. A 6023 pede um ano
entre colchetes (8.6.1.3), e ele vai no `.bib`: `year = {[2020?]}`, `year = {[20--]}`.

**`@online` sem local ou editora.** Sai só o que está no `.bib`. O `[S. l.]` em documento
online fica para o Sprint 4, porque a 6023:2025 se contradiz (briefing, 2.5).

**DOI.** A 6023:2025 não fixa a forma, e os exemplos trazem três: sem resolvedor
(7.2.2), `http://dx.doi.org/…` (7.7.6, ex. 7) e `https://doi.org/…` (7.7.6, ex. 8, novo
na 2025). O estilo imprime o `doi` como está no `.bib`, sempre com link. No `.bib` do
CRP SP, a recomendação é a forma do exemplo 8, com o endereço completo:

```bibtex
doi = {https://doi.org/10.1590/S1980-220X2017020403304},
```

## Legislação e ato normativo

Na 6023, legislação é a seção 7.11.1–7.11.2 e ato administrativo normativo, a
7.11.5–7.11.6. São dois tipos diferentes (decisão 2 do briefing):

- `@legislation`: a entrada é a jurisdição (`BRASIL.`, `CURITIBA.`), para
  Constituição, lei, decreto e medida provisória;
- `@legal`: a entrada é a entidade que emite o ato, com o órgão interno em
  `nameaddon`. Resoluções do CFP e do CRP são `@legal`.

Os dois usam o mesmo driver, porque a ordem dos elementos é a mesma:

> AUTORIA. Título. Ementa. Organizado por. Edição. *In*: obra. Publicação.
> Páginas. Notas. Complementos. DOI. Disponível em: URL. Acesso em: data.

| Campo | O que guarda | Exemplo |
|---|---|---|
| `author` | jurisdição ou entidade, entre chaves duplas | `{{Brasil}}`, `{{Conselho Federal de Psicologia}}` |
| `nameaddon` | órgão interno, ou `[Constituição (1988)]` | `Ministério da Educação` |
| `title` | epígrafe | `Lei nº 13.146, de 6 de julho de 2015` |
| `ementa` | ementa; a atribuída vai entre colchetes | `[Aquisição de leite pasteurizado]` |
| `editor` + `editortype = {organizer}` | organizador de coletânea | sai `Organizado por …` |
| `edition` | edição | `4. ed. atual.` |
| `booktitle` | obra que contém o ato | `Vade mecum` sai `In: VADE mecum.` |
| `journaltitle`, `journalsubtitle` | diário oficial e seção | `Diário Oficial da União`, `seção 1` |
| `volume` | ano do diário, **com a palavra** | `ano 139` |
| `number`, `pages` | número e páginas do diário | `8`, `1-74` |
| `location`, `publisher` | sem diário: local e responsável pela publicação | `Brasília, DF`, `Presidência da República` |
| `date` ou `year` | data da publicação; a inferida entre colchetes em `year`, com `sortyear` | `year = {[2016]}` |
| `pagetotal`, `note` | descrição física | `320`, `1 CD-ROM (p. 1-90)` |
| `complementos` | retificação, alteração, revogação, projeto de origem, assunto | `PL 634/1975` |
| `url`, `urldate`, `doi` | acesso online | |

Com `journaltitle`, a publicação sai como no diário oficial
(`Diário Oficial da União: seção 1, Brasília, DF, ano 139, n. 8, p. 1-74, 11 jan. 2002.`).
Sem ele, sai `local: editora, data.`

Escolhas que a norma não fixa:

- **`volume` como `ano 139`.** É a convenção do upstream: o campo guarda o
  rótulo junto com o número. O exemplo 5 de 7.11.5 traz `v. 22` e sai com
  `volume = {22}`.
- **Complementos antes do acesso online.** A 6023 não traz exemplo com os
  dois. Aqui, `Disponível em` fecha a referência, como nos demais documentos
  online. O upstream punha o `addendum` depois da URL.

## Jurisprudência

Na 6023, a seção 7.11.3–7.11.4. `@jurisdiction` tem driver próprio, com a ordem dos
elementos da norma e as mudanças da Emenda 1 (briefing, 2.5):

> JURISDIÇÃO. Tribunal (órgão julgador). Título. Ementa. Partes. Relator: nome,
> julgado em data. Publicação. Complementos. Disponível em: URL. Acesso em: data.

```
BRASIL. Supremo Tribunal Federal (2. Turma). Recurso Extraordinário 313060/SP. […].
Relatora: Min. Ellen Gracie, julgado em 29 nov. 2005. Brasília, DF: Superior Tribunal
de Justiça, [2006]. Disponível em: […]. Acesso em: 19 ago. 2011.
```

| Campo | O que guarda | Exemplo |
|---|---|---|
| `author` | jurisdição, entre chaves duplas | `{{Brasil}}` |
| `nameaddon` | tribunal | `Supremo Tribunal Federal` |
| `orgao` | órgão julgador; sai entre parênteses | `2. Turma` |
| `title` | tipo e número do processo, ou da súmula | `Recurso Extraordinário 313060/\mkbibacro{SP}` |
| `ementa` | ementa | |
| `partes` | partes do processo, como no documento | `Recorrente: …. Recorrido: …` |
| `relator` | relator, como no documento | `Min. Ellen Gracie` |
| `relatortype` | `relatora` troca o rótulo; o padrão é `Relator` | `relatora` |
| `eventdate` | data do julgamento; sai abreviada, depois de `julgado em` | `2005-11-29` |
| publicação | a mesma do `@legislation`: diário ou repertório em `journaltitle`, ou `location` e `publisher` | `Lex`, `Diário da Justiça` |
| `complementos`, `url`, `urldate`, `doi` | como no `@legislation` | |

Escolhas que a norma não fixa:

- **O tribunal em `nameaddon`**, como o órgão interno do `@legal`, e o órgão julgador
  num campo próprio. O briefing previa o tribunal em `orgao`; a troca mantém os dois
  tipos de ato com o mesmo contrato na entrada.
- **`relator` é texto, não lista de nomes.** A norma o transcreve como está no
  documento, com o tratamento (`Min.`), e não o inverte nem o ordena. O gênero do
  rótulo não se deduz do nome, e por isso vem em `relatortype`.
- **Julgamento sem relator** abre frase: `Ementa. Julgado em 2 maio 2019.` A norma não
  traz exemplo.

## Desenvolvimento

- `desenvolvimento/sondagem/`: a sondagem que mediu o upstream (exemplos da 2018);
- `desenvolvimento/corpus/`: os exemplos das duas normas como corpus de teste,
  extraídos por `extrair.py`; os `.bib` de 287 das 289 referências da 6023
  (`trilha-6023.bib`, `jurisprudencia-6023.bib`, `demais-6023.bib`), o medidor
  `medir.py`, o comparador com a linha-base `comparar.py` e a tabela de divergências,
  `DIVERGENCIAS.md` (`python3 <script> --help`);
- `desenvolvimento/casos/`: os casos que a norma não traz, como sigla como entrada,
  ordenação e contagem de links. Rodar com `sh verificar.sh`, que também confere a
  árvore de tags (`arvore.txt`) e passa o PDF no veraPDF UA-2;
- `desenvolvimento/verificar.sh`: a régua. Mede o corpus e as chamadas com o PDF
  tagueado, compara cada entrada com a linha-base da versão, passa os PDFs no veraPDF e
  roda os casos. Rodar depois de mexer no estilo e depois de todo `tlmgr update`:

  ```sh
  sh desenvolvimento/verificar.sh
  ```

  Qualquer mudança no texto obtido, mesmo melhora, sai com 1. A linha-base nova se grava
  com a versão nova (`DIVERGENCIAS.md`, "Régua").

Medir o estilo, a partir de `desenvolvimento/corpus/`:

```sh
TEXINPUTS="$(cd ../.. && pwd)//:" python3 medir.py trilha-6023.bib --estilo crpsp-abnt
```
