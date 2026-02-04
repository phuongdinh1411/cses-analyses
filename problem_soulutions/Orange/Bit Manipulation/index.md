---
layout: simple
title: "Bit Manipulation"
permalink: /problem_soulutions/Orange/Bit Manipulation/
---

# Bit Manipulation

Problems involving bitwise operations such as AND, OR, XOR, and bit shifting to efficiently solve computational problems.

## Problems

### Aish And XOR

#### Problem Information
- **Source:** Hackerearth
- **Difficulty:** Secret
- **Time Limit:** 1500ms
- **Memory Limit:** 512MB

#### Problem Statement

Given an array (containing only 0 and 1) of N length. For each query with L and R, find:
1. The XOR of all elements from L to R (both inclusive)
2. The number of unset bits (0's) in the given range

#### Input Format
- First line: N (number of elements)
- Second line: N numbers containing 0 and 1 only
- Third line: Q (number of queries)
- Next Q lines: L and R for each query

#### Solution

##### Approach
Use prefix arrays for both XOR and zero count:
1. **Prefix XOR:** `xor_prefix[i]` = XOR of elements from index 0 to i
   - XOR(L, R) = xor_prefix[R] ^ xor_prefix[L-1]
2. **Prefix Zero Count:** `zero_prefix[i]` = count of zeros from index 0 to i
   - Zeros(L, R) = zero_prefix[R] - zero_prefix[L-1]

##### Python Solution

```python
def solve():
    n = int(input())
    arr = list(map(int, input().split()))

    # Build prefix arrays (1-indexed)
    xor_prefix = [0] * (n + 1)
    zero_prefix = [0] * (n + 1)

    for i in range(n):
        xor_prefix[i + 1] = xor_prefix[i] ^ arr[i]
        zero_prefix[i + 1] = zero_prefix[i] + (1 if arr[i] == 0 else 0)

    q = int(input())
    for _ in range(q):
        l, r = map(int, input().split())

        # XOR of range [l, r]
        xor_result = xor_prefix[r] ^ xor_prefix[l - 1]

        # Count of zeros in range [l, r]
        zeros = zero_prefix[r] - zero_prefix[l - 1]

        print(xor_result, zeros)

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N) for preprocessing + O(1) per query = O(N + Q)
- **Space Complexity:** O(N) for prefix arrays

---

### Brexit Negotiations

#### Problem Information
- **Source:** Kattis
- **Difficulty:** Secret
- **Time Limit:** 4000ms
- **Memory Limit:** 1024MB

#### Problem Statement

Brexit negotiations have n topics with dependencies. Each topic has a base duration ei minutes. At the start of each meeting, delegates take 1 extra minute for each previous meeting to recap.

If a meeting is the k-th meeting (0-indexed), its total time is ei + k minutes.

Find an ordering of topics (respecting dependencies) that minimizes the longest meeting duration.

#### Solution

##### Approach
Key insight: Process topics in **reverse** topological order, choosing the topic with smallest base duration among those with no dependents.

If we process topics in order n-1, n-2, ..., 0 (reversed), a topic processed at position i has recap time (n-1-i). We want topics with large base durations to have small recap times.

##### Python Solution

```python
import heapq
from collections import defaultdict

def solve():
    n = int(input())

    base_time = [0] * (n + 1)
    deps = [[] for _ in range(n + 1)]
    out_degree = [0] * (n + 1)

    for u in range(1, n + 1):
        line = list(map(int, input().split()))
        base_time[u] = line[0]
        d = line[1]
        for v in line[2:2+d]:
            deps[u].append(v)
            out_degree[v] += 1

    heap = []
    for u in range(1, n + 1):
        if out_degree[u] == 0:
            heapq.heappush(heap, (base_time[u], u))

    max_meeting = 0
    recap_time = n - 1

    while heap:
        dur, u = heapq.heappop(heap)
        total_time = dur + recap_time
        max_meeting = max(max_meeting, total_time)
        recap_time -= 1

        for v in deps[u]:
            out_degree[v] -= 1
            if out_degree[v] == 0:
                heapq.heappush(heap, (base_time[v], v))

    print(max_meeting)

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N log N) for heap operations
- **Space Complexity:** O(N + E) where E is total dependencies

---

### Mattey Multiplication

#### Problem Information
- **Source:** Hackerearth
- **Difficulty:** Secret
- **Time Limit:** 4000ms
- **Memory Limit:** 512MB

#### Problem Statement

Given N and M, write an equation using left shift operators whose result equals N * M.

The equation should be in the form: (N<<p1) + (N<<p2) + ... + (N<<pk) where p1 >= p2 >= ... >= pk and k is minimum.

#### Solution

