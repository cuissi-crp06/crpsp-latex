---
tipo: relato-upstream
destino: "Bob Tennent (rdt at cs.queensu.ca), mantenedor do pacote CTAN `atkinson`"
meio: e-mail (o pacote não tem issue tracker; o README dá só o endereço)
estado: "ENVIADO e RESPONDIDO em 2026-09-17. Bob Tennent reproduziu sob lualatex e encerrou o caso do lado dele; o relato segue para o Braille Institute. Ver 'Resposta do mantenedor'"
criado: 2026-09-17
mwe: neste arquivo, seção "Minimal example"
---

# Relato ao mantenedor do pacote `atkinson`

## Por que existe

Achado na sessão de 17/09/2026, ao escrever a `crpsp-relatorio` 0.2.0-alfa.
O `.otf` da Atkinson Hyperlegible Next que o pacote CTAN `atkinson` embarca
**não mapeia U+0060**, e com isso a convenção de aspas do TeX (`` '') falha
em silêncio para quem usa fontspec: o caractere é descartado antes do
processamento OpenType, a ligadura `tlig` não tem sobre o que operar, e o PDF
sai com glifo sem mapeamento Unicode — `U+FFFD` no texto extraído. Isso é
falha de acessibilidade: leitor de tela não tem o que ler, e o PDF/UA exige
mapeamento para todo caractere.

## O que foi verificado aqui, e o que não foi

**Verificado:**

- o `.otf` do pacote CTAN tem **347 codepoints**; outro build que declara a
  mesma versão interna 2.001 (o do pacote `atkinson-hyperlegible-next-fonts`
  2.100 do Fedora 44) tem **362**;
- os 15 a mais são U+0060 e os demais **acentos soltos** (`¨ ¯ ´ ¸ ˆ ˇ ˘ ˙ ˚
  ˛ ˜ ˝`), mais `Ĺ` e `ĺ`;
- **as métricas dos dois são idênticas** — largura de uma amostra de 430
  caracteres, altura-x e eme batem até a quinta casa, medidos no motor com
  kerning. Não é uma revisão de desenho;
- **o caminho `type1` não é afetado**: na T1 o slot 96 é `quoteleft`, e
  `\usepackage[type1]{atkinson}` com pdfLaTeX produz `“ ”` corretamente. É
  provavelmente por isso que ninguém notou.

**Não verificado:** qual dos dois builds é o que o Braille Institute publica
hoje. Os dois declaram `Version 2.001`; o do CTAN traz a string de build do
Glyphs (`Glyphs 3.2.3 (3260)`) e `UKWN` no uniqueID, o do Fedora não traz a
string e põe `NONE`. São exports diferentes do mesmo número de versão, e daqui
não dá para dizer qual é o oficial.

## Minimal example

Com o `.otf` do pacote fixado por `Path`, para isolar de outra cópia que a
máquina possa ter:

```latex
\documentclass{article}
\usepackage{fontspec}
\setmainfont{AtkinsonHyperlegibleNext}[
  Path = <TEXMFDIST>/fonts/opentype/public/atkinson/,
  UprightFont = AtkinsonHyperlegibleNext-Regular.otf,
  Ligatures = TeX,
]
\tracinglostchars=3
\begin{document}
Test: ``TeX quotes'' here.
\end{document}
```

