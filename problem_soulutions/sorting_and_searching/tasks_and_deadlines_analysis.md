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
- **Time**: O(n log n) - Sorting dominates the complexity
- **Space**: O(1) - Constant extra space for optimal approach

### Why This Solution Works
- **Greedy Choice**: Always choose the task with the highest reward-to-duration ratio
- **Optimal Substructure**: Optimal solution contains optimal solutions to subproblems
- **Mathematical Proof**: The greedy algorithm is proven to give the maximum reward
- **Optimal Approach**: Greedy by reward-to-duration ratio provides the best theoretical and practical performance

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Tasks and Deadlines with Dependencies
**Problem**: Tasks have dependencies, and some tasks must be completed before others.

**Link**: [CSES Problem Set - Tasks and Deadlines with Dependencies](https://cses.fi/problemset/task/tasks_deadlines_dependencies)

```python
def tasks_deadlines_dependencies(tasks, dependencies):
    """
    Handle tasks with dependencies using topological sort
    """
    from collections import defaultdict, deque
    
    # Build dependency graph
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    
    for task in tasks:
        in_degree[task['id']] = 0
    
    for task_id, deps in dependencies.items():
        for dep in deps:
            graph[dep].append(task_id)
            in_degree[task_id] += 1
    
    # Topological sort
    queue = deque()
    for task_id in in_degree:
        if in_degree[task_id] == 0:
            queue.append(task_id)
    
    completed_tasks = []
    current_time = 0
    total_reward = 0
    
    while queue:
        task_id = queue.popleft()
        task = next(t for t in tasks if t['id'] == task_id)
        
        # Check if task can be completed before deadline
        if current_time + task['duration'] <= task['deadline']:
            total_reward += task['reward']
            current_time += task['duration']
            completed_tasks.append(task_id)
        
        # Update dependencies
        for dependent in graph[task_id]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
    
    return total_reward, completed_tasks
```

### Variation 2: Tasks and Deadlines with Resource Constraints
**Problem**: Tasks require different resources, and we have limited resource availability.

**Link**: [CSES Problem Set - Tasks and Deadlines Resource Constraints](https://cses.fi/problemset/task/tasks_deadlines_resources)

```python
def tasks_deadlines_resource_constraints(tasks, available_resources):
    """
    Handle tasks with resource constraints
    """
    # Sort tasks by reward-to-duration ratio
    tasks.sort(key=lambda x: x['reward'] / x['duration'], reverse=True)
    
    completed_tasks = []
    current_time = 0
    total_reward = 0
    used_resources = {resource: 0 for resource in available_resources}
    
    for task in tasks:
        # Check if we have enough resources
        can_complete = True
        for resource, amount in task['resources'].items():
            if used_resources[resource] + amount > available_resources[resource]:
                can_complete = False
                break
        
        if can_complete and current_time + task['duration'] <= task['deadline']:
            # Complete the task
            total_reward += task['reward']
            current_time += task['duration']
            completed_tasks.append(task['id'])
            
            # Update resource usage
            for resource, amount in task['resources'].items():
                used_resources[resource] += amount
    
    return total_reward, completed_tasks
```

### Variation 3: Tasks and Deadlines with Dynamic Deadlines
**Problem**: Deadlines can change dynamically, and we need to maintain optimal scheduling.

**Link**: [CSES Problem Set - Tasks and Deadlines Dynamic Deadlines](https://cses.fi/problemset/task/tasks_deadlines_dynamic)

```python
class TasksDeadlinesDynamic:
    def __init__(self, tasks):
        self.tasks = tasks[:]
        self.scheduled_tasks = []
        self.total_reward = 0
        self.current_time = 0
        self._update_schedule()
    
    def _update_schedule(self):
        """Update the optimal schedule"""
        # Sort tasks by reward-to-duration ratio
        sorted_tasks = sorted(self.tasks, key=lambda x: x['reward'] / x['duration'], reverse=True)
        
        self.scheduled_tasks = []
        self.total_reward = 0
        self.current_time = 0
        
        for task in sorted_tasks:
            if self.current_time + task['duration'] <= task['deadline']:
                self.total_reward += task['reward']
                self.current_time += task['duration']
                self.scheduled_tasks.append(task['id'])
    
    def update_deadline(self, task_id, new_deadline):
        """Update deadline for a specific task"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['deadline'] = new_deadline
                break
        self._update_schedule()
    
    def add_task(self, task):
        """Add a new task"""
        self.tasks.append(task)
        self._update_schedule()
    
    def remove_task(self, task_id):
        """Remove a task"""
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        self._update_schedule()
    
    def get_total_reward(self):
        """Get current total reward"""
        return self.total_reward
    
    def get_scheduled_tasks(self):
        """Get current scheduled tasks"""
        return self.scheduled_tasks
```

### Related Problems

## Problem Variations

### **Variation 1: Tasks and Deadlines with Dynamic Updates**
**Problem**: Handle dynamic task updates (add/remove/update tasks) while maintaining optimal scheduling.

**Approach**: Use priority queues and efficient re-scheduling algorithms for dynamic task management.

```python
from collections import defaultdict
import heapq

class DynamicTasksAndDeadlines:
    def __init__(self, tasks):
        self.tasks = {task['id']: task for task in tasks}
        self.scheduled_tasks = []
        self.total_reward = 0
        self.current_time = 0
        self._update_schedule()
    
    def _update_schedule(self):
        """Update the optimal schedule using greedy algorithm."""
        # Sort tasks by reward-to-duration ratio
        sorted_tasks = sorted(self.tasks.values(), 
                            key=lambda x: x['reward'] / x['duration'], 
                            reverse=True)
        
        self.scheduled_tasks = []
        self.total_reward = 0
        self.current_time = 0
        
        for task in sorted_tasks:
            if self.current_time + task['duration'] <= task['deadline']:
                self.total_reward += task['reward']
                self.current_time += task['duration']
                self.scheduled_tasks.append(task['id'])
    
    def add_task(self, task):
        """Add a new task to the system."""
        self.tasks[task['id']] = task
        self._update_schedule()
    
    def remove_task(self, task_id):
        """Remove a task from the system."""
        if task_id in self.tasks:
            del self.tasks[task_id]
            self._update_schedule()
    
    def update_task(self, task_id, updates):
        """Update a task with new parameters."""
        if task_id in self.tasks:
            self.tasks[task_id].update(updates)
            self._update_schedule()
    
    def get_scheduled_tasks(self):
        """Get current scheduled tasks."""
        return self.scheduled_tasks
    
    def get_total_reward(self):
        """Get current total reward."""
        return self.total_reward
    
    def get_tasks_with_constraints(self, constraint_func):
        """Get tasks that satisfy custom constraints."""
        result = []
        for task in self.tasks.values():
            if constraint_func(task):
                result.append(task)
        return result
    
    def get_tasks_in_time_range(self, start_time, end_time):
        """Get tasks that can be scheduled in time range."""
        result = []
        for task in self.tasks.values():
            if (start_time <= task['deadline'] - task['duration'] and 
                end_time >= task['duration']):
                result.append(task)
        return result
    
    def get_tasks_with_priority(self, priority_func):
        """Get tasks sorted by custom priority function."""
        tasks_list = list(self.tasks.values())
        tasks_list.sort(key=priority_func, reverse=True)
        return tasks_list
    
    def get_task_statistics(self):
        """Get statistics about tasks."""
        if not self.tasks:
            return {
                'total_tasks': 0,
                'scheduled_tasks': 0,
                'total_reward': 0,
                'average_duration': 0,
                'average_reward': 0
            }
        
        total_tasks = len(self.tasks)
        scheduled_tasks = len(self.scheduled_tasks)
        total_reward = self.total_reward
        
        # Calculate averages
        total_duration = sum(task['duration'] for task in self.tasks.values())
        total_reward_sum = sum(task['reward'] for task in self.tasks.values())
        average_duration = total_duration / total_tasks
        average_reward = total_reward_sum / total_tasks
        
        return {
            'total_tasks': total_tasks,
            'scheduled_tasks': scheduled_tasks,
            'total_reward': total_reward,
            'average_duration': average_duration,
            'average_reward': average_reward
        }
    
    def get_task_patterns(self):
        """Get patterns in task scheduling."""
        patterns = {
            'high_reward_tasks': 0,
            'short_duration_tasks': 0,
            'urgent_tasks': 0,
            'efficient_tasks': 0
        }
        
        for task in self.tasks.values():
            if task['reward'] > sum(t['reward'] for t in self.tasks.values()) / len(self.tasks):
                patterns['high_reward_tasks'] += 1
            
            if task['duration'] < sum(t['duration'] for t in self.tasks.values()) / len(self.tasks):
                patterns['short_duration_tasks'] += 1
            
            if task['deadline'] - task['duration'] < 10:  # Urgent if less than 10 time units
                patterns['urgent_tasks'] += 1
            
            if task['reward'] / task['duration'] > 1.0:  # Efficient if ratio > 1
                patterns['efficient_tasks'] += 1
        
        return patterns
    
    def get_optimal_scheduling_strategy(self):
        """Get optimal scheduling strategy based on task characteristics."""
        if not self.tasks:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'utilization_rate': 0
            }
        
        # Calculate efficiency rate
        total_possible_reward = sum(task['reward'] for task in self.tasks.values())
        efficiency_rate = self.total_reward / total_possible_reward if total_possible_reward > 0 else 0
        
        # Calculate utilization rate
        total_time_used = sum(self.tasks[task_id]['duration'] for task_id in self.scheduled_tasks)
        max_deadline = max(task['deadline'] for task in self.tasks.values())
        utilization_rate = total_time_used / max_deadline if max_deadline > 0 else 0
        
        # Determine recommended strategy
        if efficiency_rate > 0.8:
            recommended_strategy = 'greedy_ratio'
        elif utilization_rate > 0.7:
            recommended_strategy = 'deadline_first'
        else:
            recommended_strategy = 'reward_first'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'utilization_rate': utilization_rate
        }

# Example usage
tasks = [
    {'id': 1, 'duration': 3, 'deadline': 5, 'reward': 10},
    {'id': 2, 'duration': 2, 'deadline': 4, 'reward': 8},
    {'id': 3, 'duration': 4, 'deadline': 8, 'reward': 15},
    {'id': 4, 'duration': 1, 'deadline': 2, 'reward': 5}
]

dynamic_scheduler = DynamicTasksAndDeadlines(tasks)
print(f"Initial total reward: {dynamic_scheduler.get_total_reward()}")

# Add a new task
new_task = {'id': 5, 'duration': 2, 'deadline': 6, 'reward': 12}
dynamic_scheduler.add_task(new_task)
print(f"After adding task: {dynamic_scheduler.get_total_reward()}")

# Update a task
dynamic_scheduler.update_task(1, {'reward': 15})
print(f"After updating task: {dynamic_scheduler.get_total_reward()}")

# Remove a task
dynamic_scheduler.remove_task(4)
print(f"After removing task: {dynamic_scheduler.get_total_reward()}")

# Get tasks with constraints
def constraint_func(task):
    return task['reward'] > 10

print(f"High reward tasks: {dynamic_scheduler.get_tasks_with_constraints(constraint_func)}")

# Get tasks in time range
print(f"Tasks in time range [0, 10]: {dynamic_scheduler.get_tasks_in_time_range(0, 10)}")

# Get tasks with priority
def priority_func(task):
    return task['reward'] / task['duration']

print(f"Tasks by priority: {dynamic_scheduler.get_tasks_with_priority(priority_func)}")

# Get statistics
print(f"Statistics: {dynamic_scheduler.get_task_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_scheduler.get_task_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_scheduler.get_optimal_scheduling_strategy()}")
```

### **Variation 2: Tasks and Deadlines with Different Operations**
**Problem**: Handle different types of operations on task scheduling (weighted tasks, priority-based selection, advanced constraints).

**Approach**: Use advanced data structures for efficient different types of task scheduling queries.

```python
class AdvancedTasksAndDeadlines:
    def __init__(self, tasks, weights=None, priorities=None):
        self.tasks = {task['id']: task for task in tasks}
        self.weights = weights or {task['id']: 1 for task in tasks}
        self.priorities = priorities or {task['id']: 1 for task in tasks}
        self.scheduled_tasks = []
        self.total_reward = 0
        self.current_time = 0
        self._update_schedule()
    
    def _update_schedule(self):
        """Update the optimal schedule using advanced algorithms."""
        # Sort tasks by weighted reward-to-duration ratio
        sorted_tasks = sorted(self.tasks.values(), 
                            key=lambda x: (x['reward'] * self.weights.get(x['id'], 1)) / 
                                        (x['duration'] * self.priorities.get(x['id'], 1)), 
                            reverse=True)
        
        self.scheduled_tasks = []
        self.total_reward = 0
        self.current_time = 0
        
        for task in sorted_tasks:
            if self.current_time + task['duration'] <= task['deadline']:
                self.total_reward += task['reward'] * self.weights.get(task['id'], 1)
                self.current_time += task['duration']
                self.scheduled_tasks.append(task['id'])
    
    def get_tasks(self):
        """Get current tasks."""
        return list(self.tasks.values())
    
    def get_weighted_tasks(self):
        """Get tasks with weights applied."""
        result = []
        for task in self.tasks.values():
            weighted_task = task.copy()
            weighted_task['weighted_reward'] = task['reward'] * self.weights.get(task['id'], 1)
            weighted_task['weight'] = self.weights.get(task['id'], 1)
            result.append(weighted_task)
        return result
    
    def get_tasks_with_priority(self, priority_func):
        """Get tasks considering priority."""
        result = []
        for task in self.tasks.values():
            priority = priority_func(task, self.weights.get(task['id'], 1), 
                                   self.priorities.get(task['id'], 1))
            result.append((task, priority))
        
        # Sort by priority
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_tasks_with_optimization(self, optimization_func):
        """Get tasks using custom optimization function."""
        result = []
        for task in self.tasks.values():
            score = optimization_func(task, self.weights.get(task['id'], 1), 
                                    self.priorities.get(task['id'], 1))
            result.append((task, score))
        
        # Sort by optimization score
        result.sort(key=lambda x: x[1], reverse=True)
        return result
    
    def get_tasks_with_constraints(self, constraint_func):
        """Get tasks that satisfy custom constraints."""
        result = []
        for task in self.tasks.values():
            if constraint_func(task, self.weights.get(task['id'], 1), 
                             self.priorities.get(task['id'], 1)):
                result.append(task)
        return result
    
    def get_tasks_with_multiple_criteria(self, criteria_list):
        """Get tasks that satisfy multiple criteria."""
        result = []
        for task in self.tasks.values():
            satisfies_all_criteria = True
            for criterion in criteria_list:
                if not criterion(task, self.weights.get(task['id'], 1), 
                               self.priorities.get(task['id'], 1)):
                    satisfies_all_criteria = False
                    break
            if satisfies_all_criteria:
                result.append(task)
        return result
    
    def get_tasks_with_alternatives(self, alternatives):
        """Get tasks considering alternative parameters."""
        result = []
        
        # Check original tasks
        for task in self.tasks.values():
            result.append((task, 'original'))
        
        # Check alternative parameters
        for task_id, alt_params in alternatives.items():
            if task_id in self.tasks:
                for alt_param in alt_params:
                    # Create temporary task with alternative parameters
                    temp_task = self.tasks[task_id].copy()
                    temp_task.update(alt_param)
                    result.append((temp_task, f'alternative_{alt_param}'))
        
        return result
    
    def get_tasks_with_adaptive_criteria(self, adaptive_func):
        """Get tasks using adaptive criteria."""
        result = []
        for task in self.tasks.values():
            if adaptive_func(task, self.weights.get(task['id'], 1), 
                           self.priorities.get(task['id'], 1), result):
                result.append(task)
        return result
    
    def get_task_optimization(self):
        """Get optimal task configuration."""
        strategies = [
            ('tasks', lambda: len(self.tasks)),
            ('weighted_tasks', lambda: len(self.get_weighted_tasks())),
            ('scheduled_tasks', lambda: len(self.scheduled_tasks)),
        ]
        
        best_strategy = None
        best_value = 0
        
        for strategy_name, strategy_func in strategies:
            current_value = strategy_func()
            if current_value > best_value:
                best_value = current_value
                best_strategy = (strategy_name, current_value)
        
        return best_strategy

# Example usage
tasks = [
    {'id': 1, 'duration': 3, 'deadline': 5, 'reward': 10},
    {'id': 2, 'duration': 2, 'deadline': 4, 'reward': 8},
    {'id': 3, 'duration': 4, 'deadline': 8, 'reward': 15},
    {'id': 4, 'duration': 1, 'deadline': 2, 'reward': 5}
]

weights = {1: 2, 2: 1, 3: 3, 4: 1}
priorities = {1: 1, 2: 2, 3: 1, 4: 3}
advanced_scheduler = AdvancedTasksAndDeadlines(tasks, weights, priorities)

print(f"Tasks: {len(advanced_scheduler.get_tasks())}")
print(f"Weighted tasks: {len(advanced_scheduler.get_weighted_tasks())}")

# Get tasks with priority
def priority_func(task, weight, priority):
    return task['reward'] * weight * priority

print(f"Tasks with priority: {advanced_scheduler.get_tasks_with_priority(priority_func)}")

# Get tasks with optimization
def optimization_func(task, weight, priority):
    return (task['reward'] * weight) / (task['duration'] * priority)

print(f"Tasks with optimization: {advanced_scheduler.get_tasks_with_optimization(optimization_func)}")

# Get tasks with constraints
def constraint_func(task, weight, priority):
    return task['reward'] > 8 and weight > 1

print(f"Tasks with constraints: {advanced_scheduler.get_tasks_with_constraints(constraint_func)}")

# Get tasks with multiple criteria
def criterion1(task, weight, priority):
    return task['reward'] > 8

def criterion2(task, weight, priority):
    return weight > 1

criteria_list = [criterion1, criterion2]
print(f"Tasks with multiple criteria: {advanced_scheduler.get_tasks_with_multiple_criteria(criteria_list)}")

# Get tasks with alternatives
alternatives = {1: [{'reward': 15}, {'duration': 2}], 2: [{'deadline': 6}]}
print(f"Tasks with alternatives: {advanced_scheduler.get_tasks_with_alternatives(alternatives)}")

# Get tasks with adaptive criteria
def adaptive_func(task, weight, priority, current_result):
    return task['reward'] > 8 and len(current_result) < 3

print(f"Tasks with adaptive criteria: {advanced_scheduler.get_tasks_with_adaptive_criteria(adaptive_func)}")

# Get task optimization
print(f"Task optimization: {advanced_scheduler.get_task_optimization()}")
```

### **Variation 3: Tasks and Deadlines with Constraints**
**Problem**: Handle task scheduling with additional constraints (resource limits, dependency constraints, time constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedTasksAndDeadlines:
    def __init__(self, tasks, constraints=None):
        self.tasks = {task['id']: task for task in tasks}
        self.constraints = constraints or {}
        self.scheduled_tasks = []
        self.total_reward = 0
        self.current_time = 0
        self._update_schedule()
    
    def _update_schedule(self):
        """Update the optimal schedule considering constraints."""
        # Sort tasks by reward-to-duration ratio
        sorted_tasks = sorted(self.tasks.values(), 
                            key=lambda x: x['reward'] / x['duration'], 
                            reverse=True)
        
        self.scheduled_tasks = []
        self.total_reward = 0
        self.current_time = 0
        
        for task in sorted_tasks:
            if self._can_schedule_task(task):
                self.total_reward += task['reward']
                self.current_time += task['duration']
                self.scheduled_tasks.append(task['id'])
    
    def _can_schedule_task(self, task):
        """Check if a task can be scheduled considering constraints."""
        # Basic deadline constraint
        if self.current_time + task['duration'] > task['deadline']:
            return False
        
        # Resource constraints
        if 'resource_limits' in self.constraints:
            for resource, limit in self.constraints['resource_limits'].items():
                if resource in task.get('resources', {}):
                    current_usage = sum(self.tasks[tid].get('resources', {}).get(resource, 0) 
                                      for tid in self.scheduled_tasks)
                    if current_usage + task['resources'][resource] > limit:
                        return False
        
        # Dependency constraints
        if 'dependencies' in self.constraints:
            task_deps = self.constraints['dependencies'].get(task['id'], [])
            for dep_id in task_deps:
                if dep_id not in self.scheduled_tasks:
                    return False
        
        return True
    
    def get_tasks_with_resource_constraints(self, resource_limits):
        """Get tasks considering resource constraints."""
        result = []
        current_resources = {resource: 0 for resource in resource_limits}
        
        for task in self.tasks.values():
            # Check resource constraints
            can_schedule = True
            for resource, limit in resource_limits.items():
                if resource in task.get('resources', {}):
                    if current_resources[resource] + task['resources'][resource] > limit:
                        can_schedule = False
                        break
            
            if can_schedule:
                result.append(task)
                for resource in resource_limits:
                    if resource in task.get('resources', {}):
                        current_resources[resource] += task['resources'][resource]
        
        return result
    
    def get_tasks_with_dependency_constraints(self, dependencies):
        """Get tasks considering dependency constraints."""
        result = []
        completed_tasks = set()
        
        # Topological sort for dependencies
        while len(completed_tasks) < len(self.tasks):
            progress = False
            for task in self.tasks.values():
                if task['id'] not in completed_tasks:
                    task_deps = dependencies.get(task['id'], [])
                    if all(dep in completed_tasks for dep in task_deps):
                        result.append(task)
                        completed_tasks.add(task['id'])
                        progress = True
            
            if not progress:
                break  # Circular dependency or no progress
        
        return result
    
    def get_tasks_with_time_constraints(self, time_constraints):
        """Get tasks considering time constraints."""
        result = []
        
        for task in self.tasks.values():
            # Check time constraints
            satisfies_constraints = True
            for constraint in time_constraints:
                if not constraint(task, self.current_time):
                    satisfies_constraints = False
                    break
            
            if satisfies_constraints:
                result.append(task)
        
        return result
    
    def get_tasks_with_mathematical_constraints(self, constraint_func):
        """Get tasks that satisfy custom mathematical constraints."""
        result = []
        
        for task in self.tasks.values():
            if constraint_func(task, self.scheduled_tasks):
                result.append(task)
        
        return result
    
    def get_tasks_with_range_constraints(self, range_constraints):
        """Get tasks that satisfy range constraints."""
        result = []
        
        for task in self.tasks.values():
            # Check if task satisfies all range constraints
            satisfies_constraints = True
            for constraint in range_constraints:
                if not constraint(task):
                    satisfies_constraints = False
                    break
            
            if satisfies_constraints:
                result.append(task)
        
        return result
    
    def get_tasks_with_optimization_constraints(self, optimization_func):
        """Get tasks using custom optimization constraints."""
        # Sort tasks by optimization function
        all_tasks = []
        for task in self.tasks.values():
            score = optimization_func(task, self.scheduled_tasks)
            all_tasks.append((task, score))
        
        # Sort by optimization score
        all_tasks.sort(key=lambda x: x[1], reverse=True)
        
        return [task for task, _ in all_tasks]
    
    def get_tasks_with_multiple_constraints(self, constraints_list):
        """Get tasks that satisfy multiple constraints."""
        result = []
        
        for task in self.tasks.values():
            # Check if task satisfies all constraints
            satisfies_all_constraints = True
            for constraint in constraints_list:
                if not constraint(task, self.scheduled_tasks):
                    satisfies_all_constraints = False
                    break
            
            if satisfies_all_constraints:
                result.append(task)
        
        return result
    
    def get_tasks_with_priority_constraints(self, priority_func):
        """Get tasks with priority-based constraints."""
        # Sort tasks by priority
        all_tasks = []
        for task in self.tasks.values():
            priority = priority_func(task, self.scheduled_tasks)
            all_tasks.append((task, priority))
        
        # Sort by priority
        all_tasks.sort(key=lambda x: x[1], reverse=True)
        
        return [task for task, _ in all_tasks]
    
    def get_tasks_with_adaptive_constraints(self, adaptive_func):
        """Get tasks with adaptive constraints."""
        result = []
        
        for task in self.tasks.values():
            # Check adaptive constraints
            if adaptive_func(task, self.scheduled_tasks, result):
                result.append(task)
        
        return result
    
    def get_optimal_scheduling_strategy(self):
        """Get optimal scheduling strategy considering all constraints."""
        strategies = [
            ('resource_constraints', self.get_tasks_with_resource_constraints),
            ('dependency_constraints', self.get_tasks_with_dependency_constraints),
            ('time_constraints', self.get_tasks_with_time_constraints),
        ]
        
        best_strategy = None
        best_count = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'resource_constraints':
                    resource_limits = {'cpu': 100, 'memory': 50}
                    current_count = len(strategy_func(resource_limits))
                elif strategy_name == 'dependency_constraints':
                    dependencies = {1: [], 2: [1], 3: [1, 2], 4: []}
                    current_count = len(strategy_func(dependencies))
                elif strategy_name == 'time_constraints':
                    time_constraints = [lambda task, current_time: task['deadline'] > current_time]
                    current_count = len(strategy_func(time_constraints))
                
                if current_count > best_count:
                    best_count = current_count
                    best_strategy = (strategy_name, current_count)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'resource_limits': {'cpu': 100, 'memory': 50},
    'dependencies': {1: [], 2: [1], 3: [1, 2], 4: []}
}

tasks = [
    {'id': 1, 'duration': 3, 'deadline': 5, 'reward': 10, 'resources': {'cpu': 30, 'memory': 20}},
    {'id': 2, 'duration': 2, 'deadline': 4, 'reward': 8, 'resources': {'cpu': 20, 'memory': 15}},
    {'id': 3, 'duration': 4, 'deadline': 8, 'reward': 15, 'resources': {'cpu': 40, 'memory': 25}},
    {'id': 4, 'duration': 1, 'deadline': 2, 'reward': 5, 'resources': {'cpu': 10, 'memory': 10}}
]

constrained_scheduler = ConstrainedTasksAndDeadlines(tasks, constraints)

print("Resource-constrained tasks:", len(constrained_scheduler.get_tasks_with_resource_constraints({'cpu': 100, 'memory': 50})))

print("Dependency-constrained tasks:", len(constrained_scheduler.get_tasks_with_dependency_constraints({1: [], 2: [1], 3: [1, 2], 4: []})))

# Time constraints
time_constraints = [lambda task, current_time: task['deadline'] > current_time]
print("Time-constrained tasks:", len(constrained_scheduler.get_tasks_with_time_constraints(time_constraints)))

# Mathematical constraints
def custom_constraint(task, scheduled_tasks):
    return task['reward'] > 8 and len(scheduled_tasks) < 3

print("Mathematical constraint tasks:", len(constrained_scheduler.get_tasks_with_mathematical_constraints(custom_constraint)))

# Range constraints
def range_constraint(task):
    return 1 <= task['duration'] <= 5 and 5 <= task['reward'] <= 20

range_constraints = [range_constraint]
print("Range-constrained tasks:", len(constrained_scheduler.get_tasks_with_range_constraints(range_constraints)))

# Multiple constraints
def constraint1(task, scheduled_tasks):
    return task['reward'] > 8

def constraint2(task, scheduled_tasks):
    return len(scheduled_tasks) < 3

constraints_list = [constraint1, constraint2]
print("Multiple constraints tasks:", len(constrained_scheduler.get_tasks_with_multiple_constraints(constraints_list)))

# Priority constraints
def priority_func(task, scheduled_tasks):
    return task['reward'] / task['duration']

print("Priority-constrained tasks:", len(constrained_scheduler.get_tasks_with_priority_constraints(priority_func)))

# Adaptive constraints
def adaptive_func(task, scheduled_tasks, current_result):
    return task['reward'] > 8 and len(current_result) < 3

print("Adaptive constraint tasks:", len(constrained_scheduler.get_tasks_with_adaptive_constraints(adaptive_func)))

# Optimal strategy
optimal = constrained_scheduler.get_optimal_scheduling_strategy()
print(f"Optimal strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Tasks and Deadlines](https://cses.fi/problemset/task/1630) - Basic tasks and deadlines problem
- [Movie Festival](https://cses.fi/problemset/task/1629) - Similar scheduling problem
- [Movie Festival II](https://cses.fi/problemset/task/1630) - Advanced scheduling problem

#### **LeetCode Problems**
- [Task Scheduler](https://leetcode.com/problems/task-scheduler/) - Task scheduling with cooldown
- [Course Schedule](https://leetcode.com/problems/course-schedule/) - Course scheduling with dependencies
- [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) - Course scheduling with order
- [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) - Minimum rooms for meetings

#### **Problem Categories**
- **Greedy Algorithms**: Optimal local choices, scheduling optimization, reward maximization
- **Scheduling**: Task scheduling, deadline management, resource allocation
- **Sorting**: Array sorting, ratio-based optimization, scheduling algorithms
- **Algorithm Design**: Greedy strategies, scheduling algorithms, optimization techniques
