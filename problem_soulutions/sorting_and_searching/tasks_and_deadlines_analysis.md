---
layout: simple
title: "Tasks And Deadlines - Greedy Scheduling Problem"
permalink: /problem_soulutions/sorting_and_searching/tasks_and_deadlines_analysis
difficulty: Medium
tags: [greedy, sorting, scheduling]
---

# Tasks And Deadlines

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Greedy / Sorting |
| **Time Limit** | 1 second |
| **Key Technique** | Greedy (Sort by Duration) |
| **CSES Link** | [Tasks and Deadlines](https://cses.fi/problemset/task/1630) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Recognize scheduling problems that can be solved greedily
- [ ] Understand why sorting by duration (Shortest Job First) maximizes reward
- [ ] Derive greedy sorting criteria using algebraic manipulation
- [ ] Handle potential integer overflow in scheduling problems

---

## Problem Statement

**Problem:** You have n tasks. Each task has a duration and a deadline. You must complete all tasks, and for each task, you earn a reward equal to `deadline - finish_time`. Find the maximum total reward.

**Input:**
- Line 1: Integer n (number of tasks)
- Lines 2 to n+1: Two integers d and t (duration and deadline of each task)

**Output:**
- Maximum total reward (can be negative)

**Constraints:**
- 1 <= n <= 2 x 10^5
- 1 <= d[i], t[i] <= 10^6

### Example

```
Input:
3
6 10
8 15
5 12

Output:
2
```

**Explanation:**
- Optimal order: Task 3 (d=5), Task 1 (d=6), Task 2 (d=8)
- Task 3: finish at time 5, reward = 12 - 5 = 7
- Task 1: finish at time 11, reward = 10 - 11 = -1
- Task 2: finish at time 19, reward = 15 - 19 = -4
- Total: 7 + (-1) + (-4) = 2

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** The reward formula is `deadline - finish_time`. Since we must complete ALL tasks, total time spent is fixed (sum of all durations). What can we control?

The total reward is: sum of (deadline_i - finish_time_i)

This equals: (sum of deadlines) - (sum of finish times)

Since sum of deadlines is fixed, we need to **minimize the sum of finish times**.

### Breaking Down the Problem

1. **What are we looking for?** Maximum total reward = Minimize sum of finish times
2. **What information do we have?** Duration and deadline for each task
3. **What's the relationship?** Earlier tasks contribute their duration to ALL subsequent finish times

### The Key Insight: Shortest Job First

Consider two adjacent tasks A and B. If we swap their order:
- Order A then B: Task A finishes at time T + d_A, Task B at T + d_A + d_B
- Order B then A: Task B finishes at time T + d_B, Task A at T + d_B + d_A

The sum of finish times for these two tasks:
- Order A-B: (T + d_A) + (T + d_A + d_B) = 2T + 2*d_A + d_B
- Order B-A: (T + d_B) + (T + d_B + d_A) = 2T + 2*d_B + d_A

A-B is better when: 2*d_A + d_B < 2*d_B + d_A, which simplifies to **d_A < d_B**

**Conclusion:** Always do shorter tasks first!

### Analogy

Think of it like standing in a queue at the bank. If you want to minimize the total waiting time for everyone, you should serve customers with the shortest transactions first. This is the classic "Shortest Job First" scheduling algorithm.

---

## Solution 1: Brute Force

### Idea

Try all possible orderings (permutations) of tasks and find the one with maximum reward.

### Algorithm

1. Generate all n! permutations of tasks
2. For each permutation, calculate total reward
3. Return the maximum reward found

### Code

```python
from itertools import permutations

def solve_brute_force(tasks):
    """
    Brute force: try all permutations.

    Time: O(n! * n)
    Space: O(n)
    """
    max_reward = float('-inf')

    for order in permutations(tasks):
        current_time = 0
        total_reward = 0
        for duration, deadline in order:
            current_time += duration
            total_reward += deadline - current_time
        max_reward = max(max_reward, total_reward)

    return max_reward
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n! * n) | n! permutations, O(n) to evaluate each |
| Space | O(n) | Store one permutation at a time |

### Why This Works (But Is Slow)

Correctness is guaranteed because we check every possible ordering. However, n! grows extremely fast - even for n=12, we have 479 million permutations.

---

## Solution 2: Optimal - Greedy (Sort by Duration)

### Key Insight

> **The Trick:** Sort tasks by duration in ascending order. Shorter tasks first always yields the maximum reward.

### Why Sorting by Duration Works

From our analysis above, for any two adjacent tasks, placing the shorter one first is always better or equal. By sorting all tasks by duration, we ensure every adjacent pair is optimally ordered, which means the entire sequence is optimal.

### Algorithm

1. Sort tasks by duration (ascending)
2. Process tasks in sorted order, accumulating time and reward
3. Return total reward

### Dry Run Example

Let's trace through with input `[(6,10), (8,15), (5,12)]`:

```
Initial: tasks = [(6,10), (8,15), (5,12)]

Step 1: Sort by duration
  Sorted: [(5,12), (6,10), (8,15)]

Step 2: Process in order
  current_time = 0, total_reward = 0

  Process (5, 12):
    current_time = 0 + 5 = 5
    reward = 12 - 5 = 7
    total_reward = 0 + 7 = 7

  Process (6, 10):
    current_time = 5 + 6 = 11
    reward = 10 - 11 = -1
    total_reward = 7 + (-1) = 6

  Process (8, 15):
    current_time = 11 + 8 = 19
    reward = 15 - 19 = -4
    total_reward = 6 + (-4) = 2

Result: 2
```

### Visual Diagram

```
Tasks sorted by duration:

Task:     (5,12)    (6,10)    (8,15)
          |--5--|   |---6---|  |----8----|
Time: 0        5          11           19

Rewards:
  Task 1: deadline=12, finish=5,  reward = +7
  Task 2: deadline=10, finish=11, reward = -1
  Task 3: deadline=15, finish=19, reward = -4
                                  Total = +2
```

### Code

**Python Solution:**

```python
def solve(n, tasks):
    """
    Optimal greedy solution: sort by duration.

    Time: O(n log n)
    Space: O(1) extra (in-place sort)
    """
    # Sort by duration (shortest first)
    tasks.sort(key=lambda x: x[0])

    current_time = 0
    total_reward = 0

    for duration, deadline in tasks:
        current_time += duration
        total_reward += deadline - current_time

    return total_reward


def main():
    n = int(input())
    tasks = []
    for _ in range(n):
        d, t = map(int, input().split())
        tasks.append((d, t))

    print(solve(n, tasks))


if __name__ == "__main__":
    main()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | Dominated by sorting |
| Space | O(1) | In-place sort, only tracking two variables |

---

## Common Mistakes

### Mistake 1: Sorting by Deadline Instead of Duration

```python
# WRONG
tasks.sort(key=lambda x: x[1])  # Sort by deadline

# CORRECT
tasks.sort(key=lambda x: x[0])  # Sort by duration
```

**Problem:** Sorting by deadline seems intuitive (do urgent tasks first) but does not minimize the sum of finish times.

**Fix:** Remember the mathematical proof - only duration affects the sum of finish times.

**Problem:** With n = 2x10^5 tasks and durations up to 10^6, total time can reach 2x10^11, exceeding int range. The reward can also be very negative.

**Fix:** Use `long long` for time and reward calculations.

### Mistake 3: Forgetting Rewards Can Be Negative

```python
# WRONG - early termination on negative reward
if total_reward < 0:
    break

# CORRECT - must complete ALL tasks
for duration, deadline in tasks:
    current_time += duration
    total_reward += deadline - current_time  # May be negative
```

**Problem:** The problem requires completing ALL tasks. Negative rewards are expected and valid.

**Fix:** Process all tasks regardless of individual reward signs.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single task | `n=1, (5,10)` | 5 | 10 - 5 = 5 |
| All same duration | `(3,5), (3,8), (3,2)` | Same any order | Order doesn't matter |
| All negative rewards | `(10,1), (10,2)` | -27 | 1-10 + 2-20 = -9 + -18 |
| Large values | `n=2x10^5, d=10^6` | Use long long | Sum can exceed 32-bit |
| Deadline < Duration | `(10, 5)` | -5 | Valid input, negative reward |

---

## When to Use This Pattern

### Use This Approach When:
- You need to schedule ALL tasks (no selection involved)
- Reward/penalty depends on completion time
- Tasks are independent (no dependencies)
- You want to minimize weighted completion time

### Don't Use When:
- Tasks have dependencies (use topological sort)
- You can skip tasks (use different greedy or DP)
- Rewards have complex formulas not linear in finish time
- Tasks have different weights/priorities beyond duration

### Pattern Recognition Checklist:
- [ ] Must complete all items? -> Consider ordering optimization
- [ ] Penalty/reward based on completion time? -> Think "Shortest Job First"
- [ ] Can prove adjacent swap property? -> Greedy by sorting works

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Movie Festival (CSES 1629)](https://cses.fi/problemset/task/1629) | Basic interval scheduling, sort by end time |
| [Stick Lengths (CSES 1074)](https://cses.fi/problemset/task/1074) | Greedy with sorting, find optimal target |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Reading Books (CSES 1631)](https://cses.fi/problemset/task/1631) | Two readers, similar scheduling |
| [Movie Festival II (CSES 1632)](https://cses.fi/problemset/task/1632) | Multiple people attending movies |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Task Scheduler (LC 621)](https://leetcode.com/problems/task-scheduler/) | Cooldown constraints |
| [Course Schedule III (LC 630)](https://leetcode.com/problems/course-schedule-iii/) | Task selection + scheduling |
| [Weighted Job Scheduling (LC 1235)](https://leetcode.com/problems/maximum-profit-in-job-scheduling/) | DP with binary search |

---

## Key Takeaways

1. **The Core Idea:** Sort by duration (Shortest Job First) to minimize sum of finish times
2. **Time Optimization:** From O(n!) brute force to O(n log n) with greedy sorting
3. **Space Trade-off:** No extra space needed beyond input storage
4. **Pattern:** Adjacent swap argument proves greedy correctness

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Prove why sorting by duration is optimal using the swap argument
- [ ] Implement the solution without looking at code
- [ ] Explain why sorting by deadline does NOT work
- [ ] Handle integer overflow correctly in C++
- [ ] Recognize similar "minimize completion time" problems

---

## Mathematical Proof (Optional Deep Dive)

### Theorem: Shortest Job First is Optimal

**Claim:** Sorting tasks by duration minimizes the sum of finish times.

**Proof by Exchange Argument:**

1. Consider any optimal ordering that is NOT sorted by duration
2. There must exist adjacent tasks i and j where d_i > d_j but i comes before j
3. Let T be the time before task i starts
4. Sum of finish times for i,j: (T + d_i) + (T + d_i + d_j) = 2T + 2d_i + d_j
5. If we swap: (T + d_j) + (T + d_j + d_i) = 2T + 2d_j + d_i
6. Since d_i > d_j: 2d_i + d_j > 2d_j + d_i
7. Therefore swapping improves (or equals) the sum
8. Repeat until sorted - we can only improve, never worsen
9. Thus sorted order is optimal

This is the classic "bubble sort correctness" style proof for greedy algorithms.
