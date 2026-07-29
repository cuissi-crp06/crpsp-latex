# Briefing: `crpsp-guia_visual.cls`
**Para:** Claude Code  
**Contexto:** Sistema editorial LaTeX do CRP-SP  
**Engine obrigatória:** LuaLaTeX  
**Data:** 2026-06-24  

---

## 1. Objetivo

Criar a classe `crpsp-guia_visual.cls` para publicações em formato 16:9 (guias visuais, apresentações institucionais em PDF). A classe é **separada** de `crpsp_acessivel.cls`, mas compartilha infraestrutura comum que será **extraída** para um novo pacote `crpsp-base.sty`.

Isso implica **refatoração dos arquivos existentes**, não apenas criação de arquivo novo.

---

## 2. Inventário de arquivos de entrada

Os dois arquivos abaixo são **entrada** do processo — lê-los antes de escrever qualquer código:

| Arquivo | Papel |
|---|---|
| `crpsp_acessivel.cls` | Classe existente a ser refatorada |
| `guia-crpsp_acessivel.sty` | STY existente (linha A5, referência de padrões) |

---

## 3. Arquivos a produzir

```
crpsp-base.sty            ← NOVO: infraestrutura compartilhada
crpsp_acessivel.cls       ← REFATORADO: carrega crpsp-base.sty
crpsp-guia_visual.cls     ← NOVO: classe principal 16:9
guia-visual.sty           ← NOVO: implementação de layout, navbar, frames
exemplo-guia-visual.tex   ← NOVO: documento de teste mínimo
```

---

## 4. Arquitetura de dependências

```
crpsp-base.sty
  ├── verificação de engine (LuaLaTeX)
  ├── sistema de cores (cor1/cor2/cor3 + setters)
  └── detecção e carga de fontspec/luaotfload

crpsp_acessivel.cls
  └── \RequirePackage{crpsp-base}   ← substitui o bloco equivalente atual

crpsp-guia_visual.cls
  ├── \RequirePackage{crpsp-base}
  ├── base: article (NÃO book — sem frontmatter/mainmatter/backmatter)
  └── \RequirePackage{guia-visual}

guia-visual.sty
  ├── geometria 16:9
  ├── tipografia (mesma cadeia de fallback do guia A5)
  ├── sistema de frames
  ├── grid de três colunas
  ├── barra de navegação
  └── conformidade PDF/UA-2
```

---

## 5. Extração para `crpsp-base.sty`

Mover de `crpsp_acessivel.cls` para `crpsp-base.sty` exatamente estes blocos:

1. **Verificação de engine** (bloco `% 0.`) — erro se não for LuaLaTeX  
2. **Sistema de cores** (bloco `% 4.`) — `crpsp@cor1/2/3`, aliases públicos `cor1/2/3`, comandos `\crpspCorPrincipal`, `\crpspCorSecundaria`, `\crpspCorAcessoria`  
3. **Detecção e carga de fontspec** (bloco no `% 3.`) — flag `\ifcrpsp@fontspec`, probe Lua, `\RequirePackage{fontspec}` ou fallback `fontenc`

Após extração, `crpsp_acessivel.cls` deve fazer `\RequirePackage{crpsp-base}` no lugar desses blocos. Comportamento externo inalterado — isto é refactoring, não mudança de API.

---

## 6. Geometria 16:9

```latex
\geometry{
  paperwidth  = 338.67mm,   % padrão widescreen (PowerPoint/Impress)
  paperheight = 190.5mm,
  top         = 18mm,       % reserva para navbar + margem
  bottom      = 10mm,
  left        = 12mm,
  right       = 12mm,
  footskip    = 7mm,
}
```

A navbar ocupa os primeiros ~12mm do topo da área de texto. A geometria deve deixar espaço para ela sem comprimir o conteúdo.

---

## 7. Sistema de frames (modelo semântico)

O documento é **híbrido**: seções agrupam frames, mas não há fluxo de texto entre páginas. Cada frame é uma unidade de layout autônoma.

### 7.1 Comandos do autor

