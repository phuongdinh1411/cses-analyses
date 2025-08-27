# CSES Increasing Array - Problem Analysis

## Problem Statement
You are given an array of n integers. You want to modify the array so that it is increasing, i.e., every element is at least as large as the previous element.

On each move, you may increase the value of any element by one. What is the minimum number of moves required?

### Input
The first input line contains an integer n: the size of the array.
The second line contains n integers x1,x2,…,xn: the contents of the array.

### Output
Print one integer: the minimum number of moves.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ xi ≤ 10^9

### Example
```
Input:
5
3 2 5 1 7

Output:
5
```

## Solution Progression

### Approach 1: Brute Force - O(n!)
**Description**: Try all possible ways to modify the array and find the minimum moves.

```python
def increasing_array_brute_force(arr):
    n = len(arr)
    min_moves = float('inf')
    
    def try_modifications(index, current_arr, moves):
        nonlocal min_moves
        
        if index == n:
            # Check if array is increasing
            is_increasing = True
            for i in range(1, n):
                if current_arr[i] < current_arr[i-1]:
                    is_increasing = False
                    break
            
            if is_increasing:
                min_moves = min(min_moves, moves)
            return
        
        # Try different modifications for current element
        for increase in range(100):  # Arbitrary limit
            current_arr[index] += increase
            try_modifications(index + 1, current_arr, moves + increase)
            current_arr[index] -= increase
    
    try_modifications(0, arr.copy(), 0)
    return min_moves
```

**Why this is inefficient**: We're trying all possible modifications for each element, which leads to factorial complexity. This is completely impractical for large inputs.

### Improvement 1: Greedy Approach - O(n)
**Description**: Process the array from left to right and ensure each element is at least as large as the previous one.

```python
def increasing_array_greedy(arr):
    n = len(arr)
    moves = 0
    
    for i in range(1, n):
        if arr[i] < arr[i-1]:
            # Need to increase current element
            moves += arr[i-1] - arr[i]
            arr[i] = arr[i-1]
    
    return moves
```

**Why this improvement works**: We process the array from left to right. For each element, if it's smaller than the previous element, we increase it to match the previous element. This ensures the array becomes increasing with minimum moves.

### Alternative: Using List Comprehension - O(n)
**Description**: Use a more concise approach with list comprehension.

```python
def increasing_array_concise(arr):
    moves = 0
    for i in range(1, len(arr)):
        if arr[i] < arr[i-1]:
            moves += arr[i-1] - arr[i]
            arr[i] = arr[i-1]
    return moves
```

**Why this works**: Same logic as the greedy approach but more concise. We only need to track the total moves and update the array in place.

### Alternative: Functional Approach - O(n)
**Description**: Use a functional approach to solve the problem.

```python
def increasing_array_functional(arr):
    def process_pair(prev, curr):
        if curr < prev:
            return prev, prev - curr
        else:
            return curr, 0
    
    moves = 0
    for i in range(1, len(arr)):
        arr[i], additional_moves = process_pair(arr[i-1], arr[i])
        moves += additional_moves
    
    return moves
```

**Why this works**: We use a helper function to process each pair of consecutive elements and calculate the required moves.

## Final Optimal Solution

```python
n = int(input())
arr = list(map(int, input().split()))

moves = 0
for i in range(1, n):
    if arr[i] < arr[i-1]:
        moves += arr[i-1] - arr[i]
        arr[i] = arr[i-1]

print(moves)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n!) | O(n) | Try all modifications |
| Greedy | O(n) | O(1) | Process from left to right |
| Concise | O(n) | O(1) | Same as greedy but concise |
| Functional | O(n) | O(1) | Use helper function |

## Key Insights for Other Problems

### 1. **Greedy Array Processing**
**Principle**: Process arrays from left to right and make local optimal decisions.
**Applicable to**:
- Array modification problems
- Greedy algorithms
- Optimization problems
- Sequential processing

**Example Problems**:
- Increasing array
- Array modification
- Greedy optimization
- Sequential problems

### 2. **Local Optimization**
**Principle**: Make the best decision at each step to achieve global optimality.
**Applicable to**:
- Greedy algorithms
- Optimization problems
- Decision problems
- Algorithm design

**Example Problems**:
- Activity selection
- Huffman coding
- Dijkstra's algorithm
- Greedy optimization

### 3. **Array Traversal Patterns**
**Principle**: Use systematic traversal patterns to process arrays efficiently.
**Applicable to**:
- Array processing
- Sequential algorithms
- Pattern recognition
- Data processing

**Example Problems**:
- Array traversal
- Sequential processing
- Pattern matching
- Data analysis

### 4. **In-Place Modification**
**Principle**: Modify arrays in place to save space and improve efficiency.
**Applicable to**:
- Array manipulation
- Space optimization
- In-place algorithms
- Memory efficiency

**Example Problems**:
- In-place sorting
- Array modification
- Space optimization
- Memory efficient algorithms

## Notable Techniques

### 1. **Greedy Array Processing Pattern**
```python
# Process array from left to right
for i in range(1, n):
    if arr[i] < arr[i-1]:
        # Make local optimal decision
        moves += arr[i-1] - arr[i]
        arr[i] = arr[i-1]
```

### 2. **In-Place Modification Pattern**
```python
# Modify array in place
for i in range(n):
    if condition:
        arr[i] = new_value
```

### 3. **Functional Processing Pattern**
```python
# Use helper function for processing
def process_element(prev, curr):
    if curr < prev:
        return prev, prev - curr
    return curr, 0
```

## Edge Cases to Remember

1. **Single element**: No moves needed
2. **Already increasing**: No moves needed
3. **All same elements**: No moves needed
4. **Large numbers**: Handle integer overflow
5. **Empty array**: Handle edge case

## Problem-Solving Framework

1. **Identify optimization nature**: This is about minimizing moves to make array increasing
2. **Consider greedy approach**: Process from left to right
3. **Make local decisions**: Ensure each element is at least as large as previous
4. **Handle edge cases**: Consider special input patterns
5. **Optimize for efficiency**: Use single pass approach

---

*This analysis shows how to efficiently make an array increasing using a greedy approach.* 