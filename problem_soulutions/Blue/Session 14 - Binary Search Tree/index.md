---
layout: simple
title: "Session 14 - Binary Search Tree"
permalink: /problem_soulutions/Blue/Session 14 - Binary Search Tree/
---

# Session 14 - Binary Search Tree

This session covers Binary Search Tree (BST) data structure, including insertion, deletion, search operations, and balanced trees.

## Problems

### 514B (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/514/B
#
# Problem Name: Han Solo and Lazer Gun (Codeforces 514B)
#
# Problem Description:
# Han Solo is at position (x0, y0) and needs to shoot n stormtroopers.
# A single laser shot can kill all stormtroopers on the same ray from Han.
# Find the minimum number of shots needed to eliminate all stormtroopers.
#
# Input Format:
# - First line: n x0 y0 (number of stormtroopers, Han's position)
# - Next n lines: x y (coordinates of each stormtrooper)
#
# Output Format:
# - Minimum number of shots (distinct rays) needed
#
# Key Approach/Algorithm:
# - Two points are on the same ray if they have the same angle from origin
# - For each stormtrooper, compute angle (or slope) relative to Han's position
# - Use a set to count distinct angles/slopes
# - Stormtroopers with same slope are on the same ray


def solution():
    n, x0, y0 = map(int, input().strip().split())
    shots = set()
    for i in range(n):
        x, y = map(int, input().strip().split())
        x, y = x - x0, y - y0
        angle = 1e4
        if y != 0:
            angle = x / y
        shots.add(angle)

    print(len(shots))


solution()
```

### 704A (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/704/A
#
# Problem Name: Thor (Codeforces 704A)
#
# Problem Description:
# Simulate a notification system with n applications. Three operations:
# 1. Type 1 x: application x generates a notification
# 2. Type 2 x: read all notifications from application x
# 3. Type 3 t: read first t notifications in order
# After each operation, output the current number of unread notifications.
#
# Input Format:
# - First line: n q (number of applications, number of operations)
# - Next q lines: type x (operation type and parameter)
#
# Output Format:
# - q lines: number of unread notifications after each operation
#
# Key Approach/Algorithm:
# - Use sets to track unread notifications per application
# - Use a queue to track notification order for type 3 operations
# - For type 2: clear all notifications from specific app
# - For type 3: process notifications in order up to given index
import queue


class Node:
    def __init__(self, noti_index, app_index):
        self.noti_index = noti_index
        self.app_index = app_index

    def __lt__(self, other):
        return self.noti_index < other.noti_index


def solution():
    n, q = map(int, input().strip().split())
    apps = [set() for i in range(n + 1)]
    noti_queue = queue.Queue()
    current_noti = 0
    read_noti = 0
    current_noti_index = 1
    for i in range(q):
        q1, q2 = map(int, input().split())
        if q1 == 1:
            apps[q2].add(current_noti_index)
            noti_queue.put(Node(current_noti_index, q2))
            current_noti_index += 1
            current_noti += 1
        if q1 == 2:
            current_noti -= len(apps[q2])
            apps[q2].clear()
        if q1 == 3:
            while read_noti < q2:
                to_be_read = noti_queue.get()
                if to_be_read.noti_index in apps[to_be_read.app_index]:
                    current_noti -= 1
                    apps[to_be_read.app_index].remove(to_be_read.noti_index)
                read_noti += 1

        print(current_noti)


solution()
```

### distinct-count (Hackerearth)

```python
#  Problem from Hackerearth
#  https://www.hackerearth.com/fr/practice/data-structures/trees/binary-search-tree/practice-problems/algorithm/distinct-count/
#
# Problem Name: Distinct Count
#
# Problem Description:
# Given an array of N integers and a target X, determine if the number of
# distinct elements equals X, is less than X, or is greater than X.
#
# Input Format:
# - T: number of test cases
# - For each test case:
#   - N X: size of array and target count
#   - N integers (the array)
#
# Output Format:
# - "Good" if distinct count equals X
# - "Bad" if distinct count is less than X
# - "Average" if distinct count is greater than X
#
# Key Approach/Algorithm:
# - Use a set to count distinct elements in O(n)
# - Compare set size with X to determine result


def check_distinct(_n, _x, _a):
    distinct_set = set(_a)
    # for i in range(_n):
    #     distinct_set.add(_a[i])
    if len(distinct_set) == _x:
        return 'Good'
    if len(distinct_set) < _x:
        return 'Bad'
    return 'Average'


def solution():
    T = int(input())
    for i in range(T):
        N, X = map(int, input().strip().split())
        A = list(map(int, input().strip().split()))
        print(check_distinct(N, X, A))


solution()
```

