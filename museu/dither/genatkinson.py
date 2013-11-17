
"""
Generate Atkinson's dithering from solid white to 50% gray

http://en.wikipedia.org/wiki/Bill_Atkinson

Adapted from code from:

http://mike.teczno.com/img/atkinson.py
"""

HEIGHT = 100
WIDTH = HEIGHT

import sys, PIL.Image
from random import randrange

def paint_gradient(img, height):
	margin = (HEIGHT - height) / 2
	for y in range(margin, img.size[1]):
		for x in range(img.size[0]):
			# color = 255 - int(float(y) / HEIGHT * 255)
			color = int(float(y-margin) / (HEIGHT-margin*2) * 255)
			# color = color + (randrange(10)-5)  # add noise
			if color < 0: color = 0
			elif color > 255: color = 255
			img.putpixel((x, y), color)


def dither(img):
	threshold = 128*[0] + 128*[255]
	for y in range(img.size[1]):
		for x in range(img.size[0]):
			old = img.getpixel((x, y))
			new = threshold[old]
			err = (old - new) >> 3 # divide by 8
			img.putpixel((x, y), new)
			for nxy in [(x+1, y), (x+2, y), (x-1, y+1), (x, y+1), (x+1, y+1), (x, y+2)]:
				try:
					img.putpixel(nxy, img.getpixel(nxy) + err)
				except IndexError:
					pass


def reflect(img, flip=False):
	for y in range(img.size[1]/2):
		for x in range(img.size[0]):
			if flip:
				source_x = img.size[0]-1-x
			else:
				source_x = x 
			source_xy = (source_x, img.size[1]-1-y) 
			color = img.getpixel(source_xy)
			color = 255 - color
			img.putpixel((x, y), color)
			
			
def make_image(width, height, gradient_height):
	img = PIL.Image.new('L', (width, height), 0)
	paint_gradient(img, gradient_height)
	dither(img)
	reflect(img, flip=True)
	return img
	

if __name__=='__main__':
	import sys
	if len(sys.argv) > 1:
		gradient_height = int(sys.argv[1])
		assert gradient_height <= HEIGHT
	else:
		gradient_height = HEIGHT
	img = make_image(WIDTH, HEIGHT, gradient_height)
	img.show()
	#img.save('atk_%03d.gif' % gradient_height)
