---
layout: simple
title: "Repetitions"
permalink: /problem_soulutions/introductory_problems/repetitions_analysis
---

# Repetitions

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand string analysis and consecutive character counting problems
- Apply sliding window or linear scanning to find maximum consecutive repetitions
- Implement efficient string analysis algorithms with proper consecutive character tracking
- Optimize string analysis using linear scanning and consecutive character counting
- Handle edge cases in string analysis (single character, no repetitions, large strings)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: String analysis, consecutive character counting, sliding window, linear scanning
- **Data Structures**: String processing, character tracking, consecutive counting, maximum tracking
- **Mathematical Concepts**: String mathematics, consecutive analysis, maximum finding, string theory
- **Programming Skills**: String processing, consecutive character counting, maximum tracking, algorithm implementation
- **Related Problems**: String problems, Consecutive counting, Maximum finding, String analysis

## Problem Description

**Problem**: You are given a DNA sequence consisting of characters A, C, G, and T. Find the longest repetition in the sequence. This is a maximum-length substring containing only one type of character.

**Input**: A string of n characters (1 ≤ n ≤ 10⁶)

**Output**: Print one integer: the length of the longest repetition.

**Constraints**:
- 1 ≤ n ≤ 10⁶
- String contains only characters A, C, G, T
- Need to find maximum consecutive same characters
- Return the length of longest repetition
- Handle edge cases (single character, no repetitions)

**Example**:
```
Input: ATTCGGGA

Output: 3

Explanation: The longest repetition is "GGG" with length 3.
```

## Visual Example

### Input and Character Analysis
```
Input: ATTCGGGA
Characters: A, T, T, C, G, G, G, A

Character analysis:
A: position 0, length 1
T: positions 1-2, length 2
C: position 3, length 1
G: positions 4-6, length 3 ← Longest repetition
A: position 7, length 1
```

### Consecutive Character Tracking
```
Step-by-step tracking:
Position 0: A (current_length = 1, max_length = 1)
Position 1: T (current_length = 1, max_length = 1)
Position 2: T (current_length = 2, max_length = 2)
Position 3: C (current_length = 1, max_length = 2)
Position 4: G (current_length = 1, max_length = 2)
Position 5: G (current_length = 2, max_length = 2)
Position 6: G (current_length = 3, max_length = 3)
Position 7: A (current_length = 1, max_length = 3)

Final result: 3
```

### Key Insight
The solution works by:
1. Scanning the string from left to right
2. Tracking consecutive same characters
3. Updating maximum length when character changes
4. Time complexity: O(n) for single pass
5. Space complexity: O(1) for constant variables

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force with Nested Loops (Inefficient)

**Key Insights from Brute Force Solution:**
- Check every possible substring to find the longest repetition
- Simple but computationally expensive approach
- Not suitable for large strings
- Straightforward implementation but poor performance

**Algorithm:**
1. For each starting position, check all possible ending positions
2. For each substring, check if all characters are the same
3. Track the maximum length found
4. Return the maximum length

**Visual Example:**
```
Brute force: Check all substrings
For "ATTCGGGA":
- Check A: length 1
- Check AT: different characters
- Check ATT: different characters
- Check T: length 1
- Check TT: length 2
- Check TTC: different characters
- Check C: length 1
- Check CG: different characters
- Check G: length 1
- Check GG: length 2
- Check GGG: length 3 ← Maximum
- Check GGGA: different characters
- Check A: length 1
```

**Implementation:**
```python
def repetitions_brute_force(sequence):
    n = len(sequence)
    if n == 0:
        return 0
    
    max_length = 1
    
    # Check all possible substrings
    for i in range(n):
        for j in range(i, n):
            # Check if all characters in substring are the same
            if all(sequence[i] == sequence[k] for k in range(i, j + 1)):
                max_length = max(max_length, j - i + 1)
    
    return max_length

def solve_repetitions_brute_force():
    sequence = input().strip()
    result = repetitions_brute_force(sequence)
    print(result)
```

**Time Complexity:** O(n³) for nested loops and character checking
**Space Complexity:** O(1) for storing variables

**Why it's inefficient:**
- O(n³) time complexity is too slow for large strings
- Not suitable for competitive programming with n up to 10^6
- Inefficient for long strings
- Poor performance with large inputs

### Approach 2: Simple Linear Scanning (Better)

**Key Insights from Simple Linear Scanning Solution:**
- Use linear scanning to find consecutive same characters
- Much more efficient than brute force approach
- Standard method for consecutive character counting
- Can handle larger inputs than brute force

**Algorithm:**
1. Scan the string from left to right
2. Count consecutive same characters
3. Update maximum when character changes
4. Handle the last group of characters