**Observado:** dois avisos `Missing character: There is no ` (U+0060)`, e
`pdftotext` devolve `U+FFFD U+FFFD` no lugar de `U+201C`.
**Esperado:** `“TeX quotes”`, como sai com o outro build e como sai pelo
caminho `type1`.

⚠️ Sem o `Path`, o teste não reproduz numa máquina que tenha a fonte também
instalada no sistema: o luaotfload resolve pelo nome e pode pegar a outra
cópia. Foi assim que o defeito se escondeu aqui — `\usepackage[sfdefault]{atkinson}`
nesta máquina carrega a cópia do Fedora e funciona.

## Rascunho do e-mail

**Assunto:** `atkinson` package: bundled OTF lacks U+0060, breaking TeX quote
ligatures under fontspec

> Dear Bob Tennent,
>
> Thank you for maintaining the `atkinson` package. I am developing a set of
> LaTeX document classes for accessible PDF (PDF/UA-2) at a Brazilian
> professional council, and we are adopting Atkinson Hyperlegible Next as the
> text face of one of them. The work is still pre-release and nothing has been
> published with it yet, so I am afraid I cannot point you at a finished
> document — everything below comes from the development machine, and the
> minimal example reproduces it from scratch.
>
> I think I have found a problem with the bundled OpenType files, and I would
> be glad to be told I am wrong.
>
> The `AtkinsonHyperlegibleNext-*.otf` shipped in the package (TeX Live 2026,
> package dated 2026-01-16) do not map **U+0060 GRAVE ACCENT**. Under
> `fontspec` with `Ligatures=TeX`, the TeX quoting convention `` '' therefore
> fails: the character is dropped before OpenType processing, so the `tlig`
> ligature never fires, and the output PDF contains glyphs with no Unicode
> mapping — `pdftotext` returns U+FFFD. For documents targeting
> PDF/UA this is a conformance and accessibility problem rather than a
> cosmetic one, and it is silent: it produces only a `Missing character`
> warning, not an error.
>
> Minimal example (with `Path` set to the package's own font directory — from
> `kpsewhich --var-value TEXMFDIST` — to rule out another copy installed
> system-wide):
>
> ```latex
> \documentclass{article}
> \usepackage{fontspec}
> \setmainfont{AtkinsonHyperlegibleNext}[
>   Path = <TEXMFDIST>/fonts/opentype/public/atkinson/,
>   UprightFont = AtkinsonHyperlegibleNext-Regular.otf,
>   Ligatures = TeX,
> ]
> \tracinglostchars=3
> \begin{document}
> Test: ``TeX quotes'' here.
> \end{document}
> ```
>
> The `type1` route is not affected — in T1, slot 96 is `quoteleft`, so
> `\usepackage[type1]{atkinson}` under pdfLaTeX gives correct curly quotes.
> That may be why this has not come up before.
>
> For comparison, another build of the font declaring the same internal
> version (`Version 2.001`), shipped by Fedora 44 as
> `atkinson-hyperlegible-next-fonts-2.100`, does map U+0060. It has 362
> mapped codepoints against 347 in the CTAN copy; the 15 extra are U+0060 plus
> the other spacing diacritics (U+00A8, U+00AF, U+00B4, U+00B8, U+02C6,
> U+02C7, U+02D8, U+02D9, U+02DA, U+02DB, U+02DC, U+02DD) and U+0139/U+013A
> (L with acute). I compared the two in the engine: **the metrics are
> identical** — x-height and em agree exactly, and the width of a
> 430-character sample agrees to five decimal places (2297.41652pt in both) —
> so this looks like a difference between upstream
> exports rather than a design revision. The CTAN copy's version string
> carries a Glyphs build stamp (`Version 2.001;Glyphs 3.2.3 (3260)`, vendor
> code `UKWN` in the unique ID); the other has a plain version string and
> `NONE`. I could not determine from here which one Braille Institute
> currently publishes.
>
> If a newer upstream drop does include these glyphs, refreshing the bundled
> OTFs would fix it. If not, it is presumably worth raising with Braille
> Institute — a text face without U+0060 breaks the TeX convention for every
> Unicode-engine user.
>
> I am glad to test a candidate build on this machine, which has both copies
> installed, and to answer anything about the comparison — the full list of the
> fifteen codepoints is above.
>
> Best regards,
> Angelo Cuissi
> Conselho Regional de Psicologia de São Paulo (CRP-06)

## Revisões

**2026-09-17.** Duas frases prometiam o que não se pode cumprir, e saíram:

- *"we use Atkinson… and it has served us well"* — **não é verdade**. A linha
  está em `-alfa` e nenhuma publicação servida por ela circulou. O texto agora
  diz que o trabalho é pré-release e que **por isso** não há documento acabado
  para mostrar, o que responde à pergunta antes de ela ser feita.
- *"or to provide the comparison script"* — não existe script versionado para
  entregar. A comparação de cobertura foi feita com um analisador de `cmap`
  ad hoc, no scratchpad da sessão. Em lugar da oferta, o e-mail aponta para a
  lista dos quinze codepoints, que já está no corpo, e oferece o que a máquina
  de fato permite: **testar um build candidato**, já que ela tem as duas cópias
  instaladas.

Regra que fica: neste tipo de correspondência, só oferecer o que está pronto
para ser entregue no dia seguinte.

Na mesma releitura, três imprecisões:

- *"luaotfload's synthetic `tlig`"* — que a feature seja sintética do
  luaotfload é leitura de implementação, não coisa que eu tenha conferido. O
  que observei foi a ligadura não disparar, e é só isso que o texto diz agora.
- *"x-height, em, and the width … agree to five decimal places"* — só a largura
  da amostra tem cinco casas (2297,41652 pt); altura-x e eme o TeX imprime com
  menos. Agora está separado, e o número aparece.
- O `<TEXMFDIST>` do exemplo mínimo ganhou como obtê-lo
  (`kpsewhich --var-value TEXMFDIST`), para o exemplo ser copiável.

## Como o corpo chega ao e-mail

O texto acima é a fonte de verdade; o corpo do e-mail é derivado dele, não
mantido em paralelo. A conversão para texto puro, em 17/09/2026:

- sai a ênfase do Markdown (`**`), que em texto puro apareceria literal;
- **ficam as crases** de identificador técnico — é convenção corrente entre
  gente de TeX, e o destinatário é mantenedor de pacote;
- o exemplo mínimo perde a cerca de código e ganha indentação de quatro
  espaços, que é como se distingue código num e-mail em texto puro;
- tudo requebrado em 72 colunas.

O `<TEXMFDIST>` fica como marcador: a frase anterior diz como obtê-lo
(`kpsewhich --var-value TEXMFDIST`), e o caminho desta máquina não serviria
para o destinatário.

⚠️ **O endereço foi desofuscado.** O README do pacote escreve
"rdt **at** cs.queensu.ca", contra robôs; o rascunho foi para
`rdt@cs.queensu.ca`. É a única parte do endereço que não vem literal da fonte.

## Depois de enviar

Atualizar o `estado` no cabeçalho deste arquivo, com a data, e registrar a
resposta. Se a fonte for corrigida upstream, rever a §2b do `relatorio.sty` e
a §4b do `crpsp-base.sty`: a regra de escrita (aspas Unicode) continua valendo
de qualquer jeito, mas a sonda de glifos deixa de disparar.

## Resposta do mantenedor — 17/09/2026

Bob Tennent respondeu no mesmo dia. Em resumo: **reproduziu o defeito**, e
**encerrou o caso do lado dele**.

> After removing your Path setting which didn't work, I was able to produce
> `Missing character: There is no ` (U+0060) in font [AtkinsonHyperlegibleNext-Reg`
> using lualatex. But xelatex seemed to work fine. I suggest you contact the
> Braille Institute with your issue. I only provide pdflatex support and am
> not about to try debugging otf fonts.

