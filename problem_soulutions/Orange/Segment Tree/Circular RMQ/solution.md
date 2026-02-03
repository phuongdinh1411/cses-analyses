# Circular RMQ

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

## Problem Statement

Given a circular array of n elements, support two operations:
1. **inc(lf, rg, v)**: Add v to all elements in range [lf, rg] (circular)
2. **rmq(lf, rg)**: Return minimum in range [lf, rg] (circular)

Circular means if lf > rg, the range wraps around: [lf, n-1] ∪ [0, rg].

## Input Format
- First line: n (1 ≤ n ≤ 200000)
- Second line: n integers (initial array)
- Third line: m (0 ≤ m ≤ 200000)
- Next m lines: operations (2 integers = rmq, 3 integers = inc)

## Output Format
For each rmq operation, print the result.

## Solution

### Approach
Use Segment Tree with lazy propagation for range updates and range minimum queries. Handle circular ranges by splitting into two regular ranges.

### Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    arr = list(map(int, input().split()))
    m = int(input())

    INF = float('inf')

    # Segment tree with lazy propagation
    tree = [0] * (4 * n)
    lazy = [0] * (4 * n)

    def build(node, start, end):
        if start == end:
            tree[node] = arr[start]
            return
        mid = (start + end) // 2
        build(2*node, start, mid)
        build(2*node+1, mid+1, end)
        tree[node] = min(tree[2*node], tree[2*node+1])

    def push_down(node):
        if lazy[node] != 0:
            lazy[2*node] += lazy[node]
            lazy[2*node+1] += lazy[node]
            tree[2*node] += lazy[node]
            tree[2*node+1] += lazy[node]
            lazy[node] = 0

    def update(node, start, end, l, r, val):
        if r < start or end < l:
            return
        if l <= start and end <= r:
            tree[node] += val
            lazy[node] += val
            return
        push_down(node)
        mid = (start + end) // 2
        update(2*node, start, mid, l, r, val)
        update(2*node+1, mid+1, end, l, r, val)
        tree[node] = min(tree[2*node], tree[2*node+1])

    def query(node, start, end, l, r):
        if r < start or end < l:
            return INF
        if l <= start and end <= r:
            return tree[node]
        push_down(node)
        mid = (start + end) // 2
        return min(query(2*node, start, mid, l, r),
                   query(2*node+1, mid+1, end, l, r))

    build(1, 0, n-1)

    results = []
    for _ in range(m):
        line = list(map(int, input().split()))

        if len(line) == 2:
            # RMQ query
            lf, rg = line
            if lf <= rg:
                results.append(query(1, 0, n-1, lf, rg))
            else:
                # Circular: [lf, n-1] and [0, rg]
                results.append(min(query(1, 0, n-1, lf, n-1),
                                   query(1, 0, n-1, 0, rg)))
        else:
            # Inc update
            lf, rg, v = line
            if lf <= rg:
                update(1, 0, n-1, lf, rg, v)
            else:
                update(1, 0, n-1, lf, n-1, v)
                update(1, 0, n-1, 0, rg, v)

    print('\n'.join(map(str, results)))

if __name__ == "__main__":
    solve()
```

### Complexity Analysis
- **Time Complexity:** O((N + M) log N)
- **Space Complexity:** O(N)

### Key Insight
Circular ranges [lf, rg] where lf > rg can be split into two linear ranges: [lf, n-1] and [0, rg]. Use lazy propagation for efficient range updates. The segment tree maintains minimum values with additive lazy tags.
