from pico2d import *
import game_world
import random
import game_framework

# Run Speed
PiXEL_PER_METER = (10.0 / 0.3)  # 10 픽셀이 30 센티미터
RUN_SPEED_KMPH = 15.0  # 달리기 속도 시속 km/s
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)  # 달리기 속도 분속 (미터/분)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)  # 달리기 속도 초속 (미터/세컨드)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PiXEL_PER_METER)  # 달리기 속도 초속(픽셀/세컨드)

# Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2

class Monster:
    def __init__(self):
        self.x, self.y = None, None
        self.dir = None
        self.speed = None
        self.image = None
        self.frame = None
        self.alive = True

    def update(self):
        if self.x < 0 or self.x > 800:
            game_world.remove_object(self)

    def draw(self):
        draw_rectangle(self.lx,self.by,self.rx,self.ty)

    def get_bb(self):
        return (self.x - 25, self.y - 25, self.x + 25, self.y + 25)

class Goomba(Monster):

    image = None

    def __init__(self, x=-100, y=125):
        self.x, self.y = x, y
        self.vx = RUN_SPEED_PPS
        if Goomba.image == None:
            Goomba.image = load_image('resources/goomba.png')
        self.frame = 0
        self.alive = True

    def update(self):
        self.x += (game_framework.frame_time * self.vx)
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * \
        game_framework.frame_time) % 2

        if self.x > 800:
            self.x = 800
            self.vx *= -1
        elif self.x < 0:
            self.x = 0
            self.vx *= -1

    def draw(self):
        Frame = int(self.frame)
        self.image.clip_draw(60 * Frame, 0, 50, 50, self.x, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return (self.x - 25, self.y - 25, self.x + 25, self.y + 25)

class Killer(Monster):

    image = None

    def __init__(self, x = -50, y = 400, dir = 1):
        if dir == 0:
            dir = -1
        else:
            x = random.randint(-400, 0)

        self.x, self.y = x, y
        self.dir = dir
        self.speed = 1
        if Killer.image == None:
            Killer.image = load_image('resources/killer.png')
        self.alive = True

    def update(self):
        self.x += self.speed * self.dir
        if self.x > 800 + 25 and self.dir == 1: # 대포가 넘어가면 삭제
            game_world.remove_object(self)
        elif self.x < -25 and self.dir == -1:
            game_world.remove_object(self)

    def draw(self):
        if self.dir == -1:
            self.image.clip_draw(0, 0, 49, 43, self.x, self.y)
        elif self.dir == 1:
            self.image.clip_draw(60, 0, 49, 43, self.x, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return (self.x - 24, self.y - 21, self.x + 24, self.y + 21)
