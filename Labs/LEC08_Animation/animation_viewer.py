# animation_viewer.py
# Drill #8 애니메이션 뷰어
# ryu_sheet.png 의 여러 애니메이션을 화면 중앙에 확대해서 차례로 재생한다.

from pico2d import *

CANVAS_W, CANVAS_H = 800, 600
REPEAT = 5          # 애니메이션마다 반복할 횟수
PAUSE_TIME = 1.0    # 반복이 끝난 뒤 멈춰 있는 시간(초)
SCALE = 4   # 대기 자세 키 82px -> 328px (화면 높이 600 의 절반 이상). 가장 높은 승룡권도 600 안에 들어간다

# 애니메이션 표: (이름, 땅 높이, 프레임당 시간(초), 프레임 목록)
# 프레임당 시간은 동작 느낌에 맞춰 정했다: 공격(펀치/킥/승룡권)은 빠르게, 대기는 느리게
# 프레임 좌표는 (left, bottom, width, height, 몸통중심x) - pico2d 좌하단 원점 기준, find_frames.py 로 얻은 값
# 몸통중심x 는 프레임 왼쪽에서 몸통 중심까지의 거리. 팔다리를 뻗어도 몸이 제자리에 있도록 가로 정렬에 쓴다
# 땅 높이는 그 동작 줄에서 발이 땅에 닿은 프레임의 bottom 값
ANIMATIONS = [
    ('IDLE', 1610, 0.18, [
        (5, 1610, 41, 82, 20), (53, 1610, 41, 81, 20), (102, 1610, 41, 80, 19), (151, 1610, 41, 81, 20),
    ]),
    ('WALK', 1610, 0.12, [
        (221, 1610, 41, 75, 22), (269, 1610, 41, 80, 22), (317, 1610, 41, 80, 22), (365, 1610, 43, 81, 23),
        (413, 1610, 41, 80, 22),
    ]),
    ('PUNCH', 1495, 0.08, [
        (5, 1495, 41, 81, 20), (54, 1495, 55, 81, 23), (113, 1495, 41, 81, 20),
    ]),
    ('KICK', 1247, 0.10, [
        (4, 1247, 42, 81, 11), (53, 1247, 55, 84, 16), (111, 1247, 69, 84, 18), (184, 1247, 57, 70, 15),
        (248, 1247, 42, 73, 11),
    ]),
    ('JUMP', 1023, 0.10, [
        (158, 1023, 33, 90, 17), (205, 1060, 61, 37, 41), (282, 1046, 31, 68, 13), (329, 1061, 72, 39, 22),
        (419, 1043, 43, 74, 19), (474, 1026, 33, 90, 16),
    ]),
    ('SHORYUKEN', 730, 0.09, [
        (3, 730, 44, 74, 29), (52, 730, 49, 80, 35), (107, 730, 41, 111, 16), (155, 752, 38, 108, 16),
        (207, 765, 29, 101, 10), (256, 730, 44, 94, 16),
    ]),
]

running = True
anim = 0    # 지금 재생 중인 애니메이션 번호
frame = 0   # 그 애니메이션 안에서의 프레임 번호
loop = 0    # 지금 애니메이션을 처음부터 끝까지 몇 번 재생했는지
paused_at = None   # 5회 반복을 마치고 정지한 시각. None 이면 재생 중
frame_started = 0.0   # 지금 프레임을 보여 주기 시작한 시각


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
    global anim, frame, loop, paused_at, frame_started
    anim = (anim + 1) % len(ANIMATIONS)
    frame = 0
    loop = 0
    paused_at = None
    frame_started = get_time()


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
frame_started = get_time()

while running:
    name, ground, frame_time, frames = ANIMATIONS[anim]
    clear_canvas()
    left, bottom, w, h, cx = frames[frame]
    draw_frame(ground, frames, left, bottom, w, h, cx)
    update_canvas()
    handle_events()
    # delay(frame_time) 으로 기다리면 그동안 입력/정지 확인이 멈추고 1초 정지도 frame_time 단위로 어긋난다.
    # 루프는 짧게 돌리고, 시각을 비교해서 frame_time 이 지났을 때만 다음 프레임으로 넘긴다.
    now = get_time()
    if paused_at is not None:
        # 정지 중에는 마지막 프레임을 그대로 보여 주고, 1초가 지나면 다음 애니메이션으로.
        # next_animation() 이 마지막 다음엔 처음으로 돌아가므로 6종이 무한 반복된다
        if now - paused_at >= PAUSE_TIME:
            next_animation()
    elif now - frame_started >= frame_time:
        frame_started += frame_time   # now 로 두면 루프 지연(약 10ms)이 프레임마다 쌓인다
        frame += 1
        if frame == len(frames):   # 마지막 프레임까지 보여 줬으면 한 바퀴 완료
            loop += 1
            print(f'{name} loop {loop}')
            if loop == REPEAT:
                frame = len(frames) - 1   # 마지막 프레임에서 멈춘다
                paused_at = now
                print(f'{name} pause')
            else:
                frame = 0
    delay(0.01)

close_canvas()
