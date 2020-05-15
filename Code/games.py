from Code.Person import Data_pers, Action
from Save_Loading.json_save_loader import save, load
import json
import pygame


FPS = 60
person = None
run_menu = False
run_preset = False


class Presets:
    def __init__(self):
        self.preset = ['Вы - одиночка, с запасом самого необходимого, для выживания.']

    def one(self):
        global person
        person = Data_pers(1)
        """Отладочная характеристика персонажа(персонажей)"""
        print(person)

    def one_print(self):
        return Presets().preset[0]


def print_text(message, x, y, font_color=(0, 0, 0), font_type='Data/shrift.ttf', font_size=30):
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
                pygame.time.delay(100)
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
                pygame.time.delay(100)
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
    global run_menu, run_preset, display, back_menu, menu_rect
    display.blit(back_menu, (0, 0))
    preset_button = Button(w=480, h=50, x=75, y=14)
    run_menu, run_preset = False, True
    pygame.display.update()
    while run_preset:
        preset_button.draw_info(100, 700, 'Бывалый выживальщик.', Presets().one, Presets().one_print)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                quit()
            if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                run_menu = False
                menu()
        pygame.display.update()
        clock.tick(FPS)


def save_game():
    global person
    if person is not None:
        save(person)
        print('Игра сохранена.')
    else:
        print('Игра не создана.')


def load_game():
    global person
    try:
        temp = json.load(open('Save_Loading/save.json'))
        person = load()
        print('Игра загружена.')
    except:
        print('Нет сохранения.')


def menu():
    global run_menu, back_menu
    run_menu = True
    display.blit(back_menu, (0, 0))
    pygame.display.update()
    ex_button = Button(w=200, h=80, x=27, y=20)
    new_game_button = Button(w=280, h=50, x=52, y=13)
    save_load_button = Button(w=280, h=50, x=20, y=13)

    while run_menu:
        new_game_button.draw(820, 600, 'Новая игра', new_game)
        save_load_button.draw(820, 700, 'Загрузить игру', load_game)
        ex_button.draw(860, 900, 'Выход', quit, 50)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()
        clock.tick(FPS)


def start_game():
    global display, back_menu, menu_rect, clock
    display = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    back_menu = pygame.image.load('Data/menu.jpg')
    menu_rect = back_menu.get_rect(bottomright=(1920, 1080))
    display.blit(back_menu, (0, 0))
    pygame.mixer_music.load('Data/menu.mp3')
    pygame.mixer_music.set_volume(0.05)
    pygame.mixer_music.play(-1)
    menu()


pygame.init()
start_game()

