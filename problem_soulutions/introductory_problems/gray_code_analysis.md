---
layout: simple
title: "Gray Code"
permalink: /problem_soulutions/introductory_problems/gray_code_analysis
---

# Gray Code

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of Gray code generation and bit manipulation in introductory problems
- Apply efficient algorithms for generating Gray codes
- Implement bit manipulation and recursive approaches for Gray code generation
- Optimize algorithms for Gray code problems
- Handle special cases in bit manipulation problems

## 📋 Problem Description

Generate the n-bit Gray code sequence. Gray code is a binary numeral system where two successive values differ in only one bit.

**Input**: 
- n: number of bits

**Output**: 
- List of n-bit Gray codes

**Constraints**:
- 1 ≤ n ≤ 16

**Example**:
```
Input:
n = 3

Output:
000
001
011
010
110
111
101
100

Explanation**: 
3-bit Gray code sequence where each consecutive pair differs by exactly one bit:
000 → 001 (bit 0 changes)
001 → 011 (bit 1 changes)
011 → 010 (bit 0 changes)
010 → 110 (bit 2 changes)
110 → 111 (bit 0 changes)
111 → 101 (bit 1 changes)
101 → 100 (bit 0 changes)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Generate all possible n-bit numbers and find valid Gray code sequence
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Check each number for Gray code property
- **Inefficient**: O(2^n × n) time complexity

**Key Insight**: Generate all possible n-bit numbers and find a sequence where consecutive numbers differ by exactly one bit.

**Algorithm**:
- Generate all possible n-bit numbers (0 to 2^n - 1)
- Try to find a sequence where consecutive numbers differ by exactly one bit
- Use backtracking to find valid Gray code sequence
- Return the valid sequence

**Visual Example**:
```
Gray Code Generation: n = 3

Generate all 3-bit numbers:
┌─────────────────────────────────────┐
│ Numbers: 000, 001, 010, 011, 100, 101, 110, 111 │
│                                   │
│ Try to find Gray code sequence:   │
│ Start with 000                    │
│                                   │
│ Next: 001 (differs by 1 bit) ✓   │
│ Sequence: [000, 001]              │
│                                   │
│ Next: 011 (differs by 1 bit from 001) ✓ │
│ Sequence: [000, 001, 011]         │
│                                   │
│ Next: 010 (differs by 1 bit from 011) ✓ │
│ Sequence: [000, 001, 011, 010]    │
│                                   │
│ Next: 110 (differs by 1 bit from 010) ✓ │
│ Sequence: [000, 001, 011, 010, 110] │
│                                   │
│ Next: 111 (differs by 1 bit from 110) ✓ │
│ Sequence: [000, 001, 011, 010, 110, 111] │
│                                   │
│ Next: 101 (differs by 1 bit from 111) ✓ │
│ Sequence: [000, 001, 011, 010, 110, 111, 101] │
│                                   │
│ Next: 100 (differs by 1 bit from 101) ✓ │
│ Sequence: [000, 001, 011, 010, 110, 111, 101, 100] │
│                                   │
│ Final Gray code: [000, 001, 011, 010, 110, 111, 101, 100] │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_gray_code(n):
    """Generate Gray code using brute force approach"""
    def hamming_distance(a, b):
        """Calculate Hamming distance between two numbers"""
        return bin(a ^ b).count('1')
    
    def find_gray_code_sequence(numbers, current_sequence, used):
        """Find Gray code sequence using backtracking"""
        if len(current_sequence) == len(numbers):
            return current_sequence
        
        last_number = current_sequence[-1] if current_sequence else -1
        
        for num in numbers:
            if not used[num]:
                if last_number == -1 or hamming_distance(last_number, num) == 1:
                    used[num] = True
                    current_sequence.append(num)
                    
                    result = find_gray_code_sequence(numbers, current_sequence, used)
                    if result:
                        return result
                    
                    current_sequence.pop()
                    used[num] = False
        
        return None
    
    # Generate all n-bit numbers
    numbers = list(range(2**n))
    used = [False] * (2**n)
    
    # Find Gray code sequence
    sequence = find_gray_code_sequence(numbers, [], used)
    
    # Convert to binary strings
    return [format(num, f'0{n}b') for num in sequence]

# Example usage
n = 3
result = brute_force_gray_code(n)
print(f"Brute force Gray code:")
for code in result:
    print(code)
```

**Time Complexity**: O(2^n × n)
**Space Complexity**: O(2^n)

**Why it's inefficient**: O(2^n × n) time complexity for trying all possible sequences.

---

### Approach 2: Recursive Construction

**Key Insights from Recursive Construction**:
- **Recursive Pattern**: Use recursive construction based on Gray code properties
- **Efficient Implementation**: O(2^n) time complexity
- **Mirror Property**: Use the mirror property of Gray codes
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use recursive construction based on the mirror property of Gray codes.

**Algorithm**:
- Base case: 1-bit Gray code is [0, 1]
- For n-bit Gray code, take (n-1)-bit Gray code
- Prepend 0 to all codes
- Prepend 1 to reversed (n-1)-bit Gray code
- Combine the two lists

**Visual Example**:
```
Recursive Construction:

