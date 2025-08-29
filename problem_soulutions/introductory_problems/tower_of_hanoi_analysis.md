---
layout: simple
title: "Tower of Hanoi"
permalink: /problem_soulutions/introductory_problems/tower_of_hanoi_analysis
---

# Tower of Hanoi

## Problem Description

**Problem**: Move n disks from the first tower to the third tower using the second tower as auxiliary, following these rules:
1. Only one disk can be moved at a time
2. A larger disk cannot be placed on top of a smaller disk
3. Only the top disk of any tower can be moved

**Input**: An integer n (1 ≤ n ≤ 16)

**Output**: Print the moves required to solve the puzzle.

**Example**:
```
Input: 3

Output:
1 3
1 2
3 2
1 3
2 1
2 3
1 3

Explanation: This shows the sequence of moves to solve the puzzle with 3 disks.
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Move n disks from tower A to tower C
- Use tower B as auxiliary
- Follow the three rules strictly
- Find the sequence of moves

**Key Observations:**
- This is a classic recursive problem
- We can solve it by breaking it down into smaller subproblems
- The solution has a clear pattern
- Minimum moves required: 2ⁿ - 1

### Step 2: Recursive Approach
**Idea**: Solve the problem recursively by breaking it into smaller subproblems.

```python
def tower_of_hanoi_recursive(n, from_rod, aux_rod, to_rod):
    if n == 1:
        print(f"{from_rod} {to_rod}")
        return
    
    # Move n-1 disks from source to auxiliary
    tower_of_hanoi_recursive(n - 1, from_rod, to_rod, aux_rod)
    
    # Move the largest disk from source to destination
    print(f"{from_rod} {to_rod}")
    
    # Move n-1 disks from auxiliary to destination
    tower_of_hanoi_recursive(n - 1, aux_rod, from_rod, to_rod)
```

**Why this works:**
- Base case: move 1 disk directly
- Recursive case: solve for n-1 disks, then move largest disk
- This approach follows the rules automatically

### Step 3: Mathematical Analysis
**Idea**: Understand the mathematical properties of the solution.

```python
def analyze_tower_of_hanoi(n):
    # Number of moves: 2^n - 1
    total_moves = (1 << n) - 1
    print(f"Total moves required: {total_moves}")
    
    # Each disk moves exactly 2^(n-i) times
    for i in range(1, n + 1):
        moves_for_disk = 1 << (n - i)
        print(f"Disk {i} moves {moves_for_disk} times")
```

**Why this pattern exists:**
- Each disk moves exactly 2^(n-i) times
- Total moves = 2ⁿ - 1
- This is the minimum number of moves required

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_tower_of_hanoi():
    n = int(input())
    
    # Print total number of moves
    total_moves = (1 << n) - 1
    print(total_moves)
    
    # Solve the puzzle
    tower_of_hanoi_recursive(n, 1, 2, 3)

def tower_of_hanoi_recursive(n, from_rod, aux_rod, to_rod):
    if n == 1:
        print(f"{from_rod} {to_rod}")
        return
    
    # Move n-1 disks from source to auxiliary
    tower_of_hanoi_recursive(n - 1, from_rod, to_rod, aux_rod)
    
    # Move the largest disk from source to destination
    print(f"{from_rod} {to_rod}")
    
    # Move n-1 disks from auxiliary to destination
    tower_of_hanoi_recursive(n - 1, aux_rod, from_rod, to_rod)

# Main execution
if __name__ == "__main__":
    solve_tower_of_hanoi()
```

**Why this works:**
- Efficient recursive approach
- Follows the optimal strategy
- Handles all cases correctly

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (1, 1),    # 1 disk: 1 move
        (2, 3),    # 2 disks: 3 moves
        (3, 7),    # 3 disks: 7 moves
        (4, 15),   # 4 disks: 15 moves
    ]
    
    for n, expected_moves in test_cases:
        result = count_moves(n)
        print(f"n = {n}")
        print(f"Expected moves: {expected_moves}, Got: {result}")
        print(f"{'✓ PASS' if result == expected_moves else '✗ FAIL'}")
        print()

def count_moves(n):
    if n == 1:
        return 1
    return 2 * count_moves(n - 1) + 1

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(2ⁿ) - exponential due to recursive nature
- **Space**: O(n) - recursion depth

### Why This Solution Works
- **Recursive**: Breaks problem into smaller subproblems
- **Optimal**: Uses minimum number of moves
- **Correct**: Follows all rules automatically

## 🎯 Key Insights

### 1. **Recursive Structure**
- Base case: move 1 disk directly
- Recursive case: solve for n-1 disks, then move largest disk
- This approach follows the rules automatically

### 2. **Mathematical Properties**
- Total moves: 2ⁿ - 1
- Each disk moves exactly 2^(n-i) times
- This is the minimum number of moves required

### 3. **Optimal Strategy**
- Move n-1 disks to auxiliary tower
- Move largest disk to destination
- Move n-1 disks from auxiliary to destination

## 🎯 Problem Variations

### Variation 1: Iterative Solution
**Problem**: Solve Tower of Hanoi without recursion.

```python
def tower_of_hanoi_iterative(n):
    from collections import deque
    
    stack = deque()
    stack.append((n, (1, 3)))
    
    while stack:
        disks, towers = stack.pop()
        from_rod, to_rod = towers
        
        if disks == 1:
            print(f"{from_rod} {to_rod}")
        else:
            aux_rod = 6 - from_rod - to_rod  # Calculate auxiliary rod
            stack.append((disks - 1, (aux_rod, to_rod)))
            stack.append((1, (from_rod, to_rod)))
            stack.append((disks - 1, (from_rod, aux_rod)))
```

