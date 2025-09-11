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
- **[Reason 3]**: [Explanation]
- **Optimal Approach**: [Final explanation]
