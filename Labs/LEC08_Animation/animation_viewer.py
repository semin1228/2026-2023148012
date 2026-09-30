# animation_viewer.py
# Drill #8 애니메이션 뷰어
# ryu_sheet.png 의 여러 애니메이션을 화면 중앙에 확대해서 차례로 재생한다.

from pico2d import *

CANVAS_W, CANVAS_H = 800, 600
SCALE = 4   # 대기 자세 키 82px -> 328px (화면 높이 600 의 절반 이상). 가장 높은 승룡권도 600 안에 들어간다

# 애니메이션 표: (이름, 땅 높이, 프레임 목록)
# 프레임 좌표는 (left, bottom, width, height, 몸통중심x) - pico2d 좌하단 원점 기준, find_frames.py 로 얻은 값
# 몸통중심x 는 프레임 왼쪽에서 몸통 중심까지의 거리. 팔다리를 뻗어도 몸이 제자리에 있도록 가로 정렬에 쓴다
# 땅 높이는 그 동작 줄에서 발이 땅에 닿은 프레임의 bottom 값
ANIMATIONS = [
    ('IDLE', 1610, [
        (5, 1610, 41, 82, 20), (53, 1610, 41, 81, 20), (102, 1610, 41, 80, 19), (151, 1610, 41, 81, 20),
    ]),
    ('WALK', 1610, [
        (221, 1610, 41, 75, 22), (269, 1610, 41, 80, 22), (317, 1610, 41, 80, 22), (365, 1610, 43, 81, 23),
        (413, 1610, 41, 80, 22),
    ]),
    ('PUNCH', 1495, [
        (5, 1495, 41, 81, 20), (54, 1495, 55, 81, 23), (113, 1495, 41, 81, 20),
    ]),
    ('KICK', 1247, [
        (4, 1247, 42, 81, 11), (53, 1247, 55, 84, 16), (111, 1247, 69, 84, 18), (184, 1247, 57, 70, 15),
        (248, 1247, 42, 73, 11),
    ]),
    ('JUMP', 1023, [
        (158, 1023, 33, 90, 17), (205, 1060, 61, 37, 41), (282, 1046, 31, 68, 13), (329, 1061, 72, 39, 22),
        (419, 1043, 43, 74, 19), (474, 1026, 33, 90, 16),
    ]),
    ('SHORYUKEN', 730, [
        (3, 730, 44, 74, 29), (52, 730, 49, 80, 35), (107, 730, 41, 111, 16), (155, 752, 38, 108, 16),
        (207, 765, 29, 101, 10), (256, 730, 44, 94, 16),
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
    return max(bottom - ground + h for _, bottom, _, h, _ in frames)


def draw_frame(ground, frames, left, bottom, w, h, cx):
    # 프레임 크기가 제각각이라 중심을 고정하면 발이 위아래로 출렁인다.
    # 그래서 화면의 땅 위치를 정하고, 프레임은 시트에서 땅보다 떠 있는 만큼(bottom - ground)만 올려서 그린다.
    # 땅 위치는 애니메이션 전체 높이가 화면 세로 중앙에 오도록 잡는다.
    ground_y = CANVAS_H // 2 - anim_height(ground, frames) * SCALE // 2
    lift = (bottom - ground) * SCALE
    y = ground_y + lift + h * SCALE // 2    # clip_draw 는 중심 좌표를 받는다
    # 가로는 프레임 중심이 아니라 몸통 중심(cx)을 화면 가운데에 맞춘다
    x = CANVAS_W // 2 + (w / 2 - cx) * SCALE
    sheet.clip_draw(left, bottom, w, h, x, y, w * SCALE, h * SCALE)


open_canvas(CANVAS_W, CANVAS_H)
sheet = load_image('ryu_sheet.png')

while running:
    name, ground, frames = ANIMATIONS[anim]
    clear_canvas()
    left, bottom, w, h, cx = frames[frame]
    draw_frame(ground, frames, left, bottom, w, h, cx)
    update_canvas()
    handle_events()
    frame = (frame + 1) % len(frames)
    delay(0.15)

close_canvas()
