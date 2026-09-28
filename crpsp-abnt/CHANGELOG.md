# Changelog do crpsp-abnt

Versões conforme `CONVENCAO-VERSIONAMENTO.md`, na raiz do repositório.

## 0.1.0-alfa — 2026-09-28

Sprint 1 da trilha do piloto: legislação e ato normativo.

- `crpsp-abnt.bbx`: driver próprio para `@legislation` e `@legal`. O upstream os
  mandava para o driver de `@article`. Com ele saem `local: editora` sem diário
  oficial, a edição, `Organizado por` e `In:` (linhas 4 e 5 de
  `desenvolvimento/corpus/DIVERGENCIAS.md`).
- `crpsp-abnt.dbx`: campos `ementa` e `complementos`. O corpus passou a usá-los
  no lugar de `titleaddon` e `addendum`.
- `crpsp-abnt.cbx`: só carrega o `abnt.cbx`.
- Medida: 53 de 107 referências iguais à norma (upstream: 44), sem regressão;
  chamadas inalteradas, 22 de 29. Uma amostra das seções 7.11 sob
  `tagging=on` passa no veraPDF UA-2.
