import sys, PIL.Image

img = PIL.Image.open(sys.argv[1])
img.convert('L') # L => grayscale according to
# http://svn.effbot.org/public/tags/pil-1.1.4/libImaging/Unpack.c

for y in range(img.size[1]):
    valor = img.getpixel((img.size[0]/2, y))
    print(valor[0])

img.show()
