---
layout: simple
title: "Towers"permalink: /problem_soulutions/sorting_and_searching/towers_analysis
---


# Towers

## Problem Statement
Given n cubes with side lengths a1,a2,…,an, you want to build towers by stacking cubes. You can only place a cube on top of another cube if its side length is smaller than the side length of the cube below it. Find the minimum number of towers needed.

### Input
The first input line has an integer n: the number of cubes.
The second line has n integers a1,a2,…,an: the side lengths of the cubes.

### Output
Print one integer: the minimum number of towers needed.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ ai ≤ 10^9

### Example
```
Input:
5
3 8 2 1 5

Output:
2
```

## Solution Progression

### Approach 1: Greedy with Sorting - O(n²)
**Description**: Sort cubes and try to place each cube on the smallest possible tower.

```python
def towers_naive(n, cubes):
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

**Why this is inefficient**: For each cube, we need to check all towers, leading to O(n²) time complexity.

### Improvement 1: Binary Search - O(n log n)
**Description**: Use binary search to find the smallest tower that can hold the current cube.

```python
import bisect

def towers_optimized(n, cubes):
    cubes.sort()
    towers = []
    
    for cube in cubes:
        # Find the smallest tower that can hold this cube
        idx = bisect.bisect_right(towers, cube)
        
        if idx < len(towers):
            towers[idx] = cube
        else:
            towers.append(cube)
    
    return len(towers)
```

**Why this improvement works**: We use binary search to find the optimal tower for each cube in O(log n) time, reducing the overall complexity to O(n log n).

## Final Optimal Solution

```python
import bisect

n = int(input())
cubes = list(map(int, input().split()))

def find_minimum_towers(n, cubes):
    cubes.sort()
    towers = []
    
    for cube in cubes:
        # Find the smallest tower that can hold this cube
        idx = bisect.bisect_right(towers, cube)
        
        if idx < len(towers):
            towers[idx] = cube
        else:
            towers.append(cube)
    
    return len(towers)

result = find_minimum_towers(n, cubes)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Greedy with Sorting | O(n²) | O(n) | Try each tower for each cube |
| Binary Search | O(n log n) | O(n) | Use binary search for optimal placement |

## Key Insights for Other Problems

### 1. **Tower Building Problems**
**Principle**: Use greedy approach with binary search for optimal placement.
**Applicable to**: Tower problems, stacking problems, placement problems

### 2. **Binary Search Optimization**
**Principle**: Use binary search to find optimal positions in sorted structures.
**Applicable to**: Search problems, optimization problems, placement algorithms

### 3. **Greedy Placement**
**Principle**: Always place elements in the smallest possible valid position.
**Applicable to**: Placement problems, optimization problems, greedy algorithms

## Notable Techniques

### 1. **Binary Search Placement**
```python
def binary_search_placement(elements):
    elements.sort()
    towers = []
    
    for element in elements:
        idx = bisect.bisect_right(towers, element)
        
        if idx < len(towers):
            towers[idx] = element
        else:
            towers.append(element)
    
    return len(towers)
```

### 2. **Optimal Tower Selection**
```python
def select_optimal_tower(towers, cube):
    idx = bisect.bisect_right(towers, cube)
    
    if idx < len(towers):
        towers[idx] = cube
    else:
        towers.append(cube)
    
    return towers
```

### 3. **Tower Management**
```python
def manage_towers(cubes):
    cubes.sort()
    towers = []
    
    for cube in cubes:
        # Find optimal tower
        idx = bisect.bisect_right(towers, cube)
        
        if idx < len(towers):
            towers[idx] = cube
        else:
            towers.append(cube)
    
    return towers
```

## Problem-Solving Framework

1. **Identify problem type**: This is a tower building problem with optimal placement
2. **Choose approach**: Use greedy approach with binary search
3. **Sort elements**: Sort cubes in ascending order
4. **Initialize towers**: Start with empty tower list
5. **Place cubes**: Use binary search to find optimal tower for each cube
6. **Update towers**: Either replace existing tower or create new one
7. **Return result**: Output the minimum number of towers needed

---

