---
layout: simple
title: "String Reorder"
permalink: /problem_soulutions/introductory_problems/string_reorder_analysis
---

# String Reorder

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand lexicographic ordering and string sorting concepts
- Apply sorting algorithms to find lexicographically smallest string arrangements
- Implement efficient string sorting algorithms with proper lexicographic ordering
- Optimize string sorting using character frequency counting and lexicographic ordering
- Handle edge cases in string sorting (duplicate characters, large strings, lexicographic ordering)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: String sorting, lexicographic ordering, character frequency counting, string arrangement
- **Data Structures**: String manipulation, character frequency tracking, sorting data structures, lexicographic ordering
- **Mathematical Concepts**: Lexicographic ordering, string mathematics, sorting theory, character frequency analysis
- **Programming Skills**: String sorting, character frequency counting, lexicographic ordering, algorithm implementation
- **Related Problems**: String problems, Sorting problems, Lexicographic ordering, Character frequency

## Problem Description

**Problem**: Given a string, find the lexicographically smallest string that can be obtained by reordering its characters.

**Input**: A string s (1 ≤ |s| ≤ 10⁶)

**Output**: The lexicographically smallest string that can be obtained by reordering the characters of s.

**Constraints**:
- 1 ≤ |s| ≤ 10⁶
- String contains only uppercase letters A-Z
- Find lexicographically smallest arrangement
- Handle duplicate characters correctly
- Preserve all original characters

**Example**:
```
Input: "CAB"

Output: "ABC"

Explanation: By reordering the characters, we can get "ABC", "ACB", "BAC", "BCA", "CAB", "CBA". 
The lexicographically smallest is "ABC".
```

## Visual Example

### Input and Character Analysis
```
Input: s = "CAB"

Character frequency:
A: 1 occurrence
B: 1 occurrence
C: 1 occurrence

ASCII values:
A = 65, B = 66, C = 67

Lexicographic order: A < B < C
```

### Lexicographic Ordering Process
```
For string "CAB":

All possible arrangements:
1. ABC ← lexicographically smallest
2. ACB
3. BAC
4. BCA
5. CAB (original)
6. CBA

Lexicographic comparison:
- Compare characters from left to right
- First differing character determines order
- A < B < C in ASCII order
```

### Character Frequency Construction
```
Frequency counting approach:
For "CAB":

Step 1: Count frequencies
freq[A] = 1, freq[B] = 1, freq[C] = 1

Step 2: Construct result
result = ""
for i in range(26):
    result += chr(ord('A') + i) * freq[i]

Result: "A" + "B" + "C" = "ABC"
```

### Key Insight
The solution works by:
1. Counting frequency of each character
2. Constructing result by placing characters in lexicographic order
3. Repeating each character according to its frequency
4. Time complexity: O(n) for counting and construction
5. Space complexity: O(1) for frequency array

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Generate All Permutations (Inefficient)

**Key Insights from Permutation Generation Solution:**
- Generate all possible character arrangements
- Find the lexicographically smallest among all permutations
- Simple but computationally expensive approach
- Not suitable for large strings due to factorial growth

**Algorithm:**
1. Generate all possible permutations of the string
2. Find the lexicographically smallest permutation
3. Return the result

**Visual Example:**
```
Permutation generation: Generate all arrangements
For string "CAB":

All permutations:
ABC, ACB, BAC, BCA, CAB, CBA

Find minimum: "ABC"
```

**Implementation:**
```python
from itertools import permutations

def string_reorder_permutations(s):
    # Generate all permutations
    perms = [''.join(p) for p in permutations(s)]
    
    # Find lexicographically smallest
    return min(perms)

def solve_string_reorder_permutations():
    s = input().strip()
    result = string_reorder_permutations(s)
    print(result)
```

**Time Complexity:** O(n! × n) for generating all permutations
**Space Complexity:** O(n! × n) for storing all permutations

**Why it's inefficient:**
- O(n! × n) time complexity grows factorially
- Not suitable for competitive programming with n up to 10⁶
- Memory-intensive for large strings
- Poor performance with exponential growth

