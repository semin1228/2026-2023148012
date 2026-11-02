world = []

# 객체를 게임월드에 추가하는 함수
def add_object(o):
    world.append(o)

# 게임 로직
def update():
    for o in world:
        o.update()

# 게임 월드 렌더링
def render():
    for o in world:
        o.draw()