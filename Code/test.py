from Code.Person import Data_pers, Action
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



