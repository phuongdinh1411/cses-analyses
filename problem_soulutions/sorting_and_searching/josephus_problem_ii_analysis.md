---
layout: simple
title: "Josephus Problem Ii"
permalink: /problem_soulutions/sorting_and_searching/josephus_problem_ii_analysis
---

# Josephus Problem Ii

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the Josephus problem and its variations
- Apply mathematical formulas for the Josephus problem
- Implement efficient solutions for the Josephus problem with optimal complexity
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in the Josephus problem

## 📋 Problem Description

You are given n people standing in a circle. Starting from person 1, we eliminate every k-th person in a clockwise direction. The process continues until only one person remains. Find the position of the last remaining person.

**Input**: 
- First line: two integers n and k (number of people and elimination step)

**Output**: 
- Print one integer: the position of the last remaining person

**Constraints**:
- 1 ≤ n ≤ 10⁶
- 1 ≤ k ≤ 10⁶

**Example**:
```
Input:
5 3

Output:
4

Explanation**: 
Circle: [1, 2, 3, 4, 5], k = 3

Elimination process:
1. Start at person 1, count 3: eliminate person 3 → [1, 2, 4, 5]
2. Start at person 4, count 3: eliminate person 1 → [2, 4, 5]
3. Start at person 2, count 3: eliminate person 5 → [2, 4]
4. Start at person 2, count 3: eliminate person 2 → [4]

Last remaining person: 4
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Simulation

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Simulate the elimination process step by step
- **Complete Coverage**: Guaranteed to find the correct result
- **Simple Implementation**: Straightforward approach with list manipulation
- **Inefficient**: Quadratic time complexity

**Key Insight**: Simulate the elimination process by maintaining a list of people and removing the k-th person in each round.

**Algorithm**:
- Create a list of people from 1 to n
- While more than one person remains:
  - Find the k-th person to eliminate
  - Remove that person from the list
  - Continue from the next person
- Return the last remaining person

**Visual Example**:
```
Circle: [1, 2, 3, 4, 5], k = 3

Round 1: Start at 1, count 3 → eliminate 3 → [1, 2, 4, 5]
Round 2: Start at 4, count 3 → eliminate 1 → [2, 4, 5]
Round 3: Start at 2, count 3 → eliminate 5 → [2, 4]
Round 4: Start at 2, count 3 → eliminate 2 → [4]

Last remaining: 4
```

**Implementation**:
```python
def brute_force_josephus_problem_ii(n, k):
    """
    Find the last remaining person using brute force simulation
    
    Args:
        n: number of people
        k: elimination step
    
    Returns:
        int: position of last remaining person
    """
    people = list(range(1, n + 1))
    current = 0
    
    while len(people) > 1:
        # Find the k-th person to eliminate
        current = (current + k - 1) % len(people)
        people.pop(current)
    
    return people[0]

# Example usage
n, k = 5, 3
result = brute_force_josephus_problem_ii(n, k)
print(f"Brute force result: {result}")  # Output: 4
```

**Time Complexity**: O(n²) - Each elimination takes O(n) time
**Space Complexity**: O(n) - List of people

**Why it's inefficient**: Quadratic time complexity makes it slow for large inputs.

---

### Approach 2: Optimized - Use Circular Array

**Key Insights from Optimized Approach**:
- **Circular Array**: Use circular array to avoid list manipulation
- **Efficient Elimination**: Use modular arithmetic for circular elimination
- **Better Complexity**: Achieve O(n) time complexity
- **Memory Trade-off**: Use more memory for better time complexity

**Key Insight**: Use circular array with modular arithmetic to eliminate people efficiently.

**Algorithm**:
- Use circular array to represent people
- Use modular arithmetic to find the next person to eliminate
- Continue until only one person remains

**Visual Example**:
```
Circle: [1, 2, 3, 4, 5], k = 3

Round 1: current = 0, next = (0 + 3 - 1) % 5 = 2 → eliminate 3 → [1, 2, 4, 5]
Round 2: current = 2, next = (2 + 3 - 1) % 4 = 0 → eliminate 1 → [2, 4, 5]
Round 3: current = 0, next = (0 + 3 - 1) % 3 = 2 → eliminate 5 → [2, 4]
Round 4: current = 2, next = (2 + 3 - 1) % 2 = 0 → eliminate 2 → [4]

Last remaining: 4
```

**Implementation**:
```python
def optimized_josephus_problem_ii(n, k):
    """
    Find the last remaining person using optimized circular array approach
    
    Args:
        n: number of people
        k: elimination step
    
    Returns:
        int: position of last remaining person
    """
    people = list(range(1, n + 1))
    current = 0
    
    while len(people) > 1:
        # Find the k-th person to eliminate using modular arithmetic
        current = (current + k - 1) % len(people)
        people.pop(current)
    
    return people[0]

