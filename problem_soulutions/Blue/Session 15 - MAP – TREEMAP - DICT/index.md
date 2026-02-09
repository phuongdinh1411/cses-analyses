---
layout: simple
title: "MAP - TREEMAP - DICT"
permalink: /problem_soulutions/Blue/Session 15 - MAP – TREEMAP - DICT/
---

# MAP - TREEMAP - DICT

This session covers map-based data structures including hash maps, tree maps, and dictionary operations for efficient key-value storage and retrieval.

## Problems

### Megacity

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

#### Problem Statement

The city of Berland wants to become a megacity (population >= 1,000,000). There are n locations around the city, each at coordinates (x, y) with k people. The city can expand its borders to a circle of radius r centered at origin (0,0). Find the minimum radius r such that the city population reaches 1,000,000.

#### Input Format
- First line: n (number of locations) and s (current city population)
- Next n lines: x, y, k (coordinates and population of each location)

#### Output Format
- Minimum radius r (to 7 decimal places) to reach population 1,000,000
- Print -1 if impossible

#### Example
```
Input:
4 999998
1 1 1
2 2 1
3 3 1
4 4 1

Output:
2.8284271
```
The city needs 2 more people to reach 1,000,000. The closest locations are at (1,1) and (2,2) with distances ~1.41 and ~2.83. After including both, the minimum radius is sqrt(8) = 2.8284271.

#### Solution

##### Approach
Calculate distance from origin to each location. Sort locations by distance. Greedily add locations (closest first) until population >= 1,000,000. Uses dictionary/sorting for efficient location management.

##### Python Solution

```python
import math


def solution():
  n, s = map(int, input().split())
  # Use tuples (distance, population) instead of a class
  locations = []
  for _ in range(n):
    x, y, k = map(int, input().split())
    locations.append((math.hypot(x, y), k))

  locations.sort()

  min_r = 0
  for r, k in locations:
    if s >= 1000000:
      print(round(min_r, 7))
      return
    s += k
    min_r = r

  print(round(min_r, 7) if s >= 1000000 else -1)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n log n) for sorting
- **Space Complexity:** O(n)

---

### Powers of Two

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

Given an array of n integers, count the number of pairs (i, j) where i < j such that a[i] + a[j] is a power of 2.

#### Input Format
- First line: n (number of elements)
- Second line: n space-separated integers a[1], a[2], ..., a[n]

#### Output Format
- Single integer: number of pairs whose sum is a power of 2

#### Example
```
Input:
4
7 1 5 3

Output:
3
```
Valid pairs: (7,1)=8=2^3, (1,7) already counted, (5,3)=8=2^3, (1,3)=4=2^2. The pairs (0,1), (0,3), (2,3) give sums 8, 4, 8 respectively, totaling 3 pairs.

#### Solution

##### Approach
Use a dictionary (hash map) to store frequency of each number seen so far. For each element, check all powers of 2 (up to 2^60) and count pairs. For each power p, if (p - a[i]) exists in dictionary, add its count. Time complexity: O(n * 60) using hash map for O(1) lookups.

##### Python Solution

```python
from collections import defaultdict


def solution():
  n = int(input())
  a = list(map(int, input().split()))

  pow2 = [1 << i for i in range(61)]  # Bit shift is more Pythonic for powers of 2

  total = 0
  count = defaultdict(int)
  for num in a:
    total += sum(count[p - num] for p in pow2)
    count[num] += 1

  print(total)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n * 60) = O(n)
- **Space Complexity:** O(n)

---

### Penguins

#### Problem Information
- **Source:** ACM TIMUS
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 64MB

#### Problem Statement

A group of penguins have names. Find the most frequently occurring name among all the penguins. If there's a tie, return the name that appeared first with the maximum count.

#### Input Format
- First line: n (number of penguins)
- Next n lines: name of each penguin

#### Output Format
- The most common penguin name

#### Example
```
Input:
5
Tux
Happy
Tux
Happy
Tux

Output:
Tux
```
"Tux" appears 3 times, "Happy" appears 2 times. The most frequent name is "Tux".

