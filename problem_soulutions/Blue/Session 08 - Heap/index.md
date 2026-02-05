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

#### Solution

##### Approach
Use two heaps - one for top 1/3 ratings (min-heap to get minimum of top elements), another for candidates (max-heap). Keep balance as reviews are added.

##### Python Solution

```python
import heapq

def solution():
 top_reviews = []
 candidate_reviews = []
 N = int(input())
 results = []
 num_of_reviews = 0
 for i in range(N):
  command = input().strip()
  if command.startswith('1'):
   num_of_reviews += 1
   new_review = int(command.split()[1])
   if len(top_reviews) < num_of_reviews // 3:
    if len(candidate_reviews) < 0 or new_review > -candidate_reviews[0]:
     heapq.heappush(top_reviews, new_review)
    else:
     heapq.heappush(top_reviews, -candidate_reviews[0])
     heapq.heappop(candidate_reviews)
     heapq.heappush(candidate_reviews, -new_review)
   else:
    if len(top_reviews) > 0 and new_review > top_reviews[0]:
     heapq.heappush(candidate_reviews, -top_reviews[0])
     heapq.heappop(top_reviews)
     heapq.heappush(top_reviews, new_review)
    else:
     heapq.heappush(candidate_reviews, -new_review)
  else:
   if len(top_reviews) > 0:
    results.append(top_reviews[0])
   else:
    results.append('No reviews yet')

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

#### Solution

##### Approach
Maintain a min-heap of size 3 with the largest elements. The heap root is always the smallest of the top 3.

##### Python Solution

```python
import heapq

def solution():
 N = int(input())
 A = list(map(int, input().split()))

 if N < 3:
  print(-1)
  if N > 1:
   print(-1)
  return

 max_list = A[:3]
 heapq.heapify(max_list)

 for i in range(N):
  if i < 3:
   if i == 2:
    print(max_list[0]*max_list[1]*max_list[2])
   else:
    print(-1)
  else:
   if A[i] > max_list[0]:
    heapq.heappop(max_list)
    heapq.heappush(max_list, A[i])
   print(max_list[0]*max_list[1]*max_list[2])

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

#### Solution

##### Approach
Use a min-heap of size 5 tracking top trending by score change. Custom comparison for the Topic class handles tie-breaking.

##### Python Solution

```python
import heapq

class Topic:
 def __init__(self, topic_id, current_score, posts, likes, comments, shares):
  self.id = topic_id
  self.new_score = posts * 50 + likes * 5 + comments * 10 + shares * 20
  self.change_in_score = self.new_score - current_score

 def __lt__(self, other):
  if self.change_in_score < other.change_in_score:
   return True
  if self.change_in_score == other.change_in_score:
   if self.id < other.id:
    return True
   else:
    return False
  return False

def solution():
 N = int(input())

 top_trends = []
 for i in range(N):
  topic_id, Z, P, L, C, S = map(int, input().strip().split())
  topic = Topic(topic_id, Z, P, L, C, S)

  if i >= 5:
   if top_trends[0] < topic:
    heapq.heappop(top_trends)
    heapq.heappush(top_trends, topic)
  else:
   heapq.heappush(top_trends, topic)

 results = []
 while len(top_trends) > 0:
  topic = heapq.heappop(top_trends)
  results = [str(topic.id) + ' ' + str(topic.new_score)] + results

 print(*results, sep='\n')

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

#### Solution

##### Approach
Use a heap with lazy deletion. Track deleted elements separately and clean them when querying the minimum.

##### Python Solution

```python
import heapq

def solution():
 Q = int(input())
 my_list = []
 delete_list = []
 for i in range(Q):
  query = input()
  if query.startswith('3'):
   while True:
    if my_list[0] not in delete_list:
     break
    pos = delete_list.index(my_list[0])
    delete_list.pop(pos)
    heapq.heappop(my_list)

   print(my_list[0])
  else:
   command, param = map(int, query.split())
   if command == 1:
    heapq.heappush(my_list, param)
   else:
    delete_list.append(param)

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

#### Solution

##### Approach
Sort by deadline, use heap to always speed up the cheapest project first. When a deadline is missed, take time from the project with lowest speedup cost.

##### Python Solution

