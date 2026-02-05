---
layout: simple
title: "Segment Tree"
permalink: /problem_soulutions/Orange/Segment Tree/
---
# Segment Tree

Problems utilizing segment trees for efficient range queries and updates, supporting operations like sum, minimum, maximum, and more in O(log n) time.

## Problems

### Blueberries

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

Teresa wants to pick blueberries from N bushes. If she picks from bush i, she cannot pick from bush i+1. Find the maximum blueberries she can pick given K (the maximum she will pick from any single bush).

#### Input Format
- First line: T (number of test cases)
- Each test case:
  - First line: N (bushes) and K (max per bush)
  - Second line: N integers (blueberries in each bush)

#### Constraints
- 1 ≤ N ≤ 1000
- 1 ≤ K ≤ 1000

#### Output Format
For each case: "Scenario #i: X" where X is maximum blueberries.

#### Solution

##### Approach
This is a variant of the House Robber problem with an additional constraint K. Use DP where:
- dp[i] = max blueberries from first i bushes
- For each bush, either skip it or take min(berries[i], K)

##### Python Solution

```python
def solve():
 t = int(input())

 for case in range(1, t + 1):
  n, k = map(int, input().split())
  berries = list(map(int, input().split()))

  # Cap each bush at K
  berries = [min(b, k) for b in berries]

  if n == 0:
   print(f"Scenario #{case}: 0")
   continue

  if n == 1:
   print(f"Scenario #{case}: {berries[0]}")
   continue

  # dp[i] = max berries from bushes 0..i
  dp = [0] * n
  dp[0] = berries[0]
  dp[1] = max(berries[0], berries[1])

  for i in range(2, n):
   # Either skip bush i, or take it (can't take i-1)
   dp[i] = max(dp[i-1], dp[i-2] + berries[i])

  print(f"Scenario #{case}: {dp[n-1]}")

if __name__ == "__main__":
 solve()
```

### Space-Optimized Solution

```python
def solve():
 t = int(input())

 for case in range(1, t + 1):
  n, k = map(int, input().split())
  berries = list(map(int, input().split()))

  # Cap at K
  berries = [min(b, k) for b in berries]

  if n == 0:
   result = 0
  elif n == 1:
   result = berries[0]
  else:
   prev2 = berries[0]
   prev1 = max(berries[0], berries[1])

   for i in range(2, n):
    curr = max(prev1, prev2 + berries[i])
    prev2 = prev1
    prev1 = curr

   result = prev1

  print(f"Scenario #{case}: {result}")

if __name__ == "__main__":
 solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N) per test case
- **Space Complexity:** O(1) with optimization

##### Key Insight
This is the classic "House Robber" DP problem. The constraint K simply caps the value at each position. The recurrence is: `dp[i] = max(dp[i-1], dp[i-2] + value[i])`.

---

### Brackets

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 11000ms
- **Memory Limit:** 512MB

#### Problem Statement

Given a bracket word (string of '(' and ')'), perform operations:
1. **Replacement**: Change the i-th bracket to its opposite
2. **Check**: Determine if current word is a correct bracket expression

A correct bracket expression has matching pairs where every '(' has a corresponding ')' later.

#### Input Format
- 10 test cases (must process all)
- Each test case:
  - Line 1: n (length of bracket word)
  - Line 2: n brackets (space-separated)
  - Line 3: m (number of operations)
  - Next m lines: operation (k=0 for check, k>0 for replace position k)

#### Output Format
For each test case: "Test i:" followed by YES/NO for each check operation.

#### Solution

##### Approach
Use Segment Tree to track:
- Unmatched '(' count (open)
- Unmatched ')' count (close)

For a valid expression: both counts should be 0.

When merging two segments: ')' from right can match '(' from left.

##### Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
 for test in range(1, 11):
  n = int(input())
  brackets = input().split()
  s = ''.join(brackets)

  # Segment tree: each node stores (unmatched_open, unmatched_close)
  tree = [(0, 0)] * (4 * n)

  def merge(left, right):
   # Unmatched ')' from right can match '(' from left
   matched = min(left[0], right[1])
   return (left[0] - matched + right[0], left[1] + right[1] - matched)

  def build(node, start, end):
   if start == end:
    if s[start] == '(':
     tree[node] = (1, 0)
    else:
     tree[node] = (0, 1)
    return

   mid = (start + end) // 2
   build(2*node, start, mid)
   build(2*node+1, mid+1, end)
   tree[node] = merge(tree[2*node], tree[2*node+1])

  def update(node, start, end, idx):
   if start == end:
    # Flip bracket
    if tree[node] == (1, 0):
     tree[node] = (0, 1)
    else:
     tree[node] = (1, 0)
    return

   mid = (start + end) // 2
   if idx <= mid:
    update(2*node, start, mid, idx)
   else:
    update(2*node+1, mid+1, end, idx)
   tree[node] = merge(tree[2*node], tree[2*node+1])

  if n > 0:
   build(1, 0, n-1)

  m = int(input())
  print(f"Test {test}:")

  for _ in range(m):
   k = int(input())
   if k == 0:
    # Check if valid
    if n > 0 and tree[1] == (0, 0):
     print("YES")
    else:
     print("NO")
   else:
    # Replace bracket at position k (1-indexed)
    update(1, 0, n-1, k-1)

if __name__ == "__main__":
 solve()
```

