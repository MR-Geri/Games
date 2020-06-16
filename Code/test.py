from Code.Person import Data_pers
from Code.Graphics import blur
import json
import pygame
import random
import time


FPS = 60
# Flag
flag_esc_menu = True
# Флаги для циклов
ESC_MENU = False
NEW_GAME = False
OK_LOAD = False
LOAD_GAME = False
MENU = False
OPTION = False
EXIT = False
GAME = False
FLAG = [NEW_GAME, OK_LOAD, LOAD_GAME, MENU, OPTION, EXIT, GAME, ESC_MENU]
# Для сохранения карты
save_map = []
# Для карты и камеры
MAP = None
hero = None
camera = None
# Для камеры, движения и карты
WIN_WIDTH = 1920
WIN_HEIGHT = 1080
QUANTITY_SELL = (101, 101)
SIZE_SELL = 120
COLOR = "#888888"
MOVE = 10
left = right = False
up = down = False
# Ячейки для карты
data_sell = ['cell.jpg', 'cell_0.jpg', 'cell_1.jpg', 'cell_2.jpg', 'cell_3.jpg', 'cell_4.jpg']
# Левый клик
click_left = False
# Персонаж
person = None
# Настройки
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
        global click_left
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.w and y < mouse[1] < y + self.h:
            pygame.draw.rect(display, self.active_color, (x, y, self.w, self.h))
            flag = 0 if click_left is False else 1
            click_left = True if click[0] == 1 and flag == 0 else False
            if click_left and action is not None:
                if action is quit:
                    pygame.quit()
                    quit()
                else:
                    time.sleep(time_sleep)
                    action()
        else:
            pygame.draw.rect(display, self.inactive_color, (x, y, self.w, self.h))
        print_text(message=message, x=x + self.ots_x, y=y + self.ots_y, font_size=size)

    def draw_act(self, x, y, message=None, action=None, size=30, act=(), time_sleep=0.0):
        global click_left
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.w and y < mouse[1] < y + self.h:
            pygame.draw.rect(display, self.active_color, (x, y, self.w, self.h))
            flag = 0 if click_left is False else 1
            click_left = True if click[0] == 1 and flag == 0 else False
            if click_left and action is not None:
                if action is quit:
                    pygame.quit()
                    quit()
                if action is not None:
                    time.sleep(time_sleep)
                    action(act)
        else:
            pygame.draw.rect(display, self.inactive_color, (x, y, self.w, self.h))
        print_text(message=message, x=x + self.ots_x, y=y + self.ots_y, font_size=size)

    def draw_info(self, x, y, message=None, action=None, action_info=None, size=30):
        global click_left
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.w and y < mouse[1] < y + self.h:
            pygame.draw.rect(display, self.active_color, (x, y, self.w, self.h))
            pygame.draw.rect(display, self.inactive_color, (680, 700, 980, 600))
            print_text(action_info(), 700, 720)
            flag = 0 if click_left is False else 1
            click_left = True if click[0] == 1 and flag == 0 else False
            if click_left and action is not None:
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
        global flag_esc_menu
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
            continue_button.draw(720, 395, 'Продолжить', game)
            save_button.draw(720, 455, 'Сохранить игру', save_game)
            load_button.draw_act(720, 515, 'Загрузить игру', load_game, act='esc', time_sleep=0.25)
            option_button.draw_act(720, 575, 'Настройки', options_game, act='esc')
            menu_button.draw(720, 635, 'Выход в главное меню', menu)
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                    game()
            pygame.display.update()

    def gen_map(map_saves=None):
        class Map(pygame.sprite.Sprite):
            def __init__(self, x, y, graphic_sell):
                pygame.sprite.Sprite.__init__(self)
                self.image = pygame.image.load(f'../Data/data_sell/{graphic_sell}')
                self.rect = self.image.get_rect(center=(x + 60, y + 60))

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
                self.image = pygame.Surface((120, 120))
                self.rect = pygame.Rect(x, y, 120, 120)  # прямоугольный объект

            def update(self, left, right, up, down):
                self.x_vel = 0
                self.y_vel = 0
                if up and self.rect.y > 540:
                    self.y_vel = -MOVE

                if down and self.rect.y < total_height - 540:
                    self.y_vel = MOVE

                if left and self.rect.x > 960:
                    self.x_vel = -MOVE  # Лево = x- n

                if right and self.rect.x < total_width - 960:
                    self.x_vel = MOVE  # Право = x + n

                self.rect.y += self.y_vel
                self.rect.x += self.x_vel

        global save_map, MAP, hero, camera
        # Загрузочный экран
        display.blit(back_menu, (0, 0))
        pygame.draw.rect(display, (212, 92, 0), (850, 510, 245, 45))
        print_text('Идёт загрузка', 860, 520)
        pygame.display.update()
        #
        total_width = QUANTITY_SELL[0] * SIZE_SELL  # Высчитываем фактическую ширину уровня
        total_height = QUANTITY_SELL[1] * SIZE_SELL  # высоту
        hero = Cums(51 * SIZE_SELL, 51 * SIZE_SELL + 60)
        MAP = pygame.sprite.Group()  # Все объекты
        MAP.add(hero)
        if map_saves is not None:
            # Загрузка карты
            for y in range(QUANTITY_SELL[1]):
                for x in range(QUANTITY_SELL[0]):
                    MAP.add(Map(int(x) * 120, int(y) * 120, data_sell[int(map_saves[int(y)][int(x)])]))
        elif map_saves is None:
            # Создание и сохранение карты
            save_map_y = []
            for y in range(QUANTITY_SELL[1]):
                save_map_x = ''
                for x in range(QUANTITY_SELL[0]):
                    if y == 51 and (x == 50 or x == 51):
                        graphic_cell = data_sell[0]
                    else:
                        graphic_cell = random.choice(data_sell[1:])
                    save_map_x += str(data_sell.index(graphic_cell))
                    MAP.add(Map(x * 120, y * 120, graphic_cell))
                save_map_y.append(save_map_x)
        camera = Camera(camera_configure, total_width, total_height)
        return MAP, hero, camera

    def save_game():
        global person, save_map, flag_esc_menu
        if flag_esc_menu:
            if person is not None:
                data_t = [[], []]
                data_t[0] = save_map_y
                for pers in person.personalities:
                    temp = [pers.name, pers.surname, pers.age, list(pers.special), list(pers.skills), list(pers.buff),
                            list(pers.de_buff), pers.hp, pers.hunger, pers.water, pers.control, pers.stress,
                            pers.left_arm, pers.right_arm, pers.back, pers.pockets]
                    data_t[-1].append(temp)
                try:
                    data = json.load(open('../Save_Loading/save.json'))
                except:
                    data = []
                if data_t in data:
                    data[data.index(data_t)] = data_t
                    print('Сохранение заменено.')
                else:
                    data.append(data_t)
                    print('Сохранение создано.')

                with open('../Save_Loading/save.json', 'w') as file:
                    json.dump(data, file, indent=2, ensure_ascii=False)
                flag_esc_menu = False
            else:
                print('Игра не создана.')

    def load_game(flag):
        def helper_load(number):
            global person
            per = DATA_SAVE[number][1]
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
            gen_map(DATA_SAVE[number][0])
            game()
            print(f'Игра загружена.')

        class Helper_load:
            def __init__(self, n):
                self.n = n

            def load(self):
                if len(DATA_SAVE) > int(self.n):
                    helper_load(self.n)
                else:
                    if flag == 'esc':
                        for e in MAP:
                            display.blit(e.image, camera.apply(e))
                    else:
                        display.blit(pygame.image.frombuffer(blur(), (1920, 1080), "RGB"), (0, 0))
                    ok_button = Button(w=480, h=50, x=210, y=14)
                    flag_all_false()
                    FLAG[OK_LOAD] = True
                    while FLAG[OK_LOAD]:
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

        if flag == 'esc':
            back = game
        elif flag == 'menu':
            display.blit(pygame.image.frombuffer(blur(), (1920, 1080), "RGB"), (0, 0))
            back = menu
        back_button = Button(w=110, h=50, y=14)
        saves_button = Button(w=480, h=50, x=160, y=14)
        pygame.display.update()
        flag_all_false()
        FLAG[LOAD_GAME] = True
        while FLAG[LOAD_GAME]:
            is_active_display()
            pygame.draw.rect(display, (255, 255, 0), (700, 385, 520, 308))
            back_button.draw(10, 10, 'Назад', back, time_sleep=0.25)
            saves_button.draw(720, 395, 'Ячейка 1.', Helper_load(0).load, time_sleep=0.25)
            saves_button.draw(720, 455, 'Ячейка 2.', Helper_load(1).load, time_sleep=0.25)
            saves_button.draw(720, 515, 'Ячейка 3.', Helper_load(2).load, time_sleep=0.25)
            saves_button.draw(720, 575, 'Ячейка 4.', Helper_load(3).load, time_sleep=0.25)
            saves_button.draw(720, 635, 'Ячейка 5.', Helper_load(4).load, time_sleep=0.25)
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                    back()
            pygame.display.update()

    def options_game(flag):
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

        if flag == 'esc':
            back = game
        elif flag == 'menu':
            display.blit(pygame.image.frombuffer(blur(), (1920, 1080), "RGB"), (0, 0))
            back = menu
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
        display.blit(pygame.image.frombuffer(blur(), (1920, 1080), "RGB"), (0, 0))
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
        global left, right, up, down
        global MAP, hero, camera
        # загрузочный экран
        display.blit(back_menu, (0, 0))
        flag_all_false()
        FLAG[GAME] = True
        while FLAG[GAME]:
            is_active_display()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    esc_menu()

                if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                    up = True
                if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
                    left = True
                if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
                    right = True
                if e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
                    down = True

                if e.type == pygame.KEYUP and e.key == pygame.K_UP:
                    up = False
                if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
                    right = False
                if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
                    left = False
                if e.type == pygame.KEYUP and e.key == pygame.K_DOWN:
                    down = False
            display.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать
            camera.update(hero)  # центризируем камеру относительно персонажа
            hero.update(left, right, up, down)  # передвижение
            for e in MAP:
                display.blit(e.image, camera.apply(e))

            pygame.display.update()  # обновление и вывод всех изменений на экран

    class Presets:
        def __init__(self):
            self.preset = ['Вы - одиночка, с запасом самого необходимого, для выживания.']

        def one(self):
            global person
            if person is None:
                person = Data_pers(1)
                print(person)
                gen_map()
                save_game()
                game()

            """Отладочная характеристика персонажа(персонажей)"""

        def one_print(self):
            return Presets().preset[0]

    def menu():
        def new_game():
            display.blit(pygame.image.frombuffer(blur(), (1920, 1080), "RGB"), (0, 0))
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

        global person
        person = None
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
            save_load_button.draw_act(820, 700, 'Загрузить игру', load_game, act='menu')
            options_button.draw_act(820, 800, 'Настройки', options_game, act='menu')
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
            display = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        else:
            display = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Geri_Games_INC")
        back_menu = pygame.image.load('../Data/menu.jpg')
        display.blit(back_menu, (0, 0))
        bg = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        # clock = pygame.time.Clock() ---- clock.tick(FPS)
        pygame.mixer_music.load('../Data/menu.mp3')
        pygame.mixer_music.set_volume(volume)
        pygame.mixer_music.play(-1)
        menu()

    start_menu()


start_game()