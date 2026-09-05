from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path('images/chapter03')
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


def title(draw, main, sub):
    draw.text((85, 55), main, font=font(66, True), fill=NAVY)
    draw.text((88, 140), sub, font=font(32), fill=GRAY)


def save(img, name):
    img.convert('RGB').save(OUT / name, 'JPEG', quality=88, optimize=True, progressive=True)


def image_score_boundary_line():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '조건의 핵심은 경계값입니다', '79, 80, 89, 90, 91처럼 결과가 바뀌는 숫자를 먼저 확인합니다.')

    # category bands
    rr(d, (120, 250, 580, 390), 28, LIGHT_PINK, PINK, 3)
    rr(d, (580, 250, 1080, 390), 28, LIGHT_GREEN, GREEN, 3)
    rr(d, (1080, 250, 1480, 390), 28, LIGHT_PURPLE, PURPLE, 3)
    center(d, (135, 265, 565, 375), '보완 필요\n80점 미만', font(34, True), NAVY)
    center(d, (595, 265, 1065, 375), '합격\n80점 이상 90점 미만', font(31, True), NAVY)
    center(d, (1095, 265, 1465, 375), '우수\n90점 이상', font(34, True), NAVY)

    # number line
    y = 585
    d.line((140, y, 1460, y), fill=NAVY, width=10)
    d.polygon([(1460, y), (1425, y-20), (1425, y+20)], fill=NAVY)

    points = [(79, 430), (80, 650), (89, 950), (90, 1180), (91, 1370)]
    for value, x in points:
        accent = PINK if value < 80 else (GREEN if value < 90 else PURPLE)
        d.line((x, y-34, x, y+34), fill=accent, width=8)
        d.ellipse((x-24, y-24, x+24, y+24), fill=accent)
        center(d, (x-80, y+45, x+80, y+105), str(value), font(34, True), accent)

    # boundary callouts
    rr(d, (560, 450, 745, 525), 20, LIGHT_BLUE, BLUE, 2)
    center(d, (570, 450, 735, 525), '80 경계', font(27, True), NAVY)
    d.line((650, 525, 650, 555), fill=BLUE, width=6)

    rr(d, (1090, 450, 1270, 525), 20, LIGHT_YELLOW, YELLOW, 2)
    center(d, (1100, 450, 1260, 525), '90 경계', font(27, True), NAVY)
    d.line((1180, 525, 1180, 555), fill=YELLOW, width=6)

    rr(d, (270, 735, 1330, 830), 28, WHITE, BLUE, 3)
    center(d, (295, 745, 1305, 820), '“80점은 어느 쪽인가?”를 정확히 말할 수 있어야 조건이 정확해집니다.', font(30, True), NAVY)
    save(img, 'score-boundary-line.jpg')


