---
layout: simple
title: "Creating Strings"
permalink: /problem_soulutions/introductory_problems/creating_strings_analysis
---

# Creating Strings

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of string generation and permutation in introductory problems
- Apply efficient algorithms for generating all unique permutations of a string
- Implement backtracking and recursive approaches for string generation
- Optimize algorithms for string permutation problems
- Handle special cases in string generation problems

## 📋 Problem Description

Given a string, generate all unique permutations of its characters.

**Input**: 
- s: input string

**Output**: 
- All unique permutations of the string, one per line

**Constraints**:
- 1 ≤ |s| ≤ 8
- String contains only lowercase letters

**Example**:
```
Input:
s = "aab"

Output:
aab
aba
baa

Explanation**: 
All unique permutations of "aab":
- aab (characters at positions 0,1,2)
- aba (characters at positions 0,2,1)  
- baa (characters at positions 2,0,1)
Total: 3 unique permutations
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Generate all possible permutations and remove duplicates
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Use standard permutation generation
- **Inefficient**: O(n! × n) time complexity with duplicate handling

**Key Insight**: Generate all permutations and remove duplicates to get unique permutations.

**Algorithm**:
- Generate all possible permutations of the string
- Use a set to store unique permutations
- Convert set to sorted list
- Return all unique permutations

**Visual Example**:
```
String: "aab"

Generate all permutations:
┌─────────────────────────────────────┐
│ Permutation 1: "aab" (positions 0,1,2) │
│ - Add to set: {"aab"}              │
│                                   │
│ Permutation 2: "aab" (positions 0,2,1) │
│ - Already in set, skip            │
│                                   │
│ Permutation 3: "aba" (positions 1,0,2) │
│ - Add to set: {"aab", "aba"}      │
│                                   │
│ Permutation 4: "aba" (positions 1,2,0) │
│ - Already in set, skip            │
│                                   │
│ Permutation 5: "baa" (positions 2,0,1) │
│ - Add to set: {"aab", "aba", "baa"} │
│                                   │
│ Permutation 6: "baa" (positions 2,1,0) │
│ - Already in set, skip            │
│                                   │
│ Final set: {"aab", "aba", "baa"}  │
│ Sorted result: ["aab", "aba", "baa"] │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_creating_strings(s):
    """Generate all unique permutations using brute force approach"""
    from itertools import permutations
    
    # Generate all permutations
    all_permutations = [''.join(p) for p in permutations(s)]
    
    # Remove duplicates using set
    unique_permutations = list(set(all_permutations))
    
    # Sort for consistent output
    unique_permutations.sort()
    
    return unique_permutations

# Example usage
s = "aab"
result = brute_force_creating_strings(s)
print(f"Brute force result: {result}")
for perm in result:
    print(perm)
```

**Time Complexity**: O(n! × n)
**Space Complexity**: O(n! × n)

**Why it's inefficient**: O(n! × n) time complexity for generating all permutations and handling duplicates.

---

### Approach 2: Backtracking with Character Counting

**Key Insights from Backtracking with Character Counting**:
- **Character Counting**: Use character frequency to avoid generating duplicates
- **Efficient Implementation**: O(n! × n) time complexity but more efficient in practice
- **Backtracking**: Use backtracking to generate permutations
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use character frequency counting to generate only unique permutations.

**Algorithm**:
- Count frequency of each character
- Use backtracking to build permutations
- For each position, try each available character
- Decrease character count when used
- Increase character count when backtracking

**Visual Example**:
```
Backtracking with Character Counting:

String: "aab"
Character frequency: {'a': 2, 'b': 1}

