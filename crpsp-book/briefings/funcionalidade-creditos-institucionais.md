---
tipo: funcionalidade
dominio: editorial
projeto: crpsp-book
estado: a-implementar
criado: 2026-09-17
---

# Créditos institucionais gerados a partir do pipeline

Pedido do Angelo em 17/09/2026. A parte pré-textual das publicações traz os
créditos institucionais — composição do Plenário, da Diretoria e das comissões
envolvidas. Hoje são digitados à mão. **A classe deve recuperá-los e inseri-los
no lugar certo**, com nominata atualizada por padrão e a possibilidade de pedir
uma data ("a Diretoria em 15/09/2024", "a Comissão de Ética naquela data").

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

- [ ] **Onde mora o gerador.** `scripts/normativas/` (perto dos dados, e o
      espelho já existe) ou `editorial/` do repositório `scripts` (perto do
      `gerar_listagem_creditos.py`, que ele substitui)?
- [ ] **O formato intermediário.** JSON de nominata, como o `latexgen.py` faz,
      ou `.tex` direto do banco? O JSON permite conferir antes de compor.
- [ ] **Recuperar o `atualizar_creditos.py`** a partir do `.pyc`, ou tratá-lo
      como perdido e escrever do zero? O `.pyc` é de Python 3.14 e pode ser
      descompilado o bastante para revelar a intenção.
- [ ] **O que fazer com o `plenario_e_comissoes 1.md`** e o
      `gerar_listagem_creditos.py`: aposentar quando o gerador novo existir, ou
      manter como conferência independente do que veio do banco?
- [ ] **Nome e registro na mesma linha.** Hoje é
      `\NomeNosCreditos{nome (CRP~06/registro)}`, com o registro dentro do
      texto. Separar em dois argumentos ajudaria o tagging e a acessibilidade —
      e é mudança de API, com alias deprecado, pela disciplina do briefing do
      formulário.
- [ ] **Qual a fonte da nominata "atual"**: o registro institucional, ou o
      replay de `eventos_institucionais` até hoje? Se as duas divergirem, qual
      manda — e a divergência é achado a investigar.

## Relacionados

- `briefing-crpsp-livro-relatorio.md` — lista `creditos` como módulo opcional
  da linha `livro`. Esta é a especificação desse módulo.
- `preparo-ambiente-2026-09-17.md` — o orçamento de pacotes e a interface de
  títulos que a página de créditos vai usar.
- `scripts/normativas/ESPELHO.md` — o espelho do pipeline no workbench já ficou
  à frente do repositório três vezes. Conferir antes de mexer no gerador.
