---
layout: simple
title: "Range Update Queries - Difference Array & BIT"
permalink: /problem_soulutions/range_queries/range_update_queries_analysis
difficulty: Medium
tags: [range-queries, difference-array, fenwick-tree, bit]
prerequisites: [prefix-sums, static-range-sum-queries]
---

# Range Update Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Problem Link** | [CSES 1651 - Range Update Queries](https://cses.fi/problemset/task/1651) |
| **Difficulty** | Medium |
| **Category** | Range Queries |
| **Time Limit** | 1 second |
| **Key Technique** | Difference Array / BIT for Range Updates |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand how difference arrays convert range updates to point updates
- [ ] Implement BIT (Fenwick Tree) for range add + point query operations
- [ ] Recognize when to use difference array vs segment tree
- [ ] Apply the duality between range/point operations

---

## Problem Statement

**Problem:** Given an array of n integers, process q queries of two types:
1. **Update**: Add value u to all elements in range [a, b]
2. **Query**: Output the value at position k

**Input:**
- Line 1: n (array size), q (number of queries)
- Line 2: n integers (initial array values)
- Next q lines: Either "1 a b u" (range update) or "2 k" (point query)

**Output:**
- For each type 2 query, print the value at position k

**Constraints:**
- 1 <= n, q <= 2 * 10^5
- 1 <= a <= b <= n
- 1 <= k <= n
- -10^9 <= initial values, u <= 10^9

### Example

```
Input:
8 3
3 2 4 5 1 1 5 3
1 2 5 2
2 3
2 4

Output:
6
7
```

**Explanation:**
- Initial array: [3, 2, 4, 5, 1, 1, 5, 3]
- After adding 2 to range [2,5]: [3, 4, 6, 7, 3, 1, 5, 3]
- Query position 3: value is 6
- Query position 4: value is 7

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** We have range updates but only point queries. Can we transform this into something simpler?

The insight is that **range update + point query** is the dual of **point update + range query**. Using a difference array, we can convert a range update into two point updates.

### Breaking Down the Problem

1. **What are we looking for?** The value at a specific position after all updates
2. **What information do we have?** Initial array + range updates (add value to [a,b])
3. **What's the relationship?** Final value = initial value + sum of all updates affecting that position

### The Difference Array Trick

For a range update `add(a, b, u)`:
- Instead of updating all positions from a to b
- We mark: `diff[a] += u` and `diff[b+1] -= u`
- The prefix sum of diff gives the total update at any position

```
Original update: add 2 to [2, 5]
  Index:     1   2   3   4   5   6   7   8
  Effect:    0  +2  +2  +2  +2   0   0   0

Difference array encoding:
  diff:      0  +2   0   0   0  -2   0   0

Prefix sum of diff = Effect at each position
```

---

## Solution 1: Brute Force

### Idea

For each range update, iterate through and update all elements. For point queries, directly return the value.

### Code

```python
def solve_brute_force(n, arr, queries):
    """
    Brute force: directly apply range updates.

    Time: O(q * n) - each update touches up to n elements
    Space: O(n)
    """
    results = []

    for query in queries:
        if query[0] == 1:
            a, b, u = query[1], query[2], query[3]
            for i in range(a - 1, b):  # Convert to 0-indexed
                arr[i] += u
        else:
            k = query[1]
            results.append(arr[k - 1])

    return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(q * n) | Each update may modify n elements |
| Space | O(n) | Just the array |

### Why This Works (But Is Slow)

Correctness is guaranteed - we literally perform each update. But with q = 2*10^5 queries and n = 2*10^5 elements, worst case is 4*10^10 operations, way too slow.

---

## Solution 2: Difference Array (Offline)

### Key Insight

> **The Trick:** If we process all updates first, then all queries, we can use a difference array with O(1) updates and O(n) prefix sum computation.

This only works if queries come after all updates (offline processing).

### How Difference Array Works

| Concept | Description |
|---------|-------------|
| `diff[i]` | The change in value from position i-1 to i |
| `add(a, b, u)` | Set `diff[a] += u`, `diff[b+1] -= u` |
| `get(k)` | Compute prefix sum of diff from 1 to k |

### Code

```python
def solve_difference_array_offline(n, arr, queries):
    """
    Difference array for offline processing.
    Only works if all updates come before all queries.

    Time: O(n + q)
    Space: O(n)
    """
    diff = [0] * (n + 2)  # Extra space to avoid boundary checks

    # Separate updates and queries
    updates = [(q[1], q[2], q[3]) for q in queries if q[0] == 1]
    point_queries = [q[1] for q in queries if q[0] == 2]

    # Apply all updates to difference array
    for a, b, u in updates:
        diff[a] += u
        diff[b + 1] -= u

    # Convert difference array to actual updates via prefix sum
    total_update = [0] * (n + 1)
    running_sum = 0
    for i in range(1, n + 1):
        running_sum += diff[i]
        total_update[i] = running_sum

    # Answer queries
    results = []
    for k in point_queries:
        results.append(arr[k - 1] + total_update[k])

    return results
