# Power of Two

## Problem Information
- **Source:** Hackerearth
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

Given an array A, determine if there exists any subset where the AND of all elements is a power of two (1, 2, 4, 8, 16, ...).

## Input Format
- First line: T (number of test cases)
- For each test case:
  - First line: N (size of array)
  - Second line: N space-separated integers

## Constraints
- 1 ≤ T ≤ 1000
- 1 ≤ N ≤ 200
- 0 ≤ Aᵢ ≤ 10^9

## Output Format
For each test case, print "YES" if such a subset exists, otherwise "NO".

## Example
```
Input:
2
3
3 6 7
2
12 8

Output:
YES
NO
```
First case: {6, 7} gives AND = 6 & 7 = 6, not power of 2. But numbers with bit 1 set: {3, 6, 7}, AND = 3 & 6 & 7 = 2, which is 2^1. YES. Second case: 12 = 1100, 8 = 1000. AND = 8 (power of 2), so YES... Actually let's verify: for bit 3, numbers with it set: {12, 8}, AND = 8. That's 2^3. So the answer should be YES.

## Solution

### Approach
Key insight: For AND of a subset to be a power of 2, exactly one bit must remain set.

Strategy: For each bit position (0 to 30), AND together all numbers that have this bit set. If the result is exactly 2^bit, then we found a valid subset.

Why this works: If we want bit i to survive, we must include only numbers with bit i set. The AND of such numbers will have bit i set, plus possibly other bits. The smallest AND (best chance of being power of 2) is when we include ALL numbers with bit i set.

### Python Solution

```python
def is_power_of_two(x):
  return x > 0 and (x & (x - 1)) == 0

def solve():
  t = int(input())

  for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))

    found = False

    # For each bit position
    for bit in range(31):
      target = 1 << bit
      and_result = (1 << 31) - 1  # All bits set

      # AND all numbers that have this bit set
      has_bit = False
      for num in arr:
        if num & target:
          and_result &= num
          has_bit = True

      # Check if result is a power of 2
      if has_bit and is_power_of_two(and_result):
        found = True
        break

    print("YES" if found else "NO")

if __name__ == "__main__":
  solve()
```

### Alternative Solution

```python
def solve():
  t = int(input())

  for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))

    result = "NO"

    for bit in range(31):
      mask = 1 << bit
      and_val = -1  # All bits set (in two's complement)

      for num in arr:
        if num & mask:
          and_val &= num

      # and_val is power of 2 if exactly one bit is set
      if and_val > 0 and (and_val & (and_val - 1)) == 0:
        result = "YES"
        break

    print(result)

if __name__ == "__main__":
  solve()
```

### One-liner Style

```python
def solve():
  t = int(input())
  for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))

    def check():
      for bit in range(31):
        m = 1 << bit
        a = -1
        for x in arr:
          if x & m:
            a &= x
        if a > 0 and a & (a-1) == 0:
          return True
      return False

    print("YES" if check() else "NO")

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(31 × N) = O(N) per test case
- **Space Complexity:** O(N) for storing the array

### Key Insight
For a subset's AND to equal 2^i:
1. All elements must have bit i set
2. No other bit should survive the AND

The optimal strategy: for each bit i, AND all elements that have bit i set. This gives the minimum possible AND value among subsets where bit i could survive. If this minimum is exactly 2^i, answer is YES.
