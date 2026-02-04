---
layout: simple
title: "Greedy"
permalink: /problem_soulutions/Orange/Greedy/
---
# Greedy

Problems solved using greedy algorithms that make locally optimal choices at each step with the goal of finding a global optimum.

## Problems

### Building Permutation

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Permutation p is an ordered set of integers p1, p2, ..., pn, consisting of n distinct positive integers, each of them doesn't exceed n. We'll denote the i-th element of permutation p as pi. We'll call number n the size or the length of permutation p1, p2, ..., pn.

You have a sequence of integers a1, a2, ..., an. In one move, you are allowed to decrease or increase any number by one. Count the minimum number of moves needed to build a permutation from this sequence.

#### Input Format
- The first line contains integer n (1 ≤ n ≤ 3 × 10^5) - the size of the sought permutation.
- The second line contains n integers a1, a2, ..., an (-10^9 ≤ ai ≤ 10^9).

#### Output Format
Print a single number - the minimum number of moves.

#### Sample

**Input:**
```
2
3 0
```

**Output:**
```
2
```

**Input:**
```
3
-1 -1 2
```

**Output:**
```
6
```

#### Solution

##### Approach
The key insight is that to minimize the total number of moves, we should sort the array and then match each element to the corresponding position in the permutation [1, 2, 3, ..., n]. After sorting, the i-th smallest element should become i.

##### Python Solution

```python
def solve():
    n = int(input())
    a = list(map(int, input().split()))

    # Sort the array
    a.sort()

    # Calculate minimum moves by matching sorted array to [1, 2, ..., n]
    total_moves = 0
    for i in range(n):
        total_moves += abs(a[i] - (i + 1))

    print(total_moves)

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n log n) due to sorting
- **Space Complexity:** O(n) for storing the array

---

### Making Jumps

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

A knight is a piece used in the game of chess. The chessboard itself is a square array of cells. Each time a knight moves, its resulting position is two rows and one column, or two columns and one row away from its starting position. Thus a knight starting on row r, column c - which we'll denote as (r, c) - can move to any of the squares (r-2, c-1), (r-2, c+1), (r-1, c-2), (r-1, c+2), (r+1, c-2), (r+1, c+2), (r+2, c-1), or (r+2, c+1). Of course, the knight may not move to any square that is not on the board.

Suppose the chessboard is not square, but instead has rows with variable numbers of columns, and with each row offset zero or more columns to the right of the row above it. How many of the squares in such a modified chessboard can a knight, starting in the upper left square (marked with an asterisk), not reach in any number of moves without resting in any square more than once?

If necessary, the knight is permitted to pass over regions that are outside the borders of the modified chessboard, but as usual, it can only move to squares that are within the borders of the board.

#### Input Format
- Each test case starts with the number of rows n (1 ≤ n ≤ 10).
- For each row, there are two integers: the offset (number of cells to skip) and the number of cells in that row.
- Input is terminated when n = 0.

#### Output Format
For each test case, print "Case X, Y squares can not be reached." where X is the case number and Y is the number of unreachable squares.

#### Solution

##### Approach
This is a backtracking/DFS problem. We need to:
1. Build the board representation with offsets
2. Use DFS/backtracking to explore all possible paths from the starting position
3. Track visited squares and count maximum reachable squares
4. The answer is total squares minus maximum reachable squares

##### Python Solution

```python
def solve():
    # Knight move offsets
    moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
             (1, -2), (1, 2), (2, -1), (2, 1)]

    case_num = 0

    while True:
        n = int(input())
        if n == 0:
            break

        case_num += 1

        # Read board configuration
        rows = []
        total_squares = 0

        for i in range(n):
            offset, count = map(int, input().split())
            rows.append((offset, count))
            total_squares += count

        # Create board: board[r] contains set of valid columns for row r
        board = []
        for offset, count in rows:
            board.append(set(range(offset, offset + count)))

        # Find starting position (first cell in first row)
        start_r, start_c = 0, rows[0][0]

        # DFS with backtracking to find maximum reachable
        max_reached = [0]

        def is_valid(r, c):
            return 0 <= r < n and c in board[r]

        def dfs(r, c, visited):
            max_reached[0] = max(max_reached[0], len(visited))

            for dr, dc in moves:
                nr, nc = r + dr, c + dc
                if is_valid(nr, nc) and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    dfs(nr, nc, visited)
                    visited.remove((nr, nc))

        visited = {(start_r, start_c)}
        dfs(start_r, start_c, visited)

        unreachable = total_squares - max_reached[0]
        print(f"Case {case_num}, {unreachable} squares can not be reached.")

