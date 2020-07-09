names_m = ['Jack', 'James', "Daniel", "Harry", "Charlie", "Ethan", "Matthew", "Ryen",
           "Riley", "Noah", "Jacob", "Oliver", "Riley", "Alfie", "Mason", "Dylan", "Sherlock"]
names_d = ["Sophie", "Emily", "Grace", "Amelia", "Jessica", "Lucy", "Sophia", "Katie", "Eva", "Aoife", "Mia"]
surname = ["Abramson", "Hoggarth", "Adamson", "Holiday", "Adderiy", "Holmes", "Addington", "Howard", "Adrian",
           "Jacobson", "Albertson", "James", "Aldridge", "Jeff", "Allford", "Jenkin", "Alsopp", "Jerome"]

"""           Особенности.           """
SPECIAL_BASE = [['smart', 'stupid'], ['light sleep'], ['strong', 'frail'], ['glutton']]
SPECIAL_BASE_PRINT = {"smart": "Персонаж имеет повышенный уровень интеллекта",
                      "stupid": "Персонаж имеет пониженный уровень интеллекта",
                      "light sleep": "Персонаж чуток во сне",
                      "strong": "Персонаж в хорошей физической форме",
                      "frail": "Персонаж в плохой физической форме",
                      "glutton": "Персонаж любит покушать"}

"""           Бафы, дебафы           """
PERSON_EVENTS = ['fracture']
PERSON_EVENTS_PRINT = {'fracture': 'Перелом',
                       'overeaten': 'Объелись',
                       'full_eat': 'Сытость'}

"""           Предметы           """
"""Путь к картинке, название, вместительность"""
BACKPACK = [['travel_bag.png', 'дорожная сумка', 3]]
"""Путь к картинке, название, действие"""
SMALL_OBJECT = [['flashlight.png', 'фонарик', 'none'], ['matches.png', 'спички', 'fire']]
"""Путь к картинке, названте, урон"""
AXE = [['old_axe.png', 'старый, лесной топор', 25], ['new_axe.png', 'новый красивый топор', 35]]
SWORD = [['sword.png', 'базовый меч', 40], ['spear.png', 'копьё', 45]]
"""Путь к картинке, название, сытность"""
CANNED = [['can_of_fish.png', 'рыбные консервы', 25], ['big_can.png', 'тушёнка', 40],
          ['small_can.png', 'куриное мясо', 30], ['salami.png', 'салями', 20]]


"""Дата, выводы"""

ITEMS = [BACKPACK, SMALL_OBJECT, AXE, SWORD, CANNED]
ITEMS_Name = ['BACKPACK', 'SMALL_OBJECT', 'AXE', 'SWORD', 'CANNED']
BACKPACK_PRINT = {'дорожная сумка': 'дорожной сумке'}
