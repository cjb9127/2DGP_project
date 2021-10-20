import os

from pico2d import *

import game_framework
import game_title_state

Width, Height = 800, 600
name = "MainState"

BG = None
Mario = None
MONSTERS = []
font = None  # font는 뭔지 아직 모름

# for move left and right
is_moving = 0  # idle = 0, moving = -1, 1
direction = 0  # left = -1, right = 1

# for jump
is_jumping = 0
velocity = 5
mass = 2

# 117

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
        self.x, self.y = Width // 2, 117
        self.frame = 0
        self.dir = direction
        self.isMoving = is_moving
        self.speed = 5
        self.m = mass
        self.v = velocity
        self.isJump = 0

    def update(self):
        self.isMoving = is_moving
        self.dir = direction
        self.isJump = is_jumping
        self.frame = (self.frame + 1) % 3  # 프레임 갯수

        self.x += self.speed * self.isMoving
        if self.x > Width:
            self.x = Width
        elif self.x < 0:
            self.x = 0
        if is_jumping == 1:
            self.jump()

    def jump(self):
        global is_jumping

        if self.isJump > 0:
            if self.v > 0:
                force = (0.5 * self.m * (self.v * self.v))
            else:
                force = -(0.5 * self.m * (self.v * self.v))

            self.y += round(force)
            self.v -= 0.25  # 점프 높이를 결정하는 v

            if self.y <= 117:  # 임시로 바닥 높이에 닿으면 점프 멈추게 했음
                self.y = 117
                is_jumping = 0
                self.v = velocity

    def draw(self):  # 이미지 클립
        if self.isJump != 0:
            if self.dir == -1:
                self.image.clip_draw(300, 51, 48, 50, self.x, self.y)
            elif self.dir == 1:
                self.image.clip_draw(60, 51, 48, 50, self.x, self.y)
        elif self.isMoving == -1:  # 왼쪽 달리기 중
            if self.frame == 0:
                self.image.clip_draw(300 + self.frame * 60, 0, 49, 50, self.x, self.y)
            elif self.frame == 1:
                self.image.clip_draw(300 + self.frame * 60, 0, 37, 50, self.x, self.y)
            elif self.frame == 2:
                self.image.clip_draw(300 + self.frame * 60, 0, 43, 50, self.x, self.y)
        elif self.isMoving == 1:  # 오른쪽 달리기 중
            if self.frame == 0:
                self.image.clip_draw(60 + self.frame * 60, 0, 49, 50, self.x, self.y)
            elif self.frame == 1:
                self.image.clip_draw(60 + self.frame * 60, 0, 37, 50, self.x, self.y)
            elif self.frame == 2:
                self.image.clip_draw(60 + self.frame * 60, 0, 43, 50, self.x, self.y)
        elif self.isMoving == 0:
            if self.dir == -1:  # 왼쪽을 보고 멈춰 있음
                self.image.clip_draw(0 + 240, 51, 40, 50, self.x, self.y)
            else:  # elif self.dir == 1:
                # 오른쪽을 보고 멈춰있음
                self.image.clip_draw(0, 51, 40, 50, self.x, self.y)


class Monster:
    def __init__(self):
        self.x, self.y = None, None
        self.dir = None
        self.speed = None
        self.image = None
        self.frame = None

    def update(self):
        if self.x > Width:
            self.x = Width
        elif self.x < 0:
            self.x = 0

    def draw(self):
        pass


class Goomba(Monster):
    def __init__(self, x = -100, y = 117, dir = 1):
        self.x, self.y = x, y
        self.dir = dir
        self.speed = 3
        self.image = load_image('resources/goomba.png')
        self.frame = 0

    def update(self):
        self.x += (self.speed * self.dir)
        self.frame = (self.frame + 1) % 20
        if self.x > Width and self.dir == 1:
            self.x = Width
            self.dir = -1
        elif self.x < 0 and self.dir == -1:
            self.x = 0
            self.dir = 1

    def draw(self):
        if self.frame < 10:
            self.image.clip_draw(0, 0, 50, 50, self.x, self.y)
        elif self.frame < 20:
            self.image.clip_draw(60, 0, 50, 50, self.x, self.y)


def enter():
    global Mario, BG
    Mario = Character()
    BG = Background()
    MONSTERS.append(Goomba())
    BG.set('resources/Background1.png')


def exit():
    global Mario, BG
    del (Mario)
    del (BG)
    for monsters in MONSTERS:
        del(monsters)

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
            elif event.key == SDLK_UP and is_jumping == 0:  # 위 키
                is_jumping = 1
        elif event.type == SDL_KEYUP:  # 키를 땔 때 이벤트
            if event.key == SDLK_LEFT:
                is_moving += 1
            elif event.key == SDLK_RIGHT:
                is_moving -= 1


def update():
    Mario.update()
    for monsters in MONSTERS:
        monsters.update()


def draw():
    clear_canvas()
    BG.draw()
    for monsters in MONSTERS:
        monsters.draw()
    Mario.draw()
    update_canvas()

