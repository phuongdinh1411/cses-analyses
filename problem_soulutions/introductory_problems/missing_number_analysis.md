---
layout: simple
title: "Missing Number"
permalink: /problem_soulutions/introductory_problems/missing_number_analysis
---

# Missing Number

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand array analysis and mathematical formula problems
- Apply mathematical formulas or XOR operations to find missing elements
- Implement efficient missing number algorithms with proper mathematical calculations
- Optimize missing number solutions using mathematical formulas and XOR properties
- Handle edge cases in missing number problems (single element, large arrays, mathematical precision)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Array analysis, mathematical formulas, XOR operations, missing element detection
- **Data Structures**: Arrays, mathematical calculations, XOR operations, element tracking
- **Mathematical Concepts**: Arithmetic series, XOR properties, mathematical formulas, array mathematics
- **Programming Skills**: Array processing, mathematical calculations, XOR implementation, algorithm implementation
- **Related Problems**: Array problems, Mathematical formulas, XOR problems, Missing element problems

## Problem Description

**Problem**: You are given all numbers between 1,2,…,n except one. Your task is to find the missing number.

**Input**: 
- First line: n (2 ≤ n ≤ 2×10⁵)
- Second line: n-1 integers (each between 1 and n)

**Output**: The missing number.

**Constraints**:
- 2 ≤ n ≤ 2×10⁵
- Numbers are from 1 to n (inclusive)
- Exactly one number is missing
- All given numbers are distinct
- Need to find missing number efficiently

**Example**:
```
Input:
5
2 3 1 5

Output:
4

Explanation: The numbers 1,2,3,4,5 are expected, but 4 is missing.
```

## Visual Example

### Input and Array Analysis
```
Input: n = 5, arr = [2, 3, 1, 5]

Expected numbers: 1, 2, 3, 4, 5
Given numbers: 2, 3, 1, 5
Missing number: 4
```

### Mathematical Sum Approach
```
Expected sum of numbers 1 to 5:
1 + 2 + 3 + 4 + 5 = 15

Actual sum of given numbers:
2 + 3 + 1 + 5 = 11

Missing number = Expected sum - Actual sum
Missing number = 15 - 11 = 4
```

### XOR Approach
```
Expected XOR of numbers 1 to 5:
1 ^ 2 ^ 3 ^ 4 ^ 5 = 1

Actual XOR of given numbers:
2 ^ 3 ^ 1 ^ 5 = 5

Missing number = Expected XOR ^ Actual XOR
Missing number = 1 ^ 5 = 4
```

### Key Insight
The solution works by:
1. Using mathematical formulas for sum calculation
2. Using XOR properties for bitwise operations
3. Calculating the difference between expected and actual values
4. Time complexity: O(n) for both approaches
5. Space complexity: O(1) for constant variables

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Search (Inefficient)

**Key Insights from Brute Force Solution:**
- Search through all numbers from 1 to n to find the missing one
- Simple but computationally expensive approach
- Not suitable for large n
- Straightforward implementation but poor performance

**Algorithm:**
1. Iterate through all numbers from 1 to n
2. Check if each number exists in the given array
3. Return the first number that doesn't exist
4. Handle edge cases correctly

**Visual Example:**
```
Brute force: Search through all numbers
For n = 5, arr = [2, 3, 1, 5]:
- Check 1: exists in array ✓
- Check 2: exists in array ✓
- Check 3: exists in array ✓
- Check 4: doesn't exist in array ✗ → Missing number
```

**Implementation:**
```python
def missing_number_brute_force(n, arr):
    for i in range(1, n + 1):
        if i not in arr:
            return i
    return -1  # Should never reach here

def solve_missing_number_brute_force():
    n = int(input())
    arr = list(map(int, input().split()))
    result = missing_number_brute_force(n, arr)
    print(result)
```

**Time Complexity:** O(n²) for searching through array
**Space Complexity:** O(1) for storing variables

**Why it's inefficient:**
- O(n²) time complexity is too slow for large n
- Not suitable for competitive programming with n up to 2×10⁵
- Inefficient for large inputs
- Poor performance with quadratic growth

### Approach 2: Mathematical Sum Formula (Better)

**Key Insights from Mathematical Solution:**
- Use arithmetic series formula to calculate expected sum
- Much more efficient than brute force approach
- Standard method for missing number problems
- Can handle larger n than brute force

