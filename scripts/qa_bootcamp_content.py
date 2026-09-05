from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
RAW_PREFIX = (
    "https://raw.githubusercontent.com/"
    "GilbertMoon/python-foundation-bootcamp-student/main/"
)

EXPECTED_TITLES = {
    0: "# Chapter 00. 시작하기 전에 — Python 기본 도구를 손에 익히기",
    1: "# Chapter 01. 문제를 보면 코드부터 쓰지 않는다",
    2: "# Chapter 02. 문제를 실행 가능한 작은 단계로 나누기",
    3: "# Chapter 03. 조건은 문법이 아니라 판단 기준이다",
    4: "# Chapter 04. 반복은 for문이 아니라 반복되는 일을 발견하는 것이다",
    5: "# Chapter 05. 조건과 반복을 결합하면 실제 문제가 풀리기 시작한다",
    6: "# Chapter 06. 여러 데이터를 처리해서 하나의 결과 만들기",
    7: "# Chapter 07. 현실의 데이터를 Python 구조로 표현하기",
    8: "# Chapter 08. 여러 조건과 여러 데이터를 함께 다루기",
    9: "# Chapter 09. 큰 문제는 작은 문제의 조합이다",
    10: "# Chapter 10. 작은 기능을 연결하면 프로그램이 된다",
    11: "# Chapter 11. 오류는 실패가 아니라 단서다",
    12: "# Chapter 12. 처음 보는 문제를 혼자 해결하기",
}

EXPECTED_WORKSHEETS = {
    1: {
        "date": "2026-09-08",
        "chapters": "Chapter 01~02",
        "title": "# Session 01 Worksheet — 문제의 구조를 찾고 작은 단계로 나누기",
    },
    2: {
        "date": "2026-09-10",
        "chapters": "Chapter 03~04",
        "title": "# Session 02 Worksheet — 판단 기준과 반복되는 일을 발견하기",
    },
    3: {
        "date": "2026-09-15",
        "chapters": "Chapter 05~06",
        "title": "# Session 03 Worksheet — 필요한 데이터만 선택하고 하나의 결과 만들기",
    },
    4: {
        "date": "2026-09-17",
        "chapters": "Chapter 07~08",
        "title": "# Session 04 Worksheet — 현실 데이터를 구조화하고 여러 조건 함께 다루기",
    },
    5: {
        "date": "2026-09-22",
        "chapters": "Chapter 09~10",
        "title": "# Session 05 Worksheet — 큰 문제를 작은 함수로 나누고 다시 연결하기",
    },
    6: {
        "date": "2026-09-24",
        "chapters": "Chapter 11~12",
        "title": "# Session 06 Worksheet — 오류를 단서로 읽고 처음 보는 문제를 혼자 해결하기",
    },
}

IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
LESSON_LINK_RE = re.compile(r"\(blog/chapter\d{2}/chapter\d{2}\.md\)")
WORKSHEET_LINK_RE = re.compile(r"\(worksheets/session\d{2}\.md\)")
errors: list[str] = []
checks = 0


def check(condition: bool, message: str) -> None:
    global checks
    checks += 1
    if not condition:
        errors.append(message)


