import pygame, sys
from sprites import Sprites

from settings import *


pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

sprites = Sprites()






while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    sprites.player_move()
    

    screen.blit(sprites.background_image, sprites.background_rect)
    screen.blit(sprites.player_image, sprites.player_rect)

    sprites.create_tile()

    pygame.display.update()
    clock.tick(FPS)

    
    #print()