if __name__ == "__main__":
    solve()
```

##### Optimized

```python
def solve():
    moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
             (1, -2), (1, 2), (2, -1), (2, 1)]

    case_num = 0

    while True:
        n = int(input())
        if n == 0:
            break

        case_num += 1

        # Read board
        rows = []
        total_squares = 0
        max_col = 0

        for i in range(n):
            offset, count = map(int, input().split())
            rows.append((offset, count))
            total_squares += count
            max_col = max(max_col, offset + count)

        # Create 2D grid for faster lookup
        # grid[r][c] = True if cell exists
        grid = [[False] * max_col for _ in range(n)]
        for r, (offset, count) in enumerate(rows):
            for c in range(offset, offset + count):
                grid[r][c] = True

        start_r, start_c = 0, rows[0][0]
        max_reached = [0]

        def is_valid(r, c):
            return 0 <= r < n and 0 <= c < max_col and grid[r][c]

        def dfs(r, c, count, visited):
            max_reached[0] = max(max_reached[0], count)

            # Early termination if we've reached all squares
            if count == total_squares:
                return

            for dr, dc in moves:
                nr, nc = r + dr, c + dc
                if is_valid(nr, nc) and not visited[nr][nc]:
                    visited[nr][nc] = True
                    dfs(nr, nc, count + 1, visited)
                    visited[nr][nc] = False

        visited = [[False] * max_col for _ in range(n)]
        visited[start_r][start_c] = True
        dfs(start_r, start_c, 1, visited)

        unreachable = total_squares - max_reached[0]
        print(f"Case {case_num}, {unreachable} squares can not be reached.")

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(8^S) in worst case where S is total squares, but pruning significantly reduces this
- **Space Complexity:** O(S) for visited array and recursion stack

##### Key Insight
This is a Hamiltonian path variant - we want to find the longest path visiting each square at most once. Backtracking explores all possible paths, and we keep track of the maximum number of squares reached. The answer is the total squares minus this maximum.

---

### Petya and Catacombs

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 256MB

#### Problem Statement

Petya explores Paris catacombs. Every minute he moves through a passage to another room. When entering a room at minute i, he notes:
- If visited before: the minute he was last in this room
- Otherwise: any non-negative integer strictly less than i

Initially at minute 0, Petya was in a room (no note for t₀). Find the minimum possible number of rooms.

#### Input Format
- First line: n (1 ≤ n ≤ 2×10⁵) - number of notes
- Second line: n integers t₁, t₂, ..., tₙ (0 ≤ tᵢ < i)

#### Output Format
Print the minimum possible number of rooms in Paris catacombs.

#### Solution

##### Approach
Track which "last visit times" are available. When Petya enters a room:
- If tᵢ was a previous minute where a room was last visited, he's revisiting that room
- Otherwise, he's entering a new room

Use a set to track available "last visit" times. Initially, time 0 is available (starting room).

##### Python Solution

```python
def solve():
    n = int(input())
    times = list(map(int, input().split()))

    available = {0}  # Times when rooms were last visited
    rooms = 1  # Start with 1 room (the initial room)

    for i, t in enumerate(times, 1):
        if t in available:
            # Revisiting a room - remove old time, add current time
            available.remove(t)
            available.add(i)
        else:
            # New room
            rooms += 1
            available.add(i)

    print(rooms)

if __name__ == "__main__":
    solve()
```

