---
layout: simple
title: "Nearest Smaller Values"
permalink: /problem_soulutions/sorting_and_searching/nearest_smaller_values_analysis
---

# Nearest Smaller Values

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand nearest smaller element problems and monotonic stack techniques
- [ ] **Objective 2**: Apply monotonic stacks to efficiently find nearest smaller elements to the left
- [ ] **Objective 3**: Implement efficient nearest smaller element algorithms with O(n) time complexity
- [ ] **Objective 4**: Optimize nearest element problems using monotonic stacks and position tracking
- [ ] **Objective 5**: Handle edge cases in nearest element problems (no smaller element, all elements same, single element)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Monotonic stacks, nearest element problems, stack-based algorithms, position tracking, element comparison
- **Data Structures**: Stacks, monotonic stacks, position tracking, element tracking, comparison tracking
- **Mathematical Concepts**: Monotonic stack theory, nearest element mathematics, position analysis, element comparison
- **Programming Skills**: Stack implementation, monotonic stack implementation, position tracking, algorithm implementation
- **Related Problems**: Next Greater Element (similar concept), Monotonic stack problems, Nearest element problems

## Problem Description

**Problem**: Given an array of n integers, for each position find the nearest position to the left that has a smaller value. If there is no such position, print 0.

**Input**: 
- First line: n (size of the array)
- Second line: n integers a₁, a₂, ..., aₙ (the array)

**Output**: For each position, the nearest position to the left with a smaller value.

**Example**:
```
Input:
8
2 5 1 4 8 3 2 5

Output:
0 1 0 3 4 3 3 7

Explanation: 
Position 1 (value 2): No smaller value to the left → 0
Position 2 (value 5): Nearest smaller to left is position 1 (value 2) → 1
Position 3 (value 1): No smaller value to the left → 0
Position 4 (value 4): Nearest smaller to left is position 3 (value 1) → 3
Position 5 (value 8): Nearest smaller to left is position 4 (value 4) → 4
Position 6 (value 3): Nearest smaller to left is position 3 (value 1) → 3
Position 7 (value 2): Nearest smaller to left is position 3 (value 1) → 3
Position 8 (value 5): Nearest smaller to left is position 7 (value 2) → 7
```

## 📊 Visual Example

### Input Array
```
Array: [2, 5, 1, 4, 8, 3, 2, 5]
Index:  0  1  2  3  4  5  6  7
```

### Monotonic Stack Process
```
Step 1: Process element 2 (index 0)
┌─────────────────────────────────────┐
│ Stack: [] (empty)                   │
│ No smaller value to left → 0        │
│ Push (0, 2) to stack               │
│ Stack: [(0, 2)]                     │
└─────────────────────────────────────┘

Step 2: Process element 5 (index 1)
┌─────────────────────────────────────┐
│ Stack: [(0, 2)]                     │
│ 2 < 5, so 2 is nearest smaller      │
│ Result: position 1 (1-indexed)      │
│ Push (1, 5) to stack               │
│ Stack: [(0, 2), (1, 5)]            │
└─────────────────────────────────────┘

Step 3: Process element 1 (index 2)
┌─────────────────────────────────────┐
│ Stack: [(0, 2), (1, 5)]            │
│ 5 ≥ 1, remove (1, 5)               │
│ 2 ≥ 1, remove (0, 2)               │
│ Stack: [] (empty)                   │
│ No smaller value to left → 0        │
│ Push (2, 1) to stack               │
│ Stack: [(2, 1)]                     │
└─────────────────────────────────────┘

Step 4: Process element 4 (index 3)
┌─────────────────────────────────────┐
│ Stack: [(2, 1)]                     │
│ 1 < 4, so 1 is nearest smaller      │
│ Result: position 3 (1-indexed)      │
│ Push (3, 4) to stack               │
│ Stack: [(2, 1), (3, 4)]            │
└─────────────────────────────────────┘

Step 5: Process element 8 (index 4)
┌─────────────────────────────────────┐
│ Stack: [(2, 1), (3, 4)]            │
│ 4 < 8, so 4 is nearest smaller      │
│ Result: position 4 (1-indexed)      │
│ Push (4, 8) to stack               │
│ Stack: [(2, 1), (3, 4), (4, 8)]    │
└─────────────────────────────────────┘

Step 6: Process element 3 (index 5)
┌─────────────────────────────────────┐
│ Stack: [(2, 1), (3, 4), (4, 8)]    │
│ 8 ≥ 3, remove (4, 8)               │
│ 4 ≥ 3, remove (3, 4)               │
│ 1 < 3, so 1 is nearest smaller      │
│ Result: position 3 (1-indexed)      │
│ Push (5, 3) to stack               │
│ Stack: [(2, 1), (5, 3)]            │
└─────────────────────────────────────┘

Step 7: Process element 2 (index 6)
┌─────────────────────────────────────┐
│ Stack: [(2, 1), (5, 3)]            │
│ 3 ≥ 2, remove (5, 3)               │
│ 1 < 2, so 1 is nearest smaller      │
│ Result: position 3 (1-indexed)      │
│ Push (6, 2) to stack               │
│ Stack: [(2, 1), (6, 2)]            │
└─────────────────────────────────────┘

Step 8: Process element 5 (index 7)
┌─────────────────────────────────────┐
│ Stack: [(2, 1), (6, 2)]            │
│ 2 < 5, so 2 is nearest smaller      │
│ Result: position 7 (1-indexed)      │
│ Push (7, 5) to stack               │
│ Stack: [(2, 1), (6, 2), (7, 5)]    │
└─────────────────────────────────────┘
```

