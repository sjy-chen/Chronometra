import pygame as pg
import sys
from settings import *
from sprites import *
from os import path
from tilemap import *
import random

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')
        self.imgs = {'stone': TiledMap(path.join(map_folder, 'Stone.tmx')), 'lava': TiledMap(path.join(map_folder, 'Lava.tmx'))}
        self.type = random.choice(['stone', 'lava'])
        self.map = self.imgs[self.type]
        if self.map == self.imgs['stone']:
            maps = 'stone'
            print(maps)
        elif self.map == self.imgs['lava']:
            maps = 'lava'
            print(maps)
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img_front = pg.image.load(path.join(img_folder, 'Main Character Front.png')).convert_alpha()
        self.player_img_back = pg.image.load(path.join(img_folder, 'Main Character Back.png')).convert_alpha()
        self.player_img_left = pg.image.load(path.join(img_folder, 'Main Character Left.png')).convert_alpha()
        self.player_img_right = pg.image.load(path.join(img_folder, 'Main Character Right.png')).convert_alpha()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bossfight = pg.sprite.Group()
        self.yellow = pg.sprite.Group()
        self.orange = pg.sprite.Group()
        self.purple = pg.sprite.Group()
        self.green = pg.sprite.Group()
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'Player':
                self.player = Player(self, tile_object.x, tile_object.y)
            if tile_object.name == 'Walls':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'Boss Fight':
                Boss_Fight(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'Green':
                Green(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'Purple':
                Purple(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'Orange':
                Orange(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'Yellow':
                Yellow(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
        self.camera = Camera(self.map.width, self.map.height)


    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        green_hit = pg.sprite.spritecollide(self.player, self.green, False)
        if green_hit:
            if self.map == self.imgs['stone']:
                green = True
                status = 'Green ore collected.'
                print(status)
            elif self.map == self.imgs['lava']:
                status = 'Green ore placed.'
                print(status)

        purple_hit = pg.sprite.spritecollide(self.player, self.purple, False)
        if purple_hit:
            if self.map == self.imgs['stone']:
                status = 'Purple ore collected.'
                print(status)
            elif self.map == self.imgs['lava']:
                status = 'Purple ore placed.'
                print(status)

        orange_hit = pg.sprite.spritecollide(self.player, self.orange, False)
        if orange_hit:
            if self.map == self.imgs['stone']:
                status = 'Orange ore collected.'
                print(status)
            elif self.map == self.imgs['lava']:
                status = 'Orange ore placed.'
                print(status)

        yellow_hit = pg.sprite.spritecollide(self.player, self.yellow, False)
        if yellow_hit:
            if self.map == self.imgs['stone']:
                status = 'Yellow ore collected.'
                print(status)
            elif self.map == self.imgs['lava']:
                status = 'Yellow ore placed.'
                print(status)

        bossfight = pg.sprite.spritecollide(self.player, self.bossfight, False)
        if bossfight:
            if self.map == self.imgs['stone']:
                status = 'Next Level!'
                print(status)
            elif self.map == self.imgs['lava']:
                status = 'Boss Fight!'
                print(status)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x,0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()