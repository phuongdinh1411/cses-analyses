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
()((
4
4
0
2
0

Output:
Test 1:
YES
NO
```
Flip position 4: "()((" becomes "()()", which is correct, so YES. Flip position 2: "()()" becomes "((()", which is not, so NO. (The real input repeats this format 10 times.)

## Solution

### Approach
Store `(unmatched '(', unmatched ')')` in each segment-tree node. When merging, the right child's unmatched ')' close the left child's unmatched '(':
`matched = min(L.open, R.close)`, so the result is `(L.open - matched + R.open, L.close + R.close - matched)`.

The word is correct iff the root is `(0, 0)`. A flip swaps the two counts at a leaf and recomputes O(log n) ancestors.

The real input has exactly 10 tests. Reading until EOF handles that and shorter test files, and gluing tokens until n characters are read accepts brackets with or without spaces.

### Python Solution

```python
import sys


def merge(left, right):
  # A ')' on the right closes a '(' left open on the left.
  matched = min(left[0], right[1])
  return (left[0] - matched + right[0], left[1] + right[1] - matched)


def solve():
  data = sys.stdin.read().split()
  idx = 0
  test = 0
  while idx < len(data):
    test += 1
    n = int(data[idx]); idx += 1
    s = ""
    while len(s) < n:  # brackets may or may not be space-separated
      s += data[idx]; idx += 1

    size = 1
    while size < n:
      size *= 2
    tree = [(0, 0)] * (2 * size)  # (unmatched '(', unmatched ')')
    for i, ch in enumerate(s):
      tree[size + i] = (1, 0) if ch == '(' else (0, 1)
    for i in range(size - 1, 0, -1):
      tree[i] = merge(tree[2 * i], tree[2 * i + 1])

    m = int(data[idx]); idx += 1
    out = [f"Test {test}:"]
    for k in map(int, data[idx:idx + m]):
      if k == 0:
        out.append("YES" if tree[1] == (0, 0) else "NO")
      else:
        i = size + k - 1
        tree[i] = (tree[i][1], tree[i][0])  # flip the bracket
        i //= 2
        while i:
          tree[i] = merge(tree[2 * i], tree[2 * i + 1])
          i //= 2
    idx += m
    print("\n".join(out))


if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(M log N) per test case
- **Space Complexity:** O(N)

### Key Insight
A bracket sequence is valid iff: (1) total sum is 0 (equal '(' and ')'), and (2) no prefix has more ')' than '('. Track these with segment tree for efficient updates.
