%% crpsp-formulario.cls
%% Classe para formulários/requerimentos institucionais do CRP-SP (A4)
%% com campos preenchíveis (AcroForm) auto-dimensionáveis.
%% Arquitetura: crpsp-base.sty + crpsp-formulario.cls + formulario.sty
%% Engine obrigatória: LuaLaTeX
%% Conformidade PDF/UA-2: preparada, mas o tagging phase-III completo é
%% fase 2 (ver briefing-crpsp-formulario.md §8).
%%
%% IMPORTANTE: \DocumentMetadata{...} DEVE ser chamado pelo documento ANTES
%% de \documentclass (exigência do kernel). A classe NÃO pode emiti-lo.
%% Nesta fase os documentos não precisam de \DocumentMetadata.
%%
%% Uso:
%%   \documentclass{crpsp-formulario}            % com logo no cabeçalho
%%   \documentclass[timbrado]{crpsp-formulario}  % papel timbrado (sem logo)
%%
\NeedsTeXFormat{LaTeX2e}[2023/11/01]
\ProvidesClass{crpsp-formulario}[2026/07/03 v0.1
  Classe de formularios acessiveis CRP-SP]

% ──────────────────────────────────────────────
% 1. Opções
%    timbrado — geometria de papel timbrado (margens grandes, sem logo)
% ──────────────────────────────────────────────
\newif\ifcrpsp@form@timbrado \crpsp@form@timbradofalse
\DeclareOption{timbrado}{\crpsp@form@timbradotrue}

% Repassa opções desconhecidas para article
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

% ──────────────────────────────────────────────
% 2. Classe base: article (corpo 12pt, como os formulários atuais)
%    (NÃO book/abntex2 — o formulário é uma folha plana; sem
%    frontmatter/mainmatter nem maquinaria de tese do abntex2)
% ──────────────────────────────────────────────
\LoadClass[12pt]{article}

% ──────────────────────────────────────────────
% 3. Infraestrutura compartilhada + pacotes fundamentais
%    (engine check, cores e fontspec vêm de crpsp-base)
% ──────────────────────────────────────────────
\RequirePackage{crpsp-base}
\RequirePackage{graphicx}
\RequirePackage{geometry}
\RequirePackage{calc}
\RequirePackage{etoolbox}
\RequirePackage{setspace}
\RequirePackage{ragged2e}
\RequirePackage{framed}
\RequirePackage{xhfill}
\RequirePackage{microtype}
\RequirePackage{fancyhdr}
\RequirePackage{lastpage}
\RequirePackage{hyperref}

% ──────────────────────────────────────────────
% 4. Implementação de layout + sistema de campos
% ──────────────────────────────────────────────
\RequirePackage{formulario}

\endinput
