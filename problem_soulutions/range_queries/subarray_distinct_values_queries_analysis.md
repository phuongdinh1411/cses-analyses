---
layout: simple
title: "Distinct Values Queries - Range Queries"
permalink: /problem_soulutions/range_queries/subarray_distinct_values_queries_analysis
difficulty: Hard
tags: [range-queries, BIT, offline-processing, Mo-algorithm]
prerequisites: [static_range_sum_queries, fenwick_tree_basics]
---

# Distinct Values Queries

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Range Queries |
| **Time Limit** | 1 second |
| **Key Technique** | Offline Processing + BIT / Mo's Algorithm |
| **CSES Link** | [Distinct Values Queries](https://cses.fi/problemset/task/1734) |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Apply offline query processing to transform a hard problem into a manageable one
- [ ] Use Binary Indexed Tree (BIT) for efficient range sum queries
- [ ] Track "last occurrence" of elements to avoid double counting
- [ ] Implement Mo's algorithm as an alternative approach
- [ ] Recognize when sorting queries by right endpoint is beneficial

---

## Problem Statement

**Problem:** Given an array of n integers and q queries, for each query (l, r), count the number of distinct values in the subarray from index l to r (inclusive).

**Input:**
- Line 1: Two integers n and q (array size and number of queries)
- Line 2: n integers (the array elements)
- Next q lines: Two integers l and r for each query (1-indexed)

**Output:**
- q lines: The number of distinct values in each queried range

**Constraints:**
- 1 <= n, q <= 2 * 10^5
- 1 <= arr[i] <= 10^9
- 1 <= l <= r <= n

### Example

```
Input:
5 3
3 2 3 1 2
1 3
2 4
1 5

Output:
2
3
3
```

**Explanation:**
- Query (1,3): Subarray [3, 2, 3] has distinct values {2, 3} = 2 distinct
- Query (2,4): Subarray [2, 3, 1] has distinct values {1, 2, 3} = 3 distinct
- Query (1,5): Subarray [3, 2, 3, 1, 2] has distinct values {1, 2, 3} = 3 distinct

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How do we count distinct elements efficiently when we cannot merge segment tree nodes?

The critical insight is that counting distinct values is **not decomposable** - knowing the distinct count in [l, mid] and [mid+1, r] does not help compute the distinct count in [l, r] because elements may appear in both halves.

### Breaking Down the Problem

1. **What are we looking for?** Count of unique elements in each range [l, r]
2. **What information do we have?** Static array, multiple queries
3. **What's the relationship between input and output?** For each (l, r), count elements appearing at least once in that range

### The Key Insight: Last Occurrence Tracking

Instead of counting elements directly, we can ask: **"For each position i, does the element at i contribute to the distinct count for range [l, r]?"**

An element at position i contributes to range [l, r] if:
1. l <= i <= r (it's within the range)
2. There is no occurrence of the same element at position j where l <= j < i (it's the first/leftmost occurrence in the range)

**Reformulation:** If we mark position i with 1 when arr[i]'s last occurrence before or at position r is exactly at position i, then the distinct count for [l, r] = sum of marks in [l, r].

---

## Solution 1: Brute Force

### Idea

For each query, iterate through the range and use a set to count distinct elements.

### Algorithm

1. For each query (l, r)
2. Add all elements in range [l, r] to a set
3. Return the size of the set

### Code

```python
def solve_brute_force(n, arr, queries):
    """
    Brute force: Use a set for each query.

    Time: O(q * n)
    Space: O(n)
    """
    results = []
    for l, r in queries:
        distinct = set()
        for i in range(l - 1, r):  # Convert to 0-indexed
            distinct.add(arr[i])
        results.append(len(distinct))
    return results
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(q * n) | Each query scans up to n elements |
| Space | O(n) | Set can hold up to n elements |

### Why This Works (But Is Slow)

Correctness is guaranteed because a set inherently stores only unique elements. However, with q and n up to 2 * 10^5, this gives 4 * 10^10 operations - far too slow.

---

## Solution 2: Offline Processing + BIT (Optimal)

### Key Insight

> **The Trick:** Process queries sorted by right endpoint. For each position, only mark the rightmost occurrence of each value up to the current position.

When we process queries in order of increasing right endpoint r:
- As we move r from 1 to n, we update a BIT where position i has value 1 if arr[i] is the rightmost occurrence of that value among positions 1 to r
- For query (l, r), the answer is sum(l, r) in the BIT

### Why This Works

When processing a query with right endpoint r:
- For each unique value, exactly one position (its rightmost occurrence up to r) has a 1 in the BIT
- Elements appearing multiple times are counted exactly once
- The range sum [l, r] counts how many "rightmost occurrences" fall within [l, r]

### Algorithm

1. Store queries as (l, r, original_index), sort by r
2. Maintain a BIT and a map: value -> its current marked position
3. Process array left to right (position i from 1 to n):
   - If arr[i] was previously marked at position p, unmark it (BIT subtract 1 at p)
   - Mark position i for arr[i] (BIT add 1 at i)
   - Update map: arr[i] -> i
   - Answer all queries with r == i: answer = BIT.sum(l, i)
4. Return answers in original query order

### Dry Run Example

Let's trace through with `arr = [3, 2, 3, 1, 2]` and queries `[(1,3), (2,4), (1,5)]`:

```
Sorted queries by r: [(1,3,0), (2,4,1), (1,5,2)]

Initial state:
  BIT = [0, 0, 0, 0, 0] (conceptually)
  last_pos = {}

Step 1: i = 1, arr[1] = 3
  3 not in last_pos
  BIT.add(1, +1) -> marks position 1
  last_pos = {3: 1}
  BIT state: [1, 0, 0, 0, 0]
  No query with r = 1

Step 2: i = 2, arr[2] = 2
  2 not in last_pos
  BIT.add(2, +1) -> marks position 2
  last_pos = {3: 1, 2: 2}
  BIT state: [1, 1, 0, 0, 0]
  No query with r = 2

Step 3: i = 3, arr[3] = 3
  3 IS in last_pos at position 1
  BIT.add(1, -1) -> unmarks position 1
  BIT.add(3, +1) -> marks position 3
  last_pos = {3: 3, 2: 2}
  BIT state: [0, 1, 1, 0, 0]
  Query (1, 3): sum(1, 3) = 0 + 1 + 1 = 2  [Answer for query 0]

Step 4: i = 4, arr[4] = 1
  1 not in last_pos
  BIT.add(4, +1) -> marks position 4
  last_pos = {3: 3, 2: 2, 1: 4}
  BIT state: [0, 1, 1, 1, 0]
  Query (2, 4): sum(2, 4) = 1 + 1 + 1 = 3  [Answer for query 1]

Step 5: i = 5, arr[5] = 2
  2 IS in last_pos at position 2
  BIT.add(2, -1) -> unmarks position 2
  BIT.add(5, +1) -> marks position 5
  last_pos = {3: 3, 2: 5, 1: 4}
  BIT state: [0, 0, 1, 1, 1]
  Query (1, 5): sum(1, 5) = 0 + 0 + 1 + 1 + 1 = 3  [Answer for query 2]

Final answers in original order: [2, 3, 3]
```

### Visual Diagram

```
Array:    [3, 2, 3, 1, 2]
Index:     1  2  3  4  5

Processing at i=5 (final state):
  Value 3: last at position 3  -> BIT[3] = 1
  Value 2: last at position 5  -> BIT[5] = 1  (moved from position 2)
  Value 1: last at position 4  -> BIT[4] = 1

BIT:      [0, 0, 1, 1, 1]
           1  2  3  4  5

Query (1,5): sum of BIT[1..5] = 3 distinct values
```

### Code (Python)

```python
class BIT:
    """Binary Indexed Tree for point updates and prefix sums."""
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    def update(self, i, delta):
        """Add delta to position i (1-indexed)."""
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)

    def prefix_sum(self, i):
        """Sum of elements from 1 to i."""
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & (-i)
        return total

    def range_sum(self, l, r):
        """Sum of elements from l to r (inclusive)."""
        return self.prefix_sum(r) - self.prefix_sum(l - 1)


def solve_offline_bit(n, arr, queries):
    """
    Offline processing with BIT.

    Time: O((n + q) * log(n))
    Space: O(n + q)
    """
    # Store queries with original index, sort by right endpoint
    indexed_queries = [(l, r, i) for i, (l, r) in enumerate(queries)]
    indexed_queries.sort(key=lambda x: x[1])  # Sort by r

    bit = BIT(n)
    last_pos = {}  # value -> last position where it's marked
    answers = [0] * len(queries)

    query_idx = 0
    for i in range(1, n + 1):
        val = arr[i - 1]  # Convert to 0-indexed array access

        # If this value was marked before, unmark it
        if val in last_pos:
            bit.update(last_pos[val], -1)

        # Mark current position
        bit.update(i, 1)
        last_pos[val] = i

        # Answer all queries with right endpoint == i
        while query_idx < len(indexed_queries) and indexed_queries[query_idx][1] == i:
            l, r, orig_idx = indexed_queries[query_idx]
            answers[orig_idx] = bit.range_sum(l, r)
            query_idx += 1

    return answers


def main():
    import sys
    input_data = sys.stdin.read().split()
    idx = 0

    n, q = int(input_data[idx]), int(input_data[idx + 1])
    idx += 2

    arr = [int(input_data[idx + i]) for i in range(n)]
    idx += n

    queries = []
    for _ in range(q):
        l, r = int(input_data[idx]), int(input_data[idx + 1])
        queries.append((l, r))
        idx += 2

    results = solve_offline_bit(n, arr, queries)
    print('\n'.join(map(str, results)))


if __name__ == "__main__":
    main()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;

class BIT {
    vector<int> tree;
    int n;
public:
    BIT(int n) : n(n), tree(n + 1, 0) {}

    void update(int i, int delta) {
        for (; i <= n; i += i & (-i))
            tree[i] += delta;
    }

    int prefix_sum(int i) {
        int sum = 0;
        for (; i > 0; i -= i & (-i))
            sum += tree[i];
        return sum;
    }

    int range_sum(int l, int r) {
        return prefix_sum(r) - prefix_sum(l - 1);
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;

    vector<int> arr(n + 1);
    for (int i = 1; i <= n; i++) {
        cin >> arr[i];
    }

    // queries: {r, l, original_index}
    vector<tuple<int, int, int>> queries(q);
    for (int i = 0; i < q; i++) {
        int l, r;
        cin >> l >> r;
        queries[i] = {r, l, i};
    }

    // Sort by right endpoint
    sort(queries.begin(), queries.end());

    BIT bit(n);
    unordered_map<int, int> last_pos;
    vector<int> answers(q);

    int qi = 0;
    for (int i = 1; i <= n; i++) {
        int val = arr[i];

        // Unmark previous occurrence if exists
        if (last_pos.count(val)) {
            bit.update(last_pos[val], -1);
        }

        // Mark current position
        bit.update(i, 1);
        last_pos[val] = i;

        // Answer queries with right endpoint == i
        while (qi < q && get<0>(queries[qi]) == i) {
            int r = get<0>(queries[qi]);
            int l = get<1>(queries[qi]);
            int idx = get<2>(queries[qi]);
            answers[idx] = bit.range_sum(l, r);
            qi++;
        }
    }

    for (int ans : answers) {
        cout << ans << '\n';
    }

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O((n + q) * log n) | n BIT updates, q BIT range queries |
| Space | O(n + q) | BIT array, hash map, query storage |

---

## Solution 3: Mo's Algorithm (Alternative)

### Key Insight

> **The Trick:** Process queries in a special order that minimizes pointer movement, allowing O(1) amortized add/remove operations.

Mo's algorithm divides the array into blocks of size sqrt(n) and sorts queries by (block of l, r). This ensures the total pointer movement is O((n + q) * sqrt(n)).

### Algorithm

1. Choose block size B = sqrt(n)
2. Sort queries by (l / B, r)
3. Maintain current range [cur_l, cur_r] and frequency map
4. For each query, expand/shrink the current range to match the query
5. Track distinct count as we add/remove elements

### Code (Python)

```python
from collections import defaultdict
import math

def solve_mo(n, arr, queries):
    """
    Mo's algorithm for offline range queries.

    Time: O((n + q) * sqrt(n))
    Space: O(n + q)
    """
    block_size = max(1, int(math.sqrt(n)))

    # Store queries with original index
    indexed_queries = [(l, r, i) for i, (l, r) in enumerate(queries)]

    # Sort by (block of l, r)
    indexed_queries.sort(key=lambda x: (x[0] // block_size, x[1]))

    freq = defaultdict(int)
    distinct_count = 0
    cur_l, cur_r = 1, 0  # Empty range initially
    answers = [0] * len(queries)

    def add(idx):
        nonlocal distinct_count
        val = arr[idx - 1]  # Convert to 0-indexed
        if freq[val] == 0:
            distinct_count += 1
        freq[val] += 1

    def remove(idx):
        nonlocal distinct_count
        val = arr[idx - 1]
        freq[val] -= 1
        if freq[val] == 0:
            distinct_count -= 1

    for l, r, orig_idx in indexed_queries:
        # Expand/shrink to reach [l, r]
        while cur_r < r:
            cur_r += 1
            add(cur_r)
        while cur_l > l:
            cur_l -= 1
            add(cur_l)
        while cur_r > r:
            remove(cur_r)
            cur_r -= 1
        while cur_l < l:
            remove(cur_l)
            cur_l += 1

        answers[orig_idx] = distinct_count

    return answers
```

### Complexity (Mo's Algorithm)

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O((n + q) * sqrt(n)) | Each pointer moves O(n * sqrt(n)) total |
| Space | O(n + q) | Frequency map, query storage |

---

## Common Mistakes

### Mistake 1: Processing Queries Online

```python
# WRONG - Cannot answer each query independently in O(log n)
for l, r in queries:
    # No efficient way to count distinct in [l, r] online
    answer = some_magic_query(l, r)  # Doesn't exist!
```

**Problem:** Distinct value counting is not decomposable; segment trees cannot merge distinct counts.
**Fix:** Use offline processing to handle queries in a specific order.

### Mistake 2: Forgetting to Unmark Previous Occurrence

```python
# WRONG
for i in range(1, n + 1):
    bit.update(i, 1)  # Just marks everything
    last_pos[arr[i]] = i
```

**Problem:** An element appearing at positions 2 and 5 would be counted twice.
**Fix:** Always unmark the previous occurrence before marking the new one.

### Mistake 3: Wrong Query Sorting

```python
# WRONG - Sorting by left endpoint
indexed_queries.sort(key=lambda x: x[0])  # Sorted by l
```

**Problem:** We need to process by right endpoint to maintain the BIT invariant correctly.
**Fix:** Sort queries by right endpoint r.

### Mistake 4: Off-by-One in BIT Indexing

```python
# WRONG - Using 0-indexed in BIT
bit.update(0, 1)  # BIT is 1-indexed!
```

**Problem:** BIT operations assume 1-indexed positions.
**Fix:** Use 1-indexed positions throughout, convert array access carefully.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single element | `n=1, arr=[5], query=(1,1)` | 1 | One element is always distinct |
| All same | `n=5, arr=[3,3,3,3,3], query=(1,5)` | 1 | All elements are the same value |
| All different | `n=5, arr=[1,2,3,4,5], query=(1,5)` | 5 | Each element is unique |
| Large values | `arr=[10^9, 10^9-1]` | Works | Hash map handles large keys |
| Single query full range | `query=(1,n)` | Count of unique in entire array | Maximum range |
| Many overlapping queries | All queries are (1, n) | Same answer for all | Offline still works |

---

## When to Use This Pattern

### Use Offline + BIT When:
- Queries are given upfront (not online/streaming)
- Need O(log n) per query after sorting
- Can afford O(n log n) preprocessing
- Space for storing all queries is acceptable

### Use Mo's Algorithm When:
- Add/remove operations are O(1)
- O(sqrt(n)) per query is acceptable
- Problem involves counting or frequency tracking
- Cannot use offline + BIT due to problem structure

### Don't Use When:
- Queries must be answered online (as they arrive)
- Updates to the array are interleaved with queries
- Need sub-linear query time without preprocessing

### Pattern Recognition Checklist:
- [ ] Static array with multiple range queries? -> **Consider offline processing**
- [ ] Counting/frequency in ranges? -> **Offline + BIT or Mo's algorithm**
- [ ] Non-decomposable range function? -> **Cannot use standard segment tree**
- [ ] Need to track "first/last occurrence" in range? -> **Offline + BIT**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Static Range Sum Queries (CSES)](https://cses.fi/problemset/task/1646) | Basic range queries with prefix sums |
| [Range Minimum Queries (CSES)](https://cses.fi/problemset/task/1647) | Sparse table for static RMQ |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Distinct Values (CSES)](https://cses.fi/problemset/task/2428) | Count subarrays with at most k distinct (sliding window) |
| [Range Update Queries (CSES)](https://cses.fi/problemset/task/1651) | BIT with lazy propagation |
| [K-query (SPOJ)](https://www.spoj.com/problems/KQUERY/) | Count elements greater than k in range |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [Distinct Values Queries with Updates](https://codeforces.com/problemset/problem/1042/D) | Handle array modifications |
| [Count on a Tree (SPOJ)](https://www.spoj.com/problems/COT/) | HLD + persistent segment tree |
| [Range Distinct Query (D-Query SPOJ)](https://www.spoj.com/problems/DQUERY/) | Classic offline + BIT |

---

## Key Takeaways

1. **The Core Idea:** Transform "count distinct" into "count rightmost occurrences" using offline processing
2. **Time Optimization:** O(q * n) -> O((n + q) * log n) by processing queries in sorted order
3. **Space Trade-off:** O(n + q) space for BIT and query storage
4. **Pattern:** Offline query processing - when online is impossible, sort queries cleverly

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Explain why segment trees cannot directly solve this problem
- [ ] Implement offline + BIT solution from scratch
- [ ] Trace through the "last occurrence" invariant manually
- [ ] Recognize when Mo's algorithm is a better choice
- [ ] Handle coordinate compression if values are very large

---

## Additional Resources

- [CP-Algorithms: Fenwick Tree](https://cp-algorithms.com/data_structures/fenwick.html)
- [CP-Algorithms: Mo's Algorithm](https://cp-algorithms.com/data_structures/sqrt_decomposition.html)
- [CSES Distinct Values Queries](https://cses.fi/problemset/task/1734) - Count distinct in range
