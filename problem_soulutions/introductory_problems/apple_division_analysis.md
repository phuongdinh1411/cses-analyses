---
layout: simple
title: "Apple Division"
permalink: /problem_soulutions/introductory_problems/apple_division_analysis
---

# Apple Division

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand subset generation and partition optimization problems
- Apply bitmasking or backtracking to generate all possible subsets
- Implement efficient subset generation algorithms with proper weight calculation
- Optimize subset generation using bitmasking and mathematical optimization
- Handle edge cases in subset problems (small n, large weights, equal partitions)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Subset generation, bitmasking, backtracking, partition problems, optimization
- **Data Structures**: Bit manipulation, arrays, subset tracking, weight calculation
- **Mathematical Concepts**: Combinatorics, subset theory, optimization, partition theory
- **Programming Skills**: Bit operations, subset generation, weight calculation, algorithm implementation
- **Related Problems**: Subset problems, Partition problems, Optimization problems, Bitmasking

## Problem Description

**Problem**: Given n apples with weights w₁, w₂, ..., wₙ, divide them into two groups such that the difference between the total weights of the two groups is minimized.

**Input**: 
- First line: n (1 ≤ n ≤ 20)
- Second line: n integers w₁, w₂, ..., wₙ (1 ≤ wᵢ ≤ 10⁹)

**Output**: The minimum possible difference between the two groups.

**Constraints**:
- 1 ≤ n ≤ 20
- 1 ≤ wᵢ ≤ 10⁹
- Must divide into exactly 2 groups
- Each apple goes to exactly one group
- Find minimum weight difference

**Example**:
```
Input:
5
3 2 7 4 1

Output:
1

Explanation: Group 1: {3, 2, 1} = 6, Group 2: {7, 4} = 11, Difference = |11-6| = 5
But better: Group 1: {3, 2, 4} = 9, Group 2: {7, 1} = 8, Difference = |9-8| = 1
```

## Visual Example

### Input and Weight Analysis
```
Input: n = 5, weights = [3, 2, 7, 4, 1]

Apple weights: [3, 2, 7, 4, 1]
Total weight: 3 + 2 + 7 + 4 + 1 = 17
Target: Minimize difference between two groups
```

### Bitmask Representation
```
For n = 5 apples, we have 2^5 = 32 possible divisions:

Bitmask 00000: Group 1 = [], Group 2 = [3,2,7,4,1]
Bitmask 00001: Group 1 = [1], Group 2 = [3,2,7,4]
Bitmask 00010: Group 1 = [4], Group 2 = [3,2,7,1]
Bitmask 00011: Group 1 = [4,1], Group 2 = [3,2,7]
...
Bitmask 11111: Group 1 = [3,2,7,4,1], Group 2 = []
```

### Optimal Division Process
```
For weights = [3, 2, 7, 4, 1], total = 17:

Best division found:
Bitmask 01101: Group 1 = [2, 7, 1] = 10, Group 2 = [3, 4] = 7
Difference = |10 - 7| = 3

Even better:
Bitmask 10110: Group 1 = [3, 7, 4] = 14, Group 2 = [2, 1] = 3  
Difference = |14 - 3| = 11

Optimal:
Bitmask 11010: Group 1 = [3, 2, 4] = 9, Group 2 = [7, 1] = 8
Difference = |9 - 8| = 1 ✓
```

### Key Insight
The solution works by:
1. Using bitmasking to represent all possible divisions
2. Calculating weight difference for each division
3. Finding the minimum difference
4. Time complexity: O(n × 2^n) for checking all subsets
5. Space complexity: O(1) for storing variables

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Naive Brute Force (Inefficient)

**Key Insights from Naive Brute Force Solution:**
- Generate all possible subset divisions using bitmasking
- Simple but computationally expensive approach
- Not suitable for large n due to exponential growth
- Straightforward implementation but poor scalability

**Algorithm:**
1. Generate all possible bitmasks from 0 to 2^n - 1
2. For each bitmask, calculate group 1 weight
3. Calculate group 2 weight as total - group 1
4. Find minimum difference across all divisions

