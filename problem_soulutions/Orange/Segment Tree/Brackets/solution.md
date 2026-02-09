# Brackets

## Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 11000ms
- **Memory Limit:** 512MB

## Problem Statement

Given a bracket word (string of '(' and ')'), perform operations:
1. **Replacement**: Change the i-th bracket to its opposite
2. **Check**: Determine if current word is a correct bracket expression

A correct bracket expression has matching pairs where every '(' has a corresponding ')' later.

## Input Format
- 10 test cases (must process all)
- Each test case:
  - Line 1: n (length of bracket word)
  - Line 2: n brackets (space-separated)
  - Line 3: m (number of operations)
  - Next m lines: operation (k=0 for check, k>0 for replace position k)

## Output Format
For each test case: "Test i:" followed by YES/NO for each check operation.

## Example
```
Input:
4
( ) ( )
4
0
1
0
2

Output:
Test 1:
YES
NO
YES
```
String "()()" is valid (check 0: YES). Flip position 1 (')' to '('): "((()" is invalid (NO). Flip position 2 ('(' to ')'): "()()" is valid again (YES).

## Solution

### Approach
Use Segment Tree to track:
- Unmatched '(' count (open)
- Unmatched ')' count (close)

For a valid expression: both counts should be 0.

When merging two segments: ')' from right can match '(' from left.

### Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
  for test in range(1, 11):
    n = int(input())
    brackets = input().split()
    s = ''.join(brackets)

    # Segment tree: each node stores (unmatched_open, unmatched_close)
    tree = [(0, 0)] * (4 * n)

    def merge(left, right):
      # Unmatched ')' from right can match '(' from left
      matched = min(left[0], right[1])
      return (left[0] - matched + right[0], left[1] + right[1] - matched)

    def build(node, start, end):
      if start == end:
        if s[start] == '(':
          tree[node] = (1, 0)
        else:
          tree[node] = (0, 1)
        return

      mid = (start + end) // 2
      build(2*node, start, mid)
      build(2*node+1, mid+1, end)
      tree[node] = merge(tree[2*node], tree[2*node+1])

    def update(node, start, end, idx):
      if start == end:
        # Flip bracket
        if tree[node] == (1, 0):
          tree[node] = (0, 1)
        else:
          tree[node] = (1, 0)
        return

      mid = (start + end) // 2
      if idx <= mid:
        update(2*node, start, mid, idx)
      else:
        update(2*node+1, mid+1, end, idx)
      tree[node] = merge(tree[2*node], tree[2*node+1])

    if n > 0:
      build(1, 0, n-1)

    m = int(input())
    print(f"Test {test}:")

    for _ in range(m):
      k = int(input())
      if k == 0:
        # Check if valid
        if n > 0 and tree[1] == (0, 0):
          print("YES")
        else:
          print("NO")
      else:
        # Replace bracket at position k (1-indexed)
        update(1, 0, n-1, k-1)

if __name__ == "__main__":
  solve()
```

### Alternative Solution

```python
def solve():
  for test in range(1, 11):
    n = int(input())
    s = list(input().split())

    # Convert to +1/-1
    arr = [1 if c == '(' else -1 for c in s]

    # Segment tree storing (sum, min_prefix)
    size = 1
    while size < n:
      size *= 2

    tree_sum = [0] * (2 * size)
    tree_min = [0] * (2 * size)

    def build():
      for i in range(n):
        tree_sum[size + i] = arr[i]
        tree_min[size + i] = arr[i]

      for i in range(size - 1, 0, -1):
        tree_sum[i] = tree_sum[2*i] + tree_sum[2*i+1]
        tree_min[i] = min(tree_min[2*i], tree_sum[2*i] + tree_min[2*i+1])

    def update(idx):
      arr[idx] *= -1
      i = size + idx
      tree_sum[i] = arr[idx]
      tree_min[i] = arr[idx]

      i //= 2
      while i >= 1:
        tree_sum[i] = tree_sum[2*i] + tree_sum[2*i+1]
        tree_min[i] = min(tree_min[2*i], tree_sum[2*i] + tree_min[2*i+1])
        i //= 2

    if n > 0:
      build()

    m = int(input())
    print(f"Test {test}:")

    for _ in range(m):
      k = int(input())
      if k == 0:
        # Valid if sum=0 and min_prefix >= 0
        if n > 0 and tree_sum[1] == 0 and tree_min[1] >= 0:
          print("YES")
        else:
          print("NO")
      else:
        update(k - 1)

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(M log N) per test case
- **Space Complexity:** O(N)

### Key Insight
A bracket sequence is valid iff: (1) total sum is 0 (equal '(' and ')'), and (2) no prefix has more ')' than '('. Track these with segment tree for efficient updates.