```latex
% Preâmbulo
\documentclass{crpsp-guia_visual}
\crpspCorPrincipal{004A8F}
\crpspCorSecundaria{E8452A}

\begin{document}

\section[Apresentação]{Apresentação institucional do CRP-SP}
% argumento opcional = título curto para a navbar
% argumento obrigatório = título longo (disponível para sumário futuro)
% se [Curto] omitido, o título longo é usado na navbar também

\begin{frame}
  \begin{colunas}
    \coluna[span=2]{%
      Conteúdo principal — ocupa 2/3 da largura
    }
    \coluna[span=1]{%
      \includegraphics[alt={Descrição da imagem}]{imagem.pdf}%
    }
  \end{colunas}
\end{frame}

\begin{frame}[layout=full]   % frame sem colunas, largura total
  \includegraphics[width=\linewidth, alt={Foto panorâmica}]{panorama.pdf}%
\end{frame}

\section[Resultados]{Resultados e indicadores 2025}

\begin{frame}
  \begin{colunas}
    \coluna[span=1]{Coluna 1}
    \coluna[span=1]{Coluna 2}
    \coluna[span=1]{Coluna 3}
  \end{colunas}
\end{frame}

\end{document}
```

### 7.2 Regras do grid

- O grid é de **3 colunas iguais** (cada uma = `(\linewidth - 2\guia@colgap) / 3`)
- `\coluna[span=N]` onde N ∈ {1, 2, 3}
- A soma dos spans dentro de `\begin{colunas}` deve ser 3; se diferente, emitir `\ClassWarning`
- `layout=full` no frame desativa o grid e deixa `\linewidth` disponível
- Implementar com **tcolorbox em minipages** (ver seção 10 sobre acessibilidade)

### 7.3 Opções do ambiente `frame`

| Opção | Efeito |
|---|---|
| `layout=colunas` | padrão — ativa grid de 3 colunas |
| `layout=full` | largura total, sem colunas |
| `bg=<arquivo>` | background PDF/imagem na página (`eso-pic`) |

---

## 8. Barra de navegação

### 8.1 Referência visual

Ver `PRPer_BNDES_Rel_Anual_Integrado_2025-6.pdf`, página 6:
- Faixa horizontal no topo da página
- Seções listadas da esquerda para direita
- Seção corrente: destaque visual (fundo escuro, texto claro)
- Seções inativas: texto sobre fundo claro/neutro
- Separadores verticais entre seções
- Número de página no canto direito

### 8.2 Mecanismo de inferência automática

A navbar sabe qual seção está ativa por inferência automática. Isso exige **duas passagens de compilação**. Adotar o mesmo padrão do Beamer: **stream `.nav` dedicado**, separado do `.aux`.

**Por que `.nav` e não `.aux`:** o `.aux` é compartilhado por vários sistemas (`hyperref`, `toc`, `label`/`ref`). Um stream dedicado isola os dados de navegação, evita interações e torna o mecanismo legível.

**Abertura do stream (no preâmbulo do STY):**
```latex
\newwrite\guia@navstream
\AtBeginDocument{%
  \openout\guia@navstream=\jobname.nav\relax
}
\AtEndDocument{%
  \closeout\guia@navstream
}
```

**Primeira passagem — gravação a cada `\section`:**
```latex
% dentro da redefinição de \section:
\write\guia@navstream{%
  \string\guia@navitem
    {\the\c@navsec}%   índice
    {<título curto>}%  ver seção 9
    {\thepage}%        página de início
}
```

**Segunda passagem — leitura no início do documento:**
```latex
\AtBeginDocument{%
  \IfFileExists{\jobname.nav}{%
    \@input{\jobname.nav}%   executa os \guia@navitem gravados
  }{%
    \ClassWarning{guia-visual}{%
      Arquivo .nav nao encontrado. Execute lualatex duas vezes\MessageBreak
      para que a barra de navegacao seja renderizada corretamente.%
    }%
  }%
}
```

**Definição de `\guia@navitem`** (executada na segunda passagem):
```latex
% acumula os dados em listas paralelas via etoolbox
\newcommand{\guia@navitem}[3]{%
  % #1 = índice, #2 = título curto, #3 = página de início
  \listgadd{\guia@navtitulos}{#2}%
  \listgadd{\guia@navpaginas}{#3}%
}
```

**Inferência de seção corrente no cabeçalho:**
O cabeçalho percorre `\guia@navpaginas` e determina qual seção abrange `\thepage` por comparação numérica. A seção ativa é a última cujo número de página de início seja ≤ `\thepage`.

**Aviso de overflow:** após carregar o `.nav`, estimar a largura total da navbar somando `\widthof{<título>}` de cada item mais separadores. Se exceder `\paperwidth`, emitir:
```
\ClassWarning{guia-visual}{Navbar pode transbordar: soma dos titulos excede a largura do papel.
Use \section[Curto]{Longo} para abreviar os itens da barra.}
```

