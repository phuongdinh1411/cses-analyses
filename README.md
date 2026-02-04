# CSES Analyses & System Design

A comprehensive learning resource for **competitive programming** and **system design interviews**.

**Live Site: [https://phuongdinh1411.github.io/cses-analyses/](https://phuongdinh1411.github.io/cses-analyses/)**

---

## Table of Contents

- [System Design](#system-design)
- [CSES Problem Set](#cses-problem-set)
- [Quick Reference](#quick-reference)
- [Repository Structure](#repository-structure)
- [Local Development](#local-development)
- [Resources](#resources)

---

## System Design

### Available Guides (12 Topics)

| System | Key Concepts | Trade-offs |
|--------|--------------|------------|
| [YouTube](system_design/design-youtube.md) | Transcoding, CDN, ABR streaming | Storage cost vs latency |
| [Chat System](system_design/design-chat-system.md) | WebSocket, presence, delivery | Push vs pull |
| [News Feed](system_design/design-news-feed.md) | Fan-out, ranking, caching | Push vs pull vs hybrid |
| [URL Shortener](system_design/design-url-shortener.md) | Base62, key generation | Predictability vs security |
| [Search Autocomplete](system_design/design-search-autocomplete.md) | Trie, multi-level caching | Freshness vs latency |
| [Payment System](system_design/design-payment-system.md) | Idempotency, reconciliation | Sync vs async |
| [Web Crawler](system_design/design-web-crawler.md) | URL frontier, politeness | Breadth vs depth |
| [Key-Value Store](system_design/design-key-value-store.md) | Consistent hashing, replication | Consistency vs availability |
| [Unique ID Generator](system_design/design-unique-id-generator.md) | Snowflake, ULID | Sortability vs randomness |
| [Consistent Hashing](system_design/consistent-hashing.md) | Hash ring, virtual nodes | Distribution vs complexity |
| [Skills GraphRAG](system_design/design-skills-graphrag.md) | Graph + RAG, LLM integration | Latency vs accuracy |

### Interview Format

Each guide follows an **interview-style format**:
- **"Interview context"** - Transition phrases between topics
- **"Why not X?"** - Discussion of alternatives considered
- **"Interviewer might ask"** - Common follow-up questions
- **Trade-off tables** - Decision rationale
- **Interview tips** - Key phrases and approach

### 5-Step Framework (45 minutes)

| Step | Time | Focus |
|------|------|-------|
| 1. Requirements | 5 min | Clarify scope, scale, constraints |
| 2. Estimation | 5 min | QPS, storage, bandwidth |
| 3. High-Level Design | 10 min | Components, data flow, APIs |
| 4. Deep Dive | 20 min | 2-3 key areas in detail |
| 5. Wrap Up | 5 min | Trade-offs, bottlenecks, improvements |

### Key Phrases

| Instead of... | Say... |
|---------------|--------|
| "Use a database" | "Given the read-heavy workload, I'd use MySQL with read replicas" |
| "Add caching" | "Add Redis with a TTL of X based on data staleness tolerance" |
| "Scale horizontally" | "At this QPS, we need N servers assuming Y requests/server" |

---

## CSES Problem Set

### Problem Categories (240+ Problems)

| Category | Problems | Topics |
|----------|----------|--------|
| [Introductory Problems](problem_soulutions/introductory_problems/summary.md) | 25 | Basics, implementation |
| [Sorting and Searching](problem_soulutions/sorting_and_searching/summary.md) | 35 | Binary search, two pointers |
| [Dynamic Programming](problem_soulutions/dynamic_programming/summary.md) | 17 | Knapsack, grid DP, string DP |
| [Graph Algorithms](problem_soulutions/graph_algorithms/summary.md) | 36 | DFS, BFS, shortest paths, SCC |
| [Tree Algorithms](problem_soulutions/tree_algorithms/summary.md) | 15 | LCA, tree DP, binary lifting |
| [Range Queries](problem_soulutions/range_queries/summary.md) | 20 | Segment tree, BIT, sparse table |
| [String Algorithms](problem_soulutions/string_algorithms/summary.md) | 14 | KMP, Z-algorithm, suffix array |
| [Geometry](problem_soulutions/geometry/summary.md) | 16 | Convex hull, line intersection |
| [Advanced Graph](problem_soulutions/advanced_graph_problems/summary.md) | 28 | Max flow, matching, Euler path |
| [Counting](problem_soulutions/counting_problems/summary.md) | 19 | Combinatorics, inclusion-exclusion |

### What's in Each Problem

- Step-by-step solution (brute force → optimal)
- Time/space complexity analysis
- Key insights and techniques
- Edge cases and common mistakes
- Related problems

### Constraints → Algorithm

| Constraint | Complexity | Approach |
|------------|------------|----------|
| n ≤ 10 | O(n!) | Brute force, permutations |
| n ≤ 20 | O(2^n) | Bitmask DP |
| n ≤ 500 | O(n³) | Floyd-Warshall, matrix |
| n ≤ 5000 | O(n²) | Standard DP |
| n ≤ 10⁶ | O(n log n) | Sorting, binary search |
| n ≤ 10⁸ | O(n) | Linear scan |

### Keywords → Algorithm

| Keyword | Algorithm |
|---------|-----------|
| "shortest path" | Dijkstra, BFS, Bellman-Ford |
| "connected components" | DFS, Union-Find |
| "minimum/maximum" | DP, greedy |
| "substring/subsequence" | DP, sliding window |
| "range query" | Segment tree, BIT |
| "topological" | DFS, Kahn's algorithm |

---

## Quick Reference

| Guide | Description |
|-------|-------------|
| [Study Guide](quick_reference/study_guide.md) | Learning path and strategy |
| [Code Templates](quick_reference/code_templates.md) | Ready-to-use implementations |
| [Advanced Algorithms](quick_reference/advanced_algorithms.md) | Complex techniques |
| [Common Mistakes](quick_reference/common_mistakes.md) | Pitfalls to avoid |

---

## Repository Structure

```
cses_analyses/
├── system_design/              # System design interview guides
│   ├── index.md                # Overview and framework
│   ├── TEMPLATE.md             # Template for new designs
│   ├── design-youtube.md
│   ├── design-chat-system.md
│   └── ...
├── problem_soulutions/         # CSES problem analyses
│   ├── introductory_problems/
│   ├── dynamic_programming/
│   ├── graph_algorithms/
│   └── ...
├── quick_reference/            # Cheatsheets and guides
└── _data/navigation.yml        # Site navigation
```

---

## Local Development

```bash
# Install Jekyll
gem install bundler jekyll

# Install dependencies
bundle install

# Run locally
bundle exec jekyll serve

# Open http://localhost:4000/cses-analyses/
```

---

## Resources

### System Design
- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [Designing Data-Intensive Applications](https://dataintensive.net/)
- [Google SRE Book](https://sre.google/sre-book/table-of-contents/)

### Competitive Programming
- [CSES Problem Set](https://cses.fi/problemset/)
- [LeetCode](https://leetcode.com/)
- [Codeforces](https://codeforces.com/)
- [AtCoder](https://atcoder.jp/)

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Follow existing patterns (use `TEMPLATE.md` for system design)
4. Submit a pull request
