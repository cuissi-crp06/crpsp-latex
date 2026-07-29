---
tipo: briefing
dominio: editorial
projeto: crpsp-book
estado: pronto-para-execucao
criado: 2026-07-11
executor: a definir (Claude Opus 4.8 / GPT 5.6 Sol / Kimi 2.7-code)
---

# ~~Briefing — Ingerir as 20 normas restantes do Manual de DH~~ [EXECUTADO 2026-07-13 — 18/20]

**Resultado (sessão Claude, Bloco C):** as **18 resoluções** (17 CFP + 1
MEC/CNE/CP) foram extraídas, ingeridas (ids 2335–2352) e regeneradas como
fragmentos `\input`. Conversor generalizado:
`data/normativas/cfp/converter_normas_do_manual.py` (+ MDs de staging e
`manifest-normas-manual.json` na mesma pasta). Nenhuma estava no banco
(checado — os hits de numeração eram atas/NTs homônimas). **Critérios:**
build 2× sem erro, **veraPDF UA-2 PASS**, **diff textual 0,9925–0,9991 nas
18** (`v1/validar_normas.py`, preservado). URN do MEC: `--fonte mec` →
`urn:lex:br:mec.cne.cp:resolucao:2012-05-30;1` (fonte fora do mapa cai no
slug do órgão, como previsto). `build.ps1` agora copia fragmentos pelo
`manifest.json` do latexgen (fim da lista hardcoded). Backup do estático:
`v1/capitulos/7.normativas.tex.bak-20260713-pre-bloco-c`.

**Desvio reportado:** manual foi de 395 → **327 páginas** (esperado
~390–420). NÃO é o bug \list (que INFLA): a redução vem dos ~30
`\clearpage` internos dos blocos estáticos que a substituição eliminou +
renderização mais compacta dos fragmentos. O diff ≥99% por norma prova que
não houve perda de conteúdo; a paginação nova é decisão editorial a validar
na revisão visual (Bloco D).

**As 2 Notas Técnicas ficaram ESTÁTICAS** (comentário no .tex explica):
são prosa sem dispositivos e `latexgen.gerar_fragmento` só emite
ementa/preâmbulo/estrutura/fecho — regenerá-las exigiria suporte a corpo
de prosa no gerador. Decisão pendente com Angelo: implementar isso ou
aceitar as NTs estáticas.

**Falso alarme do briefing:** os "ANEXO" dos blocos eram menções em prosa —
nenhuma norma tinha anexo no estático. Artigo fora de macro
(`\textbf{Art. 10}.` na Res 08/2010, inconsistência do publicado) é
tratado pelo conversor.

---

# (histórico) Briefing — Ingerir as 20 normas restantes do Manual de DH e regenerá-las do banco

## Objetivo

Completar a regeneração do cap. 7 do Manual de Direitos Humanos: as ~20 normas hoje
**estáticas** em `production/editorial/publicacoes/manual_direitos_humanos/v1/capitulos/7.normativas.tex`
(marcadas com `% TODO ingerir no banco e regenerar`) devem ser ingeridas no banco de
normativas e passar a entrar no manual como fragmentos `\input{fragmentos/<id>.tex}`
regeneráveis — o mesmo caminho já validado para a DUDH e a Resolução CFP 18/2002.

## Contexto essencial (sessão 2026-07-11, Claude Fable)

O fluxo completo JÁ FUNCIONA de ponta a ponta. Não há código novo a inventar — é
**aplicação repetida de um processo validado**, com curadoria de conteúdo:

1. Extrair a norma do manual publicado → MD de staging (determinístico, via script).
2. `python -m scripts.normativas.ingerir_texto --arquivo <staging.md> --fonte cfp …`
3. `python -m scripts.normativas.consolidar --out export/`
4. `python -m scripts.normativas.latexgen --urns "@…/normas_do_manual.txt" --out export/latex/`
5. Substituir o bloco estático do 7.normativas.tex por `\input{fragmentos/<id>.tex}`,
   adicionar a URN ao `normas_do_manual.txt`, rodar `build.ps1`, validar.

**Modelo pronto**: `data/normativas/cfp/converter_cfp18_do_manual.py` extraiu a
CFP 18/2002 do `7.normativas.tex` do manual publicado (recorte por `\subsection` …
`\LegAssina`, limpeza de macros/tipografia LaTeX→texto, saída MD com H1 + ementa em
bold + preâmbulo + `Art. Nº texto`). O diff textual final contra o publicado deu
99,55%. Generalize esse script (parametrizar título/âncoras de recorte) em vez de
escrever 20 scripts.

## Leituras obrigatórias antes de codar

1. `scripts/normativas/README.md` — fases do pipeline; seção "Uso" tem os comandos.
2. `scripts/normativas/ingerir_texto.py` — docstring + CLI (`--validar`, `--artigos`,
   `--assina "NOME;Cargo"`, `--orgao`, overrides). É o ponto de entrada da ingestão.
