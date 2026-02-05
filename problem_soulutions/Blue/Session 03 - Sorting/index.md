---
layout: simple
title: "Sorting"
permalink: /problem_soulutions/Blue/Session 03 - Sorting/
---

# Sorting

This session covers sorting algorithms and techniques, including comparison-based sorting, custom comparators, and sorting-related problem solving.

## Problems

### Business Trip

#### Problem Information
- **Source:** Codeforces
- **Problem Code:** 149A
- **Difficulty:** Easy
- **URL:** http://codeforces.com/problemset/problem/149/A

#### Problem Statement
A flower must grow at least k centimeters. There are 12 months, and each month i has a potential growth a[i] centimeters if watered that month. Find the minimum number of months you need to water the flower to achieve at least k centimeters of growth. You can choose which months to water.

#### Input Format
- Line 1: Integer k (required growth in centimeters)
- Line 2: 12 integers (growth potential for each month)

#### Output Format
Minimum number of months needed, or -1 if impossible.

#### Solution

##### Approach
Sort months by growth potential in descending order, then greedily pick the highest growth months until target is reached.

##### Python Solution
```python
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

##### Complexity Analysis
- **Time Complexity:** O(n log n) where n=12 for sorting
- **Space Complexity:** O(1) - constant extra space

---

### Chores

#### Problem Information
- **Source:** Codeforces
- **Problem Code:** 169A
- **Difficulty:** Easy
- **URL:** http://codeforces.com/problemset/problem/169/A

#### Problem Statement
Petya and Vasya divide n chores. Vasya does the a "easiest" chores (lowest difficulty) and Petya does the b "hardest" chores (highest difficulty) where a + b = n.

The "gap" is the difference between the easiest chore Petya does and the hardest chore Vasya does. After sorting, this is h[b] - h[b-1].

#### Input Format
- Line 1: n a b (total chores, Vasya's count, Petya's count)
- Line 2: n integers (difficulty of each chore)

#### Output Format
The gap between Petya's easiest and Vasya's hardest chore.

#### Solution

##### Approach
Sort the array and find the difference between positions b and b-1.

##### Python Solution
```python
n, a, b = map(int, input().split())
h = list(map(int, input().split()))

h.sort()

print(h[b] - h[b - 1])
```

##### Complexity Analysis
- **Time Complexity:** O(n log n) - sorting the chores array
- **Space Complexity:** O(1) - in-place sorting

---

### Eight Point Set

#### Problem Information
- **Source:** Codeforces
- **Problem Code:** 334B
- **Difficulty:** Medium
- **URL:** http://codeforces.com/problemset/problem/334/B

#### Problem Statement
Gerald thinks that any decent eight point set must consist of all pairwise intersections of three distinct integer vertical straight lines and three distinct integer horizontal straight lines, except for the average of these nine points. In other words, there must be three integers x1, x2, x3 and three more integers y1, y2, y3, such that x1 < x2 < x3, y1 < y2 < y3 and the eight point set consists of all points (xi, yj), except for point (x2, y2).

Given a set of eight points, determine if it corresponds to Gerald's decency rules.

#### Input Format
Eight lines, each containing two space-separated integers xi and yi (coordinates of a point).

#### Output Format
"respectable" if the set is valid, "ugly" otherwise.

#### Solution

##### Approach
Extract and sort the unique x and y coordinates. Check that there are exactly 3 unique values for each, then verify all 8 required points (excluding center) exist.

##### Python Solution
```python
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

##### Complexity Analysis
- **Time Complexity:** O(1) - fixed size input (8 points)
- **Space Complexity:** O(1) - constant space for coordinates

---

### Towers

#### Problem Information
- **Source:** Codeforces
- **Problem Code:** 37A
- **Difficulty:** Easy
- **URL:** http://codeforces.com/problemset/problem/37/A

#### Problem Statement
Little Vasya has received a young builder's kit consisting of several wooden bars. Bars can be put one on top of another if their lengths are the same. Vasya wants to construct the minimal number of towers from the bars.

Find the height of the largest tower and the total number of towers.

#### Input Format
- Line 1: Integer N (number of bars)
- Line 2: N space-separated integers (bar lengths)

#### Output Format
Two integers - height of the largest tower and total number of towers.

#### Solution

##### Approach
Sort the bars and count consecutive groups of same length bars.

