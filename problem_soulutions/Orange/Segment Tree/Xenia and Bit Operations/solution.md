# Xenia and Bit Operations

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

## Problem Statement

Xenia has a sequence of 2^n non-negative integers. She calculates value v by:
1. First iteration: OR of adjacent pairs → sequence of 2^(n-1) elements
2. Second iteration: XOR of adjacent pairs → sequence of 2^(n-2) elements
3. Continue alternating OR and XOR until one element remains

Given m queries, each setting a[p] = b, output v after each query.

## Input Format
- First line: n (1 ≤ n ≤ 17), m (1 ≤ m ≤ 10^5)
- Second line: 2^n integers (the initial sequence)
- Next m lines: p, b (set a[p] = b)

## Output Format
For each query, print the resulting value v.

## Example
```
Input:
2 4
1 6 3 5
1 4
3 4
1 2
2 1

Output:
1
3
3
3
```
n=2 means 2^2=4 elements: [1,6,3,5]. First OR pairs: [1|6, 3|5] = [7, 7]. Then XOR: 7^7 = 0. Wait, let me recalculate. After query p=1, b=4: array [4,6,3,5]. OR: [4|6, 3|5]=[6,7]. XOR: 6^7=1. Output 1.

## Solution

### Approach
This is a perfect segment tree problem where:
- Leaf nodes store array values
- Internal nodes store OR or XOR depending on their level
- Level 0 (leaves): values
- Level 1: OR of pairs
- Level 2: XOR of pairs
- And so on, alternating

Update: Change leaf, propagate up with alternating operations.

### Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
  n, m = map(int, input().split())
  size = 1 << n  # 2^n

  arr = list(map(int, input().split()))

  # Segment tree
  tree = [0] * (2 * size)

  def build():
    # Fill leaves
    for i in range(size):
      tree[size + i] = arr[i]

    # Build internal nodes
    # Level counting: leaves are at level 0
    # Parent at level 1, etc.
    # At level k from bottom, use OR if k is odd, XOR if k is even (for k >= 1)

    for i in range(size - 1, 0, -1):
      # Determine level: how many times we can divide i by 2 before it becomes 0
      # Actually, level is log2(size) - log2(i)
      # Simpler: level from leaves is (n - bit_length of i + 1)
      level = n - (i.bit_length() - 1)

      if level % 2 == 1:
        tree[i] = tree[2 * i] | tree[2 * i + 1]
      else:
        tree[i] = tree[2 * i] ^ tree[2 * i + 1]

  def update(pos, val):
    pos += size  # Go to leaf
    tree[pos] = val

    level = 1  # First level above leaves
    pos //= 2

    while pos >= 1:
      if level % 2 == 1:
        tree[pos] = tree[2 * pos] | tree[2 * pos + 1]
      else:
        tree[pos] = tree[2 * pos] ^ tree[2 * pos + 1]
      pos //= 2
      level += 1

  build()

  results = []
  for _ in range(m):
    p, b = map(int, input().split())
    update(p - 1, b)  # Convert to 0-indexed
    results.append(tree[1])

  print('\n'.join(map(str, results)))

if __name__ == "__main__":
  solve()
```

### Alternative Solution - Recursive

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(500000)

def solve():
  n, m = map(int, input().split())
  size = 1 << n

  arr = list(map(int, input().split()))

  tree = [0] * (4 * size)

  def build(node, start, end, use_or):
    if start == end:
      tree[node] = arr[start]
      return

    mid = (start + end) // 2
    build(2 * node, start, mid, not use_or)
    build(2 * node + 1, mid + 1, end, not use_or)

    if use_or:
      tree[node] = tree[2 * node] | tree[2 * node + 1]
    else:
      tree[node] = tree[2 * node] ^ tree[2 * node + 1]

  def update(node, start, end, idx, val, use_or):
    if start == end:
      tree[node] = val
      return

    mid = (start + end) // 2
    if idx <= mid:
      update(2 * node, start, mid, idx, val, not use_or)
    else:
      update(2 * node + 1, mid + 1, end, idx, val, not use_or)

    if use_or:
      tree[node] = tree[2 * node] | tree[2 * node + 1]
    else:
      tree[node] = tree[2 * node] ^ tree[2 * node + 1]

  # Start with OR at root level (level n uses OR if n is odd)
  # Actually, first operation (leaves combine) is OR, so root uses OR if n is odd
  root_use_or = (n % 2 == 1)

  build(1, 0, size - 1, root_use_or)

  results = []
  for _ in range(m):
    p, b = map(int, input().split())
    update(1, 0, size - 1, p - 1, b, root_use_or)
    results.append(tree[1])

  print('\n'.join(map(str, results)))

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(2^n + m * n) for build and queries
- **Space Complexity:** O(2^n)

### Key Insight
The problem describes a perfect binary tree where operations alternate by level. Leaves store values, and each parent combines children with OR or XOR alternating by level. Point updates propagate O(n) levels up. The key is determining which operation to use at each level - if distance from leaves is odd, use OR; if even, use XOR.
