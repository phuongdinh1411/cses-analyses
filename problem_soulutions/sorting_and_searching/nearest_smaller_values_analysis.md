---
layout: simple
title: CSES Nearest Smaller Values - Problem Analysis
permalink: /problem_soulutions/sorting_and_searching/nearest_smaller_values_analysis/
---

# CSES Nearest Smaller Values - Problem Analysis

## Problem Statement
Given an array of n integers, for each position find the nearest position to the left that has a smaller value. If there is no such position, print 0.

### Input
The first input line has an integer n: the size of the array.
The second line has n integers a1,a2,…,an: the array.

### Output
Print n integers: for each position, the nearest position to the left with a smaller value.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ ai ≤ 10^9

### Example
```
Input:
8
2 5 1 4 8 3 2 5

Output:
0 1 0 3 4 3 3 7
```

## Solution Progression

### Approach 1: Brute Force - O(n²)
**Description**: For each position, scan left to find the nearest smaller value.

```python
def nearest_smaller_values_naive(n, arr):
    result = [0] * n
    
    for i in range(n):
        for j in range(i - 1, -1, -1):
            if arr[j] < arr[i]:
                result[i] = j + 1  # 1-indexed
                break
    
    return result
```

**Why this is inefficient**: For each position, we scan all previous positions, leading to O(n²) time complexity.

### Improvement 1: Monotonic Stack - O(n)
**Description**: Use a monotonic stack to efficiently find the nearest smaller value.

```python
def nearest_smaller_values_optimized(n, arr):
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

**Why this improvement works**: We maintain a monotonic stack (decreasing order) of elements. For each new element, we remove all elements from the stack that are greater than or equal to it. The top element of the stack (if any) is the nearest smaller value.

## Final Optimal Solution

```python
n = int(input())
arr = list(map(int, input().split()))

def find_nearest_smaller_values(n, arr):
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

