# crpsp-abnt

Estilo biblatex que estende o `biblatex-abnt` para a ABNT NBR 6023:2025 e a
NBR 10520:2023: documento jurídico (legislação, jurisprudência, ato
administrativo), citação autor-data acessível e mídia contemporânea.

**Estado:** Sprint 0 da trilha do piloto feito, sem código do estilo. O plano, a linha de
base medida e as decisões estão em
[`briefings/briefing-crpsp-abnt.md`](briefings/briefing-crpsp-abnt.md).

- `desenvolvimento/sondagem/`: a sondagem que mediu o upstream (exemplos da 2018);
- `desenvolvimento/corpus/`: os exemplos das duas normas como corpus de teste,
  extraídos por `extrair.py`; o `.bib` das seções da trilha, o medidor
  `medir.py` e a tabela de divergências do upstream, `DIVERGENCIAS.md`
  (`python3 <script> --help`).