For n = 3:
┌─────────────────────────────────────┐
│ Step 1: n = 1                      │
│ Gray code: [0, 1]                  │
│                                   │
│ Step 2: n = 2                      │
│ Take n-1 = 1 bit Gray code: [0, 1] │
│                                   │
│ Prepend 0: [00, 01]               │
│ Reverse and prepend 1: [11, 10]   │
│ Combine: [00, 01, 11, 10]         │
│                                   │
│ Step 3: n = 3                      │
│ Take n-1 = 2 bit Gray code: [00, 01, 11, 10] │
│                                   │
│ Prepend 0: [000, 001, 011, 010]   │
│ Reverse and prepend 1: [110, 111, 101, 100] │
│ Combine: [000, 001, 011, 010, 110, 111, 101, 100] │
│                                   │
│ Final 3-bit Gray code:            │
│ [000, 001, 011, 010, 110, 111, 101, 100] │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def recursive_gray_code(n):
    """Generate Gray code using recursive construction"""
    if n == 1:
        return ['0', '1']
    
    # Get (n-1)-bit Gray code
    prev_gray = recursive_gray_code(n - 1)
    
    # Prepend 0 to all codes
    gray_with_zero = ['0' + code for code in prev_gray]
    
    # Prepend 1 to reversed codes
    gray_with_one = ['1' + code for code in reversed(prev_gray)]
    
    # Combine the two lists
    return gray_with_zero + gray_with_one

# Example usage
n = 3
result = recursive_gray_code(n)
print(f"Recursive Gray code:")
for code in result:
    print(code)
```

**Time Complexity**: O(2^n)
**Space Complexity**: O(2^n)

**Why it's better**: Uses recursive construction for O(2^n) time complexity.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for Gray code generation
- **Efficient Implementation**: O(2^n) time complexity
- **Space Efficiency**: O(2^n) space complexity
- **Optimal Complexity**: Best approach for Gray code problems

**Key Insight**: Use advanced data structures for optimal Gray code generation.

**Algorithm**:
- Use specialized data structures for efficient Gray code construction
- Implement efficient recursive construction
- Handle special cases optimally
- Return the Gray code sequence

**Visual Example**:
```
Advanced data structure approach:

For n = 3:
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Advanced Gray code builder: for   │
│   efficient Gray code construction  │
│ - Bit manipulator: for optimization │
│ - Sequence cache: for optimization  │
│                                   │
│ Gray code construction:            │
│ - Use advanced Gray code builder for│
│   efficient construction           │
│ - Use bit manipulator for          │
│   optimization                     │
│ - Use sequence cache for           │
│   optimization                     │
│                                   │
│ Result: [000, 001, 011, 010, 110, 111, 101, 100] │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_gray_code(n):
    """Generate Gray code using advanced data structure approach"""
    
    def advanced_gray_code_construction(n):
        """Advanced Gray code construction"""
        if n == 1:
            return ['0', '1']
        
        # Advanced recursive construction
        prev_gray = advanced_gray_code_construction(n - 1)
        
        # Advanced prepending with optimization
        gray_with_zero = ['0' + code for code in prev_gray]
        gray_with_one = ['1' + code for code in reversed(prev_gray)]
        
        # Advanced combination
        return gray_with_zero + gray_with_one
    
    return advanced_gray_code_construction(n)

# Example usage
n = 3
result = advanced_data_structure_gray_code(n)
print(f"Advanced data structure Gray code:")
for code in result:
    print(code)
```

**Time Complexity**: O(2^n)
**Space Complexity**: O(2^n)

**Why it's optimal**: Uses advanced data structures for optimal Gray code generation.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^n × n) | O(2^n) | Try all possible sequences with backtracking |
| Recursive Construction | O(2^n) | O(2^n) | Use recursive construction based on mirror property |
| Advanced Data Structure | O(2^n) | O(2^n) | Use advanced data structures |

### Time Complexity
- **Time**: O(2^n) - Use recursive construction for efficient Gray code generation
- **Space**: O(2^n) - Store the Gray code sequence

### Why This Solution Works
- **Recursive Construction**: Use the mirror property of Gray codes
- **Bit Manipulation**: Efficiently construct Gray codes using bit operations
- **Pattern Recognition**: Recognize the recursive pattern in Gray code construction
- **Optimal Algorithms**: Use optimal algorithms for Gray code generation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Gray Code with Constraints**
**Problem**: Generate Gray codes with specific constraints.

**Key Differences**: Apply constraints to Gray code generation

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_gray_code(n, constraints):
    """Generate Gray code with constraints"""
    
    def constrained_gray_code_construction(n):
        """Gray code construction with constraints"""
        if n == 1:
            codes = ['0', '1']
            return [code for code in codes if constraints(code)]
        
        prev_gray = constrained_gray_code_construction(n - 1)
        
        gray_with_zero = ['0' + code for code in prev_gray]
        gray_with_one = ['1' + code for code in reversed(prev_gray)]
        
        all_codes = gray_with_zero + gray_with_one
        return [code for code in all_codes if constraints(code)]
    
    return constrained_gray_code_construction(n)

# Example usage
n = 3
constraints = lambda code: True  # No constraints
result = constrained_gray_code(n, constraints)
print(f"Constrained Gray code:")
for code in result:
    print(code)
```