#### Solution

##### Approach
Use a dictionary to count occurrences of each name. Track the most frequent name while iterating. Simple hash map frequency counting problem.

##### Python Solution

```python
from collections import defaultdict


def solution():
  penguins = defaultdict(int)
  n_penguins = int(input())
  most_count = 0
  most_common = ''

  for _ in range(n_penguins):
    penguin = input().strip()
    penguins[penguin] += 1
    if penguins[penguin] > most_count:
      most_count = penguins[penguin]
      most_common = penguin

  print(most_common)


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n)
- **Space Complexity:** O(n)

---

### Isenbaev's Number

#### Problem Information
- **Source:** ACM TIMUS
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 64MB

#### Problem Statement

In competitive programming, "Isenbaev's Number" represents the shortest chain of teammates connecting a person to Isenbaev (similar to Erdos number). Given a list of 3-person teams, calculate each person's Isenbaev number. Isenbaev himself has number 0, his teammates have number 1, etc.

#### Input Format
- First line: n (number of teams)
- Next n lines: three space-separated names (team members)

#### Output Format
- For each unique name (in alphabetical order), print: "name number" or "name undefined" if not connected to Isenbaev

#### Example
```
Input:
3
Isenbaev Petrov Sidorov
Sidorov Ivanov Kozlov
Kozlov Fedorov Romanov

Output:
Fedorov 3
Isenbaev 0
Ivanov 2
Kozlov 2
Petrov 1
Romanov 3
Sidorov 1
```
Isenbaev has number 0. Petrov and Sidorov are teammates with Isenbaev, so they have number 1. Ivanov and Kozlov teamed with Sidorov, getting number 2. And so on.

#### Solution

##### Approach
Use dictionary to store each person's proximity to Isenbaev. For each team, propagate the minimum proximity value. Sort and output results alphabetically.

##### Python Solution

```python
from collections import defaultdict

INF = int(1e9)


def solution():
  players = defaultdict(lambda: INF)
  players['Isenbaev'] = 0
  n_teams = int(input())

  for _ in range(n_teams):
    team = input().split()
    # Find minimum proximity in this team
    min_proximity = min(players[p] for p in team)

    if min_proximity < INF:
      for player in team:
        if players[player] > min_proximity:
          players[player] = min_proximity + 1

  for name in sorted(players.keys()):
    proximity = str(players[name]) if players[name] != INF else 'undefined'
    print(f"{name} {proximity}")


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n * k + m log m) where k is team size, m is unique players
- **Space Complexity:** O(m)

---

### Test Task

#### Problem Information
- **Source:** ACM TIMUS
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 64MB

#### Problem Statement

Implement a simple user authentication system with three operations:
- register login password: Register a new user
- login login password: Log in an existing user
- logout login: Log out a logged-in user

Each operation outputs success/fail with appropriate message.

#### Input Format
- First line: n (number of operations)
- Next n lines: operation with arguments

#### Output Format
- For each operation, print the result message:
  - register: "success: new user added" or "fail: user already exists"
  - login: "success: user logged in" or appropriate fail message
  - logout: "success: user logged out" or appropriate fail message

#### Example
```
Input:
6
register alice password123
login alice password123
login alice password123
logout alice
logout alice
login bob wrongpass

Output:
success: new user added
success: user logged in
fail: already logged in
success: user logged out
fail: already logged out
fail: no such user
```

#### Solution

##### Approach
Use dictionary to store user credentials and login state. Each user maps to [password, status] where status is 'in' or 'out'.

##### Python Solution

