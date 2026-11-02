
world = [ [], [] ]  # 게임월드에 존재하는 객체를 담는 리스트, [0] : background, [1] : foreground

# 객체를 게임월드에 추가하는 함수
def add_object(o, depth = 0): # depth : 0 을 기본값으로 하여, 0 레이어에 추가
    world[depth].append(o)

# 객체를 게임월드에서 제거하는 함수
def remove_object(o):
    for layer in world: # 각 레이어를 순회
        if o in layer: # 객체가 레이어에 존재하면 제거
            layer.remove(o)
            return # 제거 후 함수 종료

# 게임 로직
def update():
    # update 중에 객체가 제거될 수 있으므로 복사본을 돌며 갱신
    for layer in world:
        for o in layer:
            o.update()

# 게임 월드 렌더링
def render():
    for layer in world:
        for o in layer:
            o.draw()