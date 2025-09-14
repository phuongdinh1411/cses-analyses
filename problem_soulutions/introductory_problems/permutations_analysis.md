---
layout: simple
title: "Permutations"
permalink: /problem_soulutions/introductory_problems/permutations_analysis
---

# Permutations

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand permutation generation and lexicographic ordering concepts
- Apply backtracking or next_permutation to generate all permutations
- Implement efficient permutation generation algorithms with proper lexicographic ordering
- Optimize permutation generation using backtracking and lexicographic ordering techniques
- Handle edge cases in permutation problems (small n, lexicographic ordering, large output)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Permutation generation, backtracking, next_permutation, lexicographic ordering
- **Data Structures**: Arrays, permutation tracking, lexicographic ordering, backtracking stacks
- **Mathematical Concepts**: Permutations, combinatorics, lexicographic ordering, factorial calculations
- **Programming Skills**: Backtracking implementation, permutation generation, lexicographic ordering, algorithm implementation
- **Related Problems**: Permutation problems, Backtracking, Lexicographic ordering, Combinatorics

## Problem Description

**Problem**: Generate all permutations of numbers from 1 to n.

**Input**: An integer n (1 ≤ n ≤ 8)

**Output**: 
- First line: number of permutations
- Next lines: each permutation on a separate line (in lexicographic order)

**Constraints**:
- 1 ≤ n ≤ 8
- Generate all n! permutations
- Output must be in lexicographic order
- Each permutation on a separate line
- First line shows total count

**Example**:
```
Input: 3

Output:
6
1 2 3
1 3 2
2 1 3
2 3 1
3 1 2
3 2 1
```

## Visual Example

### Input and Permutation Generation
```
Input: n = 3

Numbers to permute: [1, 2, 3]
Total permutations: 3! = 6
```

### Lexicographic Order Generation
```
For n = 3, generating all permutations:

1. [1, 2, 3] ← Start with smallest
2. [1, 3, 2] ← Swap last two
3. [2, 1, 3] ← Move to next starting position
4. [2, 3, 1] ← Swap last two
5. [3, 1, 2] ← Move to next starting position
6. [3, 2, 1] ← Swap last two
```

### Backtracking Process
```
Backtracking tree for n = 3:

Level 0: []
├─ Level 1: [1]
│  ├─ Level 2: [1, 2]
│  │  └─ Level 3: [1, 2, 3] ✓
│  └─ Level 2: [1, 3]
│     └─ Level 3: [1, 3, 2] ✓
├─ Level 1: [2]
│  ├─ Level 2: [2, 1]
│  │  └─ Level 3: [2, 1, 3] ✓
│  └─ Level 2: [2, 3]
│     └─ Level 3: [2, 3, 1] ✓
└─ Level 1: [3]
   ├─ Level 2: [3, 1]
   │  └─ Level 3: [3, 1, 2] ✓
   └─ Level 2: [3, 2]
      └─ Level 3: [3, 2, 1] ✓
```

### Key Insight
The solution works by:
1. Using backtracking to generate all possible arrangements
2. Maintaining lexicographic order through systematic generation
3. Swapping elements to create different permutations
4. Time complexity: O(n! × n) for generating and outputting all permutations
5. Space complexity: O(n! × n) for storing all permutations

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Backtracking (Inefficient)

**Key Insights from Recursive Backtracking Solution:**
- Generate all permutations using recursive backtracking
- Simple but memory-intensive approach
- Not suitable for large n due to exponential growth
- Straightforward implementation but poor scalability

**Algorithm:**
1. Use recursive backtracking to generate all permutations
2. Build permutations by adding one element at a time
3. Use visited array to track used elements
4. Generate all possible arrangements systematically

**Visual Example:**
```
Recursive backtracking: Build permutations step by step
For n = 3, arr = [1, 2, 3]:

Step 1: Start with empty permutation []
Step 2: Add 1 → [1]
Step 3: Add 2 → [1, 2]
Step 4: Add 3 → [1, 2, 3] ✓ (complete permutation)

Backtrack and try other combinations:
Step 5: Remove 3, add 3 in different position
Step 6: Continue until all permutations generated
```

