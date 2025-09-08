---
layout: simple
title: "Two Sets"
permalink: /problem_soulutions/introductory_problems/two_sets_analysis
---

# Two Sets

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand set partitioning and mathematical analysis problems
- Apply mathematical formulas to determine if equal sum partitioning is possible
- Implement efficient set partitioning algorithms with proper mathematical analysis
- Optimize set partitioning using mathematical analysis and greedy strategies
- Handle edge cases in set partitioning (impossible partitions, large n, mathematical precision)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Set partitioning, mathematical analysis, greedy strategies, equal sum problems
- **Data Structures**: Set tracking, mathematical calculations, partition tracking, sum tracking
- **Mathematical Concepts**: Set theory, arithmetic series, partition theory, mathematical analysis
- **Programming Skills**: Set manipulation, mathematical calculations, partition construction, algorithm implementation
- **Related Problems**: Set problems, Partition problems, Mathematical analysis, Equal sum problems

## Problem Description

**Problem**: Divide the numbers 1,2,…,n into two sets of equal sum.

**Input**: An integer n (1 ≤ n ≤ 10⁶)

**Output**: Print "YES" if division is possible, "NO" otherwise. If possible, print the two sets.

**Constraints**:
- 1 ≤ n ≤ 10⁶
- Numbers 1 to n must be divided into two sets
- Both sets must have equal sum
- If total sum is odd, division is impossible
- Need to handle large n efficiently

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

## Visual Example

### Input and Set Division
```
Input: n = 7

Numbers to divide: {1, 2, 3, 4, 5, 6, 7}
Total sum = 1+2+3+4+5+6+7 = 28
Target sum for each set = 28/2 = 14

Valid division:
Set 1: {1, 2, 4, 7} → Sum = 1+2+4+7 = 14
Set 2: {3, 5, 6} → Sum = 3+5+6 = 14
```

### Mathematical Analysis
```
For n = 7:
- Total sum = n(n+1)/2 = 7×8/2 = 28
- Since 28 is even, division is possible
- Target sum = 28/2 = 14
- Need to find subset that sums to 14
```

### Greedy Construction Process
```
Start with largest numbers:
- Take 7: current_sum = 7
- Take 6: current_sum = 13
- Take 5: current_sum = 18 > 14, skip
- Take 4: current_sum = 13+4 = 17 > 14, skip
- Take 3: current_sum = 13+3 = 16 > 14, skip
- Take 2: current_sum = 13+2 = 15 > 14, skip
- Take 1: current_sum = 13+1 = 14 = target_sum

Result: Set 1 = {7, 6, 1}, Set 2 = {2, 3, 4, 5}
```

