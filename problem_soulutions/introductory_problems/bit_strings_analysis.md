---
layout: simple
title: "Bit Strings"
permalink: /problem_soulutions/introductory_problems/bit_strings_analysis
---

# Bit Strings

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of counting and combinatorics in introductory problems
- Apply efficient algorithms for counting bit strings with constraints
- Implement modular arithmetic for large number calculations
- Optimize algorithms for counting problems with constraints
- Handle special cases in combinatorics problems

## 📋 Problem Description

Count the number of bit strings of length n that do not contain two consecutive 1s.

**Input**: 
- n: length of bit string

**Output**: 
- Number of valid bit strings modulo 10^9 + 7

**Constraints**:
- 1 ≤ n ≤ 10^6

**Example**:
```
Input:
n = 3

Output:
5

Explanation**: 
Valid bit strings of length 3:
000, 001, 010, 100, 101
Invalid bit strings: 011, 110, 111
Total: 5 valid strings
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Generate all possible bit strings and check constraints
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Check each bit string for consecutive 1s
- **Inefficient**: O(2^n × n) time complexity

**Key Insight**: Generate all possible bit strings and count those without consecutive 1s.

**Algorithm**:
- Generate all possible bit strings of length n
- For each bit string, check if it contains consecutive 1s
- Count the valid bit strings
- Return the count modulo 10^9 + 7

**Visual Example**:
```
Bit strings of length 3:

Generate all 2^3 = 8 bit strings:
┌─────────────────────────────────────┐
│ String 1: 000                      │
│ - Check: No consecutive 1s ✓       │
│ - Valid ✓                          │
│                                   │
│ String 2: 001                      │
│ - Check: No consecutive 1s ✓       │
│ - Valid ✓                          │
│                                   │
│ String 3: 010                      │
│ - Check: No consecutive 1s ✓       │
│ - Valid ✓                          │
│                                   │
│ String 4: 011                      │
│ - Check: Has consecutive 1s ✗      │
│ - Invalid ✗                        │
│                                   │
│ String 5: 100                      │
│ - Check: No consecutive 1s ✓       │
│ - Valid ✓                          │
│                                   │
│ String 6: 101                      │
│ - Check: No consecutive 1s ✓       │
│ - Valid ✓                          │
│                                   │
│ String 7: 110                      │
│ - Check: Has consecutive 1s ✗      │
│ - Invalid ✗                        │
│                                   │
│ String 8: 111                      │
│ - Check: Has consecutive 1s ✗      │
│ - Invalid ✗                        │
│                                   │
│ Valid strings: 000, 001, 010, 100, 101 │
│ Total: 5                           │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_bit_strings(n):
    """Count valid bit strings using brute force approach"""
    MOD = 10**9 + 7
    count = 0
    
    # Generate all possible bit strings
    for i in range(1 << n):
        bit_string = format(i, f'0{n}b')
        
        # Check if bit string has consecutive 1s
        has_consecutive_ones = False
        for j in range(len(bit_string) - 1):
            if bit_string[j] == '1' and bit_string[j + 1] == '1':
                has_consecutive_ones = True
                break
        
        if not has_consecutive_ones:
            count += 1
    
    return count % MOD

# Example usage
n = 3
result = brute_force_bit_strings(n)
print(f"Brute force count: {result}")
```

**Time Complexity**: O(2^n × n)
**Space Complexity**: O(n)

**Why it's inefficient**: O(2^n × n) time complexity for generating and checking all bit strings.

---

### Approach 2: Dynamic Programming

**Key Insights from Dynamic Programming**:
- **Recurrence Relation**: Use DP to avoid recalculating subproblems
- **Efficient Implementation**: O(n) time complexity
- **State Definition**: dp[i] = number of valid bit strings of length i
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use dynamic programming with recurrence relation to count valid bit strings.

**Algorithm**:
- Define dp[i] as number of valid bit strings of length i
- Base cases: dp[1] = 2, dp[2] = 3
- Recurrence: dp[i] = dp[i-1] + dp[i-2]
- Return dp[n] modulo 10^9 + 7

**Visual Example**:
```
Dynamic Programming:

