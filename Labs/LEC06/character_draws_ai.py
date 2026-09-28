import os
import math
from pico2d import *

# 실행 위치와 상관없이 character.png 를 찾도록 스크립트 폴더로 이동
os.chdir(os.path.dirname(os.path.abspath(__file__)))

WIDTH, HEIGHT = 800, 600
CX, CY, RADIUS = 400, 300, 200      # 원운동 중심과 반지름
LEFT, RIGHT, BOTTOM, TOP = 50, 750, 50, 550   # 사각운동 경계
STEP = 5                            # 직선 이동 한 번의 픽셀 수
FRAME = 0.01                        # 프레임 간 지연(초)

# 삼각운동 꼭짓점 (반시계 방향)
TRIANGLE = [(400, 550), (50, 50), (750, 50)]


def handle_events():
    # 창 닫기 / ESC 로 프로그램 종료
    for event in get_events():
        if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            close_canvas()
            exit(0)


def draw_boy(x, y):
    clear_canvas()
    boy.draw(x, y)
    update_canvas()
    handle_events()
    delay(FRAME)


def move_line(x1, y1, x2, y2):
    # (x1, y1) 에서 (x2, y2) 까지 STEP 픽셀 간격으로 직선 이동
    distance = math.hypot(x2 - x1, y2 - y1)
    steps = max(1, int(distance // STEP))
    for i in range(steps):
        t = i / steps
        draw_boy(x1 + (x2 - x1) * t, y1 + (y2 - y1) * t)


def move_circle():
    for degree in range(0, 360, 2):
        theta = math.radians(degree)
        draw_boy(CX + RADIUS * math.cos(theta), CY + RADIUS * math.sin(theta))


def move_rectangle():
    corners = [(LEFT, TOP), (RIGHT, TOP), (RIGHT, BOTTOM), (LEFT, BOTTOM)]
    for i in range(4):
        x1, y1 = corners[i]
        x2, y2 = corners[(i + 1) % 4]
        move_line(x1, y1, x2, y2)


def move_triangle():
    for i in range(3):
        x1, y1 = TRIANGLE[i]
        x2, y2 = TRIANGLE[(i + 1) % 3]
        move_line(x1, y1, x2, y2)


open_canvas(WIDTH, HEIGHT)
boy = load_image('character.png')

while True:
    move_circle()
    move_rectangle()
    move_triangle()
