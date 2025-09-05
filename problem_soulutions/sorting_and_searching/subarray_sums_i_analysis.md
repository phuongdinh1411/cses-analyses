---
layout: simple
title: "Subarray Sums I"
permalink: /problem_soulutions/sorting_and_searching/subarray_sums_i_analysis
---

# Subarray Sums I

## Problem Description

**Problem**: Given an array of n integers and a target sum x, find the number of subarrays that have sum x.

**Input**: 
- First line: n x (size of array and target sum)
- Second line: n integers a₁, a₂, ..., aₙ (the array)

**Output**: Number of subarrays with sum x.

**Example**:
```
Input:
5 7
2 -1 3 5 -2

Output:
2

Explanation: 
Subarrays with sum 7:
- [2, -1, 3, 5, -2] (sum = 2 + (-1) + 3 + 5 + (-2) = 7)
- [3, 5, -2] (sum = 3 + 5 + (-2) = 6, wait... let me recalculate)
Actually, let me check the example more carefully...
```

## 📊 Visual Example

### Input Array
```
Array: [2, -1, 3, 5, -2]
Index:  0   1  2  3   4
Target: 7
```

### Prefix Sum Calculation
```
Step 1: Calculate prefix sums
┌─────────────────────────────────────┐
│ prefix[0] = 2                       │
│ prefix[1] = 2 + (-1) = 1            │
│ prefix[2] = 1 + 3 = 4               │
│ prefix[3] = 4 + 5 = 9               │
│ prefix[4] = 9 + (-2) = 7            │
└─────────────────────────────────────┘
```

### Hash Map Approach
```
Step 2: Use hash map to count subarrays
┌─────────────────────────────────────┐
│ sum_count = {0: 1} (initial)       │
│ result = 0                          │
└─────────────────────────────────────┘

Process each prefix sum:
┌─────────────────────────────────────┐
│ prefix[0] = 2                       │
│ Need: 2 - 7 = -5                    │
│ sum_count[-5] = 0 (not found)       │
│ sum_count[2] = 1                    │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ prefix[1] = 1                       │
│ Need: 1 - 7 = -6                    │
│ sum_count[-6] = 0 (not found)       │
│ sum_count[1] = 1                    │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ prefix[2] = 4                       │
│ Need: 4 - 7 = -3                    │
│ sum_count[-3] = 0 (not found)       │
│ sum_count[4] = 1                    │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ prefix[3] = 9                       │
│ Need: 9 - 7 = 2                     │
│ sum_count[2] = 1 (found!)           │
│ result += 1 = 1                     │
│ sum_count[9] = 1                    │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ prefix[4] = 7                       │
│ Need: 7 - 7 = 0                     │
│ sum_count[0] = 1 (found!)           │
│ result += 1 = 2                     │
│ sum_count[7] = 1                    │
└─────────────────────────────────────┘
```

### Subarray Verification
```
Subarray 1: [2, -1, 3, 5, -2]
- Sum: 2 + (-1) + 3 + 5 + (-2) = 7 ✓

Subarray 2: [2, -1, 3, 5, -2] (entire array)
- Sum: 7 ✓

Wait, let me check all possible subarrays:
- [2]: sum = 2
- [2, -1]: sum = 1
- [2, -1, 3]: sum = 4
- [2, -1, 3, 5]: sum = 9
- [2, -1, 3, 5, -2]: sum = 7 ✓
- [-1]: sum = -1
- [-1, 3]: sum = 2
- [-1, 3, 5]: sum = 7 ✓
- [-1, 3, 5, -2]: sum = 5
- [3]: sum = 3
- [3, 5]: sum = 8
- [3, 5, -2]: sum = 6
- [5]: sum = 5
- [5, -2]: sum = 3
- [-2]: sum = -2

Found 2 subarrays with sum 7: [2, -1, 3, 5, -2] and [-1, 3, 5]
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find all subarrays in the given array
- Calculate sum of each subarray
- Count how many have sum exactly equal to x
- Need efficient approach for large arrays

**Key Observations:**
- Brute force would check O(n²) subarrays
- Can use prefix sum to optimize
- Hash map for frequency counting
- Subarray sum = prefix_sum[end] - prefix_sum[start-1]

### Step 2: Brute Force Approach
**Idea**: Check all possible subarrays and count those with sum x.

```python
def subarray_sums_i_brute_force(n, x, arr):
    count = 0
    
    for start in range(n):
        current_sum = 0
        for end in range(start, n):
            current_sum += arr[end]
            if current_sum == x:
                count += 1
    
    return count