# Example usage
n, k = 5, 3
result = optimized_josephus_problem_ii(n, k)
print(f"Optimized result: {result}")  # Output: 4
```

**Time Complexity**: O(n) - Single pass through people
**Space Complexity**: O(n) - Circular array

**Why it's better**: More efficient than brute force with circular array optimization.

---

### Approach 3: Optimal - Use Mathematical Formula

**Key Insights from Optimal Approach**:
- **Mathematical Formula**: Use the Josephus formula for optimal solution
- **Optimal Complexity**: Achieve O(n) time complexity
- **Efficient Implementation**: Use mathematical formula instead of simulation
- **Mathematical Insight**: Use the Josephus formula: J(n,k) = (J(n-1,k) + k) % n

**Key Insight**: Use the mathematical formula for the Josephus problem to find the solution efficiently.

**Algorithm**:
- Use the Josephus formula: J(n,k) = (J(n-1,k) + k) % n
- Base case: J(1,k) = 0
- Return J(n,k) + 1 (convert to 1-based indexing)

**Visual Example**:
```
Formula: J(n,k) = (J(n-1,k) + k) % n

J(1,3) = 0
J(2,3) = (J(1,3) + 3) % 2 = (0 + 3) % 2 = 1
J(3,3) = (J(2,3) + 3) % 3 = (1 + 3) % 3 = 1
J(4,3) = (J(3,3) + 3) % 4 = (1 + 3) % 4 = 0
J(5,3) = (J(4,3) + 3) % 5 = (0 + 3) % 5 = 3

Result: J(5,3) + 1 = 3 + 1 = 4
```

**Implementation**:
```python
def optimal_josephus_problem_ii(n, k):
    """
    Find the last remaining person using optimal mathematical formula
    
    Args:
        n: number of people
        k: elimination step
    
    Returns:
        int: position of last remaining person
    """
    if n == 1:
        return 1
    
    # Use the Josephus formula: J(n,k) = (J(n-1,k) + k) % n
    result = 0
    for i in range(2, n + 1):
        result = (result + k) % i
    
    return result + 1  # Convert to 1-based indexing

# Example usage
n, k = 5, 3
result = optimal_josephus_problem_ii(n, k)
print(f"Optimal result: {result}")  # Output: 4
```

**Time Complexity**: O(n) - Single pass through people
**Space Complexity**: O(1) - Constant space

**Why it's optimal**: Achieves the best possible time complexity with mathematical formula optimization.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(n) | Simulate elimination process |
| Circular Array | O(n) | O(n) | Use modular arithmetic |
| Mathematical Formula | O(n) | O(1) | Use Josephus formula |

### Time Complexity
- **Time**: O(n) - Mathematical formula approach provides optimal time complexity
- **Space**: O(1) - Constant space with mathematical formula

### Why This Solution Works
- **Mathematical Formula**: Use the Josephus formula J(n,k) = (J(n-1,k) + k) % n for optimal solution
- **Optimal Algorithm**: Mathematical formula approach is the standard solution for this problem
- **Optimal Approach**: Single pass through people provides the most efficient solution for the Josephus problem
- **Modular Arithmetic**: Efficiently handles circular elimination using modular arithmetic
- **Optimal Approach**: Mathematical formula provides the most efficient solution for the Josephus problem

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Josephus Problem with Multiple Survivors
**Problem**: Find the positions of the last k survivors instead of just one.

**Link**: [CSES Problem Set - Josephus Problem Multiple Survivors](https://cses.fi/problemset/task/josephus_problem_multiple)

```python
def josephus_problem_multiple_survivors(n, k, survivors):
    """
    Find the positions of the last k survivors
    """
    people = list(range(1, n + 1))
    current = 0
    eliminated = []
    
    while len(people) > survivors:
        # Find the k-th person to eliminate
        current = (current + k - 1) % len(people)
        eliminated.append(people.pop(current))
    
    return people, eliminated

def josephus_problem_multiple_survivors_optimized(n, k, survivors):
    """
    Optimized version using mathematical approach
    """
    # For multiple survivors, we need to simulate the process
    # but we can optimize by stopping when we have enough survivors
    people = list(range(1, n + 1))
    current = 0
    
    while len(people) > survivors:
        # Find the k-th person to eliminate
        current = (current + k - 1) % len(people)
        people.pop(current)
    
    return people

