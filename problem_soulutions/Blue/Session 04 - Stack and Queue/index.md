---
layout: simple
title: "Session 04 - Stack and Queue"
permalink: /problem_soulutions/Blue/Session 04 - Stack and Queue/
---

# Session 04 - Stack and Queue

This session covers stack and queue data structures, including LIFO/FIFO operations, expression parsing, and simulation problems.

## Problems

### Compilers and Parsers

#### Problem Information
- **Source:** CodeChef
- **Problem Code:** COMPILER
- **Difficulty:** Easy
- **URL:** https://www.codechef.com/problems/COMPILER

#### Problem Statement
Lira is designing a language L++ where expressions consist of "<" and ">" characters. For an expression to be valid, a "<" symbol must always have a corresponding ">" character somewhere after it. Each ">" symbol should correspond to exactly one "<" symbol.

Given some expressions, find the length of the longest prefix of each expression that is valid.

#### Input Format
- First line: T (number of test cases)
- Next T lines: One expression per line

#### Output Format
For each expression, output the length of the longest valid prefix, or 0 if there's no such prefix.

#### Solution

##### Approach
Use a stack to track unmatched "<" characters. Pop when ">" is encountered. Track the longest valid prefix when the stack is empty.

##### Python Solution
```python
T = int(input())

results = []
for i in range(T):
    cur_exp = input().strip()
    my_stack = []
    exp_length = len(cur_exp)
    cur_result = 0
    cur_max = 0
    for j in range(exp_length):
        if cur_exp[j] == '>':
            if len(my_stack) == 0:
                break
            else:
                my_stack.pop()
                cur_result += 1
                if len(my_stack) == 0:
                    cur_max = cur_result
        if cur_exp[j] == '<':
            my_stack.append('<')
            cur_result += 1
    results.append(cur_max)

print(*results, sep='\n')
```

##### Complexity Analysis
- **Time Complexity:** O(n) - single pass through each expression
- **Space Complexity:** O(n) - stack size at most n/2

---

### Processing Time

#### Problem Information
- **Source:** Codeforces
- **Problem Code:** 644B
- **Difficulty:** Medium
- **URL:** http://codeforces.com/problemset/problem/644/B

#### Problem Statement
Simulate a one-thread server processing n queries. Each query arrives at time ti and needs di time to process. The server has a queue of size b. If the queue is full, queries are rejected. Determine when each query finishes processing or if it's rejected.

#### Input Format
- First line: n b (number of queries, queue size)
- Next n lines: ti di (arrival time and processing duration for each query)

#### Output Format
For each query, output the finish time or -1 if rejected.

#### Solution

##### Approach
Use a queue to simulate the server's pending requests. Process queries as they arrive and track when each completes.

##### Python Solution
```python
import queue

n, b = map(int, input().split())
result = [0] * n
last_processing = 0
waiting_queue = queue.Queue()
for i in range(n):
    ti, di = map(int, input().split())
    while waiting_queue.qsize() > 0 and last_processing <= ti:
        last_processing = max(last_processing, waiting_queue.queue[0]['time']) + waiting_queue.queue[0]['take_time']
        result[waiting_queue.queue[0]['index']] = last_processing
        waiting_queue.get()
    if waiting_queue.qsize() < b:
        waiting_queue.put({'index': i, 'time': ti, 'take_time': di})
    else:
        result[i] = -1

while waiting_queue.qsize() > 0:
    last_processing = max(last_processing, waiting_queue.queue[0]['time']) + waiting_queue.queue[0]['take_time']
    result[waiting_queue.queue[0]['index']] = last_processing
    waiting_queue.get()
print(*result, sep=' ')
```

##### Complexity Analysis
- **Time Complexity:** O(n) - each query is processed once
- **Space Complexity:** O(b) - queue size limited to b

---

### Mass of Molecule

#### Problem Information
- **Source:** SPOJ
- **Problem Code:** MMASS
- **Difficulty:** Medium
- **URL:** https://www.spoj.com/problems/MMASS/

#### Problem Statement
Calculate the mass of a molecule from its chemical formula. The formula consists of H (mass 1), C (mass 12), O (mass 16), parentheses for grouping, and numbers 2-9 for multipliers. Calculate the total mass of the molecule.

