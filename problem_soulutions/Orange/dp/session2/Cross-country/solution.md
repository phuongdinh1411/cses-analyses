# Cross-country

## Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

## Problem Statement

Agnes participates in cross-country races where participants follow route cards specifying checkpoints. She wants to choose a date from her admirers based on who can meet her the most times during the race.

Scoring rules:
- A runner scores one point if he meets Agnes at a checkpoint
- After scoring, both must move to their next checkpoints before scoring again
- Routes may cross the same checkpoint multiple times
- Each competitor must follow their card exactly

Find the maximum number of times Tom can meet Agnes.

## Input Format
- First line: d (number of data sets, 1 ≤ d ≤ 10)
- For each data set:
  - First line: Agnes' route (checkpoints separated by spaces, ending with 0)
  - Following lines: Tom's possible routes (each ending with 0)
  - A line starting with 0 marks end of data set
- Checkpoints are integers in [1, 1000]
- 2 to 2000 checkpoints per route

## Output Format
For each data set, output the maximum number of times Tom can meet Agnes.

## Solution

### Approach
This is a **Longest Common Subsequence (LCS)** problem! Tom needs to find checkpoints that appear in both his and Agnes' routes in the same order. The maximum meetings equals the LCS length between Agnes' route and Tom's route.

### Python Solution

```python
def lcs(agnes, tom):
 """Find longest common subsequence length"""
 m, n = len(agnes), len(tom)
 dp = [[0] * (n + 1) for _ in range(m + 1)]

 for i in range(1, m + 1):
  for j in range(1, n + 1):
   if agnes[i-1] == tom[j-1]:
    dp[i][j] = dp[i-1][j-1] + 1
   else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])

 return dp[m][n]

def solve():
 d = int(input())

 for _ in range(d):
  # Read Agnes' route
  agnes = []
  line = input().split()
  for x in line:
   val = int(x)
   if val == 0:
    break
   agnes.append(val)

  max_meetings = 0

  # Read Tom's routes
  while True:
   line = input().split()

   # Check for end of data set
   if line[0] == '0':
    break

   tom = []
   for x in line:
    val = int(x)
    if val == 0:
     break
    tom.append(val)

   # Compute LCS
   meetings = lcs(agnes, tom)
   max_meetings = max(max_meetings, meetings)

  print(max_meetings)

if __name__ == "__main__":
 solve()
```

### Space-Optimized Solution

```python
def lcs_optimized(agnes, tom):
 """LCS with O(n) space"""
 m, n = len(agnes), len(tom)
 prev = [0] * (n + 1)
 curr = [0] * (n + 1)

 for i in range(1, m + 1):
  for j in range(1, n + 1):
   if agnes[i-1] == tom[j-1]:
    curr[j] = prev[j-1] + 1
   else:
    curr[j] = max(prev[j], curr[j-1])
  prev, curr = curr, [0] * (n + 1)

 return prev[n]

def solve():
 import sys
 data = sys.stdin.read().split()
 idx = 0

 d = int(data[idx])
 idx += 1

 for _ in range(d):
  # Read Agnes' route
  agnes = []
  while data[idx] != '0':
   agnes.append(int(data[idx]))
   idx += 1
  idx += 1  # Skip the 0

  max_meetings = 0

  # Read Tom's routes
  while True:
   if data[idx] == '0':
    idx += 1
    break

   tom = []
   while data[idx] != '0':
    tom.append(int(data[idx]))
    idx += 1
   idx += 1  # Skip the 0

   meetings = lcs_optimized(agnes, tom)
   max_meetings = max(max_meetings, meetings)

  print(max_meetings)

if __name__ == "__main__":
 solve()
```

### Complexity Analysis
- **Time Complexity:** O(M × N) per route comparison where M and N are route lengths
- **Space Complexity:** O(M × N) for standard LCS, O(N) for optimized version

### Key Insight
The problem is exactly LCS (Longest Common Subsequence). Agnes and Tom both follow their routes in order, and Tom scores a point each time they're at the same checkpoint. This is equivalent to finding common elements that appear in the same relative order in both sequences - the definition of LCS.
