import random
import Data.file_data


"""Имена и фамилии"""
NAME_M_LIST = Data.file_data.names_m
NAME_D_LIST = Data.file_data.names_d
SURNAME_LIST = Data.file_data.surname

"""Бафы и дебафы персонажей"""
PERSON_EVENTS = Data.file_data.PERSON_EVENTS
PERSON_EVENTS_PRINT = Data.file_data.PERSON_EVENTS_PRINT

"""Особенности персонажей"""
SPECIAL_BASE = Data.file_data.SPECIAL_BASE
SPECIAL_BASE_PRINT = Data.file_data.SPECIAL_BASE_PRINT

"""Основные параметры"""
number_x_y = (4, 3)
LIMIT_STRESS = 100
LIMIT_HP, LIMIT_HUNGER, LIMIT_WATER = 100, 100, 100
DMG_START = 15
LIMIT_BUFF, LIMIT_DE_BUFF = 3, 3
LIMIT_SPECIAL = 3


class Action:
    def __init__(self, pers):
        self.pers = pers

    def damage(self, dmg):
        if not Action.is_live(self):
            return False
        self.pers.hp -= dmg
        # Лимит.
        self.pers.hp = 0 if self.pers.hp < 0 else self.pers.hp

    def is_live(self):
        if self.pers.hp > 0:
            return True
        return False

    def eat(self, hunger):
        print('Кушаем...')
        if not Action.is_live(self):
            return False
        self.pers.hunger += hunger
        # Лимит.
        if self.pers.hunger > 60 and (self.pers.hunger < 100):
            # сытость
            print(PERSON_EVENTS_PRINT['full_eat'])
            Action.add_buff(self, 'full_eat')
        elif self.pers.hunger > 100:
            # объелся
            Action.add_de_buff(self, 'overeaten')
            self.pers.hunger = 100

    def left_hunger(self, hunger):
        if not Action.is_live(self):
            return False
        self.pers.hunger -= hunger
        if self.pers.hunger < 0:
            Action(self.pers).damage(abs(self.pers.hunger * 20))
            if Action.is_live(self) is False:
                print(f'Персонаж погиб из-за голода.')
            self.pers.hunger = 0

    def drink(self, water):
        if not Action.is_live(self):
            return False
        self.pers.water += water
        # Лимит.
        self.pers.water = LIMIT_WATER if self.pers.water > LIMIT_WATER else self.pers.water

    def left_water(self, water):
        if not Action.is_live(self):
            return False
        self.pers.water -= water
        if self.pers.water < 0:
            self.pers.damage(2 * abs(self.pers.water))
            if Action.is_live(self) is False:
                print(f'Персонаж погиб из-за жажды.')
            self.pers.water = 0

    def get_stress(self, stress_points):
        if not Action.is_live(self):
            return False
        self.pers.stress -= stress_points
        if self.pers.stress > 100:
            self.pers.damage(int(0.5 * abs(self.pers.stress)))
            if Action.is_live(self) is False:
                print(f'Персонаж погиб из-за стресса.')
            self.pers.stress = 100

    def relax(self, relax_points):
        if not Action.is_live(self):
            return False
        self.pers.stress -= relax_points
        # Лимит.
        self.pers.stress = LIMIT_STRESS if self.pers.stress > LIMIT_STRESS else self.pers.stress

    def add_buff(self, buffs):
        if not Action.is_live(self):
            return False
        if len(self.pers.buff) < LIMIT_BUFF:
            self.pers.buff.add(buffs)
        else:
            print('Количество бафов максимально')

    def add_de_buff(self, de_buffs):
        if not Action.is_live(self):
            return False
        if len(self.pers.de_buff) < LIMIT_DE_BUFF:
            self.pers.de_buff.add(de_buffs)
            print(f'Дебафф добавлен: {PERSON_EVENTS_PRINT[de_buffs]}')
        else:
            print('Количество дебафов максимально')


