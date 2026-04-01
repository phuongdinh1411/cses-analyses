#!/usr/bin/env python3
"""
Re-render ByteByteGo raw JSON files into clean Markdown.

Approach: Linear scan of compiled MDX, matching JSX call patterns
and emitting markdown tokens in document order. This avoids the
complexity of full AST parsing.

Usage:
    python3 render_bytebytego.py                    # re-render all courses
    python3 render_bytebytego.py --course coding-patterns
    python3 render_bytebytego.py --sample            # render one sample + print it
"""

import argparse
import json
import re
from pathlib import Path

BASE_URL = "https://bytebytego.com"
CONTENT_DIR = Path("bytebytego_content")

# Per-lesson state: detected JSX namespace and tag variable (set by mdx_to_markdown)
_jsx_ns = 'e'
_tag_var = 't'


def mdx_to_markdown(code):
    """
    Convert compiled MDX code to clean Markdown.

    The compiled MDX has this structure:
        (0,e.jsx)(t.p, {children: "paragraph text"})
        (0,e.jsxs)(t.h2, {id:"...", children: "heading text"})
        (0,e.jsxs)(t.ul, {children: [`\\n`, (0,e.jsx)(t.li, ...), ...]})

    We scan for element openings: (0,e.jsx)(t.TAG,  or (0,e.jsxs)(t.TAG,
    then extract the children text using brace-matching for the props object.
    """
    if not code:
        return ""

    # 1. Extract image variable mappings from preamble
    image_vars = {}
    for m in re.finditer(r'var (\w+)="(/images/[^"]+)"', code):
        image_vars[m.group(1)] = BASE_URL + m.group(2)

    # 2. Auto-detect the content function and JSX namespace.
    #    Content function signature: function X(param){let var={...tag declarations like "p","h2","li"...}
    #    JSX namespace: the variable used in (0,NS.jsx)(...) calls — varies per lesson (e, C, A, V, etc.)
    fn_match = re.search(
        r'function\s+(\w+)\s*\(\w+\)\s*\{let\s+(\w+)=\{[^}]*"(?:p|h[1-6]|li)"', code
    )
    if fn_match:
        content_start = fn_match.start()
    else:
        content_start = 0

    ns_match = re.search(r'\(0,(\w+)\.jsxs?\)\(', code[content_start:])
    jsx_ns = re.escape(ns_match.group(1)) if ns_match else 'e'

    # Also detect the tag-object variable name (usually 't', but could vary)
    tag_var = re.escape(fn_match.group(2)) if fn_match else 't'

    # Store in module-level state so helper functions can access them
    global _jsx_ns, _tag_var
    _jsx_ns = jsx_ns
    _tag_var = tag_var

    body = code[content_start:]

    # 3. Find all top-level JSX element calls in order
    #    Pattern: (0,NS.jsx)(TAG_VAR.TAG, { ... })  or  (0,NS.jsxs)(TAG_VAR.TAG, { ... })
    #    Also match custom components for Image/Figure

    elements = []
    # Block-level elements we care about
    block_pat = re.compile(
        rf'\(0,{jsx_ns}\.jsxs?\)\({tag_var}\.(p|h[1-6]|li|pre|blockquote|hr|table|thead|tbody|tr|th|td),\{{'
    )
    for m in block_pat.finditer(body):
        tag = m.group(1)
        props_start = m.end() - 1  # points at the '{'
        props_str = extract_braced(body, props_start)
        if props_str:
            # Store absolute position in body AND the end position
            abs_start = m.start()
            abs_end = abs_start + (m.end() - m.start()) + len(props_str)
            elements.append((abs_start, abs_end, tag, props_str))

    # Image/Figure components (variable names from destructuring in content function)
    img_pat = re.compile(rf'\(0,{jsx_ns}\.jsxs?\)\((\w),\{{')
    for m in img_pat.finditer(body):
        props_start = m.end() - 1
        props_str = extract_braced(body, props_start)
        if props_str:
            # Only treat as image if props contain src/alt/caption
            if re.search(r'src:\s*\w+', props_str):
                abs_start = m.start()
                abs_end = abs_start + (m.end() - m.start()) + len(props_str)
                elements.append((abs_start, abs_end, '_image', props_str))

    # Sort by position
    elements.sort(key=lambda x: x[0])

    # 4. Build a set of positions that are "owned" by a parent element
    #    e.g., a <p> inside an <li> should be skipped at top level
    #    Similarly, <tr>/<th>/<td> inside <table> should be skipped.
    skip_positions = set()

    for idx, (start_pos, end_pos, tag, props) in enumerate(elements):
        if tag in ('li', 'table', 'blockquote'):
            # Mark all child elements within this element's range as skip
            for jdx in range(idx + 1, len(elements)):
                child_pos = elements[jdx][0]
                if child_pos > end_pos:
                    break
                skip_positions.add(child_pos)

    # 5. Convert to markdown
    lines = []

    for idx, (start_pos, end_pos, tag, props) in enumerate(elements):
        # Skip elements owned by a parent
        if start_pos in skip_positions:
            continue

        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            text = extract_children_text(props)
            if text.strip():
                level = int(tag[1])
                lines.append(f"\n{'#' * level} {text.strip()}\n")

        elif tag == 'p':
            text = extract_children_text(props)
            if text.strip():
                lines.append(f"\n{text.strip()}\n")

        elif tag == 'li':
            text = extract_children_text(props)
            if text.strip():
                clean = text.strip().replace('\n\n', '\n')
                lines.append(f"- {clean}")

        elif tag == 'pre':
            code_text = extract_code_block(props)
            if code_text:
                lang = extract_code_lang(props)
                lines.append(f"\n```{lang}\n{code_text}\n```\n")

        elif tag == 'blockquote':
            text = extract_children_text(props)
            if text.strip():
                quoted = "\n".join(f"> {l}" for l in text.strip().split("\n"))
                lines.append(f"\n{quoted}\n")

        elif tag == 'hr':
            lines.append("\n---\n")

        elif tag == 'table':
            table_md = extract_table(props)
            if table_md:
                lines.append(f"\n{table_md}\n")

        elif tag == '_image':
            src_match = re.search(r'src:\s*(\w+)', props)
            alt_match = re.search(r'alt:\s*"([^"]*)"', props)
            cap_match = re.search(r'caption:\s*"([^"]*)"', props)
            if src_match:
                src_var = src_match.group(1)
                src = image_vars.get(src_var, src_var)
                alt = alt_match.group(1) if alt_match else ""
                caption = cap_match.group(1) if cap_match else ""
                lines.append(f"\n![{alt or caption}]({src})\n")
                if caption and caption != alt:
                    lines.append(f"*{caption}*\n")

    return "\n".join(lines).strip()