##### Alternative

```python
def solve():
 for test in range(1, 11):
  n = int(input())
  s = list(input().split())

  # Convert to +1/-1
  arr = [1 if c == '(' else -1 for c in s]

  # Segment tree storing (sum, min_prefix)
  size = 1
  while size < n:
   size *= 2

  tree_sum = [0] * (2 * size)
  tree_min = [0] * (2 * size)

  def build():
   for i in range(n):
    tree_sum[size + i] = arr[i]
    tree_min[size + i] = arr[i]

   for i in range(size - 1, 0, -1):
    tree_sum[i] = tree_sum[2*i] + tree_sum[2*i+1]
    tree_min[i] = min(tree_min[2*i], tree_sum[2*i] + tree_min[2*i+1])

  def update(idx):
   arr[idx] *= -1
   i = size + idx
   tree_sum[i] = arr[idx]
   tree_min[i] = arr[idx]

   i //= 2
   while i >= 1:
    tree_sum[i] = tree_sum[2*i] + tree_sum[2*i+1]
    tree_min[i] = min(tree_min[2*i], tree_sum[2*i] + tree_min[2*i+1])
    i //= 2

  if n > 0:
   build()

  m = int(input())
  print(f"Test {test}:")

  for _ in range(m):
   k = int(input())
   if k == 0:
    # Valid if sum=0 and min_prefix >= 0
    if n > 0 and tree_sum[1] == 0 and tree_min[1] >= 0:
     print("YES")
    else:
     print("NO")
   else:
    update(k - 1)

if __name__ == "__main__":
 solve()
```

##### Complexity Analysis
- **Time Complexity:** O(M log N) per test case
- **Space Complexity:** O(N)

##### Key Insight
A bracket sequence is valid iff: (1) total sum is 0 (equal '(' and ')'), and (2) no prefix has more ')' than '('. Track these with segment tree for efficient updates.

---

### Circular RMQ

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given a circular array of n elements, support two operations:
1. **inc(lf, rg, v)**: Add v to all elements in range [lf, rg] (circular)
2. **rmq(lf, rg)**: Return minimum in range [lf, rg] (circular)

Circular means if lf > rg, the range wraps around: [lf, n-1] ∪ [0, rg].

#### Input Format
- First line: n (1 ≤ n ≤ 200000)
- Second line: n integers (initial array)
- Third line: m (0 ≤ m ≤ 200000)
- Next m lines: operations (2 integers = rmq, 3 integers = inc)

#### Output Format
For each rmq operation, print the result.

#### Solution

##### Approach
Use Segment Tree with lazy propagation for range updates and range minimum queries. Handle circular ranges by splitting into two regular ranges.

##### Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
 n = int(input())
 arr = list(map(int, input().split()))
 m = int(input())

 INF = float('inf')

 # Segment tree with lazy propagation
 tree = [0] * (4 * n)
 lazy = [0] * (4 * n)

 def build(node, start, end):
  if start == end:
   tree[node] = arr[start]
   return
  mid = (start + end) // 2
  build(2*node, start, mid)
  build(2*node+1, mid+1, end)
  tree[node] = min(tree[2*node], tree[2*node+1])

 def push_down(node):
  if lazy[node] != 0:
   lazy[2*node] += lazy[node]
   lazy[2*node+1] += lazy[node]
   tree[2*node] += lazy[node]
   tree[2*node+1] += lazy[node]
   lazy[node] = 0

 def update(node, start, end, l, r, val):
  if r < start or end < l:
   return
  if l <= start and end <= r:
   tree[node] += val
   lazy[node] += val
   return
  push_down(node)
  mid = (start + end) // 2
  update(2*node, start, mid, l, r, val)
  update(2*node+1, mid+1, end, l, r, val)
  tree[node] = min(tree[2*node], tree[2*node+1])

 def query(node, start, end, l, r):
  if r < start or end < l:
   return INF
  if l <= start and end <= r:
   return tree[node]
  push_down(node)
  mid = (start + end) // 2
  return min(query(2*node, start, mid, l, r),
    query(2*node+1, mid+1, end, l, r))

 build(1, 0, n-1)

 results = []
 for _ in range(m):
  line = list(map(int, input().split()))

  if len(line) == 2:
   # RMQ query
   lf, rg = line
   if lf <= rg:
    results.append(query(1, 0, n-1, lf, rg))
   else:
    # Circular: [lf, n-1] and [0, rg]
    results.append(min(query(1, 0, n-1, lf, n-1),
        query(1, 0, n-1, 0, rg)))
  else:
   # Inc update
   lf, rg, v = line
   if lf <= rg:
    update(1, 0, n-1, lf, rg, v)
   else:
    update(1, 0, n-1, lf, n-1, v)
    update(1, 0, n-1, 0, rg, v)

 print('\n'.join(map(str, results)))

if __name__ == "__main__":
 solve()
```

##### Complexity Analysis
- **Time Complexity:** O((N + M) log N)
- **Space Complexity:** O(N)

##### Key Insight
Circular ranges [lf, rg] where lf > rg can be split into two linear ranges: [lf, n-1] and [0, rg]. Use lazy propagation for efficient range updates. The segment tree maintains minimum values with additive lazy tags.

---

### Course Schedule

#### Problem Information
- **Source:** Big-O
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

There are N courses labeled from 0 to n-1. Some courses have prerequisites. For example, to take course 0 you must first take course 1, expressed as pair [0, 1].

Given the total number of courses and a list of prerequisite pairs, determine if it's possible to finish all courses.

#### Input Format
- First line: N, M - number of courses and prerequisite pairs
- Next M lines: two integers u, v representing prerequisite pair [u, v]

#### Output Format
Print "yes" if you can finish all courses, otherwise print "no".

#### Solution

##### Approach
This is a cycle detection problem in a directed graph. If the prerequisite graph contains a cycle, it's impossible to finish all courses. Use:
1. **Topological Sort (Kahn's Algorithm)**: If we can process all nodes, no cycle exists
2. **DFS with coloring**: Detect back edges indicating cycles

##### Python Solution

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

##### Alternative

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

##### Complexity Analysis
- **Time Complexity:** O(N + M)
- **Space Complexity:** O(N + M)

##### Key Insight
The problem reduces to cycle detection in a directed graph. Prerequisites form edges in the dependency graph. If there's a cycle (A requires B, B requires C, C requires A), it's impossible to complete all courses. Kahn's algorithm naturally detects cycles: if fewer than N nodes are processed, a cycle exists.

---

### Curious Robin Hood

#### Problem Information
- **Source:** LightOJ
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

#### Problem Statement

Robin Hood has n sacks numbered from 0 to n-1, each containing some money. He can perform three operations:
1. **Type 1 (i)**: Give all money from sack i to the poor (set to 0, return old value)
2. **Type 2 (i, v)**: Add money v to sack i
3. **Type 3 (i, j)**: Find total money from sack i to sack j

#### Input Format
- T test cases
- Each test case:
  - First line: n (sacks) and q (queries)
  - Second line: n integers (initial money in each sack)
  - Next q lines: operation type followed by parameters

#### Output Format
For each test case, print "Case X:" followed by results for type 1 and type 3 queries.

#### Solution

##### Approach
Use a Segment Tree for:
- Point update (set value, add value)
- Range sum query

For type 1: Query point value, then set to 0
For type 2: Add value to point
For type 3: Range sum query

##### Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
 t = int(input())

 for case in range(1, t + 1):
  n, q = map(int, input().split())
  arr = list(map(int, input().split()))

  # Segment tree for range sum
  tree = [0] * (4 * n)

  def build(node, start, end):
   if start == end:
    tree[node] = arr[start]
    return
   mid = (start + end) // 2
   build(2 * node, start, mid)
   build(2 * node + 1, mid + 1, end)
   tree[node] = tree[2 * node] + tree[2 * node + 1]

  def update(node, start, end, idx, val):
   if start == end:
    tree[node] = val
    return
   mid = (start + end) // 2
   if idx <= mid:
    update(2 * node, start, mid, idx, val)
   else:
    update(2 * node + 1, mid + 1, end, idx, val)
   tree[node] = tree[2 * node] + tree[2 * node + 1]

  def query_point(node, start, end, idx):
   if start == end:
    return tree[node]
   mid = (start + end) // 2
   if idx <= mid:
    return query_point(2 * node, start, mid, idx)
   else:
    return query_point(2 * node + 1, mid + 1, end, idx)

  def query_range(node, start, end, l, r):
   if r < start or end < l:
    return 0
   if l <= start and end <= r:
    return tree[node]
   mid = (start + end) // 2
   return query_range(2 * node, start, mid, l, r) + \
    query_range(2 * node + 1, mid + 1, end, l, r)

  build(1, 0, n - 1)

  print(f"Case {case}:")

  for _ in range(q):
   query = list(map(int, input().split()))
   op = query[0]

   if op == 1:
    # Give all money from sack i to poor
    i = query[1]
    old_val = query_point(1, 0, n - 1, i)
    update(1, 0, n - 1, i, 0)
    print(old_val)

   elif op == 2:
    # Add money v to sack i
    i, v = query[1], query[2]
    old_val = query_point(1, 0, n - 1, i)
    update(1, 0, n - 1, i, old_val + v)

   else:  # op == 3
    # Sum from sack i to sack j
    i, j = query[1], query[2]
    print(query_range(1, 0, n - 1, i, j))

if __name__ == "__main__":
 solve()
```

