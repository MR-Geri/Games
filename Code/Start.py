from Code.Person import Data_pers
from Code.Graphics import blur
import json
import pygame
import random
import time


timer = pygame.time.Clock()
active = []
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
FLAG = [NEW_GAME, PRELOAD, PRELOAD_MENU, DELL_GAME, LOAD_GAME, MENU, OPTION, EXIT, GAME, INVENTORY, ESC_MENU]
# Для сохранения карты
save_map = []
# Все объекты
camera = None
all_entity = None
# Для камеры, движения и карты
WIN_WIDTH = 1920
WIN_HEIGHT = 1080
QUANTITY_SELL = (101, 101)
SIZE_SELL = 120
COLOR = "#888888"
CAMS_SPEED = 10
# Ячейки для карты
data_sell = ['cell.jpg', 'cell_0.jpg', 'cell_1.jpg', 'cell_2.jpg', 'cell_3.jpg', 'cell_4.jpg']
data_sell_image = [pygame.image.load(f'../Data/data_sell/cell.jpg'),
                   pygame.image.load(f'../Data/data_sell/cell_0.jpg'),
                   pygame.image.load(f'../Data/data_sell/cell_1.jpg'),
                   pygame.image.load(f'../Data/data_sell/cell_2.jpg'),
                   pygame.image.load(f'../Data/data_sell/cell_3.jpg'),
                   pygame.image.load(f'../Data/data_sell/cell_4.jpg')]
data_sell_active = ['cell_ellipse.jpg', 'cell_ellipse_0.jpg', 'cell_ellipse_1.jpg', 'cell_ellipse_2.jpg',
                    'cell_ellipse_3.jpg', 'cell_ellipse_4.jpg']
data_sell_active_image = [pygame.image.load(f'../Data/data_sell/cell_ellipse.jpg'),
                          pygame.image.load(f'../Data/data_sell/cell_ellipse_0.jpg'),
                          pygame.image.load(f'../Data/data_sell/cell_ellipse_1.jpg'),
                          pygame.image.load(f'../Data/data_sell/cell_ellipse_2.jpg'),
                          pygame.image.load(f'../Data/data_sell/cell_ellipse_3.jpg'),
                          pygame.image.load(f'../Data/data_sell/cell_ellipse_4.jpg')]
# Кнопки
button_click_left = False
left_click = False
left = right = up = down = False
key_e = 1  # 1 - закрыт.
# Персонаж
person = None
# Настройки
PERMISSION = (1920, 1080)
FPS = 60
active_display = 0
FullScreen = False
volume = float(json.load(open('../Save_Loading/settings.json')))
DATA_SAVE = json.load(open('../Save_Loading/save.json'))


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
        global button_click_left
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.w and y < mouse[1] < y + self.h:
            pygame.draw.rect(display, self.active_color, (x, y, self.w, self.h))
            flag = 0 if button_click_left is False else 1
            button_click_left = True if click[0] == 1 and flag == 0 else False
            if button_click_left and action is not None:
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
        global button_click_left
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.w and y < mouse[1] < y + self.h:
            pygame.draw.rect(display, self.active_color, (x, y, self.w, self.h))
            flag = 0 if button_click_left is False else 1
            button_click_left = True if click[0] == 1 and flag == 0 else False
            if button_click_left and action is not None:
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
        global button_click_left
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.w and y < mouse[1] < y + self.h:
            pygame.draw.rect(display, self.active_color, (x, y, self.w, self.h))
            pygame.draw.rect(display, self.inactive_color, (680, 700, 980, 600))
            print_text(action_info(), 700, 720)
            flag = 0 if button_click_left is False else 1
            button_click_left = True if click[0] == 1 and flag == 0 else False
            if button_click_left and action is not None:
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