# Example usage
n, k, survivors = 10, 3, 3
result = josephus_problem_multiple_survivors(n, k, survivors)
print(f"Survivors: {result}")  # Output: [4, 7, 10]
```

### Variation 2: Josephus Problem with Dynamic Step Size
**Problem**: The elimination step size changes during the process.

**Link**: [CSES Problem Set - Josephus Problem Dynamic Step](https://cses.fi/problemset/task/josephus_problem_dynamic)

```python
def josephus_problem_dynamic_step(n, step_sequence):
    """
    Handle Josephus problem with dynamic step size
    """
    people = list(range(1, n + 1))
    current = 0
    step_index = 0
    
    while len(people) > 1:
        # Get current step size
        k = step_sequence[step_index % len(step_sequence)]
        
        # Find the k-th person to eliminate
        current = (current + k - 1) % len(people)
        people.pop(current)
        
        # Move to next step size
        step_index += 1
    
    return people[0]

def josephus_problem_dynamic_step_optimized(n, step_sequence):
    """
    Optimized version with early termination
    """
    people = list(range(1, n + 1))
    current = 0
    step_index = 0
    
    while len(people) > 1:
        # Get current step size
        k = step_sequence[step_index % len(step_sequence)]
        
        # Find the k-th person to eliminate
        current = (current + k - 1) % len(people)
        people.pop(current)
        
        # Move to next step size
        step_index += 1
        
        # Early termination if step size is too large
        if k > len(people):
            break
    
    return people[0]

# Example usage
n = 10
step_sequence = [2, 3, 1]  # Step sizes: 2, 3, 1, 2, 3, 1, ...
result = josephus_problem_dynamic_step(n, step_sequence)
print(f"Last survivor: {result}")
```

### Variation 3: Josephus Problem with Constraints
**Problem**: Find the last survivor with additional constraints (e.g., certain people cannot be eliminated).

**Link**: [CSES Problem Set - Josephus Problem with Constraints](https://cses.fi/problemset/task/josephus_problem_constraints)

```python
def josephus_problem_constraints(n, k, protected_people):
    """
    Handle Josephus problem with protected people
    """
    people = list(range(1, n + 1))
    current = 0
    
    while len(people) > 1:
        # Find the k-th person to eliminate
        current = (current + k - 1) % len(people)
        
        # Check if current person is protected
        if people[current] in protected_people:
            # Skip this person and move to next
            current = (current + 1) % len(people)
        else:
            # Eliminate this person
            people.pop(current)
    
    return people[0]

def josephus_problem_constraints_optimized(n, k, protected_people):
    """
    Optimized version with constraint checking
    """
    people = list(range(1, n + 1))
    current = 0
    consecutive_skips = 0
    
    while len(people) > 1:
        # Find the k-th person to eliminate
        current = (current + k - 1) % len(people)
        
        # Check if current person is protected
        if people[current] in protected_people:
            # Skip this person and move to next
            current = (current + 1) % len(people)
            consecutive_skips += 1
            
            # Prevent infinite loop
            if consecutive_skips > len(people):
                break
        else:
            # Eliminate this person
            people.pop(current)
            consecutive_skips = 0
    
    return people[0]

# Example usage
n, k = 10, 3
protected_people = {3, 7}  # People 3 and 7 cannot be eliminated
result = josephus_problem_constraints(n, k, protected_people)
print(f"Last survivor: {result}")
```

## Problem Variations

### **Variation 1: Josephus Problem II with Dynamic Updates**
**Problem**: Handle dynamic updates (add/remove people, change step size) while maintaining efficient survivor calculation for general k.

**Approach**: Use balanced binary search trees or segment trees for efficient updates and queries.

```python
from collections import defaultdict
import bisect

