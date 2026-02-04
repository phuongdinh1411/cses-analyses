---
layout: simple
title: "Session 03 - Sorting"
permalink: /problem_soulutions/Blue/Session 03 - Sorting/
---

# Session 03 - Sorting

This session covers sorting algorithms and techniques, including comparison-based sorting, custom comparators, and sorting-related problem solving.

## Problems

### 149A (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/149/A
#
# Problem: Business Trip
#
# A flower must grow at least k centimeters. There are 12 months, and each
# month i has a potential growth a[i] centimeters if watered that month.
# Find the minimum number of months you need to water the flower to achieve
# at least k centimeters of growth. You can choose which months to water.
#
# Input:
# - Line 1: Integer k (required growth in centimeters)
# - Line 2: 12 integers (growth potential for each month)
#
# Output: Minimum number of months needed, or -1 if impossible
#
# Approach: Sort months by growth (descending), greedily pick highest growth months

k = int(input())
a = list(map(int, input().split()))

growth_cent = 0

a.sort(key=lambda x: -x)
for i in range(12):
    if growth_cent >= k:
        print(i)
        exit()
    growth_cent += a[i]
    if growth_cent >= k:
        print(i + 1)
        exit()

print('-1')
```

### 169A (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/169/A
#
# Problem: Chores
#
# Petya and Vasya divide n chores. They have agreed:
# - Vasya does the a "easiest" chores (lowest difficulty)
# - Petya does the b "hardest" chores (highest difficulty)
# where a + b = n.
#
# The "gap" is the difference between the easiest chore Petya does and the
# hardest chore Vasya does. After sorting, this is h[b] - h[b-1].
#
# Input:
# - Line 1: n a b (total chores, Vasya's count, Petya's count)
# - Line 2: n integers (difficulty of each chore)
#
# Output: The gap between Petya's easiest and Vasya's hardest chore
#
# Approach: Sort and find difference between position b and b-1

n, a, b = map(int, input().split())
h = list(map(int, input().split()))

h.sort()

print(h[b] - h[b - 1])
```

### 334B (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/334/B
#
# Gerald is very particular to eight point sets. He thinks that any decent eight point set must consist of all pairwise intersections of three distinct integer vertical straight lines and three distinct integer horizontal straight lines, except for the average of these nine points. In other words, there must be three integers x1, x2, x3 and three more integers y1, y2, y3, such that x1 < x2 < x3, y1 < y2 < y3 and the eight point set consists of all points (xi, yj) (1 ≤ i, j ≤ 3), except for point (x2, y2).
#
# You have a set of eight points. Find out if Gerald can use this set?
#
# Input
# The input consists of eight lines, the i-th line contains two space-separated integers xi and yi (0 ≤ xi, yi ≤ 106). You do not have any other conditions for these points.
#
# Output
# In a single line print word "respectable", if the given set of points corresponds to Gerald's decency rules, and "ugly" otherwise.
#
# Examples
# input
# 0 0
# 0 1
# 0 2
# 1 0
# 1 2
# 2 0
# 2 1
# 2 2
# output
# respectable
# input
# 0 0
# 1 0
# 2 0
# 3 0
# 4 0
# 5 0
# 6 0
# 7 0
# output
# ugly
# input
# 1 1
# 1 2
# 1 3
# 2 1
# 2 2
# 2 3
# 3 1
# 3 2
# output
# ugly

x = []
y = []
for i in range(8):
    xi, yi = map(int, input().split())
    x.append(xi)
    y.append(yi)

xtmp = sorted(x)
ytmp = sorted(y)

xdist_list = [xtmp[0]]
ydist_list = [ytmp[0]]
for i in range(1, 8):
    if xtmp[i] != xtmp[i-1]:
        xdist_list.append(xtmp[i])
    if ytmp[i] != ytmp[i-1]:
        ydist_list.append(ytmp[i])

if len(xdist_list) != 3 or len(ydist_list) != 3:
    print('ugly')
    exit()

full_eight_points_set = []
for i in range(3):
    for j in range(3):
        if i != 1 or j != 1:
            found = False
            for k in range(8):
                if x[k] == xdist_list[i] and y[k] == ydist_list[j]:
                    found = True
                    break
            if not found:
                print('ugly')
                exit()
