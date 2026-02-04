---
layout: simple
title: "Session 04 - Stack and Queue"
permalink: /problem_soulutions/Blue/Session 04 - Stack and Queue/
---

# Session 04 - Stack and Queue

This session covers stack and queue data structures, including LIFO/FIFO operations, expression parsing, and simulation problems.

## Problems

### Compilers and parsers (Codechef)

```python
# Compilers and parsers Problem Code: COMPILER
# https://www.codechef.com/problems/COMPILER

# Lira is now very keen on compiler development. :)
#
# She knows that one of the most important components of a compiler, is its parser.
#
#     A parser is, in simple terms, a software component that processes text, and checks it's semantic correctness, or, if you prefer, if the text is properly built.
#
# As an example, in declaring and initializing an integer, in C/C++, you can't do something like:
#
# int = x ;4
#
# as the semantics of such statement is incorrect, as we all know that the datatype must precede an identifier and only afterwards should come the equal sign and the initialization value, so, the corrected statement should be:
#
# int x = 4;
#
# Today, Lira is concerned with an abstract instruction which is composed of the characters "<" and ">" , which she will use on the design of her language, L++ :D.
#
#                                                                                                                                                                    She is using it as an abstraction for generating XML code Tags in an easier fashion and she understood that, for an expression to be valid, a "<" symbol must always have a corresponding ">" character somewhere (not necessary immediately) after it. Moreover, each ">" symbol should correspond to exactly one "<" symbol.
#
# So, for instance, the instructions:
#
#     <<>>
#
# <>
#
# <><>
#
# are all valid. While:
#
# >>
#
# ><><
#
# are not.
#
# Given some expressions which represent some instructions to be analyzed by Lira's compiler, you should tell the length of the longest prefix of each of these expressions that is valid, or 0 if there's no such a prefix.
#
#     Input
# Input will consist of an integer T denoting the number of test cases to follow.
#
#                                                                             Then, T strings follow, each on a single line, representing a possible expression in L++.
#
# Output
# For each expression you should output the length of the longest prefix that is valid or 0 if there's no such a prefix.
# Constraints
# 1 ≤ T ≤ 500
# 1 ≤ The length of a single expression ≤ 106
# The total size all the input expressions is no more than 5*106
#
#
# Example
# Input:
# 3
# <<>>
# ><
# <>>>
# Output:
# 4
# 0
# 2


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

### 644B (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/644/B

# In this problem you have to simulate the workflow of one-thread server. There are n queries to process, the i-th will be received at moment ti and needs to be processed for di units of time. All ti are guaranteed to be distinct.
#
# When a query appears server may react in three possible ways:
#
# If server is free and query queue is empty, then server immediately starts to process this query.
# If server is busy and there are less than b queries in the queue, then new query is added to the end of the queue.
# If server is busy and there are already b queries pending in the queue, then new query is just rejected and will never be processed.
# As soon as server finished to process some query, it picks new one from the queue (if it's not empty, of course). If a new query comes at some moment x, and the server finishes to process another query at exactly the same moment, we consider that first query is picked from the queue and only then new query appears.
#
# For each query find the moment when the server will finish to process it or print -1 if this query will be rejected.
#
# Input
# The first line of the input contains two integers n and b (1 ≤ n, b ≤ 200 000) — the number of queries and the maximum possible size of the query queue.
#
# Then follow n lines with queries descriptions (in chronological order). Each description consists of two integers ti and di (1 ≤ ti, di ≤ 109), where ti is the moment of time when the i-th query appears and di is the time server needs to process it. It is guaranteed that ti - 1 < ti for all i > 1.
#
# Output
# Print the sequence of n integers e1, e2, ..., en, where ei is the moment the server will finish to process the i-th query (queries are numbered in the order they appear in the input) or  - 1 if the corresponding query will be rejected.
#
# Examples
# input
# 5 1
# 2 9
# 4 8
# 10 9
# 15 2
# 19 1
# output
# 11 19 -1 21 22
# input
# 4 1
# 2 8
# 4 8
# 10 9
# 15 2
# output
# 10 18 27 -1
# Note
# Consider the first sample.
#
# The server will start to process first query at the moment 2 and will finish to process it at the moment 11.
# At the moment 4 second query appears and proceeds to the queue.
# At the moment 10 third query appears. However, the server is still busy with query 1, b = 1 and there is already query 2 pending in the queue, so third query is just rejected.
# At the moment 11 server will finish to process first query and will take the second query from the queue.
# At the moment 15 fourth query appears. As the server is currently busy it proceeds to the queue.
# At the moment 19 two events occur simultaneously: server finishes to proceed the second query and the fifth query appears. As was said in the statement above, first server will finish to process the second query, then it will pick the fourth query from the queue and only then will the fifth query appear. As the queue is empty fifth query is proceed there.
# Server finishes to process query number 4 at the moment 21. Query number 5 is picked from the queue.
# Server finishes to process query number 5 at the moment 22.

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

### MMASS (SPOJ)

```python
# Problem from SPOJ
# https://www.spoj.com/problems/MMASS/

