# sonic_animation_viewer.py
# LEC09 애니메이션 뷰어 - sonic-sprite.png 의 동작을 재생한다

from pico2d import *

CANVAS_W, CANVAS_H = 1200, 800
SCALE = 4   # 과제 조건: 원본의 4배로 그린다
FRAME_TIME = 0.1   # 프레임 1장을 보여 주는 시간(초)
REPEAT = 5   # 동작마다 반복할 횟수
PAUSE_TIME = 1.0   # 반복이 끝난 뒤 마지막 프레임에서 쉬는 시간(초)
BG_COLOR = (40, 44, 70)   # 소닉의 파란색과 겹치지 않는 어두운 남색
GROUND_Y = 300   # 바닥선 y. 모든 프레임의 아래쪽(발끝)을 여기에 맞춘다
FLOOR_COLOR = (64, 70, 100)   # 바닥선 아래를 칠하는 색

# 동작 표: (이름, 프레임 목록). 동작을 늘릴 때 이 표에 한 줄씩 추가만 하면 된다
# 프레임 좌표는 (left, bottom, w, h) - pico2d 좌하단 원점 기준
# 프레임마다 폭과 간격이 달라서 일정한 간격으로 계산할 수 없고, 하나씩 적는다.
# 높이는 줄 전체로 잘라서 같은 줄의 프레임은 발 위치가 그대로 유지된다
ANIMATIONS = [
    ('IDLE', [   # 1번 줄 y 39~77
        (1, 447, 29, 39), (31, 447, 26, 39), (58, 447, 28, 39), (86, 447, 30, 39),
        (118, 447, 30, 39), (150, 447, 30, 39), (182, 447, 29, 39), (211, 447, 29, 39),
        (240, 447, 29, 39), (270, 447, 24, 39), (302, 447, 29, 39),
    ]),
    ('WALK', [   # 2번 줄 y 79~117
        (8, 407, 26, 39), (37, 407, 27, 39), (65, 407, 31, 39), (97, 407, 37, 39),
        (135, 407, 32, 39), (170, 407, 32, 39), (206, 407, 26, 39), (238, 407, 24, 39),
        (263, 407, 30, 39), (295, 407, 36, 39), (334, 407, 32, 39), (370, 407, 29, 39),
    ]),
    ('SKID', [   # 3번 줄 y 121~163 (브레이크, 붉은 잔상까지 한 프레임)
        (1, 361, 33, 43), (39, 361, 35, 43), (89, 361, 35, 43), (130, 361, 34, 43),
        (181, 361, 34, 43), (228, 361, 33, 43),
    ]),
    ('SPIN', [   # 4번 줄 y 167~199 (스핀 대시, 몸을 말아 공이 된다)
        (1, 325, 29, 33), (35, 325, 29, 33), (67, 325, 30, 33), (98, 325, 31, 33),
        (131, 325, 29, 33), (162, 325, 29, 33), (193, 325, 30, 33), (230, 325, 31, 33),
        (268, 325, 30, 33),
    ]),
    ('ROLL', [   # 5번 줄 y 206~232 (공 모양으로 구르기)
        (1, 292, 30, 27), (36, 292, 29, 27), (70, 292, 29, 27), (105, 292, 29, 27),
        (139, 292, 29, 27), (174, 292, 29, 27),
    ]),
    ('DASH', [   # 6번 줄 y 238~273 (빠른 달리기, 다리가 원처럼 보인다)
        (1, 251, 29, 36), (36, 251, 30, 36), (74, 251, 31, 36), (111, 251, 31, 36),
        (149, 251, 30, 36), (186, 251, 31, 36),
    ]),
    ('PEEL', [   # 7번 줄 y 283~317 (8자 다리 달리기)
        (1, 207, 29, 35), (36, 207, 30, 35), (72, 207, 39, 35), (123, 207, 39, 35),
        (172, 207, 39, 35), (218, 207, 38, 35),
    ]),
]


def handle_events():
    global running
    # 이벤트를 꺼내 주지 않으면 창이 응답 없음 상태가 된다
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def update():
    # delay 로 프레임 시간을 맞추면 컴퓨터 속도나 그리기 시간에 따라 빠르기가 달라진다.
    # 루프는 짧게 돌리고, 실제로 FRAME_TIME 이 지났을 때만 다음 프레임으로 넘긴다
    global anim, frame, repeat_count, paused, pause_started, frame_started
    frames = ANIMATIONS[anim][1]
    now = get_time()
    if paused:
        # 쉬는 동안엔 마지막 프레임을 그대로 보여 주고, PAUSE_TIME 이 지나면 다음 동작으로.
        # 마지막 동작 다음엔 % 로 첫 동작에 돌아가 무한 반복된다
        if now - pause_started >= PAUSE_TIME:
            paused = False
            anim = (anim + 1) % len(ANIMATIONS)
            frame = 0
            repeat_count = 0
            frame_started = pause_started + PAUSE_TIME
    elif now - frame_started >= FRAME_TIME:
        frame_started += FRAME_TIME   # now 로 두면 루프 지연이 프레임마다 쌓인다
        frame += 1
        if frame == len(frames):   # 마지막 프레임까지 보여 줬으면 1회 반복 완료
            repeat_count += 1
            if repeat_count == REPEAT:
                frame = len(frames) - 1   # 0 으로 되돌리지 않고 마지막 프레임에서 멈춘다
                paused = True
                pause_started = frame_started
            else:
                frame = 0


def draw():
    clear_canvas()
    draw_rectangle(0, 0, CANVAS_W, CANVAS_H, *BG_COLOR, filled=True)
    draw_rectangle(0, 0, CANVAS_W, GROUND_Y, *FLOOR_COLOR, filled=True)
    # 시트의 y 는 위가 0 이지만 pico2d 는 아래가 0 이라, 줄 아래쪽 y=77 은 bottom = 525 - 77 - 1 = 447
    left, bottom, w, h = ANIMATIONS[anim][1][frame]
    # clip_draw 는 중심 좌표를 받는다. 중심을 화면 가운데에 고정하면 높이가 다른 동작끼리 발 위치가 달라지므로,
    # 프레임 아래쪽이 바닥선에 오도록 중심 y 를 바닥선 + (그린 높이 / 2) 로 잡는다
    y = GROUND_Y + h * SCALE / 2
    sheet.clip_draw(left, bottom, w, h, CANVAS_W // 2, y, w * SCALE, h * SCALE)
    update_canvas()


open_canvas(CANVAS_W, CANVAS_H)
sheet = load_image('sonic-sprite.png')   # 399 x 525, 배경 투명

running = True
anim = 0    # 지금 재생 중인 동작 번호
frame = 0   # 지금 그리는 프레임 번호
repeat_count = 0   # 지금 동작을 처음부터 끝까지 몇 번 재생했는지
paused = False   # 5회 반복을 마치고 쉬는 중인지
pause_started = 0.0   # 쉬기 시작한 시각
frame_started = get_time()   # 지금 프레임을 보여 주기 시작한 시각
while running:
    draw()
    handle_events()
    update()
    delay(0.01)

close_canvas()
