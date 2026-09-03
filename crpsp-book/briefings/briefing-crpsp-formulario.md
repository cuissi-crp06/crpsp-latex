# Briefing: `crpsp-formulario.cls`
**Para:** Claude Code
**Contexto:** Sistema editorial LaTeX do CRP-SP — linha de formulários
**Engine obrigatória:** LuaLaTeX
**Data:** 2026-07-03

---

## 1. Objetivo

Criar a linha editorial `formulario` do sistema v2 (`crpsp-formulario.cls` +
`formulario.sty`, sobre `crpsp-base.sty`) e migrar para ela os requerimentos de
`editorial/arquivo_latex/formularios/`. O ganho central é **acabar com as
larguras de caixa calibradas à mão**: hoje cada campo preenchível recebe uma
largura literal em `em` (`{34.3em}`, `{28.15em}`…) ajustada visualmente para o
rótulo atual — qualquer mudança de rótulo/fonte/margem quebra o encaixe.

A caixa passa a **se dimensionar sozinha conforme o layout da página**,
generalizando a técnica de pré-medição já usada na v2
(`\settowidth`/`\widthof` + `\dimexpr` sobre `\linewidth` — navbar e grid de
colunas de `guia-visual.sty`) e localmente em `pf-isencao-saude.tex:17-20`.

Escopo desta fase: **arquitetura + auto-largura**. Tagging PDF/UA-2 completo
(phase-III) fica para uma fase 2 (ver §8). Os campos continuam **interativos**
(AcroForm via `hyperref`).

---

## 2. Arquivos de entrada (ler antes de codar)

| Arquivo | Papel |
|---|---|
| `desenvolvimento/v2/crpsp-guia_visual.cls` | Modelo de classe article-based sobre `crpsp-base` |
| `desenvolvimento/v2/guia-visual.sty` | Referência da técnica de pré-medição (`:133-153`, `:225-237`, `:420-445`) |
| `desenvolvimento/v2/crpsp-base.sty` | Engine check, cores `cor1/2/3`, fontspec condicional |
| `arquivo_latex/formularios/formularios.sty` | Macros/estilo atuais a substituir |
| `arquivo_latex/formularios/form-sem-logo.sty` | Gêmeo redundante (vira opção `timbrado`) |

---

## 3. Arquivos a produzir

```
desenvolvimento/v2/crpsp-formulario.cls   ← NOVO: classe da linha (article + crpsp-base)
desenvolvimento/v2/formulario.sty         ← NOVO: layout + sistema de campos
desenvolvimento/v2/exemplo-formulario.tex ← NOVO: documento de teste mínimo
```

Depois: migrar os `.tex` de `arquivo_latex/formularios/`.

---

## 4. Arquitetura de dependências

```
crpsp-base.sty (já existe)
  ├── verificação de engine (LuaLaTeX)
  ├── cores cor1/cor2/cor3 + setters
  └── fontspec condicional (\ifcrpsp@fontspec)

crpsp-formulario.cls
  ├── \LoadClass{article}
  ├── \RequirePackage{crpsp-base}
  ├── opção [timbrado] → geometria de papel timbrado, sem logo
  ├── pacotes: graphicx, geometry, hyperref (\Form), calc,
  │            setspace, ragged2e, framed, xhfill, microtype, lastpage
  └── \RequirePackage{formulario}

formulario.sty
  ├── geometria A4 (padrão) / timbrado
  ├── tipografia NewJune → fallback (\IfFontExistsTF)
  ├── cores da marca (crp1=422C73, crp2=A55DA6, crp3=BF73AB)
  ├── pagestyle com logo + \thepage/\pageref{LastPage}
  ├── seccionamento sem numeração, colorido (sem titlesec — ver §8)
  └── SISTEMA DE CAMPOS AUTO-DIMENSIONÁVEIS  ← núcleo (§6)
```

`\DocumentMetadata` NÃO é emitido pela classe (regra do kernel). Nesta fase os
`.tex` não precisam dele; a fase 2 o adicionará.

---

## 5. Geometria e marca

- **Padrão** (`= formularios.sty:35-41`): `a4paper, left=1.5cm, right=2cm,
  top=3.5cm, bottom=2cm, headheight=3.5cm, headsep=\baselineskip`.
