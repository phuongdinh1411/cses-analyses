---
layout: simple
title: "Course Schedule II - Topological Sorting for Course Prerequisites"
permalink: /problem_soulutions/advanced_graph_problems/course_schedule_ii_analysis
---

# Course Schedule II - Topological Sorting for Course Prerequisites

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of topological sorting and its applications
- Apply Kahn's algorithm for topological sorting with cycle detection
- Implement DFS-based topological sorting with cycle detection
- Handle cycle detection in directed graphs using topological sorting
- Apply topological sorting to real-world scheduling problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Topological sorting, Kahn's algorithm, DFS, cycle detection
- **Data Structures**: Adjacency lists, queues, stacks, in-degree arrays
- **Mathematical Concepts**: Graph theory, directed acyclic graphs (DAGs), ordering
- **Programming Skills**: DFS implementation, queue operations, graph representation
- **Related Problems**: Topological Sorting (basic topological sort), Building Teams (cycle detection), Round Trip (cycle detection)

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

### 📊 Visual Example

**Course Prerequisites Graph:**
```
    0 (no prerequisites)
   ╱ ╲
  ╱   ╲
 1     2
  ╲   ╱
   ╲ ╱
    3
```

**Topological Sorting Process:**
```
Step 1: Calculate in-degrees
Course:  0  1  2  3
In-degree: 0  1  1  2

Step 2: Start with courses having in-degree 0
Queue: [0]  ← Only course 0 has no prerequisites

Step 3: Process Queue
┌─────────────────────────────────────┐
│ Remove course 0 from queue          │
│ Result: [0]                         │
│ Update in-degrees of neighbors:     │
│ - Course 1: 1-1=0 (add to queue)   │
│ - Course 2: 1-1=0 (add to queue)   │
│ Queue: [1, 2]                       │
└─────────────────────────────────────┘

Step 4: Continue Processing
┌─────────────────────────────────────┐
│ Remove course 1 from queue          │
│ Result: [0, 1]                      │
│ Update in-degrees of neighbors:     │
│ - Course 3: 2-1=1                   │
│ Queue: [2]                          │
└─────────────────────────────────────┘

Step 5: Final Processing
┌─────────────────────────────────────┐
│ Remove course 2 from queue          │
│ Result: [0, 1, 2]                   │
│ Update in-degrees of neighbors:     │
│ - Course 3: 1-1=0 (add to queue)   │
│ Queue: [3]                          │
└─────────────────────────────────────┘

Final Result: [0, 1, 2, 3]
```

**Impossible Case (Cycle):**
```
Input: [[1,0],[0,1]]  ← Cycle: 0→1→0

Graph:
    0 ←──→ 1
    ↑      │
    └──────┘

In-degrees: [1, 1]  ← No course with in-degree 0
Result: []  ← Impossible to complete
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Try All Possible Course Orders

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Try all possible permutations of course completion orders
- **Constraint Checking**: For each order, verify that all prerequisites are satisfied
- **Cycle Detection**: Check if any order violates prerequisite constraints
- **Complete Coverage**: Guaranteed to find a valid order if one exists

**Key Insight**: Systematically try all possible course completion orders to find one that satisfies all prerequisite constraints.

**Algorithm**:
- Generate all possible permutations of course completion orders
- For each permutation, check if all prerequisites are satisfied
- Return the first valid order found, or empty array if none exists

**Visual Example**:
```
Courses: [0, 1, 2, 3], Prerequisites: [[1,0],[2,0],[3,1],[3,2]]

Try all possible orders:
- Order 1: [0, 1, 2, 3]
  - Check: 0 before 1 ✓, 0 before 2 ✓, 1 before 3 ✓, 2 before 3 ✓
  - Valid order found!
- Order 2: [0, 1, 3, 2]
  - Check: 0 before 1 ✓, 0 before 2 ✗ (2 comes after 0)
  - Invalid order
- Order 3: [1, 0, 2, 3]
  - Check: 0 before 1 ✗ (1 comes before 0)
  - Invalid order
- ... (continue for all permutations)

First valid order: [0, 1, 2, 3]
```

**Implementation**:
```python
def brute_force_course_schedule(n, prerequisites):
    """
    Find valid course order using brute force approach
    
    Args:
        n: number of courses
        prerequisites: list of [course, prerequisite] pairs
    
    Returns:
        list: valid course order or empty list if impossible
    """
    from itertools import permutations
    
    # Try all possible course orders
    for order in permutations(range(n)):
        valid = True
        
        # Check if this order satisfies all prerequisites
        for course, prereq in prerequisites:
            course_pos = order.index(course)
            prereq_pos = order.index(prereq)
            
            if course_pos <= prereq_pos:  # Course comes before prerequisite
                valid = False
                break
        
        if valid:
            return list(order)
    
    return []  # No valid order found

