# move_boy.py
# Drill #9 소년 상하좌우 이동 및 방향 바꾸기
# 게임 루프는 수업 노트대로 입력 처리(handle_events) -> 상태 갱신(update) -> 화면 출력(draw) 으로 나눈다.
#
# 조작: 방향키 이동 / ESC 종료

from pico2d import *

TUK_WIDTH, TUK_HEIGHT = 1280, 1024   # 배경 TUK_GROUND.png 크기에 캔버스를 맞춘다

# animation_sheet.png 는 100x100 프레임 8개짜리 줄이 4개. pico2d 좌하단 원점 기준 각 줄의 bottom
IDLE_RIGHT, IDLE_LEFT = 300, 200


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def update():
    global frame
    frame = (frame + 1) % 8


def draw():
    clear_canvas()
    tuk_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
    character.clip_draw(frame * 100, IDLE_RIGHT, 100, 100, x, y)
    update_canvas()


open_canvas(TUK_WIDTH, TUK_HEIGHT)
tuk_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')

running = True
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
frame = 0

while running:
    handle_events()
    update()
    draw()
    delay(0.05)

close_canvas()