### minimum-loss (Hackerearth)

```python
#  Problem from Hackerearth
#  https://www.hackerrank.com/contests/womens-codesprint-2/challenges/minimum-loss
#
# Problem Name: Minimum Loss
#
# Problem Description:
# Lauren wants to buy a house and sell it later. She has predicted house prices
# for n years. She must buy before selling (buy year < sell year).
# She can only afford to make a loss (buy price > sell price).
# Find the minimum possible loss she must incur.
#
# Input Format:
# - n: number of years
# - n integers: predicted house prices (all distinct)
#
# Output Format:
# - Minimum loss (buy_price - sell_price where buy_price > sell_price)
#
# Key Approach/Algorithm:
# - Build a BST as we process prices in chronological order
# - For each new price (potential sell price), find the smallest price
#   greater than it in the BST (which represents a valid buy price from past)
# - The loss is (buy_price - current_price)
# - Track minimum loss across all valid pairs


#!/bin/python3

import math
import os
import random
import re
import sys


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def add_node(root, x):
    if root is None:
        return Node(x)
    if x < root.value:
        root.left = add_node(root.left, x)
    elif x > root.value:
        root.right = add_node(root.right, x)
    return root


def max_value_node(root):
    current = root
    while current.right is not None:
        current = current.right
    return current.value


def __find_min_loss(root):
    if root is None or root.left is None:
        return -1
    return root.value - max_value_node(root.left)


def find_min_loss(root, min_loss):
    if root is None:
        return min_loss
    current_min_loss = __find_min_loss(root)
    if current_min_loss != -1 and min_loss > current_min_loss:
        min_loss = current_min_loss

    min_loss_right = find_min_loss(root.right, min_loss)
    min_loss_left = find_min_loss(root.left, min_loss_right)

    return min_loss_left


# Complete the minimumLoss function below.
def minimum_loss(price):
    n = len(price)
    root = Node(price[0])
    for i in range(1, n):
        add_node(root, price[i])

    min_loss = 1e16
    return find_min_loss(root, min_loss)


if __name__ == '__main__':
    fptr = sys.stdout

    n = int(input())

    price = list(map(int, input().rstrip().split()))

    result = minimum_loss(price)

    fptr.write(str(result) + '\n')

    fptr.close()
```

### monk-and-his-friends (Hackerearth)

```python
#  Problem from Hackerearth
#  https://www.hackerearth.com/fr/practice/data-structures/trees/binary-search-tree/practice-problems/algorithm/monk-and-his-friends/description/
#
# Problem Name: Monk and his Friends
#
# Problem Description:
# Monk is waiting for his friends in a classroom. N friends are already inside.
# M more friends arrive one by one. When a friend arrives, check if someone
# with the same ID is already in the class. After checking, the friend enters.
#
# Input Format:
# - T: number of test cases
# - For each test case:
#   - N M: friends already inside, friends arriving
#   - N+M integers: IDs (first N already inside, next M arriving)
#
# Output Format:
# - For each arriving friend: "YES" if duplicate exists, "NO" otherwise
#
# Key Approach/Algorithm:
# - Use a set to store IDs of friends inside the class
# - For each arriving friend, check if ID exists in set
# - Add the arriving friend's ID to the set after checking


def check_exist(_in, _out):
    inside_class = set(_in)
    for stu in _out:
        if stu in inside_class:
            print('YES')
        else:
            print('NO')
        inside_class.add(stu)


def solution():
    T = int(input())
    for i in range(T):
        N, M = map(int, input().strip().split())
        A = list(map(int, input().strip().split()))
        inside_class = A[:N]
        outside_class = A[N:]
        check_exist(inside_class, outside_class)


solution()
```

### 1196 (Timus)

