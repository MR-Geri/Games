from Code.Person import Data_pers
from Code.Graphics import blur
import json
import pygame


FPS = 60
DATA_SAVE = json.load(open('../Save_Loading/save.json'))
#
NEW_GAME = True
OK_LOAD = True
LOAD_GAME = True
MENU = True
OPTION = True
EXIT = True
GAME = True
FLAG = [NEW_GAME, OK_LOAD, LOAD_GAME, MENU, OPTION, EXIT, GAME]
#
WIN_WIDTH = 1920
WIN_HEIGHT = 1080
QUANTITY_SELL = (101, 101)
SIZE_SELL = 120
COLOR = "#888888"
MOVE = 10
left = right = False
up = down = False
person = None
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

    def draw(self, x, y, message=None, action=None, size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.w and y < mouse[1] < y + self.h:
            pygame.draw.rect(display, self.active_color, (x, y, self.w, self.h))
            if click[0] == 1 and action is not None:
                if action is quit:
                    pygame.quit()
                    quit()
                if action is not None:
                    action()
        else:
            pygame.draw.rect(display, self.inactive_color, (x, y, self.w, self.h))
        print_text(message=message, x=x + self.ots_x, y=y + self.ots_y, font_size=size)

    def draw_info(self, x, y, message=None, action=None, action_info=None, size=30):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.w and y < mouse[1] < y + self.h:
            pygame.draw.rect(display, self.active_color, (x, y, self.w, self.h))
            pygame.draw.rect(display, self.inactive_color, (680, 700, 980, 600))
            print_text(action_info(), 700, 720)
            if click[0] == 1 and action is not None:
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


def game():
    global left, right, up, down

    class Map(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('../Data/cell.jpg')
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
        temp = pygame.Rect(int(lo), int(t), int(w), int(h))
        return temp

    class Cums(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.x_vel = 0  # скорость перемещения. 0 - стоять на месте
            self.y_vel = 0  # скорость вертикального перемещения
            self.image = pygame.Surface((120, 120))
            self.rect = pygame.Rect(x, y - 60, 120, 120)  # прямоугольный объект

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

    total_width = QUANTITY_SELL[0] * SIZE_SELL  # Высчитываем фактическую ширину уровня
    total_height = QUANTITY_SELL[1] * SIZE_SELL  # высоту
    hero = Cums(51 * SIZE_SELL, 51 * SIZE_SELL)
    entities = pygame.sprite.Group()  # Все объекты
    entities.add(hero)
    # загрузочный экран
    display.blit(back_menu, (0, 0))
    pygame.draw.rect(display, (212, 92, 0), (850, 510, 245, 45))
    print_text('Идёт загрузка', 860, 520)
    pygame.display.update()
    for y in range(QUANTITY_SELL[1]):
        for x in range(QUANTITY_SELL[0]):
            entities.add(Map(x * 120, y * 120))
    camera = Camera(camera_configure, total_width, total_height)
    flag_all_false()
    FLAG[GAME] = True
    while FLAG[GAME]:
        is_active_display()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
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
        for e in entities:
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
            game()

        """Отладочная характеристика персонажа(персонажей)"""

    def one_print(self):
        return Presets().preset[0]


def save_game():
    def helper_save(data_save):
        data_t = []
        for pers in data_save.personalities:
            temp = [pers.name, pers.surname, pers.age, list(pers.special), list(pers.skills), list(pers.buff),
                    list(pers.de_buff), pers.hp, pers.hunger, pers.water, pers.control, pers.stress,
                    pers.left_arm, pers.right_arm, pers.back, pers.pockets]
            data_t.append(temp)
        try:
            data = json.load(open('../Save_Loading/save.json'))
        except:
            data = []
        data.append(data_t)
        with open('../Save_Loading/save.json', 'w') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    global person
    if person is not None:
        helper_save(person)
        print('Игра сохранена.')
    else:
        print('Игра не создана.')


def menu():
    def new_game():
        display.blit(pygame.image.frombuffer(blur(), (1920, 1080), "RGB"), (0, 0))
        preset_button = Button(w=480, h=50, x=75, y=14)
        back_button = Button(w=110, h=50, y=14)
        flag_all_false()
        FLAG[NEW_GAME] = True
        # тут генерируем карту
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

    def load_game():
        def helper_load(number):
            global person
            if person is None:
                temp = DATA_SAVE[number]
                person = Data_pers(len(temp), True)
                for pers in range(len(temp)):
                    person.personalities[pers].name, person.personalities[pers].surname = temp[pers][0], temp[pers][1]
                    person.personalities[pers].age = temp[pers][2]
                    person.personalities[pers].special = set(temp[pers][3])
                    person.personalities[pers].skills = set(temp[pers][4])
                    person.personalities[pers].buff = set(temp[pers][5])
                    person.personalities[pers].de_buff = set(temp[pers][6])
                    person.personalities[pers].hp = temp[pers][7]
                    person.personalities[pers].hunger, person.personalities[pers].water = temp[pers][8], temp[pers][9]
                    person.personalities[pers].control, person.personalities[pers].stress = temp[pers][10], temp[pers][
                        11]
                    person.personalities[pers].left_arm = temp[pers][12]
                    person.personalities[pers].right_arm = temp[pers][13]
                    person.personalities[pers].back, person.personalities[pers].pockets = temp[pers][14], temp[pers][15]
                print(person)
                print(f'Игра загружена.')

        class Helper_load:
            def __init__(self, n):
                self.n = n

            def load(self):
                if len(DATA_SAVE) <= self.n:
                    display.blit(pygame.image.frombuffer(blur(), (1920, 1080), "RGB"), (0, 0))
                    ok_button = Button(w=110, h=50, y=14)
                    flag_all_false()
                    FLAG[OK_LOAD] = True
                    while FLAG[OK_LOAD]:
                        is_active_display()
                        ok_button.draw(10, 10, 'Назад', menu)
                        ok_button.draw(1000, 600, 'Ок', load_game)
                        pygame.draw.rect(display, (255, 255, 0), (910, 500, 100, 40))
                        for i in pygame.event.get():
                            if i.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                            if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                                load_game()
                        pygame.display.update()
                else:
                    helper_load(self.n)
        flag_all_false()
        FLAG[LOAD_GAME] = True
        display.blit(pygame.image.frombuffer(blur(), (1920, 1080), "RGB"), (0, 0))
        pygame.display.update()
        back_button = Button(w=110, h=50, y=14)
        saves_button = Button(w=480, h=50, x=160, y=10)
        while FLAG[LOAD_GAME]:
            is_active_display()
            pygame.draw.rect(display, (255, 255, 0), (700, 385, 520, 308))
            back_button.draw(10, 10, 'Назад', menu)
            saves_button.draw(720, 395, 'Ячейка 1.', Helper_load(0).load)
            saves_button.draw(720, 455, 'Ячейка 2.', Helper_load(1).load)
            saves_button.draw(720, 515, 'Ячейка 3.', Helper_load(2).load)
            saves_button.draw(720, 575, 'Ячейка 4.', Helper_load(3).load)
            saves_button.draw(720, 635, 'Ячейка 5.', Helper_load(4).load)
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                    menu()
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

        display.blit(pygame.image.frombuffer(blur(), (1920, 1080), "RGB"), (0, 0))
        back_button = Button(w=110, h=50, y=14)
        volume_button = Button(w=100, h=100, x=35, y=35)
        flag_all_false()
        FLAG[OPTION] = True
        while FLAG[OPTION]:
            is_active_display()
            pygame.draw.rect(display, (255, 255, 0), (700, 385, 520, 308))
            back_button.draw(10, 10, 'Назад', menu)
            volume_button.draw(940, 420, '', volume_minus)
            volume_button.draw(1080, 420, '', volume_plus)
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                    menu()
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
                if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                    menu()
            pygame.display.update()

    display.blit(back_menu, (0, 0))
    ex_button = Button(w=200, h=80, x=27, y=20)
    new_game_button = Button(w=280, h=50, x=52, y=13)
    save_load_button = Button(w=280, h=50, x=20, y=13)
    options_button = Button(w=280, h=50, x=55, y=13)
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


def start_game():
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


start_game()
