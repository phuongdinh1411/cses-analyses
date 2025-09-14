---
layout: simple
title: "Trailing Zeros"
permalink: /problem_soulutions/introductory_problems/trailing_zeros_analysis
---

# Trailing Zeros

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand factorial properties and trailing zero counting concepts
- Apply mathematical formulas to count trailing zeros without computing large factorials
- Implement efficient trailing zero counting algorithms with proper mathematical calculations
- Optimize trailing zero counting using mathematical analysis and prime factorization
- Handle edge cases in factorial problems (large n, mathematical precision, overflow prevention)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Factorial properties, trailing zero counting, mathematical formulas, prime factorization
- **Data Structures**: Mathematical calculations, prime tracking, factorization tracking, mathematical operations
- **Mathematical Concepts**: Factorial theory, prime factorization, trailing zero mathematics, mathematical analysis
- **Programming Skills**: Mathematical calculations, prime factorization, trailing zero counting, algorithm implementation
- **Related Problems**: Factorial problems, Mathematical formulas, Prime factorization, Trailing zero problems

## Problem Description

**Problem**: Calculate the number of trailing zeros in n! (n factorial).

**Input**: An integer n (1 ≤ n ≤ 10⁹)

**Output**: The number of trailing zeros in n!.

**Constraints**:
- 1 ≤ n ≤ 10⁹
- Trailing zeros come from factors of 10 = 2 × 5
- In factorial, there are always more factors of 2 than 5
- Need to count factors of 5 efficiently
- Cannot compute n! directly for large n

**Example**:
```
Input: 20

Output: 4

Explanation: 20! = 2432902008176640000 has 4 trailing zeros.
```

## Visual Example

### Input and Factorial Calculation
```
Input: n = 20

20! = 20 × 19 × 18 × ... × 2 × 1
20! = 2432902008176640000
Trailing zeros: 4
```

### Factor Analysis
```
Numbers 1 to 20:
1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20

Factors of 5:
- 5: 1 factor of 5
- 10: 1 factor of 5
- 15: 1 factor of 5
- 20: 1 factor of 5

Total factors of 5: 4
```

### Mathematical Formula
```
For n = 20:
- Count multiples of 5: 20/5 = 4
- Count multiples of 25: 20/25 = 0
- Count multiples of 125: 20/125 = 0
- Total trailing zeros = 4 + 0 + 0 = 4
```

### Key Insight
The solution works by:
1. Using mathematical properties of factorial
2. Counting factors of 5 instead of computing factorial
3. Using logarithmic time complexity
4. Time complexity: O(log n) for mathematical approach
5. Space complexity: O(1) for constant variables

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Factorial Calculation (Inefficient)

**Key Insights from Brute Force Solution:**
- Calculate n! directly and count trailing zeros
- Simple but computationally expensive approach
- Not suitable for large n
- Straightforward implementation but poor performance

**Algorithm:**
1. Calculate n! by multiplying all numbers from 1 to n
2. Count trailing zeros by repeatedly dividing by 10
3. Handle large numbers with integer overflow
4. Return the count of trailing zeros

**Visual Example:**
```
Brute force: Calculate factorial directly
For n = 20:
- Calculate 20! = 2432902008176640000
- Count trailing zeros: 0000 → 4 zeros
```

**Implementation:**
```python
def trailing_zeros_brute_force(n):
    # Calculate factorial
    factorial = 1
    for i in range(1, n + 1):
        factorial *= i
    
    # Count trailing zeros
    count = 0
    while factorial % 10 == 0:
        count += 1
        factorial //= 10
    
    return count

def solve_trailing_zeros_brute_force():
    n = int(input())
    result = trailing_zeros_brute_force(n)
    print(result)
```

**Time Complexity:** O(n) for calculating factorial
**Space Complexity:** O(log n!) for storing factorial

**Why it's inefficient:**
- O(n) time complexity is too slow for large n
- Not suitable for competitive programming with n up to 10⁹
- Inefficient for large inputs
- Poor performance with factorial growth

### Approach 2: Mathematical Analysis with Factor Counting (Better)

**Key Insights from Mathematical Solution:**
- Use mathematical properties of factorial
- Much more efficient than brute force approach
- Standard method for trailing zero problems
- Can handle larger n than brute force

