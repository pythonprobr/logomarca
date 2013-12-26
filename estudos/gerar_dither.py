"""
<svg xmlns="http://www.w3.org/2000/svg">
<!--cores: verde = #ABD56C  azul = #21C2ED-->
    <rect fill="red" stroke="none" x="0" y="0" width="5" height="5" />
</svg>

"""

import xml.etree.ElementTree as ET
import atkinson
import webbrowser
import os

VERDE = '#ABD56C'
AZUL = '#21C2ED'


def construir_padrao(svg, pixels, larg_total, colunas):
    larg_cel = int(larg_total / colunas)
    alt_cel = larg_cel
    g = ET.SubElement(svg, 'g')
    g.set('stroke', 'none')
    for i, lin in enumerate(pixels):
        for j, pixel in enumerate(lin[10:10+colunas]):
            r = ET.SubElement(g, 'rect')
            x = j * larg_cel
            y = i * alt_cel
            cor = VERDE if pixel else AZUL
            r.attrib = dict(fill=cor, x=str(x), y=str(y),
                            width=str(larg_cel*1.08), height=str(alt_cel*1.08))


if __name__ == '__main__':
    larg_total = 60
    colunas = 20
    linhas = 22
    pixels = atkinson.make_bitmap(100, 100, 40)
    #print(pixels.bits)
    #print(pixels.size)
    svg = ET.Element('svg')
    svg.set('xmlns', 'http://www.w3.org/2000/svg')
    construir_padrao(svg, pixels, 60, 12)
    with open('saida.svg', 'wb') as saida:
        saida.write(ET.tostring(svg, encoding='utf-8'))
        print(os.path.abspath(saida.name))
        #webbrowser.open('file://'+os.path.abspath(saida.name))
