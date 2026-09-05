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

IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
LESSON_LINK_RE = re.compile(r"\(blog/chapter\d{2}/chapter\d{2}\.md\)")
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


# 2) Public README should expose all student lesson chapters, not only Chapter 00.
readme_path = ROOT / "README.md"
check(readme_path.exists(), "README.md is missing")
if readme_path.exists():
    readme = readme_path.read_text(encoding="utf-8")
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


# 3) Public lesson Markdown must not contain stale private/old asset repository paths.
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

print("QA PASSED: Chapter 00-12 content, images, links, generators, workflows, and README are consistent.")
