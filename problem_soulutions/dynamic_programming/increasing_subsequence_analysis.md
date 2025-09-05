---
layout: simple
title: "Increasing Subsequence"
permalink: /problem_soulutions/dynamic_programming/increasing_subsequence_analysis
---


# Increasing Subsequence

## Problem Description

**Problem**: Given an array of n integers, find the length of the longest increasing subsequence (LIS). A subsequence is a sequence that can be derived from the array by deleting some elements without changing the order of the remaining elements.

**Input**: 
- n: size of the array
- a1, a2, ..., an: the array elements

**Output**: Length of the longest increasing subsequence.

**Example**:
```
Input:
8
7 3 5 3 6 2 9 8

Output:
4

Explanation: 
The longest increasing subsequence is [3, 5, 6, 9] with length 4.
Other valid LIS include [3, 5, 6, 8] and [3, 3, 6, 9].
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find the longest subsequence where elements are strictly increasing
- Elements must appear in the same order as in the original array
- We can skip elements but cannot reorder them
- Use dynamic programming for efficiency

**Key Observations:**
- For each position, we can either include or skip the current element
- If we include an element, it must be greater than the previous element
- This is a classic dynamic programming problem
- Can use 1D or 2D DP approach

### Step 2: Dynamic Programming Approach
**Idea**: Use 1D DP array to store LIS ending at each position.

```python
def increasing_subsequence_dp(n, arr):
    # dp[i] = length of LIS ending at position i
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)
```

**Why this works:**
- Uses optimal substructure property
- Handles all cases correctly
- Efficient implementation
- O(n²) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_increasing_subsequence():
    n = int(input())
    arr = list(map(int, input().split()))
    
    # dp[i] = length of LIS ending at position i
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    print(max(dp))

# Main execution
if __name__ == "__main__":
    solve_increasing_subsequence()
```

**Why this works:**
- Optimal dynamic programming approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ([7, 3, 5, 3, 6, 2, 9, 8], 4),
        ([1, 2, 3, 4, 5], 5),
        ([5, 4, 3, 2, 1], 1),
        ([1], 1),
        ([1, 1, 1, 1], 1),
    ]
    
    for arr, expected in test_cases:
        result = solve_test(arr)
        print(f"arr={arr}, expected={expected}, result={result}")
        assert result == expected, f"Failed for arr={arr}"
        print("✓ Passed")
        print()

def solve_test(arr):
    n = len(arr)
    
    # dp[i] = length of LIS ending at position i
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n²) - we iterate through each position and check all previous positions
- **Space**: O(n) - we store dp array of size n

### Why This Solution Works
- **Dynamic Programming**: Efficiently computes LIS using optimal substructure
- **State Transition**: dp[i] = max(dp[j] + 1) for all j < i where arr[i] > arr[j]
- **Base Case**: dp[i] = 1 for all i (each element forms a LIS of length 1)
- **Optimal Substructure**: LIS ending at position i can be built from smaller subproblems

## 🎨 Visual Example

### Input Example
```
Array: [7, 3, 5, 3, 6, 2, 9, 8]
```

### All Possible Increasing Subsequences
```
Array: [7, 3, 5, 3, 6, 2, 9, 8]
Index:  0  1  2  3  4  5  6  7

All increasing subsequences:
1. [7] (length 1)
2. [3] (length 1)
3. [5] (length 1)
4. [3] (length 1)
5. [6] (length 1)
6. [2] (length 1)
7. [9] (length 1)
8. [8] (length 1)
9. [3, 5] (length 2)
10. [3, 6] (length 2)
11. [3, 9] (length 2)
12. [3, 8] (length 2)
13. [5, 6] (length 2)
14. [5, 9] (length 2)
15. [5, 8] (length 2)
16. [3, 6] (length 2)
17. [3, 9] (length 2)
18. [3, 8] (length 2)
19. [6, 9] (length 2)
20. [6, 8] (length 2)
21. [2, 9] (length 2)
22. [2, 8] (length 2)
23. [3, 5, 6] (length 3)
24. [3, 5, 9] (length 3)
25. [3, 5, 8] (length 3)
26. [3, 6, 9] (length 3)
27. [3, 6, 8] (length 3)
28. [5, 6, 9] (length 3)
29. [5, 6, 8] (length 3)
30. [2, 9, 8] (length 3) - Invalid (9 > 8)
31. [3, 5, 6, 9] (length 4)
32. [3, 5, 6, 8] (length 4)
33. [3, 6, 9, 8] (length 4) - Invalid (9 > 8)

Longest increasing subsequence: [3, 5, 6, 9] or [3, 5, 6, 8] (length 4)
```