def image_condition_decision_flow():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '조건 판단은 위에서 아래로 진행됩니다', '점수 하나가 여러 조건을 통과하면서 최종 결과를 결정합니다.')

    # student card
    rr(d, (90, 285, 390, 690), 30, WHITE, BLUE, 4)
    center(d, (115, 310, 365, 380), '학생 카드', font(34, True), NAVY)
    rr(d, (135, 410, 345, 485), 18, LIGHT_BLUE)
    center(d, (145, 410, 335, 485), '이름: 현우', font(28, True), NAVY)
    rr(d, (135, 510, 345, 610), 18, LIGHT_YELLOW)
    center(d, (145, 510, 335, 610), '점수: 91', font(34, True), NAVY)

    # arrows and decisions
    d.line((390, 490, 530, 490), fill=BLUE, width=12)
    d.polygon([(530, 490), (505, 472), (505, 508)], fill=BLUE)

    rr(d, (530, 265, 870, 430), 30, LIGHT_PURPLE, PURPLE, 4)
    center(d, (550, 280, 850, 415), 'score >= 90 ?\n\nYES → 우수', font(34, True), NAVY)

    rr(d, (530, 525, 870, 690), 30, LIGHT_GREEN, GREEN, 4)
    center(d, (550, 540, 850, 675), 'score >= 80 ?\n\nYES → 합격', font(34, True), NAVY)

    # first decision branches
    d.line((870, 345, 1060, 345), fill=PURPLE, width=12)
    d.polygon([(1060, 345), (1035, 327), (1035, 363)], fill=PURPLE)
    rr(d, (1060, 275, 1430, 420), 28, WHITE, PURPLE, 4)
    center(d, (1080, 290, 1410, 405), '91 >= 90\nTrue\n→ 우수', font(36, True), PURPLE)

    # no branch down
    d.line((700, 430, 700, 525), fill=GRAY, width=10)
    d.polygon([(700, 525), (682, 500), (718, 500)], fill=GRAY)
    d.text((725, 455), 'NO', font=font(24, True), fill=GRAY)

    # second decision branch and else
    d.line((870, 610, 1060, 610), fill=GREEN, width=12)
    d.polygon([(1060, 610), (1035, 592), (1035, 628)], fill=GREEN)
    rr(d, (1060, 535, 1430, 680), 28, WHITE, GREEN, 4)
    center(d, (1080, 550, 1410, 665), '80 이상이면\n→ 합격\n그 외 → 보완 필요', font(31, True), NAVY)

    rr(d, (280, 760, 1320, 835), 24, LIGHT_BLUE)
    center(d, (300, 760, 1300, 835), '중요: 앞 조건에서 결정되면 아래 조건은 더 이상 검사하지 않습니다.', font(29, True), NAVY)
    save(img, 'condition-decision-flow.jpg')


def image_condition_order_compare():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '조건의 순서가 결과를 바꿉니다', '넓은 조건을 먼저 검사하면 더 구체적인 조건에 도달하지 못할 수 있습니다.')

    rr(d, (75, 235, 760, 790), 30, '#FFF1F1', RED, 4)
    rr(d, (840, 235, 1525, 790), 30, '#F0FBF5', GREEN, 4)
    center(d, (95, 250, 740, 315), '잘못된 순서 ✕', font(36, True), RED)
    center(d, (860, 250, 1505, 315), '올바른 순서 ✓', font(36, True), GREEN)

    # left code blocks
    rr(d, (135, 350, 700, 470), 20, WHITE, RED, 3)
    center(d, (155, 360, 680, 460), 'if score >= 80:\n    result = "합격"', font(27, True), NAVY)
    rr(d, (135, 500, 700, 620), 20, WHITE, RED, 3)
    center(d, (155, 510, 680, 610), 'elif score >= 90:\n    result = "우수"', font(27, True), NAVY)
    rr(d, (175, 655, 660, 750), 20, LIGHT_RED)
    center(d, (190, 665, 645, 740), '91점도 첫 조건에서 True\n→ “합격”으로 끝남', font(28, True), RED)

    # right code blocks
    rr(d, (900, 350, 1465, 470), 20, WHITE, GREEN, 3)
    center(d, (920, 360, 1445, 460), 'if score >= 90:\n    result = "우수"', font(27, True), NAVY)
    rr(d, (900, 500, 1465, 620), 20, WHITE, GREEN, 3)
    center(d, (920, 510, 1445, 610), 'elif score >= 80:\n    result = "합격"', font(27, True), NAVY)
    rr(d, (940, 655, 1425, 750), 20, LIGHT_GREEN)
    center(d, (955, 665, 1410, 740), '91점은 먼저 90 이상 검사\n→ “우수”로 정확히 분류', font(28, True), GREEN)

    rr(d, (320, 815, 1280, 875), 22, LIGHT_YELLOW)
    center(d, (340, 815, 1260, 875), '조건이 겹치면 더 구체적이고 높은 기준부터 검사합니다.', font(28, True), NAVY)
    save(img, 'condition-order-compare.jpg')


if __name__ == '__main__':
    image_score_boundary_line()
    image_condition_decision_flow()
    image_condition_order_compare()
    for p in sorted(OUT.glob('*.jpg')):
        print(f'{p}: {p.stat().st_size} bytes')
