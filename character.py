from pico2d import *

import game_framework
from game_world import objects

# character event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP = range(4)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP
}

# Run Speed
PiXEL_PER_METER = (10.0 / 0.3)  # 10 픽셀이 30 센티미터
RUN_SPEED_KMPH = 25.0  # 달리기 속도 시속 km/s
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)  # 달리기 속도 분속 (미터/분)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)  # 달리기 속도 초속 (미터/세컨드)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PiXEL_PER_METER)  # 달리기 속도 초속(픽셀/세컨드)

# Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 12
class IdleState:

    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.vx += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            mario.vx -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            mario.vx -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            mario.vx += RUN_SPEED_PPS

    def exit(mario, event):
        pass

    def do(mario):
        mario.frame = (mario.frame + 1) % 3

    def draw(mario):
        if mario.dir < 0:  # 왼쪽을 보고 멈춰 있음
            mario.image.clip_draw(240, 51, 40, 50, mario.x, mario.y)
        else:  # 오른쪽을 보고 멈춰있음
            mario.image.clip_draw(0, 51, 40, 50, mario.x, mario.y)

class RunState:

    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.vx += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            mario.vx -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            mario.vx -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            mario.vx += RUN_SPEED_PPS
        mario.dir = clamp(-1, mario.vx, 1)
        print(RUN_SPEED_PPS)

    def exit(mario, event):
        pass

    def do(mario):
        mario.frame = (mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        mario.x += mario.vx * game_framework.frame_time
        mario.x = clamp(25, mario.x, 800 - 25)

    # @staticmethod
    def draw(mario):
        Frame = int(mario.frame)
        if mario.dir < 0:  # 왼쪽 달리기 중
            if Frame == 0:
                mario.image.clip_draw(300, 0, 49, 50, mario.x, mario.y)
            elif Frame == 1:
                mario.image.clip_draw(360, 0, 37, 50, mario.x, mario.y)
            elif Frame == 2:
                mario.image.clip_draw(420, 0, 43, 50, mario.x, mario.y)
        else:  # 오른쪽 달리기 중
            if Frame == 0:
                mario.image.clip_draw(60, 0, 49, 50, mario.x, mario.y)
            elif Frame == 1:
                mario.image.clip_draw(120, 0, 37, 50, mario.x, mario.y)
            elif Frame == 2:
                mario.image.clip_draw(180, 0, 43, 50, mario.x, mario.y)


next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState},
}


class Character:

    def __init__(self):
        self.image = load_image('resources/mario.png')  # 이미지 이름
        self.font = load_font('font/나눔손글씨 미니 손글씨.ttf', 36)
        self.x, self.y = 800 // 2, 125
        self.dir = 1
        self.vx = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):  # 이미지 클립
        self.cur_state.draw(self)
        self.font.draw(self.x - 60, self.y + 50, '(Time: %3.2f)' % get_time(), (255, 255, 0))

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            # print(event.type, event.key)
            self.add_event(key_event)