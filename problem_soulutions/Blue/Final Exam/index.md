---
layout: simple
title: "Final Exam"
permalink: /problem_soulutions/Blue/Final Exam/
---

# Final Exam

This section contains final examination problems covering all topics from the B course curriculum.

## Problems

### Three Distinct Permutations

#### Problem Information
- **Source:** B Course
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given an array of N integers, determine if it is possible to create at least 3 distinct permutations that, when sorted by values, produce different index mappings. If possible, output "YES" and print 3 such permutations; otherwise output "NO".

The key insight is that we need duplicate values in the array to create different permutations:
- If a value appears exactly 2 times, we can swap their positions (2 arrangements)
- If a value appears 3+ times, we get more arrangements
- To get 3 distinct permutations, we need either:
  - One value appearing 4+ times (can create 3+ arrangements from one value)
  - Two values each appearing exactly 2 times (2 * 2 = 4 >= 3 arrangements)

#### Input Format
- Line 1: Integer N (size of array)
- Line 2: N space-separated integers (the array elements)

#### Output Format
- If not possible: "NO"
- If possible: "YES" followed by 3 lines, each containing a permutation (1-indexed positions that would sort the array)

#### Solution

##### Approach
1. Track positions of each unique value using a dictionary
2. Check if conditions for 3 permutations are met:
   - Two values with exactly 2 occurrences each, OR
   - One value with 4+ occurrences
3. Generate permutations by swapping positions of duplicate values

##### Python Solution

```python
def solution():
 N = int(input())
 tasks = list(map(int, input().split()))
 markers = {}

 for i in range(N):
  if markers.get(tasks[i]) is None:
   markers[tasks[i]] = [1]
  markers[tasks[i]].append(i)

 possible = False
 possible_count = 1

 duplications = []
 duplicated_keys = []
 for key, marker in markers.items():
  if len(marker) == 3:
   possible_count *= 2
   duplications.append(marker)
   duplicated_keys.append(key)
   if possible_count >= 3:
    possible = True
    break

  elif len(marker) >= 4:
   possible = True
   duplications = [marker]
   duplicated_keys = [key]
   break

 if not possible:
  print('NO')
  return

 print('YES')
 tasks.sort()

 if len(duplications) == 2:
  for i in range(N):
   print(markers[tasks[i]][markers[tasks[i]][0]] + 1, end=' ')
   if markers[tasks[i]][0] == len(markers[tasks[i]]) - 1:
    markers[tasks[i]][0] = 1
   else:
    markers[tasks[i]][0] += 1
  markers[duplicated_keys[0]][2], markers[duplicated_keys[0]][1] = markers[duplicated_keys[0]][1], \
                  markers[duplicated_keys[0]][2]

  for marker in markers.values():
   marker[0] = 1
  print()
  for i in range(N):
   print(markers[tasks[i]][markers[tasks[i]][0]] + 1, end=' ')
   if markers[tasks[i]][0] == len(markers[tasks[i]]) - 1:
    markers[tasks[i]][0] = 1
   else:
    markers[tasks[i]][0] += 1
  for marker in markers.values():
   marker[0] = 1
  print()

  markers[duplicated_keys[1]][2], markers[duplicated_keys[1]][1] = markers[duplicated_keys[1]][1], \
                  markers[duplicated_keys[1]][2]

  for i in range(N):
   print(markers[tasks[i]][markers[tasks[i]][0]] + 1, end=' ')
   if markers[tasks[i]][0] == len(markers[tasks[i]]) - 1:
    markers[tasks[i]][0] = 1
   else:
    markers[tasks[i]][0] += 1

 if len(duplications) == 1:
  for i in range(N):
   print(markers[tasks[i]][markers[tasks[i]][0]] + 1, end=' ')
   if markers[tasks[i]][0] == len(markers[tasks[i]]) - 1:
    markers[tasks[i]][0] = 1
   else:
    markers[tasks[i]][0] += 1

  print()
  for marker in markers.values():
   marker[0] = 1
  markers[duplicated_keys[0]][2], markers[duplicated_keys[0]][1] = markers[duplicated_keys[0]][1], \
                  markers[duplicated_keys[0]][2]

  for i in range(N):
   print(markers[tasks[i]][markers[tasks[i]][0]] + 1, end=' ')
   if markers[tasks[i]][0] == len(markers[tasks[i]]) - 1:
    markers[tasks[i]][0] = 1
   else:
    markers[tasks[i]][0] += 1

  print()
  for marker in markers.values():
   marker[0] = 1
  markers[duplicated_keys[0]][2], markers[duplicated_keys[0]][3] = markers[duplicated_keys[0]][3], \
                  markers[duplicated_keys[0]][2]

  for i in range(N):
   print(markers[tasks[i]][markers[tasks[i]][0]] + 1, end=' ')
   if markers[tasks[i]][0] == len(markers[tasks[i]]) - 1:
    markers[tasks[i]][0] = 1
   else:
    markers[tasks[i]][0] += 1


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(N log N) for sorting
- **Space Complexity:** O(N) for storing markers

---

### Spiral Matrix Coordinates

#### Problem Information
- **Source:** B Course
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Imagine an infinite grid where cells are numbered starting from (1,1) in a diagonal spiral pattern. Given a cell number, find its (x, y) coordinates.

The pattern follows a diagonal spiral:
- Start at (1,1) = cell 1
- Move diagonally, filling cells in a pattern where perfect squares mark corners
- Odd perfect squares are at (k,1), even perfect squares are at (1,k)

For example:
- Cell 1 -> (1,1)
- Cell 2 -> (2,1)
- Cell 3 -> (1,2)
- Cell 4 -> (2,2)
- Cell 5 -> (1,3)

#### Input Format
- Line 1: Integer T (number of test cases)
- Next T lines: Each contains a single integer representing the cell number

#### Output Format
For each test case: "Case X: x y" where (x, y) are the coordinates.

#### Solution

##### Approach
1. Find the smallest perfect square >= given number: sqrt = ceil(sqrt(n))
2. Calculate remainder r = sqrt^2 - n
3. Determine position based on remainder and whether sqrt is odd/even:
   - If r < sqrt: coordinates are (sqrt, r+1) or (r+1, sqrt)
   - Otherwise: calculate offset from the corner
4. Swap x,y if sqrt is odd (alternating diagonal directions)

##### Python Solution

```python
import math