### DP State Representation
```
dp[i] = length of longest increasing subsequence ending at position i

For array [7, 3, 5, 3, 6, 2, 9, 8]:

Base case: dp[i] = 1 for all i (each element forms a LIS of length 1)

dp[0] = 1 (LIS ending at position 0: [7])

dp[1] = 1 (LIS ending at position 1: [3])
- Cannot extend [7] because 3 < 7

dp[2] = 2 (LIS ending at position 2: [3, 5])
- Can extend [3] because 5 > 3
- Cannot extend [7] because 5 < 7

dp[3] = 1 (LIS ending at position 3: [3])
- Cannot extend [7] because 3 < 7
- Cannot extend [3] because 3 = 3 (not strictly increasing)
- Cannot extend [5] because 3 < 5

dp[4] = 3 (LIS ending at position 4: [3, 5, 6])
- Can extend [3, 5] because 6 > 5
- Can extend [3] because 6 > 3
- Cannot extend [7] because 6 < 7

dp[5] = 1 (LIS ending at position 5: [2])
- Cannot extend any previous LIS because 2 is smaller than all

dp[6] = 4 (LIS ending at position 6: [3, 5, 6, 9])
- Can extend [3, 5, 6] because 9 > 6
- Can extend [3, 5] because 9 > 5
- Can extend [3] because 9 > 3
- Can extend [2] because 9 > 2

dp[7] = 4 (LIS ending at position 7: [3, 5, 6, 8])
- Can extend [3, 5, 6] because 8 > 6
- Can extend [3, 5] because 8 > 5
- Can extend [3] because 8 > 3
- Can extend [2] because 8 > 2
```

### DP Table Construction
```
Array: [7, 3, 5, 3, 6, 2, 9, 8]
Index:  0  1  2  3  4  5  6  7

Step 1: Initialize base cases
dp[i] = 1 for all i

Step 2: Fill DP table
dp[0] = 1 (base case)

dp[1] = 1 (cannot extend any previous LIS)
- Check arr[0] = 7: 3 < 7, cannot extend

dp[2] = 2 (can extend dp[1])
- Check arr[0] = 7: 5 < 7, cannot extend
- Check arr[1] = 3: 5 > 3, can extend dp[1] = 1 + 1 = 2

dp[3] = 1 (cannot extend any previous LIS)
- Check arr[0] = 7: 3 < 7, cannot extend
- Check arr[1] = 3: 3 = 3, cannot extend (not strictly increasing)
- Check arr[2] = 5: 3 < 5, cannot extend

dp[4] = 3 (can extend dp[2])
- Check arr[0] = 7: 6 < 7, cannot extend
- Check arr[1] = 3: 6 > 3, can extend dp[1] = 1 + 1 = 2
- Check arr[2] = 5: 6 > 5, can extend dp[2] = 2 + 1 = 3
- Check arr[3] = 3: 6 > 3, can extend dp[3] = 1 + 1 = 2
- Maximum: 3

dp[5] = 1 (cannot extend any previous LIS)
- Check all previous elements: 2 is smaller than all

dp[6] = 4 (can extend dp[4])
- Check arr[0] = 7: 9 > 7, can extend dp[0] = 1 + 1 = 2
- Check arr[1] = 3: 9 > 3, can extend dp[1] = 1 + 1 = 2
- Check arr[2] = 5: 9 > 5, can extend dp[2] = 2 + 1 = 3
- Check arr[3] = 3: 9 > 3, can extend dp[3] = 1 + 1 = 2
- Check arr[4] = 6: 9 > 6, can extend dp[4] = 3 + 1 = 4
- Check arr[5] = 2: 9 > 2, can extend dp[5] = 1 + 1 = 2
- Maximum: 4

dp[7] = 4 (can extend dp[4])
- Check arr[0] = 7: 8 > 7, can extend dp[0] = 1 + 1 = 2
- Check arr[1] = 3: 8 > 3, can extend dp[1] = 1 + 1 = 2
- Check arr[2] = 5: 8 > 5, can extend dp[2] = 2 + 1 = 3
- Check arr[3] = 3: 8 > 3, can extend dp[3] = 1 + 1 = 2
- Check arr[4] = 6: 8 > 6, can extend dp[4] = 3 + 1 = 4
- Check arr[5] = 2: 8 > 2, can extend dp[5] = 1 + 1 = 2
- Check arr[6] = 9: 8 < 9, cannot extend
- Maximum: 4

Final result: max(dp) = 4
```

