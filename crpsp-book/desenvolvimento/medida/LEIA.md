---
tipo: medicao
dominio: editorial
projeto: crpsp-book
criado: 2026-09-17
---

# Medida — Lora, Luciole e NEWJUNE no motor

Substitui, com medidas do LuaLaTeX e com kerning, as estimativas de fontTools
do [briefing de 16/09](../../briefings/briefing-crpsp-livro-relatorio.md). O
próprio briefing pede essa confirmação: registra que o método antigo subestimou
a largura da Lora em até 4%.

## O que rodar

```sh
export PATH="$HOME/texlive/2026/bin/x86_64-linux:$PATH"   # o TeX Live do Fedora não serve
cd crpsp-book/desenvolvimento/medida
lualatex medir-fontes.tex      # -> medidas-fontes.tsv, medidas-mancha.tsv
lualatex especime-fontes.tex   # -> especime-fontes.pdf (11 páginas)
```

O `.pdf` é versionado de propósito: a máquina doméstica não compila (pendência C
do `ESTADO ATUAL.md`) e precisa poder abrir o espécime para julgar.

Esta pasta fica **fora** de `mwe/` e `v2/`. O `verificar.sh` sem argumentos varre
essas duas pastas (`verificar.sh:46`); um arquivo ali entraria na régua e
deixaria a `linha-base.tsv` desatualizada por efeito colateral. Conferido em
17/09: com a pasta criada, a régua segue idêntica à linha-base, 22 linhas.

## Método

