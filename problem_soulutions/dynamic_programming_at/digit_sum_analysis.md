---
layout: simple
title: "Digit Sum"
permalink: /problem_soulutions/dynamic_programming_at/digit_sum_analysis
---

# Digit Sum

## 📋 Problem Information

### 🎯 **Learning Objectives**
- Understand digit DP
- Apply DP to solve digit-related problems
- Handle tight constraints in digit DP
- Recognize digit DP patterns

## 📋 Problem Description

Given a string K representing a number and integer D, count numbers ≤ K whose digit sum is divisible by D, modulo 10^9+7.

**Input**: 
- First line: K (string)
- Second line: D (1 ≤ D ≤ 100)

**Output**: 
- Count modulo 10^9+7

**Constraints**:
- 1 ≤ |K| ≤ 10^4
- 1 ≤ D ≤ 100

## 🔍 Solution Analysis

### Approach: Digit DP

**Key Insight**: Use digit DP with state (position, tight, digit_sum_mod_D).

**DP State Definition**:
- `dp[pos][tight][sum_mod]` = count of numbers with:
  - Processed first `pos` digits
  - `tight` = 1 if prefix equals K's prefix, 0 otherwise
  - `sum_mod` = digit sum modulo D

**Recurrence Relation**:
- For each digit d from 0 to (K[pos] if tight, else 9):
  - `new_tight = tight and (d == K[pos])`
  - `new_sum = (sum_mod + d) % D`
  - `dp[pos+1][new_tight][new_sum] += dp[pos][tight][sum_mod]`

**Implementation**:
```python
def digit_sum_count(k_str, d):
    """
    Digit DP solution for Digit Sum problem
    
    Args:
        k_str: string representation of upper bound
        d: divisor
    
    Returns:
        int: count modulo 10^9+7
    """
    MOD = 10**9 + 7
    n = len(k_str)
    k_digits = [int(c) for c in k_str]
    
    # dp[pos][tight][sum_mod]
    memo = {}
    
    def dp(pos, tight, sum_mod):
        if (pos, tight, sum_mod) in memo:
            return memo[(pos, tight, sum_mod)]
        
        # Base case: all digits processed
        if pos == n:
            return 1 if sum_mod == 0 else 0
        
        result = 0
        limit = k_digits[pos] if tight else 9
        
        for digit in range(limit + 1):
            new_tight = tight and (digit == limit)
            new_sum = (sum_mod + digit) % d
            result = (result + dp(pos + 1, new_tight, new_sum)) % MOD
        
        memo[(pos, tight, sum_mod)] = result
        return result
    
    # Subtract 1 to exclude K itself, then add if K is valid
    result = dp(0, True, 0) - 1
    if sum(k_digits) % d == 0:
        result = (result + 1) % MOD
    
    return result

# Example usage
k_str = "30"
d = 4
result = digit_sum_count(k_str, d)
print(f"Count: {result}")
```

**Time Complexity**: O(|K| * D * 2)
**Space Complexity**: O(|K| * D * 2)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Digit DP | O(|K| * D) | O(|K| * D) | Process digits with constraints |

### Why This Solution Works
- **Tight Constraint**: Track if prefix equals K's prefix
- **Modular Arithmetic**: Track digit sum modulo D
- **Memoization**: Cache computed states

## 🚀 Related Problems
- Digit DP problems
- Counting problems with constraints

## 🔗 Additional Resources
- [AtCoder DP Contest Problem S](https://atcoder.jp/contests/dp/tasks/dp_s) - Original problem
- Digit DP techniques

