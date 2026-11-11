from pico2d import *

import game_framework
import game_world
import play_mode

image = None


def init():
    global image
    image = load_image('item_select.png')


def finish():
    global image
    del image


def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_0:
                play_mode.boy.item = None
                game_framework.pop_mode()
            elif event.key == SDLK_1:
                play_mode.boy.item = 'SmallBall'
                game_framework.pop_mode()
            elif event.key == SDLK_2:
                play_mode.boy.item = 'BigBall'
                game_framework.pop_mode()
            elif event.key == SDLK_ESCAPE:
                game_framework.pop_mode()  # 선택 없이 돌아감


def update():
    # 메뉴가 떠 있는 동안에도 게임은 계속 진행 (공이 굴러가고, 소년이 잠들 수 있음)
    game_world.update()


def render():
    clear_canvas()
    game_world.render()      # 멈춘 플레이 화면
    image.draw(400, 300)     # 그 위에 아이템 선택 메뉴
    update_canvas()


def pause():
    pass


def resume():
    pass
