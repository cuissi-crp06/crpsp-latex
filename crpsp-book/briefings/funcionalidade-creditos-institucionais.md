---
tipo: funcionalidade
dominio: editorial
projeto: crpsp-book
estado: em-implementacao
atualizado: 2026-09-28
criado: 2026-09-17
---

# Créditos institucionais gerados a partir do pipeline

Pedido do Angelo em 17/09/2026. A parte pré-textual das publicações traz os
créditos institucionais — composição do Plenário, da Diretoria e das comissões
envolvidas. Hoje são digitados à mão. **A classe deve recuperá-los e inseri-los
no lugar certo**, com nominata atualizada por padrão e a possibilidade de pedir
uma data ("a Diretoria em 15/09/2024", "a Comissão de Ética naquela data").

## Estado em 28/09/2026

**A metade da classe está feita:** `relatorio` 0.3.0-alfa, §12 (ver o `CHANGELOG.md`).
Veio do `pe26` (`plan-est_2026`), que validou o modelo do Relatório de Gestão em
PDF/UA-2 nos dias 24 e 25/09.

A interface final, que é o que o gerador escreve:

| Macro | Papel |
| --- | --- |
| `\creditosoculto{título}` | nível 1, na árvore de tags e sem impressão; abre página |
| `\creditosgrupo{grupo}` | nível 2, com fio como artefato |
| `\creditossub{subgrupo}` | nível 3 |
| `\creditos{título}` | nível 1 visível, para a ficha técnica |
| `\NomeNosCreditos{nome}{registro}[nota]` | uma pessoa; registro num `Span` próprio |
| `\CargoNosCreditos[registro]{nome}{cargo}` | uma pessoa, com o cargo alinhado em coluna |
| `CreditoInstitucional`, `NomesDuasColunas` | blocos de nomes; uma pessoa não se parte |

- **Registro separado do nome:** feito. A forma de um argumento,
  `\NomeNosCreditos{nome (CRP~06/nº)}`, continua aceita e emite aviso de
  deprecação.
- **Nome do comando:** mantido `\NomeNosCreditos`, por decisão do editor em
  24/09.
- **Destino dos `.tex` gerados:** `editorial/creditos/` no workbench, um arquivo
  por divisão (`Diretoria.tex`, `Plenario.tex`, um por comissão, um por
  gerência), incluídos por `\input`. Cada arquivo traz o título da divisão e as
  linhas. A página, os grupos e as quebras continuam sendo da publicação.
  Decidido na terceira revisão do `pe26`, em 24/09.
- **O gerador:** Sprint 3 do plano, que é o Sprint 13 do ROTEIRO do
  `normativas-pipeline`. Formato intermediário JSON, e a regra é falhar alto.
- **Não feito:** a interface declarativa `\CreditosInstitucionais{...}`
  (abaixo) e a composição com data. O `\input` por divisão resolve o caso
  atual sem ela.
- **Fora do escopo desta rodada:** levar o §12 para a linha `book`, que tem a
  interface 0.5.1 com o registro dentro do nome.

## O que já existe

**A página de créditos.** `production/editorial/publicacoes/cartilhas/
apresentacoes_acessiveis/LaTeX/paratextos/creditos_institucionais.tex` é o
modelo do formato desejado:

```latex
\CreditoInstitucionalUm{XVIII Plenário}
\CreditoInstitucionalDois{Diretoria}
\begin{CreditoInstitucional}\begin{center}
  \CargoNosCreditos{Valéria Campinas Braunstein}{\textbf{presidenta}}
  …
\end{center}\end{CreditoInstitucional}
\CreditoInstitucionalDois{Conselheiras/os}
\begin{CreditoInstitucional}\begin{NomesDuasColunas}
  \NomeNosCreditos{Beatris Guarita Dotta (CRP~06/143345)}
  …
```