def extract_braced(s, start):
    """Extract a brace-matched substring starting at s[start] which must be '{'."""
    if start >= len(s) or s[start] != '{':
        return None
    depth = 0
    i = start
    # Limit how far we search
    end_limit = min(start + 200000, len(s))
    while i < end_limit:
        c = s[i]
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return s[start:i + 1]
        elif c == '"':
            # Skip string literal
            i += 1
            while i < end_limit and s[i] != '"':
                if s[i] == '\\':
                    i += 1
                i += 1
        elif c == '`':
            # Skip template literal
            i += 1
            while i < end_limit and s[i] != '`':
                if s[i] == '\\':
                    i += 1
                i += 1
        i += 1
    return None


def extract_children_text(props_str):
    """
    Extract human-readable text from a props object string.

    Handles:
    - children: "string"
    - children: `template`
    - children: ["mixed", (0,e.jsx)(t.strong, {children:"bold"}), "more"]
    - Nested JSX for inline elements (strong, em, code, a, br)
    """
    # Find children: value
    m = re.search(r'children:\s*', props_str)
    if not m:
        return ""

    rest = props_str[m.end():]
    return _resolve_value(rest)


def _resolve_value(s):
    """Resolve a JS value (string, template, array, or JSX call) to text."""
    s = s.lstrip()
    if not s:
        return ""

    # String literal
    if s[0] == '"':
        end = find_string_end(s, 0)
        if end > 0:
            return unescape(s[1:end])
        return ""

    # Template literal
    if s[0] == '`':
        end = find_template_end(s, 0)
        if end > 0:
            val = unescape(s[1:end])
            # Template literals between elements are just whitespace/newlines
            if val.strip() == '':
                return val
            return val
        return ""

    # Array
    if s[0] == '[':
        return _resolve_array(s)

    # Nested JSX call — detect dynamically using the current namespace
    if re.match(rf'\(0,{_jsx_ns}\.jsxs?\)', s):
        return _resolve_jsx_call(s)

    # Boolean / number / null - not text
    return ""