```python
import heapq

class Project:
 def __init__(self, a, b, d):
  self.a = a
  self.b = b
  self.d = d

 def __lt__(self, other):
  return self.a > other.a

def solution():
 t = int(input())

 for i in range(t):
  sum_money = 0
  initial_time = 0
  priority_queue = []
  projects = []
  n = int(input())
  for j in range(n):
   a, b, d = map(int, input().strip().split())
   projects.append(Project(a, b, d))
  projects.sort(key=lambda x: x.d, reverse=False)

  for j in range(n):
   initial_time += projects[j].b
   heapq.heappush(priority_queue, projects[j])
   if initial_time <= projects[j].d:
    continue
   while True:
    pop_project = heapq.heappop(priority_queue)
    if initial_time - pop_project.b <= projects[j].d:
     pop_project.b -= initial_time-projects[j].d
     sum_money += (initial_time-projects[j].d) / pop_project.a
     initial_time = projects[j].d
     heapq.heappush(priority_queue, pop_project)
     break
    else:
     sum_money += pop_project.b / pop_project.a
     initial_time -= pop_project.b

  print("{0:.2f}".format(sum_money))

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

#### Solution

##### Approach
Use two heaps (min and max) with lazy deletion to track receipts efficiently.

##### Python Solution

```python
import heapq

MAX = 1000005

def solution():
 n = int(input())
 sum_prizes = 0
 max_heap = []
 min_heap = []

 deleted_max = [0 for i in range(MAX)]
 deleted_min = [0 for i in range(MAX)]

 for i in range(n):
  line = list(map(int, input().strip().split()))
  num_rc = line[0]
  receipts = line[1:]
  for j in range(num_rc):
   heapq.heappush(min_heap, receipts[j])
   heapq.heappush(max_heap, -receipts[j])

  if len(max_heap) >= 2:
   from_max = heapq.heappop(max_heap)
   from_min = heapq.heappop(min_heap)
   while deleted_min[-from_max] > 0:
    deleted_min[-from_max] -= 1
    from_max = heapq.heappop(max_heap)
   while deleted_max[-from_min] > 0:
    deleted_max[-from_min] -= 1
    from_min = heapq.heappop(min_heap)

   deleted_max[from_max] += 1
   deleted_min[from_min] += 1

   sum_prizes -= (from_max + from_min)

 print(sum_prizes)

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

#### Solution

##### Approach
Simulate all three structures simultaneously and check consistency with each extraction.

##### Python Solution

```python
import heapq
import queue
import sys

class input_tokenizer:
 __tokens = None

 def has_next(self):
  return self.__tokens != [] and self.__tokens != None

 def next(self):
  token = self.__tokens[-1]
  self.__tokens.pop()
  return token

 def __init__(self):
  self.__tokens = sys.stdin.read().split()[::-1]

inp = input_tokenizer()

def solution():
 while inp.has_next():
  N = int(inp.next())
  my_heap = []
  my_queue = queue.Queue()
  mystack = []
  is_heap = 1
  is_stack = 1
  is_queue = 1
  for i in range(N):
   c_type = int(inp.next())
   x = int(inp.next())
   if is_stack + is_queue + is_heap == 0:
    continue
   if c_type == 1:
    if is_heap == 1:
     heapq.heappush(my_heap, -x)
    if is_stack == 1:
     mystack.append(x)
    if is_queue == 1:
     my_queue.put(x)
   else:
    if is_heap == 1:
     if len(my_heap) == 0 or -x != heapq.heappop(my_heap):
      is_heap = 0
    if is_stack == 1:
     if len(mystack) == 0 or x != mystack[-1]:
      is_stack = 0
     else:
      mystack.pop()
    if is_queue == 1:
     if my_queue.qsize() == 0 or x != my_queue.queue[0]:
      is_queue = 0
     else:
      my_queue.get()
  if is_heap + is_queue + is_stack > 1:
   print('not sure')
  elif is_heap + is_queue + is_stack == 0:
   print('impossible')
  else:
   if is_stack == 1:
    print('stack')
   if is_queue == 1:
    print('queue')
   if is_heap == 1:
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

#### Solution

##### Approach
Huffman-like algorithm - always add the two smallest numbers using a min-heap.

##### Python Solution

```python
import heapq

def solution():
 while True:
  N = int(input())
  if N == 0:
   return
  array = list(map(int, input().strip().split()))
  heapq.heapify(array)
  sum = 0
  while len(array) > 1:
   first = heapq.heappop(array)
   second = heapq.heappop(array)
   sum += (first + second)
   heapq.heappush(array, first + second)

  print(sum)

solution()
```

##### Complexity Analysis
- **Time Complexity:** O(N log N) for N-1 heap operations
- **Space Complexity:** O(N) for the heap
