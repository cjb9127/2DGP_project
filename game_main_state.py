import os

from pico2d import *

import game_framework
import game_title_state

Width, Height = 800, 600
name = "MainState"

BG = None
Mario = None
font = None

state = 0  # idle = 0, moving = -1, 1
direction = 0  # left = -1, right = 1

is_jumping = False
is_bottom = True
Max_jump = 210 - 20


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
        self.state = state

    def update(self):
        self.state = state
        self.dir = direction
        self.frame = (self.frame + 1) % 3  # 프레임 갯수

        self.x += 5 * self.state
        if self.x > Width:
            self.x = Width
        elif self.x < 0:
            self.x = 0
        self.jump()

    def jump(self):
        global is_jumping, is_bottom
        if is_jumping:
            self.y += 7
        elif not is_jumping and not is_bottom:
            self.y -= 7

        if is_jumping and self.y >= (Max_jump + 118):
            is_jumping = False

        if not is_bottom and self.y <= 118:
            is_bottom = True
            self.y = 117

    def draw(self):  # 이미지 클립
        if self.state == -1:  # 왼쪽 달리기 중
            if self.frame == 0:
                self.image.clip_draw(300 + self.frame * 60, 0, 49, 50, self.x, self.y)
            elif self.frame == 1:
                self.image.clip_draw(300 + self.frame * 60, 0, 37, 50, self.x, self.y)
            elif self.frame == 2:
                self.image.clip_draw(300 + self.frame * 60, 0, 43, 50, self.x, self.y)
        elif self.state == 1:  # 오른쪽 달리기 중
            if self.frame == 0:
                self.image.clip_draw(60 + self.frame * 60, 0, 49, 50, self.x, self.y)
            elif self.frame == 1:
                self.image.clip_draw(60 + self.frame * 60, 0, 37, 50, self.x, self.y)
            elif self.frame == 2:
                self.image.clip_draw(60 + self.frame * 60, 0, 43, 50, self.x, self.y)
        elif self.state == 0:
            if self.dir == -1:  # 왼쪽을 보고 멈춰 있음
                self.image.clip_draw(0 + 240, 51, 40, 50, self.x, self.y)
            else:  # elif self.dir == 1:
                # 오른쪽을 보고 멈춰있음
                self.image.clip_draw(0, 51, 40, 50, self.x, self.y)


def enter():
    global Mario, BG
    Mario = Character()
    BG = Background()
    BG.set('resources/Background1.png')


def exit():
    global Mario, BG
    del (Mario)
    del (BG)


def pause():
    pass


def resume():
    pass


def handle_events():  # 조작 이벤트
    global state, direction  # 좌우 이동
    global is_jumping, is_bottom  # 점프

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:  # 키를 누를때 이벤트
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_LEFT:  # 왼쪽 키를 누르면
                direction = -1
                state -= 1
            elif event.key == SDLK_RIGHT:  # 오른쪽 키
                direction = 1
                state += 1
            elif event.key == SDLK_UP:  # 위 키
                if is_bottom:
                    is_jumping = True
                    is_bottom = False
        elif event.type == SDL_KEYUP:  # 키를 땔 때 이벤트
            if event.key == SDLK_LEFT:
                state += 1
            elif event.key == SDLK_RIGHT:
                state -= 1


def update():
    Mario.update()


def draw():
    clear_canvas()
    BG.draw()
    Mario.draw()
    update_canvas()

