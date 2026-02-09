---
layout: simple
title: "Algorithmic Complexity"
permalink: /problem_soulutions/Blue/Session 02 - Algorithmic Complexity/
---

# Algorithmic Complexity

This session covers algorithmic complexity analysis, including time and space complexity, Big O notation, and optimization techniques.

## Problems

### Soldier and Vests

#### Problem Information
- **Source:** [Codeforces 161A](https://codeforces.com/problemset/problem/161/A)
- **Difficulty:** Easy

#### Problem Statement
There are n soldiers and m vests. Each soldier has a size a[i], and each vest has a size b[i]. A soldier can wear a vest if the vest size is in the range [a[i] - x, a[i] + y]. Both arrays are sorted in ascending order.

Find the maximum number of soldiers that can receive vests, and output the pairs (soldier index, vest index) for each assignment.

#### Input Format
- Line 1: n m x y (soldiers, vests, lower tolerance, upper tolerance)
- Line 2: n integers (soldier sizes, sorted ascending)
- Line 3: m integers (vest sizes, sorted ascending)

#### Output Format
- Line 1: Number of soldiers who get vests
- Next lines: Pairs of (soldier index, vest index) - 1-based

#### Example
```
Input:
5 3 0 0
1 2 3 3 4
1 3 5

Output:
2
1 1
3 2
```
Soldier 1 (size 1) gets vest 1 (size 1). Soldier 3 (size 3) gets vest 2 (size 3).

#### Solution

##### Approach
Use two-pointer technique on sorted arrays to efficiently match soldiers with vests.

##### Python Solution
```python
n, m, x, y = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

u, v = [], []

sindex = 0
vindex = 0

while True:

  while vindex < m and a[sindex] - x > b[vindex]:  # too small
    vindex += 1  # Add vest's size

  if vindex >= m:
    break

  while sindex < n and a[sindex] + y < b[vindex]:  # too big
    sindex += 1  # Add solider's size

  if sindex >= n:
    break

  if a[sindex] - x > b[vindex]:
    continue

  u.append(sindex + 1)
  v.append(vindex + 1)

  sindex += 1
  vindex += 1

  if sindex >= n or vindex >= m:
    break

print(len(u))
for i in range(len(u)):
  print(u[i], v[i], sep=' ')
```

##### Complexity Analysis
- **Time Complexity:** O(n + m) - single pass through both arrays
- **Space Complexity:** O(n) - storing the matching pairs

---

### Distinct K Segment

#### Problem Information
- **Source:** [Codeforces 224B](https://codeforces.com/problemset/problem/224/B)
- **Difficulty:** Medium

#### Problem Statement
Given an array of n integers and a number k, find the shortest contiguous segment that contains exactly k distinct values. Output the 1-based start and end positions of this segment.

#### Input Format
- Line 1: n k (array size, required distinct count)
- Line 2: n integers (array elements, values up to 100000)

#### Output Format
Two integers - start and end positions (1-based), or "-1 -1" if no such segment exists.

#### Example
```
Input:
5 3
1 2 1 3 2

Output:
2 4
```
Segment [2,4] contains values {2, 1, 3} - exactly 3 distinct values.

```
Input:
5 5
1 2 1 3 2

Output:
-1 -1
```
Array only has 3 distinct values, impossible to find segment with 5 distinct.

#### Solution

##### Approach
Use sliding window with two pointers. Expand right to add elements until we have k distinct values, then shrink left to find the shortest valid segment.

##### Python Solution
```python
from collections import defaultdict

n, k = map(int, input().split())
a = list(map(int, input().split()))

freq = defaultdict(int)
left = 0
result = (-1, -1)
min_len = float('inf')

for right in range(n):
    freq[a[right]] += 1

    # Shrink window while we have exactly k distinct values
    while len(freq) == k:
        if right - left + 1 < min_len:
            min_len = right - left + 1
            result = (left + 1, right + 1)

        freq[a[left]] -= 1
        if freq[a[left]] == 0:
            del freq[a[left]]
        left += 1

print(result[0], result[1])
```

##### Complexity Analysis
- **Time Complexity:** O(n) - each element is added and removed at most once
- **Space Complexity:** O(k) - frequency dictionary stores at most k distinct values

---

### Books

#### Problem Information
- **Source:** [Codeforces 279B](https://codeforces.com/problemset/problem/279/B)
- **Difficulty:** Easy

#### Problem Statement
Valera has n books on a shelf. Each book i takes a[i] minutes to read. He has t minutes of free time and wants to read as many CONSECUTIVE books as possible (starting from any position). Find the maximum number of consecutive books he can completely read within time t.

#### Input Format
- Line 1: n t (number of books, available time)
- Line 2: n integers (reading time for each book)

#### Output Format
Maximum number of consecutive books that can be read.

#### Example
```
Input:
4 5
3 1 2 1

Output:
3
```
Books 2, 3, 4 take 1+2+1=4 minutes, which is within 5 minutes. That's 3 consecutive books.

```
Input:
3 3
2 2 2

Output:
1
```
Each book takes 2 minutes, can only read 1 book completely in 3 minutes.

#### Solution

##### Approach
Use sliding window / two-pointer technique to find the maximum window where sum of reading times does not exceed t.

##### Python Solution
```python
n, t = map(int, input().split())
a = list(map(int, input().split()))

total_time = 0

left = 0
right = 0

max_total_book = 0
max_left = 0

while True:

  while right < n and total_time + a[right] <= t:
    total_time += a[right]
    right += 1

  while total_time > t:
    total_time -= a[left]
    left += 1

  if right - left > max_total_book:
    max_total_book = right - left
    max_left = left

  if right < n:
    total_time += a[right]
    right += 1
  else:
    break

print(max_total_book)
```

##### Complexity Analysis
- **Time Complexity:** O(n) - each element is visited at most twice
- **Space Complexity:** O(1) - constant extra space

---

### Sereja and Dima

#### Problem Information
- **Source:** [Codeforces 381A](https://codeforces.com/problemset/problem/381/A)
- **Difficulty:** Easy

#### Problem Statement
n cards are laid out in a row, each with a value. Sereja and Dima play a game where they take turns picking cards. On each turn, a player can take either the leftmost or rightmost card. Both players play optimally (always pick the card with the higher value). Sereja goes first.

Calculate the final scores of both players.

#### Input Format
- Line 1: Integer n (number of cards)
- Line 2: n integers (card values)

#### Output Format
Two integers - Sereja's score and Dima's score.

#### Example
```
Input:
4
4 1 2 10

Output:
12 5
```
Turn 1 (Sereja): picks 10 (right). Turn 2 (Dima): picks 4 (left). Turn 3 (Sereja): picks 2 (right). Turn 4 (Dima): picks 1.

```
Input:
5
5 2 4 8 3

Output:
15 7
```

#### Solution

##### Approach
Use two-pointer simulation from both ends, greedily selecting the larger card at each turn.

##### Python Solution
```python
n = int(input())
cards = list(map(int, input().split()))

Sereja = 0
Dima = 0

left = 0
right = n - 1

while True:
  if cards[left] > cards[right]:
    Sereja += cards[left]
    left += 1
  else:
    Sereja += cards[right]
    right -= 1
  if left > right:
    break
  if cards[left] > cards[right]:
    Dima += cards[left]
    left += 1
  else:
    Dima += cards[right]
    right -= 1
  if left > right:
    break

print(Sereja, Dima, sep=' ')
```

##### Complexity Analysis
- **Time Complexity:** O(n) - single pass through the array
- **Space Complexity:** O(1) - constant extra space

---

### George and Round

#### Problem Information
- **Source:** [Codeforces 387B](https://codeforces.com/problemset/problem/387/B)
- **Difficulty:** Easy

#### Problem Statement
George wants to prepare a programming contest with n problems of specific difficulties a[1], a[2], ..., a[n]. He has m prepared problems with difficulties b[1], b[2], ..., b[m]. Both arrays are sorted in non-decreasing order.

A prepared problem with difficulty b[j] can be used for a required problem with difficulty a[i] if b[j] >= a[i]. Each prepared problem can be used at most once. Find the minimum number of NEW problems George must create.

#### Input Format
- Line 1: n m (required problems, prepared problems)
- Line 2: n integers (required difficulties, sorted)
- Line 3: m integers (prepared difficulties, sorted)

#### Output Format
Minimum number of new problems to create.

#### Example
```
Input:
3 5
1 2 3
1 1 1 1 1

Output:
2
```
Need difficulties [1,2,3]. Only prepared problem with difficulty 1 can cover requirement 1. Need to create 2 new problems.

```
Input:
3 3
1 2 3
3 3 3

Output:
2
```
Prepared difficulty 3 can cover requirement 3, but need 2 more problems for requirements 1 and 2.

#### Solution

##### Approach
Use two-pointer greedy matching - for each required difficulty, find the smallest prepared problem that satisfies it.

##### Python Solution
```python
n, m = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

needed_problem_index = 0
prepared_problem_index = 0

while True:

  while prepared_problem_index < m and b[prepared_problem_index] < a[needed_problem_index]:
    prepared_problem_index += 1

  if prepared_problem_index >= m:
    break

  prepared_problem_index += 1

  needed_problem_index += 1

  if prepared_problem_index >= m:
    break

  if needed_problem_index >= n:
    break

print(n - needed_problem_index)
```

##### Complexity Analysis
- **Time Complexity:** O(n + m) - single pass through both arrays
- **Space Complexity:** O(1) - constant extra space

---

### Almost Constant Range

#### Problem Information
- **Source:** [Codeforces 602B](https://codeforces.com/problemset/problem/602/B)
- **Difficulty:** Medium

#### Problem Statement
Given an array of n integers, find the length of the longest contiguous subarray where the difference between the maximum and minimum values is at most 1 (i.e., max - min <= 1).

#### Input Format
- Line 1: Integer n (array size)
- Line 2: n integers (array elements)

#### Output Format
Length of the longest "almost constant" subarray.

#### Example
```
Input:
5
1 2 3 3 2

Output:
4
```
Subarray [2,3,3,2] has max=3, min=2, difference=1 which satisfies <= 1.

```
Input:
6
6 5 5 4 5 6

Output:
4
```
Subarray [5,5,4,5] has max=5, min=4, difference=1.

#### Solution

##### Approach
Use sliding window technique while tracking minimum and maximum values in the current window.

##### Python Solution
```python
n = int(input())
a = list(map(int, input().split()))

left, right = 0, 0
max_almost_constant_range = 1
evaluating_range = 1
range_max = a[0]
range_min = a[0]

while True:
  if right >= n - 1:
    break
  right += 1
  if a[right] > range_max and range_max - range_min >= 1:
    range_max = a[right]
    if max_almost_constant_range <= evaluating_range:
      max_almost_constant_range = evaluating_range
    evaluating_range = 1
    for i in range(right - 1, left - 1, -1):
      if a[i] == range_min:
        left = i + 1
        range_min += 1
        break
      evaluating_range += 1
  elif a[right] < range_min and range_max - range_min >= 1:
    range_min = a[right]
    if max_almost_constant_range <= evaluating_range:
      max_almost_constant_range = evaluating_range
    evaluating_range = 1
    for i in range(right - 1, left - 1, -1):
      if a[i] == range_max:
        left = i + 1
        range_max -= 1
        break
      evaluating_range += 1
  else:
    if a[right] > range_max:
      range_max = a[right]
    elif a[right] < range_min:
      range_min = a[right]
    evaluating_range += 1
    if max_almost_constant_range < evaluating_range:
      max_almost_constant_range = evaluating_range
print(max_almost_constant_range)
```

##### Complexity Analysis
- **Time Complexity:** O(n) - amortized linear time with sliding window
- **Space Complexity:** O(1) - constant extra space

---

### Alice, Bob and Chocolate

#### Problem Information
- **Source:** [Codeforces 6C](https://codeforces.com/problemset/problem/6/C)
- **Difficulty:** Easy

#### Problem Statement
n chocolate bars are lined up. Alice starts eating from the left side, Bob starts from the right side. They eat simultaneously and continuously. Each bar i takes t[i] seconds to eat. When they meet (or would overlap), they stop. If they finish a chocolate at the same time and there's one bar left, Alice gets it.

Determine how many chocolates each person eats.

#### Input Format
- Line 1: Integer n (number of chocolates)
- Line 2: n integers (time to eat each chocolate)

#### Output Format
Two integers - chocolates eaten by Alice and Bob.

#### Example
```
Input:
5
2 9 8 2 7

Output:
2 3
```
Alice eats chocolates 1,2 (times 2,9), Bob eats 3,4,5 (times 8,2,7). They meet after Alice finishes chocolate 2.

#### Solution

##### Approach
Use two-pointer simulation with time tracking from both ends.

##### Python Solution
```python
n = int(input())
t = list(map(int, input().split()))

alice_eating_index = 0
bob_eating_index = n - 1
while True:
  if alice_eating_index >= bob_eating_index - 1:
    break
  if t[alice_eating_index] > t[bob_eating_index]:
    t[alice_eating_index] -= t[bob_eating_index]
    bob_eating_index -= 1
  elif t[alice_eating_index] < t[bob_eating_index]:
    t[bob_eating_index] -= t[alice_eating_index]
    alice_eating_index += 1
  else:
    if bob_eating_index - alice_eating_index == 2:
      alice_eating_index += 1
    else:
      alice_eating_index += 1
      bob_eating_index -= 1


print(alice_eating_index + 1, n - alice_eating_index - 1)
```

##### Complexity Analysis
- **Time Complexity:** O(n) - each chocolate is processed once
- **Space Complexity:** O(1) - constant extra space (modifying input array)

---

### Wrath (Survivors)

#### Problem Information
- **Source:** [Codeforces 892B](https://codeforces.com/problemset/problem/892/B)
- **Difficulty:** Medium

#### Problem Statement
n people stand in a line (positions 1 to n, left to right). Each person i has a weapon that can kill L[i] people to their left. At time 0, everyone swings simultaneously. A person survives if they are not killed by anyone to their right.

Count how many people survive after everyone swings.

#### Input Format
- Line 1: Integer n (number of people)
- Line 2: n integers L[i] (kill range for each person)

#### Output Format
Number of survivors.

#### Example
```
Input:
4
0 1 0 10

Output:
1
```
Person 4 kills 3 people to their left (persons 1,2,3). Only person 4 survives.

```
Input:
2
0 0

Output:
2
```
No one has killing range, both survive.

#### Solution

##### Approach
Process from right to left, tracking kill coverage and counting survivors.

##### Python Solution
```python
n = int(input())
L = list(map(int, input().split()))

total_people = n
last_kill = 0
for i in range(n - 1, 0, -1):
  if L[i] > last_kill:
    if L[i] < i:
      total_people -= (L[i] - last_kill)
      last_kill = L[i] - 1
    else:
      total_people -= (i - last_kill)
      break
  else:
    last_kill = last_kill - 1 if last_kill > 0 else 0
print(total_people)
```

##### Complexity Analysis
- **Time Complexity:** O(n) - single pass from right to left
- **Space Complexity:** O(1) - constant extra space

