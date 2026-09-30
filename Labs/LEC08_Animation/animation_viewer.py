# animation_viewer.py
# Drill #8 애니메이션 뷰어
# ryu_sheet.png 의 여러 애니메이션을 화면 중앙에 확대해서 차례로 재생한다.

from pico2d import *

CANVAS_W, CANVAS_H = 800, 600

running = True


def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False


open_canvas(CANVAS_W, CANVAS_H)
sheet = load_image('ryu_sheet.png')

while running:
    clear_canvas()
    update_canvas()
    handle_events()
    delay(0.01)

close_canvas()
