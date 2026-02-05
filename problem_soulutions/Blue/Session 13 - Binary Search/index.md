---
layout: simple
title: "Binary Search"
permalink: /problem_soulutions/Blue/Session 13 - Binary Search/
---

# Binary Search

This session covers binary search algorithm and its applications, including search on sorted arrays and binary search on answer.

## Problems

### Neko does Maths

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given two positive integers a and b, find the smallest non-negative integer k such that LCM(a+k, b+k) is minimized. LCM is the Least Common Multiple.

#### Input Format
- Single line with two integers a and b

#### Output Format
- Single integer k that minimizes LCM(a+k, b+k)

#### Solution

##### Approach
Key insight: GCD(a+k, b+k) = GCD(a+k, |b-a|) = GCD(b+k, |b-a|). The GCD must be a divisor of |a-b|. Iterate through all divisors of |a-b| (up to sqrt(|a-b|)). For each divisor d, find smallest k such that (a+k) % d == 0. Track the k that gives minimum LCM.

##### Python Solution

```python
from math import sqrt

INF = 1e18


def gcd(x, y):
 if y == 0:
  return x
 else:
  return gcd(y, x % y)


def solution():
 atmp, btmp = map(int, input().strip().split())
 a = max(atmp, btmp)
 b = min(atmp, btmp)
 k = 0

 delta = a - b
 min_lcm = INF

 if delta == 0:
  print(0)
  exit(0)

 range_gcd = int(sqrt(delta)) + 1
 for i in range(1, range_gcd):
  if delta % i == 0:
   k, min_lcm = getk(a, b, i, k, min_lcm)
   k, min_lcm = getk(a, b, delta / i, k, min_lcm)

 print('{0:.0f}'.format(k))


def getk(a, b, i, k, min_lcm):
 current_k = 0
 if b % i > 0:
  current_k = ((b // i) + 1) * i - b
 lcm = (a + current_k) * (b + current_k) / i
 if lcm < min_lcm:
  min_lcm = lcm
  k = current_k
 return k, min_lcm


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(sqrt(|a-b|))
- **Space Complexity:** O(1)

---

### Energy Exchange

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

There are n accumulators with different energy levels. Energy can be transferred between accumulators, but k% is lost during transfer. Find the maximum equal energy level all accumulators can achieve.

#### Input Format
- First line: n k (number of accumulators, loss percentage)
- Second line: n integers (initial energy levels of accumulators)

#### Output Format
- Maximum energy level achievable for all accumulators (with 9 decimal precision)

#### Solution

##### Approach
Binary search on the answer (target energy level). For a given target, calculate energy needed by accumulators below target. Calculate energy available from accumulators above target (accounting for k% loss). Target is achievable if available energy >= needed energy.

##### Python Solution

```python
def check_possibility(_accumulators, max_value, n, k):
 less = 0
 more = 0
 for i in range(n):
  if _accumulators[i] > max_value:
   more += _accumulators[i] - max_value
  else:
   less += max_value - _accumulators[i]

 return more - k * more / 100 >= less


def solution():
 n, k = map(int, input().strip().split())
 accumulators = list(map(int, input().strip().split()))

 lo = 0
 hi = 1000
 for i in range(100):
  mid = (lo + hi) / 2
  if check_possibility(accumulators, mid, n, k):
   lo = mid
  else:
   hi = mid

 print('{0:.9f}'.format(lo))


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(100 * n) = O(n) with 100 binary search iterations
- **Space Complexity:** O(n)

---

### Eko

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 1536MB

#### Problem Statement

A woodcutter needs to collect at least M meters of wood. He sets a saw height H and cuts all trees taller than H. The wood collected from each tree is (tree_height - H) if tree_height > H, otherwise 0. Find the maximum H such that at least M meters of wood is collected.

#### Input Format
- First line: N M (number of trees, required wood)
- Second line: N integers (heights of trees)

#### Output Format
- Maximum integer height H to collect at least M meters of wood

#### Solution

##### Approach
Binary search on the answer (saw height H). For a given height, calculate total wood collected. If total >= M, try higher H (to maximize H). If total < M, try lower H.

##### Python Solution