##### Alternative

```python
import sys
input = sys.stdin.readline

def solve():
 t = int(input())

 for case in range(1, t + 1):
  n, q = map(int, input().split())
  arr = list(map(int, input().split()))

  # Fenwick tree (1-indexed)
  bit = [0] * (n + 1)

  def update_bit(i, delta):
   i += 1  # Convert to 1-indexed
   while i <= n:
    bit[i] += delta
    i += i & (-i)

  def prefix_sum(i):
   i += 1  # Convert to 1-indexed
   total = 0
   while i > 0:
    total += bit[i]
    i -= i & (-i)
   return total

  def range_sum(l, r):
   if l == 0:
    return prefix_sum(r)
   return prefix_sum(r) - prefix_sum(l - 1)

  # Build BIT
  for i in range(n):
   update_bit(i, arr[i])

  print(f"Case {case}:")

  for _ in range(q):
   query = list(map(int, input().split()))
   op = query[0]

   if op == 1:
    i = query[1]
    old_val = arr[i]
    update_bit(i, -old_val)
    arr[i] = 0
    print(old_val)

   elif op == 2:
    i, v = query[1], query[2]
    update_bit(i, v)
    arr[i] += v

   else:
    i, j = query[1], query[2]
    print(range_sum(i, j))

if __name__ == "__main__":
 solve()
```

##### Complexity Analysis
- **Time Complexity:** O((N + Q) log N)
- **Space Complexity:** O(N)

##### Key Insight
This is a classic segment tree application with point updates and range sum queries. For type 1 queries, we need to both retrieve and reset the value, which requires a point query followed by a point update. Fenwick Tree (BIT) is also applicable since we only need range sums (not other associative operations).

---

### Interval Product

#### Problem Information
- **Source:** UVALive
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

Given a sequence of N integers X1, X2, ..., XN, perform K operations:
1. **Change I V**: Set Xi to V
2. **Product I J**: Output the sign of the product Xi * Xi+1 * ... * XJ

The sign is:
- `+` if product is positive
- `-` if product is negative
- `0` if product is zero

#### Input Format
- Multiple test cases
- Each test case:
  - First line: N and K
  - Second line: N integers (-100 to 100)
  - Next K lines: operations (C for change, P for product)

#### Output Format
For each test case, output a string of signs for all product queries.

#### Solution

##### Approach
We don't need the actual product, just its sign. Track:
- Count of zeros in range
- Count of negative numbers in range

If zeros > 0: sign is '0'
Else if negatives is odd: sign is '-'
Else: sign is '+'

Use Segment Tree for efficient range queries and point updates.

##### Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
 while True:
  line = input().split()
  if not line:
   break

  n, k = int(line[0]), int(line[1])
  arr = list(map(int, input().split()))

  # Segment tree: store (zero_count, negative_count)
  tree = [(0, 0)] * (4 * n)

  def get_sign(val):
   if val == 0:
    return (1, 0)  # 1 zero, 0 negatives
   elif val < 0:
    return (0, 1)  # 0 zeros, 1 negative
   else:
    return (0, 0)  # 0 zeros, 0 negatives

  def merge(left, right):
   return (left[0] + right[0], left[1] + right[1])

  def build(node, start, end):
   if start == end:
    tree[node] = get_sign(arr[start])
    return
   mid = (start + end) // 2
   build(2 * node, start, mid)
   build(2 * node + 1, mid + 1, end)
   tree[node] = merge(tree[2 * node], tree[2 * node + 1])

  def update(node, start, end, idx, val):
   if start == end:
    tree[node] = get_sign(val)
    return
   mid = (start + end) // 2
   if idx <= mid:
    update(2 * node, start, mid, idx, val)
   else:
    update(2 * node + 1, mid + 1, end, idx, val)
   tree[node] = merge(tree[2 * node], tree[2 * node + 1])

  def query(node, start, end, l, r):
   if r < start or end < l:
    return (0, 0)  # identity
   if l <= start and end <= r:
    return tree[node]
   mid = (start + end) // 2
   return merge(query(2 * node, start, mid, l, r),
      query(2 * node + 1, mid + 1, end, l, r))

  build(1, 0, n - 1)

  result = []
  for _ in range(k):
   parts = input().split()
   op = parts[0]

   if op == 'C':
    i, v = int(parts[1]) - 1, int(parts[2])  # 1-indexed to 0-indexed
    update(1, 0, n - 1, i, v)
   else:  # op == 'P'
    i, j = int(parts[1]) - 1, int(parts[2]) - 1
    zeros, negatives = query(1, 0, n - 1, i, j)

    if zeros > 0:
     result.append('0')
    elif negatives % 2 == 1:
     result.append('-')
    else:
     result.append('+')

  print(''.join(result))

if __name__ == "__main__":
 solve()
```

##### Alternative

```python
import sys
input = sys.stdin.readline

def solve():
 while True:
  line = input().split()
  if not line:
   break

  n, k = int(line[0]), int(line[1])
  arr = list(map(int, input().split()))

  # Segment tree: store sign (-1, 0, or 1)
  tree = [1] * (4 * n)

  def sign(val):
   if val == 0:
    return 0
   return 1 if val > 0 else -1

  def build(node, start, end):
   if start == end:
    tree[node] = sign(arr[start])
    return
   mid = (start + end) // 2
   build(2 * node, start, mid)
   build(2 * node + 1, mid + 1, end)
   tree[node] = tree[2 * node] * tree[2 * node + 1]

  def update(node, start, end, idx, val):
   if start == end:
    tree[node] = sign(val)
    return
   mid = (start + end) // 2
   if idx <= mid:
    update(2 * node, start, mid, idx, val)
   else:
    update(2 * node + 1, mid + 1, end, idx, val)
   tree[node] = tree[2 * node] * tree[2 * node + 1]

  def query(node, start, end, l, r):
   if r < start or end < l:
    return 1  # identity for multiplication
   if l <= start and end <= r:
    return tree[node]
   mid = (start + end) // 2
   return query(2 * node, start, mid, l, r) * \
    query(2 * node + 1, mid + 1, end, l, r)

  build(1, 0, n - 1)

  result = []
  for _ in range(k):
   parts = input().split()
   op = parts[0]

   if op == 'C':
    i, v = int(parts[1]) - 1, int(parts[2])
    update(1, 0, n - 1, i, v)
   else:
    i, j = int(parts[1]) - 1, int(parts[2]) - 1
    s = query(1, 0, n - 1, i, j)

    if s == 0:
     result.append('0')
    elif s < 0:
     result.append('-')
    else:
     result.append('+')

  print(''.join(result))

if __name__ == "__main__":
 solve()