For n = 3:
┌─────────────────────────────────────┐
│ Base cases:                        │
│ - dp[1] = 2 (0, 1)                │
│ - dp[2] = 3 (00, 01, 10)          │
│                                   │
│ Recurrence relation:               │
│ dp[i] = dp[i-1] + dp[i-2]         │
│                                   │
│ Calculation:                       │
│ - dp[3] = dp[2] + dp[1] = 3 + 2 = 5 │
│                                   │
│ Explanation:                       │
│ - dp[i-1]: strings ending with 0   │
│ - dp[i-2]: strings ending with 01  │
│ - Total: all valid strings of length i │
│                                   │
│ Result: 5                          │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def dp_bit_strings(n):
    """Count valid bit strings using dynamic programming"""
    MOD = 10**9 + 7
    
    if n == 1:
        return 2
    if n == 2:
        return 3
    
    # Initialize DP array
    dp = [0] * (n + 1)
    dp[1] = 2  # 0, 1
    dp[2] = 3  # 00, 01, 10
    
    # Fill DP array
    for i in range(3, n + 1):
        dp[i] = (dp[i-1] + dp[i-2]) % MOD
    
    return dp[n]

# Example usage
n = 3
result = dp_bit_strings(n)
print(f"DP count: {result}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Why it's better**: Uses dynamic programming for O(n) time complexity.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for counting
- **Efficient Implementation**: O(n) time complexity
- **Space Efficiency**: O(1) space complexity
- **Optimal Complexity**: Best approach for counting problems

**Key Insight**: Use advanced data structures for optimal counting.

**Algorithm**:
- Use specialized data structures for counting
- Implement efficient DP with space optimization
- Handle special cases optimally
- Return count modulo 10^9 + 7

**Visual Example**:
```
Advanced data structure approach:

For n = 3:
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Advanced counter: for efficient   │
│   counting                          │
│ - Modular arithmetic: for optimization│
│ - Space optimization: for efficiency│
│                                   │
│ Counting calculation:               │
│ - Use advanced counter for efficient│
│   counting                          │
│ - Use modular arithmetic for       │
│   optimization                      │
│ - Use space optimization for       │
│   efficiency                        │
│                                   │
│ Result: 5                          │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_bit_strings(n):
    """Count valid bit strings using advanced data structure approach"""
    MOD = 10**9 + 7
    
    if n == 1:
        return 2
    if n == 2:
        return 3
    
    # Use space-optimized DP
    prev2 = 2  # dp[i-2]
    prev1 = 3  # dp[i-1]
    
    # Advanced DP with space optimization
    for i in range(3, n + 1):
        current = (prev1 + prev2) % MOD
        prev2 = prev1
        prev1 = current
    
    return prev1

# Example usage
n = 3
result = advanced_data_structure_bit_strings(n)
print(f"Advanced data structure count: {result}")
```

**Time Complexity**: O(n)
**Space Complexity**: O(1)

**Why it's optimal**: Uses advanced data structures for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^n × n) | O(n) | Generate all bit strings and check |
| Dynamic Programming | O(n) | O(n) | Use recurrence relation dp[i] = dp[i-1] + dp[i-2] |
| Advanced Data Structure | O(n) | O(1) | Use space-optimized DP |

### Time Complexity
- **Time**: O(n) - Use dynamic programming for efficient counting
- **Space**: O(1) - Use space-optimized DP

### Why This Solution Works
- **Recurrence Relation**: Use dp[i] = dp[i-1] + dp[i-2] to avoid recalculating
- **Base Cases**: Handle small cases directly
- **Modular Arithmetic**: Use modulo to handle large numbers
- **Optimal Algorithms**: Use optimal algorithms for counting problems

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Bit Strings with Constraints**
**Problem**: Count bit strings with specific constraints.

**Key Differences**: Apply constraints to counting

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_bit_strings(n, constraints):
    """Count valid bit strings with constraints"""
    MOD = 10**9 + 7
    
    if n == 1:
        return 2 if constraints(1) else 0
    if n == 2:
        return 3 if constraints(2) else 0
    
    prev2 = 2
    prev1 = 3
    
    for i in range(3, n + 1):
        current = (prev1 + prev2) % MOD
        if not constraints(i):
            current = 0
        prev2 = prev1
        prev1 = current
    
    return prev1

# Example usage
n = 3
constraints = lambda i: True  # No constraints
result = constrained_bit_strings(n, constraints)
print(f"Constrained count: {result}")
```

#### **2. Bit Strings with Different Metrics**
**Problem**: Count bit strings with different cost metrics.

**Key Differences**: Different cost calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_bit_strings(n, weight_function):
    """Count valid bit strings with different cost metrics"""
    MOD = 10**9 + 7
    
    if n == 1:
        return weight_function(1, 2)
    if n == 2:
        return weight_function(2, 3)
    
    prev2 = weight_function(1, 2)
    prev1 = weight_function(2, 3)
    
    for i in range(3, n + 1):
        current = (prev1 + prev2) % MOD
        current = weight_function(i, current)
        prev2 = prev1
        prev1 = current
    
    return prev1

# Example usage
n = 3
weight_function = lambda i, count: count  # No modification
result = weighted_bit_strings(n, weight_function)
print(f"Weighted count: {result}")
```

#### **3. Bit Strings with Multiple Dimensions**
**Problem**: Count bit strings in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_bit_strings(n, dimensions):
    """Count valid bit strings in multiple dimensions"""
    MOD = 10**9 + 7
    
    if n == 1:
        return 2
    if n == 2:
        return 3
    
    prev2 = 2
    prev1 = 3
    
    for i in range(3, n + 1):
        current = (prev1 + prev2) % MOD
        prev2 = prev1
        prev1 = current
    
    return prev1

# Example usage
n = 3
dimensions = 1
result = multi_dimensional_bit_strings(n, dimensions)
print(f"Multi-dimensional count: {result}")
```

## Problem Variations

### **Variation 1: Bit Strings with Dynamic Updates**
**Problem**: Handle dynamic bit string length updates (add/remove bits) while maintaining valid bit string count.

**Approach**: Use efficient data structures and algorithms for dynamic bit string management.

```python
from collections import defaultdict
import itertools

class DynamicBitStrings:
    def __init__(self, n):
        self.n = n
        self.MOD = 10**9 + 7
        self.count = self._calculate_count()
        self.valid_strings = self._generate_valid_strings()
    
    def _calculate_count(self):
        """Calculate count of valid bit strings using dynamic programming."""
        if self.n == 0:
            return 0
        if self.n == 1:
            return 2
        if self.n == 2:
            return 3
        
        prev2 = 2
        prev1 = 3
        
        for i in range(3, self.n + 1):
            current = (prev1 + prev2) % self.MOD
            prev2 = prev1
            prev1 = current
        
        return prev1
    
    def _generate_valid_strings(self):
        """Generate all valid bit strings."""
        if self.n == 0:
            return []
        if self.n == 1:
            return ['0', '1']
        if self.n == 2:
            return ['00', '01', '10']
        
        # Generate valid strings using recursive approach
        result = []
        
        def generate_strings(current, length):
            if length == self.n:
                result.append(current)
                return
            
            # Add '0' (always valid)
            generate_strings(current + '0', length + 1)
            
            # Add '1' only if previous character is not '1'
            if length == 0 or current[-1] != '1':
                generate_strings(current + '1', length + 1)
        
        generate_strings('', 0)
        return result
    
    def add_bit(self, position=None):
        """Add a bit at specified position (or at end)."""
        if position is None:
            position = self.n
        
        self.n += 1
        self.count = self._calculate_count()
        self.valid_strings = self._generate_valid_strings()
    
    def remove_bit(self, position):
        """Remove bit at specified position."""
        if 0 <= position < self.n:
            self.n -= 1
            self.count = self._calculate_count()
            self.valid_strings = self._generate_valid_strings()
    
    def get_count(self):
        """Get current count of valid bit strings."""
        return self.count
    
    def get_valid_strings(self):
        """Get current valid bit strings."""
        return self.valid_strings
    
    def get_strings_with_constraints(self, constraint_func):
        """Get bit strings that satisfy custom constraints."""
        result = []
        for bit_string in self.valid_strings:
            if constraint_func(bit_string):
                result.append(bit_string)
        return result
    
    def get_strings_in_range(self, start_pattern, end_pattern):
        """Get bit strings within specified pattern range."""
        result = []
        for bit_string in self.valid_strings:
            if start_pattern <= bit_string <= end_pattern:
                result.append(bit_string)
        return result
    
    def get_strings_with_pattern(self, pattern):
        """Get bit strings containing specified pattern."""
        result = []
        for bit_string in self.valid_strings:
            if pattern in bit_string:
                result.append(bit_string)
        return result
    
    def get_string_statistics(self):
        """Get statistics about bit strings."""
        if not self.valid_strings:
            return {
                'total_strings': 0,
                'strings_with_0': 0,
                'strings_with_1': 0,
                'average_length': 0,
                'pattern_distribution': {}
            }
        
        total_strings = len(self.valid_strings)
        strings_with_0 = sum(1 for s in self.valid_strings if '0' in s)
        strings_with_1 = sum(1 for s in self.valid_strings if '1' in s)
        average_length = sum(len(s) for s in self.valid_strings) / total_strings
        
        # Calculate pattern distribution
        pattern_distribution = defaultdict(int)
        for bit_string in self.valid_strings:
            for i in range(len(bit_string) - 1):
                pattern = bit_string[i:i+2]
                pattern_distribution[pattern] += 1
        
        return {
            'total_strings': total_strings,
            'strings_with_0': strings_with_0,
            'strings_with_1': strings_with_1,
            'average_length': average_length,
            'pattern_distribution': dict(pattern_distribution)
        }
    
    def get_string_patterns(self):
        """Get patterns in bit strings."""
        patterns = {
            'consecutive_0s': 0,
            'consecutive_1s': 0,
            'alternating_patterns': 0,
            'palindromic_strings': 0
        }
        
        for bit_string in self.valid_strings:
            # Check for consecutive 0s
            if '00' in bit_string:
                patterns['consecutive_0s'] += 1
            
            # Check for consecutive 1s (should be 0 for valid strings)
            if '11' in bit_string:
                patterns['consecutive_1s'] += 1
            
            # Check for alternating patterns
            alternating = True
            for i in range(1, len(bit_string)):
                if bit_string[i] == bit_string[i-1]:
                    alternating = False
                    break
            if alternating:
                patterns['alternating_patterns'] += 1
            
            # Check for palindromic strings
            if bit_string == bit_string[::-1]:
                patterns['palindromic_strings'] += 1
        
        return patterns
    
    def get_optimal_string_strategy(self):
        """Get optimal strategy for bit string operations."""
        if self.n == 0:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'validity_rate': 0
            }
        
        # Calculate efficiency rate
        total_possible = 2 ** self.n
        efficiency_rate = self.count / total_possible if total_possible > 0 else 0
        
        # Calculate validity rate
        valid_strings = len(self.valid_strings)
        validity_rate = valid_strings / self.count if self.count > 0 else 0
        
        # Determine recommended strategy
        if efficiency_rate > 0.5:
            recommended_strategy = 'dp_optimal'
        elif validity_rate > 0.8:
            recommended_strategy = 'recursive_generation'
        else:
            recommended_strategy = 'brute_force'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'validity_rate': validity_rate
        }

