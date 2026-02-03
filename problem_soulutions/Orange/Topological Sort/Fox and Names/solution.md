# Fox and Names

## Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

## Problem Statement

Fox Ciel is going to publish a paper on FOCS (Foxes Operated Computer Systems). She heard a rumor: the authors list on the paper is always sorted in the lexicographical order.

After checking some examples, she found out that sometimes it wasn't true. On some papers authors' names weren't sorted in lexicographical order in normal sense. But it was always true that after some modification of the order of letters in alphabet, the order of authors becomes lexicographical!

She wants to know, if there exists an order of letters in Latin alphabet such that the names on the paper she is submitting are following in the lexicographical order. If so, you should find out any such order.

Lexicographical order is defined in following way. When we compare s and t, first we find the leftmost position with differing characters: si ≠ ti. If there is no such position (i.e. s is a prefix of t or vice versa) the shortest string is less. Otherwise, we compare characters si and ti according to their order in alphabet.

## Input Format
- The first line contains an integer n (1 ≤ n ≤ 100): number of names.
- Each of the following n lines contain one string namei (1 ≤ |namei| ≤ 100), the i-th name.
- Each name contains only lowercase Latin letters. All names are different.

## Output Format
If there exists such order of letters that the given names are sorted lexicographically, output any such order as a permutation of characters 'a'-'z'.

Otherwise output a single word "Impossible" (without quotes).

## Solution

### Approach
1. Compare adjacent names to find character ordering constraints
2. Build a directed graph where an edge (u, v) means character u must come before v
3. Use topological sort to find a valid ordering
4. If a cycle exists, output "Impossible"
5. Special case: if a longer string is a prefix of a shorter one, it's impossible

### Python Solution

```python
from collections import deque, defaultdict

def solve():
    n = int(input())
    names = [input().strip() for _ in range(n)]

    # Build graph
    graph = defaultdict(set)
    in_degree = {chr(ord('a') + i): 0 for i in range(26)}

    # Compare adjacent names
    for i in range(n - 1):
        s1, s2 = names[i], names[i + 1]
        min_len = min(len(s1), len(s2))

        found = False
        for j in range(min_len):
            if s1[j] != s2[j]:
                # s1[j] must come before s2[j] in the alphabet
                if s2[j] not in graph[s1[j]]:
                    graph[s1[j]].add(s2[j])
                    in_degree[s2[j]] += 1
                found = True
                break

        # If s1 is a prefix of s2, that's fine
        # But if s2 is a prefix of s1, it's impossible
        if not found and len(s1) > len(s2):
            print("Impossible")
            return

    # Topological sort using Kahn's algorithm
    queue = deque()
    for char in in_degree:
        if in_degree[char] == 0:
            queue.append(char)

    result = []
    while queue:
        char = queue.popleft()
        result.append(char)

        for neighbor in graph[char]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Check if all characters are included (no cycle)
    if len(result) != 26:
        print("Impossible")
    else:
        print(''.join(result))

if __name__ == "__main__":
    solve()
```

### Complexity Analysis
- **Time Complexity:** O(n × L + 26) where L is the maximum name length
- **Space Complexity:** O(26²) for the graph

### Example
For names ["hack", "heaven"], comparing:
- 'h' == 'h' ✓
- 'a' vs 'e' → 'a' must come before 'e'

The topological sort will produce an alphabet where 'a' comes before 'e'.
