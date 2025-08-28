---
layout: simple
title: "Tower of Hanoi Analysis"
permalink: /problem_soulutions/introductory_problems/tower_of_hanoi_analysis
---


# Tower of Hanoi Analysis

## Problem Description

Move n disks from the first tower to the third tower using the second tower as auxiliary, following these rules:
1. Only one disk can be moved at a time
2. A larger disk cannot be placed on top of a smaller disk
3. Only the top disk of any tower can be moved

## Key Insights

### 1. Recursive Solution
- **Base case**: Move 1 disk directly from source to destination
- **Recursive case**: 
  1. Move n-1 disks from source to auxiliary
  2. Move the largest disk from source to destination
  3. Move n-1 disks from auxiliary to destination

### 2. Mathematical Properties
- **Minimum moves**: 2^n - 1
- **Pattern**: Each disk moves exactly 2^(n-i) times where i is disk number
- **Optimality**: This is the minimum number of moves required

### 3. State Representation
- Can be represented as array of stacks
- Each move is a tuple (from, to)
- State can be encoded as a single number

## Solution Approach

### Method 1: Recursive Solution
```python
def tower_of_hanoi(n, from_rod, aux_rod, to_rod):
    if n == 1:
        print(f"{from_rod} {to_rod}")
        return
    
    tower_of_hanoi(n - 1, from_rod, to_rod, aux_rod)
    print(f"{from_rod} {to_rod}")
    tower_of_hanoi(n - 1, aux_rod, from_rod, to_rod)

# Count moves
def count_moves(n):
    if n == 1:
        return 1
    return 2 * count_moves(n - 1) + 1
```

### Method 2: Iterative Solution
```python
def tower_of_hanoi_iterative(n):
    from collections import deque
    
    stack = deque()
    stack.append((n, ('A', 'C')))
    
    while stack:
        disks, towers = stack.pop()
        from_rod, to_rod = towers
        
        if disks == 1:
            print(f"{from_rod} {to_rod}")
        else:
            aux_rod = chr(ord('A') + ord('B') + ord('C') - ord(from_rod) - ord(to_rod))
            stack.append((disks - 1, (aux_rod, to_rod)))
            stack.append((1, (from_rod, to_rod)))
            stack.append((disks - 1, (from_rod, aux_rod)))
```

### Method 3: Mathematical Formula
```python
def tower_of_hanoi_mathematical(n):
    for i in range(1, (1 << n)):
        disk = (i & -i).bit_length()  # Get least significant bit
        from_rod = (i >> (disk - 1)) % 3
        to_rod = (from_rod + 1) % 3
        if n % 2 == 0 and disk == 1:
            to_rod = (to_rod + 1) % 3
        
        print(f"{chr(ord('A') + from_rod)} {chr(ord('A') + to_rod)}")
```

## Time Complexity
- **Time**: O(2^n) - exponential due to recursive nature
- **Space**: O(n) - recursion depth

## Example Walkthrough

**Input**: n = 3

**Process**:
1. Move disk 1: A → C
2. Move disk 2: A → B
3. Move disk 1: C → B
4. Move disk 3: A → C
5. Move disk 1: B → A
6. Move disk 2: B → C
7. Move disk 1: A → C

**Total moves**: 7 (2³ - 1)

## Problem Variations

### Variation 1: Constrained Moves
**Problem**: Only allow moves between adjacent towers.

**Solution**: Modify recursive calls to use adjacent towers only.

### Variation 2: Multiple Towers
**Problem**: Use k towers instead of 3.

**Approach**: Use dynamic programming with state (disks, towers).

### Variation 3: Weighted Disks
**Problem**: Each disk has a weight. Find minimum total weight moved.

**Approach**: Use greedy strategy or dynamic programming.

### Variation 4: Initial Configuration
**Problem**: Start with disks distributed across all towers.

**Solution**: Use state representation and BFS/DFS to find optimal sequence.

### Variation 5: Limited Moves
**Problem**: Find if it's possible to reach target state in k moves.

**Approach**: Use state space search with pruning.

### Variation 6: Cyclic Towers
**Problem**: Towers are arranged in a circle, can only move clockwise.

**Solution**: Modify move patterns for cyclic constraints.

## Advanced Applications

### 1. Algorithm Analysis
- Classic example of recursive algorithms
- Demonstrates exponential complexity
- Used in algorithm design courses

### 2. State Space Search
- Example of state representation
- Used in AI and game theory
- Applied in puzzle solving

### 3. Memory Management
- Analogous to memory allocation strategies
- Used in disk scheduling algorithms
- Applied in cache management

## Implementation Details

### State Representation
```python
class State:
    def __init__(self, towers):
        self.towers = towers
    
    def __eq__(self, other):
        return self.towers == other.towers
    
    def __hash__(self):
        # Custom hash function for state
        h = 0
        for tower in self.towers:
            h = h * 31 + len(tower)
        return h
```

### Move Validation
```python
def is_valid_move(state, from_tower, to_tower):
    if from_tower == to_tower:
        return False
    if not state.towers[from_tower]:
        return False
    if not state.towers[to_tower]:
        return True
    return state.towers[from_tower][-1] < state.towers[to_tower][-1]
```

## Related Problems
- [Permutations](../permutations_analysis/)
- [Creating Strings](../creating_strings_analysis/)
- [Gray Code](../gray_code_analysis/)

## Practice Problems
1. **CSES**: Tower of Hanoi
2. **LeetCode**: Similar recursive problems
3. **AtCoder**: State space search problems

## Key Takeaways
1. **Recursive thinking** is essential for this problem
2. **Mathematical formula** 2^n - 1 is elegant and useful
3. **State representation** is crucial for variations
4. **Optimality** can be proven mathematically
5. **Pattern recognition** helps in understanding the solution
6. **Memory management** is important for large n
7. **Applications** extend beyond just puzzle solving
