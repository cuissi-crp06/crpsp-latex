# Briefing: `crpsp-abnt`, extensão do biblatex-abnt

> **estado:** Sprint 3 da trilha em curso (`0.2.1-alfa`, defeitos achados ao compor o guia corrigidos); falta compor o guia com o `.bib` curado. Sprint 5 feito (`0.3.0-alfa`, jurisprudência)
> **escrito em:** 2026-09-28; **revisto em:** 2026-09-28, com a 6023:2025
> **escopo:** um estilo biblatex que estende o `biblatex-abnt` e o adequa à
> ABNT NBR 6023:2025 e à NBR 10520:2023, com três frentes: documento
> jurídico, citação e mídia contemporânea.
>
> ⚠️ A primeira versão deste briefing tomou por vigente a 6023:2018. A 3ª
> edição, de 21/05/2025, "equivale ao conjunto ABNT NBR 6023:2018 e Emenda 1"
> e cancela a de 2018 (prefácio). O que a emenda mudou está na seção 2.5.

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
| Podcast (7.13.5, ex. 1) | `GUTNER, Christian (Locução de). Podcast LXX…`, chamada (Gutner, 2010) | entrada pelo título: `PODCAST LXX: … [Locução de]: Christian Gutner.` Com entrevistado, a 2025 muda: a entrada é pelo entrevistado (ex. 2, seção 2.5) |
| Vídeo no YouTube (7.13.2) | `BOOK. 1 vídeo (3 min). … 2010.` | `BOOK. [S. l.: s. n.], 2010. 1 vídeo (3 min). …` |
| Chamada por título (10520, 7.1.4) | `(BOOK…, 2010)` | `(Book [...], 2010)` |
| Sigla como entrada (premissa da seção 1) | chamada `(IBGE, 2025)`, referência começa por `INSTITUTO BRASILEIRO…` | `IBGE — INSTITUTO BRASILEIRO…` |

A sondagem usou exemplos da 2018. Os exemplos da tabela seguem iguais na
2025, salvo o do podcast. A tabela que vale é a do Sprint 0, em
`desenvolvimento/corpus/DIVERGENCIAS.md`: 20 divergências nas seções da
trilha, 8 delas em tipos de referência que o guia usa.

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

### 2.5 O que a Emenda 1 mudou (6023:2025)

Levantado por diff de palavras entre as duas edições. A seção 6 (regras
gerais) e os modelos de legislação e de ato normativo (7.11.1, 7.11.2 salvo
um exemplo, 7.11.5, 7.11.6) não mudaram. Mudou:

- **Publicação periódica (7.7.1–7.7.4):** ISSN sai dos elementos essenciais da
  coleção. Fascículo, volume e número ficam "se houver", e suplemento e edição
  especial vão depois da data, com o título após dois-pontos:
  `v. 7, 1983. Suplemento: Mão-de-obra e previdência.` Os exemplos passam a
  ter entrada pelo título do periódico, não pelo da edição especial.
- **Abreviatura:** `Supl.` → `Suplemento`, por extenso, em todos os exemplos. O
  Anexo B tira `Supl.` e acrescenta `ca.` e `serigraf.`.
- **DOI:** passa a ser rotulado `DOI:`, com dois-pontos. O exemplo novo de
  7.7.6 (ex. 8) traz o DOI como URL: `DOI: https://doi.org/10.1590/…`.
- **Local desconhecido em documento online:** alguns exemplos perdem o `[S. l.]`
  (7.7.6 ex. 5, 7.20 exs. 5 e 9, 8.7.3). O 7.13.5 ex. 1 mantém `[S. l.]: Escriba
  Café`, e o mesmo exemplo repetido em 8.7.3 o perde. A norma se contradiz;
  a escolha fica registrada no Sprint 4.
