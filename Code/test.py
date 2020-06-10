import pygame


WIN_WIDTH = 1920
WIN_HEIGHT = 1080
WIDTH = 10
HEIGHT = 10
COLOR = "#888888"
MOVE_SPEED = 7
left = right = False
up = down = False


class Map(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../Data/cell.jpg')
        self.rect = self.image.get_rect(center=(x + 50, y + 50))


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

    lo = min(0, lo)                           # Не движемся дальше левой границы
    lo = max(-(camera.width - WIN_WIDTH), lo)   # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы
    temp = pygame.Rect(int(lo), int(t), int(w), int(h))
    return temp


class Cums(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x_vel = 0  # скорость перемещения. 0 - стоять на месте
        self.y_vel = 0  # скорость вертикального перемещения
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.rect = pygame.Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект

    def update(self, left, right, up, down):
        self.x_vel = 0
        self.y_vel = 0
        if up:
            self.y_vel = -MOVE_SPEED

        if down:
            self.y_vel = MOVE_SPEED

        if left:
            self.x_vel = -MOVE_SPEED  # Лево = x- n

        if right:
            self.x_vel = MOVE_SPEED  # Право = x + n

        self.rect.y += self.y_vel
        self.rect.x += self.x_vel


pygame.init()
display = pygame.display.set_mode((1920, 1080))
bg = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
back_menu = pygame.image.load('../Data/menu.jpg')
hero = Cums(960, 540)
entities = pygame.sprite.Group()  # Все объекты
entities.add(hero)
display.blit(back_menu, (0, 0))
for y in range(100):
    for x in range(100):
        entities.add(Map(x * 100, y * 100))
# тут генерируем карту
total_level_width = 100 * 100  # Высчитываем фактическую ширину уровня
total_level_height = 100 * 100  # высоту

camera = Camera(camera_configure, total_level_width, total_level_height)
while True:
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
