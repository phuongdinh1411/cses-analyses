---
layout: simple
title: "Dynamic Array"
permalink: /problem_soulutions/Blue/Session 01 - Dynamic Array/
---

# Dynamic Array

This session covers dynamic array fundamentals, including array manipulation, indexing, and basic operations on arrays.

## Problems

### Jacket

#### Problem Information
- **Source:** [Codeforces 691A](https://codeforces.com/problemset/problem/691/A)
- **Difficulty:** Easy
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

A jacket has n buttons arranged in a row. Each button is either fastened (1) or unfastened (0). A jacket is considered "properly fastened" if:
- When n = 1: the button must be fastened
- When n > 1: exactly one button must be unfastened

#### Input Format
- Line 1: Integer n (number of buttons)
- Line 2: n integers (0 or 1)

#### Output Format
"YES" if properly fastened, "NO" otherwise

#### Solution

##### Approach
Count the number of unfastened buttons. For n=1, check if the single button is fastened. For n>1, verify exactly one button is unfastened.

##### Python Solution

```python
def solve():
  n = int(input())
  a = list(map(int, input().split()))

  unfastened = sum(1 - x for x in a)

  if n == 1:
    print("YES" if a[0] == 1 else "NO")
  else:
    print("YES" if unfastened == 1 else "NO")

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n)
- **Space Complexity:** O(n)

---

### Vanya and Fence

#### Problem Information
- **Source:** [Codeforces 677A](https://codeforces.com/problemset/problem/677/A)
- **Difficulty:** Easy
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Vanya and his n friends want to pass under a fence of height h. Each friend has a height a[i]. If a friend's height <= h, they walk normally (width 1). If taller, they must bend sideways (width 2). Calculate the total road width needed for all friends to pass.

#### Input Format
- Line 1: n h (number of friends, fence height)
- Line 2: n integers (heights of friends)

#### Output Format
Total road width needed

#### Solution

##### Approach
For each friend, add 1 to width if height <= h, otherwise add 2. Simple linear scan.

##### Python Solution

```python
def solve():
  n, h = map(int, input().split())
  a = list(map(int, input().split()))

  road_width = sum(1 if ai <= h else 2 for ai in a)
  print(road_width)

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n)
- **Space Complexity:** O(n)

---

### Big Segment

#### Problem Information
- **Source:** [Codeforces 242B](https://codeforces.com/problemset/problem/242/B)
- **Difficulty:** Easy
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given n segments [l[i], r[i]], find if there exists a segment that completely covers all other segments (i.e., its left endpoint is the minimum of all left endpoints AND its right endpoint is the maximum of all right endpoints). If such a segment exists, output its 1-based index. Otherwise, output -1.

#### Input Format
- Line 1: Integer n (number of segments)
- Next n lines: l[i] r[i] (left and right endpoints of segment i)

#### Output Format
Index of the covering segment (1-based), or -1 if none exists

#### Solution

##### Approach
Track the global minimum left endpoint and maximum right endpoint. Then find if any segment has both these values.

##### Python Solution

```python
def solve():
  n = int(input())
  segments = []
  for _ in range(n):
    l, r = map(int, input().split())
    segments.append((l, r))

  min_left = min(s[0] for s in segments)
  max_right = max(s[1] for s in segments)

  for i, (l, r) in enumerate(segments):
    if l == min_left and r == max_right:
      print(i + 1)
      return

  print(-1)

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n)
- **Space Complexity:** O(n)

---

### Arrays

#### Problem Information
- **Source:** [Codeforces 572A](https://codeforces.com/problemset/problem/572/A)
- **Difficulty:** Easy
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given two sorted arrays a (size na) and b (size nb) in non-decreasing order, check if ALL of the first k elements of array a are strictly less than ALL of the last m elements of array b.

#### Input Format
- Line 1: na nb (sizes of arrays)
- Line 2: k m (number of elements to consider from each array)
- Line 3: Array a (na integers, sorted non-decreasing)
- Line 4: Array b (nb integers, sorted non-decreasing)

#### Output Format
"YES" if condition is satisfied, "NO" otherwise

#### Solution

##### Approach
Since arrays are sorted, just compare a[k-1] (max of first k) with b[nb-m] (min of last m).

##### Python Solution

```python
def solve():
  na, nb = map(int, input().split())
  k, m = map(int, input().split())
  a = list(map(int, input().split()))
  b = list(map(int, input().split()))

  print("YES" if a[k - 1] < b[-m] else "NO")

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n) for input, O(1) for comparison
- **Space Complexity:** O(n)

---

### Bear and Game