- **Editora igual ao autor (7.20):** `[Cupertino]: Apple` → `[Cupertino]`;
  `Roseville: FFG` → `Roseville`. Mas `Curitiba` → `Curitiba: Universidade
  Federal do Paraná`, no ex. 2, onde o autor é a Biblioteca Central. Local e
  produtor ficam "se houver" em 7.19 e 7.20.
- **Evento (7.8):** local é "(cidade, se houver)".
- **Jurisprudência (7.11.3–7.11.4):** a data de julgamento vem precedida de
  `julgado em` e abreviada (`julgado em 29 nov. 2005`); o órgão julgador entra
  entre parênteses após o tribunal (`Superior Tribunal de Justiça (1. Seção)`);
  a versão online ganha local e editora (`Brasília, DF: Superior Tribunal de
  Justiça, [2006]`). O ex. 1 passa a ser rotulado complementar.
- **Documento sonoro e podcast (7.13.3–7.13.5):** responsáveis "conforme consta
  no documento"; o podcast com entrevistado tem entrada por ele
  (`SILVEIRA, Luciana Martha. Anticast 66: …`), e o entrevistado sai da lista
  de responsáveis.
- **Série e coleção (8.10):** só a primeira palavra em maiúscula
  (`Coleção filosofia`, `Série bom apetite`).
- **Exemplos novos:** 7.7.4 ex. 5 (suplemento com ISSN), 7.7.6 ex. 8 (DOI),
  7.20 ex. 10 (notícia online sem local). Sai 8.4.4 ex. 2.
- As erratas de 2020 foram incorporadas.

A 8.1.2, que não mudou, admite a entrada da pessoa jurídica "pela forma
conhecida ou como se destaca no documento, por extenso ou abreviada", e há
exemplos só com a sigla (`PETROBRAS.`, `IBGE.` em 7.18). A forma
`SIGLA — NOME POR EXTENSO`, da orientação da especialista, não está na norma:
é uma combinação das duas formas que ela admite. A decisão 3 continua valendo,
mas o README do pacote deve dizer isso.

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
| `@jurisdiction` | 7.11.3–7.11.4 | `author` = jurisdição; `orgao` = corte, turma/região (no Sprint 5: tribunal em `nameaddon`, órgão julgador em `orgao`, `relator` como texto; ver o README); `title` = tipo e número do processo; `ementa`; `relator` (nome); `eventdate` = julgamento, impresso como `julgado em` + data abreviada (2025); órgão julgador entre parênteses após a corte; publicação |
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

O sinal de pessoa jurídica foi decidido no Sprint 2 (Angelo, 2026-09-28):
é automático. A entrada precisa ter `shortauthor` e um `author` só, inteiro
entre chaves duplas. O `authortype = {organization}` desta seção não
serviria, porque no upstream o `authortype` sai impresso entre parênteses
depois do nome (`abnt.bbx`, bibmacro `author`).

## 5. Sprints

O guia precisa ser encaminhado em poucos dias (decisão do Angelo,
28/09/2026, na revisão do briefing). O plano se divide em uma **trilha do
piloto**, só com o que as ~57 referências do guia usam, e o **restante**,
depois da entrega.

O que o guia usa (lista de `revisao_2/LaTeX/referencias_brutas.txt`): 25
artigos de periódico, ~20 documentos de pessoa jurídica com sigla, 3
capítulos, 1 trabalho de evento, 2 trabalhos acadêmicos, 3 atos de
legislação (Lei 13.146, Decreto 6.949, Lei 10.216) e 2 resoluções do CFP. Não
há jurisprudência, filme, vídeo, podcast, mapa nem patente.

### Trilha do piloto

