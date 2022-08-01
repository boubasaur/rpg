import pygame
import math
import random
from settings import *
from support import *

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width, height])
        sprite.blit(self.sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey('black')
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'
        self.animation_loop = 0

        self.image = self.game.player_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)


        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [
            self.game.player_spritesheet.get_sprite(0, 0,  TILESIZE, TILESIZE),
            self.game.player_spritesheet.get_sprite(0, 64, TILESIZE, TILESIZE),
            self.game.player_spritesheet.get_sprite(0, 128, TILESIZE, TILESIZE),
            self.game.player_spritesheet.get_sprite(0, 192, TILESIZE, TILESIZE),
        ]

        self.up_animations = [
            self.game.player_spritesheet.get_sprite(64, 0, TILESIZE, TILESIZE),
            self.game.player_spritesheet.get_sprite(64, 64, TILESIZE, TILESIZE),
            self.game.player_spritesheet.get_sprite(64, 128, TILESIZE, TILESIZE),
            self.game.player_spritesheet.get_sprite(64, 192, TILESIZE, TILESIZE),
        ]

        self.left_animations = [
            self.game.player_spritesheet.get_sprite(128, 0, TILESIZE, TILESIZE),
            self.game.player_spritesheet.get_sprite(128, 64, TILESIZE, TILESIZE),
            self.game.player_spritesheet.get_sprite(128, 128, TILESIZE, TILESIZE),
            self.game.player_spritesheet.get_sprite(128, 192, TILESIZE, TILESIZE),
        ]

        self.right_animations = [
            self.game.player_spritesheet.get_sprite(192, 0,  TILESIZE, TILESIZE),
            self.game.player_spritesheet.get_sprite(192, 64, TILESIZE, TILESIZE),
            self.game.player_spritesheet.get_sprite(192, 128, TILESIZE, TILESIZE),
            self.game.player_spritesheet.get_sprite(192, 192, TILESIZE, TILESIZE),
        ]

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x += PLAYER_SPEED
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
        if keys[pygame.K_RIGHT]:
            for sprite in self.game.all_sprites:
                sprite.rect.x -= PLAYER_SPEED
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
        if keys[pygame.K_UP]:
            for sprite in self.game.all_sprites:
                sprite.rect.y += PLAYER_SPEED
            self.y_change -= PLAYER_SPEED
            self.facing = 'up'
        if keys[pygame.K_DOWN]:
            for sprite in self.game.all_sprites:
                sprite.rect.y -= PLAYER_SPEED
            self.y_change += PLAYER_SPEED
            self.facing = 'down'

    def animate(self):
        if self.facing =='down':
            if self.y_change == 0:
                self.image = self.game.player_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 4:
                    self.animation_loop = 0
                    
        if self.facing =='up':
            if self.y_change == 0:
                self.image = self.game.player_spritesheet.get_sprite(64, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1  
                if self.animation_loop >= 4:
                    self.animation_loop = 0

        if self.facing =='left':
            if self.x_change == 0:
                self.image = self.game.player_spritesheet.get_sprite(128, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1  
                if self.animation_loop >= 4:
                    self.animation_loop = 0

        if self.facing =='right':
            if self.x_change == 0:
                self.image = self.game.player_spritesheet.get_sprite(192, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1  
                if self.animation_loop >= 4:
                    self.animation_loop = 0

    def collide_blocks(self, direction):
        if direction == 'x':
            bonk = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if bonk:
                if self.x_change > 0:
                    self.rect.x = bonk[0].rect.left - self.rect.width
                    for sprite in self.game.all_sprites:
                        sprite.rect.x += PLAYER_SPEED
                if self.x_change < 0:
                    self.rect.x = bonk[0].rect.right
                    for sprite in self.game.all_sprites:
                        sprite.rect.x -= PLAYER_SPEED

        if direction == 'y':
            bonk = pygame.sprite.spritecollide(self, self.game.blocks, False) 
            if bonk:
                if self.y_change > 0:
                    self.rect.y = bonk[0].rect.top - self.rect.height
                    for sprite in self.game.all_sprites:
                        sprite.rect.y += PLAYER_SPEED
                if self.y_change < 0:
                    self.rect.y = bonk[0].rect.bottom
                    for sprite in self.game.all_sprites:
                        sprite.rect.y -= PLAYER_SPEED

    def update(self):
        self.move()
        self.animate()

        self.rect.x += self.x_change
        self.collide_blocks('x')

        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0


class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y

        self.animation_loop = 0

        self.image = self.game.player_spritesheet.get_sprite(0, 128, TILESIZE, TILESIZE)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [
            self.game.player_spritesheet.get_sprite(0, 256, TILESIZE, TILESIZE),
            self.game.player_spritesheet.get_sprite(0, 320, TILESIZE, TILESIZE),
        ]

        self.up_animations = [
            self.game.player_spritesheet.get_sprite(64, 256, TILESIZE, TILESIZE),
            self.game.player_spritesheet.get_sprite(64, 320, TILESIZE, TILESIZE),
        ]

        self.left_animations = [
            self.game.player_spritesheet.get_sprite(128, 256, TILESIZE, TILESIZE),
            self.game.player_spritesheet.get_sprite(128, 320, TILESIZE, TILESIZE),
        ]

        self.right_animations = [
            self.game.player_spritesheet.get_sprite(192, 256, TILESIZE, TILESIZE),
            self.game.player_spritesheet.get_sprite(192, 320, TILESIZE, TILESIZE),
        ]

    def kill_enemies(self):
        pygame.sprite.pygame.sprite.spritecollide(self, self.game.enemies, True)

    def destroy_object(self):
        pygame.sprite.pygame.sprite.spritecollide(self, self.game.destroyable, True)

    def animate(self):
        direction = self.game.player.facing

        if direction == 'up':
            self.image = self.up_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 2:
                self.kill()

        if direction == 'down':
            self.image = self.down_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 2:
                self.kill()

        if direction == 'left':
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 2:
                self.kill()

        if direction == 'right':
            self.image = self.right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 2:
                self.kill()

    def update(self):
        self.animate()
        self.kill_enemies()
        self.destroy_object()


class Dialog(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.dialog
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.display_image = pygame.display.get_surface()
        self.font = pygame.font.Font('Mefika.ttf', 70)

        self.box()

        
    def box(self):
        self.image = pygame.image.load('./DialogBox.png').convert()
        self.image = pygame.transform.rotozoom(self.image, 0, 3.5)
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect(center=(WIDTH/2, HEIGHT-105))

        self.display_image.blit(self.image, self.rect)
          

class Conversation(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = DIALOG_LAYER
        self.groups = self.game.all_sprites, self.game.dialog
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.display_image = pygame.display.get_surface()
        self.font = pygame.font.Font('Mefika.ttf', 100)

        self.talking()

    def talking(self):
        self.image = self.font.render('hi', True, 'black')
        self.rect = self.image.get_rect(center=(WIDTH/2, HEIGHT-70))
        self.display_image.blit(self.image, self.rect)


class FloorBlockTile(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = FLOORBLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.image = self.game.logic_spritesheet.get_sprite(256, 0, TILESIZE, TILESIZE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class FloorTile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, value):
        self.game = game
        self._layer = FLOOR_LAYER
        self.groups = self.game.all_sprites,
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.tile_sprites = {
            '245': self.game.terrain_spritesheet.get_sprite(192, 704, TILESIZE, TILESIZE), #floor

            '201': self.game.water_spritesheet.get_sprite(320, 448, TILESIZE, TILESIZE), #border top left corner
            '202': self.game.water_spritesheet.get_sprite(384, 448, TILESIZE, TILESIZE), #border top right corner
            '168': self.game.water_spritesheet.get_sprite(0, 384, TILESIZE, TILESIZE), #main border top left corner
            '169': self.game.water_spritesheet.get_sprite(64, 384, TILESIZE, TILESIZE), #main border top
            '170': self.game.water_spritesheet.get_sprite(128, 384, TILESIZE, TILESIZE), #main border top right corner
            '196': self.game.water_spritesheet.get_sprite(0, 448, TILESIZE, TILESIZE), #main border left
            '198': self.game.water_spritesheet.get_sprite(128, 448, TILESIZE, TILESIZE), #border right
            '224': self.game.water_spritesheet.get_sprite(0, 512, TILESIZE, TILESIZE), #main border bottom left corner
            '225': self.game.water_spritesheet.get_sprite(64, 512, TILESIZE, TILESIZE), #main border bottom
            '226': self.game.water_spritesheet.get_sprite(128, 512, TILESIZE, TILESIZE), #main border bottom right corner
            '229': self.game.water_spritesheet.get_sprite(320, 512, TILESIZE, TILESIZE), #border bottom left corner
            '230': self.game.water_spritesheet.get_sprite(384, 512, TILESIZE, TILESIZE), #border bottom right corner
            
            '336': self.game.water_spritesheet.get_sprite(0, 768, TILESIZE, TILESIZE), # left of bridge
            '364': self.game.water_spritesheet.get_sprite(0, 832, TILESIZE, TILESIZE), #left of bridge
            '392': self.game.water_spritesheet.get_sprite(0, 896, TILESIZE, TILESIZE), #left of bridge
            '337': self.game.water_spritesheet.get_sprite(64, 768, TILESIZE, TILESIZE), #middle of bridge
            '365': self.game.water_spritesheet.get_sprite(64, 832, TILESIZE, TILESIZE), #middle of bridge
            '393': self.game.water_spritesheet.get_sprite(64, 896, TILESIZE, TILESIZE), #middle of bridge
            '338': self.game.water_spritesheet.get_sprite(128, 768, TILESIZE, TILESIZE), #right of bridge
            '366': self.game.water_spritesheet.get_sprite(128, 832, TILESIZE, TILESIZE), #right of bridge
            '394': self.game.water_spritesheet.get_sprite(128, 896, TILESIZE, TILESIZE), #right of bridge

            '29': self.game.water_spritesheet.get_sprite(64, 64, TILESIZE, TILESIZE), #water
        }

        self.image = self.tile_sprites[value]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class ObjectTile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, value):
        self.game = game
        self._layer = OBJECT_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.tile_sprites = {
            '1': self.game.nature_spritesheet.get_sprite(128, 0, 128, 128),   #tree
            '156': self.game.house_spritesheet.get_sprite(704, 320, TILESIZE, TILESIZE),   #fence
        }

        self.image = self.tile_sprites[value]
        self.rect = self.image.get_rect()
        self.rect = self.rect.inflate(-10, -40)

        self.rect.x = self.x
        self.rect.y = self.y - 64

class HouseTile(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = HOUSE_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.image = self.game.house_spritesheet.get_sprite(768, 0, 255, 192)

        self.rect = self.image.get_rect()
        self.rect = self.rect.inflate(-10, -40)
        self.rect.x = self.x
        self.rect.y = self.y - 128

class GrassTile(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GRASS_LAYER
        self.groups = self.game.all_sprites, self.game.destroyable
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE

        self.all_images = [
            self.game.nature_spritesheet.get_sprite(0, 640, TILESIZE, TILESIZE), 
            self.game.nature_spritesheet.get_sprite(64, 640, TILESIZE, TILESIZE), 
            self.game.nature_spritesheet.get_sprite(128, 640, TILESIZE, TILESIZE), 
            self.game.nature_spritesheet.get_sprite(192, 640, TILESIZE, TILESIZE), 
            self.game.nature_spritesheet.get_sprite(256, 640, TILESIZE, TILESIZE), 

            self.game.nature_spritesheet.get_sprite(256, 704, TILESIZE, TILESIZE), 
            self.game.nature_spritesheet.get_sprite(320, 704, TILESIZE, TILESIZE), 
            self.game.nature_spritesheet.get_sprite(384, 704, TILESIZE, TILESIZE), 
        ]
        self.image = random.choice(self.all_images)

        self.rect = self.image.get_rect()
        self.rect = self.rect.inflate(-20, -50)
        
        self.rect.x = self.x
        self.rect.y = self.y


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE


        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['down', 'up', 'left', 'right'])
        self.animation_loop = 0
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30)

        self.image = self.game.enemy_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)

        self.image.set_colorkey('white')

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [
            self.game.enemy_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.enemy_spritesheet.get_sprite(0, 64, TILESIZE, TILESIZE),
            self.game.enemy_spritesheet.get_sprite(0, 128, TILESIZE, TILESIZE),
            self.game.enemy_spritesheet.get_sprite(0, 192, TILESIZE, TILESIZE),
        ]

        self.up_animations = [
            self.game.enemy_spritesheet.get_sprite(64, 0, TILESIZE, TILESIZE),
            self.game.enemy_spritesheet.get_sprite(64, 64, TILESIZE, TILESIZE),
            self.game.enemy_spritesheet.get_sprite(64, 128, TILESIZE, TILESIZE),
            self.game.enemy_spritesheet.get_sprite(64, 192, TILESIZE, TILESIZE),
        ]

        self.left_animations = [
            self.game.enemy_spritesheet.get_sprite(128, 0, TILESIZE, TILESIZE),
            self.game.enemy_spritesheet.get_sprite(128, 64, TILESIZE, TILESIZE),
            self.game.enemy_spritesheet.get_sprite(128, 128, TILESIZE, TILESIZE),
            self.game.enemy_spritesheet.get_sprite(128, 192, TILESIZE, TILESIZE),
        ]

        self.right_animations = [
            self.game.enemy_spritesheet.get_sprite(192, 0, TILESIZE, TILESIZE),
            self.game.enemy_spritesheet.get_sprite(192, 64, TILESIZE, TILESIZE),
            self.game.enemy_spritesheet.get_sprite(192, 128, TILESIZE, TILESIZE),
            self.game.enemy_spritesheet.get_sprite(192, 192, TILESIZE, TILESIZE),
        ]

    def move(self):
        if self.facing == 'down':
            self.y_change  += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(['down', 'up', 'left', 'right'])

        if self.facing == 'up':
            self.y_change  -= ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(['down', 'up', 'left', 'right'])

        if self.facing == 'left':
            self.x_change  -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['down', 'up', 'left', 'right'])

        if self.facing == 'right':
            self.x_change  += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(['down', 'up', 'left', 'right'])

    def animate(self):
        if self.facing =='down':
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(64, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1  
                if self.animation_loop >= 4:
                    self.animation_loop = 0

        if self.facing =='up':
            if self.y_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(64, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1  
                if self.animation_loop >= 4:
                    self.animation_loop = 0

        if self.facing =='left':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(128, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1  
                if self.animation_loop >= 4:
                    self.animation_loop = 0

        if self.facing =='right':
            if self.x_change == 0:
                self.image = self.game.enemy_spritesheet.get_sprite(192, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1  
                if self.animation_loop >= 4:
                    self.animation_loop = 0

    def collide_blocks(self, direction):
        if direction == 'x':
            bonk = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if bonk:
                if self.x_change > 0:
                    self.rect.x = bonk[0].rect.left - self.rect.width
                   
                if self.x_change < 0:
                    self.rect.x = bonk[0].rect.right
                   

        if direction == 'y':
            bonk = pygame.sprite.spritecollide(self, self.game.blocks, False) 
            if bonk:
                if self.y_change > 0:
                    self.rect.y = bonk[0].rect.top - self.rect.height
                    
                if self.y_change < 0:
                    self.rect.y = bonk[0].rect.bottom
                    
    def update(self):
        self.move()
        self.animate()

        self.rect.x += self.x_change
        self.collide_blocks('x')

        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0


class Josh(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE


        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['down', 'up', 'left', 'right'])
        self.animation_loop = 0
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30)

        self.image = self.game.josh_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE)

        #self.image.set_colorkey('white')

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.down_animations = [
            self.game.josh_spritesheet.get_sprite(0, 0, TILESIZE, TILESIZE),
            self.game.josh_spritesheet.get_sprite(0, 64, TILESIZE, TILESIZE),
            self.game.josh_spritesheet.get_sprite(0, 128, TILESIZE, TILESIZE),
            self.game.josh_spritesheet.get_sprite(0, 192, TILESIZE, TILESIZE),
        ]

        self.up_animations = [
            self.game.josh_spritesheet.get_sprite(64, 0, TILESIZE, TILESIZE),
            self.game.josh_spritesheet.get_sprite(64, 64, TILESIZE, TILESIZE),
            self.game.josh_spritesheet.get_sprite(64, 128, TILESIZE, TILESIZE),
            self.game.josh_spritesheet.get_sprite(64, 192, TILESIZE, TILESIZE),
        ]

        self.left_animations = [
            self.game.josh_spritesheet.get_sprite(128, 0, TILESIZE, TILESIZE),
            self.game.josh_spritesheet.get_sprite(128, 64, TILESIZE, TILESIZE),
            self.game.josh_spritesheet.get_sprite(128, 128, TILESIZE, TILESIZE),
            self.game.josh_spritesheet.get_sprite(128, 192, TILESIZE, TILESIZE),
        ]

        self.right_animations = [
            self.game.josh_spritesheet.get_sprite(192, 0, TILESIZE, TILESIZE),
            self.game.josh_spritesheet.get_sprite(192, 64, TILESIZE, TILESIZE),
            self.game.josh_spritesheet.get_sprite(192, 128, TILESIZE, TILESIZE),
            self.game.josh_spritesheet.get_sprite(192, 192, TILESIZE, TILESIZE),
        ]

        self.kamehameha_animations = [
            self.game.josh_spritesheet.get_sprite(0, 384, TILESIZE, TILESIZE),
            self.game.josh_spritesheet.get_sprite(64, 384, TILESIZE, TILESIZE),
            self.game.josh_spritesheet.get_sprite(128, 384, TILESIZE, TILESIZE),
            self.game.josh_spritesheet.get_sprite(192, 192, TILESIZE, TILESIZE),
        ]

    def move(self):
        if self.facing == 'down':
            self.y_change  += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(['down', 'up', 'left', 'right', 'kamehameha'])

        if self.facing == 'up':
            self.y_change  -= ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(['down', 'up', 'left', 'right', 'kamehameha'])

        if self.facing == 'left':
            self.x_change  -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.facing = random.choice(['down', 'up', 'left', 'right', 'kamehameha'])

        if self.facing == 'right':
            self.x_change  += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.facing = random.choice(['down', 'up', 'left', 'right', 'kamehameha'])

    def animate(self):
        if self.facing =='down':
            if self.y_change == 0:
                self.image = self.game.josh_spritesheet.get_sprite(64, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1  
                if self.animation_loop >= 4:
                    self.animation_loop = 0

        if self.facing =='up':
            if self.y_change == 0:
                self.image = self.game.josh_spritesheet.get_sprite(64, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1  
                if self.animation_loop >= 4:
                    self.animation_loop = 0

        if self.facing =='left':
            if self.x_change == 0:
                self.image = self.game.josh_spritesheet.get_sprite(128, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1  
                if self.animation_loop >= 4:
                    self.animation_loop = 0

        if self.facing =='right':
            if self.x_change == 0:
                self.image = self.game.josh_spritesheet.get_sprite(192, 0, TILESIZE, TILESIZE)
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1  
                if self.animation_loop >= 4:
                    self.animation_loop = 0

        if self.facing =='kamehameha':
            self.image = self.kamehameha_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.1  
            if self.animation_loop > 4:
                self.animation_loop = 0
                self.facing = random.choice(['down', 'up', 'left', 'right'])

    def collide_blocks(self, direction):
        if direction == 'x':
            bonk = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if bonk:
                if self.x_change > 0:
                    self.rect.x = bonk[0].rect.left - self.rect.width
                   
                if self.x_change < 0:
                    self.rect.x = bonk[0].rect.right
                   
        if direction == 'y':
            bonk = pygame.sprite.spritecollide(self, self.game.blocks, False) 
            if bonk:
                if self.y_change > 0:
                    self.rect.y = bonk[0].rect.top - self.rect.height
                    
                if self.y_change < 0:
                    self.rect.y = bonk[0].rect.bottom
                    
    def update(self):
        self.move()
        self.animate()

        self.rect.x += self.x_change
        self.collide_blocks('x')

        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0