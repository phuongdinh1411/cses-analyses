---
layout: simple
title: "Heap"
permalink: /problem_soulutions/Blue/Session 08 - Heap/
---

# Heap

Heap data structure and priority queue problems involving min-heap, max-heap, and heap-based algorithms for efficient element retrieval.

## Problems

### Restaurant Rating

#### Problem Information
- **Source:** CodeChef RRATING
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

A restaurant receives reviews with ratings. After each review, they want to display the rating at the top 1/3 position (ceiling). For example, if there are 5 reviews, show the rating at position ceil(5/3) = 2 from top.

Operations:
- "1 x": Add a review with rating x
- "2": Query the rating at top 1/3 position (or "No reviews yet" if empty)

#### Input Format
- Line 1: N (number of operations)
- Next N lines: Operations as described above

#### Output Format
For each query (type 2), print the answer.

#### Example
```
Input:
5
1 5
1 7
1 3
2
1 9

Output:
7
```
After adding ratings 5, 7, 3: sorted = [7, 5, 3]. Position ceil(3/3) = 1. Top 1 rating is 7.

#### Solution

##### Approach
Use two heaps - one for top 1/3 ratings (min-heap to get minimum of top elements), another for candidates (max-heap). Keep balance as reviews are added.

##### Python Solution

```python
from heapq import heappush, heappop, heapreplace

def solution():
    top_reviews = []      # min-heap for top 1/3
    candidate_reviews = []  # max-heap (negated) for remaining
    n = int(input())
    results = []
    num_reviews = 0

    for _ in range(n):
        command = input().strip()
        if command.startswith('1'):
            num_reviews += 1
            new_review = int(command.split()[1])
            if len(top_reviews) < num_reviews // 3:
                if not candidate_reviews or new_review > -candidate_reviews[0]:
                    heappush(top_reviews, new_review)
                else:
                    heappush(top_reviews, -heappop(candidate_reviews))
                    heappush(candidate_reviews, -new_review)
            else:
                if top_reviews and new_review > top_reviews[0]:
                    heappush(candidate_reviews, -heapreplace(top_reviews, new_review))
                else:
                    heappush(candidate_reviews, -new_review)
        else:
            results.append(top_reviews[0] if top_reviews else 'No reviews yet')

    print(*results, sep='\n')

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(N log N) for N operations with heap operations
- **Space Complexity:** O(N) for storing all reviews

---

### Monk and Multiplication

#### Problem Information
- **Source:** Hackerearth
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given an array of N integers added one by one, after each insertion output the product of the three largest numbers. If fewer than 3 numbers have been added, output -1.

#### Input Format
- Line 1: N (number of elements)
- Line 2: N space-separated integers

#### Output Format
N lines, each containing the product of 3 largest so far, or -1.

#### Example
```
Input:
5
1 2 3 4 5

Output:
-1
-1
6
24
60
```
After 1 element: -1. After 2: -1. After 3: 1*2*3=6. After 4: 2*3*4=24. After 5: 3*4*5=60.

#### Solution

##### Approach
Maintain a min-heap of size 3 with the largest elements. The heap root is always the smallest of the top 3.

##### Python Solution

```python
from heapq import heapify, heapreplace
from math import prod

def solution():
    n = int(input())
    a = list(map(int, input().split()))

    if n < 3:
        print('\n'.join(['-1'] * n))
        return

    top3 = a[:3]
    heapify(top3)

    for i, val in enumerate(a):
        if i < 2:
            print(-1)
        elif i == 2:
            print(prod(top3))
        else:
            if val > top3[0]:
                heapreplace(top3, val)
            print(prod(top3))

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(N log 3) = O(N) for N insertions
- **Space Complexity:** O(1) for the fixed-size heap of 3 elements

---

### Roy and Trending Topics

