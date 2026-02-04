---
layout: simple
title: "Session 05 - String"
permalink: /problem_soulutions/Blue/Session 05 - String/
---

# Session 05 - String

This session covers string manipulation, pattern matching, and text processing algorithms.

## Problems

### Football Winner

#### Problem Information
- **Source:** Codeforces
- **Problem Code:** 43A
- **Difficulty:** Easy
- **URL:** http://codeforces.com/problemset/problem/43/A

#### Problem Statement
Given the results of a football match where each goal is marked with the team name, determine which team won. The team that scores more goals wins. It is guaranteed the match did not end in a tie.

#### Input Format
- First line: n (number of goals)
- Next n lines: Team name for each goal

#### Output Format
The name of the winning team.

#### Solution

##### Approach
Count goals for each team using a simple counter. Track the first team and compare scores.

##### Python Solution
```python
n = int(input())
result = {}
first_team = input().strip()
first_team_score = 1
second_team = ''
for i in range(1, n):
    cur_team_score = input().strip()
    if cur_team_score != first_team:
        first_team_score -= 1
        second_team = cur_team_score
    else:
        first_team_score += 1

print(first_team if first_team_score > 0 else second_team)
```

##### Complexity Analysis
- **Time Complexity:** O(n) - single pass through input
- **Space Complexity:** O(1) - only storing two team names

---

### Suffix Data Structures

#### Problem Information
- **Source:** Codeforces
- **Problem Code:** 448B
- **Difficulty:** Medium
- **URL:** http://codeforces.com/problemset/problem/448/B

#### Problem Statement
Transform word s into word t using suffix automaton (removes one character) and suffix array (swaps two characters). Determine which data structures are needed: "automaton" (removal only), "array" (swap only), "both", or "need tree" (impossible).

#### Input Format
- First line: String s
- Second line: String t

#### Output Format
One of: "automaton", "array", "both", or "need tree".

#### Solution

##### Approach
Check character frequencies. If same length, only swaps needed. If t is subsequence of s, only removals needed. Otherwise, both needed.

##### Python Solution
```python
def check_solution(_s, _t):
    is_array = False

    s_map = [0] * 26
    t_map = [0] * 26

    s_length = len(_s)
    t_length = len(_t)

    for i in range(s_length):
        s_map[ord(_s[i]) - 97] += 1

    for i in range(t_length):
        t_map[ord(_t[i]) - 97] += 1

    for i in range(26):
        if s_map[i] < t_map[i]:
            return 'need tree'

    if s_length == t_length:
        return 'array'

    s_left = 0
    t_left = 0
    while True:
        if s_left >= s_length or t_left >= t_length:
            break
        if _s[s_left] != _t[t_left]:
            s_left += 1
        else:
            s_left += 1
            t_left += 1
        if s_length - s_left < t_length - t_left:
            is_array = True
            break

    if is_array:
        return 'both'

    return 'automaton'


s = input()
t = input()

print(check_solution(s, t))
```

##### Complexity Analysis
- **Time Complexity:** O(n) - character frequency counting and subsequence check
- **Space Complexity:** O(1) - fixed-size frequency arrays

---

### Lecture Notes

#### Problem Information
- **Source:** Codeforces
- **Problem Code:** 499B
- **Difficulty:** Easy
- **URL:** http://codeforces.com/problemset/problem/499/B

#### Problem Statement
You know two languages with one-to-one word correspondence. During a lecture, write each word in whichever language has the shorter form. If equal length, prefer the first language.

#### Input Format
- First line: n m (words in lecture, dictionary size)
- Next m lines: Word pairs (first language, second language)
- Last line: n lecture words (in first language)

#### Output Format
The lecture with each word in its shortest form.

#### Solution

##### Approach
Build a dictionary mapping first language words to their pairs. For each lecture word, output the shorter version.

##### Python Solution
```python
def get_shorter(ci, _a, _b):
    _i = 0
    while ci != _a[_i]:
        _i += 1

    return _a[_i] if len(_a[_i]) <= len(_b[_i]) else _b[_i]


n, m = map(int, input().split())
a = []
b = []
for i in range(m):
    ai, bi = input().split()
    a.append(ai)
    b.append(bi)
c = input().split()

result = []

for i in range(n):
    result.append(get_shorter(c[i], a, b))

print(*result, sep=' ')
```

##### Complexity Analysis
- **Time Complexity:** O(n * m) - linear search for each word
- **Space Complexity:** O(m) - storing dictionary

---

### Lexicographically Between

#### Problem Information
- **Source:** Codeforces
- **Problem Code:** 518A
- **Difficulty:** Medium
- **URL:** http://codeforces.com/problemset/problem/518/A

#### Problem Statement
Given two strings s and t of equal length where s < t lexicographically, find a string that is lexicographically greater than s and less than t.

#### Input Format
- First line: String s
- Second line: String t

#### Output Format
A string between s and t, or "No such string".

#### Solution

##### Approach
Try to increment s to find a string between s and t. Handle carry-over carefully.

