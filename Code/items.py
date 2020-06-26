import pygame


class Items_DMG:
    def __init__(self, way, name, dmg, x, y):
        self.name = name
        self.dmg = dmg
        self.image = pygame.transform.scale(pygame.image.load(f'../Data/items/{way}'), (110, 110))
        self.sell_x = x
        self.sell_y = y


def item_add(name, *arg):
    if name == 'BACKPACK':
        return None
    elif name == 'SMALL_OBJECT':
        return None
    elif name == 'AXE':
        return Items_DMG(*arg)
    elif name == 'CANNED':
        return None