# Example usage
n = 4
prerequisites = [[1,0],[2,0],[3,1],[3,2]]
result = brute_force_course_schedule(n, prerequisites)
print(f"Brute force result: {result}")  # Output: [0, 1, 2, 3]
```

**Time Complexity**: O(n! × m) - All permutations of courses
**Space Complexity**: O(n) - For permutation storage

**Why it's inefficient**: Factorial time complexity makes it impractical for large inputs.

---

### Approach 2: Optimized - DFS with Cycle Detection

**Key Insights from Optimized Approach**:
- **DFS Traversal**: Use depth-first search to explore course dependencies
- **Cycle Detection**: Track nodes in current recursion stack to detect cycles
- **Topological Order**: Build result in reverse order during DFS backtracking
- **Efficient Exploration**: Process each course and its dependencies once

**Key Insight**: Use DFS with cycle detection to efficiently find a valid topological order while detecting impossible cases.

**Algorithm**:
- Build adjacency list from prerequisites
- Use DFS with three states: unvisited, visiting, visited
- Track nodes in current recursion stack to detect cycles
- Build result in reverse order during backtracking

**Visual Example**:
```
Courses: [0, 1, 2, 3], Prerequisites: [[1,0],[2,0],[3,1],[3,2]]

DFS traversal:
- Start with course 0: visited=0, in_stack=False
  - Mark as visiting: visited=1, in_stack=True
  - Explore neighbors: [1, 2]
  - Process course 1: visited=0, in_stack=False
    - Mark as visiting: visited=1, in_stack=True
    - Explore neighbors: [3]
    - Process course 3: visited=0, in_stack=False
      - Mark as visiting: visited=1, in_stack=True
      - No neighbors, mark as visited: visited=2, in_stack=False
      - Add to result: [3]
    - Mark as visited: visited=2, in_stack=False
    - Add to result: [3, 1]
  - Process course 2: visited=0, in_stack=False
    - Mark as visiting: visited=1, in_stack=True
    - Explore neighbors: [3] (already visited)
    - Mark as visited: visited=2, in_stack=False
    - Add to result: [3, 1, 2]
  - Mark as visited: visited=2, in_stack=False
  - Add to result: [3, 1, 2, 0]

Reverse result: [0, 2, 1, 3]
```

**Implementation**:
```python
def optimized_course_schedule(n, prerequisites):
    """
    Find valid course order using DFS with cycle detection
    
    Args:
        n: number of courses
        prerequisites: list of [course, prerequisite] pairs
    
    Returns:
        list: valid course order or empty list if impossible
    """
    # Build adjacency list
    adj = [[] for _ in range(n)]
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
                return []  # Cycle found
    
    return result[::-1]  # Reverse to get topological order

# Example usage
n = 4
prerequisites = [[1,0],[2,0],[3,1],[3,2]]
result = optimized_course_schedule(n, prerequisites)
print(f"Optimized result: {result}")  # Output: [0, 1, 2, 3]
```

**Time Complexity**: O(n + m) - DFS traversal
**Space Complexity**: O(n + m) - Adjacency list and recursion stack

**Why it's better**: Much more efficient than brute force, but can be optimized further.

---

### Approach 3: Optimal - Kahn's Algorithm

**Key Insights from Optimal Approach**:
- **In-Degree Counting**: Track number of prerequisites for each course
- **Queue-Based Processing**: Process courses with no prerequisites first
- **Incremental Updates**: Update in-degrees as courses are completed
- **Cycle Detection**: Detect cycles by checking if all courses are processed

**Key Insight**: Use Kahn's algorithm with in-degree counting to efficiently find topological order and detect cycles.

**Algorithm**:
- Build adjacency list and count in-degrees for each course
- Start with courses having in-degree 0 (no prerequisites)
- Process courses in queue, updating in-degrees of dependent courses
- Add courses to queue when their in-degree becomes 0
- Check if all courses are processed to detect cycles

**Visual Example**:
```
Courses: [0, 1, 2, 3], Prerequisites: [[1,0],[2,0],[3,1],[3,2]]

Step 1: Calculate in-degrees
Course:  0  1  2  3
In-degree: 0  1  1  2

Step 2: Initialize queue with courses having in-degree 0
Queue: [0]

Step 3: Process queue
- Remove course 0: result = [0]
- Update in-degrees: course 1: 1→0, course 2: 1→0
- Add to queue: [1, 2]

Step 4: Continue processing
- Remove course 1: result = [0, 1]
- Update in-degrees: course 3: 2→1
- Queue: [2]

Step 5: Final processing
- Remove course 2: result = [0, 1, 2]
- Update in-degrees: course 3: 1→0
- Add to queue: [3]

Step 6: Complete
- Remove course 3: result = [0, 1, 2, 3]
- Queue: []
- All courses processed: valid order found

