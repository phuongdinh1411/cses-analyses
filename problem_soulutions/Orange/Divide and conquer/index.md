---
layout: simple
title: "Divide and Conquer"
permalink: /problem_soulutions/Orange/Divide and conquer/
---
# Divide and conquer

Problems solved by breaking them into smaller subproblems, solving each recursively, and combining results to form the final solution.

## Problems

### Bit Maps

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Convert between two bitmap representations:
1. **B format**: 2D array of 0s and 1s (row by row)
2. **D format**: Recursive decomposition where:
   - Output '1' if all bits are 1
   - Output '0' if all bits are 0
   - Output 'D' and recursively process 4 quarters (top-left, top-right, bottom-left, bottom-right)

When dividing:
- Odd columns: left quarters have one more column than right
- Odd rows: top quarters have one more row than bottom

#### Input Format
- Format character (B or D), dimensions (rows, columns)
- The bitmap data (max 50 chars per line)
- Terminated by '#'

#### Output Format
Convert each bitmap to the other format, with dimensions right-justified (width 4 for rows, 3 for columns).

#### Solution

##### Approach
- **B to D**: Recursively check if region is all 0s, all 1s, or mixed. Mixed regions output 'D' and recurse on quarters.
- **D to B**: Read characters and fill regions recursively based on '0', '1', or 'D'.

##### Python Solution

```python
def solve():
  import sys
  data = sys.stdin.read().split()
  idx = 0

  while idx < len(data):
    fmt = data[idx]
    if fmt == '#':
      break

    h = int(data[idx + 1])
    w = int(data[idx + 2])
    idx += 3

    if fmt == 'B':
      # Read bitmap
      chars_needed = h * w
      bitmap_str = ""
      while len(bitmap_str) < chars_needed:
        bitmap_str += data[idx]
        idx += 1

      bitmap = [[0] * w for _ in range(h)]
      for i in range(h):
        for j in range(w):
          bitmap[i][j] = int(bitmap_str[i * w + j])

      # Convert B to D
      def b2d(r, c, height, width):
        if height == 0 or width == 0:
          return ""

        total = sum(bitmap[r + i][c + j]
            for i in range(height) for j in range(width))

        if total == 0:
          return "0"
        if total == height * width:
          return "1"

        # Divide into quarters
        h1, h2 = (height + 1) // 2, height // 2
        w1, w2 = (width + 1) // 2, width // 2

        return ("D" +
            b2d(r, c, h1, w1) +          # top-left
            b2d(r, c + w1, h1, w2) +     # top-right
            b2d(r + h1, c, h2, w1) +     # bottom-left
            b2d(r + h1, c + w1, h2, w2)) # bottom-right

      result = b2d(0, 0, h, w)
      print(f"D{h:4d}{w:4d}")
      for i in range(0, len(result), 50):
        print(result[i:i+50])

    else:  # fmt == 'D'
      # Read D format
      d_str = ""
      # Estimate characters needed (at most h*w for fully expanded)
      while idx < len(data) and data[idx] not in ['B', 'D', '#']:
        d_str += data[idx]
        idx += 1

      bitmap = [['0'] * w for _ in range(h)]
      d_idx = [0]

      def d2b(r, c, height, width):
        if height == 0 or width == 0:
          return

        ch = d_str[d_idx[0]]
        d_idx[0] += 1

        if ch == '0' or ch == '1':
          for i in range(height):
            for j in range(width):
              bitmap[r + i][c + j] = ch
        else:  # 'D'
          h1, h2 = (height + 1) // 2, height // 2
          w1, w2 = (width + 1) // 2, width // 2

          d2b(r, c, h1, w1)
          d2b(r, c + w1, h1, w2)
          d2b(r + h1, c, h2, w1)
          d2b(r + h1, c + w1, h2, w2)

      d2b(0, 0, h, w)
      result = ''.join(''.join(row) for row in bitmap)

      print(f"B{h:4d}{w:4d}")
      for i in range(0, len(result), 50):
        print(result[i:i+50])

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(H × W) for both conversions
- **Space Complexity:** O(H × W) for storing the bitmap

##### Key Insight
This is a divide and conquer problem with quadtree-like structure:
- B→D: Check if region is uniform; if not, divide into 4 parts
- D→B: Recursively fill regions based on the encoded characters

The quarter division rule handles odd dimensions correctly by giving the extra row/column to top/left quarters.

---

### Distance in Tree

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

Given a tree with n vertices and a positive number k, find the number of distinct pairs of vertices which have a distance of exactly k between them. Note that pairs (u, v) and (v, u) are the same.

#### Input Format
- First line: n and k (1 ≤ n ≤ 50000, 1 ≤ k ≤ 500)
- Next n-1 lines: edges aᵢ bᵢ (1 ≤ aᵢ, bᵢ ≤ n)

#### Output Format
Print the number of distinct pairs with distance exactly k.

#### Solution

##### Approach
Use Centroid Decomposition or simple DFS with counting:
1. For each node, count pairs passing through it
2. Use DFS to find distances from each node
3. Count pairs with distance sum = k

For small k (≤ 500), we can use DP on the tree.

##### Python Solution

```python
import sys
from collections import defaultdict
sys.setrecursionlimit(100000)