### Approach 2: Simple Sorting (Better)

**Key Insights from Sorting Solution:**
- Sort characters directly to get lexicographically smallest arrangement
- More efficient than permutation generation
- Standard method for lexicographic ordering
- Can handle large strings efficiently

**Algorithm:**
1. Convert string to list of characters
2. Sort the characters in ascending order
3. Join back to form the result string

**Visual Example:**
```
Simple sorting: Sort characters directly
For string "CAB":

Step 1: Convert to list → ['C', 'A', 'B']
Step 2: Sort → ['A', 'B', 'C']
Step 3: Join → "ABC"
```

**Implementation:**
```python
def string_reorder_sorting(s):
    # Sort the string directly
    return ''.join(sorted(s))

def solve_string_reorder_sorting():
    s = input().strip()
    result = string_reorder_sorting(s)
    print(result)
```

**Time Complexity:** O(n log n) for sorting
**Space Complexity:** O(n) for temporary list

**Why it's better:**
- O(n log n) time complexity is much better than O(n!)
- Uses efficient sorting algorithms
- Suitable for competitive programming
- Handles large strings efficiently

### Approach 3: Character Frequency Counting (Optimal)

**Key Insights from Frequency Counting Solution:**
- Count frequency of each character
- Construct result by placing characters in lexicographic order
- Most efficient approach for this problem
- Standard method in competitive programming

**Algorithm:**
1. Count frequency of each character using array
2. Iterate through characters in lexicographic order
3. Append each character according to its frequency
4. Construct the final result

**Visual Example:**
```
Frequency counting: Count and construct
For string "CAB":

Step 1: Count frequencies
freq[A] = 1, freq[B] = 1, freq[C] = 1

Step 2: Construct result
result = ""
for i in range(26):
    result += chr(ord('A') + i) * freq[i]

Result: "A" + "B" + "C" = "ABC"
```

**Implementation:**
```python
def string_reorder_optimal(s):
    # Count character frequencies
    freq = [0] * 26
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    # Construct lexicographically smallest string
    result = ""
    for i in range(26):
        result += chr(ord('A') + i) * freq[i]
    
    return result

def solve_string_reorder():
    s = input().strip()
    result = string_reorder_optimal(s)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_string_reorder()
```

**Time Complexity:** O(n) for counting and construction
**Space Complexity:** O(1) for frequency array

**Why it's optimal:**
- O(n) time complexity is optimal for this problem
- Uses constant space for frequency counting
- Most efficient approach for competitive programming
- Handles all cases correctly

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Lexicographically Largest String
**Problem**: Find the lexicographically largest string that can be obtained by reordering.

