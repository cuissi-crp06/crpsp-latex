---
tipo: briefing
dominio: editorial
projeto: crpsp-book
estado: pronto-para-execucao
criado: 2026-07-10
executor: Claude Code
---

# Briefing — Camada `Leg` em `book-crpsp_acessivel.sty` + gerador normativas→LaTeX

## Objetivo

Estender o pacote `editorial/latex_acessivel/book-crpsp_acessivel.sty` (v0.4.2) com comandos e ambientes `Leg` que correspondam aos tipos LeXML do pipeline de normativas, e criar um gerador que produza fragmentos `.tex` a partir do JSON canônico do `consolidar.py`. Meta final: **regerar o Manual de Direitos Humanos** a partir do banco `data/normativas/normativas.sqlite` + consultas à API LexML, compilando em PDF/UA-2. A camada `Leg` deve ficar **permanentemente disponível** no pacote book acessível.

## Leituras obrigatórias antes de codar

1. `editorial/latex_acessivel/book-crpsp_acessivel.sty` — pacote-alvo. Seção 7 já tem o embrião: `\LegArtigo{label}{texto}`, `\LegParagrafo`/`\LegParagrafoUnico`, `\LegEmenta`, `\LegTitulo`, `\LegAssina`. Ler os comentários de PDF/UA (minipages, description, proibição de titlesec).
2. `scripts/normativas/consolidar.py` + `scripts/normativas/README.md` — formato JSON canônico (o docstring já declara o conversor LaTeX como consumidor). Árvore: `estrutura[]` com `{frag_id, urn, tipo, rotulo, numero, texto, status, notas[], filhos[]}`.
3. `~/git/editoracao/manual/` — Manual de DH **publicado** (referência de conteúdo e visual, memoir/abntex2). Uso real dos comandos em `capitulos/5.dudh.tex` e `capitulos/7.normativas.tex` (padrão: `\LegEmenta{...}` → sequência de `\LegArtigo{1º}{...}` → `\LegAssina{NOME}{Cargo}`). **Base, não verdade última** — a estrutura plana dele é limitação da época, não decisão de design.
4. `scripts/normativas/lexml.py` — resolução de URN via API LexML (cache, rate-limit, curadoria de ambíguos).
5. `editorial/latex_acessivel/desenvolvimento/` e `briefings/` — histórico de decisões do pacote.

## Estado de partida (verificado em 10/07/2026)

- Pacote book acessível compila com `\DocumentMetadata{pdfstandard=ua-2, testphase={phase-III,table,firstaid}, tagging=on}`; capítulos via instância sec-template; árvore de tags validada em 2026-04-09.
- Banco de normativas: fases 1–9 operacionais; dispositivos com `frag_id`/`urn` LeXML; grafo de alterações e vigência (B2 documental); RAG e NER ativos.
- Tipos de dispositivo no banco — **agrupadores**: `prt, liv, tit, cap, sec, sub`; **dispositivos**: `art, cpt, par, inc, ali, ite, dpg`; esquema **decimal** para NRs/ABNT (`28.1.1`).
- Leis federais (13.146/2015 e 15.263/2025) em staging: `data/normativas/leis_federais/` (MD + JSON estruturado por artigo). **Ainda não ingeridas** — ver Fase 0.
- `livros_crp_v7.sty` e `livros_crp_comentado.sty` migrados para `editorial/arquivo_latex/sty/` (linha memoir; referência de identidade visual, não de código para book).

## Fase 0 — Ingestão das leis federais (pré-requisito de conteúdo)

O `ingerir.py` só aceita PDFs de fontes crp06/cfp. Criar adaptador mínimo (ex.: `ingerir --texto` ou script `ingerir_federal.py`) que:

- aceite texto/MD como fonte (as leis do staging), rode `estruturar.parse_dispositivos` (gramática legal) e ingira com `fonte=federal`, autoridade federal na URN (`urn:lex:br:federal:lei:2015;13146`);
- valide contra o JSON estruturado do staging (contagem de artigos);
- aproveite `lexml.py` para confirmar as URNs canônicas das duas leis.

Sem isso o Manual de DH não consegue citar a LBI a partir do banco.

## Fase 1 — Camada `Leg` no pacote (permanente)

Recomendação de empacotamento: módulo próprio `crpsp-leg.sty` (ou `.code.tex`) carregado incondicionalmente pelo `book-crpsp_acessivel.sty` na seção 7 — mantém o pacote modular e a camada disponível em todo documento book.

### Mapeamento tipo LeXML → LaTeX (proposta; validar contra casos reais do banco)