print('respectable')
```

### 37A (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/37/A

# Little Vasya has received a young builder’s kit. The kit consists of several wooden bars, the lengths of all of them are known. The bars can be put one on the top of the other if their lengths are the same.
#
# Vasya wants to construct the minimal number of towers from the bars. Help Vasya to use the bars in the best way possible.
#
# Input
# The first line contains an integer N (1 ≤ N ≤ 1000) — the number of bars at Vasya’s disposal. The second line contains N space-separated integers li — the lengths of the bars. All the lengths are natural numbers not exceeding 1000.
#
# Output
# In one line output two numbers — the height of the largest tower and their total number. Remember that Vasya should use all the bars.
#
# Examples
# input
# 3
# 1 2 3
# output
# 1 3
# input
# 4
# 6 5 6 7
# output
# 2 3

n = int(input())
L = list(map(int, input().split()))
L.sort()

number_of_towers = 1
highest_tower = 1
current_tower_height = 1

for i in range(1, n):
    if L[i] == L[i - 1]:
        current_tower_height += 1
        if current_tower_height > highest_tower:
            highest_tower = current_tower_height
    else:
        number_of_towers += 1
        current_tower_height = 1

print(highest_tower, number_of_towers, sep=' ')
```

### 439B (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/439/B

#
# Devu is a dumb guy, his learning curve is very slow. You are supposed to teach him n subjects, the ith subject has ci chapters. When you teach him, you are supposed to teach all the chapters of a subject continuously.
#
# Let us say that his initial per chapter learning power of a subject is x hours. In other words he can learn a chapter of a particular subject in x hours.
#
# Well Devu is not complete dumb, there is a good thing about him too. If you teach him a subject, then time required to teach any chapter of the next subject will require exactly 1 hour less than previously required (see the examples to understand it more clearly). Note that his per chapter learning power can not be less than 1 hour.
#
# You can teach him the n subjects in any possible order. Find out minimum amount of time (in hours) Devu will take to understand all the subjects and you will be free to do some enjoying task rather than teaching a dumb guy.
#
# Please be careful that answer might not fit in 32 bit data type.
#
# Input
# The first line will contain two space separated integers n, x (1 ≤ n, x ≤ 105). The next line will contain n space separated integers: c1, c2, ..., cn (1 ≤ ci ≤ 105).
#
# Output
# Output a single integer representing the answer to the problem.
# 
# Examples
# input
# 2 3
# 4 1
# output
# 11
# input
# 4 2
# 5 1 2 1
# output
# 10
# input
# 3 3
# 1 1 1
# output
# 6

n, x = map(int, input().split())
c = list(map(int, input().split()))

c.sort()
total_time = 0

for i in range(n):
    total_time += c[i] * x
    x = x - 1 if x > 1 else 1

print(total_time)
```

### 451B (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/451/B
#
# Problem: Sort the Array
#
# Given an array of n distinct integers, determine if you can sort it in
# ascending order by reversing exactly one contiguous segment. If possible,
# output "yes" and the segment boundaries. Otherwise, output "no".
#
# Input:
# - Line 1: Integer n (array size)
# - Line 2: n distinct integers (array elements)
#
# Output:
# - Line 1: "yes" or "no"
# - Line 2 (if yes): Start and end indices (1-based) of segment to reverse
#
# Approach: Find the single decreasing segment, check if reversing it sorts the array

n = int(input())
a = list(map(int, input().split()))

found_decreasing_segment = False
start_segment = 0
end_segment = 0

i = 0
while i < n - 1:
    if a[i] > a[i + 1]:
        if found_decreasing_segment:
            print('no')
            exit()
        start_segment = i
        found_decreasing_segment = True
        while i < n - 1 and a[i] > a[i + 1]:
            i += 1
        end_segment = i
        if (end_segment < n - 1 and a[start_segment] > a[end_segment + 1]) \
                or (start_segment > 0 and a[end_segment] < a[start_segment - 1]):
            print('no')
            exit()
    else:
        i += 1

print('yes')
print(start_segment + 1, end_segment + 1, sep=' ')
```