# 1) Core chapter files, exact titles, chapter-to-chapter continuity, image references.
for chapter in range(13):
    chapter_id = f"{chapter:02d}"
    md_path = ROOT / f"blog/chapter{chapter_id}/chapter{chapter_id}.md"
    check(md_path.exists(), f"[Chapter {chapter_id}] missing lesson file: {md_path.relative_to(ROOT)}")
    if not md_path.exists():
        continue

    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    first_line = lines[0].strip() if lines else ""
    check(
        first_line == EXPECTED_TITLES[chapter],
        f"[Chapter {chapter_id}] title mismatch: {first_line!r}",
    )

    # Every chapter except the Final Challenge should explicitly bridge to the next chapter.
    if chapter < 12:
        next_id = f"{chapter + 1:02d}"
        check(
            re.search(rf"Chapter\s+{next_id}\b", text) is not None,
            f"[Chapter {chapter_id}] missing explicit bridge to Chapter {next_id}",
        )

    image_urls = IMAGE_RE.findall(text)
    unique_urls = set(image_urls)
    minimum_images = 4 if chapter == 12 else 3
    check(
        len(unique_urls) >= minimum_images,
        f"[Chapter {chapter_id}] expected at least {minimum_images} unique images, found {len(unique_urls)}",
    )

    for url in unique_urls:
        check(
            "python-foundation-bootcamp-assets" not in url,
            f"[Chapter {chapter_id}] obsolete assets repository URL: {url}",
        )
        check(
            "/blob/" not in url,
            f"[Chapter {chapter_id}] GitHub blob URL used for an image: {url}",
        )
        check(
            url.startswith(RAW_PREFIX),
            f"[Chapter {chapter_id}] image is not a Public Raw absolute URL: {url}",
        )
        if url.startswith(RAW_PREFIX):
            relative = url[len(RAW_PREFIX):]
            local_path = ROOT / relative
            check(
                local_path.exists(),
                f"[Chapter {chapter_id}] image URL points to missing local file: {relative}",
            )

    # Every generated JPG in this chapter folder should actually be used in the lesson.
    image_dir = ROOT / f"images/chapter{chapter_id}"
    check(image_dir.is_dir(), f"[Chapter {chapter_id}] missing image directory")
    if image_dir.is_dir():
        jpgs = sorted(image_dir.glob("*.jpg"))
        check(
            len(jpgs) >= minimum_images,
            f"[Chapter {chapter_id}] expected at least {minimum_images} JPG files, found {len(jpgs)}",
        )
        for jpg in jpgs:
            raw_url = RAW_PREFIX + jpg.relative_to(ROOT).as_posix()
            check(
                raw_url in unique_urls,
                f"[Chapter {chapter_id}] generated image is not referenced by lesson: {jpg.relative_to(ROOT)}",
            )
            check(jpg.stat().st_size > 0, f"[Chapter {chapter_id}] empty JPG file: {jpg.relative_to(ROOT)}")

    # Reproducible asset generation must exist for every chapter.
    generator = ROOT / f"scripts/generate_chapter{chapter_id}_images.py"
    workflow = ROOT / f".github/workflows/generate-chapter{chapter_id}-images.yml"
    check(generator.exists(), f"[Chapter {chapter_id}] missing image generator script")
    check(workflow.exists(), f"[Chapter {chapter_id}] missing image generation workflow")


# 2) Public README should expose the course guide and all student lesson chapters.
readme_path = ROOT / "README.md"
check(readme_path.exists(), "README.md is missing")
readme = ""
if readme_path.exists():
    readme = readme_path.read_text(encoding="utf-8")
    check(
        "COURSE_GUIDE.md" in readme,
        "[README] missing link to COURSE_GUIDE.md",
    )
    for chapter in range(13):
        chapter_id = f"{chapter:02d}"
        lesson_path = f"blog/chapter{chapter_id}/chapter{chapter_id}.md"
        check(
            lesson_path in readme,
            f"[README] missing lesson link for Chapter {chapter_id}: {lesson_path}",
        )
    check(
        len(LESSON_LINK_RE.findall(readme)) == 13,
        f"[README] expected exactly 13 lesson links, found {len(LESSON_LINK_RE.findall(readme))}",
    )
    check(
        "python-foundation-bootcamp-assets" not in readme,
        "[README] obsolete assets repository reference remains",
    )


