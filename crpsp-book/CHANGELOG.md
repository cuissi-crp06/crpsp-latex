# crpsp-book

Linha acessível, sobre a classe `book` com LuaLaTeX, alvo PDF/UA-2.
Convenção de numeração em `editorial/inventario-latex/convencao-versionamento.md`,
no repositório `trabalho`.

O pacote canônico é implantado nos projetos sob o nome `livros_crp_acessivel_book.sty`,
e é esse o nome que ele declara — o nome do arquivo aqui (`book-crpsp_acessivel.sty`)
é do repositório, não da carga.

## 0.5.0-beta — 2026/07/10

`book-crpsp_acessivel.sty`. Variante PDF/UA da linha book, em par com
`crpsp-leg.sty`. Publicações: Caderno 12 CoREPSI e a regeneração do Manual de
Psicologia e Direitos Humanos.

A paleta ainda é fixa no pacote (`crp1`/`crp2`/`crp3`, azul). A direção adotada
daqui em diante é a da linha `desenvolvimento/v2`: paleta definida por
publicação.

### crpsp-leg 0.3.0-beta — 2026/07/13

Camada de legislação acessível. Declarada com `\ProvidesFile`, não
`\ProvidesPackage`, porque é lida via `\input` como módulo-irmão, e não por
`\usepackage`. O argumento opcional é o mesmo nos dois comandos.

## Linha `desenvolvimento/v2` — 0.1.0-alfa

`crpsp-base` (2026/07/03), `guia-crpsp_acessivel` (2026/05/25), `guia-visual`
(2026/07/03), `formulario` (2026/07/03) e `relatorio` (2026/07/29).

`crpsp-base` traz a interface de paleta por publicação: padrões neutros e os
setters `\crpspCorPrincipal`, `\crpspCorSecundaria` e `\crpspCorAcessoria`, com
os apelidos públicos `cor1`, `cor2` e `cor3`. A partir daqui a paleta deixa de
ser propriedade do pacote.

## Etiqueta

A etiqueta `book-v0.5.0` já existe. Depois que esta branch entrar em `main`,
criar as demais sobre o commit de merge:

    git tag book-v0.5.0-beta && git tag leg-v0.3.0-beta
