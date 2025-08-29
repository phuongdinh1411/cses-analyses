---
layout: simple
title: "Towers"
permalink: /problem_soulutions/sorting_and_searching/towers_analysis
---

# Towers

## Problem Description

**Problem**: Given n cubes with side lengths a₁, a₂, ..., aₙ, build towers by stacking cubes. You can only place a cube on top of another cube if its side length is smaller than the side length of the cube below it. Find the minimum number of towers needed.

**Input**: 
- First line: n (number of cubes)
- Second line: n integers a₁, a₂, ..., aₙ (side lengths)

**Output**: Minimum number of towers needed.

**Example**:
```
Input:
5
3 8 2 1 5

Output:
2

Explanation: 
Tower 1: 8 → 5 → 3 → 2 → 1
Tower 2: (empty)
Minimum towers needed: 2
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Stack cubes to form towers
- Each cube must be smaller than the one below it
- Find minimum number of towers needed
- This is similar to the Longest Decreasing Subsequence problem

**Key Observations:**
- Need to sort cubes first
- Each tower represents a decreasing subsequence
- Minimum towers = length of longest decreasing subsequence
- Can use greedy approach with binary search

### Step 2: Greedy Approach
**Idea**: Sort cubes and try to place each cube on the smallest possible tower.

```python
def towers_greedy(n, cubes):
    cubes.sort()
    towers = []
    
    for cube in cubes:
        placed = False
        for i in range(len(towers)):
            if cube < towers[i]:
                towers[i] = cube
                placed = True
                break
        
        if not placed:
            towers.append(cube)
    
    return len(towers)
```

**Why this works:**
- Sort cubes in ascending order
- Try to place each cube on existing towers
- Place on smallest tower that can hold it
- Create new tower if no suitable tower found
- O(n²) time complexity

### Step 3: Binary Search Optimization
**Idea**: Use binary search to find the optimal tower for each cube.

```python
import bisect

def towers_binary_search(n, cubes):
    cubes.sort()
    towers = []  # Stores top cube size of each tower
    
    for cube in cubes:
        # Find smallest tower whose top cube is larger than current cube
        idx = bisect.bisect_right(towers, cube)
        
        if idx < len(towers):
            # Place on existing tower
            towers[idx] = cube
        else:
            # Create new tower
            towers.append(cube)
    
    return len(towers)
```

**Why this is better:**
- O(n log n) time complexity
- Uses binary search for efficient placement
- Maintains sorted order of tower tops
- Optimal solution

### Step 4: Complete Solution
**Putting it all together:**

```python
import bisect

def solve_towers():
    n = int(input())
    cubes = list(map(int, input().split()))
    
    # Sort cubes in ascending order
    cubes.sort()
    
    # towers[i] = size of top cube in tower i
    towers = []
    
    for cube in cubes:
        # Find smallest tower whose top cube is larger than current cube
        idx = bisect.bisect_right(towers, cube)
        
        if idx < len(towers):
            # Place on existing tower
            towers[idx] = cube
        else:
            # Create new tower
            towers.append(cube)
    
    print(len(towers))

# Main execution
if __name__ == "__main__":
    solve_towers()
```

**Why this works:**
- Optimal greedy approach with binary search
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (5, [3, 8, 2, 1, 5], 2),
        (3, [1, 2, 3], 3),
        (3, [3, 2, 1], 1),
        (4, [2, 1, 4, 3], 2),
        (1, [5], 1),
    ]
    
    for n, cubes, expected in test_cases:
        result = solve_test(n, cubes)
        print(f"Cubes: {cubes}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n, cubes):
    import bisect
    
    cubes.sort()
    towers = []
    
    for cube in cubes:
        idx = bisect.bisect_right(towers, cube)
        
        if idx < len(towers):
            towers[idx] = cube
        else:
            towers.append(cube)
    
    return len(towers)

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n log n) - sorting + binary search
- **Space**: O(n) - tower array storage

### Why This Solution Works
- **Greedy Strategy**: Always place cube on smallest suitable tower
- **Binary Search**: Efficient tower selection
- **Sorted Maintenance**: Keep tower tops sorted
- **Optimal Substructure**: Each decision is locally optimal

## 🎯 Key Insights

### 1. **Longest Decreasing Subsequence**
- Each tower represents a decreasing subsequence
- Minimum towers = length of LDS
- Key insight: convert to LDS problem
- Use binary search for efficiency

### 2. **Greedy Placement**
- Always place cube on smallest suitable tower
- Maintains optimal substructure
- No need to backtrack or reconsider
- Simple and efficient strategy

### 3. **Binary Search Optimization**
- Find insertion point in sorted array
- O(log n) tower selection
- Maintains sorted order automatically
- Crucial for efficiency

## 🎯 Problem Variations

### Variation 1: Weighted Towers
**Problem**: Each tower has a weight limit. Find minimum towers needed.

```python
def weighted_towers(n, cubes, weight_limits):
    cubes.sort()
    towers = []  # (top_cube, current_weight)
    
    for cube in cubes:
        placed = False
        
        # Try to place on existing towers
        for i in range(len(towers)):
            top_cube, weight = towers[i]
            if cube < top_cube and weight + cube <= weight_limits[i]:
                towers[i] = (cube, weight + cube)
                placed = True
                break
        
        if not placed:
            # Create new tower
            towers.append((cube, cube))
    
    return len(towers)
