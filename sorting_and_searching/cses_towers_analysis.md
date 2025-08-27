# CSES Towers - Problem Analysis

## Problem Statement
You are given n cubes in a certain order, and your task is to build towers by stacking them upon each other.

You can only place a cube on top of another cube if the cube on top has a smaller size than the cube below.

What is the minimum number of towers needed?

### Input
The first input line has an integer n: the number of cubes.
The second line has n integers k1,k2,…,kn: the sizes of the cubes.

### Output
Print one integer: the minimum number of towers needed.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ ki ≤ 10^9

### Example
```
Input:
5
3 8 2 1 5

Output:
2
```

## Solution Progression

### Approach 1: Brute Force - O(n!)
**Description**: Try all possible ways to arrange cubes into towers.

```python
def towers_brute_force(cubes):
    n = len(cubes)
    min_towers = n  # Worst case: each cube in its own tower
    
    def try_arrangement(towers, cube_idx):
        nonlocal min_towers
        
        if cube_idx == n:
            min_towers = min(min_towers, len(towers))
            return
        
        current_cube = cubes[cube_idx]
        
        # Try adding to existing towers
        for i, tower in enumerate(towers):
            if not tower or tower[-1] > current_cube:
                towers[i].append(current_cube)
                try_arrangement(towers, cube_idx + 1)
                towers[i].pop()
        
        # Try creating a new tower
        towers.append([current_cube])
        try_arrangement(towers, cube_idx + 1)
        towers.pop()
    
    try_arrangement([], 0)
    return min_towers
```

**Why this is inefficient**: We're trying all possible arrangements of cubes into towers, which leads to factorial complexity. This is completely impractical for large inputs.

### Improvement 1: Greedy Approach - O(n²)
**Description**: For each cube, place it on the tower with the smallest top cube that can hold it.

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

**Why this improvement works**: Instead of trying all arrangements, we use a greedy strategy. For each cube, we place it on the tower with the smallest top cube that can hold it. This minimizes the number of towers by maximizing the use of existing towers.

### Improvement 2: Binary Search Optimization - O(n log n)
**Description**: Use binary search to find the best tower for each cube efficiently.

```python
import bisect

def towers_binary_search(cubes):
    n = len(cubes)
    towers = []  # Keep towers sorted by top cube size
    
    for cube in cubes:
        # Find the smallest tower that can hold this cube
        idx = bisect.bisect_right(towers, cube)
        
        if idx < len(towers):
            # Place on existing tower
            towers[idx] = cube
        else:
            # Create new tower
            towers.append(cube)
    
    return len(towers)
```

**Why this improvement works**: We maintain the towers in sorted order by their top cube size. For each cube, we use binary search to find the smallest tower that can hold it. This reduces the search time from O(n) to O(log n) per cube.

### Alternative: Using Multiset - O(n log n)
**Description**: Use a multiset to maintain the top cubes of all towers.

```python
from collections import defaultdict

def towers_multiset(cubes):
    n = len(cubes)
    tower_tops = []  # Multiset of tower top sizes
    
    for cube in cubes:
        # Find the smallest tower that can hold this cube
        placed = False
        for i, top in enumerate(tower_tops):
            if top > cube:
                tower_tops[i] = cube
                placed = True
                break
        
        if not placed:
            tower_tops.append(cube)
    
    return len(tower_tops)
```

**Why this works**: We maintain a list of tower top sizes and for each cube, we find the smallest tower that can hold it. This is similar to the greedy approach but more explicit.

## Final Optimal Solution

```python
import bisect

n = int(input())
cubes = list(map(int, input().split()))

# Binary search approach
towers = []

for cube in cubes:
    # Find the smallest tower that can hold this cube
    idx = bisect.bisect_right(towers, cube)
    
    if idx < len(towers):
        # Place on existing tower
        towers[idx] = cube
    else:
        # Create new tower
        towers.append(cube)

print(len(towers))
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n!) | O(n) | Try all arrangements |
| Greedy | O(n²) | O(n) | Place on best available tower |
| Binary Search | O(n log n) | O(n) | Maintain sorted towers |
| Multiset | O(n log n) | O(n) | Track tower top sizes |

## Key Insights for Other Problems

### 1. **Greedy Tower Building**
**Principle**: Always place elements on the best available option to minimize resource usage.
**Applicable to**:
- Resource allocation problems
- Scheduling problems
- Optimization problems
- Greedy algorithms

**Example Problems**:
- Towers
- Activity selection
- Job scheduling
- Resource allocation

### 2. **Binary Search for Optimization**
**Principle**: Use binary search to find the optimal position or value efficiently.
**Applicable to**:
- Search problems
- Optimization problems
- Range queries
- Decision problems

**Example Problems**:
- Binary search
- Lower/upper bound
- Optimization problems
- Search in sorted arrays

### 3. **Maintaining Sorted Data Structures**
**Principle**: Keep data structures sorted to enable efficient operations.
**Applicable to**:
- Search problems
- Range queries
- Optimization problems
- Data structure problems

**Example Problems**:
- Binary search trees
- Sorted arrays
- Priority queues
- Ordered data structures

### 4. **Minimizing Resource Usage**
**Principle**: Use greedy strategies to minimize the number of resources needed.
**Applicable to**:
- Resource allocation
- Optimization problems
- Scheduling problems
- Greedy algorithms

**Example Problems**:
- Minimum number of resources
- Optimal scheduling
- Resource allocation
- Greedy optimization

## Notable Techniques

### 1. **Greedy Tower Building Pattern**
```python
# Place element on best available tower
def place_on_tower(element, towers):
    for i, tower_top in enumerate(towers):
        if tower_top > element:
            towers[i] = element
            return True
    towers.append(element)
    return False
```

### 2. **Binary Search for Optimal Position**
```python
# Find optimal position using binary search
def find_optimal_position(element, sorted_list):
    idx = bisect.bisect_right(sorted_list, element)
    return idx
```

### 3. **Maintaining Sorted Structure**
```python
# Keep data structure sorted for efficient operations
def maintain_sorted(arr, element):
    idx = bisect.bisect_right(arr, element)
    if idx < len(arr):
        arr[idx] = element
    else:
        arr.append(element)
```

## Edge Cases to Remember

1. **Single cube**: Only 1 tower needed
2. **All same size**: Each cube needs its own tower
3. **Strictly decreasing**: Only 1 tower needed
4. **Strictly increasing**: Each cube needs its own tower
5. **Large cube sizes**: Algorithm works with large integers

## Problem-Solving Framework

1. **Identify optimization nature**: This is about minimizing resource usage
2. **Consider greedy approach**: Always place on best available option
3. **Optimize search**: Use binary search for efficient placement
4. **Maintain sorted structure**: Keep towers sorted for efficient operations
5. **Handle edge cases**: Consider special input patterns

---

*This analysis shows how to systematically improve from O(n!) to O(n log n) and extracts reusable insights for greedy optimization problems.* 