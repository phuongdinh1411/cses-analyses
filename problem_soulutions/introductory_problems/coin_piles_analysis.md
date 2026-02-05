---
layout: simple
title: "Coin Piles - Math Problem"
permalink: /problem_soulutions/introductory_problems/coin_piles_analysis
difficulty: Easy
tags: [math, diophantine-equations, number-theory]
---

# Coin Piles

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **CSES Link** | [Coin Piles](https://cses.fi/problemset/task/1754) |
| **Difficulty** | Easy |
| **Category** | Math / Number Theory |
| **Time Limit** | 1 second |
| **Key Technique** | Linear Diophantine Equations |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Model problems as systems of linear equations
- [ ] Recognize when a problem involves linear Diophantine equations
- [ ] Derive necessary conditions for integer solutions (divisibility, non-negativity)
- [ ] Solve problems in O(1) time using mathematical analysis

---

## Problem Statement

**Problem:** Given two piles with `a` and `b` coins respectively, determine if both piles can be emptied using two operations:
- **Operation 1:** Remove 1 coin from pile A and 2 coins from pile B
- **Operation 2:** Remove 2 coins from pile A and 1 coin from pile B

**Input:**
- Line 1: Number of test cases `t`
- Lines 2 to t+1: Two integers `a` and `b` (coins in each pile)

**Output:**
- For each test case: "YES" if both piles can be emptied, "NO" otherwise

**Constraints:**
- 1 <= t <= 10^5
- 0 <= a, b <= 10^9

### Example

```
Input:
3
2 1
2 2
3 3

Output:
YES
NO
YES
```

**Explanation:**
- (2,1): Use Operation 2 once: (2-2, 1-1) = (0,0). YES
- (2,2): No combination works (explained below). NO
- (3,3): Use Operation 1 once, then Operation 2 once: (3,3) -> (2,1) -> (0,0). YES

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** Can we reach (0,0) from (a,b) by repeatedly subtracting (1,2) or (2,1)?

This is a **linear Diophantine equation** problem. Let `x` = number of Operation 1s, `y` = number of Operation 2s. We need:
- `x + 2y = a` (coins removed from pile A)
- `2x + y = b` (coins removed from pile B)

### Breaking Down the Problem

1. **What are we looking for?** Non-negative integers x, y satisfying both equations
2. **What information do we have?** Values a and b
3. **What's the relationship?** We need to solve a 2x2 linear system over integers

### The Mathematics

Solving the system of equations:
```
x + 2y = a  ... (1)
2x + y = b  ... (2)
```

From (1): `x = a - 2y`
Substitute into (2): `2(a - 2y) + y = b`
Simplify: `2a - 4y + y = b` => `2a - 3y = b` => `y = (2a - b) / 3`

Similarly: `x = (2b - a) / 3`

### Three Conditions for "YES"

For a valid solution, we need:
1. **(a + b) % 3 == 0**: Sum must be divisible by 3 (each operation removes 3 coins total)
2. **a <= 2b**: Ensures y >= 0 (can't have negative operations)
3. **b <= 2a**: Ensures x >= 0 (can't have negative operations)

---

## Solution: Mathematical Analysis (Optimal)

### Key Insight

> **The Trick:** Each operation removes exactly 3 coins total. After x+y operations, we remove 3(x+y) coins. So (a+b) must be divisible by 3.

### Algorithm

1. Check if `(a + b) % 3 == 0` (divisibility condition)
2. Check if `a <= 2*b` (non-negativity of y)
3. Check if `b <= 2*a` (non-negativity of x)
4. Return "YES" if all conditions met, "NO" otherwise

### Dry Run Example

Let's trace through with inputs `(2,1)`, `(2,2)`, and `(3,3)`:

```
Test Case 1: a=2, b=1
  Condition 1: (2+1) % 3 = 3 % 3 = 0     [PASS]
  Condition 2: 2 <= 2*1 = 2              [PASS]
  Condition 3: 1 <= 2*2 = 4              [PASS]

  Verification: x = (2*1-2)/3 = 0, y = (2*2-1)/3 = 1
  Check: 0*1 + 1*2 = 2 = a, 0*2 + 1*1 = 1 = b
  Result: YES

Test Case 2: a=2, b=2
  Condition 1: (2+2) % 3 = 4 % 3 = 1     [FAIL]
  Result: NO (sum not divisible by 3)

Test Case 3: a=3, b=3
  Condition 1: (3+3) % 3 = 6 % 3 = 0     [PASS]
  Condition 2: 3 <= 2*3 = 6              [PASS]
  Condition 3: 3 <= 2*3 = 6              [PASS]

  Verification: x = (2*3-3)/3 = 1, y = (2*3-3)/3 = 1
  Check: 1*1 + 1*2 = 3 = a, 1*2 + 1*1 = 3 = b
  Result: YES
```

### Visual Diagram

```
Starting Point: (a, b)
Target: (0, 0)

Each operation is a vector subtraction:
  Op1: subtract (1, 2)
  Op2: subtract (2, 1)

Example: (3, 3) -> (0, 0)

     Pile A    Pile B
       3         3      Initial
      -1        -2      Op1 (x=1)
       2         1
      -2        -1      Op2 (y=1)
       0         0      Done!

Total: x=1 operations of type 1
       y=1 operations of type 2
```

### Code (Python)

```python
def can_empty_piles(a: int, b: int) -> str:
  """
  Check if both piles can be emptied.

  Mathematical conditions:
  1. (a + b) must be divisible by 3
  2. a <= 2*b (ensures y >= 0)
  3. b <= 2*a (ensures x >= 0)

  Time: O(1)
  Space: O(1)
  """
  if (a + b) % 3 != 0:
    return "NO"
  if a > 2 * b:
    return "NO"
  if b > 2 * a:
    return "NO"
  return "YES"


def solve():
  t = int(input())
  for _ in range(t):
    a, b = map(int, input().split())
    print(can_empty_piles(a, b))


if __name__ == "__main__":
  solve()
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(1) per test | Only arithmetic operations |
| Space | O(1) | No extra storage needed |

---

## Common Mistakes

### Mistake 1: Forgetting the Divisibility Check

```python
# WRONG - missing divisibility check
def wrong_solution(a, b):
  if a <= 2*b and b <= 2*a:
    return "YES"
  return "NO"

# Test: (2, 2) would return YES but answer is NO
# Because 2+2=4 is not divisible by 3
```

**Problem:** Without the divisibility check, (2,2) passes but has no integer solution.
**Fix:** Always check `(a + b) % 3 == 0` first.

### Mistake 2: Forgetting Bounds Check

```python
# WRONG - only checking divisibility
def wrong_solution(a, b):
  if (a + b) % 3 == 0:
    return "YES"
  return "NO"

# Test: (0, 6) would return YES but answer is NO
# Because x = (2*6-0)/3 = 4, y = (2*0-6)/3 = -2 < 0
```

**Problem:** Divisibility alone doesn't ensure non-negative x and y.
**Fix:** Check both `a <= 2*b` and `b <= 2*a`.

**Problem:** With a, b up to 10^9, their sum can exceed int range.
**Fix:** Use `long long` in C++.

---

## Edge Cases

| Case | Input (a, b) | Output | Reason |
|------|--------------|--------|--------|
| Both zero | (0, 0) | YES | Already empty |
| One zero | (0, 3) | NO | 0 > 2*3 is false, but 3 > 2*0 is true |
| Equal piles | (3, 3) | YES | (3+3)%3=0, 3<=6, 3<=6 |
| Ratio 2:1 | (4, 2) | YES | Use 2 Operation 2s: (4,2)->(2,1)->(0,0) |
| Large values | (10^9, 10^9) | NO | (2*10^9)%3 != 0 |
| Sum divisible, bad ratio | (1, 5) | NO | 5 > 2*1, so y would be negative |

---

## When to Use This Pattern

### Use This Approach When:
- Problem involves reaching a target state through repeated operations
- Each operation has fixed "costs" or "effects"
- You need to find if non-negative integer solutions exist

### Don't Use When:
- Operations have variable effects
- You need to count the number of ways (use DP instead)
- The state space is small enough for BFS/DFS

### Pattern Recognition Checklist:
- [ ] Can the problem be modeled as linear equations? -> **Consider Diophantine analysis**
- [ ] Are operations removing/adding fixed amounts? -> **Look for divisibility conditions**
- [ ] Do you need integer solutions? -> **Check GCD and bounds**

---

## Related Problems

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Gray Code (CSES)](https://cses.fi/problemset/task/2205) | Bit manipulation pattern |
| [Tower of Hanoi (CSES)](https://cses.fi/problemset/task/2165) | Recursive structure |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Josephus Problem I (CSES)](https://cses.fi/problemset/task/2162) | Mathematical recurrence |
| [Josephus Problem II (CSES)](https://cses.fi/problemset/task/2163) | Efficient simulation |

### LeetCode Related

| Problem | Connection |
|---------|------------|
| [Water and Jug Problem](https://leetcode.com/problems/water-and-jug-problem/) | GCD-based Diophantine |
| [Reaching Points](https://leetcode.com/problems/reaching-points/) | Reverse state transitions |

---

## Key Takeaways

1. **The Core Idea:** Model the problem as linear equations and derive conditions for integer solutions
2. **Time Optimization:** Mathematical analysis gives O(1) vs. simulation which could be O(min(a,b))
3. **Three Conditions:** Divisibility by 3, and both ratio bounds a<=2b and b<=2a
4. **Pattern:** Linear Diophantine equations with non-negativity constraints

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Derive the three conditions from the system of equations
- [ ] Explain why (a+b) must be divisible by 3
- [ ] Explain why a <= 2b and b <= 2a are needed
- [ ] Implement in O(1) time without looking at the solution