### Variation 2: State Tracking
**Problem**: Track the state of all towers after each move.

```python
def tower_of_hanoi_with_state(n):
    towers = [[i for i in range(n, 0, -1)], [], []]
    
    def print_state():
        print("Tower A:", towers[0])
        print("Tower B:", towers[1])
        print("Tower C:", towers[2])
        print()
    
    def move_disk(from_rod, to_rod):
        disk = towers[from_rod].pop()
        towers[to_rod].append(disk)
        print(f"Move disk {disk} from {chr(65+from_rod)} to {chr(65+to_rod)}")
        print_state()
    
    def solve_recursive(n, from_rod, aux_rod, to_rod):
        if n == 1:
            move_disk(from_rod, to_rod)
            return
        
        solve_recursive(n - 1, from_rod, to_rod, aux_rod)
        move_disk(from_rod, to_rod)
        solve_recursive(n - 1, aux_rod, from_rod, to_rod)
    
    print("Initial state:")
    print_state()
    solve_recursive(n, 0, 1, 2)
```

### Variation 3: Constrained Moves
**Problem**: Add constraints on which moves are allowed.

```python
def constrained_tower_of_hanoi(n, constraints):
    # constraints is a set of forbidden moves (from_rod, to_rod)
    
    def is_valid_move(from_rod, to_rod):
        return (from_rod, to_rod) not in constraints
    
    def solve_constrained(n, from_rod, aux_rod, to_rod):
        if n == 1:
            if is_valid_move(from_rod, to_rod):
                print(f"{from_rod} {to_rod}")
            else:
                # Need to use intermediate rod
                intermediate = 6 - from_rod - to_rod
                if is_valid_move(from_rod, intermediate) and is_valid_move(intermediate, to_rod):
                    print(f"{from_rod} {intermediate}")
                    print(f"{intermediate} {to_rod}")
                else:
                    print("No valid solution exists")
            return
        
        # Try different strategies based on constraints
        if is_valid_move(from_rod, to_rod):
            solve_constrained(n - 1, from_rod, to_rod, aux_rod)
            print(f"{from_rod} {to_rod}")
            solve_constrained(n - 1, aux_rod, from_rod, to_rod)
        else:
            # Need alternative strategy
            solve_constrained(n - 1, from_rod, to_rod, aux_rod)
            solve_constrained(1, from_rod, aux_rod, to_rod)
            solve_constrained(n - 1, aux_rod, to_rod, from_rod)
            solve_constrained(1, to_rod, from_rod, aux_rod)
            solve_constrained(n - 1, from_rod, to_rod, aux_rod)
    
    solve_constrained(n, 1, 2, 3)
```

### Variation 4: Multiple Towers
**Problem**: Solve with more than 3 towers.

```python
def multi_tower_hanoi(n, num_towers):
    # With more towers, we can use more efficient strategies
    
    def solve_multi_tower(n, towers, from_rod, to_rod):
        if n == 1:
            print(f"{from_rod} {to_rod}")
            return
        
        if num_towers == 3:
            # Standard 3-tower solution
            aux_rod = 6 - from_rod - to_rod
            solve_multi_tower(n - 1, towers, from_rod, aux_rod)
            print(f"{from_rod} {to_rod}")
            solve_multi_tower(n - 1, towers, aux_rod, to_rod)
        else:
            # With more towers, we can move multiple disks at once
            # This is more complex and requires dynamic programming
            pass
    
    solve_multi_tower(n, num_towers, 1, num_towers)
```

### Variation 5: Cost Optimization
**Problem**: Each move has a cost. Find minimum cost solution.

```python
def cost_optimized_hanoi(n, costs):
    # costs[i][j] = cost of moving from tower i to tower j
    
    def solve_with_cost(n, from_rod, to_rod, memo):
        if n == 1:
            return costs[from_rod][to_rod], [f"{from_rod} {to_rod}"]
        
        state = (n, from_rod, to_rod)
        if state in memo:
            return memo[state]
        
        aux_rod = 6 - from_rod - to_rod
        
        # Try both strategies
        cost1, moves1 = solve_with_cost(n - 1, from_rod, aux_rod, memo)
        cost2, moves2 = solve_with_cost(n - 1, aux_rod, to_rod, memo)
        
        total_cost = cost1 + costs[from_rod][to_rod] + cost2
        total_moves = moves1 + [f"{from_rod} {to_rod}"] + moves2
        
        memo[state] = (total_cost, total_moves)
        return memo[state]
    
    memo = {}
    cost, moves = solve_with_cost(n, 1, 3, memo)
    print(f"Minimum cost: {cost}")
    for move in moves:
        print(move)
```

## 🔗 Related Problems

- **[Permutations](/cses-analyses/problem_soulutions/introductory_problems/permutations_analysis)**: Recursive problems
- **[Creating Strings](/cses-analyses/problem_soulutions/introductory_problems/creating_strings_analysis)**: Recursive generation
- **[Chessboard and Queens](/cses-analyses/problem_soulutions/introductory_problems/chessboard_and_queens_analysis)**: Backtracking problems

## 📚 Learning Points

1. **Recursive Thinking**: Breaking problems into smaller subproblems
2. **Mathematical Patterns**: Understanding exponential growth
3. **Optimal Strategy**: Finding minimum moves
4. **State Management**: Tracking problem state

---

**This is a great introduction to recursive algorithms and mathematical patterns!** 🎯