**Link**: [CSES Problem Set - Lexicographically Largest String](https://cses.fi/problemset/task/lexicographically_largest_string)

```python
def lexicographically_largest(s):
    # Count character frequencies
    freq = [0] * 26
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    # Construct lexicographically largest string
    result = ""
    for i in range(25, -1, -1):  # Reverse order
        result += chr(ord('A') + i) * freq[i]
    
    return result
```

### Variation 2: String Reorder with Custom Order
**Problem**: Reorder string according to a custom character ordering.

**Link**: [CSES Problem Set - Custom String Reorder](https://cses.fi/problemset/task/custom_string_reorder)

```python
def custom_string_reorder(s, custom_order):
    # Count character frequencies
    freq = [0] * 26
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    # Construct result according to custom order
    result = ""
    for c in custom_order:
        result += c * freq[ord(c) - ord('A')]
    
    return result
```

### Variation 3: String Reorder with Constraints
**Problem**: Reorder string while satisfying certain constraints.

**Link**: [CSES Problem Set - Constrained String Reorder](https://cses.fi/problemset/task/constrained_string_reorder)

```python
def constrained_string_reorder(s, constraints):
    # Count character frequencies
    freq = [0] * 26
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    # Apply constraints and construct result
    result = ""
    for i in range(26):
        char = chr(ord('A') + i)
        if constraints(char, freq[i]):
            result += char * freq[i]
    
    return result
```

## Problem Variations

### **Variation 1: String Reorder with Dynamic Updates**
**Problem**: Handle dynamic string updates (add/remove/update characters) while maintaining optimal string reordering efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic string management.

```python
from collections import defaultdict, Counter

class DynamicStringReorder:
    def __init__(self, string=""):
        self.string = string
        self.char_count = Counter(string)
        self._update_reorder_info()
    
    def _update_reorder_info(self):
        """Update reorder feasibility information."""
        self.total_chars = len(self.string)
        self.unique_chars = len(self.char_count)
        self.reorder_feasibility = self._calculate_reorder_feasibility()
    
    def _calculate_reorder_feasibility(self):
        """Calculate string reorder feasibility."""
        if not self.string:
            return 0
        
        # Check if string can be reordered optimally
        odd_count = sum(1 for count in self.char_count.values() if count % 2 == 1)
        return 1.0 if odd_count <= 1 else 0.0
    
    def add_character(self, char, position=None):
        """Add character to the string."""
        if position is None:
            self.string += char
        else:
            self.string = self.string[:position] + char + self.string[position:]
        
        self.char_count[char] += 1
        self._update_reorder_info()
    
    def remove_character(self, position):
        """Remove character from the string."""
        if 0 <= position < len(self.string):
            char = self.string[position]
            self.string = self.string[:position] + self.string[position+1:]
            self.char_count[char] -= 1
            if self.char_count[char] == 0:
                del self.char_count[char]
            self._update_reorder_info()
    
    def update_character(self, position, new_char):
        """Update character in the string."""
        if 0 <= position < len(self.string):
            old_char = self.string[position]
            self.string = self.string[:position] + new_char + self.string[position+1:]
            
            self.char_count[old_char] -= 1
            if self.char_count[old_char] == 0:
                del self.char_count[old_char]
            
            self.char_count[new_char] += 1
            self._update_reorder_info()
    
    def get_optimal_reorder(self):
        """Get optimal string reordering."""
        if not self.string:
            return ""
        
        # Create optimal reordering
        result = []
        odd_char = None
        
        # Add characters with even counts
        for char, count in sorted(self.char_count.items()):
            if count % 2 == 0:
                result.extend([char] * (count // 2))
            else:
                result.extend([char] * (count // 2))
                odd_char = char
        
        # Create palindrome
        if odd_char:
            return ''.join(result) + odd_char + ''.join(reversed(result))
        else:
            return ''.join(result) + ''.join(reversed(result))
    
    def get_reorder_with_constraints(self, constraint_func):
        """Get reordering that satisfies custom constraints."""
        if not self.string:
            return ""
        
        if constraint_func(self.string, self.char_count):
            return self.get_optimal_reorder()
        else:
            return self.string  # Return original if constraints not met
    
    def get_reorder_in_range(self, min_length, max_length):
        """Get reordering within specified length range."""
        if not self.string:
            return ""
        
        if min_length <= len(self.string) <= max_length:
            return self.get_optimal_reorder()
        else:
            return self.string  # Return original if out of range
    
    def get_reorder_with_pattern(self, pattern_func):
        """Get reordering matching specified pattern."""
        if not self.string:
            return ""
        
        if pattern_func(self.string, self.char_count):
            return self.get_optimal_reorder()
        else:
            return self.string  # Return original if pattern not matched
    
    def get_string_statistics(self):
        """Get statistics about the string."""
        if not self.string:
            return {
                'total_chars': 0,
                'unique_chars': 0,
                'reorder_feasibility': 0,
                'char_distribution': {}
            }
        
        return {
            'total_chars': self.total_chars,
            'unique_chars': self.unique_chars,
            'reorder_feasibility': self.reorder_feasibility,
            'char_distribution': dict(self.char_count)
        }
    
    def get_reorder_patterns(self):
        """Get patterns in string reordering."""
        patterns = {
            'palindrome_possible': 0,
            'single_odd_char': 0,
            'multiple_odd_chars': 0,
            'balanced_chars': 0
        }
        
        if not self.string:
            return patterns
        
        odd_count = sum(1 for count in self.char_count.values() if count % 2 == 1)
        
        # Check if palindrome is possible
        if odd_count <= 1:
            patterns['palindrome_possible'] = 1
        
        # Check for single odd character
        if odd_count == 1:
            patterns['single_odd_char'] = 1
        
        # Check for multiple odd characters
        if odd_count > 1:
            patterns['multiple_odd_chars'] = 1
        
        # Check for balanced characters
        if all(count % 2 == 0 for count in self.char_count.values()):
            patterns['balanced_chars'] = 1
        
        return patterns
    
    def get_optimal_reorder_strategy(self):
        """Get optimal strategy for string reordering."""
        if not self.string:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'reorder_feasibility': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = self.unique_chars / self.total_chars if self.total_chars > 0 else 0
        
        # Calculate reorder feasibility
        reorder_feasibility = self.reorder_feasibility
        
        # Determine recommended strategy
        if self.reorder_feasibility == 1.0:
            recommended_strategy = 'palindrome_reorder'
        elif self.unique_chars == 1:
            recommended_strategy = 'single_char_optimization'
        else:
            recommended_strategy = 'character_balance_reorder'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'reorder_feasibility': reorder_feasibility
        }

# Example usage
string = "aabbcc"
dynamic_string_reorder = DynamicStringReorder(string)
print(f"Reorder feasibility: {dynamic_string_reorder.reorder_feasibility}")
print(f"Optimal reorder: {dynamic_string_reorder.get_optimal_reorder()}")

# Add character
dynamic_string_reorder.add_character('d')
print(f"After adding d: {dynamic_string_reorder.get_optimal_reorder()}")

# Remove character
dynamic_string_reorder.remove_character(0)
print(f"After removing first character: {dynamic_string_reorder.get_optimal_reorder()}")

# Update character
dynamic_string_reorder.update_character(0, 'e')
print(f"After updating first character to e: {dynamic_string_reorder.get_optimal_reorder()}")

# Get reorder with constraints
def constraint_func(string, char_count):
    return len(string) <= 10

print(f"Reorder with constraints: {dynamic_string_reorder.get_reorder_with_constraints(constraint_func)}")

# Get reorder in range
print(f"Reorder in range 5-15: {dynamic_string_reorder.get_reorder_in_range(5, 15)}")

# Get reorder with pattern
def pattern_func(string, char_count):
    return len(char_count) <= 5

print(f"Reorder with pattern: {dynamic_string_reorder.get_reorder_with_pattern(pattern_func)}")

# Get statistics
print(f"Statistics: {dynamic_string_reorder.get_string_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_string_reorder.get_reorder_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_string_reorder.get_optimal_reorder_strategy()}")
```

### **Variation 2: String Reorder with Different Operations**
**Problem**: Handle different types of string reordering operations (weighted characters, priority-based selection, advanced string analysis).

**Approach**: Use advanced data structures for efficient different types of string reordering operations.

```python
class AdvancedStringReorder:
    def __init__(self, string="", weights=None, priorities=None):
        self.string = string
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.char_count = Counter(string)
        self._update_reorder_info()
    
    def _update_reorder_info(self):
        """Update reorder feasibility information."""
        self.total_chars = len(self.string)
        self.unique_chars = len(self.char_count)
        self.reorder_feasibility = self._calculate_reorder_feasibility()
    
    def _calculate_reorder_feasibility(self):
        """Calculate string reorder feasibility."""
        if not self.string:
            return 0
        
        # Check if string can be reordered optimally
        odd_count = sum(1 for count in self.char_count.values() if count % 2 == 1)
        return 1.0 if odd_count <= 1 else 0.0
    
    def get_weighted_reorder(self):
        """Get reordering with weights and priorities applied."""
        if not self.string:
            return ""
        
        # Create weighted reordering
        weighted_chars = []
        for char, count in self.char_count.items():
            weight = self.weights.get(char, 1)
            priority = self.priorities.get(char, 1)
            weighted_score = count * weight * priority
            weighted_chars.append((char, count, weighted_score))
        
        # Sort by weighted score
        weighted_chars.sort(key=lambda x: x[2], reverse=True)
        
        # Create reordered string
        result = []
        odd_char = None
        
        for char, count, _ in weighted_chars:
            if count % 2 == 0:
                result.extend([char] * (count // 2))
            else:
                result.extend([char] * (count // 2))
                odd_char = char
        
        # Create palindrome
        if odd_char:
            return ''.join(result) + odd_char + ''.join(reversed(result))
        else:
            return ''.join(result) + ''.join(reversed(result))
    
    def get_reorder_with_priority(self, priority_func):
        """Get reordering considering priority."""
        if not self.string:
            return ""
        
        # Create priority-based reordering
        priority_chars = []
        for char, count in self.char_count.items():
            priority = priority_func(char, count, self.weights, self.priorities)
            priority_chars.append((char, count, priority))
        
        # Sort by priority
        priority_chars.sort(key=lambda x: x[2], reverse=True)
        
        # Create reordered string
        result = []
        odd_char = None
        
        for char, count, _ in priority_chars:
            if count % 2 == 0:
                result.extend([char] * (count // 2))
            else:
                result.extend([char] * (count // 2))
                odd_char = char
        
        # Create palindrome
        if odd_char:
            return ''.join(result) + odd_char + ''.join(reversed(result))
        else:
            return ''.join(result) + ''.join(reversed(result))
    
    def get_reorder_with_optimization(self, optimization_func):
        """Get reordering using custom optimization function."""
        if not self.string:
            return ""
        
        # Create optimization-based reordering
        optimized_chars = []
        for char, count in self.char_count.items():
            score = optimization_func(char, count, self.weights, self.priorities)
            optimized_chars.append((char, count, score))
        
        # Sort by optimization score
        optimized_chars.sort(key=lambda x: x[2], reverse=True)
        
        # Create reordered string
        result = []
        odd_char = None
        
        for char, count, _ in optimized_chars:
            if count % 2 == 0:
                result.extend([char] * (count // 2))
            else:
                result.extend([char] * (count // 2))
                odd_char = char
        
        # Create palindrome
        if odd_char:
            return ''.join(result) + odd_char + ''.join(reversed(result))
        else:
            return ''.join(result) + ''.join(reversed(result))
    
    def get_reorder_with_constraints(self, constraint_func):
        """Get reordering that satisfies custom constraints."""
        if not self.string:
            return ""
        
        if constraint_func(self.string, self.char_count, self.weights, self.priorities):
            return self.get_weighted_reorder()
        else:
            return self.string  # Return original if constraints not met
    
    def get_reorder_with_multiple_criteria(self, criteria_list):
        """Get reordering that satisfies multiple criteria."""
        if not self.string:
            return ""
        
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(self.string, self.char_count, self.weights, self.priorities):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            return self.get_weighted_reorder()
        else:
            return self.string  # Return original if criteria not met
    
    def get_reorder_with_alternatives(self, alternatives):
        """Get reordering considering alternative weights/priorities."""
        result = []
        
        # Check original reordering
        original_reorder = self.get_weighted_reorder()
        result.append((original_reorder, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedStringReorder(self.string, alt_weights, alt_priorities)
            temp_reorder = temp_instance.get_weighted_reorder()
            result.append((temp_reorder, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_reorder_with_adaptive_criteria(self, adaptive_func):
        """Get reordering using adaptive criteria."""
        if not self.string:
            return ""
        
        if adaptive_func(self.string, self.char_count, self.weights, self.priorities, []):
            return self.get_weighted_reorder()
        else:
            return self.string  # Return original if adaptive criteria not met
    
    def get_reorder_optimization(self):
        """Get optimal reordering configuration."""
        strategies = [
            ('weighted_reorder', lambda: len(self.get_weighted_reorder())),
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
string = "aabbcc"
weights = {char: ord(char) - ord('a') + 1 for char in string}  # Weight based on character position
priorities = {char: string.count(char) for char in string}  # Priority based on frequency
advanced_string_reorder = AdvancedStringReorder(string, weights, priorities)

print(f"Weighted reorder: {advanced_string_reorder.get_weighted_reorder()}")

# Get reorder with priority
def priority_func(char, count, weights, priorities):
    return count * weights.get(char, 1) + priorities.get(char, 1)

print(f"Reorder with priority: {advanced_string_reorder.get_reorder_with_priority(priority_func)}")

# Get reorder with optimization
def optimization_func(char, count, weights, priorities):
    return count * weights.get(char, 1) * priorities.get(char, 1)

print(f"Reorder with optimization: {advanced_string_reorder.get_reorder_with_optimization(optimization_func)}")

# Get reorder with constraints
def constraint_func(string, char_count, weights, priorities):
    return len(string) <= 10 and len(char_count) <= 5

print(f"Reorder with constraints: {advanced_string_reorder.get_reorder_with_constraints(constraint_func)}")

# Get reorder with multiple criteria
def criterion1(string, char_count, weights, priorities):
    return len(string) <= 10

def criterion2(string, char_count, weights, priorities):
    return len(char_count) <= 5

criteria_list = [criterion1, criterion2]
print(f"Reorder with multiple criteria: {advanced_string_reorder.get_reorder_with_multiple_criteria(criteria_list)}")

# Get reorder with alternatives
alternatives = [({char: 1 for char in string}, {char: 1 for char in string}), ({char: len(char) for char in string}, {char: char.count('a') + 1 for char in string})]
print(f"Reorder with alternatives: {len(advanced_string_reorder.get_reorder_with_alternatives(alternatives))}")

# Get reorder with adaptive criteria
def adaptive_func(string, char_count, weights, priorities, current_result):
    return len(string) <= 10 and len(current_result) < 3

print(f"Reorder with adaptive criteria: {advanced_string_reorder.get_reorder_with_adaptive_criteria(adaptive_func)}")

# Get reorder optimization
print(f"Reorder optimization: {advanced_string_reorder.get_reorder_optimization()}")
```

### **Variation 3: String Reorder with Constraints**
**Problem**: Handle string reordering with additional constraints (length limits, character constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedStringReorder:
    def __init__(self, string="", constraints=None):
        self.string = string
        self.constraints = constraints or {}
        self.char_count = Counter(string)
        self._update_reorder_info()
    
    def _update_reorder_info(self):
        """Update reorder feasibility information."""
        self.total_chars = len(self.string)
        self.unique_chars = len(self.char_count)
        self.reorder_feasibility = self._calculate_reorder_feasibility()
    
    def _calculate_reorder_feasibility(self):
        """Calculate string reorder feasibility."""
        if not self.string:
            return 0
        
        # Check if string can be reordered optimally
        odd_count = sum(1 for count in self.char_count.values() if count % 2 == 1)
        return 1.0 if odd_count <= 1 else 0.0
    
    def _is_valid_reorder(self, reordered_string):
        """Check if reordered string is valid considering constraints."""
        # Length constraints
        if 'min_length' in self.constraints:
            if len(reordered_string) < self.constraints['min_length']:
                return False
        
        if 'max_length' in self.constraints:
            if len(reordered_string) > self.constraints['max_length']:
                return False
        
        # Character constraints
        if 'forbidden_chars' in self.constraints:
            for char in reordered_string:
                if char in self.constraints['forbidden_chars']:
                    return False
        
        if 'required_chars' in self.constraints:
            for char in self.constraints['required_chars']:
                if char not in reordered_string:
                    return False
        
        # Pattern constraints
        if 'pattern_constraints' in self.constraints:
            for constraint in self.constraints['pattern_constraints']:
                if not constraint(reordered_string):
                    return False
        
        return True
    
    def get_reorder_with_length_constraints(self, min_length, max_length):
        """Get reordering considering length constraints."""
        if not self.string:
            return ""
        
        if min_length <= len(self.string) <= max_length:
            return self.get_optimal_reorder()
        else:
            return self.string  # Return original if out of range
    
    def get_reorder_with_character_constraints(self, character_constraints):
        """Get reordering considering character constraints."""
        if not self.string:
            return ""
        
        satisfies_constraints = True
        for constraint in character_constraints:
            if not constraint(self.string, self.char_count):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            return self.get_optimal_reorder()
        else:
            return self.string  # Return original if constraints not met
    
    def get_reorder_with_pattern_constraints(self, pattern_constraints):
        """Get reordering considering pattern constraints."""
        if not self.string:
            return ""
        
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(self.string, self.char_count):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            return self.get_optimal_reorder()
        else:
            return self.string  # Return original if pattern not matched
    
    def get_reorder_with_mathematical_constraints(self, constraint_func):
        """Get reordering that satisfies custom mathematical constraints."""
        if not self.string:
            return ""
        
        if constraint_func(self.string, self.char_count):
            return self.get_optimal_reorder()
        else:
            return self.string  # Return original if constraints not met
    
    def get_reorder_with_optimization_constraints(self, optimization_func):
        """Get reordering using custom optimization constraints."""
        if not self.string:
            return ""
        
        # Calculate optimization score for reordering
        score = optimization_func(self.string, self.char_count)
        
        if score > 0:
            return self.get_optimal_reorder()
        else:
            return self.string  # Return original if optimization not beneficial
    
    def get_reorder_with_multiple_constraints(self, constraints_list):
        """Get reordering that satisfies multiple constraints."""
        if not self.string:
            return ""
        
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(self.string, self.char_count):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            return self.get_optimal_reorder()
        else:
            return self.string  # Return original if constraints not met
    
    def get_reorder_with_priority_constraints(self, priority_func):
        """Get reordering with priority-based constraints."""
        if not self.string:
            return ""
        
        # Calculate priority for reordering
        priority = priority_func(self.string, self.char_count)
        
        if priority > 0:
            return self.get_optimal_reorder()
        else:
            return self.string  # Return original if priority not met
    
    def get_reorder_with_adaptive_constraints(self, adaptive_func):
        """Get reordering with adaptive constraints."""
        if not self.string:
            return ""
        
        if adaptive_func(self.string, self.char_count, []):
            return self.get_optimal_reorder()
        else:
            return self.string  # Return original if adaptive constraints not met
    
    def get_optimal_reorder(self):
        """Get optimal string reordering."""
        if not self.string:
            return ""
        
        # Create optimal reordering
        result = []
        odd_char = None
        
        # Add characters with even counts
        for char, count in sorted(self.char_count.items()):
            if count % 2 == 0:
                result.extend([char] * (count // 2))
            else:
                result.extend([char] * (count // 2))
                odd_char = char
        
        # Create palindrome
        if odd_char:
            return ''.join(result) + odd_char + ''.join(reversed(result))
        else:
            return ''.join(result) + ''.join(reversed(result))
    
    def get_optimal_reorder_strategy(self):
        """Get optimal reordering strategy considering all constraints."""
        strategies = [
            ('length_constraints', self.get_reorder_with_length_constraints),
            ('character_constraints', self.get_reorder_with_character_constraints),
            ('pattern_constraints', self.get_reorder_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_score = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'length_constraints':
                    result = strategy_func(1, 100)
                elif strategy_name == 'character_constraints':
                    character_constraints = [lambda s, cc: len(s) <= 10]
                    result = strategy_func(character_constraints)
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda s, cc: len(cc) <= 5]
                    result = strategy_func(pattern_constraints)
                
                if len(result) > best_score:
                    best_score = len(result)
                    best_strategy = (strategy_name, result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'min_length': 5,
    'max_length': 15,
    'forbidden_chars': ['x', 'y', 'z'],
    'required_chars': ['a', 'b'],
    'pattern_constraints': [lambda s: len(s) <= 10]
}

string = "aabbcc"
constrained_string_reorder = ConstrainedStringReorder(string, constraints)

print("Length-constrained reorder:", constrained_string_reorder.get_reorder_with_length_constraints(5, 15))

print("Character-constrained reorder:", constrained_string_reorder.get_reorder_with_character_constraints([lambda s, cc: len(s) <= 10]))

print("Pattern-constrained reorder:", constrained_string_reorder.get_reorder_with_pattern_constraints([lambda s, cc: len(cc) <= 5]))

# Mathematical constraints
def custom_constraint(string, char_count):
    return len(string) <= 10 and len(char_count) <= 5

print("Mathematical constraint reorder:", constrained_string_reorder.get_reorder_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(string, char_count):
    return 5 <= len(string) <= 15

range_constraints = [range_constraint]
print("Range-constrained reorder:", constrained_string_reorder.get_reorder_with_length_constraints(5, 15))

# Multiple constraints
def constraint1(string, char_count):
    return len(string) <= 10

def constraint2(string, char_count):
    return len(char_count) <= 5

constraints_list = [constraint1, constraint2]
print("Multiple constraints reorder:", constrained_string_reorder.get_reorder_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(string, char_count):
    return len(string) + len(char_count)

print("Priority-constrained reorder:", constrained_string_reorder.get_reorder_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(string, char_count, current_result):
    return len(string) <= 10 and len(current_result) < 3

print("Adaptive constraint reorder:", constrained_string_reorder.get_reorder_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_string_reorder.get_optimal_reorder_strategy()
print(f"Optimal reorder strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [String Reorder](https://cses.fi/problemset/task/1754) - Basic string reordering
- [Creating Strings](https://cses.fi/problemset/task/1622) - String generation problems
- [Palindrome Reorder](https://cses.fi/problemset/task/1755) - String manipulation problems

#### **LeetCode Problems**
- [Custom Sort String](https://leetcode.com/problems/custom-sort-string/) - Sort string according to custom order
- [Sort Characters By Frequency](https://leetcode.com/problems/sort-characters-by-frequency/) - Sort characters by frequency
- [Reorder Data in Log Files](https://leetcode.com/problems/reorder-data-in-log-files/) - Reorder log entries
- [Sort Array By Parity](https://leetcode.com/problems/sort-array-by-parity/) - Sort array by parity

#### **Problem Categories**
- **String Manipulation**: Character frequency counting, string construction, lexicographic ordering
- **Sorting**: Character sorting, frequency-based sorting, custom ordering
- **Lexicographic Ordering**: String comparison, alphabetical ordering, dictionary ordering
- **Algorithm Design**: String algorithms, sorting algorithms, frequency analysis

## 📚 Learning Points

1. **Lexicographic Ordering**: Essential for understanding string comparison
2. **Character Frequency Counting**: Key technique for efficient string manipulation
3. **Sorting Algorithms**: Important for understanding string ordering
4. **String Construction**: Critical for understanding string building
5. **Algorithm Optimization**: Foundation for many string algorithms
6. **Mathematical Analysis**: Critical for understanding string properties

## 📝 Summary

The String Reorder problem demonstrates lexicographic ordering and character frequency counting concepts for efficient string manipulation. We explored three approaches:

1. **Generate All Permutations**: O(n! × n) time complexity using permutation generation, inefficient for large strings
2. **Simple Sorting**: O(n log n) time complexity using character sorting, better approach for string ordering
3. **Character Frequency Counting**: O(n) time complexity using frequency counting and construction, optimal approach for competitive programming

The key insights include understanding lexicographic ordering principles, using character frequency counting for efficient construction, and applying optimization techniques for optimal performance. This problem serves as an excellent introduction to string algorithms and lexicographic ordering in competitive programming.