# MMASS - Mass
# of
# Molecule
# # ad-hoc-1
# English
# Vietnamese
# A molecule can be defined as a sequence of atoms and represented by a chemical formula consisting of letters denoting these atoms. E.g. letter H denotes atom of hydrogen, C denotes atom of carbon, O denotes atom of oxygen, formula COOH represents molecule consisting of one atom of carbon, two atoms of oxygen and one atom of hydrogen.
#
# To write some formulas efficiently, we use the following rules. Letters denoting some atoms can be grouped by enclosing in parentheses, e.g. formula CH(OH) contains group OH. Groups can be nested – a group can also contain other groups. To simplify a formula, consecutive occurrences of the same letter can be replaced with that letter followed by a number of these occurrences. E.g. formula COOHHH can be written as CO2H3 and it represents a molecule consisting of one atom of carbon, two atoms of oxygen and three atoms of hydrogen. Furthermore, consecutive occurrences of the same group can be replaced with that group followed by a number of these occurrences. E.g. formula CH (CO2H) (CO2H) (CO2H) can be written as CH(CO2H)3 and molecule represented by both those formulas consists of four atoms of carbon, four atoms of hydrogen and six atoms of oxygen. A number written after a letter or a group is always greater than or equal to 2 and less than or equal to 9. A mass of a molecule is a sum of masses of all its atoms. One atom of hydrogen has mass 1, one atom of carbon has mass 12 and one atom of oxygen has mass 16.
#
# Write a program that will calculate a mass of a molecule.
#
# Input
# The first and only line of input file contains a formula of a molecule whose mass needs to be determined. A formula of a molecule will consist of characters H, C, O, (, ) , 2, 3, ..., 9 only. Its length will be less or equal to 100 characters.
#
# Output
# The first and only line of output file should contain a mass of a molecule represented with a given formula. The result will always be less than or equal to 10,000.
#
# Sample
# MASS.IN
#
# COOH
#
# MASS.OUT
#
# 45
#
# MASS.IN
#
# CH(CO2H)
# 3
#
# MASS.OUT
#
# 148
#
# MASS.IN
#
# ((CH)2(OH2H)(C(H))O)3
#
# MASS.OUT
#
# 222


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

### ONP (SPOJ)

```python
# Problem from SPOJ
# https://www.spoj.com/problems/ONP/

# ONP - Transform the Expression
# #stack
# Transform the algebraic expression with brackets into RPN form (Reverse Polish Notation). Two-argument operators: +, -, *, /, ^ (priority from the lowest to the highest), brackets ( ). Operands: only letters: a,b,...,z. Assume that there is only one RPN form (no expressions like a*b*c).
#
# Input
# t [the number of expressions <= 100]
# expression [length <= 400]
# [other expressions]
# Text grouped in [ ] does not appear in the input file.
#
# Output
# The expressions in RPN form, one per line.
# Example
# Input:
# 3
# (a+(b*c))
# ((a+b)*(z+x))
# ((a+t)*((b+(a+c))^(c+d)))
#
# Output:
# abc*+
# ab+zx+*
# at+bac++cd+^*

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
        if cur_prio is None and cur_elem is not ')' and cur_elem is not '(': # This is a number
            cur_output += cur_elem
        elif cur_prio is not None: # This is an operator
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

### STPAR (SPOJ)

```python
# Problem from SPOJ
# https://www.spoj.com/problems/STPAR/

