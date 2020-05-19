from Code.Person import Data_pers
from Code.Graphics import blur
import json
import pygame


FPS = 60
person = None
active_display = 0
volume = float(json.load(open('../Save_Loading/settings.json')))


def is_active_display():
    global active_display, volume
    if pygame.display.get_active() == 0:
        pygame.mixer.music.pause()
        active_display = 1
    elif active_display == 1 and pygame.display.get_active() == 1:
        active_display = 0
        pygame.mixer_music.unpause()


class Presets:
    def __init__(self):
        self.preset = ['Вы - одиночка, с запасом самого необходимого, для выживания.']

    def one(self):
        global person
        if person is None:
            person = Data_pers(1)
            print(person)
        """Отладочная характеристика персонажа(персонажей)"""

    def one_print(self):
        return Presets().preset[0]


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
                pygame.time.delay(300)
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
                pygame.time.delay(50)
                if action is quit:
                    pygame.quit()
                    quit()
                if action is not None:
                    action()
        else:
            display.blit(back_menu, (0, 0))
            print_text(message=message, x=x + self.ots_x, y=y + self.ots_y, font_size=size)
            pygame.draw.rect(display, self.inactive_color, (x, y, self.w, self.h))
            pygame.time.delay(100)
        print_text(message=message, x=x + self.ots_x, y=y + self.ots_y, font_size=size)


def new_game():
    display.blit(back_menu, (0, 0))
    preset_button = Button(w=480, h=50, x=75, y=14)
    back_button = Button(w=110, h=50, y=14)
    while True:
        is_active_display()
        preset_button.draw_info(100, 700, 'Бывалый выживальщик.', Presets().one, Presets().one_print)
        back_button.draw(10, 10, 'Назад', menu)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                quit()
            if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                menu()
        pygame.display.update()


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


def load_game():
    def helper_load(number):
        global person
        if person is None:
            temp = json.load(open('../Save_Loading/save.json'))
            temp = temp[number]
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
                person.personalities[pers].control, person.personalities[pers].stress = temp[pers][10], temp[pers][11]
                person.personalities[pers].left_arm = temp[pers][12]
                person.personalities[pers].right_arm = temp[pers][13]
                person.personalities[pers].back, person.personalities[pers].pockets = temp[pers][14], temp[pers][15]
            print('Игра загружена.')

    display.blit(back_menu, (0, 0))
    saves_button = Button(w=480, h=50, x=10, y=10)
    while True:
        is_active_display()
        saves_button.draw(200, 200, 'Ячейка 1.', helper_load)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                quit()
            if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                menu()
        pygame.display.update()


def options():
    def volume_minus():
        global volume
        volume -= 0.01
        volume = 0 if volume < 0 else volume
        with open('../Save_Loading/settings.json', 'w') as file:
            json.dump(volume, file, indent=2, ensure_ascii=False)
        pygame.mixer_music.set_volume(volume)

    def volume_plus():
        global volume
        volume += 0.01
        with open('../Save_Loading/settings.json', 'w') as file:
            json.dump(volume, file, indent=2, ensure_ascii=False)
        pygame.mixer_music.set_volume(volume)

    display.blit(pygame.image.frombuffer(blur(), (1920, 1080), "RGB"), (0, 0))
    back_button = Button(w=110, h=50, y=14)
    settings_opt = Button(w=100, h=100, x=35, y=35)
    while True:
        is_active_display()
        back_button.draw(10, 10, 'Назад', menu)
        settings_opt.draw(100, 100, '', volume_plus)
        settings_opt.draw(100, 210, '', volume_minus)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                quit()
            if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                menu()
        pygame.display.update()


def menu():
    display.blit(back_menu, (0, 0))
    ex_button = Button(w=200, h=80, x=27, y=20)
    new_game_button = Button(w=280, h=50, x=52, y=13)
    save_load_button = Button(w=280, h=50, x=20, y=13)
    options_button = Button(w=280, h=50, x=55, y=13)
    while True:
        is_active_display()
        new_game_button.draw(820, 600, 'Новая игра', new_game)
        save_load_button.draw(820, 700, 'Загрузить игру', load_game)
        options_button.draw(820, 800, 'Настройки', options)
        ex_button.draw(860, 900, 'Выход', quit, 50)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()


def start_game():
    global display, back_menu
    pygame.init()
    display = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    back_menu = pygame.image.load('../Data/menu.jpg')
    display.blit(back_menu, (0, 0))
    # clock = pygame.time.Clock() ---- clock.tick(FPS)
    pygame.mixer_music.load('../Data/menu.mp3')
    pygame.mixer_music.set_volume(volume)
    pygame.mixer_music.play(-1)
    menu()


start_game()
