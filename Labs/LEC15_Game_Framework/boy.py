from math import pi

from pico2d import get_canvas_width, get_time, load_image
from sdl2 import (SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT,
                  SDLK_SPACE)
from transitions import Machine

import game_world
from ball import Ball

BALL_IMAGES = {
    'SmallBall': 'ball21x21.png',
    'BigBall': 'ball41x41.png',
}

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.image = load_image('animation_sheet.png')
        self.idle_started_at = get_time()
        self.dir = 0
        self.face_dir = 1
        self.pressed_keys = set()
        self.item = 'SmallBall'  # None 이면 공을 차지 않음

        self.machine = Machine(
            model=self,
            states=['IDLE', 'SLEEP', 'RUN'],
            transitions=[
                {'trigger': 'fall_asleep',
                 'source': 'IDLE', 'dest': 'SLEEP'},
                {'trigger': 'wake_up',
                 'source': 'SLEEP', 'dest': 'IDLE'},
                {'trigger': 'start_run',
                 'source': ['IDLE', 'SLEEP'], 'dest': 'RUN'},
                {'trigger': 'stop_run',
                 'source': 'RUN', 'dest': 'IDLE'},
            ],
            initial='IDLE',
            auto_transitions=False,
        )

    def on_enter_IDLE(self):
        self.idle_started_at = get_time()
        self.frame = 0

    def on_enter_SLEEP(self):
        self.frame = 0

    def on_enter_RUN(self):
        self.frame = 0

    def fire_ball(self):
        if self.item is None:
            return
        ball = Ball(self.x, self.y, self.face_dir * 10,
                    BALL_IMAGES[self.item])
        game_world.add_oject(ball)

    def release_all_keys(self):
        # 다른 모드에 가 있는 동안 놓친 키업 대신, 모든 키를 뗀 것으로 처리
        self.pressed_keys.clear()
        if self.state == 'RUN':
            self.dir = 0
            self.stop_run()

    def handle_event(self, event):
        if (event.type == SDL_KEYDOWN and
                event.key == SDLK_SPACE and
                self.state == 'SLEEP'):
            self.wake_up()
            return

        if (event.type == SDL_KEYDOWN and
                event.key == SDLK_SPACE and
                self.state in ('IDLE', 'RUN')):
            self.fire_ball()
            return

        if (event.type not in (SDL_KEYDOWN, SDL_KEYUP) or
                event.key not in (SDLK_LEFT, SDLK_RIGHT)):
            return

        if event.type == SDL_KEYDOWN:
            self.pressed_keys.add(event.key)
        else:
            self.pressed_keys.discard(event.key)

        direction = (int(SDLK_RIGHT in self.pressed_keys) -
                     int(SDLK_LEFT in self.pressed_keys))

        if direction != 0:
            self.dir = direction
            self.face_dir = direction
            if self.state in ('IDLE', 'SLEEP'):
                self.start_run()
        elif self.state == 'RUN':
            self.dir = 0
            self.stop_run()

    def update(self):
        if self.state == 'IDLE':
            if get_time() - self.idle_started_at >= 5.0:
                self.fall_asleep()
            else:
                self.frame = (self.frame + 1) % 8
        elif self.state == 'RUN':
            self.frame = (self.frame + 1) % 8
            self.x += self.dir * 5
            self.x = max(25, min(get_canvas_width() - 25, self.x))

    def draw(self):
        if self.state == 'SLEEP':
            angle = pi / 2 if self.face_dir == 1 else -pi / 2
            flip = '' if self.face_dir == 1 else 'h'
            self.image.clip_composite_draw(
                self.frame * 100, 300, 100, 100,
                angle, flip, self.x, self.y - 30, 100, 100
            )
        elif self.state == 'RUN':
            row = 100 if self.face_dir == 1 else 0
            self.image.clip_draw(self.frame * 100, row, 100, 100,
                                 self.x, self.y)
        else:
            row = 300 if self.face_dir == 1 else 200
            self.image.clip_draw(self.frame * 100, row, 100, 100,
                                 self.x, self.y)
