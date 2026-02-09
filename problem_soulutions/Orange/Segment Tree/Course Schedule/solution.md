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

## Example
```
Input:
4 4
1 0
2 0
3 1
3 2

Output:
yes
```
4 courses, 4 prerequisites. Course 1 requires 0, course 2 requires 0, course 3 requires 1 and 2. Order: 0 -> 1 -> 2 -> 3 is valid. No cycle exists, so "yes".

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
        graph[v].append(u)
        in_degree[u] += 1

    # Kahn's algorithm with deque
    queue = deque(i for i in range(n) if in_degree[i] == 0)

    processed = 0
    while queue:
        node = queue.popleft()
        processed += 1

        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Simplified output
    print("yes" if processed == n else "no")

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

    # Color states: 0 = unvisited, 1 = visiting, 2 = visited
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n

    def has_cycle(node):
        color[node] = GRAY

        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                return True
            if color[neighbor] == WHITE and has_cycle(neighbor):
                return True

        color[node] = BLACK
        return False

    # Check all components using any()
    has_any_cycle = any(color[i] == WHITE and has_cycle(i) for i in range(n))
    print("no" if has_any_cycle else "yes")

if __name__ == "__main__":
    solve()
```

### Complexity Analysis
- **Time Complexity:** O(N + M)
- **Space Complexity:** O(N + M)

### Key Insight
The problem reduces to cycle detection in a directed graph. Prerequisites form edges in the dependency graph. If there's a cycle (A requires B, B requires C, C requires A), it's impossible to complete all courses. Kahn's algorithm naturally detects cycles: if fewer than N nodes are processed, a cycle exists.