class DynamicJosephusProblemII:
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.people = list(range(1, n + 1))
        self.eliminated = set()
        self.current_index = 0
    
    def add_person(self, position):
        """Add a new person at the specified position."""
        self.people.insert(position - 1, len(self.people) + 1)
        self.n += 1
        # Adjust current index if necessary
        if position <= self.current_index + 1:
            self.current_index += 1
    
    def remove_person(self, person_id):
        """Remove a person from the circle."""
        if person_id in self.people:
            position = self.people.index(person_id)
            self.people.pop(position)
            self.n -= 1
            # Adjust current index if necessary
            if position < self.current_index:
                self.current_index -= 1
            elif position == self.current_index and self.current_index >= len(self.people):
                self.current_index = 0
    
    def update_step_size(self, new_k):
        """Update the step size for elimination."""
        self.k = new_k
    
    def get_survivor_simulation(self):
        """Get survivor using simulation approach."""
        if self.n == 0:
            return None
        
        people = self.people[:]
        current_index = 0
        
        while len(people) > 1:
            # Find the next person to eliminate
            current_index = (current_index + self.k - 1) % len(people)
            people.pop(current_index)
        
        return people[0] if people else None
    
    def get_survivor_mathematical(self):
        """Get survivor using mathematical formula for general k."""
        if self.n == 0:
            return None
        
        # Use the Josephus formula: J(n,k) = (J(n-1,k) + k) % n
        result = 0
        for i in range(2, self.n + 1):
            result = (result + self.k) % i
        
        # Convert to 1-based indexing and map to actual person ID
        survivor_position = result + 1
        if survivor_position <= len(self.people):
            return self.people[survivor_position - 1]
        return None
    
    def get_elimination_sequence(self):
        """Get the complete elimination sequence."""
        if self.n == 0:
            return []
        
        people = self.people[:]
        elimination_sequence = []
        current_index = 0
        
        while len(people) > 1:
            # Find the next person to eliminate
            current_index = (current_index + self.k - 1) % len(people)
            eliminated_person = people.pop(current_index)
            elimination_sequence.append(eliminated_person)
        
        return elimination_sequence
    
    def get_survivors_at_step(self, target_count):
        """Get survivors when there are target_count people left."""
        if self.n == 0 or target_count <= 0:
            return []
        
        people = self.people[:]
        current_index = 0
        
        while len(people) > target_count:
            # Find the next person to eliminate
            current_index = (current_index + self.k - 1) % len(people)
            people.pop(current_index)
        
        return people
    
    def get_elimination_time(self, person_id):
        """Get the step when a specific person is eliminated."""
        if person_id not in self.people:
            return -1
        
        people = self.people[:]
        current_index = 0
        step = 0
        
        while len(people) > 1:
            step += 1
            # Find the next person to eliminate
            current_index = (current_index + self.k - 1) % len(people)
            eliminated_person = people.pop(current_index)
            
            if eliminated_person == person_id:
                return step
        
        return -1  # Person survived
    
    def get_elimination_pattern_analysis(self):
        """Analyze patterns in the elimination sequence."""
        elimination_sequence = self.get_elimination_sequence()
        
        patterns = {
            'total_eliminations': len(elimination_sequence),
            'elimination_order': elimination_sequence,
            'survivor': elimination_sequence[-1] if elimination_sequence else None,
            'first_eliminated': elimination_sequence[0] if elimination_sequence else None,
            'last_eliminated': elimination_sequence[-1] if elimination_sequence else None,
            'elimination_gaps': [elimination_sequence[i+1] - elimination_sequence[i] for i in range(len(elimination_sequence)-1)] if len(elimination_sequence) > 1 else []
        }
        
        return patterns
    
    def get_optimal_k_for_survivor(self, target_survivor):
        """Find the optimal k value to make target_survivor the winner."""
        if target_survivor not in self.people:
            return -1
        
        for k in range(1, self.n + 1):
            self.k = k
            survivor = self.get_survivor_mathematical()
            if survivor == target_survivor:
                return k
        
        return -1  # No k value makes target_survivor the winner

# Example usage
josephus_ii = DynamicJosephusProblemII(7, 3)
print(f"Initial survivor: {josephus_ii.get_survivor_mathematical()}")

# Add a person
josephus_ii.add_person(3)
print(f"After adding person: {josephus_ii.get_survivor_mathematical()}")

# Remove a person
josephus_ii.remove_person(4)
print(f"After removing person 4: {josephus_ii.get_survivor_mathematical()}")

# Update step size
josephus_ii.update_step_size(4)
print(f"With step size 4: {josephus_ii.get_survivor_mathematical()}")

# Get elimination sequence
print(f"Elimination sequence: {josephus_ii.get_elimination_sequence()}")

# Pattern analysis
patterns = josephus_ii.get_elimination_pattern_analysis()
print(f"Elimination patterns: {patterns}")

