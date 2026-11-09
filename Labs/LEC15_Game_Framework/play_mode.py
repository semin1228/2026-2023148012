from pico2d import *
import game_framework
import game_world
import pause_mode
import title_mode
from boy import Boy
from grass import Grass

boy = None
paused_at = 0.0


def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.push_mode(pause_mode)
        else:
            boy.handle_event(event)


def init():
    global boy

    boy = Boy()
    game_world.add_oject(boy)

    grass = Grass()
    game_world.add_oject(grass, 0)


def update():
    game_world.update()


def render():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()


def pause():
    global paused_at
    paused_at = get_time()


def resume():
    # 멈춰 있던 시간은 서 있던 시간에서 빼서, 복귀하자마자 잠들지 않게 함
    boy.idle_started_at += get_time() - paused_at
    boy.release_all_keys()