### 8.3 Renderização com TikZ

```latex
% Estrutura lógica do cabeçalho (a implementar em fancyhdr + TikZ)
\fancyhead[C]{%
  \begin{tikzpicture}[remember picture, overlay]
    % faixa de fundo
    \fill[cor1] (0,0) rectangle (\paperwidth, \guia@navheight);
    % itens de seção
    \foreach \i/\titulo in {<lista de seções>} {
      \ifnum\i=\guia@cursec
        % item ativo
        \fill[white] ...
        \node[text=cor1, ...] {\titulo};
      \else
        % item inativo
        \node[text=white, ...] {\titulo};
      \fi
    }
    % número de página
    \node[anchor=east, text=white] at (\paperwidth-3mm, ...) {\thepage};
  \end{tikzpicture}%
}
```

Pacotes necessários: `tikz`, `fancyhdr`, `etoolbox`.

---

## 9. Redefinição de `\section`

`\section` na nova classe deve aceitar argumento opcional — sintaxe idêntica à do Beamer:

```latex
\section[Título curto]{Título longo completo}
```

Comportamento:
- **Argumento opcional presente:** usar o argumento curto na navbar; o longo fica disponível para sumário futuro
- **Argumento opcional ausente:** usar o título longo em ambos os contextos

Ações que `\section` deve executar:

1. **Iniciar nova página** (`\clearpage`) — frames de seções diferentes não coexistem na mesma página
2. **Incrementar** `\c@navsec`
3. **Gravar no stream `.nav`** o título curto e o número de página de início (ver seção 8.2)
4. **Atualizar** o contador de seção corrente (`\guia@cursec`)
5. **NÃO** produzir o título como elemento visual na página — a seção é comunicada pela navbar, não por cabeçalho no corpo

Implementação com `\RenewDocumentCommand` (xparse/LaTeX3):

```latex
\RenewDocumentCommand{\section}{o m}{%
  \clearpage
  \stepcounter{navsec}%
  \IfNoValueTF{#1}{%
    \def\guia@sec@curto{#2}%   sem argumento curto: usar longo
  }{%
    \def\guia@sec@curto{#1}%   argumento curto fornecido
  }%
  \write\guia@navstream{%
    \string\guia@navitem{\the\c@navsec}{\guia@sec@curto}{\thepage}%
  }%
  \setcounter{guia@cursec}{\value{navsec}}%
}
```

> ⚠️ Não chamar `\addcontentsline{toc}{...}` por padrão. Disponibilizar opção `toc=true` no preâmbulo se necessário.

---

## 10. Conformidade PDF/UA-2 — três colunas

### 10.1 Restrição crítica

**Não usar `multicol` nem `paracol`** — nenhum deles suporta tagged PDF no estado atual do `latex-lab`. A ordem de leitura (coluna 1 → 2 → 3) não seria garantida na estrutura do PDF.

### 10.2 Abordagem correta

Implementar colunas com **`tcolorbox` em modo `hbox` sequencial**, com estrutura de tagging explícita:

```latex
% Pseudocódigo da implementação de \colunas
\newenvironment{colunas}{%
  \tagstructbegin{tag=Sect}%  container de colunas
  \noindent
  \setlength{\guia@colwidth}{...}%  calculado por span
}{%
  \tagstructend%
  \par
}

\newcommand{\coluna}[2][span=1]{%
  % extrair span de #1
  \tagstructbegin{tag=Sect}%  cada coluna é uma Sect
  \begin{tcolorbox}[
    enhanced, sharp corners, boxrule=0pt,
    colback=white, colframe=white,
    width=<largura calculada>, nobeforeafter,
    box align=top,
  ]%
  #2%
  \end{tcolorbox}%
  \tagstructend%
}
```

A ordem de chamada das `\tagstructbegin` determina a ordem de leitura no PDF — por isso a sequência `\coluna{1}\coluna{2}\coluna{3}` garante a ordem correta.

### 10.3 Alt-text em imagens

Qualquer `\includegraphics` dentro de colunas deve usar o atributo `alt={}` suportado pelo kernel LaTeX com `\DocumentMetadata` ativo. Documentar isso no exemplo:

```latex
\includegraphics[width=\linewidth, alt={Gráfico de barras mostrando...}]{figura.pdf}
```

---

## 11. Zona de risco: `testphase={phase-III}`

> ⚠️ **Atenção: issue conhecida, verificação necessária**

