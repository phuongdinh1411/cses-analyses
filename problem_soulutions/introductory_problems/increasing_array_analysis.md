---
layout: simple
title: "Increasing Array"
permalink: /problem_soulutions/introductory_problems/increasing_array_analysis
---

# Increasing Array

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand array manipulation and greedy optimization problems
- [ ] **Objective 2**: Apply greedy algorithms to minimize operations for array transformation
- [ ] **Objective 3**: Implement efficient array manipulation algorithms with proper operation counting
- [ ] **Objective 4**: Optimize array transformation using greedy strategies and mathematical analysis
- [ ] **Objective 5**: Handle edge cases in array manipulation (large arrays, edge values, operation overflow)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Greedy algorithms, array manipulation, optimization problems, operation counting
- **Data Structures**: Arrays, operation tracking, value tracking, array processing
- **Mathematical Concepts**: Optimization theory, greedy strategies, operation analysis, array mathematics
- **Programming Skills**: Array manipulation, operation counting, greedy implementation, algorithm implementation
- **Related Problems**: Array problems, Greedy algorithms, Optimization problems, Array manipulation

## Problem Description

**Problem**: You are given an array of n integers. You want to modify the array so that it becomes strictly increasing. In one operation, you can increase any element by 1. Find the minimum number of operations needed.

**Input**: 
- First line: n (1 ≤ n ≤ 2×10⁵)
- Second line: n integers a₁, a₂, ..., aₙ (1 ≤ aᵢ ≤ 10⁹)

**Output**: The minimum number of operations needed.

**Example**:
```
Input:
5
3 2 5 1 7

Output:
5

Explanation: 
3 2 5 1 7 → 3 3 5 1 7 → 3 3 5 2 7 → 3 3 5 3 7 → 3 3 5 4 7 → 3 3 5 5 7
Operations: 1 + 1 + 1 + 1 + 1 = 5
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Start with an array that may not be increasing
- We can only increase elements (not decrease)
- Goal: make array strictly increasing (a[i] < a[i+1] for all i)
- Find minimum operations needed

**Key Observations:**
- We can only increase elements, never decrease
- Each element must be greater than the previous one
- We need to find the minimum increases needed

### Step 2: Greedy Approach
**Idea**: Process the array from left to right, ensuring each element is greater than the previous.

```python
def solve_greedy(arr):
    operations = 0
    
    for i in range(1, len(arr)):
        if arr[i] <= arr[i-1]:
            # Need to increase current element
            needed = arr[i-1] - arr[i] + 1
            operations += needed
            arr[i] += needed
    
    return operations
```

**Why this works:**
- We process from left to right
- Each element must be greater than the previous
- We calculate exactly how much to increase each element

### Step 3: Optimized Solution
**Idea**: Calculate operations without modifying the original array.

```python
def solve_optimized(arr):
    operations = 0
    prev = arr[0]
    
    for i in range(1, len(arr)):
        if arr[i] <= prev:
            # Need to increase current element
            needed = prev - arr[i] + 1
            operations += needed
            prev = arr[i] + needed
        else:
            prev = arr[i]
    
    return operations
```

**Why this is better:**
- Doesn't modify the original array
- More memory efficient
- Clearer logic flow

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_increasing_array():
    n = int(input())
    arr = list(map(int, input().split()))
    
    operations = 0
    prev = arr[0]
    
    for i in range(1, n):
        if arr[i] <= prev:
            needed = prev - arr[i] + 1
            operations += needed
            prev = arr[i] + needed
        else:
            prev = arr[i]
    
    return operations

# Main execution
if __name__ == "__main__":
    result = solve_increasing_array()
    print(result)
```