```

**Limitation:** This does NOT work for the actual problem since updates and queries are interleaved.

---

## Solution 3: BIT (Fenwick Tree) for Range Update + Point Query

### Key Insight

> **The Trick:** Use a BIT on the difference array concept. Range update becomes two point updates on BIT. Point query becomes prefix sum query on BIT.

### BIT State Definition

| State | Meaning |
|-------|---------|
| `bit[i]` | Stores difference values in BIT structure |
| `update(i, delta)` | Add delta to position i (and propagate) |
| `query(i)` | Get prefix sum from 1 to i (total update at position i) |

### Why BIT Works Here

1. **Range Update `add(a, b, u)`**:
   - `bit.update(a, +u)` - updates starting at a
   - `bit.update(b+1, -u)` - cancel updates after b

2. **Point Query `get(k)`**:
   - `arr[k] + bit.query(k)` - original value + sum of all updates affecting k

### Dry Run Example

Let's trace through: `n=8, arr=[3,2,4,5,1,1,5,3]`

```
Initial:
  arr = [3, 2, 4, 5, 1, 1, 5, 3]
  BIT = [0, 0, 0, 0, 0, 0, 0, 0, 0]  (1-indexed, index 0 unused)

Query 1: add 2 to range [2, 5]
  BIT.update(2, +2):  BIT becomes [0, 0, 2, 2, 0, 0, 0, 0, 0]
  BIT.update(6, -2):  BIT becomes [0, 0, 2, 2, 0, 0, -2, 0, -2]

  (Internal BIT representation, prefix sums give actual values)
  Prefix sums: [0, 0, 2, 2, 2, 2, 0, 0, 0]

Query 2: get value at position 3
  BIT.query(3) = 2  (prefix sum up to index 3)
  Answer = arr[3-1] + 2 = 4 + 2 = 6

Query 3: get value at position 4
  BIT.query(4) = 2
  Answer = arr[4-1] + 2 = 5 + 2 = 7
```

### Code (Python)

```python
import sys
from typing import List

def solve():
    input_data = sys.stdin.buffer.read().split()
    idx = 0

    n = int(input_data[idx]); idx += 1
    q = int(input_data[idx]); idx += 1

    arr = [0] * (n + 1)  # 1-indexed
    for i in range(1, n + 1):
        arr[i] = int(input_data[idx]); idx += 1

    # BIT for range updates (stores difference array)
    bit = [0] * (n + 2)

    def update(i: int, delta: int):
        """Add delta to position i"""
        while i <= n:
            bit[i] += delta
            i += i & (-i)

    def query(i: int) -> int:
        """Get prefix sum from 1 to i"""
        total = 0
        while i > 0:
            total += bit[i]
            i -= i & (-i)
        return total

    results = []

    for _ in range(q):
        query_type = int(input_data[idx]); idx += 1

        if query_type == 1:
            a = int(input_data[idx]); idx += 1
            b = int(input_data[idx]); idx += 1
            u = int(input_data[idx]); idx += 1
            # Range update: add u to [a, b]
            update(a, u)
            update(b + 1, -u)
        else:
            k = int(input_data[idx]); idx += 1
            # Point query: get value at k
            answer = arr[k] + query(k)
            results.append(answer)

    print('\n'.join(map(str, results)))

if __name__ == "__main__":
    solve()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

int n, q;
vector<long long> arr, bit;

void update(int i, long long delta) {
    for (; i <= n; i += i & (-i))
        bit[i] += delta;
}

