from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path('images/chapter06')
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
    draw.text((85, 55), main, font=font(62, True), fill=NAVY)
    draw.text((88, 138), sub, font=font(30), fill=GRAY)


def student_card(draw, x, y, name, score, accent=BLUE):
    rr(draw, (x, y, x+260, y+150), 24, WHITE, accent, 3)
    center(draw, (x+18, y+18, x+242, y+72), name, font(28, True), NAVY)
    rr(draw, (x+55, y+82, x+205, y+132), 18, LIGHT_BLUE if accent == BLUE else LIGHT_GREEN)
    center(draw, (x+60, y+82, x+200, y+132), f'{score}점', font(25, True), NAVY)


def image_sum_accumulation():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '합계는 반복하면서 누적됩니다', '새 점수를 만날 때마다 현재 합계에 더해 하나의 결과를 만들어 갑니다.')

    rr(d, (90, 230, 1510, 360), 30, LIGHT_BLUE, BLUE, 4)
    center(d, (110, 245, 1490, 345), '시작값 0  →  민수 +85  →  지영 +72  →  현우 +91', font(36, True), NAVY)

    steps = [
        ('시작', '0', '아직 아무 학생도 보지 않음'),
        ('민수', '85', '0 + 85 = 85'),
        ('지영', '157', '85 + 72 = 157'),
        ('현우', '248', '157 + 91 = 248'),
    ]
    colors = [(LIGHT_BLUE, BLUE), (LIGHT_GREEN, GREEN), (LIGHT_YELLOW, YELLOW), (LIGHT_PURPLE, PURPLE)]
    x_positions = [90, 460, 830, 1200]
    for i, ((label, total, desc), x) in enumerate(zip(steps, x_positions)):
        light, accent = colors[i]
        rr(d, (x, 445, x+300, 690), 28, WHITE, accent, 4)
        rr(d, (x+75, 470, x+225, 530), 20, light)
        center(d, (x+80, 470, x+220, 530), label, font(27, True), NAVY)
        center(d, (x+25, 545, x+275, 615), f'현재 합계 = {total}', font(28, True), NAVY)
        center(d, (x+25, 625, x+275, 675), desc, font(21), GRAY)
        if i < 3:
            arrow(d, x+305, 570, x_positions[i+1]-12, 570, PURPLE, 9)

    rr(d, (250, 755, 1350, 835), 26, '#EEF7FF')
    center(d, (270, 755, 1330, 835), '핵심 패턴: 초기값을 만들고 → 반복할 때마다 갱신하고 → 마지막 값을 결과로 사용한다', font(29, True), NAVY)
    save(img, 'sum-accumulation-flow.jpg')


def image_pass_counter():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '합격자 수는 조건을 통과할 때만 증가합니다', '모든 학생을 확인하지만, 카운터는 합격 조건을 만족한 학생에게만 +1 됩니다.')

    students = [('민수', 85, True), ('지영', 72, False), ('현우', 91, True)]
    xs = [100, 475, 850]
    for (name, score, passed), x in zip(students, xs):
        student_card(d, x, 300, name, score, GREEN if passed else RED)
        rr(d, (x+35, 485, x+225, 550), 20, LIGHT_GREEN if passed else LIGHT_RED, GREEN if passed else RED, 3)
        center(d, (x+45, 485, x+215, 550), '80점 이상? YES' if passed else '80점 이상? NO', font(23, True), GREEN if passed else RED)
        if passed:
            center(d, (x+25, 575, x+235, 630), '카운터 +1', font(27, True), NAVY)
        else:
            center(d, (x+25, 575, x+235, 630), '카운터 유지', font(27, True), GRAY)

    rr(d, (1240, 285, 1510, 660), 30, WHITE, PURPLE, 4)
    center(d, (1260, 310, 1490, 370), '합격자 수', font(32, True), NAVY)
    circles = [('0', 410), ('1', 500), ('1', 590), ('2', 680)]
    # draw compact timeline outside card lower area
    y = 410
    labels = [('시작', '0'), ('민수 후', '1'), ('지영 후', '1'), ('현우 후', '2')]
    for i, (label, value) in enumerate(labels):
        rr(d, (1265, y, 1485, y+62), 18, [LIGHT_BLUE, LIGHT_GREEN, LIGHT_YELLOW, LIGHT_PURPLE][i])
        center(d, (1275, y, 1475, y+62), f'{label}: {value}', font(22, True), NAVY)
        y += 72

    rr(d, (250, 745, 1350, 830), 26, '#EEF7FF')
    center(d, (270, 745, 1330, 830), '모든 데이터는 확인하지만, 조건을 통과한 데이터만 집계값을 바꿉니다.', font(30, True), NAVY)
    save(img, 'pass-counter-flow.jpg')


def image_aggregation_summary():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '여러 데이터를 하나의 요약값으로 줄일 수 있습니다', '학생 여러 명의 점수를 반복 처리하면 합계·개수·평균·최댓값 같은 집계 결과를 만들 수 있습니다.')

    student_card(d, 90, 300, '민수', 85, BLUE)
    student_card(d, 90, 490, '지영', 72, YELLOW)
    student_card(d, 90, 680, '현우', 91, PURPLE)

    rr(d, (470, 355, 760, 690), 32, LIGHT_BLUE, BLUE, 4)
    center(d, (495, 380, 735, 450), '반복 처리', font(38, True), NAVY)
    center(d, (500, 485, 730, 645), '점수를 하나씩 읽고\n필요한 값을\n계속 갱신한다', font(29, True), NAVY, 12)
    arrow(d, 365, 515, 455, 515, PURPLE, 10)
    arrow(d, 775, 515, 875, 515, PURPLE, 10)

    cards = [
        ('SUM', '248', '점수 합계', LIGHT_GREEN, GREEN),
        ('COUNT', '3', '학생 수', LIGHT_BLUE, BLUE),
        ('AVG', '82.7', '평균 점수', LIGHT_YELLOW, YELLOW),
        ('MAX', '91', '최고 점수', LIGHT_PURPLE, PURPLE),
    ]
    positions = [(900, 285), (1210, 285), (900, 545), (1210, 545)]
    for (label, value, desc, light, accent), (x, y) in zip(cards, positions):
        rr(d, (x, y, x+260, y+200), 26, WHITE, accent, 4)
        rr(d, (x+55, y+25, x+205, y+80), 18, light)
        center(d, (x+60, y+25, x+200, y+80), label, font(26, True), NAVY)
        center(d, (x+25, y+92, x+235, y+142), value, font(38, True), NAVY)
        center(d, (x+30, y+150, x+230, y+187), desc, font(22), GRAY)

    rr(d, (335, 795, 1265, 860), 22, LIGHT_GREEN)
    center(d, (350, 795, 1250, 860), '이 사고는 이후 SQL의 SUM / COUNT / AVG / MAX와 그대로 연결됩니다.', font(28, True), NAVY)
    save(img, 'aggregation-summary.jpg')


if __name__ == '__main__':
    image_sum_accumulation()
    image_pass_counter()
    image_aggregation_summary()
    for p in sorted(OUT.glob('*.jpg')):
        print(f'{p}: {p.stat().st_size} bytes')