#### Input Format
A single line containing the chemical formula.

#### Output Format
The total mass of the molecule.

#### Solution

##### Approach
Use a stack to handle nested parentheses. Process the formula character by character, multiplying masses when digits are encountered.

##### Python Solution
```python
def get_value(atom):
    if atom == 'H':
        return 1
    if atom == 'O':
        return 16
    if atom == 'C':
        return 12
    return 0


formula = input().strip()
stack = []
for i in range(len(formula)):
    if formula[i] == '(':
        stack.append(formula[i])
    if formula[i] == ')':
        tmp_total = 0
        while len(stack) > 0:
            if stack[-1] != '(':
                tmp_total += int(stack.pop())
            else:
                stack.pop()
                break
        stack.append(tmp_total)
    if get_value(formula[i]) > 0:
        if len(stack) == 0 or isinstance(stack[-1], int) and i < len(formula) - 1 and not formula[i+1].isdigit():
            if len(stack) > 0:
                stack[-1] = int(stack[-1]) + get_value(formula[i])
            else:
                stack.append(get_value(formula[i]))
        else:
            stack.append(get_value(formula[i]))
    if formula[i].isdigit():
        if isinstance(stack[-1], int):
            stack[-1] = int(stack[-1]) * int(formula[i])
total_result = 0
while len(stack) > 0:
    total_result += int(stack.pop())

print(total_result)
```

##### Complexity Analysis
- **Time Complexity:** O(n) - single pass through the formula
- **Space Complexity:** O(n) - stack size for nested parentheses

---

### Transform to RPN

#### Problem Information
- **Source:** SPOJ
- **Problem Code:** ONP
- **Difficulty:** Medium
- **URL:** https://www.spoj.com/problems/ONP/

#### Problem Statement
Transform algebraic expressions with brackets into Reverse Polish Notation (RPN). Operators are +, -, *, /, ^ (priority from lowest to highest). Operands are lowercase letters a-z.

#### Input Format
- First line: t (number of expressions)
- Next t lines: One expression per line

#### Output Format
The expressions in RPN form, one per line.

#### Solution

##### Approach
Use the Shunting Yard algorithm with a stack for operators. Output operands immediately, push operators based on precedence.

##### Python Solution
```python
n = int(input())
results = []

operator_list = {
    '+': 1,
    '-': 2,
    '*': 3,
    '/': 4,
    '^': 5
}

for i in range(n):
    cur_exp = input()
    cur_length = len(cur_exp)
    cur_output = ''
    temp_stack = []
    for j in range(cur_length):
        cur_elem = cur_exp[j]
        cur_prio = operator_list.get(cur_elem)
        if cur_prio is None and cur_elem is not ')' and cur_elem is not '(':
            cur_output += cur_elem
        elif cur_prio is not None:
            if len(temp_stack) > 0 and operator_list.get(temp_stack[-1]) is not None and operator_list.get(temp_stack[-1]) >= cur_prio:
                cur_output += temp_stack.pop()
            temp_stack.append(cur_elem)
        elif cur_elem is '(':
            temp_stack.append(cur_elem)
        else:
            while len(temp_stack) > 0:
                fr_stack = temp_stack.pop()
                if fr_stack is '(':
                    break
                cur_output += fr_stack

    while len(temp_stack) > 0:
        fr_stack = temp_stack.pop()
        cur_output += fr_stack

    results.append(cur_output)

print(*results, sep='\n')
```

##### Complexity Analysis
- **Time Complexity:** O(n) - single pass through each expression
- **Space Complexity:** O(n) - stack for operators

---

### Street Parade

#### Problem Information
- **Source:** SPOJ
- **Problem Code:** STPAR
- **Difficulty:** Medium
- **URL:** https://www.spoj.com/problems/STPAR/

#### Problem Statement
Love mobiles need to be arranged in order 1 to n for a parade. They arrive in a given order and can use a side street (stack) to help reorder. Determine if the trucks can be arranged in the correct order.

#### Input Format
- First line: n (number of trucks, 0 to end)
- Second line: n integers (arrival order)

#### Output Format
"yes" if reordering is possible, "no" otherwise.

#### Solution

