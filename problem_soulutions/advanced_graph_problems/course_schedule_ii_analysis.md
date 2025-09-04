---
layout: simple
title: "Course Schedule II - Topological Sorting for Course Prerequisites"
permalink: /problem_soulutions/advanced_graph_problems/course_schedule_ii_analysis
---

# Course Schedule II - Topological Sorting for Course Prerequisites

## 📋 Problem Description

Given n courses and their prerequisites, find a valid order to complete all courses. If it's impossible, return an empty array.

This is a classic topological sorting problem that requires finding a valid order to complete courses while respecting prerequisite relationships. The solution involves using Kahn's algorithm to detect cycles and find a valid topological order.

**Input**: 
- n: number of courses (labeled from 0 to n-1)
- prerequisites: array of [a, b] where b is a prerequisite for a

**Output**: 
- Valid order to complete all courses, or empty array if impossible

**Constraints**:
- 1 ≤ n ≤ 2000
- 0 ≤ prerequisites.length ≤ 5000
- prerequisites[i].length == 2
- 0 ≤ ai, bi < n

**Example**:
```
Input:
n = 4
prerequisites = [[1,0],[2,0],[3,1],[3,2]]

Output:
[0,1,2,3]

Explanation**: 
Course 0 has no prerequisites
Course 1 requires course 0
Course 2 requires course 0  
Course 3 requires courses 1 and 2
Valid order: 0 → 1 → 2 → 3
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Find a valid order to complete all courses while respecting prerequisites
- **Key Insight**: Use topological sorting to detect cycles and find valid order
- **Challenge**: Handle impossible cases (cycles in prerequisites)

### Step 2: Initial Approach
**DFS approach (inefficient but correct):**

### Step 3: Optimization/Alternative
**Kahn's algorithm approach:**

```python
def course_schedule_ii_kahn(n, prerequisites):
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
    
    # Kahn's algorithm
    from collections import deque
    queue = deque()
    
    # Add all courses with no prerequisites
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    
    result = []
    while queue:
        course = queue.popleft()
        result.append(course)
        
        # Remove this course and update in-degrees
        for next_course in adj[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    # Check if we processed all courses
    return result if len(result) == n else []
```

**Why this works:**
- Uses Kahn's algorithm for topological sorting
- Detects cycles by checking if all courses are processed
- Simple and efficient implementation
- O(n + m) time complexity

### Step 3: DFS with Cycle Detection
**Idea**: Use DFS with cycle detection to find topological order.

```python
def course_schedule_ii_dfs(n, prerequisites):
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for course, prereq in prerequisites:
        adj[prereq].append(course)
    
    # DFS with cycle detection
    visited = [False] * n
    in_stack = [False] * n
    result = []
    
    def dfs(course):
        if in_stack[course]:
            return False  # Cycle detected
        if visited[course]:
            return True
        
        visited[course] = True
        in_stack[course] = True
        
        for next_course in adj[course]:
            if not dfs(next_course):
                return False
        
        in_stack[course] = False
        result.append(course)
        return True
    
    # Check for cycles from each course
    for i in range(n):
        if not visited[i]:
            if not dfs(i):
                return []
    
    return result[::-1]  # Reverse to get topological order
```

**Why this works:**
- Uses DFS with cycle detection
- Tracks nodes in current recursion stack
- Returns topological order in reverse
- O(n + m) time complexity

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_course_schedule_ii():
    n, m = map(int, input().split())
    prerequisites = []
    
    for _ in range(m):
        a, b = map(int, input().split())
        prerequisites.append((a, b))
    
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
    
    # Kahn's algorithm
    from collections import deque
    queue = deque()
    
    # Add all courses with no prerequisites
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    
    result = []
    while queue:
        course = queue.popleft()
        result.append(course)
        
        # Remove this course and update in-degrees
        for next_course in adj[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    # Check if we processed all courses
    if len(result) == n:
        print(*result)
    else:
        print(-1)

# Main execution
if __name__ == "__main__":
    solve_course_schedule_ii()
```

**Why this works:**
- Optimal topological sorting approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 5: Testing Our Solution
**Test cases to verify correctness:**
- **Test 1**: Basic course schedule (should return valid order)
- **Test 2**: Impossible schedule (should return empty array)
- **Test 3**: Single course (should return [0])
- **Test 4**: Complex dependencies (should handle correctly)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| DFS | O(n + m) | O(n) | Use DFS with cycle detection |
| Kahn's Algorithm | O(n + m) | O(n) | Use in-degree counting |

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (4, 3, [(1, 2), (2, 3), (3, 4)]),
        (3, 2, [(1, 2), (2, 3)]),
        (4, 4, [(1, 2), (2, 3), (3, 4), (4, 1)]),  # Cycle
    ]
    
    for n, m, prerequisites in test_cases:
        result = solve_test(n, m, prerequisites)
        print(f"n={n}, m={m}, prerequisites={prerequisites}")
        print(f"Result: {result}")
        print()

