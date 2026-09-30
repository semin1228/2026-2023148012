# animation_viewer.py
# Drill #8 애니메이션 뷰어
# ryu_sheet.png (스트리트 파이터 II 류) 의 애니메이션 6종을 화면 중앙에 4배 확대해서 재생한다.
# 각 애니메이션은 5회 반복 후 1초 정지하고, 다음 애니메이션으로 넘어가 6종이 무한 반복된다.
#
# 조작: SPACE 다음 애니메이션 / B 프레임 경계 보기 / ESC 종료
#
# [가산점] 프레임 크기가 프레임마다 다른 시트
#   - 프레임마다 (left, bottom, w, h) 를 따로 저장해 clip_draw 로 자른다 (33x90 ~ 72x39 등)
#   - 발 위치: 시트에서 땅보다 떠 있는 만큼(bottom - ground) 올려 그려 발이 출렁이지 않는다
#   - 몸통 위치: 프레임별 몸통 중심 x(cx) 를 화면 가운데에 맞춰 팔다리를 뻗어도 몸이 제자리에 있다
# [가산점] 애니메이션마다 프레임 수가 다름
#   - 3(PUNCH) / 4(IDLE) / 5(WALK, KICK) / 6(JUMP, SHORYUKEN) 프레임을 len(frames) 로 처리한다
#
# 시트 준비: Ryu.png -> make_transparent.py (배경 투명) -> ryu_sheet.png
#           좌표표는 find_frames.py 로 분석해서 얻었다

from pico2d import *

CANVAS_W, CANVAS_H = 800, 600
REPEAT = 5          # 애니메이션마다 반복할 횟수
PAUSE_TIME = 1.0    # 반복이 끝난 뒤 멈춰 있는 시간(초)
BG_COLOR = (32, 36, 56)      # 배경색
FLOOR_COLOR = (70, 62, 58)   # 바닥색
FONT_PATH = 'C:/Windows/Fonts/consola.ttf'   # 정보 표시용 Windows 기본 글꼴
SCALE = 4   # 대기 자세 키 82px -> 328px (화면 높이 600 의 절반 이상). 가장 높은 승룡권도 600 안에 들어간다
TOP_MARGIN = 16   # 가장 높이 뜨는 프레임과 화면 위쪽 사이의 여백

# 애니메이션 표: (이름, 땅 높이, 프레임당 시간(초), 프레임 목록, 프레임별 시간 배율)
# 프레임당 시간은 동작 느낌에 맞춰 정했다: 공격(펀치/킥/승룡권)은 빠르게, 대기는 느리게
# 프레임별 시간 배율: 각 프레임은 프레임당 시간 x 배율 만큼 보인다.
#   원작처럼 공격이 다 뻗은 순간에 잠깐 머물러야 타격감이 살아서 그 프레임만 배율을 키웠다
# 프레임 좌표는 (left, bottom, width, height, 몸통중심x) - pico2d 좌하단 원점 기준, find_frames.py 로 얻은 값
# 몸통중심x 는 프레임 왼쪽에서 몸통 중심까지의 거리. 팔다리를 뻗어도 몸이 제자리에 있도록 가로 정렬에 쓴다
# 땅 높이는 그 동작 줄에서 발이 땅에 닿은 프레임의 bottom 값
ANIMATIONS = [
    ('IDLE', 1610, 0.18, [
        (5, 1610, 41, 82, 20), (53, 1610, 41, 81, 20), (102, 1610, 41, 80, 19), (151, 1610, 41, 81, 20),
    ], [1, 1, 1, 1]),
    ('WALK', 1610, 0.12, [
        (221, 1610, 41, 75, 22), (269, 1610, 41, 80, 22), (317, 1610, 41, 80, 22), (365, 1610, 43, 81, 23),
        (413, 1610, 41, 80, 22),
    ], [1, 1, 1, 1, 1]),
    ('PUNCH', 1495, 0.08, [
        (5, 1495, 41, 81, 20), (54, 1495, 55, 81, 23), (113, 1495, 41, 81, 20),
    ], [1, 2.5, 1.5]),
    ('KICK', 1247, 0.10, [
        (4, 1247, 42, 81, 11), (53, 1247, 55, 84, 16), (111, 1247, 69, 84, 18), (184, 1247, 57, 70, 15),
        (248, 1247, 42, 73, 11),
    ], [1, 1, 2.5, 1, 1]),
    # JUMP, SHORYUKEN 은 몸을 돌리거나 뛰어오르는 동작이라 몸통중심x 에 무게중심 값(mass cx)을 쓴다
    ('JUMP', 1023, 0.10, [
        (158, 1023, 33, 90, 13), (205, 1060, 61, 37, 34), (282, 1046, 31, 68, 17), (329, 1061, 72, 39, 33),
        (419, 1043, 43, 74, 22), (474, 1026, 33, 90, 15),
    ], [1.5, 1, 1.2, 1.2, 1, 1.5]),
    ('SHORYUKEN', 730, 0.09, [
        (3, 730, 44, 74, 26), (52, 730, 49, 80, 27), (107, 730, 41, 111, 19), (155, 752, 38, 108, 19),
        (207, 765, 29, 101, 14), (256, 730, 44, 94, 18),
    ], [1, 1, 1, 1.5, 3, 1.5]),
]

