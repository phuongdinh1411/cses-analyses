# Prince And Princess

## Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

On an n×n chessboard, Prince makes p jumps visiting p+1 distinct squares (x1, x2, ..., x_{p+1}). Princess makes q jumps visiting q+1 distinct squares (y1, y2, ..., y_{q+1}).

Find the longest common subsequence of their paths - the maximum number of squares they both visit in the same order.

## Input Format
- First line: T (number of test cases)
- Each test case:
  - First line: n, p, q
  - Second line: p+1 integers (Prince's path)
  - Third line: q+1 integers (Princess's path)

## Output Format
For each test case: "Case X: L" where L is the LCS length.

## Example
```
Input:
1
3 6 7
1 7 5 4 8 3 9
1 4 3 5 6 2 8 9

Output:
Case 1: 4
```
Prince's positions are 1→0, 7→1, 5→2, 4→3, 8→4, 3→5, 9→6. Princess's path becomes [0, 3, 5, 2, 4, 6] (squares 6 and 2 are dropped). Its LIS, for example [0, 2, 4, 6] (squares 1, 5, 8, 9), has length 4.

## Solution

### Approach
A direct LCS is O(p·q), which is too slow for p, q up to 62500.

Each path visits distinct squares, so map each square in Prince's path to its index. Then rewrite Princess's path as those indices, dropping squares Prince never visits. A common subsequence is now exactly an increasing subsequence of the rewritten list, so the answer is its LIS, found with patience sorting (`bisect_left`).

Note that the input starts with the number of test cases.

### Python Solution

```python
import bisect
import sys


def solve():
  data = sys.stdin.read().split()
  idx = 0
  t = int(data[idx]); idx += 1

  for case in range(1, t + 1):
    n, p, q = map(int, data[idx:idx + 3]); idx += 3
    prince = data[idx:idx + p + 1]; idx += p + 1
    princess = data[idx:idx + q + 1]; idx += q + 1

    # Squares are distinct within a path, so LCS reduces to LIS of positions.
    pos = {val: i for i, val in enumerate(prince)}
    tails = []
    for val in princess:
      if val in pos:
        x = pos[val]
        k = bisect.bisect_left(tails, x)
        if k == len(tails):
          tails.append(x)
        else:
          tails[k] = x

    print(f"Case {case}: {len(tails)}")


if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O((p + q) log(p))
- **Space Complexity:** O(p + q)

### Key Insight
LCS of two sequences with distinct elements can be reduced to LIS. Map first sequence elements to their indices. Transform second sequence using this mapping (keeping only common elements). LCS length equals LIS length of transformed sequence. This reduces O(pq) to O((p+q) log p).
