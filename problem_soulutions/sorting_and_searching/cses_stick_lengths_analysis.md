---
layout: simple
title: "Stick Lengths"
permalink: /problem_soulutions/sorting_and_searching/cses_stick_lengths_analysis
---

# Stick Lengths

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand optimization problems with median-based solutions and cost minimization
- [ ] **Objective 2**: Apply median selection to minimize total absolute deviation costs
- [ ] **Objective 3**: Implement efficient optimization algorithms with O(n log n) time complexity
- [ ] **Objective 4**: Optimize cost minimization problems using sorting and median selection
- [ ] **Objective 5**: Handle edge cases in optimization problems (single element, all same values, cost overflow)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sorting algorithms, median selection, optimization problems, cost minimization, absolute deviation
- **Data Structures**: Arrays, sorting, median tracking, cost tracking
- **Mathematical Concepts**: Median theory, optimization mathematics, absolute deviation, cost analysis
- **Programming Skills**: Sorting implementation, median calculation, cost calculation, algorithm implementation
- **Related Problems**: Optimization problems, Median problems, Cost minimization problems

## Problem Description

**Problem**: There are n sticks with some lengths. Modify the lengths so that all sticks have equal lengths. You can either lengthen or shorten each stick. Both operations cost x where x is the difference between the new and original length. What is the minimum total cost?

**Input**: 
- First line: n (number of sticks)
- Second line: n integers p₁, p₂, ..., pₙ (lengths of sticks)

**Output**: Minimum total cost.

**Example**:
```
Input:
5
2 3 1 5 2

Output:
5

Explanation: Make all sticks length 2. Cost = |2-2| + |3-2| + |1-2| + |5-2| + |2-2| = 0 + 1 + 1 + 3 + 0 = 5.
```

## 📊 Visual Example

### Input Sticks
```
Sticks: [2, 3, 1, 5, 2]
Index:   0  1  2  3  4
```

### Sorting to Find Median
```
Original: [2, 3, 1, 5, 2]
Sorted:   [1, 2, 2, 3, 5]
Index:     0  1  2  3  4

Median: arr[n//2] = arr[2] = 2
```

### Cost Calculation for Target Length 2
```
Stick 0: |2 - 2| = 0
Stick 1: |3 - 2| = 1
Stick 2: |1 - 2| = 1
Stick 3: |5 - 2| = 3
Stick 4: |2 - 2| = 0

Total cost: 0 + 1 + 1 + 3 + 0 = 5
```

### Visual Representation
```
Original lengths: [2, 3, 1, 5, 2]
Target length:    2

Stick 0: 2 → 2 (cost: 0)
Stick 1: 3 → 2 (cost: 1) ← shorten
Stick 2: 1 → 2 (cost: 1) ← lengthen
Stick 3: 5 → 2 (cost: 3) ← shorten
Stick 4: 2 → 2 (cost: 0)

Final lengths: [2, 2, 2, 2, 2]
Total cost: 5
```

