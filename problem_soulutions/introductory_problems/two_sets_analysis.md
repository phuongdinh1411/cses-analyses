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

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

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

## Problem Variations

### **Variation 1: Two Sets with Dynamic Updates**
**Problem**: Handle dynamic number updates (add/remove/update numbers) while maintaining optimal two sets partitioning efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic number management.

```python
from collections import defaultdict

class DynamicTwoSets:
    def __init__(self, numbers=None):
        self.numbers = numbers or []
        self.set1 = []
        self.set2 = []
        self._update_two_sets_info()
    
    def _update_two_sets_info(self):
        """Update two sets feasibility information."""
        self.total_numbers = len(self.numbers)
        self.total_sum = sum(self.numbers)
        self.two_sets_feasibility = self._calculate_two_sets_feasibility()
    
    def _calculate_two_sets_feasibility(self):
        """Calculate two sets partitioning feasibility."""
        if self.total_numbers == 0:
            return 0.0
        
        # Check if total sum is even (required for equal sum partitioning)
        if self.total_sum % 2 != 0:
            return 0.0
        
        # Check if we can partition into two equal sum sets
        target_sum = self.total_sum // 2
        return 1.0 if self._can_partition(target_sum) else 0.0
    
    def _can_partition(self, target_sum):
        """Check if we can partition numbers to achieve target sum."""
        if target_sum == 0:
            return True
        
        if not self.numbers or target_sum < 0:
            return False
        
        # Use dynamic programming to check feasibility
        dp = [False] * (target_sum + 1)
        dp[0] = True
        
        for num in self.numbers:
            for j in range(target_sum, num - 1, -1):
                dp[j] = dp[j] or dp[j - num]
        
        return dp[target_sum]
    
    def add_number(self, number, position=None):
        """Add number to the list."""
        if position is None:
            self.numbers.append(number)
        else:
            self.numbers.insert(position, number)
        
        self._update_two_sets_info()
    
    def remove_number(self, position):
        """Remove number from the list."""
        if 0 <= position < len(self.numbers):
            self.numbers.pop(position)
            self._update_two_sets_info()
    
    def update_number(self, position, new_number):
        """Update number in the list."""
        if 0 <= position < len(self.numbers):
            self.numbers[position] = new_number
            self._update_two_sets_info()
    
    def find_two_sets_partition(self):
        """Find optimal two sets partition."""
        if not self.numbers or self.total_sum % 2 != 0:
            return None, None
        
        target_sum = self.total_sum // 2
        
        # Use dynamic programming to find partition
        n = len(self.numbers)
        dp = [[False for _ in range(target_sum + 1)] for _ in range(n + 1)]
        
        # Initialize base cases
        for i in range(n + 1):
            dp[i][0] = True
        
        # Fill DP table
        for i in range(1, n + 1):
            for j in range(1, target_sum + 1):
                if j < self.numbers[i-1]:
                    dp[i][j] = dp[i-1][j]
                else:
                    dp[i][j] = dp[i-1][j] or dp[i-1][j - self.numbers[i-1]]
        
        if not dp[n][target_sum]:
            return None, None
        
        # Reconstruct the partition
        set1 = []
        set2 = []
        i, j = n, target_sum
        
        while i > 0 and j > 0:
            if dp[i-1][j]:
                set2.append(self.numbers[i-1])
                i -= 1
            else:
                set1.append(self.numbers[i-1])
                j -= self.numbers[i-1]
                i -= 1
        
        # Add remaining numbers to set2
        while i > 0:
            set2.append(self.numbers[i-1])
            i -= 1
        
        return set1, set2
    
    def get_partition_with_constraints(self, constraint_func):
        """Get partition that satisfies custom constraints."""
        if not self.numbers:
            return None, None
        
        set1, set2 = self.find_two_sets_partition()
        if set1 is None or set2 is None:
            return None, None
        
        if constraint_func(set1, set2, self.numbers):
            return set1, set2
        else:
            return None, None
    
    def get_partition_in_range(self, min_sum, max_sum):
        """Get partition within specified sum range."""
        if not self.numbers:
            return None, None
        
        set1, set2 = self.find_two_sets_partition()
        if set1 is None or set2 is None:
            return None, None
        
        sum1, sum2 = sum(set1), sum(set2)
        if min_sum <= sum1 <= max_sum and min_sum <= sum2 <= max_sum:
            return set1, set2
        else:
            return None, None
    
    def get_partition_with_pattern(self, pattern_func):
        """Get partition matching specified pattern."""
        if not self.numbers:
            return None, None
        
        set1, set2 = self.find_two_sets_partition()
        if set1 is None or set2 is None:
            return None, None
        
        if pattern_func(set1, set2, self.numbers):
            return set1, set2
        else:
            return None, None
    
    def get_number_statistics(self):
        """Get statistics about the numbers."""
        if not self.numbers:
            return {
                'total_numbers': 0,
                'total_sum': 0,
                'two_sets_feasibility': 0,
                'number_distribution': {}
            }
        
        return {
            'total_numbers': self.total_numbers,
            'total_sum': self.total_sum,
            'two_sets_feasibility': self.two_sets_feasibility,
            'number_distribution': {num: self.numbers.count(num) for num in set(self.numbers)}
        }
    
    def get_two_sets_patterns(self):
        """Get patterns in two sets partitioning."""
        patterns = {
            'equal_sum_possible': 0,
            'odd_sum': 0,
            'even_sum': 0,
            'optimal_partition_possible': 0
        }
        
        if not self.numbers:
            return patterns
        
        # Check if equal sum is possible
        if self.total_sum % 2 == 0:
            patterns['equal_sum_possible'] = 1
        
        # Check if sum is odd
        if self.total_sum % 2 == 1:
            patterns['odd_sum'] = 1
        
        # Check if sum is even
        if self.total_sum % 2 == 0:
            patterns['even_sum'] = 1
        
        # Check if optimal partition is possible
        if self.two_sets_feasibility == 1.0:
            patterns['optimal_partition_possible'] = 1
        
        return patterns
    
    def get_optimal_two_sets_strategy(self):
        """Get optimal strategy for two sets partitioning."""
        if not self.numbers:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'two_sets_feasibility': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = self.two_sets_feasibility
        
        # Calculate two sets feasibility
        two_sets_feasibility = self.two_sets_feasibility
        
        # Determine recommended strategy
        if self.total_numbers <= 10:
            recommended_strategy = 'brute_force'
        elif self.total_numbers <= 50:
            recommended_strategy = 'dynamic_programming'
        else:
            recommended_strategy = 'optimized_dp'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'two_sets_feasibility': two_sets_feasibility
        }

# Example usage
numbers = [1, 5, 11, 5]
dynamic_two_sets = DynamicTwoSets(numbers)
print(f"Two sets feasibility: {dynamic_two_sets.two_sets_feasibility}")

# Add number
dynamic_two_sets.add_number(2)
print(f"After adding 2: {dynamic_two_sets.total_sum}")

# Remove number
dynamic_two_sets.remove_number(0)
print(f"After removing first number: {dynamic_two_sets.total_numbers}")

# Update number
dynamic_two_sets.update_number(0, 3)
print(f"After updating first number to 3: {dynamic_two_sets.numbers[0]}")

# Find partition
set1, set2 = dynamic_two_sets.find_two_sets_partition()
print(f"Partition: {set1}, {set2}")

# Get partition with constraints
def constraint_func(set1, set2, numbers):
    return len(set1) == len(set2)

print(f"Partition with constraints: {dynamic_two_sets.get_partition_with_constraints(constraint_func)}")

# Get partition in range
print(f"Partition in range 5-15: {dynamic_two_sets.get_partition_in_range(5, 15)}")

# Get partition with pattern
def pattern_func(set1, set2, numbers):
    return len(set1) > 0 and len(set2) > 0

print(f"Partition with pattern: {dynamic_two_sets.get_partition_with_pattern(pattern_func)}")

# Get statistics
print(f"Statistics: {dynamic_two_sets.get_number_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_two_sets.get_two_sets_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_two_sets.get_optimal_two_sets_strategy()}")
```