Três coisas a tirar dali.

**1. O relato foi confirmado.** Ele viu o mesmo aviso, na mesma fonte, sob
lualatex — e sem o `Path`, ou seja, na cópia que a máquina *dele* resolve.
Isso é confirmação independente: não é artefato desta instalação.

**2. O `Path` não funcionou porque `<TEXMFDIST>` era um marcador.** O e-mail
explicava, na frase anterior, como obtê-lo (`kpsewhich --var-value TEXMFDIST`),
e ainda assim o destinatário colou o exemplo literal. ⚠️ **Regra que fica:**
em exemplo mínimo que vai para fora, nada de marcador a substituir — ou o
caminho vai resolvido, ou o `.otf` vai anexo. O leitor de um relato não é
obrigado a montar o teste.

**3. ⚠️ "But xelatex seemed to work fine" não inocenta a fonte — e essa é a
frase perigosa do e-mail dele.** Lida sem contexto, sugere defeito do
lualatex, e é exatamente a leitura que faria o Braille Institute arquivar o
caso. É falso, e foi medido aqui em 17/09:

| Motor | `Ligatures=TeX` | Aviso | Texto extraído |
| --- | --- | --- | --- |
| lualatex | sim | 2× `Missing character` U+0060 | `U+FFFD U+FFFD ... U+201D` |
| xelatex | sim | nenhum | `U+201C ... U+201D` |
| lualatex | **não** | 1× `Missing character` U+0060 | `U+FFFD` |
| xelatex | **não** | nenhum | `U+2018` |

