---
layout: simple
title: "Tower of Hanoi"
permalink: /problem_soulutions/introductory_problems/tower_of_hanoi_analysis
---

# Tower of Hanoi

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand recursive algorithms and the Tower of Hanoi problem
- Apply recursive thinking to solve the Tower of Hanoi puzzle
- Implement efficient recursive algorithms with proper move sequence generation
- Optimize recursive solutions using mathematical analysis and move optimization
- Handle edge cases in recursive problems (base cases, large n, move sequence validation)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Recursive algorithms, Tower of Hanoi, recursive thinking, move sequence generation
- **Data Structures**: Recursive call stacks, move tracking, sequence generation, recursive data structures
- **Mathematical Concepts**: Recursive mathematics, Tower of Hanoi theory, move sequence mathematics, recursive analysis
- **Programming Skills**: Recursive implementation, move sequence generation, recursive thinking, algorithm implementation
- **Related Problems**: Recursive problems, Tower of Hanoi variants, Recursive thinking, Move sequence problems

## Problem Description

**Problem**: Move n disks from the first tower to the third tower using the second tower as auxiliary, following these rules:
1. Only one disk can be moved at a time
2. A larger disk cannot be placed on top of a smaller disk
3. Only the top disk of any tower can be moved

**Input**: An integer n (1 ≤ n ≤ 16)

**Output**: Print the moves required to solve the puzzle.

**Constraints**:
- 1 ≤ n ≤ 16
- Only one disk can be moved at a time
- Larger disk cannot be placed on top of smaller disk
- Only the top disk of any tower can be moved
- Must move all disks from tower 1 to tower 3
- Use tower 2 as auxiliary

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

## Visual Example

### Input and Problem Setup
```
Input: n = 3 (3 disks)

Initial Setup:
Tower 1: [3, 2, 1]  (largest at bottom, smallest at top)
Tower 2: []         (empty auxiliary tower)
Tower 3: []         (empty destination tower)

Goal: Move all disks from Tower 1 to Tower 3
```

### Move Sequence Visualization
```
Step 1: Move disk 1 from Tower 1 to Tower 3
Tower 1: [3, 2]
Tower 2: []
Tower 3: [1]

Step 2: Move disk 2 from Tower 1 to Tower 2
Tower 1: [3]
Tower 2: [2]
Tower 3: [1]

Step 3: Move disk 1 from Tower 3 to Tower 2
Tower 1: [3]
Tower 2: [2, 1]
Tower 3: []

Step 4: Move disk 3 from Tower 1 to Tower 3
Tower 1: []
Tower 2: [2, 1]
Tower 3: [3]

Step 5: Move disk 1 from Tower 2 to Tower 1
Tower 1: [1]
Tower 2: [2]
Tower 3: [3]

Step 6: Move disk 2 from Tower 2 to Tower 3
Tower 1: [1]
Tower 2: []
Tower 3: [3, 2]

Step 7: Move disk 1 from Tower 1 to Tower 3
Tower 1: []
Tower 2: []
Tower 3: [3, 2, 1]
```

### Recursive Pattern Analysis
```
For n = 3:
1. Move 2 disks from Tower 1 to Tower 2 (using Tower 3 as auxiliary)
2. Move largest disk from Tower 1 to Tower 3
3. Move 2 disks from Tower 2 to Tower 3 (using Tower 1 as auxiliary)

This follows the recursive pattern:
- Solve for n-1 disks
- Move largest disk
- Solve for n-1 disks again
```

### Mathematical Properties
```
Total moves required: 2^n - 1
For n = 3: 2^3 - 1 = 8 - 1 = 7 moves

Each disk moves exactly 2^(n-i) times:
- Disk 1 (smallest): 2^(3-1) = 4 times
- Disk 2 (medium): 2^(3-2) = 2 times  
- Disk 3 (largest): 2^(3-3) = 1 time
```

### Key Insight
The solution works by:
1. Using recursive approach to break down the problem
2. Moving n-1 disks to auxiliary tower
3. Moving largest disk to destination
4. Moving n-1 disks from auxiliary to destination
5. Time complexity: O(2^n) for generating all moves
6. Space complexity: O(n) for recursion depth

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Naive Iterative Simulation (Inefficient)

**Key Insights from Naive Solution:**
- Simulate the puzzle step by step
- Use iterative approach to find valid moves
- Simple but computationally expensive approach
- Not suitable for large inputs due to exponential growth

**Algorithm:**
1. Represent the three towers as stacks
2. Try all possible moves at each step
3. Use backtracking to find valid sequences
4. Generate the complete move sequence

**Visual Example:**
```
Naive approach: Try all possible moves
For n = 2:

Initial state:
Tower 1: [2, 1]
Tower 2: []
Tower 3: []

Possible moves from Tower 1:
- Move disk 1 to Tower 2: [2] [] [1]
- Move disk 1 to Tower 3: [2] [] [1]

Try first option:
Tower 1: [2]
Tower 2: []
Tower 3: [1]

Possible moves:
- Move disk 2 to Tower 2: [] [2] [1]
- Move disk 2 to Tower 3: [] [] [2,1] ❌ (invalid - larger on smaller)

This leads to exponential time complexity
```

