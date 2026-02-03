---
layout: simple
title: "Pizzeria Queries - Segment Tree with Transformation"
permalink: /problem_soulutions/range_queries/pizzeria_queries_analysis
difficulty: Hard
tags: [segment-tree, range-minimum, point-update, transformation]
prerequisites: [dynamic_range_minimum_queries, dynamic_range_sum_queries]
---

# Pizzeria Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Range Queries |
| **Time Limit** | 1.0 seconds |
| **CSES Link** | [Pizzeria Queries](https://cses.fi/problemset/task/2206) |
| **Key Technique** | Two Segment Trees with Coordinate Transformation |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Transform absolute value expressions into range minimum queries
- [ ] Recognize when to split `|i - j|` into two separate cases
- [ ] Use two segment trees to handle left and right directions independently
- [ ] Apply point updates efficiently with transformed coordinates

---

## Problem Statement

**Problem:** There are n buildings on a street numbered 1 to n. Each building i has a pizzeria with price p[i]. Handle two query types:

1. **Update query**: Change the price at building k to x
2. **Minimum cost query**: Find minimum cost at position k, where cost = price[j] + |k - j|

**Input:**
- Line 1: n and q (buildings and queries)
- Line 2: n integers p[1]...p[n] (initial prices)
- Next q lines: "1 k x" (update) or "2 k" (query)

**Output:** For each type-2 query, output the minimum cost

**Constraints:** 1 <= n, q <= 2*10^5; 1 <= p[i], x <= 10^9

### Example

```
Input:
5 4
3 2 4 1 5
2 3
1 4 8
2 3
2 5

Output:
2
3
5
```

**Explanation:**
- Query "2 3": costs = (5, 3, 4, 2, 7), min = 2 from building 4
- Update "1 4 8": Price at building 4 becomes 8
- Query "2 3": costs = (5, 3, 4, 9, 7), min = 3 from building 2
- Query "2 5": costs = (7, 5, 6, 9, 5), min = 5

---

## Intuition: How to Think About This Problem

### The Core Challenge

We need to find: `min over all j of (p[j] + |k - j|)`

The absolute value is problematic for range queries. The key insight is to **split the absolute value** based on whether j is left or right of k.

### Mathematical Transformation

**Case 1: j <= k (pizzeria to the left)**
```
cost = p[j] + (k - j) = (p[j] - j) + k
```

**Case 2: j >= k (pizzeria to the right)**
```
cost = p[j] + (j - k) = (p[j] + j) - k
```

### The Key Insight

> **Transformation Trick:** By rearranging terms, we separate k from pizzeria values:
> - `min(p[j] - j)` for j in [1, k] -> add k for left-side minimum
> - `min(p[j] + j)` for j in [k, n] -> subtract k for right-side minimum

This transforms the problem into **two range minimum queries**!

---

## Solution 1: Brute Force

```python
def brute_force(n, prices, queries):
    """Time: O(q * n), Space: O(n)"""
    p = prices[:]
    results = []
    for query in queries:
        if query[0] == 1:
            p[query[1] - 1] = query[2]
        else:
            k = query[1]
            min_cost = min(p[j] + abs((k-1) - j) for j in range(n))
            results.append(min_cost)
    return results
```

With q, n up to 2*10^5, this gives 4*10^10 operations - too slow.

---

## Solution 2: Optimal - Two Segment Trees

### Data Structure Design

| Structure | Stores | Purpose |
|-----------|--------|---------|
| `left_tree` | `p[i] - i` | Query min for j <= k |
| `right_tree` | `p[i] + i` | Query min for j >= k |

### Algorithm

1. **Build:** `left_tree[i] = p[i] - i`, `right_tree[i] = p[i] + i`
2. **Update k to x:** Update both trees with `x - k` and `x + k`
3. **Query k:** Return `min(left_tree.query(1,k) + k, right_tree.query(k,n) - k)`

### Dry Run Example

```
Initial (1-indexed): prices = [3, 2, 4, 1, 5]
  p[i] - i:  [2, 0, 1, -3, 0]   (left_tree)
  p[i] + i:  [4, 4, 7, 5, 10]   (right_tree)

Query k=3:
  Left [1,3]:  min(2,0,1) = 0  -> 0 + 3 = 3
  Right [3,5]: min(7,5,10) = 5 -> 5 - 3 = 2
  Answer: min(3, 2) = 2

Update k=4, x=8:
  left_tree[4]  = 8 - 4 = 4
  right_tree[4] = 8 + 4 = 12

Query k=3:
  Left [1,3]:  min(2,0,1) = 0  -> 0 + 3 = 3
  Right [3,5]: min(7,12,10) = 7 -> 7 - 3 = 4
  Answer: min(3, 4) = 3
```

### Code (Python)

```python
import sys
from math import inf

def solve():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n, q = int(data[idx]), int(data[idx+1]); idx += 2

    prices = [0] + [int(data[idx+i]) for i in range(n)]; idx += n

    size = 1
    while size < n: size *= 2

    left_tree = [inf] * (2 * size)
    right_tree = [inf] * (2 * size)

    for i in range(1, n + 1):
        left_tree[size + i - 1] = prices[i] - i
        right_tree[size + i - 1] = prices[i] + i

    for i in range(size - 1, 0, -1):
        left_tree[i] = min(left_tree[2*i], left_tree[2*i+1])
        right_tree[i] = min(right_tree[2*i], right_tree[2*i+1])

    def update(tree, pos, val):
        pos = size + pos - 1
        tree[pos] = val
        pos //= 2
        while pos >= 1:
            tree[pos] = min(tree[2*pos], tree[2*pos+1])
            pos //= 2

    def query(tree, l, r):
        res = inf
        l, r = size + l - 1, size + r - 1
        while l <= r:
            if l % 2 == 1: res = min(res, tree[l]); l += 1
            if r % 2 == 0: res = min(res, tree[r]); r -= 1
            l //= 2; r //= 2
        return res

    results = []
    for _ in range(q):
        t = int(data[idx]); idx += 1
        if t == 1:
            k, x = int(data[idx]), int(data[idx+1]); idx += 2
            update(left_tree, k, x - k)
            update(right_tree, k, x + k)
        else:
            k = int(data[idx]); idx += 1
            left_min = query(left_tree, 1, k) + k
            right_min = query(right_tree, k, n) - k
            results.append(min(left_min, right_min))

    print('\n'.join(map(str, results)))

if __name__ == "__main__":
    solve()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

const long long INF = 1e18;

class SegmentTree {
    int n, size;
    vector<long long> tree;
public:
    SegmentTree(int n) : n(n) {
        size = 1;
        while (size < n) size *= 2;
        tree.assign(2 * size, INF);
    }

    void build(const vector<long long>& v) {
        for (int i = 0; i < n; i++) tree[size + i] = v[i];
        for (int i = size - 1; i >= 1; i--)
            tree[i] = min(tree[2*i], tree[2*i+1]);
    }

    void update(int pos, long long val) {
        pos += size;
        tree[pos] = val;
        for (pos /= 2; pos >= 1; pos /= 2)
            tree[pos] = min(tree[2*pos], tree[2*pos+1]);
    }

    long long query(int l, int r) {
        long long res = INF;
        for (l += size, r += size; l <= r; l /= 2, r /= 2) {
            if (l % 2 == 1) res = min(res, tree[l++]);
            if (r % 2 == 0) res = min(res, tree[r--]);
        }
        return res;
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;

    vector<long long> prices(n), left_vals(n), right_vals(n);
    for (int i = 0; i < n; i++) {
        cin >> prices[i];
        left_vals[i] = prices[i] - i;
        right_vals[i] = prices[i] + i;
    }

    SegmentTree left_tree(n), right_tree(n);
    left_tree.build(left_vals);
    right_tree.build(right_vals);

    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            int k; long long x;
            cin >> k >> x;
            k--;
            left_tree.update(k, x - k);
            right_tree.update(k, x + k);
        } else {
            int k;
            cin >> k;
            k--;
            long long left_min = left_tree.query(0, k) + k;
            long long right_min = right_tree.query(k, n-1) - k;
            cout << min(left_min, right_min) << "\n";
        }
    }
    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O((n + q) log n) | Build O(n), each query/update O(log n) |
| Space | O(n) | Two segment trees |

---

## Common Mistakes

### Mistake 1: Only Updating One Tree

```python
# WRONG
update(left_tree, k, x - k)
# Forgot right_tree!
```
**Fix:** Always update both trees on price change.

### Mistake 2: Wrong Query Boundaries

```python
# WRONG - excludes k
left_min = query(left_tree, 1, k - 1)
```
**Fix:** Include k in both queries: `[1, k]` and `[k, n]`.

### Mistake 3: Integer Overflow (C++)

```cpp
// WRONG
int left_val = price - index;  // May overflow

// CORRECT
long long left_val = (long long)price - index;
```

---

## Edge Cases

| Case | Handling |
|------|----------|
| Single building (n=1) | Return p[1], distance is 0 |
| Query at boundary (k=1 or k=n) | One range query gives INF, take other |
| Maximum values (10^9) | Use 64-bit integers |

---

## When to Use This Pattern

**Use when:**
- Cost formula includes `|i - j|` (absolute distance)
- You can split into "left" and "right" cases
- After splitting, expressions become range min/max queries
- Point updates are needed

**Pattern recognition:**
- Nearest facility with costs
- Distance-weighted selection
- Minimum travel cost problems

---

## Related Problems

### Easier
| Problem | Why It Helps |
|---------|--------------|
| [Dynamic Range Minimum Queries](https://cses.fi/problemset/task/1649) | Basic segment tree |
| [Range Minimum Queries](https://cses.fi/problemset/task/1647) | Static RMQ |

### Similar Difficulty
| Problem | Key Difference |
|---------|----------------|
| [Polynomial Queries](https://cses.fi/problemset/task/1736) | Lazy propagation |
| [Range Update Queries](https://cses.fi/problemset/task/1651) | Range updates |

### LeetCode Related
| Problem | Connection |
|---------|------------|
| [Shortest Distance to a Character](https://leetcode.com/problems/shortest-distance-to-a-character/) | Similar concept, simpler |
| [Range Sum Query - Mutable](https://leetcode.com/problems/range-sum-query-mutable/) | Segment tree practice |

---

## Key Takeaways

1. **Core Idea:** Transform `min(p[j] + |k-j|)` by splitting absolute value into left/right cases

2. **Math:** `|k-j| = k-j` when j <= k, and `j-k` when j >= k. This gives `(p[j]-j)+k` and `(p[j]+j)-k`

3. **Implementation:** Two segment trees storing `p[i]-i` and `p[i]+i`, query both and take minimum

4. **Pattern:** This "absolute value splitting" technique appears in many distance optimization problems

---

## Practice Checklist

- [ ] Derive the transformation from `p[j] + |k-j|` to two range queries
- [ ] Implement segment tree for range minimum with point updates
- [ ] Handle both 0-indexed and 1-indexed correctly
- [ ] Explain why we need TWO segment trees
- [ ] Solve in under 20 minutes
