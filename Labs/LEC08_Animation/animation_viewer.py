# animation_viewer.py
# Drill #8 애니메이션 뷰어
# ryu_sheet.png 의 여러 애니메이션을 화면 중앙에 확대해서 차례로 재생한다.

from pico2d import *

CANVAS_W, CANVAS_H = 800, 600
SCALE = 4   # 대기 자세 키 82px -> 328px (화면 높이 600 의 절반 이상). 가장 높은 승룡권도 600 안에 들어간다

# 애니메이션 표: (이름, 땅 높이, 프레임 목록)
# 프레임 좌표는 (left, bottom, width, height) - pico2d 좌하단 원점 기준, find_frames.py 로 얻은 값
# 땅 높이는 그 동작 줄에서 발이 땅에 닿은 프레임의 bottom 값
ANIMATIONS = [
    ('IDLE', 1610, [
        (5, 1610, 41, 82), (53, 1610, 41, 81), (102, 1610, 41, 80), (151, 1610, 41, 81),
    ]),
]

running = True
anim = 0    # 지금 재생 중인 애니메이션 번호
frame = 0   # 그 애니메이션 안에서의 프레임 번호


def handle_events():
    global running
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            next_animation()


def next_animation():
    # 다음 애니메이션으로 넘어가고, 마지막 다음엔 처음으로 돌아간다
    global anim, frame
    anim = (anim + 1) % len(ANIMATIONS)
    frame = 0


def anim_height(ground, frames):
    # 땅에서 그 애니메이션의 가장 높은 지점까지의 높이 (시트 픽셀 단위)
    return max(bottom - ground + h for _, bottom, _, h in frames)


def draw_frame(ground, frames, left, bottom, w, h):
    # 프레임 크기가 제각각이라 중심을 고정하면 발이 위아래로 출렁인다.
    # 그래서 화면의 땅 위치를 정하고, 프레임은 시트에서 땅보다 떠 있는 만큼(bottom - ground)만 올려서 그린다.
    # 땅 위치는 애니메이션 전체 높이가 화면 세로 중앙에 오도록 잡는다.
    ground_y = CANVAS_H // 2 - anim_height(ground, frames) * SCALE // 2
    lift = (bottom - ground) * SCALE
    y = ground_y + lift + h * SCALE // 2    # clip_draw 는 중심 좌표를 받는다
    sheet.clip_draw(left, bottom, w, h, CANVAS_W // 2, y, w * SCALE, h * SCALE)


open_canvas(CANVAS_W, CANVAS_H)
sheet = load_image('ryu_sheet.png')

while running:
    name, ground, frames = ANIMATIONS[anim]
    clear_canvas()
    left, bottom, w, h = frames[frame]
    draw_frame(ground, frames, left, bottom, w, h)
    update_canvas()
    handle_events()
    frame = (frame + 1) % len(frames)
    delay(0.15)

close_canvas()