def solution():
 T = int(input())

 for i in range(T):
  second = int(input())

  sqrt = math.ceil(math.sqrt(second))
  r = sqrt * sqrt - second
  if r < sqrt:
   y = r + 1
   x = sqrt
  else:
   x = 2 * sqrt - r - 1
   y = sqrt

  if sqrt % 2 == 1:
   x, y = y, x

  print("Case {0}: {1} {2}".format(i + 1, x, y))


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(1) per query
- **Space Complexity:** O(1)

---

### Religion Groups

#### Problem Information
- **Source:** B Course
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

In a group of N people, some share the same religious beliefs. If person X and person Y share the same religion, they belong to the same religious group. Given M pairs of people who share the same religion, count the total number of distinct religious groups.

This is essentially counting the number of connected components in an undirected graph where nodes are people and edges represent shared religious beliefs.

#### Input Format
- Multiple test cases, each starting with: N M (N = number of people, M = number of pairs)
- Next M lines: X Y (person X and Y share the same religion)
- Input ends when N = 0 and M = 0

#### Output Format
For each test case: "Case T: K" where T is the case number and K is the number of distinct religious groups (connected components).

#### Solution

##### Approach
1. Use Union-Find (Disjoint Set Union) data structure with:
   - Path compression in find_set() for efficiency
   - Union by rank for balanced trees
2. For each pair (X, Y), union their sets
3. Count unique root parents to get number of connected components

##### Python Solution

```python
parent = []
ranks = []


def make_set(N):
 global parent, ranks
 parent = [i for i in range(N + 5)]
 ranks = [0 for i in range(N + 5)]


def find_set(u):
 if parent[u] != u:
  parent[u] = find_set(parent[u])
 return parent[u]


def union_set(u, v):
 up = find_set(u)
 vp = find_set(v)

 if up == vp:
  return
 if ranks[up] > ranks[vp]:
  parent[vp] = up
 elif ranks[up] < ranks[vp]:
  parent[up] = vp
 else:
  parent[up] = vp
  ranks[vp] += 1


def has_same_opinion(opinions1, opinions2, length):
 for i in range(length):
  if opinions1[i] != opinions2[i]:
   return False
 return True


def solution():
 t = 1
 while True:
  n, m = map(int, input().split())
  if m == 0 and n == 0:
   break

  make_set(n)

  for i in range(m):
   x, y = map(int, input().split())
   union_set(x, y)

  religion_leaders = dict()

  for i in range(1, n + 1):
   leader = find_set(i)
   if religion_leaders.get(leader) is not None:
    religion_leaders[leader] += 1
   else:
    religion_leaders[leader] = 1

  print("Case {0}: {1}".format(t, len(religion_leaders)))
  t += 1


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(M * alpha(N)) where alpha is inverse Ackermann function
- **Space Complexity:** O(N)

---

### Connecting Freckles

#### Problem Information
- **Source:** B Course
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given N points (freckles) on a 2D plane with their (x, y) coordinates, find the minimum total length of ink needed to connect all freckles. You can connect any two freckles with a straight line, and the goal is to connect all freckles using minimum total distance.

This is the classic Minimum Spanning Tree (MST) problem where:
- Nodes are the freckle positions
- Edge weights are Euclidean distances between points
- We need to find a tree connecting all nodes with minimum total edge weight

#### Input Format
- Line 1: Integer N (number of test cases)
- For each test case:
  - Blank line
  - Integer: number of freckles
  - Next lines: x y coordinates (floating point) for each freckle

#### Output Format
- For each test case: The minimum total distance (2 decimal places)
- Blank line between test cases

#### Solution

##### Approach
1. Build a complete graph where each pair of freckles has an edge with weight = Euclidean distance
2. Apply Kruskal's algorithm:
   - Sort all edges by weight
   - Use Union-Find to avoid cycles
   - Add edges to MST until (V-1) edges are selected
3. Return the sum of edge weights in the MST

##### Python Solution

```python
import math


