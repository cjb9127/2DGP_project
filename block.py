from pico2d import *
import game_framework

class Block:
    def __init__(self, lx, by, rx, ty):
        self.lx, self.rx = lx, rx
        self.by, self.ty = by, ty

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return (self.x - 25, self.y - 25, self.x + 25, self.y + 25)

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Firebar(Block):

    image = None
    fire = None

    def __init__(self, x=225, y=125, dir=-1):
        self.x, self.y = x, y
        self.frame = 0
        self.angle = 0

        if Firebar.image == None:
            Firebar.image = load_image('resources/gray_block.png')
        if Firebar.fire == None:
            Firebar.fire = load_image('resources/fire.png')
        self.dir = dir
        self.cnt = 0

    def update(self):
        if self.dir == -1:
            self.angle += 0.2
            if self.angle >= 360.0:
                self.angle -= 360.0
        elif self.dir == 1:
            self.angle -= 2
            if self.angle <= 0.0:
                self.angle += 360.0

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    def draw(self):
        Frame = int(self.frame)
        dx, dy = math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle))
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())
        for i in range(0, 6):
            self.fire.clip_draw(20 * Frame, 0, 18, 18, dx * 18 * i + self.x, dy * 18 * i + self.y)


class Platform(Block):
    image = None

    def __init__(self, x = 600, y = 65+117):
        self.x, self.y = x, y
        self.lx, self.rx = self.x - 82, self.x + 82
        self.by, self.ty = self.y + 50, self.y + 83
        if Platform.image == None:
            Platform.image = load_image('resources/mushroom_platform2.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())