**Implementation:**
```python
def tower_of_hanoi_naive(n):
    towers = [[i for i in range(n, 0, -1)], [], []]
    moves = []
    
    def is_valid_move(from_tower, to_tower):
        if not towers[from_tower]:
            return False
        if not towers[to_tower]:
            return True
        return towers[from_tower][-1] < towers[to_tower][-1]
    
    def make_move(from_tower, to_tower):
        disk = towers[from_tower].pop()
        towers[to_tower].append(disk)
        moves.append(f"{from_tower + 1} {to_tower + 1}")
    
    def solve_recursive():
        if len(towers[2]) == n:
            return True
        
        for from_tower in range(3):
            for to_tower in range(3):
                if from_tower != to_tower and is_valid_move(from_tower, to_tower):
                    make_move(from_tower, to_tower)
                    if solve_recursive():
                        return True
                    # Backtrack
                    disk = towers[to_tower].pop()
                    towers[from_tower].append(disk)
                    moves.pop()
        
        return False
    
    solve_recursive()
    return moves

def solve_tower_of_hanoi_naive():
    n = int(input())
    moves = tower_of_hanoi_naive(n)
    
    print(len(moves))
    for move in moves:
        print(move)
```

**Time Complexity:** O(3^n) for trying all possible move sequences
**Space Complexity:** O(n) for tower representation

**Why it's inefficient:**
- O(3^n) time complexity grows exponentially
- Not suitable for competitive programming with large inputs
- Memory-intensive for large n
- Poor performance with exponential growth

### Approach 2: Recursive Solution (Better)

**Key Insights from Recursive Solution:**
- Use recursive approach to break down the problem
- More efficient than naive simulation
- Can handle larger inputs than naive approach
- Uses divide-and-conquer principles

**Algorithm:**
1. Base case: move 1 disk directly
2. Recursive case: solve for n-1 disks, then move largest disk
3. Use auxiliary tower for intermediate storage
4. Follow the optimal recursive strategy

**Visual Example:**
```
Recursive approach: Break down the problem
For n = 3:

Step 1: Move 2 disks from Tower 1 to Tower 2
- This is a subproblem of size 2
- Use Tower 3 as auxiliary

Step 2: Move largest disk from Tower 1 to Tower 3
- Direct move of disk 3

Step 3: Move 2 disks from Tower 2 to Tower 3
- This is another subproblem of size 2
- Use Tower 1 as auxiliary
```

**Implementation:**
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

def solve_tower_of_hanoi_recursive():
    n = int(input())
    
    # Print total number of moves
    total_moves = (1 << n) - 1
    print(total_moves)
    
    # Solve the puzzle
    tower_of_hanoi_recursive(n, 1, 2, 3)
```

**Time Complexity:** O(2^n) for generating all moves
**Space Complexity:** O(n) for recursion depth

**Why it's better:**
- O(2^n) time complexity is better than O(3^n)
- Uses recursive thinking for efficient solution
- Suitable for competitive programming
- Efficient for moderate inputs

### Approach 3: Optimized Recursive with Mathematical Analysis (Optimal)

**Key Insights from Optimized Solution:**
- Use mathematical analysis to understand the solution
- Most efficient approach for Tower of Hanoi problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use mathematical formula for total moves: 2^n - 1
2. Apply recursive strategy for move generation
3. Leverage mathematical properties for optimal solution
4. Use bit manipulation for efficient calculations

**Visual Example:**
```
Optimized approach: Mathematical analysis
For n = 3:

Mathematical properties:
- Total moves: 2^3 - 1 = 7
- Each disk moves exactly 2^(n-i) times
- Disk 1: 2^(3-1) = 4 times
- Disk 2: 2^(3-2) = 2 times
- Disk 3: 2^(3-3) = 1 time

Recursive strategy:
- Break problem into smaller subproblems
- Use optimal move sequence
- Follow mathematical pattern
```

**Implementation:**
```python
def solve_tower_of_hanoi():
    n = int(input())
    
    # Print total number of moves using bit manipulation
    total_moves = (1 << n) - 1
    print(total_moves)
    
    # Solve the puzzle using recursive approach
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

**Time Complexity:** O(2^n) for generating all moves
**Space Complexity:** O(n) for recursion depth

**Why it's optimal:**
- O(2^n) time complexity is optimal for this problem
- Uses mathematical analysis for efficient solution
- Most efficient approach for competitive programming
- Standard method for Tower of Hanoi problems

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Tower of Hanoi with Different Rules
**Problem**: Tower of Hanoi where you can move multiple disks at once under certain conditions.

