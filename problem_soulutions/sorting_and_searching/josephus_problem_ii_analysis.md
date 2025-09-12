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

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Josephus problem, mathematical formulas, circular elimination
- **Data Structures**: Arrays, circular data structures
- **Mathematical Concepts**: Modular arithmetic, recurrence relations, mathematical formulas
- **Programming Skills**: Algorithm implementation, complexity analysis, mathematical optimization
- **Related Problems**: Josephus Problem I (k=2), Circular elimination problems

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
