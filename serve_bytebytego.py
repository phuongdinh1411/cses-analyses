#!/usr/bin/env python3
"""
Local ByteByteGo course viewer.

Serves all crawled ByteByteGo content as a browsable local website with
course navigation, styled HTML rendering, and locally-served images.

Usage:
    python3 serve_bytebytego.py              # http://localhost:8080
    python3 serve_bytebytego.py --port 3000  # http://localhost:3000

Prerequisites:
    pip install markdown        # for markdown → HTML conversion
    python3 download_bytebytego_images.py   # download images first
"""

import argparse
import json
import mimetypes
import re
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote

try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

CONTENT_DIR = Path("bytebytego_content")
CATALOG_FILE = Path("bytebytego_courses.json")

# ── Catalog ─────────────────────────────────────────────────────────

def load_catalog():
    with open(CATALOG_FILE) as f:
        return json.load(f)


def chapter_filename(chapter):
    """Map a chapter dict to its markdown filename."""
    ch = chapter["chapter"]
    slug = chapter["slug"].replace("/", "_")
    prefix = f"{ch:03d}" if isinstance(ch, int) else str(ch)
    return f"{prefix}_{slug}.md"


# ── Markdown → HTML ─────────────────────────────────────────────────

def md_to_html(text):
    """Convert markdown text to HTML."""
    if HAS_MARKDOWN:
        return markdown.markdown(
            text,
            extensions=["tables", "fenced_code", "codehilite", "toc"],
            extension_configs={"codehilite": {"guess_lang": False, "css_class": "highlight"}},
        )
    # Fallback: very basic conversion
    return _basic_md_to_html(text)


