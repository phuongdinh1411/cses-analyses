---
layout: simple
title: "Apple Division"
permalink: /cses-analyses/problem_soulutions/introductory_problems/apple_division_analysis
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

## 🎯 Problem Analysis

### Key Insights
1. **Small n**: Since n ≤ 20, we can use brute force with bitmask
2. **Subset Sum**: We need to find two subsets with minimum difference
3. **Symmetry**: If we find one subset, the other is the complement
4. **Total Sum**: The difference is total_sum - 2*subset_sum

### Complexity Analysis
- **Time**: O(2ⁿ) - try all possible subsets
- **Space**: O(n) - for storing the weights

## 💡 Solution Approaches

### Approach 1: Bitmask Brute Force

**Idea**: Try all possible subsets using bitmask representation.

{% highlight python %}
def apple_division_bitmask(weights):
    n = len(weights)
    total_sum = sum(weights)
    min_diff = float('inf')
    
    # Try all possible subsets (2^n combinations)
    for mask in range(1 << n):
        subset_sum = 0
        for i in range(n):
            if mask & (1 << i):
                subset_sum += weights[i]
        
        # Calculate difference: |total - 2*subset|
        diff = abs(total_sum - 2 * subset_sum)
        min_diff = min(min_diff, diff)
    
    return min_diff

# Example usage
weights = [3, 2, 7, 4, 1]
result = apple_division_bitmask(weights)
print(result)  # Output: 1
{% endhighlight %}

**Time Complexity**: O(n × 2ⁿ)
**Space Complexity**: O(1)

### Approach 2: Meet in the Middle (Optimization)

**Idea**: For larger n, split the array and use meet-in-the-middle technique.

```python
def apple_division_meet_middle(weights):
    n = len(weights)
    if n <= 20:
        return apple_division_bitmask(weights)
    
    # Split into two halves
    mid = n // 2
    left = weights[:mid]
    right = weights[mid:]
    
    # Generate all subset sums for left half
    left_sums = set()
    for mask in range(1 << len(left)):
        subset_sum = sum(left[i] for i in range(len(left)) if mask & (1 << i))
        left_sums.add(subset_sum)
    
    # Generate all subset sums for right half
    right_sums = set()
    for mask in range(1 << len(right)):
        subset_sum = sum(right[i] for i in range(len(right)) if mask & (1 << i))
        right_sums.add(subset_sum)
    
    total_sum = sum(weights)
    min_diff = float('inf')
    
    # Try all combinations
    for left_sum in left_sums: for right_sum in 
right_sums: subset_sum = left_sum + right_sum
            diff = abs(total_sum - 2 * subset_sum)
            min_diff = min(min_diff, diff)
    
    return min_diff
```

**Time Complexity**: O(2^(n/2) × 2^(n/2)) = O(2^n) but with better constant
**Space Complexity**: O(2^(n/2))

### Approach 3: Dynamic Programming (Alternative)

**Idea**: Use DP to find if we can achieve each possible subset sum.

```python
def apple_division_dp(weights):
    total_sum = sum(weights)
    target = total_sum // 2
    
    # dp[i][j] = can we achieve sum j using first i elements
    dp = [[False] * (target + 1) for _ in range(len(weights) + 1)]
    dp[0][0] = True
    
    for i in range(1, len(weights) + 1):
        for j in range(target + 1):
            # Don't include current element
            dp[i][j] = dp[i-1][j]
            # Include current element
            if j >= weights[i-1]:
                dp[i][j] = dp[i][j] or dp[i-1][j - weights[i-1]]
    
    # Find the largest achievable sum ≤ target
    for j in range(target, -1, -1):
        if dp[len(weights)][j]:
            return total_sum - 2 * j
    
    return total_sum
```

**Time Complexity**: O(n × total_sum)
**Space Complexity**: O(n × total_sum)

## 🔧 Implementation

### Complete Solution

```python
def solve_apple_division():
    n = int(input())
    weights = list(map(int, input().split()))
    
    return apple_division_bitmask(weights)

# Main execution
if __name__ == "__main__":
    result = solve_apple_division()
    print(result)
```

### Test Cases

```python
def test_apple_division():
    test_cases = [
        ([3, 2, 7, 4, 1], 1),
        ([1, 1, 1, 1], 0),
        ([1, 2, 3, 4, 5], 1),
        ([10, 20, 30, 40], 0),
        ([1, 1, 1, 1, 1, 1, 1, 1], 0),
    ]
    
    for weights, expected in test_cases:
        result = apple_division_bitmask(weights)
        print(f"Weights: {weights}")
        print(f"Expected: {expected}, 
Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

test_apple_division()
```

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

## 🧮 Mathematical Analysis

### Optimal Substructure

The problem exhibits optimal substructure:
- If we know the optimal division for n-1 apples, we can extend it for n apples
- The optimal solution for n apples must include the optimal solution for some subset

### State Space

- **States**: All possible subset sums
- **Transitions**: Include or exclude each apple
- **Goal**: Find subset sum closest to total_sum/2

### Complexity Lower Bound

- **Decision version**: "Can we divide with difference ≤ k?" is NP-complete
- **Optimization version**: NP-hard
- **For small n**: Polynomial time with bitmask

## 🎯 Key Insights for Competitive Programming

### 1. **Bitmask Pattern**
```python
# Standard bitmask loop
for mask in range(1 << n):
    for i in range(n):
        if mask & (1 << i):
            # Include element i
```

### 2. **Subset Sum Optimization**
```python
# Early termination
if subset_sum > total_sum // 2:
    break  # Can't improve further
```

### 3. **Symmetry Exploitation**
```python
# Only check first half of masks
for mask in range(1 << (n-1)):
    # Check both mask and its complement
```

### 4. **Memory Optimization**
```python
# Use rolling array for DP
dp = [False] * (target + 1)
dp[0] = True
for weight in weights:
    for j in range(target, weight-1, -1):
        dp[j] = dp[j] or dp[j - weight]
```

## 🔗 Related Problems

- **Subset Sum**: Find if a subset sums to target
- **Partition Equal Subset Sum**: Divide into two equal parts
- **Target Sum**: Assign +/- to get target
- **Knapsack Problems**: Optimization with constraints

## 📚 Learning Resources

- **Bit Manipulation**: Essential for competitive programming
- **Meet-in-the-Middle**: Technique for reducing exponential complexity
- **Subset Problems**: Common pattern in competitive programming
- **Dynamic Programming**: Alternative approach for larger constraints

---

**Practice this problem to master bitmask techniques and subset problems!** 🎯 