### Visual DP Table
```
Array: [7, 3, 5, 3, 6, 2, 9, 8]
Index:  0  1  2  3  4  5  6  7
DP:    [1, 1, 2, 1, 3, 1, 4, 4]

Each cell shows length of LIS ending at that position
```

### LIS Construction Visualization
```
Array: [7, 3, 5, 3, 6, 2, 9, 8]
Index:  0  1  2  3  4  5  6  7

Position 0: [7] (length 1)
Position 1: [3] (length 1)
Position 2: [3, 5] (length 2)
Position 3: [3] (length 1)
Position 4: [3, 5, 6] (length 3)
Position 5: [2] (length 1)
Position 6: [3, 5, 6, 9] (length 4)
Position 7: [3, 5, 6, 8] (length 4)

Longest LIS: [3, 5, 6, 9] or [3, 5, 6, 8] (length 4)
```

### Algorithm Comparison Visualization
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Recursive       │ O(2^n)       │ O(n)         │ Try all      │
│                 │              │              │ subsequences │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Memoized        │ O(n²)        │ O(n²)        │ Cache        │
│ Recursion       │              │              │ results      │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Bottom-up DP    │ O(n²)        │ O(n)         │ Build from   │
│                 │              │              │ base cases   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Binary Search   │ O(n log n)   │ O(n)         │ Use binary   │
│ + DP            │              │              │ search       │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

### Increasing Subsequence Flowchart
```
                    Start
                      │
                      ▼
              ┌─────────────────┐
              │ Input: array    │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Initialize DP   │
              │ array           │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Set base case:  │
              │ dp[i] = 1 for   │
              │ all i           │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ For i = 1 to n: │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ For j = 0 to    │
              │ i-1:            │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ If arr[i] >     │
              │ arr[j]:         │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ dp[i] = max     │
              │ (dp[i], dp[j]   │
              │ + 1)            │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Return max(dp)  │
              └─────────────────┘
                      │
                      ▼
                    End
```

## 🎯 Key Insights

### 1. **Dynamic Programming for Subsequence Problems**
- Find optimal substructure in subsequence problems
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **1D DP Array**
- Use 1D array for single-sequence problems
- Important for understanding
- Fundamental concept
- Essential for algorithm

### 3. **Subsequence vs Substring**
- Subsequence allows skipping elements
- Important for understanding
- Simple but important concept
- Essential for understanding

## 🎯 Problem Variations

### Variation 1: Print the LIS
**Problem**: Find and print the actual longest increasing subsequence.

