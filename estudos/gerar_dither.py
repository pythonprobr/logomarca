"""
<svg xmlns="http://www.w3.org/2000/svg">
<!--cores: verde = #ABD56C  azul = #21C2ED--> 
	<rect fill="red" stroke="none" x="0" y="0" width="5" height="5" />
</svg>

"""

import xml.etree.ElementTree as ET

larg_total = 60
colunas = 15
linhas = 22
larg_cel = int(larg_total / colunas)
alt_cel = larg_cel
verde = '#ABD56C'
azul = '#21C2ED'

svg = ET.Element('svg')
svg.set('xmlns', 'http://www.w3.org/2000/svg')
g = ET.SubElement(svg, 'g')
g.set('stroke', 'none')
for lin in range(linhas):
	for col in range(colunas):
		r = ET.SubElement(g, 'rect')
		x = col * larg_cel
		y = lin * alt_cel
		cor = azul if (lin+col) % 2 else verde
		r.attrib = dict(fill=cor, x=str(x), y=str(y), 
				width=str(larg_cel), height=str(alt_cel))

ET.dump(svg)
