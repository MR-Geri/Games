import random
import time
import Data.Persons_data


"""Имена и фамилии"""
NAME_M_LIST = Data.Persons_data.names_m
NAME_D_LIST = Data.Persons_data.names_d
SURNAME = random.choice(Data.Persons_data.surname)

"""Ивенты персонажей"""
PERSON_EVENTS = ['fracture']
PERSON_EVENTS_PRINT = Data.Persons_data.PERSON_EVENTS_PRINT

"""Особенности персонажей"""
SPECIAL_BASE = [['smart', 'stupid'], ['light sleep'], ['strong', 'frail'], ['glutton']]
SPECIAL_BASE_PRINT = Data.Persons_data.SPECIAL_BASE_PRINT

"""Основные параметры"""
RAND_SEED = random.randint(0, 100)
LIMIT_CONTROL, LIMIT_STRESS = 100, 100
LIMIT_HP, LIMIT_HUNGER, LIMIT_WATER = 100, 100, 100
LIMIT_BUFF, LIMIT_DE_BUFF = 3, 3
LIMIT_SPECIAL = 3
TIME_SECONDS = 2


class Person:
    """ Персонажи. """

    def __init__(self, name: str = 'Имя', surname: str = 'фамилия', age: int = 0,
                 special: set = set(), skills: set = set(), buff: set = set(), de_buff: set = set()):
        """ Конструктор. """
        self.name, self.surname, self.age = name, surname, age
        self.control,  self.hunger, self.water = LIMIT_CONTROL, LIMIT_HUNGER, LIMIT_WATER
        self.hp, self.stress = LIMIT_HP, LIMIT_STRESS
        self.skills, self.special = skills, special
        self.buff, self.de_buff = buff, de_buff
        self.temp = []

    def damage(self, dmg):
        """ Урон. """
        self.hp -= dmg
        # Лимит.
        self.hp = 0 if self.hp < 0 else self.hp

    def eat(self, hunger):
        """ Есть. """
        self.hunger += hunger
        # Лимит.
        if self.hunger > 60 and (self.hunger < 100):
            # сытость
            print(PERSON_EVENTS_PRINT['full_eat'])
            Person.add_buff(self, 'full_eat')
        elif self.hunger > 100:
            # объелся
            print(PERSON_EVENTS_PRINT['overeaten'])
            Person.add_de_buff(self, 'overeaten')
            self.hunger = 100

    def left_hunger(self, hunger):
        """ Голодать. """
        self.hunger -= hunger
        if self.hunger < 0:
            self.damage(abs(self.hunger))
            if Person.is_live(self) is False:
                print(f'Персонаж погиб в результате голода.')
            self.hunger = 0

    def drink(self, water):
        """ Пить."""
        self.water += water
        # Лимит.
        self.water = self.WATER_LIMIT if self.water > self.WATER_LIMIT else self.water

    def left_water(self, water):
        """ Жажда. """
        self.water -= water
        if self.water < 0:
            self.damage(2 * abs(self.water))
            if Person.is_live(self) is False:
                print(f'Персонаж погиб в результате жажды.')
            self.water = 0

    def get_stress(self, stress_points):
        """ Стресс. """
        self.stress -= stress_points
        if self.control < 0:
            self.damage(int(0.5 * abs(self.stress)))
            if Person.is_live(self) is False:
                print(f'Персонаж погиб в результате стресса.')
            self.control = 0

    def relax(self, relax_points):
        """ Отдых. """
        self.control += relax_points
        # Лимит.
        self.control = self.STRESS_LIMIT if self.control > self.STRESS_LIMIT else self.control

    def add_buff(self, buffs):
        """ Добавление бафа. """
        if len(self.buff) < LIMIT_BUFF:
            self.buff.append(buffs)
        else:
            print('Количество бафов максимально')

    def add_de_buff(self, de_buffs):
        """ Добавление дебафа."""
        if len(self.de_buff) < LIMIT_DE_BUFF:
            self.de_buff.add(de_buffs)
            print(f'{PERSON_EVENTS_PRINT[de_buffs]}')
        else:
            print('Количество дебафов максимально')


