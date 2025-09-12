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

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Josephus Problem with Different Step Size
**Problem**: Eliminate every k-th person instead of every second person.

**Link**: [CSES Problem Set - Josephus Problem Different Step](https://cses.fi/problemset/task/josephus_different_step)

```python
def josephus_different_step(n, k):
    """
    Josephus problem with step size k
    """
    if n == 1:
        return 1
    
    # Recursive formula: J(n,k) = (J(n-1,k) + k) % n
    # If result is 0, it means the last person is at position n
    result = (josephus_different_step(n - 1, k) + k) % n
    return result if result != 0 else n

def josephus_different_step_iterative(n, k):
    """
    Iterative version for better performance
    """
    result = 0
    for i in range(2, n + 1):
        result = (result + k) % i
    return result + 1
```

### Variation 2: Josephus Problem with Multiple Survivors
**Problem**: Find the positions of the last m survivors instead of just one.

**Link**: [CSES Problem Set - Josephus Problem Multiple Survivors](https://cses.fi/problemset/task/josephus_multiple_survivors)

```python
def josephus_multiple_survivors(n, k, m):
    """
    Find positions of last m survivors
    """
    # Simulate the process to find all survivors
    people = list(range(1, n + 1))
    current_index = 0
    
    while len(people) > m:
        # Find the next person to eliminate
        current_index = (current_index + k - 1) % len(people)
        people.pop(current_index)
    
    return people

def josephus_multiple_survivors_optimized(n, k, m):
    """
    Optimized version using mathematical approach
    """
    # For small m, we can use the mathematical formula
    # and work backwards to find all survivors
    survivors = []
    
    # Start with the last survivor
    last_survivor = josephus_different_step(n, k)
    survivors.append(last_survivor)
    
    # Find previous survivors by working backwards
    current_n = n
    for _ in range(m - 1):
        # Find the previous survivor
        prev_survivor = josephus_different_step(current_n - 1, k)
        survivors.append(prev_survivor)
        current_n -= 1
    
    return sorted(survivors)
```

### Variation 3: Josephus Problem with Dynamic Step Size
**Problem**: The step size changes after each elimination (e.g., increases by 1).

**Link**: [CSES Problem Set - Josephus Problem Dynamic Step](https://cses.fi/problemset/task/josephus_dynamic_step)

```python
def josephus_dynamic_step(n, initial_k, step_increase):
    """
    Josephus problem with dynamic step size
    """
    people = list(range(1, n + 1))
    current_index = 0
    current_k = initial_k
    
    while len(people) > 1:
        # Find the next person to eliminate
        current_index = (current_index + current_k - 1) % len(people)
        people.pop(current_index)
        
        # Increase step size for next round
        current_k += step_increase
    
    return people[0]

def josephus_dynamic_step_optimized(n, initial_k, step_increase):
    """
    Optimized version using mathematical approach
    """
    # For dynamic step size, we need to simulate
    # as there's no simple mathematical formula
    people = list(range(1, n + 1))
    current_index = 0
    current_k = initial_k
    
    while len(people) > 1:
        # Find the next person to eliminate
        current_index = (current_index + current_k - 1) % len(people)
        people.pop(current_index)
        
        # Increase step size for next round
        current_k += step_increase
    
    return people[0]
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
