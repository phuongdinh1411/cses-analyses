---
layout: simple
title: "Grid Path Description"
permalink: /problem_soulutions/introductory_problems/grid_path_description_analysis
---

# Grid Path Description

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand path simulation and grid navigation problems
- [ ] **Objective 2**: Apply simulation algorithms to trace paths and count valid configurations
- [ ] **Objective 3**: Implement efficient path simulation algorithms with proper boundary checking
- [ ] **Objective 4**: Optimize path simulation using mathematical analysis and constraint validation
- [ ] **Objective 5**: Handle edge cases in path simulation (boundary conditions, invalid moves, path validation)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Path simulation, grid navigation, string processing, simulation algorithms
- **Data Structures**: 2D arrays, coordinate tracking, path tracking, string manipulation
- **Mathematical Concepts**: Coordinate geometry, path analysis, simulation theory, grid mathematics
- **Programming Skills**: Grid manipulation, coordinate tracking, string processing, simulation implementation
- **Related Problems**: Grid problems, Path simulation, String processing, Simulation algorithms

## Problem Description

**Problem**: Given a grid path description (string of 'R', 'D', 'L', 'U' for right, down, left, up), find the number of different paths that can be described by this string when starting from the top-left corner of an n×n grid.

**Input**: 
- First line: n (grid size)
- Second line: path description string

**Output**: The number of valid paths.

**Example**:
```
Input:
3
RDLU

Output:
2

Explanation: 
Starting from (0,0), the path RDLU can be:
1. (0,0) → (1,0) → (1,1) → (0,1) → (0,0) ✓
2. (0,0) → (1,0) → (1,1) → (0,1) → (0,2) ✓
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Start from top-left corner (0,0) of an n×n grid
- Follow a path described by a string of directions
- Count how many different valid paths exist
- A path is valid if it stays within grid boundaries

**Key Observations:**
- Movement mapping: R(right), D(down), L(left), U(up)
- Need to check boundaries at each step
- Multiple paths might be possible for same description
- Use dynamic programming to count all valid paths

### Step 2: Simple Recursive Approach
**Idea**: Try following the path step by step, checking boundaries.

```python
def solve_simple(path, n):
    def is_valid(x, y):
        return 0 <= x < n and 0 <= y < n
    
    def follow_path(x, y, idx):
        if idx == len(path):
            return 1
        
        count = 0
        direction = path[idx]
        
        # Try each possible direction
        if direction == 'R' and is_valid(x + 1, y):
            count += follow_path(x + 1, y, idx + 1)
        if direction == 'D' and is_valid(x, y + 1):
            count += follow_path(x, y + 1, idx + 1)
        if direction == 'L' and is_valid(x - 1, y):
            count += follow_path(x - 1, y, idx + 1)
        if direction == 'U' and is_valid(x, y - 1):
            count += follow_path(x, y - 1, idx + 1)
        
        return count
    
    return follow_path(0, 0, 0)
```

**Why this works:**
- We follow the path step by step
- Check if each move stays within boundaries
- Count all valid paths that complete the description

### Step 3: Optimized DP Approach
**Idea**: Use dynamic programming with memoization for efficiency.

```python
def solve_optimized(path, n):
    dp = {}
    
    def follow_path_dp(x, y, idx):
        if idx == len(path):
            return 1
        
        state = (x, y, idx)
        if state in dp:
            return dp[state]
        
        count = 0
        direction = path[idx]
        
        # Try each possible direction
        if direction == 'R' and x + 1 < n:
            count += follow_path_dp(x + 1, y, idx + 1)
        if direction == 'D' and y + 1 < n:
            count += follow_path_dp(x, y + 1, idx + 1)
        if direction == 'L' and x - 1 >= 0:
            count += follow_path_dp(x - 1, y, idx + 1)
        if direction == 'U' and y - 1 >= 0:
            count += follow_path_dp(x, y - 1, idx + 1)
        
        dp[state] = count
        return count
    
    return follow_path_dp(0, 0, 0)
```

**Why this is better:**
- Uses memoization to avoid recalculating states
- More efficient for repeated subproblems
- Handles larger inputs better

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_grid_path():
    n = int(input())
    path = input().strip()
    
    dp = {}
    
    def follow_path_dp(x, y, idx):
        if idx == len(path):
            return 1
        
        state = (x, y, idx)
        if state in dp:
            return dp[state]
        
        count = 0
        direction = path[idx]
        
        # Try each possible direction
        if direction == 'R' and x + 1 < n:
            count += follow_path_dp(x + 1, y, idx + 1)
        if direction == 'D' and y + 1 < n:
            count += follow_path_dp(x, y + 1, idx + 1)
        if direction == 'L' and x - 1 >= 0:
            count += follow_path_dp(x - 1, y, idx + 1)
        if direction == 'U' and y - 1 >= 0:
            count += follow_path_dp(x, y - 1, idx + 1)
        
        dp[state] = count
        return count
    
    return follow_path_dp(0, 0, 0)

# Main execution
if __name__ == "__main__":
    result = solve_grid_path()
    print(result)
```

