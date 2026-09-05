from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path('images/chapter07')
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


def student_id_card(draw, x, y, name='민수', score=85, major='AI', attendance=92, accent=BLUE, scale=1.0):
    w, h = int(430*scale), int(300*scale)
    rr(draw, (x, y, x+w, y+h), int(28*scale), WHITE, accent, max(2, int(4*scale)))
    rr(draw, (x+int(25*scale), y+int(22*scale), x+w-int(25*scale), y+int(82*scale)), int(18*scale), LIGHT_BLUE)
    center(draw, (x+int(35*scale), y+int(22*scale), x+w-int(35*scale), y+int(82*scale)), '학생 정보 카드', font(max(18, int(27*scale)), True), NAVY)
    rows = [('이름', name), ('점수', f'{score}'), ('전공', major), ('출석률', f'{attendance}%')]
    yy = y + int(100*scale)
    row_h = int(43*scale)
    for i, (k, v) in enumerate(rows):
        fill = [LIGHT_GREEN, LIGHT_YELLOW, LIGHT_PURPLE, LIGHT_PINK][i]
        rr(draw, (x+int(38*scale), yy, x+int(155*scale), yy+row_h), int(13*scale), fill)
        center(draw, (x+int(45*scale), yy, x+int(148*scale), yy+row_h), k, font(max(15, int(20*scale)), True), NAVY)
        center(draw, (x+int(180*scale), yy, x+w-int(35*scale), yy+row_h), v, font(max(15, int(21*scale)), True), NAVY)
        yy += int(47*scale)


def image_real_to_dictionary():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '현실의 한 학생을 Dictionary로 표현하기', '대상의 속성에 이름을 붙여 key-value 형태로 표현하면 의미가 분명해집니다.')

    student_id_card(d, 110, 300)
    arrow(d, 565, 455, 760, 455, PURPLE, 12)

    rr(d, (800, 245, 1490, 700), 32, '#F4F8FF', BLUE, 4)
    center(d, (835, 270, 1455, 335), 'Python Dictionary', font(38, True), NAVY)
    code_lines = [
        '{',
        '  "name": "민수",',
        '  "score": 85,',
        '  "major": "AI",',
        '  "attendance": 92',
        '}'
    ]
    y = 370
    fills = [None, LIGHT_GREEN, LIGHT_YELLOW, LIGHT_PURPLE, LIGHT_PINK, None]
    for i, line in enumerate(code_lines):
        if fills[i]:
            rr(d, (875, y-4, 1415, y+52), 15, fills[i])
        d.text((900, y), line, font=font(28, i in [0, 5]), fill=NAVY)
        y += 58

    rr(d, (250, 765, 1350, 840), 26, LIGHT_BLUE)
    center(d, (270, 765, 1330, 840), '학생 한 명 = 여러 속성을 가진 하나의 대상 → Dictionary', font(31, True), NAVY)
    save(img, 'student-card-to-dictionary.jpg')


def image_list_of_dicts():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '같은 구조의 학생이 여러 명이면 List로 묶습니다', '각 학생은 Dictionary, 여러 학생은 List of Dictionaries로 표현할 수 있습니다.')

    students = [
        ('민수', 85, 'AI', 92, BLUE),
        ('지영', 72, '경영', 88, YELLOW),
        ('현우', 91, '통계', 96, PURPLE),
    ]
    xs = [90, 545, 1000]
    for x, (name, score, major, attendance, accent) in zip(xs, students):
        student_id_card(d, x, 300, name, score, major, attendance, accent, 0.9)

    rr(d, (70, 255, 1445, 640), 36, None, GREEN, 6)
    rr(d, (615, 665, 1005, 735), 22, LIGHT_GREEN, GREEN, 3)
    center(d, (630, 665, 990, 735), 'students = [ {...}, {...}, {...} ]', font(27, True), NAVY)

    rr(d, (250, 770, 1350, 845), 26, '#EEF7FF')
    center(d, (270, 770, 1330, 845), '하나의 학생 = Dictionary   |   여러 학생 = List of Dictionaries', font(31, True), NAVY)
    save(img, 'students-list-of-dictionaries.jpg')


def image_to_table():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, 'Python 데이터 구조는 표와 데이터베이스로 이어집니다', '학생 카드 한 장은 row, 속성 이름은 column, 여러 학생의 모음은 table로 볼 수 있습니다.')

    student_id_card(d, 80, 300, '민수', 85, 'AI', 92, BLUE, 0.82)
    arrow(d, 450, 445, 610, 445, PURPLE, 11)

    rr(d, (650, 260, 1510, 700), 28, WHITE, BLUE, 4)
    center(d, (680, 275, 1480, 335), '학생 테이블', font(36, True), NAVY)

    x0, y0 = 710, 370
    col_widths = [190, 160, 190, 220]
    headers = ['name', 'score', 'major', 'attendance']
    rows = [
        ['민수', '85', 'AI', '92'],
        ['지영', '72', '경영', '88'],
        ['현우', '91', '통계', '96'],
    ]
    x = x0
    for w, htxt in zip(col_widths, headers):
        rr(d, (x, y0, x+w, y0+62), 0, LIGHT_BLUE, BLUE, 2)
        center(d, (x, y0, x+w, y0+62), htxt, font(23, True), NAVY)
        x += w
    y = y0 + 62
    for r, row in enumerate(rows):
        x = x0
        for w, value in zip(col_widths, row):
            fill = WHITE if r % 2 == 0 else '#F8FBFF'
            rr(d, (x, y, x+w, y+70), 0, fill, '#B8CBE0', 2)
            center(d, (x, y, x+w, y+70), value, font(23, True), NAVY)
            x += w
        y += 70

    rr(d, (80, 655, 420, 720), 20, LIGHT_GREEN, GREEN, 3)
    center(d, (95, 655, 405, 720), '학생 한 명 = row', font(25, True), NAVY)
    rr(d, (690, 725, 1030, 790), 20, LIGHT_PURPLE, PURPLE, 3)
    center(d, (705, 725, 1015, 790), '속성 이름 = column', font(25, True), NAVY)
    rr(d, (1080, 725, 1450, 790), 20, LIGHT_YELLOW, YELLOW, 3)
    center(d, (1095, 725, 1435, 790), '학생 모음 = table', font(25, True), NAVY)

    rr(d, (285, 820, 1315, 875), 20, LIGHT_BLUE)
    center(d, (300, 820, 1300, 875), 'List of Dictionaries를 이해하면 이후 데이터베이스와 pandas 구조가 훨씬 자연스럽습니다.', font(27, True), NAVY)
    save(img, 'dictionary-to-table.jpg')


if __name__ == '__main__':
    image_real_to_dictionary()
    image_list_of_dicts()
    image_to_table()
    for p in sorted(OUT.glob('*.jpg')):
        print(f'{p}: {p.stat().st_size} bytes')
