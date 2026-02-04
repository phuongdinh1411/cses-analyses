---
layout: simple
title: "Session 15 - MAP – TREEMAP - DICT"
permalink: /problem_soulutions/Blue/Session 15 - MAP – TREEMAP - DICT/
---

# Session 15 - MAP – TREEMAP - DICT

This session covers map-based data structures including hash maps, tree maps, and dictionary operations for efficient key-value storage and retrieval.

## Problems

### 424B (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/424/B
#
# Problem: Megacity
#
# Description:
# The city of Berland wants to become a megacity (population >= 1,000,000).
# There are n locations around the city, each at coordinates (x, y) with k people.
# The city can expand its borders to a circle of radius r centered at origin (0,0).
# Find the minimum radius r such that the city population reaches 1,000,000.
#
# Input:
# - First line: n (number of locations) and s (current city population)
# - Next n lines: x, y, k (coordinates and population of each location)
#
# Output:
# - Minimum radius r (to 7 decimal places) to reach population 1,000,000
# - Print -1 if impossible
#
# Approach:
# - Calculate distance from origin to each location
# - Sort locations by distance
# - Greedily add locations (closest first) until population >= 1,000,000
# - Uses dictionary/sorting for efficient location management


import math


class Location:
    def __init__(self, r, k):
        self.r = r
        self.k = k

    def __lt__(self, other):
        return self.r < other.r


def solution():
    n, s = map(int, input().split())
    locations = []
    for i in range(n):
        x, y, k = map(int, input().split())
        locations.append(Location(math.sqrt(x*x + y*y), k))

    locations.sort()

    min_r = 0
    for i in range(n):
        if s >= 1000000:
            print(round(min_r, 7))
            return
        s += locations[i].k
        min_r = locations[i].r

    if s >= 1000000:
        print(round(min_r, 7))
    else:
        print(-1)


solution()
```

### 702B (Codeforces)

```python
# Problem from Codeforces
# http://codeforces.com/problemset/problem/702/B
#
# Problem: Powers of Two
#
# Description:
# Given an array of n integers, count the number of pairs (i, j) where i < j
# such that a[i] + a[j] is a power of 2.
#
# Input:
# - First line: n (number of elements)
# - Second line: n space-separated integers a[1], a[2], ..., a[n]
#
# Output:
# - Single integer: number of pairs whose sum is a power of 2
#
# Approach:
# - Use a dictionary (hash map) to store frequency of each number seen so far
# - For each element, check all powers of 2 (up to 2^60) and count pairs
# - For each power p, if (p - a[i]) exists in dictionary, add its count
# - Time complexity: O(n * 60) using hash map for O(1) lookups


def solution():
    n = int(input())
    a = list(map(int, input().split()))

    pow2 = [2 ** i for i in range(61)]

    total = 0
    dic = {}
    for i in range(n):
        for j in range(60):
            if pow2[j] - a[i] in dic:
                total += dic[pow2[j] - a[i]]

        if a[i] in dic:
            dic[a[i]] += 1
        else:
            dic[a[i]] = 1

    print(total)


solution()
```

### 1585 (Timus)

```python
# Problem from ACM TIMUS
# http://acm.timus.ru/problem.aspx?space=1&num=1585
#
# Problem: Penguins
#
# Description:
# A group of penguins have names. Find the most frequently occurring name
# among all the penguins. If there's a tie, return the name that appeared
# first with the maximum count.
#
# Input:
# - First line: n (number of penguins)
# - Next n lines: name of each penguin
#
# Output:
# - The most common penguin name
#
# Approach:
# - Use a dictionary to count occurrences of each name
# - Track the most frequent name while iterating
# - Simple hash map frequency counting problem


def solution():
    penguins = {}
    n_penguins = int(input())
    most_numerous_number = 0
    most_numerous_penguin = ''
    for i in range(n_penguins):
        penguin = input().strip()
        if penguins.get(penguin) is None:
            penguins[penguin] = 1
        else:
            penguins[penguin] += 1
        if penguins[penguin] > most_numerous_number:
            most_numerous_number = penguins[penguin]
            most_numerous_penguin = penguin

    print(most_numerous_penguin)


solution()
```

### 1837 (Timus)

```python
# Problem from ACM TIMUS
# http://acm.timus.ru/problem.aspx?space=1&num=1837
#
# Problem: Isenbaev's Number
#
# Description:
# In competitive programming, "Isenbaev's Number" represents the shortest
# chain of teammates connecting a person to Isenbaev (similar to Erdos number).
# Given a list of 3-person teams, calculate each person's Isenbaev number.
# Isenbaev himself has number 0, his teammates have number 1, etc.
#
# Input:
# - First line: n (number of teams)
# - Next n lines: three space-separated names (team members)
#
# Output:
# - For each unique name (in alphabetical order), print:
#   "name number" or "name undefined" if not connected to Isenbaev
#
# Approach:
# - Use dictionary to store each person's proximity to Isenbaev
# - For each team, propagate the minimum proximity value
# - Sort and output results alphabetically


INF = int(1e9)


def solution():
    players = {'Isenbaev': 0}
    n_teams = int(input())
    for i in range(n_teams):
        players_line = input().split()
        if players.get(players_line[0]) is None:
            players[players_line[0]] = INF
        min_proximity = players[players_line[0]]
        min_index = 0
        for j in range(1, len(players_line)):
            if players.get(players_line[j]) is None:
                players[players_line[j]] = INF
            if min_proximity > players[players_line[j]]:
                min_proximity = players[players_line[j]]
                min_index = j
        if min_proximity < INF:
            for j in range(len(players_line)):
                if j is not min_index and players[players_line[j]] > min_proximity:
                    players[players_line[j]] = min_proximity + 1

    for key in sorted(players.keys()):
        proximity = str(players[key]) if players[key] is not INF else 'undefined'
        print(key + ' ' + proximity)


