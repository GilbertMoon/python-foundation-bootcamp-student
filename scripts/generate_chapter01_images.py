from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path('images/chapter01')
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
ORANGE = '#F19A52'
LIGHT_ORANGE = '#FFF0E2'
GRAY = '#5E6B78'
WHITE = '#FFFFFF'
RED = '#E45A67'

FONT_REG = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size=size)


def rr(draw, box, radius=26, fill=WHITE, outline=None, width=2):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def center(draw, box, text, fnt, fill=NAVY, spacing=6):
    x1, y1, x2, y2 = box
    bbox = draw.multiline_textbbox((0, 0), text, font=fnt, spacing=spacing, align='center')
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.multiline_text(((x1+x2-tw)/2, (y1+y2-th)/2), text, font=fnt, fill=fill, spacing=spacing, align='center')


def arrow_right(draw, x1, y, x2, color=BLUE, width=10):
    draw.line((x1, y, x2-22, y), fill=color, width=width)
    draw.polygon([(x2-22, y-16), (x2, y), (x2-22, y+16)], fill=color)


def arrow_left(draw, x1, y, x2, color=BLUE, width=10):
    draw.line((x1, y, x2+22, y), fill=color, width=width)
    draw.polygon([(x2+22, y-16), (x2, y), (x2+22, y+16)], fill=color)


def arrow_down(draw, x, y1, y2, color=BLUE, width=10):
    draw.line((x, y1, x, y2-22), fill=color, width=width)
    draw.polygon([(x-16, y2-22), (x+16, y2-22), (x, y2)], fill=color)


def save(img, name):
    img.convert('RGB').save(OUT / name, 'JPEG', quality=88, optimize=True, progressive=True)


def title(draw, main, sub):
    draw.text((85, 55), main, font=font(66, True), fill=NAVY)
    draw.text((88, 140), sub, font=font(32), fill=GRAY)


def image_two_approaches():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '문제를 보는 두 가지 방법', '코드를 먼저 쓰지 말고, 문제의 구조부터 찾습니다.')

    rr(d, (75, 235, 760, 760), 34, '#FFF7F7', RED, 4)
    rr(d, (840, 235, 1525, 760), 34, '#F4FFF9', GREEN, 4)

    center(d, (110, 265, 725, 330), '방법 A  |  문제 → 바로 코드', font(34, True), RED)
    center(d, (875, 265, 1490, 330), '방법 B  |  문제 → 구조 → 코드', font(34, True), GREEN)

    left_boxes = [
        ('문제', LIGHT_BLUE, BLUE, 360),
        ('바로 코드 작성', LIGHT_YELLOW, YELLOW, 475),
        ('막힘', LIGHT_PINK, RED, 590),
    ]
    for i, (label, fill, accent, y) in enumerate(left_boxes):
        rr(d, (210, y, 625, y+82), 24, fill, accent, 3)
        center(d, (225, y+4, 610, y+78), label, font(29, True), NAVY)
        if i < len(left_boxes)-1:
            arrow_down(d, 417, y+82, y+108, RED, 8)

    rr(d, (210, 690, 625, 738), 18, WHITE, RED, 2)
    center(d, (225, 692, 610, 736), '“어떤 문법을 써야 하지?”', font(25, True), RED)

    top = [
        ('문제', LIGHT_BLUE, BLUE, 870),
        ('데이터', LIGHT_GREEN, GREEN, 1080),
        ('반복', LIGHT_ORANGE, ORANGE, 1290),
    ]
    bottom = [
        ('코드', LIGHT_YELLOW, YELLOW, 870),
        ('결과', LIGHT_PURPLE, PURPLE, 1080),
        ('조건', LIGHT_PINK, PINK, 1290),
    ]
    bw, bh = 170, 82
    y1, y2 = 385, 560

    for label, fill, accent, x in top:
        rr(d, (x, y1, x+bw, y1+bh), 22, fill, accent, 3)
        center(d, (x+5, y1+4, x+bw-5, y1+bh-4), label, font(27, True), NAVY)
    arrow_right(d, 1045, y1+bh/2, 1070, GREEN, 8)
    arrow_right(d, 1255, y1+bh/2, 1280, GREEN, 8)
    arrow_down(d, 1375, y1+bh+8, y2-8, GREEN, 8)

    for label, fill, accent, x in bottom:
        rr(d, (x, y2, x+bw, y2+bh), 22, fill, accent, 3)
        center(d, (x+5, y2+4, x+bw-5, y2+bh-4), label, font(27, True), NAVY)
    arrow_left(d, 1280, y2+bh/2, 1260, GREEN, 8)
    arrow_left(d, 1070, y2+bh/2, 1050, GREEN, 8)

    rr(d, (300, 790, 1300, 855), 28, LIGHT_BLUE)
    center(d, (320, 790, 1280, 855), '핵심: 코드는 마지막에 작성합니다.', font(32, True), NAVY)
    save(img, 'problem-to-structure.jpg')


