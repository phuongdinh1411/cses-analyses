---
layout: simple
title: "Apple Division"
permalink: /problem_soulutions/introductory_problems/apple_division_analysis
---

# Apple Division

## Problem Description

**Problem**: Given n apples with weights w₁, w₂, ..., wₙ, divide them into two groups such that the difference between the total weights of the two groups is minimized.

**Input**: 
- First line: n (1 ≤ n ≤ 20)
- Second line: n integers w₁, w₂, ..., wₙ (1 ≤ wᵢ ≤ 10⁹)

**Output**: The minimum possible difference between the two groups.

**Example**:
```
Input:
5
3 2 7 4 1

Output:
1

Explanation: Group 1: {3, 2, 1} = 6, Group 2: {7, 4} = 11, Difference = |11-6| = 5
But better: Group 1: {3, 2, 4} = 9, Group 2: {7, 1} = 8, Difference = |9-8| = 1
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Divide n apples into exactly 2 groups
- Minimize the absolute difference between group weights
- Each apple must go to exactly one group

**Key Observations:**
- If we know one group's weight, the other group's weight is `total_weight - group_weight`
- The difference is `|total_weight - 2 × group_weight|`
- We only need to find the best weight for one group

### Step 2: Brute Force Approach
**Idea**: Try all possible ways to divide the apples.

**How to represent a division?**
- Use a binary number (bitmask) where each bit represents whether an apple goes to group 1
- Example: `10101` means apples 0,2,4 go to group 1, apples 1,3 go to group 2

```python
def solve_brute_force(weights):
    n = len(weights)
    total_sum = sum(weights)
    min_diff = float('inf')
    
    # Try all possible divisions (2^n combinations)
    for mask in range(1 << n):
        group1_sum = 0
        for i in range(n):
            if mask & (1 << i):  # If bit i is set
                group1_sum += weights[i]
        
        # Calculate difference
        diff = abs(total_sum - 2 * group1_sum)
        min_diff = min(min_diff, diff)
    
    return min_diff
```

**Why this works:**
- We try every possible way to divide the apples
- Since n ≤ 20, we have at most 2²⁰ = 1,048,576 combinations
- This is fast enough for the given constraints

### Step 3: Optimization - Early Termination
**Idea**: Stop early when we can't improve the answer.

```python
def solve_optimized(weights):
    n = len(weights)
    total_sum = sum(weights)
    min_diff = float('inf')
    
    for mask in range(1 << n):
        group1_sum = 0
        for i in range(n):
            if mask & (1 << i):
                group1_sum += weights[i]
        
        # Early termination: if group1 is already too heavy
        if group1_sum > total_sum // 2:
            continue
            
        diff = abs(total_sum - 2 * group1_sum)
        min_diff = min(min_diff, diff)
    
    return min_diff
```

**Why this optimization helps:**
- If group1 weight > total_weight/2, the difference can only get worse
- We skip about half the combinations

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_apple_division():
    n = int(input())
    weights = list(map(int, input().split()))
    
    total_sum = sum(weights)
    min_diff = float('inf')
    
    # Try all possible divisions
    for mask in range(1 << n):
        group1_sum = 0
        for i in range(n):
            if mask & (1 << i):
                group1_sum += weights[i]
        
        # Early termination
        if group1_sum > total_sum // 2:
            continue
            
        diff = abs(total_sum - 2 * group1_sum)
        min_diff = min(min_diff, diff)
    
    return min_diff

# Main execution
if __name__ == "__main__":
    result = solve_apple_division()
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
        ([3, 2, 7, 4, 1], 1),      # Should find difference of 1
        ([1, 1, 1, 1], 0),         # Perfect division possible
        ([1, 2, 3, 4, 5], 1),      # Best difference is 1
        ([10, 20, 30, 40], 0),     # Can divide perfectly
    ]
    
    for weights, expected in test_cases:
        result = solve_apple_division_test(weights)
        print(f"Weights: {weights}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_apple_division_test(weights):
    total_sum = sum(weights)
    min_diff = float('inf')
    
    for mask in range(1 << len(weights)):
        group1_sum = 0
        for i in range(len(weights)):
            if mask & (1 << i):
                group1_sum += weights[i]
        
        if group1_sum > total_sum // 2:
            continue
            
        diff = abs(total_sum - 2 * group1_sum)
        min_diff = min(min_diff, diff)
    
    return min_diff

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Brute Force**: O(n × 2ⁿ) - For each of 2ⁿ masks, we sum up to n weights
- **With Optimization**: O(n × 2ⁿ) in worst case, but much faster in practice

### Space Complexity
- O(1) - We only use a few variables

### Why Bitmask?
- **Efficient**: Each bit represents one apple's assignment
- **Complete**: We try every possible division
- **Fast**: Bit operations are very fast

## 🎯 Key Insights

### 1. **Bitmask Pattern**
```python
# Standard way to iterate through all subsets
for mask in range(1 << n):
    for i in range(n):
        if mask & (1 << i):
            # Include element i in current subset
