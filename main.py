import pygame, sys
from sprites import *
from settings import *
from support import import_csv_layout



class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('Mefika.ttf', 32)
        
        self.player_spritesheet = Spritesheet('./PlayerSpriteSheet.png')
        self.josh_spritesheet = Spritesheet('./JoshSpriteSheet.png')
        self.enemy_spritesheet = Spritesheet('./SlimeSpriteSheet.png')
        self.terrain_spritesheet = Spritesheet('./Floor.png')
        self.water_spritesheet = Spritesheet('./Water.png')
        self.nature_spritesheet = Spritesheet('./TilesetNature.png')
        self.house_spritesheet = Spritesheet('./TilesetHouse.png')
        self.logic_spritesheet = Spritesheet('./Logic.png')

        self.floorblock_csv = import_csv_layout('./map/map_FloorBlock.csv')
        self.floor_csv = import_csv_layout('./map/map_Floor.csv')
        self.tree_csv = import_csv_layout('./map/map_Trees.csv')
        self.houses_csv = import_csv_layout('./map/map_Houses.csv')
        self.objects_csv = import_csv_layout('./map/map_Objects.csv')
        self.grass_csv = import_csv_layout('./map/map_Grass.csv')
        self.enemy_csv = import_csv_layout('./map/map_Enemy.csv')
        self.josh_csv = import_csv_layout('./map/map_Josh.csv')
        self.player_csv = import_csv_layout('./map/map_Player.csv')

        self.killed_enemies = 0

    def create_tiles(self):
        for row_index, row in enumerate(self.floorblock_csv):
            for col_index, value in enumerate(row):
                if value != '-1':
                    FloorBlockTile(self, col_index-OFFSET, row_index-OFFSET)

        for row_index, row in enumerate(self.floor_csv):
            for col_index, value in enumerate(row):
                FloorTile(self, col_index-OFFSET, row_index-OFFSET, value)

        for row_index, row in enumerate(self.objects_csv):
            for col_index, value in enumerate(row):
                if value != '-1':
                    ObjectTile(self, col_index-OFFSET, row_index-OFFSET, value)

        for row_index, row in enumerate(self.houses_csv):
            for col_index, value in enumerate(row):
                if value != '-1':
                    HouseTile(self, col_index-OFFSET, row_index-OFFSET)

        for row_index, row in enumerate(self.grass_csv):
            for col_index, value in enumerate(row):
                if value != '-1':
                     GrassTile(self, col_index-OFFSET, row_index-OFFSET)

        for row_index, row in enumerate(self.enemy_csv):
            for col_index, value in enumerate(row):
                if value != '-1':
                     Enemy(self, col_index-OFFSET, row_index-OFFSET)

        for row_index, row in enumerate(self.josh_csv):
            for col_index, value in enumerate(row):
                if value != '-1':
                    Josh(self, col_index-OFFSET, row_index-OFFSET)

        for row_index, row in enumerate(self.player_csv):
            for col_index, value in enumerate(row):
                if value != '-1':
                    self.player = Player(self, col_index, row_index)

    def new_game(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.destroyable = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()
        self.dialog = pygame.sprite.LayeredUpdates()

        self.create_tiles()

    def draw(self):
        self.screen.fill('black')
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def update(self):
        self.all_sprites.update()

    def main(self):
        while True:
            global DIALOG_LAYER
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        Attack(self, self.player.rect.x, self.player.rect.y)

                    if event.key == pygame.K_f:
                        Dialog(self, self.player.rect.x, self.player.rect.y)
                        Conversation(self, self.player.rect.x, self.player.rect.y)





            self.draw()
            self.update()

            self.clock.tick(FPS)
            pygame.display.update()    

game = Game()
game.new_game()

while True:
    game.main()
    
        


