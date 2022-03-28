try:
    import Image
except ImportError:
    from PIL import Image, ImageDraw
import random

image = Image.new('RGB', (400, 400), 'white')  # background image
draw = ImageDraw.Draw(image)  # this makes you draw on image
size = image.size
x = size[0] / 2
y = size[1] / 2
r = 100
leftUpPoint = (x - r, y - r)
rightDownPoint = (x + r, y + r)
twoPointList = [leftUpPoint, rightDownPoint]
draw.ellipse(twoPointList, fill=(0, 0, 0, 0))

buffer = random.randint(10, 50)
for i in range(size[0]):
    for j in range(size[1]):
        if i == x and j == y:
            draw.rectangle((i - 5, j - 5, i + 5, j + 5), fill=None, outline=None, width=buffer)   # middle
            draw.rectangle((i - r, j - 5, i - r, j + 5), fill=None, outline=None, width=buffer)   # top
            draw.rectangle((i - 5, j + r, i + 5, j + r), fill=None, outline=None, width=buffer)   # right
            draw.rectangle((i + r, j - 5, i + r, j + 5), fill=None, outline=None, width=buffer)   # bottom
            draw.rectangle((i - 5, j - r, i + 5, j - r), fill=None, outline=None, width=buffer)   # left


image.show()
