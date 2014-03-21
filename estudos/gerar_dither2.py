"""
<svg xmlns="http://www.w3.org/2000/svg">
<!--cores: verde = #ABD56C  azul = #21C2ED-->
    <rect fill="red" stroke="none" x="0" y="0" width="5" height="5" />
</svg>

"""

import xml.etree.ElementTree as ET
import atkinson

VERDE = '#ABD56C'
AZUL = '#21C2ED'


def construir_padrao(svg, pixels, larg_total, colunas):
    larg_cel = int(larg_total / colunas)
    alt_cel = larg_cel
    g = ET.SubElement(svg, 'g')
    g.set('stroke', 'none')
    margem = int((len(pixels[0]) - colunas) / 2)
    for i, lin in enumerate(pixels):
        for j, pixel in enumerate(lin[margem:margem+colunas]):
            r = ET.SubElement(g, 'rect')
            x = j * larg_cel
            y = i * alt_cel
            cor = AZUL if pixel else VERDE
            r.attrib = dict(fill=cor, x=str(x), y=str(y),
                            width=str(larg_cel*1.08), height=str(alt_cel*1.08))


def gerar_svg(linhas):
    svg = ET.Element('svg')
    svg.set('xmlns', 'http://www.w3.org/2000/svg')
    pixels = atkinson.make_bitmap(linhas)
    largura = 60  # largura em pixels
    colunas = 24  # numero de fat bits por linha
    construir_padrao(svg, pixels, largura, colunas)
    ET.dump(svg)
    

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        linhas = int(sys.argv[1])
    else:
        linhas = 100
    gerar_svg(linhas)
