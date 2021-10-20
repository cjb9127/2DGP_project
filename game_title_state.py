import game_framework
from pico2d import *

import game_main_state

name = "TitleState"
image = None

def enter():
    global image
    image = load_image('resources/title.png')


def exit():
    global image
    del(image)


def update():
    pass

def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
                game_framework.change_state(game_main_state)


def pause(): pass
