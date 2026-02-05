---
layout: simple
title: "Movie Festival"
permalink: /problem_soulutions/sorting_and_searching/movie_festival_analysis
difficulty: Easy
tags: [sorting, greedy, interval-scheduling]
cses_link: https://cses.fi/problemset/task/1629
---

# Movie Festival

## Problem Overview

| Aspect | Details |
|--------|---------|
| Problem Type | Interval Scheduling / Activity Selection |
| Technique | Greedy Algorithm |
| Time Complexity | O(n log n) |
| Space Complexity | O(1) |
| Key Operation | Sort by end time, greedy selection |

## Learning Goals

By completing this problem, you will learn:
- The classic **interval scheduling** problem pattern
- Why **sorting by end time** leads to the optimal greedy solution
- How greedy algorithms can achieve optimal solutions when the greedy choice property holds

## Problem Statement

Given n movies with start and end times, find the maximum number of movies you can watch without overlapping. You can only watch one movie at a time.

**Input:**
- First line: integer n (1 <= n <= 2x10^5)
- Next n lines: two integers a and b (start and end time, 1 <= a <= b <= 10^9)

**Output:** Maximum number of non-overlapping movies

**Example:**
```
Input:
3
3 5
4 9
5 8

Output:
2
```

## Key Insight

**Sort movies by END time, then greedily take the earliest-ending movie that doesn't conflict with your last selection.**

This greedy approach is provably optimal for the activity selection problem.

## Why Sort by End Time?

Sorting by end time **leaves maximum room for future movies**.

When you pick a movie that ends early, you maximize the remaining time window for subsequent movies. This is the essence of the greedy choice property.

**Intuition:** Imagine you're filling a timeline. The earlier a movie ends, the more space remains for other movies.

```
Timeline: |---------------------------------------------->

Movie A (ends early):    [====]
                              ^-- lots of room left

Movie B (ends late):     [================]
                                          ^-- less room left
```

## Algorithm

1. **Sort** all movies by their end time (ascending)
2. **Initialize** `last_end = 0` (tracks when your last movie ended)
3. **For each movie** in sorted order:
   - If `start >= last_end`: take this movie, update `last_end = end`
   - Otherwise: skip (conflicts with previous selection)
4. **Return** the count of movies taken

## Visual Diagram

```
Original movies:
  Movie 1: [3----5]
  Movie 2: [4---------9]
  Movie 3:    [5----8]

After sorting by END time:
  Movie 1: [3----5]       (ends at 5)
  Movie 3:    [5----8]    (ends at 8)
  Movie 2: [4---------9]  (ends at 9)

Greedy Selection:
  Step 1: last_end = 0
          Movie 1 starts at 3 >= 0? YES -> Take it, last_end = 5

  Step 2: last_end = 5
          Movie 3 starts at 5 >= 5? YES -> Take it, last_end = 8

  Step 3: last_end = 8
          Movie 2 starts at 4 >= 8? NO -> Skip

  Result: 2 movies selected [Movie 1, Movie 3]
```

## Dry Run

| Step | Movie (start, end) | last_end | start >= last_end? | Action | Count |
|------|-------------------|----------|-------------------|--------|-------|
| 0 | - | 0 | - | Initialize | 0 |
| 1 | (3, 5) | 0 | 3 >= 0 = YES | Take, last_end = 5 | 1 |
| 2 | (5, 8) | 5 | 5 >= 5 = YES | Take, last_end = 8 | 2 |
| 3 | (4, 9) | 8 | 4 >= 8 = NO | Skip | 2 |

**Final Answer: 2**

## Python Solution

```python
def solve():
  n = int(input())
  movies = []
  for _ in range(n):
    a, b = map(int, input().split())
    movies.append((a, b))

  # Sort by end time
  movies.sort(key=lambda x: x[1])

  count = 0
  last_end = 0

  for start, end in movies:
    if start >= last_end:
      count += 1
      last_end = end

  print(count)

solve()
```

## Why Not Sort by Start Time or Duration?

### Counter-example: Sorting by Start Time

```
Movies: (1, 100), (2, 3), (4, 5)

Sort by start time: (1, 100), (2, 3), (4, 5)
Greedy result: Take (1, 100) -> blocks everything else
Result: 1 movie

Optimal (sort by end): (2, 3), (4, 5), (1, 100)
Take (2, 3), then (4, 5)
Result: 2 movies
```

Sorting by start time fails because an early-starting movie might span a long time, blocking many shorter movies.

### Counter-example: Sorting by Duration

```
Movies: (1, 3), (2, 4), (3, 5)
Durations: 2, 2, 2 (all same)

Any order might work, but consider:
Movies: (1, 2), (1, 10), (2, 3)
Durations: 1, 9, 1

Sort by duration: (1, 2), (2, 3), (1, 10)
Take (1, 2), then (2, 3) -> 2 movies (happens to work)

But: (0, 5), (1, 3), (3, 6)
Durations: 5, 2, 3

Sort by duration: (1, 3), (3, 6), (0, 5)
Take (1, 3), then (3, 6) -> 2 movies

Sort by end: (1, 3), (0, 5), (3, 6)
Take (1, 3), then (3, 6) -> 2 movies

The issue: (0, 3), (2, 5), (4, 7), (1, 8)
Durations: 3, 3, 3, 7

Sort by duration: (0, 3), (2, 5), (4, 7), (1, 8)
Take (0, 3), skip (2, 5), take (4, 7) -> 2 movies

But (1, 8) with duration 7 could block good intervals.
```

**Key insight:** Duration doesn't account for *where* the movie sits on the timeline. End time directly controls how much timeline remains.

## Common Mistakes

### 1. Sorting by Start Time Instead of End Time

```python
# WRONG
movies.sort(key=lambda x: x[0])  # Sort by start time

# CORRECT
movies.sort(key=lambda x: x[1])  # Sort by end time
```

### 2. Using Strict Inequality Instead of >=

```python
# WRONG - misses back-to-back movies
if start > last_end:

# CORRECT - allows movie starting exactly when previous ends
if start >= last_end:
```

A movie can start at the exact moment another ends. If Movie A ends at time 5, Movie B can start at time 5.

### 3. Not Handling Large Inputs Efficiently

- Use fast I/O in C++ (`ios::sync_with_stdio(false)`)
- Avoid unnecessary data structures
- The algorithm is O(n log n) due to sorting; the greedy selection is O(n)

## Complexity Analysis

| Operation | Time Complexity |
|-----------|----------------|
| Sorting | O(n log n) |
| Greedy Selection | O(n) |
| **Total** | **O(n log n)** |

**Space Complexity:** O(1) extra space (or O(n) for storing movies)

## Related Problems

- [CSES - Movie Festival II](https://cses.fi/problemset/task/1630) (Multiple members)
- [LeetCode 435 - Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/)
- [LeetCode 452 - Minimum Arrows to Burst Balloons](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/)