- **`timbrado`** (`= form-sem-logo.sty:35-41`): `left=4cm, right=2cm, top=6cm,
  bottom=4cm, headheight=4cm`, sem logo/rodapé.
- Cores institucionais (RGB atuais convertidos p/ HTML): principal `422C73`,
  secundária `A55DA6`, acessória `BF73AB`. Expor via `\crpspCor*` **e** manter
  aliases `crp1/crp2/crp3` (compat com `.tex` legados).
- `\logocrp` = `\includegraphics[height=2cm]{logo-crp.png}` com `\Alt` acessível
  (preparo p/ fase 2). Logo no `\makeoddhead`; rodapé `\thepage/\pageref
  {LastPage}`.

---

## 6. Sistema de campos auto-dimensionáveis (núcleo)

Três layouts reais precisam ser cobertos (ver formulários existentes):

### 6.1 Campo de linha cheia — `\campolinha{nome}{rótulo}`
O campo ocupa **todo o resto da linha** após o rótulo:
`width = \dimexpr\linewidth - \widthof{rótulo} - \campogap\relax`.
Substitui `\preenctext{...}{\linewidth}{}` e larguras cheias hardcoded
(ex.: campos "Motivo", "Nome da/do profissional", listas de e-mail com
`\fimdelinha`). Mede o rótulo com `\settowidth`.

### 6.2 Linha rotulada multi-campo — ambiente `camposlinha`
Vários campos rotulados numa linha, **espaço restante repartido por peso**
(mesmo princípio de `\coluna[span=N]`):

```latex
\begin{camposlinha}
  \campo[2]{banco}{Banco:}
  \campo[1]{agencia}{Ag.:}
  \campo[1]{conta}{Conta:}
\end{camposlinha}
```

Implementação **em duas passagens, estilo navbar** (sem re-executar o corpo):
`\campo` **apenas registra** (mede `\widthof{rótulo}`, guarda nome/peso/rótulo
em macros indexadas via `\csxdef`, acumula soma de rótulos e de pesos); o
ambiente, no `\end`, calcula
`unit = (\linewidth − Σrótulos − (n−1)·\campogap) / Σpesos` e desenha cada
campo com `width = peso·unit`. Determinístico; escala com fonte e margem.
Peso default = 1 (divisão igual). Avisar se `unit < 0` (rótulos não cabem).

Cobre: blocos de identificação (Nome/RG/CPF/…), "tel. res./tel. com.", as 4
minipages de `falta-atraso`, "Banco/Ag./Conta".

### 6.3 Campo embutido em prosa — `\campo*{nome}{rótulo}{largura}`
Escape hatch de largura fixa, para campos que precisam fluir **dentro de uma
frase justificada** (ex.: o "Eu, ___, RESPONSABILIZO-ME…" de `pj-termo_rt`).
Mantém a semântica de `\preenctext`, mas com **assinatura única e
documentada**. Na migração, preferir reestruturar blocos tabulares (a maioria)
em `camposlinha`; usar `\campo*` só onde o texto é mesmo corrido.

### 6.4 Primitivas auxiliares (reescritas sobre as acima)
- `\campodata{nome}` — dia/mês/ano (larguras fixas pequenas), sucessor de
  `\dataabrev` (fixar 1 assinatura).
- `\campodataextenso{nome}` — cidade + dia/mês/ano por extenso (`\dataextenso`).
- `\caixa{nome}{rótulo}` e ambiente `caixaslista` — checkbox + rótulo com
  associação acessível (sucessores de `\caixasel`/`\caixaselset`), reusando o
  padrão minipage `\boxlarg`/`\linewidth-\boxlarg` já existente (não sofre do
  problema de largura).
- `\blocoassinatura{legenda}` — `\rule{24em}{0.4pt}` + legenda (repetido em
  quase todos os formulários).
- **Altura** das caixas derivada da fonte (`\campoaltura`, default 14pt,
  ajustável), não literal por chamada.

### 6.5 Compatibilidade
Fornecer aliases `\preenctext`/`\dataabrev`/`\dataextenso`/`\caixasel`/
`\caixaselset` mapeando para as novas primitivas (fixando **uma** assinatura),
para migração incremental sem reescrever todos os `.tex` de uma vez. Documentar
a assinatura canônica no topo do `.sty`.