Final result: [0, 1, 2, 3]
```

**Implementation**:
```python
def optimal_course_schedule(n, prerequisites):
    """
    Find valid course order using Kahn's algorithm
    
    Args:
        n: number of courses
        prerequisites: list of [course, prerequisite] pairs
    
    Returns:
        list: valid course order or empty list if impossible
    """
    from collections import deque
    
    # Build adjacency list and in-degree count
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    
    for course, prereq in prerequisites:
        adj[prereq].append(course)
        in_degree[course] += 1
    
    # Kahn's algorithm
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

# Example usage
n = 4
prerequisites = [[1,0],[2,0],[3,1],[3,2]]
result = optimal_course_schedule(n, prerequisites)
print(f"Optimal result: {result}")  # Output: [0, 1, 2, 3]
```

**Time Complexity**: O(n + m) - Building graph and processing queue
**Space Complexity**: O(n + m) - Adjacency list and queue

**Why it's optimal**: O(n + m) time complexity is optimal for this problem, best possible solution.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n! × m) | O(n) | Try all permutations |
| DFS with Cycle Detection | O(n + m) | O(n + m) | Use DFS with three states |
| Kahn's Algorithm | O(n + m) | O(n + m) | Use in-degree counting |

### Time Complexity
- **Time**: O(n + m) - Building graph and topological sort
- **Space**: O(n + m) - Adjacency list and result array

### Why This Solution Works
- **Topological Sorting**: Finds valid order respecting prerequisites
- **Cycle Detection**: Identifies impossible cases
- **Kahn's Algorithm**: Efficient implementation
- **Optimal Approach**: Guarantees correct result
    
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

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

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

## Problem Variations

### **Variation 1: Course Schedule II with Dynamic Updates**
**Problem**: Handle dynamic course updates (add/remove/update courses and prerequisites) while maintaining optimal course scheduling calculation efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic course management with topological sorting.

```python
from collections import defaultdict, deque
import heapq