O valor `testphase={phase-III}` em `\DocumentMetadata` pode estar quebrado após mudanças no `latex-lab` de abril/2026. Antes de implementar o sistema de tagging, verificar:

```bash
texdoc latex-lab-new-or-exp
```

ou testar com:

```latex
\DocumentMetadata{lang=pt-BR, pdfversion=2.0, pdfstandard=ua-2, testphase={phase-III}}
```

Se o documento não compilar ou gerar warnings sobre `testphase`, tentar valores alternativos documentados na versão atual do `latex-lab`. **Não silenciar os warnings** — eles indicam se o tagging está ativo ou sendo ignorado.

O briefing assume que `phase-III` está funcional. Se não estiver, **parar e reportar antes de continuar a implementação de acessibilidade**.

---

## 12. Tipografia

Manter a mesma cadeia de fallback do `guia-crpsp_acessivel.sty`:

1. Atkinson Hyperlegible Next (preferencial)
2. TeX Gyre Heros
3. Computer Modern Sans (`\sfdefault`)

Como `crpsp-base.sty` carrega o fontspec condicionalmente, o STY `guia-visual.sty` deve apenas chamar `\setmainfont` / `\setsansfont` dentro do bloco `\ifcrpsp@fontspec`.

---

## 13. Estilos de página (fancyhdr)

| Estilo | Quando usar |
|---|---|
| `guia@corpo` | frames de conteúdo (padrão) |
| `guia@abertura` | primeira página de seção (se houver tratamento especial) |
| `guia@vazio` | frames com background full-bleed sem navbar |

O estilo `guia@corpo` renderiza a navbar via TikZ no `\fancyhead[C]` e número de página.

---

## 14. Documento de teste mínimo (`exemplo-guia-visual.tex`)

O arquivo de exemplo deve compilar sem erros com LuaLaTeX e exercitar:

- [ ] Duas seções com dois frames cada, usando `\section[Curto]{Longo}`
- [ ] Uma seção sem argumento curto (`\section{Título longo}`) para testar fallback
- [ ] Frame com colunas 1+2 (imagem placeholder)
- [ ] Frame com colunas 1+1+1
- [ ] Frame `layout=full`
- [ ] Paleta personalizada via `\crpspCorPrincipal`
- [ ] `alt={}` em todas as imagens

Usar `\rule{...}{...}` como placeholder de imagem (não depender de arquivo externo).

---

## 15. Critérios de aceitação

- [ ] `lualatex exemplo-guia-visual.tex` passa sem erros (warning sobre `.nav` ausente na primeira passagem é esperado)
- [ ] Segunda passagem: navbar exibe todos os títulos curtos com seção correta destacada
- [ ] `\section[Curto]{Longo}` e `\section{Longo}` funcionam corretamente (curto na navbar, longo disponível)
- [ ] Warning de overflow emitido se soma de larguras da navbar exceder `\paperwidth`
- [ ] `pdfinfo` mostra `PDF version: 2.0`
- [ ] Nenhum `multicol` ou `paracol` no código produzido
- [ ] `crpsp_acessivel.cls` refatorado carrega `crpsp-base.sty` e mantém comportamento original
- [ ] `\crpspCorPrincipal`, `\crpspCorSecundaria`, `\crpspCorAcessoria` funcionam em ambas as classes
- [ ] Warning emitido se `span` total em `\colunas` ≠ 3

---

## 16. O que NÃO está no escopo deste briefing

- Implementação da linha `livro` (continua pendente no CLS original)
- Correção do `testphase` se estiver quebrado — isso é um task separado
- Geração de sumário / índice
- Integração com Pandoc/pipeline editorial

---

## 17. Sequência de implementação recomendada

1. Extrair `crpsp-base.sty` e refatorar `crpsp_acessivel.cls`  
   → verificar que o guia A5 existente ainda compila  
2. Criar `crpsp-guia_visual.cls` (esqueleto mínimo, geometria)  
3. Implementar `guia-visual.sty`: frame + grid de colunas (sem navbar ainda)  
4. Testar `exemplo-guia-visual.tex` com layout apenas  
5. Implementar navbar: stream `.nav` dedicado + renderização TikZ  
6. Testar navbar em duas passagens  
7. Adicionar tagging PDF/UA-2 ao sistema de colunas  
8. Validação final contra critérios de aceitação  

> Parar e reportar ao final de cada etapa par (2, 4, 6, 8) antes de continuar.