```python
def check_possibility(_accumulators, max_value, n, k):

 total = 0
 for i in range(n):
  if _accumulators[i] > max_value:
   total += _accumulators[i] - max_value

 return total >= k


def solution():
 n, k = map(int, input().strip().split())
 trees = list(map(int, input().strip().split()))

 lo = 0
 hi = int(2e9)
 while lo < hi - 1:
  mid = (lo + hi) // 2
  if check_possibility(trees, mid, n, k):
   lo = mid
  else:
   hi = mid

 print(lo)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n * log(max_height))
- **Space Complexity:** O(n)

---

### Hacking the Random Number Generator

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 1536MB

#### Problem Statement

Given a set of N random numbers, count the number of pairs whose difference is exactly K. All numbers in the set are distinct.

#### Input Format
- First line: N K (count of numbers, required difference)
- Second line: N distinct integers

#### Output Format
- Count of pairs (a, b) where b - a = K

#### Solution

##### Approach
Sort the array. For each element a[i], binary search for a[i] + k in the remaining array. Count matches found. Alternative: Use a set for O(n) lookup.

##### Python Solution

```python
def binary_search(array, left, right, x):
 while left <= right:
  mid = (left + right) // 2
  if x == array[mid]:
   return True
  elif x < array[mid]:
   right = mid - 1
  else:
   left = mid + 1

 return False


def solution():
 n, k = map(int, input().strip().split())
 random_numbers = list(map(int, input().strip().split()))
 random_numbers.sort()
 total = 0
 n = len(random_numbers)

 for i in range(n):
  if binary_search(random_numbers, i+ 1, n - 1, random_numbers[i] + k):
   total += 1

 print(total)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n log n) for sorting and binary searches
- **Space Complexity:** O(n)

---

### OPC's Pizza

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 1536MB

#### Problem Statement

At a party, N friends want to share pizzas. Each pizza costs M dollars and must be bought by exactly two friends. Each friend has a certain amount of money. Find the maximum number of pizzas that can be bought.

#### Input Format
- T: number of test cases
- For each test case:
  - N M: number of friends, pizza cost
  - N integers: amount of money each friend has

#### Output Format
- Maximum number of pizzas that can be bought

#### Solution

##### Approach
Two-pointer technique on sorted array. Sort friends by money amount. Use left and right pointers to find pairs summing to exactly M. Move pointers based on whether sum is less, equal, or greater than M.

##### Python Solution

```python
def solution():
 T = int(input())
 for i in range(T):
  n, m = map(int, input().strip().split())
  friends = list(map(int, input().strip().split()))
  friends.sort()
  left = 0
  right = n - 1
  total = 0
  while left < right:
   if friends[left] + friends[right] == m:
    left += 1
    right -= 1
    total += 1
   if friends[left] + friends[right] > m:
    right -= 1
   if friends[left] + friends[right] < m:
    left += 1

  print(total)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(T * n log n) for sorting
- **Space Complexity:** O(n)

---

### Solve It

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

Solve the equation: p*e^(-x) + q*sin(x) + r*cos(x) + s*tan(x) + t*x^2 + u = 0 for x in the range [0, 1]. The function is monotonically decreasing in this range.

#### Input Format
- Multiple lines, each with 6 integers: p q r s t u

#### Output Format
- For each line: the root x with 4 decimal places, or "No solution"

#### Solution

##### Approach
Binary search on the answer in range [0, 1]. Since function is monotonically decreasing, if f(mid) * f(lo) < 0, the root is in [lo, mid], otherwise in [mid, hi]. Continue until result is within epsilon tolerance.

##### Python Solution

```python
import math

epsilon = math.pow(10, -9)


def calc_result(p, q, r, s, t, u, x):

 return p * math.exp(-x) + q * math.sin(x) + r * math.cos(x) + s * math.tan(x) + t * math.pow(x, 2) + u


def solution():
 while True:
  try:
   p, q, r, s, t, u= map(int, input().strip().split())
   lo, hi = 0, 1
   if -epsilon < calc_result(p, q, r, s, t, u, lo) < epsilon:
    print(lo)
    continue
   if -epsilon < calc_result(p, q, r, s, t, u, hi) < epsilon:
    print(hi)
    continue

   has_solution = False
   for i in range(1000):
    x = (lo + hi) / 2
    result = calc_result(p, q, r, s, t, u, x)

    if -epsilon < result < epsilon:
     print('{0:.4f}'.format(x))
     has_solution = True
     break
    if result * calc_result(p, q, r, s, t, u, lo) < 0:
     hi = x
    elif result * calc_result(p, q, r, s, t, u, hi) < 0:
     lo = x
   if not has_solution:
    print('No solution')

  except Exception as e:
   break


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(1000) = O(1) iterations per equation
- **Space Complexity:** O(1)

