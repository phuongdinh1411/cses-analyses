---
layout: simple
title: "String"
permalink: /problem_soulutions/Blue/Session 05 - String/
---

# String

This session covers string manipulation, pattern matching, and text processing algorithms.

## Problems

### Football Winner

#### Problem Information
- **Source:** [Codeforces 43A](https://codeforces.com/problemset/problem/43/A)
- **Difficulty:** Easy

#### Problem Statement
Given the results of a football match where each goal is marked with the team name, determine which team won. The team that scores more goals wins. It is guaranteed the match did not end in a tie.

#### Input Format
- First line: n (number of goals)
- Next n lines: Team name for each goal

#### Output Format
The name of the winning team.

#### Example
```
Input:
4
TeamA
TeamA
TeamB
TeamA

Output:
TeamA
```
TeamA scored 3 goals, TeamB scored 1. TeamA wins.

#### Solution

##### Approach
Count goals for each team using a simple counter. Track the first team and compare scores.

##### Python Solution
```python
from collections import Counter

n = int(input())
goals = [input().strip() for _ in range(n)]
goal_count = Counter(goals)
print(max(goal_count, key=goal_count.get))
```

##### Complexity Analysis
- **Time Complexity:** O(n) - single pass through input
- **Space Complexity:** O(1) - only storing two team names

---

### Suffix Data Structures

#### Problem Information
- **Source:** [Codeforces 448B](https://codeforces.com/problemset/problem/448/B)
- **Difficulty:** Medium

#### Problem Statement
Transform word s into word t using suffix automaton (removes one character) and suffix array (swaps two characters). Determine which data structures are needed: "automaton" (removal only), "array" (swap only), "both", or "need tree" (impossible).

#### Input Format
- First line: String s
- Second line: String t

#### Output Format
One of: "automaton", "array", "both", or "need tree".

#### Example
```
Input:
abacaba
aaba

Output:
automaton
```
"aaba" is a subsequence of "abacaba" - can be obtained by removing characters only.

```
Input:
abc
bca

Output:
array
```
Same length, same characters, need only swaps.

#### Solution

##### Approach
Check character frequencies. If same length, only swaps needed. If t is subsequence of s, only removals needed. Otherwise, both needed.

##### Python Solution
```python
from collections import Counter

def check_solution(s, t):
    s_count, t_count = Counter(s), Counter(t)

    # Check if t has characters not available in s
    if any(t_count[c] > s_count[c] for c in t_count):
        return 'need tree'

    # Same length means only swaps needed
    if len(s) == len(t):
        return 'array'

    # Check if t is a subsequence of s
    s_idx, t_idx = 0, 0
    while s_idx < len(s) and t_idx < len(t):
        if s[s_idx] == t[t_idx]:
            t_idx += 1
        s_idx += 1
        # Not enough chars left in s to match remaining t
        if len(s) - s_idx < len(t) - t_idx:
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
- **Source:** [Codeforces 499B](https://codeforces.com/problemset/problem/499/B)
- **Difficulty:** Easy

#### Problem Statement
You know two languages with one-to-one word correspondence. During a lecture, write each word in whichever language has the shorter form. If equal length, prefer the first language.

#### Input Format
- First line: n m (words in lecture, dictionary size)
- Next m lines: Word pairs (first language, second language)
- Last line: n lecture words (in first language)

#### Output Format
The lecture with each word in its shortest form.

#### Example
```
Input:
4 3
codeforces codesexy
contest round
letter message
codeforces contest letter contest

Output:
codeforces round letter round
```
"codeforces" (10) vs "codesexy" (8) → keep "codeforces" (equal, prefer first). "contest" (7) vs "round" (5) → use "round".

#### Solution

##### Approach
Build a dictionary mapping first language words to their pairs. For each lecture word, output the shorter version.

##### Python Solution
```python
n, m = map(int, input().split())
dictionary = {}
for _ in range(m):
    word1, word2 = input().split()
    dictionary[word1] = word1 if len(word1) <= len(word2) else word2

lecture = input().split()
result = [dictionary[word] for word in lecture]
print(' '.join(result))
```

##### Complexity Analysis
- **Time Complexity:** O(n * m) - linear search for each word
- **Space Complexity:** O(m) - storing dictionary

---

### Lexicographically Between

#### Problem Information
- **Source:** [Codeforces 518A](https://codeforces.com/problemset/problem/518/A)
- **Difficulty:** Medium

#### Problem Statement
Given two strings s and t of equal length where s < t lexicographically, find a string that is lexicographically greater than s and less than t.

#### Input Format
- First line: String s
- Second line: String t

#### Output Format
A string between s and t, or "No such string".

#### Example
```
Input:
abc
abe

Output:
abd
```
"abc" < "abd" < "abe"

```
Input:
a
b

Output:
No such string
```
No string exists between "a" and "b".

#### Solution

##### Approach
Try to increment s to find a string between s and t. Handle carry-over carefully.

##### Python Solution
```python
s = input().strip()
t = input().strip()
result = 'No such string'

for i, (sc, tc) in enumerate(zip(s, t)):
    diff = ord(tc) - ord(sc)
    if diff >= 2:
        result = s[:i] + chr(ord(sc) + 1) + s[i + 1:]
        break
    if diff == 1:
        first_smaller = i
        if s[first_smaller + 1:] >= t[first_smaller + 1:]:
            for j in range(first_smaller + 1, len(t)):
                if t[j] != 'a':
                    result = (s[:first_smaller] + chr(ord(s[first_smaller]) + 1) +
                              t[first_smaller + 1:j] + chr(ord(t[j]) - 1) + t[j + 1:])
                    break
                if s[j] != 'z':
                    result = s[:j] + chr(ord(s[j]) + 1) + s[j + 1:]
                    break
        else:
            result = s[:first_smaller] + chr(ord(s[first_smaller]) + 1) + s[first_smaller + 1:]
        break

print(result)
```

##### Complexity Analysis
- **Time Complexity:** O(n) - single pass through strings
- **Space Complexity:** O(n) - storing result string

---

### Tanya's Birthday Postcard

#### Problem Information
- **Source:** [Codeforces 518B](https://codeforces.com/problemset/problem/518/B)
- **Difficulty:** Medium

#### Problem Statement
Tanya wants to create a message of length n from letters cut from a newspaper. Count how many exact matches ("YAY!") and case-insensitive matches ("WHOOPS") she can make.

#### Input Format
- First line: String s (message to create)
- Second line: String t (newspaper letters)

#### Output Format
Two integers: number of YAY! and WHOOPS matches.

#### Example
```
Input:
AbC
abc

Output:
1 2
```
'b' matches exactly (YAY!). 'A' uses 'a' (wrong case, WHOOPS). 'C' uses 'c' (wrong case, WHOOPS).

#### Solution

##### Approach
Count character frequencies for both strings, matching exact case first, then wrong case.

##### Python Solution
```python
from collections import Counter

s = input().strip()
t = input().strip()

s_count = Counter(s)
t_count = Counter(t)

yay = whoops = 0

for c in s_count:
    # Exact match (YAY!)
    matched = min(s_count[c], t_count[c])
    yay += matched
    s_count[c] -= matched
    t_count[c] -= matched

for c in s_count:
    # Case-insensitive match (WHOOPS)
    opposite = c.swapcase()
    matched = min(s_count[c], t_count[opposite])
    whoops += matched
    s_count[c] -= matched
    t_count[opposite] -= matched

print(yay, whoops)
```

##### Complexity Analysis
- **Time Complexity:** O(n + m) - counting frequencies for both strings
- **Space Complexity:** O(1) - fixed-size frequency arrays

---

### String Concatenation

#### Problem Information
- **Source:** [Codeforces 61B](https://codeforces.com/problemset/problem/61/B)
- **Difficulty:** Medium

#### Problem Statement
Given three strings, students concatenate them in any order. Check if a student's answer matches any valid concatenation (ignoring case and special characters like "-", ";", "_").

#### Input Format
- First three lines: Original strings
- Fourth line: n (number of students)
- Next n lines: Student answers

#### Output Format
"ACC" if correct, "WA" if wrong for each student.

#### Example
```
Input:
a
b
c
2
abc
xyz

Output:
ACC
WA
```
"abc" matches "a"+"b"+"c". "xyz" doesn't match any permutation.

#### Solution

##### Approach
Normalize all strings (remove special chars, convert to lowercase), then check if student answer matches any of the 6 possible permutations.

##### Python Solution
```python
from itertools import permutations

def normalize(s):
    return s.strip().replace(';', '').replace('-', '').replace('_', '').lower()

strings = [normalize(input()) for _ in range(3)]
valid_combinations = {''.join(p) for p in permutations(strings)}
expected_len = sum(len(s) for s in strings)

n = int(input())
for _ in range(n):
    answer = normalize(input())
    if len(answer) == expected_len and answer in valid_combinations:
        print('ACC')
    else:
        print('WA')
```

##### Complexity Analysis
- **Time Complexity:** O(n * L) where L is total string length
- **Space Complexity:** O(L) - storing normalized strings

---

### Password Security

#### Problem Information
- **Source:** [Codeforces 721B](https://codeforces.com/problemset/problem/721/B)
- **Difficulty:** Medium

#### Problem Statement
Vanya tries passwords in order of increasing length, with same-length passwords in arbitrary order. After k wrong attempts, he waits 5 seconds. Find the best and worst case time to enter the correct password.

#### Input Format
- First line: n k (number of passwords, wrong attempts before wait)
- Next n lines: passwords
- Last line: correct password

#### Output Format
Two integers: best case and worst case time in seconds.

#### Example
```
Input:
5 2
a
bb
ccc
d
ee
ccc

Output:
4 6
```
Sorted by length: [a, d, bb, ee, ccc]. Best case: try 3 passwords (a, d, bb or similar until ccc) = 3+5÷2 penalty. Worst case: try more same-length ones first.

#### Solution

##### Approach
Sort passwords by length, find the position range of the correct password, calculate time including 5-second penalties.

##### Python Solution
```python
n, k = map(int, input().split())
passwords = [input() for _ in range(n)]
correct_pwd = input()

correct_len = len(correct_pwd)
passwords.sort(key=len, reverse=True)

# Find range of passwords with same length as correct
same_len_passwords = [p for p in passwords if len(p) == correct_len]
shorter_count = sum(1 for p in passwords if len(p) < correct_len)
num_correct_matches = same_len_passwords.count(correct_pwd)

# Best case: try fewest same-length before correct (just 1)
counter_best = shorter_count + 1
# Worst case: try all same-length duplicates of correct last
counter_worst = shorter_count + len(same_len_passwords) - num_correct_matches + 1

def calc_time(attempts):
    penalties = (attempts - 1) // k
    return attempts + penalties * 5

print(calc_time(counter_best), calc_time(counter_worst))
```

##### Complexity Analysis
- **Time Complexity:** O(n log n) - sorting passwords
- **Space Complexity:** O(n) - storing passwords

---

### Embosser Rotations

#### Problem Information
- **Source:** [Codeforces 731A](https://codeforces.com/problemset/problem/731/A)
- **Difficulty:** Easy

#### Problem Statement
An embosser has a wheel with letters arranged in a circle. Starting at 'a', find the minimum number of rotations (clockwise or counterclockwise) to print a given string.

#### Input Format
A single string (the exhibit name).

#### Output Format
Minimum number of rotations.

#### Example
```
Input:
zeus

Output:
18
```
a→z: min(25, 1)=1. z→e: min(21, 5)=5. e→u: min(16, 10)=10. u→s: min(24, 2)=2. Total: 1+5+10+2=18.

#### Solution

##### Approach
For each character, calculate the minimum of clockwise and counterclockwise distance from current position.

##### Python Solution
```python
name = input()
result = 0
cur_pos = ord('a')

for c in name:
    diff = abs(ord(c) - cur_pos)
    result += min(diff, 26 - diff)
    cur_pos = ord(c)

print(result)
```

##### Complexity Analysis
- **Time Complexity:** O(n) - single pass through string
- **Space Complexity:** O(1) - constant extra space

---

### African Crossword

#### Problem Information
- **Source:** [Codeforces 90B](https://codeforces.com/problemset/problem/90/B)
- **Difficulty:** Medium

#### Problem Statement
In a rectangular grid, cross out all letters that appear more than once in their row or column. The remaining letters form the encrypted word (read left to right, top to bottom).

#### Input Format
- First line: n m (grid dimensions)
- Next n lines: m characters each (the grid)

#### Output Format
The encrypted word.

#### Example
```
Input:
3 3
qwe
asd
zxc

Output:
qweasdzxc
```
All letters are unique in their row and column, so nothing is crossed out.

```
Input:
2 2
aa
aa

Output:

```
All 'a's appear multiple times in rows and columns, all crossed out, empty result.

#### Solution

##### Approach
Mark each cell if its letter repeats in the same row or column. Output unmarked letters in order.

##### Python Solution
```python
from collections import Counter

n, m = map(int, input().split())
grid = [input() for _ in range(n)]

# Count frequencies for each row and column
row_counts = [Counter(row) for row in grid]
col_counts = [Counter(grid[i][j] for i in range(n)) for j in range(m)]

result = []
for i in range(n):
    for j in range(m):
        char = grid[i][j]
        if row_counts[i][char] == 1 and col_counts[j][char] == 1:
            result.append(char)

print(''.join(result))
```

##### Complexity Analysis
- **Time Complexity:** O(n * m * (n + m)) - checking row and column for each cell
- **Space Complexity:** O(n * m) - storing the marking matrix