**Visual Example:**
```
Simple linear scanning for "ATTCGGGA":
- A: current_length = 1, max_length = 1
- T: current_length = 1, max_length = 1
- T: current_length = 2, max_length = 2
- C: current_length = 1, max_length = 2
- G: current_length = 1, max_length = 2
- G: current_length = 2, max_length = 2
- G: current_length = 3, max_length = 3
- A: current_length = 1, max_length = 3
```

**Implementation:**
```python
def repetitions_simple_linear(sequence):
    n = len(sequence)
    if n == 0:
        return 0
    
    max_length = 1
    current_length = 1
    
    for i in range(1, n):
        if sequence[i] == sequence[i - 1]:
            current_length += 1
        else:
            max_length = max(max_length, current_length)
            current_length = 1
    
    # Don't forget the last group
    max_length = max(max_length, current_length)
    
    return max_length

def solve_repetitions_simple():
    sequence = input().strip()
    result = repetitions_simple_linear(sequence)
    print(result)
```

**Time Complexity:** O(n) for single pass through the string
**Space Complexity:** O(1) for storing variables

**Why it's better:**
- O(n) time complexity is much better than O(n³)
- Uses linear scanning for efficient solution
- Suitable for competitive programming
- Efficient for all practical cases

### Approach 3: Optimized Linear Scanning (Optimal)

**Key Insights from Optimized Linear Scanning Solution:**
- Use optimized linear scanning with cleaner code
- Most efficient approach for consecutive character counting
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use optimized linear scanning
2. Update maximum inside the loop for cleaner logic
3. Handle edge cases efficiently
4. Return the maximum length found

**Visual Example:**
```
Optimized linear scanning for "ATTCGGGA":
- Optimized scanning with cleaner logic
- Update maximum inside the loop
- Handle edge cases efficiently
- Final result: 3
```

**Implementation:**
```python
def repetitions_optimized(sequence):
    n = len(sequence)
    if n == 0:
        return 0
    
    max_length = 1
    current_length = 1
    
    for i in range(1, n):
        if sequence[i] == sequence[i - 1]:
            current_length += 1
            max_length = max(max_length, current_length)
        else:
            current_length = 1
    
    return max_length

def solve_repetitions():
    sequence = input().strip()
    result = repetitions_optimized(sequence)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_repetitions()
```

**Time Complexity:** O(n) for single pass through the string
**Space Complexity:** O(1) for storing variables

**Why it's optimal:**
- O(n) time complexity is optimal for string scanning problems
- Uses optimized linear scanning
- Most efficient approach for competitive programming
- Standard method for consecutive character counting

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Repetitions with Different Characters
**Problem**: Find longest repetition with any character set.

