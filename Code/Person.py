import random
import Data.person_data


"""Имена и фамилии"""
NAME_M_LIST = Data.person_data.names_m
NAME_D_LIST = Data.person_data.names_d
SURNAME = random.choice(Data.person_data.surname)

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


class Mom:
    def set_name(self):
        self.name = random.choice(NAME_D_LIST)
        return self.name

    def set_surname(self):
        self.surname = SURNAME
        return self.surname

    def set_age(self):
        self.age = random.randint(20, 55)
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
        self.name, self.surname, self.age = Mom.set_name(self), Mom.set_surname(self), Mom.set_age(self)
        self.special, self.skills = Mom.set_special(self), set()
        self.buff, self.de_buff = Mom.set_buff(self), Mom.set_de_buff(self)
        """значения"""
        self.control, self.hunger, self.water = LIMIT_CONTROL, LIMIT_HUNGER, LIMIT_WATER
        self.hp, self.stress = LIMIT_HP, random.randint(0, 30)


class Dad:
    def set_name(self):
        self.name = random.choice(NAME_M_LIST)
        return self.name

    def set_surname(self):
        self.surname = SURNAME
        return self.surname

    def set_age(self):
        self.age = random.randint(22, 60)
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
        self.name, self.surname, self.age = Dad.set_name(self), Dad.set_surname(self), Dad.set_age(self)
        self.special, self.skills = Dad.set_special(self), set()
        self.buff, self.de_buff = Dad.set_buff(self), Dad.set_de_buff(self)
        """значения"""
        self.control, self.hunger, self.water = LIMIT_CONTROL, LIMIT_HUNGER, LIMIT_WATER
        self.hp, self.stress = LIMIT_HP, random.randint(0, 30)


class Son:
    def set_name(self):
        self.name = random.choice(NAME_M_LIST)
        return self.name

    def set_surname(self):
        self.surname = SURNAME
        return self.surname

    def set_age(self, mam):
        temp = [1, mam - 19]
        self.age = random.randint(*temp)
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

    def __init__(self, age_mom):
        """данные"""
        self.name, self.surname = Son.set_name(self), Son.set_surname(self)
        self.age = Son.set_age(self, age_mom)
        self.special, self.skills = Son.set_special(self), set()
        self.buff, self.de_buff = Son.set_buff(self), Son.set_de_buff(self)
        """значения"""
        self.control, self.hunger, self.water = LIMIT_CONTROL, LIMIT_HUNGER, LIMIT_WATER
        self.hp, self.stress = LIMIT_HP, random.randint(0, 20)


class Daughter:
    def set_name(self):
        self.name = random.choice(NAME_D_LIST)
        return self.name

    def set_surname(self):
        self.surname = SURNAME
        return self.surname

    def set_age(self, mam):
        temp = [1, mam - 19]
        self.age = random.randint(*temp)
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

    def __init__(self, age_mom):
        """данные"""
        self.name, self.surname = Daughter.set_name(self), Daughter.set_surname(self)
        self.age = Daughter.set_age(self, age_mom)
        self.special, self.skills = Daughter.set_special(self), set()
        self.buff, self.de_buff = Daughter.set_buff(self), Daughter.set_de_buff(self)
        """значения"""
        self.control, self.hunger, self.water = LIMIT_CONTROL, LIMIT_HUNGER, LIMIT_WATER
        self.hp, self.stress = LIMIT_HP, random.randint(0, 20)


class Data_pers:
    def __init__(self):
        self.mom = Mom()
        self.dad = Dad()
        self.son = Son(self.mom.age)
        self.dau = Daughter(self.mom.age)

    def info(self, pers=None):
        var = {'mom': self.mom, 'dad': self.dad, 'son': self.son, 'dau': self.dau}
        if pers is None:
            pers = input('Введите, чтобы получить статистику(mom, dad, dau, son). '
                         'Или нажмите {enter}, чтобы не выводить статисику.\n')
        if pers in ['mom', 'dad', 'son', 'dau']:
            v = (f'Статистика персонажа {pers}:\n\tИмя: {var[pers].name}\n\tФамилия: {var[pers].surname}\n\t'
                 f'Возраст: {var[pers].age}\n\tОсобенности:\n\t\t')
            v += '\n\t\t'.join([SPECIAL_BASE_PRINT[i] for i in list(var[pers].special)])
            v += f'\n\tУмения:\n\t\t{var[pers].skills}\n\tБафы:\n\t\t'
            v += '\n\t\t'.join([PERSON_EVENTS_PRINT[i] for i in list(var[pers].buff)])
            v += f'\n\tДебафы:\n\t\t{var[pers].de_buff}\n\tХП: {var[pers].hp}'
            v += f'\n\tКоличество еды: {var[pers].hunger}\n\tКоличество воды: {var[pers].water}\n\t'
            v += f'Контроль: {var[pers].control}\n\tСтресс: {var[pers].stress}'
            print(v)
        return ''

    def __repr__(self):
        Data_pers.info(self, 'mom')
        print('---------------')
        Data_pers.info(self, 'dad')
        print('---------------')
        Data_pers.info(self, 'son')
        print('---------------')
        Data_pers.info(self, 'dau')
        return '---------------'
