# e-Coins

## Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

## Problem Statement

E-coins have two values: conventional value and InfoTechnological value. The e-modulus is calculated as:
`sqrt(X*X + Y*Y)` where X is sum of conventional values and Y is sum of InfoTechnological values.

Find the minimum number of e-coins needed to achieve a target e-modulus S.

## Input Format
- Multiple test cases
- First line of each case: m (number of e-coin types) and S (target e-modulus)
- Next m lines: conventional and InfoTechnological values of each e-coin type

## Output Format
For each case, print minimum coins needed, or "not possible" if impossible.

## Solution

### Approach
This is a 2D coin change problem. Use BFS or DP:
- State: (sum_conventional, sum_info)
- Target: find state where sqrt(x² + y²) = S, i.e., x² + y² = S²
- Minimize number of coins

### Python Solution

```python
from collections import deque

def solve():
 import sys
 input_data = sys.stdin.read().split('\n')
 idx = 0

 n = int(input_data[idx])
 idx += 1

 for _ in range(n):
  parts = input_data[idx].split()
  m, S = int(parts[0]), int(parts[1])
  idx += 1

  coins = []
  for _ in range(m):
   parts = input_data[idx].split()
   coins.append((int(parts[0]), int(parts[1])))
   idx += 1

  target_sq = S * S

  # BFS to find minimum coins
  # dist[x][y] = minimum coins to reach sum (x, y)
  INF = float('inf')
  dist = [[INF] * (S + 1) for _ in range(S + 1)]
  dist[0][0] = 0

  queue = deque([(0, 0)])

  while queue:
   x, y = queue.popleft()

   for cx, cy in coins:
    nx, ny = x + cx, y + cy

    if nx <= S and ny <= S and dist[nx][ny] == INF:
     dist[nx][ny] = dist[x][y] + 1

     if nx * nx + ny * ny == target_sq:
      print(dist[nx][ny])
      break

     queue.append((nx, ny))
   else:
    continue
   break
  else:
   # Check all valid endpoints
   found = False
   for x in range(S + 1):
    for y in range(S + 1):
     if x * x + y * y == target_sq and dist[x][y] != INF:
      print(dist[x][y])
      found = True
      break
    if found:
     break
   if not found:
    print("not possible")

if __name__ == "__main__":
 solve()
```

### Alternative DP Solution

```python
def solve_case():
 line = input().split()
 m, S = int(line[0]), int(line[1])

 coins = []
 for _ in range(m):
  parts = input().split()
  coins.append((int(parts[0]), int(parts[1])))

 target_sq = S * S
 INF = float('inf')

 # dp[x][y] = min coins to achieve sums (x, y)
 dp = [[INF] * (S + 1) for _ in range(S + 1)]
 dp[0][0] = 0

 # Process like unbounded knapsack
 for cx, cy in coins:
  for x in range(S + 1):
   for y in range(S + 1):
    if dp[x][y] < INF:
     nx, ny = x + cx, y + cy
     if nx <= S and ny <= S:
      dp[nx][ny] = min(dp[nx][ny], dp[x][y] + 1)

 # Find minimum among valid targets
 ans = INF
 for x in range(S + 1):
  for y in range(S + 1):
   if x * x + y * y == target_sq:
    ans = min(ans, dp[x][y])

 if ans == INF:
  print("not possible")
 else:
  print(ans)

def solve():
 n = int(input())
 for _ in range(n):
  solve_case()

if __name__ == "__main__":
 solve()
```

### Complexity Analysis
- **Time Complexity:** O(M × S²) for DP
- **Space Complexity:** O(S²)

### Key Insight
This is a 2D variant of the coin change problem. Instead of reaching a single target value, we need to reach any (x, y) pair where x² + y² = S². BFS finds the minimum number of coins efficiently.