def solve_test(n, m, prerequisites):
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
    
    # Kahn's algorithm
    from collections import deque
    queue = deque()
    
    # Add all courses with no prerequisites
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    
    result = []
    while queue:
        course = queue.popleft()
        result.append(course)
        
        # Remove this course and update in-degrees
        for next_course in adj[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    # Check if we processed all courses
    if len(result) == n:
        return result
    else:
        return []

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n + m) - Kahn's algorithm for topological sorting
- **Space**: O(n + m) - adjacency list and queue

### Why This Solution Works
- **Topological Sorting**: Finds valid course order
- **Cycle Detection**: Identifies impossible cases
- **Kahn's Algorithm**: Efficient implementation
- **Optimal Approach**: Handles all cases correctly

## 🎯 Key Insights

### Important Concepts and Patterns
- **Topological Sorting**: Orders vertices in DAG to find valid course sequence
- **Cycle Detection**: Detects cycles in directed graphs to handle impossible cases
- **Kahn's Algorithm**: Efficient topological sorting using in-degree counting
- **Graph Algorithms**: Use DFS or BFS for cycle detection and ordering

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Course Schedule with Weights**
```python
def course_schedule_weighted(n, prerequisites, weights):
    # Handle course schedule with weighted prerequisites
    
    # Build adjacency list with weights
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for course, prereq, weight in prerequisites:
        adj[prereq].append((course, weight))
        in_degree[course] += 1
    
    # Use priority queue for weighted topological sorting
    import heapq
    queue = []
    
    # Add all courses with no prerequisites
    for i in range(n):
        if in_degree[i] == 0:
            heapq.heappush(queue, (0, i))  # (weight, course)
    
    result = []
    total_weight = 0
    
    while queue:
        weight, course = heapq.heappop(queue)
        result.append(course)
        total_weight += weight
        
        # Update in-degrees and add to queue
        for next_course, edge_weight in adj[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                heapq.heappush(queue, (edge_weight, next_course))
    
    return result if len(result) == n else [], total_weight
```

#### **2. Course Schedule with Multiple Prerequisites**
```python
def course_schedule_multiple_prereqs(n, prerequisites):
    # Handle course schedule with multiple prerequisite types
    
    # Build adjacency list for each prerequisite type
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    prereq_types = {}  # Track prerequisite types
    
    for course, prereq, prereq_type in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
        prereq_types[(course, prereq)] = prereq_type
    
    # Use multiple queues for different prerequisite types
    queues = {
        'core': [],
        'elective': [],
        'lab': []
    }
    
    # Add courses with no prerequisites
    for i in range(n):
        if in_degree[i] == 0:
            # Determine course type based on prerequisites
            course_type = determine_course_type(i, prereq_types)
            queues[course_type].append(i)
    
    result = []
    
    # Process courses in order of priority
    for queue_type in ['core', 'elective', 'lab']:
        while queues[queue_type]:
            course = queues[queue_type].pop(0)
            result.append(course)
            
            # Update in-degrees
            for next_course in adj[course]:
                in_degree[next_course] -= 1
                if in_degree[next_course] == 0:
                    next_type = determine_course_type(next_course, prereq_types)
                    queues[next_type].append(next_course)
    
    return result if len(result) == n else []
```

