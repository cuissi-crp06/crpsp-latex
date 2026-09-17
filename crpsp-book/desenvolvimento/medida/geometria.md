<!-- Gerado por geometria.py a partir de medidas-fontes.tsv.
     Não editar à mão: rodar `python3 geometria.py`. -->

# Geometria das classes, pelos critérios de 17/09

Aplica as [decisões de 17/09](../../briefings/decisoes-2026-09-17.md)
às medidas do motor. Corpo de 12 pt e entrelinha de 18 pt em todas as
linhas, como decidido.

## As fontes em disputa

| Fonte | mm/car. | Altura-x | RNIB | Largura relativa |
|---|---|---|---|---|
| Luciole | 2.0874 | 2.299 mm | minimo | — |
| NEWJUNE-Regular | 2.0149 | 2.294 mm | minimo | -3.5% |
| NEWJUNE-Serif | 2.0055 | 2.142 mm | minimo | -3.9% |
| Atkinson | 1.8778 | 2.092 mm | minimo | -10.0% |
| Lora | 1.9611 | 2.109 mm | minimo | -6.1% |

Largura relativa à Luciole. **Fonte mais estreita = mais margem externa com o mesmo número de caracteres** — que é exatamente o que o critério da decoração pede.

## Por classe

### `cartilha`

A5. Sem Leg e sem listas aninhadas, o piso deixa de existir.

Papel 148×210 mm · margem vertical 18 mm · 27 linhas por página (entrelinha de 18 pt).

| Linha | Luciole<br>mancha / **externa** | NEWJUNE-Regular<br>mancha / **externa** | NEWJUNE-Serif<br>mancha / **externa** | Atkinson<br>mancha / **externa** | Lora<br>mancha / **externa** |
|---|---|---|---|---|---|
| 60 car. | 125 mm / **8 mm** ⚠️ | 121 mm / **12 mm** ⚠️ | 120 mm / **13 mm** ⚠️ | 113 mm / **20 mm** | 118 mm / **15 mm** |
| 55 car. | 115 mm / **18 mm** | 111 mm / **22 mm** | 110 mm / **23 mm** | 103 mm / **30 mm** | 108 mm / **25 mm** |
| 50 car. | 104 mm / **29 mm** | 101 mm / **32 mm** | 100 mm / **33 mm** | 94 mm / **39 mm** | 98 mm / **35 mm** |
| 45 car. | 94 mm / **39 mm** | 91 mm / **42 mm** | 90 mm / **43 mm** | 85 mm / **48 mm** | 88 mm / **45 mm** |
| 40 car. | 83 mm / **50 mm** | 81 mm / **52 mm** | 80 mm / **53 mm** | 75 mm / **58 mm** | 78 mm / **55 mm** |

Margem interna fixa em 15 mm. ⚠️ marca a linha em que a margem externa deixa de ser maior que a interna — abaixo dela o critério da decoração não se cumpre.

### `manual`

A4. Linha flexível de 45 a 80 caracteres.

Papel 210×297 mm · margem vertical 22 mm · 39 linhas por página (entrelinha de 18 pt).

| Linha | Luciole<br>mancha / **externa** | NEWJUNE-Regular<br>mancha / **externa** | NEWJUNE-Serif<br>mancha / **externa** | Atkinson<br>mancha / **externa** | Lora<br>mancha / **externa** |
|---|---|---|---|---|---|
| 80 car. | 167 mm / **23 mm** | 161 mm / **29 mm** | 160 mm / **30 mm** | 150 mm / **40 mm** | 157 mm / **33 mm** |
| 70 car. | 146 mm / **44 mm** | 141 mm / **49 mm** | 140 mm / **50 mm** | 131 mm / **59 mm** | 137 mm / **53 mm** |
| 65 car. | 136 mm / **54 mm** | 131 mm / **59 mm** | 130 mm / **60 mm** | 122 mm / **68 mm** | 127 mm / **63 mm** |
| 60 car. | 125 mm / **65 mm** | 121 mm / **69 mm** | 120 mm / **70 mm** | 113 mm / **77 mm** | 118 mm / **72 mm** |
| 50 car. | 104 mm / **86 mm** | 101 mm / **89 mm** | 100 mm / **90 mm** | 94 mm / **96 mm** | 98 mm / **92 mm** |
| 45 car. | 94 mm / **96 mm** | 91 mm / **99 mm** | 90 mm / **100 mm** | 85 mm / **105 mm** | 88 mm / **102 mm** |

Margem interna fixa em 20 mm. ⚠️ marca a linha em que a margem externa deixa de ser maior que a interna — abaixo dela o critério da decoração não se cumpre.

### `relatorio`

A4. Decoração nas margens superior e inferior: margem vertical de 35 mm de cada lado, e a lateral fica simétrica.

Papel 210×297 mm · margem vertical 35 mm · 35 linhas por página (entrelinha de 18 pt).

| Linha | Luciole<br>mancha / margem por lado | NEWJUNE-Regular<br>mancha / margem por lado | NEWJUNE-Serif<br>mancha / margem por lado | Atkinson<br>mancha / margem por lado | Lora<br>mancha / margem por lado |
|---|---|---|---|---|---|
| 80 car. | 167 mm / 22 mm | 161 mm / 24 mm | 160 mm / 25 mm | 150 mm / 30 mm | 157 mm / 27 mm |
| 75 car. | 157 mm / 27 mm | 151 mm / 29 mm | 150 mm / 30 mm | 141 mm / 35 mm | 147 mm / 31 mm |
| 70 car. | 146 mm / 32 mm | 141 mm / 34 mm | 140 mm / 35 mm | 131 mm / 39 mm | 137 mm / 36 mm |
| 65 car. | 136 mm / 37 mm | 131 mm / 40 mm | 130 mm / 40 mm | 122 mm / 44 mm | 127 mm / 41 mm |