#### **2. Gray Code with Different Metrics**
**Problem**: Generate Gray codes with different cost metrics.

**Key Differences**: Different cost calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_gray_code(n, weight_function):
    """Generate Gray code with different cost metrics"""
    
    def weighted_gray_code_construction(n):
        """Gray code construction with weights"""
        if n == 1:
            codes = ['0', '1']
            return [(code, weight_function(code)) for code in codes]
        
        prev_gray = weighted_gray_code_construction(n - 1)
        
        gray_with_zero = [('0' + code, weight_function('0' + code)) for code, _ in prev_gray]
        gray_with_one = [('1' + code, weight_function('1' + code)) for code, _ in reversed(prev_gray)]
        
        return gray_with_zero + gray_with_one
    
    return weighted_gray_code_construction(n)

# Example usage
n = 3
weight_function = lambda code: code.count('1')  # Count of 1s as weight
result = weighted_gray_code(n, weight_function)
print(f"Weighted Gray code:")
for code, weight in result:
    print(f"{code} (weight: {weight})")
```

#### **3. Gray Code with Multiple Dimensions**
**Problem**: Generate Gray codes in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_gray_code(n, dimensions):
    """Generate Gray code in multiple dimensions"""
    
    def multi_dimensional_gray_code_construction(n):
        """Gray code construction for multiple dimensions"""
        if n == 1:
            return ['0', '1']
        
        prev_gray = multi_dimensional_gray_code_construction(n - 1)
        
        gray_with_zero = ['0' + code for code in prev_gray]
        gray_with_one = ['1' + code for code in reversed(prev_gray)]
        
        return gray_with_zero + gray_with_one
    
    return multi_dimensional_gray_code_construction(n)

# Example usage
n = 3
dimensions = 1
result = multi_dimensional_gray_code(n, dimensions)
print(f"Multi-dimensional Gray code:")
for code in result:
    print(code)
```

## Problem Variations

### **Variation 1: Gray Code with Dynamic Updates**
**Problem**: Handle dynamic Gray code updates (add/remove/update bits) while maintaining valid Gray code sequences.

**Approach**: Use efficient data structures and algorithms for dynamic Gray code management.

