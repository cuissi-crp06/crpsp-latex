%% crpsp_acessivel.cls
%% Classe editorial acessível do CRP-SP
%% Arquitetura: crpsp-base.sty + crpsp_acessivel.cls + STYs por linha editorial
%% Engine obrigatória: LuaLaTeX
%% Conformidade: PDF/UA-2 via phase-III tagging
%%
%% IMPORTANTE: \DocumentMetadata{...} DEVE ser chamado pelo
%% documento ANTES de \documentclass, conforme exigência do
%% LaTeX kernel. A classe NÃO pode emitir \DocumentMetadata.
%%
%% Uso:
%%   \DocumentMetadata{lang=pt-BR, pdfversion=2.0, pdfstandard=ua-2, testphase={phase-III}}
%%   \documentclass[guia]{crpsp_acessivel}
%%
\NeedsTeXFormat{LaTeX2e}[2023/11/01]
\ProvidesClass{crpsp_acessivel}[2026/07/03 v0.2
  Classe editorial acessivel CRP-SP]

% ──────────────────────────────────────────────
% 1. Opções de linha editorial
% ──────────────────────────────────────────────
\newif\ifcrpsp@guia   \crpsp@guiafalse
\newif\ifcrpsp@livro  \crpsp@livrofalse

\DeclareOption{guia}{\crpsp@guiatrue}
\DeclareOption{livro}{\crpsp@livrotrue}

% Repassa opções desconhecidas para book
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{book}}
\ProcessOptions\relax

% Validação: exatamente uma linha editorial
\ifcrpsp@guia
  \ifcrpsp@livro
    \ClassError{crpsp_acessivel}{%
      Opcoes 'guia' e 'livro' sao mutuamente exclusivas%
    }{Escolha apenas uma linha editorial.}
  \fi
\else
  \ifcrpsp@livro\else
    \ClassError{crpsp_acessivel}{%
      Nenhuma linha editorial selecionada%
    }{%
      Use \string\documentclass[guia]{crpsp_acessivel}\MessageBreak
      ou \string\documentclass[livro]{crpsp_acessivel}.%
    }
  \fi
\fi

% ──────────────────────────────────────────────
% 2. Carrega classe base
% ──────────────────────────────────────────────
\LoadClass[a5paper]{book}

% ──────────────────────────────────────────────
% 3. Infraestrutura compartilhada + pacotes fundamentais
%    (engine check, cores e fontspec vêm de crpsp-base)
% ──────────────────────────────────────────────
\RequirePackage{crpsp-base}
\RequirePackage{graphicx}
\RequirePackage{geometry}
\RequirePackage{eso-pic}
\RequirePackage{enumitem}
\RequirePackage{tabularray}
\RequirePackage{hyperref}

% ──────────────────────────────────────────────
% 4. Despacha para o STY da linha editorial
% ──────────────────────────────────────────────
\ifcrpsp@guia
  \RequirePackage{guia-crpsp_acessivel}
\fi

\ifcrpsp@livro
  \ClassWarning{crpsp_acessivel}{%
    Linha editorial 'livro' ainda nao implementada.\MessageBreak
    Usando configuracao minima.%
  }
\fi

\endinput
