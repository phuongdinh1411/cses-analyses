---
layout: simple
title: "Josephus Problem II
permalink: /problem_soulutions/sorting_and_searching/josephus_problem_ii_analysis/
---

# Josephus Problem II

## Problem Statement
There are n people numbered from 1 to n standing in a circle. Starting from person 1, we eliminate every k-th person until only one person remains. Find the position of the last remaining person.

### Input
The first input line has two integers n and k: the number of people and the step size.

### Output
Print one integer: the position of the last remaining person.

### Constraints
- 1 ≤ n ≤ 10^9
- 1 ≤ k ≤ 10^9

### Example
```
Input:
7 3

Output:
4
```

## Solution Progression

### Approach 1: Simulation - O(n)
**Description**: Simulate the elimination process step by step.

```python
def josephus_problem_ii_naive(n, k):
    people = list(range(1, n + 1))
    index = 0
    
    while len(people) > 1:
        # Eliminate every k-th person
        index = (index + k - 1) % len(people)
        people.pop(index)
    
    return people[0]
```

**Why this is inefficient**: We need to eliminate n-1 people, and each elimination takes O(n) time, leading to O(n²) time complexity.

### Improvement 1: Recursive Formula - O(n)
**Description**: Use the recursive formula for the Josephus problem.

```python
def josephus_problem_ii_optimized(n, k):
    if n == 1:
        return 1
    
    # Recursive formula: J(n,k) = (J(n-1,k) + k) % n
    # If the result is 0, it means the last person is at position n
    result = (josephus_problem_ii_optimized(n - 1, k) + k) % n
    return result if result != 0 else n
```

**Why this improvement works**: The Josephus problem has a recursive solution. If we know the position of the last remaining person for n-1 people, we can calculate it for n people using the formula J(n,k) = (J(n-1,k) + k) % n.

## Final Optimal Solution

```python
n, k = map(int, input().split())

def find_last_remaining_person(n, k):
    if n == 1:
        return 1
    
    # Recursive formula: J(n,k) = (J(n-1,k) + k) % n
    # If the result is 0, it means the last person is at position n
    result = (find_last_remaining_person(n - 1, k) + k) % n
    return result if result != 0 else n

result = find_last_remaining_person(n, k)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Simulation | O(n²) | O(n) | Simulate elimination process |
| Recursive Formula | O(n) | O(n) | Use recursive solution |

## Key Insights for Other Problems

### 1. **Josephus Problems**
**Principle**: Use recursive formulas for efficient solutions to Josephus problems.
**Applicable to**: Josephus problems, elimination problems, recursive problems

### 2. **Recursive Solutions**
**Principle**: Break down problems into smaller subproblems using recursion.
**Applicable to**: Recursive problems, mathematical problems, optimization problems

### 3. **Modular Arithmetic**
**Principle**: Use modular arithmetic to handle circular arrangements efficiently.
**Applicable to**: Circular problems, modular problems, mathematical problems

## Notable Techniques

### 1. **Recursive Josephus Formula**
```python
def josephus_recursive(n, k):
    if n == 1:
        return 1
    
    result = (josephus_recursive(n - 1, k) + k) % n
    return result if result != 0 else n
```

### 2. **Iterative Josephus Formula**
```python
def josephus_iterative(n, k):
    result = 0
    for i in range(2, n + 1):
        result = (result + k) % i
    
    return result + 1
```

### 3. **Modular Arithmetic Handling**
```python
def handle_modular_result(result, n):
    return result if result != 0 else n
```

## Problem-Solving Framework

1. **Identify problem type**: This is a Josephus problem with recursive solution
2. **Choose approach**: Use recursive formula for efficiency
3. **Base case**: Handle n = 1 case
4. **Recursive case**: Use J(n,k) = (J(n-1,k) + k) % n
5. **Handle zero result**: If result is 0, return n
6. **Return result**: Output the position of the last remaining person

---

*This analysis shows how to efficiently solve the Josephus problem using recursive formulas.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Josephus with Different Starting Position**
**Problem**: Start elimination from a different position instead of position 1.
```python
def josephus_different_start(n, k, start_pos):
    if n == 1:
        return start_pos
    
    # Adjust for different starting position
    result = (josephus_different_start(n - 1, k, start_pos) + k) % n
    return result if result != 0 else n
```

#### **Variation 2: Josephus with Variable Step Size**
**Problem**: The step size k changes after each elimination.
```python
def josephus_variable_step(n, step_function):
    # step_function(i) returns the step size for the i-th elimination
    if n == 1:
        return 1
    
    current_step = step_function(n)
    result = (josephus_variable_step(n - 1, step_function) + current_step) % n
    return result if result != 0 else n

# Example: step size increases by 1 each time
def increasing_step(n):
    return n

# Example: step size doubles each time
def doubling_step(n):
    return 2 ** (n - 1)
```

#### **Variation 3: Josephus with Multiple Survivors**
**Problem**: Find the positions of the last m survivors instead of just one.
```python
def josephus_multiple_survivors(n, k, m):
    if n <= m:
        return list(range(1, n + 1))
    
    # Simulate until we have m people left
    people = list(range(1, n + 1))
    index = 0
    
    while len(people) > m:
        index = (index + k - 1) % len(people)
        people.pop(index)
    
    return people