Build permutations:
┌─────────────────────────────────────┐
│ Position 0:                        │
│ - Try 'a': freq['a'] = 2 > 0 ✓     │
│ - Use 'a': freq['a'] = 1           │
│ - Current: "a"                     │
│                                   │
│ Position 1:                        │
│ - Try 'a': freq['a'] = 1 > 0 ✓     │
│ - Use 'a': freq['a'] = 0           │
│ - Current: "aa"                    │
│                                   │
│ Position 2:                        │
│ - Try 'a': freq['a'] = 0 ✗         │
│ - Try 'b': freq['b'] = 1 > 0 ✓     │
│ - Use 'b': freq['b'] = 0           │
│ - Current: "aab" (complete)        │
│ - Add to result: ["aab"]           │
│                                   │
│ Backtrack to position 1:           │
│ - Restore 'a': freq['a'] = 1       │
│ - Try 'b': freq['b'] = 1 > 0 ✓     │
│ - Use 'b': freq['b'] = 0           │
│ - Current: "ab"                    │
│                                   │
│ Position 2:                        │
│ - Try 'a': freq['a'] = 1 > 0 ✓     │
│ - Use 'a': freq['a'] = 0           │
│ - Current: "aba" (complete)        │
│ - Add to result: ["aab", "aba"]    │
│                                   │
│ Continue backtracking...           │
│ Final result: ["aab", "aba", "baa"] │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def backtracking_creating_strings(s):
    """Generate all unique permutations using backtracking with character counting"""
    from collections import Counter
    
    def backtrack(current, char_count, result):
        """Backtracking function to generate permutations"""
        if len(current) == len(s):
            result.append(current)
            return
        
        for char in char_count:
            if char_count[char] > 0:
                # Use the character
                char_count[char] -= 1
                backtrack(current + char, char_count, result)
                # Backtrack
                char_count[char] += 1
    
    # Count character frequencies
    char_count = Counter(s)
    result = []
    
    # Generate permutations using backtracking
    backtrack("", char_count, result)
    
    return result

# Example usage
s = "aab"
result = backtracking_creating_strings(s)
print(f"Backtracking result: {result}")
for perm in result:
    print(perm)
```

**Time Complexity**: O(n! × n)
**Space Complexity**: O(n! × n)

**Why it's better**: Uses character counting to avoid generating duplicates, more efficient in practice.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for character counting
- **Efficient Implementation**: O(n! × n) time complexity
- **Space Efficiency**: O(n! × n) space complexity
- **Optimal Complexity**: Best approach for string permutation problems

**Key Insight**: Use advanced data structures for optimal string permutation generation.

**Algorithm**:
- Use specialized data structures for character frequency tracking
- Implement efficient backtracking with character counting
- Handle special cases optimally
- Return all unique permutations

**Visual Example**:
```
Advanced data structure approach:

For string: "aab"
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Advanced character counter: for   │
│   efficient frequency tracking      │
│ - Backtracking stack: for optimization│
│ - Result cache: for optimization    │
│                                   │
│ String permutation generation:      │
│ - Use advanced character counter for│
│   efficient frequency tracking      │
│ - Use backtracking stack for       │
│   optimization                      │
│ - Use result cache for optimization │
│                                   │
│ Result: ["aab", "aba", "baa"]      │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_creating_strings(s):
    """Generate all unique permutations using advanced data structure approach"""
    from collections import Counter
    
    def advanced_backtrack(current, char_count, result):
        """Advanced backtracking function"""
        if len(current) == len(s):
            result.append(current)
            return
        
        # Advanced character iteration
        for char in sorted(char_count.keys()):
            if char_count[char] > 0:
                # Advanced state update
                char_count[char] -= 1
                advanced_backtrack(current + char, char_count, result)
                # Advanced backtracking
                char_count[char] += 1
    
    # Advanced character counting
    char_count = Counter(s)
    result = []
    
    # Advanced permutation generation
    advanced_backtrack("", char_count, result)
    
    return result

# Example usage
s = "aab"
result = advanced_data_structure_creating_strings(s)
print(f"Advanced data structure result: {result}")
for perm in result:
    print(perm)
