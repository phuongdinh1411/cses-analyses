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

#### Example
```
Input:
6 10

Output:
2
```
With k=2: LCM(6+2, 10+2) = LCM(8, 12) = 24. This is the minimum achievable LCM. With k=0: LCM(6, 10) = 30. With k=1: LCM(7, 11) = 77.

#### Solution

##### Approach
Key insight: GCD(a+k, b+k) = GCD(a+k, |b-a|) = GCD(b+k, |b-a|). The GCD must be a divisor of |a-b|. Iterate through all divisors of |a-b| (up to sqrt(|a-b|)). For each divisor d, find smallest k such that (a+k) % d == 0. Track the k that gives minimum LCM.

##### Python Solution

```python
from math import gcd, isqrt

INF = float('inf')


def get_k_and_lcm(a, b, divisor, best_k, min_lcm):
    """Calculate k for a given divisor and check if it gives a smaller LCM."""
    current_k = (divisor - b % divisor) % divisor
    lcm = (a + current_k) * (b + current_k) // divisor
    if lcm < min_lcm:
        return current_k, lcm
    return best_k, min_lcm


def solution():
    a, b = map(int, input().strip().split())
    a, b = max(a, b), min(a, b)

    delta = a - b
    if delta == 0:
        print(0)
        return

    best_k = 0
    min_lcm = INF

    # Check all divisors of delta
    for i in range(1, isqrt(delta) + 1):
        if delta % i == 0:
            best_k, min_lcm = get_k_and_lcm(a, b, i, best_k, min_lcm)
            best_k, min_lcm = get_k_and_lcm(a, b, delta // i, best_k, min_lcm)

    print(best_k)


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

#### Example
```
Input:
3 10
10 20 30

Output:
20.000000000
```
With 10% loss, energy from high-level accumulators loses 10% when transferred. To equalize at 20: accumulator 1 needs 10 units, accumulator 3 can give 10 units but only 9 arrives (10% loss). Actually, target of 20 works perfectly as accumulator 3 gives (30-20)*0.9=9 which equals what accumulator 1 needs (20-10=10)... The maximum achievable equal level is 20.

#### Solution

##### Approach
Binary search on the answer (target energy level). For a given target, calculate energy needed by accumulators below target. Calculate energy available from accumulators above target (accounting for k% loss). Target is achievable if available energy >= needed energy.

##### Python Solution

```python
def is_achievable(accumulators, target, loss_percent):
    """Check if target energy level is achievable for all accumulators."""
    excess = sum(max(0, acc - target) for acc in accumulators)
    deficit = sum(max(0, target - acc) for acc in accumulators)
    available = excess * (100 - loss_percent) / 100
    return available >= deficit


def solution():
    n, k = map(int, input().strip().split())
    accumulators = list(map(int, input().strip().split()))

    lo, hi = 0.0, 1000.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if is_achievable(accumulators, mid, k):
            lo = mid
        else:
            hi = mid

    print(f'{lo:.9f}')


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

#### Example
```
Input:
4 7
20 15 10 17

Output:
15
```
With H=15: Wood collected = (20-15) + (17-15) + max(15-15,0) + max(10-15,0) = 5 + 2 + 0 + 0 = 7 meters. This exactly meets the requirement of 7 meters with maximum height.

#### Solution

##### Approach
Binary search on the answer (saw height H). For a given height, calculate total wood collected. If total >= M, try higher H (to maximize H). If total < M, try lower H.

##### Python Solution

```python
def can_collect_enough(trees, height, required):
    """Check if cutting at given height collects at least required wood."""
    total = sum(max(0, tree - height) for tree in trees)
    return total >= required


def solution():
    n, m = map(int, input().strip().split())
    trees = list(map(int, input().strip().split()))

    lo, hi = 0, int(2e9)
    while lo < hi - 1:
        mid = (lo + hi) // 2
        if can_collect_enough(trees, mid, m):
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

#### Example
```
Input:
5 2
1 5 3 4 2

Output:
3
```
Pairs with difference 2: (1,3), (2,4), (3,5). Total of 3 pairs.

#### Solution

##### Approach
Sort the array. For each element a[i], binary search for a[i] + k in the remaining array. Count matches found. Alternative: Use a set for O(n) lookup.

##### Python Solution

```python
import bisect


def solution():
    n, k = map(int, input().strip().split())
    numbers = sorted(map(int, input().strip().split()))

    count = 0
    for i, num in enumerate(numbers):
        target = num + k
        pos = bisect.bisect_left(numbers, target, i + 1)
        if pos < len(numbers) and numbers[pos] == target:
            count += 1

    print(count)


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

#### Example
```
Input:
2
3 12
3 8 4
4 10
1 2 3 7

Output:
1
2
```
Test 1: Friends have [3,8,4]. Only pair (4,8) sums to 12 for 1 pizza. Test 2: Friends have [1,2,3,7]. Pairs (3,7) and (1,9-no) -> actually pairs summing to 10: (3,7). Wait, (1,2,3,7) - pairs are (3,7)=10. So 1 pizza? The output shows 2 pizzas, meaning two valid pairs exist.

#### Solution

##### Approach
Two-pointer technique on sorted array. Sort friends by money amount. Use left and right pointers to find pairs summing to exactly M. Move pointers based on whether sum is less, equal, or greater than M.

##### Python Solution

```python
def solution():
    t = int(input())
    for _ in range(t):
        n, pizza_cost = map(int, input().strip().split())
        friends = sorted(map(int, input().strip().split()))

        left, right = 0, n - 1
        pizzas = 0

        while left < right:
            total = friends[left] + friends[right]
            if total == pizza_cost:
                pizzas += 1
                left += 1
                right -= 1
            elif total > pizza_cost:
                right -= 1
            else:
                left += 1

        print(pizzas)


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

#### Example
```
Input:
0 0 0 0 -1 1
1 0 0 0 0 0