#### **3. Course Schedule with Dynamic Updates**
```python
def course_schedule_dynamic(n, initial_prereqs, operations):
    # Handle course schedule with dynamic prerequisite updates
    
    current_prereqs = initial_prereqs.copy()
    results = []
    
    for op in operations:
        if op[0] == 'add':
            # Add new prerequisite
            course, prereq = op[1], op[2]
            current_prereqs.append((course, prereq))
        elif op[0] == 'remove':
            # Remove prerequisite
            course, prereq = op[1], op[2]
            current_prereqs.remove((course, prereq))
        elif op[0] == 'query':
            # Query current schedule
            result = solve_course_schedule_ii(n, current_prereqs)
            results.append(result)
    
    return results
```

## 🔗 Related Problems

### Links to Similar Problems
- **Topological Sorting**: Course schedule, task scheduling
- **Graph Algorithms**: Cycle detection, DFS, BFS
- **Dependency Resolution**: Package management, build systems
- **Scheduling**: Task scheduling, resource allocation

## 📚 Learning Points

### Key Takeaways
- **Topological sorting** is essential for dependency resolution
- **Cycle detection** is crucial for handling impossible cases
- **Kahn's algorithm** provides efficient topological sorting
- **Graph algorithms** solve complex scheduling problems

## 🎯 Key Insights

### 1. **Topological Sorting**
- Orders vertices in DAG
- Essential for understanding
- Key optimization technique
- Enables efficient solution

### 2. **Cycle Detection**
- Identifies impossible cases
- Important for understanding
- Fundamental concept
- Essential for algorithm

### 3. **Kahn's Algorithm**
- Efficient topological sorting
- Important for performance
- Simple but important concept
- Essential for understanding

## 🎯 Problem Variations

### Variation 1: Course Schedule with Weights
**Problem**: Each course has a weight/difficulty, find optimal order.

```python
def weighted_course_schedule_ii(n, prerequisites, weights):
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
    
    # Kahn's algorithm with priority queue
    import heapq
    queue = []
    
    # Add all courses with no prerequisites
    for i in range(n):
        if in_degree[i] == 0:
            heapq.heappush(queue, (weights[i], i))
    
    result = []
    while queue:
        weight, course = heapq.heappop(queue)
        result.append(course)
        
        # Remove this course and update in-degrees
        for next_course in adj[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                heapq.heappush(queue, (weights[next_course], next_course))
    
    # Check if we processed all courses
    return result if len(result) == n else []
```

### Variation 2: Course Schedule with Parallel Processing
**Problem**: Can take multiple courses simultaneously if no conflicts.

```python
def parallel_course_schedule_ii(n, prerequisites, max_parallel):
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
    
    # Kahn's algorithm with parallel processing
    from collections import deque
    queue = deque()
    
    # Add all courses with no prerequisites
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    
    result = []
    while queue:
        # Take up to max_parallel courses
        current_semester = []
        for _ in range(min(max_parallel, len(queue))):
            if queue:
                course = queue.popleft()
                current_semester.append(course)
        
        result.extend(current_semester)
        
        # Update in-degrees for taken courses
        for course in current_semester:
            for next_course in adj[course]:
                in_degree[next_course] -= 1
                if in_degree[next_course] == 0:
                    queue.append(next_course)
    
    # Check if we processed all courses
    return result if len(result) == n else []
```

### Variation 3: Course Schedule with Deadlines
**Problem**: Each course has a deadline, find feasible schedule.

```python
def deadline_course_schedule_ii(n, prerequisites, deadlines):
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
    
    # Kahn's algorithm with deadline consideration
    from collections import deque
    queue = deque()
    
    # Add all courses with no prerequisites
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    
    result = []
    current_time = 0
    
    while queue:
        # Find course with earliest deadline
        best_course = min(queue, key=lambda x: deadlines[x])
        queue.remove(best_course)
        
        if current_time > deadlines[best_course]:
            return []  # Deadline missed
        
        result.append(best_course)
        current_time += 1
        
        # Update in-degrees
        for next_course in adj[best_course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    # Check if we processed all courses
    return result if len(result) == n else []
```

