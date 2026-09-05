from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path('images/chapter12')
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
DARK_GRAY = '#3E4A56'
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


def arrow(draw, x1, y1, x2, y2, color=BLUE, width=9):
    draw.line((x1, y1, x2-22, y2), fill=color, width=width)
    draw.polygon([(x2-22, y2-17), (x2, y2), (x2-22, y2+17)], fill=color)


def title(draw, main, sub):
    draw.text((85, 55), main, font=font(60, True), fill=NAVY)
    draw.text((88, 138), sub, font=font(29), fill=GRAY)


def save(img, name):
    img.convert('RGB').save(OUT / name, 'JPEG', quality=88, optimize=True, progressive=True)


def image_problem_solving_map():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, '처음 보는 문제도 같은 문제 해결 지도로 풀 수 있습니다', '새 문법보다 중요한 것은 문제를 이해하고, 나누고, 구현하고, 검증하는 순서입니다.')

    steps = [
        ('문제', LIGHT_BLUE, BLUE), ('이해', LIGHT_GREEN, GREEN), ('분해', LIGHT_YELLOW, YELLOW),
        ('데이터 구조', LIGHT_PURPLE, PURPLE), ('반복', LIGHT_BLUE, BLUE), ('조건', LIGHT_PINK, PINK),
        ('기능 분리', LIGHT_GREEN, GREEN), ('코드', LIGHT_YELLOW, YELLOW), ('예상', LIGHT_PURPLE, PURPLE),
        ('실행', LIGHT_BLUE, BLUE), ('수정', LIGHT_RED, RED), ('검증', LIGHT_GREEN, GREEN),
    ]
    xs = [90, 335, 580, 825, 1070, 1315]
    ys = [285, 535]
    idx = 0
    for row, y in enumerate(ys):
        items = range(6) if row == 0 else range(6)
        order = list(items) if row == 0 else list(reversed(list(items)))
        for pos in order:
            x = xs[pos]
            label, light, accent = steps[idx]
            rr(d, (x, y, x+190, y+115), 24, light, accent, 4)
            center(d, (x+10, y+15, x+180, y+100), f'{idx+1}. {label}', font(26, True), NAVY)
            if idx < 11:
                if row == 0 and pos < 5:
                    arrow(d, x+195, y+57, xs[pos+1]-8, y+57, PURPLE, 7)
                elif row == 0 and pos == 5:
                    d.line((x+95, y+120, x+95, ys[1]-5), fill=PURPLE, width=7)
                    d.polygon([(x+78, ys[1]-25), (x+95, ys[1]), (x+112, ys[1]-25)], fill=PURPLE)
                elif row == 1 and pos > 0:
                    d.line((x-5, y+57, xs[pos-1]+195, y+57), fill=PURPLE, width=7)
                    d.polygon([(xs[pos-1]+217, y+40), (xs[pos-1]+195, y+57), (xs[pos-1]+217, y+74)], fill=PURPLE)
            idx += 1

    rr(d, (245, 755, 1355, 835), 26, '#EEF7FF', BLUE, 3)
    center(d, (265, 755, 1335, 835), '핵심: 코드는 중간 단계일 뿐이다. 문제 이해부터 결과 검증까지가 전체 문제 해결 과정이다.', font(29, True), NAVY)
    save(img, 'problem-solving-map.jpg')


def image_growth_timeline():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, 'Chapter 0의 짧은 코드가 문제 해결 능력으로 성장했습니다', '같은 학생 예시를 반복하며 문법이 아니라 사고의 연결을 확장해 왔습니다.')

    labels = [
        ('Ch0', '기본 도구'), ('Ch1', '구조 찾기'), ('Ch3', '조건'), ('Ch4', '반복'),
        ('Ch5', '필터'), ('Ch6', '집계'), ('Ch7', '데이터 모델링'), ('Ch9', '함수 분리'),
        ('Ch10', '기능 연결'), ('Ch11', '디버깅'), ('Ch12', '독립 해결')
    ]
    colors = [(LIGHT_BLUE, BLUE), (LIGHT_GREEN, GREEN), (LIGHT_YELLOW, YELLOW), (LIGHT_PURPLE, PURPLE),
              (LIGHT_PINK, PINK), (LIGHT_GREEN, GREEN), (LIGHT_BLUE, BLUE), (LIGHT_YELLOW, YELLOW),
              (LIGHT_PURPLE, PURPLE), (LIGHT_RED, RED), (LIGHT_GREEN, GREEN)]
    y = 465
    start_x, end_x = 110, 1490
    d.line((start_x, y, end_x, y), fill=PURPLE, width=10)
    gap = (end_x-start_x)/(len(labels)-1)
    for i, ((ch, label), (light, accent)) in enumerate(zip(labels, colors)):
        x = start_x + i*gap
        d.ellipse((x-23, y-23, x+23, y+23), fill=accent, outline=WHITE, width=4)
        box_y = 265 if i % 2 == 0 else 545
        rr(d, (x-70, box_y, x+70, box_y+125), 22, light, accent, 3)
        center(d, (x-60, box_y+10, x+60, box_y+50), ch, font(23, True), accent)
        center(d, (x-60, box_y+52, x+60, box_y+112), label, font(22, True), NAVY)
        d.line((x, y-23 if i % 2 == 0 else y+23, x, box_y+125 if i % 2 == 0 else box_y), fill=accent, width=4)

    rr(d, (250, 755, 1350, 835), 26, LIGHT_GREEN, GREEN, 3)
    center(d, (270, 755, 1330, 835), '성장의 기준은 문법 암기가 아니라, 처음 보는 문제를 스스로 시작하고 끝까지 검증할 수 있는가이다.', font(29, True), NAVY)
    save(img, 'chapter00-to-12-growth.jpg')


