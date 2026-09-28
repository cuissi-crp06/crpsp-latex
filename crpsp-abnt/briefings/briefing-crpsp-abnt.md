# Briefing: `crpsp-abnt`, extensão do biblatex-abnt

> **estado:** planejado, decisões tomadas; nenhum código ainda
> **escrito em:** 2026-09-28
> **escopo:** um estilo biblatex que estende o `biblatex-abnt` e o adequa à
> ABNT NBR 6023:2018 (com as erratas de 2020) e à NBR 10520:2023, com três
> frentes: documento jurídico, citação e mídia contemporânea.

## 1. Origem

A revisão 2 do guia de apresentações acessíveis
(`production/editorial/publicacoes/cartilhas/apresentacoes_acessiveis/revisao_2/`,
no workbench) chegou com uma introdução nova e cerca de 57 referências. As
notas da versão (`revisao_2/notas_da_versao.md`) fixam três premissas:

- citação **autor-data**, por acessibilidade (o sistema numérico atrapalha a
  leitura com leitor de tela);
- instituição conhecida pela sigla pode ter a sigla como chamada — `(IBGE, 1989)` —
  desde que a referência comece pela sigla, travessão e nome por extenso:
  `IBGE — INSTITUTO BRASILEIRO DE GEOGRAFIA E ESTATÍSTICA`. A orientação veio de
  uma especialista da ABNT; a norma não traz o travessão;
- motor `biber`, estilo `biblatex-abnt`.

O guia é o piloto; o pacote serve a toda publicação do CRP SP que tenha
referências.

## 2. Linha de base: o que o biblatex-abnt faz hoje

Versão 4.0, de 2024-07-04 (a do TeX Live 2026 atualizado). O CHANGELOG anuncia
"Compliance with NBR10520:2023" e "Added tests for NBR6023:2018".

### 2.1 A suíte de testes não cobre a 2018

- `NBR6023-2018.bib` tem 244 entradas e difere de `NBR6023-2002.bib` em **9**,
  todas cosméticas (`Anais\ldots` → `Anais [\ldots]`). Os exemplos são os da
  2002 (Lex, Decreto 42.822/1998) e as palavras-chave seguem a numeração
  antiga: `7.9` é documento jurídico, que na 2018 é `7.11`.
- O teste (`test.sh`) sobrepõe a saída a um `*_reference.pdf` gerado pelo
  próprio pacote (`pdfpagediff` + `gs -sDEVICE=inkcov`). É regressão contra si
  mesmo, não conformidade com a norma.
- **Não há teste da 10520:2023.**

### 2.2 Documento jurídico não tem driver

`abnt.bbx:1372-1374`:

```latex
\DeclareBibliographyAlias{legislation}{article}%
\DeclareBibliographyAlias{jurisdiction}{article}%
\DeclareBibliographyAlias{legal}{article}%
```

Tudo passa pelo driver de artigo de periódico: o DOU vira `journaltitle`, o ano
do diário vira `v.`, e jurisprudência não tem campo para relator, data de
julgamento ou ementa.

### 2.3 Divergências medidas

Sondagem em `desenvolvimento/sondagem/sondagem-upstream.{tex,bib}`, com
exemplos da própria norma:

| Caso | biblatex-abnt produz | A norma pede |
|---|---|---|
| Lei no DOU (6023, 7.11.1) | `… seção 1, Brasília, DF, v. 139, n. 8 …` | `ano 139` |
| Constituição online (7.11.2) | `Presidência da República, Brasília, DF, 2016` | `Brasília, DF: Presidência da República, [2016]` |
| Podcast (7.13.5) | `GUTNER, Christian (Locução de). Podcast LXX…`, chamada (Gutner, 2010) | entrada pelo título: `PODCAST LXX: … [Locução de]: Christian Gutner.` |
| Vídeo no YouTube (7.13.2) | `BOOK. 1 vídeo (3 min). … 2010.` | `BOOK. [S. l.: s. n.], 2010. 1 vídeo (3 min). …` |
| Chamada por título (10520, 7.1.4) | `(BOOK…, 2010)` | `(Book [...], 2010)` |
| Sigla como entrada (premissa da seção 1) | chamada `(IBGE, 2025)`, referência começa por `INSTITUTO BRASILEIRO…` | `IBGE — INSTITUTO BRASILEIRO…` |

