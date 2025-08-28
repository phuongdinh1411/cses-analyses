---
layout: simple
title: "Tasks and Deadlines
permalink: /problem_soulutions/sorting_and_searching/tasks_and_deadlines_analysis/"
---


# Tasks and Deadlines

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

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Tasks with Priority and Deadlines**
**Problem**: Tasks have priority levels. Higher priority tasks must be completed first.
```python
def tasks_with_priority_and_deadlines(n, tasks, priorities):
    # tasks[i] = (duration, deadline), priorities[i] = priority level
    task_data = [(tasks[i][0], tasks[i][1], priorities[i], i) for i in range(n)]
    
    # Sort by priority (higher first), then by deadline
    task_data.sort(key=lambda x: (-x[2], x[1]))
    
    current_time = 0
    profit = 0
    
    for duration, deadline, priority, task_id in task_data:
        current_time += duration
        profit += max(0, deadline - current_time)
    
    return profit
```

#### **Variation 2: Tasks with Dependencies**
**Problem**: Some tasks must be completed before others.
```python
def tasks_with_dependencies(n, tasks, dependencies):
    # dependencies[i] = list of tasks that must be completed before task i
    from collections import defaultdict, deque
    
    # Build dependency graph
    graph = defaultdict(list)
    in_degree = [0] * n
    
    for i, deps in enumerate(dependencies):
        for dep in deps:
            graph[dep].append(i)
            in_degree[i] += 1
    
    # Topological sort with profit calculation
    queue = deque()
    completion_time = [0] * n
    profit = 0
    
    # Add tasks with no dependencies
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    
    while queue:
        task = queue.popleft()
        duration, deadline = tasks[task]
        
        # Calculate completion time
        completion_time[task] = completion_time[task] + duration
        profit += max(0, deadline - completion_time[task])
        
        # Update dependent tasks
        for next_task in graph[task]:
            in_degree[next_task] -= 1
            completion_time[next_task] = max(completion_time[next_task], completion_time[task])
            
            if in_degree[next_task] == 0:
                queue.append(next_task)
    
    return profit if max(in_degree) == 0 else -1
```

#### **Variation 3: Tasks with Resource Constraints**
**Problem**: Limited resources available. Each task requires specific resources.
```python
def tasks_with_resource_constraints(n, tasks, resource_requirements, available_resources):
    # resource_requirements[i] = list of resources needed for task i
    # available_resources = total available resources
    task_data = [(tasks[i][0], tasks[i][1], resource_requirements[i], i) for i in range(n)]
    
    # Sort by deadline
    task_data.sort(key=lambda x: x[1])
    
    current_time = 0
    profit = 0
    used_resources = set()
    
    for duration, deadline, resources, task_id in task_data:
        # Check if we have required resources
        can_execute = True
        for resource in resources:
            if resource in used_resources:
                can_execute = False
                break
        
        if can_execute:
            current_time += duration
            profit += max(0, deadline - current_time)
            
            # Mark resources as used
            for resource in resources:
                used_resources.add(resource)
    
    return profit
```

#### **Variation 4: Tasks with Dynamic Deadlines**
**Problem**: Deadlines can be extended with penalties.
```python
def tasks_with_dynamic_deadlines(n, tasks, extension_costs):
    # extension_costs[i] = cost to extend deadline of task i by 1 unit
    task_data = [(tasks[i][0], tasks[i][1], extension_costs[i], i) for i in range(n)]
    
    # Sort by deadline
    task_data.sort(key=lambda x: x[1])
    
    current_time = 0
    profit = 0
    
    for duration, deadline, extension_cost, task_id in task_data:
        current_time += duration
        
        if current_time > deadline:
            # Calculate optimal extension
            extension_needed = current_time - deadline
            extension_cost_total = extension_needed * extension_cost
            profit += max(0, deadline - current_time) - extension_cost_total
        else:
            profit += max(0, deadline - current_time)
    
    return profit
```

#### **Variation 5: Tasks with Parallel Execution**
**Problem**: Some tasks can be executed in parallel.
```python
def tasks_with_parallel_execution(n, tasks, parallel_groups):
    # parallel_groups[i] = list of tasks that can be executed in parallel with task i
    from collections import defaultdict
    
    # Build parallel execution graph
    parallel_graph = defaultdict(list)
    for i, group in enumerate(parallel_groups):
        for task in group:
            parallel_graph[i].append(task)
            parallel_graph[task].append(i)
    
    # Find connected components (parallel groups)
    visited = [False] * n
    components = []
    
    def dfs(node, component):
        visited[node] = True
        component.append(node)
        for neighbor in parallel_graph[node]:
            if not visited[neighbor]:
                dfs(neighbor, component)
    
    for i in range(n):
        if not visited[i]:
            component = []
            dfs(i, component)
            components.append(component)
    
    # Process each component optimally
    total_profit = 0
    current_time = 0
    
    for component in components:
        # Sort tasks in component by deadline
        component_tasks = [(tasks[i][0], tasks[i][1]) for i in component]
        component_tasks.sort(key=lambda x: x[1])
        
        # Execute tasks in parallel (minimum duration)
        min_duration = min(task[0] for task in component_tasks)
        current_time += min_duration
        
        # Calculate profit
        for duration, deadline in component_tasks:
            total_profit += max(0, deadline - current_time)
    
    return total_profit
```

