
"""
Generate Atkinson's dithering for linear gradient
from solid white to solid black

http://en.wikipedia.org/wiki/Bill_Atkinson

dither function adapted from code from:

http://mike.teczno.com/img/atkinson.py
"""

from array import array

HEIGHT = 100
WIDTH = HEIGHT


def paint_gradient(img, height):
    margin = (HEIGHT - height) / 2
    for y in range(margin, img.size[1]):
        for x in range(img.size[0]):
            # color = 255 - int(float(y) / HEIGHT * 255)
            color = int(float(y-margin) / (HEIGHT-margin*2) * 255)
            # color = color + (randrange(10)-5)  # add noise
            if color < 0:
                color = 0
            elif color > 255:
                color = 255
            img.putpixel((x, y), color)


def dither(img):
    threshold = 128*[0] + 128*[255]
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            old = img.getpixel((x, y))
            new = threshold[old]
            err = (old - new) >> 3  # divide by 8
            img.putpixel((x, y), new)
            for nxy in [(x+1, y), (x+2, y), (x-1, y+1),
                        (x, y+1), (x+1, y+1), (x, y+2)]:
                try:
                    color = img.getpixel(nxy) + err
                    img.putpixel(nxy, color)
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


class Bitmap(object):
    '''not a PIL.image, but implements putpixel and getpixel like one'''

    def __init__(self, width, height):
        self.bits = [array('I', [0] * width) for row in range(height)]
        
    @property
    def size(self):
        return (len(self.bits[0]), len(self.bits))

    def putpixel(self, xy, value):
        x, y = xy
        self.bits[y][x] = value

    def getpixel(self, xy):
        x, y = xy
        return self.bits[y][x]

    def flattened(self):
        for row in self.bits:
            for pixel in row:
                yield pixel

    def __getitem__(self, i):
        return self.bits[i]

    def __len__(self):
        return len(self.bits)

    def trim(self):
        trimmed = []
        for row in self.bits:
            total = sum(row)
            #print row[0], total
            if total == len(row)*row[0]:
                continue  # ignore rows where all pixels are equal
            trimmed.append(row)
        self.bits = trimmed


def make_bitmap(gradient_height, width=WIDTH, height=HEIGHT):
    assert gradient_height >= 3, 'minimum gradient_height is 3'
    bitmap = Bitmap(width, height)
    paint_gradient(bitmap, gradient_height)
    dither(bitmap)
    reflect(bitmap, flip=True)
    bitmap.trim()
    return bitmap


def make_image(gradient_height):
    import PIL.Image
    bitmap = make_bitmap(gradient_height)
    img = PIL.Image.new('L', bitmap.size, 0)
    img.putdata(list(bitmap.flattened()))
    return img


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        gradient_height = int(sys.argv[1])
        assert gradient_height <= HEIGHT
    else:
        gradient_height = HEIGHT
    img = make_image(gradient_height)
    img.show()
    #img.save('atk_%03d.gif' % gradient_height)
