# PyGame Template - framework for new pygame projects
import pygame as pg
import random
from os import path
from settings import *
from sprites import *

# assets folders
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, "img")
snd_folder = path.join(game_folder, "snd")

class Game:
    def __init__(self):
        # initialize game window etc.
        pg.init()  # init pygame
        pg.mixer.init()  # init mixer for sounds
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.menu = True
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # load high score etc.
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def new(self):
        if not self.running:
            return
        # start a new game
        self.menu = False
        self.score = 0
        self.all = pg.sprite.Group()
        self.borders = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all.add(self.player)
        # create platforms from preset list
        for plat in PLATFORM_LIST:
            p = Platform(*plat)  # explode list
            self.all.add(p)
            self.platforms.add(p)
            b = Border(plat[0]-2, plat[1]-2, plat[2]+4, plat[3]+4)
            self.all.add(b)
            self.borders.add(b)
        self.run()

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        # game loop - events
        for event in pg.event.get():
            # check for window close
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP or event.key == pg.K_w:
                    self.player.jump()
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.player.crouch()

    def update(self):
        # game loop - update
        self.all.update()

        # player stops and stands on platforms
        if self.player.vel.y > 0:
            land = pg.sprite.spritecollide(self.player, self.platforms, False)
            if land:
                self.player.pos.y = land[0].rect.top + 1
                self.player.vel.y = 0

        # move "camera" as player moves off-screen
        # climbing
        if self.player.rect.top <= HEIGHT * .25:
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT * 1.5:
                    plat.kill()
            for bord in self.borders:
                bord.rect.y += abs(self.player.vel.y)
                if bord.rect.top >= HEIGHT * 1.5:
                    bord.kill()
                    self.score += 1
        # falling
        if self.player.rect.top >= HEIGHT * .75 and len(self.platforms) > 0:
            self.player.pos.y -= abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y -= abs(self.player.vel.y)
                if plat.rect.top <= -abs(HEIGHT * 2):
                    plat.kill()
            for bord in self.borders:
                bord.rect.y -= abs(self.player.vel.y)
                if bord.rect.top <= -abs(HEIGHT * 2):
                    bord.kill()

        # DIE!!!
        if self.player.rect.top >= HEIGHT:
            self.playing = False


        # spawn new platforms
        while len(self.platforms) < 12 and self.player.rect.top <= HEIGHT * .75:
            width = random.randrange(75, 125)
            x = random.randrange(0, WIDTH-width)
            y = random.randrange(-HEIGHT, -HEIGHT + 20)
            p = Platform(x, y, width, 20)
            b = Border(x-2, y-2, width+4, 24)
            self.borders.add(b)
            self.all.add(b)
            self.platforms.add(p)
            self.all.add(p)

    def draw(self):
        # game loop - draw
        x = 50
        for i in range(0, 201):
            pg.draw.rect(self.screen, (75, x*.9, x), (0, HEIGHT - (HEIGHT/200)*i, WIDTH, (HEIGHT/200)))
            x += 1
        self.all.draw(self.screen)
        self.borders.draw(self.screen)
        self.platforms.draw(self.screen)
        self.draw_text(str(self.score), 24, BLACK, WIDTH/2, 15)

        pg.display.flip()   # always after drawing

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        surf = font.render(text, True, color)
        tRect = surf.get_rect()
        tRect.midtop = (x, y)
        self.screen.blit(surf, tRect)

    def start(self):
        if not self.running:
            return

        # draw background
        x = 50
        for i in range(0, 201):
            pg.draw.rect(self.screen, (0, x/2, x), (0, HEIGHT - (HEIGHT/200)*i, WIDTH, (HEIGHT/200)))
            x += 1

        # draw text and wait for user input
        self.draw_text(TITLE, 128, GREEN, WIDTH/2, HEIGHT/8)
        self.draw_text("ARROW KEYS/WASD TO MOVE", 24, WHITE, WIDTH/2, HEIGHT/2)
        self.draw_text("Press any key to start!", 36, WHITE, WIDTH/2, HEIGHT*.8)
        self.draw_text("High Score: " + str(self.highscore), 36, WHITE, WIDTH/2, HEIGHT*.9)

        pg.display.flip()
        self.wait_input()

    def gameover(self):
        if not self.running:
            return

        # draw background
        x = 50
        for i in range(0, 201):
            pg.draw.rect(self.screen, (x, x/4, x/4), (0, HEIGHT - (HEIGHT/200)*i, WIDTH, (HEIGHT/200)))
            x += 1

        # check and draw high schore
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 36, YELLOW, WIDTH / 2, HEIGHT * .43)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))

        # draw text and wait for user input
        self.draw_text("GAME", 128, BLACK, WIDTH/2, HEIGHT*.01)
        self.draw_text("OVER", 128, BLACK, WIDTH/2, HEIGHT*.2)
        self.draw_text("SCORE: " + str(self.score), 72, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to play again!", 36, WHITE, WIDTH/2, HEIGHT*.8)
        self.draw_text("(Q to quit to menu)", 24, WHITE, WIDTH/2, HEIGHT*.9)
        pg.display.flip()
        self.wait_input()

    def wait_input(self):
        # wait for user input in menus
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if self.menu == False and event.type == pg.KEYDOWN:
                    if event.key == pg.K_q:
                        self.menu = True
                if event.type == pg.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pg.KEYUP:
                    waiting = False


g = Game()

# game loop
while g.running:
    g.start()
    g.new()
    g.gameover()

pg.quit()