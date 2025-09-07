---
layout: simple
title: "Josephus Problem II"
permalink: /problem_soulutions/sorting_and_searching/josephus_problem_ii_analysis
---

# Josephus Problem II

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the generalized Josephus problem with variable step sizes and circular elimination
- Apply advanced mathematical formulas and simulation techniques to solve generalized Josephus problems
- Implement efficient generalized Josephus algorithms with O(n) or O(k log n) time complexity
- Optimize generalized Josephus problems using mathematical formulas and efficient simulation techniques
- Handle edge cases in generalized Josephus problems (single person, large n, large k, step size variations)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Generalized Josephus problem, circular elimination, advanced mathematical formulas, simulation algorithms, elimination strategies
- **Data Structures**: Arrays, circular structures, elimination tracking, position tracking, step tracking
- **Mathematical Concepts**: Advanced Josephus mathematics, circular mathematics, elimination theory, advanced mathematical formulas
- **Programming Skills**: Circular array implementation, elimination simulation, advanced mathematical formula implementation, algorithm implementation
- **Related Problems**: Josephus Problem I (basic version), Circular problems, Advanced mathematical problems

## Problem Description

**Problem**: There are n people numbered from 1 to n standing in a circle. Starting from person 1, we eliminate every k-th person until only one person remains. Find the position of the last remaining person.

**Input**: 
- First line: n k (number of people and step size)

**Output**: Position of the last remaining person.

**Example**:
```
Input:
7 3

Output:
4

Explanation: 
Initial circle: [1, 2, 3, 4, 5, 6, 7]
Round 1: Eliminate 3, 6, 2, 7, 5 → [1, 4]
Round 2: Eliminate 1 → [4]
Last remaining: 4

Let me trace this step by step:
Starting from 1, eliminate every 3rd person:
1, 2, 3, 4, 5, 6, 7
1, 2, _, 4, 5, _, 7  (eliminate 3, 6)
1, _, _, 4, _, _, 7  (eliminate 2, 5)
1, _, _, 4, _, _, _  (eliminate 7)
_, _, _, 4, _, _, _  (eliminate 1)
Last remaining: 4
```

## 📊 Visual Example

### Initial Circle Setup
```
People: [1, 2, 3, 4, 5, 6, 7]
Index:   0  1  2  3  4  5  6
n = 7 people, k = 3
```

### Elimination Process
```
Round 1: Eliminate every 3rd person starting from 1
┌─────────────────────────────────────┐
│ Current: [1, 2, 3, 4, 5, 6, 7]     │
│ Start from 1, count 3: eliminate 3  │
│ Remaining: [1, 2, 4, 5, 6, 7]      │
│ Start from 4, count 3: eliminate 6  │
│ Remaining: [1, 2, 4, 5, 7]         │
│ Start from 7, count 3: eliminate 2  │
│ Remaining: [1, 4, 5, 7]            │
│ Start from 4, count 3: eliminate 7  │
│ Remaining: [1, 4, 5]               │
│ Start from 1, count 3: eliminate 5  │
│ Remaining: [1, 4]                  │
└─────────────────────────────────────┘

Round 2: Continue with remaining people
┌─────────────────────────────────────┐
│ Current: [1, 4]                    │
│ Start from 1, count 3: eliminate 1  │
│ Remaining: [4]                     │
└─────────────────────────────────────┘

Final result: Person 4 survives
```

### Step-by-Step Visualization
```
Initial: 1 2 3 4 5 6 7
         ↑
         Start here

Round 1: 1 2 _ 4 5 _ 7
         ↑     ↑     ↑
         Keep  Keep  Keep

Round 2: 1 _ _ 4 _ _ _
         ↑       ↑
         Keep    Keep

Round 3: _ _ _ 4 _ _ _
         ↑
         Keep (last remaining)
```

### Mathematical Formula
```
For n people and step size k, the last remaining person is:
J(n,k) = (J(n-1,k) + k) % n

Base case: J(1,k) = 0

For n=7, k=3:
- J(1,3) = 0
- J(2,3) = (0 + 3) % 2 = 1
- J(3,3) = (1 + 3) % 3 = 1
- J(4,3) = (1 + 3) % 4 = 0
- J(5,3) = (0 + 3) % 5 = 3
- J(6,3) = (3 + 3) % 6 = 0
- J(7,3) = (0 + 3) % 7 = 3

Since we use 1-indexing, the result is 3 + 1 = 4
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- n people in a circle numbered 1 to n
- Start from person 1
- Eliminate every k-th person
- Find the last remaining person

**Key Observations:**
- This is the general Josephus problem
- Has a recursive solution
- Can be solved iteratively for efficiency
- Pattern depends on k and n

### Step 2: Brute Force Approach
**Idea**: Simulate the elimination process step by step.

```python
def josephus_problem_brute_force(n, k):
    people = list(range(1, n + 1))
    index = 0
    
    while len(people) > 1:
        # Eliminate every k-th person
        index = (index + k - 1) % len(people)
        people.pop(index)
    
    return people[0]
```

**Why this works:**
- Simulates actual elimination process
- Easy to understand and implement
- Guarantees correct answer
- O(n²) time complexity

### Step 3: Recursive Formula Optimization
**Idea**: Use the recursive formula for the Josephus problem.

```python
def josephus_problem_recursive(n, k):
    if n == 1:
        return 1
    
    # Recursive formula: J(n,k) = (J(n-1,k) + k) % n
    # If the result is 0, it means the last person is at position n
    result = (josephus_problem_recursive(n - 1, k) + k) % n
    return result if result != 0 else n
