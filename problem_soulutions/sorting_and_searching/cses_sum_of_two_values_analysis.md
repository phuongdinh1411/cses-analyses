---
layout: simple
title: "Sum of Two Values"
permalink: /problem_soulutions/sorting_and_searching/cses_sum_of_two_values_analysis
---

# Sum of Two Values

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand two-sum problems and hash map-based solutions
- Apply hash maps to efficiently find two values with target sum
- Implement efficient two-sum algorithms with O(n) time complexity
- Optimize two-sum problems using hash maps and complement searching
- Handle edge cases in two-sum problems (no solution, duplicate values, large arrays)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Hash maps, two-sum problems, complement searching, target sum problems
- **Data Structures**: Hash maps, arrays, position tracking, complement tracking
- **Mathematical Concepts**: Two-sum theory, complement mathematics, hash map mathematics
- **Programming Skills**: Hash map implementation, complement searching, position tracking, algorithm implementation
- **Related Problems**: Sum of Three/Four Values (extensions), Hash map problems, Two-sum problems

## Problem Description

**Problem**: You are given an array of n integers. Find two values (at distinct positions) whose sum is x.

**Input**: 
- First line: n and x (array size and target sum)
- Second line: n integers a₁, a₂, ..., aₙ

**Output**: Two integers representing the positions of the values (1-indexed). If no solution, print "IMPOSSIBLE".

**Example**:
```
Input:
4 8
2 7 5 1

Output:
2 4

Explanation: arr[1] + arr[3] = 7 + 1 = 8 (positions are 1-indexed).
```

## 📊 Visual Example

### Input Array
```
Array: [2, 7, 5, 1]
Index:  0  1  2  3
Target: 8
```

### Hash Map Approach Process
```
Step 1: Process element 2 (index 0)
┌─────────────────────────────────────┐
│ Current: 2, Need: 8-2 = 6           │
│ Map: {} (empty)                     │
│ 6 not found, add 2 → 0              │
│ Map: {2: 0}                         │
└─────────────────────────────────────┘

Step 2: Process element 7 (index 1)
┌─────────────────────────────────────┐
│ Current: 7, Need: 8-7 = 1           │
│ Map: {2: 0}                         │
│ 1 not found, add 7 → 1              │
│ Map: {2: 0, 7: 1}                   │
└─────────────────────────────────────┘

Step 3: Process element 5 (index 2)
┌─────────────────────────────────────┐
│ Current: 5, Need: 8-5 = 3           │
│ Map: {2: 0, 7: 1}                   │
│ 3 not found, add 5 → 2              │
│ Map: {2: 0, 7: 1, 5: 2}             │
└─────────────────────────────────────┘

Step 4: Process element 1 (index 3)
┌─────────────────────────────────────┐
│ Current: 1, Need: 8-1 = 7           │
│ Map: {2: 0, 7: 1, 5: 2}             │
│ 7 found at index 1! ✓               │
│ Solution: positions 2, 4 (1-indexed)│
└─────────────────────────────────────┘
```

### Two Pointer Approach (Sorted Array)
```
Original: [2, 7, 5, 1]
Sorted:   [1, 2, 5, 7] (with original indices)

Two pointers: left=0, right=3
┌─────────────────────────────────────┐
│ arr[0] + arr[3] = 1 + 7 = 8 = target│
│ Found solution!                     │
│ Original indices: 3, 1              │
│ 1-indexed: 4, 2                     │
└─────────────────────────────────────┘
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find two distinct positions in array
- Values at these positions sum to target
- Return positions (1-indexed)
- Handle case when no solution exists

**Key Observations:**
- Classic two sum problem
- Can use hash map for O(n) solution
- Need to track original positions
- Handle duplicates correctly

### Step 2: Hash Map Approach
**Idea**: Use a hash map to store values and their positions, then check for complements.

```python
def two_sum_hashmap(arr, target):
    seen = {}  # value -> position
    
    for i in range(len(arr)):
        complement = target - arr[i]
        
        if complement in seen:
            return (seen[complement], i + 1)  # 1-indexed positions
        
        seen[arr[i]] = i + 1
    
    return "IMPOSSIBLE"
```

**Why this works:**
- For each element, calculate needed complement
- Check if complement exists in hash map
- Store current element for future lookups
- O(1) average lookup time

### Step 3: Optimized Solution
**Idea**: Optimize the implementation with better variable names and logic.

```python
def two_sum_optimized(arr, target):
    value_positions = {}  # value -> position
    
    for current_pos in range(len(arr)):
        current_value = arr[current_pos]
        needed_value = target - current_value
        
        if needed_value in value_positions:
            return (value_positions[needed_value], current_pos + 1)
        
        value_positions[current_value] = current_pos + 1
    
    return "IMPOSSIBLE"
```

**Why this is better:**
- Clearer variable names
- More readable logic
- Same optimal time complexity

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_two_sum():
    n, target = map(int, input().split())
    arr = list(map(int, input().split()))
    
    # Hash map approach
    value_positions = {}
    
    for current_pos in range(n):
        current_value = arr[current_pos]
        needed_value = target - current_value
        
        if needed_value in value_positions:
            print(value_positions[needed_value], current_pos + 1)
            return
        
        value_positions[current_value] = current_pos + 1
    
    print("IMPOSSIBLE")

# Main execution
if __name__ == "__main__":
    solve_two_sum()
```