long long query(int i) {
    long long sum = 0;
    for (; i > 0; i -= i & (-i))
        sum += bit[i];
    return sum;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> n >> q;

    arr.resize(n + 1);
    bit.resize(n + 2, 0);

    for (int i = 1; i <= n; i++) {
        cin >> arr[i];
    }

    while (q--) {
        int type;
        cin >> type;

        if (type == 1) {
            int a, b;
            long long u;
            cin >> a >> b >> u;
            update(a, u);
            update(b + 1, -u);
        } else {
            int k;
            cin >> k;
            cout << arr[k] + query(k) << '\n';
        }
    }

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O((n + q) log n) | Each update/query is O(log n) |
| Space | O(n) | BIT array of size n |

---

## Common Mistakes

### Mistake 1: Forgetting the +1 Offset for Cancellation

```python
# WRONG - only marks start of update
def range_update(a, b, u):
    update(a, u)
    # Missing: update(b + 1, -u)

# CORRECT
def range_update(a, b, u):
    update(a, u)
    update(b + 1, -u)  # Cancel the update after position b
```

**Problem:** Without cancellation, the update extends to the end of the array.

### Mistake 2: Using Wrong Data Type

```cpp
// WRONG - may overflow with 10^9 values and 2*10^5 updates
int bit[200005];

// CORRECT
long long bit[200005];
```

**Problem:** Sum of updates can reach 2*10^14, which overflows 32-bit integers.

### Mistake 3: Off-by-One in 1-indexed BIT

```python
# WRONG - BIT is 1-indexed, but accessing arr[k] directly
answer = arr[k] + query(k)  # If arr is 0-indexed, this is wrong

# CORRECT - ensure consistent indexing
arr = [0] + original_arr  # Make arr 1-indexed too
answer = arr[k] + query(k)
```

### Mistake 4: Boundary Access

```python
# WRONG - may access bit[n+1] which could be out of bounds
update(b + 1, -u)  # When b == n

# CORRECT - allocate extra space
bit = [0] * (n + 2)  # Extra element for safety
```

---

## Edge Cases

| Case | Input | Expected Behavior | Why |
|------|-------|-------------------|-----|
| Single element | n=1, update [1,1] | Works normally | BIT handles single position |
| Full range update | update [1, n] | All elements modified | update(n+1, -u) goes to unused space |
| No updates | Only queries | Return original values | BIT query returns 0 |
| Negative updates | u = -10^9 | Handle correctly | BIT works with negative values |
| Large accumulated updates | Many updates on same position | Use long long | Sum can exceed int range |
| Query before any update | First query is type 2 | Return original value | BIT initialized to 0 |

---

## When to Use This Pattern

### Use Difference Array / BIT When:
- You have **range updates** (add value to range)
- You have **point queries** (get single element value)
- Updates and queries are **interleaved** (use BIT)
- Updates come before all queries (can use simple difference array)

### Don't Use When:
- You need **range queries** (sum of range) - use lazy segment tree or two BITs
- Updates are **assignment** not **addition** - use segment tree
- You need to query **maximum/minimum** in range - use segment tree

### Pattern Recognition Checklist:
- [ ] Range add update + Point query? --> **BIT on difference array**
- [ ] Point update + Range sum query? --> **Standard BIT**
- [ ] Range add update + Range sum query? --> **Two BITs or Lazy Segment Tree**
- [ ] Range assignment + Any query? --> **Segment Tree with Lazy Propagation**

---

## Related Problems

### Easier (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Static Range Sum Queries](https://cses.fi/problemset/task/1646) | Understand prefix sums |
| [Dynamic Range Sum Queries](https://cses.fi/problemset/task/1648) | Basic BIT for point update + range query |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Range Xor Queries](https://cses.fi/problemset/task/1650) | XOR instead of sum, uses prefix XOR |
| [Forest Queries](https://cses.fi/problemset/task/1652) | 2D prefix sums |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Range Update Range Queries](https://cses.fi/problemset/task/1651) | Need two BITs or lazy segment tree |
| [Polynomial Queries](https://cses.fi/problemset/task/1736) | Arithmetic sequence updates |
| [Range Queries and Copies](https://cses.fi/problemset/task/1737) | Persistent data structures |

---

## Key Takeaways

1. **The Core Idea:** Transform range updates into point updates using difference array concept
2. **Time Optimization:** From O(q*n) brute force to O(q log n) using BIT
3. **Space Trade-off:** O(n) extra space for BIT array
4. **Pattern:** Range update + point query is the dual of point update + range query

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain how difference arrays work
- [ ] Implement BIT update and query from scratch
- [ ] Identify when to use this pattern vs segment tree
- [ ] Handle 1-indexed vs 0-indexed correctly
- [ ] Use appropriate data types to avoid overflow

---

## Additional Resources

- [CP-Algorithms: Fenwick Tree](https://cp-algorithms.com/data_structures/fenwick.html)
- [CSES Range Update Queries](https://cses.fi/problemset/task/1651) - Difference array technique
- [Difference Array Technique](https://www.geeksforgeeks.org/difference-array-range-update-query-o1/)
