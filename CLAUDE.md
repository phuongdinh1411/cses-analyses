# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Development Commands

```bash
# Install dependencies
bundle install

# Run local development server
bundle exec jekyll serve
# Site available at http://localhost:4000/cses-analyses/

# Build static site (for production)
bundle exec jekyll build
```

## Project Overview

Jekyll-based static site for competitive programming (CSES, LeetCode, Codeforces) and system design interview preparation. Uses Minimal Mistakes theme with Kramdown/GFM markdown.

**Live Site:** https://phuongdinh1411.github.io/cses-analyses/

## Architecture

```
problem_soulutions/          # CP problems by category (note: intentional typo in folder name)
├── {category}/summary.md    # Category overview with problem list
├── {category}/*_analysis.md # Individual problem analyses
├── Blue/                    # Blue-level curriculum (DSA foundations)
├── Orange/                  # Orange-level curriculum (advanced topics)
└── leetcode_contests/       # LeetCode weekly/biweekly contest solutions

system_design/               # System design interview guides
├── TEMPLATE.md              # Template for new system designs
└── design-*.md              # Individual system designs (YouTube, Chat, etc.)

_data/navigation.yml         # Sidebar navigation structure (edit for new pages)
_config.yml                  # Jekyll config (baseurl: /cses-analyses)
```

## Content Patterns

### Adding Problem Solutions

1. Create `problem_soulutions/{category}/{problem_name}_analysis.md`
2. Include front matter with `layout: simple`, `title`, `permalink`
3. Structure: Problem statement → Brute force → Optimal → Complexity → Edge cases
4. Add entry to `_data/navigation.yml` under appropriate category

### Adding System Design Guides

1. Copy `system_design/TEMPLATE.md` to `system_design/design-{name}.md`
2. Follow interview-style format with:
   - "Interview context" transition phrases
   - Trade-off tables for design decisions
   - "Why not X?" sections for alternatives
   - "Interviewer might ask" follow-up questions
3. Add to navigation under System Design section

### Front Matter Required

```yaml
---
layout: simple
title: "Problem/Design Title"
permalink: /problem_soulutions/{category}/{problem_name}
---
```

## Navigation Updates

All content requires a navigation entry in `_data/navigation.yml`. Structure:
- Top-level: `main` array with title/url/children
- Nested categories use `children` arrays
- URLs must include `/cses-analyses/` prefix (baseurl)