**Visual Example:**
```
Naive brute force: Check all divisions
For weights = [3, 2, 7, 4, 1]:

Check all 32 bitmasks:
00000: Group1=[], Group2=[3,2,7,4,1], Diff=|0-17|=17
00001: Group1=[1], Group2=[3,2,7,4], Diff=|1-16|=15
00010: Group1=[4], Group2=[3,2,7,1], Diff=|4-13|=9
...
11010: Group1=[3,2,4], Group2=[7,1], Diff=|9-8|=1 ✓
```

**Implementation:**
```python
def apple_division_naive(weights):
    n = len(weights)
    total_sum = sum(weights)
    min_diff = float('inf')
    
    # Try all possible divisions (2^n combinations)
    for mask in range(1 << n):
        group1_sum = 0
        for i in range(n):
            if mask & (1 << i):  # If bit i is set
                group1_sum += weights[i]
        
        # Calculate difference
        diff = abs(total_sum - 2 * group1_sum)
        min_diff = min(min_diff, diff)
    
    return min_diff

def solve_apple_division_naive():
    n = int(input())
    weights = list(map(int, input().split()))
    result = apple_division_naive(weights)
    print(result)
```

**Time Complexity:** O(n × 2^n) for checking all subsets
**Space Complexity:** O(1) for storing variables

**Why it's inefficient:**
- O(n × 2^n) time complexity grows exponentially
- Not suitable for competitive programming with n up to 20
- Memory-intensive for large n
- Poor performance with exponential growth

### Approach 2: Optimized Brute Force with Early Termination (Better)

**Key Insights from Optimized Brute Force Solution:**
- Use early termination to skip unnecessary calculations
- More efficient than naive brute force approach
- Standard method for subset problems
- Can handle larger n than naive approach

**Algorithm:**
1. Generate all possible bitmasks from 0 to 2^n - 1
2. For each bitmask, calculate group 1 weight
3. Use early termination if group 1 weight > total/2
4. Find minimum difference across valid divisions

**Visual Example:**
```
Optimized brute force: Early termination
For weights = [3, 2, 7, 4, 1], total = 17:

Check bitmasks with early termination:
00000: Group1=0 ≤ 8.5, Diff=|0-17|=17
00001: Group1=1 ≤ 8.5, Diff=|1-16|=15
...
10000: Group1=3 ≤ 8.5, Diff=|3-14|=11
11000: Group1=5 ≤ 8.5, Diff=|5-12|=7
11100: Group1=12 > 8.5 → Skip (early termination)
```

**Implementation:**
```python
def apple_division_optimized(weights):
    n = len(weights)
    total_sum = sum(weights)
    min_diff = float('inf')
    
    for mask in range(1 << n):
        group1_sum = 0
        for i in range(n):
            if mask & (1 << i):
                group1_sum += weights[i]
        
        # Early termination: if group1 is already too heavy
        if group1_sum > total_sum // 2:
            continue
            
        diff = abs(total_sum - 2 * group1_sum)
        min_diff = min(min_diff, diff)
    
    return min_diff

def solve_apple_division_optimized():
    n = int(input())
    weights = list(map(int, input().split()))
    result = apple_division_optimized(weights)
    print(result)
```

**Time Complexity:** O(n × 2^n) for checking all subsets
**Space Complexity:** O(1) for storing variables

**Why it's better:**
- Uses early termination to skip about half the combinations
- More efficient than naive brute force
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Mathematical Optimization with Symmetry (Optimal)

**Key Insights from Mathematical Optimization Solution:**
- Use mathematical properties to reduce search space
- Most efficient approach for subset problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use mathematical properties to reduce search space
2. Leverage symmetry to avoid duplicate calculations
3. Use optimized bitmasking with mathematical insights
4. Apply mathematical optimization for optimal solution

**Visual Example:**
```
Mathematical optimization: Symmetry reduction
For weights = [3, 2, 7, 4, 1], total = 17:

Key insight: If mask represents Group1, then ~mask represents Group2
We only need to check masks where Group1 ≤ total/2

Symmetric pairs:
00001 ↔ 11110: Same difference
00010 ↔ 11101: Same difference
00011 ↔ 11100: Same difference
...
Only check first half of bitmasks!
```