3. `data/normativas/cfp/converter_cfp18_do_manual.py` + `resolucao_cfp_18_2002.md` —
   par ferramenta/produto do caso validado.
4. `production/editorial/publicacoes/manual_direitos_humanos/v1/README.md` — build e
   ARMADILHAS do manual (ler a seção inteira).
5. `editorial/latex_acessivel/crpsp-leg.sty` — contrato dos comandos Leg (comentários
   extensos; NÃO alterar o .sty neste trabalho).

## As 20 normas (ordem de aparição no cap. 7)

Resoluções CFP: 08/2020 (violência de gênero), 01/1999 (orientação sexual), 01/2018
(pessoas trans), 10/2018 (língua), 08/2022, 16/2017, 17/2022, 08/2022-2ª, 16/2015*,
06/2016*, 01/2017*, 17/2019, 02/2019, 09/2024, 17/2005*, 02/2000*, 31/1998*,
02/2019-2ª; Nota Técnica CRP-06; Nota Técnica CFP; Resolução MEC/CNE/CP 01/2018.
(Os números/datas exatos estão nas `\subsection` marcadas com TODO no
`7.normativas.tex` — confira lá; esta lista é orientativa.)

\* Verifique ANTES no banco (`SELECT urn, numero, ano FROM documentos WHERE fonte='cfp'`)
se alguma já entrou por outra via (a coleta CFP de 2026-07-06 ingeriu 83 legislações).
Se já existir com dispositivos bons, pule a extração e vá direto ao passo 4.

## Detalhes que vão morder (aprendidos no caso CFP 18/2002)

- **Fonte e órgão**: `--fonte cfp --orgao CFP` (resoluções CFP); Nota Técnica CRP-06
  usa `--fonte crp06 --orgao CRP-06` e `--tipo nota_tecnica`; MEC/CNE precisa de
  `--tipo resolucao` + `--orgao "MEC/CNE/CP"` (autoridade da URN cairá no fallback
  `_slugificar(orgao)` — conferir a URN gerada no `--dry-run` e validar manualmente).
- **Assinatura**: resoluções de conselho não têm fecho de Independência; use
  `--assina "NOME;Cargo"` (o texto da assinatura é removido do corpo e vai para
  `metadados_json`). O nome está no `\LegAssina{...}{...}` do bloco estático.
- **Preâmbulo**: termina em `RESOLVE:` (inclusive) — o extrator de preâmbulo já trata.
- **Estruturas além de artigos**: várias dessas resoluções têm §§ e incisos
  (`\LegParagrafo`, texto com `I —` etc. no estático). O MD de staging deve emitir
  `§ 1º texto` e `I - texto` em linhas próprias — `parse_dispositivos` reconhece.
  Valide a contagem com `--artigos N` (conte no bloco estático).
- **Emendas citadas**: se alguma norma citar outra entre aspas curvas “…”, o parser
  IGNORA os dispositivos internos (correto; é `<Alteracao>`).
- **Anexos**: se a norma tiver ANEXO no estático, decida: ingerir como componente
  (`;anexo.N` na URN — ver `_componente_anexo` em `ingerir.py`) ou manter o anexo
  estático com TODO próprio. Não invente estrutura nova sem necessidade.
- **id_arquivo**: é o nome do arquivo MD (slug estável). Padrão:
  `resolucao_cfp_08_2020.md` → fragmento `resolucao_cfp_08_2020.tex`.
- Depois de substituir cada bloco no `7.normativas.tex`, o texto estático da norma
  SAI do arquivo (fica só `\subsection` + `\input`). O diff textual (abaixo) protege
  contra perda de conteúdo.

## Critérios de aceitação

1. Cada norma ingerida com URN plausível, contagem de artigos validada e sem
   duplicar documento existente (dedup por sha256 é do arquivo MD — cheque por URN).
2. `build.ps1` compila o manual 2× sem erro; **veraPDF UA-2 PASS**
   (CLI: ver `v1/README.md`; se não estiver instalado, instalar via izpack
   `auto-install.xml` — precedente na sessão de 2026-07-11).
3. **Diff textual por norma** (pymupdf `get_text()` do PDF novo × bloco estático
   original, normalizando espaços/hifenização/aspas/travessões): similaridade ≥ 99%,
   diferenças apenas tipográficas ou a linha de epígrafe adicionada pelo gerador.
4. `normas_do_manual.txt` com as URNs novas; fragmentos NÃO versionados (são build).
5. Contagem de páginas do manual na mesma ordem de grandeza (~390–420). **Se o PDF
   inflar para milhares de páginas, é o bug \list/quebra-de-página** (ver
   `v1/README.md`, armadilha 3) — pare e reporte, não contorne.

## Fora de escopo

- Mexer nos `.sty` (qualquer necessidade de mudança na camada Leg → reportar).
- As leis/decretos/convenções do fim do cap. 7 sem marcação `% TODO` — ficam para
  quando houver fonte estruturada melhor (Planalto/LexML), não do texto do manual.
