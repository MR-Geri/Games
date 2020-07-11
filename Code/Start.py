from Code.Person import *
from Code.Graphics import blur
import Code.items
from Data.file_data import *
import math
import json
import pygame
import random
import time


timer = pygame.time.Clock()
display = None
back = None
# Flag
flag_esc_menu = True
# Флаги для циклов
ESC_MENU = False
NEW_GAME = False
PRELOAD = False
PRELOAD_MENU = False
DELL_GAME = False
LOAD_GAME = False
MENU = False
OPTION = False
EXIT = False
GAME = False
INVENTORY = False
GAME_OVER = False
FLAG = [NEW_GAME, PRELOAD, PRELOAD_MENU, DELL_GAME, LOAD_GAME, MENU, OPTION, EXIT, GAME, INVENTORY, GAME_OVER, ESC_MENU]
active_person = 0
# Для сохранения карты
save_map = []
# Все объекты
camera = None
all_entity = None
inventory = None
# Для камеры, движения и карты
WIN_WIDTH = 1920
WIN_HEIGHT = 1080
QUANTITY_SELL = (101, 101)
SIZE_SELL = 120
COLOR = "#888888"
CAMS_SPEED = 15
# Ячейки для карты
data_sell = ['cell.jpg', 'cell_0.jpg', 'cell_1.jpg', 'cell_2.jpg', 'cell_3.jpg', 'cell_4.jpg']
data_sell_image = [pygame.image.load(f'../Data/data_sell/cell.jpg'),
                   pygame.image.load(f'../Data/data_sell/cell_0.jpg'),
                   pygame.image.load(f'../Data/data_sell/cell_1.jpg'),
                   pygame.image.load(f'../Data/data_sell/cell_2.jpg'),
                   pygame.image.load(f'../Data/data_sell/cell_3.jpg'),
                   pygame.image.load(f'../Data/data_sell/cell_4.jpg')]
# image, speed, vision, radius_safety, random_move, hp, dmg, drop_item_chance, drop_item
enemy_various = [[pygame.image.load("../Data/drawing/slime.png"), 120, 4, 1, (0, 5), 50, 45, (0, 5), [CANNED]],
                 [pygame.image.load("../Data/drawing/stone.png"), 120, 2, 1, (0, 3), 200, 50, (0, 3), [CANNED]]]
# Кнопки
button_left_click = False
left_click = False
left = right = up = down = False
key_e = 1  # 1 - закрыт.
# Персонаж
person = None
motion = 0
# Настройки
PERMISSION = (1920, 1080)
FPS = 60
active_display = 0
FullScreen = False
volume = float(json.load(open('../Save_Loading/settings.json')))


def is_active_display():
    global active_display, volume
    if pygame.display.get_active() == 0:
        pygame.mixer.music.pause()
        active_display = 1
    elif active_display == 1 and pygame.display.get_active() == 1:
        active_display = 0
        pygame.mixer_music.unpause()


def flag_all_false():
    global FLAG
    FLAG = [False for _ in FLAG]