*This analysis shows how to efficiently find the minimum number of towers needed using greedy approach with binary search optimization.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Weighted Towers**
**Problem**: Each cube has a weight. Find the minimum number of towers such that the total weight of each tower doesn't exceed a given limit.
```python
def weighted_towers(n, cubes, weights, max_weight):
    # Sort by cube size
    cube_data = [(cubes[i], weights[i]) for i in range(n)]
    cube_data.sort()
    
    towers = []  # Each tower is (top_cube_size, total_weight)
    
    for cube_size, weight in cube_data:
        placed = False
        
        # Try to place on existing towers
        for i in range(len(towers)):
            top_size, tower_weight = towers[i]
            if cube_size < top_size and tower_weight + weight <= max_weight:
                towers[i] = (cube_size, tower_weight + weight)
                placed = True
                break
        
        # Create new tower if can't place on existing ones
        if not placed:
            towers.append((cube_size, weight))
    
    return len(towers)
```

#### **Variation 2: Height-Constrained Towers**
**Problem**: Each tower has a maximum height limit. Find the minimum number of towers needed.
```python
def height_constrained_towers(n, cubes, max_height):
    cubes.sort()
    towers = []  # Each tower is (top_cube_size, height)
    
    for cube in cubes:
        placed = False
        
        # Try to place on existing towers
        for i in range(len(towers)):
            top_size, height = towers[i]
            if cube < top_size and height + 1 <= max_height:
                towers[i] = (cube, height + 1)
                placed = True
                break
        
        # Create new tower if can't place on existing ones
        if not placed:
            towers.append((cube, 1))
    
    return len(towers)
```

#### **Variation 3: Multi-dimensional Towers**
**Problem**: Cubes have multiple dimensions (length, width, height). A cube can only be placed on another if all its dimensions are smaller.
```python
def multi_dimensional_towers(n, cubes):
    # cubes[i] = (length, width, height)
    cubes.sort(key=lambda x: (x[0], x[1], x[2]))
    towers = []
    
    for cube in cubes:
        placed = False
        
        # Try to place on existing towers
        for i in range(len(towers)):
            top_cube = towers[i]
            if (cube[0] < top_cube[0] and 
                cube[1] < top_cube[1] and 
                cube[2] < top_cube[2]):
                towers[i] = cube
                placed = True
                break
        
        # Create new tower if can't place on existing ones
        if not placed:
            towers.append(cube)
    
    return len(towers)
```

#### **Variation 4: Tower Stability**
**Problem**: Each cube has a stability factor. A tower is stable if the sum of stability factors of all cubes in it is above a threshold.
```python
def stable_towers(n, cubes, stabilities, min_stability):
    cube_data = [(cubes[i], stabilities[i]) for i in range(n)]
    cube_data.sort()
    
    towers = []  # Each tower is (top_cube_size, total_stability)
    
    for cube_size, stability in cube_data:
        placed = False
        
        # Try to place on existing towers
        for i in range(len(towers)):
            top_size, tower_stability = towers[i]
            if cube_size < top_size and tower_stability + stability >= min_stability:
                towers[i] = (cube_size, tower_stability + stability)
                placed = True
                break
        
        # Create new tower if can't place on existing ones
        if not placed:
            towers.append((cube_size, stability))
    
    return len(towers)
```

#### **Variation 5: Tower Cost Optimization**
**Problem**: Each tower has a cost based on the cubes in it. Find the minimum total cost for all towers.
```python
def cost_optimized_towers(n, cubes, costs):
    # costs[i] = cost of cube i
    cube_data = [(cubes[i], costs[i]) for i in range(n)]
    cube_data.sort()
    
    towers = []  # Each tower is (top_cube_size, total_cost)
    
    for cube_size, cost in cube_data:
        placed = False
        min_cost_increase = float('inf')
        best_tower = -1
        
        # Find tower with minimum cost increase
        for i in range(len(towers)):
            top_size, tower_cost = towers[i]
            if cube_size < top_size:
                cost_increase = cost  # Cost of adding this cube
                if cost_increase < min_cost_increase:
                    min_cost_increase = cost_increase
                    best_tower = i
        
        # Place on best tower or create new one
        if best_tower != -1:
            towers[best_tower] = (cube_size, towers[best_tower][1] + cost)
        else:
            towers.append((cube_size, cost))
    
    return sum(tower[1] for tower in towers)
```

### 🔗 **Related Problems & Concepts**

#### **1. Tower Building Problems**
- **Hanoi Towers**: Classic tower of Hanoi problem
- **Tower Defense**: Games with tower building mechanics
- **Tower Placement**: Optimal placement of towers
- **Tower Height**: Maximizing tower heights