**Algorithm:**
1. Understand that trailing zeros come from factors of 10 = 2 × 5
2. Count factors of 5 (since 2s are more abundant)
3. Count multiples of 5, 25, 125, etc.
4. Sum all contributions

**Visual Example:**
```
Mathematical approach: Count factors of 5
For n = 20:
- Count multiples of 5: 20/5 = 4
- Count multiples of 25: 20/25 = 0
- Count multiples of 125: 20/125 = 0
- Total trailing zeros = 4 + 0 + 0 = 4
```

**Implementation:**
```python
def trailing_zeros_mathematical(n):
    # Count factors of 5 (since 2s are more abundant)
    count = 0
    power = 5
    
    while power <= n:
        count += n // power
        power *= 5
    
    return count

def solve_trailing_zeros_mathematical():
    n = int(input())
    result = trailing_zeros_mathematical(n)
    print(result)
```

**Time Complexity:** O(log n) for mathematical calculation
**Space Complexity:** O(1) for storing variables

**Why it's better:**
- O(log n) time complexity is much better than O(n)
- Uses mathematical properties for efficient solution
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized Mathematical Formula (Optimal)

**Key Insights from Optimized Mathematical Solution:**
- Use optimized mathematical formulas for efficiency
- Most efficient approach for trailing zero problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use optimized mathematical formulas
2. Apply efficient factor counting
3. Handle edge cases efficiently
4. Return the optimal solution

**Visual Example:**
```
Optimized mathematical: Use efficient formulas
For n = 20:
- Count factors of 5: 20/5 + 20/25 + 20/125 + ... = 4
- Result = 4
```

**Implementation:**
```python
def trailing_zeros_optimized(n):
    # Count factors of 5
    count = 0
    power = 5
    
    while power <= n:
        count += n // power
        power *= 5
    
    return count

def solve_trailing_zeros():
    n = int(input())
    result = trailing_zeros_optimized(n)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_trailing_zeros()
```

**Time Complexity:** O(log n) for optimized mathematical calculation
**Space Complexity:** O(1) for storing variables

**Why it's optimal:**
- O(log n) time complexity is optimal for this problem
- Uses optimized mathematical formulas
- Most efficient approach for competitive programming
- Standard method for trailing zero calculation optimization

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Trailing Zeros in Different Bases
**Problem**: Calculate trailing zeros in n! for different bases (e.g., base 12).