**Implementation:**
```python
def permutations_recursive(n):
    def backtrack(path, used):
        if len(path) == n:
            result.append(path[:])
            return
        
        for i in range(1, n + 1):
            if not used[i]:
                used[i] = True
                path.append(i)
                backtrack(path, used)
                path.pop()
                used[i] = False
    
    result = []
    used = [False] * (n + 1)
    backtrack([], used)
    return result

def solve_permutations_recursive():
    n = int(input())
    perms = permutations_recursive(n)
    
    print(len(perms))
    for perm in perms:
        print(' '.join(map(str, perm)))
```

**Time Complexity:** O(n! × n) for generating all permutations
**Space Complexity:** O(n! × n) for storing all permutations

**Why it's inefficient:**
- O(n! × n) time complexity grows exponentially
- Not suitable for competitive programming with n up to 8
- Memory-intensive for large n
- Poor performance with factorial growth

### Approach 2: Iterative Next Permutation (Better)

**Key Insights from Iterative Solution:**
- Use iterative approach to generate permutations
- More memory-efficient than recursive backtracking
- Standard method for permutation generation
- Can handle larger n than recursive approach

**Algorithm:**
1. Start with the lexicographically smallest permutation
2. Generate next permutation using next_permutation algorithm
3. Continue until all permutations are generated
4. Output all permutations in lexicographic order

**Visual Example:**
```
Iterative approach: Generate next permutation
For n = 3, start with [1, 2, 3]:

1. [1, 2, 3] ← Initial permutation
2. [1, 3, 2] ← Next permutation
3. [2, 1, 3] ← Next permutation
4. [2, 3, 1] ← Next permutation
5. [3, 1, 2] ← Next permutation
6. [3, 2, 1] ← Final permutation
```

**Implementation:**
```python
def next_permutation(arr):
    n = len(arr)
    
    # Find the largest index i such that arr[i] < arr[i + 1]
    i = n - 2
    while i >= 0 and arr[i] >= arr[i + 1]:
        i -= 1
    
    if i == -1:
        return False  # No next permutation
    
    # Find the largest index j such that arr[i] < arr[j]
    j = n - 1
    while arr[j] <= arr[i]:
        j -= 1
    
    # Swap arr[i] and arr[j]
    arr[i], arr[j] = arr[j], arr[i]
    
    # Reverse the suffix starting at arr[i + 1]
    arr[i + 1:] = arr[i + 1:][::-1]
    
    return True

def permutations_iterative(n):
    arr = list(range(1, n + 1))
    result = [arr[:]]
    
    while next_permutation(arr):
        result.append(arr[:])
    
    return result

def solve_permutations_iterative():
    n = int(input())
    perms = permutations_iterative(n)
    
    print(len(perms))
    for perm in perms:
        print(' '.join(map(str, perm)))
```

**Time Complexity:** O(n! × n) for generating all permutations
**Space Complexity:** O(n! × n) for storing all permutations

**Why it's better:**
- More memory-efficient than recursive approach
- Uses iterative next_permutation algorithm
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Built-in itertools.permutations (Optimal)

**Key Insights from Built-in Solution:**
- Use Python's optimized itertools.permutations
- Most efficient approach for permutation generation
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use itertools.permutations to generate all permutations
2. Convert permutations to required output format
3. Print count and all permutations
4. Leverage optimized built-in implementation

**Visual Example:**
```
Built-in approach: Use itertools.permutations
For n = 3:

import itertools
perms = list(itertools.permutations(range(1, 4)))
# Generates: [(1,2,3), (1,3,2), (2,1,3), (2,3,1), (3,1,2), (3,2,1)]

Output:
6
1 2 3
1 3 2
2 1 3
2 3 1
3 1 2
3 2 1
```

