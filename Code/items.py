import pygame


class Items_DMG:
    def __init__(self, way, name, dmg, x, y):
        # сначала x потом y
        self.variation_move = [[0, 1], [1, 1], [3, 1]]
        self.name = name
        self.dmg = dmg
        self.image = pygame.transform.scale(pygame.image.load(f'../Data/items/{way}'), (110, 110))
        self.sell_x = x
        self.sell_y = y

    def move(self, x, y, pers):
        temp = [pers.left_arm, pers.right_arm, 0, pers.back]
        for var in self.variation_move:
            if x == var[0] and y == var[1]:
                temp[x] = temp[self.sell_x]
                temp[self.sell_x] = None
                self.sell_x = x
                self.sell_y = y
                pers.left_arm, pers.right_arm, pers.back = temp[0], temp[1], temp[3]


class Items_small_object:
    def __init__(self, way, name, x, y):
        # сначала x потом y
        self.variation_move = [[0, 0], [1, 0], [2, 0], [3, 0]]
        self.name = name
        self.image = pygame.transform.scale(pygame.image.load(f'../Data/items/{way}'), (110, 110))
        self.sell_x = x
        self.sell_y = y

    def move(self, x, y, pers):
        for var in self.variation_move:
            if x == var[0] and y == var[1]:
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

