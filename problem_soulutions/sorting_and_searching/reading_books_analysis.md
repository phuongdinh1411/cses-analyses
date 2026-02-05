---
layout: simple
title: "Reading Books - Sorting and Searching Problem"
permalink: /problem_soulutions/sorting_and_searching/reading_books_analysis
difficulty: Easy
tags: [math, greedy, sorting]
prerequisites: []
---

# Reading Books

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Sorting and Searching |
| **Time Limit** | 1 second |
| **Key Technique** | Mathematical Analysis |
| **CSES Link** | [Reading Books](https://cses.fi/problemset/task/1631) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Identify problems where a simple mathematical formula provides the optimal solution
- [ ] Understand parallel processing constraints when resources cannot be shared simultaneously
- [ ] Derive the formula `max(2 * max_time, total)` for scheduling problems with blocking constraints
- [ ] Recognize when sorting is unnecessary and a single pass suffices

---

## Problem Statement

**Problem:** There are `n` books, and each book has a certain number of pages. Two people need to read all the books. Both people read all books, and they cannot read the same book at the same time. Find the minimum total time to read all books.

**Input:**
- Line 1: integer `n` (number of books)
- Line 2: `n` integers `t[1], t[2], ..., t[n]` (pages/time for each book)

**Output:**
- One integer: the minimum total time needed

**Constraints:**
- 1 <= n <= 2 * 10^5
- 1 <= t[i] <= 10^9

### Example

```
Input:
3
2 8 3

Output:
16
```

**Explanation:**
- Total pages: 2 + 8 + 3 = 13
- Maximum book: 8
- Since both people must read ALL books and cannot read the same book simultaneously:
  - If one person reads the longest book (8), the other person must wait or read other books
  - The answer is max(2 * 8, 13) = max(16, 13) = 16

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** Both people must read ALL books. They cannot read the same book at the same time. What determines the minimum time?

The critical insight is that this is NOT a book distribution problem. Both people read every book. The constraint is that they cannot read the same book simultaneously.

### Breaking Down the Problem

1. **What are we looking for?** The minimum time for both people to finish reading all books.
2. **What information do we have?** The reading time for each book.
3. **What's the relationship between input and output?** The answer depends on whether the longest book dominates or if there's enough "other work" to fill the gap.

### The Key Insight

Consider what happens when one person is reading a book:
- The other person MUST be reading a different book (they cannot read the same book)
- OR the other person must wait (if no other book is available)

**Case 1: The longest book is "too long"**
```
Books: [2, 8, 3]
Total = 13, Max = 8

Person A: [8]    [2][3]    = reads max first, then others
Person B: [2][3] [8]       = reads others first, then max

Timeline:
Time:     0    5    8    13   16
Person A: |--8--|     |2||3|
Person B: |2||3|      |--8--|

When A reads 8, B can only read 2+3=5 pages worth of other books.
Then B still needs to read 8, but A has nothing to do (already read all).
A must wait for B to finish 8.

Total time = 8 + 8 = 16
```

**Case 2: The longest book is NOT "too long"**
```
Books: [5, 5, 5]
Total = 15, Max = 5

They can always swap and keep busy:
Time:     0    5    10   15
Person A: |5|  |5|  |5|
Person B: |5|  |5|  |5|

Each person reads all 15 pages = 15 time units.
Total time = 15
```

### The Formula

```
Answer = max(2 * max_book, total_sum)
```

**Why `2 * max_book`?**
- When Person A reads the longest book, Person B cannot read it
- When Person B reads the longest book, Person A cannot read it
- So the longest book creates a "blocking" period of `max_book` for each person
- Minimum time is at least `2 * max_book`

**Why `total_sum`?**
- Each person must read all books = `total_sum` pages
- No matter how we schedule, each person needs at least `total_sum` time
- So minimum time is at least `total_sum`

**Why is `max(2 * max_book, total_sum)` achievable?**
- If `2 * max_book >= total_sum`: While one reads the max book, the other reads remaining books (which take <= max_book time), then they swap.
- If `total_sum > 2 * max_book`: They can always find a book to read since no single book dominates. They finish in exactly `total_sum` time.

---

## Solution: Mathematical Formula (Optimal)

### Key Insight

> **The Trick:** The answer is simply `max(2 * max_time, total_time)` - no complex algorithm needed.

### Algorithm

1. Calculate the sum of all book times (`total`)
2. Find the maximum book time (`max_time`)
3. Return `max(2 * max_time, total)`

### Dry Run Example

Let's trace through with input `n = 3, books = [2, 8, 3]`:

```
Initial state:
  books = [2, 8, 3]

Step 1: Calculate total time
  total = 2 + 8 + 3 = 13

Step 2: Find maximum book
  max_time = max(2, 8, 3) = 8

Step 3: Apply formula
  answer = max(2 * 8, 13)
         = max(16, 13)
         = 16

Output: 16
```

### Visual Schedule (Why 16 works)

```
Books: [2, 8, 3], Total = 13, Max = 8

Optimal Schedule:
Time:     0         5    8         13        16
          |---------|----|---------|---------|----|
Person A: |----8----|    |   2     |    3    |
Person B: |  2 | 3  |    |--------8----------|

Time 0-5:   A reads book "8", B reads "2" then "3"
Time 5-8:   A reads "2" (2 units) + "3" (1 unit), B starts "8"
            Wait, that doesn't quite work...

Better visualization:
Time:     0              8              16
Person A: |------8-------|--2--|---3----|
Person B: |--2--|---3----|------8-------|

Time 0-8:   A reads book(8), B reads book(2) then book(3), finishes at time 5, waits
Time 5-8:   B waits (A still reading book 8)
Time 8-10:  A reads book(2), B reads book(8)
Time 10-13: A reads book(3), B continues book(8)
Time 13-16: A waits, B finishes book(8)

Total: 16 time units
```

### Code (Python)

```python
def solve():
 """
 Optimal solution using mathematical formula.

 Time: O(n) - single pass to compute sum and max
 Space: O(n) - storing the input array
 """
 n = int(input())
 books = list(map(int, input().split()))

 total = sum(books)
 max_time = max(books)

 # Key formula: max(2 * max_time, total)
 print(max(2 * max_time, total))

if __name__ == "__main__":
 solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n) | Single pass to compute sum and find maximum |
| Space | O(1) | Only need to store total and max (can process input on the fly) |

---

## Common Mistakes

### Mistake 1: Misunderstanding the Problem

```python
# WRONG: Thinking this is about dividing books between two people
def wrong_solution(books):
 # This solves a DIFFERENT problem!
 books.sort(reverse=True)
 p1, p2 = 0, 0
 for book in books:
  if p1 <= p2:
   p1 += book
  else:
   p2 += book
 return max(p1, p2)
```

**Problem:** The problem states BOTH people must read ALL books, not divide them.
**Fix:** Understand that the constraint is "cannot read same book simultaneously", not "distribute books".

### Mistake 2: Forgetting the 2x Factor

```python
# WRONG: Missing the factor of 2
def wrong_formula(books):
 return max(max(books), sum(books))  # Missing 2 * max!
```

**Problem:** The longest book blocks BOTH people - each must read it separately.
**Fix:** Use `max(2 * max(books), sum(books))`.

**Problem:** Sum can exceed INT_MAX (2^31 - 1).
**Fix:** Use `long long` for total and max_time.

### Mistake 4: Not Handling n = 1

```python
# Edge case: Single book
books = [5]
# Answer should be 2 * 5 = 10 (both must read it, cannot simultaneously)
# max(2 * 5, 5) = 10 - Formula handles it correctly!
```

The formula naturally handles n = 1 correctly.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single book | `n=1, [5]` | 10 | Both read it: 2 * 5 = 10 |
| Equal books | `n=3, [5,5,5]` | 15 | max(10, 15) = 15 |
| One dominates | `n=3, [1,1,100]` | 200 | max(200, 102) = 200 |
| Large values | `n=2, [10^9, 10^9]` | 2 * 10^9 | max(2*10^9, 2*10^9) |
| Many small books | `n=10^5, all 1s` | 10^5 | max(2, 10^5) = 10^5 |

---

## When to Use This Pattern

### Use This Approach When:
- Two (or more) agents must complete ALL tasks
- Agents cannot work on the same task simultaneously
- You need to find minimum completion time
- Tasks have no dependencies (can be done in any order)

### Don't Use When:
- Tasks are to be DIVIDED among workers (partition problem)
- There are dependencies between tasks
- Workers have different speeds
- Tasks can be done simultaneously by multiple workers

### Pattern Recognition Checklist:
- [ ] Both/all agents must complete ALL tasks? -> Consider this pattern
- [ ] Blocking constraint (cannot do same task simultaneously)? -> Factor of 2 for max
- [ ] No task dependencies? -> Simple formula may work
- [ ] Looking for minimum time? -> max(k * max_task, total) where k = number of agents

---

## Related Problems

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [CSES - Factory Machines](https://cses.fi/problemset/task/1620) | Binary search on answer, machines have different rates |
| [CSES - Tasks and Deadlines](https://cses.fi/problemset/task/1630) | Maximize score, not minimize time |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [CSES - Movie Festival II](https://cses.fi/problemset/task/1632) | Multiple members, interval scheduling |
| [LeetCode - Task Scheduler](https://leetcode.com/problems/task-scheduler/) | Cooldown between same tasks |
| [LeetCode - Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) | Minimum rooms needed (interval partitioning) |

### LeetCode Related

| Problem | Similarity |
|---------|------------|
| [LeetCode 621 - Task Scheduler](https://leetcode.com/problems/task-scheduler/) | Blocking/cooldown concept |
| [LeetCode 1335 - Minimum Difficulty of a Job Schedule](https://leetcode.com/problems/minimum-difficulty-of-a-job-schedule/) | Scheduling with constraints |

---

## Key Takeaways

1. **The Core Idea:** When two people must both complete all tasks and cannot work on the same task simultaneously, the answer is `max(2 * longest_task, total_time)`.

2. **Why It Works:** The longest task creates unavoidable "blocking" time. Either this blocking dominates (2 * max) or there are enough other tasks to fill the gaps (total).

3. **Pattern Recognition:** Problems about "parallel workers with blocking constraints" often have elegant mathematical solutions.

4. **Complexity:** O(n) time, O(1) space - just compute sum and max.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why the answer is `max(2 * max, total)` in your own words
- [ ] Draw a schedule showing why 2 * max is needed when one book dominates
- [ ] Draw a schedule showing why total is the answer when no book dominates
- [ ] Identify this pattern in new problems (parallel workers, blocking constraints)
- [ ] Implement in under 5 minutes (it is just sum + max + formula)

---

## Additional Resources

- [CSES Reading Books](https://cses.fi/problemset/task/1631) - Parallel scheduling
- [CP-Algorithms: Scheduling](https://cp-algorithms.com/)