**Link**: [CSES Problem Set - Repetitions Different Characters](https://cses.fi/problemset/task/repetitions_different_characters)

```python
def repetitions_different_characters(sequence, allowed_chars):
    n = len(sequence)
    if n == 0:
        return 0
    
    max_length = 1
    current_length = 1
    
    for i in range(1, n):
        if sequence[i] == sequence[i - 1] and sequence[i] in allowed_chars:
            current_length += 1
            max_length = max(max_length, current_length)
        else:
            current_length = 1
    
    return max_length
```

### Variation 2: Repetitions with Minimum Length
**Problem**: Find longest repetition with minimum length constraint.

**Link**: [CSES Problem Set - Repetitions Minimum Length](https://cses.fi/problemset/task/repetitions_minimum_length)

```python
def repetitions_minimum_length(sequence, min_length):
    n = len(sequence)
    if n == 0:
        return 0
    
    max_length = 1
    current_length = 1
    
    for i in range(1, n):
        if sequence[i] == sequence[i - 1]:
            current_length += 1
            if current_length >= min_length:
                max_length = max(max_length, current_length)
        else:
            current_length = 1
    
    return max_length if max_length >= min_length else 0
```

### Variation 3: Repetitions with Character Frequency
**Problem**: Find longest repetition considering character frequency.

**Link**: [CSES Problem Set - Repetitions Character Frequency](https://cses.fi/problemset/task/repetitions_character_frequency)

```python
def repetitions_character_frequency(sequence, char_freq):
    n = len(sequence)
    if n == 0:
        return 0
    
    max_length = 1
    current_length = 1
    
    for i in range(1, n):
        if sequence[i] == sequence[i - 1] and char_freq[sequence[i]] > 0:
            current_length += 1
            max_length = max(max_length, current_length)
        else:
            current_length = 1
    
    return max_length
```

## Problem Variations

### **Variation 1: Repetitions with Dynamic Updates**
**Problem**: Handle dynamic string updates (add/remove/update characters) while finding the longest repetition efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic string management.

```python
from collections import defaultdict

class DynamicRepetitions:
    def __init__(self, string=""):
        self.string = string
        self.char_count = defaultdict(int)
        for char in self.string:
            self.char_count[char] += 1
        self._update_repetition_info()
    
    def _update_repetition_info(self):
        """Update repetition feasibility information."""
        self.total_chars = len(self.string)
        self.unique_chars = len(self.char_count)
        self.max_repetition = self._calculate_max_repetition()
    
    def _calculate_max_repetition(self):
        """Calculate maximum consecutive repetition."""
        if not self.string:
            return 0
        
        max_repetition = 1
        current_repetition = 1
        
        for i in range(1, len(self.string)):
            if self.string[i] == self.string[i-1]:
                current_repetition += 1
                max_repetition = max(max_repetition, current_repetition)
            else:
                current_repetition = 1
        
        return max_repetition
    
    def add_character(self, char, position=None):
        """Add character to the string."""
        if position is None:
            self.string += char
        else:
            self.string = self.string[:position] + char + self.string[position:]
        
        self.char_count[char] += 1
        self._update_repetition_info()
    
    def remove_character(self, position):
        """Remove character from the string."""
        if 0 <= position < len(self.string):
            char = self.string[position]
            self.string = self.string[:position] + self.string[position+1:]
            self.char_count[char] -= 1
            if self.char_count[char] == 0:
                del self.char_count[char]
            self._update_repetition_info()
    
    def update_character(self, position, new_char):
        """Update character in the string."""
        if 0 <= position < len(self.string):
            old_char = self.string[position]
            self.string = self.string[:position] + new_char + self.string[position+1:]
            
            self.char_count[old_char] -= 1
            if self.char_count[old_char] == 0:
                del self.char_count[old_char]
            
            self.char_count[new_char] += 1
            self._update_repetition_info()
    
    def get_longest_repetition(self):
        """Get the longest consecutive repetition."""
        return self.max_repetition
    
    def get_repetitions_with_constraints(self, constraint_func):
        """Get repetitions that satisfy custom constraints."""
        if not self.string:
            return []
        
        result = []
        current_char = self.string[0]
        current_count = 1
        
        for i in range(1, len(self.string)):
            if self.string[i] == current_char:
                current_count += 1
            else:
                if constraint_func(current_char, current_count):
                    result.append((current_char, current_count))
                current_char = self.string[i]
                current_count = 1
        
        # Check last repetition
        if constraint_func(current_char, current_count):
            result.append((current_char, current_count))
        
        return result
    
    def get_repetitions_in_range(self, min_length, max_length):
        """Get repetitions within specified length range."""
        if not self.string:
            return []
        
        result = []
        current_char = self.string[0]
        current_count = 1
        
        for i in range(1, len(self.string)):
            if self.string[i] == current_char:
                current_count += 1
            else:
                if min_length <= current_count <= max_length:
                    result.append((current_char, current_count))
                current_char = self.string[i]
                current_count = 1
        
        # Check last repetition
        if min_length <= current_count <= max_length:
            result.append((current_char, current_count))
        
        return result
    
    def get_repetitions_with_pattern(self, pattern_func):
        """Get repetitions matching specified pattern."""
        if not self.string:
            return []
        
        result = []
        current_char = self.string[0]
        current_count = 1
        
        for i in range(1, len(self.string)):
            if self.string[i] == current_char:
                current_count += 1
            else:
                if pattern_func(current_char, current_count):
                    result.append((current_char, current_count))
                current_char = self.string[i]
                current_count = 1
        
        # Check last repetition
        if pattern_func(current_char, current_count):
            result.append((current_char, current_count))
        
        return result
    
    def get_string_statistics(self):
        """Get statistics about the string."""
        if not self.string:
            return {
                'total_chars': 0,
                'unique_chars': 0,
                'max_repetition': 0,
                'char_distribution': {}
            }
        
        return {
            'total_chars': self.total_chars,
            'unique_chars': self.unique_chars,
            'max_repetition': self.max_repetition,
            'char_distribution': dict(self.char_count)
        }
    
    def get_repetition_patterns(self):
        """Get patterns in repetitions."""
        patterns = {
            'single_char_repetition': 0,
            'multiple_char_repetitions': 0,
            'high_frequency_chars': 0,
            'low_frequency_chars': 0
        }
        
        if not self.string:
            return patterns
        
        # Check for single character repetition
        if len(self.char_count) == 1:
            patterns['single_char_repetition'] = 1
        
        # Check for multiple character repetitions
        if len(self.char_count) > 1:
            patterns['multiple_char_repetitions'] = 1
        
        # Check for high frequency characters
        max_freq = max(self.char_count.values())
        if max_freq > len(self.string) * 0.5:
            patterns['high_frequency_chars'] = 1
        
        # Check for low frequency characters
        min_freq = min(self.char_count.values())
        if min_freq < len(self.string) * 0.1:
            patterns['low_frequency_chars'] = 1
        
        return patterns
    
    def get_optimal_repetition_strategy(self):
        """Get optimal strategy for repetition finding."""
        if not self.string:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'repetition_feasibility': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = self.unique_chars / self.total_chars if self.total_chars > 0 else 0
        
        # Calculate repetition feasibility
        repetition_feasibility = 1.0 if self.max_repetition > 0 else 0.0
        
        # Determine recommended strategy
        if self.max_repetition <= 10:
            recommended_strategy = 'simple_scan'
        elif self.unique_chars == 1:
            recommended_strategy = 'single_char_optimization'
        else:
            recommended_strategy = 'advanced_scan'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'repetition_feasibility': repetition_feasibility
        }

# Example usage
string = "AAABBBCCCC"
dynamic_repetitions = DynamicRepetitions(string)
print(f"Max repetition: {dynamic_repetitions.max_repetition}")
print(f"Longest repetition: {dynamic_repetitions.get_longest_repetition()}")

# Add character
dynamic_repetitions.add_character('D')
print(f"After adding D: {dynamic_repetitions.max_repetition}")

# Remove character
dynamic_repetitions.remove_character(0)
print(f"After removing first character: {dynamic_repetitions.max_repetition}")

# Update character
dynamic_repetitions.update_character(0, 'E')
print(f"After updating first character to E: {dynamic_repetitions.max_repetition}")

# Get repetitions with constraints
def constraint_func(char, count):
    return count >= 3

print(f"Repetitions with count >= 3: {dynamic_repetitions.get_repetitions_with_constraints(constraint_func)}")

# Get repetitions in range
print(f"Repetitions in range 2-4: {dynamic_repetitions.get_repetitions_in_range(2, 4)}")

# Get repetitions with pattern
def pattern_func(char, count):
    return char in 'ABC'

print(f"Repetitions with pattern: {dynamic_repetitions.get_repetitions_with_pattern(pattern_func)}")

# Get statistics
print(f"Statistics: {dynamic_repetitions.get_string_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_repetitions.get_repetition_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_repetitions.get_optimal_repetition_strategy()}")
```

### **Variation 2: Repetitions with Different Operations**
**Problem**: Handle different types of repetition operations (weighted characters, priority-based selection, advanced string analysis).

**Approach**: Use advanced data structures for efficient different types of repetition operations.

```python
class AdvancedRepetitions:
    def __init__(self, string="", weights=None, priorities=None):
        self.string = string
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.char_count = defaultdict(int)
        for char in self.string:
            self.char_count[char] += 1
        self._update_repetition_info()
    
    def _update_repetition_info(self):
        """Update repetition feasibility information."""
        self.total_chars = len(self.string)
        self.unique_chars = len(self.char_count)
        self.max_repetition = self._calculate_max_repetition()
    
    def _calculate_max_repetition(self):
        """Calculate maximum consecutive repetition."""
        if not self.string:
            return 0
        
        max_repetition = 1
        current_repetition = 1
        
        for i in range(1, len(self.string)):
            if self.string[i] == self.string[i-1]:
                current_repetition += 1
                max_repetition = max(max_repetition, current_repetition)
            else:
                current_repetition = 1
        
        return max_repetition
    
    def get_weighted_repetitions(self):
        """Get repetitions with weights and priorities applied."""
        if not self.string:
            return []
        
        result = []
        current_char = self.string[0]
        current_count = 1
        
        for i in range(1, len(self.string)):
            if self.string[i] == current_char:
                current_count += 1
            else:
                weight = self.weights.get(current_char, 1)
                priority = self.priorities.get(current_char, 1)
                weighted_repetition = {
                    'char': current_char,
                    'count': current_count,
                    'weight': weight,
                    'priority': priority,
                    'weighted_score': current_count * weight * priority
                }
                result.append(weighted_repetition)
                current_char = self.string[i]
                current_count = 1
        
        # Check last repetition
        weight = self.weights.get(current_char, 1)
        priority = self.priorities.get(current_char, 1)
        weighted_repetition = {
            'char': current_char,
            'count': current_count,
            'weight': weight,
            'priority': priority,
            'weighted_score': current_count * weight * priority
        }
        result.append(weighted_repetition)
        
        return result
    
    def get_repetitions_with_priority(self, priority_func):
        """Get repetitions considering priority."""
        if not self.string:
            return []
        
        result = []
        current_char = self.string[0]
        current_count = 1
        
        for i in range(1, len(self.string)):
            if self.string[i] == current_char:
                current_count += 1
            else:
                priority = priority_func(current_char, current_count, self.weights, self.priorities)
                result.append((current_char, current_count, priority))
                current_char = self.string[i]
                current_count = 1
        
        # Check last repetition
        priority = priority_func(current_char, current_count, self.weights, self.priorities)
        result.append((current_char, current_count, priority))
        
        # Sort by priority
        result.sort(key=lambda x: x[2], reverse=True)
        return result
    
    def get_repetitions_with_optimization(self, optimization_func):
        """Get repetitions using custom optimization function."""
        if not self.string:
            return []
        
        result = []
        current_char = self.string[0]
        current_count = 1
        
        for i in range(1, len(self.string)):
            if self.string[i] == current_char:
                current_count += 1
            else:
                score = optimization_func(current_char, current_count, self.weights, self.priorities)
                result.append((current_char, current_count, score))
                current_char = self.string[i]
                current_count = 1
        
        # Check last repetition
        score = optimization_func(current_char, current_count, self.weights, self.priorities)
        result.append((current_char, current_count, score))
        
        # Sort by optimization score
        result.sort(key=lambda x: x[2], reverse=True)
        return result
    
    def get_repetitions_with_constraints(self, constraint_func):
        """Get repetitions that satisfy custom constraints."""
        if not self.string:
            return []
        
        result = []
        current_char = self.string[0]
        current_count = 1
        
        for i in range(1, len(self.string)):
            if self.string[i] == current_char:
                current_count += 1
            else:
                if constraint_func(current_char, current_count, self.weights, self.priorities):
                    result.append((current_char, current_count))
                current_char = self.string[i]
                current_count = 1
        
        # Check last repetition
        if constraint_func(current_char, current_count, self.weights, self.priorities):
            result.append((current_char, current_count))
        
        return result
    
    def get_repetitions_with_multiple_criteria(self, criteria_list):
        """Get repetitions that satisfy multiple criteria."""
        if not self.string:
            return []
        
        result = []
        current_char = self.string[0]
        current_count = 1
        
        for i in range(1, len(self.string)):
            if self.string[i] == current_char:
                current_count += 1
            else:
                satisfies_all_criteria = True
                for criterion in criteria_list:
                    if not criterion(current_char, current_count, self.weights, self.priorities):
                        satisfies_all_criteria = False
                        break
                
                if satisfies_all_criteria:
                    result.append((current_char, current_count))
                
                current_char = self.string[i]
                current_count = 1
        
        # Check last repetition
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(current_char, current_count, self.weights, self.priorities):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            result.append((current_char, current_count))
        
        return result
    
    def get_repetitions_with_alternatives(self, alternatives):
        """Get repetitions considering alternative weights/priorities."""
        result = []
        
        # Check original repetitions
        original_repetitions = self.get_weighted_repetitions()
        result.append((original_repetitions, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedRepetitions(self.string, alt_weights, alt_priorities)
            temp_repetitions = temp_instance.get_weighted_repetitions()
            result.append((temp_repetitions, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_repetitions_with_adaptive_criteria(self, adaptive_func):
        """Get repetitions using adaptive criteria."""
        if not self.string:
            return []
        
        result = []
        current_char = self.string[0]
        current_count = 1
        
        for i in range(1, len(self.string)):
            if self.string[i] == current_char:
                current_count += 1
            else:
                if adaptive_func(current_char, current_count, self.weights, self.priorities, result):
                    result.append((current_char, current_count))
                current_char = self.string[i]
                current_count = 1
        
        # Check last repetition
        if adaptive_func(current_char, current_count, self.weights, self.priorities, result):
            result.append((current_char, current_count))
        
        return result
    
    def get_repetition_optimization(self):
        """Get optimal repetition configuration."""
        strategies = [
            ('weighted_repetitions', lambda: len(self.get_weighted_repetitions())),
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
string = "AAABBBCCCC"
weights = {char: ord(char) - ord('A') + 1 for char in string}  # Weight based on character position
priorities = {char: string.count(char) for char in string}  # Priority based on frequency
advanced_repetitions = AdvancedRepetitions(string, weights, priorities)

print(f"Weighted repetitions: {len(advanced_repetitions.get_weighted_repetitions())}")

# Get repetitions with priority
def priority_func(char, count, weights, priorities):
    return count * weights.get(char, 1) + priorities.get(char, 1)

print(f"Repetitions with priority: {len(advanced_repetitions.get_repetitions_with_priority(priority_func))}")

# Get repetitions with optimization
def optimization_func(char, count, weights, priorities):
    return count * weights.get(char, 1) * priorities.get(char, 1)

print(f"Repetitions with optimization: {len(advanced_repetitions.get_repetitions_with_optimization(optimization_func))}")

# Get repetitions with constraints
def constraint_func(char, count, weights, priorities):
    return count >= 3 and weights.get(char, 1) >= 2

print(f"Repetitions with constraints: {len(advanced_repetitions.get_repetitions_with_constraints(constraint_func))}")

# Get repetitions with multiple criteria
def criterion1(char, count, weights, priorities):
    return count >= 3

def criterion2(char, count, weights, priorities):
    return weights.get(char, 1) >= 2

criteria_list = [criterion1, criterion2]
print(f"Repetitions with multiple criteria: {len(advanced_repetitions.get_repetitions_with_multiple_criteria(criteria_list))}")

# Get repetitions with alternatives
alternatives = [({char: 1 for char in string}, {char: 1 for char in string}), ({char: len(char) for char in string}, {char: char.count('A') + 1 for char in string})]
print(f"Repetitions with alternatives: {len(advanced_repetitions.get_repetitions_with_alternatives(alternatives))}")

# Get repetitions with adaptive criteria
def adaptive_func(char, count, weights, priorities, current_result):
    return count >= 3 and len(current_result) < 5

print(f"Repetitions with adaptive criteria: {len(advanced_repetitions.get_repetitions_with_adaptive_criteria(adaptive_func))}")

# Get repetition optimization
print(f"Repetition optimization: {advanced_repetitions.get_repetition_optimization()}")
```

### **Variation 3: Repetitions with Constraints**
**Problem**: Handle repetition finding with additional constraints (length limits, character constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedRepetitions:
    def __init__(self, string="", constraints=None):
        self.string = string
        self.constraints = constraints or {}
        self.char_count = defaultdict(int)
        for char in self.string:
            self.char_count[char] += 1
        self._update_repetition_info()
    
    def _update_repetition_info(self):
        """Update repetition feasibility information."""
        self.total_chars = len(self.string)
        self.unique_chars = len(self.char_count)
        self.max_repetition = self._calculate_max_repetition()
    
    def _calculate_max_repetition(self):
        """Calculate maximum consecutive repetition."""
        if not self.string:
            return 0
        
        max_repetition = 1
        current_repetition = 1
        
        for i in range(1, len(self.string)):
            if self.string[i] == self.string[i-1]:
                current_repetition += 1
                max_repetition = max(max_repetition, current_repetition)
            else:
                current_repetition = 1
        
        return max_repetition
    
    def _is_valid_repetition(self, char, count):
        """Check if repetition is valid considering constraints."""
        # Length constraints
        if 'min_length' in self.constraints:
            if count < self.constraints['min_length']:
                return False
        
        if 'max_length' in self.constraints:
            if count > self.constraints['max_length']:
                return False
        
        # Character constraints
        if 'forbidden_chars' in self.constraints:
            if char in self.constraints['forbidden_chars']:
                return False
        
        if 'required_chars' in self.constraints:
            if char not in self.constraints['required_chars']:
                return False
        
        # Pattern constraints
        if 'pattern_constraints' in self.constraints:
            for constraint in self.constraints['pattern_constraints']:
                if not constraint(char, count):
                    return False
        
        return True
    
    def get_repetitions_with_length_constraints(self, min_length, max_length):
        """Get repetitions considering length constraints."""
        if not self.string:
            return []
        
        result = []
        current_char = self.string[0]
        current_count = 1
        
        for i in range(1, len(self.string)):
            if self.string[i] == current_char:
                current_count += 1
            else:
                if min_length <= current_count <= max_length:
                    result.append((current_char, current_count))
                current_char = self.string[i]
                current_count = 1
        
        # Check last repetition
        if min_length <= current_count <= max_length:
            result.append((current_char, current_count))
        
        return result
    
    def get_repetitions_with_character_constraints(self, character_constraints):
        """Get repetitions considering character constraints."""
        if not self.string:
            return []
        
        result = []
        current_char = self.string[0]
        current_count = 1
        
        for i in range(1, len(self.string)):
            if self.string[i] == current_char:
                current_count += 1
            else:
                satisfies_constraints = True
                for constraint in character_constraints:
                    if not constraint(current_char, current_count):
                        satisfies_constraints = False
                        break
                
                if satisfies_constraints:
                    result.append((current_char, current_count))
                
                current_char = self.string[i]
                current_count = 1
        
        # Check last repetition
        satisfies_constraints = True
        for constraint in character_constraints:
            if not constraint(current_char, current_count):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            result.append((current_char, current_count))
        
        return result
    
    def get_repetitions_with_pattern_constraints(self, pattern_constraints):
        """Get repetitions considering pattern constraints."""
        if not self.string:
            return []
        
        result = []
        current_char = self.string[0]
        current_count = 1
        
        for i in range(1, len(self.string)):
            if self.string[i] == current_char:
                current_count += 1
            else:
                satisfies_pattern = True
                for constraint in pattern_constraints:
                    if not constraint(current_char, current_count):
                        satisfies_pattern = False
                        break
                
                if satisfies_pattern:
                    result.append((current_char, current_count))
                
                current_char = self.string[i]
                current_count = 1
        
        # Check last repetition
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(current_char, current_count):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            result.append((current_char, current_count))
        
        return result
    
    def get_repetitions_with_mathematical_constraints(self, constraint_func):
        """Get repetitions that satisfy custom mathematical constraints."""
        if not self.string:
            return []
        
        result = []
        current_char = self.string[0]
        current_count = 1
        
        for i in range(1, len(self.string)):
            if self.string[i] == current_char:
                current_count += 1
            else:
                if constraint_func(current_char, current_count):
                    result.append((current_char, current_count))
                current_char = self.string[i]
                current_count = 1
        
        # Check last repetition
        if constraint_func(current_char, current_count):
            result.append((current_char, current_count))
        
        return result
    
    def get_repetitions_with_optimization_constraints(self, optimization_func):
        """Get repetitions using custom optimization constraints."""
        if not self.string:
            return []
        
        # Calculate optimization score for each repetition
        all_repetitions = []
        current_char = self.string[0]
        current_count = 1
        
        for i in range(1, len(self.string)):
            if self.string[i] == current_char:
                current_count += 1
            else:
                score = optimization_func(current_char, current_count)
                all_repetitions.append((current_char, current_count, score))
                current_char = self.string[i]
                current_count = 1
        
        # Check last repetition
        score = optimization_func(current_char, current_count)
        all_repetitions.append((current_char, current_count, score))
        
        # Sort by optimization score
        all_repetitions.sort(key=lambda x: x[2], reverse=True)
        
        return [(char, count) for char, count, _ in all_repetitions]
    
    def get_repetitions_with_multiple_constraints(self, constraints_list):
        """Get repetitions that satisfy multiple constraints."""
        if not self.string:
            return []
        
        result = []
        current_char = self.string[0]
        current_count = 1
        
        for i in range(1, len(self.string)):
            if self.string[i] == current_char:
                current_count += 1
            else:
                satisfies_all_constraints = True
                for constraint in constraints_list:
                    if not constraint(current_char, current_count):
                        satisfies_all_constraints = False
                        break
                
                if satisfies_all_constraints:
                    result.append((current_char, current_count))
                
                current_char = self.string[i]
                current_count = 1
        
        # Check last repetition
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(current_char, current_count):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            result.append((current_char, current_count))
        
        return result
    
    def get_repetitions_with_priority_constraints(self, priority_func):
        """Get repetitions with priority-based constraints."""
        if not self.string:
            return []
        
        # Sort repetitions by priority
        all_repetitions = []
        current_char = self.string[0]
        current_count = 1
        
        for i in range(1, len(self.string)):
            if self.string[i] == current_char:
                current_count += 1
            else:
                priority = priority_func(current_char, current_count)
                all_repetitions.append((current_char, current_count, priority))
                current_char = self.string[i]
                current_count = 1
        
        # Check last repetition
        priority = priority_func(current_char, current_count)
        all_repetitions.append((current_char, current_count, priority))
        
        # Sort by priority
        all_repetitions.sort(key=lambda x: x[2], reverse=True)
        
        return [(char, count) for char, count, _ in all_repetitions]
    
    def get_repetitions_with_adaptive_constraints(self, adaptive_func):
        """Get repetitions with adaptive constraints."""
        if not self.string:
            return []
        
        result = []
        current_char = self.string[0]
        current_count = 1
        
        for i in range(1, len(self.string)):
            if self.string[i] == current_char:
                current_count += 1
            else:
                if adaptive_func(current_char, current_count, result):
                    result.append((current_char, current_count))
                current_char = self.string[i]
                current_count = 1
        
        # Check last repetition
        if adaptive_func(current_char, current_count, result):
            result.append((current_char, current_count))
        
        return result
    
    def get_optimal_repetition_strategy(self):
        """Get optimal repetition strategy considering all constraints."""
        strategies = [
            ('length_constraints', self.get_repetitions_with_length_constraints),
            ('character_constraints', self.get_repetitions_with_character_constraints),
            ('pattern_constraints', self.get_repetitions_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_count = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'length_constraints':
                    current_count = len(strategy_func(1, 10))
                elif strategy_name == 'character_constraints':
                    character_constraints = [lambda c, count: count >= 2]
                    current_count = len(strategy_func(character_constraints))
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda c, count: c in 'ABC']
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
    'max_length': 10,
    'forbidden_chars': ['X', 'Y', 'Z'],
    'required_chars': ['A', 'B', 'C'],
    'pattern_constraints': [lambda c, count: count >= 2]
}

string = "AAABBBCCCC"
constrained_repetitions = ConstrainedRepetitions(string, constraints)

print("Length-constrained repetitions:", len(constrained_repetitions.get_repetitions_with_length_constraints(2, 10)))

print("Character-constrained repetitions:", len(constrained_repetitions.get_repetitions_with_character_constraints([lambda c, count: count >= 2])))

print("Pattern-constrained repetitions:", len(constrained_repetitions.get_repetitions_with_pattern_constraints([lambda c, count: c in 'ABC'])))

# Mathematical constraints
def custom_constraint(char, count):
    return count >= 3 and char in 'ABC'

print("Mathematical constraint repetitions:", len(constrained_repetitions.get_repetitions_with_mathematical_constraints(custom_constraint)))

# Range constraints
def range_constraint(char, count):
    return 2 <= count <= 10

range_constraints = [range_constraint]
print("Range-constrained repetitions:", len(constrained_repetitions.get_repetitions_with_length_constraints(2, 10)))

# Multiple constraints
def constraint1(char, count):
    return count >= 2

def constraint2(char, count):
    return char in 'ABC'

constraints_list = [constraint1, constraint2]
print("Multiple constraints repetitions:", len(constrained_repetitions.get_repetitions_with_multiple_constraints(constraints_list)))

# Priority constraints
def priority_func(char, count):
    return count + ord(char) - ord('A')

print("Priority-constrained repetitions:", len(constrained_repetitions.get_repetitions_with_priority_constraints(priority_func)))

# Adaptive constraints
def adaptive_func(char, count, current_result):
    return count >= 2 and len(current_result) < 5

print("Adaptive constraint repetitions:", len(constrained_repetitions.get_repetitions_with_adaptive_constraints(adaptive_func)))

# Optimal strategy
optimal = constrained_repetitions.get_optimal_repetition_strategy()
print(f"Optimal repetition strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Repetitions](https://cses.fi/problemset/task/1069) - Find longest repetition
- [Palindrome Reorder](https://cses.fi/problemset/task/1755) - String manipulation problems
- [Creating Strings](https://cses.fi/problemset/task/1622) - String generation problems

#### **LeetCode Problems**
- [Longest Consecutive Sequence](https://leetcode.com/problems/longest-consecutive-sequence/) - Find longest consecutive sequence
- [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/) - Find longest substring without repeats
- [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) - Find longest palindrome
- [Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) - Find longest common prefix

#### **Problem Categories**
- **String Processing**: Consecutive character counting, string analysis, pattern recognition
- **Linear Scanning**: Efficient string traversal, consecutive element counting, maximum finding
- **String Analysis**: Character frequency, string patterns, consecutive sequences
- **Algorithm Design**: Linear algorithms, string optimization, pattern matching

## 📚 Learning Points

1. **String Analysis**: Essential for understanding consecutive character problems
2. **Linear Scanning**: Key technique for efficient string processing
3. **Consecutive Counting**: Important for understanding string patterns
4. **Maximum Finding**: Critical for understanding optimization problems
5. **String Processing**: Foundation for many string algorithms
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Repetitions problem demonstrates fundamental string analysis concepts for finding consecutive character patterns. We explored three approaches:

1. **Brute Force with Nested Loops**: O(n³) time complexity using nested loops to check all substrings, inefficient for large strings
2. **Simple Linear Scanning**: O(n) time complexity using linear scanning to count consecutive characters, better approach for string analysis problems
3. **Optimized Linear Scanning**: O(n) time complexity with optimized linear scanning, optimal approach for consecutive character counting

The key insights include understanding string analysis principles, using linear scanning for efficient consecutive character counting, and applying algorithm optimization techniques for optimal performance. This problem serves as an excellent introduction to string analysis and consecutive character counting algorithms.
