---
layout: simple
title: "Palindrome Reorder"
permalink: /problem_soulutions/introductory_problems/palindrome_reorder_analysis
---

# Palindrome Reorder

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand palindrome properties and string rearrangement problems
- Apply character frequency analysis to determine palindrome feasibility
- Implement efficient palindrome construction algorithms with proper character arrangement
- Optimize palindrome construction using frequency analysis and string manipulation
- Handle edge cases in palindrome problems (impossible palindromes, single characters, large strings)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Palindrome properties, character frequency analysis, string rearrangement, string construction
- **Data Structures**: Character frequency tracking, string manipulation, palindrome construction, character counting
- **Mathematical Concepts**: Palindrome theory, character frequency analysis, string mathematics, combinatorics
- **Programming Skills**: String manipulation, character frequency counting, palindrome construction, algorithm implementation
- **Related Problems**: String problems, Palindrome problems, Character frequency, String manipulation

## Problem Description

**Problem**: Given a string, determine if it can be rearranged to form a palindrome. If possible, output one such palindrome; otherwise, output "NO SOLUTION".

**Input**: A string s (1 ≤ |s| ≤ 10⁶)

**Output**: A palindrome if possible, or "NO SOLUTION".

**Constraints**:
- 1 ≤ |s| ≤ 10⁶
- String contains only uppercase letters A-Z
- Must determine palindrome feasibility
- If possible, construct one palindrome
- If impossible, output "NO SOLUTION"

**Example**:
```
Input: AAAACACBA

Output: AAACBCAAA

Explanation: The string can be rearranged to form the palindrome "AAACBCAAA".
```

## Visual Example

### Input and Character Frequency Analysis
```
Input: s = "AAAACACBA"

Character frequency analysis:
A: 5 occurrences
B: 1 occurrence  
C: 2 occurrences

Frequency pattern: [5, 1, 2, 0, 0, ..., 0]
Odd frequencies: A=5 (odd), B=1 (odd), C=2 (even)
Odd count: 2 > 1 → Cannot form palindrome
```

### Palindrome Feasibility Check
```
For string "AAAACACBA":

Step 1: Count character frequencies
A: 5, B: 1, C: 2

Step 2: Check odd frequencies
- A has 5 (odd)
- B has 1 (odd)  
- C has 2 (even)
- Total odd frequencies: 2

Step 3: Palindrome rule
- Even length: all frequencies must be even
- Odd length: exactly one frequency can be odd
- Current: 2 odd frequencies > 1 → Impossible
```

### Palindrome Construction Process
```
For string "AAAACACBA" (impossible case):
Result: "NO SOLUTION"

For string "AAAACACB" (possible case):
Character frequencies: A=4, B=1, C=2
Odd frequencies: B=1 (only one odd) → Possible

Construction:
1. First half: "AAC" (half of each even frequency)
2. Middle: "B" (the odd frequency character)
3. Second half: "CAA" (reverse of first half)
4. Result: "AAC" + "B" + "CAA" = "AACBCAA"
```

### Key Insight
The solution works by:
1. Counting character frequencies in the string
2. Checking palindrome feasibility using frequency rules
3. Constructing palindrome using frequency analysis
4. Time complexity: O(n) for frequency counting and construction
5. Space complexity: O(1) for frequency array (26 characters)

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Permutation Check (Inefficient)

**Key Insights from Brute Force Solution:**
- Generate all permutations and check if any is a palindrome
- Simple but computationally expensive approach
- Not suitable for large strings due to factorial growth
- Straightforward implementation but poor scalability

**Algorithm:**
1. Generate all possible permutations of the string
2. Check each permutation to see if it's a palindrome
3. Return the first palindrome found or "NO SOLUTION"
4. Handle edge cases correctly

**Visual Example:**
```
Brute force: Check all permutations
For string "AAB":

All permutations: ["AAB", "ABA", "BAA"]
Check each:
- "AAB" → Not palindrome (AAB ≠ BAA)
- "ABA" → Palindrome (ABA = ABA) ✓
- "BAA" → Not palindrome (BAA ≠ AAB)

Result: "ABA"
```

**Implementation:**
```python
from itertools import permutations

def palindrome_reorder_brute_force(s):
    # Generate all permutations
    perms = set(permutations(s))
    
    for perm in perms:
        perm_str = ''.join(perm)
        if perm_str == perm_str[::-1]:  # Check if palindrome
            return perm_str
    
    return "NO SOLUTION"

def solve_palindrome_reorder_brute_force():
    s = input().strip()
    result = palindrome_reorder_brute_force(s)
    print(result)
```

**Time Complexity:** O(n! × n) for generating and checking all permutations
**Space Complexity:** O(n! × n) for storing all permutations

**Why it's inefficient:**
- O(n! × n) time complexity grows factorially
- Not suitable for competitive programming with n up to 10⁶
- Memory-intensive for large strings
- Poor performance with factorial growth