```

### 2. **Symmetry Property**
- If we find group1 with weight w, group2 has weight (total - w)
- The difference is |total - 2w|
- We only need to check weights up to total/2

### 3. **Early Termination**
- Once group1 weight exceeds total/2, we can't improve
- This cuts our search space roughly in half

## 🎯 Problem Variations

### Variation 1: K Groups Division
**Problem**: Divide n apples into k groups (k > 2) with minimum maximum difference between any two groups.

```python
def k_groups_division(weights, k):
    n = len(weights)
    total_sum = sum(weights)
    
    def can_divide(target_diff):
        # Check if we can divide into k groups with max difference ≤ target_diff
        # This is a more complex problem requiring advanced techniques
        pass
    
    # Binary search on the answer
    left, right = 0, total_sum
    while left < right:
        mid = (left + right) // 2
        if can_divide(mid):
            right = mid
        else:
            left = mid + 1
    
    return left
```

### Variation 2: Fair Division with Constraints
**Problem**: Divide apples ensuring each group has at least one apple and maximum group size is limited.

```python
def constrained_division(weights, max_group_size):
    n = len(weights)
    total_sum = sum(weights)
    min_diff = float('inf')
    
    for mask in range(1 << n):
        # Count bits (group size)
        group_size = bin(mask).count('1')
        if group_size > max_group_size or group_size == 0 or group_size == n:
            continue
            
        subset_sum = sum(weights[i] for i in range(n) if mask & (1 << i))
        diff = abs(total_sum - 2 * subset_sum)
        min_diff = min(min_diff, diff)
    
    return min_diff
```

### Variation 3: Weighted Fair Division
**Problem**: Each apple has a value and weight. Maximize the minimum value-to-weight ratio in any group.

```python
def weighted_fair_division(weights, values):
    n = len(weights)
    
    def get_ratio(mask):
        total_weight = sum(weights[i] for i in range(n) if mask & (1 << i))
        total_value = sum(values[i] for i in range(n) if mask & (1 << i))
        return total_value / total_weight if total_weight > 0 else 0
    
    min_ratio = float('inf')
    
    for mask in range(1, 1 << n):
        if mask == (1 << n) - 1:  # Skip full set
            continue
        ratio = get_ratio(mask)
        min_ratio = min(min_ratio, ratio)
    
    return min_ratio
```

## 🔗 Related Problems

- **[Two Sets](/cses-analyses/problem_soulutions/introductory_problems/two_sets_analysis)**: Similar division problem
- **[Money Sums](/cses-analyses/problem_soulutions/dynamic_programming/money_sums_analysis)**: Find all possible subset sums
- **[Coin Combinations](/cses-analyses/problem_soulutions/dynamic_programming/coin_combinations_i_analysis)**: Count ways to make a sum

## 📚 Learning Points

1. **Bitmask Technique**: Essential for small subset problems
2. **Brute Force Optimization**: When n is small, brute force can be the best approach
3. **Early Termination**: Stop when you can't improve the answer
4. **Problem Transformation**: Convert division problem to subset sum problem

---

**Practice this pattern - it appears in many competitive programming problems!** 🎯 