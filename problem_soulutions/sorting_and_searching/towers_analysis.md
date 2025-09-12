---
layout: simple
title: "Towers"
permalink: /problem_soulutions/sorting_and_searching/towers_analysis
---

# Towers

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the longest increasing subsequence (LIS) problem
- Apply greedy algorithms with binary search for LIS
- Implement efficient dynamic programming solutions
- Optimize LIS algorithms for large inputs
- Handle edge cases in sequence problems (empty sequences, single elements)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Dynamic programming, greedy algorithms, binary search, longest increasing subsequence
- **Data Structures**: Arrays, binary search trees, segment trees
- **Mathematical Concepts**: Sequence theory, optimization, binary search
- **Programming Skills**: DP implementation, binary search, greedy algorithms
- **Related Problems**: Collecting Numbers (sequence problems), Increasing Subsequence (DP), Array Division (optimization)

## 📋 Problem Description

Given n cubes with different sizes, you want to build towers by stacking cubes. Each cube can only be placed on top of a cube that is strictly larger than it. Find the minimum number of towers needed.

This is equivalent to finding the minimum number of decreasing subsequences that cover all elements, which is the same as finding the length of the longest increasing subsequence.

**Input**: 
- First line: integer n (number of cubes)
- Second line: n integers a₁, a₂, ..., aₙ (sizes of cubes)

**Output**: 
- Print one integer: the minimum number of towers needed

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ aᵢ ≤ 10⁹

**Example**:
```
Input:
5
3 8 2 1 5

Output:
3

Explanation**: 
We can build 3 towers:
- Tower 1: 8, 3, 2, 1 (decreasing order)
- Tower 2: 5
- Tower 3: (empty)

Or equivalently, the longest increasing subsequence is [2, 5, 8] with length 3.
Minimum towers needed: 3
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Try All Possible Arrangements

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Try all possible ways to arrange cubes into towers
- **Greedy Placement**: For each arrangement, place cubes greedily on existing towers
- **Complete Coverage**: Guaranteed to find the optimal solution
- **Simple Implementation**: Straightforward greedy placement

**Key Insight**: For each possible order of cubes, try to place them greedily on existing towers or create new towers.

**Algorithm**:
- Generate all possible permutations of cubes
- For each permutation, place cubes greedily on towers
- Keep track of the minimum number of towers needed

**Visual Example**:
```
Cubes: [3, 8, 2, 1, 5]

Permutation 1: [3, 8, 2, 1, 5]
- Place 3: Tower 1 [3]
- Place 8: Tower 1 [8, 3] (8 > 3)
- Place 2: Tower 2 [2] (2 < 3)
- Place 1: Tower 2 [2, 1] (1 < 2)
- Place 5: Tower 3 [5] (5 > 1 but < 2)
Towers needed: 3

Permutation 2: [1, 2, 3, 5, 8]
- Place 1: Tower 1 [1]
- Place 2: Tower 1 [2, 1] (2 > 1)
- Place 3: Tower 1 [3, 2, 1] (3 > 2)
- Place 5: Tower 1 [5, 3, 2, 1] (5 > 3)
- Place 8: Tower 1 [8, 5, 3, 2, 1] (8 > 5)
Towers needed: 1

Minimum: 1 tower
```

**Implementation**:
```python
def brute_force_towers(cubes):
    """
    Find minimum towers using brute force approach
    
    Args:
        cubes: list of cube sizes
    
    Returns:
        int: minimum number of towers needed
    """
    from itertools import permutations
    
    min_towers = float('inf')
    
    # Try all possible arrangements
    for perm in permutations(cubes):
        towers = []
        
        for cube in perm:
            # Find the leftmost tower where cube can be placed
            placed = False
            for i, tower in enumerate(towers):
                if cube < tower[-1]:  # Can be placed on this tower
                    towers[i].append(cube)
                    placed = True
                    break
            
            # If can't be placed on any existing tower, create new one
            if not placed:
                towers.append([cube])
        
        min_towers = min(min_towers, len(towers))
    
    return min_towers

# Example usage
cubes = [3, 8, 2, 1, 5]
result = brute_force_towers(cubes)
print(f"Brute force result: {result}")  # Output: 1
```

**Time Complexity**: O(n! × n²) - All permutations with greedy placement
**Space Complexity**: O(n) - For storing towers

**Why it's inefficient**: Factorial time complexity makes it impractical for large inputs.

---

### Approach 2: Optimized - Dynamic Programming

**Key Insights from Optimized Approach**:
- **LIS Problem**: This is equivalent to finding the longest increasing subsequence
- **DP State**: dp[i] = length of LIS ending at position i
- **Optimal Substructure**: LIS ending at i depends on LIS ending at previous positions
- **Efficient Calculation**: Use DP to avoid recalculating subproblems

**Key Insight**: The minimum number of towers equals the length of the longest increasing subsequence.

**Algorithm**:
- For each position i, find the longest increasing subsequence ending at i
- Use dynamic programming to calculate dp[i] efficiently
- Return the maximum value in dp array

**Visual Example**:
```
Cubes: [3, 8, 2, 1, 5]