solution()
```

### 2002 (Timus)

```python
# Problem from ACM TIMUS
# http://acm.timus.ru/problem.aspx?space=1&num=2002
#
# Problem: Test Task
#
# Description:
# Implement a simple user authentication system with three operations:
# - register <login> <password>: Register a new user
# - login <login> <password>: Log in an existing user
# - logout <login>: Log out a logged-in user
# Each operation outputs success/fail with appropriate message.
#
# Input:
# - First line: n (number of operations)
# - Next n lines: operation with arguments
#
# Output:
# - For each operation, print the result message:
#   - register: "success: new user added" or "fail: user already exists"
#   - login: "success: user logged in" or appropriate fail message
#   - logout: "success: user logged out" or appropriate fail message
#
# Approach:
# - Use dictionary to store user credentials and login state
# - Each user maps to [password, status] where status is 'in' or 'out'


def solution():
    n = int(input())
    users = {}
    for i in range(n):
        operation_line = list(map(str, input().split()))
        if operation_line[0] == 'register':
            if users.get(operation_line[1]) is not None:
                print('fail: user already exists')
            else:
                users[operation_line[1]] = [operation_line[2], 'out']
                print('success: new user added')

        if operation_line[0] == 'login':
            user_identity = users.get(operation_line[1])
            if user_identity is None:
                print('fail: no such user')
            else:
                if user_identity[0] == operation_line[2]:
                    if user_identity[1] == 'out':
                        users.get(operation_line[1])[1] = 'in'
                        print('success: user logged in')
                    else:
                        print('fail: already logged in')
                else:
                    print('fail: incorrect password')
        if operation_line[0] == 'logout':
            user_identity = users.get(operation_line[1])
            if user_identity is None:
                print('fail: no such user')
            elif user_identity[1] == 'out':
                print('fail: already logged out')
            else:
                user_identity[1] = 'out'
                print('success: user logged out')


solution()
```

### 10226 (UVA)

```python
# Problem from UVA
# https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1167
#
# Problem: Hardwood Species (UVA 10226)
#
# Description:
# A census of trees in a forest has been conducted. Given a list of tree species,
# calculate what percentage of the total forest each species represents.
# Output results in alphabetical order.
#
# Input:
# - First line: number of test cases
# - For each test case: list of tree names (one per line), separated by blank lines
#
# Output:
# - For each test case: each tree species followed by its percentage (4 decimal places)
# - Species listed in alphabetical order
#
# Approach:
# - Use dictionary to count occurrences of each tree species
# - Calculate percentage = (count / total) * 100
# - Sort keys alphabetically for output

# import sys


# sys.stdin = open("file.txt", "r")


def solution():
    n = int(input())
    input()

    for i in range(n):
        population = {}
        total = 0
        while True:
            try:
                new_line = input()
                if not new_line:
                    break
            except:
                break
            if population.get(new_line) is None:
                population[new_line] = 1
            else:
                population[new_line] += 1

            total += 1
        sorted_list = sorted(population.keys())

        for tree in sorted_list:
            print(tree + ' ' + str(round(population.get(tree) * 100 / total, 4)))


solution()
```

### 11308 (UVA)

```python
# Problem from UVA
# https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=2283
#
# Problem: Bankrupt Baker (UVA 11308)
#
# Description:
# A baker has recipe binders with ingredients and recipes. Given a budget,
# find which recipes can be made within budget. Output affordable recipes
# sorted by cost (then alphabetically if tied).
#
# Input:
# - Number of binders
# - For each binder:
#   - Binder name
#   - m (ingredients), n (recipes), b (budget)
#   - m lines of ingredient name and price
#   - n recipes, each with name, number of ingredients, and ingredient quantities
#
# Output:
# - For each binder: binder name (uppercase), then affordable recipes
#   sorted by cost then name, or "Too expensive!" if none affordable
#
# Approach:
# - Use dictionary to map ingredient names to prices
# - Calculate total cost for each recipe
# - Filter and sort recipes within budget

# import sys


# sys.stdin = open("file.txt", "r")
class Recipe:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

    def __lt__(self, other):
        if self.cost < other.cost:
            return True
        elif self.cost == other.cost:
            return self.name < other.name
        return False


def solution():
    binders = int(input())
    for i in range(binders):
        binder_name = input().strip().upper()
        m, n, b = map(int, input().strip().split())
        ingredients = {}
        for j in range(m):
            ingredient_name, ingredient_price = map(str, input().split())
            ingredients[ingredient_name] = int(ingredient_price)
        print(binder_name)
        can_makes = []
        for j in range(n):
            recipe_name = input().strip()
            k = int(input())
            total_cost = 0
            for x in range(k):
                ingredient_name, quantity = map(str, input().split())
                quantity = int(quantity)
                total_cost += quantity * ingredients[ingredient_name]

            if total_cost <= b:
                can_makes.append(Recipe(recipe_name, total_cost))

        if len(can_makes) == 0:
            print('Too expensive!')
        else:
            can_makes.sort()
            n_can_makes = len(can_makes)
            for cm in range(n_can_makes):
                print(can_makes[cm].name)
        print()


solution()
```