```python
# Problem from ACM TIMUS
# http://acm.timus.ru/problem.aspx?space=1&num=1196
#
# Problem Name: History Exam (Timus 1196)
#
# Problem Description:
# A student memorized n historical years for an exam. The exam has m questions
# asking about specific years. Count how many questions the student can answer
# correctly (i.e., how many exam years match memorized years).
#
# Input Format:
# - n: number of years the student memorized
# - n lines: memorized years (one per line)
# - m: number of exam questions
# - m lines: years asked in exam (one per line)
#
# Output Format:
# - Number of correct answers (exam years that match memorized years)
#
# Key Approach/Algorithm:
# - Build a Binary Search Tree from memorized years
# - For each exam question, search the BST
# - Count successful searches


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def add_node(root, x):
    if root is None:
        return Node(x)
    if x < root.value:
        root.left = add_node(root.left, x)
    elif x > root.value:
        root.right = add_node(root.right, x)
    return root


def search_node(root, x):
    if root is None or root.value == x:
        return root
    if root.value < x:
        return search_node(root.right, x)
    return search_node(root.left, x)


def solution():
    n = int(input().strip())

    root = Node(int(input()))
    for i in range(n - 1):
        add_node(root, int(input()))
    m = int(input().strip())
    mark = 0
    for i in range(m):
        year = int(input())
        if search_node(root, year) is not None:
            mark += 1

    print(mark)


solution()
```

### 10815 (UVA)

```python
# Problem from UVA
# https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1756
#
# Problem Name: Andy's First Dictionary (UVA 10815)
#
# Problem Description:
# Andy is making a dictionary from a text. Extract all distinct words from
# the input, convert to lowercase, and output them in alphabetical order.
# Words consist only of alphabetic characters.
#
# Input Format:
# - Multiple lines of text containing words and non-alphabetic characters
#
# Output Format:
# - All distinct words in lowercase, sorted alphabetically (one per line)
#
# Key Approach/Algorithm:
# - Parse input to extract words (alphabetic sequences only)
# - Convert to lowercase
# - Use a BST (or set) to store unique words
# - In-order traversal of BST gives sorted output
# import sys
import re

# sys.stdin = open("file.txt", "r")


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def add_node(root, x):
    if root is None:
        return Node(x)
    if x < root.value:
        root.left = add_node(root.left, x)
    elif x > root.value:
        root.right = add_node(root.right, x)
    return root


def print_tree(root):
    if root is None:
        return
    print_tree(root.left)
    print(root.value)
    print_tree(root.right)


def solution():
    root = None
    while True:
        new_line = None
        new_words = []
        try:
            new_line = input().strip()
            new_words = list(map(lambda word: re.sub('[^a-z]+', '', word.lower()), re.compile(r'[^A-Za-z]').split(new_line)))
        except Exception:
            break

        new_words = list(filter(lambda x: x is not '', new_words))

        if root is None:
            if len(new_words) > 0:
                root = Node(new_words[0])

        for word in new_words:
            add_node(root, word)

    print_tree(root)


solution()
```

### 11062 (UVA)

```python
# Problem from UVA
# https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=2003
#
# Problem Name: Andy's Second Dictionary (UVA 11062)
#
# Problem Description:
# Similar to Andy's First Dictionary, but now words can contain hyphens.
# A word split across lines with a hyphen at end should be merged.
# Extract all distinct words, convert to lowercase, output alphabetically.
#
# Input Format:
# - Multiple lines of text
# - Words may contain hyphens
# - A word ending with hyphen at end of line continues on next line
#
# Output Format:
# - All distinct words in lowercase, sorted alphabetically (one per line)
#
# Key Approach/Algorithm:
# - Parse input handling hyphenated words and line-continuation hyphens
# - Track incomplete words (ending with hyphen at line end)
# - Merge with next line's first word
# - Use BST for unique sorted storage
# - In-order traversal outputs sorted words
# import sys
import re

# sys.stdin = open("file.txt", "r")


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def add_node(root, x):
    if root is None:
        return Node(x)
    if x < root.value:
        root.left = add_node(root.left, x)
    elif x > root.value:
        root.right = add_node(root.right, x)
    return root


def print_tree(root):
    if root is None:
        return
    print_tree(root.left)
    print(root.value)
    print_tree(root.right)


def solution():
    root = None
    imcompleted_word = None
    while True:
        # new_line = None
        # new_words = []

        try:
            new_line = input().strip()
            new_words = list(map(lambda word: re.sub('[^a-z\-]+', '', word.lower()), re.compile(r'[^A-Za-z\-]').split(new_line)))
        except Exception:
            break

        new_words = list(filter(lambda x: x is not '', new_words))

        if imcompleted_word is not None and len(new_words) > 0:
            new_words[0] = imcompleted_word[:-1] + new_words[0]

        if len(new_words) and new_words[-1].endswith('-'):
            imcompleted_word = new_words[-1]
            new_words = new_words[:-1]
        else:
            imcompleted_word = None

        if root is None:
            if len(new_words) > 0 and not new_words[0].endswith('-'):
                root = Node(new_words[0])

        for word in new_words:
            add_node(root, word)

    print_tree(root)


solution()
```