def solve():
  n, k = map(int, input().split())

  adj = defaultdict(list)
  for _ in range(n - 1):
    a, b = map(int, input().split())
    adj[a].append(b)
    adj[b].append(a)

  total_pairs = 0

  # cnt[v][d] = number of nodes at distance d in subtree of v
  # We'll compute this via DFS

  def dfs(u, parent):
    nonlocal total_pairs

    # cnt[d] = count of nodes at distance d from u in u's subtree
    cnt = [0] * (k + 1)
    cnt[0] = 1  # u itself at distance 0

    for v in adj[u]:
      if v == parent:
        continue

      # Get counts from child subtree
      child_cnt = dfs(v, u)

      # Count pairs: one node from previous subtrees, one from this child
      for d1 in range(k + 1):
        d2 = k - d1 - 1  # -1 because edge u-v adds 1
        if 0 <= d2 <= k and d2 < len(child_cnt):
          total_pairs += cnt[d1] * child_cnt[d2]

      # Merge child counts (shifted by 1 for edge u-v)
      for d in range(k):
        if d < len(child_cnt):
          cnt[d + 1] += child_cnt[d]

    return cnt

  dfs(1, -1)
  print(total_pairs)

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
from collections import defaultdict, deque

def solve():
  n, k = map(int, input().split())

  adj = defaultdict(list)
  for _ in range(n - 1):
    a, b = map(int, input().split())
    adj[a].append(b)
    adj[b].append(a)

  result = 0

  # For each node as root, count paths of length k passing through it
  visited = [False] * (n + 1)

  def count_at_dist(start, parent, dist):
    """Count nodes at each distance from start"""
    counts = defaultdict(int)
    queue = deque([(start, 0)])

    while queue:
      node, d = queue.popleft()
      if d > k:
        continue
      counts[d] += 1

      for neighbor in adj[node]:
        if neighbor != parent and not visited[neighbor]:
          queue.append((neighbor, d + 1))

    return counts

  # Simple O(n * k) approach
  for root in range(1, n + 1):
    cnt = [0] * (k + 2)
    cnt[0] = 1

    for child in adj[root]:
      # Get distances in child subtree
      child_dist = defaultdict(int)
      stack = [(child, root, 1)]

      while stack:
        node, par, d = stack.pop()
        if d <= k:
          child_dist[d] += 1
          for nxt in adj[node]:
            if nxt != par:
              stack.append((nxt, node, d + 1))

      # Count pairs
      for d, c in child_dist.items():
        if k - d >= 0:
          result += cnt[k - d] * c

      # Merge
      for d, c in child_dist.items():
        if d <= k:
          cnt[d] += c

  print(result // 2)  # Each pair counted twice

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N × K) with tree DP
- **Space Complexity:** O(N × K) for DP arrays

##### Key Insight
For each node u, count paths of length k passing through u by combining distances from different subtrees. If one subtree has nodes at distance d from u, and another has nodes at distance k-d, they form pairs at distance k.

---