def _resolve_array(s):
    """Parse a JS array and concatenate text of its elements."""
    parts = []
    depth = 0
    i = 1  # skip [
    current_start = 1
    limit = min(len(s), 200000)

    while i < limit:
        c = s[i]
        if c in ('{', '[', '('):
            depth += 1
        elif c in ('}', ']', ')'):
            if c == ']' and depth == 0:
                chunk = s[current_start:i].strip()
                if chunk:
                    parts.append(_resolve_value(chunk))
                break
            depth -= 1
        elif c == ',' and depth == 0:
            chunk = s[current_start:i].strip()
            if chunk:
                parts.append(_resolve_value(chunk))
            current_start = i + 1
        elif c == '"':
            i = find_string_end(s, i)
        elif c == '`':
            i = find_template_end(s, i)
        i += 1

    # Filter out pure whitespace parts
    return "".join(p for p in parts if p is not None)


def _resolve_jsx_call(s):
    """Resolve an inline JSX call to text with markdown formatting."""
    # Match: (0,NS.jsx)(TAG_VAR.TAG, {...}) or (0,NS.jsxs)(TAG_VAR.TAG, {...})
    m = re.match(rf'\(0,{_jsx_ns}\.jsxs?\)\({_tag_var}\.(\w+),', s)
    if not m:
        # Also match bare string tags: (0,NS.jsx)("u", {...})
        m = re.match(rf'\(0,{_jsx_ns}\.jsxs?\)\("(\w+)",', s)
        if not m:
            return ""

    tag = m.group(1)
    # Find the props brace
    props_start = s.find('{', m.end() - 1)
    if props_start == -1:
        return ""

    props = extract_braced(s, props_start)
    if not props:
        return ""

    text = extract_children_text(props)

    # Apply inline formatting
    if tag in ('strong', 'b'):
        return f"**{text}**"
    elif tag in ('em', 'i'):
        return f"*{text}*"
    elif tag == 'code':
        return f"`{text}`"
    elif tag == 'a':
        href_match = re.search(r'href:\s*"([^"]*)"', props)
        href = href_match.group(1) if href_match else ""
        if href:
            return f"[{text}]({href})"
        return text
    elif tag == 'u':
        return text
    elif tag == 'br':
        return "\n"
    elif tag == 'sub':
        return text
    elif tag == 'sup':
        return text
    elif tag == 'p':
        return text
    elif tag.startswith('h') and len(tag) == 2:
        return text

    return text


def extract_code_block(props_str):
    """Extract code content from a pre > code element."""
    # The structure is: pre > code > children
    # Children can be a simple string, template literal, or an array of
    # mixed text and <span> elements (syntax-highlighted code).

    # First, find the nested code element's props
    code_props_match = re.search(rf'\(0,{_jsx_ns}\.jsxs?\)\({_tag_var}\.code,\{{', props_str)
    if code_props_match:
        code_props_start = code_props_match.end() - 1
        code_props = extract_braced(props_str, code_props_start)
        if code_props:
            # Use the general-purpose children text extractor — handles strings,
            # template literals, arrays, and nested JSX spans
            return extract_children_text(code_props)

    # Fallback for simpler structures: direct string children
    code_match = re.search(rf'{_tag_var}\.code,\{{[^}}]*children:\s*"((?:[^"\\]|\\.)*)"', props_str)
    if code_match:
        return unescape(code_match.group(1))

    # Template literal
    code_match = re.search(rf'{_tag_var}\.code,\{{[^}}]*children:\s*`((?:[^`\\]|\\.)*)`', props_str)
    if code_match:
        return unescape(code_match.group(1))

    return ""


def extract_code_lang(props_str):
    """Extract language from className on code element."""
    m = re.search(r'className:\s*"[^"]*language-(\w+)"', props_str)
    return m.group(1) if m else ""