**Why this works:**
- Processes array in one pass
- Calculates minimum operations needed
- Handles all edge cases correctly

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ([3, 2, 5, 1, 7], 5),
        ([1, 1, 1, 1, 1], 4),
        ([1, 2, 3, 4, 5], 0),
        ([5, 4, 3, 2, 1], 10),
    ]
    
    for arr, expected in test_cases:
        result = solve_test(arr)
        print(f"Array: {arr}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(arr):
    operations = 0
    prev = arr[0]
    
    for i in range(1, len(arr)):
        if arr[i] <= prev:
            needed = prev - arr[i] + 1
            operations += needed
            prev = arr[i] + needed
        else:
            prev = arr[i]
    
    return operations

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Single Pass**: O(n) - we process each element once
- **Space**: O(1) - we only use a few variables

### Why This Solution Works
- **Greedy**: Always make the minimum change needed
- **Optimal**: No better solution exists
- **Complete**: Handles all possible cases

## 🎨 Visual Example

### Input Example
```
Array: [3, 2, 5, 1, 7]
Output: 5 operations
```

### Array Transformation Process
```
Initial array: [3, 2, 5, 1, 7]

Step 1: Check a[1] vs a[0]
- a[0] = 3, a[1] = 2
- 2 < 3, need to increase a[1]
- Increase a[1] by 1: 2 → 3
- Array: [3, 3, 5, 1, 7]
- Operations: 1

Step 2: Check a[2] vs a[1]
- a[1] = 3, a[2] = 5
- 5 > 3 ✓ (already increasing)
- No change needed
- Array: [3, 3, 5, 1, 7]
- Operations: 1

Step 3: Check a[3] vs a[2]
- a[2] = 5, a[3] = 1
- 1 < 5, need to increase a[3]
- Increase a[3] by 4: 1 → 5
- Array: [3, 3, 5, 5, 7]
- Operations: 1 + 4 = 5

Step 4: Check a[4] vs a[3]
- a[3] = 5, a[4] = 7
- 7 > 5 ✓ (already increasing)
- No change needed
- Array: [3, 3, 5, 5, 7]
- Operations: 5

Final array: [3, 3, 5, 5, 7] (strictly increasing)
Total operations: 5
```

### Greedy Strategy Visualization
```
Process from left to right, ensuring each element > previous:

Position: 0  1  2  3  4
Initial:  3  2  5  1  7
Step 1:   3  3  5  1  7  (increase a[1] by 1)
Step 2:   3  3  5  1  7  (no change needed)
Step 3:   3  3  5  5  7  (increase a[3] by 4)
Step 4:   3  3  5  5  7  (no change needed)

Each step makes minimum necessary changes.
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Greedy          │ O(n)         │ O(1)         │ Process      │
│                 │              │              │ left to right│
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Brute Force     │ O(n²)        │ O(n)         │ Try all      │
│                 │              │              │ combinations │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ DP              │ O(n)         │ O(n)         │ Track        │
│                 │              │              │ optimal      │
│                 │              │              │ changes      │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Greedy Strategy**
- Process from left to right
- Make minimum changes needed at each step
- This gives the optimal solution

### 2. **Strictly Increasing**
- Each element must be greater than the previous
- Not just greater than or equal to

### 3. **Only Increases Allowed**
- We can only increase elements
- This constraint makes the problem simpler

## 🔗 Related Problems

- **[Two Sets](/cses-analyses/problem_soulutions/introductory_problems/two_sets_analysis)**: Array manipulation
- **[Missing Number](/cses-analyses/problem_soulutions/introductory_problems/missing_number_analysis)**: Array problems
- **[Repetitions](/cses-analyses/problem_soulutions/introductory_problems/repetitions_analysis)**: Pattern problems

## 🎯 Problem Variations

### Variation 1: Decreasing Array
**Problem**: Make array decreasing (each element at most as large as previous).

```python
def decreasing_array(arr):
    operations = 0
    prev = arr[0]
    
    for i in range(1, len(arr)):
        if arr[i] >= prev:
            needed = arr[i] - prev + 1
            operations += needed
            prev = arr[i] - needed
        else:
            prev = arr[i]
    
    return operations
```

### Variation 2: Minimum Cost Operations
**Problem**: Each operation has different cost. Find minimum total cost.

```python
def minimum_cost_increasing(arr, costs):
    # costs[i] = cost to increase element at position i by 1
    total_cost = 0
    prev = arr[0]
    
    for i in range(1, len(arr)):
        if arr[i] <= prev:
            needed = prev - arr[i] + 1
            total_cost += needed * costs[i]
            prev = arr[i] + needed
        else:
            prev = arr[i]
    
    return total_cost
```

### Variation 3: Limited Operations
**Problem**: You can perform at most k operations. Can you make array increasing?

```python
def limited_operations_increasing(arr, k):
    operations_needed = 0
    prev = arr[0]
    
    for i in range(1, len(arr)):
        if arr[i] <= prev:
            needed = prev - arr[i] + 1
            operations_needed += needed
            if operations_needed > k:
                return False
            prev = arr[i] + needed
        else:
            prev = arr[i]
    
    return operations_needed <= k
```

### Variation 4: Non-Decreasing Subsequence
**Problem**: Find longest non-decreasing subsequence (don't modify array).

```python
def longest_non_decreasing_subsequence(arr):
    n = len(arr)
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] >= arr[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)
```

## 📚 Learning Points

1. **Greedy Algorithms**: Making optimal choices at each step
2. **Array Processing**: Efficient single-pass solutions
3. **Problem Constraints**: Understanding what operations are allowed
4. **Mathematical Thinking**: Calculating exact values needed

---

**This is a great introduction to greedy algorithms and array manipulation!** 🎯 