# For sure, the love mobiles will roll again on this summer's street parade. Each year, the organisers decide on a fixed order for the decorated trucks. Experience taught them to keep free a side street to be able to bring the trucks into order.
#
# The side street is so narrow that no two cars can pass each other. Thus, the love mobile that enters the side street last must necessarily leave the side street first. Because the trucks and the ravers move up closely, a truck cannot drive back and re-enter the side street or the approach street.
#
# You are given the order in which the love mobiles arrive. Write a program that decides if the love mobiles can be brought into the order that the organisers want them to be.
#
# Input
# There are several test cases. The first line of each test case contains a single number n, the number of love mobiles. The second line contains the numbers 1 to n in an arbitrary order. All the numbers are separated by single spaces. These numbers indicate the order in which the trucks arrive in the approach street. No more than 1000 love mobiles participate in the street parade. Input ends with number 0.
#
# Output
# For each test case your program has to output a line containing a single word "yes" if the love mobiles can be re-ordered with the help of the side street, and a single word "no" in the opposite case.
#
# Example
# Sample input:
# 5
# 5 1 2 4 3
# 0
#
# Sample output:
# yes

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

### 10901 - Ferry Loading III (UVA)

```python
# Problem from UVA 10901 - Ferry Loading III
# https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1842

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

### 10935 - Throwing cards away I (UVA)

```python
# Problem from UVA
# https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1876

#
# Given is an ordered deck of n cards numbered 1
# to n with card 1 at the top and card n at the
# bottom. The following operation is performed as
# long as there are at least two cards in the deck:
# Throw away the top card and move
# the card that is now on the top of the
# deck to the bottom of the deck.
# Your task is to find the sequence of discarded
# cards and the last, remaining card.
# Input
# Each line of input (except the last) contains a
# number n ≤ 50. The last line contains ‘0’ and
# this line should not be processed.
# Output
# For each number from the input produce two
# lines of output. The first line presents the sequence
# of discarded cards, the second line reports
# the last remaining card. No line will have
# leading or trailing spaces. See the sample for the
# expected format.
# Sample Input
# 7
# 19
# 10
# 6
# 0
# Sample Output
# Discarded cards: 1, 3, 5, 7, 4, 2
# Remaining card: 6
# Discarded cards: 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 4, 8, 12, 16, 2, 10, 18, 14
# Remaining card: 6
# Discarded cards: 1, 3, 5, 7, 9, 2, 6, 10, 8
# Remaining card: 4
# Discarded cards: 1, 3, 5, 2, 6
# Remaining card: 4

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

### 12207 - That is Your Queue (UVA)

```python
# Problem from UVA 12207	That is Your Queue
# https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=3359

# Your government has finally solved the
# problem of universal health care! Now
# everyone, rich or poor, will finally have
# access to the same level of medical care.
# Hurrah!
# There’s one minor complication. All
# of the country’s hospitals have been condensed
# down into one location, which can
# only take care of one person at a time.
# But don’t worry! There is also a plan
# in place for a fair, efficient computerized
# system to determine who will be admitted.
# You are in charge of programming
# this system.
# Every citizen in the nation will be assigned
# a unique number, from 1 to P
# (where P is the current population). They will be put into a queue, with 1 in front of 2, 2 in front of
# 3, and so on. The hospital will process patients one by one, in order, from this queue. Once a citizen
# has been admitted, they will immediately move from the front of the queue to the back.
# Of course, sometimes emergencies arise; if you’ve just been run over by a steamroller, you can’t wait
# for half the country to get a routine checkup before you can be treated! So, for these (hopefully rare)
# occasions, an expedite command can be given to move one person to the front of the queue. Everyone
# else’s relative order will remain unchanged.
# Given the sequence of processing and expediting commands, output the order in which citizens will
# be admitted to the hospital.

# Input
# Input consists of at most ten test cases. Each test case starts with a line containing P, the population
# of your country (1 ≤ P ≤ 1000000000), and C, the number of commands to process (1 ≤ C ≤ 1000).
# The next C lines each contain a command of the form ‘N’, indicating the next citizen is to be
# admitted, or ‘E x’, indicating that citizen x is to be expedited to the front of the queue.
# The last test case is followed by a line containing two zeros.
# Output
# For each test case print the serial of output. This is followed by one line of output for each ‘N’ command,
# indicating which citizen should be processed next. Look at the output for sample input for details.
# Sample Input
# 3 6
# N
# N
# E 1
# N
# N
# N
# 10 2
# N
# N
# 0 0

# Sample Output
# Case 1:
# 1
# 2
# 1
# 3
# 2
# Case 2:
# 1
# 2


class Node:
    def __init__(self, data_val=None):
        self.data_val = data_val
        self.next_node = None


class MyLinkedList:
    def __init__(self):
        self.head_node = None
        self.tail_node = self.head_node

    def print_list(self):
        print_node = self.head_node
        while True:
            if print_node.next_node is None:
                print(print_node.data_val, end='')
                break
            else:
                print(print_node.data_val, end=' ')
                print_node = print_node.next_node
        print('---')

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

