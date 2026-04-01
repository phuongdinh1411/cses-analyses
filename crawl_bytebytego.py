#!/usr/bin/env python3
"""
ByteByteGo Course Crawler
Crawls all lesson content from ByteByteGo courses and saves as markdown files.

Usage:
    python3 crawl_bytebytego.py --cookies "your_cookie_string"
    python3 crawl_bytebytego.py --cookies-file .bytebytego_cookies
    python3 crawl_bytebytego.py --course system-design-interview  # crawl one course only

Features:
    - Resumes from where it left off (skips already-downloaded lessons)
    - Extracts text content from compiled MDX (JSX)
    - Downloads images referenced in lessons
    - Rate-limited to avoid getting blocked
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

BASE_URL = "https://bytebytego.com"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
OUTPUT_DIR = Path("bytebytego_content")
CATALOG_FILE = Path("bytebytego_courses.json")
DELAY_BETWEEN_REQUESTS = 1.5  # seconds


def fetch_page(url, cookies):
    """Fetch a page with authentication cookies."""
    req = urllib.request.Request(url)
    req.add_header("User-Agent", UA)
    req.add_header("Cookie", cookies)
    req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code} for {url}")
        return None
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return None


def extract_next_data(html):
    """Extract __NEXT_DATA__ JSON from HTML."""
    match = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
        html,
        re.DOTALL,
    )
    if not match:
        return None
    return json.loads(match.group(1))


def extract_text_from_mdx(code):
    """
    Extract readable text content from compiled MDX code.
    The MDX is compiled to JSX - we extract text from template literals and children props.
    """
    if not code:
        return ""

    lines = []

    # Extract image paths
    image_paths = re.findall(r'var \w+="(/images/[^"]+)"', code)

    # Extract the main content function body
    # Find the function that creates the JSX tree
    # Text appears in patterns like:
    #   children:"some text"
    #   `template literal text`
    #   (0,e.jsx)(t.p,{children:"text"})
    #   (0,e.jsxs)(t.p,{children:["text", ...]})

    # Strategy: extract all string literals that look like content
    # 1. Find heading text: t.h1, t.h2, t.h3, etc.
    heading_pattern = re.findall(
        r'\(0,e\.jsxs?\)\(t\.(h[1-6]),\{[^}]*children:\s*"([^"]*)"',
        code,
    )

    # 2. Extract text from the MDX more carefully using a state machine approach
    # Find the main content rendering function
    content_start = code.find("function W(")
    if content_start == -1:
        content_start = code.find("function R(")
    if content_start == -1:
        content_start = 0

    content_code = code[content_start:]

    # Extract all text segments
    # Pattern: children:"text" or children:`text`
    segments = []

    # Simple string children
    for m in re.finditer(r'children:\s*"((?:[^"\\]|\\.)*)"', content_code):
        text = m.group(1)
        text = text.replace("\\n", "\n").replace('\\"', '"')
        if len(text) > 1 and not text.startswith("http"):
            segments.append(("text", m.start(), text))

    # Template literal children (backtick strings with newlines)
    for m in re.finditer(r"children:\s*`((?:[^`\\]|\\.)*)`", content_code):
        text = m.group(1)
        text = text.replace("\\n", "\n")
        if len(text) > 1:
            segments.append(("text", m.start(), text))

    # Standalone template literals (often paragraph text)
    for m in re.finditer(r'(?<!children:)\s*`((?:[^`\\]|\\.){20,})`', content_code):
        text = m.group(1).replace("\\n", "\n")
        segments.append(("text", m.start(), text))

    # Detect headings by looking for t.h1, t.h2, etc.
    for m in re.finditer(
        r'\(0,e\.jsxs?\)\(t\.(h[1-6]),\{[^}]*?(?:children:\s*(?:"((?:[^"\\]|\\.)*)"|`((?:[^`\\]|\\.)*)`|\[(.*?)\]))',
        content_code,
        re.DOTALL,
    ):
        level = m.group(1)
        text = m.group(2) or m.group(3) or ""
        if m.group(4):
            # Array children - extract strings
            arr_text = re.findall(r'"((?:[^"\\]|\\.)+)"', m.group(4))
            text = "".join(arr_text)
        if text:
            prefix = "#" * int(level[1])
            segments.append(("heading", m.start(), f"{prefix} {text}"))

    # Detect images
    for m in re.finditer(
        r'\(0,e\.jsx\)\(t\.img,\{[^}]*src:\s*(\w+)[^}]*(?:alt:\s*"([^"]*)")?',
        content_code,
    ):
        var_name = m.group(1)
        alt = m.group(2) or ""
        segments.append(("image", m.start(), f"![{alt}]"))

    # Detect code blocks
    for m in re.finditer(
        r'\(0,e\.jsx\)\(t\.code,\{[^}]*children:\s*"((?:[^"\\]|\\.)*)"',
        content_code,
    ):
        segments.append(("code", m.start(), f"`{m.group(1)}`"))

    # Sort by position and build output
    segments.sort(key=lambda x: x[1])

    output_lines = []
    for seg_type, pos, text in segments:
        text = text.strip()
        if text and len(text) > 0:
            output_lines.append(text)

    # Also include image paths as references
    if image_paths:
        output_lines.append("\n---\n## Images Referenced")
        for path in image_paths:
            output_lines.append(f"- {BASE_URL}{path}")

    return "\n\n".join(output_lines)


def extract_raw_text_simple(code):
    """
    Simpler extraction: just pull all human-readable text from the JSX.
    Falls back to this if the structured extraction is too messy.
    """
    if not code:
        return ""

    # Remove the module wrapper, keep just the content function
    content_start = code.find("function W(")
    if content_start == -1:
        content_start = code.find("function R(")
    if content_start == -1:
        content_start = len(code) // 3  # rough guess

    code = code[content_start:]

    # Collect all string content
    all_text = []

    # Extract from children props and template literals
    for m in re.finditer(r'(?:children:\s*)?(?:"((?:[^"\\]|\\.){2,})"|`((?:[^`\\]|\\.){2,})`)', code):
        text = (m.group(1) or m.group(2) or "").strip()
        text = text.replace("\\n", "\n").replace('\\"', '"').replace("\\'", "'")
        # Filter out code/variable-like strings
        if (
            text
            and len(text) > 1
            and not text.startswith("use ")
            and not text.startswith("var ")
            and not text.startswith("function")
            and "=>" not in text
            and not re.match(r"^[a-zA-Z_]+\.[a-zA-Z_]+", text)
            and not text.startswith("http")
            and not text.startswith("/images/")
        ):
            all_text.append(text)

    # Extract image references
    images = re.findall(r'var \w+="(/images/[^"]+)"', code[:content_start] if content_start > 0 else code)
    if images:
        all_text.append("\n---\nImages:")
        for img in images:
            all_text.append(f"  {BASE_URL}{img}")

    return "\n".join(all_text)


def fmt_chapter(chapter_num):
    """Format chapter number for filenames (handles int and str)."""
    if isinstance(chapter_num, int):
        return f"{chapter_num:03d}"
    return str(chapter_num)


def save_lesson_raw(course_key, chapter_num, slug, title, page_props, output_dir):
    """Save the raw pageProps JSON for a lesson."""
    raw_dir = output_dir / course_key / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    slug_safe = slug.replace("/", "_")
    filename = f"{fmt_chapter(chapter_num)}_{slug_safe}.json"
    filepath = raw_dir / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(page_props, f, indent=2, ensure_ascii=False)

    return filepath


def save_lesson_markdown(course_key, chapter_num, slug, title, content, output_dir):
    """Save extracted lesson content as markdown."""
    md_dir = output_dir / course_key
    md_dir.mkdir(parents=True, exist_ok=True)

    slug_safe = slug.replace("/", "_")
    filename = f"{fmt_chapter(chapter_num)}_{slug_safe}.md"
    filepath = md_dir / filename

    header = f"# {title}\n\n"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(header + content)

    return filepath


def crawl_course(course, cookies, output_dir, force=False, delay=1.5):
    """Crawl all chapters of a single course."""
    course_key = course["key"]
    chapters = course.get("chapters", [])
    title = course["title"]

    print(f"\n{'='*60}")
    print(f"  Course: {title}")
    print(f"  Key: {course_key}")
    print(f"  Chapters: {len(chapters)}")
    print(f"{'='*60}")

    if not chapters:
        print("  No chapters found (TOC empty). Skipping.")
        return 0, 0

    success = 0
    skipped = 0

    for ch in chapters:
        chapter_num = ch["chapter"]
        slug = ch["slug"]
        ch_title = ch["title"]

        # Check if already downloaded
        slug_safe = slug.replace("/", "_")
        raw_file = output_dir / course_key / "raw" / f"{fmt_chapter(chapter_num)}_{slug_safe}.json"
        if raw_file.exists() and not force:
            print(f"  [{chapter_num:>3}] {ch_title} — already downloaded, skipping")
            skipped += 1
            continue

        url = f"{BASE_URL}/courses/{course_key}/{slug}"
        print(f"  [{chapter_num:>3}] {ch_title} — fetching...", end=" ", flush=True)

        html = fetch_page(url, cookies)
        if not html:
            print("FAILED")
            continue

        data = extract_next_data(html)
        if not data:
            print("NO DATA")
            continue

        pp = data.get("props", {}).get("pageProps", {})
        if not pp:
            print("EMPTY")
            continue

        code = pp.get("code", "")

        # Save raw JSON
        save_lesson_raw(course_key, chapter_num, slug, ch_title, pp, output_dir)

        # Extract and save markdown
        content = extract_text_from_mdx(code)
        if not content or len(content) < 50:
            content = extract_raw_text_simple(code)

        save_lesson_markdown(course_key, chapter_num, slug, ch_title, content, output_dir)

        code_size = len(code) if code else 0
        md_size = len(content) if content else 0
        print(f"OK (raw: {code_size:,} chars, md: {md_size:,} chars)")
        success += 1

        time.sleep(delay)

    return success, skipped


def main():
    parser = argparse.ArgumentParser(description="Crawl ByteByteGo courses")
    parser.add_argument("--cookies", type=str, help="Cookie string")
    parser.add_argument("--cookies-file", type=str, help="File containing cookie string")
    parser.add_argument("--course", type=str, help="Crawl specific course key only")
    parser.add_argument("--output", type=str, default=str(OUTPUT_DIR), help="Output directory")
    parser.add_argument("--force", action="store_true", help="Re-download existing files")
    parser.add_argument("--delay", type=float, default=DELAY_BETWEEN_REQUESTS, help="Delay between requests (seconds)")
    args = parser.parse_args()

    delay = args.delay

    # Get cookies
    cookies = args.cookies
    if not cookies and args.cookies_file:
        with open(args.cookies_file) as f:
            cookies = f.read().strip()
    if not cookies:
        print("Error: provide --cookies or --cookies-file")
        sys.exit(1)

    # Load course catalog
    if not CATALOG_FILE.exists():
        print(f"Error: {CATALOG_FILE} not found. Run the catalog crawl first.")
        sys.exit(1)

    with open(CATALOG_FILE) as f:
        courses = json.load(f)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Filter to specific course if requested
    if args.course:
        courses = [c for c in courses if c["key"] == args.course]
        if not courses:
            print(f"Error: course '{args.course}' not found in catalog")
            sys.exit(1)

    total_success = 0
    total_skipped = 0
    total_chapters = sum(len(c.get("chapters", [])) for c in courses)

    print(f"ByteByteGo Course Crawler")
    print(f"Courses to crawl: {len(courses)}")
    print(f"Total chapters: {total_chapters}")
    print(f"Output directory: {output_dir}")
    print(f"Delay between requests: {delay}s")

    for course in courses:
        success, skipped = crawl_course(course, cookies, output_dir, force=args.force, delay=delay)
        total_success += success
        total_skipped += skipped

    print(f"\n{'='*60}")
    print(f"  DONE!")
    print(f"  Downloaded: {total_success} lessons")
    print(f"  Skipped (already existed): {total_skipped}")
    print(f"  Total: {total_success + total_skipped}/{total_chapters}")
    print(f"  Output: {output_dir}/")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
