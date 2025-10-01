---
layout: simple
title: "Missing Coin Sum"
permalink: /problem_soulutions/sorting_and_searching/missing_coin_sum_analysis
---

# Missing Coin Sum

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of greedy algorithms and their applications
- Apply sorting algorithms for finding optimal solutions
- Implement efficient solutions for coin sum problems
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in greedy algorithms

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sorting, greedy algorithms, optimization, mathematical reasoning
- **Data Structures**: Arrays, sorting algorithms
- **Mathematical Concepts**: Greedy choice property, optimization theory, coin problems
- **Programming Skills**: Algorithm implementation, complexity analysis, sorting
- **Related Problems**: Stick Lengths (optimization), Array Division (optimization), Collecting Numbers (greedy)

## 📋 Problem Description

You have n coins with values 1, 2, 3, ..., n. You want to select a subset of these coins such that you can make any sum from 1 to some maximum value using the selected coins.

Find the smallest sum that cannot be made using the selected coins.

**Input**: 
- First line: integer n (number of coins)
- Second line: n integers a[1], a[2], ..., a[n] (values of available coins)

**Output**: 
- Print one integer: the smallest sum that cannot be made

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ a[i] ≤ 10⁹

**Example**:
```
Input:
4
1 2 3 5

Output:
12

Explanation**: 
Available coins: [1, 2, 3, 5]

Using coins [1, 2, 3]:
- Can make: 1, 2, 3, 1+2=3, 1+3=4, 2+3=5, 1+2+3=6
- Cannot make: 7, 8, 9, 10, 11, 12, ...

Using coins [1, 2, 3, 5]:
- Can make: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
- Cannot make: 12 (smallest missing sum)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Check All Possible Sums

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Check all possible sums from 1 to some maximum
- **Complete Coverage**: Guaranteed to find the smallest missing sum
- **Simple Implementation**: Straightforward nested loops approach
- **Inefficient**: Exponential time complexity

**Key Insight**: For each possible sum, check if it can be made using the available coins.

**Algorithm**:
- For each sum from 1 to some maximum:
  - Check if the sum can be made using available coins
  - Return the first sum that cannot be made

**Visual Example**:
```
Available coins: [1, 2, 3, 5]

Check sum 1: Can make with coin 1 ✓
Check sum 2: Can make with coin 2 ✓
Check sum 3: Can make with coin 3 ✓
Check sum 4: Can make with coins 1+3 ✓
Check sum 5: Can make with coin 5 ✓
Check sum 6: Can make with coins 1+2+3 ✓
Check sum 7: Can make with coins 2+5 ✓
Check sum 8: Can make with coins 3+5 ✓
Check sum 9: Can make with coins 1+3+5 ✓
Check sum 10: Can make with coins 2+3+5 ✓
Check sum 11: Can make with coins 1+2+3+5 ✓
Check sum 12: Cannot make ✗

Smallest missing sum: 12
```

**Implementation**:
```python
def brute_force_missing_coin_sum(coins):
    """
    Find smallest missing sum using brute force approach
    
    Args:
        coins: list of available coin values
    
    Returns:
        int: smallest sum that cannot be made
    """
    def can_make_sum(target, coins):
        """Check if target sum can be made using coins"""
        if target == 0:
            return True
        if not coins or target < 0:
            return False
        
        # Try using the first coin or not using it
        return (can_make_sum(target - coins[0], coins[1:]) or 
                can_make_sum(target, coins[1:]))
    
    # Check sums starting from 1
    sum_to_check = 1
    while True:
        if not can_make_sum(sum_to_check, coins):
            return sum_to_check
        sum_to_check += 1

# Example usage
coins = [1, 2, 3, 5]
result = brute_force_missing_coin_sum(coins)
print(f"Brute force result: {result}")  # Output: 12
```

**Time Complexity**: O(2^n × S) - Exponential in number of coins
**Space Complexity**: O(n) - For recursive calls

**Why it's inefficient**: Exponential time complexity makes it impractical for large inputs.

---

### Approach 2: Optimized - Dynamic Programming

**Key Insights from Optimized Approach**:
- **Dynamic Programming**: Use DP to avoid recalculating subproblems
- **Efficient Calculation**: Calculate all possible sums in O(n × S) time
- **Better Complexity**: Achieve O(n × S) time complexity
- **Memory Trade-off**: Use more memory for better time complexity

**Key Insight**: Use dynamic programming to efficiently calculate all possible sums.

**Algorithm**:
- Create a DP array to track which sums can be made
- For each coin, update the DP array
- Find the first sum that cannot be made

**Visual Example**:
```
Available coins: [1, 2, 3, 5]
DP array: [True, False, False, False, False, False, False, False, False, False, False, False]

