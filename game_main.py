from pico2d import *
Width, Height = 800, 600


# Game object
class Background:
    def __init__(self):
        # self.image = load_image('resources/Background1.png')  # 이미지 이름
        self.x, self.y = Width // 2, Height // 2 

    def set(self, image):
        self.image = load_image(image)

    def draw(self):
        self.image.draw(self.x, self.y)  # 그리기 위치


class Character:
    def __init__(self):
        self.image = load_image('resources/스프라이트테스트4.png')  # 이미지 이름
        self.x, self.y = Width // 2, Height // 2 - 200 + 18
        self.frame = 0
        self.dir = 0
        self.state = 0
        
    def update(self):
        self.state = state
        self.frame = (self.frame + 1) % 3  # 프레임 갯수
        self.x += 10 * state
        self.dir = direction
        
        
    def draw(self):  # 이미지 클립
        if self.state == 0:
            if self.dir == 1:
                self.image.clip_draw(473+93, 0, 57, 52, self.x, self.y)
            elif self.dir == -1:
                self.image.clip_draw(473,0,57,52, self.x, self.y)
        elif self.state == -1:
            self.image.clip_draw(473 - 93 * self.frame, 0, 57, 52, self.x, self.y)
        elif self.state == 1:
            self.image.clip_draw(473+93 + 93 * self.frame, 0, 57, 52, self.x, self.y)

# func
def handle_events():  # 조작 이벤트
    global running
    global state
    global direction
    
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN: # 키를 누를때 이벤트
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_LEFT: #왼쪽 키를 누르면
                direction = -1
                state -= 1
            elif event.key == SDLK_RIGHT: #오른쪽 키
                direction = 1
                state += 1
        elif event.type == SDL_KEYUP: # 키를 땔 때 이벤트 
            if event.key == SDLK_LEFT:
                state += 1
            elif event.key == SDLK_RIGHT:
                state -= 1
                

# initialization code
open_canvas()

BasicBackground = Background()
BasicBackground.set('resources/Background1.png')
Mario = Character()

state = 0
direction = 1
running = True
# game main loop code
while running:
    handle_events()
    # Game logic 상호작용
    Mario.update()
    # Game drawing    
    clear_canvas()

    
    # drawwww
    BasicBackground.draw()
    Mario.draw()

    
    update_canvas()
    delay(0.02)


# finalization code
close_canvas()