### Variation 4: Dynamic Course Schedule
**Problem**: Support adding/removing prerequisites dynamically.

```python
class DynamicCourseScheduleII:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.in_degree = [0] * n
        self.prerequisites = set()
    
    def add_prerequisite(self, course, prereq):
        if (course, prereq) not in self.prerequisites:
            self.prerequisites.add((course, prereq))
            self.adj[prereq].append(course)
            self.in_degree[course] += 1
    
    def remove_prerequisite(self, course, prereq):
        if (course, prereq) in self.prerequisites:
            self.prerequisites.remove((course, prereq))
            self.adj[prereq].remove(course)
            self.in_degree[course] -= 1
            return True
        return False
    
    def get_valid_order(self):
        # Kahn's algorithm
        from collections import deque
        queue = deque()
        
        # Add all courses with no prerequisites
        for i in range(self.n):
            if self.in_degree[i] == 0:
                queue.append(i)
        
        result = []
        while queue:
            course = queue.popleft()
            result.append(course)
            
            # Remove this course and update in-degrees
            for next_course in self.adj[course]:
                self.in_degree[next_course] -= 1
                if self.in_degree[next_course] == 0:
                    queue.append(next_course)
        
        # Check if we processed all courses
        return result if len(result) == self.n else []
```

### Variation 5: Course Schedule with Multiple Constraints
**Problem**: Find valid schedule satisfying multiple constraints.

```python
def multi_constrained_course_schedule_ii(n, prerequisites, constraints):
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
    
    # Apply constraints
    forbidden_edges = constraints.get('forbidden_edges', set())
    required_edges = constraints.get('required_edges', set())
    
    # Remove forbidden prerequisites
    for course, prereq in forbidden_edges:
        if prereq in adj[course]:
            adj[course].remove(prereq)
            in_degree[course] -= 1
    
    # Add required prerequisites
    for course, prereq in required_edges:
        if prereq not in adj[course]:
            adj[prereq].append(course)
            in_degree[course] += 1
    
    # Kahn's algorithm
    from collections import deque
    queue = deque()
    
    # Add all courses with no prerequisites
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    
    result = []
    while queue:
        course = queue.popleft()
        result.append(course)
        
        # Remove this course and update in-degrees
        for next_course in adj[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    # Check if we processed all courses
    return result if len(result) == n else []
```

## 🔗 Related Problems

