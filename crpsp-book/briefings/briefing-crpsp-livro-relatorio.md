# Briefing — Classes livro e relatório, medida e tipografia

**Data:** 2026-09-16  
**Contexto:** sistema editorial LaTeX do CRP-SP — linhas `livro` e `relatorio` da v2

## Contexto e princípio

As classes LaTeX do CRP-SP servem à produção editorial rápida e simples e criam um limite: não invadem o espaço dos designers. A classe cuida de estrutura, medida e acessibilidade; o acabamento visual fica com os designers. As razões declaradas são interoperabilidade e permitir que as peças feitas por designers sejam mais bem acabadas e atraentes.

Repositório de acompanhamento: `cuissi-crp06/crpsp-latex` (main em `5d4a124`). Este briefing registra as decisões da sessão de 16/09/2026 e as medições que as sustentam.

## Decisões tomadas

| Tema | Decisão |
| --- | --- |
| Classes | `crpsp-livro.cls` com `manual` (A4) e `cartilha` (A5); `crpsp-relatorio.cls` separada, sobre `article`, com `interno` e `externo` |
| Base comum | O que é comum sobe para `crpsp-base.sty`; `crpsp-base.cls` descartada (uma classe só chama `\LoadClass` uma vez; conflito de nome com o `.sty`) |
| Medida A4 | Máximo de 80 caracteres por linha cheia; 60 como piso para conteúdo aninhado (listas, incisos) |
| Medida A5 | Máximo de 60 caracteres por linha cheia; 45 como piso para conteúdo aninhado |
| Corpo | 12 pt em todas as classes |
| Entrelinha | Adequada ao WCAG (1.4.8: entrelinha ≥ 1,5; espaço entre parágrafos ≥ 1,5 × entrelinha) |
| Ilustração | `manual` e `cartilha` nas margens externas; `relatorio` nas margens superior e inferior |
| `relatorio` | Sem notas marginais (layout de Tufte descartado); tabelas cabem na mancha; paleta institucional fixa |
| `relatorio`, variantes | `interno` (padrão, sem decoração, formal) e `externo` (divulgação: relatório de gestão e gêneros afins) |
| `cartilha` | Sem a camada Leg |
| Fonte de texto | Luciole em todas as classes, condicionada à comparação com a NEWJUNE |

Decoração de margem sai marcada com a chave `artifact` (o `alt={}` não marca artefato desde agosto, WA-10). O `relatorio-gestao.sty` (memoir) é o antecessor de referência da variante `externo`.

## Medições

Em 12 pt, a Luciole é cerca de 6% mais larga que a Lora e tem altura-x de 2,30 mm, a meta da RNIB. Medição com fontTools sobre uma amostra de 169 caracteres em português, com acentos, sem kerning. Na Lora, esse método subestimou a largura em até 4% frente ao LuaLaTeX.

| Corpo 12 pt | Lora | Luciole |
| --- | --- | --- |
| mm por caractere | 1,94 | 2,05 |
| Altura-x | 2,11 mm | 2,30 mm |
| Altura-x / eme | 0,500 | 0,545 |
| Altura-x / maiúscula | 0,71 | 0,71 |
| 80 car. (teto A4) | \~155 mm | \~164 mm |
| 60 car. (teto A5; piso A4) | \~116 mm | \~123 mm |
| 45 car. (piso A5) | \~87 mm | \~92 mm |
| Mancha atual do `book` A5 (98,7 mm) | 50 car. | 48 car. |

Referências da RNIB: altura-x de 2,3 mm como meta e 2 mm como mínimo. A Lora em 12 pt passa o mínimo, mas fica abaixo da meta.

## Consequências por classe

Os números abaixo usam a Luciole em 12 pt. Com a Lora, as sobras aumentam cerca de 8 mm no A4 e 6 mm no A5.

