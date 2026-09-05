from pathlib import Path
from math import cos, sin, pi
from PIL import Image, ImageDraw, ImageFont

OUT = Path('images/chapter11')
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1600, 900
BG = '#F8FBFF'
NAVY = '#173B64'
BLUE = '#5AA9E6'
LIGHT_BLUE = '#E8F4FF'
GREEN = '#63C7A5'
LIGHT_GREEN = '#E8F8F1'
YELLOW = '#F7C95C'
LIGHT_YELLOW = '#FFF7D6'
PINK = '#F18E9D'
LIGHT_PINK = '#FFE9ED'
PURPLE = '#9A8CE0'
LIGHT_PURPLE = '#F0EDFF'
RED = '#E45D5D'
LIGHT_RED = '#FFEAEA'
GRAY = '#5E6B78'
DARK_GRAY = '#3E4A56'
WHITE = '#FFFFFF'

FONT_REG = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size=size)


def rr(draw, box, radius=26, fill=WHITE, outline=None, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def center(draw, box, text, fnt, fill=NAVY, spacing=6):
    x1, y1, x2, y2 = box
    b = draw.multiline_textbbox((0, 0), text, font=fnt, spacing=spacing, align='center')
    tw, th = b[2] - b[0], b[3] - b[1]
    draw.multiline_text(((x1+x2-tw)/2, (y1+y2-th)/2), text, font=fnt, fill=fill, spacing=spacing, align='center')


def arrow(draw, x1, y1, x2, y2, color=BLUE, width=10):
    draw.line((x1, y1, x2-22, y2), fill=color, width=width)
    draw.polygon([(x2-22, y2-18), (x2, y2), (x2-22, y2+18)], fill=color)


def title(draw, main, sub):
    draw.text((85, 55), main, font=font(62, True), fill=NAVY)
    draw.text((88, 138), sub, font=font(30), fill=GRAY)


def save(img, name):
    img.convert('RGB').save(OUT / name, 'JPEG', quality=88, optimize=True, progressive=True)


def image_warning_signal():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '오류 메시지는 실패 선언이 아니라 점검 신호입니다', '자동차 경고등처럼 어디를 먼저 확인해야 하는지 알려주는 단서로 읽습니다.')

    rr(d, (95, 255, 650, 700), 36, WHITE, RED, 4)
    center(d, (130, 280, 615, 335), '자동차 경고등', font(36, True), NAVY)
    d.ellipse((250, 380, 495, 625), fill=LIGHT_RED, outline=RED, width=7)
    center(d, (275, 405, 470, 590), '!', font(120, True), RED)
    rr(d, (165, 635, 580, 685), 18, LIGHT_RED)
    center(d, (180, 635, 565, 685), '차 전체가 실패했다는 뜻이 아님', font(23, True), DARK_GRAY)

    arrow(d, 690, 475, 865, 475, PURPLE, 12)

    rr(d, (900, 255, 1505, 700), 36, WHITE, BLUE, 4)
    center(d, (940, 280, 1465, 335), '프로그램 오류 메시지', font(36, True), NAVY)
    rr(d, (960, 375, 1445, 500), 22, LIGHT_BLUE, BLUE, 3)
    center(d, (985, 385, 1420, 490), 'KeyError: score\nline 12', font(29, True), NAVY, 10)
    rr(d, (980, 540, 1425, 620), 20, LIGHT_GREEN, GREEN, 3)
    center(d, (1000, 540, 1405, 620), '어디를 점검할지 알려주는 단서', font(27, True), NAVY)

    rr(d, (260, 760, 1340, 835), 26, LIGHT_YELLOW, YELLOW, 3)
    center(d, (280, 760, 1320, 835), '오류 메시지는 정답이 아니라 단서다. → 메시지를 읽고 원인을 추론한다.', font(31, True), NAVY)
    save(img, 'error-message-as-signal.jpg')