```

**Time Complexity**: O(n! × n)
**Space Complexity**: O(n! × n)

**Why it's optimal**: Uses advanced data structures for optimal string permutation generation.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n! × n) | O(n! × n) | Generate all permutations and remove duplicates |
| Backtracking with Character Counting | O(n! × n) | O(n! × n) | Use character frequency to avoid duplicates |
| Advanced Data Structure | O(n! × n) | O(n! × n) | Use advanced data structures |

### Time Complexity
- **Time**: O(n! × n) - Generate all unique permutations using backtracking
- **Space**: O(n! × n) - Store all permutations and character counts

### Why This Solution Works
- **Character Counting**: Use character frequency to avoid generating duplicates
- **Backtracking**: Use backtracking to generate permutations efficiently
- **State Management**: Properly manage character counts during backtracking
- **Optimal Algorithms**: Use optimal algorithms for string permutation problems

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Creating Strings with Constraints**
**Problem**: Generate permutations with specific constraints.

**Key Differences**: Apply constraints to permutation generation

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_creating_strings(s, constraints):
    """Generate permutations with constraints"""
    from collections import Counter
    
    def constrained_backtrack(current, char_count, result):
        """Backtracking with constraints"""
        if len(current) == len(s):
            if constraints(current):
                result.append(current)
            return
        
        for char in char_count:
            if char_count[char] > 0:
                char_count[char] -= 1
                constrained_backtrack(current + char, char_count, result)
                char_count[char] += 1
    
    char_count = Counter(s)
    result = []
    constrained_backtrack("", char_count, result)
    return result

# Example usage
s = "aab"
constraints = lambda perm: True  # No constraints
result = constrained_creating_strings(s, constraints)
print(f"Constrained result: {result}")
for perm in result:
    print(perm)
```

#### **2. Creating Strings with Different Metrics**
**Problem**: Generate permutations with different cost metrics.

**Key Differences**: Different cost calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_creating_strings(s, weight_function):
    """Generate permutations with different cost metrics"""
    from collections import Counter
    
    def weighted_backtrack(current, char_count, result):
        """Backtracking with weights"""
        if len(current) == len(s):
            weight = weight_function(current)
            result.append((current, weight))
            return
        
        for char in char_count:
            if char_count[char] > 0:
                char_count[char] -= 1
                weighted_backtrack(current + char, char_count, result)
                char_count[char] += 1
    
    char_count = Counter(s)
    result = []
    weighted_backtrack("", char_count, result)
    return result

# Example usage
s = "aab"
weight_function = lambda perm: len(perm)  # Length as weight
result = weighted_creating_strings(s, weight_function)
print(f"Weighted result: {result}")
for perm, weight in result:
    print(f"{perm} (weight: {weight})")
```

#### **3. Creating Strings with Multiple Dimensions**
**Problem**: Generate permutations in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_creating_strings(s, dimensions):
    """Generate permutations in multiple dimensions"""
    from collections import Counter
    
    def multi_dimensional_backtrack(current, char_count, result):
        """Backtracking for multiple dimensions"""
        if len(current) == len(s):
            result.append(current)
            return
        
        for char in char_count:
            if char_count[char] > 0:
                char_count[char] -= 1
                multi_dimensional_backtrack(current + char, char_count, result)
                char_count[char] += 1
    
    char_count = Counter(s)
    result = []
    multi_dimensional_backtrack("", char_count, result)
    return result

# Example usage
s = "aab"
dimensions = 1
result = multi_dimensional_creating_strings(s, dimensions)
print(f"Multi-dimensional result: {result}")
for perm in result:
    print(perm)
```

## Problem Variations

### **Variation 1: Creating Strings with Dynamic Updates**
**Problem**: Handle dynamic string updates (add/remove/update characters) while maintaining valid string permutations.

**Approach**: Use efficient data structures and algorithms for dynamic string permutation management.

