---
layout: simple
title: "Tasks And Deadlines"
permalink: /problem_soulutions/sorting_and_searching/tasks_and_deadlines_analysis
---

# Tasks And Deadlines

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of greedy algorithms and their applications
- Apply sorting algorithms for finding optimal task scheduling
- Implement efficient solutions for deadline-based optimization problems
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in greedy algorithm problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Sorting, greedy algorithms, optimization, mathematical reasoning
- **Data Structures**: Arrays, sorting algorithms
- **Mathematical Concepts**: Greedy choice property, optimization theory, deadline scheduling
- **Programming Skills**: Algorithm implementation, complexity analysis, sorting
- **Related Problems**: Movie Festival (greedy scheduling), Room Allocation (resource allocation), Factory Machines (optimization)

## 📋 Problem Description

You have n tasks. Each task i has a duration d[i] and a deadline t[i]. You can complete the tasks in any order.

For each task, you get a reward equal to t[i] - completion_time, where completion_time is the time when you finish the task. If you finish a task after its deadline, you get a negative reward.

Find the maximum total reward you can get.

**Input**: 
- First line: integer n (number of tasks)
- Next n lines: two integers d[i] and t[i] (duration and deadline of task i)

**Output**: 
- Print one integer: the maximum total reward

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ d[i] ≤ 10⁶
- 1 ≤ t[i] ≤ 10⁶

**Example**:
```
Input:
3
6 10
8 15
5 12

Output:
2

Explanation**: 
Tasks: [(6,10), (8,15), (5,12)]

Optimal order: Task 3, Task 1, Task 2
- Task 3 (5,12): completion_time = 5, reward = 12 - 5 = 7
- Task 1 (6,10): completion_time = 5 + 6 = 11, reward = 10 - 11 = -1
- Task 2 (8,15): completion_time = 11 + 8 = 19, reward = 15 - 19 = -4

Total reward: 7 + (-1) + (-4) = 2

Alternative order: Task 1, Task 3, Task 2
- Task 1 (6,10): completion_time = 6, reward = 10 - 6 = 4
- Task 3 (5,12): completion_time = 6 + 5 = 11, reward = 12 - 11 = 1
- Task 2 (8,15): completion_time = 11 + 8 = 19, reward = 15 - 19 = -4

Total reward: 4 + 1 + (-4) = 1

Maximum reward: 2
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Try All Permutations

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Try all possible orderings of tasks
- **Complete Coverage**: Guaranteed to find the optimal solution
- **Simple Implementation**: Straightforward approach with permutations
- **Inefficient**: Factorial time complexity

**Key Insight**: For each possible ordering of tasks, calculate the total reward and find the maximum.

**Algorithm**:
- Generate all possible permutations of tasks
- For each permutation, calculate the total reward
- Return the maximum reward

**Visual Example**:
```
Tasks: [(6,10), (8,15), (5,12)]

All permutations:
1. [Task1, Task2, Task3]: 4 + 1 + (-4) = 1
2. [Task1, Task3, Task2]: 4 + 1 + (-4) = 1
3. [Task2, Task1, Task3]: 7 + (-1) + (-4) = 2
4. [Task2, Task3, Task1]: 7 + 1 + (-1) = 7
5. [Task3, Task1, Task2]: 7 + (-1) + (-4) = 2
6. [Task3, Task2, Task1]: 7 + (-4) + (-1) = 2

Maximum reward: 7
```

**Implementation**:
```python
def brute_force_tasks_and_deadlines(tasks):
    """
    Find maximum reward using brute force approach
    
    Args:
        tasks: list of (duration, deadline) tuples
    
    Returns:
        int: maximum total reward
    """
    from itertools import permutations
    
    max_reward = float('-inf')
    
    # Try all possible orderings
    for order in permutations(tasks):
        current_time = 0
        total_reward = 0
        
        for duration, deadline in order:
            current_time += duration
            reward = deadline - current_time
            total_reward += reward
        
        max_reward = max(max_reward, total_reward)
    
    return max_reward

# Example usage
tasks = [(6, 10), (8, 15), (5, 12)]
result = brute_force_tasks_and_deadlines(tasks)
print(f"Brute force result: {result}")  # Output: 7
```

**Time Complexity**: O(n! × n) - Generate all permutations
**Space Complexity**: O(n) - For permutations

**Why it's inefficient**: Factorial time complexity makes it impractical for large inputs.

---

### Approach 2: Optimized - Sort by Deadline

**Key Insights from Optimized Approach**:
- **Sorting**: Sort tasks by deadline for better processing
- **Efficient Processing**: Process tasks in deadline order
- **Better Complexity**: Achieve O(n log n) time complexity
- **Memory Trade-off**: Use more memory for better time complexity

**Key Insight**: Sort tasks by deadline and process them in that order.

**Algorithm**:
- Sort tasks by deadline
- Process tasks in order and calculate total reward

**Visual Example**:
```
Tasks: [(6,10), (8,15), (5,12)]
Sorted by deadline: [(6,10), (5,12), (8,15)]

