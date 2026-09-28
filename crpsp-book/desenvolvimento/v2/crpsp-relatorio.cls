%% crpsp-relatorio.cls
%% Classe para relatórios técnicos e institucionais do CRP-SP
%% (A4 retrato, leitura corrida, com sumário)
%% Arquitetura: crpsp-base.sty + crpsp-relatorio.cls + relatorio.sty
%% Engine obrigatória: LuaLaTeX
%% Conformidade: PDF/UA-2 via tagging=on
%%
%% IMPORTANTE: \DocumentMetadata{...} DEVE ser chamado pelo
%% documento ANTES de \documentclass, conforme exigência do
%% LaTeX kernel. A classe NÃO pode emitir \DocumentMetadata.
%%
%% Uso:
%%   \DocumentMetadata{lang=pt-BR, pdfversion=2.0, pdfstandard=ua-2,
%%                     tagging=on}
%%   \documentclass[externo]{crpsp-relatorio}
%%
%% `tagging=on` e NAO `testphase={phase-III,...}`: os mantenedores do
%% latex-lab declararam a chave testphase sintaxe legada, anterior a
%% introducao de tagging=on (issue latex3/tagging-project#1484,
%% 2026-07-14). Verificado equivalente nesta imagem: mesmo numero de
%% objetos de estrutura, mesmo resultado.
%%
%% Opções (chave-valor, \DeclareKeys — o \DeclareOption legado saiu
%% pelo princípio de consolidação de 17/09/2026):
%%
%%   interno — PADRÃO. Relatório técnico, sem decoração. Não carrega
%%             eso-pic e não define capa nem faixas.
%%   externo — Divulgação (relatório de gestão e gêneros afins).
%%             Acrescenta a camada de decoração: faixas no topo e no pé
%%             e capa de página inteira. Sem a arte, tudo cai em
%%             fallback tipográfico e nada falha.
%%   semtoc  — suprime o sumário automático. Ao contrário da linha
%%             guia_visual (navegada por navbar), aqui o sumário é o
%%             padrão: um relatório de muitas seções precisa dele.
%%
%% `interno` e `externo` são mutuamente exclusivas: combinadas, erro.
%%
\NeedsTeXFormat{LaTeX2e}[2023/11/01]
\ProvidesClass{crpsp-relatorio}[2026/09/28 v0.3.0-alfa
  Classe de relatorios A4 CRP-SP]

% ──────────────────────────────────────────────
% 1. Opções
% ──────────────────────────────────────────────
\newif\ifcrpsp@rel@toc      \crpsp@rel@toctrue
\newif\ifcrpsp@rel@externo  \crpsp@rel@externofalse
\newif\ifcrpsp@rel@variante \crpsp@rel@variantefalse

