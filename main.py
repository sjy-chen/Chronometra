import pygame as pg
import sys
from settings import *
from sprites import *
from os import path
from tilemap import *
import random
# import main_game_loop

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.orange_collected = False
        self.purple_collected = False
        self.yellow_collected = False
        self.green_collected = False
        self.orange_placed = False
        self.purple_placed = False
        self.yellow_placed = False
        self.green_placed = False
        self.next_level = False
        self.bf = False

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'img')
        self.map_folder = path.join(self.game_folder, 'maps')
        self.player_img_front = pg.image.load(path.join(self.img_folder, 'Main Character Front.png')).convert_alpha()
        self.player_img_back = pg.image.load(path.join(self.img_folder, 'Main Character Back.png')).convert_alpha()
        self.player_img_left = pg.image.load(path.join(self.img_folder, 'Main Character Left.png')).convert_alpha()
        self.player_img_right = pg.image.load(path.join(self.img_folder, 'Main Character Right.png')).convert_alpha()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bossfight = pg.sprite.Group()
        self.yellow = pg.sprite.Group()
        self.orange = pg.sprite.Group()
        self.purple = pg.sprite.Group()
        self.green = pg.sprite.Group()
        self.imgs = {'stone': TiledMap(path.join(self.map_folder, 'Stone.tmx')),
                     'lava': TiledMap(path.join(self.map_folder, 'Lava.tmx'))}
        if self.next_level:
            self.map = self.imgs['lava']
        elif not self.next_level:
            self.map = self.imgs['stone']
        if self.map == self.imgs['stone']:
            maps = 'Stone'
            print(maps)
        elif self.map == self.imgs['lava']:
            maps = 'Lava'
            print(maps)
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
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
        if self.next_level:
            self.playing = False
        green_hit = pg.sprite.spritecollide(self.player, self.green, False)
        if green_hit:
            if self.map == self.imgs['stone']:
                status = 'Green ore collected.'
                print(status)
                self.green_collected = True
            elif self.map == self.imgs['lava']:
                status = 'Green ore placed.'
                print(status)
                self.green_placed = True

        purple_hit = pg.sprite.spritecollide(self.player, self.purple, False)
        if purple_hit:
            if self.map == self.imgs['stone']:
                status = 'Purple ore collected.'
                print(status)
                self.purple_collected = True
            elif self.map == self.imgs['lava']:
                status = 'Purple ore placed.'
                print(status)
                self.purple_placed = True

        orange_hit = pg.sprite.spritecollide(self.player, self.orange, False)
        if orange_hit:
            if self.map == self.imgs['stone']:
                status = 'Orange ore collected.'
                print(status)
                self.orange_collected = True
            elif self.map == self.imgs['lava']:
                status = 'Orange ore placed.'
                print(status)
                self.orange_placed = True

        yellow_hit = pg.sprite.spritecollide(self.player, self.yellow, False)
        if yellow_hit:
            if self.map == self.imgs['stone']:
                status = 'Yellow ore collected.'
                print(status)
                self.yellow_collected = True
            elif self.map == self.imgs['lava']:
                status = 'Yellow ore placed.'
                print(status)
                self.yellow_placed = True

        bossfight = pg.sprite.spritecollide(self.player, self.bossfight, False)
        if bossfight:
            if self.map == self.imgs['stone']:
                if self.yellow_collected and self.orange_collected and self.purple_collected and self.green_collected:
                    status = 'Next Level!'
                    print(status)
                    self.next_level = True
                else:
                    status = 'Collect all the ores!'
                    print(status)
            if self.map == self.imgs['lava']:
                if self.yellow_placed and self.orange_placed and self.purple_placed and self.green_placed:
                    status = 'Boss Fight!'
                    print(status)
                    self.bf = True
                else:
                    status = 'Place all the ores!'
                    print(status)

        if self.next_level:
            self.new()
            self.next_level = False

        if self.bf:
            exec(open('main_game_loop.py').read())
            self.quit()


    # def draw_grid(self):
    #     for x in range(0, WIDTH, TILESIZE):
    #         pg.draw.line(self.screen, LIGHTGREY, (x,0), (x, HEIGHT))
    #     for y in range(0, HEIGHT, TILESIZE):
    #         pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

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

    def show_load_screen(self):
        background = pg.image.load(path.join(path.join(path.dirname(__file__), 'img'), 'Loading.png')).convert_alpha()
        background_rect = background.get_rect()
        pg.display.set_mode((WIDTH, HEIGHT)).blit(background, background_rect)
        pg.display.flip()
        pg.event.wait()
        waiting = True
        while waiting:
            pg.time.Clock().tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYUP or event.type == pg.MOUSEBUTTONDOWN:
                    waiting = False