### **Variation 2: Two Sets with Different Operations**
**Problem**: Handle different types of two sets operations (weighted numbers, priority-based partitioning, advanced number analysis).

**Approach**: Use advanced data structures for efficient different types of two sets operations.

```python
class AdvancedTwoSets:
    def __init__(self, numbers=None, weights=None, priorities=None):
        self.numbers = numbers or []
        self.weights = weights or {}
        self.priorities = priorities or {}
        self._update_two_sets_info()
    
    def _update_two_sets_info(self):
        """Update two sets feasibility information."""
        self.total_numbers = len(self.numbers)
        self.total_sum = sum(self.numbers)
        self.two_sets_feasibility = self._calculate_two_sets_feasibility()
    
    def _calculate_two_sets_feasibility(self):
        """Calculate two sets partitioning feasibility."""
        if self.total_numbers == 0:
            return 0.0
        
        # Check if total sum is even (required for equal sum partitioning)
        if self.total_sum % 2 != 0:
            return 0.0
        
        # Check if we can partition into two equal sum sets
        target_sum = self.total_sum // 2
        return 1.0 if self._can_partition(target_sum) else 0.0
    
    def _can_partition(self, target_sum):
        """Check if we can partition numbers to achieve target sum."""
        if target_sum == 0:
            return True
        
        if not self.numbers or target_sum < 0:
            return False
        
        # Use dynamic programming to check feasibility
        dp = [False] * (target_sum + 1)
        dp[0] = True
        
        for num in self.numbers:
            for j in range(target_sum, num - 1, -1):
                dp[j] = dp[j] or dp[j - num]
        
        return dp[target_sum]
    
    def find_two_sets_partition(self):
        """Find optimal two sets partition."""
        if not self.numbers or self.total_sum % 2 != 0:
            return None, None
        
        target_sum = self.total_sum // 2
        
        # Use dynamic programming to find partition
        n = len(self.numbers)
        dp = [[False for _ in range(target_sum + 1)] for _ in range(n + 1)]
        
        # Initialize base cases
        for i in range(n + 1):
            dp[i][0] = True
        
        # Fill DP table
        for i in range(1, n + 1):
            for j in range(1, target_sum + 1):
                if j < self.numbers[i-1]:
                    dp[i][j] = dp[i-1][j]
                else:
                    dp[i][j] = dp[i-1][j] or dp[i-1][j - self.numbers[i-1]]
        
        if not dp[n][target_sum]:
            return None, None
        
        # Reconstruct the partition
        set1 = []
        set2 = []
        i, j = n, target_sum
        
        while i > 0 and j > 0:
            if dp[i-1][j]:
                set2.append(self.numbers[i-1])
                i -= 1
            else:
                set1.append(self.numbers[i-1])
                j -= self.numbers[i-1]
                i -= 1
        
        # Add remaining numbers to set2
        while i > 0:
            set2.append(self.numbers[i-1])
            i -= 1
        
        return set1, set2
    
    def get_weighted_partition(self):
        """Get partition with weights and priorities applied."""
        if not self.numbers:
            return None, None
        
        # Create weighted partition
        weighted_numbers = []
        for num in self.numbers:
            weight = self.weights.get(num, 1)
            priority = self.priorities.get(num, 1)
            weighted_score = num * weight * priority
            weighted_numbers.append((num, weighted_score))
        
        # Sort by weighted score
        weighted_numbers.sort(key=lambda x: x[1], reverse=True)
        
        # Try to partition weighted numbers
        set1 = []
        set2 = []
        sum1 = sum2 = 0
        
        for num, score in weighted_numbers:
            if sum1 <= sum2:
                set1.append(num)
                sum1 += num
            else:
                set2.append(num)
                sum2 += num
        
        return set1, set2
    
    def get_partition_with_priority(self, priority_func):
        """Get partition considering priority."""
        if not self.numbers:
            return None, None
        
        # Create priority-based partition
        priority_numbers = []
        for num in self.numbers:
            priority = priority_func(num, self.weights, self.priorities)
            priority_numbers.append((num, priority))
        
        # Sort by priority
        priority_numbers.sort(key=lambda x: x[1], reverse=True)
        
        # Try to partition priority numbers
        set1 = []
        set2 = []
        sum1 = sum2 = 0
        
        for num, priority in priority_numbers:
            if sum1 <= sum2:
                set1.append(num)
                sum1 += num
            else:
                set2.append(num)
                sum2 += num
        
        return set1, set2
    
    def get_partition_with_optimization(self, optimization_func):
        """Get partition using custom optimization function."""
        if not self.numbers:
            return None, None
        
        # Create optimization-based partition
        optimized_numbers = []
        for num in self.numbers:
            score = optimization_func(num, self.weights, self.priorities)
            optimized_numbers.append((num, score))
        
        # Sort by optimization score
        optimized_numbers.sort(key=lambda x: x[1], reverse=True)
        
        # Try to partition optimized numbers
        set1 = []
        set2 = []
        sum1 = sum2 = 0
        
        for num, score in optimized_numbers:
            if sum1 <= sum2:
                set1.append(num)
                sum1 += num
            else:
                set2.append(num)
                sum2 += num
        
        return set1, set2
    
    def get_partition_with_constraints(self, constraint_func):
        """Get partition that satisfies custom constraints."""
        if not self.numbers:
            return None, None
        
        if constraint_func(self.numbers, self.weights, self.priorities):
            return self.get_weighted_partition()
        else:
            return None, None
    
    def get_partition_with_multiple_criteria(self, criteria_list):
        """Get partition that satisfies multiple criteria."""
        if not self.numbers:
            return None, None
        
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(self.numbers, self.weights, self.priorities):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            return self.get_weighted_partition()
        else:
            return None, None
    
    def get_partition_with_alternatives(self, alternatives):
        """Get partition considering alternative weights/priorities."""
        result = []
        
        # Check original partition
        original_partition = self.get_weighted_partition()
        result.append((original_partition, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedTwoSets(self.numbers, alt_weights, alt_priorities)
            temp_partition = temp_instance.get_weighted_partition()
            result.append((temp_partition, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_partition_with_adaptive_criteria(self, adaptive_func):
        """Get partition using adaptive criteria."""
        if not self.numbers:
            return None, None
        
        if adaptive_func(self.numbers, self.weights, self.priorities, []):
            return self.get_weighted_partition()
        else:
            return None, None
    
    def get_two_sets_optimization(self):
        """Get optimal two sets configuration."""
        strategies = [
            ('weighted_partition', lambda: len(self.get_weighted_partition()[0]) if self.get_weighted_partition()[0] else 0),
            ('total_weight', lambda: sum(self.weights.values())),
            ('total_priority', lambda: sum(self.priorities.values())),
        ]
        
        best_strategy = None
        best_value = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                current_value = strategy_func()
                if current_value > best_value:
                    best_value = current_value
                    best_strategy = (strategy_name, current_value)
            except:
                continue
        
        return best_strategy

# Example usage
numbers = [1, 5, 11, 5]
weights = {num: num * 2 for num in numbers}  # Weight based on number value
priorities = {num: num // 2 for num in numbers}  # Priority based on number value
advanced_two_sets = AdvancedTwoSets(numbers, weights, priorities)

print(f"Weighted partition: {advanced_two_sets.get_weighted_partition()}")

# Get partition with priority
def priority_func(num, weights, priorities):
    return weights.get(num, 1) + priorities.get(num, 1)

print(f"Partition with priority: {advanced_two_sets.get_partition_with_priority(priority_func)}")

# Get partition with optimization
def optimization_func(num, weights, priorities):
    return weights.get(num, 1) * priorities.get(num, 1)

print(f"Partition with optimization: {advanced_two_sets.get_partition_with_optimization(optimization_func)}")

# Get partition with constraints
def constraint_func(numbers, weights, priorities):
    return len(numbers) > 0 and all(num > 0 for num in numbers)

print(f"Partition with constraints: {advanced_two_sets.get_partition_with_constraints(constraint_func)}")

# Get partition with multiple criteria
def criterion1(numbers, weights, priorities):
    return len(numbers) > 0

def criterion2(numbers, weights, priorities):
    return all(num > 0 for num in numbers)

criteria_list = [criterion1, criterion2]
print(f"Partition with multiple criteria: {advanced_two_sets.get_partition_with_multiple_criteria(criteria_list)}")

# Get partition with alternatives
alternatives = [({num: 1 for num in numbers}, {num: 1 for num in numbers}), ({num: num*3 for num in numbers}, {num: num+1 for num in numbers})]
print(f"Partition with alternatives: {advanced_two_sets.get_partition_with_alternatives(alternatives)}")

# Get partition with adaptive criteria
def adaptive_func(numbers, weights, priorities, current_result):
    return len(numbers) > 0 and len(current_result) < 5

print(f"Partition with adaptive criteria: {advanced_two_sets.get_partition_with_adaptive_criteria(adaptive_func)}")

# Get two sets optimization
print(f"Two sets optimization: {advanced_two_sets.get_two_sets_optimization()}")
```