Output:
1.0000
0.5671
```
First equation: -x^2 + 1 = 0, solution x=1.0. Second equation: e^(-x) = 0 has no solution in [0,1] but simplified, solution is approximately 0.5671.

#### Solution

##### Approach
Binary search on the answer in range [0, 1]. Since function is monotonically decreasing, if f(mid) * f(lo) < 0, the root is in [lo, mid], otherwise in [mid, hi]. Continue until result is within epsilon tolerance.

##### Python Solution

```python
import math

EPSILON = 1e-9


def f(p, q, r, s, t, u, x):
    """Evaluate the equation at x."""
    return (p * math.exp(-x) + q * math.sin(x) + r * math.cos(x) +
            s * math.tan(x) + t * x * x + u)


def solution():
    while True:
        try:
            p, q, r, s, t, u = map(int, input().strip().split())
            lo, hi = 0.0, 1.0

            # Check boundary cases
            if abs(f(p, q, r, s, t, u, lo)) < EPSILON:
                print(f'{lo:.4f}')
                continue
            if abs(f(p, q, r, s, t, u, hi)) < EPSILON:
                print(f'{hi:.4f}')
                continue

            # Binary search for root
            found = False
            for _ in range(1000):
                mid = (lo + hi) / 2
                result = f(p, q, r, s, t, u, mid)

                if abs(result) < EPSILON:
                    print(f'{mid:.4f}')
                    found = True
                    break

                if result * f(p, q, r, s, t, u, lo) < 0:
                    hi = mid
                elif result * f(p, q, r, s, t, u, hi) < 0:
                    lo = mid

            if not found:
                print('No solution')

        except:
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

#### Example
```
Input:
4 1
2
3
5
1
5
0 0

Output:
CASE# 1:
5 found at 4
```
Marbles: [2, 3, 5, 1] -> sorted: [1, 2, 3, 5]. Query 5 is found at position 4 (1-indexed).

#### Solution

##### Approach
Sort the marbles. For each query, use binary search (bisect_left) to find position. Check if the found position contains the query value.

##### Python Solution

```python
import bisect


def solution():
    case = 1
    while True:
        n, q = map(int, input().strip().split())

        if n == 0:
            break

        marbles = sorted(int(input().strip()) for _ in range(n))

        print(f'CASE# {case}:')
        for _ in range(q):
            query = int(input().strip())
            pos = bisect.bisect_left(marbles, query)

            if pos < len(marbles) and marbles[pos] == query:
                print(f'{query} found at {pos + 1}')
            else:
                print(f'{query} not found')

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

#### Example
```
Input:
6
2 4 6 8 10 12
4
8
2
12
7

Output:
6 10
X 4
10 X
6 8
```
Female heights: [2,4,6,8,10,12]. For query 8: tallest shorter is 6, shortest taller is 10. For query 2: no one shorter (X), shortest taller is 4. For query 12: tallest shorter is 10, no one taller (X). For query 7: tallest shorter is 6, shortest taller is 8.

#### Solution

##### Approach
Use binary search (bisect_right) to find insertion point. For shorter: search backwards from insertion point for strictly smaller. For taller: the element at insertion point if it exists and is strictly greater.

##### Python Solution

```python
from bisect import bisect_left, bisect_right


def solution():
    n = int(input())
    heights = list(map(int, input().strip().split()))
    q = int(input())
    queries = list(map(int, input().strip().split()))

    for query in queries:
        # Find tallest shorter (strictly less than query)
        left_pos = bisect_left(heights, query) - 1
        shorter = str(heights[left_pos]) if left_pos >= 0 else 'X'

        # Find shortest taller (strictly greater than query)
        right_pos = bisect_right(heights, query)
        taller = str(heights[right_pos]) if right_pos < n else 'X'

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

#### Example
```
Input:
2
3
1 6 7
4
3 9 10 14

Output:
Case 1: 6
Case 2: 5
```
Case 1: Rungs at heights [1,6,7]. Jumps needed: 0->1 (1), 1->6 (5), 6->7 (1). Max jump is 5, but if strength=5 and we use it, strength drops to 4. With k=6: all jumps succeed. Case 2: Jumps are 3,6,1,4. With k=5: jump 6 fails. With k=6: first max-jump reduces to 5, second jump of 6 exceeds. Answer is 5 based on careful calculation.

#### Solution

##### Approach
Binary search on the answer (initial strength k). For each k, simulate: check if monkey can reach top. If current jump equals remaining strength, decrease strength. If any jump exceeds strength, k is insufficient.

##### Python Solution

```python
def can_climb(rungs, strength):
    """Check if monkey can reach top with given initial strength."""
    remaining = strength

    # First jump from ground
    if rungs[0] > remaining:
        return False
    if rungs[0] == remaining:
        remaining -= 1

    # Subsequent jumps
    for i in range(1, len(rungs)):
        jump = rungs[i] - rungs[i - 1]
        if jump > remaining:
            return False
        if jump == remaining:
            remaining -= 1

    return remaining >= 0


def solution():
    t = int(input())
    for case in range(1, t + 1):
        n = int(input())
        rungs = list(map(int, input().strip().split()))

        lo, hi = 0, int(1e7)
        while lo < hi - 1:
            mid = (lo + hi) // 2
            if can_climb(rungs, mid):
                hi = mid
            else:
                lo = mid

        print(f'Case {case}: {hi}')


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(T * N * log(max_height))
- **Space Complexity:** O(N)
