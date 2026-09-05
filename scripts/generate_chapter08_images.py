from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path('images/chapter08')
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


def arrow(draw, x1, y1, x2, y2, color=BLUE, width=10):
    draw.line((x1, y1, x2-22, y2), fill=color, width=width)
    draw.polygon([(x2-22, y2-18), (x2, y2), (x2-22, y2+18)], fill=color)


def save(img, name):
    img.convert('RGB').save(OUT / name, 'JPEG', quality=88, optimize=True, progressive=True)


def title(draw, main, sub):
    draw.text((85, 55), main, font=font(60, True), fill=NAVY)
    draw.text((88, 138), sub, font=font(29), fill=GRAY)


def image_requirement_breakdown():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '긴 요구사항도 작은 논리 블록으로 나눌 수 있습니다', '코드를 쓰기 전에 문장에서 데이터·조건·결과를 먼저 분리합니다.')

    rr(d, (90, 225, 1510, 365), 30, WHITE, BLUE, 4)
    center(d, (120, 245, 1480, 345), '“출석률이 80% 이상이면서 점수가 80점 이상인 학생은 수료, 그렇지 않으면 보완 필요로 표시한다.”', font(31, True), NAVY)

    blocks = [
        ('데이터', '학생 정보\nscore / attendance', LIGHT_BLUE, BLUE),
        ('조건 1', '출석률 >= 80', LIGHT_GREEN, GREEN),
        ('조건 2', '점수 >= 80', LIGHT_YELLOW, YELLOW),
        ('결과', '수료 / 보완 필요', LIGHT_PURPLE, PURPLE),
    ]
    xs = [80, 455, 830, 1205]
    for i, ((label, body, light, accent), x) in enumerate(zip(blocks, xs)):
        rr(d, (x, 455, x+300, 690), 28, WHITE, accent, 4)
        rr(d, (x+55, 485, x+245, 545), 18, light)
        center(d, (x+65, 485, x+235, 545), label, font(28, True), NAVY)
        center(d, (x+25, 575, x+275, 655), body, font(27, True), NAVY, 10)
        if i < 3:
            arrow(d, x+305, 575, xs[i+1]-12, 575, PURPLE, 9)

    rr(d, (265, 760, 1335, 835), 26, '#EEF7FF')
    center(d, (285, 760, 1315, 835), '긴 문장은 어렵지만, 작은 논리 블록으로 나누면 구현 순서가 보입니다.', font(30, True), NAVY)
    save(img, 'requirement-breakdown.jpg')


def image_compound_condition_gates():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, 'AND 조건은 두 기준을 모두 통과해야 합니다', '출석률과 점수 중 하나만 만족하는 것이 아니라 두 조건이 모두 참이어야 수료입니다.')

    rr(d, (90, 325, 350, 560), 28, WHITE, BLUE, 4)
    center(d, (110, 345, 330, 405), '학생 카드', font(31, True), NAVY)
    center(d, (110, 425, 330, 535), '민수\n점수 85\n출석률 92%', font(27, True), NAVY, 10)

    arrow(d, 365, 445, 520, 445, PURPLE, 10)

    rr(d, (540, 300, 825, 595), 32, LIGHT_GREEN, GREEN, 5)
    center(d, (565, 325, 800, 390), 'Gate 1', font(31, True), GREEN)
    center(d, (565, 420, 800, 500), '출석률 >= 80', font(30, True), NAVY)
    rr(d, (610, 520, 755, 570), 18, WHITE)
    center(d, (620, 520, 745, 570), '92% → 통과', font(23, True), GREEN)

    arrow(d, 840, 445, 965, 445, PURPLE, 10)

    rr(d, (985, 300, 1270, 595), 32, LIGHT_YELLOW, YELLOW, 5)
    center(d, (1010, 325, 1245, 390), 'Gate 2', font(31, True), NAVY)
    center(d, (1010, 420, 1245, 500), '점수 >= 80', font(30, True), NAVY)
    rr(d, (1055, 520, 1200, 570), 18, WHITE)
    center(d, (1065, 520, 1190, 570), '85점 → 통과', font(23, True), GREEN)

    arrow(d, 1285, 445, 1380, 445, PURPLE, 10)
    rr(d, (1390, 350, 1535, 540), 28, LIGHT_PURPLE, PURPLE, 5)
    center(d, (1405, 380, 1520, 505), '수료\nPASS', font(31, True), PURPLE)

    rr(d, (260, 690, 1340, 830), 28, WHITE, RED, 3)
    center(d, (285, 705, 1315, 765), '하나라도 통과하지 못하면 → 보완 필요', font(30, True), RED)
    center(d, (285, 770, 1315, 815), 'AND = 조건 1도 참이고 조건 2도 참이어야 한다', font(27, True), NAVY)
    save(img, 'compound-condition-gates.jpg')


def image_tools_combined():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '지금까지 배운 도구가 하나의 프로그램으로 결합됩니다', '복합 문제는 새로운 문법보다 익숙한 도구들을 올바른 순서로 조합하는 문제입니다.')

    tools = [
        ('List', '여러 학생', LIGHT_BLUE, BLUE),
        ('Dict', '학생 한 명의 속성', LIGHT_GREEN, GREEN),
        ('for', '한 명씩 반복', LIGHT_YELLOW, YELLOW),
        ('if', '조건 판단', LIGHT_PINK, PINK),
        ('계산', '점수·출석률 확인', LIGHT_PURPLE, PURPLE),
    ]
    xs = [70, 350, 630, 910, 1190]
    for i, ((label, body, light, accent), x) in enumerate(zip(tools, xs)):
        rr(d, (x, 285, x+240, 475), 26, WHITE, accent, 4)
        rr(d, (x+48, 315, x+192, 370), 17, light)
        center(d, (x+55, 315, x+185, 370), label, font(27, True), NAVY)
        center(d, (x+20, 395, x+220, 450), body, font(22, True), NAVY)
        if i < 4:
            arrow(d, x+245, 380, xs[i+1]-10, 380, PURPLE, 8)

    rr(d, (260, 565, 1340, 730), 32, '#F3F8FF', BLUE, 4)
    center(d, (295, 585, 1305, 645), '하나의 프로그램', font(39, True), NAVY)
    center(d, (295, 655, 1305, 710), '여러 학생을 반복 → 각 학생의 데이터를 읽음 → 조건 판단 → 결과 저장/출력', font(28, True), NAVY)

    rr(d, (265, 785, 1335, 855), 24, LIGHT_GREEN)
    center(d, (285, 785, 1315, 855), '복합 문제 해결 = 익숙한 도구를 요구사항의 구조에 맞게 조합하는 일', font(29, True), NAVY)
    save(img, 'tools-combined-program.jpg')


if __name__ == '__main__':
    image_requirement_breakdown()
    image_compound_condition_gates()
    image_tools_combined()
    for p in sorted(OUT.glob('*.jpg')):
        print(f'{p}: {p.stat().st_size} bytes')
