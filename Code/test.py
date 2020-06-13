from Code.Person import Data_pers
from Code.Graphics import blur
import json
import pygame
import random
import time


FPS = 60
DATA_SAVE = json.load(open('../Save_Loading/save.json'))
# Для камеры и карты

# Флаги для циклов
NEW_GAME = True
OK_LOAD = True
LOAD_GAME = True
MENU = True
OPTION = True
EXIT = True
GAME = True
FLAG = [NEW_GAME, OK_LOAD, LOAD_GAME, MENU, OPTION, EXIT, GAME]
# Для камеры, движения и карты
WIN_WIDTH = 1920
WIN_HEIGHT = 1080
QUANTITY_SELL = (101, 101)
SIZE_SELL = 120
COLOR = "#888888"
MOVE = 10
left = right = False
up = down = False
# Левый клик
click_left = False
# Персонаж
person = None
# Настройки
active_display = 0
FullScreen = False
volume = float(json.load(open('../Save_Loading/settings.json')))


def gen_map():
    class Map(pygame.sprite.Sprite):
        def __init__(self, x, y, flag):
            pygame.sprite.Sprite.__init__(self)
            temp = ['cell_0.jpg', 'cell_1.jpg', 'cell_2.jpg', 'cell_3.jpg', 'cell_4.jpg']
            if flag:
                t = 'cell.jpg'
            else:
                t = random.choice(temp)
            self.image = pygame.image.load(f'../Data/data_sell/{t}')
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

    total_width = QUANTITY_SELL[0] * SIZE_SELL  # Высчитываем фактическую ширину уровня
    total_height = QUANTITY_SELL[1] * SIZE_SELL  # высоту
    hero = Cums(51 * SIZE_SELL, 51 * SIZE_SELL + 60)
    MAP = pygame.sprite.Group()  # Все объекты
    MAP.add(hero)
    for y in range(QUANTITY_SELL[1]):
        for x in range(QUANTITY_SELL[0]):
            if y == 51 and (x == 50 or x == 51):
                MAP.add(Map(x * 120, y * 120, True))
            else:
                MAP.add(Map(x * 120, y * 120, False))
    camera = Camera(camera_configure, total_width, total_height)
    return MAP, hero, camera


with open('../Save_Loading/save.json', 'w') as file:
    json.dump(hero, file, indent=2, ensure_ascii=False)