```

### Variation 2: Colored Towers
**Problem**: Cubes have colors. No two adjacent cubes can have same color.

```python
def colored_towers(n, cubes, colors):
    cubes_with_colors = list(zip(cubes, colors))
    cubes_with_colors.sort()
    
    towers = []  # (top_cube, top_color)
    
    for cube, color in cubes_with_colors:
        placed = False
        
        for i in range(len(towers)):
            top_cube, top_color = towers[i]
            if cube < top_cube and color != top_color:
                towers[i] = (cube, color)
                placed = True
                break
        
        if not placed:
            towers.append((cube, color))
    
    return len(towers)
```

### Variation 3: Height Constrained Towers
**Problem**: Each tower has a maximum height limit.

```python
def height_constrained_towers(n, cubes, max_heights):
    cubes.sort()
    towers = []  # (top_cube, current_height)
    
    for cube in cubes:
        placed = False
        
        for i in range(len(towers)):
            top_cube, height = towers[i]
            if cube < top_cube and height + 1 <= max_heights[i]:
                towers[i] = (cube, height + 1)
                placed = True
                break
        
        if not placed:
            towers.append((cube, 1))
    
    return len(towers)
```

### Variation 4: Dynamic Towers
**Problem**: Support adding/removing cubes dynamically.

```python
class DynamicTowers:
    def __init__(self):
        self.cubes = []
        self.towers = []
    
    def add_cube(self, cube):
        import bisect
        
        self.cubes.append(cube)
        self.cubes.sort()
        
        # Rebuild towers
        self.towers = []
        for c in self.cubes:
            idx = bisect.bisect_right(self.towers, c)
            if idx < len(self.towers):
                self.towers[idx] = c
            else:
                self.towers.append(c)
        
        return len(self.towers)
    
    def remove_cube(self, cube):
        if cube in self.cubes:
            self.cubes.remove(cube)
            
            # Rebuild towers
            self.towers = []
            for c in self.cubes:
                idx = bisect.bisect_right(self.towers, c)
                if idx < len(self.towers):
                    self.towers[idx] = c
                else:
                    self.towers.append(c)
        
        return len(self.towers)
    
    def get_minimum_towers(self):
        return len(self.towers)
```

### Variation 5: Multi-Dimensional Towers
**Problem**: Cubes have multiple dimensions (length, width, height).

```python
def multi_dimensional_towers(n, cubes):
    # cubes[i] = (length, width, height)
    # Sort by volume or any dimension
    cubes.sort(key=lambda x: x[0] * x[1] * x[2])
    
    towers = []  # (top_length, top_width, top_height)
    
    for length, width, height in cubes:
        placed = False
        
        for i in range(len(towers)):
            top_l, top_w, top_h = towers[i]
            if (length < top_l and width < top_w and height < top_h):
                towers[i] = (length, width, height)
                placed = True
                break
        
        if not placed:
            towers.append((length, width, height))
    
    return len(towers)
```

## 🔗 Related Problems

- **[Towers (Original)](/cses-analyses/problem_soulutions/sorting_and_searching/cses_towers_analysis)**: Original towers problem
- **[Longest Decreasing Subsequence](/cses-analyses/problem_soulutions/sorting_and_searching/)**: LDS problems
- **[Collecting Numbers](/cses-analyses/problem_soulutions/sorting_and_searching/cses_collecting_numbers_analysis)**: Array processing

## 📚 Learning Points

1. **Longest Decreasing Subsequence**: Convert problem to LDS
2. **Binary Search**: Efficient insertion point finding
3. **Greedy Algorithms**: Optimal local choices
4. **Problem Transformation**: Convert to known problem type

---

**This is a great introduction to LDS problems and binary search optimization!** 🎯 