##### Python Solution
```python
s = input().strip()
t = input().strip()
first_smaller = -1
result = 'No such string'
for i in range(len(s)):
    if ord(t[i]) - ord(s[i]) >= 2:
        result = s[:i] + chr(ord(s[i]) + 1) + s[i + 1:]
        break
    if ord(t[i]) > ord(s[i]):
        first_smaller = i
        break

if first_smaller >= 0:
    if s[first_smaller + 1:] >= t[first_smaller + 1:]:
        for i in range(first_smaller + 1, len(t)):
            if t[i] is not 'a':
                result = s[:first_smaller] + chr(ord(s[first_smaller]) + 1) + t[first_smaller + 1:i] + chr(
                    ord(t[i]) - 1) + t[i + 1:]
                break
            if s[i] is not 'z':
                result = s[:i] + chr(ord(s[i]) + 1) + s[i + 1:]
                break
    elif s[first_smaller + 1:] < t[first_smaller + 1:]:
        result = s[:first_smaller] + chr(ord(s[first_smaller]) + 1) + s[first_smaller + 1:]

print(result)
```

##### Complexity Analysis
- **Time Complexity:** O(n) - single pass through strings
- **Space Complexity:** O(n) - storing result string

---

### Tanya's Birthday Postcard

#### Problem Information
- **Source:** Codeforces
- **Problem Code:** 518B
- **Difficulty:** Medium
- **URL:** http://codeforces.com/problemset/problem/518/B

#### Problem Statement
Tanya wants to create a message of length n from letters cut from a newspaper. Count how many exact matches ("YAY!") and case-insensitive matches ("WHOOPS") she can make.

#### Input Format
- First line: String s (message to create)
- Second line: String t (newspaper letters)

#### Output Format
Two integers: number of YAY! and WHOOPS matches.

#### Solution

##### Approach
Count character frequencies for both strings, matching exact case first, then wrong case.

##### Python Solution
```python
s = input().strip()
t = input().strip()

yay = 0
whoops = 0

slength = len(s)
tlength = len(t)

s_map = [0] * 58
t_map = [0] * 58
up_low_distance = 32

for i in range(slength):
    s_map[ord(s[i]) - 65] += 1

for i in range(tlength):
    t_map[ord(t[i]) - 65] += 1

for i in range(26):
    # Go with YAY!
    if t_map[i] >= s_map[i]:
        yay += s_map[i]
        t_map[i] -= s_map[i]
        s_map[i] = 0
    else:
        yay += t_map[i]
        s_map[i] -= t_map[i]
        t_map[i] = 0

    if t_map[i + up_low_distance] >= s_map[i + up_low_distance]:
        yay += s_map[i + up_low_distance]
        t_map[i + up_low_distance] -= s_map[i + up_low_distance]
        s_map[i + up_low_distance] = 0
    else:
        yay += t_map[i + up_low_distance]
        s_map[i + up_low_distance] -= t_map[i + up_low_distance]
        t_map[i + up_low_distance] = 0

    # Go with WHOOPS
    if t_map[i] >= s_map[i + up_low_distance]:
        whoops += s_map[i + up_low_distance]
        t_map[i] -= s_map[i + up_low_distance]
        s_map[i + up_low_distance] = 0
    else:
        whoops += t_map[i]
        s_map[i + up_low_distance] -= t_map[i]
        t_map[i] = 0

    if t_map[i + up_low_distance] >= s_map[i]:
        whoops += s_map[i]
        t_map[i + up_low_distance] -= s_map[i]
        s_map[i] = 0
    else:
        whoops += t_map[i + up_low_distance]
        s_map[i] -= t_map[i + up_low_distance]
        t_map[i + up_low_distance] = 0

print(yay, whoops)
```

##### Complexity Analysis
- **Time Complexity:** O(n + m) - counting frequencies for both strings
- **Space Complexity:** O(1) - fixed-size frequency arrays

---

### String Concatenation

#### Problem Information
- **Source:** Codeforces
- **Problem Code:** 61B
- **Difficulty:** Medium
- **URL:** http://codeforces.com/problemset/problem/61/B

#### Problem Statement
Given three strings, students concatenate them in any order. Check if a student's answer matches any valid concatenation (ignoring case and special characters like "-", ";", "_").

#### Input Format
- First three lines: Original strings
- Fourth line: n (number of students)
- Next n lines: Student answers

#### Output Format
"ACC" if correct, "WA" if wrong for each student.

#### Solution

##### Approach
Normalize all strings (remove special chars, convert to lowercase), then check if student answer matches any of the 6 possible permutations.

##### Python Solution
```python
str11 = input().strip().replace(';', '').replace('-', '').replace('_', '').lower()
str12 = input().strip().replace(';', '').replace('-', '').replace('_', '').lower()
str13 = input().strip().replace(';', '').replace('-', '').replace('_', '').lower()

n = int(input())
for i in range(n):
    ai = input().strip().replace(';', '').replace('-', '').replace('_', '').lower()
    if len(ai) != len(str11) + len(str12) + len(str13):
        print('WA')
        continue
    if (str11 + str12 + str13) == ai or (str11 + str13 + str12) == ai or (str12 + str11 + str13) == ai or (
            str12 + str13 + str11) == ai or (str13 + str11 + str12) == ai or (str13 + str12 + str11) == ai:
        print('ACC')
        continue
    print('WA')
```