# 3) Student course guide must exist and cover the full six-session learning path.
guide_path = ROOT / "COURSE_GUIDE.md"
check(guide_path.exists(), "COURSE_GUIDE.md is missing")
guide = ""
if guide_path.exists():
    guide = guide_path.read_text(encoding="utf-8")
    check(
        guide.startswith("# Python Foundation Bootcamp — 학습 진행 가이드"),
        "[COURSE_GUIDE] unexpected or missing main title",
    )
    for session in range(1, 7):
        check(
            f"{session}회차" in guide,
            f"[COURSE_GUIDE] missing session label: {session}회차",
        )
    for chapter in range(13):
        chapter_id = f"{chapter:02d}"
        lesson_path = f"blog/chapter{chapter_id}/chapter{chapter_id}.md"
        check(
            lesson_path in guide,
            f"[COURSE_GUIDE] missing Chapter {chapter_id} link: {lesson_path}",
        )
    check("Final Challenge" in guide, "[COURSE_GUIDE] missing Final Challenge guidance")
    check("Python 공식 문서" in guide, "[COURSE_GUIDE] missing official-docs usage guidance")
    check("AI" in guide, "[COURSE_GUIDE] missing AI usage guidance")
    check("Database" in guide and "SQL" in guide and "pandas" in guide, "[COURSE_GUIDE] missing next-course data bridge")
    check(
        "python-foundation-bootcamp-assets" not in guide,
        "[COURSE_GUIDE] obsolete assets repository reference remains",
    )


# 4) Student worksheets must exist, match the session schedule, and be linked from both guides.
for session, expected in EXPECTED_WORKSHEETS.items():
    session_id = f"{session:02d}"
    relative_path = f"worksheets/session{session_id}.md"
    worksheet_path = ROOT / relative_path
    check(
        worksheet_path.exists(),
        f"[Session {session_id}] missing worksheet: {relative_path}",
    )
    if not worksheet_path.exists():
        continue

    worksheet = worksheet_path.read_text(encoding="utf-8")
    lines = worksheet.splitlines()
    first_line = lines[0].strip() if lines else ""
    check(
        first_line == expected["title"],
        f"[Session {session_id}] worksheet title mismatch: {first_line!r}",
    )
    check(
        f"**수업일:** {expected['date']}" in worksheet,
        f"[Session {session_id}] expected class date {expected['date']} not found",
    )
    check(
        f"**대상 Chapter:** {expected['chapters']}" in worksheet,
        f"[Session {session_id}] expected chapter range {expected['chapters']} not found",
    )
    check(
        relative_path in readme,
        f"[README] missing worksheet link for Session {session_id}: {relative_path}",
    )
    check(
        relative_path in guide,
        f"[COURSE_GUIDE] missing worksheet link for Session {session_id}: {relative_path}",
    )
    check(
        "python-foundation-bootcamp-assets" not in worksheet,
        f"[Session {session_id}] obsolete assets repository reference remains",
    )

check(
    len(WORKSHEET_LINK_RE.findall(readme)) == 6,
    f"[README] expected exactly 6 worksheet links, found {len(WORKSHEET_LINK_RE.findall(readme))}",
)
check(
    len(WORKSHEET_LINK_RE.findall(guide)) == 6,
    f"[COURSE_GUIDE] expected exactly 6 worksheet links, found {len(WORKSHEET_LINK_RE.findall(guide))}",
)


# 5) Public lesson Markdown must not contain stale private/old asset repository paths.
for md_path in sorted((ROOT / "blog").glob("chapter*/chapter*.md")):
    text = md_path.read_text(encoding="utf-8")
    check(
        "python-foundation-bootcamp-assets" not in text,
        f"[{md_path.relative_to(ROOT)}] obsolete assets repository reference remains",
    )


print(f"QA checks executed: {checks}")
if errors:
    print(f"QA FAILED: {len(errors)} issue(s) found")
    for index, error in enumerate(errors, start=1):
        print(f"{index:02d}. {error}")
    sys.exit(1)

print(
    "QA PASSED: Chapter 00-12 content, images, links, generators, workflows, "
    "README, COURSE_GUIDE, and Session 01-06 worksheets are consistent."
)