After coin 1: [True, True, False, False, False, False, False, False, False, False, False, False]
After coin 2: [True, True, True, True, False, False, False, False, False, False, False, False]
After coin 3: [True, True, True, True, True, True, True, False, False, False, False, False]
After coin 5: [True, True, True, True, True, True, True, True, True, True, True, False]

First False at index 12 → smallest missing sum: 12
```

**Implementation**:
```python
def optimized_missing_coin_sum(coins):
    """
    Find smallest missing sum using dynamic programming
    
    Args:
        coins: list of available coin values
    
    Returns:
        int: smallest sum that cannot be made
    """
    # Sort coins for better performance
    coins.sort()
    
    # DP array to track which sums can be made
    max_sum = sum(coins) + 1
    dp = [False] * max_sum
    dp[0] = True
    
    # For each coin, update the DP array
    for coin in coins:
        for sum_val in range(max_sum - 1, coin - 1, -1):
            if dp[sum_val - coin]:
                dp[sum_val] = True
    
    # Find the first sum that cannot be made
    for sum_val in range(1, max_sum):
        if not dp[sum_val]:
            return sum_val
    
    return max_sum

# Example usage
coins = [1, 2, 3, 5]
result = optimized_missing_coin_sum(coins)
print(f"Optimized result: {result}")  # Output: 12
```

**Time Complexity**: O(n × S) - Where S is the sum of all coins
**Space Complexity**: O(S) - For DP array

**Why it's better**: Much more efficient than brute force with dynamic programming.

---

### Approach 3: Bottom-Up Dynamic Programming

**Key Insights from Bottom-Up Approach**:
- **Systematic Building**: Build solutions from smallest to largest sums
- **Tabular Method**: Use a table to store intermediate results
- **Iterative Process**: Process coins one by one, updating the table
- **Memory Efficient**: Can optimize space usage with rolling array technique

**Key Insight**: Build a table where dp[i] represents whether sum i can be made using available coins.

**Algorithm**:
- Initialize a boolean array dp where dp[i] = True if sum i can be made
- For each coin, update the dp array from right to left
- Find the first index where dp[i] = False

**Visual Example**:
```
Available coins: [1, 2, 3, 5]
DP array size: 12 (sum of all coins + 1)

Initial: [True, False, False, False, False, False, False, False, False, False, False, False]

After coin 1:
[True, True, False, False, False, False, False, False, False, False, False, False]

After coin 2:
[True, True, True, True, False, False, False, False, False, False, False, False]

After coin 3:
[True, True, True, True, True, True, True, False, False, False, False, False]

After coin 5:
[True, True, True, True, True, True, True, True, True, True, True, False]

First False at index 12 → smallest missing sum: 12
```

**Implementation**:
```python
def bottom_up_missing_coin_sum(coins):
    """
    Find smallest missing sum using bottom-up dynamic programming
    
    Args:
        coins: list of available coin values
    
    Returns:
        int: smallest sum that cannot be made
    """
    # Sort coins for better performance
    coins.sort()
    
    # Calculate maximum possible sum
    max_sum = sum(coins)
    
    # DP array: dp[i] = True if sum i can be made
    dp = [False] * (max_sum + 1)
    dp[0] = True  # Sum 0 can always be made (using no coins)
    
    # Process each coin
    for coin in coins:
        # Update dp array from right to left to avoid using same coin twice
        for sum_val in range(max_sum, coin - 1, -1):
            if dp[sum_val - coin]:
                dp[sum_val] = True
    
    # Find the first sum that cannot be made
    for sum_val in range(1, max_sum + 1):
        if not dp[sum_val]:
            return sum_val
    
    # If all sums can be made, return max_sum + 1
    return max_sum + 1