def image_ai_order():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, 'AI는 생각의 시작점이 아니라 마지막 검증 단계입니다', '먼저 스스로 문제를 풀고 실행한 뒤, 문서와 AI를 이용해 가설과 결과를 확인합니다.')

    steps = [
        ('1', '내가 먼저 생각', LIGHT_BLUE, BLUE),
        ('2', '직접 작성', LIGHT_GREEN, GREEN),
        ('3', '실행', LIGHT_YELLOW, YELLOW),
        ('4', '공식 문서 확인', LIGHT_PURPLE, PURPLE),
        ('5', '수정', LIGHT_PINK, PINK),
        ('6', 'AI 검증', LIGHT_GREEN, GREEN),
    ]
    xs = [85, 330, 575, 820, 1065, 1310]
    for i, ((num, label, light, accent), x) in enumerate(zip(steps, xs)):
        rr(d, (x, 315, x+205, 555), 28, WHITE, accent, 4)
        rr(d, (x+55, 340, x+150, 395), 18, light)
        center(d, (x+60, 340, x+145, 395), num, font(25, True), accent)
        center(d, (x+20, 420, x+185, 525), label, font(27, True), NAVY, 10)
        if i < 5:
            arrow(d, x+210, 435, xs[i+1]-8, 435, PURPLE, 8)

    rr(d, (190, 655, 1410, 750), 28, LIGHT_YELLOW, YELLOW, 3)
    center(d, (215, 655, 1385, 750), 'AI 없이 개발하는 법을 배우는 것이 아니라, AI에게 생각을 맡기지 않는 법을 배운다.', font(34, True), NAVY)
    rr(d, (325, 785, 1275, 845), 22, LIGHT_BLUE)
    center(d, (345, 785, 1255, 845), 'AI의 역할: 처음부터 정답 생성 → X   |   내 사고와 구현의 검증자 → O', font(27, True), NAVY)
    save(img, 'ai-use-order.jpg')


def image_next_bridge():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    title(d, 'Python 문제 해결 사고는 다음 데이터 과정으로 이어집니다', '도구는 바뀌어도 데이터·조건·반복·집계·검증이라는 질문은 계속 남습니다.')

    items = [
        ('Python', '문제 구조\n데이터·조건·반복', LIGHT_BLUE, BLUE),
        ('Database', '현실 데이터를\n테이블로 저장', LIGHT_GREEN, GREEN),
        ('SQL', '필터·집계·조건을\n질의로 표현', LIGHT_YELLOW, YELLOW),
        ('pandas', '표 데이터를\n코드로 처리', LIGHT_PURPLE, PURPLE),
        ('Data Analysis', '질문 → 분석 →\n해석 → 검증', LIGHT_PINK, PINK),
    ]
    xs = [85, 385, 685, 985, 1285]
    for i, ((name, desc, light, accent), x) in enumerate(zip(items, xs)):
        rr(d, (x, 300, x+230, 580), 30, WHITE, accent, 4)
        rr(d, (x+35, 330, x+195, 395), 20, light)
        center(d, (x+45, 330, x+185, 395), name, font(26, True), NAVY)
        center(d, (x+25, 430, x+205, 545), desc, font(25, True), DARK_GRAY, 10)
        if i < 4:
            arrow(d, x+235, 440, xs[i+1]-8, 440, PURPLE, 9)

    rr(d, (240, 675, 1360, 760), 26, LIGHT_GREEN, GREEN, 3)
    center(d, (260, 675, 1340, 760), 'for + if → SQL WHERE   |   누적/집계 → SUM·COUNT·AVG·MAX   |   List of Dict → rows/table', font(28, True), NAVY)
    rr(d, (325, 790, 1275, 850), 22, LIGHT_BLUE)
    center(d, (345, 790, 1255, 850), '다음 과정에서도 가장 먼저 할 질문: 데이터는 무엇이고, 어떤 결과를 원하는가?', font(27, True), NAVY)
    save(img, 'python-to-data-analysis-bridge.jpg')


if __name__ == '__main__':
    image_problem_solving_map()
    image_growth_timeline()
    image_ai_order()
    image_next_bridge()
    for p in sorted(OUT.glob('*.jpg')):
        print(f'{p}: {p.stat().st_size} bytes')
