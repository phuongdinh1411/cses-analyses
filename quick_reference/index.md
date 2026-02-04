---
layout: simple
title: "Quick Reference"
permalink: /quick_reference
---

# Quick Reference

Fast access to essential algorithms and problem-solving strategies.

## Contents

| Resource | Description |
|----------|-------------|
| [Study Guide](/cses-analyses/quick_reference/study_guide) | Learning path, pattern recognition, interview patterns |
| [Code Templates](/cses-analyses/quick_reference/code_templates) | Ready-to-use algorithm implementations |
| [Advanced Algorithms](/cses-analyses/quick_reference/advanced_algorithms) | FFT, HLD, Persistent Segment Tree, etc. |
| [Common Mistakes](/cses-analyses/quick_reference/common_mistakes) | Pitfalls to avoid |

## Quick Decision Guide

| I see... | I think... | I use... |
|----------|------------|----------|
| Sorted array | Binary search | `bisect_left/right` |
| Subarray sum | Prefix sum | `prefix[r] - prefix[l]` |
| Next greater | Monotonic stack | `while stack and ...` |
| Shortest path | BFS (unweighted) | `deque + visited` |
| Min/max path | Dijkstra | `heapq + distance` |
| Connected? | Union-Find | `find + union` |
| Count ways | DP | `dp[i] = ...` |

## Constraint-Based Selection

| Constraint | Max Complexity | Examples |
|------------|----------------|----------|
| n <= 10 | O(n!) | Brute force |
| n <= 20 | O(2^n) | Bitmask DP |
| n <= 500 | O(n^3) | Floyd-Warshall |
| n <= 5000 | O(n^2) | Simple DP |
| n <= 10^5 | O(n log n) | Sorting, Segment Tree |
| n <= 10^6 | O(n) | Linear scan |
