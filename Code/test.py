import pygame


pygame.init()
display = pygame.display.set_mode((1920, 1080))
back_menu = pygame.image.load('../Data/menu.jpg')
display.blit(back_menu, (0, 0))
display.blit(pygame.transform.scale(pygame.image.load("../Data/items/spear.png"), (120, 120)), (600, 240))
pygame.display.update()
while True:
    pass
