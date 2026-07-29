# Estado atual — ecossistema CRP acessível

Situação das linhas editoriais LaTeX do CRP-SP e pendências abertas que
atravessam mais de uma linha. Para a análise detalhada da linha `book`, ver
`README.md`; para os contornos de tagging com os MWEs que os reproduzem, ver
`skills/latex-dev/references/workarounds.md`.

**Última atualização:** 2026-07-29

---

## Linhas e situação

| Linha | Arquivos | Formato | Situação |
| --- | --- | --- | --- |
| `book` | `book-crpsp_acessivel.sty` | A5 livro | Produção |
| `guia` | `crpsp_acessivel.cls` + `guia-crpsp_acessivel.sty` | A5 | Desenvolvimento |
| `guia_visual` | `crpsp-guia_visual.cls` + `guia-visual.sty` | 16:9 | Implementada 2026-07-03 |
| `formulario` | `crpsp-formulario.cls` + `formulario.sty` | A4 AcroForm | Implementada |
| `relatorio` | `crpsp-relatorio.cls` + `relatorio.sty` | A4 retrato | Implementada 2026-07-29 |
| `livro` | — | — | Não iniciada |

Infraestrutura comum: `crpsp-base.sty` (verificação de engine, fontspec
condicional, paleta `cor1`/`cor2`/`cor3`). Compilação via podman, imagem
`crpsp-latex:dev` — ver `desenvolvimento/docker/README.md`.

---

## PENDÊNCIA 1 — migrar `testphase` para `tagging = on`

**Prioridade: alta.** É a única pendência que toca todas as linhas.

### O que aconteceu

Em resposta à issue que abrimos ([latex3/tagging-project#1484](https://github.com/latex3/tagging-project/issues/1484),
2026-07-14), David Carlisle:

> "you should not use the `testphase` key which was an earlier syntax
> predating the introduction of `tagging=on`"

A chave `testphase={phase-III,...}` — usada em praticamente todo o código e
toda a documentação deste workspace — é **sintaxe legada**.

### O que já foi verificado

Na imagem `crpsp-latex:dev` (TeX Live 2026), as duas sintaxes produzem
resultado **idêntico**: o relatório do Jornal Psi compila com as mesmas 12
páginas, os mesmos ~843 objetos de estrutura e zero erro de tagging com
`tagging=on` no lugar de `testphase={phase-III, table, firstaid}`.

Verificou-se também que o defeito do `tabularray` (WA-08) é igual nas duas
sintaxes — **não era artefato da chave legada**. Isso enfraquece a hipótese
de que outros workarounds do workspace sejam efeito colateral do `testphase`,
mas não a elimina para os workarounds que dependem de módulos nomeados.

### O que falta

- [ ] **Linha `book`** — a mais delicada. WA-01 e WA-02 dependem de módulos
      `latex-lab-testphase-sec-template` e `latex-lab-testphase-toc`
      **nomeados**; não se sabe se `tagging=on` os carrega sob outro nome nem
      se o `\TOCAcessivel` continua necessário. Agrava: o motor de referência
      histórico dessa linha é o `lualatex-dev` do MiKTeX/Windows, e a
      equivalência acima foi medida só no podman. **Recompilar nos dois
      motores e comparar a árvore de tags antes de migrar.**
- [ ] **Linha `guia`** (`crpsp_acessivel.cls`) — migrar e recompilar
      `guia-exemplo.tex`.
- [ ] **Linha `guia_visual`** — migrar e recompilar `exemplo-guia-visual.tex`.
      Atenção à navbar: ela depende de `\SuspendTagging`/`\ResumeTagging` e
      da pré-medição fora do `tikzpicture`; conferir se o comportamento se
      mantém.
- [ ] **Linha `formulario`** — migrar e recompilar `exemplo-formulario.tex`.
      Conferir os campos AcroForm, que interagem com o tagging.
- [ ] **Documentos de produção** em `production/editorial/publicacoes/*` que
      tragam o bloco antigo.
- [x] **Linha `relatorio`** — migrada em 2026-07-29 (commit `e9417f9`).
- [x] Documentação de referência (`SKILL.md`, `pdfua-checklist.md`,
      `workarounds.md`, `CLAUDE.md`) — atualizada com a ressalva de que a
      linha `book` ainda não foi reconferida.

### Como verificar cada migração

Trocar o bloco e recompilar duas vezes, comparando **antes e depois**:

```sh
# contagem de objetos de estrutura e erros de tagging
grep -oE "~[0-9]+ structure objects" <arquivo>.log | tail -1
grep -cE "not allowed|text-unit|^! |differ|open structure" <arquivo>.log
```

Resultado esperado: mesmo número de objetos de estrutura, zero erro. Qualquer
divergência é sinal de que a linha depende de um módulo `testphase-*`
específico — nesse caso, **parar e registrar aqui** em vez de forçar.

---

## PENDÊNCIA 2 — `tabularray` carregado em duas classes

**Prioridade: média.** Risco latente, não defeito ativo.

`crpsp_acessivel.cls` e `crpsp-guia_visual.cls` carregam `tabularray`, que
emite relações de tag inválidas no fecho de toda tabela (WA-08). Nenhuma
publicação daquelas linhas exercitou tabelas sob tagging até agora; a
primeira que exercitar vai esbarrar nisso sem aviso claro.

- [ ] Substituir por `tabular`/`longtable` + `\rowcolor`, como em
      `relatorio.sty` §7, ou remover a carga se as linhas não usarem tabelas.

---

## PENDÊNCIA 3 — cargas mortas e workarounds possivelmente vencidos

**Prioridade: baixa.** Higiene.

- [ ] `guia-visual.sty` carrega `tcolorbox[skins]` sem usar: a implementação
      migrou para `\parbox` justamente porque o `tcolorbox` não fica inline
      sob tagging. Manter a carga é risco sem contrapartida.
- [ ] O workaround "`enumitem` é proibido" pode estar **vencido**: o
      phase-III agora carrega `latex-lab-enumitem.sty` ("Emulating enumitem",
      v0.80f, 2026-04-21). Testar se as chaves de `\LegArtigo` voltam a
      funcionar. `crpsp_acessivel.cls` ainda carrega o `enumitem` real,
      contrariando o workaround — resolver os dois de uma vez.
- [ ] `monitor_ctan.py` teve última verificação registrada em 2026-05-09.
      Rodar antes de qualquer decisão sobre workarounds de tagging:
      `python3 monitor_ctan.py`

---

## Controle de versão

Esta pasta é um repositório git desde 2026-07-29 (commit inicial `c9d1450`).
O restante do workspace — inclusive `production/` e `skills/` — **não é
versionado**: alterações lá não têm histórico.

Consequência prática: o relatório do Jornal Psi
(`production/jornal/analise/latex/`) e a documentação em `skills/latex-dev/`
estão fora deste repositório, ainda que sejam parte do mesmo trabalho.