```python
def solution():
  n = int(input())
  users = {}  # {login: [password, logged_in]}

  for _ in range(n):
    parts = input().split()
    op, login = parts[0], parts[1]

    if op == 'register':
      if login in users:
        print('fail: user already exists')
      else:
        users[login] = [parts[2], False]
        print('success: new user added')

    elif op == 'login':
      if login not in users:
        print('fail: no such user')
      elif users[login][0] != parts[2]:
        print('fail: incorrect password')
      elif users[login][1]:
        print('fail: already logged in')
      else:
        users[login][1] = True
        print('success: user logged in')

    elif op == 'logout':
      if login not in users:
        print('fail: no such user')
      elif not users[login][1]:
        print('fail: already logged out')
      else:
        users[login][1] = False
        print('success: user logged out')


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n)
- **Space Complexity:** O(u) where u is number of unique users

---

### Hardwood Species

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

A census of trees in a forest has been conducted. Given a list of tree species, calculate what percentage of the total forest each species represents. Output results in alphabetical order.

#### Input Format
- First line: number of test cases
- For each test case: list of tree names (one per line), separated by blank lines

#### Output Format
- For each test case: each tree species followed by its percentage (4 decimal places)
- Species listed in alphabetical order

#### Example
```
Input:
1

Red Alder
Ash
Ash
Red Alder
Red Alder

Output:
Ash 40.0
Red Alder 60.0
```
Total trees = 5. Ash appears 2 times (40%), Red Alder appears 3 times (60%).

#### Solution

##### Approach
Use dictionary to count occurrences of each tree species. Calculate percentage = (count / total) * 100. Sort keys alphabetically for output.

##### Python Solution

```python
from collections import defaultdict


def solution():
  n = int(input())
  input()

  for _ in range(n):
    population = defaultdict(int)
    total = 0

    while True:
      try:
        line = input()
        if not line:
          break
      except:
        break
      population[line] += 1
      total += 1

    for tree in sorted(population):
      print(f"{tree} {round(population[tree] * 100 / total, 4)}")


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(n log n) for sorting species
- **Space Complexity:** O(n) for dictionary

---

### Bankrupt Baker

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 3000ms
- **Memory Limit:** 256MB

#### Problem Statement

A baker has recipe binders with ingredients and recipes. Given a budget, find which recipes can be made within budget. Output affordable recipes sorted by cost (then alphabetically if tied).

#### Input Format
- Number of binders
- For each binder:
  - Binder name
  - m (ingredients), n (recipes), b (budget)
  - m lines of ingredient name and price
  - n recipes, each with name, number of ingredients, and ingredient quantities

#### Output Format
- For each binder: binder name (uppercase), then affordable recipes sorted by cost then name, or "Too expensive!" if none affordable

#### Example
```
Input:
1
Desserts
3 2 10
flour 2
sugar 3
butter 5
Cake
2
flour 2
sugar 1
Cookies
2
butter 1
sugar 2

Output:
DESSERTS
Cake
Cookies

```
Cake costs 2*2 + 1*3 = 7, Cookies costs 1*5 + 2*3 = 11. With budget 10, only Cake is affordable initially, but let's recalculate: Cookies = 5 + 6 = 11 > 10, so only Cake at cost 7 is shown.

#### Solution

##### Approach
Use dictionary to map ingredient names to prices. Calculate total cost for each recipe. Filter and sort recipes within budget.

##### Python Solution

```python
def solution():
  binders = int(input())
  for _ in range(binders):
    binder_name = input().strip().upper()
    m, n, b = map(int, input().strip().split())

    ingredients = {}
    for _ in range(m):
      name, price = input().split()
      ingredients[name] = int(price)

    print(binder_name)
    affordable = []  # List of (cost, name) tuples for easy sorting

    for _ in range(n):
      recipe_name = input().strip()
      k = int(input())
      total_cost = 0
      for _ in range(k):
        name, quantity = input().split()
        total_cost += int(quantity) * ingredients[name]

      if total_cost <= b:
        affordable.append((total_cost, recipe_name))

    if not affordable:
      print('Too expensive!')
    else:
      affordable.sort()  # Sorts by cost first, then name
      for _, name in affordable:
        print(name)
    print()


solution()
```

##### Complexity Analysis
- **Time Complexity:** O(B * (M + N * K + N log N)) where B is binders, M is ingredients, N is recipes, K is ingredients per recipe
- **Space Complexity:** O(M + N)