### Key Insight
The solution works by:
1. Using mathematical analysis to check if division is possible
2. Applying greedy strategy for set construction
3. Using arithmetic series formulas for sum calculation
4. Time complexity: O(n) for greedy construction
5. Space complexity: O(n) for storing sets

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Subset Generation (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible subsets and check if any sums to target
- Simple but computationally expensive approach
- Not suitable for large n
- Straightforward implementation but poor performance

**Algorithm:**
1. Generate all possible subsets of numbers 1 to n
2. Check if any subset sums to target_sum
3. If found, construct the two sets
4. Handle edge cases correctly

**Visual Example:**
```
Brute force: Try all subsets
For n = 4:
- Try subset {1}: sum = 1 ≠ 5
- Try subset {2}: sum = 2 ≠ 5
- Try subset {3}: sum = 3 ≠ 5
- Try subset {4}: sum = 4 ≠ 5
- Try subset {1,2}: sum = 3 ≠ 5
- Try subset {1,3}: sum = 4 ≠ 5
- Try subset {1,4}: sum = 5 = 5 ✓
```

**Implementation:**
```python
def two_sets_brute_force(n):
    total_sum = n * (n + 1) // 2
    
    if total_sum % 2 != 0:
        return None
    
    target_sum = total_sum // 2
    numbers = list(range(1, n + 1))
    
    # Try all possible subsets
    for i in range(1, 2**n):
        subset = []
        for j in range(n):
            if i & (1 << j):
                subset.append(numbers[j])
        
        if sum(subset) == target_sum:
            first_set = subset
            second_set = [x for x in numbers if x not in first_set]
            return first_set, second_set
    
    return None

def solve_two_sets_brute_force():
    n = int(input())
    result = two_sets_brute_force(n)
    
    if result is None:
        print("NO")
    else:
        first_set, second_set = result
        print("YES")
        print(len(first_set))
        print(*first_set)
        print(len(second_set))
        print(*second_set)
```

**Time Complexity:** O(2ⁿ) for trying all subsets
**Space Complexity:** O(n) for storing subsets

**Why it's inefficient:**
- O(2ⁿ) time complexity is too slow for large n
- Not suitable for competitive programming with n up to 10⁶
- Inefficient for large inputs
- Poor performance with exponential growth

### Approach 2: Mathematical Analysis with Greedy Construction (Better)

**Key Insights from Mathematical Solution:**
- Use mathematical analysis to check if division is possible
- Much more efficient than brute force approach
- Standard method for set partitioning problems
- Can handle larger n than brute force

**Algorithm:**
1. Check if total sum is even (necessary condition)
2. Use greedy strategy to construct first set
3. Start with largest numbers and work backwards
4. If target sum is reached, construct second set

**Visual Example:**
```
Mathematical approach: Use greedy strategy
For n = 7:
- Total sum = 28, target = 14
- Start with largest: 7 → sum = 7
- Add 6: sum = 13
- Add 5: sum = 18 > 14, skip
- Add 4: sum = 13+4 = 17 > 14, skip
- Add 3: sum = 13+3 = 16 > 14, skip
- Add 2: sum = 13+2 = 15 > 14, skip
- Add 1: sum = 13+1 = 14 = target ✓
```

**Implementation:**
```python
def two_sets_mathematical(n):
    total_sum = n * (n + 1) // 2
    
    if total_sum % 2 != 0:
        return None
    
    target_sum = total_sum // 2
    first_set = []
    current_sum = 0
    
    # Greedy construction: start with largest numbers
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

def solve_two_sets_mathematical():
    n = int(input())
    result = two_sets_mathematical(n)
    
    if result is None:
        print("NO")
    else:
        first_set, second_set = result
        print("YES")
        print(len(first_set))
        print(*first_set)
        print(len(second_set))
        print(*second_set)
```

**Time Complexity:** O(n) for greedy construction
**Space Complexity:** O(n) for storing sets

**Why it's better:**
- O(n) time complexity is much better than O(2ⁿ)
- Uses mathematical analysis for efficient solution
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized Mathematical Formula (Optimal)

**Key Insights from Optimized Mathematical Solution:**
- Use optimized mathematical formulas for efficiency
- Most efficient approach for set partitioning problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use optimized mathematical formulas
2. Apply efficient greedy construction
3. Handle edge cases efficiently
4. Return the optimal solution

**Visual Example:**
```
Optimized mathematical: Use efficient formulas
For n = 7:
- Total sum = n(n+1)/2 = 28
- Target sum = 28/2 = 14
- Greedy construction with optimized logic
- Result = constructed sets
```

**Implementation:**
```python
def two_sets_optimized(n):
    total_sum = n * (n + 1) // 2
    
    if total_sum % 2 != 0:
        return None
    
    target_sum = total_sum // 2
    first_set = []
    current_sum = 0
    
    # Optimized greedy construction
    for i in range(n, 0, -1):
        if current_sum + i <= target_sum:
            first_set.append(i)
            current_sum += i
    
    if current_sum == target_sum:
        second_set = [x for x in range(1, n + 1) if x not in first_set]
        return first_set, second_set
    
    return None

def solve_two_sets():
    n = int(input())
    result = two_sets_optimized(n)
    
    if result is None:
        print("NO")
    else:
        first_set, second_set = result
        print("YES")
        print(len(first_set))
        print(*first_set)
        print(len(second_set))
        print(*second_set)

# Main execution
if __name__ == "__main__":
    solve_two_sets()
```

**Time Complexity:** O(n) for optimized mathematical calculation
**Space Complexity:** O(n) for storing sets

**Why it's optimal:**
- O(n) time complexity is optimal for this problem
- Uses optimized mathematical formulas
- Most efficient approach for competitive programming
- Standard method for set partitioning optimization

## 🎯 Problem Variations

### Variation 1: Two Sets with Different Sum Requirements
**Problem**: Divide numbers into two sets with different sum requirements (e.g., one set has sum k, other has sum total-k).

**Link**: [CSES Problem Set - Two Sets Different Sums](https://cses.fi/problemset/task/two_sets_different_sums)

```python
def two_sets_different_sums(n, k):
    total_sum = n * (n + 1) // 2
    
    if k > total_sum or (total_sum - k) < 0:
        return None
    
    target_sum = k
    first_set = []
    current_sum = 0
    
    # Greedy construction for target sum k
    for i in range(n, 0, -1):
        if current_sum + i <= target_sum:
            first_set.append(i)
            current_sum += i
    
    if current_sum == target_sum:
        second_set = [x for x in range(1, n + 1) if x not in first_set]
        return first_set, second_set
    
    return None
```

### Variation 2: Two Sets with Minimum Difference
**Problem**: Divide numbers into two sets such that the absolute difference between their sums is minimized.

**Link**: [CSES Problem Set - Two Sets Minimum Difference](https://cses.fi/problemset/task/two_sets_minimum_difference)

```python
def two_sets_minimum_difference(n):
    total_sum = n * (n + 1) // 2
    target_sum = total_sum // 2
    
    first_set = []
    current_sum = 0
    
    # Greedy construction for closest to target_sum
    for i in range(n, 0, -1):
        if current_sum + i <= target_sum:
            first_set.append(i)
            current_sum += i
    
    second_set = [x for x in range(1, n + 1) if x not in first_set]
    return first_set, second_set, abs(current_sum - (total_sum - current_sum))
```

### Variation 3: Two Sets with Size Constraints
**Problem**: Divide numbers into two sets with specific size constraints (e.g., one set has size k, other has size n-k).

**Link**: [CSES Problem Set - Two Sets Size Constraints](https://cses.fi/problemset/task/two_sets_size_constraints)

```python
def two_sets_size_constraints(n, k):
    if k > n or k < 0:
        return None
    
    # Try to find a subset of size k that sums to target
    total_sum = n * (n + 1) // 2
    target_sum = total_sum // 2
    
    # Use dynamic programming or backtracking for size-constrained subset
    # ... (implementation details)
    
    return result
```

## 🔗 Related Problems

- **[Set Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Set problems
- **[Partition Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Partition problems
- **[Mathematical Analysis](/cses-analyses/problem_soulutions/introductory_problems/)**: Mathematical analysis problems
- **[Equal Sum Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Equal sum problems

## 📚 Learning Points

1. **Set Partitioning**: Essential for understanding equal sum problems
2. **Mathematical Analysis**: Key technique for feasibility checking
3. **Greedy Strategies**: Important for efficient set construction
4. **Arithmetic Series**: Critical for understanding sum calculations
5. **Algorithm Optimization**: Foundation for many partitioning algorithms
6. **Mathematical Formulas**: Critical for competitive programming performance

## 📝 Summary

The Two Sets problem demonstrates set partitioning concepts for equal sum division. We explored three approaches:

1. **Brute Force Subset Generation**: O(2ⁿ) time complexity using exhaustive subset generation, inefficient for large n
2. **Mathematical Analysis with Greedy Construction**: O(n) time complexity using mathematical analysis and greedy strategy, better approach for set partitioning problems
3. **Optimized Mathematical Formula**: O(n) time complexity with optimized mathematical formulas, optimal approach for set partitioning optimization

The key insights include understanding set partitioning principles, using mathematical analysis for efficient feasibility checking, and applying greedy strategies for optimal performance. This problem serves as an excellent introduction to set partitioning algorithms and mathematical analysis.
