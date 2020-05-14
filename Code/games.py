from Code.Person import Data_pers, Action
from Save_Loading.json_save_loader import save, load
import json
import pygame


FPS = 60
person = None


def new():
    global person
    person = Data_pers(1)


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


def print_text(message, x, y, font_color=(0, 0, 0), font_type='Data/shrift.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


class Button:
    def __init__(self, w, h, x=10, y=10, inactive_color=(13, 162, 58), active_color=(23, 204, 58)):
        self.w, self.h, self.inactive_color, self.active_color = w, h, inactive_color, active_color
        self.ots_x, self.ots_y = x, y

    def draw(self, x, y, message, action=None, size=30):
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


def menu():
    run_game = True
    ex_button = Button(w=200, h=80, y=20, x=50)
    new_button = Button(w=200, h=60)
    save_load_button = Button(w=200, h=60)
    pygame.mixer_music.load('Data/menu.mp3')
    pygame.mixer_music.set_volume(0.05)
    pygame.mixer_music.play(-1)

    while run_game:
        new_button.draw(860, 500, 'Новая игра', new)
        save_load_button.draw(860, 700, 'Загрузить игру', load_game)
        ex_button.draw(860, 900, 'Выход', quit, 50)
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()
        clock.tick(FPS)


pygame.init()
display = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
clock = pygame.time.Clock()
back_menu = pygame.image.load('Data/menu.jpg')
menu_rect = back_menu.get_rect(bottomright=(1920, 1080))
display.blit(back_menu, (0, 0))
menu()
