---
tipo: plano
dominio: editorial
projeto: crpsp-book
estado: aguardando-decisoes
criado: 2026-09-16
---

# Plano de retomada — linhas ativas (`relatorio`, `livro`, `formulario`)

Sessão de planejamento de 16/09/2026, feita sobre o
[briefing das classes livro e relatório](briefing-crpsp-livro-relatorio.md),
os três briefings marcados para arquivar, o `crpsp-book/ESTADO ATUAL.md`, a
`desenvolvimento/linha-base.tsv` e os `.cls`/`.sty` de `desenvolvimento/v2/`.
Nenhum código foi alterado.

## 1. Onde as coisas estão

O briefing de 16/09 trata `relatorio` e `livro` como trabalho a iniciar. Só
metade disso é verdade.

| Linha | Código hoje | O que o briefing decide | Distância real |
|---|---|---|---|
| `relatorio` | `crpsp-relatorio.cls` + `relatorio.sty` v0.1.0-alfa, implementada e migrada para `tagging=on` (29/07); `article`, A4, **11 pt**, `oneside`; tabelas já sem `tabularray`; primeiro uso no Jornal Psi | 12 pt, linha de 80 (ou 70–75), variantes `interno`/`externo`, decoração no alto e no pé | **Revisão**, não criação. Mudar 11→12 pt remexe a mancha e a paginação de uma publicação já entregue |
| `livro` (`manual`/`cartilha`) | Nada. Dois vizinhos: `book-crpsp_acessivel.sty` v0.5.2-beta (produção, A5) e a linha `guia` (`crpsp_acessivel.cls` + `guia-crpsp_acessivel.sty`, A5) | Classe nova sobre `book`, com `manual` A4 e `cartilha` A5 | Criação — falta dizer o que acontece com os dois vizinhos |
| `formulario` | `crpsp-formulario.cls` + `formulario.sty` implementadas; `exemplo-formulario.tex` **não declara `\DocumentMetadata`** — o tagging foi adiado para a fase 2 no briefing de 03/07 | "todas acessíveis" | A fase 2 do briefing do formulário **volta ao escopo**. É a única linha ativa que hoje não produz PDF/UA |

O cancelamento da `guia_visual` e a saída da `guia` encolhem a **pendência 1**
do `ESTADO ATUAL.md` (`testphase` → `tagging=on`) de cinco frentes para duas:
`formulario` e a linha `book`/`livro`. A **pendência 2** (`tabularray` em
`crpsp_acessivel.cls` e `crpsp-guia_visual.cls`) só sobrevive se a `cartilha`
for derivada do `crpsp_acessivel.cls`.

## 2. O que incorporar dos briefings arquivados

**Do briefing do formulário (03/07):**

- A máquina de **pré-medição** (`\settowidth`/`\widthof` + `\dimexpr`, registro
  em duas passagens no `camposlinha`) é o mesmo mecanismo que a "verificação de
  medida" do briefing novo pede. Reusar, não reinventar.
- A disciplina de API: **uma assinatura canônica documentada + aliases
  deprecados**, para migração incremental dos `.tex`.
- O `crpsp-base.sty` real tem três coisas (engine check, probe do fontspec,
  paleta). **Fontes com `\IfFontExistsTF` ainda não moram lá**; o briefing novo
  as coloca na base, e isso mexe na `relatorio`, que hoje faz o fallback por
  conta própria.

**Do briefing da camada `Leg` (10/07):** o `crpsp-leg.sty` é **código vivo**
(v0.3.0, sem minipages desde 13/07) e o briefing novo lista `leg` como módulo
opcional da `livro`. O que é arquivável são as fases 2 e 3 daquele briefing
(gerador `latexgen.py`, regeneração do Manual de DH), não a camada. Duas
decisões dele ficam **herdadas em aberto** pelo módulo `leg`:

- agrupadores (`cap`/`tit`/`sec`) entram na árvore de headings ou são
  parágrafos destacados?
- `\LegTitulo` continua como alias do `\LegEpigrafe`?

**Do briefing de acabamento do Manual de DH (11/07)** — três achados técnicos
que valem mais que o briefing inteiro:

- **Fundo de página decorativo:** `alt={}` não basta, e a chave `artifact` no
  `\includegraphics` serve para arte **no fluxo**. Para fundo de shipout o
  padrão verificado é `\tagstop` + `\tagmcbegin{artifact}` … `\tagmcend` +
  `\tagstart` (zero `<Figure>` na árvore, verificado com pikepdf). A decoração
  de margem do briefing novo é do primeiro tipo; `cartilha`/`manual` vão querer
  o segundo.
- **`veraPDF` UA-2 PASS como critério de aceitação de cada tarefa**, e
  `\hypersetup{pdftitle=…}` obrigatório (sem `dc:title` o veraPDF reprova). O
  briefing novo não menciona veraPDF — é um buraco no critério de aceitação.
- **Nunca invocar ambiente por csname** (`\description`…`\enddescription`) sob
  tagging: pula os hooks e corrompe `\hsize` na quebra de página. Regra dura
  para qualquer `.cls`/`.sty` novo.

## 3. Colisões a resolver antes de codar

