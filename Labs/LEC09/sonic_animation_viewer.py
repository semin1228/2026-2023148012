# sonic_animation_viewer.py
# LEC09 애니메이션 뷰어 - sonic-sprite.png 의 동작을 재생한다

from pico2d import *

CANVAS_W, CANVAS_H = 1200, 800
SCALE = 4   # 과제 조건: 원본의 4배로 그린다
BG_COLOR = (40, 44, 70)   # 소닉의 파란색과 겹치지 않는 어두운 남색


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
while running:
    clear_canvas()
    draw_rectangle(0, 0, CANVAS_W, CANVAS_H, *BG_COLOR, filled=True)
    # 1번 줄(대기)의 첫 프레임만 잘라 그린다.
    # 시트의 y 는 위가 0 이지만 pico2d 는 아래가 0 이라, 줄 아래쪽 y=77 은 bottom = 525 - 77 - 1 = 447
    sheet.clip_draw(1, 447, 29, 39, CANVAS_W // 2, CANVAS_H // 2, 29 * SCALE, 39 * SCALE)
    update_canvas()
    handle_events()
    delay(0.01)

close_canvas()
