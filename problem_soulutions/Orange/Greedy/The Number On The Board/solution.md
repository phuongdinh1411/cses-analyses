# The Number on the Board

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

## Problem Statement

Some natural number was written on the board. Its sum of digits was not less than k. But you were distracted a bit, and someone changed this number to n, replacing some digits with others. It's known that the length of the number didn't change.

You have to find the minimum number of digits in which these two numbers can differ.

## Input Format
- The first line contains integer k (1 ≤ k ≤ 10^9).
- The second line contains integer n (1 ≤ n < 10^100000).
- There are no leading zeros in n. It's guaranteed that this situation is possible.

## Output Format
Print the minimum number of digits in which the initial number and n can differ.

## Sample Test

**Input:**
```
3
11
```
**Output:**
```
1
```

**Input:**
```
3
99
```
**Output:**
```
0
```

## Solution

### Approach
To minimize the number of changed digits while making the digit sum at least k:
1. Calculate current digit sum
2. If sum ≥ k, answer is 0
3. Otherwise, greedily change the smallest digits to 9 (maximizing gain per change)
4. Sort digits and change from smallest to largest until sum ≥ k

### Python Solution

```python
def solve():
  k = int(input())
  n = input().strip()

  # Get all digits
  digits = [int(c) for c in n]
  current_sum = sum(digits)

  # If already >= k, no changes needed
  if current_sum >= k:
    print(0)
    return

  # Sort digits to change smallest ones first (maximize gain)
  digits.sort()

  changes = 0
  i = 0

  while current_sum < k:
    # Change digit to 9
    gain = 9 - digits[i]
    if gain > 0:
      changes += 1
      current_sum += gain
    i += 1

  print(changes)

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(n log n) where n is the number of digits, due to sorting
- **Space Complexity:** O(n) for storing digits
