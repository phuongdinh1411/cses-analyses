---
layout: simple
title: "Tower of Hanoi - Introductory Problem"
permalink: /problem_soulutions/introductory_problems/tower_of_hanoi_analysis
difficulty: Easy
tags: [recursion, divide-and-conquer, classic]
---

# Tower of Hanoi

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Easy |
| **Category** | Recursion / Divide and Conquer |
| **Time Limit** | 1 second |
| **Key Technique** | Recursive Decomposition |
| **CSES Link** | [Tower of Hanoi](https://cses.fi/problemset/task/2165) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand and apply recursive problem decomposition
- [ ] Recognize the classic Tower of Hanoi recurrence: T(n) = 2T(n-1) + 1
- [ ] Generate move sequences using recursion
- [ ] Derive that the minimum number of moves is 2^n - 1

---

## Problem Statement

**Problem:** The Tower of Hanoi puzzle consists of three stacks (pegs) and n disks of different sizes. Initially, all disks are on the left stack in order of size (largest on bottom). The goal is to move all disks to the right stack following these rules:
1. Only one disk can be moved at a time
2. A larger disk cannot be placed on a smaller disk
3. A disk can only be moved from the top of a stack

**Input:**
- Line 1: Integer n - the number of disks

**Output:**
- Line 1: The minimum number of moves required
- Next lines: Each move as "a b" meaning move the top disk from stack a to stack b

**Constraints:**
- 1 <= n <= 16

### Example

```
Input:
2

Output:
3
1 2
1 3
2 3
```

**Explanation:**
- Move disk 1 from stack 1 to stack 2 (use stack 2 as auxiliary)
- Move disk 2 from stack 1 to stack 3 (move largest disk to target)
- Move disk 1 from stack 2 to stack 3 (move remaining disk to target)

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we break down moving n disks into smaller subproblems?

The Tower of Hanoi is the classic example of recursive problem-solving. The key insight is that to move n disks from source to target, we must first move n-1 disks out of the way, then move the largest disk, then move the n-1 disks on top of it.

### Breaking Down the Problem

1. **What are we looking for?** A sequence of moves to transfer all disks from stack 1 to stack 3.
2. **What information do we have?** The number of disks n and three available stacks.
3. **What's the relationship between input and output?** The number of moves follows T(n) = 2^n - 1.

### The Recursive Decomposition

To move n disks from source (S) to target (T) using auxiliary (A):

```
1. Move (n-1) disks from S to A (using T as auxiliary)
2. Move 1 disk from S to T (the largest disk)
3. Move (n-1) disks from A to T (using S as auxiliary)
```

This decomposition naturally leads to the recurrence:
```
T(n) = T(n-1) + 1 + T(n-1) = 2*T(n-1) + 1
T(1) = 1

Solution: T(n) = 2^n - 1
```

### Analogy

Think of it like moving a stack of heavy books. To move the entire stack, you must first move all the books above the bottom one, then move the bottom book, then replace the stack on top.

---

## Solution: Recursive Approach

### Key Insight

> **The Trick:** Recursively define the problem in terms of a smaller version of itself. Moving n disks requires moving n-1 disks twice plus one move for the largest disk.

### Algorithm

1. **Base case:** If n = 0, do nothing (no disks to move)
2. **Recursive step:**
   - Move n-1 disks from source to auxiliary
   - Move the largest disk from source to target (print this move)
   - Move n-1 disks from auxiliary to target

### Dry Run Example

Let's trace through with `n = 3` (disks labeled 1=smallest, 3=largest):

```
Initial State:
  Stack 1: [3, 2, 1]  (bottom to top)
  Stack 2: []
  Stack 3: []

Call: hanoi(3, 1, 3, 2)  -- Move 3 disks from 1 to 3 using 2

  Call: hanoi(2, 1, 2, 3)  -- Move 2 disks from 1 to 2 using 3

    Call: hanoi(1, 1, 3, 2)  -- Move 1 disk from 1 to 3 using 2
      Print: "1 3"  (move disk 1)
      State: [3,2] [] [1]

    Print: "1 2"  (move disk 2)
    State: [3] [2] [1]

    Call: hanoi(1, 3, 2, 1)  -- Move 1 disk from 3 to 2 using 1
      Print: "3 2"  (move disk 1)
      State: [3] [2,1] []

  Print: "1 3"  (move disk 3 - the largest)
  State: [] [2,1] [3]

  Call: hanoi(2, 2, 3, 1)  -- Move 2 disks from 2 to 3 using 1

    Call: hanoi(1, 2, 1, 3)  -- Move 1 disk from 2 to 1 using 3
      Print: "2 1"  (move disk 1)
      State: [1] [2] [3]

    Print: "2 3"  (move disk 2)
    State: [1] [] [3,2]

    Call: hanoi(1, 1, 3, 2)  -- Move 1 disk from 1 to 3 using 2
      Print: "1 3"  (move disk 1)
      State: [] [] [3,2,1]

Final Output:
7 moves: 1 3, 1 2, 3 2, 1 3, 2 1, 2 3, 1 3
```

### Visual Diagram

```
n = 2 Example:

Initial:        After move 1:    After move 2:    After move 3:
   |               |               |               |
  [1]              |               |               |
  [2]             [2]              |              [1]
 -----   ---   -----   ---     -----  [1]      -----  [2]
   1      2      3      1  2     3      1  2     3

Move 1: 1->2    Move 2: 1->3    Move 3: 2->3
```

### Python Code

```python
def solve():
    n = int(input())

    moves = []

    def hanoi(disks, source, target, auxiliary):
        """
        Move 'disks' disks from 'source' to 'target' using 'auxiliary'.

        Time: O(2^n) - we make 2^n - 1 moves
        Space: O(n) - recursion depth
        """
        if disks == 0:
            return

        # Step 1: Move n-1 disks from source to auxiliary
        hanoi(disks - 1, source, auxiliary, target)

        # Step 2: Move the largest disk from source to target
        moves.append(f"{source} {target}")

        # Step 3: Move n-1 disks from auxiliary to target
        hanoi(disks - 1, auxiliary, target, source)

    hanoi(n, 1, 3, 2)

    print(len(moves))
    print('\n'.join(moves))

solve()
```

### C++ Code

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<pair<int, int>> moves;

void hanoi(int disks, int source, int target, int auxiliary) {
    // Base case: no disks to move
    if (disks == 0) return;

    // Step 1: Move n-1 disks from source to auxiliary
    hanoi(disks - 1, source, auxiliary, target);

    // Step 2: Move largest disk from source to target
    moves.push_back({source, target});

    // Step 3: Move n-1 disks from auxiliary to target
    hanoi(disks - 1, auxiliary, target, source);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    hanoi(n, 1, 3, 2);

    cout << moves.size() << "\n";
    for (auto& [a, b] : moves) {
        cout << a << " " << b << "\n";
    }

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(2^n) | We generate exactly 2^n - 1 moves |
| Space | O(n) | Maximum recursion depth is n |

---

## Common Mistakes

### Mistake 1: Wrong Move Count Formula

```python
# WRONG
print(2 ** n)  # Off by one!

# CORRECT
print(2 ** n - 1)  # The formula is 2^n - 1
```

**Problem:** The formula for minimum moves is 2^n - 1, not 2^n.
**Fix:** Remember T(n) = 2T(n-1) + 1 solves to 2^n - 1.

### Mistake 2: Swapping Auxiliary and Target in Recursive Calls

```python
# WRONG
def hanoi(disks, source, target, auxiliary):
    hanoi(disks - 1, source, target, auxiliary)  # Wrong! Should go to auxiliary
    moves.append(f"{source} {target}")
    hanoi(disks - 1, target, auxiliary, source)  # Wrong parameters

# CORRECT
def hanoi(disks, source, target, auxiliary):
    hanoi(disks - 1, source, auxiliary, target)  # Move to auxiliary first
    moves.append(f"{source} {target}")
    hanoi(disks - 1, auxiliary, target, source)  # Move from auxiliary to target
```

**Problem:** The roles of auxiliary and target must swap correctly in each recursive call.
**Fix:** In the first recursive call, auxiliary becomes the new target. In the second, it becomes the new source.

### Mistake 3: Forgetting the Base Case

```python
# WRONG - infinite recursion
def hanoi(disks, source, target, auxiliary):
    hanoi(disks - 1, source, auxiliary, target)
    moves.append(f"{source} {target}")
    hanoi(disks - 1, auxiliary, target, source)

# CORRECT
def hanoi(disks, source, target, auxiliary):
    if disks == 0:  # Base case!
        return
    hanoi(disks - 1, source, auxiliary, target)
    moves.append(f"{source} {target}")
    hanoi(disks - 1, auxiliary, target, source)
```

**Problem:** Without a base case, recursion never terminates.
**Fix:** Always include base case for n = 0 (or n = 1).

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single disk | n = 1 | 1 move: "1 3" | Just move directly |
| Two disks | n = 2 | 3 moves | 2^2 - 1 = 3 |
| Maximum input | n = 16 | 65535 moves | 2^16 - 1 |

---

## When to Use This Pattern

### Use Recursive Decomposition When:
- A problem can be broken into smaller identical subproblems
- The solution to the original problem depends on solutions to subproblems
- There's a clear base case that terminates recursion

### Don't Use When:
- The problem has significant overlapping subproblems (use DP instead)
- Recursion depth might cause stack overflow for large inputs
- An iterative solution is simpler and more efficient

### Pattern Recognition Checklist:
- [ ] Can the problem be expressed as smaller versions of itself? -> **Consider recursion**
- [ ] Are subproblems independent (no overlap)? -> **Recursion is efficient**
- [ ] Is there a mathematical recurrence relation? -> **Recursion maps directly**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Weird Algorithm](https://cses.fi/problemset/task/1068) | Basic recursion practice |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Apple Division](https://cses.fi/problemset/task/1623) | Recursive subset generation |
| [Gray Code](https://cses.fi/problemset/task/2205) | Another classic bit/recursive pattern |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Grid Paths](https://cses.fi/problemset/task/1625) | Backtracking with pruning |
| [Chessboard and Queens](https://cses.fi/problemset/task/1624) | Recursive backtracking |

---

## Key Takeaways

1. **The Core Idea:** Recursively move n-1 disks out of the way, move the largest disk, then move n-1 disks on top.
2. **The Formula:** Minimum moves = 2^n - 1 (derived from T(n) = 2T(n-1) + 1).
3. **The Pattern:** Tower of Hanoi is the quintessential example of divide-and-conquer recursion.
4. **The Insight:** Each recursive call swaps the roles of auxiliary and target pegs.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Derive the formula 2^n - 1 from the recurrence relation
- [ ] Trace through the algorithm for n = 3 by hand
- [ ] Explain why we need exactly 2^n - 1 moves (prove optimality)

---

## Mathematical Proof: Why 2^n - 1 Moves?

### Proving the Recurrence

**Recurrence:** T(n) = 2T(n-1) + 1, with T(1) = 1

**Solving by substitution:**
```
T(n) = 2T(n-1) + 1
     = 2(2T(n-2) + 1) + 1
     = 4T(n-2) + 2 + 1
     = 4(2T(n-3) + 1) + 2 + 1
     = 8T(n-3) + 4 + 2 + 1
     ...
     = 2^k * T(n-k) + 2^(k-1) + ... + 2 + 1

When k = n-1:
T(n) = 2^(n-1) * T(1) + 2^(n-2) + ... + 2 + 1
     = 2^(n-1) + 2^(n-2) + ... + 2 + 1
     = 2^n - 1  (geometric series)
```

### Proving Optimality

The largest disk must move at least once. Before it can move, all n-1 smaller disks must be on the auxiliary peg (requiring T(n-1) moves). After moving the largest disk, the n-1 smaller disks must move to the target (requiring another T(n-1) moves). Thus, T(n) >= 2T(n-1) + 1, and our algorithm achieves this bound.
