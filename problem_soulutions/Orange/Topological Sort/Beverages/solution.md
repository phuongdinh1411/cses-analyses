# Beverages

## Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

## Problem Statement

Dilbert has just finished college and decided to go out with friends. He has some strange habits and thus he decided to celebrate this important moment of his life drinking a lot. He will start drinking beverages with low alcohol content, like beer, and then will move to a beverage that contains more alcohol, like wine, until there are no more available beverages. Once Dilbert starts to drink wine he will not drink beer again, so the alcohol content of the beverages never decreases with time.

You should help Dilbert by indicating an order in which he can drink the beverages in the way he wishes.

## Input Format
- Each test case starts with N (1 ≤ N ≤ 100), the number of available beverages.
- Then N lines follow with the name of each beverage (less than 51 characters, no white spaces).
- Then an integer M (0 ≤ M ≤ 200) followed by M lines in the form "B1 B2", indicating that B2 has more alcohol than B1, so B1 should be drunk before B2.
- There is a blank line after each test case.
- In case there is no relation between two beverages, Dilbert should drink the one that appears first in the input.
- Input is terminated by EOF.

## Output Format
For each test case print: "Case #C: Dilbert should drink beverages in this order: B1 B2 ... BN." followed by a blank line.

## Example
```
Input:
3
beer
wine
vodka
2
beer wine
wine vodka

Output:
Case #1: Dilbert should drink beverages in this order: beer wine vodka.
```
Beer must be drunk before wine, and wine before vodka. Since beer appears first in input, it comes first when there's a tie.

## Solution

### Approach
This is a topological sort problem with a twist: when there are multiple valid choices, we must pick the beverage that appeared earliest in the input (smallest index). Use a min-heap (priority queue) to always select the smallest index among nodes with zero in-degree.

### Python Solution

```python
import heapq
from collections import defaultdict

def solve():
  case_num = 0

  try:
    while True:
      n = int(input())
      case_num += 1

      # Read beverage names and create mapping
      beverages = []
      name_to_id = {}

      for i in range(n):
        name = input().strip()
        beverages.append(name)
        name_to_id[name] = i

      # Build graph
      graph = defaultdict(list)
      in_degree = [0] * n

      m = int(input())
      for _ in range(m):
        line = input().split()
        b1, b2 = line[0], line[1]
        u, v = name_to_id[b1], name_to_id[b2]
        graph[u].append(v)
        in_degree[v] += 1

      # Read blank line
      try:
        input()
      except:
        pass

      # Topological sort using min-heap (to get lexicographically smallest by input order)
      heap = []
      for i in range(n):
        if in_degree[i] == 0:
          heapq.heappush(heap, i)

      result = []
      while heap:
        u = heapq.heappop(heap)
        result.append(beverages[u])

        for v in graph[u]:
          in_degree[v] -= 1
          if in_degree[v] == 0:
            heapq.heappush(heap, v)

      # Output
      print(f"Case #{case_num}: Dilbert should drink beverages in this order: {' '.join(result)}.")
      print()

  except EOFError:
    pass

if __name__ == "__main__":
  solve()
```

### Alternative Solution with Kahn's Algorithm

```python
import heapq

def topological_sort(n, graph, in_degree):
  """Topological sort with tie-breaking by index (input order)"""
  result = []
  heap = [i for i in range(n) if in_degree[i] == 0]
  heapq.heapify(heap)

  while heap:
    u = heapq.heappop(heap)
    result.append(u)

    for v in graph[u]:
      in_degree[v] -= 1
      if in_degree[v] == 0:
        heapq.heappush(heap, v)

  return result

def solve():
  import sys
  input_data = sys.stdin.read().split('\n')
  idx = 0
  case_num = 0

  while idx < len(input_data):
    try:
      n = int(input_data[idx])
    except:
      break

    idx += 1
    case_num += 1

    # Read beverages
    beverages = []
    name_to_id = {}
    for i in range(n):
      name = input_data[idx].strip()
      beverages.append(name)
      name_to_id[name] = i
      idx += 1

    # Read constraints
    m = int(input_data[idx])
    idx += 1

    graph = [[] for _ in range(n)]
    in_degree = [0] * n

    for _ in range(m):
      parts = input_data[idx].split()
      b1, b2 = parts[0], parts[1]
      u, v = name_to_id[b1], name_to_id[b2]
      graph[u].append(v)
      in_degree[v] += 1
      idx += 1

    # Skip blank line
    if idx < len(input_data) and input_data[idx].strip() == '':
      idx += 1

    # Topological sort
    order = topological_sort(n, graph, in_degree)
    result = [beverages[i] for i in order]

    print(f"Case #{case_num}: Dilbert should drink beverages in this order: {' '.join(result)}.")
    print()

if __name__ == "__main__":
  solve()
```

### Complexity Analysis
- **Time Complexity:** O(N + M + N log N) where N is beverages and M is constraints
- **Space Complexity:** O(N + M) for graph storage

### Key Insight
Using a min-heap instead of a regular queue ensures that when multiple beverages have zero in-degree, we always pick the one that appeared first in the input (smallest index).
