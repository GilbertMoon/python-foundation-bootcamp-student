from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path('images/chapter10')
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


def save(img, name):
    img.convert('RGB').save(OUT / name, 'JPEG', quality=88, optimize=True, progressive=True)


def title(draw, main, sub):
    draw.text((85, 55), main, font=font(62, True), fill=NAVY)
    draw.text((88, 138), sub, font=font(30), fill=GRAY)


def student_card(draw, x, y, name='민수', score=85, accent=BLUE):
    rr(draw, (x, y, x+270, y+165), 24, WHITE, accent, 4)
    center(draw, (x+20, y+22, x+250, y+75), name, font(29, True), NAVY)
    rr(draw, (x+60, y+92, x+210, y+142), 18, LIGHT_BLUE)
    center(draw, (x+65, y+92, x+205, y+142), f'{score}점', font(25, True), NAVY)


def image_function_machine():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '함수는 작은 처리 기계처럼 생각할 수 있습니다', '필요한 값을 입력으로 받고, 한 가지 일을 처리한 뒤, 결과를 다음 단계로 내보냅니다.')

    rr(d, (95, 330, 385, 560), 30, LIGHT_BLUE, BLUE, 4)
    center(d, (120, 355, 360, 420), '입력', font(38, True), NAVY)
    center(d, (120, 435, 360, 520), 'score = 85', font(31, True), NAVY)

    arrow(d, 410, 445, 590, 445, PURPLE, 12)

    rr(d, (625, 270, 995, 625), 36, WHITE, GREEN, 5)
    rr(d, (680, 300, 940, 365), 20, LIGHT_GREEN)
    center(d, (695, 300, 925, 365), 'get_result(score)', font(31, True), NAVY)
    center(d, (680, 400, 940, 520), '점수를 보고\n합격 여부를 판단', font(33, True), NAVY, 12)
    rr(d, (700, 555, 920, 595), 16, '#F3FBF8')
    center(d, (710, 555, 910, 595), '한 가지 역할', font(22, True), GREEN)

    arrow(d, 1025, 445, 1205, 445, PURPLE, 12)

    rr(d, (1235, 330, 1510, 560), 30, LIGHT_YELLOW, YELLOW, 4)
    center(d, (1260, 355, 1485, 420), '결과', font(38, True), NAVY)
    center(d, (1260, 435, 1485, 520), '"합격"', font(34, True), NAVY)

    rr(d, (240, 710, 1360, 810), 28, '#EEF7FF')
    center(d, (265, 710, 1335, 810), '함수를 설계할 때 먼저 묻습니다: 무엇을 받을까? → 무슨 일을 할까? → 무엇을 돌려줄까?', font(29, True), NAVY)
    save(img, 'function-input-process-output.jpg')


def image_function_pipeline():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '작은 기능을 연결하면 하나의 프로그램이 됩니다', '한 함수의 결과가 다음 함수의 입력이 되면서 데이터가 전체 흐름을 따라 이동합니다.')

    student_card(d, 80, 365, '민수', 85, BLUE)
    arrow(d, 370, 445, 500, 445, PURPLE, 10)

    stages = [
        ('판정 함수', 'get_result', '85 → 합격', LIGHT_GREEN, GREEN),
        ('등급 함수', 'get_grade', '85 → B', LIGHT_YELLOW, YELLOW),
        ('요약 함수', 'make_summary', '이름+결과+등급', LIGHT_PURPLE, PURPLE),
        ('출력', 'print_summary', '민수 / 합격 / B', LIGHT_PINK, PINK),
    ]
    xs = [515, 800, 1085, 1370]
    widths = [235, 235, 235, 165]

    for i, ((label, fname, result, light, accent), x) in enumerate(zip(stages, xs)):
        w = widths[i]
        rr(d, (x, 300, x+w, 590), 28, WHITE, accent, 4)
        rr(d, (x+20, 325, x+w-20, 380), 17, light)
        center(d, (x+25, 325, x+w-25, 380), label, font(24, True), NAVY)
        center(d, (x+20, 410, x+w-20, 455), fname, font(23, True), NAVY)
        center(d, (x+20, 485, x+w-20, 555), result, font(22, True), GRAY)
        if i < len(stages)-1:
            arrow(d, x+w+8, 445, xs[i+1]-10, 445, BLUE, 8)

    rr(d, (250, 690, 1350, 805), 28, LIGHT_BLUE)
    center(d, (280, 690, 1320, 805), '핵심: 각 함수는 자기 역할만 수행하고, return 값으로 다음 단계와 연결됩니다.\n세부 기능은 작게, 전체 흐름은 명확하게.', font(27, True), NAVY, 10)
    save(img, 'function-pipeline.jpg')


def image_print_vs_return():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, 'print와 return은 역할이 다릅니다', 'print는 사람에게 보여주고, return은 프로그램의 다음 단계가 사용할 값을 전달합니다.')

    rr(d, (115, 250, 725, 690), 34, WHITE, BLUE, 5)
    rr(d, (170, 285, 670, 355), 22, LIGHT_BLUE)
    center(d, (190, 285, 650, 355), 'print = 화면에 보여주기', font(34, True), NAVY)

    rr(d, (190, 415, 420, 515), 22, '#F4F8FF', BLUE, 3)
    center(d, (205, 415, 405, 515), '함수 결과\n"합격"', font(27, True), NAVY)
    arrow(d, 440, 465, 555, 465, BLUE, 9)
    rr(d, (575, 405, 675, 530), 18, LIGHT_YELLOW, YELLOW, 3)
    center(d, (585, 410, 665, 525), '화면\n합격', font(24, True), NAVY)
    center(d, (170, 585, 670, 650), '값을 보여줬지만, 다음 함수에\n자동으로 전달되는 것은 아닙니다.', font(25), GRAY, 8)

    rr(d, (875, 250, 1485, 690), 34, WHITE, GREEN, 5)
    rr(d, (930, 285, 1430, 355), 22, LIGHT_GREEN)
    center(d, (950, 285, 1410, 355), 'return = 다음 단계에 값 전달', font(32, True), NAVY)

    rr(d, (950, 415, 1165, 515), 22, '#F3FBF8', GREEN, 3)
    center(d, (965, 415, 1150, 515), 'get_result\n"합격"', font(25, True), NAVY)
    arrow(d, 1185, 465, 1285, 465, GREEN, 9)
    rr(d, (1305, 405, 1415, 530), 18, LIGHT_PURPLE, PURPLE, 3)
    center(d, (1315, 410, 1405, 525), '다음\n함수', font(24, True), NAVY)
    center(d, (930, 585, 1430, 650), '돌려준 값을 변수에 저장하거나\n다른 함수의 입력으로 사용할 수 있습니다.', font(25), GRAY, 8)

    rr(d, (285, 755, 1315, 835), 24, '#EEF7FF')
    center(d, (305, 755, 1295, 835), '사람에게 보여줄 것인가? → print    |    다음 코드가 사용할 것인가? → return', font(29, True), NAVY)
    save(img, 'print-vs-return.jpg')


if __name__ == '__main__':
    image_function_machine()
    image_function_pipeline()
    image_print_vs_return()
    for p in sorted(OUT.glob('*.jpg')):
        print(f'{p}: {p.stat().st_size} bytes')
