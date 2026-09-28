# LEC06 실습: 캐릭터 원운동, 사각운동, 삼각운동을 무한 반복
# 조작: ESC 또는 창 닫기로 종료

from pico2d import *
import math
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH, HEIGHT = 800, 600
CX, CY, RADIUS = 400, 300, 200
LEFT, RIGHT, BOTTOM, TOP = 50, 750, 50, 550
STEP = 5
FRAME = 0.01

open_canvas(WIDTH, HEIGHT)
character = load_image('character.png')



def draw_circle():

    for degree in range(360):
        theta = math.radians(degree)
        x = CX + RADIUS * math.cos(theta)
        y = CY + RADIUS * math.sin(theta)
        draw_character(x, y)


def move_top():
    for x in range(LEFT, RIGHT, STEP):
        draw_character(x, TOP)

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
    delay(FRAME)


def move_right():
    for y in range(TOP, BOTTOM, -STEP):
        draw_character(RIGHT, y)

def move_bottom():
    for x in range(RIGHT, LEFT, -STEP):
        draw_character(x, BOTTOM)

def move_left():
    for y in range(BOTTOM, TOP, STEP):
        draw_character(LEFT, y)

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
    move_line(CX, TOP, LEFT, BOTTOM)

def move_tri_bottom():
    # 왼쪽 아래 (50, 50) -> 오른쪽 아래 (750, 50)
    for x in range(LEFT, RIGHT, STEP):
        draw_character(x, BOTTOM)

def move_tri_right():
    # 오른쪽 아래 (750, 50) -> 꼭대기 (400, 550)
    move_line(RIGHT, BOTTOM, CX, TOP)

def draw_triangle():
    move_tri_left()
    move_tri_bottom()
    move_tri_right()

while True:
    draw_circle()
    draw_rectangle()
    draw_triangle()