running = True
anim = 0    # 지금 재생 중인 애니메이션 번호
frame = 0   # 그 애니메이션 안에서의 프레임 번호
loop = 0    # 지금 애니메이션을 처음부터 끝까지 몇 번 재생했는지
paused_at = None   # 5회 반복을 마치고 정지한 시각. None 이면 재생 중
frame_started = 0.0   # 지금 프레임을 보여 주기 시작한 시각
show_box = False      # B 키: 프레임 경계 사각형과 몸통 중심선 보기


def handle_events():
    global running, show_box
    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            next_animation()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_b:
            show_box = not show_box


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


# 화면에서 발이 닿는 땅의 y. 모든 애니메이션이 같은 바닥에 서도록 하나로 고정한다.
# 가장 높이 뜨는 동작(승룡권, 136px * 4 = 544px)이 화면 위 여백 TOP_MARGIN 안에 들어오도록 잡는다
GROUND_Y = CANVAS_H - TOP_MARGIN - max(anim_height(g, fs) for _, g, _, fs, _ in ANIMATIONS) * SCALE


def draw_background():
    draw_rectangle(0, 0, CANVAS_W - 1, CANVAS_H - 1, *BG_COLOR, filled=True)
    draw_rectangle(0, 0, CANVAS_W - 1, GROUND_Y, *FLOOR_COLOR, filled=True)


def draw_info(name, frames, w, h):
    # 채점/발표 때 확인하기 쉽도록 이름, 반복 횟수, 프레임 번호와 현재 프레임 크기를 표시한다
    if font is None:
        return
    font.draw(20, CANVAS_H - 25, f'{anim + 1}/{len(ANIMATIONS)}  {name}', (255, 255, 255))
    state = 'PAUSE' if paused_at is not None else f'loop {loop + 1}/{REPEAT}'
    font.draw(20, CANVAS_H - 55, state, (255, 220, 100))
    font.draw(20, CANVAS_H - 85, f'frame {frame + 1}/{len(frames)}  size {w}x{h}', (180, 200, 255))
    font.draw(20, 20, 'SPACE: next   B: frame box   ESC: quit', (150, 150, 150))


def draw_frame(ground, left, bottom, w, h, cx):
    # 프레임 크기가 제각각이라 중심을 고정하면 발이 위아래로 출렁인다.
    # 그래서 화면의 땅 위치를 정하고, 프레임은 시트에서 땅보다 떠 있는 만큼(bottom - ground)만 올려서 그린다.
    lift = (bottom - ground) * SCALE
    y = GROUND_Y + lift + h * SCALE // 2    # clip_draw 는 중심 좌표를 받는다
    # 가로는 프레임 중심이 아니라 몸통 중심(cx)을 화면 가운데에 맞춘다
    x = CANVAS_W // 2 + (w / 2 - cx) * SCALE
    sheet.clip_draw(left, bottom, w, h, x, y, w * SCALE, h * SCALE)
    if show_box:
        # 프레임마다 잘라 오는 사각형의 크기가 달라지는 것을 눈으로 확인하기 위한 표시
        half_w, half_h = w * SCALE / 2, h * SCALE / 2
        draw_rectangle(x - half_w, y - half_h, x + half_w, y + half_h, 255, 60, 60)
        draw_line(CANVAS_W // 2, GROUND_Y, CANVAS_W // 2, CANVAS_H - TOP_MARGIN, 60, 255, 60)


open_canvas(CANVAS_W, CANVAS_H)
sheet = load_image('ryu_sheet.png')
try:
    font = load_font(FONT_PATH, 22)
except IOError:
    font = None   # 글꼴이 없는 환경에서도 애니메이션 재생은 되도록 정보 표시만 생략
frame_started = get_time()

while running:
    name, ground, frame_time, frames, holds = ANIMATIONS[anim]
    clear_canvas()
    draw_background()
    left, bottom, w, h, cx = frames[frame]
    draw_frame(ground, left, bottom, w, h, cx)
    draw_info(name, frames, w, h)
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
    elif now - frame_started >= frame_time * holds[frame]:
        frame_started += frame_time * holds[frame]   # now 로 두면 루프 지연(약 10ms)이 프레임마다 쌓인다
        frame += 1
        if frame == len(frames):   # 마지막 프레임까지 보여 줬으면 한 바퀴 완료
            loop += 1
            if loop == REPEAT:
                frame = len(frames) - 1   # 마지막 프레임에서 멈춘다
                paused_at = now
            else:
                frame = 0
    delay(0.01)

close_canvas()