**Why this works:**
- Efficient dynamic programming approach
- Handles all valid paths correctly
- Uses memoization for performance

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (3, "RDLU", 2),
        (2, "RD", 1),
        (3, "RRDD", 1),
        (2, "RDLU", 0),  # Goes out of bounds
    ]
    
    for n, path, expected in test_cases:
        result = solve_test(n, path)
        print(f"n={n}, path='{path}'")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n, path):
    dp = {}
    
    def follow_path_dp(x, y, idx):
        if idx == len(path):
            return 1
        
        state = (x, y, idx)
        if state in dp:
            return dp[state]
        
        count = 0
        direction = path[idx]
        
        if direction == 'R' and x + 1 < n:
            count += follow_path_dp(x + 1, y, idx + 1)
        if direction == 'D' and y + 1 < n:
            count += follow_path_dp(x, y + 1, idx + 1)
        if direction == 'L' and x - 1 >= 0:
            count += follow_path_dp(x - 1, y, idx + 1)
        if direction == 'U' and y - 1 >= 0:
            count += follow_path_dp(x, y - 1, idx + 1)
        
        dp[state] = count
        return count
    
    return follow_path_dp(0, 0, 0)

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Worst Case**: O(n² × len(path)) - for each position and path index
- **With DP**: Much faster due to memoization
- **Space**: O(n² × len(path)) - DP state space

### Why This Solution Works
- **Complete**: Tries all valid paths
- **Efficient**: Uses dynamic programming with memoization
- **Correct**: Handles boundary checking properly

## 🎨 Visual Example

### Input Example
```
n = 3, path = "RDLU"
Output: 2 valid paths
```

### Grid and Movement
```
3×3 grid with coordinates:
   0 1 2
0  . . .
1  . . .
2  . . .

Movement mapping:
'R': (x,y) → (x+1,y) - Right
'D': (x,y) → (x,y+1) - Down  
'L': (x,y) → (x-1,y) - Left
'U': (x,y) → (x,y-1) - Up
```

### Path Analysis
```
Path "RDLU" from (0,0):

Step 1: 'R' - (0,0) → (1,0) ✓ (within bounds)
Step 2: 'D' - (1,0) → (1,1) ✓ (within bounds)
Step 3: 'L' - (1,1) → (0,1) ✓ (within bounds)
Step 4: 'U' - (0,1) → (0,0) ✓ (within bounds)

Path 1: (0,0) → (1,0) → (1,1) → (0,1) → (0,0)
```

### Alternative Path
```
Path "RDLU" can also be:

Step 1: 'R' - (0,0) → (1,0) ✓
Step 2: 'D' - (1,0) → (1,1) ✓  
Step 3: 'L' - (1,1) → (0,1) ✓
Step 4: 'U' - (0,1) → (0,2) ✓ (different from path 1)

Path 2: (0,0) → (1,0) → (1,1) → (0,1) → (0,2)
```

### Boundary Checking
```
For each move, check if new position is valid:

Move 'R': x+1 < n (x+1 < 3)
Move 'D': y+1 < n (y+1 < 3)
Move 'L': x-1 ≥ 0 (x-1 ≥ 0)
Move 'U': y-1 ≥ 0 (y-1 ≥ 0)

Invalid moves would go out of bounds.
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Simulation      │ O(4^m)       │ O(m)         │ Try all      │
│                 │              │              │ directions   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Dynamic Prog    │ O(n² × m)    │ O(n² × m)    │ Memoize      │
│                 │              │              │ states       │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Backtracking    │ O(4^m)       │ O(m)         │ Prune        │
│                 │              │              │ invalid      │
│                 │              │              │ paths        │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Path Validation**
- Check if each move stays within grid boundaries
- Ensure 0 ≤ x, y < n at each step
- Count only valid paths that don't go out of bounds

### 2. **Movement Mapping**
- 'R': (x, y) → (x+1, y)
- 'D': (x, y) → (x, y+1)
- 'L': (x, y) → (x-1, y)
- 'U': (x, y) → (x, y-1)

### 3. **Dynamic Programming**
- Use DP to count valid paths
- State: (position, current index in string)
- Transition: try each possible direction

## 🎯 Problem Variations

### Variation 1: Path with Obstacles
**Problem**: Some grid cells are blocked and cannot be visited.

```python
def grid_path_with_obstacles(path, n, obstacles):
    # obstacles is a set of blocked positions
    dp = {}
    
    def follow_path_dp(x, y, idx):
        if idx == len(path):
            return 1
        
        if (x, y) in obstacles:
            return 0
        
        state = (x, y, idx)
        if state in dp:
            return dp[state]
        
        count = 0
        direction = path[idx]
        
        if direction == 'R' and x + 1 < n and (x + 1, y) not in obstacles:
            count += follow_path_dp(x + 1, y, idx + 1)
        if direction == 'D' and y + 1 < n and (x, y + 1) not in obstacles:
            count += follow_path_dp(x, y + 1, idx + 1)
        if direction == 'L' and x - 1 >= 0 and (x - 1, y) not in obstacles:
            count += follow_path_dp(x - 1, y, idx + 1)
        if direction == 'U' and y - 1 >= 0 and (x, y - 1) not in obstacles:
            count += follow_path_dp(x, y - 1, idx + 1)
        
        dp[state] = count
        return count
    
    return follow_path_dp(0, 0, 0)