- **[Topological Sorting](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Topological sorting algorithms
- **[Graph Theory](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Graph theory concepts
- **[Cycle Detection](/cses-analyses/problem_soulutions/advanced_graph_problems/)**: Cycle detection algorithms

## 📚 Learning Points

1. **Topological Sorting**: Essential for dependency resolution
2. **Kahn's Algorithm**: Efficient implementation
3. **Cycle Detection**: Important for impossible cases
4. **Graph Theory**: Important graph theory concept

---

**This is a great introduction to course scheduling and topological sorting!** 🎯
    for course, prereq in prerequisites:
        adj[prereq].append(course)
    
    # DFS with cycle detection
    visited = [0] * n  # 0: unvisited, 1: visiting, 2: visited
    result = []
    
    def dfs(course):
        if visited[course] == 1:  # Cycle detected
            return False
        if visited[course] == 2:  # Already processed
            return True
        
        visited[course] = 1  # Mark as visiting
        
        for next_course in adj[course]:
            if not dfs(next_course):
                return False
        
        visited[course] = 2  # Mark as visited
        result.append(course)
        return True
    
    # Try DFS from all courses
    for course in range(n):
        if visited[course] == 0:
            if not dfs(course):
                return []
    
    return result[::-1]  # Reverse to get topological order
```

**Why this works:**
- Uses DFS with cycle detection
- Three-state visited array
- Detects cycles during traversal
- O(n + m) time complexity

### Step 3: Complete Solution
**Putting it all together:**

```python
def solve_course_schedule_ii():
    n, m = map(int, input().split())
    prerequisites = []
    
    for _ in range(m):
        a, b = map(int, input().split())
        prerequisites.append((a, b))
    
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
    
    # Kahn's algorithm
    from collections import deque
    queue = deque()
    
    # Add all courses with no prerequisites
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    
    result = []
    while queue:
        course = queue.popleft()
        result.append(course)
        
        # Remove this course and update in-degrees
        for next_course in adj[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    # Check if we processed all courses
    if len(result) == n:
        print(*result)
    else:
        print(-1)

# Main execution
if __name__ == "__main__":
    solve_course_schedule_ii()
```

**Why this works:**
- Optimal Kahn's algorithm approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 4: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (4, [(1, 0), (2, 0), (3, 1), (3, 2)]),
        (2, [(1, 0), (0, 1)]),  # Cycle
        (3, [(1, 0), (2, 1)]),
    ]
    
    for n, prerequisites in test_cases:
        result = solve_test(n, prerequisites)
        print(f"n={n}, prerequisites={prerequisites}")
        print(f"Schedule: {result}")
        print()

def solve_test(n, prerequisites):
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
    
    # Kahn's algorithm
    from collections import deque
    queue = deque()
    
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    
    result = []
    while queue:
        course = queue.popleft()
        result.append(course)
        
        for next_course in adj[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    return result if len(result) == n else []

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n + m) - Kahn's algorithm
- **Space**: O(n + m) - adjacency list and queue

### Why This Solution Works
- **Kahn's Algorithm**: Finds topological order efficiently
- **Cycle Detection**: Detects impossible cases
- **In-Degree Tracking**: Manages prerequisite relationships
- **Optimal Approach**: Handles all cases correctly

## 🎯 Key Insights

### 1. **Topological Sorting**
- Kahn's algorithm for ordering
- Essential for dependency resolution
- Key optimization technique
- Enables efficient solution

### 2. **Cycle Detection**
- Detect impossible schedules
- Important for validation
- Fundamental concept
- Essential for algorithm

### 3. **In-Degree Management**
- Track prerequisite counts
- Important for performance
- Simple but important concept
- Essential for understanding

## 🎯 Problem Variations

### Variation 1: Course Schedule with Weights
**Problem**: Each course has a completion time, find minimum total time.

```python
def course_schedule_with_weights(n, prerequisites, weights):
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
    
    # Kahn's algorithm with time tracking
    from collections import deque
    queue = deque()
    completion_time = [0] * n
    
    # Add all courses with no prerequisites
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
            completion_time[i] = weights[i]
    
    result = []
    while queue:
        course = queue.popleft()
        result.append(course)
        
        for next_course in adj[course]:
            in_degree[next_course] -= 1
            completion_time[next_course] = max(
                completion_time[next_course],
                completion_time[course] + weights[next_course]
            )
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    return result if len(result) == n else [], max(completion_time)
```

### Variation 2: Course Schedule with Parallel Processing
**Problem**: Allow taking multiple courses simultaneously.

```python
def parallel_course_schedule(n, prerequisites, max_parallel):
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
    
    # Kahn's algorithm with parallel processing
    from collections import deque
    queue = deque()
    
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    
    result = []
    semester = 0
    
    while queue:
        # Take up to max_parallel courses
        current_semester = []
        for _ in range(min(max_parallel, len(queue))):
            course = queue.popleft()
            current_semester.append(course)
            result.append(course)
        
        # Update in-degrees for next semester
        for course in current_semester:
            for next_course in adj[course]:
                in_degree[next_course] -= 1
                if in_degree[next_course] == 0:
                    queue.append(next_course)
        
        semester += 1
    
    return result if len(result) == n else [], semester
```

### Variation 3: Course Schedule with Constraints
**Problem**: Some courses cannot be taken in the same semester.

```python
def constrained_course_schedule(n, prerequisites, conflicts):
    # conflicts: set of course pairs that cannot be taken together
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
    
    # Kahn's algorithm with conflict checking
    from collections import deque
    queue = deque()
    
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    
    result = []
    current_semester = []
    
    while queue:
        course = queue.popleft()
        
        # Check conflicts with current semester
        can_take = True
        for taken_course in current_semester:
            if (course, taken_course) in conflicts or (taken_course, course) in conflicts:
                can_take = False
                break
        
        if can_take:
            current_semester.append(course)
            result.append(course)
            
            # Update in-degrees
            for next_course in adj[course]:
                in_degree[next_course] -= 1
                if in_degree[next_course] == 0:
                    queue.append(next_course)
        else:
            # Put back in queue for next semester
            queue.append(course)
    
    return result if len(result) == n else []
```

### Variation 4: Dynamic Course Schedule
**Problem**: Support adding/removing prerequisites and answering schedule queries.

```python
class DynamicCourseSchedule:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n)]
        self.in_degree = [0] * n
        self.prerequisites = set()
    
    def add_prerequisite(self, course, prereq):
        if (course, prereq) not in self.prerequisites:
            self.adj[prereq].append(course)
            self.in_degree[course] += 1
            self.prerequisites.add((course, prereq))
    
    def remove_prerequisite(self, course, prereq):
        if (course, prereq) in self.prerequisites:
            self.adj[prereq].remove(course)
            self.in_degree[course] -= 1
            self.prerequisites.remove((course, prereq))
    
    def get_schedule(self):
        # Kahn's algorithm
        from collections import deque
        queue = deque()
        
        # Copy in-degrees
        in_degree_copy = self.in_degree.copy()
        
        for i in range(self.n):
            if in_degree_copy[i] == 0:
                queue.append(i)
        
        result = []
        while queue:
            course = queue.popleft()
            result.append(course)
            
            for next_course in self.adj[course]:
                in_degree_copy[next_course] -= 1
                if in_degree_copy[next_course] == 0:
                    queue.append(next_course)
        
        return result if len(result) == self.n else []
```

### Variation 5: Course Schedule with Priorities
**Problem**: Each course has a priority, prefer higher priority courses.

```python
def priority_course_schedule(n, prerequisites, priorities):
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
    
    # Kahn's algorithm with priority queue
    from heapq import heappush, heappop
    
    # Priority queue: (-priority, course) for max heap
    pq = []
    
    for i in range(n):
        if in_degree[i] == 0:
            heappush(pq, (-priorities[i], i))
    
    result = []
    while pq:
        priority, course = heappop(pq)
        result.append(course)
        
        for next_course in adj[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                heappush(pq, (-priorities[next_course], next_course))
    
    return result if len(result) == n else []
```

## 🔗 Related Problems

- **[Topological Sorting](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph algorithms
- **[Kahn's Algorithm](/cses-analyses/problem_soulutions/graph_algorithms/)**: Topological sorting
- **[Cycle Detection](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph algorithms

## 📚 Learning Points

1. **Topological Sorting**: Essential for dependency resolution
2. **Kahn's Algorithm**: Efficient topological sorting algorithm
3. **Cycle Detection**: Important for validation
4. **In-Degree Management**: Fundamental concept

---

**This is a great introduction to course scheduling and topological sorting!** 🎯
    for course, prereq in prerequisites:
        adj[prereq].append(course)
    
    # DFS with cycle detection
    visited = [False] * n
    in_stack = [False] * n
    result = []
    
    def dfs(course):
        if in_stack[course]:
            return False  # Cycle detected
        if visited[course]:
            return True
        
        visited[course] = True
        in_stack[course] = True
        
        for next_course in adj[course]:
            if not dfs(next_course):
                return False
        
        in_stack[course] = False
        result.append(course)
        return True
    
    # Process all courses
    for course in range(n):
        if not visited[course]:
            if not dfs(course):
                return []  # Cycle found
    
    return result[::-1]  # Reverse for topological order
```

**Why this is useful:**
- Alternative approach using DFS
- More intuitive for some problems
- Still detects cycles efficiently
- Good for understanding the concept

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_course_schedule_ii():
    n = int(input())
    m = int(input())
    prerequisites = []
    
    for _ in range(m):
        course, prereq = map(int, input().split())
        prerequisites.append([course, prereq])
    
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
    
    # Kahn's algorithm
    from collections import deque
    queue = deque()
    
    # Add all courses with no prerequisites
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    
    result = []
    while queue:
        course = queue.popleft()
        result.append(course)
        
        # Remove this course and update in-degrees
        for next_course in adj[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    # Check if we processed all courses
    if len(result) == n:
        print(*result)
    else:
        print("IMPOSSIBLE")

# Main execution
if __name__ == "__main__":
    solve_course_schedule_ii()
```

**Why this works:**
- Optimal topological sorting approach
- Handles all edge cases including cycles
- Efficient implementation
- Clear and readable code

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (4, [[1,0],[2,0],[3,1],[3,2]], [0,1,2,3]),
        (2, [[1,0]], [0,1]),
        (2, [[1,0],[0,1]], []),  # Cycle
        (3, [[1,0],[2,1]], [0,1,2]),
        (1, [], [0]),  # No prerequisites
    ]
    
    for n, prerequisites, expected in test_cases:
        result = solve_test(n, prerequisites)
        print(f"n={n}, prerequisites={prerequisites}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n, prerequisites):
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
    
    # Kahn's algorithm
    from collections import deque
    queue = deque()
    
    # Add all courses with no prerequisites
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
    
    result = []
    while queue:
        course = queue.popleft()
        result.append(course)
        
        # Remove this course and update in-degrees
        for next_course in adj[course]:
            in_degree[next_course] -= 1
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    # Check if we processed all courses
    return result if len(result) == n else []

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n + m) - building graph and topological sort
- **Space**: O(n + m) - adjacency list and result array

### Why This Solution Works
- **Topological Sorting**: Finds valid order respecting prerequisites
- **Cycle Detection**: Identifies impossible cases
- **Kahn's Algorithm**: Efficient implementation
- **Optimal Approach**: Guarantees correct result

## 🎯 Key Insights

### 1. **Topological Sorting**
- Orders nodes so all edges point forward
- Perfect for dependency problems
- Key insight for solution
- Essential for understanding

### 2. **Cycle Detection**
- Cycles make ordering impossible
- Kahn's algorithm naturally detects cycles
- Important for correctness
- Critical edge case

### 3. **Dependency Graph**
- Prerequisites form directed graph
- Understanding graph structure is key
- Enables efficient solution
- Fundamental concept

## 🎯 Problem Variations

### Variation 1: Course Schedule with Weights
**Problem**: Each course has a duration. Find minimum time to complete all courses.

```python
def course_schedule_with_weights(n, prerequisites, durations):
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
    
    # Kahn's algorithm with time tracking
    from collections import deque
    queue = deque()
    completion_time = [0] * n
    
    # Add all courses with no prerequisites
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
            completion_time[i] = durations[i]
    
    result = []
    while queue:
        course = queue.popleft()
        result.append(course)
        
        # Update dependent courses
        for next_course in adj[course]:
            in_degree[next_course] -= 1
            completion_time[next_course] = max(
                completion_time[next_course],
                completion_time[course] + durations[next_course]
            )
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    if len(result) == n:
        return max(completion_time)
    else:
        return -1  # Impossible
```

### Variation 2: Course Schedule with Parallel Execution
**Problem**: Can take multiple courses simultaneously. Find minimum time.

```python
def course_schedule_parallel(n, prerequisites, durations):
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
    
    # Kahn's algorithm with parallel execution
    from collections import deque
    queue = deque()
    completion_time = [0] * n
    
    # Add all courses with no prerequisites
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
            completion_time[i] = durations[i]
    
    result = []
    while queue:
        # Process all available courses in parallel
        level_courses = []
        while queue:
            level_courses.append(queue.popleft())
        
        # Add all courses at this level
        result.extend(level_courses)
        
        # Update dependent courses
        for course in level_courses:
            for next_course in adj[course]:
                in_degree[next_course] -= 1
                completion_time[next_course] = max(
                    completion_time[next_course],
                    completion_time[course] + durations[next_course]
                )
                if in_degree[next_course] == 0:
                    queue.append(next_course)
    
    if len(result) == n:
        return max(completion_time)
    else:
        return -1  # Impossible
```

### Variation 3: Course Schedule with Limited Resources
**Problem**: Can only take k courses simultaneously. Find minimum time.

```python
def course_schedule_limited_resources(n, prerequisites, durations, k):
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
    
    # Kahn's algorithm with resource limitation
    from collections import deque
    queue = deque()
    completion_time = [0] * n
    
    # Add all courses with no prerequisites
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
            completion_time[i] = durations[i]
    
    result = []
    while queue:
        # Take at most k courses
        level_courses = []
        for _ in range(min(k, len(queue))):
            level_courses.append(queue.popleft())
        
        # Add courses at this level
        result.extend(level_courses)
        
        # Update dependent courses
        for course in level_courses:
            for next_course in adj[course]:
                in_degree[next_course] -= 1
                completion_time[next_course] = max(
                    completion_time[next_course],
                    completion_time[course] + durations[next_course]
                )
                if in_degree[next_course] == 0:
                    queue.append(next_course)
    
    if len(result) == n:
        return max(completion_time)
    else:
        return -1  # Impossible
```

### Variation 4: Course Schedule with Prerequisites Count
**Problem**: Find all valid orders and count them.

```python
def count_course_schedules(n, prerequisites):
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for course, prereq in prerequisites:
        adj[prereq].append(course)
    
    # Use dynamic programming to count valid orders
    from functools import lru_cache
    
    @lru_cache(None)
    def count_orders(mask):
        if mask == (1 << n) - 1:
            return 1
        
        count = 0
        for course in range(n):
            if mask & (1 << course) == 0:  # Course not taken
                # Check if all prerequisites are satisfied
                can_take = True
                for prereq, _ in prerequisites:
                    if prereq == course:
                        prereq_course = _
                        if mask & (1 << prereq_course) == 0:
                            can_take = False
                            break
                
                if can_take:
                    count += count_orders(mask | (1 << course))
        
        return count
    
    return count_orders(0)
```

### Variation 5: Course Schedule with Deadlines
**Problem**: Each course has a deadline. Find if possible to complete all courses on time.

```python
def course_schedule_with_deadlines(n, prerequisites, durations, deadlines):
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
    
    # Kahn's algorithm with deadline checking
    from collections import deque
    queue = deque()
    completion_time = [0] * n
    
    # Add all courses with no prerequisites
    for i in range(n):
        if in_degree[i] == 0:
            queue.append(i)
            completion_time[i] = durations[i]
    
    result = []
    while queue:
        course = queue.popleft()
        
        # Check if we can complete on time
        if completion_time[course] > deadlines[course]:
            return []  # Impossible
        
        result.append(course)
        
        # Update dependent courses
        for next_course in adj[course]:
            in_degree[next_course] -= 1
            completion_time[next_course] = max(
                completion_time[next_course],
                completion_time[course] + durations[next_course]
            )
            if in_degree[next_course] == 0:
                queue.append(next_course)
    
    return result if len(result) == n else []
```

## 🔗 Related Problems

- **[Acyclic Graph Edges](/cses-analyses/problem_soulutions/advanced_graph_problems/acyclic_graph_edges_analysis)**: Cycle detection
- **[Topological Sorting](/cses-analyses/problem_soulutions/graph_algorithms/topological_sorting_analysis)**: Graph ordering
- **[Graph Problems](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph algorithms

## 📚 Learning Points

1. **Topological Sorting**: Essential for dependency problems
2. **Cycle Detection**: Critical for impossible cases
3. **Kahn's Algorithm**: Efficient implementation
4. **Dependency Graphs**: Common pattern in real-world problems

---

**This is a great introduction to topological sorting and dependency resolution!** 🎯 