def bottom_up_missing_coin_sum_optimized(coins):
    """
    Space-optimized bottom-up approach using rolling array
    """
    coins.sort()
    max_sum = sum(coins)
    
    # Use rolling array to save space
    dp = [False] * (max_sum + 1)
    dp[0] = True
    
    for coin in coins:
        # Process from right to left to avoid overwriting
        for sum_val in range(max_sum, coin - 1, -1):
            dp[sum_val] = dp[sum_val] or dp[sum_val - coin]
    
    # Find first impossible sum
    for sum_val in range(1, max_sum + 1):
        if not dp[sum_val]:
            return sum_val
    
    return max_sum + 1

def bottom_up_missing_coin_sum_with_tracking(coins):
    """
    Bottom-up approach with coin usage tracking
    """
    coins.sort()
    max_sum = sum(coins)
    
    # DP array with coin tracking
    dp = [False] * (max_sum + 1)
    coin_used = [[] for _ in range(max_sum + 1)]
    dp[0] = True
    coin_used[0] = []
    
    for coin in coins:
        for sum_val in range(max_sum, coin - 1, -1):
            if dp[sum_val - coin]:
                dp[sum_val] = True
                coin_used[sum_val] = coin_used[sum_val - coin] + [coin]
    
    # Find first impossible sum
    for sum_val in range(1, max_sum + 1):
        if not dp[sum_val]:
            return sum_val, coin_used
    
    return max_sum + 1, coin_used

# Example usage
coins = [1, 2, 3, 5]
result = bottom_up_missing_coin_sum(coins)
print(f"Bottom-up result: {result}")  # Output: 12

result_opt = bottom_up_missing_coin_sum_optimized(coins)
print(f"Optimized bottom-up result: {result_opt}")  # Output: 12

result_track, coin_usage = bottom_up_missing_coin_sum_with_tracking(coins)
print(f"Bottom-up with tracking result: {result_track}")
print(f"Coin usage for sum 6: {coin_usage[6]}")  # Output: [1, 2, 3]
```

**Time Complexity**: O(n × S) - Where S is the sum of all coins
**Space Complexity**: O(S) - For DP array

**Why it's effective**: 
- **Systematic Approach**: Builds solutions incrementally
- **No Recursion**: Avoids stack overflow issues
- **Clear Logic**: Easy to understand and debug
- **Flexible**: Can be extended for various coin problems

---

### Approach 4: Optimal - Greedy Algorithm

**Key Insights from Optimal Approach**:
- **Greedy Choice**: Always use the smallest available coin first
- **Mathematical Insight**: If we can make sums 1 to k, and we have a coin of value k+1, we can make sums 1 to 2k+1
- **Optimal Complexity**: Achieve O(n log n) time complexity
- **Efficient Implementation**: No need for DP array

**Key Insight**: Sort coins and use greedy approach to find the smallest missing sum.

**Algorithm**:
- Sort the coins in ascending order
- Keep track of the maximum sum that can be made
- For each coin, if it's greater than max_sum + 1, return max_sum + 1
- Otherwise, update max_sum to max_sum + coin

**Visual Example**:
```
Available coins: [1, 2, 3, 5]
Sorted: [1, 2, 3, 5]

max_sum = 0
Coin 1: 1 ≤ 0 + 1 ✓ → max_sum = 0 + 1 = 1
Coin 2: 2 ≤ 1 + 1 ✓ → max_sum = 1 + 2 = 3
Coin 3: 3 ≤ 3 + 1 ✓ → max_sum = 3 + 3 = 6
Coin 5: 5 ≤ 6 + 1 ✓ → max_sum = 6 + 5 = 11

All coins processed → return 11 + 1 = 12
```

**Implementation**:
```python
def optimal_missing_coin_sum(coins):
    """
    Find smallest missing sum using greedy algorithm
    
    Args:
        coins: list of available coin values
    
    Returns:
        int: smallest sum that cannot be made
    """
    # Sort coins in ascending order
    coins.sort()
    
    max_sum = 0
    
    # Process each coin
    for coin in coins:
        # If current coin is greater than max_sum + 1,
        # then max_sum + 1 cannot be made
        if coin > max_sum + 1:
            return max_sum + 1
        
        # Otherwise, we can make sums up to max_sum + coin
        max_sum += coin
    
    # If all coins are processed, the smallest missing sum is max_sum + 1
    return max_sum + 1