A última linha é a que explica tudo. **Sem** `Ligatures=TeX`, uma crase crua
ainda sai como `‘` no xelatex. Não é ligadura: é o `mapping=tex-text` que o
fontspec põe na própria string de carga da fonte sob XeTeX — confirmado no
log:

```
AtkinsonHyperlegibleNext-Regular.otf]/OT:script=latn;language=dflt;mapping=tex-text;"
```

Esse mapeamento TECkit reescreve U+0060 → U+2018 **antes** da consulta à
fonte. A fonte nunca chega a ser perguntada pelo caractere que não tem. No
LuaTeX o `Ligatures=TeX` é a feature OpenType `tlig`, aplicada **dentro** da
fonte — e uma feature não opera sobre um caractere que o `cmap` não mapeia.

E não é diferença de *relato* de erro: o xelatex avisa normalmente quando o
caractere de fato falta. Com `\char"05D0` (א) no mesmo preâmbulo ele emite
`Missing character: There is no א (U+05D0)`. Só U+0060 passa — porque foi
substituído antes.

**Contraprova, no mesmo dia:** o build do Fedora, sob lualatex, com
`Ligatures=TeX`, dá **zero** avisos e extrai `U+201C ... U+201D`. Mesmo motor,
mesmo preâmbulo, só o `.otf` muda. Cobertura remedida sem `fontTools`, lendo
o `cmap` direto: CTAN **347** codepoints, Fedora **362**, e os 15 da diferença
são exatamente os já listados (U+0060, U+00A8, U+00AF, U+00B4, U+00B8,
U+0139, U+013A, U+02C6, U+02C7, U+02D8, U+02D9, U+02DA, U+02DB, U+02DC,
U+02DD). **Nenhum codepoint existe só no CTAN** — a cópia do CTAN é
subconjunto próprio da outra.

## Próximo passo: Braille Institute

O caminho agora é upstream, como o Bob sugeriu. O que a própria fonte declara
na tabela `name` do `.otf` do CTAN:

- fabricante: `Applied Design Works, Letters from Sweden`
- desenho: `Elliott Scott, Megan Eiswerth, Linus Boman, Theodore Petrosky, Letters from Sweden`
- URL do fornecedor e da licença: `https://www.BrailleInstitute.org/`

⚠️ **Não há endereço de contato na fonte nem no README do pacote** — só o
domínio institucional. O canal de envio (formulário, e-mail de tipografia,
repositório público) **ainda não foi verificado**: nenhuma consulta à web foi
feita nesta sessão. Levantar isso é o primeiro passo, antes de escrever.

Quando for escrito, o corpo muda de destinatário e por isso muda de ênfase:

- **abrir pela contraprova**, não pelo TeX: dois builds da mesma `Version
  2.001`, um com 362 codepoints e outro com 347, o segundo subconjunto do
  primeiro. O interlocutor é dono do desenho, não usuário de LaTeX;
- **nada de `<TEXMFDIST>`** — anexar o `.otf` em questão, ou dar o caminho
  do CTAN por URL;
- **antecipar a objeção do xelatex**, com a tabela acima em uma frase: o
  XeTeX substitui o caractere antes de consultar a fonte, então o sucesso
  dele não é evidência de que a fonte esteja completa;
- **enquadrar como acessibilidade**, que é o terreno deles: uma face
  desenhada para legibilidade produzindo, por essa lacuna, PDF sem
  mapeamento Unicode — o oposto do propósito da família;
- manter a regra de 17/09: **só oferecer o que está pronto**. A oferta que
  se sustenta continua sendo testar um build candidato, porque esta máquina
  tem as duas cópias instaladas.

**O que não muda em produção.** A `crpsp-relatorio` e a `crpsp-base` seguem
como estão: a regra de escrita é aspa Unicode literal (`“ ”`), que não passa
por U+0060 e portanto não depende deste desfecho. A sonda de glifos continua
sendo a rede de segurança. A revisão da §2b do `relatorio.sty` e da §4b do
`crpsp-base.sty` segue condicionada à correção upstream — que agora, pela
resposta do Bob, **não virá pelo pacote CTAN**.