##### Python Solution
```python
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

##### Complexity Analysis
- **Time Complexity:** O(n log n) - sorting the bars
- **Space Complexity:** O(1) - constant extra space

---

### Devu and Subjects

#### Problem Information
- **Source:** Codeforces
- **Problem Code:** 439B
- **Difficulty:** Easy
- **URL:** http://codeforces.com/problemset/problem/439/B

#### Problem Statement
You need to teach Devu n subjects, where the ith subject has ci chapters. His initial per chapter learning power is x hours. If you teach him a subject, time required to teach any chapter of the next subject will require exactly 1 hour less (minimum 1 hour). You can teach the subjects in any order. Find the minimum amount of time Devu will take to understand all subjects.

#### Input Format
- Line 1: n x (number of subjects, initial learning power)
- Line 2: n space-separated integers (chapters in each subject)

#### Output Format
Minimum total time in hours.

#### Solution

##### Approach
Sort subjects by chapter count in ascending order, then teach subjects with fewer chapters first to maximize the benefit of decreasing learning time.

##### Python Solution
```python
n, x = map(int, input().split())
c = list(map(int, input().split()))

c.sort()
total_time = 0

for i in range(n):
    total_time += c[i] * x
    x = x - 1 if x > 1 else 1

print(total_time)
```

##### Complexity Analysis
- **Time Complexity:** O(n log n) - sorting the subjects
- **Space Complexity:** O(1) - constant extra space

---

### Sort the Array

#### Problem Information
- **Source:** Codeforces
- **Problem Code:** 451B
- **Difficulty:** Medium
- **URL:** http://codeforces.com/problemset/problem/451/B

#### Problem Statement
Given an array of n distinct integers, determine if you can sort it in ascending order by reversing exactly one contiguous segment. If possible, output "yes" and the segment boundaries. Otherwise, output "no".

#### Input Format
- Line 1: Integer n (array size)
- Line 2: n distinct integers (array elements)

#### Output Format
- Line 1: "yes" or "no"
- Line 2 (if yes): Start and end indices (1-based) of segment to reverse

#### Solution

##### Approach
Find the single decreasing segment in the array, then check if reversing it results in a sorted array.

##### Python Solution
```python
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

##### Complexity Analysis
- **Time Complexity:** O(n) - single pass to find the decreasing segment
- **Space Complexity:** O(1) - constant extra space

---

### Contest Positions

#### Problem Information
- **Source:** Codeforces
- **Problem Code:** 551A
- **Difficulty:** Easy
- **URL:** http://codeforces.com/problemset/problem/551/A

#### Problem Statement
In a contest with n students, each student has a rating. Students take positions according to their ratings - a student with strictly lower rating gets a strictly better position, and students with equal ratings share the same position.

Given the ratings, determine the position of each student after the contest.

#### Input Format
- Line 1: Integer n (number of students)
- Line 2: n numbers (ratings of each student)

#### Output Format
n integers representing the position of each student.

#### Solution

##### Approach
Sort the ratings in descending order, then for each original rating, find its position in the sorted array.

##### Python Solution
```python
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

##### Complexity Analysis
- **Time Complexity:** O(n^2) - nested loops for position lookup
- **Space Complexity:** O(n) - storing the sorted array and rankings

---

### Tea Party

#### Problem Information
- **Source:** Codeforces
- **Problem Code:** 557B
- **Difficulty:** Medium
- **URL:** http://codeforces.com/problemset/problem/557/B

#### Problem Statement
Pasha has n boys and n girls at a tea party. He has a teapot with capacity w and 2n cups. He wants to pour water such that each girl gets x milliliters and each boy gets 2x milliliters. Maximize the total water poured while respecting cup capacities.

#### Input Format
- Line 1: n w (number of each gender, teapot capacity)
- Line 2: 2n integers (cup capacities)

#### Output Format
Maximum total water that can be poured.

#### Solution

##### Approach
Sort cups by capacity. Girls should use smaller cups, boys use larger ones. The limiting factor is the smaller cup for girls vs half the n-th cup for boys.

##### Python Solution
```python
n, w = map(int, input().split())
a = list(map(int, input().split()))

a.sort()
for_girl = min(a[0], a[n]/2)

print(min(for_girl*n*3, w))
```

##### Complexity Analysis
- **Time Complexity:** O(n log n) - sorting the cups
- **Space Complexity:** O(1) - constant extra space

