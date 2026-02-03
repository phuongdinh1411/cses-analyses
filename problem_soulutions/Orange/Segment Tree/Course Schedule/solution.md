# Course Schedule

## Problem Information
- **Source:** Big-O
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

## Problem Statement

There are N courses labeled from 0 to n-1. Some courses have prerequisites. For example, to take course 0 you must first take course 1, expressed as pair [0, 1].

Given the total number of courses and a list of prerequisite pairs, determine if it's possible to finish all courses.

## Input Format
- First line: N, M - number of courses and prerequisite pairs
- Next M lines: two integers u, v representing prerequisite pair [u, v]

## Output Format
Print "yes" if you can finish all courses, otherwise print "no".

## Solution

### Approach
This is a cycle detection problem in a directed graph. If the prerequisite graph contains a cycle, it's impossible to finish all courses. Use:
1. **Topological Sort (Kahn's Algorithm)**: If we can process all nodes, no cycle exists
2. **DFS with coloring**: Detect back edges indicating cycles

### Python Solution - Kahn's Algorithm

```python
from collections import deque, defaultdict

def solve():
    n, m = map(int, input().split())

    # Build adjacency list and in-degree count
    graph = defaultdict(list)
    in_degree = [0] * n

    for _ in range(m):
        u, v = map(int, input().split())
        # u depends on v: v -> u
        graph[v].append(u)
        in_degree[u] += 1

    # Kahn's algorithm
    queue = deque()
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)

    processed = 0
    while queue:
        node = queue.popleft()
        processed += 1

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If all nodes processed, no cycle
    if processed == n:
        print("yes")
    else:
        print("no")

if __name__ == "__main__":
    solve()
```

### Alternative Solution - DFS Cycle Detection

```python
from collections import defaultdict

def solve():
    n, m = map(int, input().split())

    graph = defaultdict(list)
    for _ in range(m):
        u, v = map(int, input().split())
        graph[v].append(u)

    # 0 = unvisited, 1 = visiting, 2 = visited
    color = [0] * n

    def has_cycle(node):
        color[node] = 1  # visiting

        for neighbor in graph[node]:
            if color[neighbor] == 1:  # back edge
                return True
            if color[neighbor] == 0 and has_cycle(neighbor):
                return True

        color[node] = 2  # visited
        return False

    # Check all components
    for i in range(n):
        if color[i] == 0:
            if has_cycle(i):
                print("no")
                return

    print("yes")

if __name__ == "__main__":
    solve()
```

### Complexity Analysis
- **Time Complexity:** O(N + M)
- **Space Complexity:** O(N + M)

### Key Insight
The problem reduces to cycle detection in a directed graph. Prerequisites form edges in the dependency graph. If there's a cycle (A requires B, B requires C, C requires A), it's impossible to complete all courses. Kahn's algorithm naturally detects cycles: if fewer than N nodes are processed, a cycle exists.