def start_game():
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

    def inventory():
        global key_e, back
        back = inventory
        flag_all_false()
        FLAG[INVENTORY] = True
        pygame.draw.rect(display, (255, 255, 255), (480, 240, 960, 600))
        pygame.draw.rect(display, (212, 92, 0), (490, 250, 940, 580))
        pygame.draw.rect(display, (255, 255, 255), (480, 475, 960, 10))  # горизонтальная
        pygame.draw.rect(display, (255, 255, 255), (955, 240, 10, 240))  # вертикальная
        pygame.draw.rect(display, (255, 255, 255), (500, 260, 100, 100))  # левая верхняя ячейка
        pygame.draw.rect(display, (255, 255, 255), (500, 365, 100, 100))  # левая нижняя ячейка
        pygame.draw.rect(display, (255, 255, 255), (845, 260, 100, 100))  # правая верхняя ячейка
        pygame.draw.rect(display, (255, 255, 255), (845, 365, 100, 100))  # правая нижняя ячейка

        pygame.display.update()
        while FLAG[INVENTORY]:
            is_active_display()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_e:
                    game()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    esc_menu()

    def working_objects(data_saves=None):
        class Updating:
            def __init__(self, map, hero, cam):
                self.map = map
                self.cam = cam
                self.hero = hero
                self.invent = False

            def update(self):
                display.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать
                camera.update(self.cam)  # центризируем камеру относительно персонажа
                self.cam.update(left, right, up, down)  # передвижение камеры
                # Возврат клетки с точкой к обычной после перемещения персонажа
                for i in active:
                    self.map[i[0]][i[1]].update(pygame.mouse.get_pos())
                self.hero.update(pygame.mouse.get_pos())  # обновление персонажа
                # отрисовка карты
                for i in self.map:
                    for g in i:
                        display.blit(g.image, camera.apply(g))
                #
                display.blit(self.hero.image, camera.apply(self.hero))  # отрисовка персонажа
                pygame.display.update()

        class Map(pygame.sprite.Sprite):
            def __init__(self, x, y, graphic_sell):
                pygame.sprite.Sprite.__init__(self)
                self.last_left_click, self.last_right_click = 0, 0
                self.col_vo_click = 0
                self.image = pygame.image.load(f'../Data/data_sell/{graphic_sell}')
                self.rect = self.image.get_rect(center=(x + SIZE_SELL // 2, y + SIZE_SELL // 2))

            def update(self, mouse):
                if all_entity.invent is False:
                    # Перемещение персонажа на ячейку с точкой.
                    local_x = (self.rect.x / SIZE_SELL - all_entity.cam.rect.x / SIZE_SELL) * SIZE_SELL + 9 * SIZE_SELL
                    local_y = (self.rect.y / SIZE_SELL - all_entity.cam.rect.y / SIZE_SELL) * SIZE_SELL + 5 * SIZE_SELL
                    if local_x - SIZE_SELL < mouse[0] < local_x and \
                            local_y - SIZE_SELL / 2 < mouse[1] < local_y + SIZE_SELL / 2 and \
                            pygame.mouse.get_pressed()[0] == 1 and self.last_left_click == 0:
                        all_entity.hero.rect.x = self.rect.x
                        all_entity.hero.rect.y = self.rect.y
                        for i in active:
                            all_entity.map[i[0]][i[1]].image = data_sell_image[int(save_map[i[0]][i[1]])]
                    self.last_left_click = 0 if pygame.mouse.get_pressed()[0] == 0 else 1

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
                self.image = pygame.Surface((SIZE_SELL, SIZE_SELL))
                self.image = pygame.image.load("../Data/player.png")
                self.image = pygame.transform.scale(self.image, (SIZE_SELL, SIZE_SELL))
                self.rect = pygame.Rect(x, y, SIZE_SELL, SIZE_SELL)  # прямоугольный объект
                self.last_left_click, self.last_right_click = 0, 0
                self.col_vo_click = 0

            def update(self, mouse):
                global active, key_e
                self.x_vel = 0
                self.y_vel = 0
                # координата персонажа относительные (1920.1080)
                local_x = (self.rect.x / SIZE_SELL - all_entity.cam.rect.x / SIZE_SELL) * SIZE_SELL + 9 * SIZE_SELL
                local_y = (self.rect.y / SIZE_SELL - all_entity.cam.rect.y / SIZE_SELL) * SIZE_SELL + 5 * SIZE_SELL
                # Нажатие по персонажу ЛКМ
                if all_entity.invent is False:
                    if local_x - SIZE_SELL < mouse[0] < local_x and \
                            local_y - SIZE_SELL / 2 < mouse[1] < local_y + SIZE_SELL / 2 and \
                            pygame.mouse.get_pressed()[0] == 1 and self.last_left_click == 0:
                        self.col_vo_click += 1
                        self.col_vo_click = 0 if self.col_vo_click > 3 else self.col_vo_click
                        for y in range(-3, 4, 1):
                            for x in range(-3, 4, 1):
                                if y == 0 and x == 0:
                                    pass
                                else:
                                    position_x = self.rect.x // 120 + x
                                    position_y = self.rect.y // 120 + y
                                    sell = data_sell_active[int(save_map[position_y][position_x])] \
                                        if self.col_vo_click % 2 != 0 else data_sell[int(save_map[position_y][position_x])]
                                    active.append([position_y, position_x])
                                    all_entity.map[position_y][position_x] = Map(position_x * 120, position_y * 120, sell)
                                    active = [] if self.col_vo_click % 2 == 0 else active
                    self.last_left_click = 0 if pygame.mouse.get_pressed()[0] == 0 else 1
                # Открытие инвентаря
                key_e = 1 if key_e > 2 else key_e
                all_entity.invent = True if key_e == 2 else False

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
            all_entity = Updating(map_y,
                                  Hero(*data_saves[1]),
                                  Cums(*data_saves[2]))
        elif data_saves is None:
            # Создание и сохранение карты
            save_map = []
            map_y = []
            for y in range(QUANTITY_SELL[1]):
                save_map_x = ''
                map_x = []
                for x in range(QUANTITY_SELL[0]):
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
                                  Cums(51 * SIZE_SELL, 51 * SIZE_SELL + SIZE_SELL // 2))
        camera = Camera(camera_configure, total_width, total_height)

    def save_game():
        global person, save_map, flag_esc_menu
        if flag_esc_menu:
            # Карта. Персонажи. Положение картинки игрока. Положение камеры.
            data_t = [[], [], [], []]
            data_t[0] = save_map
            for pers in person.personalities:
                temp = [pers.name, pers.surname, pers.age, list(pers.special), list(pers.skills), list(pers.buff),
                        list(pers.de_buff), pers.hp, pers.hunger, pers.water, pers.control, pers.stress,
                        pers.left_arm, pers.right_arm, pers.back, pers.pockets]
                data_t[1].append(temp)
            data_t[2] = [all_entity.hero.rect.x, all_entity.hero.rect.y]
            data_t[3] = [all_entity.cam.rect.x, all_entity.cam.rect.y]
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
        global DATA_SAVE, back

        def load(n):
            def helper_load():
                global person
                per = DATA_SAVE[n][1]
                person = Data_pers(len(per), True)
                for pers in range(len(per)):
                    person.personalities[pers].name, person.personalities[pers].surname = per[pers][0], per[pers][1]
                    person.personalities[pers].age = per[pers][2]
                    person.personalities[pers].special = set(per[pers][3])
                    person.personalities[pers].skills = set(per[pers][4])
                    person.personalities[pers].buff = set(per[pers][5])
                    person.personalities[pers].de_buff = set(per[pers][6])
                    person.personalities[pers].hp = per[pers][7]
                    person.personalities[pers].hunger, person.personalities[pers].water = per[pers][8], per[pers][9]
                    person.personalities[pers].control, person.personalities[pers].stress = per[pers][10], per[pers][
                        11]
                    person.personalities[pers].left_arm = per[pers][12]
                    person.personalities[pers].right_arm = per[pers][13]
                    person.personalities[pers].back, person.personalities[pers].pockets = per[pers][14], per[pers][15]
                print(person)
                working_objects([DATA_SAVE[n][0], DATA_SAVE[n][2], DATA_SAVE[n][3]])
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
                    inventory()

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
            self.preset = ['Вы - одиночка, с запасом самого необходимого, для выживания.']

        def one(self):
            global person
            if person is None:
                person = Data_pers(1)
                print(person)
                working_objects()
                save_game()
                game()

            """Отладочная характеристика персонажа(персонажей)"""

        def one_print(self):
            return Presets().preset[0]

    def menu():
        def new_game():
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


start_game()
