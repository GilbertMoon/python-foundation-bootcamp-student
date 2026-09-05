from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path('images/chapter05')
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
LIGHT_GRAY = '#EEF2F6'
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


def arrow(draw, x1, y1, x2, y2, color=BLUE, width=11):
    draw.line((x1, y1, x2-22, y2), fill=color, width=width)
    draw.polygon([(x2-22, y2-18), (x2, y2), (x2-22, y2+18)], fill=color)


def down_arrow(draw, x, y1, y2, color=BLUE, width=10):
    draw.line((x, y1, x, y2-20), fill=color, width=width)
    draw.polygon([(x-16, y2-20), (x+16, y2-20), (x, y2)], fill=color)


def save(img, name):
    img.convert('RGB').save(OUT / name, 'JPEG', quality=88, optimize=True, progressive=True)


def title(draw, main, sub):
    draw.text((85, 55), main, font=font(62, True), fill=NAVY)
    draw.text((88, 137), sub, font=font(29), fill=GRAY)


def student_card(draw, box, name, score, accent=BLUE, selected=False):
    x1, y1, x2, y2 = box
    fill = LIGHT_GREEN if selected else WHITE
    outline = GREEN if selected else accent
    rr(draw, box, 25, fill, outline, 4)
    draw.ellipse((x1+20, y1+22, x1+78, y1+80), fill=accent)
    center(draw, (x1+90, y1+15, x2-15, y1+58), name, font(27, True), NAVY)
    center(draw, (x1+90, y1+56, x2-15, y1+100), f'{score}점', font(24, True), accent)
    if selected:
        rr(draw, (x1+30, y2-55, x2-30, y2-15), 15, LIGHT_GREEN)
        center(draw, (x1+35, y2-55, x2-35, y2-15), '선택됨', font(20, True), GREEN)


def image_student_filter():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '모두 확인하고, 조건에 맞는 것만 남긴다', '필터링은 일부 데이터만 보는 것이 아니라 전체를 확인한 뒤 필요한 데이터만 선택하는 과정입니다.')

    rr(d, (70, 225, 520, 760), 30, '#F4F8FC', BLUE, 4)
    center(d, (100, 245, 490, 305), '전체 학생', font(34, True), NAVY)
    student_card(d, (125, 330, 465, 455), '민수', 85, BLUE)
    student_card(d, (125, 480, 465, 605), '지영', 72, YELLOW)
    student_card(d, (125, 630, 465, 755), '현우', 91, PURPLE)

    # filter funnel
    d.polygon([(650, 330), (980, 330), (890, 500), (850, 500), (850, 660), (780, 660), (780, 500), (740, 500)], fill=LIGHT_BLUE, outline=BLUE)
    center(d, (670, 350, 960, 445), '필터', font(40, True), NAVY)
    center(d, (700, 445, 930, 520), 'score >= 80', font(27, True), BLUE)
    arrow(d, 530, 500, 650, 500, PURPLE, 12)

    rr(d, (1060, 225, 1530, 760), 30, '#F1FBF6', GREEN, 4)
    center(d, (1090, 245, 1500, 305), '조건을 통과한 결과', font(34, True), NAVY)
    student_card(d, (1125, 365, 1470, 500), '민수', 85, GREEN, True)
    student_card(d, (1125, 545, 1470, 680), '현우', 91, GREEN, True)
    arrow(d, 920, 500, 1050, 500, GREEN, 12)

    rr(d, (310, 790, 1290, 860), 22, LIGHT_YELLOW)
    center(d, (330, 790, 1270, 860), '지영도 확인은 하지만, 조건을 통과하지 않으므로 결과에는 포함되지 않습니다.', font(27, True), NAVY)
    save(img, 'student-filter-flow.jpg')


