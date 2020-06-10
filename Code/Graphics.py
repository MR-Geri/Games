from PIL import Image, ImageFilter, ImageDraw


def blur():
    image = Image.open('../Data/menu.jpg')
    filtered = image.filter(ImageFilter.GaussianBlur(radius=2))
    return filtered.tobytes("raw", 'RGB')


def create():
    image = Image.new("RGB", (100, 100))
    temp = ImageDraw.Draw(image)
    temp.polygon(((0, 0), (0, 100), (100, 100), (100, 0)), "#FFFFFF")
    temp.polygon(((10, 10), (10, 90), (90, 90), (90, 10)), "#87CEEB")
    image.save('../Data/cell.jpg')


create()