- Altura-x por `\fontdimen5`, eme por `\fontdimen6`, altura de maiúscula por
  `\fontcharht\font`H` — métricas do motor, não do arquivo de fonte.
- Largura média por `\settowidth` sobre `amostra-pt.tex`, 430 caracteres de
  português institucional com os doze acentuados da língua, **com kerning e
  ligaduras**, dividida pelo número de caracteres **com espaços** (é assim que o
  WCAG e Bringhurst contam a linha cheia).
- A NEWJUNE é declarada por arquivo, não por nome: por nome o fontspec pode
  substituir a face em silêncio. A coluna `face` do TSV registra o que o motor
  carregou de fato — nas 13 medições, sempre o arquivo pedido.

⚠️ A amostra **não é** a do briefing, que mediu sobre 169 caracteres que não
estão no repositório. Os números de largura dele não são reproduzíveis; os
daqui são, e é para isso que `amostra-pt.tex` existe.

## Corpo de texto, 12 pt

| Fonte | Altura-x | x/eme | maiúsc./eme | x/maiúsc. | mm/car. | 80 car. | RNIB |
|---|---|---|---|---|---|---|---|
| Lora | 2,109 mm | 0,500 | 0,700 | 0,714 | 1,961 | 156,9 mm | mínimo |
| Luciole | 2,299 mm | 0,545 | 0,763 | 0,714 | 2,087 | 167,0 mm | mínimo |
| NEWJUNE Regular | 2,294 mm | 0,544 | 0,744 | 0,731 | 2,015 | 161,2 mm | mínimo |
| NEWJUNE Medium | 2,303 mm | 0,546 | 0,744 | 0,734 | 2,027 | 162,2 mm | **meta** |
| NEWJUNE Light | 2,294 mm | 0,544 | 0,744 | 0,731 | 1,958 | 156,6 mm | mínimo |

RNIB: meta 2,3 mm, mínimo 2,0 mm. Só a Medium cruza a meta, e por 0,003 mm — na
prática as três NEWJUNE e a Luciole empatam **na** meta, e a Lora fica atrás.

### O que se confirmou do briefing

Altura-x e x/eme da Lora (2,11 · 0,500) e da Luciole (2,30 · 0,545) bateram na
terceira casa. **As métricas verticais do fontTools estavam certas.** A largura
da Luciole sobre a Lora, que o briefing pôs em "cerca de 6%", deu **6,4%**.

### O que mudou

Os valores absolutos de largura subiram: a Lora de 1,94 para 1,961 mm/car. e a
Luciole de 2,05 para 2,087. Consequência direta na geometria — **80 caracteres
em Luciole pedem 167 mm de mancha, não os ~164 mm do briefing**. No A4 sobram
43 mm para as duas margens, não 46.

## O achado que reabre a premissa

O briefing supõe que a NEWJUNE é esbelta demais para corpo pequeno e que por
isso conflita com o critério de baixa visão, e propõe passar esses usos para a
Luciole. **Na altura-x isso não se sustenta:** NEWJUNE Regular tem 2,294 mm
contra 2,299 mm da Luciole — diferença de 0,2%, invisível. E a NEWJUNE é 3,5%
mais **estreita**, ou seja, entrega a mesma altura-x em menos linha.

O problema dos usos em corpo pequeno da linha `book` não é a fonte, é o corpo:

| Uso real | Onde | Corpo | Altura-x | RNIB |
|---|---|---|---|---|
| Cabeçalho `\Light\small` | `book:321-324` | 10,95 pt | 2,094 mm | mínimo |
| Título de caixa `\footnotesize` | `book:755` | 10 pt | 1,912 mm | **ABAIXO** |
| `CreditoInstitucional` `\scriptsize` | `book:738` | 8 pt | 1,530 mm | **ABAIXO** |

Trocar por Luciole nos mesmos corpos praticamente não muda nada — 2,097 mm,
1,915 mm e 1,532 mm. **A troca de fonte não resolve; só aumentar o corpo
resolve.** A decisão aberta "a NEWJUNE fica só em títulos grandes e a Luciole
assume os usos em corpo pequeno" resolveria um problema que a fonte não causa.

## Caracteres por linha, 12 pt

| Mancha | Lora | Luciole | NEWJUNE Reg. | Em disputa |
|---|---|---|---|---|
| 98,7 mm | 50 | 47 | 48 | `cartilha` A5 hoje |
| 105 mm | 53 | 50 | 52 | A5 alargada |
| 110 mm | 56 | 52 | 54 | A5 alargada |
| 144 mm | 73 | 68 | 71 | `manual` A4 |
| 164 mm | 83 | 78 | 81 | `relatorio` A4 |

Os 98,7 mm da `cartilha` de hoje batem com o briefing (Lora 50, Luciole 47
contra os 48 dele). Com o piso de 45 caracteres do A5, a mancha atual em Luciole
deixa **2 caracteres** de folga para conteúdo aninhado — apertado.

## O custo da repaginação, medido

Mesmo conteúdo, mesma mancha de 160 mm em A4, altura do bloco de corpo
(páginas 8 a 11 do espécime):

| Configuração | Altura | Sobre o estado atual |
|---|---|---|
| Lora 11/13,2, sem espaço entre parágrafos — **o `relatorio` hoje** | 128,7 pt | — |
| Lora 12/18, sem espaço entre parágrafos | 176,6 pt | **+37%** |
| Lora 12/18, com espaço WCAG entre parágrafos | 230,6 pt | **+79%** |
| Luciole 12/18, com espaço WCAG | 230,9 pt | +79% |

Duas leituras para a decisão do `relatorio`:

1. **O corpo e a entrelinha custam 37%; o espaço entre parágrafos custa outros
   31%.** São decisões separáveis. O WCAG 1.4.8 é critério AAA e pede as duas;
   adotar só a entrelinha já tira o texto do vermelho na altura-x sem dobrar o
   documento.
2. **A escolha de fonte é neutra na vertical** — Lora e Luciole diferem 0,1% em
   altura de bloco. O que a fonte muda é a horizontal: caracteres por linha.

E o dado que pressiona a decisão: **a Lora em 11 pt tem altura-x de 1,933 mm,
abaixo do mínimo de 2,0 mm da RNIB.** O `relatorio` de hoje, já entregue no
Jornal Psi, não cumpre o critério que o sistema adota.

## O que isto não decide

A escolha de fonte, de mancha e de corpo é do Angelo. Este arquivo entrega a
evidência; o espécime entrega o que o número não mostra — cor, textura e o
contraste entre título em NEWJUNE e texto em Luciole, que é a pergunta que abriu
a comparação.

---

# Análise sob os critérios de 17/09

Leitura das medidas depois das [decisões de
17/09](../../briefings/decisoes-2026-09-17.md). As tabelas de geometria estão
em [`geometria.md`](geometria.md), gerado por `geometria.py` a partir do TSV —
rodar de novo se as medidas mudarem.

Entrou na medição a **NEWJUNE Serif**, que estava na pasta de fontes sem ser
referenciada em lugar nenhum do repositório. Era a única candidata capaz de
preservar o contraste serifa/sem-serifa entre título e corpo.

## 1. O teto de caracteres deixou de ser a restrição

A decisão "a margem externa é sempre maior" morde bem antes dos tetos de
medida. Com margem interna de 15 mm na `cartilha` e 20 mm no `manual`:

| Classe | Teto decidido | Último caractere em que a externa ainda é maior que a interna | Faixa útil |
|---|---|---|---|
| `cartilha` A5 | 60 car. | Luciole **56** · NEWJUNE **58** · Lora 60 | ~45–55 car. |
| `manual` A4 | 80 car. | Luciole **81** · NEWJUNE **84** · Lora 86 | ~50–70 car. |

**Os 60 caracteres do A5 são inalcançáveis pelas fontes que passam no critério
de altura-x**: a Luciole estoura em 56 e a NEWJUNE em 58. Só a Lora chega aos
60 — e a Lora é justamente a que falha na altura-x. O teto de 60 e o critério
da decoração não cabem juntos.

Os 80 do manual passam, mas por pouco e sem folga real: a 80 caracteres sobram
23 mm de margem externa em Luciole, contra 20 mm de interna. Cumpre a letra do
critério e não cumpre o propósito — 23 mm não é espaço de artefato
decorativo.

**Na prática, quem escolhe o número de caracteres é o orçamento de decoração,
não o teto de legibilidade.** A faixa flexível de 45 a 80 do `manual` é real, e
o extremo de 45 caracteres dá 96 mm de margem externa: um formato de margem
larga, coerente com uma publicação ilustrada.

Vale notar o que a decisão sobre a `cartilha` já resolveu: sem `Leg` e sem
listas aninhadas, o piso de caracteres para conteúdo aninhado desaparece, e a
mancha passa a depender só da linha cheia. Uma restrição a menos.

## 2. Nenhuma serifada passa no critério de altura-x

| Fonte | Altura-x | x/eme | x/maiúsc. | RNIB |
|---|---|---|---|---|
| Luciole | 2,299 mm | 0,545 | 0,714 | mínimo, na meta por arredondamento |
| NEWJUNE Regular | 2,294 mm | 0,544 | 0,731 | idem |
| **NEWJUNE Serif** | **2,142 mm** | 0,508 | **0,683** | mínimo |
| Lora | 2,109 mm | 0,500 | 0,714 | mínimo |

A serifada institucional é melhor que a Lora, mas por pouco: 1,6% de altura-x a
mais, custando 2,3% de largura. Continua na faixa do mínimo, longe da meta de
2,3 mm. E tem a **menor razão x/maiúscula das quatro** (0,683) — minúsculas
pequenas em relação às maiúsculas, que é o oposto do que a baixa visão pede.

**Consequência para o `\serifada`:** a serifada institucional não pode carregar
bloco de texto sob o critério de acessibilidade adotado. O contraste de gênero
entre título e corpo, que o briefing lamentava perder, **não é recuperável por
essa via** — some de qualquer jeito, e o que resta decidir é qual sem-serifa
fica no corpo. O `\serifada` só pode ser face de destaque, e a correção do
apontamento (hoje `book:96` aponta para a `NEWJUNE-REGULAR.OTF`, que é a sem
serifa) passa a ser higiene, não decisão de sistema.

## 3. A disputa real: Luciole × NEWJUNE Regular

Empatam onde mais importa: **2,299 mm contra 2,294 mm de altura-x** — 0,2%,
invisível. Separam-se na largura, e a largura agora vale margem de decoração:

| | `cartilha` a 50 car. | `manual` a 65 car. |
|---|---|---|
| Luciole | 29 mm de margem externa | 54 mm |
| NEWJUNE Regular | **32 mm** | **59 mm** |

A NEWJUNE é 3,5% mais estreita e devolve 3 mm de margem na cartilha e 5 mm no
manual, com a mesma altura-x. Pelo critério da decoração, ela ganha.

O que pesa do outro lado não é métrica:

- **Licença e distribuição.** A NEWJUNE é proprietária: não vai para o
  repositório, não viaja com o pacote, e qualquer máquina nova precisa recebê-la
  à parte. A Luciole é CC BY 4.0, vem no TeX Live, e a atribuição no colofão
  resolve a obrigação.
- **Contraste.** A NEWJUNE é a fonte dos títulos. Usá-la também no corpo apaga
  qualquer distinção de família entre título e texto — sobra tamanho e peso. Com
  a Luciole no corpo, o contraste se mantém, agora entre duas sem-serifas
  diferentes em vez de entre serifa e sem-serifa.
- **Propósito.** A Luciole foi desenhada para baixa visão; a NEWJUNE, para
  identidade de marca. Num sistema que declara acessibilidade como critério, a
  procedência da fonte é argumento defensável para fora.

Os 3 a 5 mm de margem que a NEWJUNE devolve compram-se de outro jeito: tirando
dois ou três caracteres da linha. Em `cartilha` a 48 caracteres a Luciole dá 32
mm de margem externa — a mesma da NEWJUNE a 50. **A escolha é entre economizar
caracteres e economizar dependência.**

## 4. A entrelinha já está feita; o que falta é o espaço entre parágrafos

Medido no `\onehalfspacing` do setspace, em 12 pt: **17,99 pt**. O pacote
calibra por tamanho de fonte, não pela entrelinha simples — ou seja, o
`book-crpsp_acessivel.sty`, que já usa `\setasuspacing{\onehalfspacing}`
(linha 278), **já cumpre a entrelinha do WCAG**, e os 12/18 do espécime são
exatamente a configuração de hoje.

O que falta nas duas linhas é a outra metade do critério:

| Linha | Espaço entre parágrafos hoje | O WCAG 1.4.8 pede |
|---|---|---|
| `book` | `0.5\baselineskip` = 9 pt (`book:268`) | 1,5 × entrelinha = 27 pt |
| `relatorio` | `0.6\baselineskip` (`relatorio.sty:41`) | idem |

**Nenhuma das duas está perto**, e cumprir triplica esse espaço. É o que
explica os números medidos: sair do estado atual do `relatorio` (11 pt, entrelinha
simples) para 12/18 custa +37% de altura; acrescentar o espaço entre parágrafos
leva a +79%.

Os dois parâmetros também já combinam com o resto: o `book` usa
`\parindent = 0pt` (linha 269), que é a diagramação em bloco que o espaço entre
parágrafos exige — sem recuo, o espaço é o único separador.

## 5. O que estas medidas não decidem

- **Qual sem-serifa fica no corpo** — a análise mostra o que cada escolha custa,
  não qual custo vale mais.
- **Se o espaço entre parágrafos do WCAG entra.** É o parâmetro de maior efeito
  em número de páginas de todo o sistema, e a decisão "entrelinhamento
  obrigatório" não o alcança ao pé da letra.
- **O número de caracteres de cada classe**, que agora se lê como orçamento de
  margem: escolher a margem externa desejada e ler o número na tabela.

---

# Segunda rodada — 17/09, tarde

Entraram na medição a **Atkinson Hyperlegible Next** (Braille Institute, pacote
`atkinson` do TeX Live, família completa de sete pesos) e o teste das quatro
fontes sobre publicação real.

## A Atkinson tem altura-x menor que a Lora

| Fonte | Altura-x | x/eme | x/maiúsc. | mm/car. |
|---|---|---|---|---|
| Luciole | 2,299 mm | 0,545 | 0,714 | 2,0874 |
| NEWJUNE Regular | 2,294 mm | 0,544 | 0,731 | 2,0149 |
| NEWJUNE Serif | 2,142 mm | 0,508 | 0,683 | 2,0055 |
| Lora | 2,109 mm | 0,500 | 0,714 | 1,9611 |
| **Atkinson Next** | **2,092 mm** | **0,496** | 0,743 | **1,8778** |

Resultado contraintuitivo para uma fonte de acessibilidade, e confirmado com a
face declarada por arquivo (`AtkinsonHyperlegibleNext-Regular.otf`) — não é
substituição silenciosa. **A Atkinson busca legibilidade por diferenciação de
letra** (distinguir I/l/1, O/0, b/d) **e não por altura-x.** É também a mais
estreita das cinco: 10% mais estreita que a Luciole, o que devolve muita margem
externa ou muitos caracteres de linha.

Os dois critérios de acessibilidade não são o mesmo critério. A régua da RNIB
mede altura-x; a Atkinson otimiza outra coisa.

## O `\Huge` satura, e subir o corpo comprime a hierarquia

| Base | corpo | `\huge` | `\Huge` |
|---|---|---|---|
| 11 pt | 10,95 | 20,74 | 24,88 |
| 12 pt | 12 | 24,88 | **24,88** |
| variação | +9,6% | +20% | **0%** |

O `\Huge` das classes padrão vale 24,88 pt nas duas bases. O título de capítulo
do pacote book é `title-decls = \Huge`: ao subir o corpo para 12 pt, **o título
não cresce** e a razão título/corpo cai de 2,27× para 2,07×. O número do
capítulo, que é `\huge`, faz o oposto e cresce 20%.

Nenhuma das duas coisas é visível sem medir — a hierarquia comprime em silêncio.
A correção está em [`prototipo-tipografia.tex`](prototipo-tipografia.tex), com
os valores de 11 pt multiplicados por 12/10,95.

## A NEWJUNE Serif não tem negrito

Só existem `NEWJUNESERIF-REGULAR.OTF` e `NEWJUNESERIF-REGULAR-ITALIC.OTF`:
**dois cortes, sem negrito nem negrito itálico.** Para o teste foi usado
`AutoFakeBold`, que sintetiza o peso — serve para avaliar, não para produção.

Pesa contra usá-la em bloco de texto: qualquer `\textbf` no corpo, qualquer
termo em destaque, cai num negrito falso. Some-se a isso a altura-x de 2,142 mm,
na faixa do mínimo. Para chegar aos 2,3 mm da meta da RNIB ela precisaria de
**12,9 pt** de corpo.

## O teste das quatro sobre publicação real

Capítulo "Acessibilidade para pessoas com deficiência visual" do Guia de
Apresentações Acessíveis, com a mancha e o fundo decorativo reais. Todas em
12 pt, com o WCAG inteiro, NEWJUNE nos títulos e os títulos já corrigidos:

| Corpo | Páginas | Fatais | Erros de tagging |
|---|---|---|---|
| Lora | 5 | 0 | 0 |
| Luciole | 5 | 0 | 0 |
| NEWJUNE Serif | 5 | 0 | 0 |
| Atkinson Next | 5 | 0 | 0 |

**A escolha de fonte não muda a paginação deste capítulo** — as quatro dão 5
páginas. O que muda o número de páginas é o corpo e o espaço entre parágrafos,
não a família. A comparação fica sendo só de leitura e de contraste com o
título.

Os PDFs não estão aqui: são conteúdo de publicação e ficam no workbench.

## Alinhamento à esquerda — o item do 1.4.8 que passou

O WCAG 1.4.8 tem cinco itens. Adotamos a largura de linha e a entrelinha, e
**"texto não justificado" passou despercebido** na primeira leitura. A hifenação
saiu junto por decisão do Angelo.

**O `\RaggedRight` do ragged2e sozinho não resolve.** O esticamento padrão dele
à direita é finito (`0pt plus 2em`): serrilha menos a margem, mas conta com a
hifenação para fechar as linhas difíceis. Desligada a hifenação, as linhas
transbordam. Medido no capítulo de teste, antes da correção:

| Versão | Linhas transbordando | Maior transbordo |
|---|---|---|
| Lora | 9 | 17,7 pt |
| Luciole | 9 | 12,0 pt |
| NEWJUNE Serif | 8 | 14,2 pt |
| Atkinson | 3 | 9,2 pt |

Uma delas chegou a 24 pt — 8 mm de texto dentro da margem, e numa publicação com
decoração de margem isso é colisão, não só feiura. A Atkinson transborda menos
por ser a mais estreita.

Com `\RaggedRightRightskip` em `0pt plus 1fil` não há transbordo possível por
espacejamento: a linha simplesmente termina mais cedo, que é o que o alinhamento
à esquerda quer dizer. Depois da correção, nas quatro versões:

| | Páginas | Fatais | Erros de tagging | Transbordo | Hifens no fim de linha |
|---|---|---|---|---|---|
| todas as quatro | 5 | 0 | 0 | **0** | **0** |

A mudança de alinhamento **não mexeu na paginação**: as quatro continuam em 5
páginas.
