%% crpsp-timbrado.cls
%% Classe para documentos sobre o papel timbrado do CRP-SP (A4 retrato):
%% oficios, memorandos, pareceres, notas e textos corridos que levam o
%% logo no topo e o endereco no pe, como no modelo de papelaria
%% papelCartaCRPSP_4x0_A4_sede.docx (Papelaria Institucional/2026).
%% Arquitetura: crpsp-base.sty + crpsp-timbrado.cls
%% Engine obrigatoria: LuaLaTeX
%% Conformidade: PDF/UA-2 via tagging=on
%%
%% IMPORTANTE: \DocumentMetadata{...} DEVE ser chamado pelo documento
%% ANTES de \documentclass, conforme exigencia do kernel. A classe NAO
%% pode emiti-lo.
%%
%% Uso:
%%   \DocumentMetadata{lang=pt-BR, pdfversion=2.0, pdfstandard=ua-2,
%%                     tagging=on, pdftitle={Oficio n. 123/2026}}
%%   \documentclass{crpsp-timbrado}
%%
%% Base: article. Os cinco niveis de titulo do Word (Titulo 1 a 5) sao os
%% cinco comandos de secao da article, todos em LINHA PROPRIA:
%%   \section \subsection \subsubsection \paragraph \subparagraph
%% (na article padrao os dois ultimos sao titulos embutidos na linha; aqui
%% nao, porque um titulo de nivel 4 ou 5 que nao se separa do texto nao e
%% titulo para quem navega por cabecalhos.)
%%
%% Opcoes (chave-valor, \DeclareKeys):
%%   numerado — numera os cinco niveis (1, 1.1, 1.1.1, 1.1.1.1, 1.1.1.1.1).
%%              O padrao e SEM numeracao, como na linha `relatorio`.
%%   Opcoes desconhecidas seguem para a article (draft, etc.).
%%
%% Fontes: corpo em Atkinson Hyperlegible Next (pacote `atkinson` do TeX
%% Live), titulos e rodape em NEWJUNE, que e PROPRIETARIA e nao viaja com
%% o pacote (editorial/fonts/NewJune/ no Nextcloud). A classe emite ERRO
%% claro, e nao substitui a face, se alguma faltar.
%%
%% Arte do papel timbrado (declarada, nunca embutida):
%%   \timbradoLogo[<opcoes>]{<arquivo>}  logo do cabecalho, sem extensao ou
%%                              com ela (procura .pdf, .png, .jpg).
%%                              Padrao: crpsp-timbrado-logo, que se espera ser
%%                              CRP_LogoPreferencial_Horizontal_Positivo_COR.pdf
%%                              do kit de marca (editorial/logos/marca-2023/
%%                              positiva-cor/), copiado com esse nome. O padrao
%%                              corta a margem de protecao do PDF do kit
%%                              (trim/clip) e fixa 68,6 mm de largura. Com
%%                              \timbradoLogo{outro}, sem opcoes, so a largura
%%                              fica; <opcoes> sao as do \includegraphics e
%%                              substituem o corte. Sem arquivo algum, o
%%                              cabecalho cai para o nome do Conselho em texto
%%                              e nada falha.
%%   \timbradoRodape{<l1>}{<l2>}  as duas linhas do rodape. Padrao: a sede.
%%                              Cada subsede tem o seu endereco no papel
%%                              timbrado do designer; troca-se aqui.
%%   \timbradoDescricaoLogo{<texto>}  alternativa textual do logo (tambem o
%%                              texto do cabecalho quando nao ha arquivo).
%%
%% CABECALHO E RODAPE SAO ARTEFATO
%%   Sob tagging=on o kernel marca cabecalho e rodape como artefato de
%%   paginacao: ficam fora da arvore de estrutura e fora da ordem de leitura
%%   (conferido com show-pdf-tags: zero Figure, nenhum P vindo deles). E o
%%   tratamento correto de elemento que se repete em toda pagina, mas tem
%%   uma consequencia: QUEM LE POR TECNOLOGIA ASSISTIVA NAO OUVE O LOGO NEM
%%   O ENDERECO. O remetente tem de estar identificado no corpo do texto
%%   (assinatura, cargo, unidade). O texto do rodape continua selecionavel e
%%   pesquisavel no PDF.
%%
%% O QUE O MODELO .docx FAZ E ESTA CLASSE NAO REPETE
%%   O endereco do rodape do .docx e uma IMAGEM (PNG + SVG de curvas, sem
%%   texto): nao da para selecionar, pesquisar nem copiar. Aqui e texto
%%   composto, em NEWJUNE. O logo do .docx e um PNG de 259 px no cabecalho
%%   (96 dpi a 68,6 mm); aqui entra o PDF VETORIAL do kit de marca, que
%%   imprime nitido em qualquer tamanho.
%%
\NeedsTeXFormat{LaTeX2e}[2023/11/01]
\ProvidesClass{crpsp-timbrado}[2026/10/15 v0.1.0-alfa
  Classe de papel timbrado A4 CRP-SP]

