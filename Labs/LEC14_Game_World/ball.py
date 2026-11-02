from pico2d import get_canvas_width, load_image

import game_world


class Ball:
    image = None  # 모든 볼이 이미지 하나를 공유

    def __init__(self, x, y, velocity):
        if Ball.image is None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y = x, y
        self.velocity = velocity

    def update(self):
        self.x += self.velocity
        # 화면 밖으로 완전히 나가면 월드에서 제거
        if self.x < -25 or self.x > get_canvas_width() + 25:
            game_world.remove_object(self)

    def draw(self):
        self.image.draw(self.x, self.y)
