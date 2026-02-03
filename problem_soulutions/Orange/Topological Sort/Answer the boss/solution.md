# Answer the Boss!

## Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 1024MB

## Problem Statement

Eloy wants to know the "rank" of each employee in a company. Given the number of employees and relations between them (who is lower than whom), output the rank of each employee.

Rank 1 is the "boss" (not bullied by anybody). Employees with the same rank should be listed in lexicographical order.

## Input Format
- First line: T (number of test cases)
- For each test case:
  - First line: N (employees) and R (relations)
  - Next R lines: R1 R2 meaning "employee R1 is lower than R2's rank"

## Constraints
- 1 ≤ N ≤ 1000
- 1 ≤ R ≤ 10000

## Output Format
For each test case, print "Scenario #i:" followed by N lines with rank and employee index, sorted by rank then by employee index.

## Solution

### Approach
1. Build a directed graph where edge (R2 → R1) means R1 is subordinate to R2
2. Use topological sort to process nodes in order
3. Rank of each node = max(rank of all superiors) + 1
4. Nodes with no incoming edges (in original graph) have rank 1

### Python Solution

```python
from collections import defaultdict, deque

def solve():
    t = int(input())

    for case in range(1, t + 1):
        n, r = map(int, input().split())

        # adj[v] contains subordinates of v
        # in_degree tracks how many superiors each employee has
        adj = defaultdict(list)
        in_degree = [0] * n

        for _ in range(r):
            r1, r2 = map(int, input().split())
            # r1 is lower than r2, so r2 -> r1
            adj[r2].append(r1)
            in_degree[r1] += 1

        # Compute ranks using modified topological sort
        rank = [0] * n
        queue = deque()

        # Start with bosses (no one above them)
        for i in range(n):
            if in_degree[i] == 0:
                rank[i] = 1
                queue.append(i)

        while queue:
            u = queue.popleft()
            for v in adj[u]:
                rank[v] = max(rank[v], rank[u] + 1)
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        # Create result list and sort
        employees = [(rank[i], i) for i in range(n)]
        employees.sort()

        print(f"Scenario #{case}:")
        for r, idx in employees:
            print(r, idx)

if __name__ == "__main__":
    solve()
```

### Alternative Solution with DFS

```python
def solve():
    t = int(input())

    for case in range(1, t + 1):
        n, r = map(int, input().split())

        adj = [[] for _ in range(n)]
        in_degree = [0] * n

        for _ in range(r):
            r1, r2 = map(int, input().split())
            adj[r2].append(r1)
            in_degree[r1] += 1

        # DFS to compute ranks
        rank = [0] * n

        def dfs(u, current_rank):
            rank[u] = max(rank[u], current_rank)
            for v in adj[u]:
                dfs(v, rank[u] + 1)

        # Start DFS from all bosses
        for i in range(n):
            if in_degree[i] == 0:
                dfs(i, 1)

        # Sort and output
        result = sorted([(rank[i], i) for i in range(n)])

        print(f"Scenario #{case}:")
        for r, idx in result:
            print(r, idx)

if __name__ == "__main__":
    solve()
```

### Complexity Analysis
- **Time Complexity:** O(N + R) for topological sort, O(N log N) for sorting output
- **Space Complexity:** O(N + R) for adjacency list

### Key Insight
The rank of an employee is 1 + maximum rank among all their superiors. Process employees in topological order (superiors before subordinates) to correctly compute ranks.