def extract_table(props_str):
    """Convert a table JSX element to markdown table."""
    rows = []

    # Find all tr elements
    for tr_match in re.finditer(rf'\(0,{_jsx_ns}\.jsxs?\)\({_tag_var}\.tr,\{{', props_str):
        tr_start = tr_match.end() - 1
        tr_props = extract_braced(props_str, tr_start)
        if not tr_props:
            continue

        cells = []
        is_header = False
        for cell_match in re.finditer(rf'\(0,{_jsx_ns}\.jsxs?\)\({_tag_var}\.(th|td),\{{', tr_props):
            if cell_match.group(1) == 'th':
                is_header = True
            cell_start = cell_match.end() - 1
            cell_props = extract_braced(tr_props, cell_start)
            if cell_props:
                text = extract_children_text(cell_props)
                cells.append(text.strip().replace('\n', ' '))

        if cells:
            rows.append((cells, is_header))

    if not rows:
        return ""

    # Build markdown table
    lines = []
    for i, (cells, is_header) in enumerate(rows):
        line = "| " + " | ".join(cells) + " |"
        lines.append(line)
        if is_header or (i == 0 and len(rows) > 1):
            sep = "| " + " | ".join("---" for _ in cells) + " |"
            lines.append(sep)

    return "\n".join(lines)


def find_string_end(s, start):
    """Find the closing quote of a string starting at s[start]='"'."""
    i = start + 1
    while i < len(s):
        if s[i] == '\\':
            i += 2
            continue
        if s[i] == '"':
            return i
        i += 1
    return len(s)


def find_template_end(s, start):
    """Find the closing backtick of a template literal starting at s[start]='`'."""
    i = start + 1
    while i < len(s):
        if s[i] == '\\':
            i += 2
            continue
        if s[i] == '`':
            return i
        i += 1
    return len(s)


def unescape(s):
    """Unescape JS string."""
    s = s.replace("\\n", "\n")
    s = s.replace("\\t", "\t")
    s = s.replace('\\"', '"')
    s = s.replace("\\'", "'")
    s = s.replace("\\\\", "\\")
    s = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), s)
    return s


def render_lesson(raw_json_path, output_md_path, dry_run=False):
    """Render a single lesson from raw JSON to clean Markdown."""
    with open(raw_json_path) as f:
        data = json.load(f)

    title = data.get("title", "Untitled")
    code = data.get("code", "")
    if not code:
        return False, 0

    content = mdx_to_markdown(code)
    md = f"# {title}\n\n{content}"

    if not dry_run:
        Path(output_md_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_md_path, "w", encoding="utf-8") as f:
            f.write(md)

    return True, len(md)


def main():
    parser = argparse.ArgumentParser(description="Re-render ByteByteGo content to clean Markdown")
    parser.add_argument("--course", type=str, help="Render specific course only")
    parser.add_argument("--dry-run", action="store_true", help="Don't write files")
    parser.add_argument("--sample", action="store_true", help="Render one sample + print")
    parser.add_argument("--content-dir", type=str, default=str(CONTENT_DIR))
    args = parser.parse_args()

    content_dir = Path(args.content_dir)

    if args.sample:
        # Pick a known good sample
        sample = content_dir / "system-design-interview" / "raw" / "005_design-a-rate-limiter.json"
        if not sample.exists():
            # Find any raw file
            samples = list(content_dir.glob("*/raw/*.json"))
            if not samples:
                print("No raw files found")
                return
            sample = samples[0]

        ok, size = render_lesson(sample, "/tmp/bbg_sample.md")
        print(f"Rendered {sample.name}: {size:,} chars")
        print()
        with open("/tmp/bbg_sample.md") as f:
            print(f.read()[:5000])
        return

    # Find all raw JSON files
    if args.course:
        raw_dirs = [content_dir / args.course / "raw"]
    else:
        raw_dirs = sorted(content_dir.glob("*/raw"))

    total_rendered = 0
    total_failed = 0

    for raw_dir in raw_dirs:
        if not raw_dir.exists():
            continue

        course = raw_dir.parent.name
        md_dir = raw_dir.parent
        json_files = sorted(raw_dir.glob("*.json"))

        print(f"\n  {course} ({len(json_files)} lessons)")

        for jf in json_files:
            md_path = md_dir / f"{jf.stem}.md"
            ok, size = render_lesson(jf, md_path, dry_run=args.dry_run)
            status = "OK" if ok else "FAIL"
            print(f"    {jf.stem}: {status} ({size:,} chars)")
            if ok:
                total_rendered += 1
            else:
                total_failed += 1

    print(f"\n  Done: {total_rendered} rendered, {total_failed} failed")


if __name__ == "__main__":
    main()