Três níveis de comando já existem no pacote `book` — `CreditoInstitucionalUm`,
`Dois`, o ambiente `CreditoInstitucional`, mais `\CargoNosCreditos` (nome +
cargo) e `\NomeNosCreditos` (nome + registro). O ambiente `NomesDuasColunas` é
o que entrou na 0.5.1 pela varredura de genealogia.

Ao lado, `paratextos/comissoes/` com `COE.tex`, `COF.tex` e `ComCom.tex` —
um arquivo por comissão, feitos para `\input`.

**A tentativa anterior, e o que sobrou dela.** Na pasta do Guia há
`__pycache__/atualizar_creditos.cpython-314.pyc` — **o `.py` não existe mais**,
nem no workbench nem no repositório `scripts`. É a tentativa que o Angelo
lembra. Ficou o bytecode e os `.tex` que ele gerou.

O que **sobreviveu** está versionado: `editorial/gerar_listagem_creditos.py`, no
`cuissi-crp06/scripts`. Lê um **markdown mantido à mão**
(`plenario_e_comissoes 1.md`, 53 KB, na mesma pasta do Guia), filtra por
comissão e emite as linhas `\NomeNosCreditos{nome (CRP~06/registro)}` ordenadas.
Tem `--excluir` para tirar uma pessoa da lista — sinal de que a curadoria
manual era necessária.

**Limites da solução atual:** a fonte é um markdown que alguém atualiza à mão,
não há noção de data, e cada comissão exige uma invocação com o nome exato.

## Onde os dados estão de verdade

Duas fontes no pipeline, e servem a perguntas diferentes.

**1. Registro institucional** — `pessoas`, `divisoes`, `pessoa_vinculos`,
`pessoa_aliases`, `divisao_aliases`, materializadas por
`scripts/normativas/institucional_link.py` a partir de
`data/institucional/institucional.json`. É o quadro **atual**: responde ao
padrão pedido, a nominata atualizada.

**2. `eventos_institucionais`** — uma linha por pessoa mencionada num ato que
mexe em quem ocupa o quê, extraída de portarias e resoluções por
`scripts/normativas/eventos_institucionais.py`. Colunas que interessam:

| Coluna | Serve para |
|---|---|
| `data` | ISO, do `documentos.data_publicacao` — **é o que permite pedir uma data** |
| `tipo_ato` | `composicao`, `nomeacao`, `designacao`, `exoneracao`, `destituicao`, `posse` |
| `divisao_id` / `divisao_texto` | qual comissão; `divisao_id` NULL = não resolveu |
| `pessoa_id`, `registro_num`, `nome_chave`, `funcao` | quem e em que função |
| `confianca` | `registro`, `alias` ou `nenhuma` |
| `revisado` | marca de curadoria |

Compor "a COE em 15/09/2024" é **reproduzir os eventos daquela divisão até a
data**. É para isso que a tabela existe.

## Os cuidados, que aqui não são detalhe

Uma página de créditos **nomeia pessoas reais numa publicação institucional**.
Errar um nome ou omitir alguém não é defeito estético.

O próprio `eventos_institucionais.py` registra as armadilhas:

- **A chave é o registro CRP, não o nome.** O texto vem de PDF, às vezes com
  OCR, e o nome sai corrompido com frequência. *"O nome canônico do resultado
  vem sempre do registro institucional, nunca do PDF."*
- **`pessoa_id` pode ser NULL** — pessoa fora do registro. O evento é gravado
  assim mesmo, com `nome_chave` preenchido, para fechar pares "nomeada em 2019,
  exonerada em 2021".
- **`divisao_id` pode ser NULL** quando a divisão não resolveu.
- **`confianca = nenhuma`** existe e é frequente nas portarias individuais, que
  trazem só o nome.