---

## 7. Comprimentos e parâmetros expostos

| Nome | Default | Papel |
|---|---|---|
| `\campogap` | 0.5em | folga rótulo ↔ caixa e entre campos |
| `\campoaltura` | 14pt | altura das `\TextField` |
| `\boxlarg` | 2em | largura da coluna de checkbox (compat) |
| `\fimdelinha` | `\textwidth-1.5\boxlarg` | compat com `.tex` legados |

---

## 8. Fora de escopo / fase 2 (PDF/UA-2)

- **Tagging phase-III completo.** Campos AcroForm interativos taggeados sob
  phase-III são fronteira do `latex-lab` e exigem validação própria. Nesta fase:
  só metadados + `\Alt` no logo + `tooltip`/rótulo nos campos.
- **Seccionamento sem `titlesec`.** titlesec é incompatível com phase-III
  (CLAUDE.md); redefinir os cabeçalhos via `\@startsection` (article) com cor da
  marca, `secnumdepth = -1` (sem numeração). Não introduzir titlesec.
- **`framed`** é usado hoje intensamente; verificar interação com tagging na
  fase 2 (pode precisar de contorno como tcolorbox→parbox do guia visual).
- Antes de qualquer workaround de tagging: rodar
  `python3 editorial/latex_acessivel/monitor_ctan.py`.

---

## 9. Documento de teste mínimo (`exemplo-formulario.tex`)

Deve compilar com LuaLaTeX (via podman) e exercitar:

- [ ] `\campolinha` preenchendo a linha (com rótulo curto e rótulo longo — a
      caixa encolhe sozinha)
- [ ] `camposlinha` com 2 e 3 campos, pesos iguais e diferentes
- [ ] `\campo*` de largura fixa em prosa
- [ ] `\campodata` e `\campodataextenso`
- [ ] `\caixa`/`caixaslista`
- [ ] `\blocoassinatura`
- [ ] variante `[timbrado]`

Usar `logo-crp.png` (já existe na pasta) ou fallback `\rule` se ausente no
container.

---

## 10. Critérios de aceitação

- [ ] `crpsp-formulario.cls` carrega `crpsp-base` e compila sem erro no
      container `crpsp-latex:dev`
- [ ] Numa `camposlinha`, trocar um rótulo por um mais longo **reduz** a caixa
      correspondente sem estourar a margem (prova do auto-dimensionamento)
- [ ] `\campolinha` chega à margem direita independentemente do comprimento do
      rótulo
- [ ] Campos `\TextField`/`\CheckBox` continuam preenchíveis no leitor de PDF;
      `name=` únicos
- [ ] `[timbrado]` aplica a geometria de margem grande sem logo
- [ ] Fallback de fonte funciona quando NewJune ausente (container)
- [ ] Nenhum `titlesec`; nenhuma dependência de `abntex2`

---

## 11. Sequência de implementação recomendada

1. `crpsp-formulario.cls` (esqueleto: article + crpsp-base + pacotes + opção
   `timbrado` + despacho).
2. `formulario.sty`: geometria, cores/marca, fontes com fallback, pagestyle,
   seccionamento.
3. Sistema de campos (§6) — primitivas + `camposlinha` + compat.
4. `exemplo-formulario.tex` e **compilar 2×** no container; validar §10.
5. Migrar os `.tex` (representativos primeiro: `pj-inscricao`,
   `pf-cancelamento_inscricao`, `pj-termo_rt`, `representacao`,
   `formulario-base`); depois os demais.
6. Limpeza: consolidar duplicatas (`crp-falta-atraso`≈`falta-atraso`,
   `pf-isencao-saude`≈`pf-isencao-viagem`, `declaracao`≈`pj-declaracao`,
   `autorizacao_uso_imagem`×cópia); corrigir `name=` colidido em
   `falta-atraso.tex:108,118`; resolver stub vazio `isencao-viagem.tex`;
   trazer `autorizacao_uso_imagem` e `pf-registro_especialista` p/ a linha
   comum. **Confirmar com o usuário o nome canônico antes de remover arquivos.**

> Parar e reportar após o passo 4 (exemplo compilando) antes da migração em
> massa.
