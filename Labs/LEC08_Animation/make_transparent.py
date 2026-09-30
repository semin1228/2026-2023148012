# make_transparent.py
# Ryu.png 의 청록색 단색 배경을 투명으로 바꿔 ryu_sheet.png 로 저장하는 전처리 도구.
# pico2d 는 컬러키(특정 색 투명) 기능이 없어서, 미리 알파 채널을 만들어 둔다.
# 한 번만 실행하면 되고 게임 실행에는 필요 없다. (Pillow 필요)
# 사용법: python make_transparent.py

from PIL import Image

SRC = 'Ryu.png'
DST = 'ryu_sheet.png'
BG_COLOR = (64, 144, 160)   # 시트 배경색. 비슷한 색은 그림 속 픽셀이므로 정확히 같은 색만 지운다


def main():
    img = Image.open(SRC).convert('RGBA')
    px = img.load()
    w, h = img.size
    count = 0
    for y in range(h):
        for x in range(w):
            if px[x, y][:3] == BG_COLOR:
                px[x, y] = (0, 0, 0, 0)
                count += 1
    img.save(DST)
    print(f'{DST} saved: {count} / {w * h} pixels made transparent')


if __name__ == '__main__':
    main()