##### Complexity Analysis
- **Time Complexity:** O(n * L) where L is total string length
- **Space Complexity:** O(L) - storing normalized strings

---

### Password Security

#### Problem Information
- **Source:** Codeforces
- **Problem Code:** 721B
- **Difficulty:** Medium
- **URL:** http://codeforces.com/problemset/problem/721/B

#### Problem Statement
Vanya tries passwords in order of increasing length, with same-length passwords in arbitrary order. After k wrong attempts, he waits 5 seconds. Find the best and worst case time to enter the correct password.

#### Input Format
- First line: n k (number of passwords, wrong attempts before wait)
- Next n lines: passwords
- Last line: correct password

#### Output Format
Two integers: best case and worst case time in seconds.

#### Solution

##### Approach
Sort passwords by length, find the position range of the correct password, calculate time including 5-second penalties.

##### Python Solution
```python
n, k = map(int, input().split())

passwords = []
for i in range(n):
    passwords.append(input())

passwords = sorted(passwords, key=lambda x: -len(x))
correct_pwd = input()
right_break_point = n - 1
left_break_point = 0
for i in range(n - 1, -1, -1):
    if len(correct_pwd) == len(passwords[i]):
        right_break_point = i
        break

for i in range(right_break_point, -1, -1):
    if len(correct_pwd) != len(passwords[i]):
        left_break_point = i + 1
        break

same_length_list = passwords[left_break_point:right_break_point + 1]

number_of_corrects = 0
for i in range(len(same_length_list)):
    if same_length_list[i] == correct_pwd:
        number_of_corrects += 1

counter_best_case = n - right_break_point
counter_worst_case = n - (left_break_point + number_of_corrects - 1)
best_case_mod = 1 if counter_best_case % k == 0 and counter_best_case // k > 0 else 0
worst_case_mod = 1 if counter_worst_case % k == 0 and counter_worst_case // k > 0 else 0
best_case = counter_best_case + (counter_best_case // k - best_case_mod) * 5
worst_case = counter_worst_case + (counter_worst_case // k - worst_case_mod) * 5

print(best_case, worst_case)
```

##### Complexity Analysis
- **Time Complexity:** O(n log n) - sorting passwords
- **Space Complexity:** O(n) - storing passwords

---

### Embosser Rotations

#### Problem Information
- **Source:** Codeforces
- **Problem Code:** 731A
- **Difficulty:** Easy
- **URL:** http://codeforces.com/problemset/problem/731/A

#### Problem Statement
An embosser has a wheel with letters arranged in a circle. Starting at 'a', find the minimum number of rotations (clockwise or counterclockwise) to print a given string.

#### Input Format
A single string (the exhibit name).

#### Output Format
Minimum number of rotations.

#### Solution

##### Approach
For each character, calculate the minimum of clockwise and counterclockwise distance from current position.

##### Python Solution
```python
ex_name = input()
result = 0
cur_pos = 97
for c in ex_name:
    result += min(abs(ord(c) - cur_pos), 26 - abs(ord(c) - cur_pos))
    cur_pos = ord(c)
print(result)
```

##### Complexity Analysis
- **Time Complexity:** O(n) - single pass through string
- **Space Complexity:** O(1) - constant extra space

---

### African Crossword

#### Problem Information
- **Source:** Codeforces
- **Problem Code:** 90B
- **Difficulty:** Medium
- **URL:** http://codeforces.com/problemset/problem/90/B

#### Problem Statement
In a rectangular grid, cross out all letters that appear more than once in their row or column. The remaining letters form the encrypted word (read left to right, top to bottom).

#### Input Format
- First line: n m (grid dimensions)
- Next n lines: m characters each (the grid)

#### Output Format
The encrypted word.

#### Solution

##### Approach
Mark each cell if its letter repeats in the same row or column. Output unmarked letters in order.

##### Python Solution
```python
n, m = map(int, input().split())
rectangular = []
result = ''

matrix = [[0 for i in range(m)] for j in range(n)]

for i in range(n):
    rectangular.append(input())

for i in range(n):
    for j in range(m):
        if matrix[i][j] == 0:
            for row_checker in range(m):
                if row_checker != j and rectangular[i][row_checker] == rectangular[i][j]:
                    matrix[i][row_checker] = 1
                    matrix[i][j] = 1
            for col_checker in range(n):
                if col_checker != i and rectangular[col_checker][j] == rectangular[i][j]:
                    matrix[col_checker][j] = 1
                    matrix[i][j] = 1


for i in range(n):
    for j in range(m):
        if matrix[i][j] == 0:
            result += rectangular[i][j]

print(result)
```

##### Complexity Analysis
- **Time Complexity:** O(n * m * (n + m)) - checking row and column for each cell
- **Space Complexity:** O(n * m) - storing the marking matrix