def print_text(message, x, y, font_color=(0, 0, 0), font_type='../Data/shrift.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


class Button:
    def __init__(self, w, h, x=10, y=10, inactive_color=(212, 92, 0), active_color=(255, 111, 0)):
        self.w, self.h, self.inactive_color, self.active_color = w, h, inactive_color, active_color
        self.ots_x, self.ots_y = x, y

    def draw(self, x, y, message=None, action=None, size=30, time_sleep=0.0):
        global button_left_click
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.w and y < mouse[1] < y + self.h:
            pygame.draw.rect(display, self.active_color, (x, y, self.w, self.h))
            flag = 0 if button_left_click is False else 1
            button_left_click = True if click[0] == 1 and flag == 0 else False
            if button_left_click and action is not None:
                if action is quit:
                    pygame.quit()
                    quit()
                else:
                    time.sleep(time_sleep)
                    action()
        else:
            pygame.draw.rect(display, self.inactive_color, (x, y, self.w, self.h))
        print_text(message=message, x=x + self.ots_x, y=y + self.ots_y, font_size=size)

    def draw_act(self, x, y, message=None, action=None, size=30, act=(), time_sleep=0.0, color=(0, 0, 0)):
        global button_left_click
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.w and y < mouse[1] < y + self.h:
            pygame.draw.rect(display, self.active_color, (x, y, self.w, self.h))
            flag = 0 if button_left_click is False else 1
            button_left_click = True if click[0] == 1 and flag == 0 else False
            if button_left_click and action is not None:
                if action is quit:
                    pygame.quit()
                    quit()
                if action is not None:
                    time.sleep(time_sleep)
                    action(act)
        else:
            pygame.draw.rect(display, self.inactive_color, (x, y, self.w, self.h))
        print_text(message=message, x=x + self.ots_x, y=y + self.ots_y, font_size=size, font_color=color)

    def draw_info(self, x, y, message=None, action=None, action_info=None, size=30):
        global button_left_click
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.w and y < mouse[1] < y + self.h:
            pygame.draw.rect(display, self.active_color, (x, y, self.w, self.h))
            pygame.draw.rect(display, self.inactive_color, (680, 700, 980, 600))
            print_text(action_info(), 700, 720)
            flag = 0 if button_left_click is False else 1
            button_left_click = True if click[0] == 1 and flag == 0 else False
            if button_left_click and action is not None:
                if action is quit:
                    pygame.quit()
                    quit()
                if action is not None:
                    action()
        else:
            display.blit(pygame.image.frombuffer(blur(), (1920, 1080), "RGB"), (0, 0))
            print_text(message=message, x=x + self.ots_x, y=y + self.ots_y, font_size=size)
            pygame.draw.rect(display, self.inactive_color, (x, y, self.w, self.h))
        print_text(message=message, x=x + self.ots_x, y=y + self.ots_y, font_size=size)


def esc_menu():
    global flag_esc_menu, back

    def back_to_menu():
        save_game()
        menu()

    flag_esc_menu = True
    continue_button = Button(w=480, h=50, x=145, y=14)
    save_button = Button(w=480, h=50, x=120, y=14)
    load_button = Button(w=480, h=50, x=120, y=14)
    option_button = Button(w=480, h=50, x=160, y=14)
    menu_button = Button(w=480, h=50, x=80, y=14)
    flag_all_false()
    FLAG[ESC_MENU] = True
    while FLAG[ESC_MENU]:
        is_active_display()
        pygame.draw.rect(display, (255, 255, 0), (700, 385, 520, 308))
        continue_button.draw(720, 395, 'Продолжить', back)
        save_button.draw(720, 455, 'Сохранить игру', save_game)
        load_button.draw(720, 515, 'Загрузить игру', load_game, time_sleep=0.25)
        option_button.draw(720, 575, 'Настройки', options_game)
        menu_button.draw(720, 635, 'Выход в главное меню', back_to_menu)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                quit()
            if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                back()
        pygame.display.update()


class Inventory:
    def __init__(self):
        self.last_left_click = 0
        self.last_right_click = 0
        self.number_of_left_click = 0
        self.number_of_right_click = 0
        self.last_sell = None
        self.name_invent = ['карман', 'карман', 'карман', 'карман',
                            'левая рука', 'правая рука', 'пояс', 'спина',
                            'голова', 'тело', 'ноги', 'ступни',
                            'сумка', 'сумка', 'сумка', 'сумка',
                            'сумка', 'сумка', 'сумка', 'сумка']
        self.invent = [None, None, None, None,
                       None, None, None, None,
                       None, None, None, None]

    def item_add(self, item):
        print('добавляем', item)

        for name_item in ITEMS:
            if item in name_item:
                name = ITEMS_Name[ITEMS.index(name_item)]
                break
        if name == 'SMALL_OBJECT' or name == 'CANNED':
            for index in range(4):
                if self.invent[index] is None:
                    self.invent[index] = Code.items.item_add(name, *item)
                    break
        elif name == 'AXE' or name == 'SWORD':
            if self.invent[4] is None:
                self.invent[4] = Code.items.item_add(name, *item)
            elif self.invent[5] is None:
                self.invent[5] = Code.items.item_add(name, *item)
            elif self.invent[7] is None:
                self.invent[7] = Code.items.item_add(name, *item)

    def update_invent(self):
        pers = person.personage
        # Проверка количества урона у персонажа, если оружие в руках
        pers.dmg = DMG_START
        for i in self.invent[4:6]:
            try:
                if i.dmg is not None:
                    pers.dmg += i.dmg
            except:
                pass

    def mouse_click_left(self):
        self.last_right_click = 0
        mouse, click_left = pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0]
        number_of_left_click_before = self.number_of_left_click
        self.number_of_left_click = self.number_of_left_click + 1 if click_left == 1 and self.last_left_click == 0 \
            else self.number_of_left_click
        if number_of_left_click_before + 1 == self.number_of_left_click:
            pos_cell = (mouse[0] // 120 - 3, mouse[1] // 120 - 4)
            if number_x_y[0] > pos_cell[0] > -1 and number_x_y[1] > pos_cell[1] > -1:
                if self.number_of_left_click == 1:
                    if self.invent[pos_cell[1] * 4 + pos_cell[0]] is not None:
                        self.last_sell = self.invent[pos_cell[1] * 4 + pos_cell[0]]
                    self.number_of_left_click = 0 if self.last_sell is None else self.number_of_left_click
                elif self.number_of_left_click == 2:
                    index = pos_cell[1] * 4 + pos_cell[0]
                    if self.invent[index] is None and self.invent[self.invent.index(self.last_sell)].move(*pos_cell):
                        self.invent[self.invent.index(self.last_sell)] = None
                        self.invent[index] = self.last_sell
                        print('Предмет перемещён')
                    self.number_of_left_click, self.last_sell = 0, None
            else:
                self.number_of_left_click, self.last_sell = 0, None
        self.last_left_click = 0 if pygame.mouse.get_pressed()[0] == 0 else 1
        pygame.display.update()

    def mouse_click_right(self):
        self.last_left_click = 0
        mouse, click_right = pygame.mouse.get_pos(), pygame.mouse.get_pressed()[2]
        number_of_right_click_before = self.number_of_right_click
        self.number_of_right_click = self.number_of_right_click + 1 \
            if click_right == 1 and self.last_right_click == 0 else self.number_of_right_click
        if number_of_right_click_before + 1 == self.number_of_right_click:
            pos_cell = (mouse[0] // 120 - 3, mouse[1] // 120 - 4)
            if self.number_of_right_click == 1:
                for i in self.invent:
                    sell_x = self.invent.index(i) % 4
                    sell_y = self.invent.index(i) // 4
                    if sell_x == pos_cell[0] and sell_y == pos_cell[1]:
                        x, y = mouse[0] + 30, mouse[1] + 30
                        pygame.draw.rect(display, (48, 213, 200),
                                         (x, y, 215, 40))
                        print_text('Использовать', x + 10, y + 5)
                        pygame.draw.rect(display, (48, 213, 200),
                                         (x, y + 50, 215, 40))
                        print_text('Выборосить', x + 10, y + 55)
                        for text in i.text():
                            print_text(*text)
                        pygame.display.update()
                        while True:
                            if x < pygame.mouse.get_pos()[0] < x + 215 \
                                    and y < pygame.mouse.get_pos()[1] < y + 40\
                                    and pygame.mouse.get_pressed()[0] == 1:
                                self.number_of_right_click = 0
                                self.last_right_click = 0
                                all_entity.action, dell_flag = i.use(person.personage)
                                # Обновление статистики персонажа и обновление инвентаря
                                if dell_flag:
                                    self.invent[self.invent.index(i)] = None
                                    inventory.open()
                                    break
                                inventory.open()
                            elif x < pygame.mouse.get_pos()[0] < x + 215 \
                                    and y + 50 < pygame.mouse.get_pos()[1] < y + 90\
                                    and pygame.mouse.get_pressed()[0] == 1:
                                self.number_of_right_click = 0
                                self.last_right_click = 0
                                self.invent[self.invent.index(i)] = None
                                inventory.open()
                                break
                            elif pygame.mouse.get_pressed()[0] == 1:
                                self.number_of_right_click = 0
                                self.last_right_click = 0
                                inventory.open()
                                break
                            for e in pygame.event.get():
                                if e.type == pygame.QUIT:
                                    pygame.quit()
                                    quit()
                                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                                    esc_menu()

                self.number_of_right_click = 0
        self.last_right_click = 0 if pygame.mouse.get_pressed()[2] == 0 else 1

    def open(self):
        def item_print():
            print_text('карман', 370, 530, font_size=27)
            print_text('карман', 490, 530, font_size=27)
            print_text('карман', 610, 530, font_size=27)
            print_text('карман', 730, 530, font_size=27)
            print_text('левая', 380, 640, font_size=30)
            print_text('рука', 383, 670, font_size=30)
            print_text('правая', 487, 640, font_size=30)
            print_text('рука', 503, 670, font_size=30)
            print_text('пояс', 625, 640, font_size=30)
            print_text('спина', 735, 640, font_size=30)
            print_text('голова', 370, 760, font_size=30)
            print_text('тело', 505, 760, font_size=30)
            print_text('ноги', 625, 760, font_size=30)
            print_text('ступни', 730, 760, font_size=30)
        global key_e
        global left, right, up, down

        left = right = up = down = False
        flag_all_false()
        FLAG[INVENTORY] = True
        pygame.draw.rect(display, (255, 255, 255), (340, 220, 1240, 640))
        pygame.draw.rect(display, (212, 92, 0), (350, 230, 1220, 620))  # Это фон инвентаря
        display.blit(pygame.transform.scale(
            pygame.image.load("../Data/drawing/player_front.png"), (240, 240)), (360, 240))
        display.blit(pygame.transform.scale(
            pygame.image.load("../Data/drawing/player_back.png"), (240, 240)), (600, 240))
        pygame.display.update()
        while FLAG[INVENTORY]:
            is_active_display()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if e.type == pygame.KEYDOWN and (e.key == pygame.K_e or e.key == pygame.K_ESCAPE):
                    game()
            inventory.mouse_click_left()
            inventory.mouse_click_right()
            # отрисовка ячеек инвентаря
            for x in range(person.personage.number_x_y[0]):
                for y in range(person.personage.number_x_y[1]):
                    display.blit(pygame.image.load('../Data/items/item_sell.jpg'), (360 + 120 * x, 720 - 120 * y))
            # отрисовка текста
            inventory.update_invent()
            all_entity.print_stats()
            item_print()
            for item in self.invent:
                if item is not None:
                    sell_x = self.invent.index(item) % 4
                    sell_y = self.invent.index(item) // 4
                    display.blit(pygame.image.load('../Data/items/item_sell.jpg'),
                                 (sell_x * 120 + 360, sell_y * 120 + 480))
                    display.blit(item.image, (sell_x * 120 + 365, sell_y * 120 + 485))
            pygame.display.update()


def working_objects(data_saves=None):
    class Updating:
        def __init__(self, map, hero, cam, enemy, chest, fire):
            self.map = map
            self.move = []
            self.cam = cam
            self.hero = hero
            self.enemy = [*enemy]
            self.chest = chest
            self.fire = fire
            self.action = None
            self.invent_is_open = False
            self.flag = False
            self.eat = pygame.transform.scale(pygame.image.load('../Data/drawing/eat.png'), (30, 30))
            self.water = pygame.transform.scale(pygame.image.load('../Data/drawing/water.png'), (30, 30))
            self.hp = pygame.transform.scale(pygame.image.load('../Data/drawing/hp.png'), (30, 30))
            self.sword = pygame.transform.scale(pygame.image.load('../Data/drawing/sword.png'), (30, 30))

        def print_stats(self):
            pygame.draw.rect(display, (212, 92, 0), (0, 915, 80, 160))
            display.blit(self.eat, (5, 920))
            display.blit(self.water, (5, 960))
            display.blit(self.hp, (5, 1000))
            display.blit(self.sword, (5, 1040))
            print_text(str(person.personage.hunger), 40, 930, font_size=20)
            print_text(str(person.personage.water), 40, 970, font_size=20)
            print_text(str(person.personage.hp), 40, 1010, font_size=20)
            print_text(str(person.personage.dmg), 40, 1050, font_size=20)

        def update(self):
            if not Action(person.personage).is_live():
                print('Game Over')
                ok_button = Button(w=480, h=50, x=210, y=14)
                flag_all_false()
                FLAG[GAME_OVER] = True
                while FLAG[GAME_OVER]:
                    is_active_display()
                    pygame.draw.rect(display, (255, 255, 0), (700, 495, 520, 110))
                    print_text(message='GAME OVER!', x=865, y=510, font_size=30)
                    ok_button.draw(720, 545, 'Ок', menu)
                    for i in pygame.event.get():
                        if i.type == pygame.QUIT:
                            pygame.quit()
                            quit()
                        if i.type == pygame.KEYDOWN and (i.key == pygame.K_ESCAPE or i.key == pygame.K_RETURN):
                            menu()
                    pygame.display.update()
            else:
                display.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать
                camera.update(self.cam)  # центризируем камеру относительно персонажа
                self.hero.update(pygame.mouse.get_pos())
                self.cam.update(left, right, up, down)  # передвижение камеры
                # отрисовка карты
                for y in self.map:
                    for x in y:
                        if abs(x.rect.x - self.cam.rect.x) < 1400 and abs(x.rect.y - self.cam.rect.y) < 900:
                            display.blit(x.image, camera.apply(x))
                # Отрисовка и обновление сундуков
                for ch in self.chest:
                    if abs(ch.rect.x - self.cam.rect.x) < 1400 and abs(ch.rect.y - self.cam.rect.y) < 900:
                        display.blit(ch.image, camera.apply(ch))
                        ch.update(pygame.mouse.get_pos())
                # Отрисовка и обновление костра
                for f in self.fire:
                    if abs(f.rect.x - self.cam.rect.x) < 1400 and abs(f.rect.y - self.cam.rect.y) < 900:
                        display.blit(f.image, camera.apply(f))
                        f.update(pygame.mouse.get_pos())
                # гибель противников
                for en in self.enemy:
                    for enemy in en:
                        if enemy.hp <= 0:
                            en.remove(enemy)
                            if random.randint(*enemy.drop_item_chance) == 1:
                                item = random.choice(*enemy.drop_item)
                                inventory.item_add(item)
                            print('Противник погиб.')
                        enemy.update(pygame.mouse.get_pos())
                # Удаление точки если там кто-то есть
                for move in self.move:
                    for en in self.enemy:
                        for enemy in en:
                            if enemy.rect.x == move.rect.x and enemy.rect.y == move.rect.y:
                                self.move.remove(move)
                    for ch in self.chest:
                        if ch.rect.x == move.rect.x and ch.rect.y == move.rect.y:
                            self.move.remove(move)
                    for f in self.fire:
                        if f.rect.x == move.rect.x and f.rect.y == move.rect.y:
                            self.move.remove(move)
                # отрисовка точек
                for move in self.move:
                    if abs(move.rect.x - self.cam.rect.x) < 1400 and abs(move.rect.y - self.cam.rect.y) < 900:
                        display.blit(move.image, camera.apply(move))
                        move.update(pygame.mouse.get_pos())
                self.flag = True if not self.move else False
                # отрисовка противников
                for en in self.enemy:
                    for enemy in en:
                        if abs(enemy.rect.x - self.cam.rect.x) < 1400 and abs(enemy.rect.y - self.cam.rect.y) < 900:
                            display.blit(enemy.image, camera.apply(enemy))
                display.blit(self.hero.image, camera.apply(self.hero))  # отрисовка персонажа
                # Вывод статистики левый нижний угол
                all_entity.print_stats()
                pygame.display.update()

    class Move(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('../Data/data_sell/ellipse.png')
            self.rect = pygame.Rect(x, y, SIZE_SELL, SIZE_SELL)
            self.last_left_click = 0

        def update(self, mouse):
            if not all_entity.invent_is_open:
                # Перемещение персонажа на ячейку с точкой.
                local_x = (self.rect.x / SIZE_SELL - all_entity.cam.rect.x / SIZE_SELL) * SIZE_SELL + 9 * SIZE_SELL
                local_y = (self.rect.y / SIZE_SELL - all_entity.cam.rect.y / SIZE_SELL) * SIZE_SELL + 5 * SIZE_SELL
                if local_x - SIZE_SELL < mouse[0] < local_x and \
                        local_y - SIZE_SELL / 2 < mouse[1] < local_y + SIZE_SELL / 2 and \
                        pygame.mouse.get_pressed()[0] == 1 and self.last_left_click == 0:
                    # Голод при ходьбе
                    x = abs((self.rect.x - all_entity.hero.rect.x) // 120)
                    y = abs((self.rect.y - all_entity.hero.rect.y) // 120)
                    cell = x + y if x == 0 or y == 0 else (x + y) / 2
                    Action(person.personage).left_hunger(math.ceil(cell))
                    # ---------------
                    all_entity.action = None
                    all_entity.hero.rect.x = self.rect.x
                    all_entity.hero.rect.y = self.rect.y
                    all_entity.move = []
                self.last_left_click = 0 if pygame.mouse.get_pressed()[0] == 0 else 1

    class Map(pygame.sprite.Sprite):
        def __init__(self, x, y, graphic_sell):
            pygame.sprite.Sprite.__init__(self)
            self.last_left_click, self.last_right_click = 0, 0
            self.image = pygame.image.load(f'../Data/data_sell/{graphic_sell}')
            self.rect = self.image.get_rect(center=(x + SIZE_SELL // 2, y + SIZE_SELL // 2))

    class Camera(object):
        def __init__(self, camera_func, width, height):
            self.camera_func = camera_func
            self.state = pygame.Rect(0, 0, width, height)

        def apply(self, target):
            return target.rect.move(self.state.topleft)

        def update(self, target):
            self.state = self.camera_func(self.state, target.rect)

    def camera_configure(camera, target_rect):
        lo, t = target_rect[:-2]
        w, h = camera[2:]
        lo, t = - lo + WIN_WIDTH / 2, - t + WIN_HEIGHT / 2
        lo = min(0, lo)  # Не движемся дальше левой границы
        lo = max(-(camera.width - WIN_WIDTH), lo)  # Не движемся дальше правой границы
        t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
        t = min(0, t)  # Не движемся дальше верхней границы
        return pygame.Rect(int(lo), int(t), int(w), int(h))

    class Cums(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.x_vel = 0  # скорость перемещения. 0 - стоять на месте
            self.y_vel = 0  # скорость вертикального перемещения
            self.image = pygame.Surface((0, 0))
            self.rect = pygame.Rect(x, y, SIZE_SELL, SIZE_SELL)  # прямоугольный объект

        def update(self, left, right, up, down):
            self.x_vel = 0
            self.y_vel = 0
            if up and self.rect.y > 540:
                self.y_vel = -CAMS_SPEED

            if down and self.rect.y < total_height - 540:
                self.y_vel = CAMS_SPEED

            if left and self.rect.x > 960:
                self.x_vel = -CAMS_SPEED  # Лево = x- n

            if right and self.rect.x < total_width - 960:
                self.x_vel = CAMS_SPEED  # Право = x + n

            self.rect.y += self.y_vel
            self.rect.x += self.x_vel

    class Hero(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.x_vel = 0  # скорость перемещения. 0 - стоять на месте
            self.y_vel = 0  # скорость вертикального перемещения
            self.image = pygame.image.load("../Data/drawing/player_front.png")
            self.image = pygame.transform.scale(self.image, (SIZE_SELL, SIZE_SELL))
            self.rect = pygame.Rect(x, y, SIZE_SELL, SIZE_SELL)  # прямоугольный объект
            self.last_left_click, self.last_right_click = 0, 0

        def update(self, mouse):
            global key_e, motion
            self.x_vel = 0
            self.y_vel = 0
            # координата персонажа относительные (1920.1080)
            local_x = ((self.rect.x / SIZE_SELL - all_entity.cam.rect.x / SIZE_SELL) + 9) * SIZE_SELL
            local_y = ((self.rect.y / SIZE_SELL - all_entity.cam.rect.y / SIZE_SELL) + 5) * SIZE_SELL
            # Нажатие по персонажу ЛКМ
            if not all_entity.invent_is_open:
                if local_x - SIZE_SELL < mouse[0] < local_x and \
                        local_y - SIZE_SELL / 2 < mouse[1] < local_y + SIZE_SELL / 2 and \
                        pygame.mouse.get_pressed()[0] == 1 and self.last_left_click == 0:
                    if not all_entity.move:
                        cell_move = []
                        for y in range(-3, 4, 1):
                            for x in range(-3, 4, 1):
                                if y == 0 and x == 0:
                                    pass
                                else:
                                    position_x = self.rect.x + x * 120
                                    position_y = self.rect.y + y * 120
                                    cell_move.append(Move(position_x, position_y))
                        motion += 1
                        # голод при каждом ходе
                        Action(person.personage).left_hunger(2)
                        #
                        print('Ход номер:', motion)
                        all_entity.move = cell_move
                    else:
                        all_entity.move = []
                self.last_left_click = 0 if pygame.mouse.get_pressed()[0] == 0 else 1
            # Открытие инвентаря
            key_e = 1 if key_e > 2 else key_e
            all_entity.invent_is_open = True if key_e == 2 else False

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y, image, speed, vision, radius_safety, random_move, hp, dmg, drop_item_chance,
                     drop_item):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(image, (SIZE_SELL - 8, SIZE_SELL - 8))
            self.rect = pygame.Rect(x, y, SIZE_SELL, SIZE_SELL)
            self.speed = speed
            self.vision = vision
            self.radius_safety = radius_safety
            self.random_move = random_move
            self.hp = hp
            self.dmg = dmg
            self.drop_item_chance = drop_item_chance
            self.drop_item = drop_item
            self.last_left_click = True

        def update(self, mouse):
            global motion
            hero_x = ((all_entity.hero.rect.x / SIZE_SELL - all_entity.cam.rect.x / SIZE_SELL) + 8)
            hero_y = ((all_entity.hero.rect.y / SIZE_SELL - all_entity.cam.rect.y / SIZE_SELL) + 4)
            x = (self.rect.x - all_entity.hero.rect.x) / SIZE_SELL
            y = (self.rect.y - all_entity.hero.rect.y) / SIZE_SELL
            sell_x = (hero_x + x) * SIZE_SELL
            sell_y = (hero_y + y) * SIZE_SELL + 60
            if sell_x < mouse[0] < sell_x + 120 and sell_y < mouse[1] < sell_y + 120 and self.last_left_click and \
                    pygame.mouse.get_pressed()[0] == 1 and not all_entity.move and \
                    abs(x) <= 1 and abs(y) <= 1:
                print(f"Врагу нанесено {person.personage.dmg} урона.")
                motion += 1
                self.hp -= person.personage.dmg
                print('Ход номер:', motion)
            self.last_left_click = True if pygame.mouse.get_pressed()[0] == 0 else False
            move_x = 0
            move_y = 0
            # Если упал шанс на движение
            if random.randint(*self.random_move) != 1 and all_entity.flag and all_entity.move:
                # Перемещение к игроку
                if abs(x) <= self.vision and abs(y) <= self.vision:
                    if x > self.radius_safety:
                        if y > self.radius_safety:
                            move_x = -self.speed
                            move_y = -self.speed
                        elif y < -self.radius_safety:
                            move_x = -self.speed
                            move_y = self.speed
                        else:
                            move_x = -self.speed
                    elif x < -self.radius_safety:
                        if y > self.radius_safety:
                            move_x = self.speed
                            move_y = -self.speed
                        elif y < -self.radius_safety:
                            move_x = self.speed
                            move_y = self.speed
                        else:
                            move_x = self.speed
                    else:
                        if y > self.radius_safety:
                            move_y = -self.speed
                        elif y < -self.radius_safety:
                            move_y = self.speed
                    move_x += self.rect.x
                    move_y += self.rect.y
                # перемещение по карте
                else:
                    move_x = self.rect.x + random.randint(-3, 3) * SIZE_SELL
                    move_y = self.rect.y + random.randint(-3, 3) * SIZE_SELL
                flag_move = True
                # Проверка если занято
                for en in all_entity.enemy:
                    for enemy in en:
                        flag_move = False if enemy.rect.x == move_x and enemy.rect.y == move_y else flag_move
                for sell in all_entity.chest:
                    flag_move = False if sell.rect.x == move_x and sell.rect.y == move_y else flag_move
                for f in all_entity.fire:
                    flag_move = False if f.rect.x == move_x and f.rect.y == move_y else flag_move
                #
                if flag_move and \
                        QUANTITY_SELL[0] * SIZE_SELL > move_x > 0 and QUANTITY_SELL[1] * SIZE_SELL > move_y > 0:
                    self.rect.x = move_x
                    self.rect.y = move_y

    class Chest(pygame.sprite.Sprite):
        def __init__(self, x, y, condition=True):
            pygame.sprite.Sprite.__init__(self)
            self.condition = condition
            if self.condition:
                self.image = pygame.transform.scale(pygame.image.load('../Data/data_sell/chest_close.png'),
                                                    (SIZE_SELL, SIZE_SELL))
            else:
                self.image = pygame.transform.scale(pygame.image.load('../Data/data_sell/chest_open.png'),
                                                    (SIZE_SELL, SIZE_SELL))
            self.loot = [*SMALL_OBJECT, *AXE, *SWORD]
            self.rect = pygame.Rect(x, y, SIZE_SELL, SIZE_SELL)
            self.last_left_click = False

        def update(self, mouse):
            global motion
            if self.condition:
                hero_x = ((all_entity.hero.rect.x / SIZE_SELL - all_entity.cam.rect.x / SIZE_SELL) + 8)
                hero_y = ((all_entity.hero.rect.y / SIZE_SELL - all_entity.cam.rect.y / SIZE_SELL) + 4)
                x = (self.rect.x - all_entity.hero.rect.x) / SIZE_SELL
                y = (self.rect.y - all_entity.hero.rect.y) / SIZE_SELL
                sell_x = (hero_x + x) * SIZE_SELL
                sell_y = (hero_y + y) * SIZE_SELL + 60
                if sell_x < mouse[0] < sell_x + 120 and sell_y < mouse[1] < sell_y + 120 and self.last_left_click and \
                        pygame.mouse.get_pressed()[0] == 1 and not all_entity.move and abs(x) <= 1 and abs(y) <= 1:
                    self.condition = False
                    self.image = pygame.transform.scale(pygame.image.load('../Data/data_sell/chest_open.png'),
                                                        (SIZE_SELL, SIZE_SELL))
                    inventory.item_add(random.choice(self.loot))
                    print(f"Сундук открыт")
                    motion += 1
                    print('Ход номер:', motion)
                self.last_left_click = True if pygame.mouse.get_pressed()[0] == 0 else False

    class Fire(pygame.sprite.Sprite):
        def __init__(self, x, y, condition=True):
            pygame.sprite.Sprite.__init__(self)
            self.condition = condition
            if self.condition:
                self.image = pygame.transform.scale(pygame.image.load('../Data/data_sell/firewood.png'),
                                                    (SIZE_SELL, SIZE_SELL))
            else:
                self.image = pygame.transform.scale(pygame.image.load('../Data/data_sell/fire.png'),
                                                    (SIZE_SELL, SIZE_SELL))
            self.rect = pygame.Rect(x, y, SIZE_SELL, SIZE_SELL)
            self.last_left_click = False

        def update(self, mouse):
            global motion
            if self.condition:
                x = (self.rect.x - all_entity.hero.rect.x) / SIZE_SELL
                y = (self.rect.y - all_entity.hero.rect.y) / SIZE_SELL
                if all_entity.action == 'fire':
                    all_entity.action = None
                    if not all_entity.move and abs(x) <= 1 and abs(y) <= 1:
                        self.image = pygame.transform.scale(pygame.image.load('../Data/data_sell/fire.png'),
                                                            (SIZE_SELL, SIZE_SELL))
                        self.condition = False
                        print(f"Костёр зажёгся")
                        motion += 1
                        print('Ход номер:', motion)
                    else:
                        print('Рядом не чего зажечь')
                    self.last_left_click = True if pygame.mouse.get_pressed()[0] == 0 else False

    global save_map, camera, all_entity
    # Загрузочный экран
    display.blit(back_menu, (0, 0))
    pygame.draw.rect(display, (212, 92, 0), (850, 510, 245, 45))
    print_text('Идёт загрузка', 860, 520)
    pygame.display.update()
    #
    total_width = QUANTITY_SELL[0] * SIZE_SELL  # Высчитываем фактическую ширину уровня
    total_height = QUANTITY_SELL[1] * SIZE_SELL  # высоту
    if data_saves is not None:
        # Загрузка карты
        map_y = []
        save_map = data_saves[0]
        for y in range(QUANTITY_SELL[1]):
            map_x = []
            for x in range(QUANTITY_SELL[0]):
                map_x.append(Map(x * SIZE_SELL, y * SIZE_SELL, data_sell[int(save_map[y][x])]))
            map_y.append(map_x)
        # загрузка противников на карту (Слизнь)
        enemy_list = []
        for num in data_saves[3]:
            enemy_class = []
            for j in num:
                for i in num.get(j):
                    enemy_class.append(Enemy(int(i), int(j), *enemy_various[data_saves[3].index(num)]))
            enemy_list.append(enemy_class)
        chest = []
        for y in data_saves[4]:
            for x in data_saves[4].get(y):
                chest.append(Chest(int(x[0]), int(y), x[1]))
        fire = []
        for y in data_saves[5]:
            for x in data_saves[5].get(y):
                fire.append(Fire(int(x[0]), int(y), x[1]))
        all_entity = Updating(map_y,
                              Hero(*data_saves[1]),
                              Cums(*data_saves[2]),
                              enemy_list,
                              chest,
                              fire)
    elif data_saves is None:
        # Создание и сохранение карты
        save_map = []
        map_y = []
        enemy_list = [[] for _ in range(len(enemy_various))]
        chest = []
        fire = []
        for y in range(QUANTITY_SELL[1]):
            save_map_x = ''
            map_x = []
            for x in range(QUANTITY_SELL[0]):
                # добавление разных противников на карту
                for num in range(len(enemy_various)):
                    if (random.randint(0, 50) == 1) and ((y < 50 or y > 52) and (x < 49 or x > 53)):
                        enemy_list[num].append(Enemy(x * SIZE_SELL, y * SIZE_SELL, *enemy_various[num]))
                        break
                    elif (random.randint(0, 190) == 1) and ((y < 50 or y > 52) and (x < 49 or x > 53)):
                        chest.append(Chest(x * SIZE_SELL, y * SIZE_SELL))
                        break
                    elif (random.randint(0, 170) == 1) and ((y < 50 or y > 52) and (x < 49 or x > 53)):
                        fire.append(Fire(x * SIZE_SELL, y * SIZE_SELL))
                        break
                if y == 51 and (x == 50 or x == 51):
                    graphic_cell = data_sell[0]
                else:
                    graphic_cell = random.choice(data_sell[1:])
                save_map_x += str(data_sell.index(graphic_cell))
                map_x.append(Map(x * SIZE_SELL, y * SIZE_SELL, graphic_cell))
            map_y.append(map_x)
            save_map.append(save_map_x)
        all_entity = Updating(map_y,
                              Hero(51 * SIZE_SELL, 51 * SIZE_SELL),
                              Cums(51 * SIZE_SELL, 51 * SIZE_SELL + SIZE_SELL // 2),
                              enemy_list,
                              chest,
                              fire)
    camera = Camera(camera_configure, total_width, total_height)


def save_game():
    global person, save_map, flag_esc_menu
    if flag_esc_menu:
        # Карта. Персонажи. Положение картинки игрока. Положение камеры.
        data_t = [[] for _ in range(8)]
        data_t[0] = save_map
        data_t[1] = [person.personage.name, person.personage.surname, person.personage.age, person.personage.dmg,
                     list(person.personage.special), list(person.personage.skills), list(person.personage.buff),
                     list(person.personage.de_buff), person.personage.hp, person.personage.hunger,
                     person.personage.water, person.personage.number_x_y, person.personage.stress]
        data_t[2] = [all_entity.hero.rect.x, all_entity.hero.rect.y]
        data_t[3] = [all_entity.cam.rect.x, all_entity.cam.rect.y]
        # Слизни,
        enemy = [{} for _ in range(len(enemy_various))]
        for i in all_entity.enemy:
            for en in i:
                if enemy[all_entity.enemy.index(i)].get(en.rect.y) is None:
                    enemy[all_entity.enemy.index(i)].update({en.rect.y: [en.rect.x]})
                else:
                    enemy[all_entity.enemy.index(i)][en.rect.y].append(en.rect.x)
        chest = {}
        for i in all_entity.chest:
            if chest.get(i.rect.y) is None:
                chest.update({i.rect.y: [[i.rect.x, i.condition]]})
            else:
                chest[i.rect.y].append([i.rect.x, i.condition])
        fire = {}
        for f in all_entity.fire:
            if fire.get(f.rect.y) is None:
                fire.update({f.rect.y: [[f.rect.x, f.condition]]})
            else:
                fire[f.rect.y].append([f.rect.x, f.condition])
        data_t[4] = enemy
        data_t[5] = chest
        data_t[6] = fire
        data_t[7] = motion
        # сохранение или замена
        try:
            data = json.load(open('../Save_Loading/save.json'))
        except:
            data = []
        flag = True
        for i in data:
            if i is None:
                data[data.index(i)] = data_t
                print('Сохранение создано.')
                flag = False
                break
            elif data_t[0] == i[0]:
                data[data.index(i)] = data_t
                print('Сохранение заменено.')
                flag = False
                break
        if flag:
            print('Сохранению не куда вставиться.')
        with open('../Save_Loading/save.json', 'w') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        flag_esc_menu = False


def load_game():
    def load(n):
        def helper_load():
            global person, motion, inventory
            per = DATA_SAVE[n][1]
            person = Data_pers()
            person.personage.name, person.personage.surname = per[0], per[1]
            person.personage.age = per[2]
            person.personage.dmg = per[3]
            person.personage.special = set(per[4])
            person.personage.skills = set(per[5])
            person.personage.buff = set(per[6])
            person.personage.de_buff = set(per[7])
            person.personage.hp = per[8]
            person.personage.hunger, person.personage.water = per[9], per[10]
            person.personage.number_x_y = per[11]
            person.personage.stress = per[12]
            print(person)
            motion = int(DATA_SAVE[n][7])
            inventory = Inventory()
            inventory.update_invent()
            # Нужно загрузить инвентарь....
            working_objects([DATA_SAVE[n][0], DATA_SAVE[n][2], DATA_SAVE[n][3], DATA_SAVE[n][4], DATA_SAVE[n][5],
                             DATA_SAVE[n][6]])
            print(f'Игра загружена.')
            game()

        def del_game():
            def dell():
                try:
                    data = json.load(open('../Save_Loading/save.json'))
                except:
                    data = [None, None, None, None, None]
                if data[n] is not None:
                    data[n] = None
                    with open('../Save_Loading/save.json', 'w') as file:
                        json.dump(data, file, indent=2, ensure_ascii=False)
                    print('Сохранение удалено.')
                    menu()
            # Удаление игры.
            if back == esc_menu:
                all_entity.update()
            else:
                display.blit(pygame.image.frombuffer(blur(), PERMISSION, "RGB"), (0, 0))
            choice_button_no = Button(w=120, h=80, x=15, y=16)
            choice_button_yes = Button(w=120, h=80, x=25, y=15)
            flag_all_false()
            FLAG[DELL_GAME] = True
            while FLAG[DELL_GAME]:
                is_active_display()
                pygame.draw.rect(display, (255, 255, 0), (790, 510, 340, 100))
                choice_button_yes.draw(800, 520, 'Да', dell, 50)
                choice_button_no.draw(1000, 520, 'Нет', back, 50)
                for i in pygame.event.get():
                    if i.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                        back()
                pygame.display.update()

        def load_menu():
            if back == esc_menu:
                all_entity.update()
            else:
                display.blit(pygame.image.frombuffer(blur(), PERMISSION, "RGB"), (0, 0))
            button_load = Button(w=480, h=50, x=170, y=14)
            button_dell = Button(w=480, h=50, x=185, y=14)
            flag_all_false()
            FLAG[PRELOAD_MENU] = True
            while FLAG[PRELOAD_MENU]:
                is_active_display()
                pygame.draw.rect(display, (255, 255, 0), (700, 480, 520, 125))
                button_load.draw(720, 490, 'Загрузить', helper_load)
                button_dell.draw(720, 545, 'Удалить', del_game)
                for i in pygame.event.get():
                    if i.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                        back()
                pygame.display.update()

        global back
        DATA_SAVE = json.load(open('../Save_Loading/save.json'))
        if DATA_SAVE[n] is not None:
            load_menu()
        else:
            if back == esc_menu or back == game:
                all_entity.update()
            else:
                display.blit(pygame.image.frombuffer(blur(), PERMISSION, "RGB"), (0, 0))
            ok_button = Button(w=480, h=50, x=210, y=14)
            flag_all_false()
            FLAG[PRELOAD] = True
            while FLAG[PRELOAD]:
                is_active_display()
                pygame.draw.rect(display, (255, 255, 0), (700, 495, 520, 110))
                print_text(message='Сохранение не создано.', x=780, y=510, font_size=30)
                ok_button.draw(720, 545, 'Ок', back)
                for i in pygame.event.get():
                    if i.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                        back()
                pygame.display.update()

    if back == menu:
        display.blit(pygame.image.frombuffer(blur(), (1920, 1080), "RGB"), (0, 0))
    try:
        data = json.load(open('../Save_Loading/save.json'))
    except:
        data = [None, None, None, None, None]
    back_button = Button(w=110, h=50, y=14)
    saves_button = Button(w=480, h=50, x=160, y=14)
    pygame.display.update()
    flag_all_false()
    FLAG[LOAD_GAME] = True
    while FLAG[LOAD_GAME]:
        is_active_display()
        pygame.draw.rect(display, (255, 255, 0), (700, 385, 520, 308))
        back_button.draw(10, 10, 'Назад', back, time_sleep=0.25)

        saves_button.draw_act(720, 395, 'Ячейка 1.', load, time_sleep=0.25, act=0,
                              color=(48, 213, 202) if data[0] is None else (0, 0, 0))
        saves_button.draw_act(720, 455, 'Ячейка 2.', load, time_sleep=0.25, act=1,
                              color=(48, 213, 202) if data[1] is None else (0, 0, 0))
        saves_button.draw_act(720, 515, 'Ячейка 3.', load, time_sleep=0.25, act=2,
                              color=(48, 213, 202) if data[2] is None else (0, 0, 0))
        saves_button.draw_act(720, 575, 'Ячейка 4.', load, time_sleep=0.25, act=3,
                              color=(48, 213, 202) if data[3] is None else (0, 0, 0))
        saves_button.draw_act(720, 635, 'Ячейка 5.', load, time_sleep=0.25, act=4,
                              color=(48, 213, 202) if data[4] is None else (0, 0, 0))

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                quit()
            if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                back()
        pygame.display.update()


def options_game():
    def volume_minus():
        global volume
        volume -= 0.001
        volume = 0 if volume < 0 else volume
        with open('../Save_Loading/settings.json', 'w') as file:
            json.dump(volume, file, indent=2, ensure_ascii=False)
        pygame.mixer_music.set_volume(volume)

    def volume_plus():
        global volume
        volume += 0.001
        with open('../Save_Loading/settings.json', 'w') as file:
            json.dump(volume, file, indent=2, ensure_ascii=False)
        pygame.mixer_music.set_volume(volume)

    if back == menu:
        display.blit(pygame.image.frombuffer(blur(), PERMISSION, "RGB"), (0, 0))
    back_button = Button(w=110, h=50, y=14)
    volume_button = Button(w=100, h=100, x=35, y=35)
    flag_all_false()
    FLAG[OPTION] = True
    while FLAG[OPTION]:
        is_active_display()
        pygame.draw.rect(display, (255, 255, 0), (700, 385, 520, 308))
        back_button.draw(10, 10, 'Назад', back)
        volume_button.draw(940, 420, '', volume_minus)
        volume_button.draw(1080, 420, '', volume_plus)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                quit()
            if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                back()
        pygame.display.update()


def exit_game():
    display.blit(pygame.image.frombuffer(blur(), PERMISSION, "RGB"), (0, 0))
    choice_button_no = Button(w=120, h=80, x=15, y=16)
    choice_button_yes = Button(w=120, h=80, x=25, y=15)
    flag_all_false()
    FLAG[EXIT] = True
    while FLAG[EXIT]:
        is_active_display()
        pygame.draw.rect(display, (255, 255, 0), (790, 510, 340, 100))
        choice_button_yes.draw(800, 520, 'Да', quit, 50)
        choice_button_no.draw(1000, 520, 'Нет', menu, 50)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                quit()
            # Выход при ENTER не работаееет
            if i.type == pygame.KEYDOWN and (i.key == pygame.K_RETURN or i.key == pygame.K_KP_ENTER):
                pygame.quit()
                quit()
            if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                menu()

        pygame.display.update()


def game():
    global left, right, up, down, key_e, left_click
    global camera, all_entity, display, back
    global inventory
    back = game
    display.blit(back_menu, (0, 0))
    flag_all_false()
    FLAG[GAME] = True
    while FLAG[GAME]:
        timer.tick(FPS)
        is_active_display()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                esc_menu()

            if e.type == pygame.KEYDOWN and e.key == pygame.K_w:
                up = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_a:
                left = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_d:
                right = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_s:
                down = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_e:
                inventory.open()

            if e.type == pygame.KEYUP and e.key == pygame.K_w:
                up = False
            if e.type == pygame.KEYUP and e.key == pygame.K_a:
                left = False
            if e.type == pygame.KEYUP and e.key == pygame.K_d:
                right = False
            if e.type == pygame.KEYUP and e.key == pygame.K_s:
                down = False

        all_entity.update()


class Presets:
    def __init__(self):
        self.preset = ['У вас базоавый набор вещей.']

    def one(self):
        global person, inventory

        if person is None:
            person = Data_pers()
            print(person)
            inventory = Inventory()
            inventory.item_add(AXE[0])
            inventory.item_add(CANNED[2])
            inventory.item_add(CANNED[3])
            inventory.item_add(SMALL_OBJECT[1])
            inventory.update_invent()
            working_objects()
            save_game()
            game()

        """Отладочная характеристика персонажа(персонажей)"""

    def one_print(self):
        return Presets().preset[0]


def menu():
    def new_game():
        global motion
        motion = 0
        display.blit(pygame.image.frombuffer(blur(), PERMISSION, "RGB"), (0, 0))
        preset_button = Button(w=480, h=50, x=75, y=14)
        back_button = Button(w=110, h=50, y=14)
        flag_all_false()
        FLAG[NEW_GAME] = True
        while FLAG[NEW_GAME]:
            is_active_display()
            preset_button.draw_info(100, 700, 'Бывалый выживальщик.', Presets().one, Presets().one_print)
            back_button.draw(10, 10, 'Назад', menu)
            for ivent in pygame.event.get():
                if ivent.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if ivent.type == pygame.KEYDOWN and ivent.key == pygame.K_ESCAPE:
                    menu()
            pygame.display.update()

    global person, flag_esc_menu, back
    back = menu
    person = None
    flag_esc_menu = True
    display.blit(back_menu, (0, 0))
    ex_button = Button(w=200, h=80, x=27, y=20)
    new_game_button = Button(w=280, h=50, x=52, y=13)
    save_load_button = Button(w=280, h=50, x=20, y=13)
    options_button = Button(w=280, h=50, x=50, y=13)
    flag_all_false()
    FLAG[MENU] = True
    while FLAG[MENU]:
        is_active_display()
        new_game_button.draw(820, 600, 'Новая игра', new_game)
        save_load_button.draw(820, 700, 'Загрузить игру', load_game)
        options_button.draw(820, 800, 'Настройки', options_game)
        ex_button.draw(860, 900, 'Выход', exit_game, 50)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()


def start_menu():
    global display, back_menu, bg
    pygame.init()
    if FullScreen:
        display = pygame.display.set_mode(PERMISSION, pygame.FULLSCREEN)
    else:
        display = pygame.display.set_mode(PERMISSION)
    pygame.display.set_caption("Geri_Games_INC")
    back_menu = pygame.image.load('../Data/menu.jpg')
    display.blit(back_menu, (0, 0))
    bg = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
    pygame.mixer_music.load('../Data/menu.mp3')
    pygame.mixer_music.set_volume(volume)
    pygame.mixer_music.play(-1)
    menu()


start_menu()
