import pygame


class Items_DMG:
    def __init__(self, way, name, dmg, x, y):
        self.name = name
        self.dmg = dmg
        self.image = pygame.transform.scale(pygame.image.load(f'../Data/items/{way}'), (110, 110))
        self.sell_x = x
        self.sell_y = y

    def move(self, x, y):
        self.sell_y = y
        self.sell_x = x


class Items_small_object:
    def __init__(self, way, name, x, y):
        self.name = name
        self.image = pygame.transform.scale(pygame.image.load(f'../Data/items/{way}'), (110, 110))
        self.sell_x = x
        self.sell_y = y

    def move(self, x, y):
        self.sell_y = y
        self.sell_x = x


def item_add(name, *arg):
    if name == 'BACKPACK':
        return None
    elif name == 'SMALL_OBJECT':
        return Items_small_object(*arg)
    elif name == 'AXE':
        return Items_DMG(*arg)
    elif name == 'CANNED':
        return None

