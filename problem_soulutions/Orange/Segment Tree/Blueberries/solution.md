# Blueberries

## Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

Teresa wants to pick blueberries from N bushes. If she picks from bush i, she cannot pick from bush i+1. Find the maximum blueberries she can pick given K (the maximum she will pick from any single bush).

## Input Format
- First line: T (number of test cases)
- Each test case:
  - First line: N (bushes) and K (max per bush)
  - Second line: N integers (blueberries in each bush)

## Constraints
- 1 ≤ N ≤ 1000
- 1 ≤ K ≤ 1000

## Output Format
For each case: "Scenario #i: X" where X is maximum blueberries.

## Solution

### Approach
This is a variant of the House Robber problem with an additional constraint K. Use DP where:
- dp[i] = max blueberries from first i bushes
- For each bush, either skip it or take min(berries[i], K)

### Python Solution

```python
def solve():
 t = int(input())

 for case in range(1, t + 1):
  n, k = map(int, input().split())
  berries = list(map(int, input().split()))

  # Cap each bush at K
  berries = [min(b, k) for b in berries]

  if n == 0:
   print(f"Scenario #{case}: 0")
   continue

  if n == 1:
   print(f"Scenario #{case}: {berries[0]}")
   continue

  # dp[i] = max berries from bushes 0..i
  dp = [0] * n
  dp[0] = berries[0]
  dp[1] = max(berries[0], berries[1])

  for i in range(2, n):
   # Either skip bush i, or take it (can't take i-1)
   dp[i] = max(dp[i-1], dp[i-2] + berries[i])

  print(f"Scenario #{case}: {dp[n-1]}")

if __name__ == "__main__":
 solve()
```

### Space-Optimized Solution

```python
def solve():
 t = int(input())

 for case in range(1, t + 1):
  n, k = map(int, input().split())
  berries = list(map(int, input().split()))

  # Cap at K
  berries = [min(b, k) for b in berries]

  if n == 0:
   result = 0
  elif n == 1:
   result = berries[0]
  else:
   prev2 = berries[0]
   prev1 = max(berries[0], berries[1])

   for i in range(2, n):
    curr = max(prev1, prev2 + berries[i])
    prev2 = prev1
    prev1 = curr

   result = prev1

  print(f"Scenario #{case}: {result}")

if __name__ == "__main__":
 solve()
```

### Complexity Analysis
- **Time Complexity:** O(N) per test case
- **Space Complexity:** O(1) with optimization

### Key Insight
This is the classic "House Robber" DP problem. The constraint K simply caps the value at each position. The recurrence is: `dp[i] = max(dp[i-1], dp[i-2] + value[i])`.
