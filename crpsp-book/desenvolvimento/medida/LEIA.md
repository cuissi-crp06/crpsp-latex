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
