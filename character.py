from pico2d import *
from game_world import objects

# character event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP = range(4)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP
}


class IdleState:

    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.vx += 1
        elif event == LEFT_DOWN:
            mario.vx -= 1
        elif event == RIGHT_UP:
            mario.vx -= 1
        elif event == LEFT_UP:
            mario.vx += 1

    def exit(mario, event):
        pass

    def do(mario):
        mario.frame = (mario.frame + 1) % 15


class RunState:

    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.vx += 1
        elif event == LEFT_DOWN:
            mario.vx -= 1
        elif event == RIGHT_UP:
            mario.vx -= 1
        elif event == LEFT_UP:
            mario.vx += 1
        mario.dir = mario.vx

    def exit(mario, event):
        pass

    def do(mario):
        mario.frame = (mario.frame + 1) % 15
        mario.x += mario.vx
        mario.x = clamp(25, mario.x, 800 - 25)


next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState},
}


class Character:

    def __init__(self):
        self.image = load_image('resources/mario.png')  # 이미지 이름
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
        if str(self.cur_state) == "<class 'character.RunState'>":
            if self.dir < 0:   # 왼쪽 달리기 중
                if self.frame < 5:
                    self.image.clip_draw(300, 0, 49, 50, self.x, self.y)
                elif self.frame < 10:
                    self.image.clip_draw(360, 0, 37, 50, self.x, self.y)
                elif self.frame < 15:
                    self.image.clip_draw(420, 0, 43, 50, self.x, self.y)
            elif self.dir >= 0:   # 오른쪽 달리기 중
                if self.frame < 5:
                    self.image.clip_draw(60, 0, 49, 50, self.x, self.y)
                elif self.frame < 10:
                    self.image.clip_draw(120, 0, 37, 50, self.x, self.y)
                elif self.frame < 15:
                    self.image.clip_draw(180, 0, 43, 50, self.x, self.y)
        elif str(self.cur_state) == "<class 'character.IdleState'>":
            if self.dir < 0:  # 왼쪽을 보고 멈춰 있음
                self.image.clip_draw(0 + 240, 51, 40, 50, self.x, self.y)
            else:  # 오른쪽을 보고 멈춰있음
                self.image.clip_draw(0, 51, 40, 50, self.x, self.y)
        # debug_print('Velocity :' + str(self.vx) + '  Dir:' + str(self.dir))

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            # print(event.type, event.key)
            self.add_event(key_event)