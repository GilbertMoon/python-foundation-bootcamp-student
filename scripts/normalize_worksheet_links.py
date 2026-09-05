from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
GUIDE = ROOT / "COURSE_GUIDE.md"

WORKSHEETS = [
    (1, "2026-09-08", "Chapter 01~02", "문제의 구조를 찾고 작은 단계로 나누기"),
    (2, "2026-09-10", "Chapter 03~04", "판단 기준과 반복되는 일을 발견하기"),
    (3, "2026-09-15", "Chapter 05~06", "필요한 데이터만 선택하고 하나의 결과 만들기"),
    (4, "2026-09-17", "Chapter 07~08", "현실 데이터를 구조화하고 여러 조건 함께 다루기"),
    (5, "2026-09-22", "Chapter 09~10", "큰 문제를 작은 함수로 나누고 다시 연결하기"),
    (6, "2026-09-24", "Chapter 11~12", "오류를 단서로 읽고 처음 보는 문제를 혼자 해결하기"),
]


def worksheet_lines() -> str:
    lines = []
    for session, date, chapters, title in WORKSHEETS:
        path = f"worksheets/session{session:02d}.md"
        lines.append(
            f"- [Session {session:02d}. {title}]({path}) — {date} · {chapters}"
        )
    return "\n".join(lines)


def worksheet_table() -> str:
    rows = [
        "| 회차 | 수업일 | 대상 Chapter | 학생용 워크시트 |",
        "| --- | --- | --- | --- |",
    ]
    for session, date, chapters, title in WORKSHEETS:
        path = f"worksheets/session{session:02d}.md"
        rows.append(
            f"| {session}회차 | {date} | {chapters} | [Session {session:02d}. {title}]({path}) |"
        )
    return "\n".join(rows)


def update_readme() -> bool:
    text = README.read_text(encoding="utf-8")
    marker = "## 실습 워크시트"
    if marker in text:
        return False

    anchor = "\n## 폴더\n"
    if anchor not in text:
        raise RuntimeError("README insertion anchor not found")

    section = (
        "\n## 실습 워크시트\n\n"
        "각 회차 수업에서는 강의안과 함께 아래 학생용 워크시트를 사용합니다. "
        "워크시트는 완성 정답보다 문제 분석, 실행 전 예상, 직접 구현, 디버깅 기록과 회고를 중심으로 구성되어 있습니다.\n\n"
        + worksheet_lines()
        + "\n"
    )
    README.write_text(text.replace(anchor, section + anchor, 1), encoding="utf-8")
    return True


def update_course_guide() -> bool:
    text = GUIDE.read_text(encoding="utf-8")
    marker = "## 회차별 학생 워크시트"
    if marker in text:
        return False

    anchor = (
        "> 일정은 운영 상황에 따라 조정할 수 있지만, "
        "**Chapter의 학습 순서는 유지**하는 것을 권장합니다.\n"
    )
    if anchor not in text:
        raise RuntimeError("COURSE_GUIDE insertion anchor not found")

    section = (
        "\n## 회차별 학생 워크시트\n\n"
        "각 수업에서는 해당 Chapter 강의안과 함께 학생용 워크시트를 사용합니다. "
        "워크시트의 빈 분석표와 예측·디버깅 기록을 먼저 작성한 뒤 코드를 구현합니다.\n\n"
        + worksheet_table()
        + "\n"
    )
    GUIDE.write_text(text.replace(anchor, anchor + section, 1), encoding="utf-8")
    return True


def main() -> None:
    changed = []
    if update_readme():
        changed.append("README.md")
    if update_course_guide():
        changed.append("COURSE_GUIDE.md")

    if changed:
        print("Updated: " + ", ".join(changed))
    else:
        print("Worksheet links already normalized.")


if __name__ == "__main__":
    main()