### Final Results
```
Position 1: 0
Position 2: 1
Position 3: 0
Position 4: 3
Position 5: 4
Position 6: 3
Position 7: 3
Position 8: 7
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- For each position, find the nearest smaller value to the left
- Return the position (1-indexed) of that smaller value
- If no smaller value exists, return 0

**Key Observations:**
- Need to maintain a monotonic stack (decreasing order)
- For each element, remove all larger/equal elements from stack
- Top of stack after removal is the nearest smaller value
- Stack stores (value, index) pairs

### Step 2: Brute Force Approach
**Idea**: For each position, scan left to find the nearest smaller value.

```python
def nearest_smaller_values_brute_force(n, arr):
    result = [0] * n
    
    for i in range(n):
        for j in range(i - 1, -1, -1):
            if arr[j] < arr[i]:
                result[i] = j + 1  # 1-indexed
                break
    
    return result
```

**Why this works:**
- Checks all previous positions for each element
- Simple to understand and implement
- Guarantees correct answer
- O(n²) time complexity

### Step 3: Monotonic Stack Optimization
**Idea**: Use a monotonic stack to efficiently find the nearest smaller value.

```python
def nearest_smaller_values_monotonic_stack(n, arr):
    result = [0] * n
    stack = []  # Stack of (value, index) pairs
    
    for i in range(n):
        # Remove elements from stack that are greater than or equal to current element
        while stack and stack[-1][0] >= arr[i]:
            stack.pop()
        
        # The top of stack is the nearest smaller value
        if stack:
            result[i] = stack[-1][1] + 1  # 1-indexed
        else:
            result[i] = 0
        
        # Push current element
        stack.append((arr[i], i))
    
    return result
```

**Why this is better:**
- O(n) time complexity
- Uses monotonic stack optimization
- Much more efficient
- Handles large constraints

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_nearest_smaller_values():
    n = int(input())
    arr = list(map(int, input().split()))
    
    result = [0] * n
    stack = []  # Stack of (value, index) pairs
    
    for i in range(n):
        # Remove elements from stack that are greater than or equal to current element
        while stack and stack[-1][0] >= arr[i]:
            stack.pop()
        
        # The top of stack is the nearest smaller value
        if stack:
            result[i] = stack[-1][1] + 1  # 1-indexed
        else:
            result[i] = 0
        
        # Push current element
        stack.append((arr[i], i))
    
    print(*result)

# Main execution
if __name__ == "__main__":
    solve_nearest_smaller_values()
```

