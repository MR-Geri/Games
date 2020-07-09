import pygame
import Code.Person


class Items_dmg:
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

    def use(self, pers):
        print(self.name, 'юзнуть низя')
        return 'false', False

    def dell(self, pers):
        temp = [pers.left_arm, pers.right_arm, 0, pers.back]
        temp[self.sell_x] = None
        pers.left_arm, pers.right_arm, pers.back = temp[0], temp[1], temp[3]
        print('Предмет выброшен')

    def text(self):
        return [['Наносимый урон:', 860, 260], [f'{self.dmg}', 1108, 260]]


class Items_small_object:
    def __init__(self, way, name, action, x, y):
        # сначала x потом y
        self.print_text = {'fire': 'можно что-то поджечь'}
        self.variation_move = [[0, 0], [1, 0], [2, 0], [3, 0]]
        self.name = name
        self.action = action
        self.image = pygame.transform.scale(pygame.image.load(f'../Data/items/{way}'), (110, 110))
        self.sell_x = x
        self.sell_y = y

    def move(self, x, y, pers):
        pockets = [pers.pockets[0], pers.pockets[1], pers.pockets[2], pers.pockets[3]]
        for var in self.variation_move:
            if x == var[0] and y == var[1]:
                pockets[x] = pockets[self.sell_x]
                pockets[self.sell_x] = None
                self.sell_x = x
                self.sell_y = y
                pers.pockets[0], pers.pockets[1], pers.pockets[2], pers.pockets[3] = pockets

    def use(self, pers):
        if self.action == 'fire':
            pers.pockets[self.sell_x] = None
            print('Спички использованы')
            return 'fire', True
        else:
            print(self.name, 'юзнуть низя')
        return 'false', False

    def dell(self, pers):
        pers.pockets[self.sell_x] = None
        print('Предмет выброшен')

    def text(self):
        return [['Действие:', 860, 260], [f'{self.print_text.get(self.action)}', 1015, 260]]


class Items_eat:
    def __init__(self, way, name, hunger, x, y):
        # сначала x потом y
        self.variation_move = [[0, 0], [1, 0], [2, 0], [3, 0]]
        self.name = name
        self.hunger = hunger
        self.image = pygame.transform.scale(pygame.image.load(f'../Data/items/{way}'), (110, 110))
        self.sell_x = x
        self.sell_y = y

    def move(self, x, y, pers):
        pockets = [pers.pockets[0], pers.pockets[1], pers.pockets[2], pers.pockets[3]]
        for var in self.variation_move:
            if x == var[0] and y == var[1]:
                pockets[x] = pockets[self.sell_x]
                pockets[self.sell_x] = None
                self.sell_x = x
                self.sell_y = y
                pers.pockets[0], pers.pockets[1], pers.pockets[2], pers.pockets[3] = pockets

    def use(self, pers):
        pockets = [pers.pockets[0], pers.pockets[1], pers.pockets[2], pers.pockets[3]]
        Code.Person.Action(pers).eat(pockets[self.sell_x][2])  # прибавляем единицы из file_data
        pockets[self.sell_x] = None
        pers.pockets[0], pers.pockets[1], pers.pockets[2], pers.pockets[3] = pockets
        return 'eat', True

    def dell(self, pers):
        pers.pockets[self.sell_x] = None
        print('Предмет выброшен')

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