**0. Corpus contra a norma.** Feito na trilha (28/09). `corpus/extrair.py` lê a
6023:2025 direto do PDF (sem ingestão no pipeline, para ganhar tempo) e a
10520:2023 do JSON do pipeline, e grava `corpus/nbr6023.tsv` (289 referências,
20 fragmentos) e `corpus/nbr10520.tsv`. Falta escrever o `.bib` e medir o
upstream **só nas seções que o guia usa**: 7.1.1, 7.1.2, 7.2.2, 7.3, 7.4,
7.7.5, 7.7.6, 7.8.4.1, 7.8.5, 7.11.1, 7.11.2, 7.11.5, 7.11.6, 8.1 (autoria e
pessoa jurídica), 8.5.4 (sigla como editora); e, na 10520, as chamadas de
6.1.1–6.1.4, 6.1.7, 6.1.8 e 7.1.3–7.1.4. Foram 107 referências e 29
chamadas: `corpus/trilha-6023.bib`, `corpus/trilha-10520.bib` e
`corpus/chamadas-10520.tsv`, medidos por `corpus/medir.py`. O upstream acerta
44 referências e 22 chamadas; a tabela está em `corpus/DIVERGENCIAS.md`.

**1. Legislação e ato normativo.** Drivers de `@legislation` e `@legal`, os
campos do `.dbx` que eles usam (`ementa`, `complementos`) e os testes de
7.11.1, 7.11.2, 7.11.5 e 7.11.6. `@jurisdiction` fica para depois. Feito em
28/09 (`0.1.0-alfa`): os 15 exemplos dessas seções no corpus saem iguais à norma,
exceto 4, que dependem das linhas 1 e 3 do Sprint 2 (meia-risca e `(Estado)`). O
contrato de campos está no README. O `.dbx` carrega sozinho com o estilo, e por isso
a opção `datamodel` da seção 4 não é necessária.

**2. Sigla e chamada.** Sigla como entrada (`SIGLA — NOME`) nas duas pontas,
com o sinal de pessoa jurídica decidido aqui; chamada como **um** link;
chamada por título com `[...]`; os localizadores que o guia usar. Feito em
28/09 (`0.2.0-alfa`), e chega a 85/107 referências e 27/29 chamadas. Fecha as
linhas 1, 2, 3, 6, 9, 11 e 12 da tabela, mais uma achada no caminho: o artigo
na entrada pelo título, da 8.2.1. As opções de autores ficaram decididas:
todos os autores na referência, até 20, e na chamada o primeiro e `et al.` a
partir de quatro. O DOI sai como está no `.bib`, porque a 2025 traz três
formas. A sigla não tem exemplo na norma e ganhou casos próprios, com contagem
de links e veraPDF, em `desenvolvimento/casos/`. Os localizadores do upstream
já saíam certos.

**3. Piloto.** Revisão 2 do guia, com o `.bib` curado (seção 7). A régua do
piloto é a tabela do Sprint 0 reduzida, mais o veraPDF UA-2 do PDF do guia.
Em curso. A composição do `.bib` curado achou quatro defeitos do estilo, corrigidos
na `0.2.1-alfa` (linhas 22 a 25 de `DIVERGENCIAS.md`): `@online` sem local e editora,
chamada com o ano do acesso, `p. E16-E18` e o ano da defesa no trabalho acadêmico.
Falta a troca de `[n]` por `\cite` no texto, que espera a revisão da introdução.

### Depois da entrega

**4. Mídia contemporânea.** 7.13 (filme, vídeo, sonoro, podcast) e 7.20, já
com as mudanças da Emenda 1: entrevistado como entrada, `[S. l.]` em
documento online (a norma se contradiz, seção 2.5), editora igual ao autor.
Onde a norma for ambígua, a escolha fica registrada no README com a seção que
a motiva.

**5. Jurisprudência.** `@jurisdiction`, com `julgado em`, órgão julgador
entre parênteses e a publicação online com editora (seção 2.5). Feito em 28/09
(`0.3.0-alfa`): os 5 exemplos da 7.11.3–7.11.4 saem iguais à norma (upstream: 0),
medidos em `corpus/jurisprudencia-6023.bib`, fora da trilha. O contrato mudou em
relação à seção 4.1: o tribunal vai em `nameaddon`, como no `@legal`; `orgao` guarda
só o órgão julgador; `relator` é texto, com o gênero do rótulo em `relatortype`;
e as partes do processo ganharam o campo `partes`.

