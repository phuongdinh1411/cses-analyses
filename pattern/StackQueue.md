---
layout: simple
title: "Stack & Queue Patterns"
permalink: /pattern/stack-queue
---

# Stack & Queue Patterns — Comprehensive Guide

Stacks and queues are deceptively powerful. Beyond basic LIFO/FIFO operations, they unlock efficient solutions to problems involving **nearest elements**, **sliding windows**, **expression parsing**, and **histogram areas** --- problems that would otherwise require O(N^2) brute force.

---

## Quick Navigation: "I need to..."

| I need to... | Technique | Section |
|--------------|-----------|---------|
| Find **next greater/smaller** element | Monotonic Stack | [2](#2-monotonic-stack) |
| Find **previous greater/smaller** element | Monotonic Stack (iterate forward) | [2](#2-monotonic-stack) |
| **Sliding window** min/max | Monotonic Deque | [5](#5-monotonic-deque-sliding-window-minmax) |
| **Validate** brackets/parentheses | Stack matching | [3](#3-parentheses-and-bracket-matching) |
| **Evaluate** mathematical expressions | Stack-based parser | [4](#4-expression-evaluation) |
| **Largest rectangle** in histogram | Monotonic Stack | [6](#6-histogram-problems) |
| **Max rectangle** in binary matrix | Histogram + Monotonic Stack | [6](#6-histogram-problems) |
| **Stock span** / days until warmer | Monotonic Stack | [7](#7-stock-span-and-daily-temperatures) |
| **Sliding window** with sum/average | Queue / prefix sums | [8](#8-queue-patterns) |
| Process in **level order** | BFS queue | [8](#8-queue-patterns) |
| **Min stack** / **Max queue** | Augmented structures | [9](#9-augmented-stacks-and-queues) |
| **Trapping rain water** | Monotonic Stack or two pointers | [10](#10-trapping-rain-water) |

---

## Table of Contents

1. [Stack & Queue Fundamentals](#1-stack--queue-fundamentals)
2. [Monotonic Stack](#2-monotonic-stack)
3. [Parentheses and Bracket Matching](#3-parentheses-and-bracket-matching)
4. [Expression Evaluation](#4-expression-evaluation)
5. [Monotonic Deque (Sliding Window Min/Max)](#5-monotonic-deque-sliding-window-minmax)
6. [Histogram Problems](#6-histogram-problems)
7. [Stock Span and Daily Temperatures](#7-stock-span-and-daily-temperatures)
8. [Queue Patterns](#8-queue-patterns)
9. [Augmented Stacks and Queues](#9-augmented-stacks-and-queues)
10. [Trapping Rain Water](#10-trapping-rain-water)
11. [Pattern Recognition Cheat Sheet](#11-pattern-recognition-cheat-sheet)

---

## 1. Stack & Queue Fundamentals

### Stack (LIFO --- Last In, First Out)

```
Push 1, Push 2, Push 3:

  |  3  |  <-- top
  |  2  |
  |  1  |
  +-----+

Pop -> 3, Pop -> 2, Pop -> 1
```

```python
# Python: use a list
stack = []
stack.append(1)    # push
stack.append(2)
top = stack[-1]    # peek: 2
stack.pop()        # pop: 2
```

### Queue (FIFO --- First In, First Out)

```
Enqueue 1, 2, 3:

  Front -> [1, 2, 3] <- Back

Dequeue -> 1, Dequeue -> 2, Dequeue -> 3
```

```python
from collections import deque
queue = deque()
queue.append(1)     # enqueue (right)
queue.append(2)
front = queue[0]    # peek: 1
queue.popleft()     # dequeue: 1
```

### Deque (Double-Ended Queue)

```
Can push/pop from BOTH ends in O(1):

  Front <-> [1, 2, 3] <-> Back

appendleft / popleft  |  append / pop
```

```python
from collections import deque
dq = deque()
dq.append(3)        # add right
dq.appendleft(1)    # add left
dq.pop()            # remove right: 3
dq.popleft()        # remove left: 1
```

### Why Not Just Use Arrays?

| Operation | List | deque |
|-----------|------|-------|
| append (right) | O(1) | O(1) |
| pop (right) | O(1) | O(1) |
| insert (left) | **O(N)** | O(1) |
| pop (left) | **O(N)** | O(1) |

Use `deque` whenever you need O(1) operations at both ends.

---

## 2. Monotonic Stack

The single most important stack pattern. Solves a family of "nearest" problems in O(N).

### The Core Idea

A **monotonic stack** maintains elements in sorted order (either increasing or decreasing). When a new element violates the order, pop elements until the invariant is restored. The popped elements have found their "answer."

```
Monotonic DECREASING stack (for next greater element):

Array: [2, 1, 5, 6, 2, 3]

Process each element:
  2: stack empty, push             stack: [2]
  1: 1 < 2 (ok, maintain order)   stack: [2, 1]
  5: 5 > 1, pop 1 (next greater of 1 is 5)
     5 > 2, pop 2 (next greater of 2 is 5)
     push 5                        stack: [5]
  6: 6 > 5, pop 5 (next greater of 5 is 6)
     push 6                        stack: [6]
  2: 2 < 6, push                   stack: [6, 2]
  3: 3 > 2, pop 2 (next greater of 2 is 3)
     push 3                        stack: [6, 3]
  End: remaining in stack have no next greater -> -1

Result: [5, 5, 6, -1, 3, -1]
```

### 2.1 Next Greater Element

**Problem**: For each element, find the first element to its right that is larger.

```python
def next_greater(arr):
    n = len(arr)
    result = [-1] * n
    stack = []  # stores indices, elements in decreasing order

    for i in range(n):
        while stack and arr[stack[-1]] < arr[i]:
            idx = stack.pop()
            result[idx] = arr[i]
        stack.append(i)

    return result
```

```
arr:    [2, 1, 5, 6, 2, 3]
result: [5, 5, 6,-1, 3,-1]
```

### 2.2 Next Smaller Element

Flip the comparison. Use a monotonic **increasing** stack.

```python
def next_smaller(arr):
    n = len(arr)
    result = [-1] * n
    stack = []  # stores indices, elements in increasing order

    for i in range(n):
        while stack and arr[stack[-1]] > arr[i]:
            idx = stack.pop()
            result[idx] = arr[i]
        stack.append(i)

    return result
```

```
arr:    [4, 8, 5, 2, 25]
result: [2, 5, 2,-1, -1]
```

### 2.3 Previous Greater Element

Iterate **forward** (same direction), but the answer is what's already on the stack when you push.

```python
def previous_greater(arr):
    n = len(arr)
    result = [-1] * n
    stack = []  # decreasing stack

    for i in range(n):
        while stack and arr[stack[-1]] <= arr[i]:
            stack.pop()
        result[i] = arr[stack[-1]] if stack else -1
        stack.append(i)

    return result
```

```
arr:    [10, 4, 2, 20, 40, 12, 30]
result: [-1,10,4, -1, -1, 40, 40]
```

### 2.4 Previous Smaller Element

```python
def previous_smaller(arr):
    n = len(arr)
    result = [-1] * n
    stack = []  # increasing stack

    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        result[i] = arr[stack[-1]] if stack else -1
        stack.append(i)

    return result
```

### The Complete Monotonic Stack Family

| Problem | Stack type | When to pop | Answer for popped | Answer from stack top |
|---------|-----------|-------------|-------------------|-----------------------|
| **Next greater** | Decreasing | `arr[stack[-1]] < arr[i]` | Popped element's next greater = arr[i] | --- |
| **Next smaller** | Increasing | `arr[stack[-1]] > arr[i]` | Popped element's next smaller = arr[i] | --- |
| **Previous greater** | Decreasing | `arr[stack[-1]] <= arr[i]` | --- | stack top after pops = prev greater of i |
| **Previous smaller** | Increasing | `arr[stack[-1]] >= arr[i]` | --- | stack top after pops = prev smaller of i |

### The Key Insight

```
When you pop element X because of element Y:
  - Y is the NEXT greater/smaller of X (depending on stack type)
  - The new stack top is the PREVIOUS greater/smaller of X

One pass gives you TWO pieces of information per element!
```

### Circular Array Variant

For circular arrays, iterate the array **twice** (indices 0 to 2N-1):

```python
def next_greater_circular(arr):
    n = len(arr)
    result = [-1] * n
    stack = []

    for i in range(2 * n):
        while stack and arr[stack[-1]] < arr[i % n]:
            idx = stack.pop()
            result[idx] = arr[i % n]
        if i < n:
            stack.append(i)

    return result
```

```
arr:    [1, 2, 1]
result: [2,-1, 2]  (circular: after arr[2]=1, next is arr[0]=1, then arr[1]=2)
```

---

## 3. Parentheses and Bracket Matching

### Valid Parentheses

```python
def is_valid(s):
    stack = []
    pairs = {')': '(', ']': '[', '}': '{'}

    for ch in s:
        if ch in '([{':
            stack.append(ch)
        elif ch in ')]}':
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()

    return len(stack) == 0
```

### Minimum Removals to Make Valid

```python
def min_removals(s):
    stack = []  # indices of unmatched parentheses

    for i, ch in enumerate(s):
        if ch == '(':
            stack.append(i)
        elif ch == ')':
            if stack and s[stack[-1]] == '(':
                stack.pop()
            else:
                stack.append(i)

    return len(stack)  # all unmatched
```

### Longest Valid Parentheses

```python
def longest_valid_parentheses(s):
    stack = [-1]  # sentinel: index before the start of current valid sequence
    max_len = 0

    for i, ch in enumerate(s):
        if ch == '(':
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)  # new sentinel
            else:
                max_len = max(max_len, i - stack[-1])

    return max_len
```

```
s = ")()())"

i=0 ')': pop -1, stack empty -> push 0 as sentinel  stack: [0]
i=1 '(': push 1                                      stack: [0, 1]
i=2 ')': pop 1, length = 2-0 = 2                     stack: [0]
i=3 '(': push 3                                      stack: [0, 3]
i=4 ')': pop 3, length = 4-0 = 4                     stack: [0]
i=5 ')': pop 0, stack empty -> push 5                 stack: [5]

Answer: 4
```

### Score of Parentheses

```
() = 1
(()) = 2 * 1 = 2
()() = 1 + 1 = 2
(()(()))  = 2 * (1 + 2*1) = 6
```

```python
def score_of_parentheses(s):
    stack = [0]  # current depth's score

    for ch in s:
        if ch == '(':
            stack.append(0)  # start new depth
        else:
            inner = stack.pop()
            stack[-1] += max(1, 2 * inner)

    return stack[0]
```

---

## 4. Expression Evaluation

### Infix Evaluation (with precedence)

```
Input: "3 + 2 * 4 - 1"
       = 3 + 8 - 1
       = 10
```

Use two stacks: one for numbers, one for operators.

```python
def evaluate(expression):
    def precedence(op):
        if op in ('+', '-'):
            return 1
        if op in ('*', '/'):
            return 2
        return 0

    def apply_op(ops, vals):
        op = ops.pop()
        b = vals.pop()
        a = vals.pop()
        if op == '+': vals.append(a + b)
        elif op == '-': vals.append(a - b)
        elif op == '*': vals.append(a * b)
        elif op == '/': vals.append(int(a / b))

    vals = []
    ops = []
    i = 0
    tokens = expression.replace(' ', '')

    while i < len(tokens):
        if tokens[i].isdigit():
            num = 0
            while i < len(tokens) and tokens[i].isdigit():
                num = num * 10 + int(tokens[i])
                i += 1
            vals.append(num)
            continue

        if tokens[i] == '(':
            ops.append('(')
        elif tokens[i] == ')':
            while ops[-1] != '(':
                apply_op(ops, vals)
            ops.pop()  # remove '('
        else:
            while ops and ops[-1] != '(' and precedence(ops[-1]) >= precedence(tokens[i]):
                apply_op(ops, vals)
            ops.append(tokens[i])
        i += 1

    while ops:
        apply_op(ops, vals)

    return vals[0]
```

### Infix to Postfix (Shunting Yard)

```
Infix:    3 + 4 * 2 / (1 - 5)
Postfix:  3 4 2 * 1 5 - / +
```

```python
def infix_to_postfix(tokens):
    output = []
    ops = []
    prec = {'+': 1, '-': 1, '*': 2, '/': 2}

    for token in tokens:
        if isinstance(token, (int, float)):
            output.append(token)
        elif token == '(':
            ops.append(token)
        elif token == ')':
            while ops[-1] != '(':
                output.append(ops.pop())
            ops.pop()
        else:
            while ops and ops[-1] != '(' and prec.get(ops[-1], 0) >= prec[token]:
                output.append(ops.pop())
            ops.append(token)

    while ops:
        output.append(ops.pop())

    return output
```

### Postfix Evaluation

```python
def eval_postfix(tokens):
    stack = []
    for token in tokens:
        if isinstance(token, (int, float)):
            stack.append(token)
        else:
            b, a = stack.pop(), stack.pop()
            if token == '+': stack.append(a + b)
            elif token == '-': stack.append(a - b)
            elif token == '*': stack.append(a * b)
            elif token == '/': stack.append(int(a / b))
    return stack[0]
```

---

## 5. Monotonic Deque (Sliding Window Min/Max)

The queue counterpart of monotonic stack. Maintains a window's min or max in **O(1) per element**.

### The Core Idea

Maintain a deque of indices. The front is always the current window's min (or max). Remove from the back when a new element makes old elements irrelevant. Remove from the front when the element leaves the window.

```
Sliding window max, window size k=3:

arr: [1, 3, -1, -3, 5, 3, 6, 7]

Window [1,3,-1]:
  deque maintains DECREASING order of values
  deque (indices): [1]  (index of 3 -- 1 and -1 are smaller, irrelevant)
  max = arr[deque[0]] = 3

Window [3,-1,-3]:
  deque: [1, 2]  wait... let me trace properly
```

### Sliding Window Maximum

```python
from collections import deque

def max_sliding_window(arr, k):
    dq = deque()  # stores indices, values in DECREASING order
    result = []

    for i in range(len(arr)):
        # Remove elements outside the window
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        # Remove elements smaller than arr[i] from back
        # (they can never be the max while arr[i] is in the window)
        while dq and arr[dq[-1]] <= arr[i]:
            dq.pop()

        dq.append(i)

        # Window is full (i >= k-1), record the max
        if i >= k - 1:
            result.append(arr[dq[0]])

    return result
```

### Trace

```
arr = [1, 3, -1, -3, 5, 3, 6, 7],  k = 3

i=0: arr[0]=1,  dq=[0]                          (not full yet)
i=1: arr[1]=3,  pop 0 (1<3), dq=[1]             (not full yet)
i=2: arr[2]=-1, dq=[1,2]                        result: [3]   (max=arr[1]=3)
i=3: arr[3]=-3, dq=[1,2,3]                      result: [3,3] (max=arr[1]=3)
i=4: arr[4]=5,  pop 3,2,1 (all<5), dq=[4]       result: [3,3,5]
i=5: arr[5]=3,  dq=[4,5]                        result: [3,3,5,5]
i=6: arr[6]=6,  pop 5,4 (all<6), dq=[6]         result: [3,3,5,5,6]
i=7: arr[7]=7,  pop 6 (6<7), dq=[7]             result: [3,3,5,5,6,7]
```

### Sliding Window Minimum

Flip the comparison: maintain **increasing** order in the deque.

```python
from collections import deque

def min_sliding_window(arr, k):
    dq = deque()  # stores indices, values in INCREASING order
    result = []

    for i in range(len(arr)):
        while dq and dq[0] < i - k + 1:
            dq.popleft()

        while dq and arr[dq[-1]] >= arr[i]:
            dq.pop()

        dq.append(i)

        if i >= k - 1:
            result.append(arr[dq[0]])

    return result
```

### Why It's O(N)

Each element is pushed into the deque **once** and popped **at most once**. Total operations: 2N. Even though there's a while loop inside the for loop, the total work across all iterations is O(N).

### Monotonic Deque vs Monotonic Stack

| | Monotonic Stack | Monotonic Deque |
|--|----------------|-----------------|
| Structure | Stack (one end) | Deque (both ends) |
| Window | Unbounded (all previous) | Fixed size k |
| Remove from | Back only | Front (expired) + Back (dominated) |
| Finds | Next/previous greater/smaller | Sliding window min/max |
| Time | O(N) total | O(N) total |

---

## 6. Histogram Problems

### Largest Rectangle in Histogram

**Problem**: Given bars of varying heights, find the largest rectangular area.

```
Heights: [2, 1, 5, 6, 2, 3]

     _
    | |
  _ | |
 | || |   _
 | || | _ | |
_| || || || |
|_||_||_||_||_|
 2  1  5  6  2  3

Largest rectangle: 5x2 = 10 (bars of height 5 and 6)
```

**Key insight**: For each bar, find how far it can extend left and right (i.e., the nearest shorter bar on each side). This is exactly **previous smaller** + **next smaller**.

```python
def largest_rectangle_histogram(heights):
    n = len(heights)
    stack = []  # monotonic increasing stack of indices
    max_area = 0

    for i in range(n + 1):
        h = heights[i] if i < n else 0  # sentinel: force empty the stack

        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            # width: from (stack top + 1) to (i - 1)
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)

        stack.append(i)

    return max_area
```

### Trace

```
heights = [2, 1, 5, 6, 2, 3]

i=0: h=2, push          stack: [0]
i=1: h=1, pop 0 (h=2)   area = 2*1 = 2     stack: [1]
i=2: h=5, push           stack: [1, 2]
i=3: h=6, push           stack: [1, 2, 3]
i=4: h=2, pop 3 (h=6)    area = 6*1 = 6
          pop 2 (h=5)    area = 5*2 = 10    stack: [1, 4]
i=5: h=3, push           stack: [1, 4, 5]
i=6: h=0 (sentinel)
     pop 5 (h=3)    area = 3*1 = 3
     pop 4 (h=2)    area = 2*4 = 8
     pop 1 (h=1)    area = 1*6 = 6

Max area = 10
```

### Why Width Calculation Works

When we pop index `j` because of index `i`:
- `i` is the **next smaller** on the right
- `stack[-1]` (after pop) is the **previous smaller** on the left
- Width = `i - stack[-1] - 1` (everything between the two boundaries)

```
heights:   ... [3] [5] [6] [2] ...
indices:   ...  a   j        i  ...

Pop j (height 5) because of i (height 2):
  Left boundary: a (previous smaller)
  Right boundary: i (next smaller)
  Width = i - a - 1
```

### Maximal Rectangle in Binary Matrix

**Problem**: Find the largest rectangle of 1s in a binary matrix.

**Reduction**: Treat each row as the base of a histogram. Build up heights row by row, apply histogram algorithm.

```python
def maximal_rectangle(matrix):
    if not matrix:
        return 0
    m, n = len(matrix), len(matrix[0])
    heights = [0] * n
    max_area = 0

    for i in range(m):
        for j in range(n):
            heights[j] = heights[j] + 1 if matrix[i][j] == 1 else 0

        max_area = max(max_area, largest_rectangle_histogram(heights))

    return max_area
```

```
Matrix:         Heights row by row:
1 0 1 0 0       [1, 0, 1, 0, 0]  -> max rect = 1
1 0 1 1 1       [2, 0, 2, 1, 1]  -> max rect = 3
1 1 1 1 1       [3, 1, 3, 2, 2]  -> max rect = 6
1 0 0 1 0       [4, 0, 0, 3, 0]  -> max rect = 3

Answer: 6 (3x2 block in row 3)
```

---

## 7. Stock Span and Daily Temperatures

### Stock Span

**Problem**: For each day, how many consecutive days before it had a price <= today's price?

```
Prices:  [100, 80, 60, 70, 60, 75, 85]
Spans:   [  1,  1,  1,  2,  1,  4,  6]
                          ^        ^
                        60,70    60,70,60,75,80,85? No...
```

This is **previous greater** in disguise: span = distance to the previous day with a strictly higher price.

```python
def stock_span(prices):
    n = len(prices)
    span = [0] * n
    stack = []  # decreasing stack of indices

    for i in range(n):
        while stack and prices[stack[-1]] <= prices[i]:
            stack.pop()
        span[i] = i + 1 if not stack else i - stack[-1]
        stack.append(i)

    return span
```

### Daily Temperatures

**Problem**: For each day, how many days until a warmer temperature?

This is **next greater element** returning the distance.

```python
def daily_temperatures(temps):
    n = len(temps)
    result = [0] * n
    stack = []  # decreasing stack of indices

    for i in range(n):
        while stack and temps[stack[-1]] < temps[i]:
            idx = stack.pop()
            result[idx] = i - idx
        stack.append(i)

    return result
```

```
temps:  [73, 74, 75, 71, 69, 72, 76, 73]
result: [ 1,  1,  4,  2,  1,  1,  0,  0]
```

---

## 8. Queue Patterns

### BFS (Breadth-First Search)

The most fundamental queue pattern. Process nodes level by level.

```python
from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

### Level-Order Processing

When you need to process each level separately:

```python
def bfs_by_level(graph, start):
    visited = {start}
    queue = deque([start])
    level = 0

    while queue:
        size = len(queue)  # number of nodes at current level
        for _ in range(size):
            node = queue.popleft()
            # process node at this level
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        level += 1
```

### Task Scheduling / Process Queue

```python
from collections import deque

def round_robin(tasks, quantum):
    """Simulate round-robin CPU scheduling."""
    queue = deque(tasks)  # (task_name, remaining_time)
    time = 0
    order = []

    while queue:
        name, remaining = queue.popleft()
        run = min(quantum, remaining)
        time += run
        remaining -= run
        if remaining > 0:
            queue.append((name, remaining))
        else:
            order.append((name, time))

    return order
```

### Recent Counter (Sliding Window with Queue)

```python
class RecentCounter:
    """Count requests in the last 3000 ms."""
    def __init__(self):
        self.queue = deque()

    def ping(self, t):
        self.queue.append(t)
        while self.queue[0] < t - 3000:
            self.queue.popleft()
        return len(self.queue)
```

---

## 9. Augmented Stacks and Queues

### Min Stack (O(1) getMin)

```python
class MinStack:
    def __init__(self):
        self.stack = []     # (value, current_min)

    def push(self, val):
        curr_min = min(val, self.stack[-1][1]) if self.stack else val
        self.stack.append((val, curr_min))

    def pop(self):
        return self.stack.pop()[0]

    def top(self):
        return self.stack[-1][0]

    def get_min(self):
        return self.stack[-1][1]
```

### Max Stack (O(1) getMax)

Same idea: store `(value, current_max)` pairs.

### Min Queue (O(1) amortized getMin)

Use **two stacks** to simulate a queue, each stack tracking its min.

```python
class MinQueue:
    """Queue with O(1) amortized min query."""
    def __init__(self):
        self.push_stack = []   # (val, min_so_far)
        self.pop_stack = []    # (val, min_so_far)

    def enqueue(self, val):
        curr_min = min(val, self.push_stack[-1][1]) if self.push_stack else val
        self.push_stack.append((val, curr_min))

    def dequeue(self):
        if not self.pop_stack:
            while self.push_stack:
                val, _ = self.push_stack.pop()
                curr_min = min(val, self.pop_stack[-1][1]) if self.pop_stack else val
                self.pop_stack.append((val, curr_min))
        return self.pop_stack.pop()[0]

    def get_min(self):
        if self.push_stack and self.pop_stack:
            return min(self.push_stack[-1][1], self.pop_stack[-1][1])
        elif self.push_stack:
            return self.push_stack[-1][1]
        else:
            return self.pop_stack[-1][1]
```

### Two Stacks = One Queue

The classic trick: a push stack and a pop stack. When pop stack is empty, pour all elements from push stack (reversing the order).

```
Enqueue 1, 2, 3:     push_stack: [1, 2, 3]    pop_stack: []
Dequeue:              push_stack: []            pop_stack: [3, 2, 1]
                      pop from pop_stack -> 1 (correct FIFO order!)
```

Amortized O(1) per operation: each element is moved at most once from push to pop stack.

---

## 10. Trapping Rain Water

A classic that combines multiple stack/pointer techniques.

### Approach 1: Monotonic Stack

```python
def trap_stack(height):
    stack = []  # decreasing stack of indices
    water = 0

    for i in range(len(height)):
        while stack and height[stack[-1]] < height[i]:
            bottom = stack.pop()
            if not stack:
                break
            width = i - stack[-1] - 1
            bounded_height = min(height[i], height[stack[-1]]) - height[bottom]
            water += width * bounded_height

        stack.append(i)

    return water
```

### How It Works

```
height: [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]

When we pop index 2 (h=0) because of index 3 (h=2):
  bottom = height[2] = 0
  left wall = height[stack[-1]] = height[1] = 1
  right wall = height[3] = 2
  water level = min(1, 2) - 0 = 1
  width = 3 - 1 - 1 = 1
  water += 1 * 1 = 1

We compute water LAYER BY LAYER, horizontally.
```

### Approach 2: Two Pointers (O(1) space)

```python
def trap_two_pointers(height):
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0

    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1

    return water
```

### Approach 3: Prefix Max Arrays

```python
def trap_prefix(height):
    n = len(height)
    left_max = [0] * n
    right_max = [0] * n

    left_max[0] = height[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i-1], height[i])

    right_max[n-1] = height[n-1]
    for i in range(n-2, -1, -1):
        right_max[i] = max(right_max[i+1], height[i])

    water = 0
    for i in range(n):
        water += min(left_max[i], right_max[i]) - height[i]

    return water
```

### Comparison

| Approach | Time | Space | Idea |
|----------|------|-------|------|
| Monotonic Stack | O(N) | O(N) | Horizontal layers between walls |
| Two Pointers | O(N) | O(1) | Process from both ends inward |
| Prefix Max | O(N) | O(N) | Water at each position = min(left_max, right_max) - height |

---

## 11. Pattern Recognition Cheat Sheet

### By Problem Type

| You see... | Think... | Section |
|------------|----------|---------|
| "Next greater/smaller element" | Monotonic Stack | 2 |
| "Previous greater/smaller element" | Monotonic Stack | 2 |
| "Sliding window min/max" | Monotonic Deque | 5 |
| "Valid parentheses" | Stack matching | 3 |
| "Evaluate expression" | Two stacks (values + ops) | 4 |
| "Largest rectangle in histogram" | Monotonic Stack (increasing) | 6 |
| "Maximal rectangle in matrix" | Row histograms + monotonic stack | 6 |
| "Stock span" / "days until warmer" | Monotonic Stack (decreasing) | 7 |
| "Trapping rain water" | Stack / Two Pointers / Prefix Max | 10 |
| "Process level by level" | BFS with queue | 8 |
| "Min/Max in O(1) with push/pop" | Augmented Stack | 9 |
| "Min/Max in O(1) with enqueue/dequeue" | Augmented Queue (2 stacks) | 9 |

### Monotonic Stack Decision Table

| Problem | Stack Order | Iterate Direction | Answer Location |
|---------|-------------|-------------------|-----------------|
| Next greater | Decreasing | Left to right | On pop: `arr[i]` is the answer |
| Next smaller | Increasing | Left to right | On pop: `arr[i]` is the answer |
| Previous greater | Decreasing | Left to right | Stack top is the answer |
| Previous smaller | Increasing | Left to right | Stack top is the answer |
| Largest rectangle | Increasing | Left to right | On pop: compute width x height |
| Trapping water | Decreasing | Left to right | On pop: compute trapped water |

### Complexity Summary

| Pattern | Time | Space |
|---------|------|-------|
| Monotonic Stack (any variant) | O(N) | O(N) |
| Monotonic Deque (sliding window) | O(N) | O(K) where K = window size |
| Bracket matching | O(N) | O(N) |
| Expression evaluation | O(N) | O(N) |
| Histogram largest rectangle | O(N) | O(N) |
| Maximal rectangle in matrix | O(MN) | O(N) |
| Min Stack / Max Stack | O(1) per op | O(N) |
| Min Queue (two stacks) | O(1) amortized | O(N) |
| Trapping rain water | O(N) | O(1) to O(N) |

### The Meta-Pattern

Almost every stack/queue problem follows this template:

```
for each element:
    while stack/deque is not empty AND current element violates the invariant:
        pop and COMPUTE ANSWER for popped element
    push current element
```

The "invariant" is either increasing or decreasing order. The "answer computation" varies by problem (next greater, rectangle area, trapped water, etc.), but the structure is always the same.
