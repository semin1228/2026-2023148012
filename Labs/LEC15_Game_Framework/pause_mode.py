import os

import pico2d
from pico2d import *

import game_framework
import game_world

font = None


def init():
    global font
    # pico2d 패키지에 들어 있는 기본 폰트를 사용
    font_path = os.path.join(os.path.dirname(pico2d.__file__),
                             'data', 'ConsolaMalgun.ttf')
    font = load_font(font_path, 40)


def finish():
    global font
    font = None


def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.pop_mode()


def update():
    # 게임 오브젝트를 update 하지 않으므로 게임이 멈춘다
    pass


def render():
    clear_canvas()
    game_world.render()  # 멈춘 플레이 화면을 그대로 보여줌
    font.draw(300, 300, 'PAUSED', (255, 0, 0))
    update_canvas()


def pause():
    pass


def resume():
    pass
