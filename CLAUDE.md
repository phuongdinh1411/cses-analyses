# CSES Analyses & System Design

A Jekyll-based learning resource for competitive programming (CSES, LeetCode, Codeforces) and system design interviews.

**Live Site:** https://phuongdinh1411.github.io/cses-analyses/

## Project Structure

```
cses_analyses/
├── system_design/           # System design interview guides (13 topics)
├── problem_soulutions/      # CP problem analyses by category
│   ├── introductory_problems/
│   ├── dynamic_programming/
│   ├── graph_algorithms/
│   ├── sorting_and_searching/
│   ├── Blue/                # Blue-level problems
│   └── Orange/              # Orange-level problems
├── quick_reference/         # Cheatsheets and study guides
├── _layouts/                # Jekyll layouts
├── _includes/               # Jekyll includes
├── _data/navigation.yml     # Site navigation
└── assets/                  # CSS and JS
```

## Tech Stack

- **Static Site Generator:** Jekyll with Minimal Mistakes theme
- **Hosting:** GitHub Pages
- **Markdown:** Kramdown with GFM support

## Local Development

```bash
bundle install
bundle exec jekyll serve
# Open http://localhost:4000/cses-analyses/
```

## Content Guidelines

### System Design
- Follow interview-style format with "Interview context" transitions
- Include trade-off tables and "Why not X?" discussions
- Use `system_design/TEMPLATE.md` for new designs

### Problem Solutions
- Include brute force to optimal progression
- Document time/space complexity
- Note edge cases and common mistakes

## Key Files

- `_config.yml` - Jekyll configuration
- `_data/navigation.yml` - Sidebar navigation
- `index.md` - Homepage
- `Gemfile` - Ruby dependencies