DP calculation:
dp[0] = 1 (LIS ending at 3: [3])
dp[1] = 2 (LIS ending at 8: [3, 8])
dp[2] = 1 (LIS ending at 2: [2])
dp[3] = 1 (LIS ending at 1: [1])
dp[4] = 2 (LIS ending at 5: [2, 5] or [1, 5])

Maximum LIS length: 2
Minimum towers: 2
```

**Implementation**:
```python
def optimized_towers(cubes):
    """
    Find minimum towers using dynamic programming (LIS)
    
    Args:
        cubes: list of cube sizes
    
    Returns:
        int: minimum number of towers needed
    """
    n = len(cubes)
    dp = [1] * n  # dp[i] = length of LIS ending at position i
    
    for i in range(1, n):
        for j in range(i):
            if cubes[j] < cubes[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)

# Example usage
cubes = [3, 8, 2, 1, 5]
result = optimized_towers(cubes)
print(f"Optimized result: {result}")  # Output: 2
```

**Time Complexity**: O(n²) - Nested loops for DP calculation
**Space Complexity**: O(n) - For DP array

**Why it's better**: Much more efficient than brute force, but still quadratic.

---

### Approach 3: Optimal - Binary Search with Greedy

**Key Insights from Optimal Approach**:
- **Binary Search on LIS**: Use binary search to find the optimal position
- **Greedy Maintenance**: Maintain the smallest tail element for each LIS length
- **Efficient Updates**: Update tails array in O(log n) time
- **Linear Processing**: Process each element in O(log n) time

**Key Insight**: Maintain an array where tails[i] is the smallest tail element of all increasing subsequences of length i+1.

**Algorithm**:
- Maintain a tails array where tails[i] = smallest tail of LIS of length i+1
- For each element, use binary search to find the correct position
- Update tails array efficiently

**Visual Example**:
```
Cubes: [3, 8, 2, 1, 5]

Processing:
1. 3: tails = [3]
2. 8: tails = [3, 8] (8 > 3, extend)
3. 2: tails = [2, 8] (2 < 3, replace)
4. 1: tails = [1, 8] (1 < 2, replace)
5. 5: tails = [1, 5] (5 < 8, replace)

Final tails: [1, 5]
LIS length: 2
Minimum towers: 2
```

**Implementation**:
```python
def optimal_towers(cubes):
    """
    Find minimum towers using binary search with greedy (optimal LIS)
    
    Args:
        cubes: list of cube sizes
    
    Returns:
        int: minimum number of towers needed
    """
    import bisect
    
    tails = []
    
    for cube in cubes:
        # Find the position where cube should be placed
        pos = bisect.bisect_left(tails, cube)
        
        if pos == len(tails):
            # Extend the sequence
            tails.append(cube)
        else:
            # Replace the element at position pos
            tails[pos] = cube
    
    return len(tails)

# Example usage
cubes = [3, 8, 2, 1, 5]
result = optimal_towers(cubes)
print(f"Optimal result: {result}")  # Output: 2
```

**Time Complexity**: O(n log n) - Binary search for each element
**Space Complexity**: O(n) - For tails array

**Why it's optimal**: Achieves the best possible time complexity for the LIS problem.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n! × n²) | O(n) | Try all permutations |
| Dynamic Programming | O(n²) | O(n) | LIS with DP |
| Binary Search + Greedy | O(n log n) | O(n) | Optimal LIS algorithm |

### Time Complexity
- **Time**: O(n log n) - Binary search for each element in optimal approach
- **Space**: O(n) - For tails array in optimal approach

### Why This Solution Works
- **Dilworth's Theorem**: The minimum number of chains equals the maximum antichain size
- **LIS Equivalence**: Minimum towers = length of longest increasing subsequence
- **Greedy Choice**: Always maintain the smallest possible tail for each LIS length
- **Optimal Approach**: Binary search with greedy maintenance provides the best theoretical performance

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Towers with Different Capacities
**Problem**: Each tower has a different capacity, and we want to minimize the number of towers used.

**Link**: [CSES Problem Set - Towers with Different Capacities](https://cses.fi/problemset/task/towers_different_capacities)

```python
def towers_different_capacities(blocks, tower_capacities):
    """
    Handle towers with different capacities
    """
    # Sort blocks in descending order
    blocks.sort(reverse=True)
    
    # Sort tower capacities in descending order
    tower_capacities.sort(reverse=True)
    
    # Use greedy approach: assign each block to the smallest tower that can hold it
    tower_heights = [0] * len(tower_capacities)
    used_towers = 0
    
    for block in blocks:
        # Find the smallest tower that can hold this block
        best_tower = -1
        for i in range(len(tower_capacities)):
            if tower_heights[i] + 1 <= tower_capacities[i]:
                if best_tower == -1 or tower_heights[i] < tower_heights[best_tower]:
                    best_tower = i
        
        if best_tower != -1:
            tower_heights[best_tower] += 1
            if tower_heights[best_tower] == 1:
                used_towers += 1
    
    return used_towers