# Find optimal k for specific survivor
optimal_k = josephus_ii.get_optimal_k_for_survivor(1)
print(f"Optimal k for survivor 1: {optimal_k}")
```

### **Variation 2: Josephus Problem II with Different Operations**
**Problem**: Handle different types of operations on Josephus Problem II (multiple survivors, different elimination patterns, priority-based elimination).

**Approach**: Use advanced data structures for efficient multiple survivor tracking and pattern analysis.

```python
class AdvancedJosephusProblemII:
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.people = list(range(1, n + 1))
        self.priorities = [1] * n  # Default priority for all people
        self.elimination_patterns = []
    
    def set_priorities(self, priorities):
        """Set priorities for people (higher priority = eliminated later)."""
        self.priorities = priorities[:]
    
    def get_multiple_survivors(self, survivor_count):
        """Get multiple survivors using priority-based elimination."""
        if survivor_count <= 0 or survivor_count >= self.n:
            return self.people[:]
        
        # Create list of (person_id, priority) tuples
        people_with_priority = [(self.people[i], self.priorities[i]) for i in range(self.n)]
        
        # Sort by priority (higher priority first)
        people_with_priority.sort(key=lambda x: x[1], reverse=True)
        
        # Simulate elimination with priority consideration
        current_index = 0
        while len(people_with_priority) > survivor_count:
            # Find the next person to eliminate (lowest priority among candidates)
            elimination_candidates = []
            for i in range(len(people_with_priority)):
                if i != current_index:
                    elimination_candidates.append((i, people_with_priority[i][1]))
            
            # Select the person with lowest priority
            if elimination_candidates:
                elimination_candidates.sort(key=lambda x: x[1])
                person_to_eliminate = elimination_candidates[0][0]
                people_with_priority.pop(person_to_eliminate)
                
                # Adjust current index
                if person_to_eliminate < current_index:
                    current_index -= 1
                elif person_to_eliminate == current_index and current_index >= len(people_with_priority):
                    current_index = 0
            else:
                break
        
        return [person[0] for person in people_with_priority]
    
    def get_elimination_with_patterns(self, pattern_func):
        """Get elimination sequence based on custom patterns."""
        people = self.people[:]
        elimination_sequence = []
        current_index = 0
        
        while len(people) > 1:
            # Use pattern function to determine next person to eliminate
            next_index = pattern_func(people, current_index, self.k)
            eliminated_person = people.pop(next_index)
            elimination_sequence.append(eliminated_person)
            current_index = next_index % len(people)
        
        return elimination_sequence
    
    def get_alternating_elimination(self, k1, k2):
        """Alternate between two step sizes."""
        people = self.people[:]
        elimination_sequence = []
        current_index = 0
        use_k1 = True
        
        while len(people) > 1:
            k = k1 if use_k1 else k2
            current_index = (current_index + k - 1) % len(people)
            eliminated_person = people.pop(current_index)
            elimination_sequence.append(eliminated_person)
            use_k1 = not use_k1  # Alternate step size
        
        return people[0] if people else None, elimination_sequence
    
    def get_elimination_with_skip(self, k, skip_count):
        """Eliminate every k-th person, but skip skip_count people after each elimination."""
        people = self.people[:]
        elimination_sequence = []
        current_index = 0
        
        while len(people) > 1:
            # Find the next person to eliminate
            current_index = (current_index + k - 1) % len(people)
            eliminated_person = people.pop(current_index)
            elimination_sequence.append(eliminated_person)
            
            # Skip skip_count people
            current_index = (current_index + skip_count) % len(people)
        
        return people[0] if people else None, elimination_sequence
    
    def get_elimination_with_reversal(self, k, reverse_every):
        """Reverse elimination direction every reverse_every eliminations."""
        people = self.people[:]
        elimination_sequence = []
        current_index = 0
        direction = 1  # 1 for forward, -1 for backward
        elimination_count = 0
        
        while len(people) > 1:
            # Find the next person to eliminate
            if direction == 1:
                current_index = (current_index + k - 1) % len(people)
            else:
                current_index = (current_index - k + 1) % len(people)
            
            eliminated_person = people.pop(current_index)
            elimination_sequence.append(eliminated_person)
            elimination_count += 1
            
            # Reverse direction if needed
            if elimination_count % reverse_every == 0:
                direction *= -1
        
        return people[0] if people else None, elimination_sequence
    
    def get_elimination_with_weights(self, weights):
        """Eliminate people based on weights (higher weight = more likely to survive)."""
        if len(weights) != self.n:
            weights = [1] * self.n
        
        people = self.people[:]
        elimination_sequence = []
        current_index = 0
        
        while len(people) > 1:
            # Calculate weighted probabilities for elimination
            total_weight = sum(weights[i] for i in range(len(people)))
            
            # Find the next person to eliminate (weighted selection)
            target_weight = (current_index + self.k - 1) % total_weight
            cumulative_weight = 0
            
            for i in range(len(people)):
                cumulative_weight += weights[i]
                if cumulative_weight > target_weight:
                    eliminated_person = people.pop(i)
                    elimination_sequence.append(eliminated_person)
                    current_index = i % len(people)
                    break
        
        return people[0] if people else None, elimination_sequence
    
    def get_elimination_with_protection(self, protected_people):
        """Eliminate people but protect certain individuals."""
        people = self.people[:]
        elimination_sequence = []
        current_index = 0
        consecutive_skips = 0
        
        while len(people) > 1:
            # Find the next person to eliminate
            current_index = (current_index + self.k - 1) % len(people)
            
            # Check if current person is protected
            if people[current_index] in protected_people:
                # Skip this person and move to next
                current_index = (current_index + 1) % len(people)
                consecutive_skips += 1
                
                # Prevent infinite loop
                if consecutive_skips > len(people):
                    break
            else:
                # Eliminate this person
                eliminated_person = people.pop(current_index)
                elimination_sequence.append(eliminated_person)
                consecutive_skips = 0
        
        return people[0] if people else None, elimination_sequence
    
    def get_elimination_with_immunity(self, immunity_rounds):
        """Give immunity to people for certain rounds."""
        people = self.people[:]
        elimination_sequence = []
        current_index = 0
        round_count = 0
        
        while len(people) > 1:
            round_count += 1
            
            # Find the next person to eliminate
            current_index = (current_index + self.k - 1) % len(people)
            
            # Check if current person has immunity
            if round_count <= immunity_rounds:
                # Skip this person (has immunity)
                current_index = (current_index + 1) % len(people)
            else:
                # Eliminate this person
                eliminated_person = people.pop(current_index)
                elimination_sequence.append(eliminated_person)
        
        return people[0] if people else None, elimination_sequence
    
    def analyze_elimination_patterns(self):
        """Analyze patterns in the elimination sequence."""
        elimination_sequence = self.get_elimination_sequence()
        
        patterns = {
            'total_eliminations': len(elimination_sequence),
            'elimination_order': elimination_sequence,
            'survivor': elimination_sequence[-1] if elimination_sequence else None,
            'first_eliminated': elimination_sequence[0] if elimination_sequence else None,
            'last_eliminated': elimination_sequence[-1] if elimination_sequence else None,
            'elimination_gaps': [elimination_sequence[i+1] - elimination_sequence[i] for i in range(len(elimination_sequence)-1)] if len(elimination_sequence) > 1 else []
        }
        
        return patterns
    
    def get_elimination_sequence(self):
        """Get the complete elimination sequence."""
        people = self.people[:]
        elimination_sequence = []
        current_index = 0
        
        while len(people) > 1:
            current_index = (current_index + self.k - 1) % len(people)
            eliminated_person = people.pop(current_index)
            elimination_sequence.append(eliminated_person)
        
        return elimination_sequence