### Fill The Containers

#### Problem Information
- **Source:** UVa
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

A conveyor belt has a number of vessels of different capacities each filled to the brim with milk. The milk from conveyor belt is to be filled into 'm' containers. The constraints are:

1. Whenever milk from a vessel is poured into a container, the milk in the vessel must be completely poured into that container only. That is, milk from the same vessel cannot be poured into different containers.
2. The milk from the vessel must be poured into the container in order which they appear in the conveyor belt. That is, you cannot randomly pick up a vessel from the conveyor belt and fill the container.
3. The ith container must be filled with milk only from those vessels that appear earlier to those that fill jth container, for all i < j.

Given the number of containers 'm', you have to fill the containers with milk from all the vessels, without leaving any milk in the vessel. Your job is to find out the minimal possible capacity of the container which has maximal capacity.

#### Input Format
- Each test case consists of 2 lines.
- First line: n (1 ≤ n ≤ 1000) number of vessels and m (1 ≤ m ≤ 1000000) number of containers.
- Second line: capacity c (1 ≤ c ≤ 1000000) of each vessel in order.
- Multiple test cases terminated by EOF.

#### Output Format
For each test case, print the minimal possible capacity of the container with maximal capacity.

#### Solution

##### Approach
This is a classic binary search on answer problem. We binary search on the maximum container capacity and check if it's feasible to distribute all milk into m containers with that capacity.