### Why Median is Optimal
```
Key Insight: Median minimizes sum of absolute differences

Proof intuition:
- If we choose a value smaller than median:
  - More elements are above the target
  - Sum of differences increases
- If we choose a value larger than median:
  - More elements are below the target
  - Sum of differences increases
- Median balances the differences optimally
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Make all sticks the same length
- Cost is absolute difference between original and target length
- Find minimum total cost
- Need to choose optimal target length

**Key Observations:**
- This is a median problem
- Median minimizes sum of absolute differences
- Sort array to find median efficiently
- Cost is sum of absolute differences from median

### Step 2: Median Approach
**Idea**: The optimal target length is the median of the array.

```python
def stick_lengths_median(lengths):
    n = len(lengths)
    
    # Sort to find median
    lengths.sort()
    
    # Use median as target length
    target = lengths[n // 2]
    
    # Calculate total cost
    cost = 0
    for length in lengths:
        cost += abs(length - target)
    
    return cost
```

**Why this works:**
- Median minimizes sum of absolute differences
- Mathematical property: median is optimal for L1 norm
- Sort enables efficient median finding
- Simple and efficient approach

### Step 3: Optimized Solution
**Idea**: Optimize the implementation with better variable names and logic.

```python
def stick_lengths_optimized(lengths):
    n = len(lengths)
    
    # Sort to find median
    lengths.sort()
    
    # Use middle element as target (median)
    target_length = lengths[n // 2]
    
    # Calculate minimum cost
    total_cost = 0
    for stick_length in lengths:
        total_cost += abs(stick_length - target_length)
    
    return total_cost
```

**Why this is better:**
- Clearer variable names
- More readable logic
- Same optimal time complexity

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_stick_lengths():
    n = int(input())
    lengths = list(map(int, input().split()))
    
    # Sort to find median
    lengths.sort()
    
    # Use median as target length
    target_length = lengths[n // 2]
    
    # Calculate minimum cost
    total_cost = 0
    for stick_length in lengths:
        total_cost += abs(stick_length - target_length)
    
    print(total_cost)

# Main execution
if __name__ == "__main__":
    solve_stick_lengths()
```

**Why this works:**
- Optimal median approach
- Handles all edge cases
- Efficient implementation

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ([2, 3, 1, 5, 2], 5),
        ([1, 2, 3, 4, 5], 6),
        ([1, 1, 1, 1], 0),
        ([1, 2], 1),
        ([5], 0),
    ]
    
    for lengths, expected in test_cases:
        result = solve_test(lengths)
        print(f"Lengths: {lengths}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(lengths):
    n = len(lengths)
    lengths.sort()
    target_length = lengths[n // 2]
    
    total_cost = 0
    for stick_length in lengths:
        total_cost += abs(stick_length - target_length)
    
    return total_cost

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n log n) - sorting to find median
- **Space**: O(1) - constant extra space

### Why This Solution Works
- **Median Property**: Median minimizes sum of absolute differences
- **Mathematical Proof**: L1 norm is minimized at median
- **Efficient**: Single sort operation
- **Optimal**: No better solution exists

## 🎯 Key Insights

### 1. **Median Property**
- Median minimizes sum of absolute differences
- Mathematical property of L1 norm
- Works for any array of numbers
- Proven optimal solution

### 2. **Sorting Strategy**
- Sort to find median efficiently
- Middle element is median for odd n
- Average of two middle elements for even n
- O(n log n) time complexity

### 3. **Cost Calculation**
- Cost is absolute difference from target
- Sum all differences to get total cost
- Linear time calculation after sorting
- Simple arithmetic operations

## 🎯 Problem Variations

### Variation 1: Weighted Stick Lengths
**Problem**: Each stick has a weight. Minimize weighted sum of differences.

```python
def weighted_stick_lengths(lengths, weights):
    n = len(lengths)
    
    # Create pairs of (length, weight) and sort by length
    pairs = list(zip(lengths, weights))
    pairs.sort()
    
    # Find weighted median
    total_weight = sum(weights)
    cumulative_weight = 0
    target_length = pairs[0][0]
    
    for length, weight in pairs:
        cumulative_weight += weight
        if cumulative_weight >= total_weight / 2:
            target_length = length
            break
    
    # Calculate weighted cost
    total_cost = 0
    for length, weight in pairs:
        total_cost += weight * abs(length - target_length)
    
    return total_cost
```

### Variation 2: Stick Lengths with Constraints
**Problem**: Target length must be within a specific range.

```python
def constrained_stick_lengths(lengths, min_target, max_target):
    n = len(lengths)
    lengths.sort()
    
    # Find median
    median = lengths[n // 2]
    
    # Clamp median to range
    target_length = max(min_target, min(max_target, median))
    
    # Calculate cost
    total_cost = 0
    for stick_length in lengths:
        total_cost += abs(stick_length - target_length)
    
    return total_cost
```

### Variation 3: Stick Lengths with Different Costs
**Problem**: Lengthening and shortening have different costs.

```python
def asymmetric_stick_lengths(lengths, lengthen_cost, shorten_cost):
    n = len(lengths)
    lengths.sort()
    
    # Try different target lengths around median
    median = lengths[n // 2]
    min_cost = float('inf')
    
    # Check a range around median
    for target in range(median - 10, median + 11):
        cost = 0
        for stick_length in lengths:
            diff = target - stick_length
            if diff > 0:
                cost += diff * lengthen_cost
            else:
                cost += abs(diff) * shorten_cost
        min_cost = min(min_cost, cost)
    
    return min_cost
```

### Variation 4: Stick Lengths with Multiple Targets
**Problem**: Divide sticks into k groups, each with equal length.

```python
def k_groups_stick_lengths(lengths, k):
    n = len(lengths)
    lengths.sort()
    
    # Use k-means clustering approach
    # For simplicity, divide into k equal-sized groups
    group_size = n // k
    total_cost = 0
    
    for i in range(k):
        start_idx = i * group_size
        end_idx = min((i + 1) * group_size, n)
        group = lengths[start_idx:end_idx]
        
        # Find median of this group
        group_median = group[len(group) // 2]
        
        # Calculate cost for this group
        for stick_length in group:
            total_cost += abs(stick_length - group_median)
    
    return total_cost
```

### Variation 5: Dynamic Stick Lengths
**Problem**: Support adding/removing sticks dynamically.

```python
class DynamicStickLengths:
    def __init__(self):
        self.lengths = []
        self.sorted_lengths = []
    
    def add_stick(self, length):
        self.lengths.append(length)
        self.sorted_lengths.append(length)
        self.sorted_lengths.sort()
        return self.get_min_cost()
    
    def remove_stick(self, length):
        if length in self.lengths:
            self.lengths.remove(length)
            self.sorted_lengths.remove(length)
        return self.get_min_cost()
    
    def get_min_cost(self):
        if not self.sorted_lengths:
            return 0
        
        n = len(self.sorted_lengths)
        target_length = self.sorted_lengths[n // 2]
        
        total_cost = 0
        for stick_length in self.sorted_lengths:
            total_cost += abs(stick_length - target_length)
        
        return total_cost
```

## 🔗 Related Problems

- **[Array Division](/cses-analyses/problem_soulutions/sorting_and_searching/array_division_analysis)**: Optimization problems
- **[Minimum Subarray Sum](/cses-analyses/problem_soulutions/sorting_and_searching/minimum_subarray_sum_analysis)**: Sum optimization
- **[Traffic Lights](/cses-analyses/problem_soulutions/sorting_and_searching/traffic_lights_analysis)**: Optimization problems

## 📚 Learning Points

1. **Median Property**: Median minimizes sum of absolute differences
2. **Mathematical Optimization**: L1 norm optimization
3. **Sorting**: Efficient way to find median
4. **Greedy Algorithms**: Optimal local choices

---

**This is a great introduction to median properties and mathematical optimization!** 🎯 