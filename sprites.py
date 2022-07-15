import pygame

from settings import *

class Sprites:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.player_image = pygame.image.load('./player.png').convert_alpha()
        self.player_rect = self.player_image.get_rect(center = (640, 360))

        self.map_x = 640
        self.map_y = 360
        self.background_image = pygame.image.load('./ground2.png').convert_alpha()
        self.background_rect = self.background_image.get_rect(center = (self.map_x, self.map_y))

        self.tile_x = 0
        self.tile_y = 0
        self.tile_image = pygame.image.load('./rock.png').convert_alpha()
        self.tile_rect = self.tile_image.get_rect(center = (self.tile_x, self.tile_y))

    def create_tile(self):
        for row_index,row in enumerate(GAME_MAP):
            for col_index, col in enumerate(row):
                self.tile_x = col_index * TILESIZE
                self.tile_y = row_index * TILESIZE
                if col == 'x':
                    self.tile_rect = self.tile_image.get_rect(topleft = (self.tile_x, self.tile_y))
                    self.display_surface.blit(self.tile_image, self.tile_rect)
    
    def player_move(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            self.player_rect.move_ip(0, -10)
            #self.background_rect.move_ip(0, 10)

        if key[pygame.K_s]:
            self.player_rect.move_ip(0, 10)
            #self.background_rect.move_ip(0, -10)

        if key[pygame.K_a]:
            self.player_rect.move_ip(-10, 0)
            #self.background_rect.move_ip(10, 0)

        if key[pygame.K_d]:
            self.player_rect.move_ip(10, 0)
            #self.background_rect.move_ip(-10, 0)




    