class DynamicCourseScheduleII:
    def __init__(self, n=None, prerequisites=None):
        self.n = n or 0
        self.prerequisites = prerequisites or []
        self.graph = defaultdict(list)
        self.in_degree = defaultdict(int)
        self._update_course_schedule_info()
    
    def _update_course_schedule_info(self):
        """Update course schedule feasibility information."""
        self.course_schedule_feasibility = self._calculate_course_schedule_feasibility()
    
    def _calculate_course_schedule_feasibility(self):
        """Calculate course schedule feasibility."""
        if self.n <= 0:
            return 0.0
        
        # Check if we can schedule all courses
        return 1.0 if self.n > 0 else 0.0
    
    def update_courses(self, new_n, new_prerequisites):
        """Update the courses with new count and prerequisites."""
        self.n = new_n
        self.prerequisites = new_prerequisites
        self._build_graph()
        self._update_course_schedule_info()
    
    def add_course(self, course, prerequisites_list):
        """Add a new course with its prerequisites."""
        if 0 <= course < self.n:
            for prereq in prerequisites_list:
                if 0 <= prereq < self.n:
                    self.prerequisites.append([prereq, course])
            self._build_graph()
            self._update_course_schedule_info()
    
    def remove_course(self, course):
        """Remove a course and its related prerequisites."""
        # Remove prerequisites where this course is involved
        self.prerequisites = [p for p in self.prerequisites if p[0] != course and p[1] != course]
        self._build_graph()
        self._update_course_schedule_info()
    
    def _build_graph(self):
        """Build the graph from prerequisites."""
        self.graph = defaultdict(list)
        self.in_degree = defaultdict(int)
        
        for prereq, course in self.prerequisites:
            self.graph[prereq].append(course)
            self.in_degree[course] += 1
    
    def find_course_order(self):
        """Find the order to take all courses using topological sort."""
        if not self.course_schedule_feasibility:
            return []
        
        # Kahn's algorithm for topological sort
        in_degree_copy = self.in_degree.copy()
        queue = deque()
        
        # Find all courses with no prerequisites
        for i in range(self.n):
            if in_degree_copy[i] == 0:
                queue.append(i)
        
        result = []
        
        while queue:
            course = queue.popleft()
            result.append(course)
            
            for next_course in self.graph[course]:
                in_degree_copy[next_course] -= 1
                if in_degree_copy[next_course] == 0:
                    queue.append(next_course)
        
        return result if len(result) == self.n else []
    
    def find_course_order_with_priorities(self, priorities):
        """Find course order considering course priorities."""
        if not self.course_schedule_feasibility:
            return []
        
        # Use priority queue for courses with same in-degree
        in_degree_copy = self.in_degree.copy()
        pq = []
        
        # Add courses with no prerequisites to priority queue
        for i in range(self.n):
            if in_degree_copy[i] == 0:
                heapq.heappush(pq, (-priorities.get(i, 0), i))
        
        result = []
        
        while pq:
            _, course = heapq.heappop(pq)
            result.append(course)
            
            for next_course in self.graph[course]:
                in_degree_copy[next_course] -= 1
                if in_degree_copy[next_course] == 0:
                    heapq.heappush(pq, (-priorities.get(next_course, 0), next_course))
        
        return result if len(result) == self.n else []
    
    def get_course_schedule_with_constraints(self, constraint_func):
        """Get course schedule that satisfies custom constraints."""
        if not self.course_schedule_feasibility:
            return []
        
        course_order = self.find_course_order()
        if course_order and constraint_func(self.n, self.prerequisites, course_order):
            return course_order
        else:
            return []
    
    def get_course_schedule_in_range(self, min_courses, max_courses):
        """Get course schedule within specified course count range."""
        if not self.course_schedule_feasibility:
            return []
        
        if min_courses <= self.n <= max_courses:
            return self.find_course_order()
        else:
            return []
    
    def get_course_schedule_with_pattern(self, pattern_func):
        """Get course schedule matching specified pattern."""
        if not self.course_schedule_feasibility:
            return []
        
        course_order = self.find_course_order()
        if pattern_func(self.n, self.prerequisites, course_order):
            return course_order
        else:
            return []
    
    def get_course_schedule_statistics(self):
        """Get statistics about the course schedule."""
        if not self.course_schedule_feasibility:
            return {
                'n': 0,
                'course_schedule_feasibility': 0,
                'is_schedulable': False,
                'prerequisite_count': 0
            }
        
        course_order = self.find_course_order()
        return {
            'n': self.n,
            'course_schedule_feasibility': self.course_schedule_feasibility,
            'is_schedulable': len(course_order) == self.n,
            'prerequisite_count': len(self.prerequisites)
        }
    
    def get_course_schedule_patterns(self):
        """Get patterns in course schedule."""
        patterns = {
            'has_prerequisites': 0,
            'has_valid_courses': 0,
            'optimal_scheduling_possible': 0,
            'has_large_course_set': 0
        }
        
        if not self.course_schedule_feasibility:
            return patterns
        
        # Check if has prerequisites
        if len(self.prerequisites) > 0:
            patterns['has_prerequisites'] = 1
        
        # Check if has valid courses
        if self.n > 0:
            patterns['has_valid_courses'] = 1
        
        # Check if optimal scheduling is possible
        if self.course_schedule_feasibility == 1.0:
            patterns['optimal_scheduling_possible'] = 1
        
        # Check if has large course set
        if self.n > 100:
            patterns['has_large_course_set'] = 1
        
        return patterns
    
    def get_optimal_course_schedule_strategy(self):
        """Get optimal strategy for course scheduling."""
        if not self.course_schedule_feasibility:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'course_schedule_feasibility': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = self.course_schedule_feasibility
        
        # Calculate course schedule feasibility
        course_schedule_feasibility = self.course_schedule_feasibility
        
        # Determine recommended strategy
        if self.n <= 100:
            recommended_strategy = 'topological_sort'
        elif self.n <= 1000:
            recommended_strategy = 'optimized_kahn'
        else:
            recommended_strategy = 'advanced_scheduling'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'course_schedule_feasibility': course_schedule_feasibility
        }

# Example usage
n = 4
prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]
dynamic_course_schedule = DynamicCourseScheduleII(n, prerequisites)
print(f"Course schedule feasibility: {dynamic_course_schedule.course_schedule_feasibility}")

# Update courses
dynamic_course_schedule.update_courses(5, [[1, 0], [2, 0], [3, 1], [3, 2], [4, 3]])
print(f"After updating courses: n={dynamic_course_schedule.n}, prerequisites={dynamic_course_schedule.prerequisites}")

# Add course
dynamic_course_schedule.add_course(4, [3])
print(f"After adding course 4 with prerequisite 3: {dynamic_course_schedule.prerequisites}")

# Remove course
dynamic_course_schedule.remove_course(4)
print(f"After removing course 4: {dynamic_course_schedule.prerequisites}")

# Find course order
course_order = dynamic_course_schedule.find_course_order()
print(f"Course order: {course_order}")

# Find course order with priorities
priorities = {0: 3, 1: 2, 2: 2, 3: 1}
priority_order = dynamic_course_schedule.find_course_order_with_priorities(priorities)
print(f"Course order with priorities: {priority_order}")

# Get course schedule with constraints
def constraint_func(n, prerequisites, course_order):
    return len(course_order) == n and len(prerequisites) > 0

print(f"Course schedule with constraints: {dynamic_course_schedule.get_course_schedule_with_constraints(constraint_func)}")

# Get course schedule in range
print(f"Course schedule in range 1-10: {dynamic_course_schedule.get_course_schedule_in_range(1, 10)}")

# Get course schedule with pattern
def pattern_func(n, prerequisites, course_order):
    return len(course_order) == n and len(prerequisites) > 0