O que funciona: `shortauthor` já alimenta a chamada (`abnt.cbx:35`), e a
chamada de pessoa física já sai em caixa alta e baixa.

### 2.4 Acessibilidade

Com `\DocumentMetadata{tagging=on, pdfstandard=ua-2}` a sondagem **passa no
veraPDF 1.30.2** e a lista sai tagueada `L/LI/Lbl/LBody`. O `latex-lab-testphase-bib`
não trata o biblatex; o resultado vem do tagueamento genérico de listas. Dois
defeitos:

- cada chamada vira **dois links** (`Brasil` e `2002`), lidos em separado pelo
  leitor de tela;
- o negrito de destaque dos títulos não gera `Strong`/`Em`.

## 3. Decisões (Angelo, 2026-09-28)

1. **Nome e lugar:** `crpsp-abnt`, pasta própria neste repositório.
2. **Legislação e ato administrativo são tipos distintos:** 7.11.1 ≠ 7.11.5.
   Resoluções do CFP e do CRP são `@legal` — a entrada é o cabeçalho da
   entidade, não a jurisdição.
3. **Sigla como entrada é o padrão** do pacote, não opção.
4. **`bibgen`** (gerar `.bib` a partir do banco de normativas) fica planejado,
   sem urgência.
5. **A checagem das referências** do guia entra junto com a revisão da
   introdução (seção 7).

Não vira compromisso: mandar correções genéricas (10520:2023, ordem
local: editora) ao upstream é possibilidade a avaliar depois do Sprint 2.

## 4. Arquitetura

Extensão, não fork. Carrega o upstream e sobrepõe:

| Arquivo | Papel |
|---|---|
| `crpsp-abnt.bbx` | `\RequireBibliographyStyle{abnt}`; drivers jurídicos, correções de mídia, sigla na entrada |
| `crpsp-abnt.cbx` | `\RequireCitationStyle{abnt}`; chamada por título, localizadores, link único |
| `crpsp-abnt.dbx` | só os campos que o biblatex não tem |
| `brazilian-crpsp-abnt.lbx` | strings novas (`Relator:`, `Destinatário:`, `[Locução de]:`…), se preciso |

Uso: `\usepackage[style=crpsp-abnt, datamodel=crpsp-abnt, backend=biber]{biblatex}`.
Versão inicial `0.1.0-alfa`, conforme `CONVENCAO-VERSIONAMENTO.md`.

### 4.1 Tipos jurídicos

| Tipo | Seção da 6023 | Mapeamento |
|---|---|---|
| `@legislation` | 7.11.1–7.11.2 | `author` = jurisdição; `nameaddon` = `[Constituição (1988)]`; `title` = epígrafe; `ementa`; publicação oficial com `journaltitle`, `journalsubtitle` (seção), `volume` impresso como **ano**, `number`, `pages`, `date` |
| `@jurisdiction` | 7.11.3–7.11.4 | `author` = jurisdição; `orgao` = corte, turma/região; `title` = tipo e número do processo; `ementa`; `relator` (nome); `eventdate` = julgamento; publicação |
| `@legal` | 7.11.5–7.11.6 | `author` = entidade; `nameaddon` = órgão interno; `title` = epígrafe; `ementa`; publicação |

Campos novos no `.dbx`: `ementa` (literal), `orgao` (literal), `relator`
(lista de nomes), `complementos` (literal: retificações, revogações, vigência,
projeto de origem — impressos no fim, como a norma manda). `eventdate` já
existe e cobre a data de julgamento.

Casos que o driver precisa aceitar sem remendo: ementa ausente, ementa
atribuída entre colchetes (7.11.5, exemplo 1), supressão com `[...]`,
publicação fora do diário oficial (Lex, coletânea, *vade mecum* com `In:`).

### 4.2 Sigla como entrada

Quando a entrada é pessoa jurídica com `shortauthor`:

- referência: `SIGLA — NOME POR EXTENSO`;
- ordenação pela sigla (é por ela que o leitor procura, vindo da chamada);
- chamada: a sigla, em maiúsculas (10520:2023, 6.1.1.2 recomenda).