1. **Paleta.** `relatorio`/`book` usam `crp1` = `#04586E` (azul); o
   `formulario.sty` usa `crp1` = `422C73` (roxo), com os mesmos nomes de alias.
   As duas linhas estão ativas e compartilham `crpsp-base`.
2. **11 pt → 12 pt no `relatorio`** invalida a paginação do relatório do Jornal
   Psi e parte da `linha-base.tsv`.
3. ~~**Luciole não está instalada** na imagem `crpsp-latex:dev`.~~
   **Resolvido em 17/09:** não está na imagem, mas está no TeX Live upstream do
   Fedora (v0.75), que é onde o `verificar.sh` roda. A imagem segue pendente
   para o WSL, não para a máquina de desenvolvimento.
4. ~~**NEWJUNE:** os `.OTF` não estão no repositório.~~ **Resolvido em 17/09:**
   não estão no repositório porque são proprietários, mas estão no workbench
   (`editorial/fonts/NewJune/`, 24 arquivos) e expostos por fontconfig desde
   13/09. A comparação foi feita: ver
   [`../desenvolvimento/medida/LEIA.md`](../desenvolvimento/medida/LEIA.md).
5. **Destino do `book-crpsp_acessivel.sty` e da linha `guia`** quando a
   `cartilha` existir.

## 4. Linha de ação

A ordem do briefing (cartilha → manual → relatorio → módulos → pandoc) supõe
que tudo depende da tipografia. Não depende.

**Fase 0 — terreno (nenhuma decisão pendente)**

1. Rodar `monitor_ctan.py` e `sh crpsp-book/desenvolvimento/verificar.sh` para
   **re-estabelecer a linha-base** antes de qualquer mudança (a atual é de
   13/09).
2. ~~Instalar `luciole` na imagem e fixar no `Containerfile`.~~ Continua
   valendo para a imagem, mas **não é pré-requisito**: o `verificar.sh` compila
   com o TeX Live nativo, não com podman, e lá a Luciole já está.
3. Fechar a **pendência 4** do `ESTADO ATUAL.md` (terceiro estado do
   `sec-template`: módulo ausente → aviso e formato padrão, ou erro claro). É o
   passo 1 do próprio briefing e não depende de tipografia.

**Fase 1 — a régua antes das margens**

4. Implementar a verificação de medida como módulo de `crpsp-base.sty`,
   reusando a pré-medição do `formulario`/`guia-visual`, e **confirmar em
   LuaLaTeX com kerning** as medidas que hoje vêm do fontTools — o briefing
   registra que o método subestimou a Lora em até 4%.

**Fase 2 — `formulario` fase 2, em paralelo** (independe da tipografia)

5. MWE primeiro: um `\TextField` sob `tagging=on` produz árvore válida? A
   resposta muda o que "formulário acessível" pode significar (talvez duas
   saídas: interativa e tagueada).

**Fase 3 — as classes**, na ordem do briefing (`cartilha` → `manual` → revisão
do `relatorio`), com a régua funcionando e as decisões da seção 5 travadas.

**Fase 4 — migração dos `.tex` de produção** e a limpeza listada no briefing do
formulário (duplicatas, `name=` colidido em `falta-atraso.tex:108,118`, stub
vazio de `isencao-viagem.tex`), com a regra dele: confirmar o nome canônico
antes de remover arquivo.

## 5. Decisões pendentes (destravam o resto)

- [ ] **Paleta institucional:** azul `#04586E` ou roxo `422C73` como `cor1` da
      base? `manual`/`cartilha` usam paleta fixa ou paleta por publicação?
- [x] ~~**NEWJUNE:** enviar os `.OTF`. Caminho crítico.~~ Nunca esteve
      bloqueado: os `.OTF` estão no workbench. Medido em 17/09 — e o resultado
      reabre a pergunta, porque a altura-x da NEWJUNE empata com a da Luciole.
- [ ] **Destino do `book-crpsp_acessivel.sty` e da linha `guia`** quando a
      `cartilha` existir.
- [ ] **Relatório:** 12 pt repaginando o Jornal Psi, ou o `relatorio` fica em
      11 pt e só as linhas novas vão a 12?
- [ ] Herdadas do briefing `Leg`: agrupadores como headings? `\LegTitulo` como
      alias?

~~As duas primeiras são o caminho crítico.~~ **Revisto em 17/09:** a segunda
nunca foi bloqueio, e a medida que dependia dela está feita. O caminho crítico
que resta é a **paleta**, e a decisão do `relatorio`, que agora tem número: o
mesmo conteúdo ocupa +37% de altura ao ir de 11/13,2 para 12/18, e +79% se
entrar também o espaço entre parágrafos do WCAG — dois custos separáveis. Pesa
a favor de subir: a Lora em 11 pt tem altura-x de 1,933 mm, **abaixo do mínimo
da RNIB**, então o `relatorio` de hoje já não cumpre o critério do sistema.

As fases 0 e 1 andam sem nenhuma decisão pendente — por isso estão primeiro. Em
17/09 a fase 0 andou: linha-base reconferida (idêntica, 22 linhas), CTAN
verificado, e a fase 1 ganhou a régua de medida em
`desenvolvimento/medida/`.
