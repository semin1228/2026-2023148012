# move_boy.py
# Drill #9 소년 상하좌우 이동 및 방향 바꾸기
# 게임 루프는 수업 노트대로 입력 처리(handle_events) -> 상태 갱신(update) -> 화면 출력(draw) 으로 나눈다.
#
# 조작: 방향키 이동 / ESC 종료

from pico2d import *

TUK_WIDTH, TUK_HEIGHT = 1280, 1024   # 배경 TUK_GROUND.png 크기에 캔버스를 맞춘다

# animation_sheet.png 는 100x100 프레임 8개짜리 줄이 4개. pico2d 좌하단 원점 기준 각 줄의 bottom
IDLE_RIGHT, IDLE_LEFT = 300, 200
RUN_RIGHT, RUN_LEFT = 100, 0
SPEED = 10   # 한 프레임(0.05초)에 움직이는 거리. 초당 200 픽셀


def handle_events():
    # 이벤트에서는 이동 상태(dir_x, dir_y)만 바꾸고, 실제 이동은 update 에서 매 프레임 한다.
    # 키를 누르면 그 방향 값을 더하고, 떼면 더했던 값을 되돌린다 (수업의 dir 방식을 상하로 확장).
    # 반대 방향 키를 함께 누르면 상쇄되어 0(정지)이 된다
    global running, dir_x, dir_y
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
    global x, y, frame
    x += dir_x * SPEED
    y += dir_y * SPEED   # pico2d 는 y 가 위로 증가하므로 위 키(+1)가 위로 간다
    frame = (frame + 1) % 8


def draw():
    clear_canvas()
    tuk_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
    if dir_x > 0:
        action = RUN_RIGHT
    elif dir_x < 0:
        action = RUN_LEFT
    else:
        action = IDLE_RIGHT
    character.clip_draw(frame * 100, action, 100, 100, x, y)
    update_canvas()


open_canvas(TUK_WIDTH, TUK_HEIGHT)
tuk_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')

running = True
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
frame = 0
dir_x, dir_y = 0, 0   # +1: 오른쪽/위, -1: 왼쪽/아래, 0: 정지

while running:
    handle_events()
    update()
    draw()
    delay(0.05)

close_canvas()