```

##### Complexity Analysis
- **Time Complexity:** O((N + K) log N)
- **Space Complexity:** O(N)

##### Key Insight
Instead of tracking actual products (which would overflow), track only the sign. The sign of a product depends on: (1) whether any element is zero, and (2) the parity of negative numbers. The alternative solution is more elegant: store signs (-1, 0, 1) and multiply them directly, since sign(a*b) = sign(a) * sign(b).

---

### Xenia and Bit Operations

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

#### Problem Statement

Xenia has a sequence of 2^n non-negative integers. She calculates value v by:
1. First iteration: OR of adjacent pairs → sequence of 2^(n-1) elements
2. Second iteration: XOR of adjacent pairs → sequence of 2^(n-2) elements
3. Continue alternating OR and XOR until one element remains

Given m queries, each setting a[p] = b, output v after each query.

#### Input Format
- First line: n (1 ≤ n ≤ 17), m (1 ≤ m ≤ 10^5)
- Second line: 2^n integers (the initial sequence)
- Next m lines: p, b (set a[p] = b)

#### Output Format
For each query, print the resulting value v.

#### Solution

##### Approach
This is a perfect segment tree problem where:
- Leaf nodes store array values
- Internal nodes store OR or XOR depending on their level
- Level 0 (leaves): values
- Level 1: OR of pairs
- Level 2: XOR of pairs
- And so on, alternating

Update: Change leaf, propagate up with alternating operations.

##### Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
 n, m = map(int, input().split())
 size = 1 << n  # 2^n

 arr = list(map(int, input().split()))

 # Segment tree
 tree = [0] * (2 * size)

 def build():
  # Fill leaves
  for i in range(size):
   tree[size + i] = arr[i]

  # Build internal nodes
  # Level counting: leaves are at level 0
  # Parent at level 1, etc.
  # At level k from bottom, use OR if k is odd, XOR if k is even (for k >= 1)

  for i in range(size - 1, 0, -1):
   # Determine level: how many times we can divide i by 2 before it becomes 0
   # Actually, level is log2(size) - log2(i)
   # Simpler: level from leaves is (n - bit_length of i + 1)
   level = n - (i.bit_length() - 1)

   if level % 2 == 1:
    tree[i] = tree[2 * i] | tree[2 * i + 1]
   else:
    tree[i] = tree[2 * i] ^ tree[2 * i + 1]

 def update(pos, val):
  pos += size  # Go to leaf
  tree[pos] = val

  level = 1  # First level above leaves
  pos //= 2

  while pos >= 1:
   if level % 2 == 1:
    tree[pos] = tree[2 * pos] | tree[2 * pos + 1]
   else:
    tree[pos] = tree[2 * pos] ^ tree[2 * pos + 1]
   pos //= 2
   level += 1

 build()

 results = []
 for _ in range(m):
  p, b = map(int, input().split())
  update(p - 1, b)  # Convert to 0-indexed
  results.append(tree[1])

 print('\n'.join(map(str, results)))

if __name__ == "__main__":
 solve()
```

##### Alternative

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(500000)

def solve():
 n, m = map(int, input().split())
 size = 1 << n

 arr = list(map(int, input().split()))

 tree = [0] * (4 * size)

 def build(node, start, end, use_or):
  if start == end:
   tree[node] = arr[start]
   return

  mid = (start + end) // 2
  build(2 * node, start, mid, not use_or)
  build(2 * node + 1, mid + 1, end, not use_or)

  if use_or:
   tree[node] = tree[2 * node] | tree[2 * node + 1]
  else:
   tree[node] = tree[2 * node] ^ tree[2 * node + 1]

 def update(node, start, end, idx, val, use_or):
  if start == end:
   tree[node] = val
   return

  mid = (start + end) // 2
  if idx <= mid:
   update(2 * node, start, mid, idx, val, not use_or)
  else:
   update(2 * node + 1, mid + 1, end, idx, val, not use_or)

  if use_or:
   tree[node] = tree[2 * node] | tree[2 * node + 1]
  else:
   tree[node] = tree[2 * node] ^ tree[2 * node + 1]

 # Start with OR at root level (level n uses OR if n is odd)
 # Actually, first operation (leaves combine) is OR, so root uses OR if n is odd
 root_use_or = (n % 2 == 1)

 build(1, 0, size - 1, root_use_or)

 results = []
 for _ in range(m):
  p, b = map(int, input().split())
  update(1, 0, size - 1, p - 1, b, root_use_or)
  results.append(tree[1])

 print('\n'.join(map(str, results)))

if __name__ == "__main__":
 solve()
```

##### Complexity Analysis
- **Time Complexity:** O(2^n + m * n) for build and queries
- **Space Complexity:** O(2^n)

##### Key Insight
The problem describes a perfect binary tree where operations alternate by level. Leaves store values, and each parent combines children with OR or XOR alternating by level. Point updates propagate O(n) levels up. The key is determining which operation to use at each level - if distance from leaves is odd, use OR; if even, use XOR.