### 551A (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/551/A

#
# Professor GukiZ likes programming contests. He especially likes to rate his students on the contests he prepares. Now, he has decided to prepare a new contest.
#
# In total, n students will attend, and before the start, every one of them has some positive integer rating. Students are indexed from 1 to n. Let's denote the rating of i-th student as ai. After the contest ends, every student will end up with some positive integer position. GukiZ expects that his students will take places according to their ratings.
#
# He thinks that each student will take place equal to . In particular, if student A has rating strictly lower then student B, A will get the strictly better position than B, and if two students have equal ratings, they will share the same position.
#
# GukiZ would like you to reconstruct the results by following his expectations. Help him and determine the position after the end of the contest for each of his students if everything goes as expected.
#
# Input
# The first line contains integer n (1 ≤ n ≤ 2000), number of GukiZ's students.
#
# The second line contains n numbers a1, a2, ... an (1 ≤ ai ≤ 2000) where ai is the rating of i-th student (1 ≤ i ≤ n).
#
# Output
# In a single line, print the position after the end of the contest for each of n students in the same order as they appear in the input.
#
# Examples
# input
# 3
# 1 3 3
# output
# 3 1 1
# input
# 1
# 1
# output
# 1
# input
# 5
# 3 5 3 4 5
# output
# 4 1 4 3 1
# Note
# In the first sample, students 2 and 3 are positioned first (there is no other student with higher rating), and student 1 is positioned third since there are two students with higher rating.
#
# In the second sample, first student is the only one on the contest.
#
# In the third sample, students 2 and 5 share the first position with highest rating, student 4 is next with third position, and students 1 and 3 are the last sharing fourth position.

n = int(input())
a = list(map(int, input().split()))
bsorted = sorted(a, key=lambda x: -x)
ranking_list = []

for i in range(n):
    for j in range(n):
        if a[i] == bsorted[j]:
            ranking_list.append(j + 1)
            break
print(*ranking_list, sep=' ')
```

### 557B (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/557/B

# Pasha decided to invite his friends to a tea party. For that occasion, he has a large teapot with the capacity of w milliliters and 2n tea cups, each cup is for one of Pasha's friends. The i-th cup can hold at most ai milliliters of water.
#
# It turned out that among Pasha's friends there are exactly n boys and exactly n girls and all of them are going to come to the tea party. To please everyone, Pasha decided to pour the water for the tea as follows:
#
# Pasha can boil the teapot exactly once by pouring there at most w milliliters of water;
# Pasha pours the same amount of water to each girl;
# Pasha pours the same amount of water to each boy;
# if each girl gets x milliliters of water, then each boy gets 2x milliliters of water.
# In the other words, each boy should get two times more water than each girl does.
#
# Pasha is very kind and polite, so he wants to maximize the total amount of the water that he pours to his friends. Your task is to help him and determine the optimum distribution of cups between Pasha's friends.
#
# Input
# The first line of the input contains two integers, n and w (1 ≤ n ≤ 105, 1 ≤ w ≤ 109) — the number of Pasha's friends that are boys (equal to the number of Pasha's friends that are girls) and the capacity of Pasha's teapot in milliliters.
#
# The second line of the input contains the sequence of integers ai (1 ≤ ai ≤ 109, 1 ≤ i ≤ 2n) — the capacities of Pasha's tea cups in milliliters.
#
# Output
# Print a single real number — the maximum total amount of water in milliliters that Pasha can pour to his friends without violating the given conditions. Your answer will be considered correct if its absolute or relative error doesn't exceed 10 - 6.
#
# Examples
# input
# 2 4
# 1 1 1 1
# output
# 3
# input
# 3 18
# 4 4 4 2 2 2
# output
# 18
# input
# 1 5
# 2 3
# output
# 4.5
# Note
# Pasha also has candies that he is going to give to girls but that is another task...

n, w = map(int, input().split())
a = list(map(int, input().split()))

a.sort()
for_girl = min(a[0], a[n]/2)

print(min(for_girl*n*3, w))
```

