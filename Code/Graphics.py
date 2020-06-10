from PIL import Image, ImageFilter, ImageDraw
import random


def blur():
    image = Image.open('../Data/menu.jpg')
    filtered = image.filter(ImageFilter.GaussianBlur(radius=2))
    return filtered.tobytes("raw", 'RGB')


def create():
    image = Image.new("RGB", (120, 120))
    temp = ImageDraw.Draw(image)
    temp.polygon(((0, 0), (0, 120), (120, 120), (120, 0)), "#000000")
    temp.polygon(((5, 5), (5, 115), (115, 115), (115, 5)), "#FFFFFF")
    for i in range(5):
        color = '#{:06x}'.format(random.randint(0, 256 ** 3))
        temp.polygon(((10, 10), (10, 110), (110, 110), (110, 10)), color)
        image.save(f'../Data/data_sell/cell_{i}.jpg')