def image_same_structure():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '문제는 달라도 구조는 같습니다', '학생 성적 문제에서 익힌 생각을 쇼핑몰 주문 문제로 옮겨 봅니다.')

    # 왼쪽: 학생 성적 문제
    rr(d, (40, 215, 520, 760), 34, LIGHT_BLUE, BLUE, 4)
    center(d, (75, 238, 485, 300), '학생 성적 문제', font(38, True), BLUE)
    rr(d, (145, 318, 415, 365), 18, '#D7ECFF')
    center(d, (150, 320, 410, 362), '점수 데이터', font(25, True), NAVY)

    students = [('민수', '85점'), ('지영', '72점'), ('현우', '91점')]
    y = 390
    for name, score in students:
        rr(d, (78, y, 482, y+82), 22, WHITE, BLUE, 2)
        d.text((110, y+19), name, font=font(29, True), fill=NAVY)
        d.text((330, y+19), score, font=font(29, True), fill=NAVY)
        y += 105

    rr(d, (80, 700, 480, 742), 18, WHITE)
    center(d, (90, 701, 470, 741), '80점 이상 → 합격', font(25, True), RED)

    # 가운데: 가장 중요한 공통 구조
    rr(d, (555, 205, 1045, 770), 34, '#FBF9FF', PURPLE, 5)
    center(d, (590, 230, 1010, 302), '공통 구조', font(43, True), PURPLE)

    steps = [
        ('여러 대상', '반복할 대상들'),
        ('하나씩 확인', '반복'),
        ('조건 판단', '조건'),
        ('결과 표시', '결과'),
    ]
    sy = 335
    for i, (label, tag) in enumerate(steps):
        rr(d, (610, sy, 900, sy+78), 22, WHITE, PURPLE, 3)
        center(d, (625, sy+4, 885, sy+74), label, font(29, True), NAVY)
        rr(d, (918, sy+15, 1005, sy+63), 19, LIGHT_PURPLE)
        center(d, (922, sy+16, 1001, sy+62), tag, font(19, True), PURPLE)
        if i < len(steps)-1:
            arrow_down(d, 755, sy+78, sy+105, PURPLE, 8)
        sy += 105

    # 오른쪽: 쇼핑몰 주문 문제
    rr(d, (1080, 215, 1560, 760), 34, LIGHT_GREEN, GREEN, 4)
    center(d, (1110, 238, 1530, 300), '쇼핑몰 주문 문제', font(38, True), GREEN)
    rr(d, (1180, 318, 1460, 365), 18, '#D9F5E9')
    center(d, (1185, 320, 1455, 362), '주문 금액 데이터', font(24, True), NAVY)

    orders = [('민수', '45,000원'), ('지영', '72,000원'), ('현우', '53,000원')]
    y = 390
    for name, amount in orders:
        rr(d, (1118, y, 1522, y+82), 22, WHITE, GREEN, 2)
        d.text((1150, y+19), name, font=font(29, True), fill=NAVY)
        d.text((1320, y+19), amount, font=font(27, True), fill=NAVY)
        y += 105

    rr(d, (1120, 700, 1520, 742), 18, WHITE)
    center(d, (1130, 701, 1510, 741), '50,000원 이상 → 무료배송', font(23, True), RED)

    # 두 사례가 가운데 공통 구조로 수렴하도록 표현
    arrow_right(d, 520, 485, 552, BLUE, 10)
    arrow_left(d, 1080, 485, 1048, GREEN, 10)

    rr(d, (130, 800, 1470, 862), 28, LIGHT_YELLOW)
    center(
        d,
        (155, 800, 1445, 862),
        '소재가 바뀌어도 “반복 → 조건 판단 → 결과”라는 사고 구조는 그대로입니다.',
        font(30, True),
        NAVY,
    )
    save(img, 'same-structure-different-problem.jpg')


def image_sentence_breakdown():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '문제 문장을 구조로 해체하기', '긴 문장을 그대로 코드로 옮기지 말고, 먼저 필요한 요소를 찾습니다.')

    sentence = '여러 학생의 이름과 점수가 주어져 있습니다. 학생을 한 명씩 확인해서\n점수가 80점 이상이면 합격, 그렇지 않으면 불합격이라고 출력하세요.'
    rr(d, (90, 235, 1510, 365), 28, WHITE, BLUE, 3)
    center(d, (120, 245, 1480, 355), sentence, font(29, True), NAVY, spacing=10)

    items = [
        ('데이터', '학생 · 이름 · 점수', LIGHT_BLUE, BLUE),
        ('반복', '학생을 한 명씩 확인', LIGHT_ORANGE, ORANGE),
        ('조건', '점수 >= 80', LIGHT_PINK, PINK),
        ('결과', '합격 / 불합격 출력', LIGHT_GREEN, GREEN),
    ]
    x_positions = [90, 465, 840, 1215]
    for (label, body, fill, accent), x in zip(items, x_positions):
        rr(d, (x, 445, x+295, 680), 28, WHITE, accent, 4)
        rr(d, (x+30, 475, x+265, 535), 20, fill)
        center(d, (x+35, 478, x+260, 532), label, font(29, True), accent)
        center(d, (x+32, 555, x+263, 655), body, font(25, True), NAVY)

    d.line((800, 365, 800, 410), fill=PURPLE, width=7)
    d.line((237, 410, 1362, 410), fill=PURPLE, width=7)
    for x in (237, 612, 987, 1362):
        arrow_down(d, x, 410, 442, PURPLE, 7)

    rr(d, (260, 760, 1340, 840), 28, LIGHT_PURPLE)
    center(d, (285, 760, 1315, 840), '문장을 나누면 어떤 Python 도구가 필요한지 훨씬 쉽게 보입니다.', font(29, True), NAVY)
    save(img, 'problem-sentence-breakdown.jpg')


if __name__ == '__main__':
    image_two_approaches()
    image_same_structure()
    image_sentence_breakdown()
    print('Generated Chapter 01 JPG images:')
    for p in sorted(OUT.glob('*.jpg')):
        print(f'- {p} ({p.stat().st_size} bytes)')