class Personage:
    def set_name(self):
        self.name = random.choice(NAME_D_LIST)
        return self.name

    def set_surname(self):
        self.surname = random.choice(SURNAME_LIST)
        return self.surname

    def set_age(self):
        self.age = random.randint(18, 55)
        return self.age

    def set_special(self):
        temp = list(SPECIAL_BASE)
        self.special = set()
        for _ in range(LIMIT_SPECIAL):
            spec_group = random.choice(temp)
            temp.remove(spec_group)
            self.special.add(random.choice(spec_group))
        return self.special

    def set_buff(self):
        self.buff = set()
        self.buff.add('full_eat')
        return self.buff

    def set_de_buff(self):
        self.de_buff = set()
        self.de_buff.add('fracture')
        return self.de_buff

    def __init__(self):
        """Характеристика"""
        self.name, self.surname = Personage.set_name(self), Personage.set_surname(self)
        self.age = Personage.set_age(self)
        self.dmg = DMG_START
        self.special, self.skills = Personage.set_special(self), set()
        self.buff, self.de_buff = Personage.set_buff(self), Personage.set_de_buff(self)
        """значения"""
        self.number_x_y = number_x_y
        self.hunger, self.water = LIMIT_HUNGER, LIMIT_WATER
        self.hp, self.stress = LIMIT_HP, random.randint(0, 30)
        """Инвентарь"""
        self.head = self.body = self.legs = self.feet = None
        self.pockets = [None, None, None, None]
        self.left_arm, self.right_arm, self.back, self.belt = None, None, None, None


class Data_pers:
    def __init__(self):
        """Создание наборов для персонажей"""
        self.personage = Personage()
        #  добавление предметов в инвентарь
        data = Data.file_data
        # Оружие
        self.personage.right_arm = data.AXE[0]
        # Предметы
        self.personage.pockets[0] = data.SMALL_OBJECT[1]
        # Еда
        self.personage.pockets[1] = data.CANNED[2]
        self.personage.pockets[2] = data.CANNED[3]

    def info(self):
        special = 'нет' if self.personage.special == set() else \
            '\n\t\t'.join([SPECIAL_BASE_PRINT[i] for i in list(self.personage.special)])
        skills = 'нет' if self.personage.skills == set() else \
            '\n\t\t'.join([SPECIAL_BASE_PRINT[i] for i in list(self.personage.skills)])
        buff = 'нет' if self.personage.buff == set() else \
            '\n\t\t'.join([PERSON_EVENTS_PRINT[i] for i in list(self.personage.buff)])
        de_buff = 'нет' if self.personage.skills == set() else \
            '\n\t\t'.join([PERSON_EVENTS_PRINT[i] for i in list(self.personage.de_buff)])

        left_arm = 'пусто' if self.personage.left_arm is None else self.personage.left_arm[1]
        right_arm = 'пусто' if self.personage.right_arm is None else self.personage.right_arm[1]
        back = 'пусто' if self.personage.back is None else self.personage.back[1]
        belt = 'пусто' if self.personage.belt is None else self.personage.belt[1]
        backpack = False
        if type(back) == list:
            backpack = [i[1] for i in self.personage.back[2][1:]] if back != 'пусто' else False
            backpack = ', '.join(backpack) if backpack is not False else False
        temp = []
        for i in self.personage.pockets:
            if i is not None:
                temp.append(i[1])
        pockets = ''.join(['пусто'] if ''.join([i for i in temp]) == '' else
                          [', '.join([i for i in temp])])
        print(f'{self.personage.name} {self.personage.surname}:\n\tВозраст: {self.personage.age}\n\t'
              f'Здоровье: {self.personage.hp}\n\tКоличество еды: {self.personage.hunger}\n\t'
              f'Воды: {self.personage.water}\n\t'
              f'Стресс: {self.personage.stress}\n\tОсобенности:\n\t\t{special}'
              f'\n\tУмения:\n\t\t{skills}\n\tБафы:\n\t\t{buff}\n\tДебафы:\n\t\t{de_buff}\n\t'
              f'В левой руке {left_arm}.\n\tВ правой руке {right_arm}.'
              f'\n\tЗа спиной {back}.\n\tНа поясе {belt}.\n\tВ карманах {pockets}.')
        if backpack is not False:
            print(f'\tВ {Data.file_data.BACKPACK_PRINT[back]} находятся {backpack}.')
        return '---------------'

    def __repr__(self):
        print(Data_pers.info(self))
        return ''