- Lower bound: maximum single vessel capacity (can't split a vessel)
- Upper bound: sum of all vessels (one container takes all)

##### Python Solution

```python
def can_fill(vessels, max_capacity, m):
  """Check if we can fill all vessels into m containers with given max capacity"""
  containers_used = 1
  current_sum = 0

  for vessel in vessels:
    if vessel > max_capacity:
      return False

    if current_sum + vessel > max_capacity:
      containers_used += 1
      current_sum = vessel
      if containers_used > m:
        return False
    else:
      current_sum += vessel

  return True

def solve():
  import sys

  for line in sys.stdin:
    parts = line.split()
    n, m = int(parts[0]), int(parts[1])

    vessels = list(map(int, input().split()))

    # Binary search on maximum container capacity
    low = max(vessels)  # At minimum, need to fit largest vessel
    high = sum(vessels)  # At maximum, one container fits all

    result = high

    while low <= high:
      mid = (low + high) // 2

      if can_fill(vessels, mid, m):
        result = mid
        high = mid - 1
      else:
        low = mid + 1

    print(result)

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
def min_max_capacity(vessels, m):
  def feasible(capacity):
    containers = 1
    current = 0

    for v in vessels:
      if v > capacity:
        return False
      if current + v > capacity:
        containers += 1
        current = v
      else:
        current += v

    return containers <= m

  lo, hi = max(vessels), sum(vessels)

  while lo < hi:
    mid = (lo + hi) // 2
    if feasible(mid):
      hi = mid
    else:
      lo = mid + 1

  return lo

def solve():
  import sys
  lines = sys.stdin.read().strip().split('\n')
  i = 0

  while i < len(lines):
    n, m = map(int, lines[i].split())
    vessels = list(map(int, lines[i + 1].split()))
    print(min_max_capacity(vessels, m))
    i += 2

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n log S) where S is the sum of all vessel capacities
- **Space Complexity:** O(n) for storing vessel capacities

##### Key Insight
This is the "minimize the maximum" pattern, which is typically solved with binary search. The key insight is that if we can fill containers with a maximum capacity of X, we can definitely fill them with any capacity > X. This monotonicity allows binary search.

The check function greedily fills each container until it would overflow, then starts a new container. If we use more than m containers, the capacity is too small.

---

### Painting fence

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

Bizon the Champion isn't just attentive, he also is very hardworking.

Bizon the Champion decided to paint his old fence his favorite color, orange. The fence is represented as n vertical planks, put in a row. Adjacent planks have no gap between them. The planks are numbered from the left to the right starting from one, the i-th plank has the width of 1 meter and the height of ai meters.

Bizon the Champion bought a brush in the shop, the brush's width is 1 meter. He can make vertical and horizontal strokes with the brush. During a stroke the brush's full surface must touch the fence at all the time. What minimum number of strokes should Bizon the Champion do to fully paint the fence? Note that you are allowed to paint the same area of the fence multiple times.

#### Input Format
- The first line contains integer n (1 ≤ n ≤ 5000) - the number of fence planks.
- The second line contains n space-separated integers a1, a2, ..., an (1 ≤ ai ≤ 10^9).

#### Output Format
Print a single integer - the minimum number of strokes needed to paint the whole fence.

#### Solution

##### Approach
This is a classic divide and conquer problem. At each step, we have two choices:
1. **Vertical strokes**: Paint each plank vertically (costs = number of planks)
2. **Horizontal strokes**: Find the minimum height plank, paint horizontal strokes up to that height, then recursively solve for the remaining parts

Take the minimum of these two options.

##### Python Solution

```python
import sys
sys.setrecursionlimit(10000)

def min_strokes(arr, left, right, painted_height):
  if left > right:
    return 0

  # Find the plank with minimum height in range
  min_idx = left
  for i in range(left, right + 1):
    if arr[i] < arr[min_idx]:
      min_idx = i

  # Option 1: Paint all planks vertically
  vertical_strokes = right - left + 1

  # Option 2: Paint horizontally up to minimum height, then divide
  min_height = arr[min_idx]
  horizontal_strokes = (min_height - painted_height)  # Paint up to min height

  # Recursively solve for left and right parts
  horizontal_strokes += min_strokes(arr, left, min_idx - 1, min_height)
  horizontal_strokes += min_strokes(arr, min_idx + 1, right, min_height)

  return min(vertical_strokes, horizontal_strokes)

def solve():
  n = int(input())
  arr = list(map(int, input().split()))

  print(min_strokes(arr, 0, n - 1, 0))

if __name__ == "__main__":
  solve()
```

##### Optimized

```python
import sys
sys.setrecursionlimit(10000)

def build_segment_tree(arr, tree, node, start, end):
  if start == end:
    tree[node] = (arr[start], start)
  else:
    mid = (start + end) // 2
    build_segment_tree(arr, tree, 2*node, start, mid)
    build_segment_tree(arr, tree, 2*node+1, mid+1, end)
    tree[node] = min(tree[2*node], tree[2*node+1])

def query_min(tree, node, start, end, l, r):
  if r < start or end < l:
    return (float('inf'), -1)
  if l <= start and end <= r:
    return tree[node]
  mid = (start + end) // 2
  left_min = query_min(tree, 2*node, start, mid, l, r)
  right_min = query_min(tree, 2*node+1, mid+1, end, l, r)
  return min(left_min, right_min)

def min_strokes(arr, tree, n, left, right, painted_height):
  if left > right:
    return 0

  # Find minimum using segment tree
  min_val, min_idx = query_min(tree, 1, 0, n-1, left, right)

  # Option 1: Vertical strokes
  vertical = right - left + 1

  # Option 2: Horizontal strokes
  horizontal = (min_val - painted_height)
  horizontal += min_strokes(arr, tree, n, left, min_idx - 1, min_val)
  horizontal += min_strokes(arr, tree, n, min_idx + 1, right, min_val)

  return min(vertical, horizontal)

def solve():
  n = int(input())
  arr = list(map(int, input().split()))

  # Build segment tree for range minimum query
  tree = [(float('inf'), -1)] * (4 * n)
  build_segment_tree(arr, tree, 1, 0, n-1)

  print(min_strokes(arr, tree, n, 0, n - 1, 0))

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n²) for basic solution, O(n log n) with segment tree
- **Space Complexity:** O(n) for recursion stack

##### Key Insight
The divide and conquer works because after painting horizontal strokes up to the minimum height, the fence splits into independent subproblems that can be solved separately.

---

### The Closest Pair Problem

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

#### Problem Statement

Given a set of points in a two dimensional space, you will have to find the distance between the closest two points.

