from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path('images/chapter00')
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


def center_text(draw, box, text, fnt, fill=NAVY, spacing=6):
    x1, y1, x2, y2 = box
    bbox = draw.multiline_textbbox((0, 0), text, font=fnt, spacing=spacing, align='center')
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.multiline_text(((x1+x2-tw)/2, (y1+y2-th)/2), text, font=fnt, fill=fill, spacing=spacing, align='center')


def arrow(draw, x1, y, x2, color=BLUE, width=14):
    draw.line((x1, y, x2-25, y), fill=color, width=width)
    draw.polygon([(x2-25, y-20), (x2, y), (x2-25, y+20)], fill=color)


def save(img, name):
    img.convert('RGB').save(OUT / name, 'JPEG', quality=88, optimize=True, progressive=True)


def image_toolbox():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((90, 65), 'Python 기본 도구 상자', font=font(72, True), fill=NAVY)
    d.text((92, 150), '이미 배운 도구를 언제 꺼낼지 연습합니다.', font=font(34), fill=GRAY)

    # toolbox body
    rr(d, (100, 260, 1500, 700), 38, '#2F6E9F')
    rr(d, (135, 300, 1465, 640), 28, '#204C72')
    tools = [
        ('변수', 'x = 85', YELLOW, LIGHT_YELLOW),
        ('List', '[ 85, 72, 91 ]', BLUE, LIGHT_BLUE),
        ('Dictionary', '{ name, score }', GREEN, LIGHT_GREEN),
        ('if', '80점 이상?', PINK, LIGHT_PINK),
        ('for', '하나씩 반복', PURPLE, LIGHT_PURPLE),
    ]
    x = 165
    card_w = 238
    gap = 22
    for label, body, accent, light in tools:
        rr(d, (x, 330, x+card_w, 610), 24, WHITE)
        rr(d, (x+28, 365, x+card_w-28, 500), 20, light, accent, 3)
        center_text(d, (x+38, 370, x+card_w-38, 495), body, font(28, True), NAVY)
        center_text(d, (x+18, 520, x+card_w-18, 585), label, font(31, True), accent)
        x += card_w + gap

    rr(d, (280, 748, 1320, 828), 30, LIGHT_BLUE)
    center_text(d, (300, 748, 1300, 828), '새 문법을 찾기 전에, 이미 가진 도구부터 떠올려 봅니다.', font(31, True), NAVY)
    save(img, 'python-toolbox.jpg')


def image_student_cards():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((90, 60), '공통 학생 데이터 카드', font=font(68, True), fill=NAVY)
    d.text((92, 145), '학생 한 명은 Dictionary, 여러 학생은 List로 표현합니다.', font=font(34), fill=GRAY)

    rr(d, (85, 245, 1515, 760), 38, LIGHT_BLUE, BLUE, 4)
    rr(d, (120, 275, 360, 335), 22, BLUE)
    center_text(d, (125, 275, 355, 335), 'students  (List)', font(26, True), WHITE)

    cards = [
        ('민수', '85', LIGHT_YELLOW, YELLOW),
        ('지영', '72', LIGHT_PINK, PINK),
        ('현우', '91', LIGHT_GREEN, GREEN),
    ]
    x = 185
    for i, (name, score, light, accent) in enumerate(cards):
        rr(d, (x, 375, x+350, 680), 30, WHITE, accent, 4)
        rr(d, (x+30, 400, x+320, 455), 20, light)
        center_text(d, (x+35, 400, x+315, 455), '학생 1명 = Dictionary', font(24, True), accent)
        d.text((x+55, 500), 'name', font=font(27), fill=GRAY)
        d.text((x+185, 500), name, font=font(34, True), fill=NAVY)
        d.text((x+55, 570), 'score', font=font(27), fill=GRAY)
        d.text((x+185, 570), score, font=font(34, True), fill=NAVY)
        if i < 2:
            d.text((x+380, 505), ',', font=font(72, True), fill=NAVY)
        x += 430

    center_text(d, (260, 785, 1340, 850), '[  {민수},  {지영},  {현우}  ]  →  List of Dictionaries', font(30, True), NAVY)
    save(img, 'student-data-cards.jpg')


def image_code_flow():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((90, 55), '기본 코드 구조 해부도', font=font(68, True), fill=NAVY)
    d.text((92, 140), '학생 데이터 → 반복 → 값 확인 → 조건 판단 → 결과 출력', font=font(34), fill=GRAY)

    steps = [
        ('1', '학생 데이터', 'List 안에\n학생 3명', LIGHT_BLUE, BLUE),
        ('2', '한 명씩 꺼내기', 'for로\nstudent 선택', LIGHT_GREEN, GREEN),
        ('3', '점수 확인', 'student["score"]', LIGHT_YELLOW, YELLOW),
        ('4', '80점 판단', 'score >= 80 ?', LIGHT_PINK, PINK),
        ('5', '결과 출력', '합격 / 불합격', LIGHT_PURPLE, PURPLE),
    ]
    start_x = 55
    box_w = 270
    gap = 45
    y1, y2 = 300, 680
    for idx, (num, title, body, light, accent) in enumerate(steps):
        x1 = start_x + idx*(box_w+gap)
        x2 = x1 + box_w
        rr(d, (x1, y1, x2, y2), 30, WHITE, accent, 4)
        d.ellipse((x1+95, y1+25, x1+175, y1+105), fill=accent)
        center_text(d, (x1+95, y1+25, x1+175, y1+105), num, font(34, True), WHITE)
        center_text(d, (x1+18, y1+125, x2-18, y1+205), title, font(29, True), NAVY)
        rr(d, (x1+25, y1+225, x2-25, y2-35), 22, light)
        center_text(d, (x1+35, y1+235, x2-35, y2-45), body, font(27, True), NAVY)
        if idx < 4:
            arrow(d, x2+8, (y1+y2)//2, x2+gap-8)

    rr(d, (250, 760, 1350, 840), 30, LIGHT_BLUE)
    center_text(d, (270, 760, 1330, 840), '이 다섯 단계를 모든 학생에게 반복하면 프로그램이 완성됩니다.', font(30, True), NAVY)
    save(img, 'basic-code-flow.jpg')


if __name__ == '__main__':
    image_toolbox()
    image_student_cards()
    image_code_flow()
    print('Generated Chapter 00 JPG images:')
    for p in sorted(OUT.glob('*.jpg')):
        print(f'- {p} ({p.stat().st_size} bytes)')
