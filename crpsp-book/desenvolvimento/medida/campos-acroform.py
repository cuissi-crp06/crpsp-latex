#!/usr/bin/env python3
"""Lista os campos AcroForm de um PDF: nome, tipo, flags e retângulo.

Usado na lista de aceite do briefing-crpsp-formulario.md (§10): mede a largura
dos widgets (/Rect, em bp), confere /FT e /Ff e acusa nome (/T) duplicado.
Depende só do `mutool` (mupdf-tools). Largura em bp: 1 pt = 0,99626 bp.

Uso: python3 campos-acroform.py arquivo.pdf
"""
import re
import subprocess
import sys

pdf = sys.argv[1]


def show(caminho):
    return subprocess.run(['mutool', 'show', pdf, caminho],
                          capture_output=True, text=True).stdout


# /Fields pode ser array direto ou referência indireta (PDF com tagging).
bruto = show('trailer/Root/AcroForm/Fields')
if not re.search(r'\d+ 0 R', bruto):
    bruto = show('trailer/Root/AcroForm')
    bruto = re.search(r'/Fields \[(.*?)\]', bruto, re.S).group(1)
ids = re.findall(r'(\d+) 0 R', bruto)

print('obj\tnome\tFT\tFf\tx0\tx1\tlargura\ty0\ty1\taltura')
nomes = []
for i in ids:
    o = show(i)
    t = re.search(r'/T (<[0-9A-Fa-f]+>|\(.*?\))', o).group(1)
    nome = (bytes.fromhex(t.strip('<>')).decode('utf-16')
            if t.startswith('<') else t.strip('()'))
    ft = re.search(r'/FT /(\w+)', o)
    ff = re.search(r'/Ff (\d+)', o)
    r = [float(v) for v in
         re.search(r'/Rect \[\s*([-\d. ]+)\]', o).group(1).split()]
    nomes.append(nome)
    print(i, nome, ft.group(1) if ft else '-', ff.group(1) if ff else '-',
          r[0], r[2], round(r[2] - r[0], 2), r[1], r[3], round(r[3] - r[1], 2),
          sep='\t')
dup = sorted({n for n in nomes if nomes.count(n) > 1})
print(f'campos: {len(nomes)}; nomes duplicados: {dup if dup else "nenhum"}')
