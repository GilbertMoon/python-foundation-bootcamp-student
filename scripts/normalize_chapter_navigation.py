from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TITLES = {
    0: "시작하기 전에 — Python 기본 도구를 손에 익히기",
    1: "문제를 보면 코드부터 쓰지 않는다",
    2: "문제를 실행 가능한 작은 단계로 나누기",
    3: "조건은 문법이 아니라 판단 기준이다",
    4: "반복은 for문이 아니라 반복되는 일을 발견하는 것이다",
    5: "조건과 반복을 결합하면 실제 문제가 풀리기 시작한다",
    6: "여러 데이터를 처리해서 하나의 결과 만들기",
    7: "현실의 데이터를 Python 구조로 표현하기",
    8: "여러 조건과 여러 데이터를 함께 다루기",
    9: "큰 문제는 작은 문제의 조합이다",
    10: "작은 기능을 연결하면 프로그램이 된다",
    11: "오류는 실패가 아니라 단서다",
    12: "처음 보는 문제를 혼자 해결하기",
}

# Final QA에서 실제로 다음 Chapter 번호가 명시되지 않은 것으로 확인된 Chapter들.
TARGETS = [0, 1, 3, 7, 8, 9, 10, 11]

for chapter in TARGETS:
    current_id = f"{chapter:02d}"
    next_chapter = chapter + 1
    next_id = f"{next_chapter:02d}"
    path = ROOT / f"blog/chapter{current_id}/chapter{current_id}.md"
    text = path.read_text(encoding="utf-8").rstrip()

    marker = f"## 다음 Chapter — Chapter {next_id}"
    if marker in text:
        print(f"skip: {path.relative_to(ROOT)}")
        continue

    footer = f"""

---

## 다음 Chapter — Chapter {next_id}

다음은 [Chapter {next_id}. {TITLES[next_chapter]}](../chapter{next_id}/chapter{next_id}.md)입니다.

지금까지 익힌 내용을 다음 문제 해결 단계로 연결해 보세요.
"""
    path.write_text(text + footer, encoding="utf-8")
    print(f"updated: {path.relative_to(ROOT)}")