def _basic_md_to_html(text):
    """Minimal markdown to HTML (no external deps)."""
    lines = text.split("\n")
    html_lines = []
    in_code = False
    in_list = False

    for line in lines:
        # Code blocks
        if line.startswith("```"):
            if in_code:
                html_lines.append("</code></pre>")
                in_code = False
            else:
                lang = line[3:].strip()
                html_lines.append(f'<pre><code class="language-{lang}">')
                in_code = True
            continue
        if in_code:
            html_lines.append(line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
            continue

        # Headings
        hm = re.match(r"^(#{1,6})\s+(.*)", line)
        if hm:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            level = len(hm.group(1))
            text_content = _inline(hm.group(2))
            html_lines.append(f"<h{level}>{text_content}</h{level}>")
            continue

        # List items
        if line.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{_inline(line[2:])}</li>")
            continue

        if in_list and (not line.strip()):
            html_lines.append("</ul>")
            in_list = False

        # Horizontal rule
        if line.strip() == "---":
            html_lines.append("<hr>")
            continue

        # Table rows
        if line.startswith("|"):
            # Simple table passthrough
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if all(c.startswith("---") for c in cells):
                continue
            row = "".join(f"<td>{_inline(c)}</td>" for c in cells)
            html_lines.append(f"<tr>{row}</tr>")
            continue

        # Paragraph
        stripped = line.strip()
        if stripped:
            html_lines.append(f"<p>{_inline(stripped)}</p>")

    if in_list:
        html_lines.append("</ul>")
    return "\n".join(html_lines)


def _inline(text):
    """Process inline markdown: bold, italic, code, links, images."""
    # Images
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1" loading="lazy">', text)
    # Links
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    # Inline code
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


# ── HTML Templates ──────────────────────────────────────────────────

CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
       display: flex; min-height: 100vh; background: #fff; color: #374151; }
a { color: #3b82f6; text-decoration: none; }
a:hover { text-decoration: underline; }

/* Sidebar */
.sidebar { width: 280px; min-width: 280px; background: #f8f9fb; color: #475569;
           padding: 20px 0; overflow-y: auto; position: fixed; top: 0; bottom: 0; left: 0;
           font-size: 14px; border-right: 1px solid #e5e7eb; }
.sidebar h2 { padding: 0 20px 15px; font-size: 16px; color: #111827; font-weight: 700;
              border-bottom: 1px solid #e5e7eb; margin-bottom: 10px; }
.sidebar a { color: #475569; display: block; padding: 7px 20px;
             border-left: 3px solid transparent; transition: all 0.15s; font-size: 14px; }
.sidebar a:hover { color: #1e293b; background: #f1f5f9; text-decoration: none; }
.sidebar a.active { color: #2563eb; border-left-color: #2563eb; background: #eff6ff;
                    font-weight: 600; }
.sidebar .ch-num { display: inline-block; min-width: 28px; color: #94a3b8; font-size: 12px;
                    margin-right: 4px; flex-shrink: 0; white-space: nowrap; }
.sidebar a.active .ch-num { color: #2563eb; }
.sidebar .section-group { }
.sidebar .section-label { padding: 14px 20px 6px; font-size: 12px; font-weight: 700;
                           color: #64748b; text-transform: uppercase; letter-spacing: 0.5px;
                           cursor: pointer; user-select: none; }
.sidebar .section-label:hover { color: #334155; }
.sidebar .section-toggle::after { content: "▾"; margin-right: 6px; font-size: 11px; }
.sidebar .section-group.collapsed .section-toggle::after { content: "▸"; }
.sidebar .section-group.collapsed .section-items { display: none; }
.sidebar .back { padding: 10px 20px; margin-bottom: 10px; font-size: 14px;
                 border-bottom: 1px solid #e5e7eb; }
.sidebar .back a { color: #64748b; padding: 0; display: inline; }
.sidebar .back a:hover { color: #2563eb; }

/* Content */
.content { margin-left: 280px; flex: 1; padding: 40px 60px; max-width: 900px; }
.content h1 { font-size: 28px; margin-bottom: 20px; color: #111827; font-weight: 700; }
.content h2 { font-size: 22px; margin: 30px 0 15px; color: #111827; font-weight: 600;
              border-bottom: 1px solid #f0f0f0; padding-bottom: 8px; }
.content h3 { font-size: 18px; margin: 25px 0 10px; color: #1f2937; }
.content h4 { font-size: 16px; margin: 20px 0 8px; color: #1f2937; }
.content p { line-height: 1.75; margin: 12px 0; color: #374151; }
.content ul, .content ol { margin: 12px 0; padding-left: 28px; }
.content li { margin: 6px 0; line-height: 1.65; }
.content img { max-width: 100%; height: auto; margin: 20px 0; border-radius: 8px;
               box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.content pre { background: #1e1e2e; color: #cdd6f4; padding: 16px 20px; border-radius: 10px;
               overflow-x: auto; margin: 16px 0; font-size: 13px; line-height: 1.5; }
.content code { font-family: 'Fira Code', 'Cascadia Code', Menlo, monospace; font-size: 0.9em; }
.content p code, .content li code, .content td code { background: #f1f5f9; padding: 2px 6px;
               border-radius: 4px; color: #e11d48; font-size: 0.85em; }
.content .highlight pre { background: #1e1e2e; color: #cdd6f4; }

/* Syntax highlighting — Catppuccin Mocha palette */
.highlight .k, .highlight .kn, .highlight .kd, .highlight .kc,
.highlight .kr, .highlight .kt { color: #cba6f7; }          /* keywords — mauve */
.highlight .nf, .highlight .fm, .highlight .nx { color: #89b4fa; }  /* function names — blue */
.highlight .nb, .highlight .bp { color: #f9e2af; }           /* builtins — yellow */
.highlight .n, .highlight .nn, .highlight .ni { color: #cdd6f4; }   /* names — text */
.highlight .s, .highlight .s1, .highlight .s2, .highlight .sa,
.highlight .sb, .highlight .sc, .highlight .dl,
.highlight .sd, .highlight .sh { color: #a6e3a1; }           /* strings — green */
.highlight .mi, .highlight .mf, .highlight .mh, .highlight .mo,
.highlight .il, .highlight .mb { color: #fab387; }           /* numbers — peach */
.highlight .c, .highlight .c1, .highlight .ch, .highlight .cm,
.highlight .cs, .highlight .cp, .highlight .cpf { color: #6c7086; font-style: italic; }  /* comments — overlay0 */
.highlight .o, .highlight .ow { color: #89dceb; }            /* operators — sky */
.highlight .p { color: #9399b2; }                             /* punctuation — overlay2 */
.highlight .nc, .highlight .ne { color: #f9e2af; }           /* class names — yellow */
.highlight .nd { color: #89b4fa; }                            /* decorators — blue */
.highlight .se { color: #f2cdcd; }                            /* string escape — flamingo */
.highlight .si { color: #f2cdcd; }                            /* string interp — flamingo */
.highlight .w { color: #cdd6f4; }                             /* whitespace */
.highlight .err { color: #f38ba8; }                           /* errors — red */
.highlight .gh, .highlight .gu { color: #89b4fa; font-weight: bold; } /* headings */
.highlight .gd { color: #f38ba8; }                            /* diff deleted — red */
.highlight .gi { color: #a6e3a1; }                            /* diff inserted — green */

/* Code tabs */
.code-tabs { margin: 16px 0; border-radius: 10px; overflow: hidden; border: 1px solid #e5e7eb; }
.tab-buttons { display: flex; background: #f8f9fb; border-bottom: 1px solid #e5e7eb; }
.tab-btn { background: transparent; color: #64748b; border: none; padding: 8px 18px;
           cursor: pointer; font-size: 13px; border-bottom: 2px solid transparent;
           font-family: inherit; transition: all 0.15s; }
.tab-btn:hover { color: #1e293b; background: #f1f5f9; }
.tab-btn.active { color: #3b82f6; border-bottom-color: #3b82f6; background: #fff; }
.tab-panel { display: none; }
.tab-panel.active { display: block; }
.tab-panel .highlight pre { margin: 0; border-radius: 0; }

.content blockquote { border-left: 3px solid #3b82f6; padding: 12px 20px; margin: 16px 0;
                      background: #f0f9ff; color: #1e293b; border-radius: 0 8px 8px 0; }
.content table { border-collapse: collapse; margin: 16px 0; width: 100%; }
.content th, .content td { border: 1px solid #e5e7eb; padding: 10px 14px; text-align: left; }
.content th { background: #f9fafb; font-weight: 600; color: #374151; }
.content tr:hover { background: #f9fafb; }
.content em { display: block; text-align: center; color: #6b7280; font-size: 0.9em; margin: -10px 0 20px; }

/* Navigation */
.nav-footer { display: flex; justify-content: space-between; margin-top: 50px;
              padding-top: 20px; border-top: 1px solid #f0f0f0; }
.nav-footer a { padding: 8px 20px; background: #3b82f6; color: #fff; border-radius: 8px;
                font-size: 14px; font-weight: 500; transition: background 0.15s; }
.nav-footer a:hover { background: #2563eb; text-decoration: none; }

/* Home page */
.course-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
               gap: 24px; margin-top: 24px; }
.course-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 16px;
               overflow: hidden; transition: box-shadow 0.2s, transform 0.2s;
               display: flex; flex-direction: column; }
.course-card:hover { box-shadow: 0 6px 20px rgba(0,0,0,0.08); transform: translateY(-2px);
                     text-decoration: none; }
.course-cover { width: 100%; height: 200px; object-fit: contain;
                background: #f8f9fb; padding: 12px; }
.card-body { padding: 14px 18px; }
.course-card h3 { font-size: 15px; margin-bottom: 4px; color: #111827; font-weight: 600; }
.course-card .meta { color: #94a3b8; font-size: 13px; }
.home-content { max-width: 1100px; margin: 0 auto; padding: 40px; width: 100%; }
.home-content h1 { font-size: 32px; margin-bottom: 8px; color: #111827; }
.home-content .subtitle { color: #6b7280; margin-bottom: 30px; font-size: 16px; }

/* Hamburger button — hidden on desktop */
.menu-toggle { display: none; position: fixed; top: 12px; left: 12px; z-index: 1100;
               background: #fff; border: 1px solid #e5e7eb; border-radius: 8px;
               width: 40px; height: 40px; cursor: pointer; align-items: center;
               justify-content: center; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
.menu-toggle svg { width: 20px; height: 20px; stroke: #475569; }
.sidebar-overlay { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.3);
                   z-index: 999; }

@media (max-width: 768px) {
    .menu-toggle { display: flex; }
    .sidebar { transform: translateX(-100%); transition: transform 0.25s ease;
               z-index: 1000; box-shadow: none; }
    .sidebar.open { transform: translateX(0); box-shadow: 4px 0 16px rgba(0,0,0,0.1); }
    .sidebar-overlay.open { display: block; }
    .content { margin-left: 0; padding: 60px 20px 20px; }
    .home-content { padding-top: 20px; }
}
"""


def page_html(title, body, sidebar=""):
    """Wrap content in full HTML page."""
    layout = "home-content" if not sidebar else "content"
    menu_btn = '<button class="menu-toggle" onclick="toggleSidebar()" aria-label="Menu"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg></button>' if sidebar else ""
    overlay = '<div class="sidebar-overlay" onclick="toggleSidebar()"></div>' if sidebar else ""
    sidebar_html = f'{menu_btn}{overlay}<nav class="sidebar">{sidebar}</nav>' if sidebar else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — ByteByteGo Local</title>
<style>{CSS}</style>
</head>
<body>
{sidebar_html}
<main class="{layout}">{body}</main>
<script>
function toggleSection(el){{el.closest('.section-group').classList.toggle('collapsed')}}
function switchTab(btn){{var c=btn.closest('.code-tabs'),idx=+btn.getAttribute('data-idx');c.querySelectorAll('.tab-btn').forEach(function(b){{b.classList.remove('active')}});c.querySelectorAll('.tab-panel').forEach(function(p){{p.classList.remove('active')}});btn.classList.add('active');c.querySelectorAll('.tab-panel')[idx].classList.add('active')}}
function toggleSidebar(){{var s=document.querySelector('.sidebar'),o=document.querySelector('.sidebar-overlay');s.classList.toggle('open');o.classList.toggle('open')}}
</script>
</body>
</html>"""


def render_home(courses):
    """Render the course listing home page."""
    cards = []
    for c in courses:
        ch_count = len(c.get("chapters", []))
        cover = f'/covers/{c["key"]}.png'
        cards.append(
            f'<a href="/courses/{c["key"]}" class="course-card">'
            f'<img src="{cover}" alt="{c["title"]}" class="course-cover" loading="lazy">'
            f'<div class="card-body">'
            f'<h3>{c["title"]}</h3>'
            f'<p class="meta">{ch_count} lessons</p>'
            f'</div></a>'
        )
    total_lessons = sum(len(c.get("chapters", [])) for c in courses)
    body = (
        '<h1>ByteByteGo Courses</h1>'
        f'<p class="subtitle">Offline local viewer — {len(courses)} courses, {total_lessons} lessons</p>'
        f'<div class="course-grid">{"".join(cards)}</div>'
    )
    return page_html("Home", body)


def render_course_index(course):
    """Render a course's chapter list."""
    chapters = course.get("chapters", [])
    sidebar = build_sidebar(course, active_slug=None)
    items = []
    for ch in chapters:
        items.append(
            f'<li><a href="/courses/{course["key"]}/{ch["slug"]}">{ch["title"]}</a></li>'
        )
    body = f'<h1>{course["title"]}</h1><ol>{"".join(items)}</ol>'
    return page_html(course["title"], body, sidebar)


# ── Code Tabs (coding-patterns only) ──────────────────────────────

LANG_DISPLAY = {
    "python": "Python", "py": "Python",
    "javascript": "JavaScript", "js": "JavaScript",
    "java": "Java",
    "cpp": "C++", "c++": "C++",
    "c": "C", "go": "Go", "rust": "Rust",
    "typescript": "TypeScript", "ts": "TypeScript",
}


def extract_code_groups(md_text):
    """
    Scan markdown for consecutive fenced code blocks and group them.

    Returns a list of groups, where each group is a list of display
    language names: [["Python","JavaScript","Java"], ["Python","Java"]]
    """
    # Find all fenced code blocks: ```lang ... ```
    blocks = []
    for m in re.finditer(r'^```(\w+)\s*\n(.*?)^```\s*$', md_text, re.MULTILINE | re.DOTALL):
        lang = m.group(1).lower()
        display = LANG_DISPLAY.get(lang, lang.capitalize())
        blocks.append((m.start(), m.end(), display))

    if not blocks:
        return []

    # Group consecutive blocks (only whitespace between them)
    groups = []
    current_group = [blocks[0]]
    for i in range(1, len(blocks)):
        gap = md_text[blocks[i - 1][1]:blocks[i][0]]
        if gap.strip() == "":
            current_group.append(blocks[i])
        else:
            if len(current_group) >= 2:
                groups.append(current_group)
            current_group = [blocks[i]]
    if len(current_group) >= 2:
        groups.append(current_group)

    # Split groups at language repetition (e.g., py/js/java/py/js/java → 2 groups of 3)
    result = []
    for group in groups:
        result.extend(_split_lang_cycle(group))

    return [[b[2] for b in g] for g in result]


def _split_lang_cycle(group):
    """Split a group of code blocks at language repetition."""
    langs = [b[2] for b in group]
    # Find if the first language repeats
    first = langs[0]
    for i in range(1, len(langs)):
        if langs[i] == first:
            # Split here
            left = group[:i]
            right = group[i:]
            if len(left) >= 2 and len(right) >= 2:
                return [left] + _split_lang_cycle(right)
            elif len(left) >= 2:
                return [left, right] if len(right) >= 2 else [left]
            break
    return [group]


def add_code_tabs(html, code_groups):
    """
    Post-process HTML to wrap consecutive <div class="highlight"> blocks
    in a tabbed UI, using language names from code_groups.
    """
    # Find all <div class="highlight"> blocks in the HTML
    highlight_pattern = re.compile(r'<div class="highlight">(.*?)</div>', re.DOTALL)
    matches = list(highlight_pattern.finditer(html))

    if not matches:
        return html

    # Group consecutive highlight divs (adjacent in HTML, possibly separated by whitespace)
    html_groups = []
    current = [matches[0]]
    for i in range(1, len(matches)):
        gap = html[matches[i - 1].end():matches[i].start()]
        if gap.strip() == "":
            current.append(matches[i])
        else:
            if len(current) >= 2:
                html_groups.append(current)
            current = [matches[i]]
    if len(current) >= 2:
        html_groups.append(current)

    # Split oversized HTML groups to match code_groups sizes
    split_html_groups = []
    group_idx = 0
    for hg in html_groups:
        remaining = list(hg)
        while remaining and group_idx < len(code_groups):
            expected_size = len(code_groups[group_idx])
            if expected_size <= len(remaining):
                split_html_groups.append((remaining[:expected_size], code_groups[group_idx]))
                remaining = remaining[expected_size:]
                group_idx += 1
            else:
                break
        if remaining and len(remaining) >= 2:
            # Leftover that didn't match — skip tabbing for safety
            pass

    if not split_html_groups:
        return html

    # Apply replacements from end to start to preserve positions
    for html_matches, lang_names in reversed(split_html_groups):
        if len(html_matches) != len(lang_names):
            continue

        # Build tab HTML
        buttons = []
        panels = []
        for idx, (m, lang) in enumerate(zip(html_matches, lang_names)):
            active = " active" if idx == 0 else ""
            buttons.append(
                f'<button class="tab-btn{active}" onclick="switchTab(this)" '
                f'data-idx="{idx}">{lang}</button>'
            )
            panels.append(
                f'<div class="tab-panel{active}">'
                f'<div class="highlight">{m.group(1)}</div></div>'
            )

        tab_html = (
            '<div class="code-tabs">'
            f'<div class="tab-buttons">{"".join(buttons)}</div>'
            f'{"".join(panels)}'
            '</div>'
        )

        # Replace the range from first match start to last match end
        start = html_matches[0].start()
        end = html_matches[-1].end()
        html = html[:start] + tab_html + html[end:]

    return html


def render_lesson(course, chapter, md_content, prev_ch, next_ch):
    """Render a lesson page with sidebar navigation."""
    # Rewrite image URLs to local paths
    md_content = md_content.replace("https://bytebytego.com/images/", "/images/")

    # Pre-extract code block language groups (for tab UI)
    code_groups = None
    if course["key"] == "coding-patterns":
        code_groups = extract_code_groups(md_content)

    html_body = md_to_html(md_content)

    # Apply tabbed code blocks for coding-patterns
    if code_groups:
        html_body = add_code_tabs(html_body, code_groups)

    sidebar = build_sidebar(course, active_slug=chapter["slug"])

    # Prev/Next nav
    nav = '<div class="nav-footer">'
    if prev_ch:
        nav += f'<a href="/courses/{course["key"]}/{prev_ch["slug"]}">← {prev_ch["title"]}</a>'
    else:
        nav += "<span></span>"
    if next_ch:
        nav += f'<a href="/courses/{course["key"]}/{next_ch["slug"]}">{next_ch["title"]} →</a>'
    else:
        nav += "<span></span>"
    nav += "</div>"

    body = html_body + nav
    return page_html(chapter["title"], body, sidebar)


def build_sidebar(course, active_slug):
    """Build sidebar HTML for a course."""
    lines = [
        f'<div class="back"><a href="/">← All Courses</a></div>',
        f'<h2>{course["title"]}</h2>',
    ]
    chapters = course.get("chapters", [])

    # Detect if course uses sectioned chapters (e.g., "01-00", "01-01")
    has_sections = any("-" in str(ch["chapter"]) for ch in chapters)

    if has_sections:
        # Determine which section contains the active slug
        active_section = None
        if active_slug:
            for ch in chapters:
                if ch["slug"] == active_slug:
                    active_section = str(ch["chapter"]).split("-")[0]
                    break

        # Group by section prefix with collapsible wrappers
        current_section = None
        for ch in chapters:
            chnum = str(ch["chapter"])
            sec = chnum.split("-")[0]
            sub = chnum.split("-")[1] if "-" in chnum else "00"
            if sec != current_section:
                # Close previous section group
                if current_section is not None:
                    lines.append('</div></div>')
                current_section = sec
                collapsed = "" if sec == active_section else " collapsed"
                # Section intro (XX-00) title becomes the group header
                intro = ch["title"] if sub == "00" else ""
                if intro.startswith("Introduction to "):
                    intro = intro[len("Introduction to "):]
                lines.append(f'<div class="section-group{collapsed}">')
                lines.append(
                    f'<div class="section-label" onclick="toggleSection(this)">'
                    f'<span class="section-toggle"></span>{intro}</div>'
                )
                lines.append('<div class="section-items">')
            cls = ' class="active"' if ch["slug"] == active_slug else ""
            lines.append(
                f'<a href="/courses/{course["key"]}/{ch["slug"]}"{cls}>'
                f'<span class="ch-num">{sub}</span>{ch["title"]}</a>'
            )
        # Close the last section group
        if current_section is not None:
            lines.append('</div></div>')
    else:
        # Flat numbered list
        for ch in chapters:
            cls = ' class="active"' if ch["slug"] == active_slug else ""
            chnum = ch["chapter"]
            num_str = f"{chnum:02d}" if isinstance(chnum, int) else str(chnum)
            lines.append(
                f'<a href="/courses/{course["key"]}/{ch["slug"]}"{cls}>'
                f'<span class="ch-num">{num_str}</span>{ch["title"]}</a>'
            )

    return "\n".join(lines)


# ── HTTP Server ─────────────────────────────────────────────────────

class ByteByteGoHandler(SimpleHTTPRequestHandler):

    catalog = None  # set in main()
    course_map = None

    def do_GET(self):
        path = unquote(self.path).split("?")[0].rstrip("/") or "/"

        # Home
        if path == "/":
            return self._send_html(render_home(self.catalog))

        # Static images and covers
        if path.startswith("/images/") or path.startswith("/covers/"):
            return self._serve_static(CONTENT_DIR / path.lstrip("/"))

        # Course routes: /courses/{key} or /courses/{key}/{slug}
        m = re.match(r"^/courses/([^/]+)(?:/(.+))?$", path)
        if m:
            course_key = m.group(1)
            slug = m.group(2)

            course = self.course_map.get(course_key)
            if not course:
                return self._send_404()

            if not slug:
                return self._send_html(render_course_index(course))

            # Find chapter by slug
            chapters = course.get("chapters", [])
            for i, ch in enumerate(chapters):
                if ch["slug"] == slug:
                    md_file = CONTENT_DIR / course_key / chapter_filename(ch)
                    if not md_file.exists():
                        return self._send_404()
                    md_content = md_file.read_text(encoding="utf-8")
                    prev_ch = chapters[i - 1] if i > 0 else None
                    next_ch = chapters[i + 1] if i < len(chapters) - 1 else None
                    return self._send_html(render_lesson(course, ch, md_content, prev_ch, next_ch))

            return self._send_404()

        self._send_404()

    def _send_html(self, html):
        data = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(data))
        self.end_headers()
        self.wfile.write(data)

    def _serve_static(self, filepath):
        if not filepath.exists():
            return self._send_404()
        mime, _ = mimetypes.guess_type(str(filepath))
        data = filepath.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mime or "application/octet-stream")
        self.send_header("Content-Length", len(data))
        self.send_header("Cache-Control", "public, max-age=86400")
        self.end_headers()
        self.wfile.write(data)

    def _send_404(self):
        body = page_html("Not Found", "<h1>404 — Page not found</h1><p><a href='/'>Go home</a></p>")
        data = body.encode("utf-8")
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(data))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        # Quieter logging — skip image requests
        if not self.path.startswith("/images/") and not self.path.startswith("/covers/"):
            super().log_message(format, *args)


def main():
    parser = argparse.ArgumentParser(description="Serve ByteByteGo content locally")
    parser.add_argument("--port", type=int, default=8080, help="Port (default: 8080)")
    args = parser.parse_args()

    catalog = load_catalog()
    ByteByteGoHandler.catalog = catalog
    ByteByteGoHandler.course_map = {c["key"]: c for c in catalog}

    if not HAS_MARKDOWN:
        print("  Note: 'markdown' package not installed — using basic renderer")
        print("  For better rendering: pip install markdown")

    server = HTTPServer(("0.0.0.0", args.port), ByteByteGoHandler)
    print(f"\n  ByteByteGo Local Viewer")
    print(f"  http://localhost:{args.port}")
    print(f"  {len(catalog)} courses, {sum(len(c.get('chapters',[])) for c in catalog)} lessons")
    print(f"  Press Ctrl+C to stop\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        server.server_close()


if __name__ == "__main__":
    main()
