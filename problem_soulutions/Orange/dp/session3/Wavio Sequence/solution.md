# Wavio Sequence

## Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

A Wavio sequence has these properties:
- Length L = 2n + 1 (odd length)
- First n+1 integers are strictly increasing
- Last n+1 integers are strictly decreasing
- No adjacent integers are equal

Find the length of the longest Wavio subsequence.

Example: In "1 2 3 2 1 2 3 4 3 2 1 5 4 1 2 3 2 2 1", the longest Wavio is "1 2 3 4 5 4 3 2 1" with length 9.

## Input Format
- Multiple test cases until EOF
- Each test case:
  - First line: N (1 ≤ N ≤ 10000)
  - Following lines: N integers

## Output Format
For each test case, print the length of longest Wavio sequence.

## Example
```
Input:
10
1 2 3 4 5 4 3 2 1 10

Output:
9
```
The array [1,2,3,4,5,4,3,2,1,10] contains the Wavio subsequence [1,2,3,4,5,4,3,2,1] of length 9. This has 5 increasing elements to peak (5) and 5 decreasing from peak.

## Solution

### Approach
For each position i:
1. Compute LIS ending at i (increasing from left)
2. Compute LDS starting at i (decreasing to right)
3. Wavio with peak at i has length 2 * min(LIS[i], LDS[i]) - 1

Use binary search for O(n log n) LIS/LDS computation.

### Python Solution

```python
import bisect

def compute_lis_ending(arr):
  """For each i, compute length of LIS ending at i"""
  n = len(arr)
  lis = [0] * n
  tails = []

  for i in range(n):
    pos = bisect.bisect_left(tails, arr[i])
    lis[i] = pos + 1

    if pos == len(tails):
      tails.append(arr[i])
    else:
      tails[pos] = arr[i]

  return lis

def compute_lds_starting(arr):
  """For each i, compute length of LDS starting at i"""
  n = len(arr)
  lds = [0] * n
  tails = []

  # Process from right to left
  for i in range(n - 1, -1, -1):
    pos = bisect.bisect_left(tails, arr[i])
    lds[i] = pos + 1

    if pos == len(tails):
      tails.append(arr[i])
    else:
      tails[pos] = arr[i]

  return lds

def solve():
  import sys
  data = sys.stdin.read().split()
  idx = 0

  while idx < len(data):
    n = int(data[idx])
    idx += 1

    arr = []
    for _ in range(n):
      arr.append(int(data[idx]))
      idx += 1

    # Compute LIS ending at each position
    lis = compute_lis_ending(arr)

    # Compute LDS starting at each position
    lds = compute_lds_starting(arr)

    # Find max Wavio length
    max_wavio = 0
    for i in range(n):
      # Wavio with peak at i
      k = min(lis[i], lds[i])
      wavio_len = 2 * k - 1
      max_wavio = max(max_wavio, wavio_len)

    print(max_wavio)

if __name__ == "__main__":
  solve()
```

### Alternative Solution with Detailed Comments

```python
import bisect
import sys

def solve():
  input_data = sys.stdin.read().split()
  idx = 0

  while idx < len(input_data):
    n = int(input_data[idx])
    idx += 1

    arr = [int(input_data[idx + i]) for i in range(n)]
    idx += n

    # LIS[i] = length of longest strictly increasing subsequence ending at i
    LIS = [0] * n
    tails = []
    for i in range(n):
      pos = bisect.bisect_left(tails, arr[i])
      LIS[i] = pos + 1
      if pos == len(tails):
        tails.append(arr[i])
      else:
        tails[pos] = arr[i]

    # LDS[i] = length of longest strictly decreasing subsequence starting at i
    # Equivalent to LIS from right with negated values
    LDS = [0] * n
    tails = []
    for i in range(n - 1, -1, -1):
      pos = bisect.bisect_left(tails, arr[i])
      LDS[i] = pos + 1
      if pos == len(tails):
        tails.append(arr[i])
      else:
        tails[pos] = arr[i]

    # Maximum Wavio length
    result = max(2 * min(LIS[i], LDS[i]) - 1 for i in range(n))
    print(result)

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(n log n)
- **Space Complexity:** O(n)

### Key Insight
A Wavio sequence is a "mountain" shape: strictly increasing to a peak, then strictly decreasing. For each position as the peak, the Wavio length is 2 * min(LIS_ending_here, LDS_starting_here) - 1. The minimum ensures both sides can match in length. Pre-compute LIS and LDS arrays in O(n log n) using binary search.
