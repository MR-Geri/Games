from PIL import Image, ImageFilter, ImageDraw
import random


def blur():
    image = Image.open('../Data/menu.jpg')
    filtered = image.filter(ImageFilter.GaussianBlur(radius=2))
    return filtered.tobytes("raw", 'RGB')


def create(figure, quantity=5):
    i = 1
    image = Image.new("RGB", (120 * i, 120 * i))
    temp = ImageDraw.Draw(image)
    if figure == 'квадрат':
        temp.polygon(((0 * i, 0 * i), (0 * i, 120 * i), (120 * i, 120 * i), (120 * i, 0 * i)), "#000000")
        temp.polygon(((5 * i, 5 * i), (5 * i, 115 * i), (115 * i, 115 * i), (115 * i, 5 * i)), "#FFFFFF")
        color = '#{:06x}'.format(random.randint(0, 256 ** 3))
        temp.polygon(((10 * i, 10 * i), (10 * i, 110 * i), (110 * i, 110 * i), (110 * i, 10 * i)), color)
        image.save(f'../Data/data_sell/cell_{quantity}.jpg')
        temp.ellipse((50 * i, 50 * i, 70 * i, 70 * i), fill='red', outline='red')
        image.thumbnail((120, 120), Image.ANTIALIAS)
        image.save(f'../Data/data_sell/cell_ellipse_{quantity}.jpg')
    elif figure == 'круг':
        temp.ellipse((30, 30, 90, 90), fill='red', outline='blue')
        image.save(f'../Data/ellipse.png')