##### Approach
Use a stack as the side street. Try to output trucks in order 1 to n, using the stack to temporarily hold trucks that can't go directly.

##### Python Solution
```python
results = []
while True:
    n = int(input())
    if n == 0:
        break

    trucks = list(map(int, input().split()))

    side_street = []
    result_order = []

    current_expect = 1

    while True:
        if len(trucks) > 0:
            if trucks[0] == current_expect:
                current_expect += 1
                result_order.append(trucks.pop(0))
            elif len(side_street) > 0 and side_street[-1] == current_expect:
                result_order.append(side_street.pop())
                current_expect += 1
            else:
                side_street.append(trucks.pop(0))
        elif len(side_street) > 0:
            from_side_street = side_street.pop()
            if from_side_street == current_expect:
                result_order.append(from_side_street)
                current_expect += 1
            else:
                results.append('no')
                break
        else:
            results.append('yes')
            break
print(*results, sep='\n')
```

##### Complexity Analysis
- **Time Complexity:** O(n) - each truck is processed once
- **Space Complexity:** O(n) - stack for side street

---

### Ferry Loading III

#### Problem Information
- **Source:** UVA
- **Problem Code:** 10901
- **Difficulty:** Medium
- **URL:** https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1842

#### Problem Statement
A ferry carries cars between two banks. Given arrival times and bank for each car, and ferry crossing time t, determine when each car arrives at the destination bank.

#### Input Format
- Multiple test cases
- For each: n (ferry capacity), t (crossing time), m (number of cars)
- m lines: arrival time and bank ("left" or "right")

#### Output Format
For each car, output its arrival time at the destination.

#### Solution

##### Approach
Use two queues for left and right banks. Simulate ferry trips, loading cars based on their arrival times.

##### Python Solution
```python
import queue

n_test_cases = int(input())
results = []
for i in range(n_test_cases):
    n, t, m = map(int, input().split())
    tmp_result = [0] * m
    left_queue = queue.Queue()
    right_queue = queue.Queue()

    for j in range(m):
        ti, side = input().split()
        if side == 'left':
            left_queue.put({'index': j, 'time': int(ti)})
        else:
            right_queue.put({'index': j, 'time': int(ti)})
    current_time = 0
    at_left = True
    while right_queue.qsize() > 0 or left_queue.qsize() > 0:
        if at_left:
            if left_queue.qsize() == 0 or left_queue.queue[0]['time'] > current_time:
                if left_queue.qsize() == 0 or (right_queue.qsize() > 0 and right_queue.queue[0]['time'] < left_queue.queue[0]['time']):
                    current_time = max(right_queue.queue[0]['time'] + t, current_time + t)
                    at_left = not at_left
                    continue
                else:
                    current_time = left_queue.queue[0]['time']
            for k in range(n):
                if left_queue.qsize() > 0 and left_queue.queue[0]['time'] <= current_time:
                    tmp_result[left_queue.queue[0]['index']] = current_time + t
                    left_queue.get()
                else:
                    break
            current_time += t
        else:
            if right_queue.qsize() == 0 or right_queue.queue[0]['time'] > current_time:
                if right_queue.qsize() == 0 or (left_queue.qsize() > 0 and left_queue.queue[0]['time'] < right_queue.queue[0]['time']):
                    current_time = max(left_queue.queue[0]['time'] + t, current_time + t)
                    at_left = not at_left
                    continue
                else:
                    current_time = right_queue.queue[0]['time']
            for k in range(n):
                if right_queue.qsize() > 0 and right_queue.queue[0]['time'] <= current_time:
                    tmp_result[right_queue.queue[0]['index']] = current_time + t
                    right_queue.get()
                else:
                    break
            current_time += t
        at_left = not at_left

    results.append(tmp_result)

for i in range(len(results)):
    print(*results[i], sep='\n')
    if i < len(results) - 1:
        print()
```

##### Complexity Analysis
- **Time Complexity:** O(m) - each car processed once
- **Space Complexity:** O(m) - queues for both banks

---

### Throwing Cards Away

#### Problem Information
- **Source:** UVA
- **Problem Code:** 10935
- **Difficulty:** Easy
- **URL:** https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1876

#### Problem Statement
Given a deck of n cards numbered 1 to n, repeatedly throw away the top card and move the next card to the bottom until one card remains. Find the sequence of discarded cards and the remaining card.