#### Problem Information
- **Source:** [Codeforces 673A](https://codeforces.com/problemset/problem/673/A)
- **Difficulty:** Easy
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

A bear watches a 90-minute football game on TV. There are n interesting moments at times t[1], t[2], ..., t[n] (in increasing order). The bear turns off the TV if more than 15 consecutive minutes pass without any interesting moment. Determine at what minute he stops watching.

#### Input Format
- Line 1: Integer n (number of interesting moments)
- Line 2: n integers t[i] (times of interesting moments, 1 <= t[i] <= 90)

#### Output Format
The minute when the bear stops watching

#### Solution

##### Approach
Check gaps between consecutive interesting moments. If any gap exceeds 15 minutes, the bear stops 15 minutes after the previous moment.

##### Python Solution

```python
def solve():
  n = int(input())
  t = list(map(int, input().split()))

  if t[0] > 15:
    print(15)
    return

  for i in range(1, n):
    if t[i] - t[i - 1] > 15:
      print(t[i - 1] + 15)
      return

  if 90 - t[n - 1] > 15:
    print(t[n - 1] + 15)
  else:
    print(90)

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n)
- **Space Complexity:** O(n)

---

### Semifinals

#### Problem Information
- **Source:** [Codeforces 378B](https://codeforces.com/problemset/problem/378/B)
- **Difficulty:** Medium
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Two semifinals of a race, each with n participants. The top n participants overall (by finish time) will qualify for the finals. For each position in each semifinal, determine if that racer has a chance to qualify (1) or definitely won't qualify (0).

#### Input Format
- Line 1: Integer n (participants per semifinal)
- Next n lines: a[i] b[i] (finish times for position i in semifinals A and B)

#### Output Format
Two lines of n characters each (0 or 1), representing qualification chances for each position in semifinal A and B respectively

#### Solution

##### Approach
The first ceil(n/2) from each semifinal are guaranteed to qualify. The remaining spots depend on cross-semifinal comparisons.

##### Python Solution

```python
def solve():
  n = int(input())
  a, b = [], []
  for _ in range(n):
    ai, bi = map(int, input().split())
    a.append(ai)
    b.append(bi)

  k = n // 2
  chances = [[1] * k + [0] * (n - k) for _ in range(2)]

  last_a = k - 1
  last_b = k - 1

  if n % 2 == 1:
    if a[k] < b[k]:
      last_a += 1
      chances[0][k] = 1
    else:
      last_b += 1
      chances[1][k] = 1

  while last_a < n - 1 and last_b < n - 1:
    if a[last_a + 1] < b[n - (last_a + 1) - 1]:
      last_a += 1
      chances[0][last_a] = 1
    elif b[last_b + 1] < a[n - (last_b + 1) - 1]:
      last_b += 1
      chances[1][last_b] = 1
    else:
      break

  print(''.join(map(str, chances[0])))
  print(''.join(map(str, chances[1])))

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n)
- **Space Complexity:** O(n)

---

### Nicholas and Permutation

#### Problem Information
- **Source:** [Codeforces 676A](https://codeforces.com/problemset/problem/676/A)
- **Difficulty:** Easy
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given a permutation of integers 1 to n, you can perform at most one swap of any two elements. Find the maximum possible distance between the positions of elements 1 and n after the swap.

#### Input Format
- Line 1: Integer n
- Line 2: A permutation of integers 1 to n

#### Output Format
Maximum achievable distance between positions of 1 and n

#### Solution

##### Approach
You can move either 1 or n to an endpoint (position 0 or n-1) to maximize distance. Check all 4 possibilities.

##### Python Solution

```python
def solve():
  n = int(input())
  a = list(map(int, input().split()))

  pos_min = a.index(1)
  pos_max = a.index(n)

  result = max(n - 1 - pos_max, n - 1 - pos_min, pos_max, pos_min)
  print(result)

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n)
- **Space Complexity:** O(n)

---

### The Best Gift

#### Problem Information
- **Source:** [Codeforces 609B](https://codeforces.com/problemset/problem/609/B)
- **Difficulty:** Easy
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

#### Problem Statement

There are n books of m different genres. Tanya wants to choose 2 books of DIFFERENT genres as a gift. Count the number of ways to choose such a pair.

#### Input Format
- Line 1: n m (number of books, number of genres)
- Line 2: n integers (genre of each book, values from 1 to m)

#### Output Format
Number of ways to choose 2 books of different genres

#### Solution

##### Approach
Count books per genre, then sum count[i] * count[j] for all pairs i < j.

##### Python Solution

```python
def solve():
  n, m = map(int, input().split())
  a = list(map(int, input().split()))

  genre_count = [0] * m
  for genre in a:
    genre_count[genre - 1] += 1

  total = 0
  for i in range(m - 1):
    for j in range(i + 1, m):
      total += genre_count[i] * genre_count[j]

  print(total)

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n + m^2)
- **Space Complexity:** O(m)

---

### Balls Game

#### Problem Information
- **Source:** [Codeforces 430B](https://codeforces.com/problemset/problem/430/B)
- **Difficulty:** Medium
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

A row of n colored balls is arranged in a line. You have one ball of color x that you can insert between any two adjacent balls of the same color as x. When k or more consecutive balls of the same color form, they are destroyed. Chain reactions can occur. Find the maximum number of balls you can destroy.

#### Input Format
- Line 1: n k x (number of balls, threshold for destruction, your ball's color)
- Line 2: n integers (colors of balls in the row)

#### Output Format
Maximum number of balls that can be destroyed

#### Solution

##### Approach
Try inserting between each pair of adjacent x-colored balls, simulate chain reactions recursively.

##### Python Solution

```python
def solve():
  n, k, x = map(int, input().split())
  c = list(map(int, input().split()))

  def destroy_balls(a, b, target):
    if len(a) == 0 or len(b) == 0:
      return 0

    if a[-1] != b[0]:
      return 0

    to_destroy = 2
    a_idx = len(a) - 2
    b_idx = 1

    while a_idx >= 0 and a[a_idx] == target:
      to_destroy += 1
      a_idx -= 1

    while b_idx < len(b) and b[b_idx] == target:
      to_destroy += 1
      b_idx += 1

    if to_destroy > 2:
      new_target = a[a_idx] if a_idx >= 0 else None
      return to_destroy + destroy_balls(a[:a_idx + 1], b[b_idx:], new_target)

    return 0

  max_destroyed = 0

  for i in range(n - 1):
    if c[i] == x and c[i] == c[i + 1]:
      left = c[:i + 1] + [x]
      right = c[i + 1:]
      destroyed = destroy_balls(left, right, x)
      max_destroyed = max(max_destroyed, destroyed)

  if max_destroyed >= 2:
    max_destroyed -= 1
  else:
    max_destroyed = 0

  print(max_destroyed)

if __name__ == "__main__":
  solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n^2) in worst case due to simulation
- **Space Complexity:** O(n)

---