#### Input Format
- The input contains several testcases.
- Each testcase starts with an integer N (0 ≤ N ≤ 10000), which denotes the number of points in this test.
- The next N lines contain the coordinates of N two-dimensional points. The first of the two numbers denotes the X-coordinate and the latter denotes the Y-coordinate.
- The input is terminated by a test in which N = 0. This test should not be processed.
- The value of the coordinates will be less than 40000 and non-negative.

#### Output Format
For each test produce a single line of output containing a floating point number (with four digits after the decimal point) denoting the distance between the closest two points. If there is no such two points whose distance is less than 10000, print the line "INFINITY".

#### Solution

##### Approach
This is a classic divide and conquer problem:
1. Sort all points by x-coordinate
2. Divide the points into two halves
3. Recursively find the minimum distance in each half
4. Find the minimum distance across the dividing line (the strip)
5. For the strip, only consider points within distance d from the middle line, sorted by y-coordinate

##### Python Solution

```python
import math

def distance(p1, p2):
  return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def brute_force(points):
  min_dist = float('inf')
  n = len(points)
  for i in range(n):
    for j in range(i + 1, n):
      min_dist = min(min_dist, distance(points[i], points[j]))
  return min_dist

def strip_closest(strip, d):
  min_dist = d
  # Sort by y coordinate
  strip.sort(key=lambda p: p[1])

  n = len(strip)
  for i in range(n):
    j = i + 1
    while j < n and (strip[j][1] - strip[i][1]) < min_dist:
      min_dist = min(min_dist, distance(strip[i], strip[j]))
      j += 1

  return min_dist

def closest_pair(points):
  n = len(points)

  # Base case: use brute force for small sets
  if n <= 3:
    return brute_force(points)

  mid = n // 2
  mid_point = points[mid]

  # Recursively find minimum in left and right halves
  dl = closest_pair(points[:mid])
  dr = closest_pair(points[mid:])
  d = min(dl, dr)

  # Build strip of points within distance d from middle line
  strip = [p for p in points if abs(p[0] - mid_point[0]) < d]

  # Find closest points in strip
  return min(d, strip_closest(strip, d))

def solve():
  while True:
    n = int(input())
    if n == 0:
      break

    points = []
    for _ in range(n):
      x, y = map(float, input().split())
      points.append((x, y))

    # Sort by x coordinate
    points.sort(key=lambda p: p[0])

    if n < 2:
      print("INFINITY")
      continue

    result = closest_pair(points)

    if result < 10000:
      print(f"{result:.4f}")
    else:
      print("INFINITY")

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n log² n) - can be optimized to O(n log n)
- **Space Complexity:** O(n)

##### Key Insight
The clever observation is that for points in the strip, when sorted by y-coordinate, each point needs to be compared with at most 7 other points (due to geometric constraints). This keeps the strip processing linear.

---

### The closest two points

#### Problem Information
- **Source:** Classic Algorithm Problem
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

Given n points in a 2D plane, find the pair of points with the smallest Euclidean distance between them.

#### Input Format
- First line: n (number of points)
- Next n lines: x y coordinates of each point

#### Output Format
Output the minimum distance between any two points.

#### Solution

##### Approach
Use the classic Divide and Conquer algorithm:
1. Sort points by x-coordinate
2. Divide the points into two halves
3. Recursively find minimum distance in each half
4. Find minimum distance across the dividing line (strip region)
5. Return the overall minimum

The key insight is that we only need to check points within distance d of the dividing line, and for each such point, we only need to check at most 7 other points in the strip.

##### Python Solution

```python
import math

def distance(p1, p2):
  return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def brute_force(points):
  min_dist = float('inf')
  n = len(points)
  for i in range(n):
    for j in range(i + 1, n):
      min_dist = min(min_dist, distance(points[i], points[j]))
  return min_dist

def strip_closest(strip, d):
  min_dist = d
  # Sort by y coordinate
  strip.sort(key=lambda p: p[1])

  n = len(strip)
  for i in range(n):
    j = i + 1
    while j < n and (strip[j][1] - strip[i][1]) < min_dist:
      min_dist = min(min_dist, distance(strip[i], strip[j]))
      j += 1

  return min_dist