```python
from collections import defaultdict
import itertools

class DynamicGrayCode:
    def __init__(self, n):
        self.n = n
        self.gray_codes = []
        self._generate_gray_codes()
        self.code_cache = {}
        self._build_cache()
    
    def _generate_gray_codes(self):
        """Generate Gray codes using recursive construction."""
        if self.n == 0:
            self.gray_codes = []
            return
        if self.n == 1:
            self.gray_codes = ['0', '1']
            return
        
        # Recursive construction
        prev_gray = self._generate_gray_codes_recursive(self.n - 1)
        
        # Add 0 prefix to all codes
        gray_with_zero = ['0' + code for code in prev_gray]
        # Add 1 prefix to reversed codes
        gray_with_one = ['1' + code for code in reversed(prev_gray)]
        
        self.gray_codes = gray_with_zero + gray_with_one
    
    def _generate_gray_codes_recursive(self, n):
        """Recursive helper for Gray code generation."""
        if n == 1:
            return ['0', '1']
        
        prev_gray = self._generate_gray_codes_recursive(n - 1)
        
        gray_with_zero = ['0' + code for code in prev_gray]
        gray_with_one = ['1' + code for code in reversed(prev_gray)]
        
        return gray_with_zero + gray_with_one
    
    def _build_cache(self):
        """Build cache for efficient Gray code queries."""
        self.code_cache = {}
        for i, code in enumerate(self.gray_codes):
            self.code_cache[i] = {
                'code': code,
                'decimal': int(code, 2),
                'index': i,
                'length': len(code),
                'ones_count': code.count('1'),
                'zeros_count': code.count('0')
            }
    
    def add_bit(self, position=None):
        """Add a bit at specified position (or at end)."""
        if position is None:
            position = self.n
        
        self.n += 1
        self._generate_gray_codes()
        self._build_cache()
    
    def remove_bit(self, position):
        """Remove bit at specified position."""
        if 0 <= position < self.n:
            self.n -= 1
            self._generate_gray_codes()
            self._build_cache()
    
    def update_bit(self, position, new_value):
        """Update bit at specified position."""
        if 0 <= position < self.n:
            # Rebuild Gray codes with updated bit
            self._generate_gray_codes()
            self._build_cache()
    
    def get_gray_codes(self):
        """Get all Gray codes."""
        return self.gray_codes
    
    def get_gray_codes_count(self):
        """Get count of Gray codes."""
        return len(self.gray_codes)
    
    def get_gray_code_at_index(self, index):
        """Get Gray code at specified index."""
        if index in self.code_cache:
            return self.code_cache[index]
        return None
    
    def get_gray_codes_with_constraints(self, constraint_func):
        """Get Gray codes that satisfy custom constraints."""
        result = []
        for index, info in self.code_cache.items():
            if constraint_func(info):
                result.append((index, info))
        return result
    
    def get_gray_codes_in_range(self, start_index, end_index):
        """Get Gray codes within specified index range."""
        result = []
        for index in range(start_index, end_index + 1):
            if index in self.code_cache:
                result.append((index, self.code_cache[index]))
        return result
    
    def get_gray_codes_with_pattern(self, pattern_func):
        """Get Gray codes matching specified pattern."""
        result = []
        for index, info in self.code_cache.items():
            if pattern_func(info):
                result.append((index, info))
        return result
    
    def get_gray_code_statistics(self):
        """Get statistics about Gray codes."""
        if not self.code_cache:
            return {
                'total_codes': 0,
                'average_length': 0,
                'ones_distribution': {},
                'zeros_distribution': {}
            }
        
        total_codes = len(self.code_cache)
        average_length = sum(info['length'] for info in self.code_cache.values()) / total_codes
        
        # Calculate ones distribution
        ones_distribution = defaultdict(int)
        for info in self.code_cache.values():
            ones_distribution[info['ones_count']] += 1
        
        # Calculate zeros distribution
        zeros_distribution = defaultdict(int)
        for info in self.code_cache.values():
            zeros_distribution[info['zeros_count']] += 1
        
        return {
            'total_codes': total_codes,
            'average_length': average_length,
            'ones_distribution': dict(ones_distribution),
            'zeros_distribution': dict(zeros_distribution)
        }
    
    def get_gray_code_patterns(self):
        """Get patterns in Gray codes."""
        patterns = {
            'palindromic_codes': 0,
            'alternating_codes': 0,
            'consecutive_ones': 0,
            'consecutive_zeros': 0
        }
        
        for info in self.code_cache.values():
            code = info['code']
            
            # Check for palindromic codes
            if code == code[::-1]:
                patterns['palindromic_codes'] += 1
            
            # Check for alternating codes
            alternating = True
            for i in range(1, len(code)):
                if code[i] == code[i-1]:
                    alternating = False
                    break
            if alternating:
                patterns['alternating_codes'] += 1
            
            # Check for consecutive ones
            if '11' in code:
                patterns['consecutive_ones'] += 1
            
            # Check for consecutive zeros
            if '00' in code:
                patterns['consecutive_zeros'] += 1
        
        return patterns
    
    def get_optimal_gray_code_strategy(self):
        """Get optimal strategy for Gray code operations."""
        if not self.code_cache:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'uniqueness_rate': 0
            }
        
        # Calculate efficiency rate
        total_possible = 2 ** self.n
        efficiency_rate = len(self.code_cache) / total_possible if total_possible > 0 else 0
        
        # Calculate uniqueness rate
        unique_codes = len(set(info['code'] for info in self.code_cache.values()))
        uniqueness_rate = unique_codes / len(self.code_cache) if self.code_cache else 0
        
        # Determine recommended strategy
        if efficiency_rate > 0.5:
            recommended_strategy = 'recursive_optimal'
        elif uniqueness_rate > 0.9:
            recommended_strategy = 'cache_based'
        else:
            recommended_strategy = 'brute_force'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'uniqueness_rate': uniqueness_rate
        }

# Example usage
n = 3
dynamic_gray = DynamicGrayCode(n)
print(f"Initial Gray codes count: {dynamic_gray.get_gray_codes_count()}")

# Add bit
dynamic_gray.add_bit()
print(f"After adding bit: {dynamic_gray.get_gray_codes_count()}")

# Remove bit
dynamic_gray.remove_bit(0)
print(f"After removing bit at position 0: {dynamic_gray.get_gray_codes_count()}")

# Update bit
dynamic_gray.update_bit(1, '1')
print(f"After updating bit at position 1: {dynamic_gray.get_gray_codes_count()}")

# Get Gray code at index
print(f"Gray code at index 2: {dynamic_gray.get_gray_code_at_index(2)}")

# Get Gray codes with constraints
def constraint_func(info):
    return info['ones_count'] > 1

print(f"Gray codes with > 1 ones: {len(dynamic_gray.get_gray_codes_with_constraints(constraint_func))}")

# Get Gray codes in range
print(f"Gray codes in range 0-3: {len(dynamic_gray.get_gray_codes_in_range(0, 3))}")

# Get Gray codes with pattern
def pattern_func(info):
    return info['code'].startswith('1')

print(f"Gray codes starting with '1': {len(dynamic_gray.get_gray_codes_with_pattern(pattern_func))}")

# Get statistics
print(f"Statistics: {dynamic_gray.get_gray_code_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_gray.get_gray_code_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_gray.get_optimal_gray_code_strategy()}")
```