class Mom(Person):
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
        self.name, self.surname, self.age = Mom.set_name(self), Mom.set_surname(self), Mom.set_age(self)
        self.special, self.skills = Mom.set_special(self), set()
        self.buff, self.de_buff = Mom.set_buff(self), Mom.set_de_buff(self)
        super().__init__(self.name, self.surname, self.age, self.special, self.skills, self.buff, self.de_buff)


class Dad(Person):
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
        self.name, self.surname, self.age = Dad.set_name(self), Dad.set_surname(self), Dad.set_age(self)
        self.special, self.skills = Dad.set_special(self), set()
        self.buff, self.de_buff = Dad.set_buff(self), Dad.set_de_buff(self)
        super().__init__(self.name, self.surname, self.age, self.special, self.skills, self.buff, self.de_buff)


class Son(Person):
    def set_name(self):
        self.name = random.choice(NAME_M_LIST)
        return self.name

    def set_surname(self):
        self.surname = SURNAME
        return self.surname

    def set_age(self, mam, dad):
        temp = [mam - 19, dad - 20]
        temp.sort()
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

    def __init__(self):
        self.name, self.surname, self.age = Son.set_name(self), Son.set_surname(self), 0
        self.special, self.skills = Son.set_special(self), set()
        self.buff, self.de_buff = Son.set_buff(self), Son.set_de_buff(self)
        super().__init__(self.name, self.surname, self.age, self.special, self.skills, self.buff, self.de_buff)


class Daughter(Person):
    def set_name(self):
        self.name = random.choice(NAME_D_LIST)
        return self.name

    def set_surname(self):
        self.surname = SURNAME
        return self.surname

    def set_age(self, mam, dad):
        temp = [mam - 19, dad - 20]
        temp.sort()
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

    def __init__(self):
        self.name, self.surname, self.age = Daughter.set_name(self), Daughter.set_surname(self), 0
        self.special, self.skills = Daughter.set_special(self), set()
        self.buff, self.de_buff = Daughter.set_buff(self), Daughter.set_de_buff(self)
        super().__init__(self.name, self.surname, self.age, self.special, self.skills, self.buff, self.de_buff)


def events_time():
    """Проходит день."""
    for i in range(1, 13):
        if random.randint(1, 4) == 3:
            event = random.choice(PERSON_EVENTS)
            print(f'Сейчас {i} час. Выпало {event}')
            # дебаф добовляем персанажу Mom
            print(Person(*Mom().main()).add_de_buff(event))
        time.sleep(TIME_SECONDS)


class Gen:
    mam = Mom()
    dad = Dad()
    dau = Daughter()
    son = Son()
    son.set_age(mam.age, dad.age)
    dau.set_age(mam.age, dad.age)


def info(ge):
    var = {'mam': ge.mam, 'dad': ge.dad, 'dau': ge.dau, 'son': ge.son}
    pers = input('Введите, чтобы получить статистику(mam, dad, dau, son). '
                 'Или нажмите {enter}, чтобы не выводить статисику.\n')
    if pers != '':
        v = (f'Статистика персонажа {pers}:\n\tИмя: {var[pers].name}\n\tФамилия: {var[pers].surname}\n\t'
             f'Возраст: {var[pers].age}\n\tОсобенности:\n\t\t')
        v += '\n\t\t'.join([SPECIAL_BASE_PRINT[i] for i in list(var[pers].special)])
        v += f'\n\tУмения: {var[pers].skills}\n\tБафы:\n\t\t'
        v += '\n\t\t'.join([PERSON_EVENTS_PRINT[i] for i in list(var[pers].buff)])
        v += f'\n\tДебафы: {var[pers].de_buff}'
        print(v)


if __name__ == '__main__':
    g = Gen()
    info(g)
    info(g)
    info(g)
    info(g)
    info(g)