# create the game object
g = Game()
g.new()
g.show_start_screen()
# g.show_load_screen()
while not g.bf:
    g.run()

# global win
# win = pg.display.set_mode((800, 800))
#
#
# #title and Icon
# pg.display.set_caption("Chronometra")
# icon = pg.image.load('Images\Chronometra Icon.png')
# pg.display.set_icon(icon)
#
# class player(object):
#     def __init__(self, x, y, move):
#         self.x = x
#         self.y = y
#         self.move = move
#         self.vel = 0.5
#     def draw(self, win):
#         if self.move != "hidden":
#             if self.move == "s": mainCharacter = pg.image.load('Images\Main Character Front.png')
#             elif self.move == "a": mainCharacter = pg.image.load('Images\Main Character Left.png')
#             elif self.move == "d": mainCharacter = pg.image.load('Images\Main Character Right.png')
#             elif self.move == "w": mainCharacter = pg.image.load('Images\Main Character Back.png')
#             win.blit(mainCharacter, (self.x, self.y))
#
# class fireball(object):
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.vel = 10
#
#     def draw(self, win):
#         win.blit(pg.image.load('Images\Fire Ball Right.png'), (self.x, self.y))
#
# class heart(object):
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.vel = 7
#         self.rage = 0
#     def draw(self, win):
#         win.blit(pg.image.load('Images\Heart.png'), (self.x, self.y))
#         #health bar
#         pg.draw.rect(win, (255, 0, 0), (10, 400, 100, 20))
#         if self.rage < 100: pg.draw.rect(win, (0, 255, 0), (10 + self.rage, 400, 100 - self.rage, 20))
#
#     def hit(self):
#         for fb in fireballs:
#             if fb.x >= h.x - 16 and fb.x <= h.x + 16 and fb.y >= h.y - 16 and fb.y <= h.y + 16:
#                 fireballs.pop(fireballs.index(fb))
#                 self.rage += 5
#         for fs in fireSpirits:
#             if fs.x >= h.x - 16 and fs.x <= h.x + 16 and fs.y >= h.y - 16 and fs.y <= h.y + 16:
#                 fireSpirits.pop(fireSpirits.index(fs))
#                 self.rage += 3
#         if len(lasers) != 0 and lasers[0].status == "shoot" and h.y >= lasers[0].y - 50 and h.y <= lasers[0].y + 15:
#             self.rage += 5
#
#
# class laser(object):
#     def __init__(self, y):
#         self.x = 295
#         self.y = y
#         self.timer = 0
#         self.status = "ready"
#     def draw(self, win):
#         if self.status == "ready":
#             pg.draw.rect(win, (255, 0, 0), (self.x, self.y, 220, 3))
#         else:
#             win.blit(pg.image.load('Images\Laser.png'), (self.x - 50, self.y - 150))
#
# class actB(object):
#     def __init__(self):
#         self.x = 80
#         self.y = 500
#         self.status = "not chosen"
#     def draw(self, win):
#         mouseX, mouseY = pg.mouse.get_pos()
#         if mouseX >= self.x and mouseX <= self.x + 228 and mouseY >= self.y and mouseY <= self.y + 108:
#             self.status = "chosen"
#             win.blit(pg.image.load('Images\Act Chosen.png'), (self.x, self.y))
#         else:
#             self.status = "not chosen"
#             win.blit(pg.image.load('Images\Act.png'), (self.x, self.y))
#
# class fightB(object):
#     def __init__(self):
#         self.x = 500
#         self.y = 500
#         self.status = "not chosen"
#     def draw(self, win):
#         mouseX, mouseY = pg.mouse.get_pos()
#         if mouseX >= self.x and mouseX <= self.x + 228 and mouseY >= self.y and mouseY <= self.y + 108:
#             self.status = "chosen"
#             win.blit(pg.image.load('Images\Fight Chosen.png'), (self.x, self.y))
#         else:
#             self.status = "not chosen"
#             win.blit(pg.image.load('Images\Fight.png'), (self.x, self.y))
#
# class text(object):
#     def __init__(self):
#         self.timer = 0
#     def draw(self, win):
#         if act and not fight:
#             font = pg.font.SysFont('Comic Sans MS', 30)
#             t = font.render('The Demon Blushes Deeply At Your Compliment.', False, (255, 255, 255))
#             win.blit(t, (50, 500))
#         else:
#             font = pg.font.SysFont('Comic Sans MS', 30)
#             t = font.render('The Violence Increased Your Rage.', False, (255, 255, 255))
#             win.blit(t, (150, 500))
#             t2 = font.render('It Is Not The Way.', False, (255, 255, 255))
#             win.blit(t2, (150, 600))
#
# class fireSpirit(object):
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.timer = 0
#     def draw(self, win):
#         win.blit(pg.image.load('Images\Fire Spirit.png'), (int(self.x), int(self.y)))
#
#
# def redrawGameWindow():
#     if puzzle: p.draw(win)
#     if bossfight:
#         win.blit(pg.image.load('Images\Boss Fight Screen.png'), (0, 0))
#         win.blit(pg.image.load('Images\WrathDemon.png'), (275, 0))
#         h.draw(win)
#         for fb in fireballs:
#             fb.draw(win)
#         if len(lasers) != 0: lasers[0].draw(win)
#         for fs in fireSpirits:
#             fs.draw(win)
#     if playermove:
#         win.blit(pg.image.load('Images\Playermove Background.png'), (0, 0))
#         win.blit(pg.image.load('Images\WrathDemon.png'), (275, 0))
#         if not act and not fight:
#             a.draw(win)
#             f.draw(win)
#         elif t.timer < 30:
#             t.draw(win)
#             t.timer += 1
#     if end and not playermove:
#         if h.rage > 100:
#             win.blit(pg.image.load('Images\Bad Ending BG.png'), (0, 0))
#             font = pg.font.SysFont('Comic Sans MS', 30)
#             txt = font.render('You Have Been Consumed By Your Rage.', False, (255, 255, 255))
#             txt2 = font.render('GAME OVER', False, (255, 255, 255))
#             win.blit(txt, (150, 400))
#             win.blit(txt2, (300, 500))
#         elif compliment >= 2:
#             win.blit(pg.image.load('Images\Weird Ending ish.png'), (0, 0))
#             win.blit(pg.image.load('Images\WrathDemon.png'), (200, 300))
#             win.blit(pg.image.load('Images\Main Character Front.png'), (500, 400))
#             font = pg.font.SysFont('Comic Sans MS', 25)
#             txt = font.render('After Your Compliments, The Demon Falls In Love With You.', False, (255, 255, 255))
#             txt2 = font.render('You Live Happily Ever After. THE END', False, (255, 255, 255))
#             win.blit(txt, (30, 600))
#             win.blit(txt2, (120, 700))
#         else:
#             font = pg.font.SysFont('Comic Sans MS', 25)
#             txt = font.render('CONGRADULATIONS! You Survived The Wrath Demon.', False, (255, 255, 255))
#             txt2 = font.render('THE END.', False, (255, 255, 255))
#             win.blit(txt, (70, 400))
#             win.blit(txt2, (350, 500))
#
#     pg.display.update()
#
# global compliment
# compliment = 0
# act = False
# fight = False
# bossfight = True
# playermove = False
# puzzle = False
# end = False
# temp = 0
# global fireballs
# fireballs = []
# global lasers
# lasers = []
# global fireSpirits
# fireSpirits = []
# stage = 1
# p = player(450, 300, "s")
# h = heart(384, 574)
# t = text()
# global tick
# tick = 0
# # game loop
# running = False
# if g.bf:
#     running = True
#     g.quit()
# while running:
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             running = False
#
#     keys = pg.key.get_pressed()
#     if keys[pg.K_s] and puzzle:
#         p.y += p.vel
#         p.move = "s"
#     elif keys[pg.K_s] and bossfight and h.y <= 657:
#         h.y += h.vel
#     if keys[pg.K_d] and puzzle:
#         p.x += p.vel
#         p.move = "d"
#     elif keys[pg.K_d] and bossfight and h.x <= 473:
#         h.x += h.vel
#     if keys[pg.K_a] and puzzle:
#         p.x -= p.vel
#         p.move = "a"
#     elif keys[pg.K_a] and bossfight and h.x >= 295:
#         h.x -= h.vel
#     if keys[pg.K_w] and puzzle:
#         p.y -= p.vel
#         p.move = "w"
#     elif keys[pg.K_w] and bossfight and h.y >= 480:
#         h.y -= h.vel
#     if playermove and pg.mouse.get_pressed()[0] and a.status == "chosen":
#         act = True
#         compliment += 1
#     elif playermove and pg.mouse.get_pressed()[0] and f.status == "chosen":
#         fight = True
#         h.rage += 5
#
#
#
#     if bossfight and stage <= 3:
#         p.move = "hidden"
#         if stage == 1:
#             if temp != 50:
#                 y = random.randint(470, 647)
#                 fireballs.append(fireball(10, y))
#                 temp += 1
#             if temp == 50 and len(fireballs) == 0:
#                 stage += 1
#                 temp = 0
#                 bossfight = False
#                 playermove = True
#         elif stage == 2:
#             if temp != 5:
#                 y = random.randint(470, 647)
#                 lasers.append(laser(y))
#                 temp += 1
#             if len(lasers) != 0:
#                 if lasers[0].timer == 10:
#                     lasers[0].status = "shoot"
#                 elif lasers[0].timer == 20:
#                     lasers.pop(0)
#                 if len(lasers) != 0: lasers[0].timer += 1
#             else:
#                 bossfight = False
#                 stage += 1
#                 temp = 0
#                 playermove = True
#         elif stage == 3:
#             x = random.randint(100, 500)
#             if temp != 70:
#                 fireSpirits.append(fireSpirit(x, 470))
#                 temp += 1
#             if len(fireSpirits) != 0:
#                 for fs in fireSpirits:
#                     if fs.y > 800:
#                         fireSpirits.pop(fireSpirits.index(fs))
#                     else:
#                         fs.timer += 1
#             else:
#                 end = True
#                 bossfight = False
#                 playermove = False
#
#     if h.rage > 100:
#         end = True
#         bossfight = False
#         playermove = False
#
#     if playermove and not fight and not act:
#         a = actB()
#         f = fightB()
#
#     for fs in fireSpirits:
#         velx = random.randint(1, 10)
#         vely = random.randint(1, 10)
#         fs.x += velx
#         fs.y += vely
#     for fb in fireballs:
#         if fb.x > 0 and fb.x < 800:
#             fb.x += fb.vel
#         else:
#             fireballs.pop(fireballs.index(fb))
#
#     if t.timer == 30:
#         bossfight = True
#         playermove = False
#         t.timer = 0
#         fight = False
#         act = False
#
#     h.hit()
#     win.fill((0, 0, 0))
#     redrawGameWindow()
# pg.quit()
