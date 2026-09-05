from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path('images/chapter09')
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
PURPLE = '#9A8CE0'
LIGHT_PURPLE = '#F0EDFF'
PINK = '#F18E9D'
LIGHT_PINK = '#FFE9ED'
GRAY = '#5E6B78'
WHITE = '#FFFFFF'
RED = '#E45D5D'
LIGHT_RED = '#FFEAEA'

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


def title(draw, main, sub):
    draw.text((85, 55), main, font=font(60, True), fill=NAVY)
    draw.text((88, 138), sub, font=font(29), fill=GRAY)


def save(img, name):
    img.convert('RGB').save(OUT / name, 'JPEG', quality=88, optimize=True, progressive=True)


def image_task_decomposition():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '큰 문제는 작은 역할로 나누면 쉬워집니다', '학생 성적 처리라는 큰 업무를 서로 다른 책임을 가진 작은 기능으로 분리합니다.')

    rr(d, (100, 300, 470, 610), 34, WHITE, BLUE, 5)
    center(d, (125, 330, 445, 415), '학생 성적 처리', font(38, True), NAVY)
    center(d, (135, 440, 435, 560), '한 덩어리로 보면\n복잡하고 길어 보임', font(27), GRAY, 10)

    arrow(d, 500, 455, 650, 455, PURPLE, 12)

    blocks = [
        ('합격 판단', 'score → 합격/불합격', LIGHT_GREEN, GREEN),
        ('등급 판단', 'score → A/B/C', LIGHT_YELLOW, YELLOW),
        ('평균 계산', 'students → 평균', LIGHT_PURPLE, PURPLE),
        ('결과 출력', '데이터 → 화면 표시', LIGHT_PINK, PINK),
    ]
    pos = [(720, 270), (1120, 270), (720, 520), (1120, 520)]
    for (name, desc, light, accent), (x, y) in zip(blocks, pos):
        rr(d, (x, y, x+320, y+180), 28, WHITE, accent, 4)
        rr(d, (x+45, y+30, x+275, y+90), 18, light)
        center(d, (x+55, y+30, x+265, y+90), name, font(28, True), NAVY)
        center(d, (x+30, y+105, x+290, y+160), desc, font(22), GRAY)

    rr(d, (250, 770, 1350, 845), 26, LIGHT_BLUE)
    center(d, (270, 770, 1330, 845), '핵심: 함수는 코드를 묶는 문법이 아니라, 큰 문제를 작은 책임으로 나누는 도구입니다.', font(30, True), NAVY)
    save(img, 'task-decomposition.jpg')


def image_code_to_functions():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '긴 코드에 먼저 역할 이름을 붙여 봅니다', 'Before의 한 덩어리 코드를 After의 이름 있는 기능 블록으로 정리합니다.')

    rr(d, (90, 245, 650, 735), 30, WHITE, RED, 4)
    center(d, (120, 265, 620, 325), 'BEFORE · 한 덩어리 코드', font(31, True), RED)
    lines = [
        'for student in students:',
        '  score = student["score"]',
        '  if score >= 80: ...',
        '  if score >= 90: ...',
        '  total += score',
        '  print(...)',
        '...',
        '역할이 섞여 있음'
    ]
    y = 365
    for i, line in enumerate(lines):
        fill = NAVY if i < 7 else RED
        d.text((145, y), line, font=font(25, i == 7), fill=fill)
        y += 48

    arrow(d, 685, 490, 835, 490, PURPLE, 12)

    rr(d, (870, 245, 1510, 735), 30, WHITE, GREEN, 4)
    center(d, (900, 265, 1480, 325), 'AFTER · 역할별 함수 블록', font(31, True), GREEN)
    funcs = [
        ('get_result(score)', '합격 여부 판단', LIGHT_GREEN, GREEN),
        ('get_grade(score)', '등급 판단', LIGHT_YELLOW, YELLOW),
        ('calculate_average(students)', '평균 계산', LIGHT_PURPLE, PURPLE),
        ('print_result(...)', '결과 출력', LIGHT_PINK, PINK),
    ]
    y = 365
    for fname, role, light, accent in funcs:
        rr(d, (940, y, 1440, y+72), 18, light, accent, 3)
        d.text((965, y+11), fname, font=font(23, True), fill=NAVY)
        d.text((1205, y+14), role, font=font(20), fill=GRAY)
        y += 88

    rr(d, (250, 780, 1350, 845), 24, '#EEF7FF')
    center(d, (270, 780, 1330, 845), '코드를 함수로 바꾸기 전에 “이 부분은 무슨 일을 하는가?”부터 이름 붙입니다.', font(29, True), NAVY)
    save(img, 'code-to-function-blocks.jpg')


def image_responsibility_cards():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '좋은 함수는 입력 · 하는 일 · 결과가 분명합니다', '함수의 모양보다 한 가지 책임에 집중하는지가 더 중요합니다.')

    cards = [
        ('get_result(score)', '입력\nscore', '하는 일\n80점 기준 판단', '결과\n"합격" / "불합격"', GREEN, LIGHT_GREEN),
        ('get_grade(score)', '입력\nscore', '하는 일\n등급 기준 판단', '결과\n"A" / "B" / "C"', YELLOW, LIGHT_YELLOW),
        ('calculate_average(students)', '입력\nstudents', '하는 일\n점수 합계와 개수 계산', '결과\n평균 점수', PURPLE, LIGHT_PURPLE),
    ]
    xs = [85, 555, 1025]
    for (fname, inp, work, result, accent, light), x in zip(cards, xs):
        rr(d, (x, 270, x+410, 700), 30, WHITE, accent, 4)
        rr(d, (x+25, 295, x+385, 365), 18, light)
        center(d, (x+35, 295, x+375, 365), fname, font(25, True), NAVY)

        sections = [(inp, 400, LIGHT_BLUE), (work, 500, '#F7F9FC'), (result, 600, light)]
        for text, y, fill in sections:
            rr(d, (x+40, y, x+370, y+75), 18, fill)
            center(d, (x+55, y, x+355, y+75), text, font(22, True), NAVY, 4)

    rr(d, (260, 760, 1340, 840), 26, LIGHT_BLUE)
    center(d, (280, 760, 1320, 840), '한 함수 = 한 가지 책임 · 이름만 읽어도 역할이 보여야 합니다.', font(31, True), NAVY)
    save(img, 'function-responsibility-cards.jpg')


if __name__ == '__main__':
    image_task_decomposition()
    image_code_to_functions()
    image_responsibility_cards()
    for p in sorted(OUT.glob('*.jpg')):
        print(f'{p}: {p.stat().st_size} bytes')
