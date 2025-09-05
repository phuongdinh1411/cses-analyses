---
layout: simple
title: "Towers - Minimum Number of Cube Towers"
permalink: /problem_soulutions/sorting_and_searching/cses_towers_analysis
---

# Towers - Minimum Number of Cube Towers

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand longest decreasing subsequence problems and greedy tower placement strategies
- [ ] **Objective 2**: Apply greedy algorithms with binary search to minimize tower count
- [ ] **Objective 3**: Implement efficient tower placement algorithms with O(n log n) time complexity
- [ ] **Objective 4**: Optimize tower placement using binary search and greedy selection techniques
- [ ] **Objective 5**: Handle edge cases in tower placement (increasing sequence, decreasing sequence, single cube)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Greedy algorithms, binary search, longest decreasing subsequence, tower placement, optimization problems
- **Data Structures**: Arrays, binary search tracking, tower tracking, sequence tracking
- **Mathematical Concepts**: Longest decreasing subsequence theory, tower mathematics, optimization problems
- **Programming Skills**: Binary search implementation, greedy algorithm implementation, tower placement logic, algorithm implementation
- **Related Problems**: Longest Increasing Subsequence (similar concept), Binary search problems, Greedy algorithm problems

## 📋 Problem Description

You are given n cubes in a certain order. Build towers by stacking them upon each other. You can only place a cube on top of another cube if the cube on top has a smaller size than the cube below. What is the minimum number of towers needed?

This is a longest decreasing subsequence problem that requires finding the minimum number of towers to stack all cubes. The solution involves using a greedy approach with binary search to efficiently place each cube on the optimal tower.

**Input**: 
- First line: n (number of cubes)
- Second line: n integers k₁, k₂, ..., kₙ (sizes of cubes)

**Output**: 
- Minimum number of towers needed

**Constraints**:
- 1 ≤ n ≤ 2⋅10⁵
- 1 ≤ kᵢ ≤ 10⁹

**Example**:
```
Input:
5
3 8 2 1 5

Output:
2

Explanation**: 
- Cube sequence: [3, 8, 2, 1, 5]
- Tower 1: 3 → 2 → 1 (decreasing order)
- Tower 2: 8 → 5 (decreasing order)
- Minimum towers needed: 2
- Cannot stack more cubes as they would violate the size constraint
```

## 📊 Visual Example

### Input Cubes
```
Cubes: [3, 8, 2, 1, 5]
Index:  0  1  2  3  4
```

### Tower Building Process
```
Step 1: Process cube 3
┌─────────────────────────────────────┐
│ Towers: []                          │
│ Place cube 3 on new tower          │
│ Towers: [3]                         │
└─────────────────────────────────────┘

Step 2: Process cube 8
┌─────────────────────────────────────┐
│ Towers: [3]                         │
│ Cube 8 > 3, cannot stack on tower 1 │
│ Create new tower for cube 8         │
│ Towers: [3, 8]                      │
└─────────────────────────────────────┘

Step 3: Process cube 2
┌─────────────────────────────────────┐
│ Towers: [3, 8]                      │
│ Cube 2 < 3, can stack on tower 1    │
│ Towers: [3→2, 8]                    │
└─────────────────────────────────────┘

Step 4: Process cube 1
┌─────────────────────────────────────┐
│ Towers: [3→2, 8]                    │
│ Cube 1 < 2, can stack on tower 1    │
│ Towers: [3→2→1, 8]                  │
└─────────────────────────────────────┘

Step 5: Process cube 5
┌─────────────────────────────────────┐
│ Towers: [3→2→1, 8]                  │
│ Cube 5 > 1, cannot stack on tower 1 │
│ Cube 5 < 8, can stack on tower 2    │
│ Towers: [3→2→1, 8→5]                │
└─────────────────────────────────────┘
```

### Final Tower Configuration
```
Tower 1: 3 → 2 → 1
Tower 2: 8 → 5

Visual representation:
    ┌─┐
    │1│ ← Tower 1
    ├─┤
    │2│
    ├─┤
    │3│
    └─┘

    ┌─┐
    │5│ ← Tower 2
    ├─┤
    │8│
    └─┘

Total towers: 2
```