**Algorithm:**
1. Calculate expected sum using formula n(n+1)/2
2. Calculate actual sum of given numbers
3. Find missing number as difference
4. Return the missing number

**Visual Example:**
```
Mathematical approach: Use sum formula
For n = 5, arr = [2, 3, 1, 5]:
- Expected sum = 5×6/2 = 15
- Actual sum = 2+3+1+5 = 11
- Missing number = 15 - 11 = 4
```

**Implementation:**
```python
def missing_number_mathematical(n, arr):
    # Expected sum of numbers from 1 to n
    expected_sum = n * (n + 1) // 2
    
    # Actual sum of given numbers
    actual_sum = sum(arr)
    
    # Missing number
    missing = expected_sum - actual_sum
    
    return missing

def solve_missing_number_mathematical():
    n = int(input())
    arr = list(map(int, input().split()))
    result = missing_number_mathematical(n, arr)
    print(result)
```

**Time Complexity:** O(n) for summing array
**Space Complexity:** O(1) for storing variables

**Why it's better:**
- O(n) time complexity is much better than O(n²)
- Uses mathematical properties for efficient solution
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: XOR Bitwise Operations (Optimal)

**Key Insights from XOR Solution:**
- Use XOR properties for efficient bitwise operations
- Most efficient approach for missing number problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Calculate XOR of all numbers from 1 to n
2. Calculate XOR of all given numbers
3. Find missing number using XOR properties
4. Return the missing number

**Visual Example:**
```
XOR approach: Use bitwise operations
For n = 5, arr = [2, 3, 1, 5]:
- Expected XOR = 1^2^3^4^5 = 1
- Actual XOR = 2^3^1^5 = 5
- Missing number = 1^5 = 4
```

**Implementation:**
```python
def missing_number_xor(n, arr):
    # XOR all numbers from 1 to n
    expected_xor = 0
    for i in range(1, n + 1):
        expected_xor ^= i
    
    # XOR all given numbers
    actual_xor = 0
    for num in arr:
        actual_xor ^= num
    
    # Missing number
    missing = expected_xor ^ actual_xor
    
    return missing

def solve_missing_number():
    n = int(input())
    arr = list(map(int, input().split()))
    result = missing_number_xor(n, arr)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_missing_number()
```

**Time Complexity:** O(n) for XOR operations
**Space Complexity:** O(1) for storing variables

**Why it's optimal:**
- O(n) time complexity is optimal for this problem
- Uses XOR properties for efficient solution
- Most efficient approach for competitive programming
- Standard method for missing number optimization

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Missing Number with Duplicates
**Problem**: Find the missing number when duplicates are allowed in the array.

