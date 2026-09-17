---
tipo: relato-upstream
destino: "Bob Tennent (rdt at cs.queensu.ca), mantenedor do pacote CTAN `atkinson`"
meio: e-mail (o pacote não tem issue tracker; o README dá só o endereço)
estado: "RASCUNHO — aguarda leitura e envio pelo Angelo. Revisto em 2026-09-17: ver 'Revisões'"
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

## Depois de enviar

Atualizar o `estado` no cabeçalho deste arquivo, com a data, e registrar a
resposta. Se a fonte for corrigida upstream, rever a §2b do `relatorio.sty` e
a §4b do `crpsp-base.sty`: a regra de escrita (aspas Unicode) continua valendo
de qualquer jeito, mas a sonda de glifos deixa de disparar.
