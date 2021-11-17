from pico2d import *
import game_world
import random

class Monster:
    def __init__(self):
        self.x, self.y = None, None
        self.lx, self.rx = None, None
        self.by, self.ty = None, None
        self.dir = None
        self.speed = None
        self.image = None
        self.frame = None
        self.alive = True

    def update(self):
        pass

    def draw(self):
        draw_rectangle(self.lx,self.by,self.rx,self.ty)


class Goomba(Monster):

    image = None

    def __init__(self, x=-100, y=122, dir=1):
        self.x, self.y = x, y
        self.lx, self.rx = self.x - 25, self.x + 25
        self.by, self.ty = self.y - 25, self.y + 25
        self.dir = dir
        self.speed = 1.25
        if Goomba.image == None:
            Goomba.image = load_image('resources/goomba.png')
        self.frame = 0
        self.alive = True

    def update(self):
        self.x += (self.speed * self.dir)
        self.lx, self.rx = self.x - 25, self.x + 25
        self.by, self.ty = self.y - 25, self.y + 25
        self.frame = (self.frame + 1) % 60
        if self.x > 800 and self.dir == 1:
            self.x = 800
            self.dir = -1
        elif self.x < 0 and self.dir == -1:
            self.x = 0
            self.dir = 1

    def draw(self):
        if self.frame < 30:
            self.image.clip_draw(0, 0, 50, 50, self.x, self.y)
        elif self.frame < 60:
            self.image.clip_draw(60, 0, 50, 50, self.x, self.y)
        draw_rectangle(self.lx, self.by, self.rx, self.ty)


class Killer(Monster):

    image = None

    def __init__(self, x = -50, y = 400, dir = 1):
        if dir == 0:
            dir = -1
        else:
            x = random.randint(-400, 0)

        self.x, self.y = x, y
        self.lx, self.rx = self.x - 24, self.x + 24
        self.by, self.ty = self.y - 21, self.y + 21
        self.dir = dir
        self.speed = 1
        if Killer.image == None:
            Killer.image = load_image('resources/killer.png')
        self.alive = True

    def update(self):
        self.x += self.speed * self.dir
        self.lx, self.rx = self.x - 24, self.x + 24
        if self.x > 800 + 25 and self.dir == 1: # 대포가 넘어가면 삭제
            game_world.remove_object(self)
        elif self.x < -25 and self.dir == -1:
            game_world.remove_object(self)

    def draw(self):
        if self.dir == -1:
            self.image.clip_draw(0, 0, 49, 43, self.x, self.y)
        elif self.dir == 1:
            self.image.clip_draw(60, 0, 49, 43, self.x, self.y)
        draw_rectangle(self.lx, self.by, self.rx, self.ty)
