# Sprites Classes for Game
import pygame as pg
import os
from settings import *
vec = pg.math.Vector2

# assets folders
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "img")

class Player(pg.sprite.Sprite):
    # sprite for the arbitrary player
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, "sprite_man.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (10, HEIGHT - 20)
        self.pos = vec(25, HEIGHT * .75)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.state = 'stand'

    def jump(self):
        self.rect.y += 1
        land = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if land:
            self.vel.y = -PLAYER_JUMP
            self.state = 'jump'

    def crouch(self):
        self.rect.y += 1
        land = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1
        if land and self.state != 'crouch':
            self.pos.y += 5
            self.state = 'crouch'

    def update(self):
        self.acc = vec(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = PLAYER_ACC

        # apply speed physics
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.acc.y += self.vel.y * (PLAYER_FRICTION/5)
        self.vel += self.acc
        self.pos += self.vel + .5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y < 0:
            self.pos.y = HEIGHT

        self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Border(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y