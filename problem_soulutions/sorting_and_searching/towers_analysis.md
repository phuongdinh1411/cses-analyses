---
layout: simple
title: "Towers - Sorting and Searching Problem"
permalink: /problem_soulutions/sorting_and_searching/towers_analysis
difficulty: Medium
tags: [greedy, binary-search, multiset, LIS]
---

# Towers

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Sorting and Searching |
| **Time Limit** | 1 second |
| **Key Technique** | Greedy + Binary Search (Multiset) |
| **CSES Link** | [https://cses.fi/problemset/task/1073](https://cses.fi/problemset/task/1073) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply greedy algorithms to minimize resource usage
- [ ] Use multiset/binary search to efficiently find insertion points
- [ ] Understand the connection between tower stacking and LIS
- [ ] Implement `upper_bound` logic for greedy placement decisions

---

## Problem Statement

**Problem:** You are given n cubes in a certain order, and your task is to build towers by placing them on top of each other. You can always place a cube on the ground, and you can place a cube on another cube if the upper cube is strictly smaller than the lower cube. What is the minimum number of towers you need?

**Input:**
- Line 1: integer n (number of cubes)
- Line 2: n integers k_1, k_2, ..., k_n (sizes of cubes in the given order)

**Output:**
- Print one integer: the minimum number of towers

**Constraints:**
- 1 <= n <= 2 * 10^5
- 1 <= k_i <= 10^9

### Example

```
Input:
5
3 8 2 1 5

Output:
2
```

**Explanation:**
- Tower 1: Place 3, then 8 on ground (8 > 3, so 3 goes on 8). Tower: [8, 3, 2, 1]
- Tower 2: Place 5. Tower: [5]
- Processing order: 3 -> 8 -> 2 -> 1 -> 5
  - 3: New tower [3]
  - 8: Cannot place on 3 (8 > 3), new tower [8]
  - 2: Place on 3 (2 < 3), towers: [3,2], [8]
  - 1: Place on 2 (1 < 2), towers: [3,2,1], [8]
  - 5: Place on 8 (5 < 8), towers: [3,2,1], [8,5]
- Result: 2 towers

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we minimize the number of towers when cubes must be placed in order?

The key insight is that we want to **greedily place each cube on the tower with the smallest top that is still larger than the cube**. This maximizes our options for future cubes.

### Breaking Down the Problem

1. **What are we looking for?** The minimum number of towers (decreasing subsequences) needed to cover all cubes.
2. **What information do we have?** Cube sizes in the order they must be processed.
3. **What's the relationship?** Each tower is a strictly decreasing sequence. We want to pack cubes into as few towers as possible.

### Analogies

Think of this problem like organizing documents into folders where each folder can only hold documents in decreasing size order. When a new document arrives, you want to put it in a folder where it fits (smallest folder top > document size) to leave larger folders available for larger future documents.

### Connection to LIS

By Dilworth's theorem, the minimum number of decreasing subsequences needed to cover a sequence equals the length of the longest increasing subsequence (LIS). However, the greedy simulation approach is more intuitive and gives us the actual tower structure.

---

## Solution 1: Brute Force

### Idea

For each cube, try placing it on every existing tower where it fits, or create a new tower. Try all possibilities to find the minimum.

### Algorithm

1. For each cube in order
2. Try placing on each valid tower (top > cube)
3. Also try creating a new tower
4. Recursively process remaining cubes
5. Return minimum towers used

### Code

```python
def solve_brute_force(cubes):
    """
    Brute force: try all valid placements.

    Time: O(n! * n) in worst case
    Space: O(n) for recursion stack
    """
    def backtrack(idx, towers):
        if idx == len(cubes):
            return len(towers)

        cube = cubes[idx]
        min_towers = float('inf')

        # Try placing on existing tower
        for i in range(len(towers)):
            if towers[i] > cube:  # Can place
                old_top = towers[i]
                towers[i] = cube
                min_towers = min(min_towers, backtrack(idx + 1, towers))
                towers[i] = old_top  # Restore

        # Try creating new tower
        towers.append(cube)
        min_towers = min(min_towers, backtrack(idx + 1, towers))
        towers.pop()

        return min_towers

    return backtrack(0, [])
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n! * n) | Exponential branching at each step |
| Space | O(n) | Recursion depth and tower list |

### Why This Works (But Is Slow)

Correct because it explores all valid placements and takes the minimum. Slow because it doesn't prune the search space intelligently.

---

## Solution 2: Optimal Solution (Greedy + Binary Search)

### Key Insight

> **The Trick:** Always place a cube on the tower with the **smallest top that is still strictly greater** than the cube. This greedy choice is optimal.

### Why Greedy Works

If we place a cube on a tower with a larger top than necessary, we waste a "good" tower that could have accommodated a larger future cube. By choosing the smallest valid top, we preserve flexibility.

### Data Structure: Multiset of Tower Tops

We maintain a **multiset** (sorted collection with duplicates) of all tower tops:
- To place cube `k`: Find the smallest top `> k` using `upper_bound(k)`
- If found: Remove that top, add `k` (cube becomes new top)
- If not found: Create new tower (add `k` to multiset)

### Algorithm

1. Initialize empty multiset of tower tops
2. For each cube `k` in order:
   - Find iterator to smallest element > k (upper_bound)
   - If found: Replace that element with k
   - Else: Insert k (new tower)
3. Return size of multiset

### Dry Run Example

Let's trace through with input `n = 5, cubes = [3, 8, 2, 1, 5]`:

```
Initial state:
  tower_tops = {} (empty multiset)

Step 1: Process cube = 3
  upper_bound(3) = end (no top > 3)
  Create new tower
  tower_tops = {3}

Step 2: Process cube = 8
  upper_bound(8) = end (no top > 8)
  Create new tower
  tower_tops = {3, 8}

Step 3: Process cube = 2
  upper_bound(2) = iterator to 3 (smallest > 2)
  Place 2 on tower with top 3
  Remove 3, insert 2
  tower_tops = {2, 8}

Step 4: Process cube = 1
  upper_bound(1) = iterator to 2 (smallest > 1)
  Place 1 on tower with top 2
  Remove 2, insert 1
  tower_tops = {1, 8}

Step 5: Process cube = 5
  upper_bound(5) = iterator to 8 (smallest > 5)
  Place 5 on tower with top 8
  Remove 8, insert 5
  tower_tops = {1, 5}

Final: 2 towers
```

### Visual Diagram

```
Cubes (processing order): 3 -> 8 -> 2 -> 1 -> 5

Tower Evolution (showing tops in multiset):

  cube=3    cube=8    cube=2    cube=1    cube=5
    |         |         |         |         |
   {3}    -> {3,8}  -> {2,8}  -> {1,8}  -> {1,5}

Final Towers (top to bottom):
  Tower 1: 1 <- 2 <- 3    (tops at each step: 3->2->1)
  Tower 2: 5 <- 8         (tops at each step: 8->5)
```

### Code (Python)

```python
import bisect

def solve_optimal(n, cubes):
    """
    Greedy with binary search using sorted list.

    Time: O(n log n)
    Space: O(n)
    """
    tower_tops = []  # Sorted list of tower tops

    for cube in cubes:
        # Find smallest top > cube (upper_bound)
        pos = bisect.bisect_right(tower_tops, cube)

        if pos < len(tower_tops):
            # Place on existing tower, update top
            tower_tops[pos] = cube
        else:
            # Create new tower
            tower_tops.append(cube)

        # Keep sorted (append preserves order since cube <= all elements after pos)
        # But we replaced at pos, need to re-sort that section
        # Actually, bisect_right + replace may break sorting!
        # Must use a proper approach

    return len(tower_tops)


def solve_optimal_correct(n, cubes):
    """
    Correct greedy with binary search.

    Since we need upper_bound and then replace, we can use
    a list but must maintain sortedness.

    Time: O(n log n)
    Space: O(n)
    """
    from sortedcontainers import SortedList

    tower_tops = SortedList()

    for cube in cubes:
        # Find index of smallest element > cube
        pos = tower_tops.bisect_right(cube)

        if pos < len(tower_tops):
            # Remove old top, add new (cube becomes top)
            tower_tops.pop(pos)
            tower_tops.add(cube)
        else:
            # No valid tower, create new one
            tower_tops.add(cube)

    return len(tower_tops)


# For competitive programming without SortedList:
def solve_with_bisect(n, cubes):
    """
    Using bisect with manual list management.

    Key insight: tower_tops stays sorted because:
    - We replace element at bisect_right position with smaller value
    - This maintains sorted order

    Time: O(n log n)
    Space: O(n)
    """
    tower_tops = []

    for cube in cubes:
        # bisect_right: find first position where element > cube
        pos = bisect.bisect_right(tower_tops, cube)

        if pos == len(tower_tops):
            # No tower has top > cube, create new
            tower_tops.append(cube)
        else:
            # tower_tops[pos] > cube, place cube there
            tower_tops[pos] = cube

    return len(tower_tops)


# Standard input/output version
def main():
    import bisect

    n = int(input())
    cubes = list(map(int, input().split()))

    tower_tops = []

    for cube in cubes:
        pos = bisect.bisect_right(tower_tops, cube)

        if pos == len(tower_tops):
            tower_tops.append(cube)
        else:
            tower_tops[pos] = cube

    print(len(tower_tops))


if __name__ == "__main__":
    main()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int n;
    cin >> n;

    multiset<int> tower_tops;

    for (int i = 0; i < n; i++) {
        int cube;
        cin >> cube;

        // Find smallest top > cube
        auto it = tower_tops.upper_bound(cube);

        if (it != tower_tops.end()) {
            // Place cube on this tower
            tower_tops.erase(it);
            tower_tops.insert(cube);
        } else {
            // Create new tower
            tower_tops.insert(cube);
        }
    }

    cout << tower_tops.size() << "\n";

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n) | n cubes, each with O(log n) multiset operations |
| Space | O(n) | Multiset stores at most n tower tops |

