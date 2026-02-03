---
layout: simple
title: "Li Chao Tree - Range Queries Data Structure"
permalink: /problem_soulutions/range_queries/li_chao_tree_analysis
difficulty: Hard
tags: [segment-tree, convex-hull-trick, dp-optimization, geometry, range-queries]
---

# Li Chao Tree

## Problem Overview

| Attribute | Value |
|-----------|-------|
| **Difficulty** | Hard |
| **Category** | Range Queries / DP Optimization |
| **Key Technique** | Segment Tree with Line Storage |
| **Time per Query** | O(log N) |

### Learning Goals

After studying this topic, you will be able to:
- [ ] Understand how Li Chao Tree maintains a set of lines efficiently
- [ ] Implement insertion and query operations in O(log N)
- [ ] Apply Li Chao Tree for DP optimization problems
- [ ] Choose between Li Chao Tree and Convex Hull Trick appropriately

---

## Concept Explanation

**Problem:** Given a set of lines of the form `y = mx + b`, efficiently:
1. **Insert** a new line into the set
2. **Query** the minimum (or maximum) y-value at a given x-coordinate

**Key Insight:** Li Chao Tree is a segment tree where each node stores the "winner" line for its interval's midpoint. When inserting a new line, we compare it with the existing line at the midpoint and recursively push the "loser" to the appropriate child.

### Why Li Chao Tree?

- **Arbitrary Query Order:** Unlike standard CHT, queries can come in any order
- **Simple Implementation:** Easier to code than dynamic CHT with binary search
- **Persistent Friendly:** Can be made persistent for advanced applications

---

## Intuition: Li Chao Tree vs Convex Hull Trick

### Pattern Recognition

> **Key Question:** When do we use Li Chao Tree instead of Convex Hull Trick?

The Convex Hull Trick (CHT) requires either:
1. Lines inserted in order of increasing/decreasing slope, OR
2. Queries in sorted order of x-coordinate

Li Chao Tree removes these restrictions at the cost of slightly higher constant factor.

### Comparison Table

| Aspect | Convex Hull Trick | Li Chao Tree |
|--------|------------------|--------------|
| Insert Order | Must be sorted by slope | Any order |
| Query Order | Must be sorted (for deque) | Any order |
| Time Complexity | O(n) total / O(log n) per query | O(log N) per operation |
| Space | O(n) | O(N) where N = x-range |
| Implementation | Tricky edge cases | Cleaner recursion |
| Use Case | Sorted slopes/queries | Arbitrary order |

### Breaking Down the Problem

1. **What are we storing?** Lines in the form y = mx + b
2. **What's the query?** Find min/max y at a specific x
3. **Why segment tree?** Each node represents an x-interval; we store the "best" line for that interval's midpoint

---

## Algorithm: How Li Chao Tree Works

### Core Idea

Each segment tree node covering interval [lo, hi]:
- Stores the line that is **best at the midpoint** mid = (lo + hi) / 2
- When inserting a new line, compare at midpoint:
  - Winner stays at current node
  - Loser is pushed to the child where it might still win

### Insert Operation

```
insert(node, [lo, hi], new_line):
    mid = (lo + hi) / 2

    if new_line is better at mid than current line:
        swap(new_line, current_line)

    if lo == hi:
        return

    if new_line is better at lo:
        insert(left_child, [lo, mid], new_line)
    else:
        insert(right_child, [mid+1, hi], new_line)
```

### Query Operation

```
query(node, [lo, hi], x):
    if node is null:
        return infinity (or -infinity for max)

    mid = (lo + hi) / 2
    current_value = evaluate(node.line, x)

    if x <= mid:
        return min(current_value, query(left_child, [lo, mid], x))
    else:
        return min(current_value, query(right_child, [mid+1, hi], x))
```

---

## Dry Run: Inserting Lines

Let's trace inserting lines into a Li Chao Tree for **minimum queries** with x-range [0, 8].

### Lines to Insert
1. Line A: y = 2x + 1
2. Line B: y = -x + 10
3. Line C: y = 0.5x + 4

### Step-by-Step Execution