### Approach 2: Character Frequency Analysis (Better)

**Key Insights from Frequency Analysis Solution:**
- Use character frequency counting to determine feasibility
- Much more efficient than brute force approach
- Standard method for palindrome problems
- Can handle larger strings than brute force approach

**Algorithm:**
1. Count frequency of each character in the string
2. Check if palindrome is possible using frequency rules
3. If possible, construct palindrome using frequency analysis
4. Return constructed palindrome or "NO SOLUTION"

**Visual Example:**
```
Frequency analysis: Count and check
For string "AAAACACBA":

Step 1: Count frequencies
A: 5, B: 1, C: 2

Step 2: Check odd frequencies
Odd count: 2 (A=5, B=1)
Since odd count > 1 → Impossible

Result: "NO SOLUTION"
```

**Implementation:**
```python
def palindrome_reorder_frequency(s):
    freq = [0] * 26
    
    # Count character frequencies
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    # Check feasibility
    odd_count = sum(1 for f in freq if f % 2 == 1)
    if odd_count > 1:
        return "NO SOLUTION"
    
    # Construct palindrome
    first_half = ""
    middle = ""
    
    for i in range(26):
        if freq[i] > 0:
            if freq[i] % 2 == 1:
                middle = chr(ord('A') + i)
                freq[i] -= 1
            first_half += chr(ord('A') + i) * (freq[i] // 2)
    
    second_half = first_half[::-1]
    return first_half + middle + second_half

def solve_palindrome_reorder_frequency():
    s = input().strip()
    result = palindrome_reorder_frequency(s)
    print(result)
```

**Time Complexity:** O(n) for frequency counting and construction
**Space Complexity:** O(1) for frequency array

**Why it's better:**
- O(n) time complexity is much better than O(n!)
- Uses frequency analysis for efficient solution
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized Frequency Analysis with Early Termination (Optimal)

**Key Insights from Optimized Solution:**
- Use optimized frequency analysis with early termination
- Most efficient approach for palindrome construction
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Count character frequencies in single pass
2. Check feasibility with early termination
3. Construct palindrome efficiently using frequency analysis
4. Leverage mathematical properties for optimal solution

**Visual Example:**
```
Optimized approach: Early termination
For string "AAAACACBA":

Step 1: Count frequencies with early termination
A: 5, B: 1, C: 2
Odd count: 2 > 1 → Early termination

Result: "NO SOLUTION" (no need to construct)
```

**Implementation:**
```python
def palindrome_reorder_optimized(s):
    freq = [0] * 26
    
    # Count character frequencies
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    # Check feasibility with early termination
    odd_count = 0
    odd_char = -1
    
    for i in range(26):
        if freq[i] % 2 == 1:
            odd_count += 1
            odd_char = i
            if odd_count > 1:
                return "NO SOLUTION"
    
    # Construct palindrome efficiently
    first_half = ""
    middle = ""
    
    for i in range(26):
        if freq[i] > 0:
            if i == odd_char:
                middle = chr(ord('A') + i)
                freq[i] -= 1
            first_half += chr(ord('A') + i) * (freq[i] // 2)
    
    second_half = first_half[::-1]
    return first_half + middle + second_half

def solve_palindrome_reorder():
    s = input().strip()
    result = palindrome_reorder_optimized(s)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_palindrome_reorder()
```

**Time Complexity:** O(n) for frequency counting and construction
**Space Complexity:** O(1) for frequency array

**Why it's optimal:**
- O(n) time complexity is optimal for this problem
- Uses early termination for efficient feasibility check
- Most efficient approach for competitive programming
- Standard method for palindrome construction optimization

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Palindrome with Lowercase Letters
**Problem**: Handle both uppercase and lowercase letters in palindrome construction.

