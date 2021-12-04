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
from block import Firebar

Width, Height = 800, 600
name = "MainState"

BG = None
Mario = None
Monsters = None
Fires = None

def enter():
    global Mario, BG
    global Monsters
    global Fires

    Mario = Character()
    BG = Background()
    Monsters = [Goomba() for _ in range(3)]
    Fires =  [Firebar()]

    game_world.add_object(BG, 0)
    game_world.add_object(Mario, 1)
    game_world.add_objects(Monsters, 1)
    game_world.add_objects(Fires, 1)


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
    for mon in Monsters:
        if collide(Mario, mon):
            print('collision mario and monster')
    for fir in Fires:
        if collide(Mario, fir):
            print('collision mario and fireblock')

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