##### Alternative

```python
def solve():
    n = int(input())
    notes = list(map(int, input().split()))

    # Track which timestamps are "used" (a room was last visited at that time)
    used = [False] * (n + 1)
    used[0] = True  # Initial room at time 0
    rooms = 1

    for i in range(n):
        t = notes[i]
        current_time = i + 1

        if used[t]:
            # Revisiting room that was last visited at time t
            used[t] = False
            used[current_time] = True
        else:
            # Must be a new room
            rooms += 1
            used[current_time] = True

    print(rooms)

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(N)
- **Space Complexity:** O(N)

##### Key Insight
Each room has a "last visited time". When we see note tᵢ, if time t was previously a room's last-visit-time, we can revisit that room (updating its last-visit to current time i). Otherwise, we must create a new room. Greedy assignment minimizes rooms.

---

### Roma and Changing Signs

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

#### Problem Statement

Roma works in a company that sells TVs. Now he has to prepare a report for the last year.

Roma has got a list of the company's incomes. The list is a sequence that consists of n integers. The total income of the company is the sum of all integers in sequence. Roma decided to perform exactly k changes of signs of several numbers in the sequence. He can also change the sign of a number one, two or more times.

The operation of changing a number's sign is the operation of multiplying this number by -1.

Help Roma perform the changes so as to make the total income of the company (the sum of numbers in the resulting sequence) maximum. Note that Roma should perform exactly k changes.

#### Input Format
- The first line contains two integers n and k (1 ≤ n, k ≤ 10^5), showing how many numbers are in the sequence and how many swaps are to be made.
- The second line contains a non-decreasing sequence, consisting of n integers ai (|ai| ≤ 10^4). The numbers in the lines are separated by single spaces. Please note that the given sequence is sorted in non-decreasing order.

#### Output Format
In the single line print the answer to the problem - the maximum total income that we can obtain after exactly k changes.

#### Solution

##### Approach
1. First, flip all negative numbers to positive (starting from the most negative) as long as we have operations left.
2. After flipping all negatives, if we still have operations left:
   - If remaining operations is even, we can flip any number twice (no net change)
   - If remaining operations is odd, flip the smallest absolute value number once

##### Python Solution

```python
def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    # Flip negative numbers starting from smallest (most negative)
    for i in range(n):
        if a[i] < 0 and k > 0:
            a[i] = -a[i]
            k -= 1

    # Sort again to find the minimum element
    a.sort()

    # If k is odd, flip the smallest element
    if k % 2 == 1:
        a[0] = -a[0]

    print(sum(a))

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n log n) due to sorting
- **Space Complexity:** O(n) for storing the array

---

### The Number On The Board

#### Problem Information
- **Source:** Codeforces
- **Difficulty:** Secret
- **Time Limit:** 2000ms
- **Memory Limit:** 256MB

#### Problem Statement

Some natural number was written on the board. Its sum of digits was not less than k. But you were distracted a bit, and someone changed this number to n, replacing some digits with others. It's known that the length of the number didn't change.

You have to find the minimum number of digits in which these two numbers can differ.

#### Input Format
- The first line contains integer k (1 ≤ k ≤ 10^9).
- The second line contains integer n (1 ≤ n < 10^100000).
- There are no leading zeros in n. It's guaranteed that this situation is possible.

#### Output Format
Print the minimum number of digits in which the initial number and n can differ.

#### Sample

**Input:**
```
3
11
```
**Output:**
```
1
```

**Input:**
```
3
99
```
**Output:**
```
0
```

#### Solution

##### Approach
To minimize the number of changed digits while making the digit sum at least k:
1. Calculate current digit sum
2. If sum ≥ k, answer is 0
3. Otherwise, greedily change the smallest digits to 9 (maximizing gain per change)
4. Sort digits and change from smallest to largest until sum ≥ k

##### Python Solution

