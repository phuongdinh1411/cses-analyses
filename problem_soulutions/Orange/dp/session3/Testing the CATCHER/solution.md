# Testing the CATCHER

## Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

## Problem Statement

A CATCHER missile defense system can intercept missiles if:
1. The missile is the first one, OR
2. The missile height is ≤ the height of the last intercepted missile

Given a sequence of incoming missile heights, find the maximum number of missiles the CATCHER can intercept.

## Input Format
- Multiple test cases
- Each test case: sequence of missile heights ending with -1
- Input ends with -1 as first value

## Output Format
For each test: "Test #X:" followed by "maximum possible number of missiles: Y"

## Solution

### Approach
This is the Longest Non-Increasing Subsequence problem, which is equivalent to:
- Longest Decreasing Subsequence (LDS) if heights are strictly decreasing
- Or Longest Non-Increasing Subsequence if equal heights allowed

Since each missile must have height ≤ previous intercepted missile, we need the longest non-increasing subsequence.

This equals the Longest Increasing Subsequence of the reversed sequence.

### Python Solution

```python
import bisect

def longest_non_increasing(arr):
  """Find length of longest non-increasing subsequence"""
  if not arr:
    return 0

  # Reverse and find LIS with non-strict inequality
  # Or: find longest non-decreasing in reversed array
  # Equivalent to finding LIS on negated values

  # For non-increasing: each next element <= previous
  # Use LIS on negated values with bisect_right for non-strict

  tails = []
  for x in arr:
    neg_x = -x
    # bisect_right for non-strict (allowing equal)
    idx = bisect.bisect_right(tails, neg_x)
    if idx == len(tails):
      tails.append(neg_x)
    else:
      tails[idx] = neg_x

  return len(tails)

def solve():
  import sys
  data = sys.stdin.read().split()
  idx = 0
  case = 0

  while idx < len(data):
    missiles = []
    while idx < len(data):
      h = int(data[idx])
      idx += 1
      if h == -1:
        break
      missiles.append(h)

    if not missiles:
      break

    case += 1
    result = longest_non_increasing(missiles)

    if case > 1:
      print()
    print(f"Test #{case}:")
    print(f"  maximum possible number of missiles intercepted: {result}")

if __name__ == "__main__":
  solve()
```

### Alternative Solution - Direct DP

```python
def solve():
  import sys
  data = list(map(int, sys.stdin.read().split()))
  idx = 0
  case = 0

  while idx < len(data):
    missiles = []
    while idx < len(data):
      h = data[idx]
      idx += 1
      if h == -1:
        break
      missiles.append(h)

    if not missiles:
      break

    case += 1
    n = len(missiles)

    # dp[i] = length of longest non-increasing subsequence ending at i
    dp = [1] * n

    for i in range(1, n):
      for j in range(i):
        if missiles[j] >= missiles[i]:
          dp[i] = max(dp[i], dp[j] + 1)

    result = max(dp)

    if case > 1:
      print()
    print(f"Test #{case}:")
    print(f"  maximum possible number of missiles intercepted: {result}")

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(n log n) with binary search, O(n²) with basic DP
- **Space Complexity:** O(n)

### Key Insight
The problem asks for the longest subsequence where each element is ≤ the previous one (non-increasing). This is the reverse of LIS. Use LIS algorithm on negated values, using bisect_right instead of bisect_left to handle equal elements (non-strict inequality).
