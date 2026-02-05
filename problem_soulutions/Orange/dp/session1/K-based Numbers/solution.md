# K-based Numbers

## Problem Information
- **Source:** Timus Online Judge
- **Difficulty:** Secret
- **Time Limit:** 500ms
- **Memory Limit:** 256MB

## Problem Statement

Let's consider K-based numbers, containing exactly N digits. We define a number to be valid if its K-based notation doesn't contain two successive zeros. For example:

- 1010230 is a valid 7-digit number
- 1000198 is not a valid number (contains "00")
- 0001235 is not a 7-digit number, it is a 4-digit number

Given two numbers N and K, you are to calculate an amount of valid K-based numbers, containing N digits. You may assume that 2 ≤ K ≤ 10; N ≥ 2; N + K ≤ 18.

## Input Format
The numbers N and K in decimal notation separated by the line break.

## Output Format
The result in decimal notation.

## Solution

### Approach
Use dynamic programming where:
- `dp[i][0]` = count of valid i-digit numbers ending with 0
- `dp[i][1]` = count of valid i-digit numbers ending with non-zero

Transitions:
- A number ending with 0 can only be extended from a number ending with non-zero (to avoid "00")
- A number ending with non-zero can be extended from any valid number

### Python Solution

```python
def solve():
 n = int(input())
 k = int(input())

 # dp[i][0] = valid i-digit numbers ending with 0
 # dp[i][1] = valid i-digit numbers ending with non-zero

 # First digit cannot be 0 (would make it not N digits)
 # dp[1][0] = 0 (first digit can't be 0)
 # dp[1][1] = k-1 (digits 1 to k-1)

 dp = [[0, 0] for _ in range(n + 1)]
 dp[1][0] = 0  # First digit cannot be 0
 dp[1][1] = k - 1  # First digit can be 1 to k-1

 for i in range(2, n + 1):
  # Ending with 0: previous must end with non-zero
  dp[i][0] = dp[i-1][1]

  # Ending with non-zero: previous can be anything
  # (k-1) choices for the current non-zero digit
  dp[i][1] = (dp[i-1][0] + dp[i-1][1]) * (k - 1)

 # Total valid N-digit numbers
 print(dp[n][0] + dp[n][1])

if __name__ == "__main__":
 solve()
```

### Space Optimized Solution

```python
def solve():
 n = int(input())
 k = int(input())

 # Only need previous state
 end_zero = 0      # Numbers ending with 0
 end_nonzero = k - 1  # Numbers ending with non-zero (first digit: 1 to k-1)

 for i in range(2, n + 1):
  new_end_zero = end_nonzero
  new_end_nonzero = (end_zero + end_nonzero) * (k - 1)

  end_zero = new_end_zero
  end_nonzero = new_end_nonzero

 print(end_zero + end_nonzero)

if __name__ == "__main__":
 solve()
```

### Complexity Analysis
- **Time Complexity:** O(N)
- **Space Complexity:** O(1) for optimized version, O(N) for basic DP

### Example Walkthrough
For N=2, K=10:
- dp[1][0] = 0 (can't start with 0)
- dp[1][1] = 9 (digits 1-9)
- dp[2][0] = 9 (numbers: 10, 20, ..., 90)
- dp[2][1] = 9 * 9 = 81 (any digit 1-9 can follow any first digit)
- Total = 9 + 81 = 90

This matches: 2-digit numbers in base 10 are 10-99 (90 numbers), and all are valid since none have "00".