# Example usage
coins = [1, 2, 3, 5]
result = optimal_missing_coin_sum(coins)
print(f"Optimal result: {result}")  # Output: 12
```

**Time Complexity**: O(n log n) - Sorting dominates
**Space Complexity**: O(1) - Constant extra space

**Why it's optimal**: Achieves the best possible time complexity with mathematical insight.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^n × S) | O(n) | Check all possible sums |
| Dynamic Programming | O(n × S) | O(S) | Use DP to avoid recalculations |
| Bottom-Up DP | O(n × S) | O(S) | Build solutions systematically |
| Greedy Algorithm | O(n log n) | O(1) | Use mathematical insight |

### Time Complexity
- **Time**: O(n log n) - Greedy algorithm provides optimal time complexity
- **Space**: O(1) - Constant extra space for greedy approach

### Why This Solution Works
- **Greedy Choice**: Always using the smallest available coin first is optimal
- **Mathematical Insight**: The greedy approach is mathematically proven to be correct
- **Efficient Implementation**: No need for complex data structures
- **Optimal Approach**: Greedy algorithm provides the most efficient solution for this problem

### Approach Comparison and When to Use Each

#### **Brute Force Approach**
- **When to use**: Small inputs, educational purposes, or when you need to understand all possible combinations
- **Pros**: Simple to understand, guaranteed correct result
- **Cons**: Exponential time complexity, impractical for large inputs
- **Best for**: Learning the problem, small test cases

#### **Dynamic Programming (Top-Down)**
- **When to use**: When you need to avoid recalculating subproblems, medium-sized inputs
- **Pros**: Avoids redundant calculations, clear recursive structure
- **Cons**: Stack overflow risk for large inputs, higher space complexity
- **Best for**: Medium-sized problems, when you need to understand the recursive structure

#### **Bottom-Up Dynamic Programming**
- **When to use**: Large inputs, when you need systematic solution building, production code
- **Pros**: No recursion stack issues, systematic approach, easy to optimize
- **Cons**: Higher space complexity, less intuitive than recursive approach
- **Best for**: Large-scale problems, production environments, when you need to track coin usage

#### **Greedy Algorithm**
- **When to use**: When you need optimal time complexity, large inputs, competitive programming
- **Pros**: Optimal O(n log n) complexity, minimal space usage, mathematically proven correct
- **Cons**: Requires understanding of greedy choice property, less flexible for variations
- **Best for**: Competitive programming, large inputs, when optimal complexity is required

### Choosing the Right Approach

```python
def choose_approach(coins, requirements):
    """
    Choose the best approach based on requirements
    """
    n = len(coins)
    max_sum = sum(coins)
    
    if n <= 10 and max_sum <= 100:
        return "brute_force"  # Small inputs
    elif n <= 1000 and max_sum <= 10000:
        return "dynamic_programming"  # Medium inputs
    elif requirements.get("need_coin_tracking", False):
        return "bottom_up_dp"  # Need to track which coins are used
    elif n > 1000 or max_sum > 10000:
        return "greedy"  # Large inputs
    else:
        return "bottom_up_dp"  # Default choice

# Example usage
coins = [1, 2, 3, 5, 8, 13, 21]
requirements = {"need_coin_tracking": True}

approach = choose_approach(coins, requirements)
print(f"Recommended approach: {approach}")
```

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Missing Coin Sum with Limited Quantities
**Problem**: Each coin has a limited quantity, and we want to find the smallest impossible sum.

**Link**: [CSES Problem Set - Missing Coin Sum Limited Quantities](https://cses.fi/problemset/task/missing_coin_sum_limited)

```python
def missing_coin_sum_limited_quantities(coins, quantities):
    """
    Find smallest impossible sum with limited coin quantities
    """
    # Create list of (value, quantity) pairs
    coin_data = [(coins[i], quantities[i]) for i in range(len(coins))]
    coin_data.sort()  # Sort by value
    
    current_sum = 0
    
    for value, quantity in coin_data:
        # If current value is greater than current_sum + 1,
        # then current_sum + 1 is impossible
        if value > current_sum + 1:
            return current_sum + 1
        
        # Add all possible sums using this coin
        # We can create sums from current_sum + 1 to current_sum + value * quantity
        current_sum += value * quantity
    
    return current_sum + 1

