import pygame


class Items_DMG:
    def __init__(self, name, dmg, x, y):
        self.name = name
        self.dmg = dmg
        self.image = pygame.transform.scale(pygame.image.load('../Data/items/flashlight.png'), (110, 110))
        self.sell_x = x
        self.sell_y = y

