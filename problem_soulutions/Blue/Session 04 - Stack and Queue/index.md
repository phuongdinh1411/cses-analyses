---
layout: simple
title: "Stack and Queue"
permalink: /problem_soulutions/Blue/Session 04 - Stack and Queue/
---

# Stack and Queue

This session covers stack and queue data structures, including LIFO/FIFO operations, expression parsing, and simulation problems.

## Problems

### Compilers and Parsers

#### Problem Information
- **Source:** [CodeChef COMPILER](https://www.codechef.com/problems/COMPILER)
- **Difficulty:** Easy

#### Problem Statement
Lira is designing a language L++ where expressions consist of "<" and ">" characters. For an expression to be valid, a "<" symbol must always have a corresponding ">" character somewhere after it. Each ">" symbol should correspond to exactly one "<" symbol.

Given some expressions, find the length of the longest prefix of each expression that is valid.

#### Input Format
- First line: T (number of test cases)
- Next T lines: One expression per line

#### Output Format
For each expression, output the length of the longest valid prefix, or 0 if there's no such prefix.

#### Example
```
Input:
2
<<>>
><

Output:
4
0
```
"<<>>" is fully valid (length 4). "><" starts with ">" which is invalid, so longest valid prefix is 0.

```
Input:
1
<<><>>

Output:
6
```
The entire string is valid.

#### Solution

##### Approach
Use a stack to track unmatched "<" characters. Pop when ">" is encountered. Track the longest valid prefix when the stack is empty.

##### Python Solution
```python
T = int(input())

results = []
for _ in range(T):
    exp = input().strip()
    stack_depth = 0
    length = 0
    max_valid = 0

    for char in exp:
        if char == '<':
            stack_depth += 1
            length += 1
        elif char == '>':
            if not stack_depth:
                break
            stack_depth -= 1
            length += 1
            if stack_depth == 0:
                max_valid = length

    results.append(max_valid)

print(*results, sep='\n')
```

##### Complexity Analysis
- **Time Complexity:** O(n) - single pass through each expression
- **Space Complexity:** O(n) - stack size at most n/2

---

### Processing Time

#### Problem Information
- **Source:** [Codeforces 644B](https://codeforces.com/problemset/problem/644/B)
- **Difficulty:** Medium

#### Problem Statement
Simulate a one-thread server processing n queries. Each query arrives at time ti and needs di time to process. The server has a queue of size b. If the queue is full, queries are rejected. Determine when each query finishes processing or if it's rejected.

#### Input Format
- First line: n b (number of queries, queue size)
- Next n lines: ti di (arrival time and processing duration for each query)

#### Output Format
For each query, output the finish time or -1 if rejected.

#### Example
```
Input:
5 2
2 9
4 8
10 9
15 2
19 1

Output:
11 19 -1 21 22
```
Query 1 arrives at t=2, finishes at 2+9=11. Query 2 queued, finishes at 11+8=19. Query 3 arrives when queue is full, rejected. Etc.

#### Solution

##### Approach
Use a queue to simulate the server's pending requests. Process queries as they arrive and track when each completes.

##### Python Solution
```python
from collections import deque

n, b = map(int, input().split())
result = [0] * n
last_processing = 0
waiting_queue = deque()

for i in range(n):
    ti, di = map(int, input().split())

    while waiting_queue and last_processing <= ti:
        idx, time, duration = waiting_queue.popleft()
        last_processing = max(last_processing, time) + duration
        result[idx] = last_processing

    if len(waiting_queue) < b:
        waiting_queue.append((i, ti, di))
    else:
        result[i] = -1

while waiting_queue:
    idx, time, duration = waiting_queue.popleft()
    last_processing = max(last_processing, time) + duration
    result[idx] = last_processing

print(*result)
```

##### Complexity Analysis
- **Time Complexity:** O(n) - each query is processed once
- **Space Complexity:** O(b) - queue size limited to b

---

### Mass of Molecule

#### Problem Information
- **Source:** [SPOJ MMASS](https://www.spoj.com/problems/MMASS/)
- **Difficulty:** Medium

#### Problem Statement
Calculate the mass of a molecule from its chemical formula. The formula consists of H (mass 1), C (mass 12), O (mass 16), parentheses for grouping, and numbers 2-9 for multipliers. Calculate the total mass of the molecule.

#### Input Format
A single line containing the chemical formula.

#### Output Format
The total mass of the molecule.

#### Example
```
Input:
WATER

Output:
18
```
W is not a valid atom. Actually the input should be like H2O. Let me use a valid example:

```
Input:
H2O

Output:
18
```
H=1, so H2=2. O=16. Total = 2 + 16 = 18.

```
Input:
Ca(OH)2

Output:
74
```
Ca=40, O=16, H=1. Ca + 2×(O+H) = 40 + 2×17 = 74.

#### Solution

##### Approach
Use a stack to handle nested parentheses. Process the formula character by character, multiplying masses when digits are encountered.

##### Python Solution
```python
ATOM_MASS = {'H': 1, 'O': 16, 'C': 12}

formula = input().strip()
stack = []

for i, char in enumerate(formula):
    if char == '(':
        stack.append(char)
    elif char == ')':
        total = 0
        while stack and stack[-1] != '(':
            total += stack.pop()
        if stack:
            stack.pop()  # Remove '('
        stack.append(total)
    elif char in ATOM_MASS:
        mass = ATOM_MASS[char]
        if stack and isinstance(stack[-1], int) and i < len(formula) - 1 and not formula[i + 1].isdigit():
            stack[-1] += mass
        else:
            stack.append(mass)
    elif char.isdigit():
        if isinstance(stack[-1], int):
            stack[-1] *= int(char)

print(sum(stack))
```

##### Complexity Analysis
- **Time Complexity:** O(n) - single pass through the formula
- **Space Complexity:** O(n) - stack size for nested parentheses

---

### Transform to RPN

#### Problem Information
- **Source:** [SPOJ ONP](https://www.spoj.com/problems/ONP/)
- **Difficulty:** Medium

#### Problem Statement
Transform algebraic expressions with brackets into Reverse Polish Notation (RPN). Operators are +, -, *, /, ^ (priority from lowest to highest). Operands are lowercase letters a-z.

#### Input Format
- First line: t (number of expressions)
- Next t lines: One expression per line

#### Output Format
The expressions in RPN form, one per line.

#### Example
```
Input:
3
(a+(b*c))
((a+b)*(z+x))
((a+t)*((b+(a+c))^(c+d)))

Output:
abc*+
ab+zx+*
at+bac++cd+^*
```
Infix "(a+(b*c))" becomes postfix "abc*+" - operands appear, then operators in correct precedence order.

#### Solution

##### Approach
Use the Shunting Yard algorithm with a stack for operators. Output operands immediately, push operators based on precedence.

##### Python Solution
```python
n = int(input())
results = []

PRIORITY = {'+': 1, '-': 2, '*': 3, '/': 4, '^': 5}

for _ in range(n):
    exp = input()
    output = []
    stack = []

    for char in exp:
        if char.isalpha():
            output.append(char)
        elif char in PRIORITY:
            while stack and PRIORITY.get(stack[-1], 0) >= PRIORITY[char]:
                output.append(stack.pop())
            stack.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack:
                stack.pop()  # Remove '('

    while stack:
        output.append(stack.pop())

    results.append(''.join(output))

print(*results, sep='\n')
```

##### Complexity Analysis
- **Time Complexity:** O(n) - single pass through each expression
- **Space Complexity:** O(n) - stack for operators

---

### Street Parade

#### Problem Information
- **Source:** [SPOJ STPAR](https://www.spoj.com/problems/STPAR/)
- **Difficulty:** Medium

#### Problem Statement
Love mobiles need to be arranged in order 1 to n for a parade. They arrive in a given order and can use a side street (stack) to help reorder. Determine if the trucks can be arranged in the correct order.

#### Input Format
- First line: n (number of trucks, 0 to end)
- Second line: n integers (arrival order)

#### Output Format
"yes" if reordering is possible, "no" otherwise.

#### Example
```
Input:
5
5 1 2 4 3
0

Output:
yes
```
Arrival: 5,1,2,4,3. Push 5 to stack, output 1, output 2, push 4 to stack, push 3 to stack. Pop 3, pop 4, pop 5. Final order: 1,2,3,4,5.

```
Input:
5
4 1 5 3 2
0

Output:
no
```
Cannot reorder to 1,2,3,4,5 using a single stack.

#### Solution

##### Approach
Use a stack as the side street. Try to output trucks in order 1 to n, using the stack to temporarily hold trucks that can't go directly.

##### Python Solution
```python
from collections import deque

results = []
while True:
    n = int(input())
    if n == 0:
        break

    trucks = deque(map(int, input().split()))
    side_street = []
    expected = 1

    while trucks or side_street:
        if trucks and trucks[0] == expected:
            trucks.popleft()
            expected += 1
        elif side_street and side_street[-1] == expected:
            side_street.pop()
            expected += 1
        elif trucks:
            side_street.append(trucks.popleft())
        else:
            results.append('no')
            break
    else:
        results.append('yes')

print(*results, sep='\n')
```

##### Complexity Analysis
- **Time Complexity:** O(n) - each truck is processed once
- **Space Complexity:** O(n) - stack for side street

---

### Ferry Loading III

#### Problem Information
- **Source:** [UVA 10901](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=10901)
- **Difficulty:** Medium

#### Problem Statement
A ferry carries cars between two banks. Given arrival times and bank for each car, and ferry crossing time t, determine when each car arrives at the destination bank.

#### Input Format
- Multiple test cases
- For each: n (ferry capacity), t (crossing time), m (number of cars)
- m lines: arrival time and bank ("left" or "right")

#### Output Format
For each car, output its arrival time at the destination.

#### Example
```
Input:
1
2 10 3
0 left
10 left
20 right

Output:
10
30
30
```
Ferry (capacity 2, crossing time 10). Car 1 arrives at 0 on left, crosses at 0, arrives at 10. Car 2 at 10 left, car 3 at 20 right. Ferry goes right at 10, picks car 3, arrives left at 30 with car 2.

#### Solution

##### Approach
Use two queues for left and right banks. Simulate ferry trips, loading cars based on their arrival times.

##### Python Solution
```python
from collections import deque

n_test_cases = int(input())
results = []

for _ in range(n_test_cases):
    n, t, m = map(int, input().split())
    result = [0] * m
    left_queue = deque()
    right_queue = deque()

    for j in range(m):
        ti, side = input().split()
        queue = left_queue if side == 'left' else right_queue
        queue.append((j, int(ti)))

    current_time = 0
    at_left = True

    while left_queue or right_queue:
        current_queue = left_queue if at_left else right_queue
        other_queue = right_queue if at_left else left_queue

        if not current_queue or current_queue[0][1] > current_time:
            if not current_queue or (other_queue and other_queue[0][1] < current_queue[0][1]):
                current_time = max(other_queue[0][1] + t, current_time + t)
                at_left = not at_left
                continue
            else:
                current_time = current_queue[0][1]

        for _ in range(n):
            if current_queue and current_queue[0][1] <= current_time:
                idx, _ = current_queue.popleft()
                result[idx] = current_time + t
            else:
                break

        current_time += t
        at_left = not at_left

    results.append(result)

for i, res in enumerate(results):
    print(*res, sep='\n')
    if i < len(results) - 1:
        print()
```

##### Complexity Analysis
- **Time Complexity:** O(m) - each car processed once
- **Space Complexity:** O(m) - queues for both banks

---

### Throwing Cards Away

#### Problem Information
- **Source:** [UVA 10935](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=10935)
- **Difficulty:** Easy

#### Problem Statement
Given a deck of n cards numbered 1 to n, repeatedly throw away the top card and move the next card to the bottom until one card remains. Find the sequence of discarded cards and the remaining card.

#### Input Format
Multiple lines, each containing n (number of cards). 0 to end.

#### Output Format
For each test case, print the discarded cards and the remaining card.

#### Example
```
Input:
7
0

Output:
Discarded cards: 1, 3, 5, 7, 4, 2
Remaining card: 6
```
Start: [1,2,3,4,5,6,7]. Discard 1, move 2 to back: [3,4,5,6,7,2]. Discard 3, move 4 to back: [5,6,7,2,4]. Continue until one remains.

```
Input:
1
0

Output:
Discarded cards:
Remaining card: 1
```

#### Solution

##### Approach
Use a queue to simulate the card operations. Dequeue top, move next to back.

##### Python Solution
```python
from collections import deque

results = []
while True:
    n = int(input())
    if n == 0:
        break

    cards = deque(range(1, n + 1))
    discarded = []

    while len(cards) > 1:
        discarded.append(cards.popleft())
        cards.append(cards.popleft())

    results.append((discarded, cards[0]))

for discarded, remaining in results:
    if discarded:
        print(f"Discarded cards: {', '.join(map(str, discarded))}")
    else:
        print("Discarded cards:")
    print(f"Remaining card: {remaining}")
```

##### Complexity Analysis
- **Time Complexity:** O(n) - each card is processed twice
- **Space Complexity:** O(n) - queue for cards

---

### That is Your Queue

#### Problem Information
- **Source:** [UVA 12207](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=12207)
- **Difficulty:** Medium

#### Problem Statement
Simulate a hospital queue with P citizens and C commands. Commands are 'N' (next person) or 'E x' (expedite person x to front). Output the processed person for each 'N' command.

#### Input Format
- Multiple test cases until P=C=0
- P C (population, commands)
- C command lines

#### Output Format
For each 'N' command, output the citizen number being processed.

#### Example
```
Input:
4 5
N
N
E 1
N
N
0 0

Output:
Case 1:
1
2
1
3
```
Initially: [1,2,3,4]. N→1 (queue becomes [2,3,4,1]). N→2 (queue [3,4,1,2]). E 1→moves 1 to front [1,3,4,2]. N→1. N→3.

#### Solution

##### Approach
Use a linked list to efficiently handle insertions at front and removals from middle.

##### Python Solution
```python
from collections import deque

results = []
case_num = 0

while True:
    P, C = map(int, input().split())
    if P == 0:
        break

    case_num += 1
    queue_size = min(P, C)
    queue = deque(range(1, queue_size + 1))
    output = []

    for _ in range(C):
        cmd = input().split()
        if cmd[0] == 'N':
            person = queue.popleft()
            output.append(person)
            queue.append(person)
        else:
            person = int(cmd[1])
            queue.remove(person)
            queue.appendleft(person)

    results.append(output)

for i, res in enumerate(results, 1):
    print(f"Case {i}:")
    print(*res, sep='\n')
```

##### Complexity Analysis
- **Time Complexity:** O(C * P) - worst case for expedite operations
- **Space Complexity:** O(min(P, C)) - linked list size