| Classe | Linha cheia | Mancha | Sobra p/ margens | Recuo até o piso |
| --- | --- | --- | --- | --- |
| `relatorio` (A4) | 80 car. | \~164 mm | \~46 mm (\~23 por lado) | \~41 mm |
| `manual` (A4) | \~70 car. | \~144 mm | \~66 mm | \~21 mm |
| `cartilha` (A5), mancha atual | 48 car. | 98,7 mm | \~49 mm | \~6 mm |
| `cartilha` (A5), mancha alargada | 51–53 car. | 105–110 mm | 38–43 mm | 13–18 mm |

- **`relatorio`.** A linha de 80 caracteres deixa margens laterais menores que as "margens grandes" desejadas. Reduzir para 70–75 caracteres devolve margem. A decoração no alto e no pé divide espaço com cabeçalho e número de página; falta definir o comportamento nas páginas em paisagem.
- **`manual`.** Com 80 caracteres, a coluna externa fica estreita demais para ilustração. Com \~70, cabe, por exemplo, 20 mm na interna e \~46 mm na externa.
- **`cartilha`.** Os 60 caracteres deixam só \~25 mm para as duas margens, incompatível com ilustração externa. Sem a camada Leg, o recuo serve só a listas; a mancha atual comporta um nível raso.
- **Altura da página.** Entrelinha de 18 pt (\~6,35 mm) reduz linhas por página: cerca de 25 num A5 com 160 mm de mancha vertical. O número de páginas das publicações atuais muda.

## Tipografia: Luciole e NEWJUNE

A adoção da Luciole em todas as classes depende de avaliar o contraste com a NEWJUNE, esbelta, frente à Luciole, mais larga. Com a troca, some o contraste de gênero que existe hoje (Lora com serifa, NEWJUNE sem serifa); restam largura, peso e proporção.