```
Initial State: Empty tree, range [0, 8]

=== Insert Line A: y = 2x + 1 ===
Node [0,8], mid=4:
  - No existing line, store A
  Tree: [0,8] -> A

=== Insert Line B: y = -x + 10 ===
Node [0,8], mid=4:
  - A at mid=4: 2(4)+1 = 9
  - B at mid=4: -4+10 = 6
  - B wins at mid, swap: node stores B, push A down
  - A at lo=0: 2(0)+1 = 1
  - B at lo=0: -0+10 = 10
  - A better at lo, go LEFT

Node [0,4], mid=2:
  - No existing line, store A
  Tree:
        [0,8] -> B
        /
    [0,4] -> A

=== Insert Line C: y = 0.5x + 4 ===
Node [0,8], mid=4:
  - B at mid=4: 6
  - C at mid=4: 0.5(4)+4 = 6
  - Tie! Keep B (arbitrary), push C
  - C at lo=0: 0.5(0)+4 = 4
  - B at lo=0: 10
  - C better at lo, go LEFT

Node [0,4], mid=2:
  - A at mid=2: 2(2)+1 = 5
  - C at mid=2: 0.5(2)+4 = 5
  - Tie! Keep A, push C
  - C at lo=0: 4
  - A at lo=0: 1
  - A better at lo, go RIGHT

Node [3,4], mid=3:
  - No existing line, store C

Final Tree:
            [0,8] -> B (y=-x+10)
            /
        [0,4] -> A (y=2x+1)
            \
          [3,4] -> C (y=0.5x+4)
```

### Query Example: Find min at x=1

```
Query x=1:
  Node [0,8]: B gives -1+10=9, go left (1 <= 4)
  Node [0,4]: A gives 2(1)+1=3, go left (1 <= 2)
  Node [0,2]: null, return inf

  Result: min(9, 3, inf) = 3 (from line A)
```

---

## Solution: Python Implementation

```python
class LiChaoTree:
    """
    Li Chao Tree for minimum line queries.

    Time: O(log N) per insert/query
    Space: O(N) where N = hi - lo + 1
    """

    def __init__(self, lo: int, hi: int):
        self.lo = lo
        self.hi = hi
        self.tree = {}  # node_id -> (m, b) representing y = mx + b
        self.INF = float('inf')

    def _eval(self, line, x):
        """Evaluate line y = mx + b at point x."""
        if line is None:
            return self.INF
        m, b = line
        return m * x + b

    def insert(self, m: int, b: int):
        """Insert line y = mx + b."""
        self._insert(1, self.lo, self.hi, (m, b))

    def _insert(self, node: int, lo: int, hi: int, new_line):
        if lo > hi:
            return

        mid = (lo + hi) // 2
        cur_line = self.tree.get(node)

        # Determine winner at midpoint
        new_better_at_mid = self._eval(new_line, mid) < self._eval(cur_line, mid)

        if new_better_at_mid:
            self.tree[node] = new_line
            new_line, cur_line = cur_line, new_line

        if lo == hi or new_line is None:
            return

        # Determine which side the loser might still win
        new_better_at_lo = self._eval(new_line, lo) < self._eval(cur_line, lo)

        if new_better_at_lo:
            self._insert(2 * node, lo, mid, new_line)
        else:
            self._insert(2 * node + 1, mid + 1, hi, new_line)

    def query(self, x: int) -> int:
        """Query minimum y-value at x."""
        return self._query(1, self.lo, self.hi, x)

    def _query(self, node: int, lo: int, hi: int, x: int):
        if lo > hi or node not in self.tree:
            return self.INF

        mid = (lo + hi) // 2
        cur_val = self._eval(self.tree.get(node), x)

        if lo == hi:
            return cur_val

        if x <= mid:
            return min(cur_val, self._query(2 * node, lo, mid, x))
        else:
            return min(cur_val, self._query(2 * node + 1, mid + 1, hi, x))


# Example usage
if __name__ == "__main__":
    tree = LiChaoTree(0, 1000000)

    # Insert lines: y = mx + b
    tree.insert(2, 1)      # y = 2x + 1
    tree.insert(-1, 10)    # y = -x + 10
    tree.insert(0, 5)      # y = 5 (horizontal)

    # Query minimum at various x
    print(tree.query(0))   # min at x=0
    print(tree.query(5))   # min at x=5
    print(tree.query(10))  # min at x=10
```

