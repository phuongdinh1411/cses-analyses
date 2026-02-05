# Sansa and XOR

## Problem Information
- **Source:** Hackerrank
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

Sansa has an array. She wants to find the value obtained by XOR-ing the contiguous subarrays, followed by XOR-ing the values thus obtained. Can you help her in this task?

For example, if arr = [3, 4, 5]:

| Subarray | Operation | Result |
|----------|-----------|--------|
| 3 | None | 3 |
| 4 | None | 4 |
| 5 | None | 5 |
| 3, 4 | 3 XOR 4 | 7 |
| 4, 5 | 4 XOR 5 | 1 |
| 3, 4, 5 | 3 XOR 4 XOR 5 | 2 |

Now we take the resultant values and XOR them together: 3 ⊕ 4 ⊕ 5 ⊕ 7 ⊕ 1 ⊕ 2 = 6

## Input Format
- The first line contains an integer T, the number of the test cases.
- Each of the next T pairs of lines:
  - The first line contains an integer n, the number of elements in arr.
  - The second line contains n space-separated integers arr_i.

## Constraints
- 1 ≤ T ≤ 5
- 2 ≤ n ≤ 10^5
- 1 ≤ arr_i ≤ 10^8

## Output Format
Print the result of each test case on a separate line.

## Solution

### Approach
The key insight is that XOR has a special property: a ⊕ a = 0.

For each element at index i (0-indexed), count how many subarrays include it:
- The element can be the start of a subarray at positions 0 to i (that's i+1 choices)
- The element can be the end of a subarray at positions i to n-1 (that's n-i choices)
- Total subarrays containing element i = (i+1) × (n-i)

If this count is odd, the element contributes to the final XOR. If even, it cancels out.

### Python Solution

```python
def solve():
 t = int(input())

 for _ in range(t):
  n = int(input())
  arr = list(map(int, input().split()))

  result = 0

  for i in range(n):
   # Number of subarrays containing arr[i]
   # (i+1) choices for left endpoint, (n-i) choices for right endpoint
   count = (i + 1) * (n - i)

   # Only XOR if count is odd
   if count % 2 == 1:
    result ^= arr[i]

  print(result)

if __name__ == "__main__":
 solve()
```

### Optimized Observation

For arrays with even length, every element appears an even number of times, so result is always 0.

For arrays with odd length, elements at even indices (0, 2, 4, ...) appear an odd number of times.

```python
def solve_optimized():
 t = int(input())

 for _ in range(t):
  n = int(input())
  arr = list(map(int, input().split()))

  # If n is even, result is always 0
  if n % 2 == 0:
   print(0)
   continue

  # If n is odd, XOR elements at even indices
  result = 0
  for i in range(0, n, 2):
   result ^= arr[i]

  print(result)

if __name__ == "__main__":
 solve_optimized()
```

### Complexity Analysis
- **Time Complexity:** O(n) per test case
- **Space Complexity:** O(n) for storing the array

### Key Insight
The number of subarrays containing element at index i is (i+1) × (n-i). This value is odd only when both (i+1) and (n-i) are odd, which happens when n is odd and i is even.
