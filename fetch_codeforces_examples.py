#!/usr/bin/env python3
"""
Fetch examples from Codeforces problems and add them to B/O markdown files.
"""
import os
import re
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path

BLUE_DIR = "problem_soulutions/Blue"
ORANGE_DIR = "problem_soulutions/Orange"

# Headers to mimic browser
HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

def extract_cf_link(content):
  """Extract Codeforces problem URL from markdown content."""
  # Match patterns like [Codeforces 691A](https://codeforces.com/problemset/problem/691/A)
  # or [Codeforces](https://codeforces.com/contest/691/problem/A)
  patterns = [
    r'https://codeforces\.com/problemset/problem/(\d+)/([A-Z]\d?)',
    r'https://codeforces\.com/contest/(\d+)/problem/([A-Z]\d?)',
  ]

  for pattern in patterns:
    match = re.search(pattern, content)
    if match:
      contest_id = match.group(1)
      problem_id = match.group(2)
      return f"https://codeforces.com/problemset/problem/{contest_id}/{problem_id}", contest_id, problem_id

  return None, None, None

def fetch_cf_examples(url):
  """Fetch examples from a Codeforces problem page."""
  try:
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    examples = []
    sample_tests = soup.find('div', class_='sample-test')

    if not sample_tests:
      return None

    inputs = sample_tests.find_all('div', class_='input')
    outputs = sample_tests.find_all('div', class_='output')

    for i, (inp, out) in enumerate(zip(inputs, outputs)):
      input_pre = inp.find('pre')
      output_pre = out.find('pre')

      if input_pre and output_pre:
        # Handle different pre formats (some have <br>, some have <div>)
        input_text = get_pre_text(input_pre)
        output_text = get_pre_text(output_pre)

        examples.append({
          'input': input_text.strip(),
          'output': output_text.strip()
        })

    return examples if examples else None

  except Exception as e:
    print(f"    Error fetching {url}: {e}")
    return None

def get_pre_text(pre_element):
  """Extract text from pre element, handling various formats."""
  # Replace <br> with newlines
  for br in pre_element.find_all('br'):
    br.replace_with('\n')

  # Handle divs inside pre
  for div in pre_element.find_all('div'):
    div.insert_after('\n')
    div.unwrap()

  return pre_element.get_text()

def format_examples(examples):
  """Format examples as markdown."""
  if not examples:
    return None

  md = "\n## Examples\n"

  for i, ex in enumerate(examples, 1):
    md += f"\n**Example {i}:**\n"
    md += f"\n**Input:**\n```\n{ex['input']}\n```\n"
    md += f"\n**Output:**\n```\n{ex['output']}\n```\n"

  return md

def has_examples_section(content):
  """Check if the file already has an Examples section."""
  return bool(re.search(r'^##\s+Examples?\s*$', content, re.MULTILINE))

def insert_examples(content, examples_md):
  """Insert examples section after Input/Output Format or Problem Statement."""
  # Try to insert after Output Format section
  patterns = [
    (r'(##\s+Output\s+Format\s*\n(?:.*?\n)*?)(\n##\s+Solution)', r'\1' + examples_md + r'\2'),
    (r'(##\s+Output\s*\n(?:.*?\n)*?)(\n##\s+Solution)', r'\1' + examples_md + r'\2'),
    (r'(####\s+Output\s+Format\s*\n(?:.*?\n)*?)(\n####\s+Solution)', r'\1' + examples_md + r'\2'),
    (r'(####\s+Output\s+Format\s*\n(?:.*?\n)*?)(\n---)', r'\1' + examples_md + r'\2'),
  ]

  for pattern, replacement in patterns:
    new_content, count = re.subn(pattern, replacement, content, count=1, flags=re.DOTALL)
    if count > 0:
      return new_content

  # Fallback: insert before Solution section
  solution_match = re.search(r'\n(#{2,4})\s+Solution', content)
  if solution_match:
    pos = solution_match.start()
    return content[:pos] + examples_md + content[pos:]

  return None

def process_file(filepath):
  """Process a single markdown file."""
  with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

  # Skip if already has examples
  if has_examples_section(content):
    return "skipped (has examples)"

  # Extract Codeforces link
  url, contest_id, problem_id = extract_cf_link(content)
  if not url:
    return "skipped (no CF link)"

  # Fetch examples
  examples = fetch_cf_examples(url)
  if not examples:
    return "skipped (no examples found)"

  # Format examples
  examples_md = format_examples(examples)

  # Insert into content
  new_content = insert_examples(content, examples_md)
  if not new_content:
    return "skipped (couldn't insert)"

  # Write back
  with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

  return f"updated ({len(examples)} examples)"

def find_md_files(directory):
  """Find all markdown files in directory."""
  md_files = []
  for root, dirs, files in os.walk(directory):
    for file in files:
      if file.endswith('.md'):
        md_files.append(os.path.join(root, file))
  return md_files

def main():
  # Find all markdown files
  files = []
  for directory in [BLUE_DIR, ORANGE_DIR]:
    if os.path.exists(directory):
      files.extend(find_md_files(directory))

  print(f"Found {len(files)} markdown files")
  print("-" * 50)

  stats = {
    'updated': 0,
    'skipped': 0,
    'errors': 0
  }

  for i, filepath in enumerate(files, 1):
    print(f"[{i}/{len(files)}] {filepath}")

    try:
      result = process_file(filepath)
      print(f"    -> {result}")

      if result.startswith("updated"):
        stats['updated'] += 1
        # Rate limiting to avoid being blocked
        time.sleep(1)
      else:
        stats['skipped'] += 1

    except Exception as e:
      print(f"    -> error: {e}")
      stats['errors'] += 1

  print("-" * 50)
  print(f"Done! Updated: {stats['updated']}, Skipped: {stats['skipped']}, Errors: {stats['errors']}")

if __name__ == "__main__":
  main()
