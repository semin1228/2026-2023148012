# sonic_animation_viewer.py
# LEC09 애니메이션 뷰어
# sonic-sprite.png 에 들어 있는 소닉의 동작 12개를 원본의 4배로 재생한다.
# 각 동작은 5회 반복한 뒤 마지막 프레임에서 1초 쉬고 다음 동작으로 넘어가며,
# 마지막 동작(WAVE) 다음엔 첫 동작(IDLE)으로 돌아가 창을 닫을 때까지 계속된다.
#
# 실행: 이 파일이 있는 폴더(Labs/LEC09)에서 python sonic_animation_viewer.py
# 조작: ESC 또는 창 닫기 - 종료
# 화면: 왼쪽 위에 '동작 이름 반복 횟수/5' (쉬는 중이면 PAUSE), 동작 순번, 프레임 시간과 이동 속도를 표시한다
#
# 동작 (시트의 줄 순서, 8번 줄과 10번 줄은 각각 둘로 나눴다)
#   IDLE 11, WALK 12, SKID 6, SPIN 9, ROLL 6, DASH 6, PEEL 6, TURN 6, HURT 2, PUSH 8, RAISE 2, WAVE 2 프레임 (합계 76)
#   프레임 시간은 동작 느낌에 맞춰 0.04 ~ 0.15초로 다르고, 한 바퀴는 약 46초다
#   (동작마다 프레임 수 x 프레임 시간 x 5회 의 합 33.9초 + 1초 x 12동작)
#
# 이동
#   - WALK, SKID, ROLL, DASH, PEEL, PUSH 는 애니메이션과 동시에 오른쪽으로 이동하고, 나머지는 제자리다
#   - 이동 동작은 가운데보다 (5회 이동 거리 / 2) 왼쪽에서 출발해 같은 거리만큼 오른쪽에서 끝난다.
#     출발 위치와 끝 위치가 가운데를 기준으로 대칭이고, 몸이 화면 밖으로 나가지 않는다
#   - HURT 는 화면 위쪽에서 중력처럼 떨어져 5회가 끝날 때 바닥에 닿는다
#
# 시트 특징과 처리
#   - 프레임마다 폭과 간격이 달라서 프레임 좌표를 하나씩 표(ANIMATIONS)에 적었다
#   - 프레임 높이는 줄 전체로 잘라서, 같은 동작 안에서 발이 떠 있는 프레임은 떠 있는 그대로 보인다
#   - 줄마다 높이가 달라서 프레임 아래쪽을 바닥선(GROUND_Y)에 맞춰 그린다
#   - 프레임 전환, 1초 쉬기, 이동은 모두 get_time() 경과 시간으로 재서 컴퓨터 속도와 관계없이 같은 빠르기로 재생된다

from pico2d import *

# 화면
CANVAS_W, CANVAS_H = 1200, 800
SCALE = 4   # 과제 조건: 원본의 4배로 그린다
GROUND_Y = 300   # 바닥선 y. 모든 프레임의 아래쪽(발끝)을 여기에 맞춘다
BG_COLOR = (40, 44, 70)   # 소닉의 파란색과 겹치지 않는 어두운 남색
FLOOR_COLOR = (64, 70, 100)   # 바닥선 아래를 칠하는 색

# 재생
REPEAT = 5   # 동작마다 반복할 횟수
PAUSE_TIME = 1.0   # 반복이 끝난 뒤 마지막 프레임에서 쉬는 시간(초)
LOOP_DELAY = 0.01   # 루프 한 번마다 쉬는 시간. 프레임 시간과 상관없이 입력 확인을 자주 하려고 짧게 둔다

# 글자
FONT_PATH = 'C:/Windows/Fonts/consola.ttf'   # 정보 표시용 Windows 기본 글꼴
FONT_SIZE = 32
TEXT_COLOR = (255, 255, 255)   # 동작 이름, 반복 횟수
SUB_TEXT_COLOR = (180, 190, 230)   # 동작 순번

