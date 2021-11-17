from pico2d import *

class Background:
    def __init__(self):
        self.image = load_image('resources/Background2.png')  # 이미지 이름
        self.x, self.y = 800 // 2, 600 // 2

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x, self.y)  # 그리기 위치