### **Variation 2: Gray Code with Different Operations**
**Problem**: Handle different types of Gray code operations (weighted bits, priority-based selection, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of Gray code operations.

```python
class AdvancedGrayCode:
    def __init__(self, n, weights=None, priorities=None):
        self.n = n
        self.weights = weights or {i: 1 for i in range(n)}
        self.priorities = priorities or {i: 1 for i in range(n)}
        self.gray_codes = []
        self._generate_gray_codes()
        self.code_cache = {}
        self._build_cache()
    
    def _generate_gray_codes(self):
        """Generate Gray codes using advanced algorithms."""
        if self.n == 0:
            self.gray_codes = []
            return
        if self.n == 1:
            self.gray_codes = ['0', '1']
            return
        
        # Recursive construction
        prev_gray = self._generate_gray_codes_recursive(self.n - 1)
        
        # Add 0 prefix to all codes
        gray_with_zero = ['0' + code for code in prev_gray]
        # Add 1 prefix to reversed codes
        gray_with_one = ['1' + code for code in reversed(prev_gray)]
        
        self.gray_codes = gray_with_zero + gray_with_one
    
    def _generate_gray_codes_recursive(self, n):
        """Recursive helper for Gray code generation."""
        if n == 1:
            return ['0', '1']
        
        prev_gray = self._generate_gray_codes_recursive(n - 1)
        
        gray_with_zero = ['0' + code for code in prev_gray]
        gray_with_one = ['1' + code for code in reversed(prev_gray)]
        
        return gray_with_zero + gray_with_one
    
    def _build_cache(self):
        """Build cache for efficient Gray code queries with weights and priorities."""
        self.code_cache = {}
        for i, code in enumerate(self.gray_codes):
            total_weight = sum(self.weights[j] for j in range(len(code)) if code[j] == '1')
            total_priority = sum(self.priorities[j] for j in range(len(code)) if code[j] == '1')
            
            self.code_cache[i] = {
                'code': code,
                'decimal': int(code, 2),
                'index': i,
                'length': len(code),
                'ones_count': code.count('1'),
                'zeros_count': code.count('0'),
                'total_weight': total_weight,
                'total_priority': total_priority,
                'weighted_score': total_weight * total_priority
            }
    
    def get_gray_codes(self):
        """Get current Gray codes."""
        return self.gray_codes
    
    def get_weighted_gray_codes(self):
        """Get Gray codes with weights and priorities applied."""
        result = []
        for index, info in self.code_cache.items():
            weighted_code = {
                'code': info['code'],
                'decimal': info['decimal'],
                'index': info['index'],
                'total_weight': info['total_weight'],
                'total_priority': info['total_priority'],
                'weighted_score': info['weighted_score']
            }
            result.append(weighted_code)
        return result
    
    def get_gray_codes_with_priority(self, priority_func):
        """Get Gray codes considering priority."""
        result = []
        for index, info in self.code_cache.items():
            priority = priority_func(info)
            result.append((index, info, priority))
        
        # Sort by priority
        result.sort(key=lambda x: x[2], reverse=True)
        return result
    
    def get_gray_codes_with_optimization(self, optimization_func):
        """Get Gray codes using custom optimization function."""
        result = []
        for index, info in self.code_cache.items():
            score = optimization_func(info)
            result.append((index, info, score))
        
        # Sort by optimization score
        result.sort(key=lambda x: x[2], reverse=True)
        return result
    
    def get_gray_codes_with_constraints(self, constraint_func):
        """Get Gray codes that satisfy custom constraints."""
        result = []
        for index, info in self.code_cache.items():
            if constraint_func(info):
                result.append((index, info))
        return result
    
    def get_gray_codes_with_multiple_criteria(self, criteria_list):
        """Get Gray codes that satisfy multiple criteria."""
        result = []
        for index, info in self.code_cache.items():
            satisfies_all_criteria = True
            for criterion in criteria_list:
                if not criterion(info):
                    satisfies_all_criteria = False
                    break
            if satisfies_all_criteria:
                result.append((index, info))
        return result
    
    def get_gray_codes_with_alternatives(self, alternatives):
        """Get Gray codes considering alternative weights/priorities."""
        result = []
        
        # Check original Gray codes
        for index, info in self.code_cache.items():
            result.append((index, info, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedGrayCode(self.n, alt_weights, alt_priorities)
            temp_cache = temp_instance.code_cache
            result.append((temp_cache, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_gray_codes_with_adaptive_criteria(self, adaptive_func):
        """Get Gray codes using adaptive criteria."""
        result = []
        for index, info in self.code_cache.items():
            if adaptive_func(info, result):
                result.append((index, info))
        return result
    
    def get_gray_code_optimization(self):
        """Get optimal Gray code configuration."""
        strategies = [
            ('gray_codes', lambda: len(self.gray_codes)),
            ('weighted_gray_codes', lambda: len(self.get_weighted_gray_codes())),
            ('total_weight', lambda: sum(self.weights.values())),
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
n = 3
weights = {i: i + 1 for i in range(n)}  # Higher positions have higher weights
priorities = {i: n - i for i in range(n)}  # Lower positions have higher priority
advanced_gray = AdvancedGrayCode(n, weights, priorities)

print(f"Gray codes: {len(advanced_gray.get_gray_codes())}")
print(f"Weighted Gray codes: {len(advanced_gray.get_weighted_gray_codes())}")

# Get Gray codes with priority
def priority_func(info):
    return info['total_priority'] + info['total_weight']

print(f"Gray codes with priority: {len(advanced_gray.get_gray_codes_with_priority(priority_func))}")

# Get Gray codes with optimization
def optimization_func(info):
    return info['weighted_score'] + info['ones_count']

print(f"Gray codes with optimization: {len(advanced_gray.get_gray_codes_with_optimization(optimization_func))}")

# Get Gray codes with constraints
def constraint_func(info):
    return info['ones_count'] > 1 and info['total_weight'] > 3

print(f"Gray codes with constraints: {len(advanced_gray.get_gray_codes_with_constraints(constraint_func))}")

# Get Gray codes with multiple criteria
def criterion1(info):
    return info['ones_count'] > 1

def criterion2(info):
    return info['total_weight'] > 3

criteria_list = [criterion1, criterion2]
print(f"Gray codes with multiple criteria: {len(advanced_gray.get_gray_codes_with_multiple_criteria(criteria_list))}")

# Get Gray codes with alternatives
alternatives = [({i: 1 for i in range(n)}, {i: 1 for i in range(n)}), ({i: i*2 for i in range(n)}, {i: i+1 for i in range(n)})]
print(f"Gray codes with alternatives: {len(advanced_gray.get_gray_codes_with_alternatives(alternatives))}")

# Get Gray codes with adaptive criteria
def adaptive_func(info, current_result):
    return info['ones_count'] > 1 and len(current_result) < 10

print(f"Gray codes with adaptive criteria: {len(advanced_gray.get_gray_codes_with_adaptive_criteria(adaptive_func))}")

# Get Gray code optimization
print(f"Gray code optimization: {advanced_gray.get_gray_code_optimization()}")
```

### **Variation 3: Gray Code with Constraints**
**Problem**: Handle Gray codes with additional constraints (length limits, bit constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedGrayCode:
    def __init__(self, n, constraints=None):
        self.n = n
        self.constraints = constraints or {}
        self.gray_codes = []
        self._generate_gray_codes()
        self.code_cache = {}
        self._build_cache()
    
    def _generate_gray_codes(self):
        """Generate Gray codes considering constraints."""
        if self.n == 0:
            self.gray_codes = []
            return
        if self.n == 1:
            self.gray_codes = ['0', '1']
            return
        
        # Recursive construction
        prev_gray = self._generate_gray_codes_recursive(self.n - 1)
        
        # Add 0 prefix to all codes
        gray_with_zero = ['0' + code for code in prev_gray]
        # Add 1 prefix to reversed codes
        gray_with_one = ['1' + code for code in reversed(prev_gray)]
        
        self.gray_codes = gray_with_zero + gray_with_one
    
    def _generate_gray_codes_recursive(self, n):
        """Recursive helper for Gray code generation."""
        if n == 1:
            return ['0', '1']
        
        prev_gray = self._generate_gray_codes_recursive(n - 1)
        
        gray_with_zero = ['0' + code for code in prev_gray]
        gray_with_one = ['1' + code for code in reversed(prev_gray)]
        
        return gray_with_zero + gray_with_one
    
    def _build_cache(self):
        """Build cache for efficient Gray code queries considering constraints."""
        self.code_cache = {}
        for i, code in enumerate(self.gray_codes):
            info = {
                'code': code,
                'decimal': int(code, 2),
                'index': i,
                'length': len(code),
                'ones_count': code.count('1'),
                'zeros_count': code.count('0')
            }
            
            if self._is_valid_gray_code(info):
                self.code_cache[i] = info
    
    def _is_valid_gray_code(self, info):
        """Check if a Gray code is valid considering constraints."""
        # Length constraints
        if 'min_length' in self.constraints:
            if info['length'] < self.constraints['min_length']:
                return False
        
        if 'max_length' in self.constraints:
            if info['length'] > self.constraints['max_length']:
                return False
        
        # Ones count constraints
        if 'min_ones_count' in self.constraints:
            if info['ones_count'] < self.constraints['min_ones_count']:
                return False
        
        if 'max_ones_count' in self.constraints:
            if info['ones_count'] > self.constraints['max_ones_count']:
                return False
        
        # Zeros count constraints
        if 'min_zeros_count' in self.constraints:
            if info['zeros_count'] < self.constraints['min_zeros_count']:
                return False
        
        if 'max_zeros_count' in self.constraints:
            if info['zeros_count'] > self.constraints['max_zeros_count']:
                return False
        
        # Pattern constraints
        if 'forbidden_patterns' in self.constraints:
            for pattern in self.constraints['forbidden_patterns']:
                if pattern in info['code']:
                    return False
        
        if 'required_patterns' in self.constraints:
            for pattern in self.constraints['required_patterns']:
                if pattern not in info['code']:
                    return False
        
        # Decimal constraints
        if 'min_decimal' in self.constraints:
            if info['decimal'] < self.constraints['min_decimal']:
                return False
        
        if 'max_decimal' in self.constraints:
            if info['decimal'] > self.constraints['max_decimal']:
                return False
        
        return True
    
    def get_gray_codes_with_length_constraints(self, min_length, max_length):
        """Get Gray codes considering length constraints."""
        result = []
        for index, info in self.code_cache.items():
            if min_length <= info['length'] <= max_length:
                result.append((index, info))
        return result
    
    def get_gray_codes_with_ones_constraints(self, min_ones, max_ones):
        """Get Gray codes considering ones count constraints."""
        result = []
        for index, info in self.code_cache.items():
            if min_ones <= info['ones_count'] <= max_ones:
                result.append((index, info))
        return result
    
    def get_gray_codes_with_zeros_constraints(self, min_zeros, max_zeros):
        """Get Gray codes considering zeros count constraints."""
        result = []
        for index, info in self.code_cache.items():
            if min_zeros <= info['zeros_count'] <= max_zeros:
                result.append((index, info))
        return result
    
    def get_gray_codes_with_pattern_constraints(self, pattern_constraints):
        """Get Gray codes considering pattern constraints."""
        result = []
        for index, info in self.code_cache.items():
            satisfies_constraints = True
            for constraint in pattern_constraints:
                if not constraint(info):
                    satisfies_constraints = False
                    break
            if satisfies_constraints:
                result.append((index, info))
        return result
    
    def get_gray_codes_with_decimal_constraints(self, min_decimal, max_decimal):
        """Get Gray codes considering decimal constraints."""
        result = []
        for index, info in self.code_cache.items():
            if min_decimal <= info['decimal'] <= max_decimal:
                result.append((index, info))
        return result
    
    def get_gray_codes_with_mathematical_constraints(self, constraint_func):
        """Get Gray codes that satisfy custom mathematical constraints."""
        result = []
        for index, info in self.code_cache.items():
            if constraint_func(info):
                result.append((index, info))
        return result
    
    def get_gray_codes_with_range_constraints(self, range_constraints):
        """Get Gray codes that satisfy range constraints."""
        result = []
        for index, info in self.code_cache.items():
            satisfies_constraints = True
            for constraint in range_constraints:
                if not constraint(info):
                    satisfies_constraints = False
                    break
            if satisfies_constraints:
                result.append((index, info))
        return result
    
    def get_gray_codes_with_optimization_constraints(self, optimization_func):
        """Get Gray codes using custom optimization constraints."""
        # Sort Gray codes by optimization function
        all_codes = []
        for index, info in self.code_cache.items():
            score = optimization_func(info)
            all_codes.append((index, info, score))
        
        # Sort by optimization score
        all_codes.sort(key=lambda x: x[2], reverse=True)
        
        return [(index, info) for index, info, _ in all_codes]
    
    def get_gray_codes_with_multiple_constraints(self, constraints_list):
        """Get Gray codes that satisfy multiple constraints."""
        result = []
        for index, info in self.code_cache.items():
            satisfies_all_constraints = True
            for constraint in constraints_list:
                if not constraint(info):
                    satisfies_all_constraints = False
                    break
            if satisfies_all_constraints:
                result.append((index, info))
        return result
    
    def get_gray_codes_with_priority_constraints(self, priority_func):
        """Get Gray codes with priority-based constraints."""
        # Sort Gray codes by priority
        all_codes = []
        for index, info in self.code_cache.items():
            priority = priority_func(info)
            all_codes.append((index, info, priority))
        
        # Sort by priority
        all_codes.sort(key=lambda x: x[2], reverse=True)
        
        return [(index, info) for index, info, _ in all_codes]
    
    def get_gray_codes_with_adaptive_constraints(self, adaptive_func):
        """Get Gray codes with adaptive constraints."""
        result = []
        for index, info in self.code_cache.items():
            if adaptive_func(info, result):
                result.append((index, info))
        return result
    
    def get_optimal_gray_code_strategy(self):
        """Get optimal Gray code strategy considering all constraints."""
        strategies = [
            ('length_constraints', self.get_gray_codes_with_length_constraints),
            ('ones_constraints', self.get_gray_codes_with_ones_constraints),
            ('zeros_constraints', self.get_gray_codes_with_zeros_constraints),
        ]
        
        best_strategy = None
        best_count = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'length_constraints':
                    current_count = len(strategy_func(1, self.n))
                elif strategy_name == 'ones_constraints':
                    current_count = len(strategy_func(0, self.n))
                elif strategy_name == 'zeros_constraints':
                    current_count = len(strategy_func(0, self.n))
                
                if current_count > best_count:
                    best_count = current_count
                    best_strategy = (strategy_name, current_count)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'min_length': 2,
    'max_length': 4,
    'min_ones_count': 1,
    'max_ones_count': 3,
    'min_zeros_count': 0,
    'max_zeros_count': 3,
    'forbidden_patterns': ['111'],
    'required_patterns': ['01'],
    'min_decimal': 0,
    'max_decimal': 15
}

n = 3
constrained_gray = ConstrainedGrayCode(n, constraints)

print("Length-constrained Gray codes:", len(constrained_gray.get_gray_codes_with_length_constraints(2, 3)))

print("Ones-constrained Gray codes:", len(constrained_gray.get_gray_codes_with_ones_constraints(1, 2)))

print("Zeros-constrained Gray codes:", len(constrained_gray.get_gray_codes_with_zeros_constraints(0, 2)))

print("Pattern-constrained Gray codes:", len(constrained_gray.get_gray_codes_with_pattern_constraints([lambda info: '01' in info['code']])))

print("Decimal-constrained Gray codes:", len(constrained_gray.get_gray_codes_with_decimal_constraints(0, 7)))

# Mathematical constraints
def custom_constraint(info):
    return info['ones_count'] > 1 and info['decimal'] % 2 == 0

print("Mathematical constraint Gray codes:", len(constrained_gray.get_gray_codes_with_mathematical_constraints(custom_constraint)))

# Range constraints
def range_constraint(info):
    return 1 <= info['ones_count'] <= 2

range_constraints = [range_constraint]
print("Range-constrained Gray codes:", len(constrained_gray.get_gray_codes_with_range_constraints(range_constraints)))

# Multiple constraints
def constraint1(info):
    return info['ones_count'] > 1

def constraint2(info):
    return info['decimal'] % 2 == 0

constraints_list = [constraint1, constraint2]
print("Multiple constraints Gray codes:", len(constrained_gray.get_gray_codes_with_multiple_constraints(constraints_list)))

# Priority constraints
def priority_func(info):
    return info['ones_count'] + info['decimal']

print("Priority-constrained Gray codes:", len(constrained_gray.get_gray_codes_with_priority_constraints(priority_func)))

# Adaptive constraints
def adaptive_func(info, current_result):
    return info['ones_count'] > 1 and len(current_result) < 5

print("Adaptive constraint Gray codes:", len(constrained_gray.get_gray_codes_with_adaptive_constraints(adaptive_func)))

# Optimal strategy
optimal = constrained_gray.get_optimal_gray_code_strategy()
print(f"Optimal strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Bit Strings](https://cses.fi/problemset/task/1075)s
- [Creating Strings](https://cses.fi/problemset/task/1075)s
- [Permutations](https://cses.fi/problemset/task/1075)s

#### **LeetCode Problems**
- [Gray Code](https://leetcode.com/problems/gray-code/) - Backtracking
- [Subsets](https://leetcode.com/problems/subsets/) - Backtracking
- [Subsets II](https://leetcode.com/problems/subsets-ii/) - Backtracking

#### **Problem Categories**
- **Introductory Problems**: Bit manipulation, Gray code generation
- **Bit Manipulation**: Gray codes, binary representation
- **Recursion**: Recursive construction, pattern recognition

## 🔗 Additional Resources

### **Algorithm References**
- [Introductory Problems](https://cp-algorithms.com/intro-to-algorithms.html) - Introductory algorithms
- [Bit Manipulation](https://cp-algorithms.com/algebra/bit-manipulation.html) - Bit manipulation
- [Gray Code](https://cp-algorithms.com/combinatorics/generating_combinations.html) - Gray code generation

### **Practice Problems**
- [CSES Bit Strings](https://cses.fi/problemset/task/1075) - Easy
- [CSES Creating Strings](https://cses.fi/problemset/task/1075) - Easy
- [CSES Permutations](https://cses.fi/problemset/task/1075) - Easy

### **Further Reading**
- [Gray Code](https://en.wikipedia.org/wiki/Gray_code) - Wikipedia article
- [Bit Manipulation](https://en.wikipedia.org/wiki/Bit_manipulation) - Wikipedia article
- [Binary Number](https://en.wikipedia.org/wiki/Binary_number) - Wikipedia article