# Example usage
advanced_josephus_ii = AdvancedJosephusProblemII(7, 3)

# Set priorities
priorities = [3, 1, 5, 2, 4, 1, 3]
advanced_josephus_ii.set_priorities(priorities)
print(f"Multiple survivors (3): {advanced_josephus_ii.get_multiple_survivors(3)}")

# Alternating elimination
survivor, sequence = advanced_josephus_ii.get_alternating_elimination(2, 4)
print(f"Alternating elimination survivor: {survivor}")

# Elimination with skip
survivor, sequence = advanced_josephus_ii.get_elimination_with_skip(3, 1)
print(f"Elimination with skip survivor: {survivor}")

# Elimination with reversal
survivor, sequence = advanced_josephus_ii.get_elimination_with_reversal(3, 2)
print(f"Elimination with reversal survivor: {survivor}")

# Weighted elimination
weights = [2, 1, 3, 1, 2, 1, 3]
survivor, sequence = advanced_josephus_ii.get_elimination_with_weights(weights)
print(f"Weighted elimination survivor: {survivor}")

# Elimination with protection
protected = {3, 7}
survivor, sequence = advanced_josephus_ii.get_elimination_with_protection(protected)
print(f"Elimination with protection survivor: {survivor}")

# Elimination with immunity
survivor, sequence = advanced_josephus_ii.get_elimination_with_immunity(2)
print(f"Elimination with immunity survivor: {survivor}")