# 동작 표: (이름, 프레임 시간(초), 이동 속도, (시작 높이, 끝 높이), 프레임 목록). 동작을 늘릴 때 이 표에 한 줄씩 추가만 하면 된다
# 프레임 시간은 프레임 1장을 보여 주는 시간으로, 동작마다 다르게 줄 수 있다
# 이동 속도는 원본 픽셀/초 (그릴 때처럼 SCALE 을 곱해 화면에서 움직인다). 0 이면 제자리, 양수면 오른쪽(소닉이 보는 방향)
# 높이는 바닥선에서 떠 있는 높이(원본 픽셀). 5회 반복하는 동안 시작 높이에서 끝 높이로 바뀐다. (0, 0) 이면 바닥에 서 있다
# 프레임 좌표는 (left, bottom, w, h) - pico2d 좌하단 원점 기준
# 프레임마다 폭과 간격이 달라서 일정한 간격으로 계산할 수 없고, 하나씩 적는다.
# 높이는 줄 전체로 잘라서 같은 줄의 프레임은 발 위치가 그대로 유지된다
ANIMATIONS = [
    ('IDLE', 0.15, 0, (0, 0), [   # 1번 줄 y 39~77. 서서 기다리기 - 느리게
        (1, 447, 29, 39), (31, 447, 26, 39), (58, 447, 28, 39), (86, 447, 30, 39),
        (118, 447, 30, 39), (150, 447, 30, 39), (182, 447, 29, 39), (211, 447, 29, 39),
        (240, 447, 29, 39), (270, 447, 24, 39), (302, 447, 29, 39),
    ]),
    ('WALK', 0.07, 60, (0, 0), [   # 2번 줄 y 79~117. 걷기 -> 달리기 - 보통 빠르기로 오른쪽으로 간다
        (8, 407, 26, 39), (37, 407, 27, 39), (65, 407, 31, 39), (97, 407, 37, 39),
        (135, 407, 32, 39), (170, 407, 32, 39), (206, 407, 26, 39), (238, 407, 24, 39),
        (263, 407, 30, 39), (295, 407, 36, 39), (334, 407, 32, 39), (370, 407, 29, 39),
    ]),
    ('SKID', 0.08, 30, (0, 0), [   # 3번 줄 y 121~163. 브레이크(붉은 잔상까지 한 프레임) - 미끄러지며 천천히 앞으로
        (1, 361, 33, 43), (39, 361, 35, 43), (89, 361, 35, 43), (130, 361, 34, 43),
        (181, 361, 34, 43), (228, 361, 33, 43),
    ]),
    ('SPIN', 0.05, 0, (0, 0), [   # 4번 줄 y 167~199. 스핀 대시(몸을 말아 공이 된다) - 제자리 회전이라 빠르게
        (1, 325, 29, 33), (35, 325, 29, 33), (67, 325, 30, 33), (98, 325, 31, 33),
        (131, 325, 29, 33), (162, 325, 29, 33), (193, 325, 30, 33), (230, 325, 31, 33),
        (268, 325, 30, 33),
    ]),
    ('ROLL', 0.04, 150, (0, 0), [   # 5번 줄 y 206~232. 공 모양으로 구르기 - 빠르게 굴러간다
        (1, 292, 30, 27), (36, 292, 29, 27), (70, 292, 29, 27), (105, 292, 29, 27),
        (139, 292, 29, 27), (174, 292, 29, 27),
    ]),
    ('DASH', 0.05, 120, (0, 0), [   # 6번 줄 y 238~273. 빠른 달리기(다리가 원처럼 보인다) - 빠르게 달려간다
        (1, 251, 29, 36), (36, 251, 30, 36), (74, 251, 31, 36), (111, 251, 31, 36),
        (149, 251, 30, 36), (186, 251, 31, 36),
    ]),
    ('PEEL', 0.04, 180, (0, 0), [   # 7번 줄 y 283~317. 8자 다리 달리기 - 가장 빠르게 달려간다
        (1, 207, 29, 35), (36, 207, 30, 35), (72, 207, 39, 35), (123, 207, 39, 35),
        (172, 207, 39, 35), (218, 207, 38, 35),
    ]),
    # 8번 줄에는 몸을 돌리는 동작과 피격 동작이 같이 있어서 둘로 나눴다
    ('TURN', 0.12, 0, (0, 0), [   # 8번 줄 앞 6프레임 y 326~370. 앞 -> 뒤로 돌기 - 천천히
        (1, 154, 24, 45), (31, 154, 29, 45), (65, 154, 20, 45), (90, 154, 25, 45),
        (119, 154, 25, 45), (149, 154, 20, 45),
    ]),
    ('HURT', 0.15, 0, (95, 0), [   # 8번 줄 뒤 2프레임. 피격 - 느리게, 화면 위쪽에서 떨어진다
        # 시작 높이 95 x 4 = 380px. 바닥선 300 + 380 + 프레임 높이 112 = 792 라 출발할 때도 화면 위로 나가지 않는다
        # 키가 작아서 이 2프레임의 범위 y 341~368 로 잘라 바닥에 닿게 했다
        (184, 156, 40, 28), (232, 156, 39, 28),
    ]),
    ('PUSH', 0.12, 15, (0, 0), [   # 9번 줄 y 377~416. 밀기 - 힘주는 동작이라 느리게, 밀면서 천천히 앞으로
        (1, 108, 27, 40), (31, 108, 31, 40), (64, 108, 31, 40), (99, 108, 33, 40),
        (136, 108, 32, 40), (176, 108, 33, 40), (217, 108, 33, 40), (254, 108, 33, 40),
    ]),
    # 10번 줄에는 두 팔을 드는 동작과 한 손을 흔드는 동작이 같이 있어서 둘로 나눴다
    ('RAISE', 0.15, 0, (0, 0), [   # 10번 줄 앞 2프레임 y 426~468. 두 팔 들기 - 느리게
        (6, 56, 34, 43), (49, 56, 34, 43),
    ]),
    ('WAVE', 0.15, 0, (0, 0), [   # 10번 줄 뒤 2프레임. 한 손 흔들기 - 느리게
        # 발이 앞 2프레임보다 3px 높아서 이 2프레임의 범위 y 427~465 로 잘라 바닥에 닿게 했다
        (96, 59, 23, 39), (125, 59, 23, 39),
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


def start_x(index):
    # 이동 동작이 화면 밖으로 나가지 않도록, 5회 동안 갈 거리의 절반만큼 가운데보다 왼쪽에서 출발한다.
    # 그러면 끝나는 위치는 가운데보다 같은 거리만큼 오른쪽이라, 출발 위치와 끝 위치가 가운데를 기준으로 대칭이 된다.
    # 가장 멀리 가는 WALK(1008px)도 몸 양 끝이 화면 안(22 ~ 1178)에 들어온다. 제자리 동작은 거리가 0 이라 가운데
    name, frame_time, speed, height, frames = ANIMATIONS[index]
    distance = speed * SCALE * len(frames) * frame_time * REPEAT
    return CANVAS_W // 2 - distance / 2


def update():
    # delay 로 프레임 시간을 맞추면 컴퓨터 속도나 그리기 시간에 따라 빠르기가 달라진다.
    # 루프는 짧게 돌리고, 실제로 그 동작의 프레임 시간이 지났을 때만 다음 프레임으로 넘긴다
    global anim, frame, repeat_count, paused, pause_started, frame_started, x, last_update, lift, anim_started
    name, frame_time, speed, height, frames = ANIMATIONS[anim]
    now = get_time()
    dt = now - last_update   # 지난 update 뒤로 흐른 시간. 이동 거리를 시간에 비례하게 만든다
    last_update = now
    if paused:
        # 쉬는 동안엔 마지막 프레임을 그대로 보여 주고, PAUSE_TIME 이 지나면 다음 동작으로.
        # 마지막 동작 다음엔 % 로 첫 동작에 돌아가 무한 반복된다
        if now - pause_started >= PAUSE_TIME:
            paused = False
            anim = (anim + 1) % len(ANIMATIONS)
            frame = 0
            repeat_count = 0
            frame_started = pause_started + PAUSE_TIME
            anim_started = frame_started
            x = start_x(anim)
            lift = ANIMATIONS[anim][3][0] * SCALE   # 첫 프레임부터 시작 높이에 그려지게 바로 맞춰 둔다
        return   # 쉬는 동안은 움직이지 않는다
    # 프레임 전환과 같은 시간(get_time) 기준으로 움직여서 애니메이션과 이동이 함께 맞는다
    x += speed * SCALE * dt
    start_h, end_h = height
    if start_h != end_h:
        # 5회 재생 시간 T 동안 시작 높이에서 끝 높이로 바꿔, 끝나는 순간(t = T) 정확히 끝 높이에 닿게 한다.
        # 떨어질 때는 중력처럼 처음엔 천천히, 바닥에 가까울수록 빠르게 (진행 비율 u^2)
        play_time = len(frames) * frame_time * REPEAT
        u = min(now - anim_started, play_time) / play_time
        lift = (start_h + (end_h - start_h) * u ** 2) * SCALE
    if now - frame_started >= frame_time:
        frame_started += frame_time   # now 로 두면 루프 지연이 프레임마다 쌓인다
        frame += 1
        if frame == len(frames):   # 마지막 프레임까지 보여 줬으면 1회 반복 완료
            repeat_count += 1
            if repeat_count == REPEAT:
                frame = len(frames) - 1   # 0 으로 되돌리지 않고 마지막 프레임에서 멈춘다
                paused = True
                pause_started = frame_started
                lift = height[1] * SCALE   # 끝 높이에 머문 채로 쉰다
            else:
                frame = 0


def draw_info():
    # 5회 반복과 1초 쉬기가 지켜지는지 눈으로 셀 수 있도록 지금 상태를 글자로 보여 준다
    name, frame_time, speed, height, frames = ANIMATIONS[anim]
    state = 'PAUSE' if paused else f'{repeat_count + 1}/{REPEAT}'   # repeat_count 는 끝낸 횟수라 +1
    font.draw(30, CANVAS_H - 30, f'{name} {state}', TEXT_COLOR)
    font.draw(30, CANVAS_H - 70, f'animation {anim + 1}/{len(ANIMATIONS)}', SUB_TEXT_COLOR)
    # 동작마다 다른 프레임 시간과 이동 속도(화면 px/초)를 확인할 수 있게 함께 보여 준다
    font.draw(30, CANVAS_H - 110, f'frame {frame_time:.2f}s  speed {speed * SCALE}px/s', SUB_TEXT_COLOR)


def draw():
    clear_canvas()
    draw_rectangle(0, 0, CANVAS_W, CANVAS_H, *BG_COLOR, filled=True)
    draw_rectangle(0, 0, CANVAS_W, GROUND_Y, *FLOOR_COLOR, filled=True)
    # 시트의 y 는 위가 0 이지만 pico2d 는 아래가 0 이라, 줄 아래쪽 y=77 은 bottom = 525 - 77 - 1 = 447
    left, bottom, w, h = ANIMATIONS[anim][4][frame]
    # clip_draw 는 중심 좌표를 받는다. 중심을 화면 가운데에 고정하면 높이가 다른 동작끼리 발 위치가 달라지므로,
    # 프레임 아래쪽이 바닥선에 오도록 중심 y 를 바닥선 + (그린 높이 / 2) 로 잡는다
    y = GROUND_Y + lift + h * SCALE / 2   # lift: 떨어지는 동작에서 바닥선 위로 떠 있는 높이
    sheet.clip_draw(left, bottom, w, h, x, y, w * SCALE, h * SCALE)
    draw_info()
    update_canvas()


open_canvas(CANVAS_W, CANVAS_H)
sheet = load_image('sonic-sprite.png')   # 399 x 525, 배경 투명
font = load_font(FONT_PATH, FONT_SIZE)

running = True
anim = 0    # 지금 재생 중인 동작 번호
frame = 0   # 지금 그리는 프레임 번호
repeat_count = 0   # 지금 동작을 처음부터 끝까지 몇 번 재생했는지
paused = False   # 5회 반복을 마치고 쉬는 중인지
pause_started = 0.0   # 쉬기 시작한 시각
frame_started = get_time()   # 지금 프레임을 보여 주기 시작한 시각
x = start_x(anim)   # 캐릭터의 화면 x. 이동 동작에서 바뀐다
lift = ANIMATIONS[anim][3][0] * SCALE   # 바닥선에서 떠 있는 높이(화면 px). 높이가 바뀌는 동작에서 바뀐다
anim_started = frame_started   # 지금 동작을 시작한 시각. 높이 계산에 쓴다
last_update = get_time()   # 마지막으로 update 한 시각
while running:
    draw()
    handle_events()
    update()
    delay(LOOP_DELAY)

close_canvas()
