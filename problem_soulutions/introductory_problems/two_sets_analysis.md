---
layout: simple
title: "Two Sets"
permalink: /problem_soulutions/introductory_problems/two_sets_analysis
---

# Two Sets

## Problem Description

**Problem**: Divide the numbers 1,2,…,n into two sets of equal sum.

**Input**: An integer n (1 ≤ n ≤ 10⁶)

**Output**: Print "YES" if division is possible, "NO" otherwise. If possible, print the two sets.

**Example**:
```
Input: 7

Output:
YES
4
1 2 4 7
3
3 5 6

Explanation: Sum of first set = 1+2+4+7 = 14, Sum of second set = 3+5+6 = 14
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Divide numbers 1 to n into two sets
- Both sets must have equal sum
- Find if this is possible and construct the sets

**Key Observations:**
- Total sum = n(n+1)/2 (sum of first n natural numbers)
- For equal division, total sum must be even
- If total sum is odd, division is impossible
- We need to find a subset that sums to total_sum/2

### Step 2: Mathematical Analysis
**Idea**: Check if total sum is even, then construct the sets.

```python
def two_sets_math(n):
    total_sum = n * (n + 1) // 2
    
    if total_sum % 2 != 0:
        return None  # Impossible if total sum is odd
    
    target_sum = total_sum // 2
    
    # Try to construct the first set
    first_set = []
    current_sum = 0
    
    # Start from the largest number and work backwards
    for i in range(n, 0, -1):
        if current_sum + i <= target_sum:
            first_set.append(i)
            current_sum += i
            if current_sum == target_sum:
                break
    
    if current_sum == target_sum:
        second_set = [x for x in range(1, n + 1) if x not in first_set]
        return first_set, second_set
    
    return None
```

**Why this works:**
- Check if total sum is even (necessary condition)
- Use greedy approach: take largest numbers first
- If we can reach target sum, we have a solution

### Step 3: Optimized Construction
**Idea**: Use a more efficient construction method.

```python
def two_sets_optimized(n):
    total_sum = n * (n + 1) // 2
    
    if total_sum % 2 != 0:
        return None
    
    target_sum = total_sum // 2
    first_set = []
    current_sum = 0
    
    # Use a more systematic approach
    for i in range(n, 0, -1):
        if current_sum + i <= target_sum:
            first_set.append(i)
            current_sum += i
    
    if current_sum == target_sum:
        second_set = [x for x in range(1, n + 1) if x not in first_set]
        return first_set, second_set
    
    return None
```

**Why this is better:**
- More systematic construction
- Handles edge cases better
- Clearer logic

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_two_sets():
    n = int(input())
    
    total_sum = n * (n + 1) // 2
    
    if total_sum % 2 != 0:
        print("NO")
        return
    
    target_sum = total_sum // 2
    first_set = []
    current_sum = 0
    
    # Construct first set
    for i in range(n, 0, -1):
        if current_sum + i <= target_sum:
            first_set.append(i)
            current_sum += i
    
    if current_sum == target_sum:
        print("YES")
        print(len(first_set))
        print(*first_set)
        
        second_set = [x for x in range(1, n + 1) if x not in first_set]
        print(len(second_set))
        print(*second_set)
    else:
        print("NO")

# Main execution
if __name__ == "__main__":
    solve_two_sets()
```

**Why this works:**
- Efficient mathematical approach
- Handles all cases correctly
- Constructs sets systematically

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (3, True),   # 1+2+3=6, can divide into {1,2} and {3}
        (4, True),   # 1+2+3+4=10, can divide into {1,4} and {2,3}
        (5, False),  # 1+2+3+4+5=15 (odd), cannot divide
        (7, True),   # 1+2+3+4+5+6+7=28, can divide
    ]
    
    for n, expected in test_cases:
        result = solve_test(n)
        print(f"n = {n}")
        print(f"Expected: {'YES' if expected else 'NO'}")
        print(f"Got: {result}")
        print(f"{'✓ PASS' if (result == 'YES') == expected else '✗ FAIL'}")
        print()

def solve_test(n):
    total_sum = n * (n + 1) // 2
    
    if total_sum % 2 != 0:
        return "NO"
    
    target_sum = total_sum // 2
    first_set = []
    current_sum = 0
    
    for i in range(n, 0, -1):
        if current_sum + i <= target_sum:
            first_set.append(i)
            current_sum += i
    
    if current_sum == target_sum:
        return "YES"
    else:
        return "NO"

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - we iterate through numbers once
- **Space**: O(n) - to store the sets

### Why This Solution Works
- **Mathematical**: Uses mathematical properties of sum
- **Greedy**: Takes largest numbers first
- **Correct**: Handles all cases properly

## 🎯 Key Insights

### 1. **Sum Properties**
- Total sum = n(n+1)/2 (sum of first n natural numbers)
- For equal division, total sum must be even
- If total sum is odd, division is impossible