⚠️ **O padrão tem de ser falhar alto, não adivinhar.** Se a composição pedida
tiver qualquer pessoa sem `pessoa_id`, divisão sem `divisao_id` ou linha com
`confianca = nenhuma`, a geração deve **parar com mensagem clara** em vez de
emitir uma lista plausível e errada. Publicar nome de OCR é pior que não
publicar.

## O desenho, e a restrição que o decide

**A classe não pode consultar o banco.** O banco tem 525 MB, vive fora do
workbench (`~/normativas-run/`) e se instala por `baixar_banco.sh` a partir de
uma release. Uma classe LaTeX que exigisse isso não compilaria em máquina
nenhuma sem o pipeline montado — e o WSL doméstico é exatamente esse caso.

**O precedente do projeto já resolve isso.** O `scripts/normativas/latexgen.py`
declara no cabeçalho:

> "Consome exclusivamente os JSONs em `export/normas/<id_arquivo>.json`;
> **nunca** consulta o SQLite diretamente — a interface única é o JSON."

O mesmo contrato vale aqui:

```
pipeline (banco) → JSON de nominata → gerador → .tex → \input pela classe
```

O `.tex` gerado fica versionado junto da publicação, como os `COE.tex` de hoje.
A classe só precisa saber **onde** procurá-lo e **como** compor a página.

## O produto final

**Decidido em 17/09.** O gerador emite `.tex`, nesta granularidade:

- **um arquivo para Plenário e Diretoria**, que andam juntos na página;
- **um arquivo por comissão**.

É a granularidade que a pasta `paratextos/comissoes/` do Guia já pratica, com
`COE.tex`, `COF.tex` e `ComCom.tex` — a diferença é que passam a ser gerados, e
não digitados.

## O que a classe faz, então

Uma interface declarativa no preâmbulo, resolvida contra os `.tex` gerados:

```latex
\CreditosInstitucionais{
  plenario  = atual,
  diretoria = atual,
  comissoes = {COE, CDH},
}
```

e a variante com data:

```latex
\CreditosInstitucionais{
  diretoria = 2024-09-15,
  comissoes = {COE = 2024-09-15},
}
```

`atual` é o padrão quando a chave não traz data. A classe monta os níveis de
título e o ambiente de colunas; quem preenche os nomes é o fragmento gerado.

## Decisões em aberto

- [x] ~~**Onde mora o gerador.**~~ **Decidido em 17/09: no
      `cuissi-crp06/normativas-pipeline`.** O gerador se relaciona com o
      **sprint 10** do pipeline, ainda não definido, e é natural que fique lá —
      junto dos dados e do `latexgen.py`, que já faz o mesmo tipo de travessia.
      Chega ao workbench pelo espelho `scripts/normativas/`, no sentido repo →
      espelho, nunca o contrário.
- [ ] **O formato intermediário.** Em aberto, com **aposta em JSON** — é o que o
      `latexgen.py` já usa, e permite conferir a nominata antes de compor a
      página. A confirmar no sprint 10.
- [x] ~~**A conversão nominata → TEX sai em Lua?**~~ **Resolvido em 17/09 pela
      norma de linguagem:** `crpsp-latex` em TeX e Lua, `normativas-pipeline` em
      Python. O gerador mora no pipeline, então **sai em Python**, ao lado do
      `latexgen.py`. Ver a seção abaixo e o README da raiz.
- [ ] **Recuperar o `atualizar_creditos.py`** a partir do `.pyc`, ou escrever do
      zero? **Fica para o sprint 10 definir.** O `.pyc` é de Python 3.14 e pode
      ser descompilado o bastante para revelar a intenção — a pergunta é se vale
      o trabalho, ou se o que se sabe da saída dele já basta.
- [x] ~~**O que fazer com o `plenario_e_comissoes 1.md`** e o
      `gerar_listagem_creditos.py`~~ **Decidido em 17/09: podem ser
      aposentados.** Não ficam como conferência independente. O markdown é
      conteúdo e sai pelo caminho de conteúdo; o `gerar_listagem_creditos.py`
      está no `cuissi-crp06/scripts` e sai de lá quando o gerador novo existir —
      **não antes**, para não abrir um vão sem substituto.