**6. Corpus completo e régua.** O `.bib` das ~290 referências da 6023; testes
no molde do `verificar.sh` do `crpsp-book`: texto normalizado por entrada
(não pixels), `show-pdf-tags` para a árvore e veraPDF UA-2.

**7. Ingestão da 6023:2025 no pipeline.** Trocar a leitura do PDF pelo JSON e
corrigir no parser os defeitos que `extrair.py` remenda (seção 6). Feito em 28/09,
sem versão nova, porque o estilo não muda. O parser de norma técnica do pipeline
ganhou um modo próprio (`normativas-pipeline` #69):

- o número fora de sequência não abre nó;
- o título de primeiro nível vira item;
- anexos e bibliografia saem do corpo;
- a marca de licença deixa de apagar texto ("uso exclusivo", da 6.10);
- o hífen de fim de linha segue a regra do `extrair.py`.

Os 175 nós da 6023:2025 saem do JSON iguais, texto a texto, aos da leitura do PDF.
O `extrair.py` perdeu a leitura do PDF e os remendos, e a medida da 0.3.0 não mudou.
A 6023 muda só na coluna `origem`. A 10520 ganha o `10520:8:1`, o exemplo de notas
que o remendo antigo cortava junto com o título "8 Notas". Por decisão do Angelo
(28/09), a 2025 entrou no banco pela cópia emprestada e está na release `db-20260928`. A
6023:2018 ficou no banco, revogada em 21/05/2025.

**8. `bibgen` (sem urgência).** No `normativas-pipeline`, gerar entradas
`@legislation`/`@legal` do banco (tipo, número, data, ementa, órgão emissor,
URL), como o `latexgen` faz com o texto. Depende do contrato de campos fixado
no Sprint 1.

## 6. Riscos

- **Upstream parado ou mudando por baixo.** Última versão em 2024. Sobrepor
  macros internas do `abnt.bbx` quebra se ele mudar; a régua do Sprint 6 deve
  rodar depois de todo `tlmgr update`.
- **Direito autoral das normas.** O repositório é privado e o corpus guarda só
  os exemplos, não o texto normativo. Se o pacote um dia for publicado, o
  corpus precisa ser revisto.
- **Cópia emprestada da 6023:2025.** A cópia em `editorial/apoio/normas/ABNT/`
  foi emprestada para uso emergencial e traz a marca de licença de outra
  instituição. O corpus não carrega nada dela além dos exemplos. Desde o
  Sprint 7 (decisão do Angelo, 28/09), o texto dela está no banco de
  normativas e na release, sem a marca. Conferir o banco e o corpus contra um
  exemplar licenciado ao CRP SP quando houver.
- **Corpus lido de PDF.** O hífen de fim de linha, os espaços dentro de URL e
  as palavras coladas por kerning são remendados por regra, não garantidos,
  agora no pipeline (Sprint 7). Divergência que só aparece numa URL ou num
  hífen é primeiro suspeita de extração.
- **Defeitos do parser de normas técnicas do pipeline.** O JSON da 2018 tinha nó
  novo a cada linha iniciada por número, título de seção e índice grudados no
  nó anterior, e a ementa anunciava as erratas sem aplicá-las. Corrigidos no
  Sprint 7 para toda norma técnica, e a ementa da 2018 agora diz que as erratas
  não estão aplicadas. Sobra o OCR da ISO 2108, que perde o título do Anexo A.
- **A norma é ambígua em mídia** (7.13 e documentos online). As escolhas
  precisam de registro, senão viram gosto.

## 7. Frente paralela: as referências do guia (conteúdo, fica no workbench)

Com o prazo do piloto, esta frente é o caminho crítico: o pacote não corrige
referência errada, e várias da lista não têm URL nem DOI, que a 6023:2025
pede para documento online (`DOI: https://doi.org/…`).

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
