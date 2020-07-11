import pygame
import Code.Person


class Items_dmg:
    def __init__(self, way, name, dmg):
        # сначала x потом y
        self.variation_move = [[0, 1], [1, 1], [3, 1]]
        self.name = name
        self.dmg = dmg
        self.image = pygame.transform.scale(pygame.image.load(f'../Data/items/{way}'), (110, 110))

    def move(self, x, y):
        for i in self.variation_move:
            if i == [x, y]:
                return True
        return False

    def use(self, pers):
        print(self.name, 'юзнуть низя')
        return 'false', False

    def text(self):
        return [['Наносимый урон:', 860, 260], [f'{self.dmg}', 1108, 260]]


class Items_small_object:
    def __init__(self, way, name, action):
        # сначала x потом y
        self.print_text = {'fire': 'можно что-то поджечь'}
        self.variation_move = [[0, 0], [1, 0], [2, 0], [3, 0]]
        self.name = name
        self.action = action
        self.image = pygame.transform.scale(pygame.image.load(f'../Data/items/{way}'), (110, 110))

    def move(self, x, y):
        for i in self.variation_move:
            if i == [x, y]:
                return True
        return False

    def use(self, pers):
        if self.action == 'fire':
            return 'fire', True
        else:
            print(self.name, 'юзнуть низя')
        return 'false', False

    def text(self):
        return [['Действие:', 860, 260], [f'{self.print_text.get(self.action)}', 1015, 260]]


class Items_eat:
    def __init__(self, way, name, hunger):
        # сначала x потом y
        self.variation_move = [[0, 0], [1, 0], [2, 0], [3, 0]]
        self.name = name
        self.hunger = hunger
        self.image = pygame.transform.scale(pygame.image.load(f'../Data/items/{way}'), (110, 110))

    def move(self, x, y):
        for i in self.variation_move:
            if i == [x, y]:
                return True
        return False

    def use(self, pers):
        Code.Person.Action(pers).eat(self.hunger)  # прибавляем единицы из file_data
        return 'eat', True

    def text(self):
        return [['Питательность:', 860, 260], [f'{self.hunger}', 1100, 260]]


def item_add(name, *arg):
    if name == 'BACKPACK':
        return None
    elif name == 'SMALL_OBJECT':
        return Items_small_object(*arg)
    elif name == 'AXE' or name == 'SWORD':
        return Items_dmg(*arg)
    elif name == 'CANNED':
        return Items_eat(*arg)

