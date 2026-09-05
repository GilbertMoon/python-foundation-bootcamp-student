from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path('images/chapter04')
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


def title(draw, main, sub):
    draw.text((85, 55), main, font=font(66, True), fill=NAVY)
    draw.text((88, 140), sub, font=font(31), fill=GRAY)


def save(img, name):
    img.convert('RGB').save(OUT / name, 'JPEG', quality=88, optimize=True, progressive=True)


def student_card(draw, x, y, name, score, accent=BLUE, active=False):
    fill = LIGHT_YELLOW if active else WHITE
    width = 5 if active else 3
    rr(draw, (x, y, x+215, y+150), 24, fill, accent, width)
    center(draw, (x+15, y+15, x+200, y+62), name, font(27, True), NAVY)
    center(draw, (x+15, y+66, x+200, y+125), f'score: {score}', font(24, True), accent)


def image_manual_vs_loop():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '수작업 100회 vs 반복 처리', '같은 작업이 여러 대상에게 반복된다면, 반복되는 패턴부터 찾아야 합니다.')

    rr(d, (70, 235, 760, 790), 32, '#FFF3F3', RED, 4)
    rr(d, (840, 235, 1530, 790), 32, '#F1FBF6', GREEN, 4)
    center(d, (95, 250, 735, 315), '수작업 방식', font(36, True), RED)
    center(d, (865, 250, 1505, 315), '반복 처리 방식', font(36, True), GREEN)

    # left: repeated code-like rows
    y = 350
    for i, name in enumerate(['민수', '지영', '현우', '...', '100번째 학생']):
        rr(d, (125, y, 705, y+65), 18, WHITE, RED if i < 3 else GRAY, 2)
        center(d, (140, y, 690, y+65), f'{name} 점수 확인 → 판단 → 출력', font(24, True), NAVY)
        y += 80
    center(d, (140, 715, 690, 765), '같은 코드를 계속 다시 작성', font(25, True), RED)

    # right: cards through one processor
    student_card(d, 880, 390, '민수', '85', BLUE)
    student_card(d, 880, 570, '지영', '72', PINK)
    arrow(d, 1110, 465, 1230, 465, GREEN)
    arrow(d, 1110, 645, 1230, 645, GREEN)
    rr(d, (1235, 360, 1480, 690), 28, WHITE, GREEN, 4)
    center(d, (1260, 385, 1455, 455), '하나의 처리', font(30, True), NAVY)
    center(d, (1260, 470, 1455, 635), '점수 확인\n↓\n조건 판단\n↓\n결과 출력', font(27, True), GREEN)
    center(d, (890, 715, 1480, 765), '여러 학생이 같은 처리 과정을 통과', font(25, True), GREEN)

    rr(d, (280, 815, 1320, 875), 22, LIGHT_BLUE)
    center(d, (300, 815, 1300, 875), '핵심 질문: “여러 대상에게 똑같이 하는 일은 무엇인가?”', font(29, True), NAVY)
    save(img, 'manual-vs-loop.jpg')


def image_list_iteration_flow():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, 'List에서 학생을 한 명씩 꺼내기', '`for student in students`는 목록에서 현재 처리할 학생을 하나씩 바꾸는 과정입니다.')

    rr(d, (90, 240, 1510, 760), 34, '#F3F8FF', BLUE, 4)
    center(d, (120, 260, 500, 320), 'students  (List)', font(34, True), BLUE)

    student_card(d, 155, 370, '민수', '85', BLUE, active=True)
    student_card(d, 420, 370, '지영', '72', PINK)
    student_card(d, 685, 370, '현우', '91', GREEN)

    arrow(d, 915, 445, 1035, 445, PURPLE)
    rr(d, (1040, 345, 1425, 545), 28, WHITE, PURPLE, 4)
    center(d, (1070, 365, 1395, 420), '현재 student', font(29, True), PURPLE)
    center(d, (1070, 430, 1395, 515), '{"name": "민수",\n "score": 85}', font(25, True), NAVY)

    rr(d, (175, 590, 1370, 690), 26, WHITE, GREEN, 3)
    center(d, (195, 600, 1350, 680), '목록 → 한 명 꺼냄 → 처리 → 다음 학생 → 처리 → ... → 목록 끝', font(30, True), NAVY)

    rr(d, (300, 805, 1300, 865), 22, LIGHT_GREEN)
    center(d, (320, 805, 1280, 865), '`student`는 고정된 한 사람이 아니라 반복할 때마다 바뀌는 “현재 학생”입니다.', font(28, True), NAVY)
    save(img, 'list-iteration-flow.jpg')


def image_loop_inside_zoom():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '반복문 안에서는 한 학생에게 무슨 일이 일어날까?', '반복은 여러 명을 처리하지만, 한 번의 반복 안에서는 항상 “현재 한 명”만 다룹니다.')

    student_card(d, 95, 350, '현재 학생: 민수', '85', BLUE, active=True)
    arrow(d, 325, 425, 455, 425, BLUE)

    steps = [
        ('1', 'name 확인', 'name = student["name"]', LIGHT_BLUE, BLUE),
        ('2', 'score 확인', 'score = student["score"]', LIGHT_YELLOW, YELLOW),
        ('3', '조건 판단', 'score >= 80 ?', LIGHT_PINK, PINK),
        ('4', '결과 출력', 'print(name, score, result)', LIGHT_GREEN, GREEN),
    ]
    x = 470
    box_w = 245
    gap = 35
    for i, (num, head, code, light, accent) in enumerate(steps):
        rr(d, (x, 300, x+box_w, 610), 26, WHITE, accent, 4)
        d.ellipse((x+82, 320, x+162, 400), fill=accent)
        center(d, (x+82, 320, x+162, 400), num, font(31, True), WHITE)
        center(d, (x+20, 420, x+box_w-20, 475), head, font(27, True), NAVY)
        rr(d, (x+18, 500, x+box_w-18, 575), 18, light)
        center(d, (x+25, 500, x+box_w-25, 575), code, font(18, True), NAVY)
        if i < len(steps)-1:
            arrow(d, x+box_w+5, 455, x+box_w+gap-5, 455, GRAY, 8)
        x += box_w + gap

    rr(d, (220, 680, 1380, 775), 28, LIGHT_PURPLE)
    center(d, (245, 690, 1355, 765), '이 작업 묶음이 민수 → 지영 → 현우에게 똑같이 반복됩니다.', font(31, True), NAVY)
    rr(d, (305, 810, 1295, 870), 22, LIGHT_BLUE)
    center(d, (325, 810, 1275, 870), '반복을 이해하려면 “현재 한 명에게 하는 일”부터 정확히 설명할 수 있어야 합니다.', font(27, True), NAVY)
    save(img, 'loop-inside-zoom.jpg')


if __name__ == '__main__':
    image_manual_vs_loop()
    image_list_iteration_flow()
    image_loop_inside_zoom()
    for p in sorted(OUT.glob('*.jpg')):
        print(f'{p}: {p.stat().st_size} bytes')
