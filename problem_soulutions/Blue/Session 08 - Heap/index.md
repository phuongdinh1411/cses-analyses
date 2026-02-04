---
layout: simple
title: "Session 08 - Heap"
permalink: /problem_soulutions/Blue/Session 08 - Heap/
---

# Session 08 - Heap

This session covers heap data structure and priority queue operations, including min-heap, max-heap, and heap-based algorithms.

## Problems

### RRATING (Codechef)

```python
# Problem from CodeChef
# https://www.codechef.com/problems/RRATING
#
# Problem: Restaurant Rating
#
# A restaurant receives reviews with ratings. After each review, they want
# to display the rating at the top 1/3 position (ceiling). For example, if
# there are 5 reviews, show the rating at position ceil(5/3) = 2 from top.
#
# Operations:
# - "1 x": Add a review with rating x
# - "2": Query the rating at top 1/3 position (or "No reviews yet" if empty)
#
# Input:
# - Line 1: N (number of operations)
# - Next N lines: Operations as described above
#
# Output: For each query (type 2), print the answer
#
# Approach: Use two heaps - one for top 1/3 ratings (min-heap), another for
#           candidates (max-heap). Keep balance as reviews are added.


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

### monk-and-multiplication (Hackerearth)

```python
#  Problem from Hackerearth
#  https://www.hackerearth.com/fr/practice/data-structures/trees/heapspriority-queues/practice-problems/algorithm/monk-and-multiplication/
#
# Problem: Monk and Multiplication
#
# Given an array of N integers added one by one, after each insertion output
# the product of the three largest numbers. If fewer than 3 numbers have been
# added, output -1.
#
# Input:
# - Line 1: N (number of elements)
# - Line 2: N space-separated integers
#
# Output: N lines, each containing the product of 3 largest so far, or -1
#
# Approach: Maintain a min-heap of size 3 with the largest elements


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

### trending (Hackerearth)

```python
#  Problem from Hackerearth
#  https://www.hackerearth.com/fr/practice/data-structures/trees/heapspriority-queues/practice-problems/algorithm/roy-and-trending-topics-1/description/
#
# Problem: Roy and Trending Topics
#
# Given N topics with current scores and engagement data (posts, likes,
# comments, shares), calculate new scores using:
#   new_score = posts*50 + likes*5 + comments*10 + shares*20
#
# Find the top 5 trending topics based on the CHANGE in score (new - old).
# Ties are broken by higher topic ID.
#
# Input:
# - Line 1: N (number of topics)
# - Next N lines: topic_id current_score posts likes comments shares
#
# Output: Top 5 topics with their new scores (highest change first)
#
# Approach: Min-heap of size 5 tracking top trending by score change


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

### qheap1 (Hackerrank)

```python
#  Problem from Hackerrank
#  https://www.hackerrank.com/challenges/qheap1/problem
#
# Problem: QHEAP1
#
# Implement a min-heap that supports the following operations:
# - "1 v": Add element v to the heap
# - "2 v": Delete element v from the heap (v is guaranteed to exist)
# - "3": Print the minimum element
#
# Input:
# - Line 1: Q (number of queries)
# - Next Q lines: Queries as described above
#
# Output: For each type-3 query, print the minimum element
#
# Approach: Use a heap with lazy deletion (track deleted elements separately)


#  Using not in and index is faster than checking manually using for loop
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


#
# from queue import PriorityQueue
#
# def main():
#     n = int(input())
#     q = PriorityQueue()
#     remove = []
#     for i in range(n):
#         line = list(map(int, input().split()))
#         if line[0] == 1:
#             q.put(line[1])
#         elif line[0] == 2:
#             remove.append(line[1])
#         else:
#             while q.queue[0] in remove:
#                 remove.pop(remove.index(q.get()))
#             print(q.queue[0])
#
# if __name__ == '__main__':
#     main()
```

### LAZYPROG (SPOJ)

```python
#  Problem from SPOJ
#  https://www.spoj.com/problems/LAZYPROG/
#
# Problem: LAZYPROG - Lazy Programmer
#
# A lazy programmer has N projects with deadlines. Each project i has:
# - a[i]: cost per unit time to speed up (dollars/hour)
# - b[i]: time needed to complete at normal speed (hours)
# - d[i]: deadline (hours from now)
#
# He can pay to speed up any project. Find the minimum total cost to meet
# all deadlines.
#
# Input:
# - Line 1: T (test cases)
# - For each test case:
#   - Line 1: N (number of projects)
#   - Next N lines: a b d for each project
#
# Output: Minimum cost (2 decimal places)
#
# Approach: Sort by deadline, use heap to always speed up cheapest project first


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

### PRO (SPOJ)

```python
#  Problem from SPOJ
#  https://www.spoj.com/problems/PRO/
#
# Problem: PRO - Promotion
#
# A supermarket runs a promotion over N days. Each day, some customers submit
# receipts. At the end of each day, the customer with the highest receipt wins
# prize equal to receipt value, and the lowest receipt customer wins prize
# equal to their receipt value (both are removed from future consideration).
#
# Calculate total prize money: sum(max) - sum(min) over all days.
#
# Input:
# - Line 1: N (number of days)
# - Next N lines: k r1 r2 ... rk (k receipts for that day)
#
# Output: Total prize difference
#
# Approach: Use two heaps (min and max) with lazy deletion to track receipts


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

### 11995 (UVA)

```python
#  Problem from UVA
#  https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3146
#
# Problem: UVA 11995 - I Can Guess the Data Structure!
#
# Given a sequence of operations (insert and extract), determine what data
# structure is being used: stack, queue, or priority queue (max-heap).
#
# Operations:
# - "1 x": Insert element x
# - "2 x": Extract returns element x
#
# Output:
# - "stack" if it matches stack behavior (LIFO)
# - "queue" if it matches queue behavior (FIFO)
# - "priority queue" if it matches max-heap behavior
# - "not sure" if multiple structures are possible
# - "impossible" if no structure matches
#
# Input: Multiple test cases until EOF, each with N operations
#
# Output: One line per test case
#
# Approach: Simulate all three structures and check consistency


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

### AddAll (UVA)

```python
#  Problem from UVA
#  https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1895
#
# Problem: UVA 10954 - Add All
#
# Given N numbers, you need to add them all together. Each addition operation
# costs the sum of the two numbers being added. Find the minimum total cost
# to combine all numbers into one.
#
# Input:
# - Multiple test cases until N=0
# - Line 1: N
# - Line 2: N integers
#
# Output: Minimum total cost for each test case
#
# Example: Numbers [1, 2, 3] -> Add 1+2=3 (cost 3), then 3+3=6 (cost 6) = 9
#          Better: Add 1+2=3 (cost 3), then 3+3=6 (cost 6) = 9
#          Or: 1+3=4 (cost 4), 4+2=6 (cost 6) = 10 (worse)
#
# Approach: Huffman-like algorithm - always add two smallest (use min-heap)


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