---

## Common Mistakes

### Mistake 1: Using lower_bound instead of upper_bound

```cpp
// WRONG
auto it = tower_tops.lower_bound(cube);

// CORRECT
auto it = tower_tops.upper_bound(cube);
```

**Problem:** `lower_bound` finds first element >= cube, but we need **strictly greater** (top > cube for valid placement).
**Fix:** Use `upper_bound` which finds first element > cube.

### Mistake 2: Using bisect_left instead of bisect_right in Python

```python
# WRONG
pos = bisect.bisect_left(tower_tops, cube)

# CORRECT
pos = bisect.bisect_right(tower_tops, cube)
```

**Problem:** `bisect_left` returns position of first element >= cube. If equal elements exist, we'd try to place on a tower of same size (invalid).
**Fix:** Use `bisect_right` to skip past equal elements.

### Mistake 3: Not erasing before inserting in multiset

```cpp
// WRONG
tower_tops.insert(cube);  // Forgot to erase old top!

// CORRECT
tower_tops.erase(it);
tower_tops.insert(cube);
```

**Problem:** Inserting without erasing adds a new tower instead of updating existing one.
**Fix:** Always erase the old top before inserting new top.

### Mistake 4: Confusing this with LIS

```python
# WRONG: Treating this as standard LIS
# LIS uses bisect_left to find position to replace

# This problem needs bisect_right because:
# - LIS: find longest increasing subsequence (strictly increasing)
# - Towers: place cube on smallest valid top (strictly greater)
```