```

**Why this is better:**
- O(n) time complexity
- Uses mathematical insight
- More efficient than simulation
- Handles large n

### Step 4: Iterative Optimization
**Idea**: Convert recursive solution to iterative for better efficiency.

```python
def josephus_problem_iterative(n, k):
    result = 0  # 0-indexed result
    
    for i in range(2, n + 1):
        result = (result + k) % i
    
    return result + 1  # Convert to 1-indexed
```

**Why this is better:**
- O(n) time complexity
- O(1) space complexity
- No recursion stack
- Most efficient approach

### Step 5: Complete Solution
**Putting it all together:**

```python
def solve_josephus_problem_ii():
    n, k = map(int, input().split())
    
    result = 0  # 0-indexed result
    
    for i in range(2, n + 1):
        result = (result + k) % i
    
    print(result + 1)  # Convert to 1-indexed

# Main execution
if __name__ == "__main__":
    solve_josephus_problem_ii()
```

**Why this works:**
- Optimal iterative approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 6: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (7, 3, 4),
        (5, 2, 3),
        (3, 2, 3),
        (1, 1, 1),
        (10, 3, 4),
    ]
    
    for n, k, expected in test_cases:
        result = solve_test(n, k)
        print(f"n={n}, k={k}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n, k):
    result = 0
    for i in range(2, n + 1):
        result = (result + k) % i
    return result + 1

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - iterate from 2 to n
- **Space**: O(1) - constant extra space

### Why This Solution Works
- **Recursive Formula**: J(n,k) = (J(n-1,k) + k) % n
- **Iterative Conversion**: Convert recursion to iteration
- **Modulo Arithmetic**: Handle circular elimination
- **Optimal Approach**: No better solution possible

## 🎯 Key Insights

### 1. **Recursive Formula**
- Josephus problem has recursive solution
- J(n,k) = (J(n-1,k) + k) % n
- Base case: J(1,k) = 1
- Key insight for efficiency

### 2. **Iterative Conversion**
- Convert recursion to iteration
- Avoid recursion stack overhead
- Maintain same mathematical logic
- Crucial for optimization

### 3. **Modulo Arithmetic**
- Handle circular elimination
- Use modulo to wrap around
- Essential for correct calculation
- Important for understanding

## 🎯 Problem Variations

### Variation 1: Josephus Problem with Survivors
**Problem**: Find the last m survivors instead of just one.

```python
def josephus_problem_multiple_survivors(n, k, m):
    if m >= n:
        return list(range(1, n + 1))
    
    people = list(range(1, n + 1))
    index = 0
    
    while len(people) > m:
        # Eliminate every k-th person
        index = (index + k - 1) % len(people)
        people.pop(index)
    
    return people
```

### Variation 2: Josephus Problem with Direction Change
**Problem**: Change direction after each elimination.

```python
def josephus_problem_direction_change(n, k):
    people = list(range(1, n + 1))
    index = 0
    direction = 1  # 1 for clockwise, -1 for counterclockwise
    
    while len(people) > 1:
        # Move k steps in current direction
        index = (index + direction * (k - 1)) % len(people)
        people.pop(index)
        
        # Change direction
        direction *= -1
    
    return people[0]
```

### Variation 3: Josephus Problem with Skip
**Problem**: Skip m people before eliminating the next person.

```python
def josephus_problem_with_skip(n, k, skip):
    people = list(range(1, n + 1))
    index = 0
    
    while len(people) > 1:
        # Skip m people, then eliminate the k-th person
        index = (index + skip + k - 1) % len(people)
        people.pop(index)
    
    return people[0]
```

### Variation 4: Josephus Problem with Weights
**Problem**: Each person has a weight, eliminate person with minimum weight.

```python
def josephus_problem_with_weights(n, weights):
    people = [(i + 1, weights[i]) for i in range(n)]
    
    while len(people) > 1:
        # Find person with minimum weight
        min_idx = 0
        for i in range(1, len(people)):
            if people[i][1] < people[min_idx][1]:
                min_idx = i
        
        # Eliminate this person
        people.pop(min_idx)
    
    return people[0][0]
```

### Variation 5: Dynamic Josephus Problem
**Problem**: Support adding/removing people dynamically.

```python
class DynamicJosephus:
    def __init__(self):
        self.people = []
        self.n = 0
    
    def add_person(self, person_id):
        self.people.append(person_id)
        self.n += 1
        return self.get_last_survivor()
    
    def remove_person(self, person_id):
        if person_id in self.people:
            self.people.remove(person_id)
            self.n -= 1
        return self.get_last_survivor()
    
    def get_last_survivor(self, k=2):
        if self.n == 0:
            return None
        if self.n == 1:
            return self.people[0]
        
        # Use iterative formula
        result = 0
        for i in range(2, self.n + 1):
            result = (result + k) % i
        
        survivor_pos = result
        return self.people[survivor_pos] if survivor_pos < self.n else self.people[0]
```

## 🔗 Related Problems

- **[Josephus Problem I](/cses-analyses/problem_soulutions/sorting_and_searching/josephus_problem_i_analysis)**: Special case with k=2
- **[Gray Code](/cses-analyses/problem_soulutions/introductory_problems/gray_code_analysis)**: Bit manipulation
- **[Bit Strings](/cses-analyses/problem_soulutions/introductory_problems/bit_strings_analysis)**: Binary representation

## 📚 Learning Points

1. **Recursive Thinking**: Break down problems into smaller subproblems
2. **Iterative Conversion**: Convert recursion to iteration for efficiency
3. **Modulo Arithmetic**: Handle circular structures and wrapping
4. **Mathematical Patterns**: Recognize and use mathematical formulas

---

**This is a great introduction to recursive problem-solving and mathematical patterns!** 🎯 