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
- Multiple test cases
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
4 4 3
1 7 5 4 8
1 7 5 8

Output:
Case 1: 3
```
Prince visits squares [1, 7, 5, 4, 8], Princess visits [1, 7, 5, 8]. The LCS is [1, 7, 5] or [1, 7, 8] with length 3.

## Solution

### Approach
Direct LCS would be O(p×q) which is too slow for p, q up to 62500.

Key insight: All numbers in each sequence are distinct and ≤ n².
Transform to LIS: Map Prince's sequence to positions 1, 2, ..., p+1. Then for each element in Princess's sequence, replace with its position in Prince's sequence (or skip if not present). The LCS equals LIS of the transformed sequence.

### Python Solution

```python
import bisect

def solve():
  import sys
  input = sys.stdin.readline

  case = 0
  while True:
    line = input().split()
    if not line:
      break

    n, p, q = int(line[0]), int(line[1]), int(line[2])
    case += 1

    prince = list(map(int, input().split()))
    princess = list(map(int, input().split()))

    # Map prince's sequence to positions
    pos = {}
    for i, val in enumerate(prince):
      pos[val] = i

    # Transform princess's sequence
    transformed = []
    for val in princess:
      if val in pos:
        transformed.append(pos[val])

    # LIS on transformed sequence
    if not transformed:
      print(f"Case {case}: 0")
      continue

    tails = []
    for x in transformed:
      idx = bisect.bisect_left(tails, x)
      if idx == len(tails):
        tails.append(x)
      else:
        tails[idx] = x

    print(f"Case {case}: {len(tails)}")

if __name__ == "__main__":
  solve()
```

### Alternative Solution

```python
import bisect
import sys

def solve():
  input = sys.stdin.readline
  case = 0

  while True:
    try:
      line = input()
      if not line.strip():
        break
      n, p, q = map(int, line.split())
    except:
      break

    case += 1

    prince = list(map(int, input().split()))
    princess = list(map(int, input().split()))

    # Create position map for prince
    prince_pos = {v: i for i, v in enumerate(prince)}

    # Convert princess to positions in prince's sequence
    seq = [prince_pos[v] for v in princess if v in prince_pos]

    # LIS
    dp = []
    for x in seq:
      pos = bisect.bisect_left(dp, x)
      if pos == len(dp):
        dp.append(x)
      else:
        dp[pos] = x

    print(f"Case {case}: {len(dp)}")

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O((p + q) log(p))
- **Space Complexity:** O(p + q)

### Key Insight
LCS of two sequences with distinct elements can be reduced to LIS. Map first sequence elements to their indices. Transform second sequence using this mapping (keeping only common elements). LCS length equals LIS length of transformed sequence. This reduces O(pq) to O((p+q) log p).