**Link**: [CSES Problem Set - Palindrome with Lowercase](https://cses.fi/problemset/task/palindrome_lowercase)

```python
def palindrome_reorder_lowercase(s):
    freq = [0] * 52  # 26 uppercase + 26 lowercase
    
    for c in s:
        if c.isupper():
            freq[ord(c) - ord('A')] += 1
        else:
            freq[ord(c) - ord('a') + 26] += 1
    
    odd_count = sum(1 for f in freq if f % 2 == 1)
    if odd_count > 1:
        return "NO SOLUTION"
    
    # Construct palindrome with case preservation
    first_half = ""
    middle = ""
    
    for i in range(52):
        if freq[i] > 0:
            char = chr(ord('A') + i) if i < 26 else chr(ord('a') + i - 26)
            if freq[i] % 2 == 1:
                middle = char
                freq[i] -= 1
            first_half += char * (freq[i] // 2)
    
    second_half = first_half[::-1]
    return first_half + middle + second_half
```

### Variation 2: Longest Palindrome Subsequence
**Problem**: Find the longest palindrome that can be formed as a subsequence.

**Link**: [CSES Problem Set - Longest Palindrome Subsequence](https://cses.fi/problemset/task/longest_palindrome_subsequence)

```python
def longest_palindrome_subsequence(s):
    freq = [0] * 26
    
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    # Count pairs and odd characters
    pairs = 0
    odd_chars = 0
    
    for f in freq:
        pairs += f // 2
        if f % 2 == 1:
            odd_chars += 1
    
    # Longest palindrome length
    return pairs * 2 + min(odd_chars, 1)
```

### Variation 3: Minimum Insertions for Palindrome
**Problem**: Find minimum number of insertions needed to make string a palindrome.

**Link**: [CSES Problem Set - Minimum Insertions for Palindrome](https://cses.fi/problemset/task/minimum_insertions_palindrome)

```python
def minimum_insertions_palindrome(s):
    freq = [0] * 26
    
    for c in s:
        freq[ord(c) - ord('A')] += 1
    
    odd_count = sum(1 for f in freq if f % 2 == 1)
    
    # Minimum insertions = max(0, odd_count - 1)
    return max(0, odd_count - 1)
```

## Problem Variations

### **Variation 1: Palindrome Reorder with Dynamic Updates**
**Problem**: Handle dynamic string updates (add/remove/update characters) while maintaining palindrome feasibility efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic palindrome management.

```python
from collections import defaultdict
import itertools

class DynamicPalindromeReorder:
    def __init__(self, s=""):
        self.s = list(s)
        self.char_count = defaultdict(int)
        for char in s:
            self.char_count[char] += 1
        self._update_palindrome_info()
    
    def _update_palindrome_info(self):
        """Update palindrome feasibility information."""
        self.odd_count = 0
        self.even_count = 0
        self.odd_chars = []
        self.even_chars = []
        
        for char, count in self.char_count.items():
            if count % 2 == 1:
                self.odd_count += 1
                self.odd_chars.append(char)
            else:
                self.even_count += 1
                self.even_chars.append(char)
    
    def add_character(self, char):
        """Add character to string."""
        self.s.append(char)
        self.char_count[char] += 1
        self._update_palindrome_info()
    
    def remove_character(self, char):
        """Remove character from string."""
        if char in self.s and self.char_count[char] > 0:
            self.s.remove(char)
            self.char_count[char] -= 1
            if self.char_count[char] == 0:
                del self.char_count[char]
            self._update_palindrome_info()
    
    def update_character(self, old_char, new_char):
        """Update character in string."""
        if old_char in self.s:
            self.remove_character(old_char)
            self.add_character(new_char)
    
    def can_form_palindrome(self):
        """Check if string can form a palindrome."""
        return self.odd_count <= 1
    
    def get_palindrome(self):
        """Get palindrome if possible."""
        if not self.can_form_palindrome():
            return None
        
        # Build palindrome
        result = []
        
        # Add even characters (half of each)
        for char in self.even_chars:
            count = self.char_count[char]
            result.extend([char] * (count // 2))
        
        # Add odd character (if exists)
        if self.odd_chars:
            odd_char = self.odd_chars[0]
            result.extend([odd_char] * self.char_count[odd_char])
        
        # Add even characters (other half, reversed)
        for char in reversed(self.even_chars):
            count = self.char_count[char]
            result.extend([char] * (count // 2))
        
        return ''.join(result)
    
    def get_palindromes_with_constraints(self, constraint_func):
        """Get palindromes that satisfy custom constraints."""
        if not self.can_form_palindrome():
            return []
        
        result = []
        # Generate different palindrome arrangements
        for arrangement in self._generate_palindrome_arrangements():
            if constraint_func(arrangement):
                result.append(arrangement)
        return result
    
    def _generate_palindrome_arrangements(self):
        """Generate different palindrome arrangements."""
        arrangements = []
        
        # Basic palindrome
        basic_palindrome = self.get_palindrome()
        if basic_palindrome:
            arrangements.append(basic_palindrome)
        
        # Try different arrangements of even characters
        if self.even_chars:
            even_permutations = itertools.permutations(self.even_chars)
            for perm in even_permutations:
                arrangement = self._build_palindrome_with_permutation(perm)
                if arrangement:
                    arrangements.append(arrangement)
        
        return arrangements
    
    def _build_palindrome_with_permutation(self, even_perm):
        """Build palindrome with specific even character permutation."""
        result = []
        
        # Add even characters (half of each)
        for char in even_perm:
            count = self.char_count[char]
            result.extend([char] * (count // 2))
        
        # Add odd character (if exists)
        if self.odd_chars:
            odd_char = self.odd_chars[0]
            result.extend([odd_char] * self.char_count[odd_char])
        
        # Add even characters (other half, reversed)
        for char in reversed(even_perm):
            count = self.char_count[char]
            result.extend([char] * (count // 2))
        
        return ''.join(result)
    
    def get_palindromes_in_range(self, start, end):
        """Get palindromes within specified character range."""
        if not self.can_form_palindrome():
            return []
        
        result = []
        for arrangement in self._generate_palindrome_arrangements():
            if start <= len(arrangement) <= end:
                result.append(arrangement)
        return result
    
    def get_palindromes_with_pattern(self, pattern_func):
        """Get palindromes matching specified pattern."""
        if not self.can_form_palindrome():
            return []
        
        result = []
        for arrangement in self._generate_palindrome_arrangements():
            if pattern_func(arrangement):
                result.append(arrangement)
        return result
    
    def get_string_statistics(self):
        """Get statistics about string and palindrome properties."""
        total_chars = len(self.s)
        unique_chars = len(self.char_count)
        
        return {
            'total_characters': total_chars,
            'unique_characters': unique_chars,
            'odd_frequency_chars': self.odd_count,
            'even_frequency_chars': self.even_count,
            'can_form_palindrome': self.can_form_palindrome(),
            'character_distribution': dict(self.char_count)
        }
    
    def get_palindrome_patterns(self):
        """Get patterns in palindrome arrangements."""
        patterns = {
            'symmetric_patterns': 0,
            'alternating_patterns': 0,
            'repeating_patterns': 0,
            'balanced_patterns': 0
        }
        
        if not self.can_form_palindrome():
            return patterns
        
        palindrome = self.get_palindrome()
        if not palindrome:
            return patterns
        
        # Check for symmetric patterns
        if palindrome == palindrome[::-1]:
            patterns['symmetric_patterns'] = 1
        
        # Check for alternating patterns
        alternating = True
        for i in range(1, len(palindrome)):
            if palindrome[i] == palindrome[i-1]:
                alternating = False
                break
        if alternating:
            patterns['alternating_patterns'] = 1
        
        # Check for repeating patterns
        for char, count in self.char_count.items():
            if count >= 4:  # At least 2 pairs
                patterns['repeating_patterns'] += 1
        
        # Check for balanced patterns
        if self.odd_count <= 1 and self.even_count >= 1:
            patterns['balanced_patterns'] = 1
        
        return patterns
    
    def get_optimal_palindrome_strategy(self):
        """Get optimal strategy for palindrome construction."""
        if not self.s:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'palindrome_feasibility': 0
            }
        
        # Calculate efficiency rate
        total_chars = len(self.s)
        unique_chars = len(self.char_count)
        efficiency_rate = unique_chars / total_chars if total_chars > 0 else 0
        
        # Calculate palindrome feasibility
        palindrome_feasibility = 1.0 if self.can_form_palindrome() else 0.0
        
        # Determine recommended strategy
        if self.odd_count <= 1:
            recommended_strategy = 'frequency_analysis'
        elif self.even_count > self.odd_count:
            recommended_strategy = 'character_balancing'
        else:
            recommended_strategy = 'brute_force_permutation'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'palindrome_feasibility': palindrome_feasibility
        }

# Example usage
s = "aabbcc"
dynamic_palindrome = DynamicPalindromeReorder(s)
print(f"Can form palindrome: {dynamic_palindrome.can_form_palindrome()}")
print(f"Palindrome: {dynamic_palindrome.get_palindrome()}")

# Add character
dynamic_palindrome.add_character('d')
print(f"After adding 'd': {dynamic_palindrome.get_palindrome()}")

# Remove character
dynamic_palindrome.remove_character('a')
print(f"After removing 'a': {dynamic_palindrome.get_palindrome()}")

# Update character
dynamic_palindrome.update_character('b', 'e')
print(f"After updating 'b' to 'e': {dynamic_palindrome.get_palindrome()}")

# Get palindromes with constraints
def constraint_func(palindrome):
    return len(palindrome) <= 10

print(f"Palindromes with constraints: {len(dynamic_palindrome.get_palindromes_with_constraints(constraint_func))}")

# Get palindromes in range
print(f"Palindromes in range 5-10: {len(dynamic_palindrome.get_palindromes_in_range(5, 10))}")

# Get palindromes with pattern
def pattern_func(palindrome):
    return palindrome.startswith('a')

print(f"Palindromes starting with 'a': {len(dynamic_palindrome.get_palindromes_with_pattern(pattern_func))}")

# Get statistics
print(f"Statistics: {dynamic_palindrome.get_string_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_palindrome.get_palindrome_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_palindrome.get_optimal_palindrome_strategy()}")
```

### **Variation 2: Palindrome Reorder with Different Operations**
**Problem**: Handle different types of palindrome operations (weighted characters, priority-based selection, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of palindrome operations.

```python
class AdvancedPalindromeReorder:
    def __init__(self, s="", weights=None, priorities=None):
        self.s = list(s)
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.char_count = defaultdict(int)
        for char in s:
            self.char_count[char] += 1
        self._update_palindrome_info()
    
    def _update_palindrome_info(self):
        """Update palindrome feasibility information."""
        self.odd_count = 0
        self.even_count = 0
        self.odd_chars = []
        self.even_chars = []
        
        for char, count in self.char_count.items():
            if count % 2 == 1:
                self.odd_count += 1
                self.odd_chars.append(char)
            else:
                self.even_count += 1
                self.even_chars.append(char)
    
    def get_weighted_palindromes(self):
        """Get palindromes with weights and priorities applied."""
        if not self.can_form_palindrome():
            return []
        
        result = []
        for arrangement in self._generate_palindrome_arrangements():
            weighted_palindrome = {
                'palindrome': arrangement,
                'total_weight': sum(self.weights.get(char, 1) for char in arrangement),
                'total_priority': sum(self.priorities.get(char, 1) for char in arrangement),
                'weighted_score': sum(self.weights.get(char, 1) * self.priorities.get(char, 1) for char in arrangement)
            }
            result.append(weighted_palindrome)
        return result
    
    def get_palindromes_with_priority(self, priority_func):
        """Get palindromes considering priority."""
        if not self.can_form_palindrome():
            return []
        
        result = []
        for arrangement in self._generate_palindrome_arrangements():
            priority = priority_func(arrangement, self.weights, self.priorities)
            result.append((arrangement, priority))
        
        # Sort by priority
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_palindromes_with_optimization(self, optimization_func):
        """Get palindromes using custom optimization function."""
        if not self.can_form_palindrome():
            return []
        
        result = []
        for arrangement in self._generate_palindrome_arrangements():
            score = optimization_func(arrangement, self.weights, self.priorities)
            result.append((arrangement, score))
        
        # Sort by optimization score
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_palindromes_with_constraints(self, constraint_func):
        """Get palindromes that satisfy custom constraints."""
        if not self.can_form_palindrome():
            return []
        
        result = []
        for arrangement in self._generate_palindrome_arrangements():
            if constraint_func(arrangement, self.weights, self.priorities):
                result.append(arrangement)
        return result
    
    def get_palindromes_with_multiple_criteria(self, criteria_list):
        """Get palindromes that satisfy multiple criteria."""
        if not self.can_form_palindrome():
            return []
        
        result = []
        for arrangement in self._generate_palindrome_arrangements():
            satisfies_all_criteria = True
            for criterion in criteria_list:
                if not criterion(arrangement, self.weights, self.priorities):
                    satisfies_all_criteria = False
                    break
            if satisfies_all_criteria:
                result.append(arrangement)
        return result
    
    def get_palindromes_with_alternatives(self, alternatives):
        """Get palindromes considering alternative weights/priorities."""
        result = []
        
        # Check original palindromes
        original_palindromes = self.get_weighted_palindromes()
        result.append((original_palindromes, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedPalindromeReorder(''.join(self.s), alt_weights, alt_priorities)
            temp_palindromes = temp_instance.get_weighted_palindromes()
            result.append((temp_palindromes, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_palindromes_with_adaptive_criteria(self, adaptive_func):
        """Get palindromes using adaptive criteria."""
        if not self.can_form_palindrome():
            return []
        
        result = []
        for arrangement in self._generate_palindrome_arrangements():
            if adaptive_func(arrangement, self.weights, self.priorities, result):
                result.append(arrangement)
        return result
    
    def _generate_palindrome_arrangements(self):
        """Generate different palindrome arrangements."""
        arrangements = []
        
        # Basic palindrome
        basic_palindrome = self.get_palindrome()
        if basic_palindrome:
            arrangements.append(basic_palindrome)
        
        # Try different arrangements of even characters
        if self.even_chars:
            even_permutations = itertools.permutations(self.even_chars)
            for perm in even_permutations:
                arrangement = self._build_palindrome_with_permutation(perm)
                if arrangement:
                    arrangements.append(arrangement)
        
        return arrangements
    
    def _build_palindrome_with_permutation(self, even_perm):
        """Build palindrome with specific even character permutation."""
        result = []
        
        # Add even characters (half of each)
        for char in even_perm:
            count = self.char_count[char]
            result.extend([char] * (count // 2))
        
        # Add odd character (if exists)
        if self.odd_chars:
            odd_char = self.odd_chars[0]
            result.extend([odd_char] * self.char_count[odd_char])
        
        # Add even characters (other half, reversed)
        for char in reversed(even_perm):
            count = self.char_count[char]
            result.extend([char] * (count // 2))
        
        return ''.join(result)
    
    def can_form_palindrome(self):
        """Check if string can form a palindrome."""
        return self.odd_count <= 1
    
    def get_palindrome(self):
        """Get palindrome if possible."""
        if not self.can_form_palindrome():
            return None
        
        # Build palindrome
        result = []
        
        # Add even characters (half of each)
        for char in self.even_chars:
            count = self.char_count[char]
            result.extend([char] * (count // 2))
        
        # Add odd character (if exists)
        if self.odd_chars:
            odd_char = self.odd_chars[0]
            result.extend([odd_char] * self.char_count[odd_char])
        
        # Add even characters (other half, reversed)
        for char in reversed(self.even_chars):
            count = self.char_count[char]
            result.extend([char] * (count // 2))
        
        return ''.join(result)
    
    def get_palindrome_optimization(self):
        """Get optimal palindrome configuration."""
        strategies = [
            ('weighted_palindromes', lambda: len(self.get_weighted_palindromes())),
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
s = "aabbcc"
weights = {char: ord(char) for char in s}  # ASCII values as weights
priorities = {char: len(s) - s.count(char) for char in s}  # Inverse frequency as priority
advanced_palindrome = AdvancedPalindromeReorder(s, weights, priorities)

print(f"Weighted palindromes: {len(advanced_palindrome.get_weighted_palindromes())}")

# Get palindromes with priority
def priority_func(palindrome, weights, priorities):
    return sum(weights.get(char, 1) for char in palindrome) + sum(priorities.get(char, 1) for char in palindrome)

print(f"Palindromes with priority: {len(advanced_palindrome.get_palindromes_with_priority(priority_func))}")

# Get palindromes with optimization
def optimization_func(palindrome, weights, priorities):
    return sum(weights.get(char, 1) * priorities.get(char, 1) for char in palindrome)

print(f"Palindromes with optimization: {len(advanced_palindrome.get_palindromes_with_optimization(optimization_func))}")

# Get palindromes with constraints
def constraint_func(palindrome, weights, priorities):
    return len(palindrome) <= 10 and sum(weights.get(char, 1) for char in palindrome) <= 1000

print(f"Palindromes with constraints: {len(advanced_palindrome.get_palindromes_with_constraints(constraint_func))}")

# Get palindromes with multiple criteria
def criterion1(palindrome, weights, priorities):
    return len(palindrome) <= 10

def criterion2(palindrome, weights, priorities):
    return sum(weights.get(char, 1) for char in palindrome) <= 1000

criteria_list = [criterion1, criterion2]
print(f"Palindromes with multiple criteria: {len(advanced_palindrome.get_palindromes_with_multiple_criteria(criteria_list))}")

# Get palindromes with alternatives
alternatives = [({char: 1 for char in s}, {char: 1 for char in s}), ({char: ord(char) for char in s}, {char: s.count(char) for char in s})]
print(f"Palindromes with alternatives: {len(advanced_palindrome.get_palindromes_with_alternatives(alternatives))}")

# Get palindromes with adaptive criteria
def adaptive_func(palindrome, weights, priorities, current_result):
    return len(palindrome) <= 10 and len(current_result) < 5

print(f"Palindromes with adaptive criteria: {len(advanced_palindrome.get_palindromes_with_adaptive_criteria(adaptive_func))}")

# Get palindrome optimization
print(f"Palindrome optimization: {advanced_palindrome.get_palindrome_optimization()}")
```

### **Variation 3: Palindrome Reorder with Constraints**
**Problem**: Handle palindrome construction with additional constraints (length limits, character constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedPalindromeReorder:
    def __init__(self, s="", constraints=None):
        self.s = list(s)
        self.constraints = constraints or {}
        self.char_count = defaultdict(int)
        for char in s:
            self.char_count[char] += 1
        self._update_palindrome_info()
    
    def _update_palindrome_info(self):
        """Update palindrome feasibility information."""
        self.odd_count = 0
        self.even_count = 0
        self.odd_chars = []
        self.even_chars = []
        
        for char, count in self.char_count.items():
            if count % 2 == 1:
                self.odd_count += 1
                self.odd_chars.append(char)
            else:
                self.even_count += 1
                self.even_chars.append(char)
    
    def _is_valid_palindrome(self, palindrome):
        """Check if palindrome is valid considering constraints."""
        # Length constraints
        if 'min_length' in self.constraints:
            if len(palindrome) < self.constraints['min_length']:
                return False
        
        if 'max_length' in self.constraints:
            if len(palindrome) > self.constraints['max_length']:
                return False
        
        # Character constraints
        if 'forbidden_chars' in self.constraints:
            for char in palindrome:
                if char in self.constraints['forbidden_chars']:
                    return False
        
        if 'required_chars' in self.constraints:
            for char in self.constraints['required_chars']:
                if char not in palindrome:
                    return False
        
        # Pattern constraints
        if 'pattern_constraints' in self.constraints:
            for constraint in self.constraints['pattern_constraints']:
                if not constraint(palindrome):
                    return False
        
        return True
    
    def get_palindromes_with_length_constraints(self, min_length, max_length):
        """Get palindromes considering length constraints."""
        if not self.can_form_palindrome():
            return []
        
        result = []
        for arrangement in self._generate_palindrome_arrangements():
            if min_length <= len(arrangement) <= max_length:
                result.append(arrangement)
        return result
    
    def get_palindromes_with_character_constraints(self, character_constraints):
        """Get palindromes considering character constraints."""
        if not self.can_form_palindrome():
            return []
        
        result = []
        for arrangement in self._generate_palindrome_arrangements():
            satisfies_constraints = True
            for constraint in character_constraints:
                if not constraint(arrangement):
                    satisfies_constraints = False
                    break
            if satisfies_constraints:
                result.append(arrangement)
        return result
    
    def get_palindromes_with_pattern_constraints(self, pattern_constraints):
        """Get palindromes considering pattern constraints."""
        if not self.can_form_palindrome():
            return []
        
        result = []
        for arrangement in self._generate_palindrome_arrangements():
            satisfies_pattern = True
            for constraint in pattern_constraints:
                if not constraint(arrangement):
                    satisfies_pattern = False
                    break
            if satisfies_pattern:
                result.append(arrangement)
        return result
    
    def get_palindromes_with_mathematical_constraints(self, constraint_func):
        """Get palindromes that satisfy custom mathematical constraints."""
        if not self.can_form_palindrome():
            return []
        
        result = []
        for arrangement in self._generate_palindrome_arrangements():
            if constraint_func(arrangement):
                result.append(arrangement)
        return result
    
    def get_palindromes_with_optimization_constraints(self, optimization_func):
        """Get palindromes using custom optimization constraints."""
        if not self.can_form_palindrome():
            return []
        
        # Sort palindromes by optimization function
        all_palindromes = []
        for arrangement in self._generate_palindrome_arrangements():
            score = optimization_func(arrangement)
            all_palindromes.append((arrangement, score))
        
        # Sort by optimization score
        all_palindromes.sort(key=lambda x: x[1], reverse=True)
        
        return [palindrome for palindrome, _ in all_palindromes]
    
    def get_palindromes_with_multiple_constraints(self, constraints_list):
        """Get palindromes that satisfy multiple constraints."""
        if not self.can_form_palindrome():
            return []
        
        result = []
        for arrangement in self._generate_palindrome_arrangements():
            satisfies_all_constraints = True
            for constraint in constraints_list:
                if not constraint(arrangement):
                    satisfies_all_constraints = False
                    break
            if satisfies_all_constraints:
                result.append(arrangement)
        return result
    
    def get_palindromes_with_priority_constraints(self, priority_func):
        """Get palindromes with priority-based constraints."""
        if not self.can_form_palindrome():
            return []
        
        # Sort palindromes by priority
        all_palindromes = []
        for arrangement in self._generate_palindrome_arrangements():
            priority = priority_func(arrangement)
            all_palindromes.append((arrangement, priority))
        
        # Sort by priority
        all_palindromes.sort(key=lambda x: x[1], reverse=True)
        
        return [palindrome for palindrome, _ in all_palindromes]
    
    def get_palindromes_with_adaptive_constraints(self, adaptive_func):
        """Get palindromes with adaptive constraints."""
        if not self.can_form_palindrome():
            return []
        
        result = []
        for arrangement in self._generate_palindrome_arrangements():
            if adaptive_func(arrangement, result):
                result.append(arrangement)
        return result
    
    def _generate_palindrome_arrangements(self):
        """Generate different palindrome arrangements."""
        arrangements = []
        
        # Basic palindrome
        basic_palindrome = self.get_palindrome()
        if basic_palindrome and self._is_valid_palindrome(basic_palindrome):
            arrangements.append(basic_palindrome)
        
        # Try different arrangements of even characters
        if self.even_chars:
            even_permutations = itertools.permutations(self.even_chars)
            for perm in even_permutations:
                arrangement = self._build_palindrome_with_permutation(perm)
                if arrangement and self._is_valid_palindrome(arrangement):
                    arrangements.append(arrangement)
        
        return arrangements
    
    def _build_palindrome_with_permutation(self, even_perm):
        """Build palindrome with specific even character permutation."""
        result = []
        
        # Add even characters (half of each)
        for char in even_perm:
            count = self.char_count[char]
            result.extend([char] * (count // 2))
        
        # Add odd character (if exists)
        if self.odd_chars:
            odd_char = self.odd_chars[0]
            result.extend([odd_char] * self.char_count[odd_char])
        
        # Add even characters (other half, reversed)
        for char in reversed(even_perm):
            count = self.char_count[char]
            result.extend([char] * (count // 2))
        
        return ''.join(result)
    
    def can_form_palindrome(self):
        """Check if string can form a palindrome."""
        return self.odd_count <= 1
    
    def get_palindrome(self):
        """Get palindrome if possible."""
        if not self.can_form_palindrome():
            return None
        
        # Build palindrome
        result = []
        
        # Add even characters (half of each)
        for char in self.even_chars:
            count = self.char_count[char]
            result.extend([char] * (count // 2))
        
        # Add odd character (if exists)
        if self.odd_chars:
            odd_char = self.odd_chars[0]
            result.extend([odd_char] * self.char_count[odd_char])
        
        # Add even characters (other half, reversed)
        for char in reversed(self.even_chars):
            count = self.char_count[char]
            result.extend([char] * (count // 2))
        
        return ''.join(result)
    
    def get_optimal_palindrome_strategy(self):
        """Get optimal palindrome strategy considering all constraints."""
        strategies = [
            ('length_constraints', self.get_palindromes_with_length_constraints),
            ('character_constraints', self.get_palindromes_with_character_constraints),
            ('pattern_constraints', self.get_palindromes_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_count = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'length_constraints':
                    current_count = len(strategy_func(1, 10))
                elif strategy_name == 'character_constraints':
                    character_constraints = [lambda p: len(p) <= 10]
                    current_count = len(strategy_func(character_constraints))
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda p: p.startswith('a')]
                    current_count = len(strategy_func(pattern_constraints))
                
                if current_count > best_count:
                    best_count = current_count
                    best_strategy = (strategy_name, current_count)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'min_length': 1,
    'max_length': 10,
    'forbidden_chars': ['x', 'y', 'z'],
    'required_chars': ['a', 'b'],
    'pattern_constraints': [lambda p: len(p) <= 8]
}

s = "aabbcc"
constrained_palindrome = ConstrainedPalindromeReorder(s, constraints)

print("Length-constrained palindromes:", len(constrained_palindrome.get_palindromes_with_length_constraints(1, 8)))

print("Character-constrained palindromes:", len(constrained_palindrome.get_palindromes_with_character_constraints([lambda p: len(p) <= 8])))

print("Pattern-constrained palindromes:", len(constrained_palindrome.get_palindromes_with_pattern_constraints([lambda p: p.startswith('a')])))

# Mathematical constraints
def custom_constraint(palindrome):
    return len(palindrome) <= 8 and palindrome.count('a') >= 1

print("Mathematical constraint palindromes:", len(constrained_palindrome.get_palindromes_with_mathematical_constraints(custom_constraint)))

# Range constraints
def range_constraint(palindrome):
    return 1 <= len(palindrome) <= 8

range_constraints = [range_constraint]
print("Range-constrained palindromes:", len(constrained_palindrome.get_palindromes_with_length_constraints(1, 8)))

# Multiple constraints
def constraint1(palindrome):
    return len(palindrome) <= 8

def constraint2(palindrome):
    return palindrome.count('a') >= 1

constraints_list = [constraint1, constraint2]
print("Multiple constraints palindromes:", len(constrained_palindrome.get_palindromes_with_multiple_constraints(constraints_list)))

# Priority constraints
def priority_func(palindrome):
    return len(palindrome) + palindrome.count('a')

print("Priority-constrained palindromes:", len(constrained_palindrome.get_palindromes_with_priority_constraints(priority_func)))

# Adaptive constraints
def adaptive_func(palindrome, current_result):
    return len(palindrome) <= 8 and len(current_result) < 5

print("Adaptive constraint palindromes:", len(constrained_palindrome.get_palindromes_with_adaptive_constraints(adaptive_func)))

# Optimal strategy
optimal = constrained_palindrome.get_optimal_palindrome_strategy()
print(f"Optimal palindrome strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Palindrome Reorder](https://cses.fi/problemset/task/1755) - Basic palindrome reordering
- [Palindrome Check](https://cses.fi/problemset/task/1754) - Check if string can be palindrome
- [String Matching](https://cses.fi/problemset/task/1753) - String matching problems

#### **LeetCode Problems**
- [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/) - Check if string is palindrome
- [Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/) - Partition string into palindromes
- [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/) - Find longest palindrome
- [Palindrome Number](https://leetcode.com/problems/palindrome-number/) - Check if number is palindrome

#### **Problem Categories**
- **String Manipulation**: Character frequency, string construction, palindrome properties
- **Combinatorics**: Permutation counting, character arrangement, frequency analysis
- **Greedy Algorithms**: Optimal character placement, palindrome construction strategies
- **Character Analysis**: Frequency counting, character distribution, string properties

## 📚 Learning Points

1. **Palindrome Properties**: Essential for understanding palindrome construction
2. **Character Frequency Analysis**: Key technique for efficient feasibility checking
3. **String Manipulation**: Important for understanding palindrome construction
4. **Mathematical Analysis**: Critical for understanding frequency rules
5. **Algorithm Optimization**: Foundation for many string manipulation algorithms
6. **Early Termination**: Critical for competitive programming efficiency

## 📝 Summary

The Palindrome Reorder problem demonstrates palindrome properties and character frequency analysis concepts for efficient palindrome construction. We explored three approaches:

1. **Brute Force Permutation Check**: O(n! × n) time complexity using permutation generation, inefficient for large strings
2. **Character Frequency Analysis**: O(n) time complexity using frequency counting, better approach for palindrome construction
3. **Optimized Frequency Analysis with Early Termination**: O(n) time complexity with early termination, optimal approach for palindrome construction

The key insights include understanding palindrome properties, using character frequency analysis for efficient feasibility checking, and applying mathematical analysis for optimal performance. This problem serves as an excellent introduction to string manipulation algorithms and palindrome construction optimization.
