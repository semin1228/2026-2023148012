import game_framework
from pico2d import *

image = None


def init():
    global image
    image = load_image('title.png')


def finish():
    global image
    del image


def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()


def update():
    pass


def render():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()


def pause():
    pass


def resume():
    pass