def closest_pair(points_sorted_x):
  n = len(points_sorted_x)

  # Base case
  if n <= 3:
    return brute_force(points_sorted_x)

  mid = n // 2
  mid_point = points_sorted_x[mid]

  # Divide
  left_half = points_sorted_x[:mid]
  right_half = points_sorted_x[mid:]

  # Conquer
  d_left = closest_pair(left_half)
  d_right = closest_pair(right_half)
  d = min(d_left, d_right)

  # Build strip
  strip = [p for p in points_sorted_x if abs(p[0] - mid_point[0]) < d]

  # Find closest in strip
  return strip_closest(strip, d)

def solve():
  n = int(input())
  points = []

  for _ in range(n):
    x, y = map(float, input().split())
    points.append((x, y))

  # Sort by x coordinate
  points.sort(key=lambda p: p[0])

  result = closest_pair(points)
  print(f"{result:.6f}")

if __name__ == "__main__":
  solve()
```

##### Optimized

```python
import math

def solve():
  n = int(input())
  points = []

  for _ in range(n):
    x, y = map(float, input().split())
    points.append((x, y))

  def dist(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

  def closest(px, py):
    n = len(px)

    if n <= 3:
      min_d = float('inf')
      for i in range(n):
        for j in range(i+1, n):
          min_d = min(min_d, dist(px[i], px[j]))
      return min_d

    mid = n // 2
    mid_x = px[mid][0]

    # Split py into left and right based on x coordinate
    pyl = [p for p in py if p[0] <= mid_x]
    pyr = [p for p in py if p[0] > mid_x]

    # Handle edge case where all points go to one side
    if len(pyl) == 0 or len(pyr) == 0:
      pyl = py[:mid]
      pyr = py[mid:]

    dl = closest(px[:mid], pyl)
    dr = closest(px[mid:], pyr)
    d = min(dl, dr)

    # Strip points sorted by y
    strip = [p for p in py if abs(p[0] - mid_x) < d]

    for i in range(len(strip)):
      j = i + 1
      while j < len(strip) and strip[j][1] - strip[i][1] < d:
        d = min(d, dist(strip[i], strip[j]))
        j += 1

    return d

  px = sorted(points, key=lambda p: p[0])
  py = sorted(points, key=lambda p: p[1])

  result = closest(px, py)
  print(f"{result:.6f}")

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n log n) - sorting plus divide and conquer
- **Space Complexity:** O(n) for storing sorted arrays

##### Key Insight
The divide and conquer approach works because:
1. The closest pair is either entirely in the left half, entirely in the right half, or spans both halves
2. For the spanning case, we only need to check a strip of width 2d around the dividing line
3. Within the strip, each point needs to be compared with at most 7 other points (geometric proof)

This reduces the naive O(n²) approach to O(n log n).

---

### Tree Summing

#### Problem Information
- **Source:** UVa
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 512MB

#### Problem Statement

LISP was one of the earliest high-level programming languages. Lists, which are the fundamental data structures in LISP, can easily be adapted to represent other important data structures such as trees.

Given a binary tree of integers, you are to write a program that determines whether there exists a root-to-leaf path whose nodes sum to a specified integer.

Binary trees are represented in the input file as LISP S-expressions having the following form:
- empty tree ::= ()
- tree ::= empty tree | (integer tree tree)

Example: `(5 (4 (11 (7 () ()) (2 () ())) ()) (8 (13 () ()) (4 () (1 () ()))))`

Note that with this formulation all leaves of a tree are of the form `(integer () ())`

#### Input Format
- The input consists of a sequence of test cases in the form of integer/tree pairs.
- Each test case consists of an integer followed by one or more spaces followed by a binary tree formatted as an S-expression.
- Expressions may be spread over several lines and may contain spaces.
- Input is terminated by end-of-file.

#### Output Format
For each pair I, T (I represents the integer, T represents the tree), output "yes" if there is a root-to-leaf path in T whose sum is I and "no" if there is no such path.

#### Solution

##### Approach
Parse the LISP S-expression and use recursion/stack to track the current path sum. When we encounter a leaf node (integer () ()), check if the sum equals the target.

##### Python Solution