- [x] ~~**Nome e registro na mesma linha.**~~ **Decidido em 17/09: separar em
      dois argumentos.** Hoje é `\NomeNosCreditos{nome (CRP~06/registro)}`, com
      o registro dentro do texto — o tagging não distingue um do outro, e o
      leitor de tela lê o número como parte do nome. A classe adota a forma
      melhor, com alias deprecado para os `.tex` existentes, pela disciplina do
      briefing do formulário. É aplicação do princípio de consolidação
      registrado nas [decisões de 17/09](decisoes-2026-09-17.md).

      O nome do comando também está em aberto: `\NomeNosCreditos` descreve onde
      ele aparece, não o que ele é.
- [x] ~~**Qual a fonte da nominata "atual"**~~ **Decidido em 17/09: o registro
      institucional.** É o quadro corrente, materializado por
      `institucional_link.py`, e não depende de reproduzir atos. O
      `eventos_institucionais` fica para as composições **com data**, que é o
      que só ele sabe responder.

      Continua valendo conferir: se o replay até hoje divergir do registro, a
      divergência é achado a investigar no pipeline — não empate a desempatar
      na hora de compor a página.

## Lua na conversão — a avaliar, e a bifurcação

Decisão do Angelo em 17/09: **avaliar Lua para converter a nominata em TEX,
aproveitando o motor de compilação.** Faz sentido — o LuaTeX já está ali, e é o
único motor que estas linhas aceitam.

⚠️ **Mas "aproveitar o motor" admite duas leituras, e elas não são equivalentes.**

**A. Script `texlua` autônomo.** Lê o JSON e grava os `.tex`, como o
`latexgen.py` faz hoje com as normas. Roda no pipeline, fora da compilação do
documento. Preserva a decisão já tomada — o produto é um `.tex` para
Plenário/Diretoria e um por comissão — e mantém a nominata conferível antes de
entrar na publicação.

**B. Lua dentro do documento.** A classe lê o JSON em tempo de compilação e
compõe os créditos direto, sem `.tex` intermediário. Mais curto, mas:

- **contradiz a decisão do produto final** ser arquivo `.tex`;
- move a validação para o tempo de compilação, onde a regra de *falhar alto*
  (`pessoa_id` NULL, `confianca = nenhuma`) vira erro de LaTeX em vez de erro do
  pipeline — pior lugar para tratar dado sujo;
- o JSON passa a ser dependência de compilação da publicação, e a página de
  créditos deixa de ser auditável pelo diff do `.tex`.

**Resolvido em 17/09: fica a A, em Python.** Os dois pontos práticos que
pesavam contra a Lua aqui viraram norma de repositório (README da raiz):

- o `normativas-pipeline` é um pipeline **Python**, e um `texlua` ali não
  compartilharia ambiente virtual, dependências nem testes com o resto;
- o `latexgen.py` já faz JSON → LaTeX em Python. Um gerador em Lua criaria
  **dois caminhos diferentes** para a mesma travessia no mesmo repositório.

A norma: `crpsp-latex` em TeX e Lua, `normativas-pipeline` em Python; travessia
que cruza os dois é escrita na linguagem **do repositório onde mora**. Lua segue
disponível — para o que roda dentro das classes, que é onde o motor de fato
está.

## Relacionados

- `briefing-crpsp-livro-relatorio.md` — lista `creditos` como módulo opcional
  da linha `livro`. Esta é a especificação desse módulo.
- `preparo-ambiente-2026-09-17.md` — o orçamento de pacotes e a interface de
  títulos que a página de créditos vai usar.
- `scripts/normativas/ESPELHO.md` — o espelho do pipeline no workbench já ficou
  à frente do repositório três vezes. Conferir antes de mexer no gerador.
