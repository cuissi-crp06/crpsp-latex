# crpsp-abnt

Estilo biblatex que estende o `biblatex-abnt` para a ABNT NBR 6023:2025 e a
NBR 10520:2023: documento jurídico (legislação, jurisprudência, ato
administrativo), citação autor-data acessível e mídia contemporânea.

**Estado:** `0.1.0-alfa`, Sprint 1 da trilha do piloto: legislação e ato normativo.
O plano, a linha de base medida e as decisões estão em
[`briefings/briefing-crpsp-abnt.md`](briefings/briefing-crpsp-abnt.md). As divergências
que faltam fechar estão em
[`desenvolvimento/corpus/DIVERGENCIAS.md`](desenvolvimento/corpus/DIVERGENCIAS.md).

## Uso

```latex
\usepackage[style=crpsp-abnt, backend=biber]{biblatex}
```

O `crpsp-abnt.dbx` é carregado junto com o estilo, sem a opção `datamodel`. Fora
da árvore do TeX, a pasta precisa estar no `TEXINPUTS`.

| Arquivo | Papel |
|---|---|
| `crpsp-abnt.bbx` | carrega o `abnt.bbx` e acrescenta o driver de `@legislation` e `@legal` |
| `crpsp-abnt.cbx` | por ora, só carrega o `abnt.cbx`; a chamada entra no Sprint 2 |
| `crpsp-abnt.dbx` | os campos `ementa` e `complementos` |

## Legislação e ato normativo

Na 6023, legislação é a seção 7.11.1–7.11.2 e ato administrativo normativo, a
7.11.5–7.11.6. São dois tipos diferentes (decisão 2 do briefing):

- `@legislation`: a entrada é a jurisdição (`BRASIL.`, `CURITIBA.`), para
  Constituição, lei, decreto e medida provisória;
- `@legal`: a entrada é a entidade que emite o ato, com o órgão interno em
  `nameaddon`. Resoluções do CFP e do CRP são `@legal`.

Os dois usam o mesmo driver, porque a ordem dos elementos é a mesma:

> AUTORIA. Título. Ementa. Organizado por. Edição. *In*: obra. Publicação.
> Páginas. Notas. Complementos. DOI. Disponível em: URL. Acesso em: data.

| Campo | O que guarda | Exemplo |
|---|---|---|
| `author` | jurisdição ou entidade, entre chaves duplas | `{{Brasil}}`, `{{Conselho Federal de Psicologia}}` |
| `nameaddon` | órgão interno, ou `[Constituição (1988)]` | `Ministério da Educação` |
| `title` | epígrafe | `Lei nº 13.146, de 6 de julho de 2015` |
| `ementa` | ementa; a atribuída vai entre colchetes | `[Aquisição de leite pasteurizado]` |
| `editor` + `editortype = {organizer}` | organizador de coletânea | sai `Organizado por …` |
| `edition` | edição | `4. ed. atual.` |
| `booktitle` | obra que contém o ato | `Vade mecum` sai `In: VADE mecum.` |
| `journaltitle`, `journalsubtitle` | diário oficial e seção | `Diário Oficial da União`, `seção 1` |
| `volume` | ano do diário, **com a palavra** | `ano 139` |
| `number`, `pages` | número e páginas do diário | `8`, `1-74` |
| `location`, `publisher` | sem diário: local e responsável pela publicação | `Brasília, DF`, `Presidência da República` |
| `date` ou `year` | data da publicação; a inferida entre colchetes em `year`, com `sortyear` | `year = {[2016]}` |
| `pagetotal`, `note` | descrição física | `320`, `1 CD-ROM (p. 1-90)` |
| `complementos` | retificação, alteração, revogação, projeto de origem, assunto | `PL 634/1975` |
| `url`, `urldate`, `doi` | acesso online | |

Com `journaltitle`, a publicação sai como no diário oficial
(`Diário Oficial da União: seção 1, Brasília, DF, ano 139, n. 8, p. 1-74, 11 jan. 2002.`).
Sem ele, sai `local: editora, data.`

Escolhas que a norma não fixa:

- **`volume` como `ano 139`.** É a convenção do upstream: o campo guarda o
  rótulo junto com o número. O exemplo 5 de 7.11.5 traz `v. 22` e sai com
  `volume = {22}`.
- **Complementos antes do acesso online.** A 6023 não traz exemplo com os
  dois. Aqui, `Disponível em` fecha a referência, como nos demais documentos
  online. O upstream punha o `addendum` depois da URL.

`@jurisdiction` continua no driver de artigo do upstream até o Sprint 5.

## Desenvolvimento

- `desenvolvimento/sondagem/`: a sondagem que mediu o upstream (exemplos da 2018);
- `desenvolvimento/corpus/`: os exemplos das duas normas como corpus de teste,
  extraídos por `extrair.py`; o `.bib` das seções da trilha, o medidor
  `medir.py` e a tabela de divergências, `DIVERGENCIAS.md`
  (`python3 <script> --help`).

Medir o estilo, a partir de `desenvolvimento/corpus/`:

```sh
TEXINPUTS="$(cd ../.. && pwd)//:" python3 medir.py trilha-6023.bib --estilo crpsp-abnt
```
