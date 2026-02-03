# Curious Robin Hood

## Problem Information
- **Source:** LightOJ
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

## Problem Statement

Robin Hood has n sacks numbered from 0 to n-1, each containing some money. He can perform three operations:
1. **Type 1 (i)**: Give all money from sack i to the poor (set to 0, return old value)
2. **Type 2 (i, v)**: Add money v to sack i
3. **Type 3 (i, j)**: Find total money from sack i to sack j

## Input Format
- T test cases
- Each test case:
  - First line: n (sacks) and q (queries)
  - Second line: n integers (initial money in each sack)
  - Next q lines: operation type followed by parameters

## Output Format
For each test case, print "Case X:" followed by results for type 1 and type 3 queries.

## Solution

### Approach
Use a Segment Tree for:
- Point update (set value, add value)
- Range sum query

For type 1: Query point value, then set to 0
For type 2: Add value to point
For type 3: Range sum query

### Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for case in range(1, t + 1):
        n, q = map(int, input().split())
        arr = list(map(int, input().split()))

        # Segment tree for range sum
        tree = [0] * (4 * n)

        def build(node, start, end):
            if start == end:
                tree[node] = arr[start]
                return
            mid = (start + end) // 2
            build(2 * node, start, mid)
            build(2 * node + 1, mid + 1, end)
            tree[node] = tree[2 * node] + tree[2 * node + 1]

        def update(node, start, end, idx, val):
            if start == end:
                tree[node] = val
                return
            mid = (start + end) // 2
            if idx <= mid:
                update(2 * node, start, mid, idx, val)
            else:
                update(2 * node + 1, mid + 1, end, idx, val)
            tree[node] = tree[2 * node] + tree[2 * node + 1]

        def query_point(node, start, end, idx):
            if start == end:
                return tree[node]
            mid = (start + end) // 2
            if idx <= mid:
                return query_point(2 * node, start, mid, idx)
            else:
                return query_point(2 * node + 1, mid + 1, end, idx)

        def query_range(node, start, end, l, r):
            if r < start or end < l:
                return 0
            if l <= start and end <= r:
                return tree[node]
            mid = (start + end) // 2
            return query_range(2 * node, start, mid, l, r) + \
                   query_range(2 * node + 1, mid + 1, end, l, r)

        build(1, 0, n - 1)

        print(f"Case {case}:")

        for _ in range(q):
            query = list(map(int, input().split()))
            op = query[0]

            if op == 1:
                # Give all money from sack i to poor
                i = query[1]
                old_val = query_point(1, 0, n - 1, i)
                update(1, 0, n - 1, i, 0)
                print(old_val)

            elif op == 2:
                # Add money v to sack i
                i, v = query[1], query[2]
                old_val = query_point(1, 0, n - 1, i)
                update(1, 0, n - 1, i, old_val + v)

            else:  # op == 3
                # Sum from sack i to sack j
                i, j = query[1], query[2]
                print(query_range(1, 0, n - 1, i, j))

if __name__ == "__main__":
    solve()
```

### Alternative Solution - Fenwick Tree (BIT)

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for case in range(1, t + 1):
        n, q = map(int, input().split())
        arr = list(map(int, input().split()))

        # Fenwick tree (1-indexed)
        bit = [0] * (n + 1)

        def update_bit(i, delta):
            i += 1  # Convert to 1-indexed
            while i <= n:
                bit[i] += delta
                i += i & (-i)

        def prefix_sum(i):
            i += 1  # Convert to 1-indexed
            total = 0
            while i > 0:
                total += bit[i]
                i -= i & (-i)
            return total

        def range_sum(l, r):
            if l == 0:
                return prefix_sum(r)
            return prefix_sum(r) - prefix_sum(l - 1)

        # Build BIT
        for i in range(n):
            update_bit(i, arr[i])

        print(f"Case {case}:")

        for _ in range(q):
            query = list(map(int, input().split()))
            op = query[0]

            if op == 1:
                i = query[1]
                old_val = arr[i]
                update_bit(i, -old_val)
                arr[i] = 0
                print(old_val)

            elif op == 2:
                i, v = query[1], query[2]
                update_bit(i, v)
                arr[i] += v

            else:
                i, j = query[1], query[2]
                print(range_sum(i, j))

if __name__ == "__main__":
    solve()
```

### Complexity Analysis
- **Time Complexity:** O((N + Q) log N)
- **Space Complexity:** O(N)

### Key Insight
This is a classic segment tree application with point updates and range sum queries. For type 1 queries, we need to both retrieve and reset the value, which requires a point query followed by a point update. Fenwick Tree (BIT) is also applicable since we only need range sums (not other associative operations).
