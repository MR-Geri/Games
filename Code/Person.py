import random
import Data.person_data


"""Имена и фамилии"""
NAME_M_LIST = Data.person_data.names_m
NAME_D_LIST = Data.person_data.names_d
SURNAME_LIST = Data.person_data.surname

"""Ивенты персонажей"""
PERSON_EVENTS = Data.person_data.PERSON_EVENTS
PERSON_EVENTS_PRINT = Data.person_data.PERSON_EVENTS_PRINT

"""Особенности персонажей"""
SPECIAL_BASE = Data.person_data.SPECIAL_BASE
SPECIAL_BASE_PRINT = Data.person_data.SPECIAL_BASE_PRINT

"""Основные параметры"""
LIMIT_CONTROL, LIMIT_STRESS = 100, 100
LIMIT_HP, LIMIT_HUNGER, LIMIT_WATER = 100, 100, 100
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
        print('Персонаж мёртв.')
        return False

    def eat(self, hunger):
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
            print(PERSON_EVENTS_PRINT['overeaten'])
            Action.add_de_buff(self, 'overeaten')
            self.pers.hunger = 100

    def left_hunger(self, hunger):
        if not Action.is_live(self):
            return False
        self.pers.hunger -= hunger
        if self.pers.hunger < 0:
            self.pers.damage(abs(self.pers.hunger))
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
        if self.pers.control < 0:
            self.pers.damage(int(0.5 * abs(self.pers.stress)))
            if Action.is_live(self) is False:
                print(f'Персонаж погиб из-за стресса.')
            self.pers.control = 0

    def relax(self, relax_points):
        if not Action.is_live(self):
            return False
        self.pers.control += relax_points
        # Лимит.
        self.pers.control = LIMIT_STRESS if self.pers.control > LIMIT_STRESS else self.pers.control

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
            print(f'{PERSON_EVENTS_PRINT[de_buffs]}')
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
        self.buff = set()
        return self.buff

    def __init__(self):
        """данные"""
        self.name, self.surname = Personage.set_name(self), Personage.set_surname(self)
        self.age = Personage.set_age(self)
        self.special, self.skills = Personage.set_special(self), set()
        self.buff, self.de_buff = Personage.set_buff(self), Personage.set_de_buff(self)
        """значения"""
        self.control, self.hunger, self.water = LIMIT_CONTROL, LIMIT_HUNGER, LIMIT_WATER
        self.hp, self.stress = LIMIT_HP, random.randint(0, 30)


class Data_pers:
    def __init__(self, flag=None):
        self.personalities = []
        flag = int(input('Сценарий:\n')) if flag is None else flag
        for i in range(flag):
            self.personalities.append(Personage())

    def info(self, pers=None):
        if pers is None:
            pers = int(input(f'Введите, чтобы получить статистику. Число от 0 до {len(self.personalities)}'
                             f' Или нажмите enter, чтобы не выводить статисику.\n'))
        if pers >= 0 or pers < len(self.personalities):
            v = (f'Статистика персонажа {pers}:\n\tИмя: {self.personalities[pers].name}\n\t'
                 f'Фамилия: {self.personalities[pers].surname}\n\t'
                 f'Возраст: {self.personalities[pers].age}\n\tОсобенности:\n\t\t')
            v += '\n\t\t'.join([SPECIAL_BASE_PRINT[i] for i in list(self.personalities[pers].special)])
            v += f'\n\tУмения:\n\t\t{self.personalities[pers].skills}\n\tБафы:\n\t\t'
            v += '\n\t\t'.join([PERSON_EVENTS_PRINT[i] for i in list(self.personalities[pers].buff)])
            v += f'\n\tДебафы:\n\t\t{self.personalities[pers].de_buff}\n\tХП: {self.personalities[pers].hp}'
            v += f'\n\tКоличество еды: {self.personalities[pers].hunger}\n\t' \
                 f'Количество воды: {self.personalities[pers].water}\n\t' \
                 f'Контроль: {self.personalities[pers].control}\n\tСтресс: {self.personalities[pers].stress}'
            print(v)
        return '---------------'

    def __repr__(self):
        for i in range(len(self.personalities)):
            print(Data_pers.info(self, i))
        return ''
