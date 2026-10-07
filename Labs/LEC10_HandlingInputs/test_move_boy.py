# test_move_boy.py
# move_boy.py 자동 테스트. 실제 키보드 대신 정해 둔 키 이벤트를 넣어 게임을 돌리고,
# 매 프레임 그린 위치와 시트 줄을 기록해 채점 기준대로 움직이는지 확인한다.
# 창이 잠깐 떴다가 닫힌다. (게임 실행에는 필요 없음)
# 사용법: python test_move_boy.py

import pico2d

GAME = 'move_boy.py'
KEYS = {'L': pico2d.SDLK_LEFT, 'R': pico2d.SDLK_RIGHT, 'U': pico2d.SDLK_UP, 'D': pico2d.SDLK_DOWN}
ROWS = {300: 'IDLE_R', 200: 'IDLE_L', 100: 'RUN_R', 0: 'RUN_L'}


class FakeEvent:
    def __init__(self, type, key):
        self.type, self.key = type, key


def run(frames, script):
    # script: {프레임 번호: ['+R', '-R', ...]}  + 는 누르기, - 는 떼기
    # 돌려주는 값: 프레임마다 (x, y, 동작 이름)
    tick = 0
    log = []

    def get_events():
        nonlocal tick
        if tick >= frames:
            return [FakeEvent(pico2d.SDL_QUIT, None)]
        events = [FakeEvent(pico2d.SDL_KEYDOWN if s[0] == '+' else pico2d.SDL_KEYUP, KEYS[s[1]])
                  for s in script.get(tick, [])]
        tick += 1
        return events

    def clip_draw(self, left, bottom, w, h, x, y, *rest):
        log.append((round(x), round(y), ROWS[bottom]))

    # move_boy.py 는 from pico2d import * 로 가져가므로 실행 전에 pico2d 쪽 함수를 바꿔 둔다
    pico2d.get_events = get_events
    pico2d.delay = lambda t: None
    pico2d.Image.clip_draw = clip_draw
    exec(open(GAME, encoding='utf-8').read(), {'__name__': '__main__'})
    return log


def test_idle():
    log = run(5, {})
    assert all(a == 'IDLE_R' for _, _, a in log), log
    assert len({(x, y) for x, y, _ in log}) == 1, '가만히 있으면 움직이지 않아야 함'


def test_move_four_directions():
    for key, dx, dy in (('R', 1, 0), ('L', -1, 0), ('U', 0, 1), ('D', 0, -1)):
        log = run(5, {0: ['+' + key]})
        (x0, y0, _), (x1, y1, _) = log[0], log[-1]
        assert (x1 - x0) * dx > 0 or dx == 0, (key, log)
        assert (y1 - y0) * dy > 0 or dy == 0, (key, log)
        assert (x1 == x0) == (dx == 0) and (y1 == y0) == (dy == 0), (key, log)


def test_stop_on_key_up():
    log = run(8, {0: ['+R'], 3: ['-R']})
    assert log[-1][:2] == log[-3][:2], '키를 떼면 멈춰야 함'
    assert log[-1][2] == 'IDLE_R'


def test_run_animation_direction():
    assert run(3, {0: ['+R']})[-1][2] == 'RUN_R'
    assert run(3, {0: ['+L']})[-1][2] == 'RUN_L'


def test_up_down_keeps_direction():
    # 왼쪽을 보다가 위아래로 움직이면 왼쪽 달리기, 멈추면 왼쪽 IDLE
    log = run(10, {0: ['+L'], 2: ['-L', '+U'], 5: ['-U', '+D'], 8: ['-D']})
    assert [a for _, _, a in log[3:8]] == ['RUN_L'] * 5, log
    assert log[-1][2] == 'IDLE_L', log
    # 처음(오른쪽)부터 위로만 움직이면 오른쪽 달리기
    assert run(3, {0: ['+U']})[-1][2] == 'RUN_R'


if __name__ == '__main__':
    tests = [f for name, f in list(globals().items()) if name.startswith('test_')]
    for test in tests:
        test()
        print('PASS', test.__name__)
    print(f'{len(tests)} tests passed')
