from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path('images/chapter02')
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
    tw, th = b[2]-b[0], b[3]-b[1]
    draw.multiline_text(((x1+x2-tw)/2, (y1+y2-th)/2), text, font=fnt, fill=fill, spacing=spacing, align='center')


def arrow(draw, x1, y1, x2, y2, color=BLUE, width=12):
    draw.line((x1, y1, x2-22, y2), fill=color, width=width)
    draw.polygon([(x2-22, y2-18), (x2, y2), (x2-22, y2+18)], fill=color)


def save(img, name):
    img.convert('RGB').save(OUT / name, 'JPEG', quality=88, optimize=True, progressive=True)


def title(draw, main, sub):
    draw.text((85, 55), main, font=font(66, True), fill=NAVY)
    draw.text((88, 140), sub, font=font(32), fill=GRAY)


def image_problem_breakdown():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '큰 문제를 작은 단계로 나누기', '“학생 성적 처리”도 한 번에 하지 않고, 실행 가능한 작은 단계로 나눕니다.')

    rr(d, (120, 235, 1480, 355), 32, LIGHT_BLUE, BLUE, 4)
    center(d, (140, 245, 1460, 345), '큰 문제: 학생들의 점수를 확인하고 합격 여부를 출력하라', font(38, True), NAVY)

    steps = [
        ('1', '데이터 준비', '학생 목록을 준비'),
        ('2', '학생 선택', '한 명씩 꺼내기'),
        ('3', '점수 확인', '현재 학생 점수 보기'),
        ('4', '합격 판단', '80점 이상인가?'),
        ('5', '결과 출력', '합격/불합격 표시'),
    ]
    colors = [(LIGHT_BLUE, BLUE), (LIGHT_GREEN, GREEN), (LIGHT_YELLOW, YELLOW), (LIGHT_PINK, PINK), (LIGHT_PURPLE, PURPLE)]
    x = 70
    box_w = 250
    gap = 55
    for i, (num, head, body) in enumerate(steps):
        light, accent = colors[i]
        rr(d, (x, 455, x+box_w, 700), 28, WHITE, accent, 4)
        d.ellipse((x+85, 475, x+165, 555), fill=accent)
        center(d, (x+85, 475, x+165, 555), num, font(32, True), WHITE)
        center(d, (x+20, 565, x+box_w-20, 620), head, font(29, True), NAVY)
        rr(d, (x+24, 635, x+box_w-24, 680), 18, light)
        center(d, (x+30, 635, x+box_w-30, 680), body, font(21, True), NAVY)
        if i < len(steps)-1:
            arrow(d, x+box_w+8, 575, x+box_w+gap-8, 575)
        x += box_w + gap

    rr(d, (300, 760, 1300, 835), 28, '#EEF7FF')
    center(d, (320, 760, 1280, 835), '큰 문제도 작은 단계로 나누면 “무엇부터 해야 할지”가 보입니다.', font(30, True), NAVY)
    save(img, 'problem-step-breakdown.jpg')


def image_korean_to_code():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '한국어 절차를 Python 코드로 옮기기', '먼저 사람의 말로 순서를 정한 뒤, 각 단계를 코드 한 조각씩 대응시킵니다.')

    left_x1, left_x2 = 90, 720
    right_x1, right_x2 = 880, 1510
    rr(d, (left_x1, 230, left_x2, 790), 30, '#FFFDF5', YELLOW, 4)
    rr(d, (right_x1, 230, right_x2, 790), 30, '#F3F8FF', BLUE, 4)
    center(d, (left_x1, 245, left_x2, 315), '사람의 말', font(36, True), NAVY)
    center(d, (right_x1, 245, right_x2, 315), 'Python 코드', font(36, True), NAVY)

    pairs = [
        ('학생을 한 명씩 꺼낸다', 'for student in students:'),
        ('이름을 확인한다', 'name = student["name"]'),
        ('점수를 확인한다', 'score = student["score"]'),
        ('80점 이상인지 판단한다', 'if score >= 80:'),
        ('결과를 출력한다', 'print(name, score, result)'),
    ]
    y = 335
    for idx, (human, code) in enumerate(pairs):
        light = [LIGHT_BLUE, LIGHT_GREEN, LIGHT_YELLOW, LIGHT_PINK, LIGHT_PURPLE][idx]
        rr(d, (130, y, 680, y+75), 20, light)
        center(d, (145, y, 665, y+75), human, font(26, True), NAVY)
        arrow(d, 735, y+38, 855, y+38, PURPLE, 10)
        rr(d, (920, y, 1470, y+75), 20, WHITE, BLUE, 2)
        center(d, (935, y, 1455, y+75), code, font(22, True), NAVY)
        y += 92

    rr(d, (310, 820, 1290, 875), 20, LIGHT_GREEN)
    center(d, (325, 820, 1275, 875), '코드는 갑자기 떠올리는 것이 아니라, 정리한 절차를 번역하는 것입니다.', font(27, True), NAVY)
    save(img, 'procedure-to-code.jpg')


def image_order_matters():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '프로그래밍에서는 순서가 중요합니다', '같은 일을 하더라도 필요한 정보를 먼저 준비하지 않으면 다음 단계로 갈 수 없습니다.')

    rr(d, (80, 240, 765, 785), 30, '#F1FBF6', GREEN, 4)
    rr(d, (835, 240, 1520, 785), 30, '#FFF2F2', RED, 4)
    center(d, (100, 255, 745, 320), '올바른 순서 ✓', font(36, True), GREEN)
    center(d, (855, 255, 1500, 320), '잘못된 순서 ✕', font(36, True), RED)

    good = ['학생 선택', '점수 확인', '80점 이상인지 판단', '결과 출력']
    bad = ['학생 선택', '80점 이상인지 판단', '점수 확인', '결과 출력']

    def flow(x1, x2, items, bad_idx=None):
        y = 355
        for i, item in enumerate(items):
            if i == bad_idx:
                fill, outline = LIGHT_RED, RED
            else:
                fill, outline = WHITE, BLUE
            rr(d, (x1+95, y, x2-95, y+72), 22, fill, outline, 3)
            center(d, (x1+110, y, x2-110, y+72), item, font(27, True), NAVY)
            if i < len(items)-1:
                d.line(((x1+x2)//2, y+72, (x1+x2)//2, y+105), fill=GRAY, width=8)
                d.polygon([((x1+x2)//2-14, y+93), ((x1+x2)//2+14, y+93), ((x1+x2)//2, y+110)], fill=GRAY)
            y += 108

    flow(80, 765, good)
    flow(835, 1520, bad, 1)

    center(d, (905, 680, 1450, 760), '점수를 아직 확인하지 않았는데\n무엇을 기준으로 판단할까요?', font(26, True), RED)
    rr(d, (300, 810, 1300, 870), 22, LIGHT_BLUE)
    center(d, (320, 810, 1280, 870), '프로그래밍 = 컴퓨터가 따라갈 수 있도록 정확한 순서를 만드는 일', font(28, True), NAVY)
    save(img, 'why-order-matters.jpg')


if __name__ == '__main__':
    image_problem_breakdown()
    image_korean_to_code()
    image_order_matters()
    for p in sorted(OUT.glob('*.jpg')):
        print(f'{p}: {p.stat().st_size} bytes')