#### Problem Information
- **Source:** Hackerearth
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given N topics with current scores and engagement data (posts, likes, comments, shares), calculate new scores using:
```
new_score = posts*50 + likes*5 + comments*10 + shares*20
```

Find the top 5 trending topics based on the CHANGE in score (new - old). Ties are broken by higher topic ID.

#### Input Format
- Line 1: N (number of topics)
- Next N lines: topic_id current_score posts likes comments shares

#### Output Format
Top 5 topics with their new scores (highest change first).

#### Example
```
Input:
6
1 100 10 20 5 3
2 200 5 10 2 1
3 50 20 40 10 5
4 300 2 5 1 0
5 150 15 30 8 4
6 80 8 15 4 2

Output:
3 850
5 640
1 660
6 330
2 370
```
Topic 3 has highest change: new_score = 20*50+40*5+10*10+5*20 = 850, change = 850-50 = 800.

#### Solution

##### Approach
Use a min-heap of size 5 tracking top trending by score change. Custom comparison for the Topic class handles tie-breaking.

##### Python Solution

```python
from heapq import heappush, heappop, heapreplace

class Topic:
    def __init__(self, topic_id, current_score, posts, likes, comments, shares):
        self.id = topic_id
        self.new_score = posts * 50 + likes * 5 + comments * 10 + shares * 20
        self.change_in_score = self.new_score - current_score

    def __lt__(self, other):
        if self.change_in_score != other.change_in_score:
            return self.change_in_score < other.change_in_score
        return self.id < other.id

def solution():
    n = int(input())
    top_trends = []

    for i in range(n):
        topic_id, z, p, l, c, s = map(int, input().split())
        topic = Topic(topic_id, z, p, l, c, s)

        if i < 5:
            heappush(top_trends, topic)
        elif top_trends[0] < topic:
            heapreplace(top_trends, topic)

    results = []
    while top_trends:
        topic = heappop(top_trends)
        results.append(f"{topic.id} {topic.new_score}")

    print(*reversed(results), sep='\n')

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(N log 5) = O(N) for processing N topics
- **Space Complexity:** O(1) for fixed-size heap of 5 elements

---

### QHEAP1

#### Problem Information
- **Source:** Hackerrank
- **Difficulty:** Secret
- **Time Limit:** 4000ms
- **Memory Limit:** 512MB

#### Problem Statement

Implement a min-heap that supports the following operations:
- "1 v": Add element v to the heap
- "2 v": Delete element v from the heap (v is guaranteed to exist)
- "3": Print the minimum element

#### Input Format
- Line 1: Q (number of queries)
- Next Q lines: Queries as described above

#### Output Format
For each type-3 query, print the minimum element.

#### Example
```
Input:
5
1 4
1 9
3
2 4
3

Output:
4
9
```
Insert 4, insert 9. Minimum is 4. Delete 4. Minimum is now 9.

#### Solution

##### Approach
Use a heap with lazy deletion. Track deleted elements separately and clean them when querying the minimum.

##### Python Solution

```python
from heapq import heappush, heappop
from collections import Counter

def solution():
    q = int(input())
    heap = []
    deleted = Counter()

    for _ in range(q):
        query = input().split()
        if query[0] == '3':
            while deleted[heap[0]] > 0:
                deleted[heap[0]] -= 1
                heappop(heap)
            print(heap[0])
        elif query[0] == '1':
            heappush(heap, int(query[1]))
        else:
            deleted[int(query[1])] += 1

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(Q log Q) for Q operations
- **Space Complexity:** O(Q) for heap and delete list

---

### LAZYPROG - Lazy Programmer

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 368ms
- **Memory Limit:** 1536MB

#### Problem Statement

A lazy programmer has N projects with deadlines. Each project i has:
- a[i]: cost per unit time to speed up (dollars/hour)
- b[i]: time needed to complete at normal speed (hours)
- d[i]: deadline (hours from now)

He can pay to speed up any project. Find the minimum total cost to meet all deadlines.

