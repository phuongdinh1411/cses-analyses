# Aish And XOR

## Problem Information
- **Source:** Hackerearth
- **Difficulty:** Secret
- **Time Limit:** 1500ms
- **Memory Limit:** 512MB

## Problem Statement

Given an array (containing only 0 and 1) of N length. For each query with L and R, find:
1. The XOR of all elements from L to R (both inclusive)
2. The number of unset bits (0's) in the given range

## Input Format
- First line: N (number of elements)
- Second line: N numbers containing 0 and 1 only
- Third line: Q (number of queries)
- Next Q lines: L and R for each query

## Constraints
- 1 ≤ N ≤ 100000 (1-based indexing)
- 1 ≤ Q ≤ N
- 1 ≤ L ≤ R ≤ 100000

## Output Format
For each query, print the XOR value and number of unset bits in that range.

## Example
```
Input:
5
1 0 1 0 1
2
1 3
2 5

Output:
0 1
1 2
```
For query [1,3]: XOR of {1,0,1} = 0, zeros count = 1. For query [2,5]: XOR of {0,1,0,1} = 0 XOR 1 XOR 0 XOR 1 = 0... wait, let me recalculate: 0^1=1, 1^0=1, 1^1=0. So XOR=0 and zeros=2.

## Solution

### Approach
Use prefix arrays for both XOR and zero count:
1. **Prefix XOR:** `xor_prefix[i]` = XOR of elements from index 0 to i
   - XOR(L, R) = xor_prefix[R] ^ xor_prefix[L-1]
2. **Prefix Zero Count:** `zero_prefix[i]` = count of zeros from index 0 to i
   - Zeros(L, R) = zero_prefix[R] - zero_prefix[L-1]

### Python Solution

```python
from itertools import accumulate
import operator

def solve():
    n = int(input())
    arr = list(map(int, input().split()))

    # Build prefix arrays using accumulate for more Pythonic approach
    xor_prefix = [0] + list(accumulate(arr, operator.xor))
    zero_prefix = [0] + list(accumulate(1 - x for x in arr))

    q = int(input())
    for _ in range(q):
        l, r = map(int, input().split())

        # XOR of range [l, r] and count of zeros using tuple unpacking
        xor_result = xor_prefix[r] ^ xor_prefix[l - 1]
        zeros = zero_prefix[r] - zero_prefix[l - 1]

        print(xor_result, zeros)

if __name__ == "__main__":
    solve()
```

### Alternative Solution (0-indexed)

```python
def solve():
    n = int(input())
    arr = list(map(int, input().split()))

    # Build prefix arrays using list comprehension style
    xor_pref, zero_pref = [0], [0]

    for x in arr:
        xor_pref.append(xor_pref[-1] ^ x)
        zero_pref.append(zero_pref[-1] + (1 - x))

    q = int(input())

    # Use list comprehension to collect results
    results = []
    for _ in range(q):
        l, r = map(int, input().split())
        xor_val, zeros = xor_pref[r] ^ xor_pref[l - 1], zero_pref[r] - zero_pref[l - 1]
        results.append(f"{xor_val} {zeros}")

    print('\n'.join(results))

if __name__ == "__main__":
    solve()
```

### One-liner Style

```python
def solve():
  n = int(input())
  arr = list(map(int, input().split()))

  # Cumulative XOR and zero count
  from itertools import accumulate
  import operator

  xor_pref = [0] + list(accumulate(arr, operator.xor))
  zero_pref = [0] + list(accumulate(1 - x for x in arr))

  q = int(input())
  for _ in range(q):
    l, r = map(int, input().split())
    print(xor_pref[r] ^ xor_pref[l-1], zero_pref[r] - zero_pref[l-1])

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(N) for preprocessing + O(1) per query = O(N + Q)
- **Space Complexity:** O(N) for prefix arrays

### Key Insight
XOR has the property that `A ^ A = 0` and `A ^ 0 = A`. So:
- `XOR(L, R) = XOR(0, R) ^ XOR(0, L-1)`

This is because elements from 0 to L-1 appear in both prefixes and cancel out.

For zero counting, simple prefix sums work since we're just counting occurrences.