```

**Why this works:**
- Checks all possible subarrays
- Simple to understand and implement
- Guarantees correct answer
- O(n²) time complexity

### Step 3: Prefix Sum Optimization
**Idea**: Use prefix sum and hash map to count subarrays with sum x.

```python
def subarray_sums_i_prefix_sum(n, x, arr):
    count = 0
    prefix_sum = 0
    sum_count = {0: 1}  # Count of prefix sums
    
    for i in range(n):
        prefix_sum += arr[i]
        
        # If prefix_sum - x exists, we found a subarray with sum x
        if prefix_sum - x in sum_count:
            count += sum_count[prefix_sum - x]
        
        # Update count of current prefix sum
        sum_count[prefix_sum] = sum_count.get(prefix_sum, 0) + 1
    
    return count
```

**Why this is better:**
- O(n) time complexity
- Uses prefix sum insight
- Hash map for efficient lookup
- Much more efficient

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_subarray_sums_i():
    n, x = map(int, input().split())
    arr = list(map(int, input().split()))
    
    count = 0
    prefix_sum = 0
    sum_count = {0: 1}  # Count of prefix sums
    
    for i in range(n):
        prefix_sum += arr[i]
        
        # If prefix_sum - x exists, we found a subarray with sum x
        if prefix_sum - x in sum_count:
            count += sum_count[prefix_sum - x]
        
        # Update count of current prefix sum
        sum_count[prefix_sum] = sum_count.get(prefix_sum, 0) + 1
    
    print(count)

# Main execution
if __name__ == "__main__":
    solve_subarray_sums_i()
```