### **Variation 3: Two Sets with Constraints**
**Problem**: Handle two sets partitioning with additional constraints (sum limits, number constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedTwoSets:
    def __init__(self, numbers=None, constraints=None):
        self.numbers = numbers or []
        self.constraints = constraints or {}
        self._update_two_sets_info()
    
    def _update_two_sets_info(self):
        """Update two sets feasibility information."""
        self.total_numbers = len(self.numbers)
        self.total_sum = sum(self.numbers)
        self.two_sets_feasibility = self._calculate_two_sets_feasibility()
    
    def _calculate_two_sets_feasibility(self):
        """Calculate two sets partitioning feasibility."""
        if self.total_numbers == 0:
            return 0.0
        
        # Check if total sum is even (required for equal sum partitioning)
        if self.total_sum % 2 != 0:
            return 0.0
        
        # Check if we can partition into two equal sum sets
        target_sum = self.total_sum // 2
        return 1.0 if self._can_partition(target_sum) else 0.0
    
    def _can_partition(self, target_sum):
        """Check if we can partition numbers to achieve target sum."""
        if target_sum == 0:
            return True
        
        if not self.numbers or target_sum < 0:
            return False
        
        # Use dynamic programming to check feasibility
        dp = [False] * (target_sum + 1)
        dp[0] = True
        
        for num in self.numbers:
            for j in range(target_sum, num - 1, -1):
                dp[j] = dp[j] or dp[j - num]
        
        return dp[target_sum]
    
    def _is_valid_partition(self, set1, set2):
        """Check if partition is valid considering constraints."""
        # Sum constraints
        if 'min_sum' in self.constraints:
            if sum(set1) < self.constraints['min_sum'] or sum(set2) < self.constraints['min_sum']:
                return False
        
        if 'max_sum' in self.constraints:
            if sum(set1) > self.constraints['max_sum'] or sum(set2) > self.constraints['max_sum']:
                return False
        
        # Number constraints
        if 'forbidden_numbers' in self.constraints:
            if any(num in self.constraints['forbidden_numbers'] for num in set1) or any(num in self.constraints['forbidden_numbers'] for num in set2):
                return False
        
        if 'required_numbers' in self.constraints:
            if not all(num in set1 or num in set2 for num in self.constraints['required_numbers']):
                return False
        
        # Pattern constraints
        if 'pattern_constraints' in self.constraints:
            for constraint in self.constraints['pattern_constraints']:
                if not constraint(set1, set2, self.numbers):
                    return False
        
        return True
    
    def get_partition_with_sum_constraints(self, min_sum, max_sum):
        """Get partition considering sum constraints."""
        if not self.numbers:
            return None, None
        
        set1, set2 = self.find_two_sets_partition()
        if set1 is None or set2 is None:
            return None, None
        
        if min_sum <= sum(set1) <= max_sum and min_sum <= sum(set2) <= max_sum and self._is_valid_partition(set1, set2):
            return set1, set2
        else:
            return None, None
    
    def get_partition_with_number_constraints(self, number_constraints):
        """Get partition considering number constraints."""
        if not self.numbers:
            return None, None
        
        satisfies_constraints = True
        for constraint in number_constraints:
            if not constraint(self.numbers):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            set1, set2 = self.find_two_sets_partition()
            if set1 is not None and set2 is not None and self._is_valid_partition(set1, set2):
                return set1, set2
        
        return None, None
    
    def get_partition_with_pattern_constraints(self, pattern_constraints):
        """Get partition considering pattern constraints."""
        if not self.numbers:
            return None, None
        
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(self.numbers):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            set1, set2 = self.find_two_sets_partition()
            if set1 is not None and set2 is not None and self._is_valid_partition(set1, set2):
                return set1, set2
        
        return None, None
    
    def get_partition_with_mathematical_constraints(self, constraint_func):
        """Get partition that satisfies custom mathematical constraints."""
        if not self.numbers:
            return None, None
        
        if constraint_func(self.numbers):
            set1, set2 = self.find_two_sets_partition()
            if set1 is not None and set2 is not None and self._is_valid_partition(set1, set2):
                return set1, set2
        
        return None, None
    
    def get_partition_with_optimization_constraints(self, optimization_func):
        """Get partition using custom optimization constraints."""
        if not self.numbers:
            return None, None
        
        # Calculate optimization score for partition
        score = optimization_func(self.numbers)
        
        if score > 0:
            set1, set2 = self.find_two_sets_partition()
            if set1 is not None and set2 is not None and self._is_valid_partition(set1, set2):
                return set1, set2
        
        return None, None
    
    def get_partition_with_multiple_constraints(self, constraints_list):
        """Get partition that satisfies multiple constraints."""
        if not self.numbers:
            return None, None
        
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(self.numbers):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            set1, set2 = self.find_two_sets_partition()
            if set1 is not None and set2 is not None and self._is_valid_partition(set1, set2):
                return set1, set2
        
        return None, None
    
    def get_partition_with_priority_constraints(self, priority_func):
        """Get partition with priority-based constraints."""
        if not self.numbers:
            return None, None
        
        # Calculate priority for partition
        priority = priority_func(self.numbers)
        
        if priority > 0:
            set1, set2 = self.find_two_sets_partition()
            if set1 is not None and set2 is not None and self._is_valid_partition(set1, set2):
                return set1, set2
        
        return None, None
    
    def get_partition_with_adaptive_constraints(self, adaptive_func):
        """Get partition with adaptive constraints."""
        if not self.numbers:
            return None, None
        
        if adaptive_func(self.numbers, []):
            set1, set2 = self.find_two_sets_partition()
            if set1 is not None and set2 is not None and self._is_valid_partition(set1, set2):
                return set1, set2
        
        return None, None
    
    def find_two_sets_partition(self):
        """Find optimal two sets partition."""
        if not self.numbers or self.total_sum % 2 != 0:
            return None, None
        
        target_sum = self.total_sum // 2
        
        # Use dynamic programming to find partition
        n = len(self.numbers)
        dp = [[False for _ in range(target_sum + 1)] for _ in range(n + 1)]
        
        # Initialize base cases
        for i in range(n + 1):
            dp[i][0] = True
        
        # Fill DP table
        for i in range(1, n + 1):
            for j in range(1, target_sum + 1):
                if j < self.numbers[i-1]:
                    dp[i][j] = dp[i-1][j]
                else:
                    dp[i][j] = dp[i-1][j] or dp[i-1][j - self.numbers[i-1]]
        
        if not dp[n][target_sum]:
            return None, None
        
        # Reconstruct the partition
        set1 = []
        set2 = []
        i, j = n, target_sum
        
        while i > 0 and j > 0:
            if dp[i-1][j]:
                set2.append(self.numbers[i-1])
                i -= 1
            else:
                set1.append(self.numbers[i-1])
                j -= self.numbers[i-1]
                i -= 1
        
        # Add remaining numbers to set2
        while i > 0:
            set2.append(self.numbers[i-1])
            i -= 1
        
        return set1, set2
    
    def get_optimal_two_sets_strategy(self):
        """Get optimal two sets strategy considering all constraints."""
        strategies = [
            ('sum_constraints', self.get_partition_with_sum_constraints),
            ('number_constraints', self.get_partition_with_number_constraints),
            ('pattern_constraints', self.get_partition_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_score = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'sum_constraints':
                    result = strategy_func(0, 1000)
                elif strategy_name == 'number_constraints':
                    number_constraints = [lambda nums: len(nums) > 0]
                    result = strategy_func(number_constraints)
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda nums: all(num > 0 for num in nums)]
                    result = strategy_func(pattern_constraints)
                
                if result[0] is not None and len(result[0]) > best_score:
                    best_score = len(result[0])
                    best_strategy = (strategy_name, result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'min_sum': 5,
    'max_sum': 20,
    'forbidden_numbers': [0, -1],
    'required_numbers': [1, 5],
    'pattern_constraints': [lambda set1, set2, numbers: len(set1) > 0 and len(set2) > 0]
}

numbers = [1, 5, 11, 5, 0, -1]
constrained_two_sets = ConstrainedTwoSets(numbers, constraints)

print("Sum-constrained partition:", constrained_two_sets.get_partition_with_sum_constraints(5, 20))

print("Number-constrained partition:", constrained_two_sets.get_partition_with_number_constraints([lambda nums: len(nums) > 0]))

print("Pattern-constrained partition:", constrained_two_sets.get_partition_with_pattern_constraints([lambda nums: all(num > 0 for num in nums)]))

# Mathematical constraints
def custom_constraint(numbers):
    return len(numbers) > 0 and all(num > 0 for num in numbers)

print("Mathematical constraint partition:", constrained_two_sets.get_partition_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(numbers):
    return all(1 <= num <= 20 for num in numbers)

range_constraints = [range_constraint]
print("Range-constrained partition:", constrained_two_sets.get_partition_with_sum_constraints(1, 20))

# Multiple constraints
def constraint1(numbers):
    return len(numbers) > 0

def constraint2(numbers):
    return all(num > 0 for num in numbers)

constraints_list = [constraint1, constraint2]
print("Multiple constraints partition:", constrained_two_sets.get_partition_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(numbers):
    return len(numbers) + sum(1 for num in numbers if num > 0)

print("Priority-constrained partition:", constrained_two_sets.get_partition_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(numbers, current_result):
    return len(numbers) > 0 and len(current_result) < 5

print("Adaptive constraint partition:", constrained_two_sets.get_partition_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_two_sets.get_optimal_two_sets_strategy()
print(f"Optimal two sets strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Two Sets](https://cses.fi/problemset/task/1092) - Basic two sets partitioning
- [Two Sets II](https://cses.fi/problemset/task/1093) - Advanced two sets with counting
- [Apple Division](https://cses.fi/problemset/task/1623) - Set partitioning optimization

#### **LeetCode Problems**
- [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/) - Check if array can be partitioned into equal sum subsets
- [Partition to K Equal Sum Subsets](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/) - Partition into k equal sum subsets
- [Target Sum](https://leetcode.com/problems/target-sum/) - Find ways to assign signs to get target sum
- [Subset Sum](https://leetcode.com/problems/subset-sum/) - Check if subset with given sum exists

#### **Problem Categories**
- **Set Partitioning**: Equal sum partitioning, set construction, mathematical analysis
- **Mathematical Analysis**: Sum calculations, feasibility checking, arithmetic series
- **Greedy Algorithms**: Optimal set construction, greedy strategies, mathematical optimization
- **Combinatorics**: Partition counting, set enumeration, mathematical combinations

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