def image_debugging_loop():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '디버깅은 한 번의 정답 찾기가 아니라 반복 루프입니다', '예상과 실제의 차이를 근거로 가설을 세우고, 한 부분만 수정한 뒤 다시 검증합니다.')

    cx, cy = 800, 505
    rx, ry = 560, 275
    steps = [
        ('1', '예상', LIGHT_BLUE, BLUE),
        ('2', '실행', LIGHT_GREEN, GREEN),
        ('3', '차이 발견', LIGHT_YELLOW, YELLOW),
        ('4', '위치 찾기', LIGHT_PINK, PINK),
        ('5', '가설 세우기', LIGHT_PURPLE, PURPLE),
        ('6', '한 부분 수정', LIGHT_RED, RED),
        ('7', '재실행', LIGHT_GREEN, GREEN),
        ('8', '검증', LIGHT_BLUE, BLUE),
    ]
    positions = []
    for i in range(8):
        angle = -pi/2 + i * (2*pi/8)
        x = cx + rx*cos(angle)
        y = cy + ry*sin(angle)
        positions.append((x, y))

    for i, (num, label, light, accent) in enumerate(steps):
        x, y = positions[i]
        w, h = 235, 105
        rr(d, (x-w/2, y-h/2, x+w/2, y+h/2), 24, light, accent, 4)
        center(d, (x-w/2+10, y-h/2+8, x+w/2-10, y-5), num, font(23, True), accent)
        center(d, (x-w/2+10, y-4, x+w/2-10, y+h/2-8), label, font(27, True), NAVY)

    # curved-cycle impression with directional arrows between nodes
    for i in range(8):
        x1, y1 = positions[i]
        x2, y2 = positions[(i+1) % 8]
        vx, vy = x2-x1, y2-y1
        length = (vx*vx + vy*vy) ** 0.5
        sx, sy = x1 + vx*0.27, y1 + vy*0.27
        ex, ey = x1 + vx*0.73, y1 + vy*0.73
        if length > 0:
            d.line((sx, sy, ex, ey), fill=PURPLE, width=8)
            ux, uy = vx/length, vy/length
            px, py = -uy, ux
            d.polygon([
                (ex, ey),
                (ex-ux*22+px*13, ey-uy*22+py*13),
                (ex-ux*22-px*13, ey-uy*22-py*13),
            ], fill=PURPLE)

    rr(d, (555, 420, 1045, 590), 30, WHITE, NAVY, 4)
    center(d, (585, 440, 1015, 570), '한 번에 여러 곳을 고치지 않는다\n가설 하나 → 수정 하나 → 검증 하나', font(30, True), NAVY, 12)

    rr(d, (270, 785, 1330, 850), 22, LIGHT_GREEN)
    center(d, (290, 785, 1310, 850), '디버깅의 핵심: 차이를 관찰하고, 원인 가설을 세우고, 작은 수정으로 확인한다.', font(28, True), NAVY)
    save(img, 'debugging-loop.jpg')


def image_error_types():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '오류는 발생 시점과 증상에 따라 다르게 읽습니다', '문법 오류·실행 오류·논리 오류는 확인해야 할 단서가 서로 다릅니다.')

    cards = [
        ('문법 오류', 'Syntax Error', '실행 전 막힘', '괄호·콜론·들여쓰기 등\n코드 형태부터 확인', LIGHT_RED, RED),
        ('실행 오류', 'Runtime Error', '실행 중 중단', 'KeyError·TypeError 등\n오류 줄과 실제 값 확인', LIGHT_YELLOW, YELLOW),
        ('논리 오류', 'Logical Error', '실행되지만 결과가 틀림', '예상값과 실제값 비교\n조건·경계·계산 순서 확인', LIGHT_BLUE, BLUE),
    ]
    xs = [95, 565, 1035]
    for x, (kor, eng, symptom, action, light, accent) in zip(xs, cards):
        rr(d, (x, 270, x+410, 700), 32, WHITE, accent, 4)
        rr(d, (x+35, 300, x+375, 370), 20, light)
        center(d, (x+50, 300, x+360, 370), kor, font(34, True), NAVY)
        center(d, (x+45, 390, x+365, 435), eng, font(22, True), accent)
        rr(d, (x+45, 465, x+365, 530), 18, '#F7F9FC')
        center(d, (x+60, 465, x+350, 530), symptom, font(25, True), DARK_GRAY)
        center(d, (x+45, 555, x+365, 665), action, font(25, True), NAVY, 10)

    rr(d, (235, 760, 1365, 840), 26, LIGHT_PURPLE, PURPLE, 3)
    center(d, (255, 760, 1345, 840), '실행이 멈췄는지, 실행 중 깨졌는지, 실행은 됐지만 값이 틀렸는지부터 구분한다.', font(29, True), NAVY)
    save(img, 'error-types-compare.jpg')


if __name__ == '__main__':
    image_warning_signal()
    image_debugging_loop()
    image_error_types()
    for p in sorted(OUT.glob('*.jpg')):
        print(f'{p}: {p.stat().st_size} bytes')