---

## Solution: C++ Implementation

```cpp
#include <bits/stdc++.h>
using namespace std;

class LiChaoTree {
private:
    struct Line {
        long long m, b;  // y = mx + b
        long long eval(long long x) const { return m * x + b; }
    };

    static const long long INF = 1e18;
    int lo, hi;
    vector<Line> tree;
    vector<bool> has_line;

    void insert(int node, int l, int r, Line new_line) {
        if (l > r) return;

        int mid = l + (r - l) / 2;

        if (!has_line[node]) {
            tree[node] = new_line;
            has_line[node] = true;
            return;
        }

        bool new_better_mid = new_line.eval(mid) < tree[node].eval(mid);
        bool new_better_lo = new_line.eval(l) < tree[node].eval(l);

        if (new_better_mid) swap(tree[node], new_line);

        if (l == r) return;

        // After swap, new_line is the loser at mid
        // Push loser to the side where it might win
        if (new_better_lo != new_better_mid) {
            insert(2 * node, l, mid, new_line);
        } else {
            insert(2 * node + 1, mid + 1, r, new_line);
        }
    }

    long long query(int node, int l, int r, long long x) {
        if (l > r || !has_line[node]) return INF;

        int mid = l + (r - l) / 2;
        long long cur = tree[node].eval(x);

        if (l == r) return cur;

        if (x <= mid) {
            return min(cur, query(2 * node, l, mid, x));
        } else {
            return min(cur, query(2 * node + 1, mid + 1, r, x));
        }
    }

public:
    LiChaoTree(int lo, int hi) : lo(lo), hi(hi) {
        int size = 4 * (hi - lo + 2);
        tree.resize(size);
        has_line.resize(size, false);
    }

    void insert(long long m, long long b) {
        insert(1, lo, hi, {m, b});
    }

    long long query(long long x) {
        return query(1, lo, hi, x);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    LiChaoTree tree(0, 1000000);

    tree.insert(2, 1);     // y = 2x + 1
    tree.insert(-1, 10);   // y = -x + 10
    tree.insert(0, 5);     // y = 5

    cout << tree.query(0) << "\n";   // Query at x=0
    cout << tree.query(5) << "\n";   // Query at x=5
    cout << tree.query(10) << "\n";  // Query at x=10

    return 0;
}
```

---

## Common Mistakes

### Mistake 1: Using Wrong Infinity Value

```cpp
// WRONG: Integer overflow when evaluating
const int INF = 1e9;
long long eval = m * x + b;  // Can overflow if m, x are large

// CORRECT: Use appropriate infinity
const long long INF = 1e18;
```

**Problem:** When m and x are both up to 10^6, their product exceeds int range.
**Fix:** Use `long long` for all line evaluations and a sufficiently large INF.

### Mistake 2: Wrong Recursion Direction

```cpp
// WRONG: Always going left when loser is better at lo
if (new_better_at_lo) {
    insert(left, new_line);  // Wrong logic
}

// CORRECT: Consider relationship between mid and lo comparisons
if (new_better_at_lo != new_better_at_mid) {
    insert(left, new_line);
} else {
    insert(right, new_line);
}
```

**Problem:** The loser should go to the child where it has a chance to win.
**Fix:** Use XOR logic: if results differ at lo and mid, go left; else go right.

### Mistake 3: Not Handling Empty Nodes

```python
# WRONG: Accessing node without checking
cur_val = self.tree[node].eval(x)  # KeyError if node doesn't exist

# CORRECT: Check for existence
cur_line = self.tree.get(node)
if cur_line is None:
    return self.INF
```

---

## Edge Cases

