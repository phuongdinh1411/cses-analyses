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
3 5 7
3
1 2 4

Output:
YES
YES
```
First case: AND of {5, 7} = 5 (101 & 111 = 101 = 5), not power of 2. But {3, 7} = 3 & 7 = 3, not power of 2. However, checking bit 0: all numbers with bit 0 set are {3,5,7}, AND = 1 which is 2^0. So YES. Second case: Element 1, 2, or 4 alone is a power of 2. YES.

## Solution

### Approach
Key insight: For AND of a subset to be a power of 2, exactly one bit must remain set.

Strategy: For each bit position (0 to 30), AND together all numbers that have this bit set. If the result is exactly 2^bit, then we found a valid subset.

### Python Solution

```python
from functools import reduce
import operator

def is_power_of_two(x):
    return x > 0 and (x & (x - 1)) == 0

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))

        # Check if any single element is power of 2 using any()
        found = any(is_power_of_two(num) for num in arr)

        if not found:
            # For each bit position, check if AND of numbers with that bit is power of 2
            for bit in range(31):
                target = 1 << bit
                # Filter numbers with this bit set using list comprehension
                nums_with_bit = [num for num in arr if num & target]

                if nums_with_bit:
                    # Use reduce to AND all filtered numbers
                    and_result = reduce(operator.and_, nums_with_bit)
                    if is_power_of_two(and_result):
                        found = True
                        break

        print("YES" if found else "NO")

if __name__ == "__main__":
    solve()
```

### Alternative Solution

```python
from functools import reduce
import operator

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))

        def check_bit(bit):
            mask = 1 << bit
            nums_with_bit = [num for num in arr if num & mask]
            if not nums_with_bit:
                return False
            and_val = reduce(operator.and_, nums_with_bit)
            return and_val > 0 and (and_val & (and_val - 1)) == 0

        # Use any() with generator for cleaner check
        result = "YES" if any(check_bit(bit) for bit in range(31)) else "NO"
        print(result)

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

The optimal strategy: for each bit i, AND all elements that have bit i set. This gives the minimum possible AND value among subsets where bit i could survive.