```python
def solve():
    k = int(input())
    n = input().strip()

    # Get all digits
    digits = [int(c) for c in n]
    current_sum = sum(digits)

    # If already >= k, no changes needed
    if current_sum >= k:
        print(0)
        return

    # Sort digits to change smallest ones first (maximize gain)
    digits.sort()

    changes = 0
    i = 0

    while current_sum < k:
        # Change digit to 9
        gain = 9 - digits[i]
        if gain > 0:
            changes += 1
            current_sum += gain
        i += 1

    print(changes)

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n log n) where n is the number of digits, due to sorting
- **Space Complexity:** O(n) for storing digits

---

### Through the Desert 

#### Problem Information
- **Source:** UVA
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

Cross a desert with a jeep. The fuel tank must be large enough to complete the journey. Events along the way:
- **Fuel consumption n**: Truck uses n litres per 100 km
- **Leak**: Adds 1 litre/km leak rate (cumulative)
- **Gas station**: Fill up tank completely
- **Mechanic**: Fixes all leaks (leak rate becomes 0)
- **Goal**: Journey's end

Find the minimum tank size (in litres) to complete the journey.

#### Input Format
- Multiple test cases (up to 50 events each)
- Events given by: distance (km from start) and event type
- First event: "0 Fuel consumption n"
- Last event: "d Goal"
- Events sorted by distance
- Input ends with "0 Fuel consumption 0"

#### Output Format
For each test case, print minimum tank volume with 3 decimal places.

#### Solution

##### Approach
Simulate the journey backwards or use binary search on tank size.

Key insight: The minimum tank size is determined by the segment that requires the most fuel between refills (gas stations or start).

For each segment between gas stations:
- Track fuel consumption rate and leak rate
- Calculate fuel needed for each sub-segment
- The tank must hold enough for the worst segment

##### Python Solution

```python
def solve():
    while True:
        events = []

        while True:
            line = input().split()
            dist = int(line[0])
            event_type = line[1]

            if event_type == "Fuel":
                consumption = int(line[3])
                events.append((dist, "fuel", consumption))

                if dist == 0 and consumption == 0:
                    return

            elif event_type == "Leak":
                events.append((dist, "leak", 0))
            elif event_type == "Gas":
                events.append((dist, "gas", 0))
            elif event_type == "Mechanic":
                events.append((dist, "mechanic", 0))
            elif event_type == "Goal":
                events.append((dist, "goal", 0))
                break

        # Simulate to find minimum tank size
        # Binary search on tank capacity

        def can_complete(tank_capacity):
            fuel = tank_capacity
            consumption = 0  # litres per 100 km
            leak_rate = 0    # litres per km
            prev_dist = 0

            for dist, event, val in events:
                delta = dist - prev_dist

                if delta > 0:
                    # Fuel used = (consumption/100) * delta + leak_rate * delta
                    fuel_used = (consumption / 100) * delta + leak_rate * delta
                    fuel -= fuel_used

                    if fuel < -1e-9:
                        return False

                if event == "fuel":
                    consumption = val
                elif event == "leak":
                    leak_rate += 1
                elif event == "gas":
                    fuel = tank_capacity
                elif event == "mechanic":
                    leak_rate = 0
                elif event == "goal":
                    pass

                prev_dist = dist

            return fuel >= -1e-9

        # Binary search for minimum tank capacity
        lo, hi = 0.0, 1e9

        for _ in range(100):  # Enough iterations for precision
            mid = (lo + hi) / 2
            if can_complete(mid):
                hi = mid
            else:
                lo = mid

        print(f"{hi:.3f}")

if __name__ == "__main__":
    solve()
