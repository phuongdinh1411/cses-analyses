# Hierarchy

## Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1500ms
- **Memory Limit:** 1024MB

## Problem Statement

A group of graduated students wants to establish a company hierarchy. One student will be the main boss, and each other student will have exactly one boss. Every boss has a strictly greater salary than all subordinates (no cycles).

K most successful students (numbered 1 to K) have given statements about who they want to be superior to. A superior means being the boss or one of the boss's superiors (not necessarily direct boss).

Create a hierarchy satisfying all successful students' wishes.

## Input Format
- First line: N (total students, N ≤ 100000) and K (successful students, K < N)
- Next K lines: For student A, first an integer W (number of wishes, 1 ≤ W ≤ 10), then W integers representing students that A wants to be superior to

## Output Format
Output N integers. The A-th integer is 0 if student A is the main boss, otherwise it's the boss of student A.

## Example
```
Input:
5 2
2 3 4
1 5

Output:
0
1
2
2
1
```
Student 1 wants to be superior to students 3, 4. Student 2 wants to be superior to student 5. A valid hierarchy: Student 1 is the main boss (0), Student 2's boss is Student 1, Students 3 and 4 report to Student 2, and Student 5 reports to Student 1.

## Solution

### Approach
1. Build a directed graph where edge (A → B) means A wants to be superior to B
2. Perform topological sort to get a valid ordering
3. Assign each person's boss as the previous person in the topological order
4. The first person in the order becomes the main boss (0)

### Python Solution

```python
from collections import defaultdict

def solve():
  n, k = map(int, input().split())

  adj = defaultdict(list)

  for u in range(k):
    line = list(map(int, input().split()))
    w, *subordinates = line  # Tuple unpacking for cleaner parsing
    for v in subordinates:
      adj[u].append(v - 1)  # 0-indexed

  # DFS-based topological sort
  WHITE, GRAY, BLACK = 0, 1, 2
  color = [WHITE] * n
  topo_order = []

  def dfs(u):
    color[u] = GRAY
    for v in adj[u]:
      if color[v] == WHITE:
        dfs(v)
    color[u] = BLACK
    topo_order.append(u)

  for i in range(n):
    if color[i] == WHITE:
      dfs(i)

  topo_order.reverse()

  # Assign bosses using enumerate
  boss = [0] * n
  for i, node in enumerate(topo_order):
    boss[node] = 0 if i == 0 else topo_order[i - 1] + 1

  # Print all bosses
  print('\n'.join(map(str, boss)))

if __name__ == "__main__":
  solve()
```

### Alternative Solution with Iterative DFS

```python
def solve():
  n, k = map(int, input().split())

  adj = [[] for _ in range(n)]

  for u in range(k):
    line = list(map(int, input().split()))
    w = line[0]
    for i in range(1, w + 1):
      v = line[i] - 1
      adj[u].append(v)

  # Iterative DFS for topological sort
  visited = [False] * n
  topo_order = []

  for start in range(n):
    if visited[start]:
      continue

    stack = [(start, False)]

    while stack:
      node, processed = stack.pop()

      if processed:
        topo_order.append(node)
        continue

      if visited[node]:
        continue

      visited[node] = True
      stack.append((node, True))

      for neighbor in adj[node]:
        if not visited[neighbor]:
          stack.append((neighbor, False))

  topo_order.reverse()

  # Assign bosses based on topological order
  boss = [0] * n
  for i in range(1, n):
    boss[topo_order[i]] = topo_order[i - 1] + 1

  for b in boss:
    print(b)

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(N + E) where E is total number of wishes
- **Space Complexity:** O(N + E) for adjacency list

### Key Insight
The topological order gives us a valid hierarchy chain. If A must be superior to B, then A appears before B in topological order. By making each person's boss the immediately preceding person in this order, we create a chain that satisfies all constraints.