result = find_nearest_smaller_values(n, arr)
print(*result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(n) | Scan left for each position |
| Monotonic Stack | O(n) | O(n) | Maintain decreasing stack |

## Key Insights for Other Problems

### 1. **Nearest Element Problems**
**Principle**: Use monotonic stack to efficiently find nearest smaller/larger elements.
**Applicable to**: Nearest element problems, stack problems, range problems

### 2. **Monotonic Stack**
**Principle**: Maintain a stack with monotonic property to enable efficient queries.
**Applicable to**: Stack problems, monotonic problems, range queries

### 3. **Left-to-Right Processing**
**Principle**: Process elements from left to right while maintaining useful information in a stack.
**Applicable to**: Sequential processing, stack problems, range problems

## Notable Techniques

### 1. **Monotonic Stack Implementation**
```python
def monotonic_stack_nearest_smaller(arr):
    n = len(arr)
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
```

### 2. **Stack Management**
```python
def manage_monotonic_stack(stack, current_value, current_index):
    # Remove elements that are greater than or equal to current value
    while stack and stack[-1][0] >= current_value:
        stack.pop()
    
    # Get nearest smaller value
    if stack:
        nearest_index = stack[-1][1] + 1
    else:
        nearest_index = 0
    
    # Push current element
    stack.append((current_value, current_index))
    
    return nearest_index
```

### 3. **Nearest Element Finding**
```python
def find_nearest_elements(arr, comparison_func):
    n = len(arr)
    result = [0] * n
    stack = []
    
    for i in range(n):
        while stack and comparison_func(stack[-1][0], arr[i]):
            stack.pop()
        
        if stack:
            result[i] = stack[-1][1] + 1
        else:
            result[i] = 0
        
        stack.append((arr[i], i))
    
    return result
```

## Problem-Solving Framework

1. **Identify problem type**: This is a nearest element problem with monotonic stack
2. **Choose approach**: Use monotonic stack to maintain decreasing order
3. **Initialize stack**: Start with empty stack
4. **Process elements**: For each element, remove larger elements from stack
5. **Find nearest**: Top of stack is the nearest smaller value
6. **Update stack**: Push current element onto stack
7. **Return result**: Output nearest smaller positions

---

*This analysis shows how to efficiently find nearest smaller values using monotonic stack technique.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Nearest Larger Values**
**Problem**: Find the nearest position to the left that has a larger value.
```python
def nearest_larger_values(n, arr):
    result = [0] * n
    stack = []  # Stack of (value, index) pairs
    
    for i in range(n):
        # Remove elements from stack that are smaller than or equal to current element
        while stack and stack[-1][0] <= arr[i]:
            stack.pop()
        
        # The top of stack is the nearest larger value
        if stack:
            result[i] = stack[-1][1] + 1  # 1-indexed
        else:
            result[i] = 0
        
        # Push current element
        stack.append((arr[i], i))
    
    return result
```

#### **Variation 2: Nearest Smaller Values in Both Directions**
**Problem**: Find nearest smaller values to both left and right.
```python
def nearest_smaller_both_directions(n, arr):
    left_result = [0] * n
    right_result = [0] * n
    
    # Find nearest smaller to the left
    stack = []
    for i in range(n):
        while stack and stack[-1][0] >= arr[i]:
            stack.pop()
        
        if stack:
            left_result[i] = stack[-1][1] + 1
        else:
            left_result[i] = 0
        
        stack.append((arr[i], i))
    
    # Find nearest smaller to the right
    stack = []
    for i in range(n-1, -1, -1):
        while stack and stack[-1][0] >= arr[i]:
            stack.pop()
        
        if stack:
            right_result[i] = stack[-1][1] + 1
        else:
            right_result[i] = 0
        
        stack.append((arr[i], i))
    
    return left_result, right_result
```

#### **Variation 3: Nearest Smaller Values with Distance**
**Problem**: Find the nearest smaller value and its distance.
```python
def nearest_smaller_with_distance(n, arr):
    result = [(0, 0)] * n  # (position, distance)
    stack = []  # Stack of (value, index) pairs
    
    for i in range(n):
        while stack and stack[-1][0] >= arr[i]:
            stack.pop()
        
        if stack:
            position = stack[-1][1] + 1
            distance = i - stack[-1][1]
            result[i] = (position, distance)
        else:
            result[i] = (0, 0)
        
        stack.append((arr[i], i))
    
    return result
```

#### **Variation 4: Nearest Smaller Values with Constraints**
**Problem**: Find nearest smaller value within a maximum distance D.
```python
def nearest_smaller_with_distance_constraint(n, arr, max_distance):
    result = [0] * n
    stack = []  # Stack of (value, index) pairs
    
    for i in range(n):
        # Remove elements that are too far or greater than current
        while stack and (i - stack[-1][1] > max_distance or stack[-1][0] >= arr[i]):
            stack.pop()
        
        if stack:
            result[i] = stack[-1][1] + 1
        else:
            result[i] = 0
        
        stack.append((arr[i], i))
    
    return result
```

#### **Variation 5: Nearest Smaller Values with Dynamic Updates**
**Problem**: Support adding and removing elements dynamically.
```python
class DynamicNearestSmaller:
    def __init__(self):
        self.arr = []
        self.stack = []
        self.result = []
    
    def add_element(self, value):
        self.arr.append(value)
        i = len(self.arr) - 1
        
        # Update stack
        while self.stack and self.stack[-1][0] >= value:
            self.stack.pop()
        
        if self.stack:
            self.result.append(self.stack[-1][1] + 1)
        else:
            self.result.append(0)
        
        self.stack.append((value, i))
        return self.result[-1]
    
    def remove_element(self, index):
        if 0 <= index < len(self.arr):
            # Remove from array
            self.arr.pop(index)
            
            # Rebuild stack and result
            self.stack = []
            self.result = []
            
            for i, value in enumerate(self.arr):
                while self.stack and self.stack[-1][0] >= value:
                    self.stack.pop()
                
                if self.stack:
                    self.result.append(self.stack[-1][1] + 1)
                else:
                    self.result.append(0)
                
                self.stack.append((value, i))
        
        return self.result
```

### 🔗 **Related Problems & Concepts**

#### **1. Monotonic Stack Problems**
- **Largest Rectangle in Histogram**: Find largest rectangle in histogram
- **Trapping Rain Water**: Calculate trapped water
- **Next Greater Element**: Find next greater element
- **Previous Greater Element**: Find previous greater element

#### **2. Range Query Problems**
- **Range Minimum Queries**: Find minimum in range
- **Range Maximum Queries**: Find maximum in range
- **Sparse Table**: Data structure for range queries
- **Segment Tree**: Dynamic range queries

#### **3. Array Processing Problems**
- **Array Manipulation**: Efficient array operations
- **Array Partitioning**: Partition array based on conditions
- **Array Merging**: Merge sorted arrays
- **Array Sorting**: Sort array efficiently

#### **4. Stack Problems**
- **Stack Implementation**: Custom stack design
- **Stack Applications**: Various stack applications
- **Expression Evaluation**: Evaluate expressions using stack
- **Parentheses Matching**: Match parentheses using stack

#### **5. Optimization Problems**
- **Linear Programming**: Formulate as LP problem
- **Dynamic Programming**: Optimal substructure
- **Greedy Algorithms**: Local optimal choices
- **Approximation Algorithms**: Find approximate solutions

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n = int(input())
    arr = list(map(int, input().split()))
    
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
    
    print(*result)
```

#### **2. Range Queries**
```python
# Precompute nearest smaller values for different subarrays
def precompute_nearest_smaller(arr):
    n = len(arr)
    nearest_matrix = [[0] * n for _ in range(n)]
    
    for start in range(n):
        stack = []
        for end in range(start, n):
            while stack and stack[-1][0] >= arr[end]:
                stack.pop()
            
            if stack:
                nearest_matrix[start][end] = stack[-1][1] - start + 1
            else:
                nearest_matrix[start][end] = 0
            
            stack.append((arr[end], end - start))
    
    return nearest_matrix

# Answer queries about nearest smaller values in subarrays
def nearest_query(nearest_matrix, start, end):
    return nearest_matrix[start][end]
```

#### **3. Interactive Problems**
```python
# Interactive nearest smaller values finder
def interactive_nearest_smaller():
    n = int(input("Enter array size: "))
    arr = list(map(int, input("Enter array: ").split()))
    
    print(f"Array: {arr}")
    
    result = [0] * n
    stack = []
    
    for i in range(n):
        print(f"\nProcessing position {i+1} with value {arr[i]}")
        print(f"Current stack: {stack}")
        
        while stack and stack[-1][0] >= arr[i]:
            removed = stack.pop()
            print(f"Removed {removed} from stack")
        
        if stack:
            result[i] = stack[-1][1] + 1
            print(f"Nearest smaller: position {result[i]} with value {stack[-1][0]}")
        else:
            result[i] = 0
            print("No smaller value found")
        
        stack.append((arr[i], i))
        print(f"Added ({arr[i]}, {i}) to stack")
    
    print(f"\nFinal result: {result}")
```

### 🧮 **Mathematical Extensions**

#### **1. Monotonicity Theory**
- **Monotonic Functions**: Properties of monotonic functions
- **Monotonic Sequences**: Properties of monotonic sequences
- **Monotonic Stack Properties**: Properties of monotonic stacks
- **Monotonicity Applications**: Applications of monotonicity

#### **2. Algorithm Analysis**
- **Complexity Analysis**: Time and space complexity
- **Amortized Analysis**: Average case analysis
- **Probabilistic Analysis**: Expected performance
- **Worst Case Analysis**: Upper bounds

#### **3. Data Structure Analysis**
- **Stack Analysis**: Analysis of stack operations
- **Monotonic Stack Analysis**: Analysis of monotonic stacks
- **Range Query Analysis**: Analysis of range queries
- **Dynamic Data Structure Analysis**: Analysis of dynamic structures

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Monotonic Stack**: Efficient stack-based algorithms
- **Range Query Algorithms**: Efficient range query algorithms
- **Stack Algorithms**: Various stack-based algorithms
- **Array Processing**: Efficient array operations

#### **2. Mathematical Concepts**
- **Monotonicity**: Properties of monotonic functions
- **Algorithm Analysis**: Complexity and correctness
- **Data Structure Theory**: Theory of data structures
- **Discrete Mathematics**: Discrete structures

#### **3. Programming Concepts**
- **Stack Implementation**: Efficient stack operations
- **Array Manipulation**: Efficient array operations
- **Algorithm Design**: Problem-solving strategies
- **Data Structure Design**: Efficient data structure design

---

*This analysis demonstrates monotonic stack techniques and shows various extensions for range query problems.* 