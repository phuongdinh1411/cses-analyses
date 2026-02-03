---
layout: simple
title: "Intervals - Dynamic Programming Problem"
permalink: /problem_soulutions/dynamic_programming_at/intervals_analysis
difficulty: Hard
tags: [dp, segment-tree, interval-scheduling, range-max-query]
---

# Intervals

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Source** | [AtCoder DP Contest - W (Intervals)](https://atcoder.jp/contests/dp/tasks/dp_w) |
| **Difficulty** | Hard |
| **Category** | Dynamic Programming |
| **Time Limit** | 2 seconds |
| **Key Technique** | DP with Segment Tree for Range Max Query |

### Learning Goals

After solving this problem, you will be able to:
- [ ] Combine DP with segment trees for efficient range queries
- [ ] Identify problems where interval right-endpoint ordering enables optimal substructure
- [ ] Apply lazy propagation concepts for interval DP problems
- [ ] Transform interval selection into point-based DP states

---

## Problem Statement

**Problem:** Given M intervals on positions 1 to N, each interval [l, r] has a score a. Select a set of positions S such that for each interval, if all positions in [l, r] are selected (included in S), you gain score a. Maximize the total score minus the cost of selected positions.

**Simplified View:** Actually, the problem asks: choose a subset of integers from [1, N]. For each interval [l, r] with score a, if you choose ALL positions in that interval, you get score a. However, each position you choose costs you nothing directly - the intervals give positive or negative scores.

**Cleaner Interpretation:** Select intervals such that no two overlap, maximizing total score.

**Input:**
- Line 1: N, M (range size and number of intervals)
- Next M lines: l_i, r_i, a_i (interval left, right, score)

**Output:**
- Maximum total score achievable

**Constraints:**
- 1 <= N <= 2 x 10^5
- 1 <= M <= 2 x 10^5
- 1 <= l_i <= r_i <= N
- |a_i| <= 10^9

### Example

```
Input:
5 3
1 3 10
2 4 20
3 5 30

Output:
30
```

**Explanation:**
- Interval [1,3] has score 10
- Interval [2,4] has score 20
- Interval [3,5] has score 30

We can only pick non-overlapping intervals. The best choice is [3,5] with score 30. Picking [1,3] + another interval would overlap.

---

## Intuition: How to Think About This Problem

### Pattern Recognition

> **Key Question:** How can we efficiently find the maximum score ending at any position when processing intervals by right endpoint?

This is a classic interval scheduling problem with weighted intervals. The challenge is efficiently querying the maximum score achievable before each interval starts.

### Breaking Down the Problem

1. **What are we looking for?** Maximum score from non-overlapping intervals
2. **What information do we have?** Intervals with positions and scores
3. **What's the relationship?** For interval [l,r], we need best score from intervals ending before l

### Why Segment Tree?

When we process interval [l, r], we need: `dp[r] = max(dp[0], dp[1], ..., dp[l-1]) + score`

This is a **range maximum query** - segment tree answers this in O(log N).

### Analogies

Think of this like scheduling meetings in a conference room:
- Each meeting has a time slot [l, r] and a profit
- Meetings cannot overlap
- You want maximum total profit
- To decide on a meeting ending at time r, you need the best achievable before time l

---

## Solution 1: Naive DP (TLE)

### Idea

Process intervals sorted by right endpoint. For each position, propagate the maximum score.

### Algorithm

1. Sort intervals by right endpoint
2. For each position i from 1 to N:
   - `dp[i] = dp[i-1]` (don't end any interval here)
   - For each interval ending at i: `dp[i] = max(dp[i], dp[l-1] + score)`
3. Return `dp[N]`

### Code

```python
def intervals_naive(n: int, intervals: list) -> int:
    """
    Naive DP solution - O(N + M) assuming intervals already grouped.

    Time: O(N + M)
    Space: O(N)

    Note: This works when N is small, but fails for the actual
    problem where we need range max queries efficiently.
    """
    intervals.sort(key=lambda x: x[1])  # Sort by right endpoint

    dp = [0] * (n + 1)
    idx = 0

    for i in range(1, n + 1):
        dp[i] = dp[i - 1]
        while idx < len(intervals) and intervals[idx][1] == i:
            l, r, score = intervals[idx]
            dp[i] = max(dp[i], dp[l - 1] + score)
            idx += 1

    return dp[n]
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O(N + M log M) | Sorting + linear scan |
| Space | O(N) | DP array |

### Why This Works (But Is Slow for Variants)

This O(N) approach works here, but in problems requiring point updates with range queries (like when coordinate compression is needed), we need a segment tree.

---

## Solution 2: DP with Segment Tree

### Key Insight

> **The Trick:** Use a segment tree to maintain `dp[i]` values and answer range max queries in O(log N).

### DP State Definition

| State | Meaning |
|-------|---------|
| `dp[i]` | Maximum score achievable using intervals that end at or before position i |

**In plain English:** `dp[i]` represents the best total score we can get if we only consider the number line from 1 to i.

### State Transition

```
For interval [l, r] with score a:
    dp[r] = max(dp[r], query_max(0, l-1) + a)
```

**Why?** To use interval [l, r], all previous intervals must end before l. We query the maximum score achievable in range [0, l-1].

### Base Cases

| Case | Value | Reason |
|------|-------|--------|
| `dp[0]` | 0 | No intervals considered, score is 0 |

### Algorithm

1. Sort intervals by right endpoint
2. Group intervals by their right endpoint
3. For each position r from 1 to N:
   - For each interval [l, r, a] ending at r:
     - `candidate = segment_tree.query_max(0, l-1) + a`
     - Update answer for position r
   - Update segment tree: `segment_tree.update(r, dp[r])`
4. Return `segment_tree.query_max(0, N)`

### Dry Run Example

Let's trace through with input `N=5, intervals=[(1,3,10), (2,4,20), (3,5,30)]`:

```
Initial state:
  Segment Tree: [0, 0, 0, 0, 0, 0] (indices 0-5)
  Sorted intervals by right endpoint: [(1,3,10), (2,4,20), (3,5,30)]

Step 1: Process position 1, 2 (no intervals end here)
  No updates needed
  Segment Tree: [0, 0, 0, 0, 0, 0]

Step 2: Process position 3, interval (1, 3, 10)
  query_max(0, 0) = 0  (positions before l=1)
  candidate = 0 + 10 = 10
  Update position 3: dp[3] = 10
  Segment Tree: [0, 0, 0, 10, 0, 0]

Step 3: Process position 4, interval (2, 4, 20)
  query_max(0, 1) = 0  (positions before l=2)
  candidate = 0 + 20 = 20
  Update position 4: dp[4] = max(dp[3], 20) = 20
  But also propagate: dp[4] >= dp[3]
  Segment Tree: [0, 0, 0, 10, 20, 0]

Step 4: Process position 5, interval (3, 5, 30)
  query_max(0, 2) = 0  (positions before l=3)
  candidate = 0 + 30 = 30
  Update position 5: dp[5] = max(dp[4], 30) = 30
  Segment Tree: [0, 0, 0, 10, 20, 30]

Final Answer: query_max(0, 5) = 30
```

### Visual Diagram

```
Position:  0   1   2   3   4   5
           |   |   |   |   |   |
           0   0   0   10  20  30
                       ^   ^   ^
                       |   |   |
Intervals:        [1---3]  |   |
                      [2---4]  |
                          [3---5]

Best: Pick interval [3,5] = 30
(Cannot combine [1,3]+[3,5] as they share position 3)
```

### Code (Python)

```python
class SegmentTree:
    """Segment Tree for Range Maximum Query with Point Update."""

    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (4 * n)

    def update(self, node: int, start: int, end: int, idx: int, val: int):
        if start == end:
            self.tree[node] = max(self.tree[node], val)
            return
        mid = (start + end) // 2
        if idx <= mid:
            self.update(2 * node, start, mid, idx, val)
        else:
            self.update(2 * node + 1, mid + 1, end, idx, val)
        self.tree[node] = max(self.tree[2 * node], self.tree[2 * node + 1])

    def query(self, node: int, start: int, end: int, l: int, r: int) -> int:
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        left_max = self.query(2 * node, start, mid, l, r)
        right_max = self.query(2 * node + 1, mid + 1, end, l, r)
        return max(left_max, right_max)


def solve_intervals(n: int, m: int, intervals: list) -> int:
    """
    Optimal solution using Segment Tree for range max queries.

    Time: O(M log N) for M intervals with range [1, N]
    Space: O(N) for segment tree

    Args:
        n: Range size [1, N]
        m: Number of intervals
        intervals: List of (l, r, score) tuples

    Returns:
        Maximum achievable score
    """
    from collections import defaultdict

    # Group intervals by right endpoint
    by_right = defaultdict(list)
    for l, r, a in intervals:
        by_right[r].append((l, a))

    seg_tree = SegmentTree(n + 1)

    for r in range(1, n + 1):
        # Process all intervals ending at position r
        for l, score in by_right[r]:
            # Query max score achievable before position l
            best_before = seg_tree.query(1, 0, n, 0, l - 1)
            candidate = best_before + score
            seg_tree.update(1, 0, n, r, candidate)

        # Propagate: dp[r] >= dp[r-1]
        prev_max = seg_tree.query(1, 0, n, 0, r - 1)
        seg_tree.update(1, 0, n, r, prev_max)

    return seg_tree.query(1, 0, n, 0, n)


def main():
    import sys
    input_data = sys.stdin.read().split()
    idx = 0
    n = int(input_data[idx]); idx += 1
    m = int(input_data[idx]); idx += 1

    intervals = []
    for _ in range(m):
        l = int(input_data[idx]); idx += 1
        r = int(input_data[idx]); idx += 1
        a = int(input_data[idx]); idx += 1
        intervals.append((l, r, a))

    print(solve_intervals(n, m, intervals))


if __name__ == "__main__":
    main()
```

### Code (C++)

```cpp
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

class SegmentTree {
private:
    int n;
    vector<ll> tree;

    void update(int node, int start, int end, int idx, ll val) {
        if (start == end) {
            tree[node] = max(tree[node], val);
            return;
        }
        int mid = (start + end) / 2;
        if (idx <= mid)
            update(2 * node, start, mid, idx, val);
        else
            update(2 * node + 1, mid + 1, end, idx, val);
        tree[node] = max(tree[2 * node], tree[2 * node + 1]);
    }

    ll query(int node, int start, int end, int l, int r) {
        if (r < start || end < l) return 0;
        if (l <= start && end <= r) return tree[node];
        int mid = (start + end) / 2;
        return max(query(2 * node, start, mid, l, r),
                   query(2 * node + 1, mid + 1, end, l, r));
    }

public:
    SegmentTree(int n) : n(n), tree(4 * n, 0) {}

    void update(int idx, ll val) {
        update(1, 0, n - 1, idx, val);
    }

    ll query(int l, int r) {
        return query(1, 0, n - 1, l, r);
    }
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;

    // Group intervals by right endpoint
    vector<vector<pair<int, ll>>> by_right(n + 1);

    for (int i = 0; i < m; i++) {
        int l, r;
        ll a;
        cin >> l >> r >> a;
        by_right[r].push_back({l, a});
    }

    SegmentTree seg(n + 2);

    for (int r = 1; r <= n; r++) {
        // Process intervals ending at r
        for (auto& [l, score] : by_right[r]) {
            ll best_before = seg.query(0, l - 1);
            ll candidate = best_before + score;
            seg.update(r, candidate);
        }

        // Propagate: dp[r] >= dp[r-1]
        ll prev_max = seg.query(0, r - 1);
        seg.update(r, prev_max);
    }

    cout << seg.query(0, n) << "\n";

    return 0;
}
```

### Complexity

| Metric | Value | Explanation |
|--------|-------|-------------|
| Time | O((N + M) log N) | Each position: O(log N) query and update |
| Space | O(N + M) | Segment tree O(N) + interval storage O(M) |

---

## Common Mistakes

### Mistake 1: Forgetting to Propagate

```python
# WRONG - Missing propagation
for r in range(1, n + 1):
    for l, score in by_right[r]:
        best = seg.query(0, l - 1)
        seg.update(r, best + score)
    # Missing: seg.update(r, seg.query(0, r-1))
```

**Problem:** Without propagation, dp[r] might be less than dp[r-1], breaking optimality.
**Fix:** Always propagate the maximum from previous positions.

### Mistake 2: Wrong Query Range

```python
# WRONG - Including position l in query
best_before = seg.query(0, l)  # Should be l-1

# CORRECT
best_before = seg.query(0, l - 1)
```

**Problem:** If we include position l, we might count overlapping intervals.
**Fix:** Query range [0, l-1] to ensure no overlap with interval [l, r].

### Mistake 3: Integer Overflow

```cpp
// WRONG - Using int for scores
int best = seg.query(0, l - 1);
int candidate = best + score;  // Overflow!

// CORRECT - Use long long
ll best = seg.query(0, l - 1);
ll candidate = best + score;
```

**Problem:** Scores can be up to 10^9, sum of M scores can exceed int range.
**Fix:** Use `long long` in C++ or Python's native big integers.

---

## Edge Cases

| Case | Input | Expected Output | Why |
|------|-------|-----------------|-----|
| Single interval | N=5, M=1, [(1,5,100)] | 100 | Take the only interval |
| All overlapping | N=3, M=3, [(1,3,1),(1,3,2),(1,3,3)] | 3 | Take max score interval |
| No intervals | N=5, M=0 | 0 | No score possible |
| Adjacent intervals | N=4, [(1,2,10),(3,4,20)] | 30 | Can take both |
| Negative scores | N=3, [(1,3,-5)] | 0 | Better to take nothing |

---

## When to Use This Pattern

### Use This Approach When:
- Selecting non-overlapping intervals with weights
- DP state depends on range maximum/minimum queries
- Need O(log N) per transition instead of O(N)
- Coordinate compression is applied and N becomes manageable

### Don't Use When:
- Intervals are unweighted (greedy suffices)
- N is very small (naive DP is simpler)
- Problem requires finding all optimal solutions

### Pattern Recognition Checklist:
- [ ] Weighted interval scheduling? -> **Segment tree DP**
- [ ] Need max/min over a range of DP values? -> **Segment tree**
- [ ] Intervals sorted by endpoint? -> **Consider this pattern**
- [ ] O(N^2) DP but need faster? -> **Segment tree optimization**

---

## Related Problems

### Easier (Do These First)

| Problem | Why It Helps |
|---------|--------------|
| [Activity Selection (Greedy)](https://www.geeksforgeeks.org/activity-selection-problem-greedy-algo-1/) | Unweighted version, greedy approach |
| [Range Max Query](https://cses.fi/problemset/task/1647) | Practice segment tree basics |

### Similar Difficulty

| Problem | Key Difference |
|---------|----------------|
| [Weighted Job Scheduling](https://leetcode.com/problems/maximum-profit-in-job-scheduling/) | Same concept, LeetCode version |
| [AtCoder DP - V (Subtree)](https://atcoder.jp/contests/dp/tasks/dp_v) | Tree DP with rerooting |

### Harder (Do These After)

| Problem | New Concept |
|---------|-------------|
| [CSES - Nested Ranges Count](https://cses.fi/problemset/task/2169) | Counting with BIT/Segment Tree |
| [AtCoder DP - X (Tower)](https://atcoder.jp/contests/dp/tasks/dp_x) | Interval DP with sorting trick |

---

## Key Takeaways

1. **Core Idea:** Transform interval selection into point-based DP with range queries
2. **Time Optimization:** Segment tree reduces O(N) range queries to O(log N)
3. **Space Trade-off:** O(N) segment tree enables efficient range operations
4. **Pattern:** Weighted interval scheduling with segment tree optimization

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement a segment tree for range max queries
- [ ] Explain why we process intervals by right endpoint
- [ ] Handle the propagation step correctly
- [ ] Identify similar problems requiring segment tree DP

---

## Additional Resources

- [AtCoder DP Contest Editorial](https://atcoder.jp/contests/dp/editorial)
- [CP-Algorithms: Segment Tree](https://cp-algorithms.com/data_structures/segment_tree.html)
- [TopCoder: Segment Trees Tutorial](https://www.topcoder.com/thrive/articles/Range%20Minimum%20Query%20and%20Lowest%20Common%20Ancestor)
