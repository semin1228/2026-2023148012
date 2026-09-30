# animation_viewer.py
# Drill #8 애니메이션 뷰어
# ryu_sheet.png 의 여러 애니메이션을 화면 중앙에 확대해서 차례로 재생한다.

from pico2d import *

CANVAS_W, CANVAS_H = 800, 600

# 프레임 좌표 (left, bottom, width, height) - pico2d 좌하단 원점 기준
# find_frames.py 로 ryu_sheet.png 를 분석해서 얻은 값
IDLE_FRAMES = [
    (5, 1610, 41, 82), (53, 1610, 41, 81), (102, 1610, 41, 80), (151, 1610, 41, 81),
]

running = True
frame = 0


def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False


open_canvas(CANVAS_W, CANVAS_H)
sheet = load_image('ryu_sheet.png')

while running:
    clear_canvas()
    left, bottom, w, h = IDLE_FRAMES[frame]
    sheet.clip_draw(left, bottom, w, h, CANVAS_W // 2, CANVAS_H // 2)
    update_canvas()
    handle_events()
    frame = (frame + 1) % len(IDLE_FRAMES)
    delay(0.15)

close_canvas()