**Why this works:**
- Optimal hash map approach
- Handles all edge cases
- Efficient implementation

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ([2, 7, 5, 1], 8, (2, 4)),
        ([1, 2, 3, 4], 7, (3, 4)),
        ([1, 1], 2, (1, 2)),
        ([1, 2, 3], 10, "IMPOSSIBLE"),
        ([5], 10, "IMPOSSIBLE"),
    ]
    
    for arr, target, expected in test_cases:
        result = solve_test(arr, target)
        print(f"Array: {arr}, Target: {target}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(arr, target):
    value_positions = {}
    
    for current_pos in range(len(arr)):
        current_value = arr[current_pos]
        needed_value = target - current_value
        
        if needed_value in value_positions:
            return (value_positions[needed_value], current_pos + 1)
        
        value_positions[current_value] = current_pos + 1
    
    return "IMPOSSIBLE"

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through array
- **Space**: O(n) - hash map storage

### Why This Solution Works
- **Hash Map**: O(1) average lookup time
- **Single Pass**: Process each element once
- **Position Tracking**: Store original positions
- **Complement Search**: Efficient target finding

## 🎯 Key Insights

### 1. **Hash Map Strategy**
- Store values as keys, positions as values
- Check for complement (target - current_value)
- O(1) average lookup and insertion
- Handles duplicates correctly

### 2. **Single Pass Algorithm**
- Process each element exactly once
- No need for nested loops
- Early termination when solution found
- Optimal time complexity

### 3. **Position Tracking**
- Store 1-indexed positions
- Return positions in correct order
- Handle edge cases properly
- Clear output format

## 🎯 Problem Variations

### Variation 1: Three Sum
**Problem**: Find three values that sum to target.

```python
def three_sum(arr, target):
    n = len(arr)
    
    for i in range(n):
        # Use two sum for remaining elements
        remaining_target = target - arr[i]
        value_positions = {}
        
        for j in range(i + 1, n):
            current_value = arr[j]
            needed_value = remaining_target - current_value
            
            if needed_value in value_positions:
                return (i + 1, value_positions[needed_value], j + 1)
            
            value_positions[current_value] = j + 1
    
    return "IMPOSSIBLE"
```

### Variation 2: Four Sum
**Problem**: Find four values that sum to target.

```python
def four_sum(arr, target):
    n = len(arr)
    
    for i in range(n):
        for j in range(i + 1, n):
            # Use two sum for remaining elements
            remaining_target = target - arr[i] - arr[j]
            value_positions = {}
            
            for k in range(j + 1, n):
                current_value = arr[k]
                needed_value = remaining_target - current_value
                
                if needed_value in value_positions:
                    return (i + 1, j + 1, value_positions[needed_value], k + 1)
                
                value_positions[current_value] = k + 1
    
    return "IMPOSSIBLE"
```

### Variation 3: Closest Sum
**Problem**: Find two values whose sum is closest to target.

```python
def closest_two_sum(arr, target):
    n = len(arr)
    arr.sort()
    
    left, right = 0, n - 1
    closest_sum = float('inf')
    closest_pair = None
    
    while left < right:
        current_sum = arr[left] + arr[right]
        
        if abs(current_sum - target) < abs(closest_sum - target):
            closest_sum = current_sum
            closest_pair = (left + 1, right + 1)
        
        if current_sum < target:
            left += 1
        else:
            right -= 1
    
    return closest_pair, closest_sum
```

### Variation 4: All Pairs
**Problem**: Find all pairs that sum to target.

```python
def all_two_sum_pairs(arr, target):
    value_positions = {}  # value -> list of positions
    pairs = []
    
    for current_pos in range(len(arr)):
        current_value = arr[current_pos]
        needed_value = target - current_value
        
        if needed_value in value_positions:
            # Add all pairs with this complement
            for pos in value_positions[needed_value]:
                pairs.append((pos, current_pos + 1))
        
        # Add current value to positions
        if current_value not in value_positions:
            value_positions[current_value] = []
        value_positions[current_value].append(current_pos + 1)
    
    return pairs
```

### Variation 5: Two Sum with Constraints
**Problem**: Find two values that sum to target with additional constraints.

```python
def constrained_two_sum(arr, target, min_diff=0):
    value_positions = {}
    
    for current_pos in range(len(arr)):
        current_value = arr[current_pos]
        needed_value = target - current_value
        
        if needed_value in value_positions:
            pos1, pos2 = value_positions[needed_value], current_pos + 1
            
            # Check constraint: positions must be at least min_diff apart
            if abs(pos1 - pos2) >= min_diff:
                return (pos1, pos2)
        
        value_positions[current_value] = current_pos + 1
    
    return "IMPOSSIBLE"
```

## 🔗 Related Problems

- **[Sum of Three Values](/cses-analyses/problem_soulutions/sorting_and_searching/sum_of_three_values_analysis)**: Three sum problems
- **[Sum of Four Values](/cses-analyses/problem_soulutions/sorting_and_searching/sum_of_four_values_analysis)**: Four sum problems
- **[Subarray Sums](/cses-analyses/problem_soulutions/sorting_and_searching/subarray_sums_i_analysis)**: Subarray sum problems

## 📚 Learning Points

1. **Hash Maps**: Efficient lookup data structures
2. **Two Pointers**: Alternative approach with sorting
3. **Complement Strategy**: Calculate needed value efficiently
4. **Position Tracking**: Maintain original indices

---

**This is a great introduction to hash maps and two sum problems!** 🎯 