| Tipo | Comando/ambiente | Notas |
|---|---|---|
| norma (wrapper) | `\begin{LegNorma}{<urn>}{<epígrafe>}` | espaçamento simples, `\hypertarget` da norma, fonte sans `\footnotesize`+`\singlespacing` como no visual atual; fecha com restauração completa |
| epígrafe | `\LegEpigrafe{RESOLUÇÃO CFP Nº 18/2002}` | hoje coberto por `\LegTitulo` (centrado/negrito) — criar `\LegEpigrafe` e manter `\LegTitulo` como alias deprecado (colide semanticamente com o agrupador "Título") |
| ementa | `\LegEmenta{...}` | existe; manter |
| preâmbulo | `\LegPreambulo{...}` | novo |
| prt/liv/tit/cap/sec/sub | `\LegAgrup{<tipo>}{<rótulo>}{<nome>}` ou comandos específicos (`\LegCapitulo` etc.) | headings internos à norma; NÃO usar `\section` do book (entraria no TOC e na hierarquia H do documento). Decidir tag: parágrafo destacado é aceitável; se virar heading, cuidar do nível na árvore |
| art (com cpt) | `\begin{LegArtigo}{Art. 1º}{<caput>} ... \end{LegArtigo}` | novo ambiente aninhável; manter o comando plano `\LegArtigo{label}{texto}` retrocompatível (o Manual publicado o usa) |
| par | `\LegParagrafo{§ 1º}{texto}` / `\LegParagrafoUnico` | existem; manter interface |
| inc / ali / ite | `\LegInciso{III}{texto}`, `\LegAlinea{a}{texto}`, `\LegItem{1}{texto}` | novos; aninhamento inc>ali>ite deve gerar `<L>/<LI>` corretos (listas aninhadas via description/enumitem compatível com block do phase-III — testar, enumitem tem restrições conhecidas com tagging) |
| decimal (NR) | `\LegDispDecimal{28.1.1}{texto}` | novo; recuo proporcional à profundidade |
| dpg (pena/disposição) | cobrir com `\LegDisp{<rótulo>}{texto}` genérico | fallback para tipos raros |
| fecho/assinatura | `\LegFecho{local, data}`, `\LegAssina{Nome}{Cargo}` | `\LegAssina` existe |

### Vigência, alterações e referências (dados que o banco fornece)

- `\LegNotaAlteracao{<texto da nota>}{<urn_alvo>}` — "(Redação dada pela Resolução X)" como nota pequena após o dispositivo, com hyperlink.
- `status=revogado`: marcar **textualmente** ("(Revogado)") além de visualmente (cinza) — leitor de tela não vê cor. Nunca usar riscado como única marca.
- `\LegRef{<urn>}{<texto>}` — link interno (`\hyperlink`) se o alvo estiver no documento; senão, externo para `https://www.lexml.gov.br/urn/<urn>`.
- `\LegAncora{<frag_id>}` — `\hypertarget` por dispositivo (gerador emite automaticamente; permite remissão fina art8_cpt_inc3).

### Restrições de acessibilidade (inegociáveis)

- Nada de titlesec; nada de tabular para layout; minipages são tecnicamente toleradas (precedente `\LegEmenta`/`\LegParagrafo`) mas **preferir** soluções por listas/parágrafos com recuo — as minipages atuais já têm nota de risco de ordem de leitura.
- Validar árvore de tags do MWE com lualatex-dev + inspeção (padrão do projeto: `<Sect>→<H1>…`, listas como `<L>/<LI>`).
- Texto de norma dentro de `LegNorma` deve permanecer no fluxo de leitura natural (sem artefatos).

## Fase 2 — Gerador `scripts/normativas/latexgen.py`

- Consome o JSON do `consolidar.py` (não consultar o SQLite diretamente — a interface única é o JSON; mesma fonte do viewer HTML).
- Emite um fragmento `.tex` por norma (`export/latex/<id_arquivo>.tex`) usando exclusivamente a camada `Leg`; escapar LaTeX (`&`, `%`, `#`, `_`…), converter aspas/travessões conforme tipografia do projeto.
- Recursão sobre `estrutura[]`: `art`→ambiente `LegArtigo` (caput = filho `cpt`), `inc/ali/ite` aninhados, agrupadores como `\LegAgrup`.
- `notas[]` → `\LegNotaAlteracao`; `status` → marcação de revogado; `relacoes.saidas` com `urn_alvo` → `\LegRef`.
- CLI: `python -m scripts.normativas.latexgen --urns <lista|arquivo> --out export/latex/`.

## Fase 3 — Manual de DH regenerado (prova de conceito)

1. Selecionar as normas do manual publicado (cap. 7: Resolução CFP 18/2002, e as demais listadas lá; cap. 5: DUDH — **não está no banco**; decidir: ingerir DUDH como documento `fonte=internacional` ou manter o capítulo como texto estático com `\LegArtigo` plano).
2. Documento-mestre `production/editorial/` novo, classe book + `\DocumentMetadata` UA-2, capítulos de prosa reaproveitados de `~/git/editoracao/manual/capitulos/` (converter resquícios memoir: `\OnehalfSpacing`→`\onehalfspacing`, `background`→`eso-pic`, `\tableofcontents*`→`\TOCAcessivel`).
3. Normas entram por `\input{export/latex/<id>.tex}`.
4. Compilar 2× lualatex; validar com veraPDF (UA-2) e conferência visual contra o manual publicado.

## Critérios de aceitação

- MWE com uma resolução real do banco compila sem warnings de estrutura aberta; árvore de tags correta; veraPDF UA-2 sem falhas de tagging.
- Resolução CFP 18/2002 regenerada do banco é textualmente idêntica à do manual publicado (diff tolerando tipografia).
- Leis 13.146 e 15.263 no banco com URN federal correta e artigos contados contra o JSON de staging.
- `book-crpsp_acessivel.sty` carrega a camada `Leg` sem quebrar documentos existentes (retrocompatibilidade de `\LegArtigo`, `\LegParagrafo`, `\LegEmenta`, `\LegTitulo`, `\LegAssina`).

## Decisões em aberto (perguntar a Angelo antes de fechar)

1. `\LegTitulo` legado vs. agrupador "Título" — renomear agora ou conviver com alias?
2. Agrupadores como headings tagueados (entram na árvore H) ou parágrafos destacados (fora dela)?
3. DUDH: ingerir no banco ou manter estática no manual?
4. Fragmentos gerados: versionados no git ou artefatos de build (regeráveis)?
