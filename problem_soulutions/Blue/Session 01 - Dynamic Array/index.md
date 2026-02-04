---
layout: simple
title: "Session 01 - Dynamic Array"
permalink: /problem_soulutions/Blue/Session 01 - Dynamic Array/
---

# Session 01 - Dynamic Array

This session covers dynamic array fundamentals, including array manipulation, indexing, and basic operations on arrays.

## Problems

### 691A (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/691/A
#
# Problem: Jacket
#
# A jacket has n buttons arranged in a row. Each button is either fastened (1)
# or unfastened (0). A jacket is considered "properly fastened" if:
# - When n = 1: the button must be fastened
# - When n > 1: exactly one button must be unfastened
#
# Input:
# - Line 1: Integer n (number of buttons)
# - Line 2: n integers (0 or 1)
#
# Output: "YES" if properly fastened, "NO" otherwise
#
# Example: n=3, buttons=[1,0,1] → "YES" (exactly one unfastened)


def check_jacket(_a, _n):
    un_fastened = 0
    if _n == 1:
        if _a[0] == 0:
            return 'NO'
        else:
            return 'YES'
    else:
        for i in range(_n):
            un_fastened += (1 - _a[i])
            if un_fastened > 1:
                return 'NO'
        if un_fastened == 0:
            return 'NO'
        else:
            return 'YES'


n = int(input())
a = list(map(int, input().split()))
print(check_jacket(a, n))
```

### 677A (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/677/A
#
# Problem: Vanya and Fence
#
# Vanya and his n friends want to pass under a fence of height h. Each friend
# has a height a[i]. If a friend's height <= h, they walk normally (width 1).
# If taller, they must bend sideways (width 2). Calculate the total road width
# needed for all friends to pass.
#
# Input:
# - Line 1: n h (number of friends, fence height)
# - Line 2: n integers (heights of friends)
#
# Output: Total road width needed
#
# Example: n=3, h=7, heights=[4,5,14] → 4 (1+1+2)


def cal_road_width(_a, _h):
    road_width = 0
    for ai in _a:
        road_width += 1 if ai <= _h else 2
    return road_width


n, h = map(int, input().split())
a = list(map(int, input().split()))
print(cal_road_width(a, h))
```

### 242B (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/242/B
#
# Problem: Big Segment
#
# Given n segments [l[i], r[i]], find if there exists a segment that completely
# covers all other segments (i.e., its left endpoint is the minimum of all left
# endpoints AND its right endpoint is the maximum of all right endpoints).
# If such a segment exists, output its 1-based index. Otherwise, output -1.
#
# Input:
# - Line 1: Integer n (number of segments)
# - Next n lines: l[i] r[i] (left and right endpoints of segment i)
#
# Output: Index of the covering segment (1-based), or -1 if none exists
#
# Example: Segments [1,5], [2,3], [1,10] → 3 (segment [1,10] covers all)


def check_cover(_l, _r, _n):
    min_left, max_right = _l[0], _r[0]
    pos = 0
    for i in range(1, n):
        if _l[i] < min_left:
            min_left = _l[i]
            if _r[i] >= max_right:
                pos = i
                max_right = _r[i]
            else:
                pos = -2
        elif _r[i] > max_right:
            max_right = _r[i]
            if _l[i] <= min_left:
                pos = i
                min_left = _l[i]
            else:
                pos = -2
        elif _l[i] == min_left and _r[i] == max_right:
            pos = i

    return pos + 1


n = int(input())
l, r = [], []
for i in range(n):
    li, ri = map(int, input().split())
    l.append(li)
    r.append(ri)
print(check_cover(l, r, n))
```

### 572A (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/572/A
#
# Problem: Arrays
#
# Given two sorted arrays a (size na) and b (size nb) in non-decreasing order,
# check if ALL of the first k elements of array a are strictly less than ALL
# of the last m elements of array b.
#
# Input:
# - Line 1: na nb (sizes of arrays)
# - Line 2: k m (number of elements to consider from each array)
# - Line 3: Array a (na integers, sorted non-decreasing)
# - Line 4: Array b (nb integers, sorted non-decreasing)
#
# Output: "YES" if condition is satisfied, "NO" otherwise
#
# Key insight: Just compare a[k-1] < b[nb-m] (max of first k vs min of last m)


def check_arrays(_a, _b, _k, _m):
    if _a[k - 1] >= _b[-m]:
        return 'NO'
    else:
        return 'YES'


na, nb = map(int, input().split())
k, m = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))
print(check_arrays(a, b, k, m))
```

### 673A (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/673/A
#
# Problem: Bear and Game
#
# A bear watches a 90-minute football game on TV. There are n interesting
# moments at times t[1], t[2], ..., t[n] (in increasing order). The bear
# turns off the TV if more than 15 consecutive minutes pass without any
# interesting moment. Determine at what minute he stops watching.
#
# Input:
# - Line 1: Integer n (number of interesting moments)
# - Line 2: n integers t[i] (times of interesting moments, 1 <= t[i] <= 90)
#
# Output: The minute when the bear stops watching
#
# Example: n=3, times=[7,20,88] → 35 (gap from 20 to 88 > 15, stops at 20+15)


def calc_mins(_t, _n):
    if _t[0] > 15:
        return 15
    for i in range(1, _n):
        if _t[i] - _t[i - 1] > 15:
            return t[i - 1] + 15
    if 90 - _t[_n - 1] > 15:
        return _t[n - 1] + 15
    return 90