### 2. **Greedy Construction**
- Start with largest numbers
- Take numbers that fit within target sum
- This greedy approach works for this problem

### 3. **Set Construction**
- Build first set greedily
- Second set is remaining numbers
- Verify both sets have equal sum

## 🎯 Problem Variations

### Variation 1: Three Sets
**Problem**: Divide numbers into three sets of equal sum.

```python
def three_sets(n):
    total_sum = n * (n + 1) // 2
    
    if total_sum % 3 != 0:
        return None
    
    target_sum = total_sum // 3
    sets = [[], [], []]
    current_sums = [0, 0, 0]
    
    # Try to construct three sets
    for i in range(n, 0, -1):
        # Find set with minimum sum
        min_set = min(range(3), key=lambda x: current_sums[x])
        if current_sums[min_set] + i <= target_sum:
            sets[min_set].append(i)
            current_sums[min_set] += i
    
    # Check if all sets have target sum
    if all(s == target_sum for s in current_sums):
        return sets
    
    return None
```

### Variation 2: Minimum Difference
**Problem**: Divide numbers into two sets with minimum difference.

```python
def minimum_difference_sets(n):
    numbers = list(range(1, n + 1))
    total_sum = sum(numbers)
    
    # Use dynamic programming to find closest sum to total_sum/2
    target = total_sum // 2
    dp = [False] * (target + 1)
    dp[0] = True
    
    for num in numbers:
        for i in range(target, num - 1, -1):
            if dp[i - num]:
                dp[i] = True
    
    # Find largest achievable sum <= target
    first_sum = 0
    for i in range(target, -1, -1):
        if dp[i]:
            first_sum = i
            break
    
    # Construct sets
    first_set = []
    current_sum = first_sum
    for num in reversed(numbers):
        if current_sum >= num and dp[current_sum - num]:
            first_set.append(num)
            current_sum -= num
    
    second_set = [x for x in numbers if x not in first_set]
    return first_set, second_set, abs(first_sum - (total_sum - first_sum))
```

### Variation 3: Weighted Sets
**Problem**: Each number has a weight. Divide into two sets with equal total weight.

```python
def weighted_sets(n, weights):
    # weights[i] = weight of number i+1
    total_weight = sum(weights)
    
    if total_weight % 2 != 0:
        return None
    
    target_weight = total_weight // 2
    
    # Use dynamic programming
    dp = [False] * (target_weight + 1)
    dp[0] = True
    
    for i, weight in enumerate(weights):
        for j in range(target_weight, weight - 1, -1):
            if dp[j - weight]:
                dp[j] = True
    
    if not dp[target_weight]:
        return None
    
    # Reconstruct first set
    first_set = []
    current_weight = target_weight
    for i in range(n - 1, -1, -1):
        if current_weight >= weights[i] and dp[current_weight - weights[i]]:
            first_set.append(i + 1)
            current_weight -= weights[i]
    
    second_set = [x for x in range(1, n + 1) if x not in first_set]
    return first_set, second_set
```

### Variation 4: Constrained Sets
**Problem**: Divide numbers with constraints on set sizes.

```python
def constrained_sets(n, min_size, max_size):
    total_sum = n * (n + 1) // 2
    
    if total_sum % 2 != 0:
        return None
    
    target_sum = total_sum // 2
    
    # Try different set sizes within constraints
    for size in range(min_size, min(max_size + 1, n // 2 + 1)):
        # Try to find a set of this size with target sum
        if size * (size + 1) // 2 <= target_sum <= (n - size + 1 + n) * size // 2:
            # This size is theoretically possible
            first_set = []
            current_sum = 0
            
            # Try to construct set of this size
            for i in range(n, 0, -1):
                if len(first_set) < size and current_sum + i <= target_sum:
                    first_set.append(i)
                    current_sum += i
                
                if len(first_set) == size and current_sum == target_sum:
                    second_set = [x for x in range(1, n + 1) if x not in first_set]
                    return first_set, second_set
    
    return None
```

## 🔗 Related Problems

- **[Apple Division](/cses-analyses/problem_soulutions/introductory_problems/apple_division_analysis)**: Subset sum problems
- **[Coin Piles](/cses-analyses/problem_soulutions/introductory_problems/coin_piles_analysis)**: Mathematical division problems
- **[Two Knights](/cses-analyses/problem_soulutions/introductory_problems/two_knights_analysis)**: Counting problems

## 📚 Learning Points

1. **Mathematical Analysis**: Understanding sum properties
2. **Greedy Algorithms**: Using greedy approach for construction
3. **Subset Sum**: Finding subsets with target sum
4. **Optimization**: Avoiding brute force approaches

---

**This is a great introduction to mathematical analysis and subset sum problems!** 🎯 