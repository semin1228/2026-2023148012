# find_frames.py
# ryu_sheet.png 에서 캐릭터 프레임의 사각형 좌표를 찾아 출력하는 분석 도구.
# 프레임마다 크기와 위치가 제각각이라 격자로 자를 수 없어서, 투명하지 않은 픽셀끼리
# 이어진 덩어리를 찾아 그 경계 사각형을 프레임으로 본다. 출력은 (left, bottom, w, h, 몸통중심x).
# (게임 실행에는 필요 없음, Pillow 필요)
# 사용법: python find_frames.py [top_y] [bottom_y]   <- 시트의 해당 세로 범위만 출력

import sys
from PIL import Image

SHEET = 'ryu_sheet.png'
MIN_W, MIN_H = 4, 30   # 구분선(폭 1~2px), 글씨/떨어진 그림자(높이 15px 이하)를 걸러내는 기준
DARK = 40              # 이보다 어두운 픽셀(검은 띠, 머리카락, 윤곽선)의 평균 x 를 몸통 중심으로 본다


def find_blobs(img):
    w, h = img.size
    px = img.load()
    seen = [[False] * w for _ in range(h)]
    blobs = []
    for sy in range(h):
        for sx in range(w):
            if seen[sy][sx] or px[sx, sy][3] == 0:
                continue
            # 8방향으로 이어진 픽셀을 모두 방문하며 경계 사각형을 넓혀 간다
            stack = [(sx, sy)]
            seen[sy][sx] = True
            l, t, r, b = sx, sy, sx, sy
            while stack:
                x, y = stack.pop()
                l, t, r, b = min(l, x), min(t, y), max(r, x), max(b, y)
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx] and px[nx, ny][3] != 0:
                            seen[ny][nx] = True
                            stack.append((nx, ny))
            blobs.append((l, t, r, b))
    return blobs


def body_center_x(px, l, t, r, b):
    # 팔다리를 뻗으면 프레임 중심과 몸통 중심이 어긋난다.
    # 어두운 픽셀의 평균 x 를 프레임 왼쪽 기준으로 돌려주어 몸통 기준 정렬에 쓴다.
    xs = [x - l for y in range(t, b + 1) for x in range(l, r + 1)
          if px[x, y][3] != 0 and max(px[x, y][:3]) < DARK]
    return round(sum(xs) / len(xs)) if xs else (r - l + 1) // 2


def main():
    y_from = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    y_to = int(sys.argv[2]) if len(sys.argv) > 2 else 99999
    img = Image.open(SHEET).convert('RGBA')
    sheet_h = img.size[1]

    frames = [b for b in find_blobs(img)
              if b[2] - b[0] + 1 >= MIN_W and b[3] - b[1] + 1 >= MIN_H
              and y_from <= b[1] <= y_to]

    # 아래쪽 y(발 위치)가 비슷한 것끼리 한 줄로 묶고, 줄 안에서는 왼쪽부터 정렬
    frames.sort(key=lambda b: (b[3], b[0]))
    rows = []
    for f in frames:
        if rows and abs(rows[-1][0][3] - f[3]) < 20:
            rows[-1].append(f)
        else:
            rows.append([f])
    px = img.load()
    for row in rows:
        row.sort(key=lambda b: b[0])
        print(f'--- row (bottom ~ {row[0][3]}): {len(row)} frames')
        for l, t, r, b in row:
            w, h = r - l + 1, b - t + 1
            # pico2d 는 원점이 좌하단이라 bottom = 시트높이 - 1 - 아래쪽y 로 바꿔서 출력
            cx = body_center_x(px, l, t, r, b)
            print(f'    ({l}, {sheet_h - 1 - b}, {w}, {h}, {cx}),   # x={l}..{r}, y={t}..{b}')


if __name__ == '__main__':
    main()
