# move_boy.py
# Drill #9 소년 상하좌우 이동 및 방향 바꾸기
# 게임 루프는 수업 노트대로 입력 처리(handle_events) -> 상태 갱신(update) -> 화면 출력(draw) 으로 나눈다.
#
# 조작: 방향키 이동 / I 정보 표시 켜고 끄기 / ESC 종료

import math
import os

from pico2d import *

TUK_WIDTH, TUK_HEIGHT = 1280, 1024   # 배경 TUK_GROUND.png 크기에 캔버스를 맞춘다

# animation_sheet.png 는 100x100 프레임 8개짜리 줄이 4개. pico2d 좌하단 원점 기준 각 줄의 bottom
IDLE_RIGHT, IDLE_LEFT = 300, 200
RUN_RIGHT, RUN_LEFT = 100, 0
FRAME_SIZE = 100    # 프레임 한 칸의 가로, 세로 크기
FRAME_COUNT = 8     # 한 줄의 프레임 수
FRAME_TIME = 0.05   # 한 프레임을 보여 주는 시간(초)
# 프레임 중심에서 실제 그림이 있는 끝까지의 거리 (32 프레임 전체의 투명하지 않은 영역으로 잼).
# 100x100 프레임에는 투명 여백이 있어서 50 으로 막으면 화면 끝에 닿기 전에 멈춰 보인다
MARGIN_LEFT, MARGIN_RIGHT = 32, 34
MARGIN_BOTTOM, MARGIN_TOP = 39, 41
FONT_PATH = 'C:/Windows/Fonts/consola.ttf'   # 정보 표시용 Windows 기본 글꼴
ACTION_NAMES = {IDLE_RIGHT: 'IDLE RIGHT', IDLE_LEFT: 'IDLE LEFT', RUN_RIGHT: 'RUN RIGHT', RUN_LEFT: 'RUN LEFT'}
SPEED = 10   # 한 프레임(FRAME_TIME)에 움직이는 거리. 초당 200 픽셀


def handle_events():
    # 이벤트에서는 이동 상태(dir_x, dir_y)만 바꾸고, 실제 이동은 update 에서 매 프레임 한다.
    # 키를 누르면 그 방향 값을 더하고, 떼면 더했던 값을 되돌린다 (수업의 dir 방식을 상하로 확장).
    # 반대 방향 키를 함께 누르면 상쇄되어 0(정지)이 된다
    global running, dir_x, dir_y, show_info
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                dir_x += 1
            elif event.key == SDLK_LEFT:
                dir_x -= 1
            elif event.key == SDLK_UP:
                dir_y += 1
            elif event.key == SDLK_DOWN:
                dir_y -= 1
            elif event.key == SDLK_i:
                show_info = not show_info
            elif event.key == SDLK_ESCAPE:
                running = False
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                dir_x -= 1
            elif event.key == SDLK_LEFT:
                dir_x += 1
            elif event.key == SDLK_UP:
                dir_y -= 1
            elif event.key == SDLK_DOWN:
                dir_y += 1


def update():
    global x, y, frame, face, action
    if dir_x != 0:
        face = dir_x   # 좌우로 움직일 때만 바라보는 방향을 바꾼다
    # 위아래로만 움직일 때는 dir_x 가 0 이므로 기존에 바라보던 방향(face)으로 달린다
    if dir_x != 0 or dir_y != 0:
        new_action = RUN_RIGHT if face == 1 else RUN_LEFT
    else:
        new_action = IDLE_RIGHT if face == 1 else IDLE_LEFT
    if new_action != action:
        action = new_action
        frame = -1   # 아래에서 1 을 더해 새 동작은 0 번 프레임부터 재생된다
    # 대각선은 그냥 더하면 sqrt(2) 배 빨라지므로 방향 길이로 나눠 어느 방향이든 같은 속도로 움직인다
    length = math.sqrt(dir_x ** 2 + dir_y ** 2)
    if length > 0:
        x += dir_x / length * SPEED
        y += dir_y / length * SPEED   # pico2d 는 y 가 위로 증가하므로 위 키(+1)가 위로 간다
    x = clamp(MARGIN_LEFT, x, TUK_WIDTH - MARGIN_RIGHT)   # 화면 경계에 닿으면 더 나가지 않는다
    y = clamp(MARGIN_BOTTOM, y, TUK_HEIGHT - MARGIN_TOP)
    frame = (frame + 1) % FRAME_COUNT


def draw_info():
    # 채점 때 확인하기 쉽도록 지금 동작과 위치를 표시한다
    if font is None or not show_info:
        return
    # 배경 그림이 복잡해서 글씨가 묻히지 않도록 어두운 사각형을 먼저 깐다
    draw_rectangle(10, TUK_HEIGHT - 70, 400, TUK_HEIGHT - 10, 0, 0, 0, filled=True)
    font.draw(20, TUK_HEIGHT - 25, f'{ACTION_NAMES[action]}  ({round(x)}, {round(y)})', (255, 255, 255))
    font.draw(20, TUK_HEIGHT - 55, 'ARROW: move   I: info   ESC: quit', (255, 255, 200))


def draw():
    clear_canvas()
    tuk_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
    character.clip_draw(frame * FRAME_SIZE, action, FRAME_SIZE, FRAME_SIZE, x, y)
    draw_info()
    update_canvas()


# 이미지는 상대경로('TUK_GROUND.png')로 읽는다. 다른 폴더에서 실행하거나 더블클릭해도
# 찾을 수 있도록 작업 폴더를 이 파일이 있는 폴더로 옮겨 둔다
os.chdir(os.path.dirname(os.path.abspath(__file__)))

open_canvas(TUK_WIDTH, TUK_HEIGHT)
tuk_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')
try:
    font = load_font(FONT_PATH, 22)
except IOError:
    font = None   # 글꼴이 없는 환경에서도 게임은 되도록 정보 표시만 생략

running = True
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
frame = 0
dir_x, dir_y = 0, 0   # +1: 오른쪽/위, -1: 왼쪽/아래, 0: 정지
face = 1   # 바라보는 방향. 1: 오른쪽, -1: 왼쪽
action = IDLE_RIGHT   # 지금 재생할 시트 줄(bottom)
show_info = True   # I 키로 켜고 끄는 정보 표시

while running:
    handle_events()
    update()
    draw()
    delay(FRAME_TIME)

close_canvas()