**Why this works:**
- Optimal prefix sum approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (5, 7, [2, -1, 3, 5, -2], 2),
        (4, 6, [1, 2, 3, 4], 2),
        (3, 5, [1, 2, 3], 1),
        (2, 3, [1, 2], 1),
        (1, 1, [1], 1),
    ]
    
    for n, x, arr, expected in test_cases:
        result = solve_test(n, x, arr)
        print(f"n={n}, x={x}, arr={arr}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n, x, arr):
    count = 0
    prefix_sum = 0
    sum_count = {0: 1}
    
    for i in range(n):
        prefix_sum += arr[i]
        
        if prefix_sum - x in sum_count:
            count += sum_count[prefix_sum - x]
        
        sum_count[prefix_sum] = sum_count.get(prefix_sum, 0) + 1
    
    return count

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through array
- **Space**: O(n) - storing prefix sum frequencies

### Why This Solution Works
- **Prefix Sum**: Efficient subarray sum calculation
- **Hash Map**: Fast lookup for target differences
- **Frequency Counting**: Track how many times each sum occurs
- **Optimal Approach**: Linear time complexity

## 🎯 Key Insights

### 1. **Prefix Sum Technique**
- Calculate cumulative sums efficiently
- Subarray sum = prefix_sum[end] - prefix_sum[start-1]
- Enables O(1) subarray sum calculation
- Foundation for many subarray problems

### 2. **Hash Map for Frequency**
- Track how many times each prefix sum occurs
- When target difference found, add frequency to count
- Initialize with {0: 1} for empty prefix
- O(1) lookup and update operations

### 3. **Target Difference Logic**
- If prefix_sum[i] - prefix_sum[j] = x, then prefix_sum[i] - x = prefix_sum[j]
- Look for prefix_sum - x in hash map
- Each occurrence gives us a valid subarray
- Key insight for O(n) solution

## 🎯 Problem Variations

### Variation 1: Subarray Sum in Range
**Problem**: Find number of subarrays with sum in range [L, R].

```python
def subarray_sum_in_range(n, L, R, arr):
    count = 0
    prefix_sum = 0
    sum_count = {0: 1}
    
    for i in range(n):
        prefix_sum += arr[i]
        
        # Count subarrays ending at i with sum in [L, R]
        for prev_sum in sum_count:
            current_sum = prefix_sum - prev_sum
            if L <= current_sum <= R:
                count += sum_count[prev_sum]
        
        sum_count[prefix_sum] = sum_count.get(prefix_sum, 0) + 1
    
    return count
```

### Variation 2: Maximum Subarray Sum
**Problem**: Find maximum subarray sum.

```python
def max_subarray_sum(n, arr):
    max_sum = float('-inf')
    current_sum = 0
    
    for i in range(n):
        current_sum = max(arr[i], current_sum + arr[i])
        max_sum = max(max_sum, current_sum)
    
    return max_sum
```

### Variation 3: Subarray with Zero Sum
**Problem**: Find number of subarrays with sum zero.

```python
def subarray_zero_sum(n, arr):
    count = 0
    prefix_sum = 0
    sum_count = {0: 1}
    
    for i in range(n):
        prefix_sum += arr[i]
        
        if prefix_sum in sum_count:
            count += sum_count[prefix_sum]
        
        sum_count[prefix_sum] = sum_count.get(prefix_sum, 0) + 1
    
    return count
```

### Variation 4: Subarray Sum with Length Constraint
**Problem**: Find subarrays with sum x and length in range [L, R].

```python
def subarray_sum_with_length_constraint(n, x, L, R, arr):
    count = 0
    prefix_sum = 0
    sum_positions = {0: [0]}  # Store positions for each sum
    
    for i in range(n):
        prefix_sum += arr[i]
        
        if prefix_sum - x in sum_positions:
            # Check positions that satisfy length constraints
            for pos in sum_positions[prefix_sum - x]:
                length = i - pos
                if L <= length <= R:
                    count += 1
        
        if prefix_sum not in sum_positions:
            sum_positions[prefix_sum] = []
        sum_positions[prefix_sum].append(i + 1)
    
    return count
```

### Variation 5: Dynamic Subarray Sums
**Problem**: Support dynamic updates to the array.

```python
class DynamicSubarraySums:
    def __init__(self, n):
        self.n = n
        self.arr = [0] * n
        self.prefix_sums = [0] * (n + 1)
        self.sum_counts = {0: 1}
    
    def update(self, index, value):
        old_value = self.arr[index]
        self.arr[index] = value
        
        # Update prefix sums
        diff = value - old_value
        for i in range(index + 1, self.n + 1):
            self.prefix_sums[i] += diff
        
        # Recalculate sum counts
        self.sum_counts = {0: 1}
        for i in range(1, self.n + 1):
            self.sum_counts[self.prefix_sums[i]] = self.sum_counts.get(self.prefix_sums[i], 0) + 1
    
    def get_subarray_count(self, target):
        count = 0
        prefix_sum = 0
        
        for i in range(self.n):
            prefix_sum += self.arr[i]
            
            if prefix_sum - target in self.sum_counts:
                count += self.sum_counts[prefix_sum - target]
            
            self.sum_counts[prefix_sum] = self.sum_counts.get(prefix_sum, 0) + 1
        
        return count
```

## 🔗 Related Problems

- **[Subarray Sums II](/cses-analyses/problem_soulutions/sorting_and_searching/subarray_sums_ii_analysis)**: Advanced subarray problems
- **[Subarray Divisibility](/cses-analyses/problem_soulutions/sorting_and_searching/subarray_divisibility_analysis)**: Divisibility problems
- **[Maximum Subarray Sum](/cses-analyses/problem_soulutions/sorting_and_searching/cses_maximum_subarray_sum_analysis)**: Maximum subarray problems

## 📚 Learning Points

1. **Prefix Sum**: Efficient subarray sum calculation technique
2. **Hash Map Usage**: Fast frequency counting and lookup
3. **Target Difference Logic**: Key insight for O(n) solution
4. **Subarray Problems**: Common pattern in competitive programming

---

**This is a great introduction to prefix sum and hash map techniques!** 🎯 