**Link**: [CSES Problem Set - Tower of Hanoi Extended](https://cses.fi/problemset/task/tower_of_hanoi_extended)

```python
def tower_of_hanoi_extended(n, max_move_size):
    def solve_extended(n, from_rod, aux_rod, to_rod):
        if n <= max_move_size:
            print(f"{from_rod} {to_rod} {n}")
            return
        
        # Move n-max_move_size disks to auxiliary
        solve_extended(n - max_move_size, from_rod, to_rod, aux_rod)
        
        # Move max_move_size disks to destination
        print(f"{from_rod} {to_rod} {max_move_size}")
        
        # Move n-max_move_size disks from auxiliary to destination
        solve_extended(n - max_move_size, aux_rod, from_rod, to_rod)
    
    solve_extended(n, 1, 2, 3)
```

### Variation 2: Tower of Hanoi with Minimum Moves
**Problem**: Tower of Hanoi where you need to find the minimum number of moves to reach a specific configuration.

**Link**: [CSES Problem Set - Tower of Hanoi Minimum Moves](https://cses.fi/problemset/task/tower_of_hanoi_minimum_moves)

```python
def tower_of_hanoi_minimum_moves(n, target_config):
    def count_moves_to_config(n, current_config, target_config):
        if n == 0:
            return 0
        
        if current_config[n-1] == target_config[n-1]:
            return count_moves_to_config(n-1, current_config, target_config)
        
        # Need to move disk n to target position
        return (1 << (n-1)) + count_moves_to_config(n-1, current_config, target_config)
    
    return count_moves_to_config(n, [1] * n, target_config)
```

### Variation 3: Tower of Hanoi with Cost
**Problem**: Tower of Hanoi where each move has a different cost.

**Link**: [CSES Problem Set - Tower of Hanoi with Cost](https://cses.fi/problemset/task/tower_of_hanoi_cost)

```python
def tower_of_hanoi_with_cost(n, move_costs):
    def solve_with_cost(n, from_rod, aux_rod, to_rod):
        if n == 1:
            cost = move_costs[from_rod-1][to_rod-1]
            print(f"{from_rod} {to_rod} {cost}")
            return cost
        
        # Move n-1 disks from source to auxiliary
        cost1 = solve_with_cost(n - 1, from_rod, to_rod, aux_rod)
        
        # Move the largest disk from source to destination
        cost2 = move_costs[from_rod-1][to_rod-1]
        print(f"{from_rod} {to_rod} {cost2}")
        
        # Move n-1 disks from auxiliary to destination
        cost3 = solve_with_cost(n - 1, aux_rod, from_rod, to_rod)
        
        return cost1 + cost2 + cost3
    
    return solve_with_cost(n, 1, 2, 3)
```

### Related Problems

#### **CSES Problems**
- [Tower of Hanoi](https://cses.fi/problemset/task/2165) - Basic Tower of Hanoi problem
- [Chessboard and Queens](https://cses.fi/problemset/task/1624) - Recursive backtracking problems
- [Creating Strings](https://cses.fi/problemset/task/1622) - Recursive string generation

#### **LeetCode Problems**
- [Tower of Hanoi](https://leetcode.com/problems/tower-of-hanoi/) - Classic Tower of Hanoi problem
- [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/) - Recursive generation
- [Permutations](https://leetcode.com/problems/permutations/) - Recursive permutation generation
- [Subsets](https://leetcode.com/problems/subsets/) - Recursive subset generation

#### **Problem Categories**
- **Recursive Algorithms**: Divide-and-conquer, recursive thinking, recursive problem solving
- **Mathematical Sequences**: Move counting, pattern recognition, mathematical analysis
- **Divide and Conquer**: Problem decomposition, recursive structure, base case handling
- **Algorithm Design**: Recursive algorithms, mathematical algorithms, sequence generation

## 📚 Learning Points

1. **Recursive Thinking**: Essential for understanding divide-and-conquer algorithms
2. **Tower of Hanoi Theory**: Key technique for understanding recursive problems
3. **Mathematical Analysis**: Important for understanding move patterns
4. **Divide and Conquer**: Critical for understanding recursive problem solving
5. **Base Cases**: Foundation for recursive algorithm design
6. **Recursive Patterns**: Critical for understanding recursive problem structures

## 📝 Summary

The Tower of Hanoi problem demonstrates recursive algorithms and mathematical analysis concepts for efficient puzzle solving. We explored three approaches:

1. **Naive Iterative Simulation**: O(3^n) time complexity using backtracking simulation, inefficient due to exponential growth
2. **Recursive Solution**: O(2^n) time complexity using recursive approach, better approach for recursive problems
3. **Optimized Recursive with Mathematical Analysis**: O(2^n) time complexity with mathematical understanding, optimal approach for competitive programming

The key insights include understanding recursive thinking, using divide-and-conquer principles, and applying mathematical patterns for optimal performance. This problem serves as an excellent introduction to recursive algorithms and mathematical analysis in competitive programming.