---

### Where is the Marble?

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given N marbles with numbers written on them, sort them and answer Q queries. Each query asks for the position of a marble with a specific number.

#### Input Format
- Multiple test cases until N=0 and Q=0
- For each test case:
  - N Q: number of marbles, number of queries
  - N marble values (one per line)
  - Q query values (one per line)

#### Output Format
- "CASE# X:" followed by query results
  - "Q found at P" if found (1-indexed position)
  - "Q not found" if not present

#### Solution

##### Approach
Sort the marbles. For each query, use binary search (bisect_left) to find position. Check if the found position contains the query value.

##### Python Solution

```python
import bisect

INF = float(1e9)


def solution():
 case = 1
 while True:
  N, Q = map(int, input().strip().split())

  if N == 0:
   break

  marbles = []
  for i in range(N):
   marbles.append(int(input().strip()))

  marbles.sort()

  print('CASE# ' + str(case) + ':')
  for i in range(Q):
   q = int(input().strip())
   result = bisect.bisect_left(marbles, q)

   if 0 <= result < len(marbles) and marbles[result] == q:
    print('{:d} found at {:d}'.format(q, result + 1))
   else:
    print('{:d} not found'.format(q))

  case += 1


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(N log N + Q log N) per test case
- **Space Complexity:** O(N)

---

### The Playboy Chimp

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

A male chimp wants to find a partner among N female chimps lined up by height. For Q male chimps with given heights, find the tallest female shorter than him and the shortest female taller than him.

#### Input Format
- N: number of female chimps
- N heights of female chimps (sorted in non-decreasing order)
- Q: number of queries
- Q heights of male chimps

#### Output Format
- For each query: two values separated by space
  - Tallest female shorter than query height (or 'X' if none)
  - Shortest female taller than query height (or 'X' if none)

#### Solution

##### Approach
Use binary search (bisect_right) to find insertion point. For shorter: search backwards from insertion point for strictly smaller. For taller: the element at insertion point if it exists and is strictly greater.

##### Python Solution

```python
from bisect import bisect_right


def solution():
 N = int(input())
 lady_chimps = list(map(int, input().strip().split()))
 Q = int(input())
 queries = list(map(int, input().strip().split()))

 for q in queries:
  upper_bound = bisect_right(lady_chimps, q)
  shorter_index = -1
  if upper_bound > 0:
   for i in range(upper_bound - 1, -1, -1):
    if lady_chimps[i] < q:
     shorter_index = i
     break
  shorter = 'X'
  taller = 'X'
  if shorter_index != -1:
   shorter = str(lady_chimps[shorter_index])
  if upper_bound < N:
   taller = str(lady_chimps[upper_bound])

  print(shorter, taller)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(N + Q log N) average case
- **Space Complexity:** O(N)

---

### The Monkey and the Oiled Bamboo

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

A monkey climbs a bamboo ladder with rungs at given heights. The monkey starts with strength k and can jump up to k units. After a maximum-strength jump, strength decreases by 1. Find the minimum initial strength k to reach the top.

#### Input Format
- T: number of test cases
- For each test case:
  - N: number of rungs
  - N integers: heights of rungs from ground

#### Output Format
- For each case: "Case X: k" where k is minimum initial strength needed

#### Solution

##### Approach
Binary search on the answer (initial strength k). For each k, simulate: check if monkey can reach top. If current jump equals remaining strength, decrease strength. If any jump exceeds strength, k is insufficient.

##### Python Solution

```python
def check_possibility(rungs, k, n):

 remain = k
 if rungs[0] > remain:
  return False
 if rungs[0] == remain:
  remain -= 1
 for i in range(1, n):
  if rungs[i] - rungs[i - 1] > remain:
   return False
  if rungs[i] - rungs[i-1] == remain:
   remain -= 1

 return remain >= 0


def solution():
 T = int(input())
 for i in range(T):
  N = int(input())
  rungs = list(map(int, input().strip().split()))

  lo = 0
  hi = int(1e7)
  while lo < hi - 1:
   mid = (lo + hi) // 2
   if check_possibility(rungs, mid, N):
    hi = mid
   else:
    lo = mid

  print('Case {0}: {1}'.format(i + 1, hi))


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(T * N * log(max_height))
- **Space Complexity:** O(N)
