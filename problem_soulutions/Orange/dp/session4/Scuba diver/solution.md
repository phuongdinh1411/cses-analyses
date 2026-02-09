# Scuba diver

## Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

## Problem Statement

A scuba diver needs specific amounts of oxygen (t) and nitrogen (a) for a dive. He has n cylinders available, each with:
- Oxygen volume: ti
- Nitrogen volume: ai
- Weight: wi

Find the minimum total weight of cylinders to carry to meet both gas requirements.

## Input Format
- c test cases (separated by blank lines)
- Each test case:
  - First line: t, a (required oxygen and nitrogen)
  - Second line: n (number of cylinders)
  - Next n lines: ti, ai, wi (oxygen, nitrogen, weight) for each cylinder

## Constraints
- 1 ≤ t ≤ 21
- 1 ≤ a ≤ 79
- 1 ≤ n ≤ 1000

## Output Format
For each test case, print the minimum weight needed.

## Example
```
Input:
1
5 60
5
3 36 120
10 25 129
5 50 250
1 45 130
4 20 119

Output:
249
```
Need 5 oxygen and 60 nitrogen. Cylinders: (3,36,120), (10,25,129), (5,50,250), (1,45,130), (4,20,119). Select cylinders 1 and 5: oxygen=3+4=7>=5, nitrogen=36+20=56<60. Need more. Best combination weighs 249 (e.g., cylinders 2+5: 10+4=14 oxygen, 25+20=45<60... continue searching).

## Solution

### Approach
This is a 2D knapsack problem (minimization variant):
- Two constraints: oxygen ≥ t, nitrogen ≥ a
- Minimize total weight

dp[i][j] = minimum weight to get at least i oxygen and j nitrogen

### Python Solution

```python
def solve():
  import sys
  input = sys.stdin.readline

  c = int(input())

  for _ in range(c):
    t_req, a_req = map(int, input().split())
    n = int(input())

    # Read cylinders using list comprehension with tuple unpacking
    cylinders = [
      tuple(map(int, input().split()))
      for _ in range(n)
    ]

    INF = float('inf')

    # dp[o][n] = min weight to get at least o oxygen and n nitrogen
    dp = [[INF] * (a_req + 1) for _ in range(t_req + 1)]
    dp[0][0] = 0

    for oxy, nit, weight in cylinders:
      # Process in reverse (0/1 knapsack)
      for o in range(t_req, -1, -1):
        for ni in range(a_req, -1, -1):
          if dp[o][ni] < INF:
            # New oxygen and nitrogen (cap at requirements)
            new_o, new_n = min(o + oxy, t_req), min(ni + nit, a_req)
            dp[new_o][new_n] = min(dp[new_o][new_n], dp[o][ni] + weight)

    print(dp[t_req][a_req])

if __name__ == "__main__":
  solve()
```

### Alternative Solution

```python
def solve():
  import sys
  data = sys.stdin.read().split()
  idx = 0

  c = int(data[idx])
  idx += 1

  for _ in range(c):
    t_req = int(data[idx])
    a_req = int(data[idx + 1])
    idx += 2

    n = int(data[idx])
    idx += 1

    cylinders = []
    for _ in range(n):
      ti = int(data[idx])
      ai = int(data[idx + 1])
      wi = int(data[idx + 2])
      idx += 3
      cylinders.append((ti, ai, wi))

    INF = float('inf')

    # dp[oxygen][nitrogen] = min weight
    dp = [[INF] * (a_req + 1) for _ in range(t_req + 1)]
    dp[0][0] = 0

    for oxy, nit, weight in cylinders:
      new_dp = [row[:] for row in dp]

      for o in range(t_req + 1):
        for n in range(a_req + 1):
          if dp[o][n] == INF:
            continue

          # Add this cylinder
          no = min(o + oxy, t_req)
          nn = min(n + nit, a_req)
          new_dp[no][nn] = min(new_dp[no][nn], dp[o][n] + weight)

      dp = new_dp

    print(dp[t_req][a_req])

if __name__ == "__main__":
  solve()
```

### In-Place Solution

```python
def solve():
  import sys
  input = sys.stdin.readline

  c = int(input())

  for _ in range(c):
    t_req, a_req = map(int, input().split())
    n = int(input())

    INF = 10**9

    # dp[o][n] = min weight for o oxygen, n nitrogen
    dp = [[INF] * (a_req + 1) for _ in range(t_req + 1)]
    dp[0][0] = 0

    for _ in range(n):
      ti, ai, wi = map(int, input().split())

      # Reverse iteration for 0/1 knapsack
      for o in range(t_req, -1, -1):
        for ni in range(a_req, -1, -1):
          if dp[o][ni] < INF:
            new_o = min(o + ti, t_req)
            new_n = min(ni + ai, a_req)
            dp[new_o][new_n] = min(dp[new_o][new_n], dp[o][ni] + wi)

    print(dp[t_req][a_req])

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(n × t × a)
- **Space Complexity:** O(t × a)

### Key Insight
This is a 2D 0/1 knapsack where we minimize weight while meeting two constraints (oxygen ≥ t, nitrogen ≥ a). Since we need "at least" the requirements, we cap states at the requirement values - any excess doesn't help. dp[t_req][a_req] gives the minimum weight to meet both requirements exactly or exceed them.