| Case | Input | Handling | Why |
|------|-------|----------|-----|
| Empty tree query | Query before any insert | Return INF | No lines to evaluate |
| Single line | One insert, many queries | Works normally | Base case |
| Parallel lines | Same slope, different intercepts | Keep better one | Loser never wins anywhere |
| Identical lines | Same m and b | Either can stay | No difference in output |
| Negative x queries | x < 0 | Ensure range covers negatives | Adjust lo parameter |
| Large coordinates | x up to 10^9 | Use coordinate compression or implicit tree | Avoid MLE |
| Tie at midpoint | Equal values at mid | Arbitrary winner choice | Consistency matters, not which |

---

## When to Use Li Chao Tree

### Use Li Chao Tree When:
- Lines are inserted in arbitrary order (no slope sorting)
- Queries come in arbitrary order (no x sorting)
- You need online queries (no offline processing possible)
- DP optimization where slopes are not monotonic

### Use Standard CHT Instead When:
- Lines come in sorted slope order AND queries are sorted
- Memory is very tight (CHT uses O(n), Li Chao uses O(range))
- You need the absolute fastest constant factor

### Pattern Recognition Checklist:
- [ ] DP recurrence of form: `dp[i] = min(dp[j] + cost(j, i))` where `cost(j,i) = a[j] * b[i] + c[j]` -> **CHT/Li Chao**
- [ ] Need min/max over lines at arbitrary x? -> **Li Chao Tree**
- [ ] Slopes not sorted, queries not sorted? -> **Li Chao Tree (not basic CHT)**
- [ ] Need to delete lines? -> **Consider other structures**

---

## Comparison: Li Chao vs CHT Implementations

| Feature | Basic CHT (Deque) | Dynamic CHT | Li Chao Tree |
|---------|-------------------|-------------|--------------|
| Insert Time | O(1) amortized | O(log n) | O(log N) |
| Query Time | O(log n) or O(1)* | O(log n) | O(log N) |
| Slope Order | Required | Not required | Not required |
| Query Order | Required for O(1)* | Not required | Not required |
| Space | O(n) | O(n) | O(N) |
| Code Simplicity | Medium | Complex | Simple |
| Persistence | Hard | Hard | Easy |

*O(1) queries possible with pointer technique when x values are monotonic.

---

## Related Problems

### Prerequisites (Do These First)
| Problem | Why It Helps |
|---------|--------------|
| [Dynamic Range Sum (CSES)](https://cses.fi/problemset/task/1648) | Segment tree basics |
| [Salary Queries (CSES)](https://cses.fi/problemset/task/1144) | Dynamic queries on ranges |

### Direct Applications
| Problem | Key Insight |
|---------|-------------|
| [Codeforces - Kalila and Dimna](https://codeforces.com/contest/319/problem/C) | Classic DP + CHT |
| [AtCoder - Walk (DP Contest)](https://atcoder.jp/contests/dp/tasks/dp_r) | Linear function optimization |

### Harder (Do These After)
| Problem | New Concept |
|---------|-------------|
| [Codeforces - The Bakery](https://codeforces.com/contest/834/problem/D) | Divide and conquer DP optimization |
| [Codeforces - Ann and Books](https://codeforces.com/contest/877/problem/F) | Li Chao with complex state |

---

## Key Takeaways

1. **Core Idea:** Store "winner" line at midpoint, push "loser" to potential winning region
2. **Main Advantage:** Handles arbitrary insert and query order
3. **Trade-off:** O(N) space for x-range vs O(n) space for CHT
4. **Use Case:** DP optimization when slopes/queries are unsorted

---

## Practice Checklist

Before moving on, make sure you can:
- [ ] Implement Li Chao Tree from scratch
- [ ] Explain why the loser goes to a specific child
- [ ] Convert a DP problem to Li Chao Tree form
- [ ] Choose between CHT and Li Chao Tree for a given problem
- [ ] Handle both min and max query variants

---

## Additional Resources

- [CP-Algorithms: Li Chao Tree](https://cp-algorithms.com/geometry/convex_hull_trick.html)
- [Codeforces Blog: Li Chao Tree Tutorial](https://codeforces.com/blog/entry/86731)
- [KACTL Implementation](https://github.com/kth-competitive-programming/kactl)