#### Input Format
Multiple lines, each containing n (number of cards). 0 to end.

#### Output Format
For each test case, print the discarded cards and the remaining card.

#### Solution

##### Approach
Use a queue to simulate the card operations. Dequeue top, move next to back.

##### Python Solution
```python
import queue

results = []
while True:
    cur_input = int(input())
    if cur_input == 0:
        break

    cur_queue = queue.Queue()
    for i in range(cur_input):
        cur_queue.put(i + 1)
    cur_result = []
    while True:
        if cur_queue.qsize() >= 2:
            cur_result.append(cur_queue.get())
            cur_queue.put(cur_queue.get())
        elif cur_queue.qsize() >= 1:
            cur_result.append(cur_queue.get())
        else:
            break
    results.append(cur_result)

for i in range(len(results)):
    remaining_card = results[i].pop()
    if len(results[i]) > 0:
        end_by = ' '
    else:
        end_by = ''
    print('Discarded cards:', end=end_by)
    print(*results[i], sep=', ')
    print('Remaining card: ' + str(remaining_card))
```

##### Complexity Analysis
- **Time Complexity:** O(n) - each card is processed twice
- **Space Complexity:** O(n) - queue for cards

---

### That is Your Queue

#### Problem Information
- **Source:** UVA
- **Problem Code:** 12207
- **Difficulty:** Medium
- **URL:** https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=3359

#### Problem Statement
Simulate a hospital queue with P citizens and C commands. Commands are 'N' (next person) or 'E x' (expedite person x to front). Output the processed person for each 'N' command.

#### Input Format
- Multiple test cases until P=C=0
- P C (population, commands)
- C command lines

#### Output Format
For each 'N' command, output the citizen number being processed.

#### Solution

##### Approach
Use a linked list to efficiently handle insertions at front and removals from middle.

##### Python Solution
```python
class Node:
    def __init__(self, data_val=None):
        self.data_val = data_val
        self.next_node = None


class MyLinkedList:
    def __init__(self):
        self.head_node = None
        self.tail_node = self.head_node

    def add_node(self, value=None):
        new_node = Node(value)
        if self.tail_node is not None:
            self.tail_node.next_node = new_node
            self.tail_node = new_node
        else:
            self.head_node = new_node
            self.tail_node = new_node

    def remove_head(self):
        head_value = self.head_node.data_val
        if self.head_node == self.tail_node:
            self.head_node = None
            self.tail_node = None
        else:
            self.head_node = self.head_node.next_node
        return head_value

    def remove_node(self, val_to_remove):
        cur_node = self.head_node
        cur_pre_node = None
        while True:
            if cur_node is None:
                return
            if cur_node.data_val == val_to_remove:
                if cur_pre_node is not None:
                    cur_pre_node.next_node = cur_node.next_node
                else:
                    self.head_node = cur_node.next_node
                if cur_node.next_node is None:
                    self.tail_node = cur_pre_node
                return
            else:
                cur_pre_node = cur_node
                cur_node = cur_node.next_node

    def add_head(self, val_to_add):
        new_node = Node(val_to_add)
        if self.head_node is not None:
            new_node.next_node = self.head_node
            self.head_node = new_node
        else:
            self.head_node = new_node
            self.tail_node = new_node


results = []
while True:
    P, C = map(int, input().split())

    if P == 0:
        break
    P = min(P, C)

    cur_queue = MyLinkedList()
    for i in range(P):
        cur_queue.add_node(i + 1)
    cur_result = []
    for i in range(C):
        Ci = input()
        if Ci is 'N':
            cur_treating = cur_queue.remove_head()
            cur_result.append(cur_treating)
            cur_queue.add_node(cur_treating)
        else:
            expedited_index = int(Ci.split()[1])
            cur_queue.remove_node(expedited_index)
            cur_queue.add_head(expedited_index)

    results.append(cur_result)

for i in range(len(results)):
    print('Case %d:' %(i + 1))
    print(*results[i], sep='\n')
```

##### Complexity Analysis
- **Time Complexity:** O(C * P) - worst case for expedite operations
- **Space Complexity:** O(min(P, C)) - linked list size