**Luciole.** Desenvolvida para pessoas com deficiência visual pelo Centre Technique Régional pour la Déficience Visuelle e pelo estúdio typographies.fr ([luciole-vision.com](https://luciole-vision.com/)). Quatro estilos: regular, negrito, itálico e negrito itálico. Fontes de texto sob CC BY 4.0, que exige atribuição; a Luciole Math sai sob OFL. Pacote `luciole` no CTAN, v0.75, incluído no TeX Live e no MiKTeX ([CTAN](https://ctan.org/pkg/luciole)). Não traz `luciole.sty` para `\usepackage`: entrega os quatro `.ttf` de texto, o `Luciole.fontspec` e o `luciole-math.sty` — em texto, o uso é por fontspec. **Instalada** no TeX Live upstream do Fedora (ver errata de 17/09).

**NEWJUNE hoje no `book`.** Os `.OTF` não estão no repositório; o pacote os referencia por nome, sem `Path`.

| Uso | Onde | Leitura |
| --- | --- | --- |
| Títulos grandes | `\Huge`, `\huge`, `\Large` com `\bfseries\sffamily` | Contraste esbelta × larga tende a funcionar; o tamanho compensa |
| Cabeçalhos | `\Light\small` (linhas 321–324) | Estreita e leve em corpo pequeno; conflita com o critério de baixa visão |
| Bloco em corpo pequeno | `\sffamily\scriptsize` (linha 738) | Idem |
| Títulos de caixa | `\sffamily\footnotesize\bfseries` (linha 755) | Idem |
| Seis famílias extras | `\media`, `\fininha`, `\Light`, `\fontebook`, `\serifada`, `\pesada` | Acabamento; espaço dos designers |

**Comparação a fazer**, quando os `.OTF` (Regular, Bold, Light, Medium) estiverem disponíveis:

| Métrica | Luciole | NEWJUNE |
| --- | --- | --- |
| Altura-x / eme | 0,545 | a medir |
| Altura de maiúscula / eme | 0,763 | a medir |
| Altura-x / maiúscula | 0,71 | a medir |
| Largura média (amostra PT) | \~0,49 eme | a medir |
| Pesos | 400 e 700 | ≥ 7 famílias |

O espécime em LuaLaTeX deve mostrar três situações reais: título de capítulo sobre parágrafo, título de caixa em `\footnotesize` e cabeçalho em corpo pequeno. No texto corrido, a troca não perde pesos: o `\setmainfont` do `book` declara só os quatro estilos básicos da Lora.

## Implementação

O comum às classes mora em `crpsp-base.sty`: fontes com `\IfFontExistsTF`, verificação de medida e tabelas acessíveis. A verificação de medida passa a ler a faixa conforme o papel.

**Verificação de medida.** Em LuaLaTeX, no `\begin{document}`:

1. Medir uma amostra em português, com acentos, na fonte e no corpo correntes (o método do memoir mede só o alfabeto minúsculo e fixa 45 e 65).
2. Registrar no log os caracteres por linha de `\textwidth`.
3. Medir também a largura útil no nível mais profundo de `enumitem` e, onde houver, no recuo da camada Leg.
4. Avisar quando a linha cheia passar do teto (80 no A4, 60 no A5) ou o conteúdo aninhado ficar abaixo do piso (60 no A4, 45 no A5).
5. Registrar a altura-x efetiva contra 2 mm (mínimo) e 2,3 mm (meta).

Os resultados entram como colunas na `verificar.sh`.

**Ordem de desenvolvimento** (definida antes nesta sessão; ainda não executada):

1. Esqueleto de `crpsp-livro.cls` com `cartilha`, implementação num `livro.sty`; exemplo já com `tagging=on` (pendência 1) e correção do terceiro estado do `sec-template` (pendência 4). Teste: reescrever `mwe_acessivel_book` para a classe, comparando a árvore de tags.
2. `manual`, com geometria parametrizada por papel.
3. `relatorio`: variantes `interno`/`externo`, paleta travada, tabelas portadas de `relatorio.sty` sem `tabularray` (pendência 2).
4. Módulos opcionais: `leg` (fora da `cartilha`), `creditos`, `svg`.
   O `creditos` tem especificação própria desde 17/09: ver
   [`funcionalidade-creditos-institucionais.md`](funcionalidade-creditos-institucionais.md)
   — recupera Plenário, Diretoria e comissões do pipeline de normativas,
   com nominata atual por padrão e composição por data.
5. Template pandoc e filtros Lua, testados com publicação real.
6. Exemplos da classe na `verificar.sh` desde o passo 1.

## Pendências e decisões abertas

- [ ] Comparar Luciole e NEWJUNE (métricas e espécime); depende do envio dos `.OTF`.
- [ ] Decidir se a NEWJUNE fica só em títulos grandes e a Luciole assume os usos em corpo pequeno.
- [ ] Qual é a cor institucional (azul `crp1` do `book` × roxo `422C73` do `formulario`).
- [ ] `manual` e `cartilha`: paleta institucional fixa ou paleta da publicação.
- [ ] Linha cheia do `relatorio`: 80 caracteres ou 70–75, para margens maiores.
- [ ] Linha cheia do `manual`: \~70 caracteres ou outro valor abaixo do teto.
- [ ] Mancha da `cartilha`: manter 98,7 mm ou alargar para 105–110 mm.
- [ ] Decoração superior e inferior do `relatorio` em páginas em paisagem.
- [ ] Crédito da Luciole (CC BY 4.0) no colofão, possivelmente automático.
- [ ] Confirmar as medidas em LuaLaTeX com kerning antes de fixar margens.
- [ ] Conferir os recuos do `crpsp-leg.sty` contra o piso de 60 caracteres no `manual`.
- [ ] Núcleo × módulos (`leg`, `creditos`, `svg`); opções mutuamente exclusivas: erro se combinadas e qual é o padrão.
- [ ] Aplicação do eMAG a conselho profissional (não localizado na verificação).

Divergências registradas no `book-crpsp_acessivel.sty`: o comentário calcula `bottom` em 46,667 mm, mas o código usa 30 mm; outro comentário cita `titlesec`, que o código já não usa (WA-03).

## Fontes verificadas e afirmações descartadas

As referências abaixo foram conferidas por busca durante a sessão; as URLs completas das verificações anteriores estão no transcrito da sessão.

**Aproveitáveis para a medida.** Bringhurst (45–75 caracteres); Dyson e Haselgrove (\~55 em tela); Tinker; Rello e Baeza-Yates; Wery e Diliberto; WCAG 1.4.8 (AAA: até 80 caracteres, entrelinha ≥ 1,5) e 1.4.12. Nenhuma contradiz as faixas adotadas. O WCAG foi escrito para conteúdo web; aplicá-lo a PDF de layout fixo é adoção por analogia.

**RNIB.** 12 pt como meta para leitores em geral; 14 pt como mínimo para pessoas com baixa visão; recomenda medir altura-x (2,3 mm; mínimo 2 mm).

**Descartadas do relatório do Gemini:**

| Afirmação | Situação |
| --- | --- |
| Legge (1985), mínimo de 13 caracteres | O artigo trata de ganho de velocidade até 4 caracteres, com texto rolando em monitor |
| Zebrado "confirmado" por eye-tracking (Enders, 2008) | A autora relata pouca evidência e ganho pequeno |
| WCAG 1.4.10 exige reflow de tabelas | O critério isenta conteúdo bidimensional, como tabelas de dados |
| Bachmann (2008), *Body Consciousness* | O livro é de Richard Shusterman, sem relação com alinhamento |
| eMAG 3.1 sobre texto justificado | Não localizado |

Sem conferência: Abubaker e Lu (2012), Karatay e Unal (2023), Galiano et al., regra alfabeto × 1,75 e "16–18 pt" para CPS.

**Luciole:** [luciole-vision.com](https://luciole-vision.com/) · [CTAN, pacote luciole](https://ctan.org/pkg/luciole).

## Errata — 17/09/2026

Este briefing foi escrito no **WSL doméstico**, a máquina que a pendência C do
`ESTADO ATUAL.md` registra como incapaz de compilar. Três afirmações de
ambiente descrevem os limites daquela máquina, não os do projeto. Conferido no
Fedora, que é a máquina de desenvolvimento desde 13/09:

| Afirmação | Situação real |
|---|---|
| "Luciole… não está instalada no ambiente de teste" | Instalada, v0.75, no TeX Live upstream. E o pacote não tem `.sty` de texto |
| Os `.OTF` da NEWJUNE não estão disponíveis | Os 24 `.OTF` estão em `editorial/fonts/NewJune/`, ligados a `~/.local/share/fonts/crpsp` desde 13/09 |

**A comparação Luciole × NEWJUNE, que o plano tratava como caminho crítico, não
estava bloqueada.** Foi feita em 17/09 e está em
[`../desenvolvimento/medida/LEIA.md`](../desenvolvimento/medida/LEIA.md), com a
sonda que a produziu e o espécime.

O que a medição no motor devolveu a este briefing:

- **As métricas verticais do fontTools estavam certas** — altura-x e x/eme da
  Lora e da Luciole bateram na terceira casa.
- **As de largura, não.** 80 caracteres em Luciole pedem **167 mm** de mancha,
  não os ~164 mm da tabela de "Consequências por classe": sobram 43 mm para as
  duas margens do A4, não 46.
- **A premissa da seção "Tipografia" cai.** A altura-x da NEWJUNE Regular é
  2,294 mm contra 2,299 mm da Luciole, e a NEWJUNE é 3,5% mais estreita. O que
  falha no critério de baixa visão não é a fonte: é o corpo. `\footnotesize`
  (10 pt) dá 1,912 mm e `\scriptsize` (8 pt) dá 1,530 mm, ambos abaixo do
  mínimo de 2,0 mm da RNIB — e em Luciole dariam 1,915 mm e 1,532 mm. A
  pendência "decidir se a NEWJUNE fica só em títulos grandes e a Luciole assume
  os usos em corpo pequeno" resolveria um problema que a fonte não causa.
- **O espécime que a seção pede está feito**, com as três situações reais.
