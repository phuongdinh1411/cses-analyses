# LeetCode Contest Crawling & Documentation Template

This guide explains how to crawl LeetCode contests, fetch problems, and add hints/approaches.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Getting LeetCode Cookies](#getting-leetcode-cookies)
3. [Running the Crawler](#running-the-crawler)
4. [Contest File Format](#contest-file-format)
5. [Adding Hints & Approaches](#adding-hints--approaches)
6. [Updating Navigation](#updating-navigation)

---

## Prerequisites

- Python 3.x
- `curl` command available
- LeetCode account (logged in)

---

## Getting LeetCode Cookies

1. Open browser DevTools (F12) on leetcode.com while logged in
2. Go to **Network** tab
3. Refresh the page
4. Click any request to leetcode.com
5. Find **Cookie** in Request Headers
6. Copy the entire cookie string
7. Save to `.leetcode_cookies` file:

```bash
echo 'YOUR_COOKIE_STRING_HERE' > .leetcode_cookies
```

**Important cookies needed:**
- `LEETCODE_SESSION`
- `csrftoken`

---

## Running the Crawler

### The Crawler Script

Save as `fetch_leetcode_contests.py`:

```python
#!/usr/bin/env python3
"""
Fetch LeetCode contest data and save as markdown files.
"""
import json
import subprocess
import os
import re
import html
from datetime import datetime

COOKIES_FILE = ".leetcode_cookies"
OUTPUT_DIR = "problem_soulutions/leetcode_contests"

def load_cookies():
  with open(COOKIES_FILE, 'r') as f:
    return f.read().strip()

def fetch_contest_list():
  """Fetch list of all contests via GraphQL"""
  cookies = load_cookies()
  query = '{"query":"query { allContests { title titleSlug startTime duration } }","variables":{}}'

  cmd = f'''curl -s 'https://leetcode.com/graphql/' \
    -H 'content-type: application/json' \
    -b '{cookies}' \
    -H 'user-agent: Mozilla/5.0' \
    --data-raw '{query}' '''

  result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
  data = json.loads(result.stdout)
  return data['data']['allContests']

def fetch_contest_details(title_slug):
  """Fetch details for a specific contest"""
  cookies = load_cookies()
  url = f'https://leetcode.com/contest/api/info/{title_slug}/'

  cmd = f'''curl -s '{url}' \
    -b '{cookies}' \
    -H 'user-agent: Mozilla/5.0' '''

  result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
  return json.loads(result.stdout)

def fetch_problem_description(title_slug):
  """Fetch problem description via GraphQL"""
  cookies = load_cookies()
  query = json.dumps({
    "query": "query { question(titleSlug: \"" + title_slug + "\") { content difficulty exampleTestcases } }",
    "variables": {}
  })

  cmd = f'''curl -s 'https://leetcode.com/graphql/' \
    -H 'content-type: application/json' \
    -b '{cookies}' \
    -H 'user-agent: Mozilla/5.0' \
    --data-raw '{query}' '''

  result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
  try:
    data = json.loads(result.stdout)
    return data['data']['question']
  except:
    return None

def html_to_markdown(html_content):
  """Convert HTML to markdown"""
  if not html_content:
    return ""

  text = html_content
  text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', text)
  text = re.sub(r'<code>(.*?)</code>', r'`\1`', text)
  text = re.sub(r'<pre>(.*?)</pre>', r'```\n\1\n```', text, flags=re.DOTALL)
  text = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1', text, flags=re.DOTALL)
  text = re.sub(r'<[^>]+>', '', text)
  text = html.unescape(text)
  text = re.sub(r'\n{3,}', '\n\n', text)
  return text.strip()

def main():
  os.makedirs(OUTPUT_DIR, exist_ok=True)
  print("Fetching contest list...")
  all_contests = fetch_contest_list()

  # Process recent contests
  for contest in all_contests[:15]:
    title_slug = contest['titleSlug']
    print(f"Fetching: {contest['title']}")

    try:
      details = fetch_contest_details(title_slug)
      if not details.get('questions'):
        continue
      # Generate markdown and save...
    except Exception as e:
      print(f"Error: {e}")

if __name__ == "__main__":
  main()
```

### Run the crawler:

```bash
python3 fetch_leetcode_contests.py
```

---

## Contest File Format

Each contest file follows this structure:

```markdown
---
layout: simple
title: "Weekly Contest 487"
permalink: /problem_soulutions/leetcode_contests/weekly-contest-487/
---

# Weekly Contest 487

## Contest Information

| Field | Value |
|-------|-------|
| **Date** | February 01, 2026 |
| **Time** | 09:30 UTC |
| **Duration** | 90 minutes |
| **Contest Link** | [LeetCode](https://leetcode.com/contest/weekly-contest-487/) |

---

## Problems

### Q1. Problem Title Here

| Field | Value |
|-------|-------|
| **Difficulty** | Easy |
| **Points** | 3 |
| **Link** | [LeetCode](https://leetcode.com/problems/problem-slug/) |

#### Problem Description

Problem description text here...

**Example 1:**

**Input:** nums = [1,2,3]

**Output:** 6

**Constraints:**

- `1 <= nums.length <= 10^5`

<details markdown="1">
<summary><strong>💡 Hints & Approach</strong></summary>

**Key Insight:** Brief description of the core idea.

**Hint 1:** First progressive hint.

**Hint 2:** Second progressive hint.

**Approach:**
1. Step one
2. Step two
3. Step three

```python
def solutionFunction(nums):
  # 2-space indentation
  result = 0
  for x in nums:
    result += x
  return result
```

**Time Complexity:** O(n)
**Space Complexity:** O(1)

</details>

---

### Q2. Next Problem...
```

---

## Adding Hints & Approaches

### Hint Structure

Each problem should have a collapsible `<details>` section with:

1. **Key Insight** - The core algorithmic idea (1-2 sentences)
2. **Progressive Hints** - 2-4 hints that guide without giving away the solution
3. **Approach** - Step-by-step algorithm explanation
4. **Python Code** - Clean solution with 2-space indentation
5. **Complexity Analysis** - Time and space complexity

### Template for Hints Section

```markdown
<details markdown="1">
<summary><strong>💡 Hints & Approach</strong></summary>

**Key Insight:** [Core algorithmic idea - what makes this problem solvable]

**Hint 1:** [First hint - identify the pattern or data structure]

**Hint 2:** [Second hint - how to approach the problem]

**Hint 3:** [Third hint - edge cases or optimization]

**Approach:**
1. [First step]
2. [Second step]
3. [Third step]

```python
def solutionFunction(params):
  # Implementation with 2-space indentation
  pass
```

**Time Complexity:** O(...)
**Space Complexity:** O(...)

</details>
```

### Common Algorithm Patterns

| Pattern | When to Use | Key Insight Example |
|---------|-------------|---------------------|
| **Two Pointers** | Sorted arrays, palindromes | "Use left/right pointers moving inward" |
| **Sliding Window** | Subarray/substring problems | "Maintain a window with specific property" |
| **Binary Search** | Sorted data, optimization | "Search space can be halved each step" |
| **BFS/DFS** | Graph traversal, grids | "Explore level by level / depth first" |
| **Dynamic Programming** | Optimal substructure | "Build solution from smaller subproblems" |
| **Greedy** | Local optimal = global optimal | "Always pick the best choice at each step" |
| **Hash Map** | Frequency counting, lookup | "Store seen elements for O(1) lookup" |
| **Stack/Queue** | Matching, monotonic sequences | "Track elements in LIFO/FIFO order" |
| **Union-Find** | Connected components | "Group elements by connectivity" |
| **Bit Manipulation** | XOR, subsets | "Use bits to represent states" |

### Difficulty-Based Hint Guidelines

#### Easy (Q1) - 3 points
- Usually straightforward simulation or basic data structures
- 1-2 hints sufficient
- Focus on edge cases

#### Medium (Q2, Q3) - 4-5 points
- Requires recognizing a pattern or technique
- 2-3 hints to guide toward the approach
- Include optimization if naive solution is too slow

#### Hard (Q4) - 6-7 points
- Often combines multiple techniques
- 3-4 hints building up to the solution
- May need to explain the key observation that makes it tractable

---

## Updating Navigation

After adding new contests, update `_data/navigation.yml`:

```yaml
- title: LeetCode Contests
  url: /cses-analyses/problem_soulutions/leetcode_contests/
  children:
  - title: Weekly Contest 487
    url: /cses-analyses/problem_soulutions/leetcode_contests/weekly-contest-487/
  - title: Weekly Contest 488
    url: /cses-analyses/problem_soulutions/leetcode_contests/weekly-contest-488/
  # Add new contests here...
```

Also update the index page at `problem_soulutions/leetcode_contests/index.md` with the new contest entries.

---

## Workflow Summary

1. **Crawl contests**: `python3 fetch_leetcode_contests.py`
2. **Review generated files**: Check `problem_soulutions/leetcode_contests/`
3. **Add hints/approaches**: Fill in the `<details>` sections for each problem
4. **Update navigation**: Add entries to `_data/navigation.yml`
5. **Update index**: Add to `problem_soulutions/leetcode_contests/index.md`
6. **Commit and push**:
   ```bash
   git add problem_soulutions/leetcode_contests/ _data/navigation.yml
   git commit -m "feat: add LeetCode Contest XXX with hints"
   git push
   ```

---

## Tips for Writing Good Hints

1. **Don't give away the answer** - Hints should guide, not solve
2. **Be progressive** - Each hint should build on the previous
3. **Focus on the "why"** - Explain why a technique works, not just what to do
4. **Include complexity** - Help readers understand efficiency
5. **Use 2-space indentation** - Keep Python code consistent
6. **Test your solution** - Verify code works before adding
