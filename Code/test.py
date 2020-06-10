import pygame


WIN_WIDTH = 1920
WIN_HEIGHT = 1080
WIDTH = 10
HEIGHT = 10
COLOR = "#888888"
JUMP_POWER = 10
GRAVITY = 0.35 # Сила, которая будет тянуть нас вниз
MOVE_SPEED = 7


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
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = - l + WIN_WIDTH / 2, - t + WIN_HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return pygame.Rect(l, t, w, h)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill(pygame.Color(COLOR))
        self.rect = pygame.Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.image.set_colorkey(pygame.Color(COLOR))  # делаем фон прозрачным

    def update(self, left, right, up, platforms):

        if up:
            self.yvel = -JUMP_POWER
            self.image.fill(pygame.Color(COLOR))

        if left:
            self.xvel = -MOVE_SPEED  # Лево = x- n
            self.image.fill(pygame.Color(COLOR))

        if right:
            self.xvel = MOVE_SPEED  # Право = x + n
            self.image.fill(pygame.Color(COLOR))

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0

        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p): # если есть пересечение платформы с игроком

                if xvel > 0:                      # если движется вправо
                    self.rect.right = p.rect.left # то не движется вправо

                if xvel < 0:                      # если движется влево
                    self.rect.left = p.rect.right # то не движется влево

                if yvel > 0:                      # если падает вниз
                    self.rect.bottom = p.rect.top # то не падает вниз
                    self.onGround = True          # и становится на что-то твердое
                    self.yvel = 0                 # и энергия падения пропадает

                if yvel < 0:                      # если движется вверх
                    self.rect.top = p.rect.bottom
                    self.yvel = 0


pygame.init()
display = pygame.display.set_mode((1920, 1080))
bg = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
back_menu = pygame.image.load('../Data/menu.jpg')
left = right = False  # по умолчанию - стоим
up = False
hero = Player(10, 10)
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

        if e.type == pygame.KEYUP and e.key == pygame.K_UP:
            up = False
        if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
            right = False
        if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
            left = False
    display.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать

    camera.update(hero)  # центризируем камеру относительно персонажа
    hero.update(left, right, up)  # передвижение
    # entities.draw(screen) # отображение
    for e in entities:
        display.blit(e.image, camera.apply(e))

    pygame.display.update()  # обновление и вывод всех изменений на экран