**Problem:** Standard LIS uses `bisect_left` but this problem needs `bisect_right` for the greedy placement.
**Fix:** Understand that we're finding towers to place on, not building an increasing sequence.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single cube | `n=1, [5]` | 1 | One cube needs one tower |
| All same size | `n=4, [3,3,3,3]` | 4 | Cannot stack equal cubes |
| Strictly increasing | `n=4, [1,2,3,4]` | 4 | Each needs its own tower |
| Strictly decreasing | `n=4, [4,3,2,1]` | 1 | All fit in one tower |
| Large values | `n=2, [10^9, 1]` | 1 | Handle large integers |
| Alternating | `n=4, [1,3,2,4]` | 2 | Tests greedy placement |

---

## When to Use This Pattern

### Use This Approach When:
- You need to partition a sequence into minimum number of monotonic subsequences
- Greedy placement with "best fit" strategy applies
- You need efficient lookup of "next larger/smaller" element

### Don't Use When:
- You need the actual subsequences, not just the count (need to track assignments)
- The placement rule is more complex (may need DP)
- Elements can be reordered (different problem)

### Pattern Recognition Checklist:
- [ ] Placing items in order into containers with size constraints? -> **Greedy + Binary Search**
- [ ] Minimizing number of decreasing subsequences? -> **This is LIS length by Dilworth's theorem**
- [ ] Need upper_bound/lower_bound repeatedly? -> **Use multiset (C++) or SortedList (Python)**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Longest Increasing Subsequence (CSES)](https://cses.fi/problemset/task/1145) | Classic LIS with binary search |
| [LIS (LeetCode 300)](https://leetcode.com/problems/longest-increasing-subsequence/) | Same technique, different framing |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Russian Doll Envelopes (LC 354)](https://leetcode.com/problems/russian-doll-envelopes/) | 2D version of LIS |
| [Book Shop (CSES)](https://cses.fi/problemset/task/1158) | Knapsack but similar greedy thinking |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Increasing Subsequence (CSES)](https://cses.fi/problemset/task/1145) | Need to reconstruct the actual LIS |
| [Non-overlapping Intervals (LC 435)](https://leetcode.com/problems/non-overlapping-intervals/) | Interval scheduling, related greedy |

---

## Key Takeaways

1. **The Core Idea:** Greedily place each cube on the smallest valid tower top (upper_bound), creating new towers only when necessary.
2. **Time Optimization:** Binary search on sorted tower tops reduces O(n^2) brute force to O(n log n).
3. **Space Trade-off:** O(n) space to store tower tops enables O(log n) lookup.
4. **Pattern:** Greedy + Binary Search for partition into monotonic subsequences.

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Solve this problem without looking at the solution
- [ ] Explain why greedy with upper_bound is optimal
- [ ] Implement using multiset (C++) or bisect (Python) in under 10 minutes
- [ ] Explain the connection to LIS and Dilworth's theorem
- [ ] Handle edge cases (all same, increasing, decreasing)

---

## Additional Resources

- [CSES Problem Set](https://cses.fi/problemset/)
- [CP-Algorithms: LIS](https://cp-algorithms.com/sequences/longest_increasing_subsequence.html)
- [Dilworth's Theorem (Wikipedia)](https://en.wikipedia.org/wiki/Dilworth%27s_theorem)
