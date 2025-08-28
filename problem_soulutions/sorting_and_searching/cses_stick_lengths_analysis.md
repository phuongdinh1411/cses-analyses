---
layout: simple
title: "Stick Lengths"permalink: /problem_soulutions/sorting_and_searching/cses_stick_lengths_analysis
---


# Stick Lengths

## Problem Statement
There are n sticks with some lengths. Your task is to modify the lengths so that all sticks have equal lengths. You can either lengthen or shorten each stick. Both operations cost x where x is the difference between the new and original length.

What is the minimum total cost?

### Input
The first input line has an integer n: the number of sticks.
The second line has n integers p1,p2,…,pn: the lengths of the sticks.

### Output
Print one integer: the minimum total cost.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ pi ≤ 10^9

### Example
```
Input:
5
2 3 1 5 2

Output:
5
```

## Solution Progression

### Approach 1: Brute Force - O(n * range)
**Description**: Try all possible target lengths and calculate the cost for each.

```python
def stick_lengths_brute_force(lengths):
    n = len(lengths)
    min_length = min(lengths)
    max_length = max(lengths)
    min_cost = float('inf')
    
    # Try all possible target lengths
    for target in range(min_length, max_length + 1):
        cost = 0
        for length in lengths:
            cost += abs(length - target)
        min_cost = min(min_cost, cost)
    
    return min_cost
```

**Why this is inefficient**: We're trying every possible target length between min and max, which can be very large (up to 10^9). This leads to O(n * range) complexity, which is too slow.

### Improvement 1: Median as Target - O(n log n)
**Description**: The optimal target length is the median of the array.

```python
def stick_lengths_median(lengths):
    n = len(lengths)
    
    # Sort to find median
    lengths.sort()
    
    # Median is the middle element (or average of two middle elements)
    if n % 2 == 1:
        target = lengths[n // 2]  # Odd number of elements
    else:
        target = (lengths[n // 2 - 1] + lengths[n // 2]) // 2  # Even number
    
    # Calculate cost
    cost = 0
    for length in lengths:
        cost += abs(length - target)
    
    return cost
```

**Why this improvement works**: The median minimizes the sum of absolute differences. This is because the median is the point that minimizes the total distance to all other points in a one-dimensional space.

### Improvement 2: Optimized Median Calculation - O(n log n)
**Description**: Use the median directly without trying all possible values.

```python
def stick_lengths_optimized(lengths):
    n = len(lengths)
    
    # Sort to find median
    lengths.sort()
    
    # Use the middle element as target (median)
    target = lengths[n // 2]
    
    # Calculate cost
    cost = 0
    for length in lengths:
        cost += abs(length - target)
    
    return cost
```

**Why this improvement works**: For odd n, the median is the middle element. For even n, both middle elements give the same optimal cost, so we can use either. This eliminates the need to try multiple target values.

### Alternative: Quick Select - O(n) average
**Description**: Use quick select to find the median without sorting the entire array.

```python
def quick_select(arr, k):
    """Find the k-th smallest element in arr"""
    if len(arr) == 1:
        return arr[0]
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    if k < len(left):
        return quick_select(left, k)
    elif k < len(left) + len(middle):
        return pivot
    else:
        return quick_select(right, k - len(left) - len(middle))

def stick_lengths_quick_select(lengths):
    n = len(lengths)
    
    # Find median using quick select
    target = quick_select(lengths, n // 2)
    
    # Calculate cost
    cost = 0
    for length in lengths:
        cost += abs(length - target)
    
    return cost
```

**Why this works**: Quick select finds the k-th smallest element in O(n) average time, which is faster than sorting for finding just the median.

## Final Optimal Solution