#### Input Format
- Line 1: T (test cases)
- For each test case:
  - Line 1: N (number of projects)
  - Next N lines: a b d for each project

#### Output Format
Minimum cost (2 decimal places).

#### Example
```
Input:
1
2
1 2 2
2 1 3

Output:
0.50
```
Two projects: Project 1 costs 1$/hr to speed up, needs 2 hrs, deadline 2. Project 2 costs 2$/hr, needs 1 hr, deadline 3. Do P1 (2 hrs), then P2 (1 hr) = 3 hrs total. P2 finishes at hr 3, meeting deadline. But we need to speed up P1 by 0.5 hrs (cheaper at 1$/hr) to finish P2 by deadline 3. Cost = 0.5 * 1 = 0.50.

#### Solution

##### Approach
Sort by deadline, use heap to always speed up the cheapest project first. When a deadline is missed, take time from the project with lowest speedup cost.

##### Python Solution

```python
from heapq import heappush, heappop

class Project:
    def __init__(self, a, b, d):
        self.a = a  # cost per unit time
        self.b = b  # time needed
        self.d = d  # deadline

    def __lt__(self, other):
        return self.a > other.a  # max-heap by cost (cheaper to speed up first)

def solution():
    t = int(input())

    for _ in range(t):
        total_cost = 0.0
        current_time = 0
        pq = []

        n = int(input())
        projects = [Project(*map(int, input().split())) for _ in range(n)]
        projects.sort(key=lambda x: x.d)

        for proj in projects:
            current_time += proj.b
            heappush(pq, proj)

            if current_time <= proj.d:
                continue

            while current_time > proj.d:
                cheapest = heappop(pq)
                time_over = current_time - proj.d
                if cheapest.b >= time_over:
                    cheapest.b -= time_over
                    total_cost += time_over / cheapest.a
                    current_time = proj.d
                    heappush(pq, cheapest)
                else:
                    total_cost += cheapest.b / cheapest.a
                    current_time -= cheapest.b

        print(f"{total_cost:.2f}")

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(N log N) for sorting and heap operations
- **Space Complexity:** O(N) for storing projects

---

### PRO - Promotion

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 1536MB

#### Problem Statement

A supermarket runs a promotion over N days. Each day, some customers submit receipts. At the end of each day, the customer with the highest receipt wins prize equal to receipt value, and the lowest receipt customer wins prize equal to their receipt value (both are removed from future consideration).

Calculate total prize money: sum(max) - sum(min) over all days.

#### Input Format
- Line 1: N (number of days)
- Next N lines: k r1 r2 ... rk (k receipts for that day)

#### Output Format
Total prize difference.

#### Example
```
Input:
2
3 1 2 3
2 1 2

Output:
4
```
Day 1: receipts [1,2,3]. Max=3 wins, Min=1 wins. Day 2: receipts [1,2]. Max=2 wins, Min=1 wins. Total = (3+2) - (1+1) = 4.

#### Solution

##### Approach
Use two heaps (min and max) with lazy deletion to track receipts efficiently.

##### Python Solution

```python
from heapq import heappush, heappop
from collections import defaultdict

def solution():
    n = int(input())
    total_prizes = 0
    max_heap = []  # negated for max behavior
    min_heap = []

    deleted_from_max = defaultdict(int)
    deleted_from_min = defaultdict(int)

    for _ in range(n):
        line = list(map(int, input().split()))
        receipts = line[1:]

        for receipt in receipts:
            heappush(min_heap, receipt)
            heappush(max_heap, -receipt)

        if len(max_heap) >= 2:
            # Get max (skip deleted)
            while deleted_from_min[-max_heap[0]] > 0:
                deleted_from_min[-max_heap[0]] -= 1
                heappop(max_heap)
            from_max = heappop(max_heap)

            # Get min (skip deleted)
            while deleted_from_max[min_heap[0]] > 0:
                deleted_from_max[min_heap[0]] -= 1
                heappop(min_heap)
            from_min = heappop(min_heap)

            # Mark as deleted for the other heap
            deleted_from_max[from_max] += 1
            deleted_from_min[from_min] += 1

            total_prizes -= (from_max + from_min)

    print(total_prizes)

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(R log R) where R is total number of receipts
- **Space Complexity:** O(R) for heaps and deletion arrays