**Implementation:**
```python
def apple_division_mathematical(weights):
    n = len(weights)
    total_sum = sum(weights)
    min_diff = float('inf')
    
    # Only check first half due to symmetry
    for mask in range(1 << (n - 1)):
        group1_sum = 0
        for i in range(n):
            if mask & (1 << i):
                group1_sum += weights[i]
        
        # Calculate difference
        diff = abs(total_sum - 2 * group1_sum)
        min_diff = min(min_diff, diff)
    
    return min_diff

def solve_apple_division():
    n = int(input())
    weights = list(map(int, input().split()))
    result = apple_division_mathematical(weights)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_apple_division()
```

**Time Complexity:** O(n × 2^(n-1)) for checking half the subsets
**Space Complexity:** O(1) for storing variables

**Why it's optimal:**
- O(n × 2^(n-1)) time complexity is optimal for this problem
- Uses mathematical symmetry to reduce search space by half
- Most efficient approach for competitive programming
- Standard method for subset optimization

## 🎯 Problem Variations

### Variation 1: Three Group Division
**Problem**: Divide apples into three groups to minimize maximum group weight.

**Link**: [CSES Problem Set - Three Group Division](https://cses.fi/problemset/task/three_group_division)

```python
def three_group_division(weights):
    n = len(weights)
    min_max_weight = float('inf')
    
    # Try all possible 3-group divisions
    for mask in range(3**n):
        groups = [0, 0, 0]
        temp_mask = mask
        
        for i in range(n):
            group = temp_mask % 3
            groups[group] += weights[i]
            temp_mask //= 3
        
        min_max_weight = min(min_max_weight, max(groups))
    
    return min_max_weight
```

### Variation 2: K Group Division
**Problem**: Divide apples into k groups to minimize maximum group weight.

**Link**: [CSES Problem Set - K Group Division](https://cses.fi/problemset/task/k_group_division)

```python
def k_group_division(weights, k):
    n = len(weights)
    min_max_weight = float('inf')
    
    # Try all possible k-group divisions
    for mask in range(k**n):
        groups = [0] * k
        temp_mask = mask
        
        for i in range(n):
            group = temp_mask % k
            groups[group] += weights[i]
            temp_mask //= k
        
        min_max_weight = min(min_max_weight, max(groups))
    
    return min_max_weight
```

### Variation 3: Balanced Partition
**Problem**: Find if apples can be divided into two groups with equal weight.

**Link**: [CSES Problem Set - Balanced Partition](https://cses.fi/problemset/task/balanced_partition)

```python
def balanced_partition(weights):
    total_sum = sum(weights)
    
    # If total is odd, cannot divide equally
    if total_sum % 2 != 0:
        return False
    
    target = total_sum // 2
    n = len(weights)
    
    # Check if any subset sums to target
    for mask in range(1 << n):
        subset_sum = 0
        for i in range(n):
            if mask & (1 << i):
                subset_sum += weights[i]
        
        if subset_sum == target:
            return True
    
    return False
```

## 🔗 Related Problems

- **[Subset Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Subset problems
- **[Partition Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Partition problems
- **[Optimization Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Optimization problems
- **[Bitmasking Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Bitmasking problems

## 📚 Learning Points

1. **Subset Generation**: Essential for understanding partition problems
2. **Bitmasking**: Key technique for efficient subset representation
3. **Mathematical Optimization**: Important for understanding symmetry reduction
4. **Early Termination**: Critical for understanding performance optimization
5. **Algorithm Optimization**: Foundation for many subset generation algorithms
6. **Mathematical Properties**: Critical for competitive programming efficiency

## 📝 Summary

The Apple Division problem demonstrates subset generation and mathematical optimization concepts for efficient partition problems. We explored three approaches:

1. **Naive Brute Force**: O(n × 2^n) time complexity using complete subset enumeration, inefficient for large n
2. **Optimized Brute Force with Early Termination**: O(n × 2^n) time complexity using early termination, better approach for subset problems
3. **Mathematical Optimization with Symmetry**: O(n × 2^(n-1)) time complexity with symmetry reduction, optimal approach for subset optimization

The key insights include understanding subset generation principles, using bitmasking for efficient subset representation, and applying mathematical optimization for optimal performance. This problem serves as an excellent introduction to subset generation algorithms and mathematical optimization techniques.