\newcommand{\crpsp@rel@variante@escolhe}{%
  \ifcrpsp@rel@variante
    \ClassError{crpsp-relatorio}{%
      As opcoes `interno' e `externo' sao mutuamente exclusivas%
    }{%
      `interno' e um relatorio tecnico sem decoracao; `externo' traz a\MessageBreak
      camada de arte (faixas e capa). Escolha uma das duas, ou nenhuma:\MessageBreak
      o padrao e `interno'.%
    }%
  \fi
  \crpsp@rel@variantetrue
}

\DeclareKeys{
  interno .code  = {\crpsp@rel@variante@escolhe},
  interno .usage = load,
  externo .code  = {\crpsp@rel@variante@escolhe\crpsp@rel@externotrue},
  externo .usage = load,
  semtoc  .ifnot = crpsp@rel@toc,
  semtoc  .usage = load,
}
% Opções desconhecidas seguem para article (oneside, draft, etc.).
% O handler recebe a chave em #1 e o valor em #2 — não há \CurrentOption
% no sistema de chaves.
\DeclareUnknownKeyHandler{%
  \def\crpsp@rel@valor{#2}%
  \ifx\crpsp@rel@valor\@empty
    \PassOptionsToClass{#1}{article}%
  \else
    \PassOptionsToClass{#1=#2}{article}%
  \fi
}
\ProcessKeyOptions\relax

% ──────────────────────────────────────────────
% 2. Classe base: article
%    (NÃO book: o relatório é uma sequência plana de seções,
%    sem capítulos, frontmatter ou partes. E NÃO memoir/scrbook,
%    que geram árvore de tags incorreta sob tagging=on.)
%
%    12 pt desde 17/09/2026, era 11 pt. A Lora em 11 pt tinha
%    altura-x de 1,933 mm, ABAIXO do mínimo de 2,0 mm da RNIB: a
%    linha não cumpria o critério que o próprio sistema adota.
%    O custo está medido — o mesmo conteúdo ocupa +79% de altura ao
%    ir de 11/13,2 sem espaço entre parágrafos para 12/18 com o
%    espaço do WCAG — e foi aceito.
% ──────────────────────────────────────────────
\LoadClass[a4paper, 12pt, oneside]{article}

% ──────────────────────────────────────────────
% 3. Infraestrutura compartilhada + pacotes fundamentais
%    (engine check, cores, fontspec e o bloco do WCAG vêm de crpsp-base)
%
%    NÃO carregar, por incompatibilidade com o tagging:
%      titlesec   — quebra os hooks de parágrafo do tagging (WA-03)
%      enumitem   — incompatível com o módulo `block` do latex-lab
%                   (sob tagging=on o latex-lab o substitui pela emulação)
%      tcolorbox  — força \par em volta da box, empilhando o que
%                   deveria ficar lado a lado (ver relatorio.sty §5)
%      tabularray — gera relações de tag inválidas ('text' -> 'text-unit')
%                   no fecho de todo tblr, mesmo com testphase=table.
%                   Usa-se tabular/longtable + \rowcolor (relatorio.sty §7).
%      pdfpages   — achado de 17/09/2026: é por onde entra a capa do Guia
%                   de Apresentações Acessíveis, e é incompatível com
%                   tagging. A capa do `externo` usa shipout marcado como
%                   artefato (relatorio.sty §10), nunca \includepdf.
%      multicol/paracol — sem suporte a tagged PDF para texto corrido.
%                   Exceção: o multicol entra pelo NomesDuasColunas
%                   dos créditos (relatorio.sty §12), validado para
%                   uma lista de nomes, um P por pessoa.
% ──────────────────────────────────────────────
% A opção `table` do xcolor (que traz \rowcolor) precisa ser passada
% ANTES de crpsp-base, que é quem carrega o xcolor.
\PassOptionsToPackage{table}{xcolor}
\RequirePackage{crpsp-base}
\RequirePackage{graphicx}
\RequirePackage{geometry}
\RequirePackage{longtable}
\RequirePackage{booktabs}
% babel com padrões de hifenização do português. Mesmo com a hifenação
% desligada pelo WCAG 1.4.8, o babel continua respondendo pelo idioma
% dos nomes automáticos (Sumário, Tabela, Figura). O `lang=pt-BR` do
% \DocumentMetadata declara o idioma no PDF e não faz isso.
\RequirePackage[brazil]{babel}
\RequirePackage{hyperref}
\RequirePackage{url}
\urlstyle{same}

% O bloco do WCAG 1.4.8 (espaço entre parágrafos, alinhamento à
% esquerda sem hifenação, compensação do \@afterheading). É opt-in na
% base de propósito — ver o cabeçalho de crpsp-base.sty.
\crpspTipografiaWCAG

% Régua de medida: registra no log os caracteres da linha cheia e avisa
% se passarem do teto do WCAG 1.4.8 (80). A mancha desta linha é
% desenhada para 75 — ver relatorio.sty §1.

% Sonda de glifo de convenção: avisa, no carregamento, se a face não
% tiver o U+0060. Ver crpsp-base §4b — o defeito depende de qual das
% duas Atkinson instaladas o luaotfload escolhe.
\crpspMedida{80}
\crpspSondaGlifos

% ──────────────────────────────────────────────
% 4. Implementação de layout
% ──────────────────────────────────────────────
\RequirePackage{relatorio}

\endinput