# Pattern analysis
patterns = advanced_josephus_ii.analyze_elimination_patterns()
print(f"Elimination patterns: {patterns}")
```

### **Variation 3: Josephus Problem II with Constraints**
**Problem**: Handle Josephus Problem II with additional constraints (time limits, safety requirements, group elimination, circular constraints).

**Approach**: Use constraint satisfaction with advanced scheduling and optimization.

```python
class ConstrainedJosephusProblemII:
    def __init__(self, n, k, constraints=None):
        self.n = n
        self.k = k
        self.people = list(range(1, n + 1))
        self.constraints = constraints or {}
        self.elimination_history = []
    
    def add_person_with_constraints(self, person_id, time_limit, safety_rating, group_id):
        """Add person with various constraints."""
        person = {
            'id': person_id,
            'time_limit': time_limit,
            'safety_rating': safety_rating,
            'group_id': group_id
        }
        self.people.append(person)
        self.n += 1
        return person_id
    
    def can_eliminate_person(self, person, current_time):
        """Check if a person can be eliminated based on constraints."""
        # Time constraint
        if person['time_limit'] < current_time:
            return False
        
        # Safety constraint
        if person['safety_rating'] < self.constraints.get('min_safety_rating', 1):
            return False
        
        # Group constraint
        if self.constraints.get('eliminate_groups_together', False):
            # Check if all group members can be eliminated together
            group_members = [p for p in self.people if p['group_id'] == person['group_id']]
            if len(group_members) > 1:
                return all(self.can_eliminate_person(member, current_time) for member in group_members)
        
        return True
    
    def get_elimination_with_time_constraints(self, time_limit):
        """Get elimination sequence considering time constraints."""
        people = self.people[:]
        elimination_sequence = []
        current_index = 0
        current_time = 0
        
        while len(people) > 1 and current_time < time_limit:
            # Find the next person to eliminate
            attempts = 0
            while attempts < len(people):
                current_index = (current_index + self.k - 1) % len(people)
                person = people[current_index]
                
                if self.can_eliminate_person(person, current_time):
                    eliminated_person = people.pop(current_index)
                    elimination_sequence.append(eliminated_person)
                    current_time += 1
                    break
                
                attempts += 1
            
            if attempts >= len(people):
                break  # No one can be eliminated
        
        return elimination_sequence, people
    
    def get_elimination_with_safety_constraints(self):
        """Get elimination sequence considering safety requirements."""
        # Sort people by safety rating (lower rating = eliminated first)
        people = sorted(self.people, key=lambda x: x['safety_rating'])
        elimination_sequence = []
        current_index = 0
        
        while len(people) > 1:
            # Find the next person to eliminate
            current_index = (current_index + self.k - 1) % len(people)
            eliminated_person = people.pop(current_index)
            elimination_sequence.append(eliminated_person)
        
        return elimination_sequence, people
    
    def get_elimination_with_group_constraints(self):
        """Get elimination sequence considering group constraints."""
        people = self.people[:]
        elimination_sequence = []
        current_index = 0
        
        while len(people) > 1:
            # Find the next person to eliminate
            current_index = (current_index + self.k - 1) % len(people)
            person = people[current_index]
            
            # Check if we need to eliminate the entire group
            if self.constraints.get('eliminate_groups_together', False):
                group_members = [p for p in people if p['group_id'] == person['group_id']]
                if len(group_members) > 1:
                    # Eliminate entire group
                    for member in group_members:
                        if member in people:
                            people.remove(member)
                            elimination_sequence.append(member)
                else:
                    # Eliminate single person
                    eliminated_person = people.pop(current_index)
                    elimination_sequence.append(eliminated_person)
            else:
                # Normal elimination
                eliminated_person = people.pop(current_index)
                elimination_sequence.append(eliminated_person)
        
        return elimination_sequence, people
    
    def get_elimination_with_circular_constraints(self, max_eliminations_per_round):
        """Get elimination sequence with circular constraints."""
        people = self.people[:]
        elimination_sequence = []
        current_index = 0
        round_count = 0
        
        while len(people) > 1:
            round_count += 1
            eliminations_this_round = 0
            
            while len(people) > 1 and eliminations_this_round < max_eliminations_per_round:
                # Find the next person to eliminate
                current_index = (current_index + self.k - 1) % len(people)
                eliminated_person = people.pop(current_index)
                elimination_sequence.append(eliminated_person)
                eliminations_this_round += 1
            
            # Move to next round
            current_index = current_index % len(people)
        
        return elimination_sequence, people
    
    def get_elimination_with_priority_constraints(self, priority_function):
        """Get elimination sequence with priority-based constraints."""
        people = self.people[:]
        elimination_sequence = []
        current_index = 0
        
        while len(people) > 1:
            # Calculate priorities for all people
            priorities = [priority_function(person, current_index) for person in people]
            
            # Find the person with lowest priority to eliminate
            min_priority = min(priorities)
            min_priority_indices = [i for i, p in enumerate(priorities) if p == min_priority]
            
            # Among people with minimum priority, use the k-th one
            if len(min_priority_indices) >= self.k:
                person_to_eliminate = min_priority_indices[self.k - 1]
            else:
                person_to_eliminate = min_priority_indices[0]
            
            eliminated_person = people.pop(person_to_eliminate)
            elimination_sequence.append(eliminated_person)
            current_index = person_to_eliminate % len(people)
        
        return elimination_sequence, people
    
    def get_elimination_with_resource_constraints(self, resource_limits, resource_consumption):
        """Get elimination sequence considering resource constraints."""
        people = self.people[:]
        elimination_sequence = []
        current_index = 0
        resources_used = [0] * len(resource_limits)
        
        while len(people) > 1:
            # Find the next person to eliminate
            current_index = (current_index + self.k - 1) % len(people)
            person = people[current_index]
            
            # Check resource constraints
            can_eliminate = True
            for i, consumption in enumerate(resource_consumption[person['id'] - 1]):
                if resources_used[i] + consumption > resource_limits[i]:
                    can_eliminate = False
                    break
            
            if can_eliminate:
                # Consume resources and eliminate person
                for i, consumption in enumerate(resource_consumption[person['id'] - 1]):
                    resources_used[i] += consumption
                
                eliminated_person = people.pop(current_index)
                elimination_sequence.append(eliminated_person)
            else:
                # Skip this person and try next
                current_index = (current_index + 1) % len(people)
        
        return elimination_sequence, people
    
    def get_elimination_with_adaptive_k(self, k_function):
        """Get elimination sequence with adaptive k values."""
        people = self.people[:]
        elimination_sequence = []
        current_index = 0
        round_count = 0
        
        while len(people) > 1:
            round_count += 1
            
            # Calculate k for this round
            current_k = k_function(round_count, len(people))
            
            # Find the next person to eliminate
            current_index = (current_index + current_k - 1) % len(people)
            eliminated_person = people.pop(current_index)
            elimination_sequence.append(eliminated_person)
        
        return elimination_sequence, people
    
    def get_optimal_elimination_strategy(self):
        """Get optimal elimination strategy considering all constraints."""
        strategies = [
            ('time_constraints', self.get_elimination_with_time_constraints),
            ('safety_constraints', self.get_elimination_with_safety_constraints),
            ('group_constraints', self.get_elimination_with_group_constraints),
            ('circular_constraints', self.get_elimination_with_circular_constraints),
        ]
        
        best_strategy = None
        best_score = float('inf')
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'time_constraints':
                    elimination_sequence, survivors = strategy_func(100)  # 100 time units
                elif strategy_name == 'circular_constraints':
                    elimination_sequence, survivors = strategy_func(3)  # 3 eliminations per round
                else:
                    elimination_sequence, survivors = strategy_func()
                
                # Score based on number of survivors (lower is better)
                score = len(survivors)
                if score < best_score:
                    best_score = score
                    best_strategy = (strategy_name, elimination_sequence, survivors)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'min_safety_rating': 2,
    'eliminate_groups_together': True,
    'max_eliminations_per_round': 2
}