**Why this works:**
- Optimal monotonic stack approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (8, [2, 5, 1, 4, 8, 3, 2, 5], [0, 1, 0, 3, 4, 3, 3, 7]),
        (5, [1, 2, 3, 4, 5], [0, 1, 2, 3, 4]),
        (5, [5, 4, 3, 2, 1], [0, 0, 0, 0, 0]),
        (3, [1, 1, 1], [0, 0, 0]),
    ]
    
    for n, arr, expected in test_cases:
        result = solve_test(n, arr)
        print(f"n={n}, arr={arr}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n, arr):
    result = [0] * n
    stack = []
    
    for i in range(n):
        while stack and stack[-1][0] >= arr[i]:
            stack.pop()
        
        if stack:
            result[i] = stack[-1][1] + 1
        else:
            result[i] = 0
        
        stack.append((arr[i], i))
    
    return result

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - each element pushed/popped at most once
- **Space**: O(n) - stack can contain all elements

### Why This Solution Works
- **Monotonic Stack**: Maintains decreasing order of values
- **Efficient Removal**: Remove all larger/equal elements for each new element
- **Nearest Smaller**: Top of stack after removal is the answer
- **Optimal Approach**: Each element processed at most twice

## 🎯 Key Insights

### 1. **Monotonic Stack**
- Maintains decreasing order of values
- Efficiently finds nearest smaller value
- Each element processed at most twice
- Key insight for optimization

### 2. **Stack Operations**
- Remove all larger/equal elements for each new element
- Push current element onto stack
- Top of stack is the answer
- Crucial for understanding

### 3. **Amortized Analysis**
- Each element pushed once
- Each element popped at most once
- Total operations: O(n)
- Important for complexity analysis

## 🎯 Problem Variations

### Variation 1: Nearest Greater Values
**Problem**: Find the nearest greater value to the left.

```python
def nearest_greater_values(n, arr):
    result = [0] * n
    stack = []  # Stack of (value, index) pairs
    
    for i in range(n):
        # Remove elements from stack that are less than or equal to current element
        while stack and stack[-1][0] <= arr[i]:
            stack.pop()
        
        # The top of stack is the nearest greater value
        if stack:
            result[i] = stack[-1][1] + 1  # 1-indexed
        else:
            result[i] = 0
        
        # Push current element
        stack.append((arr[i], i))
    
    return result
```

### Variation 2: Nearest Smaller Values to Right
**Problem**: Find the nearest smaller value to the right.

```python
def nearest_smaller_values_right(n, arr):
    result = [0] * n
    stack = []  # Stack of (value, index) pairs
    
    # Process from right to left
    for i in range(n - 1, -1, -1):
        # Remove elements from stack that are greater than or equal to current element
        while stack and stack[-1][0] >= arr[i]:
            stack.pop()
        
        # The top of stack is the nearest smaller value to the right
        if stack:
            result[i] = stack[-1][1] + 1  # 1-indexed
        else:
            result[i] = 0
        
        # Push current element
        stack.append((arr[i], i))
    
    return result
```

### Variation 3: Nearest Smaller Values with Distance
**Problem**: Find the nearest smaller value and its distance.

```python
def nearest_smaller_values_with_distance(n, arr):
    result = [(0, 0)] * n  # (position, distance)
    stack = []  # Stack of (value, index) pairs
    
    for i in range(n):
        # Remove elements from stack that are greater than or equal to current element
        while stack and stack[-1][0] >= arr[i]:
            stack.pop()
        
        # The top of stack is the nearest smaller value
        if stack:
            position = stack[-1][1] + 1  # 1-indexed
            distance = i - stack[-1][1]
            result[i] = (position, distance)
        else:
            result[i] = (0, 0)
        
        # Push current element
        stack.append((arr[i], i))
    
    return result
```

### Variation 4: Nearest Smaller Values in 2D
**Problem**: Find nearest smaller values in a 2D array for each row.

```python
def nearest_smaller_values_2d(n, m, matrix):
    result = [[0] * m for _ in range(n)]
    
    for row in range(n):
        stack = []
        for col in range(m):
            # Remove elements from stack that are greater than or equal to current element
            while stack and stack[-1][0] >= matrix[row][col]:
                stack.pop()
            
            # The top of stack is the nearest smaller value
            if stack:
                result[row][col] = stack[-1][1] + 1  # 1-indexed
            else:
                result[row][col] = 0
            
            # Push current element
            stack.append((matrix[row][col], col))
    
    return result
```

### Variation 5: Dynamic Nearest Smaller Values
**Problem**: Support adding elements dynamically and finding nearest smaller values.

```python
class DynamicNearestSmaller:
    def __init__(self):
        self.arr = []
        self.stack = []
        self.results = []
    
    def add_element(self, value):
        self.arr.append(value)
        i = len(self.arr) - 1
        
        # Remove elements from stack that are greater than or equal to current element
        while self.stack and self.stack[-1][0] >= value:
            self.stack.pop()
        
        # The top of stack is the nearest smaller value
        if self.stack:
            result = self.stack[-1][1] + 1  # 1-indexed
        else:
            result = 0
        
        self.results.append(result)
        self.stack.append((value, i))
        
        return result
    
    def get_results(self):
        return self.results.copy()
```

## 🔗 Related Problems

- **[Subarray Minimums](/cses-analyses/problem_soulutions/sliding_window/subarray_minimums_analysis)**: Monotonic stack applications
- **[Subarray Maximums](/cses-analyses/problem_soulutions/sliding_window/subarray_maximums_analysis)**: Monotonic stack variations
- **[Largest Rectangle in Histogram](/cses-analyses/problem_soulutions/advanced_algorithms/largest_rectangle_histogram_analysis)**: Monotonic stack problems

## 📚 Learning Points

1. **Monotonic Stack**: Powerful data structure for range queries
2. **Amortized Analysis**: Understanding why operations are efficient
3. **Stack Operations**: Efficient element removal and insertion
4. **Range Problems**: Common pattern in competitive programming

---

**This is a great introduction to monotonic stack techniques and range query problems!** 🎯 