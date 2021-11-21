from pico2d import *

class Block:
    def __init__(self, lx, by, rx, ty):
        self.lx, self.rx = lx, rx
        self.by, self.ty = by, ty

    def draw(self):
        draw_rectangle(self.lx,self.by,self.rx,self.ty)

    def update(self):
        pass

class Firebar(Block):

    image = None
    fire = None

    def __init__(self, x=218, y=340, dir=-1):
        self.x, self.y = x, y
        self.lx, self.rx = x - 25, x + 25
        self.by, self.ty = y - 25, y + 25
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
            self.angle += 2
            if self.angle >= 360.0:
                self.angle -= 360.0
        elif self.dir == 1:
            self.angle -= 2
            if self.angle <= 0.0:
                self.angle += 360.0

        self.frame = (self.cnt) // 20
        self.cnt += 1
        if self.cnt >= 79:
            self.cnt = 0

    def draw(self):
        dx, dy = math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle))
        self.image.draw(self.x, self.y)
        draw_rectangle(self.lx,self.by,self.rx,self.ty)
        for i in range(0, 6):
            self.fire.clip_draw(20 * self.frame, 0, 18, 18, dx * 18 * i + self.x, dy * 18 * i + self.y)


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
        draw_rectangle(self.lx,self.by,self.rx,self.ty)