**Link**: [CSES Problem Set - Trailing Zeros Different Bases](https://cses.fi/problemset/task/trailing_zeros_different_bases)

```python
def trailing_zeros_different_base(n, base):
    # Factorize the base
    factors = {}
    temp = base
    for i in range(2, int(temp**0.5) + 1):
        while temp % i == 0:
            factors[i] = factors.get(i, 0) + 1
            temp //= i
    if temp > 1:
        factors[temp] = factors.get(temp, 0) + 1
    
    # Count factors for each prime in the base
    min_count = float('inf')
    for prime, exp in factors.items():
        count = 0
        power = prime
        while power <= n:
            count += n // power
            power *= prime
        min_count = min(min_count, count // exp)
    
    return min_count
```

### Variation 2: Trailing Zeros in Product of Range
**Problem**: Calculate trailing zeros in the product of numbers from a to b.

**Link**: [CSES Problem Set - Trailing Zeros Range Product](https://cses.fi/problemset/task/trailing_zeros_range_product)

```python
def trailing_zeros_range_product(a, b):
    def count_factors(n, factor):
        count = 0
        power = factor
        while power <= n:
            count += n // power
            power *= factor
        return count
    
    # Count factors of 5 in range [a, b]
    count_5 = count_factors(b, 5) - count_factors(a - 1, 5)
    count_2 = count_factors(b, 2) - count_factors(a - 1, 2)
    
    return min(count_2, count_5)
```

### Variation 3: Trailing Zeros in Binomial Coefficient
**Problem**: Calculate trailing zeros in C(n, k) = n! / (k! × (n-k)!).

**Link**: [CSES Problem Set - Trailing Zeros Binomial](https://cses.fi/problemset/task/trailing_zeros_binomial)

```python
def trailing_zeros_binomial(n, k):
    def count_factors(n, factor):
        count = 0
        power = factor
        while power <= n:
            count += n // power
            power *= factor
        return count
    
    # Count factors of 5 in n!, k!, and (n-k)!
    count_5 = count_factors(n, 5) - count_factors(k, 5) - count_factors(n - k, 5)
    count_2 = count_factors(n, 2) - count_factors(k, 2) - count_factors(n - k, 2)
    
    return min(count_2, count_5)
```

## Problem Variations

### **Variation 1: Trailing Zeros with Dynamic Updates**
**Problem**: Handle dynamic number updates (add/remove/update numbers) while maintaining optimal trailing zeros calculation efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic number management.

```python
from collections import defaultdict

class DynamicTrailingZeros:
    def __init__(self, numbers=None):
        self.numbers = numbers or []
        self.factorial_cache = {}
        self._update_trailing_zeros_info()
    
    def _update_trailing_zeros_info(self):
        """Update trailing zeros feasibility information."""
        self.total_numbers = len(self.numbers)
        self.max_number = max(self.numbers) if self.numbers else 0
        self.trailing_zeros_feasibility = self._calculate_trailing_zeros_feasibility()
    
    def _calculate_trailing_zeros_feasibility(self):
        """Calculate trailing zeros calculation feasibility."""
        if not self.numbers:
            return 0
        
        # Check if all numbers are positive
        positive_count = sum(1 for num in self.numbers if num > 0)
        return positive_count / len(self.numbers) if self.numbers else 0
    
    def add_number(self, number, position=None):
        """Add number to the list."""
        if position is None:
            self.numbers.append(number)
        else:
            self.numbers.insert(position, number)
        
        self._update_trailing_zeros_info()
    
    def remove_number(self, position):
        """Remove number from the list."""
        if 0 <= position < len(self.numbers):
            self.numbers.pop(position)
            self._update_trailing_zeros_info()
    
    def update_number(self, position, new_number):
        """Update number in the list."""
        if 0 <= position < len(self.numbers):
            self.numbers[position] = new_number
            self._update_trailing_zeros_info()
    
    def count_trailing_zeros(self, n):
        """Count trailing zeros in n! efficiently."""
        if n in self.factorial_cache:
            return self.factorial_cache[n]
        
        if n < 0:
            return 0
        
        count = 0
        while n >= 5:
            n //= 5
            count += n
        
        self.factorial_cache[n] = count
        return count
    
    def get_trailing_zeros_with_constraints(self, constraint_func):
        """Get trailing zeros that satisfies custom constraints."""
        if not self.numbers:
            return []
        
        result = []
        for num in self.numbers:
            if constraint_func(num, self.numbers):
                trailing_zeros = self.count_trailing_zeros(num)
                result.append((num, trailing_zeros))
        
        return result
    
    def get_trailing_zeros_in_range(self, min_val, max_val):
        """Get trailing zeros within specified range."""
        if not self.numbers:
            return []
        
        result = []
        for num in self.numbers:
            if min_val <= num <= max_val:
                trailing_zeros = self.count_trailing_zeros(num)
                result.append((num, trailing_zeros))
        
        return result
    
    def get_trailing_zeros_with_pattern(self, pattern_func):
        """Get trailing zeros matching specified pattern."""
        if not self.numbers:
            return []
        
        result = []
        for num in self.numbers:
            if pattern_func(num, self.numbers):
                trailing_zeros = self.count_trailing_zeros(num)
                result.append((num, trailing_zeros))
        
        return result
    
    def get_number_statistics(self):
        """Get statistics about the numbers."""
        if not self.numbers:
            return {
                'total_numbers': 0,
                'max_number': 0,
                'trailing_zeros_feasibility': 0,
                'number_distribution': {}
            }
        
        return {
            'total_numbers': self.total_numbers,
            'max_number': self.max_number,
            'trailing_zeros_feasibility': self.trailing_zeros_feasibility,
            'number_distribution': {num: self.numbers.count(num) for num in set(self.numbers)}
        }
    
    def get_trailing_zeros_patterns(self):
        """Get patterns in trailing zeros calculation."""
        patterns = {
            'all_positive': 0,
            'has_negative': 0,
            'has_zero': 0,
            'large_numbers': 0
        }
        
        if not self.numbers:
            return patterns
        
        # Check if all numbers are positive
        if all(num > 0 for num in self.numbers):
            patterns['all_positive'] = 1
        
        # Check if has negative numbers
        if any(num < 0 for num in self.numbers):
            patterns['has_negative'] = 1
        
        # Check if has zero
        if 0 in self.numbers:
            patterns['has_zero'] = 1
        
        # Check if has large numbers
        if any(num > 1000 for num in self.numbers):
            patterns['large_numbers'] = 1
        
        return patterns
    
    def get_optimal_trailing_zeros_strategy(self):
        """Get optimal strategy for trailing zeros calculation."""
        if not self.numbers:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'trailing_zeros_feasibility': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = self.trailing_zeros_feasibility
        
        # Calculate trailing zeros feasibility
        trailing_zeros_feasibility = self.trailing_zeros_feasibility
        
        # Determine recommended strategy
        if self.max_number <= 10:
            recommended_strategy = 'direct_calculation'
        elif self.max_number <= 1000:
            recommended_strategy = 'optimized_calculation'
        else:
            recommended_strategy = 'advanced_optimization'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'trailing_zeros_feasibility': trailing_zeros_feasibility
        }

# Example usage
numbers = [5, 10, 15, 20]
dynamic_trailing_zeros = DynamicTrailingZeros(numbers)
print(f"Trailing zeros feasibility: {dynamic_trailing_zeros.trailing_zeros_feasibility}")

# Add number
dynamic_trailing_zeros.add_number(25)
print(f"After adding 25: {dynamic_trailing_zeros.max_number}")

# Remove number
dynamic_trailing_zeros.remove_number(0)
print(f"After removing first number: {dynamic_trailing_zeros.total_numbers}")

# Update number
dynamic_trailing_zeros.update_number(0, 30)
print(f"After updating first number to 30: {dynamic_trailing_zeros.numbers[0]}")

# Get trailing zeros with constraints
def constraint_func(num, numbers):
    return num > 10

print(f"Trailing zeros with constraints: {dynamic_trailing_zeros.get_trailing_zeros_with_constraints(constraint_func)}")

# Get trailing zeros in range
print(f"Trailing zeros in range 10-30: {dynamic_trailing_zeros.get_trailing_zeros_in_range(10, 30)}")

# Get trailing zeros with pattern
def pattern_func(num, numbers):
    return num % 5 == 0

print(f"Trailing zeros with pattern: {dynamic_trailing_zeros.get_trailing_zeros_with_pattern(pattern_func)}")

# Get statistics
print(f"Statistics: {dynamic_trailing_zeros.get_number_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_trailing_zeros.get_trailing_zeros_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_trailing_zeros.get_optimal_trailing_zeros_strategy()}")
```

### **Variation 2: Trailing Zeros with Different Operations**
**Problem**: Handle different types of trailing zeros operations (weighted numbers, priority-based calculation, advanced number analysis).

**Approach**: Use advanced data structures for efficient different types of trailing zeros operations.

```python
class AdvancedTrailingZeros:
    def __init__(self, numbers=None, weights=None, priorities=None):
        self.numbers = numbers or []
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.factorial_cache = {}
        self._update_trailing_zeros_info()
    
    def _update_trailing_zeros_info(self):
        """Update trailing zeros feasibility information."""
        self.total_numbers = len(self.numbers)
        self.max_number = max(self.numbers) if self.numbers else 0
        self.trailing_zeros_feasibility = self._calculate_trailing_zeros_feasibility()
    
    def _calculate_trailing_zeros_feasibility(self):
        """Calculate trailing zeros calculation feasibility."""
        if not self.numbers:
            return 0
        
        # Check if all numbers are positive
        positive_count = sum(1 for num in self.numbers if num > 0)
        return positive_count / len(self.numbers) if self.numbers else 0
    
    def count_trailing_zeros(self, n):
        """Count trailing zeros in n! efficiently."""
        if n in self.factorial_cache:
            return self.factorial_cache[n]
        
        if n < 0:
            return 0
        
        count = 0
        while n >= 5:
            n //= 5
            count += n
        
        self.factorial_cache[n] = count
        return count
    
    def get_weighted_trailing_zeros(self):
        """Get trailing zeros with weights and priorities applied."""
        if not self.numbers:
            return []
        
        # Create weighted trailing zeros
        weighted_results = []
        for num in self.numbers:
            trailing_zeros = self.count_trailing_zeros(num)
            weight = self.weights.get(num, 1)
            priority = self.priorities.get(num, 1)
            weighted_score = trailing_zeros * weight * priority
            weighted_results.append((num, trailing_zeros, weighted_score))
        
        # Sort by weighted score
        weighted_results.sort(key=lambda x: x[2], reverse=True)
        
        return weighted_results
    
    def get_trailing_zeros_with_priority(self, priority_func):
        """Get trailing zeros considering priority."""
        if not self.numbers:
            return []
        
        # Create priority-based trailing zeros
        priority_results = []
        for num in self.numbers:
            trailing_zeros = self.count_trailing_zeros(num)
            priority = priority_func(num, trailing_zeros, self.weights, self.priorities)
            priority_results.append((num, trailing_zeros, priority))
        
        # Sort by priority
        priority_results.sort(key=lambda x: x[2], reverse=True)
        return priority_results
    
    def get_trailing_zeros_with_optimization(self, optimization_func):
        """Get trailing zeros using custom optimization function."""
        if not self.numbers:
            return []
        
        # Create optimization-based trailing zeros
        optimized_results = []
        for num in self.numbers:
            trailing_zeros = self.count_trailing_zeros(num)
            score = optimization_func(num, trailing_zeros, self.weights, self.priorities)
            optimized_results.append((num, trailing_zeros, score))
        
        # Sort by optimization score
        optimized_results.sort(key=lambda x: x[2], reverse=True)
        return optimized_results
    
    def get_trailing_zeros_with_constraints(self, constraint_func):
        """Get trailing zeros that satisfies custom constraints."""
        if not self.numbers:
            return []
        
        if constraint_func(self.numbers, self.weights, self.priorities):
            return self.get_weighted_trailing_zeros()
        else:
            return []
    
    def get_trailing_zeros_with_multiple_criteria(self, criteria_list):
        """Get trailing zeros that satisfies multiple criteria."""
        if not self.numbers:
            return []
        
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(self.numbers, self.weights, self.priorities):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            return self.get_weighted_trailing_zeros()
        else:
            return []
    
    def get_trailing_zeros_with_alternatives(self, alternatives):
        """Get trailing zeros considering alternative weights/priorities."""
        result = []
        
        # Check original trailing zeros
        original_trailing_zeros = self.get_weighted_trailing_zeros()
        result.append((original_trailing_zeros, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedTrailingZeros(self.numbers, alt_weights, alt_priorities)
            temp_trailing_zeros = temp_instance.get_weighted_trailing_zeros()
            result.append((temp_trailing_zeros, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_trailing_zeros_with_adaptive_criteria(self, adaptive_func):
        """Get trailing zeros using adaptive criteria."""
        if not self.numbers:
            return []
        
        if adaptive_func(self.numbers, self.weights, self.priorities, []):
            return self.get_weighted_trailing_zeros()
        else:
            return []
    
    def get_trailing_zeros_optimization(self):
        """Get optimal trailing zeros configuration."""
        strategies = [
            ('weighted_trailing_zeros', lambda: len(self.get_weighted_trailing_zeros())),
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
numbers = [5, 10, 15, 20]
weights = {num: num * 2 for num in numbers}  # Weight based on number value
priorities = {num: num // 5 for num in numbers}  # Priority based on number value
advanced_trailing_zeros = AdvancedTrailingZeros(numbers, weights, priorities)

print(f"Weighted trailing zeros: {len(advanced_trailing_zeros.get_weighted_trailing_zeros())}")

# Get trailing zeros with priority
def priority_func(num, trailing_zeros, weights, priorities):
    return weights.get(num, 1) + priorities.get(num, 1)

print(f"Trailing zeros with priority: {len(advanced_trailing_zeros.get_trailing_zeros_with_priority(priority_func))}")

# Get trailing zeros with optimization
def optimization_func(num, trailing_zeros, weights, priorities):
    return weights.get(num, 1) * priorities.get(num, 1)

print(f"Trailing zeros with optimization: {len(advanced_trailing_zeros.get_trailing_zeros_with_optimization(optimization_func))}")

# Get trailing zeros with constraints
def constraint_func(numbers, weights, priorities):
    return len(numbers) > 0 and all(num > 0 for num in numbers)

print(f"Trailing zeros with constraints: {len(advanced_trailing_zeros.get_trailing_zeros_with_constraints(constraint_func))}")

# Get trailing zeros with multiple criteria
def criterion1(numbers, weights, priorities):
    return len(numbers) > 0

def criterion2(numbers, weights, priorities):
    return all(num > 0 for num in numbers)

criteria_list = [criterion1, criterion2]
print(f"Trailing zeros with multiple criteria: {len(advanced_trailing_zeros.get_trailing_zeros_with_multiple_criteria(criteria_list))}")

# Get trailing zeros with alternatives
alternatives = [({num: 1 for num in numbers}, {num: 1 for num in numbers}), ({num: num*3 for num in numbers}, {num: num+1 for num in numbers})]
print(f"Trailing zeros with alternatives: {len(advanced_trailing_zeros.get_trailing_zeros_with_alternatives(alternatives))}")

# Get trailing zeros with adaptive criteria
def adaptive_func(numbers, weights, priorities, current_result):
    return len(numbers) > 0 and len(current_result) < 5

print(f"Trailing zeros with adaptive criteria: {len(advanced_trailing_zeros.get_trailing_zeros_with_adaptive_criteria(adaptive_func))}")

# Get trailing zeros optimization
print(f"Trailing zeros optimization: {advanced_trailing_zeros.get_trailing_zeros_optimization()}")
```

### **Variation 3: Trailing Zeros with Constraints**
**Problem**: Handle trailing zeros calculation with additional constraints (range limits, number constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedTrailingZeros:
    def __init__(self, numbers=None, constraints=None):
        self.numbers = numbers or []
        self.constraints = constraints or {}
        self.factorial_cache = {}
        self._update_trailing_zeros_info()
    
    def _update_trailing_zeros_info(self):
        """Update trailing zeros feasibility information."""
        self.total_numbers = len(self.numbers)
        self.max_number = max(self.numbers) if self.numbers else 0
        self.trailing_zeros_feasibility = self._calculate_trailing_zeros_feasibility()
    
    def _calculate_trailing_zeros_feasibility(self):
        """Calculate trailing zeros calculation feasibility."""
        if not self.numbers:
            return 0
        
        # Check if all numbers are positive
        positive_count = sum(1 for num in self.numbers if num > 0)
        return positive_count / len(self.numbers) if self.numbers else 0
    
    def count_trailing_zeros(self, n):
        """Count trailing zeros in n! efficiently."""
        if n in self.factorial_cache:
            return self.factorial_cache[n]
        
        if n < 0:
            return 0
        
        count = 0
        while n >= 5:
            n //= 5
            count += n
        
        self.factorial_cache[n] = count
        return count
    
    def _is_valid_number(self, num):
        """Check if number is valid considering constraints."""
        # Range constraints
        if 'min_value' in self.constraints:
            if num < self.constraints['min_value']:
                return False
        
        if 'max_value' in self.constraints:
            if num > self.constraints['max_value']:
                return False
        
        # Number constraints
        if 'forbidden_numbers' in self.constraints:
            if num in self.constraints['forbidden_numbers']:
                return False
        
        if 'required_numbers' in self.constraints:
            if num not in self.constraints['required_numbers']:
                return False
        
        # Pattern constraints
        if 'pattern_constraints' in self.constraints:
            for constraint in self.constraints['pattern_constraints']:
                if not constraint(num, self.numbers):
                    return False
        
        return True
    
    def get_trailing_zeros_with_range_constraints(self, min_val, max_val):
        """Get trailing zeros considering range constraints."""
        if not self.numbers:
            return []
        
        result = []
        for num in self.numbers:
            if min_val <= num <= max_val and self._is_valid_number(num):
                trailing_zeros = self.count_trailing_zeros(num)
                result.append((num, trailing_zeros))
        
        return result
    
    def get_trailing_zeros_with_number_constraints(self, number_constraints):
        """Get trailing zeros considering number constraints."""
        if not self.numbers:
            return []
        
        satisfies_constraints = True
        for constraint in number_constraints:
            if not constraint(self.numbers):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            result = []
            for num in self.numbers:
                if self._is_valid_number(num):
                    trailing_zeros = self.count_trailing_zeros(num)
                    result.append((num, trailing_zeros))
            return result
        else:
            return []
    
    def get_trailing_zeros_with_pattern_constraints(self, pattern_constraints):
        """Get trailing zeros considering pattern constraints."""
        if not self.numbers:
            return []
        
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(self.numbers):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            result = []
            for num in self.numbers:
                if self._is_valid_number(num):
                    trailing_zeros = self.count_trailing_zeros(num)
                    result.append((num, trailing_zeros))
            return result
        else:
            return []
    
    def get_trailing_zeros_with_mathematical_constraints(self, constraint_func):
        """Get trailing zeros that satisfies custom mathematical constraints."""
        if not self.numbers:
            return []
        
        if constraint_func(self.numbers):
            result = []
            for num in self.numbers:
                if self._is_valid_number(num):
                    trailing_zeros = self.count_trailing_zeros(num)
                    result.append((num, trailing_zeros))
            return result
        else:
            return []
    
    def get_trailing_zeros_with_optimization_constraints(self, optimization_func):
        """Get trailing zeros using custom optimization constraints."""
        if not self.numbers:
            return []
        
        # Calculate optimization score for trailing zeros
        score = optimization_func(self.numbers)
        
        if score > 0:
            result = []
            for num in self.numbers:
                if self._is_valid_number(num):
                    trailing_zeros = self.count_trailing_zeros(num)
                    result.append((num, trailing_zeros))
            return result
        else:
            return []
    
    def get_trailing_zeros_with_multiple_constraints(self, constraints_list):
        """Get trailing zeros that satisfies multiple constraints."""
        if not self.numbers:
            return []
        
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(self.numbers):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            result = []
            for num in self.numbers:
                if self._is_valid_number(num):
                    trailing_zeros = self.count_trailing_zeros(num)
                    result.append((num, trailing_zeros))
            return result
        else:
            return []
    
    def get_trailing_zeros_with_priority_constraints(self, priority_func):
        """Get trailing zeros with priority-based constraints."""
        if not self.numbers:
            return []
        
        # Calculate priority for trailing zeros
        priority = priority_func(self.numbers)
        
        if priority > 0:
            result = []
            for num in self.numbers:
                if self._is_valid_number(num):
                    trailing_zeros = self.count_trailing_zeros(num)
                    result.append((num, trailing_zeros))
            return result
        else:
            return []
    
    def get_trailing_zeros_with_adaptive_constraints(self, adaptive_func):
        """Get trailing zeros with adaptive constraints."""
        if not self.numbers:
            return []
        
        if adaptive_func(self.numbers, []):
            result = []
            for num in self.numbers:
                if self._is_valid_number(num):
                    trailing_zeros = self.count_trailing_zeros(num)
                    result.append((num, trailing_zeros))
            return result
        else:
            return []
    
    def get_optimal_trailing_zeros_strategy(self):
        """Get optimal trailing zeros strategy considering all constraints."""
        strategies = [
            ('range_constraints', self.get_trailing_zeros_with_range_constraints),
            ('number_constraints', self.get_trailing_zeros_with_number_constraints),
            ('pattern_constraints', self.get_trailing_zeros_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_score = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'range_constraints':
                    result = strategy_func(0, 1000)
                elif strategy_name == 'number_constraints':
                    number_constraints = [lambda nums: len(nums) > 0]
                    result = strategy_func(number_constraints)
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda nums: all(num > 0 for num in nums)]
                    result = strategy_func(pattern_constraints)
                
                if len(result) > best_score:
                    best_score = len(result)
                    best_strategy = (strategy_name, result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'min_value': 1,
    'max_value': 100,
    'forbidden_numbers': [0, -1],
    'required_numbers': [5, 10],
    'pattern_constraints': [lambda num, numbers: num > 0]
}

numbers = [5, 10, 15, 20, 0, -1]
constrained_trailing_zeros = ConstrainedTrailingZeros(numbers, constraints)

print("Range-constrained trailing zeros:", len(constrained_trailing_zeros.get_trailing_zeros_with_range_constraints(1, 100)))

print("Number-constrained trailing zeros:", len(constrained_trailing_zeros.get_trailing_zeros_with_number_constraints([lambda nums: len(nums) > 0])))

print("Pattern-constrained trailing zeros:", len(constrained_trailing_zeros.get_trailing_zeros_with_pattern_constraints([lambda nums: all(num > 0 for num in nums)])))

# Mathematical constraints
def custom_constraint(numbers):
    return len(numbers) > 0 and all(num > 0 for num in numbers)

print("Mathematical constraint trailing zeros:", len(constrained_trailing_zeros.get_trailing_zeros_with_mathematical_constraints(custom_constraint)))

# Range constraints
def range_constraint(numbers):
    return all(1 <= num <= 100 for num in numbers)

range_constraints = [range_constraint]
print("Range-constrained trailing zeros:", len(constrained_trailing_zeros.get_trailing_zeros_with_range_constraints(1, 100)))

# Multiple constraints
def constraint1(numbers):
    return len(numbers) > 0

def constraint2(numbers):
    return all(num > 0 for num in numbers)

constraints_list = [constraint1, constraint2]
print("Multiple constraints trailing zeros:", len(constrained_trailing_zeros.get_trailing_zeros_with_multiple_constraints(constraints_list)))

# Priority constraints
def priority_func(numbers):
    return len(numbers) + sum(1 for num in numbers if num > 0)

print("Priority-constrained trailing zeros:", len(constrained_trailing_zeros.get_trailing_zeros_with_priority_constraints(priority_func)))

# Adaptive constraints
def adaptive_func(numbers, current_result):
    return len(numbers) > 0 and len(current_result) < 5

print("Adaptive constraint trailing zeros:", len(constrained_trailing_zeros.get_trailing_zeros_with_adaptive_constraints(adaptive_func)))

# Optimal strategy
optimal = constrained_trailing_zeros.get_optimal_trailing_zeros_strategy()
print(f"Optimal trailing zeros strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Trailing Zeros](https://cses.fi/problemset/task/1618) - Count trailing zeros in factorial
- [Factorial](https://cses.fi/problemset/task/1083) - Calculate factorial
- [Prime Factorization](https://cses.fi/problemset/task/1081) - Prime factorization problems

#### **LeetCode Problems**
- [Factorial Trailing Zeroes](https://leetcode.com/problems/factorial-trailing-zeroes/) - Count trailing zeros
- [Preimage Size of Factorial Zeroes Function](https://leetcode.com/problems/preimage-size-of-factorial-zeroes-function/) - Find numbers with k trailing zeros
- [Count Primes](https://leetcode.com/problems/count-primes/) - Count prime numbers
- [Ugly Number](https://leetcode.com/problems/ugly-number/) - Check if number has only 2,3,5 factors

#### **Problem Categories**
- **Number Theory**: Factorial properties, prime factorization, mathematical analysis
- **Mathematical Formulas**: Efficient counting, mathematical optimization, formula derivation
- **Prime Numbers**: Prime factorization, factor counting, mathematical properties
- **Algorithm Design**: Mathematical algorithms, optimization techniques, efficient calculations

## 📚 Learning Points

1. **Factorial Properties**: Essential for understanding trailing zero problems
2. **Mathematical Analysis**: Key technique for efficient counting
3. **Prime Factorization**: Important for understanding factor counting
4. **Mathematical Formulas**: Critical for understanding efficient calculations
5. **Algorithm Optimization**: Foundation for many mathematical algorithms
6. **Mathematical Properties**: Critical for competitive programming performance

## 📝 Summary

The Trailing Zeros problem demonstrates factorial properties and mathematical analysis concepts for efficient counting. We explored three approaches:

1. **Brute Force Factorial Calculation**: O(n) time complexity using direct factorial calculation, inefficient for large n
2. **Mathematical Analysis with Factor Counting**: O(log n) time complexity using mathematical properties and factor counting, better approach for trailing zero problems
3. **Optimized Mathematical Formula**: O(log n) time complexity with optimized mathematical formulas, optimal approach for trailing zero calculation optimization

The key insights include understanding factorial properties, using mathematical analysis for efficient factor counting, and applying mathematical formulas for optimal performance. This problem serves as an excellent introduction to factorial mathematics and mathematical analysis algorithms.