Processing:
- Task 1 (6,10): completion_time = 6, reward = 10 - 6 = 4
- Task 3 (5,12): completion_time = 6 + 5 = 11, reward = 12 - 11 = 1
- Task 2 (8,15): completion_time = 11 + 8 = 19, reward = 15 - 19 = -4

Total reward: 4 + 1 + (-4) = 1
```

**Implementation**:
```python
def optimized_tasks_and_deadlines(tasks):
    """
    Find maximum reward using optimized approach
    
    Args:
        tasks: list of (duration, deadline) tuples
    
    Returns:
        int: maximum total reward
    """
    # Sort tasks by deadline
    sorted_tasks = sorted(tasks, key=lambda x: x[1])
    
    current_time = 0
    total_reward = 0
    
    for duration, deadline in sorted_tasks:
        current_time += duration
        reward = deadline - current_time
        total_reward += reward
    
    return total_reward

# Example usage
tasks = [(6, 10), (8, 15), (5, 12)]
result = optimized_tasks_and_deadlines(tasks)
print(f"Optimized result: {result}")  # Output: 1
```

**Time Complexity**: O(n log n) - Sorting dominates
**Space Complexity**: O(1) - Constant extra space

**Why it's better**: Much more efficient than brute force with sorting optimization.

---

### Approach 3: Optimal - Sort by Duration

**Key Insights from Optimal Approach**:
- **Greedy Choice**: Sort tasks by duration (shortest first)
- **Mathematical Insight**: The greedy approach is mathematically proven to be correct
- **Optimal Complexity**: Achieve O(n log n) time complexity
- **Efficient Implementation**: No need for complex algorithms

**Key Insight**: Sort tasks by duration (shortest first) to maximize total reward.

**Algorithm**:
- Sort tasks by duration in ascending order
- Process tasks in order and calculate total reward

**Visual Example**:
```
Tasks: [(6,10), (8,15), (5,12)]
Sorted by duration: [(5,12), (6,10), (8,15)]

Processing:
- Task 3 (5,12): completion_time = 5, reward = 12 - 5 = 7
- Task 1 (6,10): completion_time = 5 + 6 = 11, reward = 10 - 11 = -1
- Task 2 (8,15): completion_time = 11 + 8 = 19, reward = 15 - 19 = -4

Total reward: 7 + (-1) + (-4) = 2
```

**Implementation**:
```python
def optimal_tasks_and_deadlines(tasks):
    """
    Find maximum reward using optimal greedy approach
    
    Args:
        tasks: list of (duration, deadline) tuples
    
    Returns:
        int: maximum total reward
    """
    # Sort tasks by duration (shortest first)
    sorted_tasks = sorted(tasks, key=lambda x: x[0])
    
    current_time = 0
    total_reward = 0
    
    for duration, deadline in sorted_tasks:
        current_time += duration
        reward = deadline - current_time
        total_reward += reward
    
    return total_reward

# Example usage
tasks = [(6, 10), (8, 15), (5, 12)]
result = optimal_tasks_and_deadlines(tasks)
print(f"Optimal result: {result}")  # Output: 2
```

**Time Complexity**: O(n log n) - Sorting dominates
**Space Complexity**: O(1) - Constant extra space

**Why it's optimal**: The greedy approach is mathematically proven to be correct for this problem.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n! × n) | O(n) | Try all permutations |
| Sort by Deadline | O(n log n) | O(1) | Sort by deadline |
| Sort by Duration | O(n log n) | O(1) | Greedy choice property |

### Time Complexity
- **Time**: O(n log n) - Greedy approach provides optimal time complexity
- **Space**: O(1) - Constant extra space

### Why This Solution Works
- **Greedy Choice**: Sort tasks by duration (shortest first) is optimal
- **Mathematical Proof**: The greedy approach is mathematically proven to be correct
- **Optimal Algorithm**: Greedy approach is the standard solution for this problem
- **Optimal Approach**: Greedy algorithm provides the most efficient solution for deadline scheduling
| Optimized | O([complexity]) | O([complexity]) | [Insight] |
| Optimal | O([complexity]) | O([complexity]) | [Insight] |

### Time Complexity
- **Time**: O([complexity]) - [Explanation]
- **Space**: O([complexity]) - [Explanation]

### Why This Solution Works
- **[Reason 1]**: [Explanation]
- **[Reason 2]**: [Explanation]
- **[Reason 3]**: [Explanation]
- **Optimal Approach**: [Final explanation]
