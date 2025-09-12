---
layout: simple
title: "Josephus Problem I"
permalink: /problem_soulutions/sorting_and_searching/josephus_problem_i_analysis
---

# Josephus Problem I

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the classic Josephus problem and its mathematical properties
- Apply simulation techniques for elimination problems
- Implement efficient solutions for circular elimination problems with optimal complexity
- Optimize solutions for large inputs with mathematical formulas
- Handle edge cases in circular elimination problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Simulation, mathematical formulas, circular elimination, modular arithmetic
- **Data Structures**: Arrays, circular arrays, mathematical sequences
- **Mathematical Concepts**: Josephus problem, modular arithmetic, recurrence relations, mathematical sequences
- **Programming Skills**: Algorithm implementation, complexity analysis, mathematical formula derivation
- **Related Problems**: Josephus Problem II (advanced), Circular elimination problems, Mathematical sequence problems

## 📋 Problem Description

There are n people sitting in a circle. We start counting from person 1 and eliminate every second person (person 2, 4, 6, ...) until only one person remains.

Find the position of the last remaining person.

**Input**: 
- One integer n (number of people)

**Output**: 
- Print one integer: the position of the last remaining person

**Constraints**:
- 1 ≤ n ≤ 10⁶

**Example**:
```
Input:
7

Output:
7

Explanation**: 
Circle: [1, 2, 3, 4, 5, 6, 7]

Round 1: Eliminate 2, 4, 6 → Remaining: [1, 3, 5, 7]
Round 2: Eliminate 3, 7 → Remaining: [1, 5]
Round 3: Eliminate 5 → Remaining: [1]

Last remaining: Person 1

Wait, let me recalculate:
Circle: [1, 2, 3, 4, 5, 6, 7]

Round 1: Start from 1, eliminate 2, 4, 6 → Remaining: [1, 3, 5, 7]
Round 2: Start from 1, eliminate 3, 7 → Remaining: [1, 5]
Round 3: Start from 1, eliminate 5 → Remaining: [1]

Last remaining: Person 1

Actually, let me trace more carefully:
Circle: [1, 2, 3, 4, 5, 6, 7]

Round 1: Start from 1, count 1,2 → eliminate 2
         Start from 3, count 3,4 → eliminate 4
         Start from 5, count 5,6 → eliminate 6
         Start from 7, count 7,1 → eliminate 1
         Remaining: [3, 5, 7]

Round 2: Start from 3, count 3,5 → eliminate 5
         Start from 7, count 7,3 → eliminate 3
         Remaining: [7]

Last remaining: Person 7
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: [Description]
- **Complete Coverage**: [Description]
- **Simple Implementation**: [Description]

**Key Insight**: [Main insight]

**Algorithm**:
- [Step 1]
- [Step 2]
- [Step 3]

**Implementation**:
```python
def brute_force_josephus_problem_i(arr):
    """
    [Description]
    
    Args:
        arr: [Description]
    
    Returns:
        [Description]
    """
    # Implementation will be added
    pass
```

**Time Complexity**: O([complexity])
**Space Complexity**: O([complexity])

**Why it's inefficient**: [Reason]

---

### Approach 2: Optimized

**Key Insights from Optimized Approach**:
- **Optimization Technique**: [Description]
- **Efficiency Improvement**: [Description]
- **Better Complexity**: [Description]

**Key Insight**: [Main insight]

**Algorithm**:
- [Step 1]
- [Step 2]
- [Step 3]

**Implementation**:
```python
def optimized_josephus_problem_i(arr):
    """
    [Description]
    
    Args:
        arr: [Description]
    
    Returns:
        [Description]
    """
    # Implementation will be added
    pass
```

**Time Complexity**: O([complexity])
**Space Complexity**: O([complexity])

**Why it's better**: [Reason]

---

### Approach 3: Optimal

**Key Insights from Optimal Approach**:
- **Optimal Algorithm**: [Description]
- **Best Complexity**: [Description]
- **Efficient Implementation**: [Description]

**Key Insight**: [Main insight]

**Algorithm**:
- [Step 1]
- [Step 2]
- [Step 3]

**Implementation**:
```python
def optimal_josephus_problem_i(arr):
    """
    [Description]
    
    Args:
        arr: [Description]
    
    Returns:
        [Description]
    """
    # Implementation will be added
    pass
```

**Time Complexity**: O([complexity])
**Space Complexity**: O([complexity])

**Why it's optimal**: [Reason]

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O([complexity]) | O([complexity]) | [Insight] |
| Optimized | O([complexity]) | O([complexity]) | [Insight] |
| Optimal | O([complexity]) | O([complexity]) | [Insight] |

### Time Complexity
- **Time**: O([complexity]) - [Explanation]
- **Space**: O([complexity]) - [Explanation]

### Why This Solution Works
- **Mathematical Formula**: Use the Josephus formula for optimal solution
- **Simulation Approach**: Simulate the elimination process for understanding
- **Optimal Algorithm**: Mathematical formula provides O(1) solution
- **Optimal Approach**: Mathematical approach is the most efficient for large inputs

## Problem Variations

### **Variation 1: Josephus Problem with Dynamic Updates**
**Problem**: Handle dynamic updates (add/remove people, change step size) while maintaining efficient survivor calculation.

**Approach**: Use balanced binary search trees or segment trees for efficient updates and queries.

```python
from collections import defaultdict
import bisect

