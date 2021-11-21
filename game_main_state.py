import os
import random
import math

from pico2d import *
import game_framework
import game_title_state
import game_world

from character import Character
from background import Background
from monster import Monster, Goomba, Killer

Width, Height = 800, 600
name = "MainState"

BG = None
Mario = None

def enter():
    global Mario, BG
    Mario = Character()
    BG = Background()
    game_world.add_object(BG, 0)
    game_world.add_object(Mario, 1)


def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():  # 조작 이벤트
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:  # 키를 누를때 이벤트
            game_framework.quit()
        else:
            Mario.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()



