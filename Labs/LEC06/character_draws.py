from pico2d import *
import math
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

open_canvas(800, 600)
character = load_image('character.png')



def draw_circle():

    for degree in range(360):
        theta = math.radians(degree)
        x = 400 + 200 * math.cos(theta)
        y = 300 + 200 * math.sin(theta)
        draw_character(x, y)


def move_top():
    for x in range(50, 750, 5):
        draw_character(x, 550)

def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            close_canvas()
            exit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            close_canvas()
            exit()

def draw_character(x, y):
    clear_canvas()
    character.draw(x, y)
    update_canvas()
    handle_events()
    delay(0.002)


def move_right():
    for y in range(550, 50, -5):
        draw_character(750, y)

def move_bottom():
    for x in range(750, 50, -5):
        draw_character(x, 50)

def move_left():
    for y in range(50, 550, 5):
        draw_character(50, y)

def draw_rectangle():
    move_top()
    move_right()
    move_bottom()
    move_left()


def move_line(x1, y1, x2, y2):
    for i in range(100):
        t = i / 100
        x = x1 + (x2 - x1) * t
        y = y1 + (y2 - y1) * t
        draw_character(x, y)

def move_tri_left():
    # 꼭대기 (400, 550) -> 왼쪽 아래 (50, 50)
    move_line(400, 550, 50, 50)

def move_tri_bottom():
    # 왼쪽 아래 (50, 50) -> 오른쪽 아래 (750, 50)
    for x in range(50, 750, 5):
        draw_character(x, 50)

def move_tri_right():
    # 오른쪽 아래 (750, 50) -> 꼭대기 (400, 550)
    move_line(750, 50, 400, 550)

def draw_triangle():
    move_tri_left()
    move_tri_bottom()
    move_tri_right()

while True:
    draw_circle()
    draw_rectangle()
    draw_triangle()
