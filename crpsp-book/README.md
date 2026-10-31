> **Atualização de 2026-10-31 (v0.6.0-alfa, issue #35).** O corpo mudou em relação
> à análise abaixo (escrita na v0.4.2): Atkinson Hyperlegible Next no lugar da Lora,
> sem hifenização, sem órfãs e viúvas, alinhamento à esquerda e pé irregular, sem
> `pdfpages` e sem `ragged2e`, `\DocumentMetadata` só com `tagging=on`, opções
> `web` e `print` e comandos novos (ver a seção 11). As seções 2, 3.1, 3.2, 3.3 e 3.4
> já estão ajustadas; o resto da análise vale como estava.

## Análise de `book-crpsp_acessivel.sty` (v0.4.2)

### 1. Contexto e propósito

Este pacote é uma **variante acessível** do pacote editorial `livros_crp.sty` (base `memoir`). Foi criado para produzir **PDFs compatíveis com PDF/UA-2** usando o motor **LuaLaTeX-dev** com o mecanismo de tagging automático do `latex-lab` (phase-III).

A decisão arquitetural central foi a **migração de `memoir` para `book`** (classe padrão do LaTeX), pois testes mostraram que `scrbook` (e presumivelmente `memoir`) produzia árvore de tags estruturalmente incorreta — títulos de capítulo e seção apareciam como `<P>` dentro de `<Part>`, sem `<H1>`/`<H2>`.

---

### 2. Pré-requisito obrigatório no documento

O `.tex` principal **deve** conter **antes** do `\documentclass`:

`\DocumentMetadata{     lang        = pt-BR,     pdfstandard = ua-2,     pdfversion  = 2.0,     tagging     = on, } \documentclass[11pt,a5paper,twoside,openright]{book}`

Sem isso, os workarounds de tagging não fazem sentido e a identidade visual pode degradar.

A chave `testphase={phase-III,...}`, que a documentação anterior prescrevia, é sintaxe legada ([issue 1484 do tagging-project](https://github.com/latex3/tagging-project/issues/1484), 2026-07-14): trabalho novo usa só `tagging=on`. Os MWEs antigos da régua ainda a declaram; os novos (`mwe_book_web`, `mwe_book_print`) não.

---

### 3. Estrutura detalhada do pacote

#### 3.1 Tipografia (seção 1)

|Aspecto|Implementação|
|---|---|
|**Motor**|`fontspec` com opção `[no-math]`|
|**Fonte do corpo**|Atkinson Hyperlegible Next (OTF do pacote `atkinson` do TeX Live), pelo `Path` resolvido no kpathsea; erro se faltar. `\tracinglostchars=3` faz glifo ausente (a Atkinson não tem U+0060) virar erro|
|**Fonte sans-serif**|NEWJUNE (família completa com 7 pesos: Regular, Bold, Medium, Fine, Light, Book, Ultrabold + itálicos)|
|**Famílias customizadas**|`\media`, `\fininha`, `\Light`, `\fontebook`, `\serifada`, `\pesada`|
|**Microtipografia**|`microtype` (protrusion + expansion)|
|**Hifenização**|Desligada (`\hyphenpenalty` e `\exhyphenpenalty` em 10000, mais o mesmo e `\lefthyphenmin`/`\righthyphenmin` em 62 no gancho `para/begin`). `babel[brazilian]` e `hyphenat` seguem carregados; `\hyph` marca ponto de quebra explícito em composto|
|**Reticências**|`xellipsis[oldmla]` — compatível com leitores de tela|
|**Espaçamento**|`\frenchspacing`|

**Observação PDF/UA:** o LuaTeX embute a fonte OpenType (subconjunto) com ToUnicode correto, essencial para acessibilidade. A Lora e a exigência dos `Lora-*.ttf` na pasta do documento saíram da `.sty` na 0.6.0; os arquivos continuam em `desenvolvimento/mwe/` só para as variantes de `legado/book-variantes/` que os MWEs `mwe_sty_manual` e `mwe_sty_notitlesec` ainda carregam.

#### 3.2 Cores e gráficos (seção 2)

- **Paleta CRP-SP:** `crp1` (azul escuro `#04586E`), `crp2` (azul médio `#199FAF`), `crp3` (rosa claro `#BF73AB`)
- **`eso-pic` substituiu `background`:** A API legada do `background` (v2.1 de 2014) injetava um "Draft" como marca d'água que virava conteúdo tagueado indesejado. `eso-pic` é ativamente mantido e integra bem com tagging.
- **Imagens de fundo são artefato:** `\includegraphics[artifact]{...}` (o latex-lab trata `alt={}` vazio como alt ausente, então não serve). `\FundoArtefato` (próxima página) e `\FundoTexto` (todas as páginas) já fazem isso.

#### 3.3 Tabelas (seção 3)

Pacotes carregados: `array`, `colortbl`, `multirow`, `longtable`, `tabularx`, `booktabs`, `enumitem`.  
Configurações: colunas `P{<larg>}` (centralizada) e `L{<larg>}` (à esquerda; sem hifenização, a célula `p{}` justificada estica os espaços), `\arraystretch=1.2`. Para tabela de dados com cabeçalho repetido, ver `tabelaguia` na seção 11.

#### 3.4 Diagramação e layout (seção 4) — **mudanças significativas**

**Layout de página via `geometry`:**

Reproduz manualmente o `\semiisopage` do `memoir` para A5:

- inner = 16.444mm, outer = 32.889mm
- top = 23.333mm, bottom = 30mm
- headheight = 14pt, headsep = 1.618\baselineskip

**Sumário:**

- `\setcounter{tocdepth}{0}` — apenas partes e capítulos
- `\setcounter{secnumdepth}{-1}` — sem numeração visível (hierarquia via tags)

**Redefinição de `\l@chapter`:** reduz o `\addvspace` de 1.0em para 0.5em para evitar transbordo da última entrada para página extra. Desde a 0.6.0 a margem direita da entrada é elástica (`\rightskip` com `plus 4em`) e a tolerância fica aberta dentro do grupo, porque sem hifenização a entrada longa batia no número da página (medida na seção 11).

**Penalidades tipográficas:** viúvas e órfãs proibidas (`\widowpenalty`, `\clubpenalty` e `\@clubpenalty` em 10000; o `\@afterheading` reatribui o `\clubpenalty` depois de todo título, então só o `\@clubpenalty` segura o ajuste nos capítulos). Antes eram 9999 e 9996.

**Parskip:** 0.5\baselineskip + 2pt (equivalente ao `\nonzeroparskip` do memoir).

**Alinhamento e pé de página (0.6.0):** `\raggedright` do kernel ligado no início do documento (no lugar do `\justifying` do `ragged2e`, que deixava `/TextAlign /Justify` na árvore de tags); `\raggedbottom` e `\topskip` rígido de 11 pt, de modo que a primeira linha de toda página de texto cai à mesma distância do cabeçalho. Custo: pé de página irregular.

**Espaçamento entre linhas:** indireção via `\setasuspacing`, padrão `onehalfspacing`.

**Page styles via `fancyhdr`:**

|Estilo|Uso|Características|
|---|---|---|
|`crp`|Miolo principal|Régua colorida + `\Light small` + número de página em `crp1`|
|`crpPre`|Pré-textuais|Mesmo layout, fonte `\fontebook` em itálico|
|`pretext`|Folha de rosto/partes|Sem cabeçalho|
|`plain`|Páginas de abertura de capítulo|Sem cabeçalho (redefinido)|

A régua colorida é feita redefinindo `\headrule` com `\color{crp1}`, já que `fancyhdr` não tem equivalente ao `\makeheadfootruleprefix` do memoir.

---

### 4. Workarounds críticos para tagging (PDF/UA)

Esta é a parte mais complexa e sofisticada do pacote.

#### 4.1 Títulos de capítulo via `sec-template` (latex-lab phase-III)

**Problema:** Com `\DocumentMetadata` + `tagging=on`, o `latex-lab-testphase-sec-template.sty` declara a instância `chapter` do tipo `heading/display` via `\AddToHook{class/book/after}`. Isso faz `\chapter` usar `\UseInstance{heading}{chapter}` em vez de chamar `\@makechapterhead`. Redefinir `\@makechapterhead` torna-se letra morta.

**Solução:** Redeclarar a instância `chapter` com `\AddToHook{class/book/after}[crp/chapter]`, configurando:

- `decls = \raggedright\parindent0pt\bfseries\sffamily`
- `number-decls = \huge\color{crp1}`
- `title-decls = \Huge\color{crp1}`

**Nota técnica importante:** `\color{crp2}` foi inicialmente tentado em `decls`, mas o `headformat/display` do `sec-template` executa `\normalfont\normalcolor` antes de `decls`, resetando a cor. A cor correta é aplicada em `title-decls` e `number-decls`, que rodam por último.

#### 4.2 Sumário acessível (`\TOCAcessivel`)

**Bug upstream conhecido:** `latex-lab-testphase-toc` captura o título do sumário antes de `\protect` resolver `\contentsname`, resultando em tags `<H1>` com conteúdo cru:

```
Sum\'ario\protect \markboth {\MakeUppercase []{Sum\'ari...
```

**Workaround:** `\TOCAcessivel` usa `\chapter*{Sumário}` + `\@starttoc{toc}` diretamente, omitindo `\phantomsection` e `\addcontentsline` (evita entrada recursiva). Quando o bug for corrigido upstream, pode-se voltar a `\tableofcontents`.

**Defeito cosmético residual:** O `<TOCI>` das partes mostra prefixo `"l1em"` colado ao texto (ex.: `"l1emPrimeira parte do teste"`). Origem não confirmada — pode ser `\l@part` do `book.cls`, `titlesec` (não usado aqui), ou o próprio `latex-lab-testphase-toc`.

#### 4.3 Seções via `\@startsection` (sem `titlesec`)

`titlesec` é **incompatível** com `latex-lab` phase-III, causando:

```
number of automatic begin (N) and end (N-1) text-unit para hooks differ
```

Solução: redefinir diretamente `\@startsection` para `\section`, `\subsection`, `\subsubsection`, `\paragraph`, `\subparagraph`. Isso preserva o mecanismo de tagging nativo do `latex-lab`.

#### 4.4 Partes (`\part`)

Redefinidas manualmente (`\@part`, `\@spart`) mantendo `\cleardoublepage` e `\@endpart` do `book.cls`. `\MakeUppercase` foi **removido** intencionalmente — leitor de tela pronunciaria siglas letra-por-letra. Se caixa alta for necessária, deve ser escrita literalmente no `.tex`.

#### 4.5 Cor `crp1` nos links

`hyperref` configurado com `linkcolor=crp1` (na versão memoir era `black`). Isso melhora a usabilidade sem prejudicar a acessibilidade, desde que haja contraste suficiente.

#### 4.6 Correção `nameref`

O `nameref` captura `\@chapter` antes de `\@makechapterhead` estar disponível. Corrigido via `\AtBeginDocument{\let\NR@chapter\@chapter \let\NR@schapter\@schapter}`.

---

### 5. Seção 7: Comandos e ambientes institucionais

|Comando/Ambiente|Função|Status PDF/UA|
|---|---|---|
|`\SubTituloUm`|Subtítulo sobrescrito ao título de capítulo|✅|
|`\estrangeirismo{idioma}{termo}`|Itálico + `Span` com `/Lang` (0.6.0)|✅ no veraPDF; leitor de tela não verificado|
|`tabelaguia`, `\FundoArtefato`, `\FundoTexto`, `\iniciotextual`, `Colofao`|Ver a seção 11 (0.6.0)|✅|
|`\Entretitulo`|Intertítulo em `crp1` + `\Light`|✅|
|`\setetoques`|Filete decorativo|✅ (semântica neutra)|
|`\assinaapresenta`|Bloco de assinatura institucional|⚠️ (flushright pode gerar warning de ordem de leitura)|
|`\LegAssina`|Assinatura centrada (nome + cargo)|✅|
|`\LegTitulo`|Título centrado em negrito|✅|
|`\LegEmenta`|Ementa de legislação com offset|⚠️ (minipage pode gerar warning de ordem de leitura no tagpdf)|
|`\LegArtigo`|Artigo de lei via `description`|⚠️ (phase-III intercepta `description`, rejeita chaves `enumitem`)|
|`\LegParagrafo`|Parágrafo de lei com recuo|⚠️ (mesmo warning de minipage)|
|`\Caso`|Abertura de caso clínico/ético|✅|
|`blocao` / `blocaosingle`|Bloco sem recuo|✅|
|Ambientes `CreditoInstitucional`|Páginas de créditos|✅|
|`\CreditoTecnico`|Label + valor|**Refatorado:** `tabular` → `\parbox` duplo (PDF/UA proíbe tabelas de layout)|
|`\CargoNosCreditos`|Duas colunas de cargos|**Refatorado:** `tabular` → `\parbox` duplo. **Mudança de interface:** agora requer 2 args separados|
|`\NomeNosCreditos`|Lista de nomes|**Refatorado:** `tabular{p{\linewidth}}` → parágrafo direto|

#### Decisão importante sobre tabelas de layout

A refatoração dos créditos removeu todas as `tabular` usadas para layout (proibidas por PDF/UA). A interface de `\CargoNosCreditos` mudou de um argumento tabular (`col1 & col2 \\`) para dois argumentos separados (`\CargoNosCreditos{col1}{col2}`). Documentos existentes precisam ser atualizados.

#### `\LegArtigo` e `enumitem`

O comentário no código alerta que `phase-III/block` intercepta `description` e rejeita chaves `enumitem` (`align`, `leftmargin`, `labelwidth`, `labelsep`). A indentação padrão do `book` é aceita.

---

### 6. O que foi removido em relação à versão memoir

|Elemento|Versão memoir|Versão book acessível|Motivo|
|---|---|---|---|
|**Classe base**|`memoir`|`book`|Compatibilidade com tagging|
|**Comandos memoir-only**|`\semiisopage`, `\checkandfixthelayout`, `\nonzeroparskip`, `\sloppybottom`|`geometry`, `\setlength`, `\parskip`|memoir não suporta phase-III|
|**Page styles**|`\makepagestyle`, `\copypagestyle`, `\makeheadrule`|`fancyhdr`|API memoir incompatível|
|**Títulos de seção**|`\setsecheadstyle`, `\hangsecnum`|`\@startsection` redefinido + `sec-template`|titlesec incompatível com tagging|
|**Capítulos**|`\chapterstyle{CRP01}`|Instância `heading` do `sec-template`|phase-III intercepta|
|**Partes**|`\printparttitle`, `\beforepartskip`|`\part` redefinido manualmente|controle total da tagueação|
|**`background`**|Sim|`eso-pic`|API legada, injetava tags indesejadas|
|**`changes`**|Sim|Removido|colide com `\comment` e não deve ir no PDF final|
|**`colophon`**|Sim|Removido (implícito)|depende de memoir|
|**`tocvsec2`**|Sim|Removido|memoir-only|

---

### 7. Problemas conhecidos e dívidas técnicas

1. **Prefixo `"l1em"` no `<TOCI>` das partes:** não bloqueante, origem não confirmada.
2. **Minipages em `\LegEmenta` e `\LegParagrafo`:** `tagpdf` pode emitir warnings de ordem de leitura. Mantido por decisão do usuário (compatibilidade visual).
3. **`\TOCAcessivel` é workaround:** deve ser substituído por `\tableofcontents` quando o bug upstream for corrigido.
4. **Cor das partes:** usando `crp1`, enquanto `\@makechapterhead` (fallback) usa `crp2`. Isso é intencional? A consistência visual entre capítulos e partes merece revisão.
5. **`\boxementa`, `\indicartigo` etc.:** calculados em `\AtBeginDocument` — sensíveis a mudanças de fonte/layout posteriores ao preâmbulo.

---

### 8. Linha do tempo evolutiva (arquivo de versões)

Com base nos arquivos encontrados em `arquivo_latex\sty\`:

|Arquivo|Data|Tamanho|Notas|
|---|---|---|---|
|`livros_crp.sty`|09/04/2026|18.043 B|Base memoir (produção legada)|
|`livros_crp_acessivel.sty`|09/04/2026|14.039 B|Primeira tentativa acessível (provavelmente com scrbook)|
|`livros_crp_acessivel_notitlesec.sty`|09/04/2026|17.109 B|Teste sem titlesec|
|`livros_crp_acessivel_manual.sty`|09/04/2026|7.280 B|MWE das redefinições manuais|
|`livros_crp_acessivel_book.sty`|10/04/2026|24.434 B|**Versão book estável**|
|`livros_crp_acessivel_book_old.sty`|15/04/2026|24.631 B|Iteração anterior do book|
|**`book-crpsp_acessivel.sty`** (atual)|**14/04/2026**|**27.952 B**|**Versão final renomeada**|

A versão atual é a mais completa, incorporando:

- Seção 7 inteira (comandos institucionais)
- Refatoração de tabelas de layout para `\parbox`
- Workarounds para `nameref` e `sec-template`
- Documentação extensa inline

---

### 9. Recomendações técnicas

1. **Compilação obrigatória com `lualatex-dev`:** a versão `-dev` do LaTeX contém os módulos `latex-lab-dev` com correções de tagging não disponíveis na versão estável. O ganho principal é a estruturação correta do sumário com `<TOCI>/<Reference>/<Link>`.
2. **Monitoramento do upstream:** os workarounds `\TOCAcessivel` e a redeclaração da instância `chapter` via `sec-template` são dependentes de versões específicas do `latex-lab`. Deve-se acompanhar o changelog do `latex-lab-testphase-sec-template` e do `latex-lab-testphase-toc` para remover as gambiarras quando possível.
3. **Migração de documentos legados:** qualquer documento que use `\CargoNosCreditos{col1 & col2 \\}` deve ser atualizado para `\CargoNosCreditos{col1}{col2}`. Recomendo criar um script de busca/substituição ou documentar essa quebra de compatibilidade em notas de release.
4. **Investigação do prefixo `"l1em"`:** embora não seja bloqueante, esse artefato no `<TOCI>` das partes indica que alguma macro interna do `book.cls` ou do `latex-lab` está capturando um `\hspace` literal. Vale abrir um `gather` para isolar se vem de `\l@part`, do `sec-template` ou do hook de TOC.
5. **Contraste de cores:** as cores `crp1` (`#04586E`) e `crp2` (`#199FAF`) sobre branco devem ser verificadas formalmente contra os critérios de contraste WCAG 2.1 (mínimo 4.5:1 para texto normal, 3:1 para texto grande). A cor `crp3` (`#BF73AB`) é mais clara e deve ser usada apenas para elementos decorativos, nunca para texto funcional.
6. **Validação contínua:** após cada compilação, abrir o PDF no Acrobat Reader (painel Tags) ou usar `veraPDF` para validação automática de PDF/UA-2. Em específico:
    - Verificar se `<H1>` aparece para capítulos
    - Verificar se `<H2>`/`H3` aparecem para seções/subseções
    - Confirmar que imagens decorativas têm `alt=""` (não omitido)
    - Confirmar que `<TOCI>` não contém macros cruas

---

### 10. Conclusão

O `book-crpsp_acessivel.sty` é um pacote de produção editorial maduro e bem documentado, resultado de uma migração deliberada e justificada da classe `memoir` para `book`. Possui as seguintes características distintivas:

**Pontos fortes:**

- **Arquitetura correta para PDF/UA-2:** a decisão de usar `book` + `latex-lab` phase-III é tecnicamente sólida e validada por MWEs isolados.
- **Workarounds bem documentados:** cada gambiarra tem comentário explicando o bug upstream, a data do teste e quando pode ser removida.
- **Identidade visual preservada:** apesar da mudança de classe, o layout (margens, fontes, cores, page styles) reproduz fielmente a versão memoir.
- **Remoção de antipadrões de acessibilidade:** tabelas de layout foram substituídas por `\parbox`, `\MakeUppercase` foi removido, e `alt={}` é documentado para imagens decorativas.

**Pontos de atenção:**

- **Fragilidade upstream:** o pacote depende de versões `-dev` do LaTeX e de hooks internos do `latex-lab` que podem mudar. A manutenção exige acompanhar releases do LaTeX.
- **Quebra de compatibilidade:** a interface de `\CargoNosCreditos` mudou; documentos antigos precisam ser portados manualmente.
- **Minipages pendentes:** `\LegEmenta` e `\LegParagrafo` usam `minipage`, que pode gerar warnings de ordem de leitura no futuro.

**Status geral:** o pacote está pronto para produção de publicações institucionais do CRP-SP em formato PDF/UA-2. O pipeline `.tex → lualatex-dev → PDF validado` funciona para os cenários testados (texto corrido, títulos, tabelas simples, listas, links e imagens decorativas). A dívida técnica está concentrada em workarounds documentados cuja remoção depende do upstream, não da lógica interna do pacote.

---

Essa análise cobre a totalidade do arquivo `book-crpsp_acessivel.sty`, seu contexto de desenvolvimento, sua genealogia e sua maturidade para uso em produção editorial acessível.

---

## A. Monitoramento CTAN (`latex-base-dev`)

Esta seção é atualizada automaticamente pelo script `monitor_ctan.py`.

<!-- CTAN-VERSION-START -->
**Última verificação CTAN:** 2026-10-05 08:10

- `latex-base-dev`: **`pre-release 2`** (2026-11-01) ✅
- `latex-lab`: **`2026-06-01a`** () ✅
- `tagpdf`: **`1.0g`** (2026-09-23) ⚠️ NOVA VERSÃO
<!-- CTAN-VERSION-END -->

Para executar a verificação manualmente (de `crpsp-book/`):
```bash
python3 monitor_ctan.py
```

---

## B. Briefings (`briefings/`)

Especificação escrita antes da implementação: cada linha editorial nova, ou
cada mudança grande numa existente, entra primeiro como briefing e só depois
vira `.cls`/`.sty`. Ler o briefing relevante por completo antes de mexer no
código correspondente.

**Escopo ativo (desde 2026-09-16).** O desenvolvimento se concentra em três
linhas, todas acessíveis: `relatorio`, `livro` (cartilha/manual) e
`formulario`. A linha `guia_visual` foi **cancelada** — a publicação em 16:9
migra para GitHub Pages. Os demais briefings ficam marcados para arquivar:
valem como registro do que foi decidido e feito, não como trabalho a executar.

| Arquivo | Data | Do que trata | Estado |
|---|---|---|---|
| [`briefing-crpsp-livro-relatorio.md`](briefings/briefing-crpsp-livro-relatorio.md) | 2026-09-16 | Classes `crpsp-livro.cls` (`manual`/`cartilha`) e `crpsp-relatorio.cls` (`interno`/`externo`): medida por papel, corpo 12 pt e adoção condicional da Luciole | **Ativo.** A metade `relatorio` está feita (0.2.0-alfa, 2026-09-17, com `interno`/`externo`); a `livro` não começou. ⚠️ A tipografia do briefing foi superada: o corpo do `relatorio` é Atkinson, não Luciole, e a mancha é de 75 caracteres — ver `decisoes-2026-09-17.md` |
| [`briefing-crpsp-formulario.md`](briefings/briefing-crpsp-formulario.md) | 2026-07-03 | Linha `formulario` da v2 (`crpsp-formulario.cls` + `formulario.sty`) e migração dos requerimentos de `formularios/` | **Ativo.** Implementado em `desenvolvimento/v2/`; não se confunde com os `.sty` memoir de `crpsp-forms/` |
| [`briefing-leg-book-acessivel.md`](briefings/briefing-leg-book-acessivel.md) | 2026-07-10 | Camada `Leg` no `book-crpsp_acessivel.sty` (tipos LeXML) e gerador normativas→LaTeX | Arquivar as fases 2 e 3 (gerador, Manual de DH). A camada em si é código vivo: `crpsp-leg.sty` v0.3.0, previsto como módulo `leg` da linha `livro` |
| [`briefing-manual-dh-acabamento.md`](briefings/briefing-manual-dh-acabamento.md) | 2026-07-11 | Acabamento visual e de acessibilidade do Manual de DH v1 | Arquivar |
| [`briefing-manual-dh-normas-restantes.md`](briefings/briefing-manual-dh-normas-restantes.md) | 2026-07-11 | Ingestão das 20 normas restantes do Manual de DH | Arquivar (executado em 2026-07-13, 18/20) |
| [`briefing-crpsp-guia_visual.md`](briefings/briefing-crpsp-guia_visual.md) | 2026-06-24 | Classe 16:9 (`crpsp-guia_visual.cls` + `guia-visual.sty`) e extração de `crpsp-base.sty` a partir de `crpsp_acessivel.cls` | **Cancelado** em 2026-09-16 (migra para GitHub Pages); os arquivos seguem em `desenvolvimento/v2/`, e a extração do `crpsp-base.sty` que ele motivou continua valendo |

O plano de retomada
[`plano-2026-09-16-linhas-ativas.md`](briefings/plano-2026-09-16-linhas-ativas.md)
lê os briefings em conjunto: o que incorporar dos arquivados, as colisões
abertas (paleta, 11 pt × 12 pt no `relatorio`, destino do `book` e da linha
`guia`) e a ordem de trabalho proposta.

Na mesma pasta, fora da série: [`guia_visual.md`](briefings/guia_visual.md) e
`guia_visual.excalidraw.md` (organização fixa dos guias e esboço de layout,
insumos do briefing de 2026-06-24 — arquivar junto com ele), `insumos-jornal/` (expedientes, paleta e
relatório que alimentaram o relatório do Jornal Psi) e
`issue-draft-list-csname-tagging.md` + `issue-link-prefilled.txt` (rascunho de
issue para o upstream do tagging: `\hsize` corrompido quando um `description`
na forma csname atravessa quebra de página) e
[`relato-atkinson-u0060.md`](briefings/relato-atkinson-u0060.md) (rascunho de
e-mail ao mantenedor do pacote CTAN `atkinson`: o `.otf` embarcado não mapeia
U+0060, e a convenção de aspas do TeX falha em silêncio sob fontspec).

---

## 11. Versão 0.6.0-alfa: opções `web` e `print` e o que veio do guia (issue #35)

A revisão 2 do *Guia de boas práticas para apresentações acessíveis* reuniu em 30/09
e 01/10/2026 soluções que viviam só no `.tex` da publicação. A 0.6.0-alfa as traz
para a `.sty`. Detalhe da numeração e das medidas em `CHANGELOG.md`.

### Opções do pacote

| | sem opção | `web` | `print` |
|---|---|---|---|
| Faces e abertura de capítulo | as do `\documentclass` | `oneside` + `openany` | `twoside` + `openright` |
| Fundo de texto (`\FundoTexto`) | ímpar/par se `twoside`, só o ímpar se `oneside` | só o ímpar | ímpar e par |
| Referências | a cargo do documento | `\nocite{*}` se o biblatex estiver carregado | a cargo do documento |

As opções forçam `\if@twoside` e `\if@openright` no início do pacote, antes do
`geometry`. O `geometry` relê as opções do `\documentclass` e religaria o `twoside`,
então a `.sty` também repassa `twoside=false` (ou `true`) a ele por
`\PassOptionsToPackage`. Por isso a opção vale mesmo quando o `\documentclass`
pede o contrário (os dois MWEs fazem isso de propósito). **Sem opção** o pacote
respeita o `\documentclass`, para não quebrar documento existente; a decisão de
qual deve ser o padrão fica com o mantenedor. Fora do escopo, por decisão: cinza,
corte, sangria e PDF/X do `print`.

### Comandos e ambientes novos

| Item | Função |
|---|---|
| `\estrangeirismo{en}{termo}` | itálico + `Span` com `/Lang` (WCAG 3.1.2); `\foreignlanguage` do babel não grava `/Lang` sob `tagging=on`. Não usar em título |
| `tabelaguia{colunas}` | `longtable` com a primeira linha como cabeçalho (repetido na quebra), `\footnotesize`, `\arraystretch` 1,3; `\rowcolor` por `colortbl`. Colunas `L{larg}` (à esquerda) |
| `\FundoArtefato{arte.pdf}` | arte de página inteira, só na próxima página, como artefato (capa e quarta capa) |
| `\FundoTexto{impar.pdf}{par.pdf}` | fundo de todas as páginas daqui em diante, como artefato; alterna ímpar/par só em `twoside` |
| `\iniciotextual` | `\mainmatter` + `\pagestyle{crp}`: a Introdução fica no pré-textual e a numeração árabe começa no primeiro capítulo |
| `Colofao` | página própria com os créditos técnicos, a licença e a ficha catalográfica, se houver |

`\SubTituloUm` e `\assinaapresenta` passaram de `\justifying` a `\raggedright`; o
`crpsp-leg.sty` (0.3.1-alfa) também, em `\LegEmenta`, porque o `ragged2e` saiu.

### MWEs

`desenvolvimento/mwe/mwe_book_web.tex` e `mwe_book_print.tex` compilam o mesmo
conteúdo (`mwe/book_comum/corpo.tex`, `refs.bib` e fundos A5 provisórios, gerados por
`gerar-fundos.tex`) com uma opção e a outra. O `\documentclass` de cada um pede o
contrário da opção. Sem `crpsp-abnt.bbx` no caminho (régua), caem para `authoryear` e
a lista sai vazia, porque o biber não roda lá; para a lista real, compilar com
`lualatex`, `biber`, `lualatex` (duas vezes) e `crpsp-abnt` e `biblatex-abnt` no
`TEXINPUTS`.

### Sumário sem hifenização

`desenvolvimento/medida/sumario-longo.tex` gera 48 capítulos com títulos de 3 a 18
palavras e conta os `Overfull` do sumário. Com a margem rígida do `book.cls`, 42
entradas estouram (até 81 pt); com `plus 4em` (solução do guia), 12 (até 40 pt); com
`plus 4em` e `\tolerance 10000` dentro do grupo da entrada, nenhuma. É a solução
adotada em `\l@chapter`; a escolha final é do mantenedor.

### Pendente

- Nenhuma conferência no MiKTeX (a linha `book` foi medida no podman).
- A troca de voz do `\estrangeirismo` não foi ouvida em NVDA + Acrobat Reader.
- Título de capítulo muito longo estoura o cabeçalho corrente das páginas pares em
  `twoside` (`\leftmark` não quebra linha): o aviso do `fancyhdr` sobre
  `\headheight` aparece no MWE `print`.