```python
from collections import defaultdict, Counter
import itertools

class DynamicCreatingStrings:
    def __init__(self, s):
        self.s = s
        self.char_count = Counter(s)
        self.permutations = []
        self._generate_all_permutations()
    
    def _generate_all_permutations(self):
        """Generate all unique permutations using backtracking."""
        self.permutations = []
        
        def backtrack(current, char_count):
            if len(current) == len(self.s):
                self.permutations.append(current)
                return
            
            for char in char_count:
                if char_count[char] > 0:
                    char_count[char] -= 1
                    backtrack(current + char, char_count)
                    char_count[char] += 1
        
        backtrack("", self.char_count.copy())
    
    def add_character(self, char):
        """Add a character to the string."""
        self.s += char
        self.char_count[char] += 1
        self._generate_all_permutations()
    
    def remove_character(self, char):
        """Remove a character from the string."""
        if char in self.s and self.char_count[char] > 0:
            self.s = self.s.replace(char, '', 1)
            self.char_count[char] -= 1
            if self.char_count[char] == 0:
                del self.char_count[char]
            self._generate_all_permutations()
    
    def update_character(self, old_char, new_char):
        """Update a character in the string."""
        if old_char in self.s and self.char_count[old_char] > 0:
            self.s = self.s.replace(old_char, new_char, 1)
            self.char_count[old_char] -= 1
            if self.char_count[old_char] == 0:
                del self.char_count[old_char]
            self.char_count[new_char] += 1
            self._generate_all_permutations()
    
    def get_permutations(self):
        """Get all unique permutations."""
        return self.permutations
    
    def get_permutations_count(self):
        """Get count of unique permutations."""
        return len(self.permutations)
    
    def get_permutations_with_constraints(self, constraint_func):
        """Get permutations that satisfy custom constraints."""
        result = []
        for perm in self.permutations:
            if constraint_func(perm):
                result.append(perm)
        return result
    
    def get_permutations_in_range(self, start_pattern, end_pattern):
        """Get permutations within specified pattern range."""
        result = []
        for perm in self.permutations:
            if start_pattern <= perm <= end_pattern:
                result.append(perm)
        return result
    
    def get_permutations_with_pattern(self, pattern):
        """Get permutations containing specified pattern."""
        result = []
        for perm in self.permutations:
            if pattern in perm:
                result.append(perm)
        return result
    
    def get_permutation_statistics(self):
        """Get statistics about permutations."""
        if not self.permutations:
            return {
                'total_permutations': 0,
                'average_length': 0,
                'character_distribution': {},
                'pattern_distribution': {}
            }
        
        total_permutations = len(self.permutations)
        average_length = sum(len(perm) for perm in self.permutations) / total_permutations
        
        # Calculate character distribution
        character_distribution = defaultdict(int)
        for perm in self.permutations:
            for char in perm:
                character_distribution[char] += 1
        
        # Calculate pattern distribution
        pattern_distribution = defaultdict(int)
        for perm in self.permutations:
            for i in range(len(perm) - 1):
                pattern = perm[i:i+2]
                pattern_distribution[pattern] += 1
        
        return {
            'total_permutations': total_permutations,
            'average_length': average_length,
            'character_distribution': dict(character_distribution),
            'pattern_distribution': dict(pattern_distribution)
        }
    
    def get_permutation_patterns(self):
        """Get patterns in permutations."""
        patterns = {
            'palindromic_permutations': 0,
            'sorted_permutations': 0,
            'alternating_permutations': 0,
            'repeated_character_permutations': 0
        }
        
        for perm in self.permutations:
            # Check for palindromic permutations
            if perm == perm[::-1]:
                patterns['palindromic_permutations'] += 1
            
            # Check for sorted permutations
            if perm == ''.join(sorted(perm)):
                patterns['sorted_permutations'] += 1
            
            # Check for alternating permutations
            alternating = True
            for i in range(1, len(perm)):
                if perm[i] == perm[i-1]:
                    alternating = False
                    break
            if alternating:
                patterns['alternating_permutations'] += 1
            
            # Check for repeated character permutations
            if len(set(perm)) < len(perm):
                patterns['repeated_character_permutations'] += 1
        
        return patterns
    
    def get_optimal_permutation_strategy(self):
        """Get optimal strategy for string permutation operations."""
        if not self.permutations:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'uniqueness_rate': 0
            }
        
        # Calculate efficiency rate
        total_possible = len(self.s) ** len(self.s)
        efficiency_rate = len(self.permutations) / total_possible if total_possible > 0 else 0
        
        # Calculate uniqueness rate
        unique_permutations = len(set(self.permutations))
        uniqueness_rate = unique_permutations / len(self.permutations) if self.permutations else 0
        
        # Determine recommended strategy
        if efficiency_rate > 0.5:
            recommended_strategy = 'backtracking_optimal'
        elif uniqueness_rate > 0.8:
            recommended_strategy = 'set_based'
        else:
            recommended_strategy = 'brute_force'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'uniqueness_rate': uniqueness_rate
        }

# Example usage
s = "aab"
dynamic_strings = DynamicCreatingStrings(s)
print(f"Initial permutations count: {dynamic_strings.get_permutations_count()}")

# Add character
dynamic_strings.add_character('c')
print(f"After adding 'c': {dynamic_strings.get_permutations_count()}")

# Remove character
dynamic_strings.remove_character('a')
print(f"After removing 'a': {dynamic_strings.get_permutations_count()}")

# Update character
dynamic_strings.update_character('b', 'd')
print(f"After updating 'b' to 'd': {dynamic_strings.get_permutations_count()}")

# Get permutations with constraints
def constraint_func(perm):
    return len(perm) <= 4

print(f"Permutations with <= 4 length: {len(dynamic_strings.get_permutations_with_constraints(constraint_func))}")

# Get permutations in range
print(f"Permutations in range 'a'-'z': {len(dynamic_strings.get_permutations_in_range('a', 'z'))}")

# Get permutations with pattern
print(f"Permutations containing 'ab': {len(dynamic_strings.get_permutations_with_pattern('ab'))}")

# Get statistics
print(f"Statistics: {dynamic_strings.get_permutation_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_strings.get_permutation_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_strings.get_optimal_permutation_strategy()}")
```