```

##### Alternative

```python
def solve():
    while True:
        events = []

        while True:
            parts = input().split()
            dist = int(parts[0])
            event = parts[1]

            if event == "Fuel":
                rate = int(parts[3])
                if dist == 0 and rate == 0:
                    return
                events.append((dist, "fuel", rate))
            elif event == "Leak":
                events.append((dist, "leak", 0))
            elif event == "Gas":
                events.append((dist, "gas", 0))
            elif event == "Mechanic":
                events.append((dist, "mech", 0))
            elif event == "Goal":
                events.append((dist, "goal", 0))
                break

        # Find min tank by checking each segment between gas stations
        # Tank must be large enough for worst segment

        def simulate(capacity):
            tank = capacity
            cons = 0
            leak = 0
            pos = 0

            for d, e, v in events:
                dist = d - pos

                if dist > 0:
                    usage = cons * dist / 100 + leak * dist
                    tank -= usage
                    if tank < -1e-9:
                        return False

                if e == "fuel":
                    cons = v
                elif e == "leak":
                    leak += 1
                elif e == "gas":
                    tank = capacity
                elif e == "mech":
                    leak = 0

                pos = d

            return True

        lo, hi = 0, 2e7
        for _ in range(100):
            mid = (lo + hi) / 2
            if simulate(mid):
                hi = mid
            else:
                lo = mid

        print(f"{hi:.3f}")

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(E × log(MAX_CAPACITY)) where E is number of events
- **Space Complexity:** O(E)

##### Key Insight
Binary search on tank capacity. For each candidate capacity, simulate the journey: track fuel level, consumption rate, and leak rate. The tank is filled at gas stations and at the start. Leaks accumulate (each "Leak" event adds 1 L/km). Mechanic resets leak rate to 0. The minimum capacity is the smallest value that allows completing the journey without running out.

---

### Wine trading in Gergovia

#### Problem Information
- **Source:** SPOJ
- **Difficulty:** Secret
- **Time Limit:** 1000ms
- **Memory Limit:** 512MB

#### Problem Statement

Gergovia consists of one street, and every inhabitant of the city is a wine salesman. Everyone buys wine from other inhabitants of the city. Every day each inhabitant decides how much wine he wants to buy or sell. Interestingly, demand and supply is always the same, so that each inhabitant gets what he wants.

There is one problem, however: Transporting wine from one house to another results in work. Since all wines are equally good, the inhabitants of Gergovia don't care which persons they are doing trade with, they are only interested in selling or buying a specific amount of wine.

In this problem you are asked to reconstruct the trading during one day in Gergovia. For simplicity we will assume that the houses are built along a straight line with equal distance between adjacent houses. Transporting one bottle of wine from one house to an adjacent house results in one unit of work.

#### Input Format
- The input consists of several test cases.
- Each test case starts with the number of inhabitants N (2 ≤ N ≤ 100000).
- The following line contains n integers ai (-1000 ≤ ai ≤ 1000).
- If ai ≥ 0, it means that the inhabitant living in the i-th house wants to buy ai bottles of wine.
- If ai < 0, he wants to sell -ai bottles of wine.
- You may assume that the numbers ai sum up to 0.
- The last test case is followed by a line containing 0.

#### Output Format
For each test case print the minimum amount of work units needed so that every inhabitant has his demand fulfilled.

#### Solution

##### Approach
The key insight is to think about the flow of wine between adjacent houses. At each position, we track the cumulative "debt" - how much wine needs to flow past that point. The total work is the sum of absolute values of this running balance.

##### Python Solution

```python
def solve():
    while True:
        n = int(input())
        if n == 0:
            break

        a = list(map(int, input().split()))

        # Calculate total work using prefix sum approach
        total_work = 0
        carry = 0  # Wine that needs to be transported to the right

        for i in range(n):
            carry += a[i]
            total_work += abs(carry)

        print(total_work)

if __name__ == "__main__":
    solve()
```

##### Complexity Analysis
- **Time Complexity:** O(n) per test case
- **Space Complexity:** O(n) for storing the array

### Explanation
Think of it as: between each pair of adjacent houses, some wine needs to flow. If house i has demand `a[i]`, the wine flowing between house i and i+1 is the cumulative sum up to i. The work done is |cumulative_sum| for each edge.

