import os
import random
import math
from pico2d import *

import game_framework
import game_title_state

Width, Height = 800, 600
name = "MainState"

BG = None
Mario = None
PF = None
Bottom = None
FBS = []
MONSTERS = []
font = None
BLOCKS = []

# for move left and right
is_moving = 0  # idle = 0, moving = -1, 1
direction = 1  # left = -1, right = 1

# for jump
is_jumping = 0
is_falling = 0
velocity = 5
mass = 2

# 122, 293

# Game object
class Background:
    def __init__(self):
        # self.image = load_image('resources/Background1.png')  # 이미지 이름
        self.x, self.y = Width // 2, Height // 2
        self.image = None

    def set(self, image):
        self.image = load_image(image)

    def draw(self):
        self.image.draw(self.x, self.y)  # 그리기 위치


class Character:
    def __init__(self):
        self.image = load_image('resources/mario.png')  # 이미지 이름
        self.x, self.y = Width // 2, 125
        self.lx, self.rx = self.x - 20, self.x + 20
        self.by, self.ty = self.y - 25, self.y + 25
        self.frame = 0
        self.dir = direction
        self.isMoving = is_moving
        self.speed = 4.5
        self.m = mass
        self.v = velocity
        self.isJump = 0
        self.isFall = 0

    def update(self):
        self.isMoving = is_moving
        self.dir = direction
        self.isJump = is_jumping
        self.isFall = is_falling
        self.frame = (self.frame + 1) % 15  # 프레임 갯수

        self.x += self.speed * self.isMoving
        self.lx, self.rx = self.x - 20, self.x + 20
        self.by, self.ty = self.y - 25, self.y + 25

        if self.x > Width:
            self.x = Width
        elif self.x < 0:
            self.x = 0
        # if (self.rx < PF.lx or self.lx > PF.rx ):
        #     self.isFall = 1
        if self.isJump == 1:
            self.jump()
        elif self.isFall == 1:
            self.fall()
        else:
            self.collid_y()

    def collid_y(self):
        for block_list in BLOCKS:
            if str(type(block_list)) == "<class 'list'>":
                for block in block_list:
                    if (self.rx < block.lx - 3 or self.lx > block.rx + 3) and self.y == block.ty + 25:
                        self.isFall = 1
                        self.v = 0
                        self.fall()
            else:
                if (self.rx < block_list.lx - 3 or self.lx > block_list.rx + 3) and self.y == block_list.ty + 25:
                    self.isFall = 1
                    self.v = 0
                    self.fall()

    def jump(self):
        global is_jumping, is_falling

        if self.isJump > 0:
            if self.v > 0:
                force = (0.5 * self.m * (self.v * self.v))
            else:
                is_jumping = 0
                is_falling = 1
                return None
                force = -(0.5 * self.m * (self.v * self.v))

            self.y += round(force)
            self.v -= 0.25  # 점프 높이를 결정하는 v

            if self.y <= 125:  # 임시로 바닥 높이에 닿으면 점프 멈추게 했음
                self.y = 125
                is_jumping = 0
                self.v = velocity

    def fall(self):
        global is_falling
        # 점프한 뒤에 폴링, 그냥 바닥에서 나왔을때 폴링
        # 폴링 해제 조건 = self.y <= 125 or self.by가 platform의 ty
        force = -(0.5 * self.m * (self.v * self.v))
        if self.y + round(force) <= 125:  # 바닥에 뚝
            self.y = 125
            is_falling = 0
            self.v = velocity
        elif (self.rx >= PF.lx and self.lx <= PF.rx) and self.by >= PF.ty:  # 플랫폼 x사이, y값 더 위에
            if self.by + round(force) <= PF.ty:  # 플랫폼 바닥에 뚝
                self.y = PF.ty + 25
                is_falling = 0
                self.v = velocity
            else:
                self.y += round(force)  # 그냥 자유낙하 중
                self.v -= 0.25
                is_falling = 1
        else:
            self.y += round(force)  # 그냥 자유낙하 중
            self.v -= 0.25
            is_falling = 1

        # if self.y <= 125:  # 임시로 바닥 높이에 닿으면 점프 멈추게 했음
        #     self.y = 125
        #     is_falling = 0
        #     self.v = velocity

    def draw(self):  # 이미지 클립
        draw_rectangle(self.lx, self.by, self.rx, self.ty)
        if self.isJump != 0 or self.isFall != 0:
            if self.dir == -1:
                self.image.clip_draw(300, 51, 48, 50, self.x, self.y)
            elif self.dir == 1:
                self.image.clip_draw(60, 51, 48, 50, self.x, self.y)
        elif self.isMoving == -1:  # 왼쪽 달리기 중
            if self.frame < 5:
                self.image.clip_draw(300, 0, 49, 50, self.x, self.y)
            elif self.frame < 10:
                self.image.clip_draw(360, 0, 37, 50, self.x, self.y)
            elif self.frame < 15:
                self.image.clip_draw(420, 0, 43, 50, self.x, self.y)
        elif self.isMoving == 1:  # 오른쪽 달리기 중
            if self.frame < 5:
                self.image.clip_draw(60, 0, 49, 50, self.x, self.y)
            elif self.frame < 10:
                self.image.clip_draw(120, 0, 37, 50, self.x, self.y)
            elif self.frame < 15:
                self.image.clip_draw(180, 0, 43, 50, self.x, self.y)
        elif self.isMoving == 0:
            if self.dir == -1:  # 왼쪽을 보고 멈춰 있음
                self.image.clip_draw(0 + 240, 51, 40, 50, self.x, self.y)
            else:  # elif self.dir == 1:
                # 오른쪽을 보고 멈춰있음
                self.image.clip_draw(0, 51, 40, 50, self.x, self.y)


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
        if self.x > Width and self.dir == 1:
            self.x = Width
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
        if self.x > Width + 25 and self.dir == 1: # 대포가 넘어가면 삭제
            self.alive = False
        elif self.x < -25 and self.dir == -1:
            self.alive = False

    def draw(self):
        if self.dir == -1:
            self.image.clip_draw(0, 0, 49, 43, self.x, self.y)
        elif self.dir == 1:
            self.image.clip_draw(60, 0, 49, 43, self.x, self.y)
        draw_rectangle(self.lx, self.by, self.rx, self.ty)


