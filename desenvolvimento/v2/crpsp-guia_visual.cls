%% crpsp-guia_visual.cls
%% Classe para publicações 16:9 do CRP-SP (guias visuais,
%% apresentações institucionais em PDF)
%% Arquitetura: crpsp-base.sty + crpsp-guia_visual.cls + guia-visual.sty
%% Engine obrigatória: LuaLaTeX
%% Conformidade: PDF/UA-2 via phase-III tagging
%%
%% IMPORTANTE: \DocumentMetadata{...} DEVE ser chamado pelo
%% documento ANTES de \documentclass, conforme exigência do
%% LaTeX kernel. A classe NÃO pode emitir \DocumentMetadata.
%%
%% Uso:
%%   \DocumentMetadata{lang=pt-BR, pdfversion=2.0, pdfstandard=ua-2, testphase={phase-III}}
%%   \documentclass{crpsp-guia_visual}
%%
%% Opções:
%%   toc   — \section volta a alimentar o sumário (\addcontentsline);
%%           desligado por padrão (a navegação é feita pela navbar)
%%
\NeedsTeXFormat{LaTeX2e}[2023/11/01]
\ProvidesClass{crpsp-guia_visual}[2026/07/03 v0.1
  Classe guia visual 16:9 CRP-SP]

% ──────────────────────────────────────────────
% 1. Opções
% ──────────────────────────────────────────────
\newif\ifcrpsp@guiavisual@toc \crpsp@guiavisual@tocfalse
\DeclareOption{toc}{\crpsp@guiavisual@toctrue}

% Repassa opções desconhecidas para article
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

% ──────────────────────────────────────────────
% 2. Classe base: article
%    (NÃO book — sem frontmatter/mainmatter/backmatter;
%    o documento é uma sequência plana de seções e frames)
% ──────────────────────────────────────────────
\LoadClass{article}

% ──────────────────────────────────────────────
% 3. Infraestrutura compartilhada + pacotes fundamentais
%    (engine check, cores e fontspec vêm de crpsp-base)
% ──────────────────────────────────────────────
\RequirePackage{crpsp-base}
\RequirePackage{graphicx}
\RequirePackage{geometry}
\RequirePackage{eso-pic}
\RequirePackage{tabularray}
\RequirePackage{hyperref}

% ──────────────────────────────────────────────
% 4. Implementação de layout (frames, colunas, navbar)
% ──────────────────────────────────────────────
\RequirePackage{guia-visual}

\endinput