### Greedy Strategy Explanation
```
Key Insight: Always place cube on the leftmost tower where it fits

Why this works:
- If we place a cube on a tower that's not the leftmost possible:
  - We might block future cubes that could fit on that tower
  - The leftmost tower gives us the most flexibility for future cubes
- This minimizes the number of towers needed
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Stack cubes into towers
- Each cube must be smaller than the cube below it
- Find minimum number of towers needed
- Process cubes in given order

**Key Observations:**
- This is a longest decreasing subsequence problem
- Can use greedy approach with binary search
- Need to track top cube of each tower
- Optimal strategy: place on smallest valid tower

### Step 2: Greedy Approach
**Idea**: For each cube, place it on the tower with the smallest top cube that can hold it.

```python
def towers_greedy(cubes):
    n = len(cubes)
    towers = []  # Each tower is represented by its top cube size
    
    for cube in cubes:
        # Find the best tower to place this cube
        best_tower = -1
        best_size = float('inf')
        
        for i, top_size in enumerate(towers):
            if top_size > cube and top_size < best_size:
                best_tower = i
                best_size = top_size
        
        if best_tower != -1:
            # Place on existing tower
            towers[best_tower] = cube
        else:
            # Create new tower
            towers.append(cube)
    
    return len(towers)
```

**Why this works:**
- Always place cube on smallest valid tower
- This minimizes number of towers needed
- Greedy choice is optimal
- Simple and intuitive approach

### Step 3: Optimized Solution with Binary Search
**Idea**: Use binary search to find the optimal tower efficiently.

```python
def towers_optimized(cubes):
    n = len(cubes)
    towers = []  # Top cube of each tower
    
    for cube in cubes:
        # Binary search for the smallest tower that can hold this cube
        left, right = 0, len(towers)
        
        while left < right:
            mid = (left + right) // 2
            if towers[mid] > cube:
                right = mid
            else:
                left = mid + 1
        
        if left < len(towers):
            # Place on existing tower
            towers[left] = cube
        else:
            # Create new tower
            towers.append(cube)
    
    return len(towers)
```

**Why this is better:**
- Binary search reduces complexity from O(n²) to O(n log n)
- More efficient for large inputs
- Same optimal result
- Cleaner implementation

### Step 3: Optimization/Alternative
**Alternative approaches:**
- **Brute Force**: Check all possible tower placements O(n²)
- **Greedy with Binary Search**: Optimal O(n log n) approach
- **Dynamic Programming**: For weighted cube problems

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_towers():
    n = int(input())
    cubes = list(map(int, input().split()))
    
    # Optimized greedy approach with binary search
    towers = []
    
    for cube in cubes:
        # Binary search for optimal tower
        left, right = 0, len(towers)
        
        while left < right:
            mid = (left + right) // 2
            if towers[mid] > cube:
                right = mid
            else:
                left = mid + 1
        
        if left < len(towers):
            towers[left] = cube
        else:
            towers.append(cube)
    
    print(len(towers))

# Main execution
if __name__ == "__main__":
    solve_towers()
```

