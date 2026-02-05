# Online Courses in BSU

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

Polycarp needs to pass k main online courses to get a diploma. There are n courses total, with dependencies (prerequisites). Find the minimum number of courses to pass and the order to pass them.

## Input Format
- First line: n (total courses) and k (main courses needed)
- Second line: k distinct integers (main course numbers)
- Next n lines: for course i, first tᵢ (number of prerequisites), then tᵢ course numbers

## Constraints
- 1 ≤ k ≤ n ≤ 10^5
- Sum of all tᵢ ≤ 10^5

## Output Format
- Print -1 if impossible (cycle exists)
- Otherwise, print m (minimum courses) and the order to pass them

## Solution

### Approach
Use DFS-based topological sort starting only from main courses. This naturally finds only the necessary prerequisites. Detect cycles using three-color marking (white/gray/black).

### Python Solution

```python
import sys
sys.setrecursionlimit(200000)

def solve():
  n, k = map(int, input().split())
  main_courses = list(map(int, input().split()))

  # Build dependency graph (course -> its prerequisites)
  deps = [[] for _ in range(n + 1)]
  for i in range(1, n + 1):
    line = list(map(int, input().split()))
    t = line[0]
    deps[i] = line[1:t+1]

  # DFS with cycle detection
  WHITE, GRAY, BLACK = 0, 1, 2
  color = [WHITE] * (n + 1)
  result = []
  has_cycle = False

  def dfs(u):
    nonlocal has_cycle
    if has_cycle:
      return

    color[u] = GRAY

    for v in deps[u]:
      if color[v] == GRAY:
        has_cycle = True
        return
      if color[v] == WHITE:
        dfs(v)

    color[u] = BLACK
    result.append(u)

  # Start DFS from each main course
  for course in main_courses:
    if color[course] == WHITE:
      dfs(course)

  if has_cycle:
    print(-1)
  else:
    print(len(result))
    print(' '.join(map(str, result)))

if __name__ == "__main__":
  solve()
```

### Iterative DFS Solution

```python
def solve():
  n, k = map(int, input().split())
  main_courses = list(map(int, input().split()))

  deps = [[] for _ in range(n + 1)]
  for i in range(1, n + 1):
    line = list(map(int, input().split()))
    t = line[0]
    deps[i] = line[1:t+1]

  WHITE, GRAY, BLACK = 0, 1, 2
  color = [WHITE] * (n + 1)
  result = []

  def dfs_iterative(start):
    stack = [(start, False)]

    while stack:
      node, processed = stack.pop()

      if processed:
        color[node] = BLACK
        result.append(node)
        continue

      if color[node] == BLACK:
        continue
      if color[node] == GRAY:
        return False  # Cycle detected

      color[node] = GRAY
      stack.append((node, True))

      for dep in deps[node]:
        if color[dep] == GRAY:
          return False  # Cycle
        if color[dep] == WHITE:
          stack.append((dep, False))

    return True

  for course in main_courses:
    if color[course] == WHITE:
      if not dfs_iterative(course):
        print(-1)
        return

  print(len(result))
  print(' '.join(map(str, result)))

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(N + E) where E is total dependencies
- **Space Complexity:** O(N + E)

### Key Insight
By starting DFS only from main courses and their dependencies, we automatically find the minimal set of required courses. The topological order gives a valid sequence (prerequisites before dependents). Cycle detection ensures the problem is solvable.
