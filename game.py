import pico2d

import game_framework
import game_main_state
import game_title_state

pico2d.open_canvas()
game_framework.run(game_title_state)
pico2d.close_canvas()


