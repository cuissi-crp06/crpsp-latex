# Convenção de versionamento

Regras para numerar os `.sty` e `.cls` deste repositório. Reúne o que estava
espalhado na mensagem do commit `f5c98e8` (2026-09-04), nos changelogs e no
`PROVENIENCIA.md`. O arquivo que o CHANGELOG da linha book citava
(`editorial/inventario-latex/convencao-versionamento.md`) não existia no
workbench em 2026-09-13; este o substitui.

## Por que importa

`\@ifpackagelater` compara **só a data** declarada, não a versão nem o conteúdo.
Dois corpos diferentes com a mesma data são indistinguíveis para o LaTeX. O
defeito que esta convenção corrige nunca foi falta de versão, e sim **rótulo
repetido**: três arquivos declaravam `v7.0` de 2025/09/26, e três corpos
declaravam `v0.5.0` de 2026/07/10.

**Regra zero: corpos diferentes do mesmo pacote nunca compartilham data nem
versão**, nem aqui nem nas cópias de produção.

## Declaração

    \ProvidesPackage{nome}[AAAA/MM/DD vMAJOR.MINOR.PATCH-fase Descrição]

- **Data**: a da autoria daquele corpo. Se não houver, a da última gravação do arquivo de origem. Se nem isso, a da passagem que o versionou, e o CHANGELOG diz qual das três foi usada.
- **Descrição** em ASCII, sem acento nem travessão, como nas demais declarações do repositório.
- `\ProvidesFile` segue o mesmo formato (caso do `crpsp-leg.sty`, lido por `\input`).

## Números

A série é **por linha** (`crpsp-book`, `crpsp-memoir`, `crpsp-forms`, e cada linha
de `crpsp-book/desenvolvimento/v2/`), não global.

- **MAJOR** fica em `0` enquanto nenhuma versão for declarada estável. A passagem a `1.0.0` é decisão ainda não tomada.
- **MINOR** marca a geração: base nova, reengenharia, mudança de abordagem. Na linha memoir, 0.2 é a base de 2025, 0.4 a geração das primeiras tentativas de PDF acessível e 0.5 o Relatório de Gestão.
- **PATCH** é acréscimo ou correção dentro da geração. Na linha book, 0.5.1 é o ajuste às chaves renomeadas do `sec-template` e 0.5.2 o ambiente `NomesDuasColunas`.

## Fase

A fase é **propriedade da publicação**, não do arquivo:

| sufixo | quando |
|---|---|
| `-alfa` | nenhuma publicação servida por aquele corpo circulou fora do CRP SP — **inclusive quando não se sabe** |
| `-beta` | ao menos uma publicação servida por aquele corpo circulou fora do CRP SP |
| sem sufixo | versão estável. Reservado; nenhuma linha chegou lá |

A ordem é a do semver: `alfa` < `beta` < sem sufixo. Por isso fase desconhecida é
`alfa`, e não ausência de sufixo, que ordenaria acima de `beta`. Assim que uma
publicação circular, a declaração do mesmo corpo sobe para `-beta`, e o
CHANGELOG registra quando e por quê.

**Exceção:** as cópias em `legado/` declaram o próprio nome de arquivo, ficam
fora de qualquer série e **não levam fase** (ver `PROVENIENCIA.md`, "Limite").
O número delas é indicativo.

## Nome declarado

- O pacote **implantado** declara o nome sob o qual os documentos o carregam (`livros_crp`, `livros_crp_acessivel_book`, `formularios`), mesmo que o arquivo aqui tenha outro nome. Mudar isso quebra o `\usepackage` dos documentos.
- Toda variante **não implantada** declara o próprio nome de arquivo.
- Nenhum nome declarado se repete no repositório.

## Rótulos herdados de outros esquemas

`v7.0`, `v0.2` e semelhantes são **remapeados** para a série da linha, na ordem
em que os corpos foram escritos. Só a declaração é reescrita: corpo intacto,
data de autoria mantida, e o CHANGELOG registra o rótulo antigo.

## Trazer um arquivo de produção

1. Comparar pelo corpo contra todo o histórico:
   `python3 ferramentas/comparar-corpo.py ~/Documentos/trabalho --repo .`
2. Só entra o que estiver **fora do histórico**. Cópia que apenas ficou atrás não vem.
3. Reescrever só a declaração, com a próxima versão da série e a fase da publicação.
4. Registrar o sha256 (12) **da origem** e **do blob**. Desde o `.gitattributes` de 2026-09-13, texto é gravado com LF, então os dois só coincidem quando a origem já era LF e a declaração não mudou.
5. Corrigir a declaração das cópias de produção que tenham o mesmo corpo, para que a regra zero valha também lá.

## Etiquetas

`<linha>-v<versão>`, anotadas: `book-v0.5.2-beta`, `leg-v0.3.0-beta`,
`memoir-v0.5.0-beta`, `forms-v0.1.0-alfa`.

Vão sobre o commit em que a declaração do arquivo coincide com a etiqueta. Quando
isso não existe, porque a versão foi atribuída depois, a etiqueta vai sobre o
primeiro commit com aquele corpo, e a mensagem diz o que o arquivo declara ali.