# Example usage
n = 4
dynamic_bit_strings = DynamicBitStrings(n)
print(f"Initial count: {dynamic_bit_strings.get_count()}")

# Add a bit
dynamic_bit_strings.add_bit()
print(f"After adding bit: {dynamic_bit_strings.get_count()}")

# Remove a bit
dynamic_bit_strings.remove_bit(0)
print(f"After removing bit: {dynamic_bit_strings.get_count()}")

# Get strings with constraints
def constraint_func(bit_string):
    return bit_string.count('1') <= 2

print(f"Strings with at most 2 ones: {len(dynamic_bit_strings.get_strings_with_constraints(constraint_func))}")

# Get strings in range
print(f"Strings in range ['00', '10']: {len(dynamic_bit_strings.get_strings_in_range('00', '10'))}")

# Get strings with pattern
print(f"Strings containing '01': {len(dynamic_bit_strings.get_strings_with_pattern('01'))}")

# Get statistics
print(f"Statistics: {dynamic_bit_strings.get_string_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_bit_strings.get_string_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_bit_strings.get_optimal_string_strategy()}")
```

### **Variation 2: Bit Strings with Different Operations**
**Problem**: Handle different types of operations on bit strings (weighted bits, priority-based selection, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of bit string queries.

```python
class AdvancedBitStrings:
    def __init__(self, n, weights=None, priorities=None):
        self.n = n
        self.weights = weights or [1] * n
        self.priorities = priorities or [1] * n
        self.MOD = 10**9 + 7
        self.count = self._calculate_count()
        self.valid_strings = self._generate_valid_strings()
        self.weighted_strings = self._generate_weighted_strings()
    
    def _calculate_count(self):
        """Calculate count of valid bit strings using dynamic programming."""
        if self.n == 0:
            return 0
        if self.n == 1:
            return 2
        if self.n == 2:
            return 3
        
        prev2 = 2
        prev1 = 3
        
        for i in range(3, self.n + 1):
            current = (prev1 + prev2) % self.MOD
            prev2 = prev1
            prev1 = current
        
        return prev1
    
    def _generate_valid_strings(self):
        """Generate all valid bit strings."""
        if self.n == 0:
            return []
        if self.n == 1:
            return ['0', '1']
        if self.n == 2:
            return ['00', '01', '10']
        
        result = []
        
        def generate_strings(current, length):
            if length == self.n:
                result.append(current)
                return
            
            # Add '0' (always valid)
            generate_strings(current + '0', length + 1)
            
            # Add '1' only if previous character is not '1'
            if length == 0 or current[-1] != '1':
                generate_strings(current + '1', length + 1)
        
        generate_strings('', 0)
        return result
    
    def _generate_weighted_strings(self):
        """Generate weighted bit strings."""
        result = []
        for bit_string in self.valid_strings:
            weighted_string = {
                'string': bit_string,
                'weight': sum(self.weights[i] for i in range(len(bit_string)) if bit_string[i] == '1'),
                'priority': sum(self.priorities[i] for i in range(len(bit_string)) if bit_string[i] == '1')
            }
            result.append(weighted_string)
        return result
    
    def get_strings(self):
        """Get current valid bit strings."""
        return self.valid_strings
    
    def get_weighted_strings(self):
        """Get weighted bit strings."""
        return self.weighted_strings
    
    def get_strings_with_priority(self, priority_func):
        """Get bit strings considering priority."""
        result = []
        for bit_string in self.valid_strings:
            priority = priority_func(bit_string, self.weights, self.priorities)
            result.append((bit_string, priority))
        
        # Sort by priority
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_strings_with_optimization(self, optimization_func):
        """Get bit strings using custom optimization function."""
        result = []
        for bit_string in self.valid_strings:
            score = optimization_func(bit_string, self.weights, self.priorities)
            result.append((bit_string, score))
        
        # Sort by optimization score
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_strings_with_constraints(self, constraint_func):
        """Get bit strings that satisfy custom constraints."""
        result = []
        for bit_string in self.valid_strings:
            if constraint_func(bit_string, self.weights, self.priorities):
                result.append(bit_string)
        return result
    
    def get_strings_with_multiple_criteria(self, criteria_list):
        """Get bit strings that satisfy multiple criteria."""
        result = []
        for bit_string in self.valid_strings:
            satisfies_all_criteria = True
            for criterion in criteria_list:
                if not criterion(bit_string, self.weights, self.priorities):
                    satisfies_all_criteria = False
                    break
            if satisfies_all_criteria:
                result.append(bit_string)
        return result
    
    def get_strings_with_alternatives(self, alternatives):
        """Get bit strings considering alternative weights/priorities."""
        result = []
        
        # Check original strings
        for bit_string in self.valid_strings:
            result.append((bit_string, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedBitStrings(self.n, alt_weights, alt_priorities)
            temp_strings = temp_instance.get_valid_strings()
            result.append((temp_strings, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_strings_with_adaptive_criteria(self, adaptive_func):
        """Get bit strings using adaptive criteria."""
        result = []
        for bit_string in self.valid_strings:
            if adaptive_func(bit_string, self.weights, self.priorities, result):
                result.append(bit_string)
        return result
    
    def get_string_optimization(self):
        """Get optimal bit string configuration."""
        strategies = [
            ('strings', lambda: len(self.valid_strings)),
            ('weighted_strings', lambda: len(self.weighted_strings)),
            ('count', lambda: self.count),
        ]
        
        best_strategy = None
        best_value = 0
        
        for strategy_name, strategy_func in strategies:
            current_value = strategy_func()
            if current_value > best_value:
                best_value = current_value
                best_strategy = (strategy_name, current_value)
        
        return best_strategy

# Example usage
n = 4
weights = [2, 1, 3, 1]
priorities = [1, 2, 1, 3]
advanced_bit_strings = AdvancedBitStrings(n, weights, priorities)

print(f"Strings: {len(advanced_bit_strings.get_strings())}")
print(f"Weighted strings: {len(advanced_bit_strings.get_weighted_strings())}")

# Get strings with priority
def priority_func(bit_string, weights, priorities):
    return sum(weights[i] for i in range(len(bit_string)) if bit_string[i] == '1') + sum(priorities[i] for i in range(len(bit_string)) if bit_string[i] == '1')

print(f"Strings with priority: {len(advanced_bit_strings.get_strings_with_priority(priority_func))}")

# Get strings with optimization
def optimization_func(bit_string, weights, priorities):
    return sum(weights[i] * priorities[i] for i in range(len(bit_string)) if bit_string[i] == '1')

print(f"Strings with optimization: {len(advanced_bit_strings.get_strings_with_optimization(optimization_func))}")

# Get strings with constraints
def constraint_func(bit_string, weights, priorities):
    return bit_string.count('1') <= 2 and sum(weights[i] for i in range(len(bit_string)) if bit_string[i] == '1') <= 5

print(f"Strings with constraints: {len(advanced_bit_strings.get_strings_with_constraints(constraint_func))}")

# Get strings with multiple criteria
def criterion1(bit_string, weights, priorities):
    return bit_string.count('1') <= 2

def criterion2(bit_string, weights, priorities):
    return sum(weights[i] for i in range(len(bit_string)) if bit_string[i] == '1') <= 5

criteria_list = [criterion1, criterion2]
print(f"Strings with multiple criteria: {len(advanced_bit_strings.get_strings_with_multiple_criteria(criteria_list))}")

# Get strings with alternatives
alternatives = [([1, 1, 1, 1], [1, 1, 1, 1]), ([3, 2, 1, 4], [2, 1, 3, 1])]
print(f"Strings with alternatives: {len(advanced_bit_strings.get_strings_with_alternatives(alternatives))}")

# Get strings with adaptive criteria
def adaptive_func(bit_string, weights, priorities, current_result):
    return bit_string.count('1') <= 2 and len(current_result) < 5

print(f"Strings with adaptive criteria: {len(advanced_bit_strings.get_strings_with_adaptive_criteria(adaptive_func))}")

# Get string optimization
print(f"String optimization: {advanced_bit_strings.get_string_optimization()}")
```

### **Variation 3: Bit Strings with Constraints**
**Problem**: Handle bit strings with additional constraints (length limits, pattern constraints, weight constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedBitStrings:
    def __init__(self, n, constraints=None):
        self.n = n
        self.constraints = constraints or {}
        self.MOD = 10**9 + 7
        self.count = self._calculate_count()
        self.valid_strings = self._generate_valid_strings()
    
    def _calculate_count(self):
        """Calculate count of valid bit strings considering constraints."""
        if self.n == 0:
            return 0
        if self.n == 1:
            return 2
        if self.n == 2:
            return 3
        
        prev2 = 2
        prev1 = 3
        
        for i in range(3, self.n + 1):
            current = (prev1 + prev2) % self.MOD
            prev2 = prev1
            prev1 = current
        
        return prev1
    
    def _generate_valid_strings(self):
        """Generate all valid bit strings considering constraints."""
        if self.n == 0:
            return []
        if self.n == 1:
            return ['0', '1']
        if self.n == 2:
            return ['00', '01', '10']
        
        result = []
        
        def generate_strings(current, length):
            if length == self.n:
                if self._is_valid_string(current):
                    result.append(current)
                return
            
            # Add '0' (always valid)
            generate_strings(current + '0', length + 1)
            
            # Add '1' only if previous character is not '1'
            if length == 0 or current[-1] != '1':
                generate_strings(current + '1', length + 1)
        
        generate_strings('', 0)
        return result
    
    def _is_valid_string(self, bit_string):
        """Check if a bit string is valid considering constraints."""
        # Basic constraint: no consecutive 1s
        if '11' in bit_string:
            return False
        
        # Length constraints
        if 'min_length' in self.constraints:
            if len(bit_string) < self.constraints['min_length']:
                return False
        
        if 'max_length' in self.constraints:
            if len(bit_string) > self.constraints['max_length']:
                return False
        
        # Pattern constraints
        if 'forbidden_patterns' in self.constraints:
            for pattern in self.constraints['forbidden_patterns']:
                if pattern in bit_string:
                    return False
        
        if 'required_patterns' in self.constraints:
            for pattern in self.constraints['required_patterns']:
                if pattern not in bit_string:
                    return False
        
        # Weight constraints
        if 'max_weight' in self.constraints:
            weight = sum(self.constraints.get('weights', [1] * len(bit_string))[i] for i in range(len(bit_string)) if bit_string[i] == '1')
            if weight > self.constraints['max_weight']:
                return False
        
        if 'min_weight' in self.constraints:
            weight = sum(self.constraints.get('weights', [1] * len(bit_string))[i] for i in range(len(bit_string)) if bit_string[i] == '1')
            if weight < self.constraints['min_weight']:
                return False
        
        return True
    
    def get_strings_with_length_constraints(self, min_length, max_length):
        """Get bit strings considering length constraints."""
        result = []
        for bit_string in self.valid_strings:
            if min_length <= len(bit_string) <= max_length:
                result.append(bit_string)
        return result
    
    def get_strings_with_pattern_constraints(self, pattern_constraints):
        """Get bit strings considering pattern constraints."""
        result = []
        for bit_string in self.valid_strings:
            satisfies_constraints = True
            for constraint in pattern_constraints:
                if not constraint(bit_string):
                    satisfies_constraints = False
                    break
            if satisfies_constraints:
                result.append(bit_string)
        return result
    
    def get_strings_with_weight_constraints(self, weight_limits):
        """Get bit strings considering weight constraints."""
        result = []
        weights = self.constraints.get('weights', [1] * self.n)
        
        for bit_string in self.valid_strings:
            weight = sum(weights[i] for i in range(len(bit_string)) if bit_string[i] == '1')
            if weight_limits[0] <= weight <= weight_limits[1]:
                result.append(bit_string)
        return result
    
    def get_strings_with_mathematical_constraints(self, constraint_func):
        """Get bit strings that satisfy custom mathematical constraints."""
        result = []
        for bit_string in self.valid_strings:
            if constraint_func(bit_string):
                result.append(bit_string)
        return result
    
    def get_strings_with_range_constraints(self, range_constraints):
        """Get bit strings that satisfy range constraints."""
        result = []
        for bit_string in self.valid_strings:
            satisfies_constraints = True
            for constraint in range_constraints:
                if not constraint(bit_string):
                    satisfies_constraints = False
                    break
            if satisfies_constraints:
                result.append(bit_string)
        return result
    
    def get_strings_with_optimization_constraints(self, optimization_func):
        """Get bit strings using custom optimization constraints."""
        # Sort strings by optimization function
        all_strings = []
        for bit_string in self.valid_strings:
            score = optimization_func(bit_string)
            all_strings.append((bit_string, score))
        
        # Sort by optimization score
        all_strings.sort(key=lambda x: x[1], reverse=True)
        
        return [bit_string for bit_string, _ in all_strings]
    
    def get_strings_with_multiple_constraints(self, constraints_list):
        """Get bit strings that satisfy multiple constraints."""
        result = []
        for bit_string in self.valid_strings:
            satisfies_all_constraints = True
            for constraint in constraints_list:
                if not constraint(bit_string):
                    satisfies_all_constraints = False
                    break
            if satisfies_all_constraints:
                result.append(bit_string)
        return result
    
    def get_strings_with_priority_constraints(self, priority_func):
        """Get bit strings with priority-based constraints."""
        # Sort strings by priority
        all_strings = []
        for bit_string in self.valid_strings:
            priority = priority_func(bit_string)
            all_strings.append((bit_string, priority))
        
        # Sort by priority
        all_strings.sort(key=lambda x: x[1], reverse=True)
        
        return [bit_string for bit_string, _ in all_strings]
    
    def get_strings_with_adaptive_constraints(self, adaptive_func):
        """Get bit strings with adaptive constraints."""
        result = []
        for bit_string in self.valid_strings:
            if adaptive_func(bit_string, result):
                result.append(bit_string)
        return result
    
    def get_optimal_string_strategy(self):
        """Get optimal bit string strategy considering all constraints."""
        strategies = [
            ('length_constraints', self.get_strings_with_length_constraints),
            ('pattern_constraints', self.get_strings_with_pattern_constraints),
            ('weight_constraints', self.get_strings_with_weight_constraints),
        ]
        
        best_strategy = None
        best_count = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'length_constraints':
                    current_count = len(strategy_func(1, self.n))
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda s: '00' not in s]
                    current_count = len(strategy_func(pattern_constraints))
                elif strategy_name == 'weight_constraints':
                    current_count = len(strategy_func((0, 10)))
                
                if current_count > best_count:
                    best_count = current_count
                    best_strategy = (strategy_name, current_count)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'min_length': 2,
    'max_length': 5,
    'forbidden_patterns': ['111'],
    'required_patterns': ['01'],
    'max_weight': 10,
    'min_weight': 1,
    'weights': [2, 1, 3, 1, 2]
}

n = 5
constrained_bit_strings = ConstrainedBitStrings(n, constraints)

print("Length-constrained strings:", len(constrained_bit_strings.get_strings_with_length_constraints(2, 4)))

# Pattern constraints
pattern_constraints = [lambda s: '00' not in s, lambda s: s.count('1') <= 2]
print("Pattern-constrained strings:", len(constrained_bit_strings.get_strings_with_pattern_constraints(pattern_constraints)))

print("Weight-constrained strings:", len(constrained_bit_strings.get_strings_with_weight_constraints((1, 8))))

# Mathematical constraints
def custom_constraint(bit_string):
    return bit_string.count('1') == 2 and bit_string.startswith('0')

print("Mathematical constraint strings:", len(constrained_bit_strings.get_strings_with_mathematical_constraints(custom_constraint)))

# Range constraints
def range_constraint(bit_string):
    return 1 <= bit_string.count('1') <= 3

range_constraints = [range_constraint]
print("Range-constrained strings:", len(constrained_bit_strings.get_strings_with_range_constraints(range_constraints)))

# Multiple constraints
def constraint1(bit_string):
    return bit_string.count('1') <= 2

def constraint2(bit_string):
    return bit_string.startswith('0')

constraints_list = [constraint1, constraint2]
print("Multiple constraints strings:", len(constrained_bit_strings.get_strings_with_multiple_constraints(constraints_list)))

# Priority constraints
def priority_func(bit_string):
    return bit_string.count('1') + len(bit_string)

print("Priority-constrained strings:", len(constrained_bit_strings.get_strings_with_priority_constraints(priority_func)))

# Adaptive constraints
def adaptive_func(bit_string, current_result):
    return bit_string.count('1') <= 2 and len(current_result) < 5

print("Adaptive constraint strings:", len(constrained_bit_strings.get_strings_with_adaptive_constraints(adaptive_func)))

# Optimal strategy
optimal = constrained_bit_strings.get_optimal_string_strategy()
print(f"Optimal strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Creating Strings](https://cses.fi/problemset/task/1075)s
- [Permutations](https://cses.fi/problemset/task/1075)s
- [Two Knights](https://cses.fi/problemset/task/1075)s

#### **LeetCode Problems**
- [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) - Dynamic Programming
- [Fibonacci Number](https://leetcode.com/problems/fibonacci-number/) - Dynamic Programming
- [House Robber](https://leetcode.com/problems/house-robber/) - Dynamic Programming

#### **Problem Categories**
- **Introductory Problems**: Counting, combinatorics
- **Dynamic Programming**: Recurrence relations, counting
- **Combinatorics**: Bit strings, counting problems

## 🔗 Additional Resources

### **Algorithm References**
- [Introductory Problems](https://cp-algorithms.com/intro-to-algorithms.html) - Introductory algorithms
- [Dynamic Programming](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP algorithms
- [Combinatorics](https://cp-algorithms.com/combinatorics/basic-combinatorics.html) - Combinatorics

### **Practice Problems**
- [CSES Creating Strings](https://cses.fi/problemset/task/1075) - Easy
- [CSES Permutations](https://cses.fi/problemset/task/1075) - Easy
- [CSES Two Knights](https://cses.fi/problemset/task/1075) - Easy

### **Further Reading**
- [Combinatorics](https://en.wikipedia.org/wiki/Combinatorics) - Wikipedia article
- [Dynamic Programming](https://en.wikipedia.org/wiki/Dynamic_programming) - Wikipedia article
- [Bit String](https://en.wikipedia.org/wiki/Bit_string) - Wikipedia article