**Why this works:**
- Optimal greedy approach
- Efficient binary search implementation
- Handles all edge cases

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ([3, 8, 2, 1, 5], 2),
        ([1, 2, 3, 4, 5], 5),
        ([5, 4, 3, 2, 1], 1),
        ([1, 1, 1, 1], 4),
        ([1], 1),
    ]
    
    for cubes, expected in test_cases:
        result = solve_test(cubes)
        print(f"Cubes: {cubes}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(cubes):
    towers = []
    
    for cube in cubes:
        left, right = 0, len(towers)
        
        while left < right:
            mid = (left + right) // 2
            if towers[mid] > cube:
                right = mid
            else:
                left = mid + 1
        
        if left < len(towers):
            towers[left] = cube
        else:
            towers.append(cube)
    
    return len(towers)

test_solution()
```

### Step 5: Testing Our Solution
**Test cases to verify correctness:**
- **Test 1**: Basic tower building (should return optimal count)
- **Test 2**: All cubes same size (should return n)
- **Test 3**: Strictly decreasing (should return 1)
- **Test 4**: Complex pattern (should return optimal count)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(n) | Check all possible placements |
| Greedy with Binary Search | O(n log n) | O(n) | Binary search for optimal tower |
| Dynamic Programming | O(n²) | O(n) | For weighted cube problems |

### Time Complexity
- **Time**: O(n log n) - binary search for each cube
- **Space**: O(n) - tower storage

### Why This Solution Works
- **Greedy Strategy**: Always place on smallest valid tower
- **Binary Search**: Efficient tower finding
- **Optimal Substructure**: Each decision is optimal
- **Correctness**: Proven greedy approach

## 🎯 Key Insights

### 1. **Greedy Strategy**
- Always place cube on smallest valid tower
- This minimizes number of towers needed
- Greedy choice leads to optimal solution
- No need for backtracking

### 2. **Binary Search Optimization**
- Towers array is always sorted
- Binary search finds optimal position
- Reduces complexity from O(n²) to O(n log n)
- Efficient for large inputs

### 3. **Longest Decreasing Subsequence**
- This problem is equivalent to LDS
- Number of towers = length of LDS
- Can use standard LDS algorithms
- Well-studied problem

## 🎯 Problem Variations

### Variation 1: Towers with Height Limit
**Problem**: Each tower has a maximum height limit.

```python
def towers_with_height_limit(cubes, max_height):
    n = len(cubes)
    towers = []  # (top_cube, height) for each tower
    
    for cube in cubes:
        # Find best tower considering height limit
        best_tower = -1
        best_size = float('inf')
        
        for i, (top_cube, height) in enumerate(towers):
            if top_cube > cube and height < max_height and top_cube < best_size:
                best_tower = i
                best_size = top_cube
        
        if best_tower != -1:
            # Place on existing tower
            towers[best_tower] = (cube, towers[best_tower][1] + 1)
        else:
            # Create new tower
            towers.append((cube, 1))
    
    return len(towers)
```

### Variation 2: Towers with Weight Constraints
**Problem**: Each cube has a weight, and towers have weight limits.

```python
def towers_with_weight_limit(cubes, weights, max_weight):
    n = len(cubes)
    towers = []  # (top_cube, total_weight) for each tower
    
    for i, cube in enumerate(cubes):
        weight = weights[i]
        
        # Find best tower considering weight limit
        best_tower = -1
        best_size = float('inf')
        
        for j, (top_cube, total_weight) in enumerate(towers):
            if (top_cube > cube and 
                total_weight + weight <= max_weight and 
                top_cube < best_size):
                best_tower = j
                best_size = top_cube
        
        if best_tower != -1:
            # Place on existing tower
            towers[best_tower] = (cube, towers[best_tower][1] + weight)
        else:
            # Create new tower
            towers.append((cube, weight))
    
    return len(towers)
```

### Variation 3: Towers with Different Base Sizes
**Problem**: Each tower has a different base size requirement.

```python
def towers_with_base_requirements(cubes, base_sizes):
    n = len(cubes)
    towers = []  # (top_cube, base_size) for each tower
    
    for i, cube in enumerate(cubes):
        # Find best tower considering base size
        best_tower = -1
        best_size = float('inf')
        
        for j, (top_cube, base_size) in enumerate(towers):
            if (top_cube > cube and 
                cube >= base_sizes[j] and 
                top_cube < best_size):
                best_tower = j
                best_size = top_cube
        
        if best_tower != -1:
            # Place on existing tower
            towers[best_tower] = (cube, towers[best_tower][1])
        else:
            # Create new tower
            towers.append((cube, cube))
    
    return len(towers)
```

### Variation 4: Towers with Color Constraints
**Problem**: Cubes have colors, and adjacent cubes must have different colors.

```python
def towers_with_color_constraints(cubes, colors):
    n = len(cubes)
    towers = []  # (top_cube, top_color) for each tower
    
    for i, cube in enumerate(cubes):
        color = colors[i]
        
        # Find best tower considering color constraint
        best_tower = -1
        best_size = float('inf')
        
        for j, (top_cube, top_color) in enumerate(towers):
            if (top_cube > cube and 
                color != top_color and 
                top_cube < best_size):
                best_tower = j
                best_size = top_cube
        
        if best_tower != -1:
            # Place on existing tower
            towers[best_tower] = (cube, color)
        else:
            # Create new tower
            towers.append((cube, color))
    
    return len(towers)
```

### Variation 5: Dynamic Tower Management
**Problem**: Support adding/removing cubes dynamically.

```python
class DynamicTowers:
    def __init__(self):
        self.towers = []
    
    def add_cube(self, cube):
        # Binary search for optimal tower
        left, right = 0, len(self.towers)
        
        while left < right:
            mid = (left + right) // 2
            if self.towers[mid] > cube:
                right = mid
            else:
                left = mid + 1
        
        if left < len(self.towers):
            self.towers[left] = cube
        else:
            self.towers.append(cube)
        
        return len(self.towers)
    
    def remove_cube(self, cube):
        # Find and remove cube from towers
        for i, top_cube in enumerate(self.towers):
            if top_cube == cube:
                self.towers.pop(i)
                break
        
        return len(self.towers)
    
    def get_tower_count(self):
        return len(self.towers)
```

## 🎯 Key Insights

### Important Concepts and Patterns
- **Greedy Algorithm**: Always choose the locally optimal choice
- **Binary Search**: Efficiently find optimal placement
- **Longest Decreasing Subsequence**: Classic problem with greedy solution
- **Tower Building**: Stack elements in decreasing order

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Towers with Weighted Cubes**
```python
def towers_weighted(cubes, weights):
    # Handle towers with weighted cubes
    
    # Sort cubes by weight (heaviest first)
    cube_data = [(cubes[i], weights[i]) for i in range(len(cubes))]
    cube_data.sort(key=lambda x: x[1], reverse=True)
    
    towers = []
    
    for cube, weight in cube_data:
        # Binary search for optimal tower
        left, right = 0, len(towers)
        
        while left < right:
            mid = (left + right) // 2
            if towers[mid][0] > cube:
                right = mid
            else:
                left = mid + 1
        
        if left < len(towers):
            towers[left] = (cube, weight)
        else:
            towers.append((cube, weight))
    
    return len(towers)
```

#### **2. Towers with Height Constraints**
```python
def towers_height_constrained(cubes, max_height):
    # Handle towers with maximum height constraints
    
    towers = []
    
    for cube in cubes:
        # Binary search for optimal tower
        left, right = 0, len(towers)
        
        while left < right:
            mid = (left + right) // 2
            if towers[mid][-1] > cube:
                right = mid
            else:
                left = mid + 1
        
        if left < len(towers):
            # Check height constraint
            if len(towers[left]) < max_height:
                towers[left].append(cube)
            else:
                # Create new tower
                towers.append([cube])
        else:
            # Create new tower
            towers.append([cube])
    
    return len(towers)
```

#### **3. Towers with Dynamic Updates**
```python
def towers_dynamic(operations):
    # Handle towers with dynamic cube additions/removals
    
    cubes = []
    towers = []
    
    for operation in operations:
        if operation[0] == 'add':
            # Add new cube
            cube = operation[1]
            cubes.append(cube)
            
            # Rebuild towers optimally
            towers = rebuild_towers(cubes)
        
        elif operation[0] == 'remove':
            # Remove cube at index
            index = operation[1]
            if 0 <= index < len(cubes):
                cubes.pop(index)
                towers = rebuild_towers(cubes)
        
        elif operation[0] == 'query':
            # Return current number of towers
            yield len(towers)
    
    return list(towers_dynamic(operations))

def rebuild_towers(cubes):
    towers = []
    
    for cube in cubes:
        left, right = 0, len(towers)
        
        while left < right:
            mid = (left + right) // 2
            if towers[mid] > cube:
                right = mid
            else:
                left = mid + 1
        
        if left < len(towers):
            towers[left] = cube
        else:
            towers.append(cube)
    
    return towers
```

## 🔗 Related Problems

### Links to Similar Problems
- **Longest Decreasing Subsequence**: Similar greedy approach
- **Binary Search**: Problems requiring optimal placement
- **Greedy Algorithms**: Problems with optimal local choices
- **Stacking Problems**: Tower building and stacking

## 📚 Learning Points

1. **Greedy Algorithms**: Optimal local choices lead to global optimum
2. **Binary Search**: Efficient search in sorted arrays
3. **Longest Decreasing Subsequence**: Classic algorithmic problem
4. **Dynamic Programming**: Alternative approach for LDS

---

**This is a great introduction to greedy algorithms and binary search!** 🎯 