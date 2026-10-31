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

> **Medição de 2026-10-31** (imagem `crpsp-latex:rodada-20261031`, TeX Live 2026,
> 2 passadas). Larguras em bp, lidas do `/Rect` dos widgets por
> `desenvolvimento/medida/campos-acroform.py`; a largura pedida a cada campo
> sai do `.log` de `v2/exemplo-formulario-aceite.tex`, que traz os casos que o
> `exemplo-formulario.tex` não cobria (rótulo curto/médio/longo, pesos 2:1 e
> 3:1:2, campo único, rótulos que não cabem e a variante `timbrado`). O
> `/Rect` de um campo sem tagging é 2,07 bp mais largo que a largura pedida
> (a borda do widget); com `tagging=on` fica na pedida (±0,1 bp).

- [x] `\campolinha` preenchendo a linha (com rótulo curto e rótulo longo — a
      caixa encolhe sozinha). *Medido:* rótulo `Nome:` 450,89 bp; `Nome
      completo:` 399,25 bp; rótulo de 376 pt 111,39 bp; as três terminam em
      533,60 bp.
- [x] `camposlinha` com 2 e 3 campos, pesos iguais e diferentes. *Medido:*
      pesos 1:1:1 dão 126,19 bp cada; 2:1 dão 273,62 e 137,81 bp (razão pedida
      2,000); 3:1:2 dão pedidas 172,78 / 57,59 / 115,19 pt (razão 3,00:1:2,00).
- [x] `\campo*` de largura fixa em prosa. *Medido:* na implementação o nome é
      `\campofixo{nome}{rótulo}{largura}` (o `\campo*` do §6.3 não existe);
      `18em` pedido dá 217,19 bp (= 215,19 bp + borda), dentro de parágrafo
      justificado.
- [x] `\campodata` e `\campodataextenso`. *Medido:* 20 campos no exemplo, 3 de
      `\campodata` (25,9 / 25,9 / 37,86 bp) e 4 de `\campodataextenso`.
- [x] `\caixa`/`caixaslista`. *Medido:* 3 widgets `/FT /Btn`, 12,95 bp de lado
      (11 pt + borda). O exemplo emite 3 `Underfull \hbox` nas linhas das
      `\caixaitem`, sem efeito visível medido.
- [x] `\blocoassinatura`. *Medido:* o texto "Assinatura" sai no PDF; a régua de
      24em não foi medida em bp.
- [x] variante `[timbrado]`. *Medido:* ver §10.

Usar `logo-crp.png` (já existe na pasta) ou fallback `\rule` se ausente no
container.

*Medido:* sem o arquivo na pasta, o fallback `\rule` compila sem erro; com
`logo-crp.png` na pasta há 1 imagem (1570 × 618 px) na página. O `logo-crp.png`
mora em `formularios/`, não em `desenvolvimento/v2/`.

---

## 10. Critérios de aceitação

- [x] `crpsp-formulario.cls` carrega `crpsp-base` e compila sem erro no
      container `crpsp-latex:dev`. *Medido na imagem `crpsp-latex:rodada-20261031`
      (não na `:dev`):* `exemplo-formulario.tex` e `exemplo-formulario-aceite.tex`,
      1 página, 0 erro fatal, 0 `Missing character`, 0 erro de tagging. O
      `exemplo-formulario.tex` tem 3 `Underfull \hbox` (as `\caixaitem`).
- [x] Numa `camposlinha`, trocar um rótulo por um mais longo **reduz** a caixa
      correspondente sem estourar a margem (prova do auto-dimensionamento).
      *Medido:* `Banco:`/`Ag.:`/`Conta:` dão 126,19 bp por caixa; trocando `Ag.:`
      por `Agência bancária completa:` cada caixa cai para 84,13 bp (-42,06 bp).
      A unidade é comum à linha, então **todas** as caixas encolhem, não só a do
      rótulo trocado. A borda direita fica em 539,58 bp nos dois casos, 1,0 bp
      (a borda do widget) além da margem em 538,58 bp.
- [ ] `\campolinha` chega à margem direita independentemente do comprimento do
      rótulo. *Falhou:* nos três rótulos a caixa termina em
      533,60 bp, constante, mas **4,98 bp (1 `\campogap`) antes** da margem
      (538,58 bp). A classe subtrai `2\campogap`; o §6.1 acima escreve `1`. Não
      alterado: o ajuste é decisão do mantenedor (com 1 gap a caixa passaria a
      terminar a 1 bp além da margem, como na `camposlinha`).
- [ ] Campos `\TextField`/`\CheckBox` continuam preenchíveis no leitor de PDF;
      `name=` únicos. *Parcial: estrutura AcroForm e `name=` únicos medidos;
      preenchimento em leitor gráfico não verificado.* Medido por `mutool show`: `/AcroForm` presente com
      `/NeedAppearances true`; 17 `/FT /Tx` + 3 `/FT /Btn` no exemplo, nenhum com
      `/Ff` (nenhum somente-leitura); 0 nome duplicado em `/T` (20 de 20 no
      exemplo, 17 de 17 no de aceite). **Não verificado:** preenchimento em
      leitor gráfico. **Risco:** `\campodata{id}` e `\campodataextenso{id}` geram
      `dia<id>`, `mes<id>`, `ano<id>`; repetir o mesmo `id` duplica o `name=`, e
      nada na classe avisa.
- [x] `[timbrado]` aplica a geometria de margem grande sem logo. *Medido:* texto
      começa em x = 113,39 bp (4 cm; padrão 42,52 bp); o título desce 70,9 bp
      (2,5 cm = 6 cm - 3,5 cm); `pdfimages` não acha imagem e o rodapé `1/1`
      some. Margem inferior de 4 cm não medida.
- [x] Fallback de fonte funciona quando NewJune ausente (container).
      *Medido:* sem `/fonts` montado o PDF usa `TeXGyreHeros`, 0 aviso e 20
      campos idênticos aos da compilação com as fontes montadas (mesmo `pdftotext`,
      mesmos `/Rect`). **Achado:** a ramificação NewJune nunca é tomada aqui:
      `\IfFontExistsTF{NewJune}` dá falso mesmo com `editorial/fonts` montado,
      porque as faces do Nextcloud se chamam `NewJuneRegular`, `NewJuneBold`…
      (arquivos `NEWJUNE-REGULAR.OTF`; `relatorio.sty` carrega por arquivo).
      Não alterado: mudar de Heros para NewJune muda toda a paginação. O terceiro
      nível (Computer Modern Sans) não foi exercitado.
- [x] Nenhum `titlesec`; nenhuma dependência de `abntex2`. *Medido:* 0 ocorrência
      nos dois `.log`; nos fontes `.cls`/`.sty` as palavras só aparecem em
      comentário.

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
