%% crpsp-relatorio.cls
%% Classe para relatórios técnicos e institucionais do CRP-SP
%% (A4 retrato, leitura corrida, com sumário)
%% Arquitetura: crpsp-base.sty + crpsp-relatorio.cls + relatorio.sty
%% Engine obrigatória: LuaLaTeX
%% Conformidade: PDF/UA-2 via phase-III tagging
%%
%% IMPORTANTE: \DocumentMetadata{...} DEVE ser chamado pelo
%% documento ANTES de \documentclass, conforme exigência do
%% LaTeX kernel. A classe NÃO pode emitir \DocumentMetadata.
%%
%% Uso:
%%   \DocumentMetadata{lang=pt-BR, pdfversion=2.0, pdfstandard=ua-2,
%%                     tagging=on}
%%   \documentclass{crpsp-relatorio}
%%
%% `tagging=on` e NAO `testphase={phase-III,...}`: os mantenedores do
%% latex-lab declararam a chave testphase sintaxe legada, anterior a
%% introducao de tagging=on (issue latex3/tagging-project#1484,
%% 2026-07-14). Verificado equivalente nesta imagem: mesmo numero de
%% objetos de estrutura, mesmo resultado.
%%
%% Opções:
%%   semtoc — suprime o sumário automático. Ao contrário da linha
%%            guia_visual (navegada por navbar), aqui o sumário é o
%%            padrão: um relatório de muitas seções precisa dele.
%%
\NeedsTeXFormat{LaTeX2e}[2023/11/01]
\ProvidesClass{crpsp-relatorio}[2026/07/29 v0.1
  Classe de relatorios A4 CRP-SP]

% ──────────────────────────────────────────────
% 1. Opções
% ──────────────────────────────────────────────
\newif\ifcrpsp@relatorio@toc \crpsp@relatorio@toctrue
\DeclareOption{semtoc}{\crpsp@relatorio@tocfalse}

% Repassa opções desconhecidas para article
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

% ──────────────────────────────────────────────
% 2. Classe base: article
%    (NÃO book: o relatório é uma sequência plana de seções,
%    sem capítulos, frontmatter ou partes. E NÃO memoir/scrbook,
%    que geram árvore de tags incorreta sob phase-III.)
% ──────────────────────────────────────────────
\LoadClass[a4paper, 11pt, oneside]{article}

% ──────────────────────────────────────────────
% 3. Infraestrutura compartilhada + pacotes fundamentais
%    (engine check, cores e fontspec vêm de crpsp-base)
%
%    NÃO carregar, por incompatibilidade com phase-III:
%      titlesec   — quebra os hooks de parágrafo do tagging (WA-03)
%      enumitem   — incompatível com o módulo `block` do latex-lab
%      tcolorbox  — força \par em volta da box, empilhando o que
%                   deveria ficar lado a lado (ver relatorio.sty §5)
%      tabularray — gera relações de tag inválidas ('text' -> 'text-unit')
%                   no fecho de todo tblr, mesmo com testphase=table.
%                   Usa-se tabular/longtable + \rowcolor (relatorio.sty §7).
%                   ATENÇÃO: as outras classes v2 ainda carregam
%                   tabularray; se vierem a usar tabelas sob tagging,
%                   esbarrarão no mesmo defeito.
%      multicol/paracol — sem suporte a tagged PDF
% ──────────────────────────────────────────────
% A opção `table` do xcolor (que traz \rowcolor) precisa ser passada
% ANTES de crpsp-base, que é quem carrega o xcolor.
\PassOptionsToPackage{table}{xcolor}
\RequirePackage{crpsp-base}
\RequirePackage{graphicx}
\RequirePackage{geometry}
\RequirePackage{longtable}
\RequirePackage{booktabs}
% babel com padrões de hifenização do português: sem ele o TeX quebra
% as linhas com padrões do inglês e a justificação de texto corrido em
% pt-BR acumula overfull. O `lang=pt-BR` do \DocumentMetadata declara o
% idioma no PDF, mas NÃO carrega padrões de hifenização.
\RequirePackage[brazil]{babel}
\RequirePackage{hyperref}
\RequirePackage{url}
\urlstyle{same}

% ──────────────────────────────────────────────
% 4. Implementação de layout
% ──────────────────────────────────────────────
\RequirePackage{relatorio}

\endinput