#### **2. Stacking Problems**
- **Box Stacking**: Stacking boxes optimally
- **Container Loading**: Loading containers efficiently
- **Pallet Stacking**: Stacking pallets optimally
- **Block Stacking**: Stacking blocks with constraints

#### **3. Placement Problems**
- **Optimal Placement**: Finding optimal positions
- **Resource Allocation**: Allocating resources optimally
- **Scheduling**: Scheduling tasks optimally
- **Assignment**: Assigning items to containers

#### **4. Optimization Problems**
- **Minimum Cost**: Minimizing total cost
- **Maximum Efficiency**: Maximizing efficiency
- **Resource Optimization**: Optimizing resource usage
- **Constraint Satisfaction**: Satisfying constraints optimally

#### **5. Geometric Problems**
- **3D Geometry**: Three-dimensional geometric problems
- **Spatial Arrangement**: Arranging objects in space
- **Volume Optimization**: Optimizing volume usage
- **Surface Area**: Minimizing surface area

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n = int(input())
    cubes = list(map(int, input().split()))
    
    result = find_minimum_towers(n, cubes)
    print(result)
```

#### **2. Range Queries**
```python
# Precompute for different cube ranges
def precompute_tower_counts(cubes):
    n = len(cubes)
    # Precompute for all possible ranges
    dp = {}
    
    for start in range(n):
        for end in range(start, n):
            subarray = cubes[start:end+1]
            count = find_minimum_towers(len(subarray), subarray)
            dp[(start, end)] = count
    
    return dp

# Answer range queries efficiently
def tower_query(dp, start, end):
    return dp.get((start, end), 0)
```

#### **3. Interactive Problems**
```python
# Interactive tower builder
def interactive_tower_builder():
    n = int(input("Enter number of cubes: "))
    cubes = []
    
    for i in range(n):
        size = int(input(f"Enter size of cube {i+1}: "))
        cubes.append(size)
    
    print("Cubes:", cubes)
    
    while True:
        query = input("Enter query (min_towers/weighted/height/cost/exit): ")
        if query == "exit":
            break
        
        if query == "min_towers":
            result = find_minimum_towers(n, cubes)
            print(f"Minimum towers needed: {result}")
        elif query == "weighted":
            weights = []
            max_weight = int(input("Enter maximum weight per tower: "))
            for i in range(n):
                weight = int(input(f"Enter weight of cube {i+1}: "))
                weights.append(weight)
            result = weighted_towers(n, cubes, weights, max_weight)
            print(f"Minimum towers with weight constraint: {result}")
        elif query == "height":
            max_height = int(input("Enter maximum height per tower: "))
            result = height_constrained_towers(n, cubes, max_height)
            print(f"Minimum towers with height constraint: {result}")
        elif query == "cost":
            costs = []
            for i in range(n):
                cost = int(input(f"Enter cost of cube {i+1}: "))
                costs.append(cost)
            result = cost_optimized_towers(n, cubes, costs)
            print(f"Minimum total cost: {result}")
```

### 🧮 **Mathematical Extensions**

#### **1. Geometry**
- **3D Geometry**: Three-dimensional geometric properties
- **Volume Calculations**: Calculating volumes of towers
- **Surface Area**: Calculating surface areas
- **Spatial Relationships**: Understanding spatial relationships

#### **2. Optimization Theory**
- **Linear Programming**: Formulate as LP problem
- **Integer Programming**: Discrete optimization
- **Combinatorial Optimization**: Optimizing combinations
- **Constraint Optimization**: Optimization with constraints

#### **3. Algorithm Analysis**
- **Complexity Analysis**: Time and space complexity
- **Optimality Proofs**: Proving algorithm optimality
- **Lower Bounds**: Establishing problem lower bounds
- **Approximation**: Finding approximate solutions

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Greedy Algorithms**: Core technique for tower building
- **Binary Search**: For optimal placement
- **Dynamic Programming**: Alternative approach for some variations
- **Sorting Algorithms**: For efficient processing

#### **2. Mathematical Concepts**
- **Geometry**: Understanding geometric properties
- **Optimization**: Mathematical optimization techniques
- **Combinatorics**: Counting and arrangement
- **Algorithm Analysis**: Complexity and correctness

#### **3. Programming Concepts**
- **Data Structures**: Efficient storage and retrieval
- **Algorithm Design**: Problem-solving strategies
- **Binary Search**: Efficient search techniques
- **Sorting**: Efficient sorting techniques

---

*This analysis demonstrates efficient tower building techniques and shows various extensions for stacking and placement problems.* 