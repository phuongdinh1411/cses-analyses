# Interval Product

## Problem Information
- **Source:** UVALive
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

## Problem Statement

Given a sequence of N integers X1, X2, ..., XN, perform K operations:
1. **Change I V**: Set Xi to V
2. **Product I J**: Output the sign of the product Xi * Xi+1 * ... * XJ

The sign is:
- `+` if product is positive
- `-` if product is negative
- `0` if product is zero

## Input Format
- Multiple test cases
- Each test case:
  - First line: N and K
  - Second line: N integers (-100 to 100)
  - Next K lines: operations (C for change, P for product)

## Output Format
For each test case, output a string of signs for all product queries.

## Solution

### Approach
We don't need the actual product, just its sign. Track:
- Count of zeros in range
- Count of negative numbers in range

If zeros > 0: sign is '0'
Else if negatives is odd: sign is '-'
Else: sign is '+'

Use Segment Tree for efficient range queries and point updates.

### Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
  while True:
    line = input().split()
    if not line:
      break

    n, k = int(line[0]), int(line[1])
    arr = list(map(int, input().split()))

    # Segment tree: store (zero_count, negative_count)
    tree = [(0, 0)] * (4 * n)

    def get_sign(val):
      if val == 0:
        return (1, 0)  # 1 zero, 0 negatives
      elif val < 0:
        return (0, 1)  # 0 zeros, 1 negative
      else:
        return (0, 0)  # 0 zeros, 0 negatives

    def merge(left, right):
      return (left[0] + right[0], left[1] + right[1])

    def build(node, start, end):
      if start == end:
        tree[node] = get_sign(arr[start])
        return
      mid = (start + end) // 2
      build(2 * node, start, mid)
      build(2 * node + 1, mid + 1, end)
      tree[node] = merge(tree[2 * node], tree[2 * node + 1])

    def update(node, start, end, idx, val):
      if start == end:
        tree[node] = get_sign(val)
        return
      mid = (start + end) // 2
      if idx <= mid:
        update(2 * node, start, mid, idx, val)
      else:
        update(2 * node + 1, mid + 1, end, idx, val)
      tree[node] = merge(tree[2 * node], tree[2 * node + 1])

    def query(node, start, end, l, r):
      if r < start or end < l:
        return (0, 0)  # identity
      if l <= start and end <= r:
        return tree[node]
      mid = (start + end) // 2
      return merge(query(2 * node, start, mid, l, r),
            query(2 * node + 1, mid + 1, end, l, r))

    build(1, 0, n - 1)

    result = []
    for _ in range(k):
      parts = input().split()
      op = parts[0]

      if op == 'C':
        i, v = int(parts[1]) - 1, int(parts[2])  # 1-indexed to 0-indexed
        update(1, 0, n - 1, i, v)
      else:  # op == 'P'
        i, j = int(parts[1]) - 1, int(parts[2]) - 1
        zeros, negatives = query(1, 0, n - 1, i, j)

        if zeros > 0:
          result.append('0')
        elif negatives % 2 == 1:
          result.append('-')
        else:
          result.append('+')

    print(''.join(result))

if __name__ == "__main__":
  solve()
```

### Alternative Solution - Direct Sign Tracking

```python
import sys
input = sys.stdin.readline

def solve():
  while True:
    line = input().split()
    if not line:
      break

    n, k = int(line[0]), int(line[1])
    arr = list(map(int, input().split()))

    # Segment tree: store sign (-1, 0, or 1)
    tree = [1] * (4 * n)

    def sign(val):
      if val == 0:
        return 0
      return 1 if val > 0 else -1

    def build(node, start, end):
      if start == end:
        tree[node] = sign(arr[start])
        return
      mid = (start + end) // 2
      build(2 * node, start, mid)
      build(2 * node + 1, mid + 1, end)
      tree[node] = tree[2 * node] * tree[2 * node + 1]

    def update(node, start, end, idx, val):
      if start == end:
        tree[node] = sign(val)
        return
      mid = (start + end) // 2
      if idx <= mid:
        update(2 * node, start, mid, idx, val)
      else:
        update(2 * node + 1, mid + 1, end, idx, val)
      tree[node] = tree[2 * node] * tree[2 * node + 1]

    def query(node, start, end, l, r):
      if r < start or end < l:
        return 1  # identity for multiplication
      if l <= start and end <= r:
        return tree[node]
      mid = (start + end) // 2
      return query(2 * node, start, mid, l, r) * \
        query(2 * node + 1, mid + 1, end, l, r)

    build(1, 0, n - 1)

    result = []
    for _ in range(k):
      parts = input().split()
      op = parts[0]

      if op == 'C':
        i, v = int(parts[1]) - 1, int(parts[2])
        update(1, 0, n - 1, i, v)
      else:
        i, j = int(parts[1]) - 1, int(parts[2]) - 1
        s = query(1, 0, n - 1, i, j)

        if s == 0:
          result.append('0')
        elif s < 0:
          result.append('-')
        else:
          result.append('+')

    print(''.join(result))

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O((N + K) log N)
- **Space Complexity:** O(N)

### Key Insight
Instead of tracking actual products (which would overflow), track only the sign. The sign of a product depends on: (1) whether any element is zero, and (2) the parity of negative numbers. The alternative solution is more elegant: store signs (-1, 0, 1) and multiply them directly, since sign(a*b) = sign(a) * sign(b).