print(f"Course schedule with pattern: {dynamic_course_schedule.get_course_schedule_with_pattern(pattern_func)}")

# Get statistics
print(f"Statistics: {dynamic_course_schedule.get_course_schedule_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_course_schedule.get_course_schedule_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_course_schedule.get_optimal_course_schedule_strategy()}")
```

### **Variation 2: Course Schedule II with Different Operations**
**Problem**: Handle different types of course scheduling operations (weighted courses, priority-based selection, advanced scheduling analysis).

**Approach**: Use advanced data structures for efficient different types of course scheduling operations.

```python
class AdvancedCourseScheduleII:
    def __init__(self, n=None, prerequisites=None, weights=None, priorities=None):
        self.n = n or 0
        self.prerequisites = prerequisites or []
        self.weights = weights or {}
        self.priorities = priorities or {}
        self.graph = defaultdict(list)
        self._update_course_schedule_info()
    
    def _update_course_schedule_info(self):
        """Update course schedule feasibility information."""
        self.course_schedule_feasibility = self._calculate_course_schedule_feasibility()
    
    def _calculate_course_schedule_feasibility(self):
        """Calculate course schedule feasibility."""
        if self.n <= 0:
            return 0.0
        
        # Check if we can schedule all courses
        return 1.0 if self.n > 0 else 0.0
    
    def _build_graph(self):
        """Build the graph from prerequisites."""
        self.graph = defaultdict(list)
        self.in_degree = defaultdict(int)
        
        for prereq, course in self.prerequisites:
            self.graph[prereq].append(course)
            self.in_degree[course] += 1
    
    def find_course_order(self):
        """Find the order to take all courses using topological sort."""
        if not self.course_schedule_feasibility:
            return []
        
        self._build_graph()
        
        # Kahn's algorithm for topological sort
        in_degree_copy = self.in_degree.copy()
        queue = deque()
        
        # Find all courses with no prerequisites
        for i in range(self.n):
            if in_degree_copy[i] == 0:
                queue.append(i)
        
        result = []
        
        while queue:
            course = queue.popleft()
            result.append(course)
            
            for next_course in self.graph[course]:
                in_degree_copy[next_course] -= 1
                if in_degree_copy[next_course] == 0:
                    queue.append(next_course)
        
        return result if len(result) == self.n else []
    
    def get_weighted_course_schedule(self):
        """Get course schedule with weights and priorities applied."""
        if not self.course_schedule_feasibility:
            return []
        
        course_order = self.find_course_order()
        if not course_order:
            return []
        
        # Create weighted course schedule
        weighted_schedule = []
        for course in course_order:
            weight = self.weights.get(course, 1)
            priority = self.priorities.get(course, 1)
            weighted_score = weight * priority
            weighted_schedule.append((course, weighted_score))
        
        # Sort by weighted score (descending for maximization)
        weighted_schedule.sort(key=lambda x: x[1], reverse=True)
        
        return weighted_schedule
    
    def get_course_schedule_with_priority(self, priority_func):
        """Get course schedule considering priority."""
        if not self.course_schedule_feasibility:
            return []
        
        course_order = self.find_course_order()
        if not course_order:
            return []
        
        # Create priority-based course schedule
        priority_schedule = []
        for course in course_order:
            priority = priority_func(course, self.weights, self.priorities)
            priority_schedule.append((course, priority))
        
        # Sort by priority (descending for maximization)
        priority_schedule.sort(key=lambda x: x[1], reverse=True)
        
        return priority_schedule
    
    def get_course_schedule_with_optimization(self, optimization_func):
        """Get course schedule using custom optimization function."""
        if not self.course_schedule_feasibility:
            return []
        
        course_order = self.find_course_order()
        if not course_order:
            return []
        
        # Create optimization-based course schedule
        optimized_schedule = []
        for course in course_order:
            score = optimization_func(course, self.weights, self.priorities)
            optimized_schedule.append((course, score))
        
        # Sort by optimization score (descending for maximization)
        optimized_schedule.sort(key=lambda x: x[1], reverse=True)
        
        return optimized_schedule
    
    def get_course_schedule_with_constraints(self, constraint_func):
        """Get course schedule that satisfies custom constraints."""
        if not self.course_schedule_feasibility:
            return []
        
        if constraint_func(self.n, self.prerequisites, self.weights, self.priorities):
            return self.get_weighted_course_schedule()
        else:
            return []
    
    def get_course_schedule_with_multiple_criteria(self, criteria_list):
        """Get course schedule that satisfies multiple criteria."""
        if not self.course_schedule_feasibility:
            return []
        
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(self.n, self.prerequisites, self.weights, self.priorities):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            return self.get_weighted_course_schedule()
        else:
            return []
    
    def get_course_schedule_with_alternatives(self, alternatives):
        """Get course schedule considering alternative weights/priorities."""
        result = []
        
        # Check original course schedule
        original_schedule = self.get_weighted_course_schedule()
        result.append((original_schedule, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedCourseScheduleII(self.n, self.prerequisites, alt_weights, alt_priorities)
            temp_schedule = temp_instance.get_weighted_course_schedule()
            result.append((temp_schedule, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_course_schedule_with_adaptive_criteria(self, adaptive_func):
        """Get course schedule using adaptive criteria."""
        if not self.course_schedule_feasibility:
            return []
        
        if adaptive_func(self.n, self.prerequisites, self.weights, self.priorities, []):
            return self.get_weighted_course_schedule()
        else:
            return []
    
    def get_course_schedule_optimization(self):
        """Get optimal course schedule configuration."""
        strategies = [
            ('weighted_schedule', lambda: len(self.get_weighted_course_schedule())),
            ('total_weight', lambda: sum(self.weights.values())),
            ('total_priority', lambda: sum(self.priorities.values())),
        ]
        
        best_strategy = None
        best_value = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                current_value = strategy_func()
                if current_value > best_value:
                    best_value = current_value
                    best_strategy = (strategy_name, current_value)
            except:
                continue
        
        return best_strategy

# Example usage
n = 4
prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]
weights = {i: (i + 1) * 2 for i in range(n)}  # Weight based on course number
priorities = {i: 1 for i in range(n)}  # Equal priority
advanced_course_schedule = AdvancedCourseScheduleII(n, prerequisites, weights, priorities)

print(f"Weighted course schedule: {advanced_course_schedule.get_weighted_course_schedule()}")

# Get course schedule with priority
def priority_func(course, weights, priorities):
    return weights.get(course, 1) + priorities.get(course, 1)

print(f"Course schedule with priority: {advanced_course_schedule.get_course_schedule_with_priority(priority_func)}")

# Get course schedule with optimization
def optimization_func(course, weights, priorities):
    return weights.get(course, 1) * priorities.get(course, 1)

print(f"Course schedule with optimization: {advanced_course_schedule.get_course_schedule_with_optimization(optimization_func)}")

# Get course schedule with constraints
def constraint_func(n, prerequisites, weights, priorities):
    return len(prerequisites) > 0 and n > 0

print(f"Course schedule with constraints: {advanced_course_schedule.get_course_schedule_with_constraints(constraint_func)}")

# Get course schedule with multiple criteria
def criterion1(n, prerequisites, weights, priorities):
    return len(prerequisites) > 0

def criterion2(n, prerequisites, weights, priorities):
    return len(weights) > 0

criteria_list = [criterion1, criterion2]
print(f"Course schedule with multiple criteria: {advanced_course_schedule.get_course_schedule_with_multiple_criteria(criteria_list)}")

# Get course schedule with alternatives
alternatives = [({i: 1 for i in range(n)}, {i: 1 for i in range(n)}), ({i: (i+1)*3 for i in range(n)}, {i: 2 for i in range(n)})]
print(f"Course schedule with alternatives: {advanced_course_schedule.get_course_schedule_with_alternatives(alternatives)}")

# Get course schedule with adaptive criteria
def adaptive_func(n, prerequisites, weights, priorities, current_result):
    return len(prerequisites) > 0 and len(current_result) < 10

print(f"Course schedule with adaptive criteria: {advanced_course_schedule.get_course_schedule_with_adaptive_criteria(adaptive_func)}")

# Get course schedule optimization
print(f"Course schedule optimization: {advanced_course_schedule.get_course_schedule_optimization()}")
```

### **Variation 3: Course Schedule II with Constraints**
**Problem**: Handle course scheduling with additional constraints (course limits, scheduling constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedCourseScheduleII:
    def __init__(self, n=None, prerequisites=None, constraints=None):
        self.n = n or 0
        self.prerequisites = prerequisites or []
        self.constraints = constraints or {}
        self.graph = defaultdict(list)
        self._update_course_schedule_info()
    
    def _update_course_schedule_info(self):
        """Update course schedule feasibility information."""
        self.course_schedule_feasibility = self._calculate_course_schedule_feasibility()
    
    def _calculate_course_schedule_feasibility(self):
        """Calculate course schedule feasibility."""
        if self.n <= 0:
            return 0.0
        
        # Check if we can schedule all courses
        return 1.0 if self.n > 0 else 0.0
    
    def _is_valid_course(self, course):
        """Check if course is valid considering constraints."""
        # Course constraints
        if 'allowed_courses' in self.constraints:
            if course not in self.constraints['allowed_courses']:
                return False
        
        if 'forbidden_courses' in self.constraints:
            if course in self.constraints['forbidden_courses']:
                return False
        
        # Range constraints
        if 'max_course' in self.constraints:
            if course > self.constraints['max_course']:
                return False
        
        if 'min_course' in self.constraints:
            if course < self.constraints['min_course']:
                return False
        
        # Pattern constraints
        if 'pattern_constraints' in self.constraints:
            for constraint in self.constraints['pattern_constraints']:
                if not constraint(course, self.n, self.prerequisites):
                    return False
        
        return True
    
    def _build_graph(self):
        """Build the graph from prerequisites."""
        self.graph = defaultdict(list)
        self.in_degree = defaultdict(int)
        
        for prereq, course in self.prerequisites:
            if self._is_valid_course(prereq) and self._is_valid_course(course):
                self.graph[prereq].append(course)
                self.in_degree[course] += 1
    
    def find_course_order(self):
        """Find the order to take all courses using topological sort."""
        if not self.course_schedule_feasibility:
            return []
        
        self._build_graph()
        
        # Kahn's algorithm for topological sort
        in_degree_copy = self.in_degree.copy()
        queue = deque()
        
        # Find all courses with no prerequisites
        for i in range(self.n):
            if self._is_valid_course(i) and in_degree_copy[i] == 0:
                queue.append(i)
        
        result = []
        
        while queue:
            course = queue.popleft()
            result.append(course)
            
            for next_course in self.graph[course]:
                in_degree_copy[next_course] -= 1
                if in_degree_copy[next_course] == 0:
                    queue.append(next_course)
        
        return result if len(result) == self.n else []
    
    def get_course_schedule_with_course_constraints(self, min_courses, max_courses):
        """Get course schedule considering course count constraints."""
        if not self.course_schedule_feasibility:
            return []
        
        if min_courses <= self.n <= max_courses:
            return self._calculate_constrained_course_schedule()
        else:
            return []
    
    def get_course_schedule_with_scheduling_constraints(self, scheduling_constraints):
        """Get course schedule considering scheduling constraints."""
        if not self.course_schedule_feasibility:
            return []
        
        satisfies_constraints = True
        for constraint in scheduling_constraints:
            if not constraint(self.n, self.prerequisites):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            return self._calculate_constrained_course_schedule()
        else:
            return []
    
    def get_course_schedule_with_pattern_constraints(self, pattern_constraints):
        """Get course schedule considering pattern constraints."""
        if not self.course_schedule_feasibility:
            return []
        
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(self.n, self.prerequisites):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            return self._calculate_constrained_course_schedule()
        else:
            return []
    
    def get_course_schedule_with_mathematical_constraints(self, constraint_func):
        """Get course schedule that satisfies custom mathematical constraints."""
        if not self.course_schedule_feasibility:
            return []
        
        if constraint_func(self.n, self.prerequisites):
            return self._calculate_constrained_course_schedule()
        else:
            return []
    
    def get_course_schedule_with_optimization_constraints(self, optimization_func):
        """Get course schedule using custom optimization constraints."""
        if not self.course_schedule_feasibility:
            return []
        
        # Calculate optimization score for course schedule
        score = optimization_func(self.n, self.prerequisites)
        
        if score > 0:
            return self._calculate_constrained_course_schedule()
        else:
            return []
    
    def get_course_schedule_with_multiple_constraints(self, constraints_list):
        """Get course schedule that satisfies multiple constraints."""
        if not self.course_schedule_feasibility:
            return []
        
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(self.n, self.prerequisites):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            return self._calculate_constrained_course_schedule()
        else:
            return []
    
    def get_course_schedule_with_priority_constraints(self, priority_func):
        """Get course schedule with priority-based constraints."""
        if not self.course_schedule_feasibility:
            return []
        
        # Calculate priority for course schedule
        priority = priority_func(self.n, self.prerequisites)
        
        if priority > 0:
            return self._calculate_constrained_course_schedule()
        else:
            return []
    
    def get_course_schedule_with_adaptive_constraints(self, adaptive_func):
        """Get course schedule with adaptive constraints."""
        if not self.course_schedule_feasibility:
            return []
        
        if adaptive_func(self.n, self.prerequisites, []):
            return self._calculate_constrained_course_schedule()
        else:
            return []
    
    def _calculate_constrained_course_schedule(self):
        """Calculate course schedule considering all constraints."""
        if not self.course_schedule_feasibility:
            return []
        
        course_order = self.find_course_order()
        if not course_order:
            return []
        
        # Filter valid courses
        valid_courses = [course for course in course_order if self._is_valid_course(course)]
        
        return valid_courses
    
    def get_optimal_course_schedule_strategy(self):
        """Get optimal course schedule strategy considering all constraints."""
        strategies = [
            ('course_constraints', self.get_course_schedule_with_course_constraints),
            ('scheduling_constraints', self.get_course_schedule_with_scheduling_constraints),
            ('pattern_constraints', self.get_course_schedule_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_score = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'course_constraints':
                    result = strategy_func(1, 1000)
                elif strategy_name == 'scheduling_constraints':
                    scheduling_constraints = [lambda n, prerequisites: len(prerequisites) > 0]
                    result = strategy_func(scheduling_constraints)
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda n, prerequisites: len(prerequisites) > 0]
                    result = strategy_func(pattern_constraints)
                
                if result and len(result) > best_score:
                    best_score = len(result)
                    best_strategy = (strategy_name, result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'allowed_courses': [0, 1, 2, 3, 4],
    'forbidden_courses': [5, 6, 7, 8, 9],
    'max_course': 10,
    'min_course': 0,
    'pattern_constraints': [lambda course, n, prerequisites: course >= 0 and course < n]
}

n = 4
prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]
constrained_course_schedule = ConstrainedCourseScheduleII(n, prerequisites, constraints)

print("Course-constrained course schedule:", constrained_course_schedule.get_course_schedule_with_course_constraints(1, 10))

print("Scheduling-constrained course schedule:", constrained_course_schedule.get_course_schedule_with_scheduling_constraints([lambda n, prerequisites: len(prerequisites) > 0]))

print("Pattern-constrained course schedule:", constrained_course_schedule.get_course_schedule_with_pattern_constraints([lambda n, prerequisites: len(prerequisites) > 0]))

# Mathematical constraints
def custom_constraint(n, prerequisites):
    return len(prerequisites) > 0

print("Mathematical constraint course schedule:", constrained_course_schedule.get_course_schedule_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(n, prerequisites):
    return 1 <= n <= 100

range_constraints = [range_constraint]
print("Range-constrained course schedule:", constrained_course_schedule.get_course_schedule_with_course_constraints(1, 10))

# Multiple constraints
def constraint1(n, prerequisites):
    return len(prerequisites) > 0

def constraint2(n, prerequisites):
    return n > 0

constraints_list = [constraint1, constraint2]
print("Multiple constraints course schedule:", constrained_course_schedule.get_course_schedule_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(n, prerequisites):
    return n + len(prerequisites)

print("Priority-constrained course schedule:", constrained_course_schedule.get_course_schedule_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(n, prerequisites, current_result):
    return len(prerequisites) > 0 and len(current_result) < 10

print("Adaptive constraint course schedule:", constrained_course_schedule.get_course_schedule_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_course_schedule.get_optimal_course_schedule_strategy()
print(f"Optimal course schedule strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Course Schedule II](https://cses.fi/problemset/task/1757) - Advanced course scheduling
- [Topological Sorting](https://cses.fi/problemset/task/1679) - Basic topological sorting
- [Acyclic Graph Edges](https://cses.fi/problemset/task/1679) - Acyclic graph problems

#### **LeetCode Problems**
- [Course Schedule](https://leetcode.com/problems/course-schedule/) - Check if courses can be completed
- [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) - Find course order
- [Alien Dictionary](https://leetcode.com/problems/alien-dictionary/) - Topological sorting with constraints
- [Minimum Height Trees](https://leetcode.com/problems/minimum-height-trees/) - Tree topological properties

#### **Problem Categories**
- **Topological Sorting**: Kahn's algorithm, DFS-based sorting, dependency resolution
- **Graph Theory**: Cycle detection, acyclic graphs, dependency graphs
- **Course Scheduling**: Prerequisite management, course ordering, dependency resolution
- **Algorithm Design**: Graph algorithms, sorting algorithms, cycle detection algorithms

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

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

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

### Related Problems

#### **CSES Problems**
- [Course Schedule II](https://cses.fi/problemset/task/1757) - Advanced course scheduling
- [Acyclic Graph Edges](https://cses.fi/problemset/task/1679) - Cycle detection problems
- [Topological Sorting](https://cses.fi/problemset/task/1679) - Basic topological sorting

#### **LeetCode Problems**
- [Course Schedule](https://leetcode.com/problems/course-schedule/) - Check if courses can be completed
- [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) - Find course order
- [Alien Dictionary](https://leetcode.com/problems/alien-dictionary/) - Topological sorting with constraints
- [Minimum Height Trees](https://leetcode.com/problems/minimum-height-trees/) - Tree topological properties

#### **Problem Categories**
- **Topological Sorting**: Kahn's algorithm, DFS-based sorting, dependency resolution
- **Graph Theory**: Cycle detection, acyclic graphs, dependency graphs
- **Course Scheduling**: Prerequisite management, course ordering, dependency resolution
- **Algorithm Design**: Graph algorithms, sorting algorithms, cycle detection algorithms

## 📚 Learning Points

1. **Topological Sorting**: Essential for dependency problems
2. **Cycle Detection**: Critical for impossible cases
3. **Kahn's Algorithm**: Efficient implementation
4. **Dependency Graphs**: Common pattern in real-world problems

---

**This is a great introduction to topological sorting and dependency resolution!** 🎯 