def image_loop_condition_flow():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '반복 + 조건 = 필터링', '모든 항목을 한 번씩 확인하고, 현재 항목이 조건을 만족할 때만 선택합니다.')

    boxes = [
        (110, 300, 390, 420, '학생 목록', LIGHT_BLUE, BLUE),
        (500, 300, 780, 420, '한 명 꺼내기', LIGHT_PURPLE, PURPLE),
        (890, 285, 1190, 435, '80점 이상?', LIGHT_YELLOW, YELLOW),
    ]
    for x1, y1, x2, y2, text, fill, outline in boxes:
        rr(d, (x1, y1, x2, y2), 28, fill, outline, 4)
        center(d, (x1+15, y1+10, x2-15, y2-10), text, font(31, True), NAVY)
    arrow(d, 400, 360, 490, 360)
    arrow(d, 790, 360, 880, 360)

    rr(d, (1290, 220, 1510, 340), 26, LIGHT_GREEN, GREEN, 4)
    center(d, (1305, 230, 1495, 330), 'YES\n선택', font(30, True), GREEN)
    rr(d, (1290, 465, 1510, 585), 26, LIGHT_RED, RED, 4)
    center(d, (1305, 475, 1495, 575), 'NO\n통과', font(30, True), RED)
    arrow(d, 1200, 330, 1280, 285, GREEN, 10)
    arrow(d, 1200, 395, 1280, 525, RED, 10)

    rr(d, (450, 610, 1190, 725), 28, WHITE, BLUE, 4)
    center(d, (470, 625, 1170, 710), '다음 학생이 있으면 다시 “한 명 꺼내기”로 돌아간다', font(30, True), NAVY)
    down_arrow(d, 1400, 600, 670, GRAY, 8)
    d.line((1400, 670, 1210, 670), fill=GRAY, width=8)
    d.polygon([(1210, 670), (1235, 654), (1235, 686)], fill=GRAY)

    rr(d, (285, 775, 1315, 850), 24, LIGHT_GREEN)
    center(d, (305, 775, 1295, 850), '핵심 패턴: 모두 확인한다 → 각 데이터를 판단한다 → 필요한 것만 선택한다', font(29, True), NAVY)
    save(img, 'loop-condition-filter.jpg')


def image_future_filtering_bridge():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '같은 필터링 사고는 이후에도 계속 사용됩니다', '문법은 달라져도 “조건에 맞는 데이터만 선택한다”는 문제 구조는 같습니다.')

    cards = [
        ('Python', 'for + if', '한 명씩 확인\n→ 조건 통과 시 선택', LIGHT_BLUE, BLUE),
        ('SQL', 'WHERE', '행을 확인\n→ 조건에 맞는 행 선택', LIGHT_GREEN, GREEN),
        ('pandas', 'boolean filtering', '데이터를 비교\n→ True인 행 선택', LIGHT_PURPLE, PURPLE),
    ]
    xs = [90, 590, 1090]
    for i, (name, keyword, body, fill, accent) in enumerate(cards):
        x = xs[i]
        rr(d, (x, 270, x+420, 680), 32, WHITE, accent, 4)
        rr(d, (x+35, 305, x+385, 375), 22, fill)
        center(d, (x+45, 305, x+375, 375), name, font(35, True), NAVY)
        center(d, (x+45, 415, x+375, 480), keyword, font(32, True), accent)
        center(d, (x+45, 520, x+375, 625), body, font(25, True), NAVY)
        if i < 2:
            arrow(d, x+430, 475, xs[i+1]-10, 475, GRAY, 8)

    rr(d, (230, 735, 1370, 835), 28, LIGHT_YELLOW)
    center(d, (250, 745, 1350, 825), 'Python에서 익힌 “필터링” 사고가 SQL과 데이터 분석으로 그대로 이어집니다.', font(31, True), NAVY)
    save(img, 'filtering-future-bridge.jpg')


if __name__ == '__main__':
    image_student_filter()
    image_loop_condition_flow()
    image_future_filtering_bridge()
    for p in sorted(OUT.glob('*.jpg')):
        print(f'{p}: {p.stat().st_size} bytes')
