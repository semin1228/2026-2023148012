# sonic_animation_viewer.py
# LEC09 애니메이션 뷰어 - sonic-sprite.png 의 동작을 재생한다

from pico2d import *

CANVAS_W, CANVAS_H = 1200, 800
SCALE = 4   # 과제 조건: 원본의 4배로 그린다
BG_COLOR = (40, 44, 70)   # 소닉의 파란색과 겹치지 않는 어두운 남색

# 1번 줄(대기) 프레임 좌표 (left, bottom, w, h) - pico2d 좌하단 원점 기준
# 프레임마다 폭과 간격이 달라서 일정한 간격으로 계산할 수 없고, 하나씩 적는다.
# 높이는 줄 전체(y 39~77)로 잘라서 같은 줄의 프레임은 발 위치가 그대로 유지된다
IDLE_FRAMES = [
    (1, 447, 29, 39), (31, 447, 26, 39), (58, 447, 28, 39), (86, 447, 30, 39),
    (118, 447, 30, 39), (150, 447, 30, 39), (182, 447, 29, 39), (211, 447, 29, 39),
    (240, 447, 29, 39), (270, 447, 24, 39), (302, 447, 29, 39),
]


def handle_events():
    global running
    # 이벤트를 꺼내 주지 않으면 창이 응답 없음 상태가 된다
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


open_canvas(CANVAS_W, CANVAS_H)
sheet = load_image('sonic-sprite.png')   # 399 x 525, 배경 투명

running = True
frame = 0   # 지금 그리는 프레임 번호
while running:
    clear_canvas()
    draw_rectangle(0, 0, CANVAS_W, CANVAS_H, *BG_COLOR, filled=True)
    # 시트의 y 는 위가 0 이지만 pico2d 는 아래가 0 이라, 줄 아래쪽 y=77 은 bottom = 525 - 77 - 1 = 447
    left, bottom, w, h = IDLE_FRAMES[frame]
    sheet.clip_draw(left, bottom, w, h, CANVAS_W // 2, CANVAS_H // 2, w * SCALE, h * SCALE)
    update_canvas()
    handle_events()
    frame = (frame + 1) % len(IDLE_FRAMES)   # 마지막 프레임 다음엔 첫 프레임으로
    delay(0.1)

close_canvas()
