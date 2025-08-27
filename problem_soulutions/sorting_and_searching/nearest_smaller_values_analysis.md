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