class Triad:
 def __init__(self, source, target, weight):
  self.source = source
  self.target = target
  self.weight = weight

 def __repr__(self):
  return str(self.source) + '-' + str(self.target) + ': ' + str(self.weight)


parent = []
ranks = []
dist = []
graph = []


def make_set(V):
 global parent, ranks, dist
 parent = [i for i in range(V + 1)]
 ranks = [0 for _ in range(V + 1)]


def find_set(u):
 if parent[u] != u:
  parent[u] = find_set(parent[u])
 return parent[u]


def union_set(u, v):
 up = find_set(u)
 vp = find_set(v)
 if up == vp:
  return
 if ranks[up] > ranks[vp]:
  parent[vp] = up
 elif ranks[up] < ranks[vp]:
  parent[up] = vp
 else:
  parent[up] = vp
  ranks[vp] += 1


def kruskal(number_of_cities):
 graph.sort(key=lambda _edge: _edge.weight)
 i = 0
 mst = 0
 while len(dist) != number_of_cities - 1 and i < len(graph):
  edge = graph[i]
  i += 1
  u = find_set(edge.source)
  v = find_set(edge.target)
  if u != v:
   dist.append(edge)
   union_set(u, v)
   mst += edge.weight

 return mst


def calculate_distance(freckle1, freckle2):
 x1, y1 = freckle1
 x2, y2 = freckle2
 return math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))


def solution():
 N = int(input())
 for t in range(N):
  input()
  global graph, dist
  graph = []
  dist = []
  freckles_number = int(input())
  freckles = []

  for i in range(freckles_number):
   x, y = map(float, input().split())
   freckles.append((x, y))

  for i in range(freckles_number):
   for j in range(i + 1, freckles_number):
    graph.append(Triad(i, j, calculate_distance(freckles[i], freckles[j])))

  make_set(freckles_number)

  print('%.2f' % kruskal(freckles_number))
  if t != N - 1:
   print()


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(N^2 log N) for building and sorting edges
- **Space Complexity:** O(N^2) for storing all edges

---

### Phone List Consistency

#### Problem Information
- **Source:** B Course
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given a list of phone numbers, determine if the list is "consistent" - meaning no phone number is a prefix of another phone number. For example, if the list contains both "911" and "9111234", it is inconsistent because "911" is a prefix of "9111234".

This problem is also known as:
- Phone List (UVa)
- Consistent Phone Numbers
- Prefix-Free Code Validation

#### Input Format
- Line 1: Integer T (number of test cases)
- For each test case:
  - Line 1: Integer N (number of phone numbers)
  - Next N lines: One phone number string per line

#### Output Format
For each test case: "YES" if the list is consistent (no prefix conflicts), "NO" otherwise.

#### Solution

##### Approach
1. Use a Trie (prefix tree) data structure
2. For each phone number, insert it into the trie character by character
3. While inserting, check for prefix conflicts:
   - If we pass through a node marked as end of a word -> current number has a prefix in the set
   - If we reach the end but the node has children -> current number is a prefix of another
4. If any conflict is found, output "NO"; otherwise "YES"

##### Python Solution

```python
class Node:
 def __init__(self):
  self.countWord = 0
  self.child = dict()


def add_word(root, s):
 tmp = root
 for ch in s:
  if ch not in tmp.child:
   tmp.child[ch] = Node()
  tmp = tmp.child[ch]
  if tmp.countWord > 0:
   return False

 if len(tmp.child) > 0:
  return False
 tmp.countWord += 1
 return True


def solution():
 tc = int(input())
 for t in range(tc):
  root = Node()
  n = int(input())
  duplicated = False
  for i in range(n):
   s = input()
   result = add_word(root, s)
   if not result:
    print('NO')
    duplicated = True
    break
  if not duplicated:
   print('YES')


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(N * L) where L is the average phone number length
- **Space Complexity:** O(N * L) for Trie storage