```

### Variation 2: Weighted Path
**Problem**: Each cell has a weight. Find path with minimum total weight.

```python
def weighted_grid_path(path, n, weights):
    # weights[x][y] = weight of cell (x, y)
    dp = {}
    
    def follow_path_dp(x, y, idx, current_weight):
        if idx == len(path):
            return current_weight
        
        state = (x, y, idx)
        if state in dp:
            return dp[state]
        
        min_weight = float('inf')
        direction = path[idx]
        
        if direction == 'R' and x + 1 < n:
            weight = follow_path_dp(x + 1, y, idx + 1, current_weight + weights[x + 1][y])
            min_weight = min(min_weight, weight)
        if direction == 'D' and y + 1 < n:
            weight = follow_path_dp(x, y + 1, idx + 1, current_weight + weights[x][y + 1])
            min_weight = min(min_weight, weight)
        if direction == 'L' and x - 1 >= 0:
            weight = follow_path_dp(x - 1, y, idx + 1, current_weight + weights[x - 1][y])
            min_weight = min(min_weight, weight)
        if direction == 'U' and y - 1 >= 0:
            weight = follow_path_dp(x, y - 1, idx + 1, current_weight + weights[x][y - 1])
            min_weight = min(min_weight, weight)
        
        dp[state] = min_weight
        return min_weight
    
    return follow_path_dp(0, 0, 0, weights[0][0])
```

### Variation 3: Multiple Paths
**Problem**: Find all possible path descriptions that lead to a target cell.

```python
def find_path_descriptions(n, target_x, target_y, max_length):
    def is_valid(x, y):
        return 0 <= x < n and 0 <= y < n
    
    def generate_paths(x, y, current_path, paths):
        if len(current_path) > max_length:
            return
        
        if x == target_x and y == target_y and len(current_path) > 0:
            paths.append(''.join(current_path))
        
        # Try each direction
        directions = [('R', x + 1, y), ('D', x, y + 1), ('L', x - 1, y), ('U', x, y - 1)]
        for direction, new_x, new_y in directions:
            if is_valid(new_x, new_y):
                current_path.append(direction)
                generate_paths(new_x, new_y, current_path, paths)
                current_path.pop()
    
    paths = []
    generate_paths(0, 0, [], paths)
    return paths
```

### Variation 4: Circular Grid
**Problem**: Grid wraps around (toroidal surface).

```python
def circular_grid_path(path, n):
    dp = {}
    
    def follow_path_dp(x, y, idx):
        if idx == len(path):
            return 1
        
        state = (x, y, idx)
        if state in dp:
            return dp[state]
        
        count = 0
        direction = path[idx]
        
        # Handle wraparound
        if direction == 'R':
            new_x = (x + 1) % n
            count += follow_path_dp(new_x, y, idx + 1)
        if direction == 'D':
            new_y = (y + 1) % n
            count += follow_path_dp(x, new_y, idx + 1)
        if direction == 'L':
            new_x = (x - 1) % n
            count += follow_path_dp(new_x, y, idx + 1)
        if direction == 'U':
            new_y = (y - 1) % n
            count += follow_path_dp(x, new_y, idx + 1)
        
        dp[state] = count
        return count
    
    return follow_path_dp(0, 0, 0)
```

## 🔗 Related Problems

- **[Grid Paths](/cses-analyses/problem_soulutions/dynamic_programming/grid_paths_analysis)**: Dynamic programming on grids
- **[Labyrinth](/cses-analyses/problem_soulutions/graph_algorithms/labyrinth_analysis)**: Path finding problems
- **[Two Knights](/cses-analyses/problem_soulutions/introductory_problems/two_knights_analysis)**: Grid movement problems

## 📚 Learning Points

1. **Path Finding**: Understanding grid-based path problems
2. **Dynamic Programming**: Using DP for counting problems
3. **Boundary Checking**: Validating moves within constraints
4. **State Representation**: Efficiently representing problem states

---

**This is a great introduction to grid-based path problems and dynamic programming!** 🎯