Precisa definir como marcar pessoa jurídica: chaves duplas no `author`
bastam para o biber, mas o estilo precisa de um sinal explícito
(`authortype = {organization}` ou similar). Decidir no Sprint 2.

## 5. Sprints

**0. Corpus contra a norma.** Extrair de `export/normas/abnt-nbr-6023-2018.json`
e `abnt-nbr-10520-2023.json` (workbench, saída do pipeline) todos os exemplos
como pares *entrada `.bib` → texto esperado*, numerados pela seção. Conferir se
as erratas 1 e 2 de 2020 estão no JSON; se não, aplicar a partir de
`editorial/apoio/normas/ABNT/`. Confirmar no catálogo ABNT que 6023:2018 e
10520:2023 seguem vigentes. Rodar o upstream contra o corpus e produzir a
tabela de divergências por seção — ela, e não a seção 2.3, é o escopo real.
O script de extração é código e vem para cá; o texto das normas não.

**1. Documento jurídico.** Os três drivers, o `.dbx`, os testes da 7.11.

**2. Citação (10520:2023).** Chamada por título com `[...]`; localizadores
(`local.`, `slide`, `cap. V, art. 49, inc. I`, `9 min 41 s`); sigla como
entrada nas duas pontas; chamada como **um** link.

**3. Mídia contemporânea.** 7.13 (filme, vídeo, sonoro, podcast) e documento
online: ordem dos elementos, `[S. l.: s. n.]`, descrição física. Onde a norma
for ambígua, a escolha fica registrada no README com a seção que a motiva.

**4. Régua.** Testes no molde do `verificar.sh` do `crpsp-book`: comparação de
texto normalizado por entrada (não de pixels), `show-pdf-tags` para a árvore e
veraPDF UA-2.

**5. Piloto.** Revisão 2 do guia de apresentações acessíveis, com o `.bib`
curado (seção 7).

**6. `bibgen` (sem urgência).** No `normativas-pipeline`, gerar entradas
`@legislation`/`@legal` do banco (tipo, número, data, ementa, órgão emissor,
URL), como o `latexgen` faz com o texto. Depende do contrato de campos fixado
no Sprint 1.

## 6. Riscos

- **Upstream parado ou mudando por baixo.** Última versão em 2024. Sobrepor
  macros internas do `abnt.bbx` quebra se ele mudar; a régua do Sprint 4 deve
  rodar depois de todo `tlmgr update`.
- **Direito autoral das normas.** O repositório é privado e o corpus guarda só
  os exemplos, não o texto normativo. Se o pacote um dia for publicado, o
  corpus precisa ser revisto.
- **A norma é ambígua em mídia** (7.13 e documentos online). As escolhas
  precisam de registro, senão viram gosto.

## 7. Frente paralela: as referências do guia (conteúdo, fica no workbench)

A lista recebida não está em ABNT: é um híbrido com a APA (`&` entre autores,
`(Eds.)`, `et al.` dentro do `In:`), algo típico de lista APA convertida.
Sinais de referência mal resolvida:

- quatro entradas pelo título, sem autor, onde o artigo tem autoria
  (`RECOGNIZING ableism…`, `THE EVIDENCE underlying…`,
  `SENSORY ABNORMALITIES… PMC`, `AMBIENTES ESCOLARES…`);
- uma associação (ABPEE) como autora de artigo da *Revista Brasileira de
  Educação Especial*;
- Tomchek e Dunn em periódico improvável (o artigo conhecido é de 2007, na
  *American Journal of Occupational Therapy*).

O `crpsp-acessibilidade.bib`, gerado pelo text2bib.org, tem erros próprios:
leis com `location = {DF}, publisher = {Brasília}`, uma entrada sem tipo
(`{finkel2020accessibility,,`), leis e resoluções como `@Book`.

A checagem confere, para cada referência, existência, autoria, periódico,
volume, páginas e DOI, e sai como relatório em `revisao_2/` no workbench,
junto com a revisão da introdução. Referência que não se confirmar não entra
no piloto. O `.bib` curado é conteúdo e não vem para este repositório.