### 🔗 **Related Problems & Concepts**

#### **1. Scheduling Problems**
- **Job Scheduling**: Schedule jobs on machines optimally
- **Interval Scheduling**: Schedule non-overlapping intervals
- **Resource Scheduling**: Schedule limited resources
- **Task Scheduling**: Schedule tasks with constraints

#### **2. Optimization Problems**
- **Linear Programming**: Formulate as LP problem
- **Integer Programming**: Discrete optimization
- **Combinatorial Optimization**: Optimize discrete structures
- **Approximation Algorithms**: Find approximate solutions

#### **3. Greedy Algorithm Problems**
- **Activity Selection**: Select maximum activities
- **Fractional Knapsack**: Fill knapsack optimally
- **Huffman Coding**: Build optimal prefix codes"
- **Dijkstra's Algorithm**: Find shortest paths

#### **4. Graph Theory Problems**
- **Topological Sort**: Sort nodes in directed acyclic graph
- **Dependency Resolution**: Resolve dependencies between tasks
- **Critical Path**: Find critical path in project
- **Task Dependencies**: Handle task dependencies

#### **5. Dynamic Programming Problems**
- **Job Scheduling**: Dynamic programming for job scheduling
- **Resource Allocation**: Dynamic resource allocation
- **Task Assignment**: Dynamic task assignment
- **Scheduling Optimization**: Dynamic scheduling optimization

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n = int(input())
    tasks = []
    for _ in range(n):
        d, x = map(int, input().split())
        tasks.append((d, x))
    
    # Sort tasks by deadline
    tasks.sort(key=lambda x: x[1])
    
    current_time = 0
    profit = 0
    
    for duration, deadline in tasks:
        current_time += duration
        profit += max(0, deadline - current_time)
    
    print(profit)
```

#### **2. Range Queries**
```python
# Precompute profits for different task subsets
def precompute_task_profits(tasks):
    n = len(tasks)
    profit_matrix = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(i, n):
            subset_tasks = tasks[i:j+1]
            subset_tasks.sort(key=lambda x: x[1])
            
            current_time = 0
            profit = 0
            
            for duration, deadline in subset_tasks:
                current_time += duration
                profit += max(0, deadline - current_time)
            
            profit_matrix[i][j] = profit
    
    return profit_matrix

# Answer queries about profits for task subsets
def profit_query(profit_matrix, l, r):
    return profit_matrix[l][r]
```

#### **3. Interactive Problems**
```python
# Interactive task scheduler
def interactive_task_scheduler():
    n = int(input("Enter number of tasks: "))
    tasks = []
    
    for i in range(n):
        duration = int(input(f"Enter duration for task {i+1}: "))
        deadline = int(input(f"Enter deadline for task {i+1}: "))
        tasks.append((duration, deadline))
    
    print(f"Tasks: {tasks}")
    
    # Sort by deadline
    tasks.sort(key=lambda x: x[1])
    print(f"Sorted tasks by deadline: {tasks}")
    
    current_time = 0
    profit = 0
    
    for i, (duration, deadline) in enumerate(tasks):
        current_time += duration
        task_profit = max(0, deadline - current_time)
        profit += task_profit
        
        print(f"\nTask {i+1}: duration={duration}, deadline={deadline}")
        print(f"Completion time: {current_time}")
        print(f"Task profit: {task_profit}")
        print(f"Total profit so far: {profit}")
    
    print(f"\nFinal profit: {profit}")
```

### 🧮 **Mathematical Extensions**

#### **1. Scheduling Theory**
- **Scheduling Algorithms**: Theory of scheduling algorithms
- **Resource Allocation**: Mathematical resource allocation
- **Optimization Theory**: Mathematical optimization
- **Queueing Theory**: Mathematical queueing theory

#### **2. Algorithm Analysis**
- **Complexity Analysis**: Time and space complexity
- **Greedy Correctness**: Proving greedy choice property
- **Optimal Substructure**: Proving optimal substructure
- **Lower Bounds**: Establishing problem lower bounds

#### **3. Operations Research**
- **Linear Programming**: Formulate scheduling as LP
- **Integer Programming**: Discrete scheduling optimization
- **Network Flow**: Maximum flow applications
- **Combinatorial Optimization**: Discrete optimization

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Greedy Algorithms**: Local optimal choices
- **Scheduling Algorithms**: Efficient scheduling algorithms
- **Optimization Algorithms**: Mathematical optimization
- **Dynamic Programming**: Optimal substructure

#### **2. Mathematical Concepts**
- **Scheduling Theory**: Mathematical scheduling
- **Optimization**: Mathematical optimization theory
- **Operations Research**: Mathematical operations research
- **Algorithm Analysis**: Complexity and correctness

#### **3. Programming Concepts**
- **Greedy Algorithm Design**: Problem-solving strategies
- **Scheduling Implementation**: Efficient scheduling techniques
- **Algorithm Design**: Problem-solving strategies
- **Resource Management**: Efficient resource handling

---

*This analysis demonstrates scheduling and optimization techniques for task management problems.* 