```python
def print_longest_increasing_subsequence(arr):
    n = len(arr)
    
    # dp[i] = length of LIS ending at position i
    dp = [1] * n
    # prev[i] = previous element in LIS ending at position i
    prev = [-1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                prev[i] = j
    
    # Find the end of the longest LIS
    max_len = max(dp)
    end_pos = dp.index(max_len)
    
    # Reconstruct the LIS
    lis = []
    pos = end_pos
    while pos != -1:
        lis.append(arr[pos])
        pos = prev[pos]
    
    return lis[::-1]

# Example usage
result = print_longest_increasing_subsequence([7, 3, 5, 3, 6, 2, 9, 8])
print(f"LIS: {result}")
```

### Variation 2: Count All LIS
**Problem**: Count the number of different longest increasing subsequences.

```python
def count_longest_increasing_subsequences(arr):
    n = len(arr)
    
    # dp[i] = length of LIS ending at position i
    dp = [1] * n
    # count[i] = number of LIS ending at position i
    count = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j]:
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    count[i] = count[j]
                elif dp[j] + 1 == dp[i]:
                    count[i] += count[j]
    
    max_len = max(dp)
    total_count = sum(count[i] for i in range(n) if dp[i] == max_len)
    
    return total_count

# Example usage
result = count_longest_increasing_subsequences([7, 3, 5, 3, 6, 2, 9, 8])
print(f"Number of LIS: {result}")
```

### Variation 3: LIS with Constraints
**Problem**: Find LIS with additional constraints.

```python
def constrained_lis(arr, constraints):
    n = len(arr)
    
    # dp[i] = length of LIS ending at position i
    dp = [1] * n
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j] and constraints(arr[i], arr[j]):
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)

# Example usage
def constraint_func(curr, prev):
    return curr % 2 == prev % 2  # Same parity constraint

result = constrained_lis([7, 3, 5, 3, 6, 2, 9, 8], constraint_func)
print(f"Constrained LIS length: {result}")
```

### Variation 4: LIS with Weights
**Problem**: Find LIS where each element has a weight.

```python
def weighted_lis(arr, weights):
    n = len(arr)
    
    # dp[i] = weight of LIS ending at position i
    dp = [weights[i] for i in range(n)]
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j]:
                dp[i] = max(dp[i], dp[j] + weights[i])
    
    return max(dp)

# Example usage
weights = [1, 2, 3, 4, 5, 6, 7, 8]
result = weighted_lis([7, 3, 5, 3, 6, 2, 9, 8], weights)
print(f"Weighted LIS: {result}")
```

### Variation 5: LIS with Dynamic Programming Optimization
**Problem**: Optimize the DP solution for better performance.

```python
def optimized_lis(arr):
    n = len(arr)
    
    # Use binary search for O(n log n) solution
    tails = []
    
    for num in arr:
        # Find position to insert num
        left, right = 0, len(tails)
        while left < right:
            mid = (left + right) // 2
            if tails[mid] < num:
                left = mid + 1
            else:
                right = mid
        
        if left == len(tails):
            tails.append(num)
        else:
            tails[left] = num
    
    return len(tails)

# Example usage
result = optimized_lis([7, 3, 5, 3, 6, 2, 9, 8])
print(f"Optimized LIS length: {result}")
```

## 🔗 Related Problems

- **[Longest Common Subsequence](/cses-analyses/problem_soulutions/dynamic_programming/)**: Similar subsequence problems
- **[Edit Distance](/cses-analyses/problem_soulutions/dynamic_programming/)**: Similar string problems
- **[Subsequence Problems](/cses-analyses/problem_soulutions/dynamic_programming/)**: General subsequence problems

## 📚 Learning Points

1. **Dynamic Programming**: Essential for subsequence problems
2. **1D DP Arrays**: Important for single-sequence problems
3. **Subsequence vs Substring**: Important for understanding constraints
4. **Binary Search Optimization**: Important for performance improvement

---

**This is a great introduction to dynamic programming for subsequence problems!** 🎯 