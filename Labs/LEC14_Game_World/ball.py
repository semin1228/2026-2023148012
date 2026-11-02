from pico2d import get_canvas_width, load_image

import game_world

RADIUS = 11  # ball21x21.png 의 반지름 (픽셀)


class Ball:
    image = None  # 모든 볼이 이미지 하나를 공유

    def __init__(self, x, y, velocity):
        if Ball.image is None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y = x, y
        self.velocity = velocity
        self.angle = 0

    def update(self):
        self.x += self.velocity
        # 굴러간 거리 / 반지름 만큼 회전 (오른쪽으로 가면 시계 방향)
        self.angle -= self.velocity / RADIUS
        # 화면 밖으로 완전히 나가면 월드에서 제거
        if self.x < -25 or self.x > get_canvas_width() + 25:
            game_world.remove_object(self)

    def draw(self):
        self.image.rotate_draw(self.angle, self.x, self.y)