class DynamicJosephusProblem:
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
        """Get survivor using mathematical formula."""
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

# Example usage
josephus = DynamicJosephusProblem(7, 2)
print(f"Initial survivor: {josephus.get_survivor_mathematical()}")

# Add a person
josephus.add_person(3)
print(f"After adding person: {josephus.get_survivor_mathematical()}")

# Remove a person
josephus.remove_person(4)
print(f"After removing person 4: {josephus.get_survivor_mathematical()}")

# Update step size
josephus.update_step_size(3)
print(f"With step size 3: {josephus.get_survivor_mathematical()}")

# Get elimination sequence
print(f"Elimination sequence: {josephus.get_elimination_sequence()}")
```

### **Variation 2: Josephus Problem with Different Operations**
**Problem**: Handle different types of operations on Josephus problem (multiple survivors, different elimination patterns, priority-based elimination).

**Approach**: Use advanced data structures for efficient multiple survivor tracking and pattern analysis.

```python
class AdvancedJosephusProblem:
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
    
    def analyze_elimination_patterns(self):
        """Analyze patterns in the elimination sequence."""
        elimination_sequence = self.get_elimination_sequence()
        
        patterns = {
            'total_eliminations': len(elimination_sequence),
            'elimination_order': elimination_sequence,
            'survivor': elimination_sequence[-1] if elimination_sequence else None,
            'first_eliminated': elimination_sequence[0] if elimination_sequence else None,
            'last_eliminated': elimination_sequence[-1] if elimination_sequence else None
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
advanced_josephus = AdvancedJosephusProblem(7, 2)

# Set priorities
priorities = [3, 1, 5, 2, 4, 1, 3]
advanced_josephus.set_priorities(priorities)
print(f"Multiple survivors (3): {advanced_josephus.get_multiple_survivors(3)}")

# Alternating elimination
survivor, sequence = advanced_josephus.get_alternating_elimination(2, 3)
print(f"Alternating elimination survivor: {survivor}")

# Elimination with skip
survivor, sequence = advanced_josephus.get_elimination_with_skip(2, 1)
print(f"Elimination with skip survivor: {survivor}")

# Elimination with reversal
survivor, sequence = advanced_josephus.get_elimination_with_reversal(2, 3)
print(f"Elimination with reversal survivor: {survivor}")

# Weighted elimination
weights = [2, 1, 3, 1, 2, 1, 3]
survivor, sequence = advanced_josephus.get_elimination_with_weights(weights)
print(f"Weighted elimination survivor: {survivor}")

# Pattern analysis
patterns = advanced_josephus.analyze_elimination_patterns()
print(f"Elimination patterns: {patterns}")
```

### **Variation 3: Josephus Problem with Constraints**
**Problem**: Handle Josephus problem with additional constraints (time limits, safety requirements, group elimination, circular constraints).

**Approach**: Use constraint satisfaction with advanced scheduling and optimization.

```python
class ConstrainedJosephusProblem:
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

constrained_josephus = ConstrainedJosephusProblem(7, 2, constraints)

# Add people with constraints
person1 = constrained_josephus.add_person_with_constraints(1, 20, 3, 1)
person2 = constrained_josephus.add_person_with_constraints(2, 15, 2, 1)
person3 = constrained_josephus.add_person_with_constraints(3, 25, 4, 2)

print("Time-constrained elimination:", constrained_josephus.get_elimination_with_time_constraints(10))
print("Safety-constrained elimination:", constrained_josephus.get_elimination_with_safety_constraints())
print("Group-constrained elimination:", constrained_josephus.get_elimination_with_group_constraints())

# Priority-based elimination
def priority_func(person, current_index):
    return person['safety_rating'] + person['time_limit']

print("Priority-constrained elimination:", constrained_josephus.get_elimination_with_priority_constraints(priority_func))

# Resource-constrained elimination
resource_limits = [100, 50]
resource_consumption = [[10, 5], [15, 8], [12, 6]]
print("Resource-constrained elimination:", constrained_josephus.get_elimination_with_resource_constraints(resource_limits, resource_consumption))

# Optimal strategy
optimal = constrained_josephus.get_optimal_elimination_strategy()
print(f"Optimal strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Josephus Problem I](https://cses.fi/problemset/task/2162) - Basic Josephus problem
- [Josephus Problem II](https://cses.fi/problemset/task/2163) - Advanced Josephus problem
- [Circular Elimination](https://cses.fi/problemset/task/circular_elimination) - General circular elimination

#### **LeetCode Problems**
- [Find the Winner of the Circular Game](https://leetcode.com/problems/find-the-winner-of-the-circular-game/) - Josephus problem variant
- [Elimination Game](https://leetcode.com/problems/elimination-game/) - Linear elimination game
- [Last Stone Weight](https://leetcode.com/problems/last-stone-weight/) - Stone elimination problem
- [Last Stone Weight II](https://leetcode.com/problems/last-stone-weight-ii/) - Advanced stone elimination

#### **Problem Categories**
- **Mathematical Algorithms**: Josephus problem, modular arithmetic, recurrence relations
- **Simulation**: Circular elimination, step-by-step simulation, elimination games
- **Mathematical Sequences**: Number sequences, elimination patterns, mathematical formulas
- **Algorithm Design**: Mathematical algorithms, simulation techniques, optimization strategies
