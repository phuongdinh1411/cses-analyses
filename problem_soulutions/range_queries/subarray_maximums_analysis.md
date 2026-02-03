---
layout: simple
title: "Static Range Maximum Queries - Range Queries Problem"
permalink: /problem_soulutions/range_queries/subarray_maximums_analysis
difficulty: Medium
tags: [sparse-table, range-queries, preprocessing, rmq]
prerequisites: []
---

# Static Range Maximum Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Medium |
| **Category** | Range Queries |
| **Time Limit** | 1 second |
| **Key Technique** | Sparse Table |
| **CSES Link** | [Static Range Maximum Queries](https://cses.fi/problemset/task/1647) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Understand the Sparse Table data structure for idempotent range queries
- [ ] Implement O(n log n) preprocessing for O(1) range queries
- [ ] Recognize when Sparse Table is preferred over Segment Tree
- [ ] Handle edge cases in range query problems

---

## Problem Statement

**Problem:** Given an array of n integers and q queries, answer each query asking for the maximum element in a subarray [a, b].

**Input:**
- Line 1: Two integers n and q (array size and number of queries)
- Line 2: n integers x_1, x_2, ..., x_n (array elements)
- Next q lines: Two integers a and b (query range, 1-indexed)

**Output:**
- For each query, print the maximum element in the range [a, b]

**Constraints:**
- 1 <= n, q <= 2 x 10^5
- 1 <= x_i <= 10^9
- 1 <= a <= b <= n

### Example

```
Input:
8 4
3 2 4 5 1 1 5 3
2 4
5 6
1 8
3 3

Output:
5
1
5
4
```

**Explanation:**
- Query [2,4]: max(2, 4, 5) = 5
- Query [5,6]: max(1, 1) = 1
- Query [1,8]: max(3, 2, 4, 5, 1, 1, 5, 3) = 5
- Query [3,3]: max(4) = 4

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we precompute information to answer range maximum queries in O(1) time?

The Sparse Table exploits a key property of the maximum operation: it is **idempotent** (max(a, a) = a). This means overlapping ranges give the correct answer. We can cover any range [L, R] with just two precomputed ranges of length 2^k that might overlap.

### Breaking Down the Problem

1. **What are we looking for?** Maximum value in any given range
2. **What information do we have?** Static array (no updates)
3. **What's the relationship between input and output?** max(arr[L..R]) for each query

### Analogies

Think of this like creating a lookup table for "best scores in time periods." If you know the best score for days 1-4 and days 5-8, you can quickly find the best score for days 2-7 by just comparing two precomputed values (since finding the max of overlapping periods still gives the correct answer).

---

## Solution 1: Brute Force

### Idea

For each query, iterate through the range and find the maximum element directly.

### Algorithm

1. Read all queries
2. For each query [L, R], iterate from L to R
3. Track and return the maximum value found

### Code

```python
def solve_brute_force(n, arr, queries):
    """
    Brute force: scan each query range.

    Time: O(q * n) per query
    Space: O(1) auxiliary
    """
    results = []
    for l, r in queries:
        max_val = arr[l - 1]  # Convert to 0-indexed
        for i in range(l - 1, r):
            max_val = max(max_val, arr[i])
        results.append(max_val)
    return results
```

```cpp
#include <bits/stdc++.h>
using namespace std;

vector<int> solveBruteForce(int n, vector<int>& arr, vector<pair<int,int>>& queries) {
    vector<int> results;
    for (auto& [l, r] : queries) {
        int maxVal = arr[l - 1];  // Convert to 0-indexed
        for (int i = l - 1; i < r; i++) {
            maxVal = max(maxVal, arr[i]);
        }
        results.push_back(maxVal);
    }
    return results;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(q * n) | Each query scans up to n elements |
| Space | O(1) | Only stores current maximum |

### Why This Works (But Is Slow)

Correctness is guaranteed because we check every element. However, with q and n up to 2 x 10^5, this gives 4 x 10^10 operations, far too slow for the 1-second limit.

---

## Solution 2: Optimal - Sparse Table

### Key Insight

> **The Trick:** Precompute maximums for all ranges of length 2^k. Any range can be covered by at most 2 overlapping power-of-2 ranges, and since max is idempotent, overlapping is fine.

### Sparse Table Definition

| State | Meaning |
|-------|---------|
| `st[i][j]` | Maximum value in range [i, i + 2^j - 1] |

**In plain English:** st[i][j] stores the maximum of 2^j consecutive elements starting at index i.

### Building the Sparse Table

```
st[i][0] = arr[i]                                    (base case: range of length 1)
st[i][j] = max(st[i][j-1], st[i + 2^(j-1)][j-1])    (combine two halves)
```

**Why?** A range of length 2^j is the union of two ranges of length 2^(j-1). The maximum of the whole is the maximum of the two halves.

### Query Strategy

For range [L, R] with length = R - L + 1:
1. Find k = floor(log2(length))
2. Answer = max(st[L][k], st[R - 2^k + 1][k])

The two ranges [L, L+2^k-1] and [R-2^k+1, R] together cover [L, R] completely.

### Algorithm

1. Precompute log values for O(1) lookup
2. Build sparse table in O(n log n)
3. Answer each query in O(1)

### Dry Run Example

Let's trace through with input `arr = [3, 2, 4, 5, 1, 1, 5, 3]` (0-indexed):

```
Building Sparse Table:

j=0 (ranges of length 1):
  st[0][0]=3, st[1][0]=2, st[2][0]=4, st[3][0]=5
  st[4][0]=1, st[5][0]=1, st[6][0]=5, st[7][0]=3

j=1 (ranges of length 2):
  st[0][1] = max(st[0][0], st[1][0]) = max(3,2) = 3  // [0,1]
  st[1][1] = max(st[1][0], st[2][0]) = max(2,4) = 4  // [1,2]
  st[2][1] = max(st[2][0], st[3][0]) = max(4,5) = 5  // [2,3]
  st[3][1] = max(st[3][0], st[4][0]) = max(5,1) = 5  // [3,4]
  st[4][1] = max(st[4][0], st[5][0]) = max(1,1) = 1  // [4,5]
  st[5][1] = max(st[5][0], st[6][0]) = max(1,5) = 5  // [5,6]
  st[6][1] = max(st[6][0], st[7][0]) = max(5,3) = 5  // [6,7]

j=2 (ranges of length 4):
  st[0][2] = max(st[0][1], st[2][1]) = max(3,5) = 5  // [0,3]
  st[1][2] = max(st[1][1], st[3][1]) = max(4,5) = 5  // [1,4]
  st[2][2] = max(st[2][1], st[4][1]) = max(5,1) = 5  // [2,5]
  st[3][2] = max(st[3][1], st[5][1]) = max(5,5) = 5  // [3,6]
  st[4][2] = max(st[4][1], st[6][1]) = max(1,5) = 5  // [4,7]

j=3 (ranges of length 8):
  st[0][3] = max(st[0][2], st[4][2]) = max(5,5) = 5  // [0,7]

Query [2,4] (1-indexed) = [1,3] (0-indexed):
  length = 3, k = floor(log2(3)) = 1
  Answer = max(st[1][1], st[3-2+1][1]) = max(st[1][1], st[2][1])
         = max(4, 5) = 5
```

### Visual Diagram

```
Array (0-indexed): [3, 2, 4, 5, 1, 1, 5, 3]
                    0  1  2  3  4  5  6  7

Sparse Table Coverage for query [1,3]:

j=1: length=2
     st[1][1] covers [1,2]: max(2,4) = 4
     st[2][1] covers [2,3]: max(4,5) = 5

     [1  2  3]
      |--|     <- st[1][1] = 4
         |--|  <- st[2][1] = 5

     Final: max(4, 5) = 5
```

### Code

```python
import sys
from math import log2

def solve():
    input_data = sys.stdin.read().split()
    idx = 0
    n, q = int(input_data[idx]), int(input_data[idx + 1])
    idx += 2

    arr = [int(input_data[idx + i]) for i in range(n)]
    idx += n

    # Precompute logs
    LOG = [0] * (n + 1)
    for i in range(2, n + 1):
        LOG[i] = LOG[i // 2] + 1

    # Build sparse table
    K = LOG[n] + 1
    st = [[0] * K for _ in range(n)]

    # Base case: ranges of length 1
    for i in range(n):
        st[i][0] = arr[i]

    # Fill for lengths 2^j
    for j in range(1, K):
        for i in range(n - (1 << j) + 1):
            st[i][j] = max(st[i][j - 1], st[i + (1 << (j - 1))][j - 1])

    # Answer queries
    results = []
    for _ in range(q):
        l, r = int(input_data[idx]) - 1, int(input_data[idx + 1]) - 1  # 0-indexed
        idx += 2

        length = r - l + 1
        k = LOG[length]
        ans = max(st[l][k], st[r - (1 << k) + 1][k])
        results.append(ans)

    print('\n'.join(map(str, results)))

if __name__ == "__main__":
    solve()
```

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MAXN = 200005;
const int MAXLOG = 18;

int st[MAXN][MAXLOG];
int LOG[MAXN];

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;

    // Precompute logs
    LOG[1] = 0;
    for (int i = 2; i <= n; i++) {
        LOG[i] = LOG[i / 2] + 1;
    }

    // Read array and initialize base case
    for (int i = 0; i < n; i++) {
        cin >> st[i][0];
    }

    // Build sparse table
    for (int j = 1; j < MAXLOG; j++) {
        for (int i = 0; i + (1 << j) <= n; i++) {
            st[i][j] = max(st[i][j - 1], st[i + (1 << (j - 1))][j - 1]);
        }
    }

    // Answer queries
    while (q--) {
        int l, r;
        cin >> l >> r;
        l--; r--;  // Convert to 0-indexed

        int len = r - l + 1;
        int k = LOG[len];
        cout << max(st[l][k], st[r - (1 << k) + 1][k]) << '\n';
    }

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(n log n + q) | O(n log n) preprocessing, O(1) per query |
| Space | O(n log n) | Sparse table storage |

---

## Common Mistakes

### Mistake 1: Wrong Log Calculation

```python
# WRONG - might cause index out of bounds
k = int(log2(length))  # Floating point errors possible

# CORRECT - precompute integer logs
LOG[i] = LOG[i // 2] + 1
```

**Problem:** Floating-point log2 can have precision errors.
**Fix:** Precompute integer logarithms in a table.

### Mistake 2: Off-by-One in Sparse Table Bounds

```cpp
// WRONG
for (int i = 0; i + (1 << j) < n; i++)  // Missing the last valid range

// CORRECT
for (int i = 0; i + (1 << j) <= n; i++)  // Include boundary
```

**Problem:** Missing valid ranges at the end of the array.
**Fix:** Use `<= n` instead of `< n` for the loop bound.

### Mistake 3: Not Converting to 0-indexed

```python
# WRONG - using 1-indexed directly
ans = max(st[l][k], st[r - (1 << k) + 1][k])  # l, r are 1-indexed!

# CORRECT - convert first
l -= 1
r -= 1
ans = max(st[l][k], st[r - (1 << k) + 1][k])
```

**Problem:** CSES uses 1-indexed input, but arrays are 0-indexed.
**Fix:** Convert indices before querying.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single element query | `[5], query [1,1]` | 5 | Range contains only one element |
| Entire array | `[1,2,3], query [1,3]` | 3 | k = log2(3) = 1, overlapping ranges |
| All same values | `[7,7,7], query [1,3]` | 7 | Maximum is still correct |
| Large values | `[10^9, 1], query [1,2]` | 10^9 | Handle large integers |
| n = 1 | `[42], query [1,1]` | 42 | Minimal input size |

---

## When to Use This Pattern

### Use Sparse Table When:
- Queries are on a **static array** (no updates)
- The operation is **idempotent** (max, min, gcd, AND, OR)
- You need **O(1) query time** after preprocessing
- Memory O(n log n) is acceptable

### Don't Use When:
- Array has **dynamic updates** (use Segment Tree instead)
- Operation is **not idempotent** (sum, product - use Segment Tree)
- Memory is very constrained (Segment Tree uses O(n))
- Only a few queries (brute force may be simpler)

### Pattern Recognition Checklist:
- [ ] Static array with no updates? --> **Consider Sparse Table**
- [ ] Operation is max/min/gcd/AND/OR? --> **Sparse Table works**
- [ ] Need O(1) queries? --> **Sparse Table is optimal**
- [ ] Updates required? --> **Use Segment Tree instead**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Static Range Sum Queries](https://cses.fi/problemset/task/1646) | Prefix sums for range queries |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Static Range Minimum Queries](https://cses.fi/problemset/task/1647) | Same problem with min instead of max |
| [Range Minimum Query (RMQ)](https://www.spoj.com/problems/RMQSQ/) | Classic RMQ problem |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Dynamic Range Minimum Queries](https://cses.fi/problemset/task/1649) | Adds point updates, needs Segment Tree |
| [Range Update Queries](https://cses.fi/problemset/task/1651) | Range updates with lazy propagation |
| [Forest Queries](https://cses.fi/problemset/task/1652) | 2D prefix sums |

---

## Key Takeaways

1. **The Core Idea:** Precompute maximums for all power-of-2 length ranges; any query can be answered with 2 overlapping ranges
2. **Time Optimization:** From O(n) per query to O(1) per query with O(n log n) preprocessing
3. **Space Trade-off:** Use O(n log n) space to achieve O(1) query time
4. **Pattern:** Sparse Table for idempotent range queries on static arrays

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why overlapping ranges work for max/min but not for sum
- [ ] Build a sparse table from scratch without reference
- [ ] Calculate the correct k value for any query range
- [ ] Implement in your preferred language in under 15 minutes

---

## Additional Resources

- [CP-Algorithms: Sparse Table](https://cp-algorithms.com/data_structures/sparse-table.html)
- [CSES Problem Set - Range Queries](https://cses.fi/problemset/list/)
- [TopCoder: Range Minimum Query and Lowest Common Ancestor](https://www.topcoder.com/thrive/articles/Range%20Minimum%20Query%20and%20Lowest%20Common%20Ancestor)