**Link**: [CSES Problem Set - Missing Number with Duplicates](https://cses.fi/problemset/task/missing_number_duplicates)

```python
def missing_number_duplicates(n, arr):
    # Use set to handle duplicates
    present = set(arr)
    
    for i in range(1, n + 1):
        if i not in present:
            return i
    
    return -1
```

### Variation 2: Multiple Missing Numbers
**Problem**: Find all missing numbers when multiple numbers are missing.

**Link**: [CSES Problem Set - Multiple Missing Numbers](https://cses.fi/problemset/task/multiple_missing_numbers)

```python
def multiple_missing_numbers(n, arr):
    present = set(arr)
    missing = []
    
    for i in range(1, n + 1):
        if i not in present:
            missing.append(i)
    
    return missing
```

### Variation 3: Missing Number in Sorted Array
**Problem**: Find the missing number in a sorted array efficiently.

**Link**: [CSES Problem Set - Missing Number Sorted Array](https://cses.fi/problemset/task/missing_number_sorted_array)

```python
def missing_number_sorted(n, arr):
    # Use binary search for O(log n) solution
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == mid + 1:
            left = mid + 1
        else:
            right = mid - 1
    
    return left + 1
```

## Problem Variations

### **Variation 1: Missing Number with Dynamic Updates**
**Problem**: Handle dynamic array updates (add/remove/update elements) while finding missing numbers efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic missing number management.

```python
from collections import defaultdict
import itertools

class DynamicMissingNumber:
    def __init__(self, n, arr=None):
        self.n = n
        self.arr = arr[:] if arr else []
        self.present = set(self.arr)
        self.expected_sum = n * (n + 1) // 2
        self.actual_sum = sum(self.arr)
        self.expected_xor = 0
        self.actual_xor = 0
        
        # Calculate expected XOR
        for i in range(1, n + 1):
            self.expected_xor ^= i
        
        # Calculate actual XOR
        for num in self.arr:
            self.actual_xor ^= num
    
    def add_number(self, num):
        """Add number to array."""
        if 1 <= num <= self.n and num not in self.present:
            self.arr.append(num)
            self.present.add(num)
            self.actual_sum += num
            self.actual_xor ^= num
    
    def remove_number(self, num):
        """Remove number from array."""
        if num in self.present:
            self.arr.remove(num)
            self.present.remove(num)
            self.actual_sum -= num
            self.actual_xor ^= num
    
    def update_number(self, old_num, new_num):
        """Update number in array."""
        if old_num in self.present and 1 <= new_num <= self.n and new_num not in self.present:
            self.remove_number(old_num)
            self.add_number(new_num)
    
    def get_missing_number_sum(self):
        """Get missing number using sum formula."""
        return self.expected_sum - self.actual_sum
    
    def get_missing_number_xor(self):
        """Get missing number using XOR."""
        return self.expected_xor ^ self.actual_xor
    
    def get_missing_numbers(self):
        """Get all missing numbers."""
        missing = []
        for i in range(1, self.n + 1):
            if i not in self.present:
                missing.append(i)
        return missing
    
    def get_missing_numbers_with_constraints(self, constraint_func):
        """Get missing numbers that satisfy custom constraints."""
        result = []
        for i in range(1, self.n + 1):
            if i not in self.present and constraint_func(i):
                result.append(i)
        return result
    
    def get_missing_numbers_in_range(self, start, end):
        """Get missing numbers within specified range."""
        result = []
        for i in range(max(1, start), min(self.n + 1, end + 1)):
            if i not in self.present:
                result.append(i)
        return result
    
    def get_missing_numbers_with_pattern(self, pattern_func):
        """Get missing numbers matching specified pattern."""
        result = []
        for i in range(1, self.n + 1):
            if i not in self.present and pattern_func(i):
                result.append(i)
        return result
    
    def get_array_statistics(self):
        """Get statistics about array and missing numbers."""
        total_numbers = self.n
        present_count = len(self.present)
        missing_count = total_numbers - present_count
        
        # Calculate number distribution
        number_distribution = defaultdict(int)
        for num in self.arr:
            number_distribution[num] += 1
        
        return {
            'total_numbers': total_numbers,
            'present_count': present_count,
            'missing_count': missing_count,
            'completion_rate': present_count / total_numbers if total_numbers > 0 else 0,
            'number_distribution': dict(number_distribution)
        }
    
    def get_array_patterns(self):
        """Get patterns in array numbers."""
        patterns = {
            'consecutive_sequences': 0,
            'arithmetic_sequences': 0,
            'even_numbers': 0,
            'odd_numbers': 0
        }
        
        if not self.arr:
            return patterns
        
        sorted_arr = sorted(self.arr)
        
        # Check for consecutive sequences
        consecutive_count = 1
        for i in range(1, len(sorted_arr)):
            if sorted_arr[i] == sorted_arr[i-1] + 1:
                consecutive_count += 1
            else:
                if consecutive_count >= 2:
                    patterns['consecutive_sequences'] += 1
                consecutive_count = 1
        if consecutive_count >= 2:
            patterns['consecutive_sequences'] += 1
        
        # Check for arithmetic sequences
        if len(sorted_arr) >= 3:
            diff = sorted_arr[1] - sorted_arr[0]
            is_arithmetic = True
            for i in range(2, len(sorted_arr)):
                if sorted_arr[i] - sorted_arr[i-1] != diff:
                    is_arithmetic = False
                    break
            if is_arithmetic:
                patterns['arithmetic_sequences'] = 1
        
        # Count even and odd numbers
        for num in self.arr:
            if num % 2 == 0:
                patterns['even_numbers'] += 1
            else:
                patterns['odd_numbers'] += 1
        
        return patterns
    
    def get_optimal_missing_strategy(self):
        """Get optimal strategy for finding missing numbers."""
        if not self.arr:
            return {
                'recommended_strategy': 'sum_formula',
                'efficiency_rate': 1.0,
                'missing_rate': 1.0
            }
        
        # Calculate efficiency rate
        missing_count = len(self.get_missing_numbers())
        missing_rate = missing_count / self.n if self.n > 0 else 0
        
        # Calculate efficiency rate (lower missing rate is better)
        efficiency_rate = 1.0 - missing_rate
        
        # Determine recommended strategy
        if missing_count == 1:
            recommended_strategy = 'sum_formula'
        elif missing_count <= 3:
            recommended_strategy = 'xor_operations'
        else:
            recommended_strategy = 'set_operations'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'missing_rate': missing_rate
        }

# Example usage
n = 5
arr = [2, 3, 1, 5]
dynamic_missing = DynamicMissingNumber(n, arr)
print(f"Initial missing number (sum): {dynamic_missing.get_missing_number_sum()}")
print(f"Initial missing number (XOR): {dynamic_missing.get_missing_number_xor()}")

# Add number
dynamic_missing.add_number(4)
print(f"After adding 4: {dynamic_missing.get_missing_numbers()}")

# Remove number
dynamic_missing.remove_number(2)
print(f"After removing 2: {dynamic_missing.get_missing_numbers()}")

# Update number
dynamic_missing.update_number(3, 6)
print(f"After updating 3 to 6: {dynamic_missing.get_missing_numbers()}")

# Get missing numbers with constraints
def constraint_func(num):
    return num % 2 == 0

print(f"Missing even numbers: {dynamic_missing.get_missing_numbers_with_constraints(constraint_func)}")

# Get missing numbers in range
print(f"Missing numbers in range 1-3: {dynamic_missing.get_missing_numbers_in_range(1, 3)}")

# Get missing numbers with pattern
def pattern_func(num):
    return num > 3

print(f"Missing numbers > 3: {dynamic_missing.get_missing_numbers_with_pattern(pattern_func)}")

# Get statistics
print(f"Statistics: {dynamic_missing.get_array_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_missing.get_array_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_missing.get_optimal_missing_strategy()}")
```

### **Variation 2: Missing Number with Different Operations**
**Problem**: Handle different types of missing number operations (weighted numbers, priority-based selection, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of missing number operations.

```python
class AdvancedMissingNumber:
    def __init__(self, n, arr=None, weights=None, priorities=None):
        self.n = n
        self.arr = arr[:] if arr else []
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.present = set(self.arr)
        self._calculate_expected_values()
        self._calculate_actual_values()
    
    def _calculate_expected_values(self):
        """Calculate expected sum and XOR values."""
        self.expected_sum = 0
        self.expected_xor = 0
        self.expected_weighted_sum = 0
        
        for i in range(1, self.n + 1):
            self.expected_sum += i
            self.expected_xor ^= i
            weight = self.weights.get(i, 1)
            priority = self.priorities.get(i, 1)
            self.expected_weighted_sum += i * weight * priority
    
    def _calculate_actual_values(self):
        """Calculate actual sum and XOR values."""
        self.actual_sum = 0
        self.actual_xor = 0
        self.actual_weighted_sum = 0
        
        for num in self.arr:
            self.actual_sum += num
            self.actual_xor ^= num
            weight = self.weights.get(num, 1)
            priority = self.priorities.get(num, 1)
            self.actual_weighted_sum += num * weight * priority
    
    def get_weighted_missing_numbers(self):
        """Get missing numbers with weights and priorities applied."""
        result = []
        for i in range(1, self.n + 1):
            if i not in self.present:
                weighted_missing = {
                    'number': i,
                    'weight': self.weights.get(i, 1),
                    'priority': self.priorities.get(i, 1),
                    'weighted_value': i * self.weights.get(i, 1) * self.priorities.get(i, 1)
                }
                result.append(weighted_missing)
        return result
    
    def get_missing_numbers_with_priority(self, priority_func):
        """Get missing numbers considering priority."""
        result = []
        for i in range(1, self.n + 1):
            if i not in self.present:
                priority = priority_func(i, self.weights, self.priorities)
                result.append((i, priority))
        
        # Sort by priority
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_missing_numbers_with_optimization(self, optimization_func):
        """Get missing numbers using custom optimization function."""
        result = []
        for i in range(1, self.n + 1):
            if i not in self.present:
                score = optimization_func(i, self.weights, self.priorities)
                result.append((i, score))
        
        # Sort by optimization score
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_missing_numbers_with_constraints(self, constraint_func):
        """Get missing numbers that satisfy custom constraints."""
        result = []
        for i in range(1, self.n + 1):
            if i not in self.present and constraint_func(i, self.weights, self.priorities):
                result.append(i)
        return result
    
    def get_missing_numbers_with_multiple_criteria(self, criteria_list):
        """Get missing numbers that satisfy multiple criteria."""
        result = []
        for i in range(1, self.n + 1):
            if i not in self.present:
                satisfies_all_criteria = True
                for criterion in criteria_list:
                    if not criterion(i, self.weights, self.priorities):
                        satisfies_all_criteria = False
                        break
                if satisfies_all_criteria:
                    result.append(i)
        return result
    
    def get_missing_numbers_with_alternatives(self, alternatives):
        """Get missing numbers considering alternative weights/priorities."""
        result = []
        
        # Check original missing numbers
        original_missing = self.get_weighted_missing_numbers()
        result.append((original_missing, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedMissingNumber(self.n, self.arr, alt_weights, alt_priorities)
            temp_missing = temp_instance.get_weighted_missing_numbers()
            result.append((temp_missing, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_missing_numbers_with_adaptive_criteria(self, adaptive_func):
        """Get missing numbers using adaptive criteria."""
        result = []
        for i in range(1, self.n + 1):
            if i not in self.present and adaptive_func(i, self.weights, self.priorities, result):
                result.append(i)
        return result
    
    def get_missing_optimization(self):
        """Get optimal missing number configuration."""
        strategies = [
            ('weighted_missing', lambda: len(self.get_weighted_missing_numbers())),
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
n = 5
arr = [2, 3, 1, 5]
weights = {i: i + 1 for i in range(1, n + 1)}  # Higher numbers have higher weights
priorities = {i: n - i + 1 for i in range(1, n + 1)}  # Lower numbers have higher priority
advanced_missing = AdvancedMissingNumber(n, arr, weights, priorities)

print(f"Weighted missing numbers: {len(advanced_missing.get_weighted_missing_numbers())}")

# Get missing numbers with priority
def priority_func(num, weights, priorities):
    return num * weights.get(num, 1) + priorities.get(num, 1)

print(f"Missing numbers with priority: {len(advanced_missing.get_missing_numbers_with_priority(priority_func))}")

# Get missing numbers with optimization
def optimization_func(num, weights, priorities):
    return num * weights.get(num, 1) * priorities.get(num, 1)

print(f"Missing numbers with optimization: {len(advanced_missing.get_missing_numbers_with_optimization(optimization_func))}")

# Get missing numbers with constraints
def constraint_func(num, weights, priorities):
    return num <= 4 and weights.get(num, 1) <= 5

print(f"Missing numbers with constraints: {len(advanced_missing.get_missing_numbers_with_constraints(constraint_func))}")

# Get missing numbers with multiple criteria
def criterion1(num, weights, priorities):
    return num <= 4

def criterion2(num, weights, priorities):
    return weights.get(num, 1) <= 5

criteria_list = [criterion1, criterion2]
print(f"Missing numbers with multiple criteria: {len(advanced_missing.get_missing_numbers_with_multiple_criteria(criteria_list))}")

# Get missing numbers with alternatives
alternatives = [({i: 1 for i in range(1, n + 1)}, {i: 1 for i in range(1, n + 1)}), ({i: i*2 for i in range(1, n + 1)}, {i: i+1 for i in range(1, n + 1)})]
print(f"Missing numbers with alternatives: {len(advanced_missing.get_missing_numbers_with_alternatives(alternatives))}")

# Get missing numbers with adaptive criteria
def adaptive_func(num, weights, priorities, current_result):
    return num <= 4 and len(current_result) < 3

print(f"Missing numbers with adaptive criteria: {len(advanced_missing.get_missing_numbers_with_adaptive_criteria(adaptive_func))}")

# Get missing optimization
print(f"Missing optimization: {advanced_missing.get_missing_optimization()}")
```

### **Variation 3: Missing Number with Constraints**
**Problem**: Handle missing number detection with additional constraints (range limits, pattern constraints, mathematical constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedMissingNumber:
    def __init__(self, n, arr=None, constraints=None):
        self.n = n
        self.arr = arr[:] if arr else []
        self.constraints = constraints or {}
        self.present = set(self.arr)
        self._calculate_expected_values()
        self._calculate_actual_values()
    
    def _calculate_expected_values(self):
        """Calculate expected sum and XOR values."""
        self.expected_sum = 0
        self.expected_xor = 0
        
        for i in range(1, self.n + 1):
            if self._is_valid_number(i):
                self.expected_sum += i
                self.expected_xor ^= i
    
    def _calculate_actual_values(self):
        """Calculate actual sum and XOR values."""
        self.actual_sum = 0
        self.actual_xor = 0
        
        for num in self.arr:
            if self._is_valid_number(num):
                self.actual_sum += num
                self.actual_xor ^= num
    
    def _is_valid_number(self, num):
        """Check if number is valid considering constraints."""
        # Range constraints
        if 'min_value' in self.constraints:
            if num < self.constraints['min_value']:
                return False
        
        if 'max_value' in self.constraints:
            if num > self.constraints['max_value']:
                return False
        
        # Pattern constraints
        if 'forbidden_numbers' in self.constraints:
            if num in self.constraints['forbidden_numbers']:
                return False
        
        if 'allowed_numbers' in self.constraints:
            if num not in self.constraints['allowed_numbers']:
                return False
        
        # Mathematical constraints
        if 'mathematical_constraints' in self.constraints:
            for constraint in self.constraints['mathematical_constraints']:
                if not constraint(num):
                    return False
        
        return True
    
    def get_missing_numbers_with_range_constraints(self, min_val, max_val):
        """Get missing numbers considering range constraints."""
        result = []
        for i in range(max(1, min_val), min(self.n + 1, max_val + 1)):
            if i not in self.present and self._is_valid_number(i):
                result.append(i)
        return result
    
    def get_missing_numbers_with_pattern_constraints(self, pattern_constraints):
        """Get missing numbers considering pattern constraints."""
        result = []
        for i in range(1, self.n + 1):
            if i not in self.present:
                satisfies_pattern = True
                for constraint in pattern_constraints:
                    if not constraint(i):
                        satisfies_pattern = False
                        break
                if satisfies_pattern and self._is_valid_number(i):
                    result.append(i)
        return result
    
    def get_missing_numbers_with_mathematical_constraints(self, constraint_func):
        """Get missing numbers that satisfy custom mathematical constraints."""
        result = []
        for i in range(1, self.n + 1):
            if i not in self.present and constraint_func(i) and self._is_valid_number(i):
                result.append(i)
        return result
    
    def get_missing_numbers_with_optimization_constraints(self, optimization_func):
        """Get missing numbers using custom optimization constraints."""
        # Sort missing numbers by optimization function
        all_missing = []
        for i in range(1, self.n + 1):
            if i not in self.present and self._is_valid_number(i):
                score = optimization_func(i)
                all_missing.append((i, score))
        
        # Sort by optimization score
        all_missing.sort(key=lambda x: x[1], reverse=True)
        
        return [num for num, _ in all_missing]
    
    def get_missing_numbers_with_multiple_constraints(self, constraints_list):
        """Get missing numbers that satisfy multiple constraints."""
        result = []
        for i in range(1, self.n + 1):
            if i not in self.present:
                satisfies_all_constraints = True
                for constraint in constraints_list:
                    if not constraint(i):
                        satisfies_all_constraints = False
                        break
                if satisfies_all_constraints and self._is_valid_number(i):
                    result.append(i)
        return result
    
    def get_missing_numbers_with_priority_constraints(self, priority_func):
        """Get missing numbers with priority-based constraints."""
        # Sort missing numbers by priority
        all_missing = []
        for i in range(1, self.n + 1):
            if i not in self.present and self._is_valid_number(i):
                priority = priority_func(i)
                all_missing.append((i, priority))
        
        # Sort by priority
        all_missing.sort(key=lambda x: x[1], reverse=True)
        
        return [num for num, _ in all_missing]
    
    def get_missing_numbers_with_adaptive_constraints(self, adaptive_func):
        """Get missing numbers with adaptive constraints."""
        result = []
        for i in range(1, self.n + 1):
            if i not in self.present and self._is_valid_number(i) and adaptive_func(i, result):
                result.append(i)
        return result
    
    def get_optimal_missing_strategy(self):
        """Get optimal missing number strategy considering all constraints."""
        strategies = [
            ('range_constraints', self.get_missing_numbers_with_range_constraints),
            ('pattern_constraints', self.get_missing_numbers_with_pattern_constraints),
            ('mathematical_constraints', self.get_missing_numbers_with_mathematical_constraints),
        ]
        
        best_strategy = None
        best_count = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'range_constraints':
                    current_count = len(strategy_func(1, 4))
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda i: i % 2 == 0]
                    current_count = len(strategy_func(pattern_constraints))
                elif strategy_name == 'mathematical_constraints':
                    def custom_constraint(i):
                        return i <= 4
                    current_count = len(strategy_func(custom_constraint))
                
                if current_count > best_count:
                    best_count = current_count
                    best_strategy = (strategy_name, current_count)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'min_value': 1,
    'max_value': 5,
    'forbidden_numbers': [6, 7, 8],
    'allowed_numbers': [i for i in range(1, 6)],
    'mathematical_constraints': [lambda x: x <= 5]
}

n = 5
arr = [2, 3, 1, 5]
constrained_missing = ConstrainedMissingNumber(n, arr, constraints)

print("Range-constrained missing numbers:", len(constrained_missing.get_missing_numbers_with_range_constraints(1, 4)))

print("Pattern-constrained missing numbers:", len(constrained_missing.get_missing_numbers_with_pattern_constraints([lambda i: i % 2 == 0])))

# Mathematical constraints
def custom_constraint(num):
    return num <= 4 and num % 2 == 0

print("Mathematical constraint missing numbers:", len(constrained_missing.get_missing_numbers_with_mathematical_constraints(custom_constraint)))

# Range constraints
def range_constraint(num):
    return 1 <= num <= 4

range_constraints = [range_constraint]
print("Range-constrained missing numbers:", len(constrained_missing.get_missing_numbers_with_range_constraints(1, 4)))

# Multiple constraints
def constraint1(num):
    return num <= 4

def constraint2(num):
    return num % 2 == 0

constraints_list = [constraint1, constraint2]
print("Multiple constraints missing numbers:", len(constrained_missing.get_missing_numbers_with_multiple_constraints(constraints_list)))

# Priority constraints
def priority_func(num):
    return num + 10

print("Priority-constrained missing numbers:", len(constrained_missing.get_missing_numbers_with_priority_constraints(priority_func)))

# Adaptive constraints
def adaptive_func(num, current_result):
    return num <= 4 and len(current_result) < 3

print("Adaptive constraint missing numbers:", len(constrained_missing.get_missing_numbers_with_adaptive_constraints(adaptive_func)))

# Optimal strategy
optimal = constrained_missing.get_optimal_missing_strategy()
print(f"Optimal missing strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Missing Number](https://cses.fi/problemset/task/1083) - Basic missing number problem
- [Number Spiral](https://cses.fi/problemset/task/1071) - Mathematical sequence problems
- [Two Sets](https://cses.fi/problemset/task/1092) - Set partitioning problems

#### **LeetCode Problems**
- [Missing Number](https://leetcode.com/problems/missing-number/) - Find missing number in array
- [First Missing Positive](https://leetcode.com/problems/first-missing-positive/) - Find first missing positive integer
- [Find All Numbers Disappeared in an Array](https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/) - Find all missing numbers
- [Single Number](https://leetcode.com/problems/single-number/) - Find single missing number using XOR

#### **Problem Categories**
- **Array Analysis**: Missing element detection, array manipulation, mathematical analysis
- **Mathematical Formulas**: Sum calculations, arithmetic series, mathematical optimization
- **XOR Operations**: Bitwise operations, mathematical properties, efficient algorithms
- **Algorithm Design**: Array algorithms, mathematical algorithms, optimization techniques

## 📚 Learning Points

1. **Array Analysis**: Essential for understanding missing number problems
2. **Mathematical Formulas**: Key technique for efficient sum calculation
3. **XOR Properties**: Important for understanding bitwise operations
4. **Arithmetic Series**: Critical for understanding sum formulas
5. **Algorithm Optimization**: Foundation for many array analysis algorithms
6. **Mathematical Properties**: Critical for competitive programming performance

## 📝 Summary

The Missing Number problem demonstrates array analysis and mathematical formula concepts for efficient missing element detection. We explored three approaches:

1. **Brute Force Search**: O(n²) time complexity using linear search through array, inefficient for large n
2. **Mathematical Sum Formula**: O(n) time complexity using arithmetic series and sum calculation, better approach for missing number problems
3. **XOR Bitwise Operations**: O(n) time complexity with XOR properties, optimal approach for missing number optimization

The key insights include understanding array analysis principles, using mathematical formulas for efficient sum calculation, and applying XOR properties for optimal performance. This problem serves as an excellent introduction to array analysis algorithms and mathematical formula optimization.