---

### I Can Guess the Data Structure!

#### Problem Information
- **Source:** UVA 11995
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given a sequence of operations (insert and extract), determine what data structure is being used: stack, queue, or priority queue (max-heap).

Operations:
- "1 x": Insert element x
- "2 x": Extract returns element x

Output:
- "stack" if it matches stack behavior (LIFO)
- "queue" if it matches queue behavior (FIFO)
- "priority queue" if it matches max-heap behavior
- "not sure" if multiple structures are possible
- "impossible" if no structure matches

#### Input Format
Multiple test cases until EOF, each with N operations.

#### Output Format
One line per test case.

#### Example
```
Input:
6
1 1
1 2
1 3
2 1
2 2
2 3

Output:
queue
```
Insert 1, 2, 3 then extract 1, 2, 3. This is FIFO order, so it's a queue.

#### Solution

##### Approach
Simulate all three structures simultaneously and check consistency with each extraction.

##### Python Solution

```python
from heapq import heappush, heappop
from collections import deque
import sys

def solution():
    tokens = sys.stdin.read().split()[::-1]

    while tokens:
        n = int(tokens.pop())
        heap = []           # max-heap (negated)
        stack = []
        queue = deque()

        is_heap = is_stack = is_queue = True

        for _ in range(n):
            op, x = int(tokens.pop()), int(tokens.pop())

            if not any([is_heap, is_stack, is_queue]):
                continue

            if op == 1:
                if is_heap:
                    heappush(heap, -x)
                if is_stack:
                    stack.append(x)
                if is_queue:
                    queue.append(x)
            else:
                if is_heap:
                    if not heap or -heappop(heap) != x:
                        is_heap = False
                if is_stack:
                    if not stack or stack.pop() != x:
                        is_stack = False
                if is_queue:
                    if not queue or queue.popleft() != x:
                        is_queue = False

        matches = sum([is_heap, is_stack, is_queue])
        if matches > 1:
            print('not sure')
        elif matches == 0:
            print('impossible')
        elif is_stack:
            print('stack')
        elif is_queue:
            print('queue')
        else:
            print('priority queue')

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(N log N) per test case for heap operations
- **Space Complexity:** O(N) for storing elements in each structure

---

### Add All

#### Problem Information
- **Source:** UVA 10954
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given N numbers, you need to add them all together. Each addition operation costs the sum of the two numbers being added. Find the minimum total cost to combine all numbers into one.

Example: Numbers [1, 2, 3]
- Add 1+2=3 (cost 3), then 3+3=6 (cost 6) = total 9

#### Input Format
- Multiple test cases until N=0
- Line 1: N
- Line 2: N integers

#### Output Format
Minimum total cost for each test case.

#### Example
```
Input:
3
1 2 3
0

Output:
9
```
Numbers [1, 2, 3]. Add 1+2=3 (cost 3). Add 3+3=6 (cost 6). Total cost = 9.

#### Solution

##### Approach
Huffman-like algorithm - always add the two smallest numbers using a min-heap.

##### Python Solution

```python
from heapq import heapify, heappop, heappush

def solution():
    while True:
        n = int(input())
        if n == 0:
            return

        nums = list(map(int, input().split()))
        heapify(nums)
        total_cost = 0

        while len(nums) > 1:
            first, second = heappop(nums), heappop(nums)
            combined = first + second
            total_cost += combined
            heappush(nums, combined)

        print(total_cost)

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(N log N) for N-1 heap operations
- **Space Complexity:** O(N) for the heap