##### Approach
N x M = N x (sum of powers of 2 in M's binary representation)

If M = 2^a + 2^b + 2^c + ..., then:
N x M = (N << a) + (N << b) + (N << c) + ...

##### Python Solution

```python
def solve():
    t = int(input())

    for _ in range(t):
        n, m = map(int, input().split())

        positions = []
        bit_pos = 0

        while m > 0:
            if m & 1:
                positions.append(bit_pos)
            m >>= 1
            bit_pos += 1

        terms = []
        for pos in reversed(positions):
            terms.append(f"({n}<<{pos})")

        print(" + ".join(terms))

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(log M) per test case
- **Space Complexity:** O(log M) for storing bit positions

---

### Online Courses in BSU

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

Polycarp needs to pass k main online courses to get a diploma. There are n courses total, with dependencies (prerequisites). Find the minimum number of courses to pass and the order to pass them.

#### Solution

##### Approach
Use DFS-based topological sort starting only from main courses. This naturally finds only the necessary prerequisites. Detect cycles using three-color marking (white/gray/black).

##### Python Solution

```python
import sys
sys.setrecursionlimit(200000)

def solve():
    n, k = map(int, input().split())
    main_courses = list(map(int, input().split()))

    deps = [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        line = list(map(int, input().split()))
        t = line[0]
        deps[i] = line[1:t+1]

    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * (n + 1)
    result = []
    has_cycle = False

    def dfs(u):
        nonlocal has_cycle
        if has_cycle:
            return

        color[u] = GRAY

        for v in deps[u]:
            if color[v] == GRAY:
                has_cycle = True
                return
            if color[v] == WHITE:
                dfs(v)

        color[u] = BLACK
        result.append(u)

    for course in main_courses:
        if color[course] == WHITE:
            dfs(course)

    if has_cycle:
        print(-1)
    else:
        print(len(result))
        print(' '.join(map(str, result)))

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N + E) where E is total dependencies
- **Space Complexity:** O(N + E)

---

### Power of Two

#### Problem Information
- **Source:** Hackerearth
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

Given an array A, determine if there exists any subset where the AND of all elements is a power of two (1, 2, 4, 8, 16, ...).

#### Solution

##### Approach
For AND of a subset to be a power of 2, exactly one bit must remain set.

Strategy: For each bit position (0 to 30), AND together all numbers that have this bit set. If the result is exactly 2^bit, then we found a valid subset.

##### Python Solution

```python
def is_power_of_two(x):
    return x > 0 and (x & (x - 1)) == 0

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))

        found = False

        for bit in range(31):
            target = 1 << bit
            and_result = (1 << 31) - 1

            has_bit = False
            for num in arr:
                if num & target:
                    and_result &= num
                    has_bit = True

            if has_bit and is_power_of_two(and_result):
                found = True
                break

        print("YES" if found else "NO")

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(31 x N) = O(N) per test case
- **Space Complexity:** O(N) for storing the array

---

### Samu and her Birthday Party

#### Problem Information
- **Source:** Hackerearth
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

Samu is planning a birthday party and wants to select dishes for the menu. She has N friends and K available dishes. Each friend has preferences represented as a binary string where '1' means they like that dish.

Find the minimum number of dishes to include in the menu so that every friend has at least one dish they like.

#### Solution

##### Approach
Since K <= 10, we can enumerate all 2^K possible subsets of dishes. For each subset, check if every friend likes at least one dish in it. Track the minimum subset size that satisfies everyone.

##### Python Solution

```python
def solve():
    t = int(input())

    for _ in range(t):
        n, k = map(int, input().split())
        preferences = []

        for _ in range(n):
            pref = input().strip()
            mask = int(pref, 2)
            preferences.append(mask)

        min_dishes = k

        for subset in range(1, 1 << k):
            all_satisfied = True

            for pref in preferences:
                if (pref & subset) == 0:
                    all_satisfied = False
                    break

            if all_satisfied:
                dish_count = bin(subset).count('1')
                min_dishes = min(min_dishes, dish_count)

        print(min_dishes)

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(2^K x N) per test case
- **Space Complexity:** O(N) for storing preferences

---

### Sansa and XOR

#### Problem Information
- **Source:** Hackerrank
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

Sansa has an array. She wants to find the value obtained by XOR-ing the contiguous subarrays, followed by XOR-ing the values thus obtained.

#### Solution

##### Approach
For each element at index i (0-indexed), count how many subarrays include it:
- Total subarrays containing element i = (i+1) x (n-i)

If this count is odd, the element contributes to the final XOR. If even, it cancels out.

##### Python Solution

```python
def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))

        result = 0

        for i in range(n):
            count = (i + 1) * (n - i)
            if count % 2 == 1:
                result ^= arr[i]

        print(result)

if __name__ == "__main__":
    solve()
```

##### Optimized Solution

```python
def solve_optimized():
    t = int(input())

    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))

        # If n is even, result is always 0
        if n % 2 == 0:
            print(0)
            continue

        # If n is odd, XOR elements at even indices
        result = 0
        for i in range(0, n, 2):
            result ^= arr[i]

        print(result)

if __name__ == "__main__":
    solve_optimized()
```

##### Complexity Analysis
- **Time Complexity:** O(n) per test case
- **Space Complexity:** O(n) for storing the array

---

### power of 2

#### Problem Information
- **Source:** Hackerearth
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

Given an array A, determine if there exists any subset where the AND of all elements is a power of two (1, 2, 4, 8, 16, ...).

#### Solution

##### Python Solution

```python
def is_power_of_two(x):
    return x > 0 and (x & (x - 1)) == 0

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))

        found = False

        # Check if any single element is power of 2
        for num in arr:
            if is_power_of_two(num):
                found = True
                break

        if not found:
            for bit in range(31):
                target = 1 << bit
                and_result = (1 << 31) - 1

                has_bit = False
                for num in arr:
                    if num & target:
                        and_result &= num
                        has_bit = True

                if has_bit and is_power_of_two(and_result):
                    found = True
                    break

        print("YES" if found else "NO")

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(31 x N) = O(N) per test case
- **Space Complexity:** O(N) for storing the array