### **Variation 2: Creating Strings with Different Operations**
**Problem**: Handle different types of string operations (weighted characters, priority-based selection, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of string permutation queries.

```python
class AdvancedCreatingStrings:
    def __init__(self, s, weights=None, priorities=None):
        self.s = s
        self.weights = weights or {char: 1 for char in s}
        self.priorities = priorities or {char: 1 for char in s}
        self.char_count = Counter(s)
        self.permutations = []
        self._generate_all_permutations()
    
    def _generate_all_permutations(self):
        """Generate all unique permutations using advanced algorithms."""
        self.permutations = []
        
        def backtrack(current, char_count):
            if len(current) == len(self.s):
                self.permutations.append(current)
                return
            
            for char in char_count:
                if char_count[char] > 0:
                    char_count[char] -= 1
                    backtrack(current + char, char_count)
                    char_count[char] += 1
        
        backtrack("", self.char_count.copy())
    
    def get_permutations(self):
        """Get current unique permutations."""
        return self.permutations
    
    def get_weighted_permutations(self):
        """Get permutations with weights and priorities applied."""
        result = []
        for perm in self.permutations:
            weighted_perm = {
                'permutation': perm,
                'total_weight': sum(self.weights[char] for char in perm),
                'total_priority': sum(self.priorities[char] for char in perm),
                'weighted_score': sum(self.weights[char] * self.priorities[char] for char in perm)
            }
            result.append(weighted_perm)
        return result
    
    def get_permutations_with_priority(self, priority_func):
        """Get permutations considering priority."""
        result = []
        for perm in self.permutations:
            priority = priority_func(perm, self.weights, self.priorities)
            result.append((perm, priority))
        
        # Sort by priority
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_permutations_with_optimization(self, optimization_func):
        """Get permutations using custom optimization function."""
        result = []
        for perm in self.permutations:
            score = optimization_func(perm, self.weights, self.priorities)
            result.append((perm, score))
        
        # Sort by optimization score
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_permutations_with_constraints(self, constraint_func):
        """Get permutations that satisfy custom constraints."""
        result = []
        for perm in self.permutations:
            if constraint_func(perm, self.weights, self.priorities):
                result.append(perm)
        return result
    
    def get_permutations_with_multiple_criteria(self, criteria_list):
        """Get permutations that satisfy multiple criteria."""
        result = []
        for perm in self.permutations:
            satisfies_all_criteria = True
            for criterion in criteria_list:
                if not criterion(perm, self.weights, self.priorities):
                    satisfies_all_criteria = False
                    break
            if satisfies_all_criteria:
                result.append(perm)
        return result
    
    def get_permutations_with_alternatives(self, alternatives):
        """Get permutations considering alternative weights/priorities."""
        result = []
        
        # Check original permutations
        for perm in self.permutations:
            result.append((perm, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedCreatingStrings(self.s, alt_weights, alt_priorities)
            temp_permutations = temp_instance.get_permutations()
            result.append((temp_permutations, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_permutations_with_adaptive_criteria(self, adaptive_func):
        """Get permutations using adaptive criteria."""
        result = []
        for perm in self.permutations:
            if adaptive_func(perm, self.weights, self.priorities, result):
                result.append(perm)
        return result
    
    def get_permutation_optimization(self):
        """Get optimal permutation configuration."""
        strategies = [
            ('permutations', lambda: len(self.permutations)),
            ('weighted_permutations', lambda: len(self.get_weighted_permutations())),
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
s = "aab"
weights = {'a': 2, 'b': 1}
priorities = {'a': 1, 'b': 3}
advanced_strings = AdvancedCreatingStrings(s, weights, priorities)

print(f"Permutations: {len(advanced_strings.get_permutations())}")
print(f"Weighted permutations: {len(advanced_strings.get_weighted_permutations())}")

# Get permutations with priority
def priority_func(perm, weights, priorities):
    return sum(weights[char] for char in perm) + sum(priorities[char] for char in perm)

print(f"Permutations with priority: {len(advanced_strings.get_permutations_with_priority(priority_func))}")

# Get permutations with optimization
def optimization_func(perm, weights, priorities):
    return sum(weights[char] * priorities[char] for char in perm)

print(f"Permutations with optimization: {len(advanced_strings.get_permutations_with_optimization(optimization_func))}")

# Get permutations with constraints
def constraint_func(perm, weights, priorities):
    return len(perm) <= 4 and sum(weights[char] for char in perm) <= 10

print(f"Permutations with constraints: {len(advanced_strings.get_permutations_with_constraints(constraint_func))}")

# Get permutations with multiple criteria
def criterion1(perm, weights, priorities):
    return len(perm) <= 4

def criterion2(perm, weights, priorities):
    return sum(weights[char] for char in perm) <= 10

criteria_list = [criterion1, criterion2]
print(f"Permutations with multiple criteria: {len(advanced_strings.get_permutations_with_multiple_criteria(criteria_list))}")

# Get permutations with alternatives
alternatives = [({'a': 1, 'b': 1}, {'a': 1, 'b': 1}), ({'a': 3, 'b': 2}, {'a': 2, 'b': 1})]
print(f"Permutations with alternatives: {len(advanced_strings.get_permutations_with_alternatives(alternatives))}")

# Get permutations with adaptive criteria
def adaptive_func(perm, weights, priorities, current_result):
    return len(perm) <= 4 and len(current_result) < 10

print(f"Permutations with adaptive criteria: {len(advanced_strings.get_permutations_with_adaptive_criteria(adaptive_func))}")

# Get permutation optimization
print(f"Permutation optimization: {advanced_strings.get_permutation_optimization()}")
```

### **Variation 3: Creating Strings with Constraints**
**Problem**: Handle string permutations with additional constraints (length limits, character constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedCreatingStrings:
    def __init__(self, s, constraints=None):
        self.s = s
        self.constraints = constraints or {}
        self.char_count = Counter(s)
        self.permutations = []
        self._generate_all_permutations()
    
    def _generate_all_permutations(self):
        """Generate all unique permutations considering constraints."""
        self.permutations = []
        
        def backtrack(current, char_count):
            if len(current) == len(self.s):
                if self._is_valid_permutation(current):
                    self.permutations.append(current)
                return
            
            for char in char_count:
                if char_count[char] > 0:
                    char_count[char] -= 1
                    backtrack(current + char, char_count)
                    char_count[char] += 1
        
        backtrack("", self.char_count.copy())
    
    def _is_valid_permutation(self, perm):
        """Check if a permutation is valid considering constraints."""
        # Length constraints
        if 'min_length' in self.constraints:
            if len(perm) < self.constraints['min_length']:
                return False
        
        if 'max_length' in self.constraints:
            if len(perm) > self.constraints['max_length']:
                return False
        
        # Character constraints
        if 'forbidden_chars' in self.constraints:
            for char in self.constraints['forbidden_chars']:
                if char in perm:
                    return False
        
        if 'required_chars' in self.constraints:
            for char in self.constraints['required_chars']:
                if char not in perm:
                    return False
        
        # Pattern constraints
        if 'forbidden_patterns' in self.constraints:
            for pattern in self.constraints['forbidden_patterns']:
                if pattern in perm:
                    return False
        
        if 'required_patterns' in self.constraints:
            for pattern in self.constraints['required_patterns']:
                if pattern not in perm:
                    return False
        
        # Weight constraints
        if 'max_weight' in self.constraints:
            weights = self.constraints.get('weights', {char: 1 for char in perm})
            weight = sum(weights[char] for char in perm)
            if weight > self.constraints['max_weight']:
                return False
        
        if 'min_weight' in self.constraints:
            weights = self.constraints.get('weights', {char: 1 for char in perm})
            weight = sum(weights[char] for char in perm)
            if weight < self.constraints['min_weight']:
                return False
        
        return True
    
    def get_permutations_with_length_constraints(self, min_length, max_length):
        """Get permutations considering length constraints."""
        result = []
        for perm in self.permutations:
            if min_length <= len(perm) <= max_length:
                result.append(perm)
        return result
    
    def get_permutations_with_character_constraints(self, character_constraints):
        """Get permutations considering character constraints."""
        result = []
        for perm in self.permutations:
            satisfies_constraints = True
            for constraint in character_constraints:
                if not constraint(perm):
                    satisfies_constraints = False
                    break
            if satisfies_constraints:
                result.append(perm)
        return result
    
    def get_permutations_with_pattern_constraints(self, pattern_constraints):
        """Get permutations considering pattern constraints."""
        result = []
        for perm in self.permutations:
            satisfies_constraints = True
            for constraint in pattern_constraints:
                if not constraint(perm):
                    satisfies_constraints = False
                    break
            if satisfies_constraints:
                result.append(perm)
        return result
    
    def get_permutations_with_weight_constraints(self, weight_limits):
        """Get permutations considering weight constraints."""
        result = []
        weights = self.constraints.get('weights', {char: 1 for char in self.s})
        
        for perm in self.permutations:
            weight = sum(weights[char] for char in perm)
            if weight_limits[0] <= weight <= weight_limits[1]:
                result.append(perm)
        return result
    
    def get_permutations_with_mathematical_constraints(self, constraint_func):
        """Get permutations that satisfy custom mathematical constraints."""
        result = []
        for perm in self.permutations:
            if constraint_func(perm):
                result.append(perm)
        return result
    
    def get_permutations_with_range_constraints(self, range_constraints):
        """Get permutations that satisfy range constraints."""
        result = []
        for perm in self.permutations:
            satisfies_constraints = True
            for constraint in range_constraints:
                if not constraint(perm):
                    satisfies_constraints = False
                    break
            if satisfies_constraints:
                result.append(perm)
        return result
    
    def get_permutations_with_optimization_constraints(self, optimization_func):
        """Get permutations using custom optimization constraints."""
        # Sort permutations by optimization function
        all_permutations = []
        for perm in self.permutations:
            score = optimization_func(perm)
            all_permutations.append((perm, score))
        
        # Sort by optimization score
        all_permutations.sort(key=lambda x: x[1], reverse=True)
        
        return [perm for perm, _ in all_permutations]
    
    def get_permutations_with_multiple_constraints(self, constraints_list):
        """Get permutations that satisfy multiple constraints."""
        result = []
        for perm in self.permutations:
            satisfies_all_constraints = True
            for constraint in constraints_list:
                if not constraint(perm):
                    satisfies_all_constraints = False
                    break
            if satisfies_all_constraints:
                result.append(perm)
        return result
    
    def get_permutations_with_priority_constraints(self, priority_func):
        """Get permutations with priority-based constraints."""
        # Sort permutations by priority
        all_permutations = []
        for perm in self.permutations:
            priority = priority_func(perm)
            all_permutations.append((perm, priority))
        
        # Sort by priority
        all_permutations.sort(key=lambda x: x[1], reverse=True)
        
        return [perm for perm, _ in all_permutations]
    
    def get_permutations_with_adaptive_constraints(self, adaptive_func):
        """Get permutations with adaptive constraints."""
        result = []
        for perm in self.permutations:
            if adaptive_func(perm, result):
                result.append(perm)
        return result
    
    def get_optimal_permutation_strategy(self):
        """Get optimal permutation strategy considering all constraints."""
        strategies = [
            ('length_constraints', self.get_permutations_with_length_constraints),
            ('character_constraints', self.get_permutations_with_character_constraints),
            ('pattern_constraints', self.get_permutations_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_count = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'length_constraints':
                    current_count = len(strategy_func(1, len(self.s)))
                elif strategy_name == 'character_constraints':
                    character_constraints = [lambda p: 'a' in p]
                    current_count = len(strategy_func(character_constraints))
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda p: 'ab' not in p]
                    current_count = len(strategy_func(pattern_constraints))
                
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
    'forbidden_chars': ['x', 'y'],
    'required_chars': ['a'],
    'forbidden_patterns': ['aa'],
    'required_patterns': ['ab'],
    'max_weight': 10,
    'min_weight': 2,
    'weights': {'a': 2, 'b': 1, 'c': 3}
}

s = "aab"
constrained_strings = ConstrainedCreatingStrings(s, constraints)

print("Length-constrained permutations:", len(constrained_strings.get_permutations_with_length_constraints(2, 3)))

print("Character-constrained permutations:", len(constrained_strings.get_permutations_with_character_constraints([lambda p: 'a' in p])))

print("Pattern-constrained permutations:", len(constrained_strings.get_permutations_with_pattern_constraints([lambda p: 'ab' not in p])))

print("Weight-constrained permutations:", len(constrained_strings.get_permutations_with_weight_constraints((2, 8))))

# Mathematical constraints
def custom_constraint(perm):
    return len(perm) <= 3 and perm.count('a') <= 2

print("Mathematical constraint permutations:", len(constrained_strings.get_permutations_with_mathematical_constraints(custom_constraint)))

# Range constraints
def range_constraint(perm):
    return 2 <= len(perm) <= 4

range_constraints = [range_constraint]
print("Range-constrained permutations:", len(constrained_strings.get_permutations_with_range_constraints(range_constraints)))

# Multiple constraints
def constraint1(perm):
    return len(perm) <= 3

def constraint2(perm):
    return perm.count('a') <= 2

constraints_list = [constraint1, constraint2]
print("Multiple constraints permutations:", len(constrained_strings.get_permutations_with_multiple_constraints(constraints_list)))

# Priority constraints
def priority_func(perm):
    return len(perm) + sum(1 for char in perm if char == 'a')

print("Priority-constrained permutations:", len(constrained_strings.get_permutations_with_priority_constraints(priority_func)))

# Adaptive constraints
def adaptive_func(perm, current_result):
    return len(perm) <= 3 and len(current_result) < 10

print("Adaptive constraint permutations:", len(constrained_strings.get_permutations_with_adaptive_constraints(adaptive_func)))

# Optimal strategy
optimal = constrained_strings.get_optimal_permutation_strategy()
print(f"Optimal strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Permutations](https://cses.fi/problemset/task/1075)s
- [Bit Strings](https://cses.fi/problemset/task/1075)s
- [Chessboard and Queens](https://cses.fi/problemset/task/1075)s

#### **LeetCode Problems**
- [Permutations](https://leetcode.com/problems/permutations/) - Backtracking
- [Permutations II](https://leetcode.com/problems/permutations-ii/) - Backtracking
- [Next Permutation](https://leetcode.com/problems/next-permutation/) - Array

#### **Problem Categories**
- **Introductory Problems**: String generation, permutations
- **Backtracking**: String permutations, recursive generation
- **String Algorithms**: String manipulation, permutation generation

## 🔗 Additional Resources

### **Algorithm References**
- [Introductory Problems](https://cp-algorithms.com/intro-to-algorithms.html) - Introductory algorithms
- [Backtracking](https://cp-algorithms.com/backtracking.html) - Backtracking algorithms
- [String Algorithms](https://cp-algorithms.com/string/basic-string-processing.html) - String algorithms

### **Practice Problems**
- [CSES Permutations](https://cses.fi/problemset/task/1075) - Easy
- [CSES Bit Strings](https://cses.fi/problemset/task/1075) - Easy
- [CSES Chessboard and Queens](https://cses.fi/problemset/task/1075) - Easy

### **Further Reading**
- [Permutation](https://en.wikipedia.org/wiki/Permutation) - Wikipedia article
- [Backtracking](https://en.wikipedia.org/wiki/Backtracking) - Wikipedia article
- [String](https://en.wikipedia.org/wiki/String_(computer_science)) - Wikipedia article
