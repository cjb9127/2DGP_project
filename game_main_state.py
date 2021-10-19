import os

from pico2d import *

import game_framework
import game_title_state

Width, Height = 800, 600
name = "MainState"

BG = None
Mario = None
font = None

state = 0   # idle = 0, moving = -1, 1
direction = 0   # left = -1, right = 1


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
        self.image = load_image('resources/스프라이트테스트4.png')  # 이미지 이름
        self.x, self.y = Width // 2, Height // 2 - 200 + 18
        self.frame = 0
        self.dir = direction
        self.state = state
        
    def update(self):
        self.state = state
        self.frame = (self.frame + 1) % 3  # 프레임 갯수
        self.dir = direction
        self.x += 4 * self.state

    def draw(self):  # 이미지 클립
        if self.state == -1:
            self.image.clip_draw(473 - 93 * self.frame, 0, 57, 52, self.x, self.y)
        elif self.state == 1:
            self.image.clip_draw(473 + 93 + 93 * self.frame, 0, 57, 52, self.x, self.y)
        elif self.state == 0:
            if self.dir == -1:
                self.image.clip_draw(473,0,57,52, self.x, self.y)
            else:  # self.dir == 1:
                self.image.clip_draw(473+93, 0, 57, 52, self.x, self.y)


def enter():
    global Mario, BG
    Mario = Character()
    BG = Background()
    BG.set('resources/Background1.png')


def exit():
    global Mario, BG
    del(Mario)
    del(BG)


def pause():
    pass


def resume():
    pass


def handle_events():  # 조작 이벤트
    global running
    global state
    global direction
    
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