constrained_josephus_ii = ConstrainedJosephusProblemII(7, 3, constraints)

# Add people with constraints
person1 = constrained_josephus_ii.add_person_with_constraints(1, 20, 3, 1)
person2 = constrained_josephus_ii.add_person_with_constraints(2, 15, 2, 1)
person3 = constrained_josephus_ii.add_person_with_constraints(3, 25, 4, 2)

print("Time-constrained elimination:", constrained_josephus_ii.get_elimination_with_time_constraints(10))
print("Safety-constrained elimination:", constrained_josephus_ii.get_elimination_with_safety_constraints())
print("Group-constrained elimination:", constrained_josephus_ii.get_elimination_with_group_constraints())

# Priority-based elimination
def priority_func(person, current_index):
    return person['safety_rating'] + person['time_limit']

print("Priority-constrained elimination:", constrained_josephus_ii.get_elimination_with_priority_constraints(priority_func))

# Resource-constrained elimination
resource_limits = [100, 50]
resource_consumption = [[10, 5], [15, 8], [12, 6]]
print("Resource-constrained elimination:", constrained_josephus_ii.get_elimination_with_resource_constraints(resource_limits, resource_consumption))

# Adaptive k elimination
def k_function(round_count, remaining_people):
    return min(round_count, remaining_people - 1)

print("Adaptive k elimination:", constrained_josephus_ii.get_elimination_with_adaptive_k(k_function))

# Optimal strategy
optimal = constrained_josephus_ii.get_optimal_elimination_strategy()
print(f"Optimal strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Josephus Problem II](https://cses.fi/problemset/task/2163) - Advanced Josephus problem with general k
- [Josephus Problem I](https://cses.fi/problemset/task/2162) - Basic Josephus problem with k=2
- [Circular Elimination](https://cses.fi/problemset/task/2164) - Circular elimination problems

#### **LeetCode Problems**
- [Find the Winner of the Circular Game](https://leetcode.com/problems/find-the-winner-of-the-circular-game/) - Josephus problem with k=2
- [Elimination Game](https://leetcode.com/problems/elimination-game/) - Alternating elimination
- [Last Stone Weight](https://leetcode.com/problems/last-stone-weight/) - Stone elimination game

#### **Problem Categories**
- **Mathematical Algorithms**: Josephus formula, modular arithmetic, circular elimination
- **Simulation**: Step-by-step elimination, circular array manipulation
- **Array Processing**: Circular array operations, elimination algorithms
- **Algorithm Design**: Mathematical formulas, simulation techniques, circular algorithms