n = int(input())
t = list(map(int, input().split()))
print(calc_mins(t, n))
```

### 378B (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/378/B
#
# Problem: Semifinals
#
# Two semifinals of a race, each with n participants. The top n participants
# overall (by finish time) will qualify for the finals. For each position in
# each semifinal, determine if that racer has a chance to qualify (1) or
# definitely won't qualify (0).
#
# The first ceil(n/2) from each semifinal are guaranteed to qualify. The
# remaining spots depend on cross-semifinal comparisons.
#
# Input:
# - Line 1: Integer n (participants per semifinal)
# - Next n lines: a[i] b[i] (finish times for position i in semifinals A and B)
#
# Output: Two lines of n characters each (0 or 1), representing qualification
#         chances for each position in semifinal A and B respectively


def calc_chances_matrix(_n, _a, _b):
    k = n // 2
    chances_matrix = [[1] * k + [0] * (n - k) for j in range(2)]

    last_a = k - 1
    last_b = k - 1
    if n % 2 == 1:
        if _a[k] < _b[k]:
            last_a += 1
            chances_matrix[0][k] = 1
        else:
            last_b += 1
            chances_matrix[1][k] = 1
    while last_a < n - 1 and last_b < n - 1:
        if _a[last_a + 1] < _b[n - (last_a + 1) - 1]:
            last_a += 1
            chances_matrix[0][last_a] = 1
        elif _b[last_b + 1] < _a[n - (last_b + 1) - 1]:
            last_b += 1
            chances_matrix[1][last_b] = 1
        else:
            break
    return chances_matrix


n = int(input())
a, b = [], []
for i in range(n):
    ai, bi = map(int, input().split())
    a.append(ai)
    b.append(bi)

print(*calc_chances_matrix(n, a, b)[0], sep='')
print(*calc_chances_matrix(n, a, b)[1], sep='')
```

### 676A (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/676/A
#
# Problem: Nicholas and Permutation
#
# Given a permutation of integers 1 to n, you can perform at most one swap
# of any two elements. Find the maximum possible distance between the
# positions of elements 1 and n after the swap.
#
# Distance is defined as |pos(1) - pos(n)|.
#
# Input:
# - Line 1: Integer n
# - Line 2: A permutation of integers 1 to n
#
# Output: Maximum achievable distance between positions of 1 and n
#
# Key insight: You can move either 1 or n to an endpoint (position 0 or n-1)
#              to maximize distance. Check all 4 possibilities.


def calc_max_dist(_a, _n):
    pos_min, pos_max = 0, 0
    for i in range(_n):
        if _a[i] == n:
            pos_max = i
        if _a[i] == 1:
            pos_min = i
    return max(n - 1 - pos_max, n - 1 - pos_min, pos_max, pos_min)


n = int(input())
a = list(map(int, input().split()))
print(calc_max_dist(a, n))
```

### 609B (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/609/B
#
# Problem: The Best Gift
#
# There are n books of m different genres. Tanya wants to choose 2 books of
# DIFFERENT genres as a gift. Count the number of ways to choose such a pair.
#
# Input:
# - Line 1: n m (number of books, number of genres)
# - Line 2: n integers (genre of each book, values from 1 to m)
#
# Output: Number of ways to choose 2 books of different genres
#
# Approach: Count books per genre, then sum count[i] * count[j] for all i < j


n, m = map(int, input().split())
a = list(map(int, input().split()))

total = 0
type_list = [0] * m
for i in range(n):
    type_list[a[i] - 1] += 1
for j in range(m - 1):
    for k in range(j + 1, m):
        total += type_list[j] * type_list[k]
print(total)
```

### 430B (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/430/B
#
# Problem: Balls Game
#
# A row of n colored balls is arranged in a line. You have one ball of color x
# that you can insert between any two adjacent balls of the same color as x.
# When k or more consecutive balls of the same color form, they are destroyed.
# Chain reactions can occur. Find the maximum number of balls you can destroy.
#
# Input:
# - Line 1: n k x (number of balls, threshold for destruction, your ball's color)
# - Line 2: n integers (colors of balls in the row)
#
# Output: Maximum number of balls that can be destroyed
#
# Approach: Try inserting between each pair of adjacent x-colored balls,
#           simulate chain reactions recursively


def destroy_balls(_a, _b, _x):
    if len(_a) == 0 or len(_b) == 0:
        return 0
    lenb = len(_b)
    a_cur_index = len(_a) - 1
    b_cur_index = 0
    if _a[a_cur_index] == _b[b_cur_index]:
        to_be_destroyed = 2
        a_cur_index -= 1
        b_cur_index += 1
        while a_cur_index >= 0:
            if _a[a_cur_index] == _x:
                to_be_destroyed += 1
                a_cur_index -= 1
            else:
                break
        while b_cur_index < lenb:
            if _b[b_cur_index] == _x:
                to_be_destroyed += 1
                b_cur_index += 1
            else:
                break
        if to_be_destroyed > 2:
            return to_be_destroyed + destroy_balls(_a[0:a_cur_index + 1], _b[b_cur_index:], _a[a_cur_index])
        else:
            return 0

    return 0


n, k, x = map(int, input().split())
c = list(map(int, input().split()))

cur_max = 0
for i in range(n - 1):
    if c[i] == x and c[i] == c[i + 1]:
        tmp_a = c[0:i+1]
        tmp_b = c[i+1:n]
        tmp_a.append(x)
        i += 1
        tmp_max = destroy_balls(tmp_a, tmp_b, x)
        if tmp_max > cur_max:
            cur_max = tmp_max
if cur_max >= 2:
    cur_max -= 1
else:
    cur_max = 0
print(cur_max)
```