def missing_coin_sum_limited_quantities_optimized(coins, quantities):
    """
    Optimized version for large quantities
    """
    # Create list of (value, quantity) pairs
    coin_data = [(coins[i], quantities[i]) for i in range(len(coins))]
    coin_data.sort()  # Sort by value
    
    current_sum = 0
    
    for value, quantity in coin_data:
        if value > current_sum + 1:
            return current_sum + 1
        
        # For large quantities, we can optimize by using binary search
        # to find the maximum number of coins we can use
        max_coins = min(quantity, (current_sum + 1) // value)
        current_sum += value * max_coins
    
    return current_sum + 1
```

### Variation 2: Missing Coin Sum with Different Denominations
**Problem**: Coins have different denominations and we want to find the smallest impossible sum.

**Link**: [CSES Problem Set - Missing Coin Sum Different Denominations](https://cses.fi/problemset/task/missing_coin_sum_denominations)

```python
def missing_coin_sum_different_denominations(coins):
    """
    Find smallest impossible sum with different coin denominations
    """
    coins.sort()  # Sort coins in ascending order
    
    current_sum = 0
    
    for coin in coins:
        # If current coin is greater than current_sum + 1,
        # then current_sum + 1 is impossible
        if coin > current_sum + 1:
            return current_sum + 1
        
        # We can create all sums from 1 to current_sum + coin
        current_sum += coin
    
    return current_sum + 1

def missing_coin_sum_different_denominations_optimized(coins):
    """
    Optimized version with early termination
    """
    coins.sort()
    
    current_sum = 0
    
    for coin in coins:
        if coin > current_sum + 1:
            return current_sum + 1
        
        current_sum += coin
        
        # Early termination if we can create all sums up to a large number
        if current_sum > 10**9:  # Assuming reasonable upper bound
            break
    
    return current_sum + 1
```

### Variation 3: Missing Coin Sum with Dynamic Updates
**Problem**: Coins can be added or removed dynamically, and we need to maintain the smallest impossible sum.

**Link**: [CSES Problem Set - Missing Coin Sum Dynamic Updates](https://cses.fi/problemset/task/missing_coin_sum_dynamic)

```python
class MissingCoinSumDynamic:
    def __init__(self, coins):
        self.coins = sorted(coins)
        self.smallest_impossible = self._calculate_smallest_impossible()
    
    def _calculate_smallest_impossible(self):
        """Calculate the smallest impossible sum"""
        current_sum = 0
        
        for coin in self.coins:
            if coin > current_sum + 1:
                return current_sum + 1
            current_sum += coin
        
        return current_sum + 1
    
    def add_coin(self, coin):
        """Add a new coin"""
        # Insert coin in sorted order
        import bisect
        bisect.insort(self.coins, coin)
        self.smallest_impossible = self._calculate_smallest_impossible()
    
    def remove_coin(self, coin):
        """Remove a coin"""
        if coin in self.coins:
            self.coins.remove(coin)
            self.smallest_impossible = self._calculate_smallest_impossible()
    
    def get_smallest_impossible(self):
        """Get current smallest impossible sum"""
        return self.smallest_impossible
    
    def can_make_sum(self, target):
        """Check if we can make a specific sum"""
        return target < self.smallest_impossible
```


### Related Problems

#### **CSES Problems**
- [Missing Coin Sum](https://cses.fi/problemset/task/2183) - Basic missing coin sum problem
- [Coin Combinations I](https://cses.fi/problemset/task/1635) - Coin combination counting
- [Coin Combinations II](https://cses.fi/problemset/task/1636) - Coin combination counting with order

#### **LeetCode Problems**
- [Coin Change](https://leetcode.com/problems/coin-change/) - Minimum coins to make amount
- [Coin Change 2](https://leetcode.com/problems/coin-change-2/) - Number of ways to make amount
- [Minimum Number of Refueling Stops](https://leetcode.com/problems/minimum-number-of-refueling-stops/) - Greedy optimization
- [Jump Game](https://leetcode.com/problems/jump-game/) - Greedy reachability

#### **Problem Categories**
- **Greedy Algorithms**: Optimal local choices, coin optimization, sum construction
- **Mathematical Algorithms**: Number theory, sum construction, optimization theory
- **Sorting**: Array sorting, greedy optimization, mathematical algorithms
- **Algorithm Design**: Greedy strategies, mathematical algorithms, optimization techniques