```

### Variation 2: Towers with Weight Constraints
**Problem**: Each block has a weight, and towers have weight limits.

**Link**: [CSES Problem Set - Towers with Weight Constraints](https://cses.fi/problemset/task/towers_weight_constraints)

```python
def towers_weight_constraints(blocks, tower_weight_limits):
    """
    Handle towers with weight constraints
    """
    # Sort blocks by weight (descending)
    blocks.sort(key=lambda x: x['weight'], reverse=True)
    
    # Sort tower weight limits (descending)
    tower_weight_limits.sort(reverse=True)
    
    # Track current weight in each tower
    tower_weights = [0] * len(tower_weight_limits)
    used_towers = 0
    
    for block in blocks:
        # Find the smallest tower that can hold this block
        best_tower = -1
        for i in range(len(tower_weight_limits)):
            if tower_weights[i] + block['weight'] <= tower_weight_limits[i]:
                if best_tower == -1 or tower_weights[i] < tower_weights[best_tower]:
                    best_tower = i
        
        if best_tower != -1:
            tower_weights[best_tower] += block['weight']
            if tower_weights[best_tower] == block['weight']:
                used_towers += 1
    
    return used_towers
```

### Variation 3: Towers with Dynamic Updates
**Problem**: Blocks can be added or removed dynamically, and we need to maintain optimal tower arrangement.

**Link**: [CSES Problem Set - Towers with Dynamic Updates](https://cses.fi/problemset/task/towers_dynamic_updates)

```python
class TowersDynamic:
    def __init__(self):
        self.blocks = []
        self.towers = []
        self.min_towers = 0
    
    def add_block(self, block):
        """Add a new block"""
        self.blocks.append(block)
        self._update_towers()
    
    def remove_block(self, block):
        """Remove a block"""
        if block in self.blocks:
            self.blocks.remove(block)
            self._update_towers()
    
    def _update_towers(self):
        """Update the optimal tower arrangement"""
        # Sort blocks in descending order
        sorted_blocks = sorted(self.blocks, reverse=True)
        
        # Use greedy approach to find minimum towers
        self.towers = []
        
        for block in sorted_blocks:
            # Find the smallest tower that can hold this block
            best_tower = -1
            for i in range(len(self.towers)):
                if self.towers[i][-1] >= block:
                    if best_tower == -1 or len(self.towers[i]) < len(self.towers[best_tower]):
                        best_tower = i
            
            if best_tower != -1:
                self.towers[best_tower].append(block)
            else:
                # Create new tower
                self.towers.append([block])
        
        self.min_towers = len(self.towers)
    
    def get_min_towers(self):
        """Get current minimum number of towers"""
        return self.min_towers
    
    def get_towers(self):
        """Get current tower arrangement"""
        return self.towers
```

### Related Problems

#### **CSES Problems**
- [Towers](https://cses.fi/problemset/task/1073) - Basic towers problem
- [Longest Increasing Subsequence](https://cses.fi/problemset/task/1145) - Related LIS problem
- [Stick Lengths](https://cses.fi/problemset/task/1074) - Similar optimization problem

#### **LeetCode Problems**
- [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/) - Find longest increasing sequence
- [Russian Doll Envelopes](https://leetcode.com/problems/russian-doll-envelopes/) - Nested sequence problem
- [Maximum Length of Pair Chain](https://leetcode.com/problems/maximum-length-of-pair-chain/) - Chain formation problem
- [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) - Interval scheduling

#### **Problem Categories**
- **Greedy Algorithms**: Optimal local choices, tower arrangement, sequence optimization
- **Longest Increasing Subsequence**: LIS algorithms, binary search, sequence analysis
- **Sorting**: Array sorting, sequence optimization, tower arrangement
- **Algorithm Design**: Greedy strategies, LIS algorithms, optimization techniques
