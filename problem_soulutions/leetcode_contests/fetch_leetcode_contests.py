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
    -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' \
    -H 'referer: https://leetcode.com/' \
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
    -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' \
    -H 'referer: https://leetcode.com/' '''

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
    -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' \
    -H 'referer: https://leetcode.com/' \
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

  # Convert common HTML tags to markdown
  text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', text)
  text = re.sub(r'<b>(.*?)</b>', r'**\1**', text)
  text = re.sub(r'<em>(.*?)</em>', r'*\1*', text)
  text = re.sub(r'<i>(.*?)</i>', r'*\1*', text)
  text = re.sub(r'<code>(.*?)</code>', r'`\1`', text)
  text = re.sub(r'<pre>(.*?)</pre>', r'```\n\1\n```', text, flags=re.DOTALL)
  text = re.sub(r'<sup>(.*?)</sup>', r'^\1', text)
  text = re.sub(r'<sub>(.*?)</sub>', r'_\1', text)

  # Lists
  text = re.sub(r'<ul[^>]*>', '', text)
  text = re.sub(r'</ul>', '', text)
  text = re.sub(r'<ol[^>]*>', '', text)
  text = re.sub(r'</ol>', '', text)
  text = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1', text, flags=re.DOTALL)

  # Paragraphs and divs
  text = re.sub(r'<p[^>]*>', '\n', text)
  text = re.sub(r'</p>', '\n', text)
  text = re.sub(r'<div[^>]*>', '\n', text)
  text = re.sub(r'</div>', '\n', text)
  text = re.sub(r'<br\s*/?>', '\n', text)

  # Remove remaining HTML tags
  text = re.sub(r'<[^>]+>', '', text)

  # Decode HTML entities
  text = html.unescape(text)

  # Clean up whitespace
  text = re.sub(r'\n{3,}', '\n\n', text)
  text = text.strip()

  return text

def difficulty_to_str(diff):
  mapping = {1: 'Easy', 2: 'Medium', 3: 'Hard'}
  return mapping.get(diff, 'Unknown')

def generate_markdown(contest_data):
  """Generate markdown content for a contest"""
  contest = contest_data['contest']
  questions = contest_data['questions']

  title = contest['title']
  title_slug = contest['title_slug']
  start_time = datetime.fromtimestamp(contest['start_time'])
  duration_mins = contest['duration'] // 60

  md = f"""---
layout: simple
title: "{title}"
permalink: /problem_soulutions/leetcode_contests/{title_slug}/
---

# {title}

## Contest Information

| Field | Value |
|-------|-------|
| **Date** | {start_time.strftime('%B %d, %Y')} |
| **Time** | {start_time.strftime('%H:%M UTC')} |
| **Duration** | {duration_mins} minutes |
| **Contest Link** | [LeetCode](https://leetcode.com/contest/{title_slug}/) |

---

## Problems

"""

  for i, q in enumerate(questions, 1):
    q_title = q['title']
    slug = q['title_slug']
    diff = difficulty_to_str(q['difficulty'])
    credit = q['credit']

    md += f"""### Q{i}. {q_title}

| Field | Value |
|-------|-------|
| **Difficulty** | {diff} |
| **Points** | {credit} |
| **Link** | [LeetCode](https://leetcode.com/problems/{slug}/) |

"""

    # Fetch and add problem description
    print(f"    Fetching description for: {slug}")
    problem = fetch_problem_description(slug)
    if problem and problem.get('content'):
      description = html_to_markdown(problem['content'])
      md += f"""#### Problem Description

{description}

<details>
<summary><strong>💡 Hints & Approach</strong> (Click to expand)</summary>

*Hints coming soon...*

</details>

"""

    md += "---\n\n"

  return md

def main():
  os.makedirs(OUTPUT_DIR, exist_ok=True)

  # Fetch recent contests
  print("Fetching contest list...")
  all_contests = fetch_contest_list()

  # Process last 10 weekly and 5 biweekly contests
  weekly_count = 0
  biweekly_count = 0

  for contest in all_contests:
    if weekly_count >= 10 and biweekly_count >= 5:
      break

    title_slug = contest['titleSlug']

    if 'weekly' in title_slug and weekly_count < 10:
      weekly_count += 1
    elif 'biweekly' in title_slug and biweekly_count < 5:
      biweekly_count += 1
    else:
      continue

    print(f"Fetching: {contest['title']}")

    try:
      details = fetch_contest_details(title_slug)
      if not details.get('questions'):
        print(f"  Skipping (no problems yet)")
        continue

      md_content = generate_markdown(details)

      output_file = os.path.join(OUTPUT_DIR, f"{title_slug}.md")
      with open(output_file, 'w') as f:
        f.write(md_content)

      print(f"  Saved: {output_file}")
    except Exception as e:
      print(f"  Error: {e}")

if __name__ == "__main__":
  main()
