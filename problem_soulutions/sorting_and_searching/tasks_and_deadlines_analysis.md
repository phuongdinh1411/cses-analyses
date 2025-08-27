# CSES Tasks and Deadlines - Problem Analysis

## Problem Statement
Given n tasks, each with a duration and deadline, find the maximum profit that can be obtained. The profit for a task is deadline - completion_time, and completion_time is the sum of durations of all tasks completed before it plus its own duration.

### Input
The first input line has an integer n: the number of tasks.
Then there are n lines. Each line has two integers d and x: the duration and deadline of a task.

### Output
Print one integer: the maximum profit.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ d,x ≤ 10^9

### Example
```
Input:
3
6 10
8 15
5 12

Output:
17
```

## Solution Progression

### Approach 1: Brute Force - O(n!)
**Description**: Try all possible orderings of tasks.

```python
def tasks_and_deadlines_naive(n, tasks):
    from itertools import permutations
    
    max_profit = 0
    
    for order in permutations(range(n)):
        current_time = 0
        profit = 0
        
        for task_idx in order:
            duration, deadline = tasks[task_idx]
            current_time += duration
            profit += max(0, deadline - current_time)
        
        max_profit = max(max_profit, profit)
    
    return max_profit
```

**Why this is inefficient**: We try all n! possible orderings, leading to factorial time complexity.

### Improvement 1: Greedy by Deadline - O(n log n)
**Description**: Sort tasks by deadline and process them in order.

```python
def tasks_and_deadlines_optimized(n, tasks):
    # Sort tasks by deadline (ascending)
    tasks.sort(key=lambda x: x[1])
    
    current_time = 0
    profit = 0
    
    for duration, deadline in tasks:
        current_time += duration
        profit += max(0, deadline - current_time)
    
    return profit
```

**Why this improvement works**: The optimal strategy is to process tasks in order of increasing deadline. This ensures that we complete tasks with earlier deadlines first, maximizing the profit.

## Final Optimal Solution

```python
n = int(input())
tasks = []
for _ in range(n):
    d, x = map(int, input().split())
    tasks.append((d, x))

def find_maximum_profit(n, tasks):
    # Sort tasks by deadline (ascending)
    tasks.sort(key=lambda x: x[1])
    
    current_time = 0
    profit = 0
    
    for duration, deadline in tasks:
        current_time += duration
        profit += max(0, deadline - current_time)
    
    return profit

result = find_maximum_profit(n, tasks)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n!) | O(n) | Try all possible orderings |
| Greedy by Deadline | O(n log n) | O(1) | Sort by deadline for optimal order |

## Key Insights for Other Problems

### 1. **Task Scheduling Problems**
**Principle**: Sort tasks by deadline to maximize profit in scheduling problems.
**Applicable to**: Scheduling problems, deadline problems, optimization problems

### 2. **Greedy Scheduling**
**Principle**: Process tasks with earlier deadlines first to maximize profit.
**Applicable to**: Greedy algorithms, scheduling problems, deadline-based problems

### 3. **Profit Maximization**
**Principle**: Calculate profit as deadline - completion_time and maximize total profit.
**Applicable to**: Profit problems, optimization problems, scheduling problems

## Notable Techniques

### 1. **Deadline-based Sorting**
```python
def sort_by_deadline(tasks):
    return sorted(tasks, key=lambda x: x[1])
```

### 2. **Profit Calculation**
```python
def calculate_profit(tasks):
    current_time = 0
    profit = 0
    
    for duration, deadline in tasks:
        current_time += duration
        profit += max(0, deadline - current_time)
    
    return profit
```

### 3. **Greedy Task Processing**
```python
def process_tasks_greedily(tasks):
    # Sort by deadline
    sorted_tasks = sort_by_deadline(tasks)
    
    # Process in order
    return calculate_profit(sorted_tasks)
```

## Problem-Solving Framework

1. **Identify problem type**: This is a task scheduling problem with deadline constraints
2. **Choose approach**: Use greedy approach by sorting by deadline
3. **Sort tasks**: Sort tasks by deadline in ascending order
4. **Process tasks**: Process tasks in sorted order
5. **Calculate profit**: For each task, calculate profit as deadline - completion_time
6. **Track time**: Maintain current completion time
7. **Return result**: Output the maximum total profit

---

*This analysis shows how to efficiently maximize profit in task scheduling using greedy approach by deadline.* 