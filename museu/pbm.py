"""
P1
# CREATOR: GIMP PNM Filter Version 1.1
60 22
1011111111111111111111111011111111111111111111111111111111111111011111
1101111111101111110111111101111111111011101101111011111110110111011011
...
"""

from array import array

def ler(arq):
	tipo = None
	largura = None
	pixels = []
	linha_logica = []
	for lin in arq:
		if lin.startswith('#'):
			continue
		lin = lin.rstrip()
		if tipo is None:
			tipo = lin
			assert tipo == 'P1', 'tipo tem que ser P1'
		elif largura is None:
			largura, altura = [int(s) for s in lin.split()]
		else:
			linha_logica.extend([int(c) for c in lin])
			while len(linha_logica) >= largura:
				pixels.append(array('B', linha_logica[:largura]))
				linha_logica = linha_logica[largura:]
	assert 0 == len(linha_logica), '0 != %d' % len(linha_logica)
	assert largura == len(pixels[0]), 'largura[0] %d != %d' % (largura, len(pixels[0]))
	assert largura == len(pixels[-1]), 'largura[-1] %d != %d' % (largura, len(pixels[-1]))
	assert altura == len(pixels), 'altura %d != %d' % (altura, len(pixels))
	return pixels
	
if __name__=='__main__':
	import sys
	with open(sys.argv[1]) as arq:
		print(ler(arq))