class Block:
    def __init__(self, lx, by, rx, ty):
        self.lx, self.rx = lx, rx
        self.by, self.ty = by, ty

    def draw(self):
        draw_rectangle(self.lx,self.by,self.rx,self.ty)


class Firebar(Block):

    image = None
    fire = None

    def __init__(self, x=218, y=340, dir=-1):
        self.x, self.y = x, y
        self.lx, self.rx = x - 25, x + 25
        self.by, self.ty = y - 25, y + 25
        self.frame = 0
        self.angle = 0
        if Firebar.image == None:
            Firebar.image = load_image('resources/gray_block.png')
        if Firebar.fire == None:
            Firebar.fire = load_image('resources/fire.png')
        self.dir = dir
        self.cnt = 0

    def update(self):
        if self.dir == -1:
            self.angle += 2
            if self.angle >= 360.0:
                self.angle -= 360.0
        elif self.dir == 1:
            self.angle -= 2
            if self.angle <= 0.0:
                self.angle += 360.0

        self.frame = (self.cnt) // 20
        self.cnt += 1
        if self.cnt >= 79:
            self.cnt = 0

    def draw(self):
        dx, dy = math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle))
        self.image.draw(self.x, self.y)
        draw_rectangle(self.lx,self.by,self.rx,self.ty)
        for i in range(0,6):
            self.fire.clip_draw(20 * self.frame, 0, 18, 18, dx * 18 * i + self.x, dy * 18 * i + self.y)


class Platform(Block):
    def __init__(self, x = 600, y = 65+117):
        self.x, self.y = x, y
        self.lx, self.rx = self.x - 82, self.x + 82
        self.by, self.ty = self.y + 50, self.y + 83
        self.image = load_image('resources/mushroom_platform2.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(self.lx,self.by,self.rx,self.ty)


def enter():
    global Mario, BG
    global MONSTERS, FBS
    global PF, Bottom
    global BLOCKS
    Mario = Character()
    BG = Background()
    Bottom = Block(0,0,800,100)
    MONSTERS.append(Goomba())
    for _ in range(0,4):
        x = random.randint(800, 1200)
        y = random.randint(300, 550)
        dir = random.randint(0, 1)
        MONSTERS.append(Killer(x, y, dir))

    FBS = [Firebar(), Firebar(218+200, 340, 1)]
    PF = Platform()
    BLOCKS = [Bottom, FBS, PF]
    BG.set('resources/Background2.png')


def exit():
    global Mario, BG, PF
    global MONSTERS
    global FBS
    del (Mario)
    del (BG)
    for monster in MONSTERS:
        del(monster)
    for FB in FBS:
        del(FB)
    del(PF)


def pause():
    pass


def resume():
    pass


def handle_events():  # 조작 이벤트
    global is_moving, direction  # 좌우 이동
    global is_jumping  # 점프

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:  # 키를 누를때 이벤트
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_LEFT:  # 왼쪽 키를 누르면
                direction = -1
                is_moving -= 1
            elif event.key == SDLK_RIGHT:  # 오른쪽 키
                direction = 1
                is_moving += 1
            elif event.key == SDLK_UP and is_jumping == 0 and is_falling == 0:  # 위 키
                is_jumping = 1
        elif event.type == SDL_KEYUP:  # 키를 땔 때 이벤트
            if event.key == SDLK_LEFT:
                is_moving += 1
            elif event.key == SDLK_RIGHT:
                is_moving -= 1


def update():
    index = []
    Mario.update()
    for i in range(0, len(MONSTERS)):
        if not MONSTERS[i].alive:
            index.append(i)
        else:
            MONSTERS[i].update()

    for i in index:
        del MONSTERS[i]

    for FB in FBS:
        FB.update()


def draw():
    clear_canvas()
    BG.draw()
    Bottom.draw()
    PF.draw()
    for monsters in MONSTERS:
        monsters.draw()
    Mario.draw()
    for FB in FBS:
        FB.draw()
    update_canvas()