% ──────────────────────────────────────────────
% 1. Opcoes
% ──────────────────────────────────────────────
\newif\ifcrpsp@timb@numerado \crpsp@timb@numeradofalse

\DeclareKeys{
  numerado .if    = crpsp@timb@numerado,
  numerado .usage = load,
}
\DeclareUnknownKeyHandler{%
  \def\crpsp@timb@valor{#2}%
  \ifx\crpsp@timb@valor\@empty
    \PassOptionsToClass{#1}{article}%
  \else
    \PassOptionsToClass{#1=#2}{article}%
  \fi
}
\ProcessKeyOptions\relax

% ──────────────────────────────────────────────
% 2. Classe base: article, 12 pt
%    (12 pt pelo mesmo motivo da linha `relatorio`: a altura-x da
%    Atkinson em 11 pt fica abaixo do minimo de 2,0 mm da RNIB.)
% ──────────────────────────────────────────────
\LoadClass[a4paper, 12pt, oneside]{article}

% ──────────────────────────────────────────────
% 3. Infraestrutura compartilhada e pacotes
%
%    NAO carregar, por incompatibilidade com o tagging: titlesec,
%    enumitem, tcolorbox, tabularray, pdfpages. Os motivos estao em
%    crpsp-relatorio.cls §3. fancyhdr tambem fica de fora: o estilo de
%    pagina e definido direto (\ps@timbrado), que e o mecanismo da
%    propria article e nao depende de pacote que o tagging precise
%    conhecer.
% ──────────────────────────────────────────────
\RequirePackage{crpsp-base}
\RequirePackage{graphicx}
\RequirePackage{geometry}
\RequirePackage{lastpage}
\RequirePackage[brazilian]{babel}
\RequirePackage{hyperref}
\RequirePackage{url}
\urlstyle{same}

\crpspTipografiaWCAG
\crpspMedida{80}
\crpspSondaGlifos

% ──────────────────────────────────────────────
% 4. Geometria do papel timbrado
%
%    Medidas do .docx (twips -> mm):
%      pgMar top 2722 = 48 mm   bottom 1134 = 20 mm
%            left 1418 = 25 mm  right  1701 = 30 mm
%            header/footer 709 = 12,5 mm
%    O logo do .docx comeca a 12,5 mm do topo e mede 68,6 x 25,8 mm; o
%    corpo comeca a 48 mm. headsep + headheight = 48 - 12,5 = 35,5 mm.
%
%    Embaixo, o .docx deixa 20 mm e o endereco fica ancorado na faixa de
%    rodape, a cerca de 16 mm da borda. Aqui o corpo para a 25 mm da borda
%    e a ultima linha do endereco assenta a 14,5 mm dela (footskip =
%    25 - 14,5), para que o rodape de duas linhas nao encoste no texto.
%
%    A MARGEM DIREITA E MAIOR QUE A DO .docx: 37 mm, e nao 30. Com 30 mm a
%    mancha tem 155 mm e a linha cheia 83 caracteres em Atkinson 12 pt
%    (medido pelo \crpspMedida), acima do teto de 80 do WCAG 1.4.8 que a
%    linha adota. A mancha de 148 mm da ~79. A esquerda fica em 25 mm para
%    o texto alinhar com o logo, como no modelo.
% ──────────────────────────────────────────────
\geometry{%
  a4paper,
  top        = 48mm,
  bottom     = 25mm,
  left       = 25mm,
  right      = 37mm,
  headheight = 26mm,
  headsep    = 9.5mm,
  footskip   = 10.5mm,
}

% ──────────────────────────────────────────────
% 5. Cores derivadas e hyperref
% ──────────────────────────────────────────────
\definecolor{crpsp@tinta}{HTML}{0D0D0D}
\AtBeginDocument{\color{crpsp@tinta}}

\hypersetup{
  colorlinks = true,
  linkcolor  = crpsp@cor1,
  urlcolor   = crpsp@cor2,
  citecolor  = crpsp@cor2,
}

% ──────────────────────────────────────────────
% 6. Fontes
%
%    Atkinson: o Path vem do kpathsea, e nao de busca por nome, para que
%    os quatro cortes saiam do mesmo build. Este Fedora ja teve duas
%    Atkinson Hyperlegible Next com md5 diferentes (ver relatorio.sty §2).
%    O Lua so IMPRIME o diretorio e o \edef captura; o -2 do tex.sprint
%    imprime com catcode 12.
% ──────────────────────────────────────────────
\edef\crpsp@timb@atkinson{%
  \directlua{
    local achado = kpse.find_file("AtkinsonHyperlegibleNext-Regular.otf",
                                  "opentype fonts")
    if achado then tex.sprint(-2, (achado:gsub("[^/]*$", ""))) end
  }%
}
\ifx\crpsp@timb@atkinson\@empty
  \ClassError{crpsp-timbrado}{Atkinson Hyperlegible Next nao encontrada}{%
    O kpathsea nao resolveu AtkinsonHyperlegibleNext-Regular.otf.\MessageBreak
    Instale o pacote `atkinson' do TeX Live: tlmgr install atkinson%
  }%
\fi

\ifcrpsp@fontspec
  \crpspExigeFonte{AtkinsonHyperlegibleNext-Regular.otf}%
    {Atkinson Hyperlegible Next}%
    {pacote `atkinson' do TeX Live (tlmgr install atkinson)}%
  \crpspExigeFonte{NEWJUNE-REGULAR.OTF}%
    {NEWJUNE (institucional, proprietaria)}%
    {editorial/fonts/NewJune/ no Nextcloud}%
  \setmainfont{AtkinsonHyperlegibleNext}[
    Path           = \crpsp@timb@atkinson,
    UprightFont    = AtkinsonHyperlegibleNext-Regular.otf,
    ItalicFont     = AtkinsonHyperlegibleNext-RegularItalic.otf,
    BoldFont       = AtkinsonHyperlegibleNext-Bold.otf,
    BoldItalicFont = AtkinsonHyperlegibleNext-BoldItalic.otf,
    Ligatures      = TeX,
  ]
  \setsansfont{NEWJUNE}[
    UprightFont    = NEWJUNE-REGULAR.OTF,
    ItalicFont     = NEWJUNE-REGULAR-ITALIC.OTF,
    BoldFont       = NEWJUNE-BOLD.OTF,
    BoldItalicFont = NEWJUNE-BOLD-ITALIC.OTF,
    Ligatures      = TeX,
  ]
  \IfFontExistsTF{AtkinsonHyperlegibleMono-Regular.otf}{%
    \setmonofont{AtkinsonHyperlegibleMono}[
      Path           = \crpsp@timb@atkinson,
      UprightFont    = AtkinsonHyperlegibleMono-Regular.otf,
      ItalicFont     = AtkinsonHyperlegibleMono-RegularItalic.otf,
      BoldFont       = AtkinsonHyperlegibleMono-Bold.otf,
      BoldItalicFont = AtkinsonHyperlegibleMono-BoldItalic.otf,
    ]%
  }{}%
\else
  \ClassError{crpsp-timbrado}{%
    Esta classe exige fontspec com luaotfload funcional%
  }{%
    Sem fontspec nao ha como declarar as fontes por arquivo, e\MessageBreak
    declarar por nome permitiria substituicao silenciosa da face.%
  }
\fi

% Caractere que a fonte nao tem vira ERRO, nao aviso: o PDF ficaria com
% glifo sem mapeamento Unicode (ver relatorio.sty §2b).
\AtBeginDocument{\tracinglostchars=3\relax}

% ──────────────────────────────────────────────
% 7. Seccionamento: os cinco niveis, todos em linha propria
%
%    Via \@startsection, NUNCA titlesec (quebra os hooks do tagging).
%    Os cinco nomes sao os da article e cada um e redefinido UMA vez:
%    sob tagging a primeira chamada de \@startsection por NOME congela o
%    estilo (ver relatorio.sty §4, "regra do nome proprio").
%
%    \paragraph e \subparagraph: o afterskip POSITIVO e o que torna o
%    titulo de linha propria; na article ele e negativo (titulo embutido).
%
%    Tamanhos absolutos em NEWJUNE; a hierarquia sai de tamanho nos tres
%    primeiros niveis e de peso e inclinacao nos dois ultimos, sem caixa
%    alta (o \MakeUppercase esconde a caixa real do texto para o leitor
%    de tela).
% ──────────────────────────────────────────────
\newcommand{\crpsp@timb@titulo}[3]{%
  \normalfont\sffamily\fontsize{#1}{#2}\selectfont#3\color{crpsp@cor1}}

\renewcommand\section{\@startsection{section}{1}{0pt}%
  {2\baselineskip}{0.5\baselineskip}%
  {\crpsp@timb@titulo{18}{21.6}{\bfseries}}}
\renewcommand\subsection{\@startsection{subsection}{2}{0pt}%
  {1.5\baselineskip}{0.4\baselineskip}%
  {\crpsp@timb@titulo{15}{18}{\bfseries}}}
\renewcommand\subsubsection{\@startsection{subsubsection}{3}{0pt}%
  {1.25\baselineskip}{0.3\baselineskip}%
  {\crpsp@timb@titulo{13}{15.6}{\bfseries}}}
\renewcommand\paragraph{\@startsection{paragraph}{4}{0pt}%
  {1.1\baselineskip}{0.25\baselineskip}%
  {\crpsp@timb@titulo{12}{14.4}{\bfseries}}}
\renewcommand\subparagraph{\@startsection{subparagraph}{5}{0pt}%
  {1.1\baselineskip}{0.25\baselineskip}%
  {\crpsp@timb@titulo{12}{14.4}{\bfseries\itshape}}}

% Padrao sem numeracao; `numerado` numera ate o nivel 5.
\ifcrpsp@timb@numerado
  \setcounter{secnumdepth}{5}
  \renewcommand\theparagraph{\thesubsubsection.\arabic{paragraph}}
  \renewcommand\thesubparagraph{\theparagraph.\arabic{subparagraph}}
\else
  \setcounter{secnumdepth}{-1}
\fi

% ──────────────────────────────────────────────
% 8. Papel timbrado: cabecalho e rodape
%
%    O estilo de pagina e o unico, e vale para todas as paginas, como o
%    .docx (um so cabecalho padrao; o de primeira pagina existe no
%    arquivo mas nao e ativado, falta o titlePg).
%
%    Cabecalho: o logo assenta na linha de base do cabecalho, que fica a
%    \headsep acima do corpo, e portanto seu topo cai a 12,5 mm da borda.
%    A direita, "Pagina X de Y" so aparece quando o documento tem mais
%    de uma pagina.
%
%    Rodape: duas linhas em NEWJUNE italica, na cor principal. A primeira
%    tem a segunda metade em negrito, como no modelo.
% ──────────────────────────────────────────────
\newcommand{\crpsp@timb@logo}{crpsp-timbrado-logo}
\newcommand{\crpsp@timb@logoalt}{Conselho Regional de Psicologia de São Paulo}
\newlength{\crpsp@timb@logolargura}
\setlength{\crpsp@timb@logolargura}{68.6mm}

% O PDF do kit (CRP_LogoPreferencial_Horizontal_Positivo_COR.pdf, pagina de
% 425,197 x 170,079 pt) traz margem de protecao embutida: o desenho ocupa
% 87% da largura. O PNG do .docx e rente ao desenho. Para o logo ter os
% mesmos 68,6 x 25,8 mm visiveis do papel original, o corte tira a folga
% medida na pagina rasterizada a 144 dpi (esquerda 29 px, embaixo 31, direita
% 80, em cima 30): trim = esq. baixo dir. cima, em pt. Fica 370,7 x 139,6 pt,
% proporcao 2,655, igual a do PNG do .docx (2,661).
\newcommand{\crpsp@timb@logoopts}{%
  trim=14.5pt 15.5pt 40pt 15pt, clip, width=\crpsp@timb@logolargura}
\newcommand{\timbradoLogo}[2][]{%
  \renewcommand{\crpsp@timb@logo}{#2}%
  \def\crpsp@timb@logoarg{#1}%
  \ifx\crpsp@timb@logoarg\@empty
    \renewcommand{\crpsp@timb@logoopts}{width=\crpsp@timb@logolargura}%
  \else
    \renewcommand{\crpsp@timb@logoopts}{#1}%
  \fi
}
\newcommand{\timbradoDescricaoLogo}[1]{\renewcommand{\crpsp@timb@logoalt}{#1}}

\newcommand{\crpsp@timb@rodape@um}{}
\newcommand{\crpsp@timb@rodape@dois}{}
\newcommand{\timbradoRodape}[2]{%
  \renewcommand{\crpsp@timb@rodape@um}{#1}%
  \renewcommand{\crpsp@timb@rodape@dois}{#2}%
}
\timbradoRodape
  {Conselho Federal de Psicologia · \textbf{Conselho Regional de Psicologia da 6ª Região}}
  {Rua Teodoro Sampaio, 417, Pinheiros, São Paulo, SP.
   CEP 05405-000. Site www.crpsp.org.br}

% O \IfFileExists do LaTeX nao tenta extensao, e o \includegraphics sim.
% Aqui o nome e testado como veio e depois com .pdf, .png e .jpg, na
% ordem de preferencia do vetor para o raster.
\newif\ifcrpsp@timb@temlogo
\newcommand{\crpsp@timb@procuralogo}{%
  \crpsp@timb@temlogofalse
  \@for\crpsp@timb@ext:={,.pdf,.png,.jpg}\do{%
    \ifcrpsp@timb@temlogo\else
      \IfFileExists{\crpsp@timb@logo\crpsp@timb@ext}{%
        \crpsp@timb@temlogotrue}{}%
    \fi
  }%
}

% Sem o arquivo o cabecalho cai para texto, e isso nao pode passar calado:
% um oficio sem logo sairia sem ninguem perceber. O aviso e dado UMA vez, no
% inicio do documento (o cabecalho e recomposto em toda pagina). E aviso, e
% nao erro, porque o exemplo do repositorio compila sem a arte.
\AtBeginDocument{%
  \crpsp@timb@procuralogo
  \ifcrpsp@timb@temlogo\else
    \ClassWarning{crpsp-timbrado}{%
      Logo `\crpsp@timb@logo' (.pdf, .png ou .jpg) nao encontrado; o\MessageBreak
      cabecalho sai com o nome do Conselho em texto. Copie o PDF do\MessageBreak
      kit de marca como crpsp-timbrado-logo.pdf, ao lado do documento%
    }%
  \fi
}

\newcommand{\crpsp@timb@cabecalho}{%
  \crpsp@timb@procuralogo
  \ifcrpsp@timb@temlogo
    % \expandafter: o keyval nao expande a macro que abre a lista.
    \expandafter\includegraphics\expandafter[\crpsp@timb@logoopts,
                     alt={\crpsp@timb@logoalt}]{\crpsp@timb@logo}%
  \else
    {\sffamily\bfseries\large\color{crpsp@cor1}\crpsp@timb@logoalt}%
  \fi
  \hfill
  \ifnum\getpagerefnumber{LastPage}>1
    {\sffamily\small\color{crpsp@cor1}%
     Página~\thepage~de~\pageref*{LastPage}}%
  \fi
}

\newcommand{\crpsp@timb@rodape}{%
  \parbox[b]{\textwidth}{\centering\sffamily\itshape\fontsize{8}{10}\selectfont
    \color{crpsp@cor1}%
    \crpsp@timb@rodape@um\\
    \crpsp@timb@rodape@dois}%
}

\newcommand{\ps@timbrado}{%
  \let\@mkboth\@gobbletwo
  \def\@oddhead{\crpsp@timb@cabecalho}%
  \let\@evenhead\@oddhead
  \def\@oddfoot{\crpsp@timb@rodape}%
  \let\@evenfoot\@oddfoot
}
\pagestyle{timbrado}
% \maketitle e \part passam por \thispagestyle{plain}/{empty} na article;
% aqui o timbrado vale em toda pagina.
\let\ps@plain\ps@timbrado

\endinput