```python
import sys

def solve():
  data = sys.stdin.read()
  idx = 0
  n = len(data)

  def skip_whitespace():
    nonlocal idx
    while idx < n and data[idx] in ' \t\n\r':
      idx += 1

  def parse_int():
    nonlocal idx
    skip_whitespace()
    negative = False
    if idx < n and data[idx] == '-':
      negative = True
      idx += 1
    num = 0
    while idx < n and data[idx].isdigit():
      num = num * 10 + int(data[idx])
      idx += 1
    return -num if negative else num

  def parse_tree(target, current_sum):
    """Returns True if there's a root-to-leaf path with sum = target"""
    nonlocal idx
    skip_whitespace()

    if idx >= n or data[idx] != '(':
      return False

    idx += 1  # Skip '('
    skip_whitespace()

    # Check for empty tree
    if data[idx] == ')':
      idx += 1
      return None  # Empty tree marker

    # Parse integer
    value = parse_int()
    current_sum += value

    # Parse left subtree
    left_result = parse_tree(target, current_sum)

    # Parse right subtree
    right_result = parse_tree(target, current_sum)

    skip_whitespace()
    idx += 1  # Skip ')'

    # If both children are empty (leaf node)
    if left_result is None and right_result is None:
      return current_sum == target

    # If one child is empty, check the other
    if left_result is None:
      return right_result
    if right_result is None:
      return left_result

    # Both children exist
    return left_result or right_result

  while idx < n:
    skip_whitespace()
    if idx >= n:
      break

    # Check if we have an integer (target)
    if data[idx].isdigit() or data[idx] == '-':
      target = parse_int()
      skip_whitespace()

      if idx >= n or data[idx] != '(':
        break

      # Check for empty tree
      result = parse_tree(target, 0)

      if result is None:
        print("no")  # Empty tree
      else:
        print("yes" if result else "no")
    else:
      idx += 1

if __name__ == "__main__":
  solve()
```

##### Alternative

```python
import sys
import re

def solve():
  data = sys.stdin.read()

  # Extract all tokens: integers and parentheses
  tokens = re.findall(r'-?\d+|\(|\)', data)

  i = 0
  while i < len(tokens):
    # Read target sum
    target = int(tokens[i])
    i += 1

    stack = []  # Stack of (value, null_count)
    current_sum = 0
    found = False

    while i < len(tokens):
      token = tokens[i]
      i += 1

      if token == '(':
        if i < len(tokens) and tokens[i] not in '()':
          # This is a node with a value
          value = int(tokens[i])
          i += 1
          stack.append((value, 0))
          current_sum += value
        else:
          # Empty tree marker
          if stack:
            val, null_count = stack[-1]
            stack[-1] = (val, null_count + 1)

      elif token == ')':
        if not stack:
          break  # End of tree

        val, null_count = stack[-1]

        if null_count >= 2:
          # This is a leaf node
          if current_sum == target:
            found = True

          # Pop this node
          stack.pop()
          current_sum -= val

          # Update parent's null count
          if stack:
            parent_val, parent_null = stack[-1]
            stack[-1] = (parent_val, parent_null + 1)
        else:
          # Not enough children processed yet
          pass

    print("yes" if found else "no")

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N) where N is the length of the input string
- **Space Complexity:** O(H) where H is the height of the tree (for recursion stack)

##### Key Insight
The main challenge is parsing the LISP S-expression correctly. A leaf node is identified when both its children are empty trees `()`. Only at leaf nodes do we check if the accumulated sum equals the target.

---

### Tricky Function

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 512MB

#### Problem Statement

You're given a 1-based array `a` with n elements. Let's define function `f(i, j)` (1 ≤ i, j ≤ n) as:

```
f(i, j) = (i - j)² + g(i, j)²
```

Function `g` is calculated by the following pseudo-code:

```
int g(int i, int j) {
    int sum = 0;
    for (int k = min(i, j) + 1; k <= max(i, j); k = k + 1)
        sum = sum + a[k];
    return sum;
}
```

Find the minimum value of `f(i, j)` where i ≠ j.

#### Input Format
- First line: integer n (2 ≤ n ≤ 100000)
- Second line: n integers a₁, a₂, ..., aₙ (-10⁴ ≤ aᵢ ≤ 10⁴)

#### Output Format
Output a single integer - the minimum value of f(i, j) where i ≠ j.

#### Solution

##### Approach
The key insight is that `g(i, j)` is the sum of elements between indices i and j. Using prefix sums:
- `g(i, j) = prefix[max(i,j)] - prefix[min(i,j)]`

So `f(i, j) = (i - j)² + (prefix[j] - prefix[i])²`

This is exactly the squared Euclidean distance between points (i, prefix[i]) and (j, prefix[j])!

Therefore, this problem reduces to the **Closest Pair of Points** problem, which can be solved in O(n log n) using divide and conquer.

##### Python Solution

```python
import sys
sys.setrecursionlimit(200000)

