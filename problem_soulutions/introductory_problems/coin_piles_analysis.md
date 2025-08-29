---
layout: simple
title: "Coin Piles Analysis"
permalink: /problem_soulutions/introductory_problems/coin_piles_analysis
---


# Coin Piles Analysis

## Problem Description

You have two piles of coins. In one move, you can either:
- Remove 1 coin from the first pile and 2 coins from the second pile, OR
- Remove 2 coins from the first pile and 1 coin from the second pile

Determine if it's possible to empty both piles completely.

## Key Insights

### 1. Mathematical Analysis
- Let's say we make `x` moves of type 1 and `y` moves of type 2
- From pile 1: `x + 2y` coins removed
- From pile 2: `2x + y` coins removed
- We need: `x + 2y = a` and `2x + y = b`

### 2. System of Equations
```
x + 2y = a  (pile 1)
2x + y = b  (pile 2)
```

Solving:
- Multiply first equation by 2: `2x + 4y = 2a`
- Subtract second equation: `3y = 2a - b`
- Therefore: `y = (2a - b) / 3`
- Similarly: `x = (2b - a) / 3`

### 3. Conditions for Solution
- Both `x` and `y` must be non-negative integers
- `2a - b` must be divisible by 3
- `2b - a` must be divisible by 3
- Both results must be ≥ 0

## Solution Approach

```python
def can_empty_piles(a, b):
    # Check if 2a - b is divisible by 3 and non-negative
    if (2 * a - b) % 3 != 0 or (2 * a - b) < 0:
        return False
    
    # Check if 2b - a is divisible by 3 and non-negative
    if (2 * b - a) % 3 != 0 or (2 * b - a) < 0:
        return False
    
    return True
```

## Time Complexity
- **Time**: O(1) - constant time mathematical check
- **Space**: O(1) - constant space

## Example Walkthrough

**Example 1**: a = 3, b = 3
- `2a - b = 6 - 3 = 3` ✓ (divisible by 3)
- `2b - a = 6 - 3 = 3` ✓ (divisible by 3)
- `y = 3/3 = 1` ✓ (non-negative)
- `x = 3/3 = 1` ✓ (non-negative)
- **Result**: YES

**Example 2**: a = 1, b = 1
- `2a - b = 2 - 1 = 1` ✗ (not divisible by 3)
- **Result**: NO

## Problem Variations

### Variation 1: Multiple Pile Types
**Problem**: You have 3 piles with coins (a, b, c). In one move, you can remove:
- 1 from pile 1, 2 from pile 2, 1 from pile 3, OR
- 2 from pile 1, 1 from pile 2, 2 from pile 3

**Solution**: Similar approach with 3 variables and 3 equations.

### Variation 2: Weighted Coins
**Problem**: Each coin has a weight. Find the minimum total weight of coins removed.

**Approach**: Use dynamic programming with state (remaining coins in each pile).

### Variation 3: Constrained Moves
**Problem**: You can only make at most k moves. Can you empty the piles?

**Approach**: Check if the required moves ≤ k.

### Variation 4: Maximum Coins Removed
**Problem**: Instead of emptying, find the maximum coins you can remove.

**Approach**: Use greedy strategy or dynamic programming.

## Related Problems
- [Two Sets](/cses-analyses/problem_soulutions/two_sets_analysis/)
- [Apple Division](/cses-analyses/problem_soulutions/apple_division_analysis/)
- [Creating Strings](/cses-analyses/problem_soulutions/creating_strings_analysis/)

## Practice Problems
1. **CSES**: Coin Piles
2. **AtCoder**: Similar coin removal problems
3. **Codeforces**: Constructive algorithms with constraints

## Key Takeaways
1. **Mathematical modeling** is crucial for constructive problems
2. **System of equations** can be solved analytically
3. **Integer constraints** must be carefully checked
4. **Edge cases** like negative results are important
5. **Modular arithmetic** is often needed for divisibility checks