**Implementation:**
```python
from itertools import permutations

def solve_permutations():
    n = int(input())
    
    # Generate all permutations using built-in function
    perms = list(permutations(range(1, n + 1)))
    
    # Print output
    print(len(perms))
    for perm in perms:
        print(' '.join(map(str, perm)))

# Main execution
if __name__ == "__main__":
    solve_permutations()
```

**Time Complexity:** O(n! × n) for generating all permutations
**Space Complexity:** O(n! × n) for storing all permutations

**Why it's optimal:**
- Uses optimized built-in implementation
- Most efficient approach for competitive programming
- Standard method for permutation generation
- Leverages Python's optimized algorithms

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Permutations with Repetition
**Problem**: Generate all permutations when elements can be repeated.

**Link**: [CSES Problem Set - Permutations with Repetition](https://cses.fi/problemset/task/permutations_with_repetition)

```python
from itertools import product

def permutations_with_repetition(n, k):
    # Generate all k-length permutations with repetition
    return list(product(range(1, n + 1), repeat=k))
```

### Variation 2: Permutations of String
**Problem**: Generate all permutations of a given string.

**Link**: [CSES Problem Set - String Permutations](https://cses.fi/problemset/task/string_permutations)

```python
from itertools import permutations

def string_permutations(s):
    # Generate all permutations of string
    return [''.join(p) for p in permutations(s)]
```

### Variation 3: Next Permutation
**Problem**: Find the next lexicographically greater permutation.

**Link**: [CSES Problem Set - Next Permutation](https://cses.fi/problemset/task/next_permutation)

```python
def next_permutation(arr):
    n = len(arr)
    
    # Find the largest index i such that arr[i] < arr[i + 1]
    i = n - 2
    while i >= 0 and arr[i] >= arr[i + 1]:
        i -= 1
    
    if i == -1:
        return False  # No next permutation
    
    # Find the largest index j such that arr[i] < arr[j]
    j = n - 1
    while arr[j] <= arr[i]:
        j -= 1
    
    # Swap arr[i] and arr[j]
    arr[i], arr[j] = arr[j], arr[i]
    
    # Reverse the suffix starting at arr[i + 1]
    arr[i + 1:] = arr[i + 1:][::-1]
    
    return True
```

## Problem Variations

### **Variation 1: Permutations with Dynamic Updates**
**Problem**: Handle dynamic element updates (add/remove/update elements) while generating permutations efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic permutation management.

```python
from collections import defaultdict
import itertools

class DynamicPermutations:
    def __init__(self, elements=None):
        self.elements = list(elements) if elements else []
        self.element_count = defaultdict(int)
        for element in self.elements:
            self.element_count[element] += 1
        self._update_permutation_info()
    
    def _update_permutation_info(self):
        """Update permutation feasibility information."""
        self.total_elements = len(self.elements)
        self.unique_elements = len(self.element_count)
        self.total_permutations = self._calculate_total_permutations()
    
    def _calculate_total_permutations(self):
        """Calculate total number of permutations."""
        if not self.elements:
            return 0
        
        # Handle duplicates
        total = 1
        for i in range(1, len(self.elements) + 1):
            total *= i
        
        # Divide by factorials of duplicate counts
        for count in self.element_count.values():
            if count > 1:
                for i in range(1, count + 1):
                    total //= i
        
        return total
    
    def add_element(self, element):
        """Add element to the set."""
        self.elements.append(element)
        self.element_count[element] += 1
        self._update_permutation_info()
    
    def remove_element(self, element):
        """Remove element from the set."""
        if element in self.elements and self.element_count[element] > 0:
            self.elements.remove(element)
            self.element_count[element] -= 1
            if self.element_count[element] == 0:
                del self.element_count[element]
            self._update_permutation_info()
    
    def update_element(self, old_element, new_element):
        """Update element in the set."""
        if old_element in self.elements:
            self.remove_element(old_element)
            self.add_element(new_element)
    
    def get_all_permutations(self):
        """Get all permutations of the elements."""
        if not self.elements:
            return []
        
        # Use itertools.permutations for efficiency
        return list(itertools.permutations(self.elements))
    
    def get_permutations_with_constraints(self, constraint_func):
        """Get permutations that satisfy custom constraints."""
        result = []
        for perm in self.get_all_permutations():
            if constraint_func(perm):
                result.append(perm)
        return result
    
    def get_permutations_in_range(self, start, end):
        """Get permutations within specified index range."""
        all_perms = self.get_all_permutations()
        return all_perms[start:end]
    
    def get_permutations_with_pattern(self, pattern_func):
        """Get permutations matching specified pattern."""
        result = []
        for perm in self.get_all_permutations():
            if pattern_func(perm):
                result.append(perm)
        return result
    
    def get_permutation_statistics(self):
        """Get statistics about permutations."""
        if not self.elements:
            return {
                'total_elements': 0,
                'unique_elements': 0,
                'total_permutations': 0,
                'element_distribution': {}
            }
        
        return {
            'total_elements': self.total_elements,
            'unique_elements': self.unique_elements,
            'total_permutations': self.total_permutations,
            'element_distribution': dict(self.element_count)
        }
    
    def get_permutation_patterns(self):
        """Get patterns in permutations."""
        patterns = {
            'lexicographic_order': 0,
            'reverse_lexicographic_order': 0,
            'cyclic_permutations': 0,
            'symmetric_permutations': 0
        }
        
        if not self.elements:
            return patterns
        
        all_perms = self.get_all_permutations()
        
        # Check for lexicographic order
        if all_perms == sorted(all_perms):
            patterns['lexicographic_order'] = 1
        
        # Check for reverse lexicographic order
        if all_perms == sorted(all_perms, reverse=True):
            patterns['reverse_lexicographic_order'] = 1
        
        # Check for cyclic permutations
        if len(self.elements) > 1:
            cyclic_count = 0
            for perm in all_perms:
                if self._is_cyclic_permutation(perm):
                    cyclic_count += 1
            patterns['cyclic_permutations'] = cyclic_count
        
        # Check for symmetric permutations
        symmetric_count = 0
        for perm in all_perms:
            if perm == perm[::-1]:
                symmetric_count += 1
        patterns['symmetric_permutations'] = symmetric_count
        
        return patterns
    
    def _is_cyclic_permutation(self, perm):
        """Check if permutation is cyclic."""
        if len(perm) <= 1:
            return True
        
        # Check if permutation is a single cycle
        visited = set()
        current = 0
        cycle_length = 0
        
        while current not in visited:
            visited.add(current)
            current = perm.index(self.elements[current])
            cycle_length += 1
        
        return cycle_length == len(perm)
    
    def get_optimal_permutation_strategy(self):
        """Get optimal strategy for permutation generation."""
        if not self.elements:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'permutation_feasibility': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = self.unique_elements / self.total_elements if self.total_elements > 0 else 0
        
        # Calculate permutation feasibility
        permutation_feasibility = 1.0 if self.total_permutations > 0 else 0.0
        
        # Determine recommended strategy
        if self.total_permutations <= 1000:
            recommended_strategy = 'itertools_permutations'
        elif self.unique_elements == self.total_elements:
            recommended_strategy = 'iterative_next_permutation'
        else:
            recommended_strategy = 'recursive_backtracking'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'permutation_feasibility': permutation_feasibility
        }

# Example usage
elements = [1, 2, 3]
dynamic_permutations = DynamicPermutations(elements)
print(f"Total permutations: {dynamic_permutations.total_permutations}")
print(f"All permutations: {dynamic_permutations.get_all_permutations()}")

# Add element
dynamic_permutations.add_element(4)
print(f"After adding 4: {dynamic_permutations.total_permutations}")

# Remove element
dynamic_permutations.remove_element(2)
print(f"After removing 2: {dynamic_permutations.total_permutations}")

# Update element
dynamic_permutations.update_element(3, 5)
print(f"After updating 3 to 5: {dynamic_permutations.total_permutations}")

# Get permutations with constraints
def constraint_func(perm):
    return perm[0] == 1

print(f"Permutations starting with 1: {len(dynamic_permutations.get_permutations_with_constraints(constraint_func))}")

# Get permutations in range
print(f"Permutations in range 0-2: {len(dynamic_permutations.get_permutations_in_range(0, 2))}")

# Get permutations with pattern
def pattern_func(perm):
    return len(perm) <= 3

print(f"Permutations with length <= 3: {len(dynamic_permutations.get_permutations_with_pattern(pattern_func))}")

# Get statistics
print(f"Statistics: {dynamic_permutations.get_permutation_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_permutations.get_permutation_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_permutations.get_optimal_permutation_strategy()}")
```

### **Variation 2: Permutations with Different Operations**
**Problem**: Handle different types of permutation operations (weighted elements, priority-based selection, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of permutation operations.

```python
class AdvancedPermutations:
    def __init__(self, elements=None, weights=None, priorities=None):
        self.elements = list(elements) if elements else []
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.element_count = defaultdict(int)
        for element in self.elements:
            self.element_count[element] += 1
        self._update_permutation_info()
    
    def _update_permutation_info(self):
        """Update permutation feasibility information."""
        self.total_elements = len(self.elements)
        self.unique_elements = len(self.element_count)
        self.total_permutations = self._calculate_total_permutations()
    
    def _calculate_total_permutations(self):
        """Calculate total number of permutations."""
        if not self.elements:
            return 0
        
        # Handle duplicates
        total = 1
        for i in range(1, len(self.elements) + 1):
            total *= i
        
        # Divide by factorials of duplicate counts
        for count in self.element_count.values():
            if count > 1:
                for i in range(1, count + 1):
                    total //= i
        
        return total
    
    def get_weighted_permutations(self):
        """Get permutations with weights and priorities applied."""
        result = []
        for perm in self.get_all_permutations():
            weighted_permutation = {
                'permutation': perm,
                'total_weight': sum(self.weights.get(element, 1) for element in perm),
                'total_priority': sum(self.priorities.get(element, 1) for element in perm),
                'weighted_score': sum(self.weights.get(element, 1) * self.priorities.get(element, 1) for element in perm)
            }
            result.append(weighted_permutation)
        return result
    
    def get_permutations_with_priority(self, priority_func):
        """Get permutations considering priority."""
        result = []
        for perm in self.get_all_permutations():
            priority = priority_func(perm, self.weights, self.priorities)
            result.append((perm, priority))
        
        # Sort by priority
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_permutations_with_optimization(self, optimization_func):
        """Get permutations using custom optimization function."""
        result = []
        for perm in self.get_all_permutations():
            score = optimization_func(perm, self.weights, self.priorities)
            result.append((perm, score))
        
        # Sort by optimization score
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_permutations_with_constraints(self, constraint_func):
        """Get permutations that satisfy custom constraints."""
        result = []
        for perm in self.get_all_permutations():
            if constraint_func(perm, self.weights, self.priorities):
                result.append(perm)
        return result
    
    def get_permutations_with_multiple_criteria(self, criteria_list):
        """Get permutations that satisfy multiple criteria."""
        result = []
        for perm in self.get_all_permutations():
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
        original_permutations = self.get_weighted_permutations()
        result.append((original_permutations, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedPermutations(self.elements, alt_weights, alt_priorities)
            temp_permutations = temp_instance.get_weighted_permutations()
            result.append((temp_permutations, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_permutations_with_adaptive_criteria(self, adaptive_func):
        """Get permutations using adaptive criteria."""
        result = []
        for perm in self.get_all_permutations():
            if adaptive_func(perm, self.weights, self.priorities, result):
                result.append(perm)
        return result
    
    def get_all_permutations(self):
        """Get all permutations of the elements."""
        if not self.elements:
            return []
        
        # Use itertools.permutations for efficiency
        return list(itertools.permutations(self.elements))
    
    def get_permutation_optimization(self):
        """Get optimal permutation configuration."""
        strategies = [
            ('weighted_permutations', lambda: len(self.get_weighted_permutations())),
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
elements = [1, 2, 3]
weights = {element: element * 2 for element in elements}  # Double the element value as weight
priorities = {element: len(elements) - elements.index(element) for element in elements}  # Higher index = lower priority
advanced_permutations = AdvancedPermutations(elements, weights, priorities)

print(f"Weighted permutations: {len(advanced_permutations.get_weighted_permutations())}")

# Get permutations with priority
def priority_func(perm, weights, priorities):
    return sum(weights.get(element, 1) for element in perm) + sum(priorities.get(element, 1) for element in perm)

print(f"Permutations with priority: {len(advanced_permutations.get_permutations_with_priority(priority_func))}")

# Get permutations with optimization
def optimization_func(perm, weights, priorities):
    return sum(weights.get(element, 1) * priorities.get(element, 1) for element in perm)

print(f"Permutations with optimization: {len(advanced_permutations.get_permutations_with_optimization(optimization_func))}")

# Get permutations with constraints
def constraint_func(perm, weights, priorities):
    return len(perm) <= 3 and sum(weights.get(element, 1) for element in perm) <= 20

print(f"Permutations with constraints: {len(advanced_permutations.get_permutations_with_constraints(constraint_func))}")

# Get permutations with multiple criteria
def criterion1(perm, weights, priorities):
    return len(perm) <= 3

def criterion2(perm, weights, priorities):
    return sum(weights.get(element, 1) for element in perm) <= 20

criteria_list = [criterion1, criterion2]
print(f"Permutations with multiple criteria: {len(advanced_permutations.get_permutations_with_multiple_criteria(criteria_list))}")

# Get permutations with alternatives
alternatives = [({element: 1 for element in elements}, {element: 1 for element in elements}), ({element: element*3 for element in elements}, {element: element+1 for element in elements})]
print(f"Permutations with alternatives: {len(advanced_permutations.get_permutations_with_alternatives(alternatives))}")

# Get permutations with adaptive criteria
def adaptive_func(perm, weights, priorities, current_result):
    return len(perm) <= 3 and len(current_result) < 5

print(f"Permutations with adaptive criteria: {len(advanced_permutations.get_permutations_with_adaptive_criteria(adaptive_func))}")

# Get permutation optimization
print(f"Permutation optimization: {advanced_permutations.get_permutation_optimization()}")
```

### **Variation 3: Permutations with Constraints**
**Problem**: Handle permutation generation with additional constraints (length limits, element constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedPermutations:
    def __init__(self, elements=None, constraints=None):
        self.elements = list(elements) if elements else []
        self.constraints = constraints or {}
        self.element_count = defaultdict(int)
        for element in self.elements:
            self.element_count[element] += 1
        self._update_permutation_info()
    
    def _update_permutation_info(self):
        """Update permutation feasibility information."""
        self.total_elements = len(self.elements)
        self.unique_elements = len(self.element_count)
        self.total_permutations = self._calculate_total_permutations()
    
    def _calculate_total_permutations(self):
        """Calculate total number of permutations."""
        if not self.elements:
            return 0
        
        # Handle duplicates
        total = 1
        for i in range(1, len(self.elements) + 1):
            total *= i
        
        # Divide by factorials of duplicate counts
        for count in self.element_count.values():
            if count > 1:
                for i in range(1, count + 1):
                    total //= i
        
        return total
    
    def _is_valid_permutation(self, perm):
        """Check if permutation is valid considering constraints."""
        # Length constraints
        if 'min_length' in self.constraints:
            if len(perm) < self.constraints['min_length']:
                return False
        
        if 'max_length' in self.constraints:
            if len(perm) > self.constraints['max_length']:
                return False
        
        # Element constraints
        if 'forbidden_elements' in self.constraints:
            for element in perm:
                if element in self.constraints['forbidden_elements']:
                    return False
        
        if 'required_elements' in self.constraints:
            for element in self.constraints['required_elements']:
                if element not in perm:
                    return False
        
        # Pattern constraints
        if 'pattern_constraints' in self.constraints:
            for constraint in self.constraints['pattern_constraints']:
                if not constraint(perm):
                    return False
        
        return True
    
    def get_permutations_with_length_constraints(self, min_length, max_length):
        """Get permutations considering length constraints."""
        result = []
        for perm in self.get_all_permutations():
            if min_length <= len(perm) <= max_length:
                result.append(perm)
        return result
    
    def get_permutations_with_element_constraints(self, element_constraints):
        """Get permutations considering element constraints."""
        result = []
        for perm in self.get_all_permutations():
            satisfies_constraints = True
            for constraint in element_constraints:
                if not constraint(perm):
                    satisfies_constraints = False
                    break
            if satisfies_constraints:
                result.append(perm)
        return result
    
    def get_permutations_with_pattern_constraints(self, pattern_constraints):
        """Get permutations considering pattern constraints."""
        result = []
        for perm in self.get_all_permutations():
            satisfies_pattern = True
            for constraint in pattern_constraints:
                if not constraint(perm):
                    satisfies_pattern = False
                    break
            if satisfies_pattern:
                result.append(perm)
        return result
    
    def get_permutations_with_mathematical_constraints(self, constraint_func):
        """Get permutations that satisfy custom mathematical constraints."""
        result = []
        for perm in self.get_all_permutations():
            if constraint_func(perm):
                result.append(perm)
        return result
    
    def get_permutations_with_optimization_constraints(self, optimization_func):
        """Get permutations using custom optimization constraints."""
        # Sort permutations by optimization function
        all_permutations = []
        for perm in self.get_all_permutations():
            score = optimization_func(perm)
            all_permutations.append((perm, score))
        
        # Sort by optimization score
        all_permutations.sort(key=lambda x: x[1], reverse=True)
        
        return [perm for perm, _ in all_permutations]
    
    def get_permutations_with_multiple_constraints(self, constraints_list):
        """Get permutations that satisfy multiple constraints."""
        result = []
        for perm in self.get_all_permutations():
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
        for perm in self.get_all_permutations():
            priority = priority_func(perm)
            all_permutations.append((perm, priority))
        
        # Sort by priority
        all_permutations.sort(key=lambda x: x[1], reverse=True)
        
        return [perm for perm, _ in all_permutations]
    
    def get_permutations_with_adaptive_constraints(self, adaptive_func):
        """Get permutations with adaptive constraints."""
        result = []
        for perm in self.get_all_permutations():
            if adaptive_func(perm, result):
                result.append(perm)
        return result
    
    def get_all_permutations(self):
        """Get all permutations of the elements."""
        if not self.elements:
            return []
        
        # Use itertools.permutations for efficiency
        return list(itertools.permutations(self.elements))
    
    def get_optimal_permutation_strategy(self):
        """Get optimal permutation strategy considering all constraints."""
        strategies = [
            ('length_constraints', self.get_permutations_with_length_constraints),
            ('element_constraints', self.get_permutations_with_element_constraints),
            ('pattern_constraints', self.get_permutations_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_count = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'length_constraints':
                    current_count = len(strategy_func(1, 3))
                elif strategy_name == 'element_constraints':
                    element_constraints = [lambda p: len(p) <= 3]
                    current_count = len(strategy_func(element_constraints))
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda p: p[0] == 1]
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
    'max_length': 3,
    'forbidden_elements': [4, 5, 6],
    'required_elements': [1, 2],
    'pattern_constraints': [lambda p: len(p) <= 3]
}

elements = [1, 2, 3]
constrained_permutations = ConstrainedPermutations(elements, constraints)

print("Length-constrained permutations:", len(constrained_permutations.get_permutations_with_length_constraints(1, 3)))

print("Element-constrained permutations:", len(constrained_permutations.get_permutations_with_element_constraints([lambda p: len(p) <= 3])))

print("Pattern-constrained permutations:", len(constrained_permutations.get_permutations_with_pattern_constraints([lambda p: p[0] == 1])))

# Mathematical constraints
def custom_constraint(perm):
    return len(perm) <= 3 and perm.count(1) >= 1

print("Mathematical constraint permutations:", len(constrained_permutations.get_permutations_with_mathematical_constraints(custom_constraint)))

# Range constraints
def range_constraint(perm):
    return 1 <= len(perm) <= 3

range_constraints = [range_constraint]
print("Range-constrained permutations:", len(constrained_permutations.get_permutations_with_length_constraints(1, 3)))

# Multiple constraints
def constraint1(perm):
    return len(perm) <= 3

def constraint2(perm):
    return perm.count(1) >= 1

constraints_list = [constraint1, constraint2]
print("Multiple constraints permutations:", len(constrained_permutations.get_permutations_with_multiple_constraints(constraints_list)))

# Priority constraints
def priority_func(perm):
    return len(perm) + perm.count(1)

print("Priority-constrained permutations:", len(constrained_permutations.get_permutations_with_priority_constraints(priority_func)))

# Adaptive constraints
def adaptive_func(perm, current_result):
    return len(perm) <= 3 and len(current_result) < 5

print("Adaptive constraint permutations:", len(constrained_permutations.get_permutations_with_adaptive_constraints(adaptive_func)))

# Optimal strategy
optimal = constrained_permutations.get_optimal_permutation_strategy()
print(f"Optimal permutation strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Permutations](https://cses.fi/problemset/task/1070) - Generate all permutations
- [Creating Strings](https://cses.fi/problemset/task/1622) - Generate permutations of string
- [Chessboard and Queens](https://cses.fi/problemset/task/1624) - Permutation with constraints

#### **LeetCode Problems**
- [Permutations](https://leetcode.com/problems/permutations/) - Generate all permutations
- [Permutations II](https://leetcode.com/problems/permutations-ii/) - Permutations with duplicates
- [Next Permutation](https://leetcode.com/problems/next-permutation/) - Find next lexicographical permutation
- [Permutation Sequence](https://leetcode.com/problems/permutation-sequence/) - Kth permutation

#### **Problem Categories**
- **Combinatorics**: Permutation generation, factorial calculations, arrangement counting
- **Backtracking**: Recursive generation, constraint satisfaction, systematic exploration
- **Lexicographic Ordering**: Systematic arrangement, ordered generation, sequence analysis
- **Algorithm Design**: Recursive algorithms, iterative generation, optimization techniques

## 📚 Learning Points

1. **Permutation Generation**: Essential for understanding combinatorial problems
2. **Backtracking**: Key technique for generating all possible arrangements
3. **Lexicographic Ordering**: Important for understanding systematic generation
4. **Combinatorics**: Critical for understanding factorial calculations
5. **Algorithm Optimization**: Foundation for many combinatorial algorithms
6. **Built-in Functions**: Critical for competitive programming efficiency

## 📝 Summary

The Permutations problem demonstrates permutation generation and lexicographic ordering concepts for systematic arrangement generation. We explored three approaches:

1. **Recursive Backtracking**: O(n! × n) time complexity using recursive backtracking, inefficient for large n
2. **Iterative Next Permutation**: O(n! × n) time complexity using iterative next_permutation algorithm, better approach for permutation generation
3. **Built-in itertools.permutations**: O(n! × n) time complexity with optimized built-in implementation, optimal approach for permutation generation

The key insights include understanding permutation generation principles, using backtracking for systematic arrangement generation, and applying built-in functions for optimal performance. This problem serves as an excellent introduction to combinatorial algorithms and permutation generation optimization.