def solve():
  n = int(input())
  a = list(map(int, input().split()))

  # Create points (index, prefix_sum)
  prefix = [0] * (n + 1)
  for i in range(n):
    prefix[i + 1] = prefix[i] + a[i]

  # Points are (i, prefix[i]) for i = 1 to n
  points = [(i, prefix[i]) for i in range(1, n + 1)]

  def dist_sq(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

  def brute_force(pts):
    min_d = float('inf')
    for i in range(len(pts)):
      for j in range(i + 1, len(pts)):
        min_d = min(min_d, dist_sq(pts[i], pts[j]))
    return min_d

  def closest_pair(pts):
    if len(pts) <= 3:
      return brute_force(pts)

    mid = len(pts) // 2
    mid_x = pts[mid][0]

    left = pts[:mid]
    right = pts[mid:]

    d_left = closest_pair(left)
    d_right = closest_pair(right)
    d = min(d_left, d_right)

    # Build strip
    strip = [p for p in pts if (p[0] - mid_x) ** 2 < d]
    strip.sort(key=lambda p: p[1])  # Sort by y (prefix sum)

    # Check strip
    for i in range(len(strip)):
      j = i + 1
      while j < len(strip) and (strip[j][1] - strip[i][1]) ** 2 < d:
        d = min(d, dist_sq(strip[i], strip[j]))
        j += 1

    return d

  # Sort by x coordinate
  points.sort()

  print(closest_pair(points))

if __name__ == "__main__":
  solve()
```

##### Optimized

```python
def solve():
  n = int(input())
  a = list(map(int, input().split()))

  # Build prefix sums
  prefix = [0]
  for x in a:
    prefix.append(prefix[-1] + x)

  # Points: (x=index, y=prefix_sum)
  points = list(range(n + 1))  # indices 0 to n

  def dist(i, j):
    dx = i - j
    dy = prefix[i] - prefix[j]
    return dx * dx + dy * dy

  def closest(indices):
    if len(indices) <= 3:
      min_d = float('inf')
      for i in range(len(indices)):
        for j in range(i + 1, len(indices)):
          min_d = min(min_d, dist(indices[i], indices[j]))
      return min_d

    mid = len(indices) // 2
    mid_x = indices[mid]

    d = min(closest(indices[:mid]), closest(indices[mid:]))

    # Merge step
    strip = [i for i in indices if (i - mid_x) ** 2 < d]
    strip.sort(key=lambda i: prefix[i])

    for i in range(len(strip)):
      for j in range(i + 1, len(strip)):
        if (prefix[strip[j]] - prefix[strip[i]]) ** 2 >= d:
          break
        d = min(d, dist(strip[i], strip[j]))

    return d

  # Sort indices by x coordinate (which is just the index itself)
  points.sort()

  # We need i != j, and since points start from 0, we use indices 1 to n
  points = list(range(1, n + 1))
  print(closest(points))

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n log² n) due to sorting in each merge step, can be optimized to O(n log n)
- **Space Complexity:** O(n) for storing points and recursion stack

##### Key Insight
The brilliant observation is that `f(i, j)` represents the squared Euclidean distance between two points in a 2D plane where:
- x-coordinate = index i
- y-coordinate = prefix sum up to index i

This transforms the problem into the classical "Closest Pair of Points" problem, solvable efficiently using divide and conquer.

