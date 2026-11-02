world = []

# 객체를 게임월드에 추가하는 함수
def add_object(o):
    world.append(o)

# 객체를 게임월드에서 제거하는 함수
def remove_object(o):
    world.remove(o)

# 게임 로직
def update():
    # update 중에 객체가 제거될 수 있으므로 복사본을 돌며 갱신
    for o in world[:]:
        o.update()

# 게임 월드 렌더링
def render():
    for o in world:
        o.draw()