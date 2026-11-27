---
layout: simple
title: "Course Schedule II - Reverse Topological Sort with Max-Heap"
permalink: /problem_soulutions/advanced_graph_problems/course_schedule_ii_analysis
difficulty: Hard
tags: [topological-sort, graph, heap, greedy, kahn-algorithm]
prerequisites: [course_schedule, topological_sorting]
---

# Course Schedule II

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Course Schedule II](https://cses.fi/problemset/task/1757) |
| **Difficulty** | Hard |
| **Category** | Graph / Topological Sort |
| **Time Limit** | 1 second |
| **Key Technique** | Kahn's Algorithm on the Reversed Graph with a Max-Heap |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Explain why "lexicographically smallest topological order" is not "course 1 as early as possible"
- [ ] Build an order from the back by reversing the graph
- [ ] Use a max-heap to decide which course goes last
- [ ] Prove a greedy choice with an exchange argument

---

## Problem Statement

**Problem:** There are n courses and m requirements of the form "course a has to be completed before course b". Complete course 1 as early as possible; among those schedules, complete course 2 as early as possible; and so on. Print the resulting order.

**Input:**
- Line 1: Two integers n and m (number of courses and requirements)
- Next m lines: Two integers a and b: course a must be completed before course b

**Output:**
- One line with n integers: the order in which the courses are completed

**Constraints:**
- 1 <= n <= 10^5
- 1 <= m <= 2 * 10^5
- 1 <= a, b <= n
- At least one valid schedule exists (the graph is acyclic)

### Example

```
Input:
4 2
2 1
2 3

Output:
2 1 3 4
```

**Explanation:** Course 1 needs course 2 first, so the earliest course 1 can be completed is second: `2 1`. Then course 3 (its only requirement, 2, is done), then 4.

A case where the "obvious" greedy fails:

```
Input:
3 1
3 1

Output:
3 1 2
```

Taking the smallest available course first gives `2 3 1`, which puts course 1 third. The required answer puts it second.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** Kahn's algorithm with a min-heap gives the lexicographically smallest order. Why isn't that enough?

Lexicographically smallest compares the *sequence of courses*: it wants a small course at position 1, then at position 2. This problem compares the *positions of courses*: course 1 must be as early as possible, even if that means taking a large course first. In the second example, `2 3 1` < `3 1 2` lexicographically, yet `3 1 2` is what we want.

### The Reversal Trick

Look at the schedule from the end. The last course can be any course that no other course depends on. Which one should go last? **The largest such course.** Pushing a large course to the end never delays a smaller one, while putting a small course last would make it as late as possible.

So: reverse every edge, run Kahn's algorithm with a **max-heap** to build the schedule back to front, then reverse the result.

### Why the Greedy Is Correct (Sketch)

Suppose the largest available course x is not last in an optimal schedule; some y < x is last instead. Both have no dependents left, so moving x to the end keeps the schedule valid. Courses smaller than x keep or improve their positions, and y moves one place earlier. That is no worse in the "course 1 first, then course 2…" comparison, so some optimal schedule ends with x. Repeat on the remaining courses.

---

## Solution 1: Brute Force

### Idea

Try all n! orders, keep the valid ones, and pick the one whose position vector (position of course 1, position of course 2, ...) is lexicographically smallest.

```python
from itertools import permutations

def brute_force(n, edges):
  best = None
  for order in permutations(range(1, n + 1)):
    pos = [0] * (n + 1)
    for i, c in enumerate(order):
      pos[c] = i
    if all(pos[a] < pos[b] for a, b in edges):
      key = pos[1:]
      if best is None or key < best[0]:
        best = (key, order)
  return list(best[1])
```

**Time:** O(n! * (n + m)): usable only to check small cases.

---

## Solution 2: Optimal - Reverse Graph + Max-Heap

### Algorithm

1. For each requirement `a b`, add the reversed edge b -> a and count `out[a] += 1` (how many courses still have to come after a).
2. Push every course with `out = 0` into a max-heap.
3. Repeatedly pop the largest course x and append it to `rev`. For each reversed edge x -> a, decrement `out[a]`; push a when it reaches 0.
4. Print `rev` reversed.

### Dry Run Example

Input `4 2 / 2 1 / 2 3`:

```
Reversed edges: 1 -> 2, 3 -> 2        out[2] = 2, others 0

Heap {1, 3, 4}   pop 4   rev = [4]
Heap {1, 3}      pop 3   rev = [4, 3]         out[2]: 2 -> 1
Heap {1}         pop 1   rev = [4, 3, 1]      out[2]: 1 -> 0, push 2
Heap {2}         pop 2   rev = [4, 3, 1, 2]

Reverse: 2 1 3 4
```

### Code (Python)

```python
import sys
import heapq

def main():
  data = sys.stdin.buffer.read().split()
  n, m = int(data[0]), int(data[1])

  radj = [[] for _ in range(n + 1)]
  out = [0] * (n + 1)
  for i in range(m):
    a, b = int(data[2 + 2 * i]), int(data[3 + 2 * i])
    radj[b].append(a)
    out[a] += 1

  heap = [-c for c in range(1, n + 1) if out[c] == 0]
  heapq.heapify(heap)

  rev = []
  while heap:
    x = -heapq.heappop(heap)
    rev.append(x)
    for a in radj[x]:
      out[a] -= 1
      if out[a] == 0:
        heapq.heappush(heap, -a)

  print(" ".join(map(str, reversed(rev))))

if __name__ == "__main__":
  main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n + m) | Each course is pushed and popped once; each edge is relaxed once |
| Space | O(n + m) | Reversed adjacency list and heap |

---

## Common Mistakes

### Mistake 1: Min-Heap on the Forward Graph

```python
# WRONG - lexicographically smallest order, not "course 1 earliest"
heap = [c for c in range(1, n + 1) if indeg[c] == 0]
x = heapq.heappop(heap)        # 3 1 / 3 1 -> 2 3 1
```

**Problem:** Taking a small course early can delay course 1.
**Fix:** Build from the back: reversed graph, max-heap, reverse the result.

### Mistake 2: Reading the Requirement Backwards

CSES means "a before b". The forward edge is a -> b, so the reversed edge used here is b -> a, and it is `a` whose count drops when `b` is placed.

### Mistake 3: Forgetting the Final Reverse

`rev` lists courses from last to first. Printing it directly gives the schedule backwards.

---

## Edge Cases

| Case | Input | Expected | Why |
|------|-------|----------|-----|
| No requirements | `3 0` | `1 2 3` | Every course is free; smallest first |
| Course 1 has a long chain | `3 2 / 3 2 / 2 1` | `3 2 1` | 1 can only come after its ancestors |
| Smallest-first trap | `3 1 / 3 1` | `3 1 2` | Not `2 3 1` |
| Duplicate requirement | `2 2 / 1 2 / 1 2` | `1 2` | Counts handle repeated edges |
| Single course | `1 0` | `1` | Trivial |

---

## When to Use This Pattern

### Use This Approach When:
- The objective is "item 1 as early as possible, then item 2, ..." under precedence constraints
- A min-heap topological sort gives a plausible but wrong answer on small tests

### Don't Use When:
- Any valid order is accepted: plain Kahn's algorithm is enough ([Course Schedule](https://cses.fi/problemset/task/1679))
- The lexicographically smallest sequence is asked for: forward graph with a min-heap

### Pattern Recognition Checklist:
- [ ] Precedence constraints + "minimise positions in priority order"? -> **Reverse graph, max-heap**
- [ ] Precedence constraints + "smallest sequence"? -> **Forward graph, min-heap**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Course Schedule (CSES 1679)](https://cses.fi/problemset/task/1679) | Plain topological sort with cycle detection |
| [Longest Flight Route (CSES 1680)](https://cses.fi/problemset/task/1680) | DP over a topological order |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Game Routes (CSES 1681)](https://cses.fi/problemset/task/1681) | Count paths in a DAG |
| [Course Schedule II (LeetCode 210)](https://leetcode.com/problems/course-schedule-ii/) | Any valid order (with cycle detection) |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Planets and Kingdoms (CSES 1683)](https://cses.fi/problemset/task/1683) | Strongly connected components |
| [Round Trip II (CSES 1678)](https://cses.fi/problemset/task/1678) | Find an actual directed cycle |

---

## Key Takeaways

1. **The Core Idea:** To make small courses early, decide the *last* course first: the largest course with no remaining dependents.
2. **Technique:** Kahn's algorithm on the reversed graph with a max-heap, then reverse.
3. **Trap:** The lexicographically smallest topological order answers a different question.
4. **Proof Tool:** An exchange argument justifies the greedy choice at the end of the schedule.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Give a 3-course example where the min-heap greedy fails
- [ ] Implement the reversed max-heap version from memory
- [ ] Explain the exchange argument in two sentences