```

#### **Variation 4: Josephus with Reversal**
**Problem**: After each elimination, reverse the direction of counting.
```python
def josephus_with_reversal(n, k):
    people = list(range(1, n + 1))
    index = 0
    direction = 1  # 1 for clockwise, -1 for counterclockwise
    
    while len(people) > 1:
        # Eliminate every k-th person
        index = (index + direction * (k - 1)) % len(people)
        people.pop(index)
        
        # Reverse direction
        direction *= -1
    
    return people[0]
```

#### **Variation 5: Josephus with Skip Pattern**
**Problem**: Skip certain positions during elimination (e.g., skip every other position).
```python
def josephus_with_skip(n, k, skip_pattern):
    # skip_pattern is a function that returns True if position should be skipped
    people = list(range(1, n + 1))
    index = 0
    
    while len(people) > 1:
        # Find next valid position to eliminate
        eliminated = False
        attempts = 0
        
        while not eliminated and attempts < len(people):
            index = (index + k - 1) % len(people)
            
            if not skip_pattern(people[index]):
                people.pop(index)
                eliminated = True
            else:
                index = (index + 1) % len(people)
                attempts += 1
    
    return people[0]

# Example: Skip even numbers
def skip_even(pos):
    return pos % 2 == 0
```

### 🔗 **Related Problems & Concepts**

#### **1. Elimination Problems**
- **Elimination Games**: Games with elimination mechanics
- **Last Man Standing**: Find the last remaining element
- **Survivor Problems**: Problems about surviving elements
- **Elimination Sequences**: Sequences of eliminations

#### **2. Circular Problems**
- **Circular Arrays**: Arrays arranged in circles
- **Circular Traversal**: Traversing circular structures
- **Circular Permutations**: Permutations in circular arrangements
- **Circular Shifts**: Shifting elements in circles

#### **3. Recursive Problems**
- **Recursive Sequences**: Sequences defined recursively
- **Recursive Counting**: Counting using recursion
- **Recursive Elimination**: Elimination using recursion
- **Recursive Patterns**: Patterns in recursive problems

#### **4. Mathematical Problems**
- **Number Theory**: Mathematical properties of numbers
- **Modular Arithmetic**: Arithmetic with remainders
- **Sequences**: Mathematical sequences
- **Patterns**: Mathematical patterns

#### **5. Simulation Problems**
- **Process Simulation**: Simulating processes step by step
- **Game Simulation**: Simulating games
- **Event Simulation**: Simulating events
- **System Simulation**: Simulating systems

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    result = find_last_remaining_person(n, k)
    print(result)
```

#### **2. Range Queries**
```python
# Precompute Josephus results for different n and k values
def precompute_josephus(max_n, max_k):
    dp = {}
    
    for n in range(1, max_n + 1):
        for k in range(1, max_k + 1):
            dp[(n, k)] = find_last_remaining_person(n, k)
    
    return dp

# Answer queries efficiently
def josephus_query(dp, n, k):
    return dp.get((n, k), find_last_remaining_person(n, k))
```

#### **3. Interactive Problems**
```python
# Interactive Josephus game
def interactive_josephus():"
    print("Welcome to the Josephus Problem!")
    
    while True:
        n = int(input("Enter number of people (or 0 to exit): "))
        if n == 0:
            break
        
        k = int(input("Enter step size: "))
        
        if n < 1 or k < 1:
            print("Invalid input!")
            continue
        
        result = find_last_remaining_person(n, k)
        print(f"Last remaining person: {result}")
        
        # Show simulation
        people = list(range(1, n + 1))
        index = 0
        step = 1
        
        print("Elimination sequence:")
        while len(people) > 1:
            index = (index + k - 1) % len(people)
            eliminated = people.pop(index)
            print(f"Step {step}: Eliminated person {eliminated}")
            step += 1
        
        print(f"Final survivor: {people[0]}")
```

### 🧮 **Mathematical Extensions**

#### **1. Number Theory**
- **Modular Arithmetic**: Mathematical foundation for Josephus
- **Number Sequences**: Sequences in Josephus problems
- **Prime Numbers**: Properties related to prime steps
- **Divisibility**: Divisibility properties in Josephus

#### **2. Combinatorics**
- **Permutations**: Arrangements in Josephus problems
- **Combinations**: Combinations of eliminations
- **Counting**: Counting elimination sequences
- **Partitions**: Partitioning people into groups

#### **3. Recurrence Relations**
- **Linear Recurrences**: Linear recurrence in Josephus
- **Non-linear Recurrences**: Non-linear recurrence variations
- **Recurrence Solutions**: Solving recurrence relations
- **Recurrence Patterns**: Patterns in recurrence relations

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Recursive Algorithms**: Core technique for Josephus
- **Iterative Algorithms**: Alternative approach
- **Simulation Algorithms**: Direct simulation approach
- **Mathematical Algorithms**: Mathematical solutions

#### **2. Mathematical Concepts**
- **Modular Arithmetic**: Essential for Josephus problems
- **Recurrence Relations**: Mathematical foundation
- **Number Theory**: Properties of numbers
- **Combinatorics**: Counting and arrangements

#### **3. Programming Concepts**
- **Recursion**: Core programming technique
- **Simulation**: Step-by-step simulation
- **Data Structures**: Efficient data structures
- **Algorithm Design**: Problem-solving strategies

---

*This analysis demonstrates efficient Josephus problem solving techniques and shows various extensions for elimination problems.* 