```python
n = int(input())
lengths = list(map(int, input().split()))

# Sort to find median
lengths.sort()
target = lengths[n // 2]

# Calculate minimum cost
cost = 0
for length in lengths:
    cost += abs(length - target)

print(cost)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n * range) | O(1) | Try all possible targets |
| Median | O(n log n) | O(1) | Use median as optimal target |
| Quick Select | O(n) average | O(n) | Find median without full sort |

## Key Insights for Other Problems

### 1. **Median Minimizes Absolute Differences**
**Principle**: The median minimizes the sum of absolute differences from all points.
**Applicable to**:
- Minimizing total distance problems
- Facility location problems
- Optimization problems with absolute differences
- Cost minimization problems

**Example Problems**:
- Stick lengths
- Meeting point in 1D
- Warehouse location
- Median of medians

### 2. **Sorting for Finding Order Statistics**
**Principle**: Sort to easily find median, quartiles, or other order statistics.
**Applicable to**:
- Finding median, mode, percentiles
- Order-based problems
- Statistical problems
- Optimization problems

**Example Problems**:
- Find median of two sorted arrays
- K-th largest element
- Percentile calculations
- Order statistics

### 3. **Quick Select for Order Statistics**
**Principle**: Use quick select to find k-th smallest element without full sorting.
**Applicable to**:
- Finding order statistics
- Median finding
- K-th largest/smallest element
- Partial sorting problems

**Example Problems**:
- Find k-th largest element
- Median of unsorted array
- Top k elements
- Order statistics

### 4. **Absolute Difference Optimization**
**Principle**: Problems involving absolute differences often have median as optimal solution.
**Applicable to**:
- Distance minimization
- Cost optimization
- Facility location
- Statistical problems

**Example Problems**:
- Minimum moves to equal array
- Meeting point problems
- Warehouse location
- Cost optimization

## Notable Techniques

### 1. **Median Finding Pattern**
```python
# Sort and find median
arr.sort()
median = arr[len(arr) // 2]  # For odd length
# or
median = (arr[len(arr)//2 - 1] + arr[len(arr)//2]) // 2  # For even length
```

### 2. **Quick Select Pattern**
```python
def quick_select(arr, k):
    if len(arr) == 1:
        return arr[0]
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    if k < len(left):
        return quick_select(left, k)
    elif k < len(left) + len(middle):
        return pivot
    else:
        return quick_select(right, k - len(left) - len(middle))
```

### 3. **Absolute Difference Sum**
```python
# Calculate sum of absolute differences
def abs_diff_sum(arr, target):
    return sum(abs(x - target) for x in arr)
```

## Edge Cases to Remember

1. **Single element**: Cost is 0 (already optimal)
2. **All same lengths**: Cost is 0 (no changes needed)
3. **Even number of elements**: Both middle elements give same optimal cost
4. **Large numbers**: Handle integer overflow in cost calculation
5. **Negative numbers**: Algorithm works with negative lengths

## Problem-Solving Framework

1. **Identify optimization nature**: This is a cost minimization problem
2. **Consider median approach**: Median minimizes absolute differences
3. **Choose efficient median finding**: Sort for simplicity, quick select for speed
4. **Handle edge cases**: Single element, all same, etc.
5. **Calculate cost efficiently**: Sum absolute differences

---

*This analysis shows how to systematically improve from O(n * range) to O(n log n) and extracts reusable insights for optimization problems involving absolute differences.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Stick Lengths with Different Costs**
**Problem**: Lengthening and shortening have different costs per unit.
```python
def stick_lengths_different_costs(lengths, lengthen_cost, shorten_cost):
    n = len(lengths)
    lengths.sort()
    target = lengths[n // 2]  # Median
    
    cost = 0
    for length in lengths:
        if length < target:
            cost += (target - length) * lengthen_cost
        else:
            cost += (length - target) * shorten_cost
    
    return cost
```

#### **Variation 2: Stick Lengths with Constraints**
**Problem**: Target length must be between L and R.
```python
def stick_lengths_with_constraints(lengths, min_target, max_target):
    n = len(lengths)
    lengths.sort()
    median = lengths[n // 2]
    
    # Clamp median to valid range
    target = max(min_target, min(max_target, median))
    
    cost = 0
    for length in lengths:
        cost += abs(length - target)
    
    return cost
```

#### **Variation 3: Stick Lengths with K Groups**
**Problem**: Divide sticks into K groups, each group having equal lengths.
```python
def stick_lengths_k_groups(lengths, k):
    n = len(lengths)
    lengths.sort()
    
    # Use dynamic programming to find optimal grouping
    dp = [[float('inf')] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    
    for i in range(1, n + 1):
        for j in range(1, k + 1):
            # Try grouping elements from start to i
            for start in range(i):
                # Calculate cost for group [start, i-1]
                group_lengths = lengths[start:i]
                group_target = group_lengths[len(group_lengths) // 2]
                group_cost = sum(abs(x - group_target) for x in group_lengths)
                
                dp[i][j] = min(dp[i][j], dp[start][j - 1] + group_cost)
    
    return dp[n][k]
```

#### **Variation 4: Stick Lengths with Weighted Sticks**
**Problem**: Each stick has a weight. Minimize weighted sum of changes.
```python
def stick_lengths_weighted(lengths, weights):
    n = len(lengths)
    
    # Create weighted median
    weighted_pairs = [(lengths[i], weights[i]) for i in range(n)]
    weighted_pairs.sort()
    
    total_weight = sum(weights)
    cumulative_weight = 0
    target = weighted_pairs[0][0]
    
    for length, weight in weighted_pairs:
        cumulative_weight += weight
        if cumulative_weight >= total_weight / 2:
            target = length
            break
    
    cost = 0
    for i in range(n):
        cost += abs(lengths[i] - target) * weights[i]
    
    return cost
```

#### **Variation 5: Stick Lengths with Dynamic Updates**
**Problem**: Support adding and removing sticks dynamically.
```python
class DynamicStickLengths:
    def __init__(self):
        self.lengths = []
        self.total_cost = 0
    
    def add_stick(self, length):
        # Insert in sorted order
        import bisect
        pos = bisect.bisect_left(self.lengths, length)
        self.lengths.insert(pos, length)
        
        # Recalculate target and cost
        self._update_cost()
    
    def remove_stick(self, length):
        # Remove from sorted list
        pos = bisect.bisect_left(self.lengths, length)
        if pos < len(self.lengths) and self.lengths[pos] == length:
            self.lengths.pop(pos)
            self._update_cost()
    
    def _update_cost(self):
        if not self.lengths:
            self.total_cost = 0
            return
        
        target = self.lengths[len(self.lengths) // 2]
        self.total_cost = sum(abs(x - target) for x in self.lengths)
    
    def get_min_cost(self):
        return self.total_cost
```

### 🔗 **Related Problems & Concepts**

#### **1. Optimization Problems**
- **Linear Programming**: Formulate as LP problem
- **Convex Optimization**: Optimize convex functions
- **Combinatorial Optimization**: Optimize discrete structures
- **Approximation Algorithms**: Find approximate solutions

#### **2. Mathematical Problems**
- **Median Finding**: Find median efficiently
- **Mean vs Median**: Compare central tendency measures
- **Statistical Measures**: Various statistical concepts
- **Mathematical Optimization**: Mathematical optimization theory

#### **3. Sorting Problems**
- **Array Sorting**: Sort array efficiently
- **Custom Sorting**: Sort based on custom criteria
- **Stable Sorting**: Maintain relative order of equal elements
- **In-place Sorting**: Sort without extra space

#### **4. Dynamic Programming Problems**
- **Partitioning Problems**: Partition arrays optimally
- **Grouping Problems**: Group elements optimally
- **Cost Optimization**: Minimize various costs
- **State Management**: Manage dynamic states

#### **5. Data Structure Problems**
- **Priority Queue**: Efficient element management
- **Binary Search Tree**: Ordered data structure
- **Segment Tree**: Range query data structure
- **Fenwick Tree**: Dynamic range queries

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n = int(input())
    lengths = list(map(int, input().split()))
    
    lengths.sort()
    target = lengths[n // 2]
    
    cost = 0
    for length in lengths:
        cost += abs(length - target)
    
    print(cost)
```

#### **2. Range Queries**
```python
# Precompute minimum costs for different subarrays
def precompute_stick_costs(lengths):
    n = len(lengths)
    cost_matrix = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(i, n):
            subarray = lengths[i:j+1]
            subarray.sort()
            target = subarray[len(subarray) // 2]
            cost = sum(abs(x - target) for x in subarray)
            cost_matrix[i][j] = cost
    
    return cost_matrix

# Answer queries about minimum costs for subarrays
def cost_query(cost_matrix, l, r):
    return cost_matrix[l][r]
```

#### **3. Interactive Problems**
```python
# Interactive stick length optimizer
def interactive_stick_lengths():
    n = int(input("Enter number of sticks: "))
    lengths = list(map(int, input("Enter stick lengths: ").split()))
    
    print(f"Original lengths: {lengths}")
    
    # Sort and find median
    lengths.sort()
    target = lengths[n // 2]
    
    print(f"Sorted lengths: {lengths}")
    print(f"Target length (median): {target}")
    
    # Calculate changes
    changes = []
    total_cost = 0
    
    for i, length in enumerate(lengths):
        change = abs(length - target)
        changes.append(change)
        total_cost += change
        print(f"Stick {i+1}: {length} -> {target} (change: {change})")
    
    print(f"Total cost: {total_cost}")
    print(f"Changes: {changes}")
```

### 🧮 **Mathematical Extensions**

#### **1. Statistics and Probability**
- **Central Tendency**: Mean, median, mode
- **Dispersion**: Variance, standard deviation
- **Probability Distributions**: Various distributions
- **Statistical Inference**: Statistical analysis

#### **2. Optimization Theory**
- **Linear Programming**: Formulate as LP problem
- **Convex Optimization**: Analyze convexity properties
- **Duality Theory**: Study dual problems
- **Sensitivity Analysis**: Analyze parameter changes

#### **3. Algorithm Analysis**
- **Complexity Analysis**: Time and space complexity
- **Amortized Analysis**: Average case analysis
- **Probabilistic Analysis**: Expected performance
- **Worst Case Analysis**: Upper bounds

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Sorting Algorithms**: Various sorting techniques
- **Median Finding**: Efficient median algorithms
- **Dynamic Programming**: Optimal substructure
- **Binary Search**: Efficient search techniques

#### **2. Mathematical Concepts**
- **Statistics**: Central tendency and dispersion
- **Optimization**: Mathematical optimization theory
- **Combinatorics**: Counting and arrangement
- **Algorithm Analysis**: Complexity and correctness

#### **3. Programming Concepts**
- **Array Manipulation**: Efficient array operations
- **Data Structures**: Efficient storage and retrieval
- **Algorithm Design**: Problem-solving strategies
- **Complexity Analysis**: Performance evaluation

---

*This analysis demonstrates optimization techniques and shows various extensions for mathematical problems.* 