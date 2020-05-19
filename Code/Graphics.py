from PIL import Image, ImageFilter


def blur():
    image = Image.open('../Data/menu.jpg')
    filtered = image.filter(ImageFilter.GaussianBlur(radius=5))
    return filtered.tobytes("raw", 'RGB')
