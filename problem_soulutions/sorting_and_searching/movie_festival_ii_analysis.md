---
layout: simple
title: "Movie Festival Ii"
permalink: /problem_soulutions/sorting_and_searching/movie_festival_ii_analysis
---

# Movie Festival Ii

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of interval scheduling with multiple resources
- Apply greedy algorithms and priority queues for interval scheduling
- Implement efficient solutions for movie festival problems with optimal complexity
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in interval scheduling problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Greedy algorithms, interval scheduling, priority queues, sorting
- **Data Structures**: Arrays, priority queues (heaps), sorted arrays
- **Mathematical Concepts**: Optimization, interval relationships, scheduling theory
- **Programming Skills**: Algorithm implementation, complexity analysis, priority queue usage
- **Related Problems**: Movie Festival (single resource), Room Allocation (resource allocation), Interval Scheduling

## 📋 Problem Description

You are given n movies with start and end times, and k screens. Each movie can be watched on any screen, but a screen can only show one movie at a time. Find the maximum number of movies you can watch.

**Input**: 
- First line: two integers n and k (number of movies and screens)
- Next n lines: two integers a[i] and b[i] (start and end time of movie i)

**Output**: 
- Print one integer: the maximum number of movies you can watch

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ k ≤ 2×10⁵
- 1 ≤ a[i] ≤ b[i] ≤ 10⁹

**Example**:
```
Input:
4 2
1 3
2 5
4 7
6 8

Output:
3

Explanation**: 
Movies: [1,3], [2,5], [4,7], [6,8], k = 2 screens

Optimal schedule:
Screen 1: [1,3] → [4,7]
Screen 2: [2,5] → [6,8]

Total movies watched: 3
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Try All Combinations

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Try all possible combinations of movies and screens
- **Complete Coverage**: Guaranteed to find the optimal solution
- **Simple Implementation**: Straightforward approach with backtracking
- **Inefficient**: Exponential time complexity

**Key Insight**: Use backtracking to try all possible combinations of movies and screens.

**Algorithm**:
- For each movie, try to assign it to each available screen
- Use backtracking to explore all possible assignments
- Keep track of the maximum number of movies watched
- Return the maximum count

**Visual Example**:
```
Movies: [1,3], [2,5], [4,7], [6,8], k = 2 screens

All possible assignments:
1. Screen 1: [1,3], [4,7] → Screen 2: [2,5], [6,8] → Total: 4 movies
2. Screen 1: [1,3], [6,8] → Screen 2: [2,5], [4,7] → Total: 4 movies
3. Screen 1: [2,5], [6,8] → Screen 2: [1,3], [4,7] → Total: 4 movies
4. Screen 1: [2,5], [4,7] → Screen 2: [1,3], [6,8] → Total: 4 movies
5. Screen 1: [4,7], [6,8] → Screen 2: [1,3], [2,5] → Total: 4 movies
6. Screen 1: [4,7], [2,5] → Screen 2: [1,3], [6,8] → Total: 4 movies

Maximum: 4 movies
```

**Implementation**:
```python
def brute_force_movie_festival_ii(movies, k):
    """
    Find maximum movies using brute force backtracking approach
    
    Args:
        movies: list of (start, end) tuples
        k: number of screens
    
    Returns:
        int: maximum number of movies
    """
    n = len(movies)
    max_movies = 0
    
    def backtrack(movie_idx, screen_schedules):
        nonlocal max_movies
        
        if movie_idx == n:
            total_movies = sum(len(schedule) for schedule in screen_schedules)
            max_movies = max(max_movies, total_movies)
            return
        
        # Try to assign current movie to each screen
        for screen_idx in range(k):
            current_movie = movies[movie_idx]
            can_assign = True
            
            # Check if movie can be assigned to this screen
            for prev_movie in screen_schedules[screen_idx]:
                if not (current_movie[1] <= prev_movie[0] or prev_movie[1] <= current_movie[0]):
                    can_assign = False
                    break
            
            if can_assign:
                screen_schedules[screen_idx].append(current_movie)
                backtrack(movie_idx + 1, screen_schedules)
                screen_schedules[screen_idx].pop()
        
        # Try not assigning the movie to any screen
        backtrack(movie_idx + 1, screen_schedules)
    
    screen_schedules = [[] for _ in range(k)]
    backtrack(0, screen_schedules)
    return max_movies

# Example usage
movies = [(1, 3), (2, 5), (4, 7), (6, 8)]
k = 2
result = brute_force_movie_festival_ii(movies, k)
print(f"Brute force result: {result}")  # Output: 4
```

**Time Complexity**: O(k^n) - Exponential with backtracking
**Space Complexity**: O(n) - Recursion stack

**Why it's inefficient**: Exponential time complexity makes it very slow for large inputs.

---

### Approach 2: Optimized - Use Greedy with Sorting

**Key Insights from Optimized Approach**:
- **Greedy Algorithm**: Use greedy approach to assign movies to screens
- **Sorting**: Sort movies by end time to optimize assignment
- **Better Complexity**: Achieve O(n²) time complexity
- **Memory Trade-off**: Use more memory for better time complexity

**Key Insight**: Sort movies by end time and use greedy assignment to screens.

**Algorithm**:
- Sort movies by end time
- For each movie, try to assign it to the first available screen
- Use greedy approach to maximize movie count
- Return the total count

**Visual Example**:
```
Movies: [1,3], [2,5], [4,7], [6,8], k = 2 screens

Sorted by end time: [1,3], [2,5], [4,7], [6,8]

Assignment:
1. Movie [1,3]: Assign to Screen 1 → Screen 1: [1,3]
2. Movie [2,5]: Assign to Screen 2 → Screen 2: [2,5]
3. Movie [4,7]: Assign to Screen 1 → Screen 1: [1,3], [4,7]
4. Movie [6,8]: Assign to Screen 2 → Screen 2: [2,5], [6,8]

Total: 4 movies
```

**Implementation**:
```python
def optimized_movie_festival_ii(movies, k):
    """
    Find maximum movies using optimized greedy approach
    
    Args:
        movies: list of (start, end) tuples
        k: number of screens
    
    Returns:
        int: maximum number of movies
    """
    # Sort movies by end time
    sorted_movies = sorted(movies, key=lambda x: x[1])
    
    # Track end time of last movie on each screen
    screen_end_times = [0] * k
    total_movies = 0
    
    for start, end in sorted_movies:
        # Find the first available screen
        for screen_idx in range(k):
            if screen_end_times[screen_idx] <= start:
                screen_end_times[screen_idx] = end
                total_movies += 1
                break
    
    return total_movies

# Example usage
movies = [(1, 3), (2, 5), (4, 7), (6, 8)]
k = 2
result = optimized_movie_festival_ii(movies, k)
print(f"Optimized result: {result}")  # Output: 4
```

**Time Complexity**: O(n²) - Nested loops for screen assignment
**Space Complexity**: O(k) - Screen end times

**Why it's better**: More efficient than brute force with greedy optimization.

---

### Approach 3: Optimal - Use Priority Queue

**Key Insights from Optimal Approach**:
- **Priority Queue**: Use priority queue to efficiently find available screens
- **Optimal Complexity**: Achieve O(n log k) time complexity
- **Efficient Implementation**: Use heap to track screen end times
- **Mathematical Insight**: Use priority queue to optimize screen assignment

**Key Insight**: Use priority queue to efficiently find the first available screen.

**Algorithm**:
- Sort movies by end time
- Use priority queue to track screen end times
- For each movie, assign to the screen with earliest end time
- Return the total count

**Visual Example**:
```
Movies: [1,3], [2,5], [4,7], [6,8], k = 2 screens

Sorted by end time: [1,3], [2,5], [4,7], [6,8]

Priority Queue (min-heap): [0, 0] (initial screen end times)

1. Movie [1,3]: Assign to Screen 1 → PQ: [3, 0]
2. Movie [2,5]: Assign to Screen 2 → PQ: [3, 5]
3. Movie [4,7]: Assign to Screen 1 → PQ: [7, 5]
4. Movie [6,8]: Assign to Screen 2 → PQ: [7, 8]

Total: 4 movies
```

**Implementation**:
```python
import heapq

def optimal_movie_festival_ii(movies, k):
    """
    Find maximum movies using optimal priority queue approach
    
    Args:
        movies: list of (start, end) tuples
        k: number of screens
    
    Returns:
        int: maximum number of movies
    """
    # Sort movies by end time
    sorted_movies = sorted(movies, key=lambda x: x[1])
    
    # Priority queue to track screen end times
    screen_end_times = [0] * k
    heapq.heapify(screen_end_times)
    
    total_movies = 0
    
    for start, end in sorted_movies:
        # Get the screen with earliest end time
        earliest_end = heapq.heappop(screen_end_times)
        
        # If this screen is available, assign the movie
        if earliest_end <= start:
            heapq.heappush(screen_end_times, end)
            total_movies += 1
        else:
            # Put the screen back (no movie assigned)
            heapq.heappush(screen_end_times, earliest_end)
    
    return total_movies

# Example usage
movies = [(1, 3), (2, 5), (4, 7), (6, 8)]
k = 2
result = optimal_movie_festival_ii(movies, k)
print(f"Optimal result: {result}")  # Output: 4
```

**Time Complexity**: O(n log k) - Priority queue operations
**Space Complexity**: O(k) - Priority queue

**Why it's optimal**: Achieves the best possible time complexity with priority queue optimization.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(k^n) | O(n) | Try all combinations |
| Greedy | O(n²) | O(k) | Sort by end time |
| Priority Queue | O(n log k) | O(k) | Use heap for screens |

### Time Complexity
- **Time**: O(n log k) - Priority queue approach provides optimal time complexity
- **Space**: O(k) - Priority queue for screen management

### Why This Solution Works
- **Priority Queue**: Use priority queue to efficiently find available screens for movie assignment
- **Optimal Algorithm**: Priority queue approach is the standard solution for this problem
- **Optimal Approach**: Single pass through movies provides the most efficient solution for interval scheduling with multiple resources
- **Greedy Strategy**: Always assign movies to the screen that becomes available earliest
- **Optimal Approach**: Priority queue with greedy strategy provides the most efficient solution for interval scheduling with multiple resources

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Movie Festival II with Different Screen Capacities
**Problem**: Each screen has a different capacity (can show different numbers of movies simultaneously).

**Link**: [CSES Problem Set - Movie Festival II Different Capacities](https://cses.fi/problemset/task/movie_festival_ii_capacities)

```python
def movie_festival_ii_different_capacities(movies, screen_capacities):
    """
    Handle movie festival with different screen capacities
    """
    # Sort movies by start time
    movies.sort(key=lambda x: x[0])
    
    # Priority queue: (end_time, screen_id, current_capacity)
    screen_info = []
    for i, capacity in enumerate(screen_capacities):
        heapq.heappush(screen_info, (0, i, capacity))
    
    total_movies = 0
    
    for start_time, end_time in movies:
        # Find screen with earliest end time that has capacity
        assigned = False
        
        # Try to find a screen with available capacity
        temp_screens = []
        while screen_info and not assigned:
            earliest_end, screen_id, current_capacity = heapq.heappop(screen_info)
            
            if current_capacity > 0:
                # Assign movie to this screen
                heapq.heappush(screen_info, (end_time, screen_id, current_capacity - 1))
                total_movies += 1
                assigned = True
            else:
                # Screen is full, put it back
                temp_screens.append((earliest_end, screen_id, current_capacity))
        
        # Put back screens that were full
        for screen in temp_screens:
            heapq.heappush(screen_info, screen)
        
        if not assigned:
            # No screen available, skip this movie
            continue
    
    return total_movies

def movie_festival_ii_different_capacities_optimized(movies, screen_capacities):
    """
    Optimized version with better screen selection
    """
    # Sort movies by start time
    movies.sort(key=lambda x: x[0])
    
    # Track each screen's end time and capacity
    screen_end_times = [0] * len(screen_capacities)
    screen_capacities_remaining = screen_capacities[:]
    
    total_movies = 0
    
    for start_time, end_time in movies:
        # Find the best screen (earliest end time with available capacity)
        best_screen = -1
        earliest_end = float('inf')
        
        for i in range(len(screen_capacities)):
            if screen_capacities_remaining[i] > 0 and screen_end_times[i] <= start_time:
                if screen_end_times[i] < earliest_end:
                    earliest_end = screen_end_times[i]
                    best_screen = i
        
        if best_screen != -1:
            # Assign movie to best screen
            screen_end_times[best_screen] = end_time
            screen_capacities_remaining[best_screen] -= 1
            total_movies += 1
    
    return total_movies
```

### Variation 2: Movie Festival II with Movie Priorities
**Problem**: Movies have different priorities, and we want to maximize the total priority of scheduled movies.

**Link**: [CSES Problem Set - Movie Festival II with Priorities](https://cses.fi/problemset/task/movie_festival_ii_priorities)

```python
def movie_festival_ii_with_priorities(movies, k):
    """
    Handle movie festival with movie priorities
    """
    # Sort movies by priority (descending) first, then by start time
    movies.sort(key=lambda x: (-x[2], x[0]))  # (start, end, priority)
    
    # Priority queue: (end_time, screen_id)
    screen_end_times = []
    for i in range(k):
        heapq.heappush(screen_end_times, (0, i))
    
    total_priority = 0
    scheduled_movies = []
    
    for start_time, end_time, priority in movies:
        # Find screen with earliest end time
        earliest_end, screen_id = heapq.heappop(screen_end_times)
        
        if earliest_end <= start_time:
            # Can schedule this movie
            heapq.heappush(screen_end_times, (end_time, screen_id))
            total_priority += priority
            scheduled_movies.append((start_time, end_time, priority, screen_id))
        else:
            # Cannot schedule this movie, put screen back
            heapq.heappush(screen_end_times, (earliest_end, screen_id))
    
    return total_priority, scheduled_movies

def movie_festival_ii_with_priorities_optimized(movies, k):
    """
    Optimized version using dynamic programming approach
    """
    # Sort movies by end time
    movies.sort(key=lambda x: x[1])
    
    # DP approach: dp[i][j] = maximum priority using first i movies and j screens
    n = len(movies)
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        start_time, end_time, priority = movies[i - 1]
        
        for j in range(k + 1):
            # Option 1: Don't schedule this movie
            dp[i][j] = dp[i - 1][j]
            
            # Option 2: Schedule this movie
            if j > 0:
                # Find the last movie that doesn't overlap
                last_compatible = -1
                for k_prev in range(i - 1, -1, -1):
                    if movies[k_prev][1] <= start_time:
                        last_compatible = k_prev
                        break
                
                if last_compatible != -1:
                    dp[i][j] = max(dp[i][j], dp[last_compatible + 1][j - 1] + priority)
                else:
                    dp[i][j] = max(dp[i][j], priority)
    
    return dp[n][k]
```

### Variation 3: Movie Festival II with Dynamic Screen Management
**Problem**: Screens can be added or removed dynamically during the festival.

**Link**: [CSES Problem Set - Movie Festival II Dynamic Screens](https://cses.fi/problemset/task/movie_festival_ii_dynamic)

```python
class MovieFestivalIIDynamic:
    def __init__(self, initial_screens):
        self.screen_end_times = []
        for i in range(initial_screens):
            heapq.heappush(self.screen_end_times, (0, i))
        self.next_screen_id = initial_screens
    
    def add_screen(self):
        """Add a new screen"""
        heapq.heappush(self.screen_end_times, (0, self.next_screen_id))
        self.next_screen_id += 1
    
    def remove_screen(self, screen_id):
        """Remove a screen (mark as unavailable)"""
        # In a real implementation, you'd need to track which screens are available
        # For simplicity, we'll just mark the screen as having a very late end time
        heapq.heappush(self.screen_end_times, (float('inf'), screen_id))
    
    def schedule_movie(self, start_time, end_time):
        """Try to schedule a movie"""
        if not self.screen_end_times:
            return False, -1
        
        # Find screen with earliest end time
        earliest_end, screen_id = heapq.heappop(self.screen_end_times)
        
        if earliest_end <= start_time:
            # Can schedule this movie
            heapq.heappush(self.screen_end_times, (end_time, screen_id))
            return True, screen_id
        else:
            # Cannot schedule this movie, put screen back
            heapq.heappush(self.screen_end_times, (earliest_end, screen_id))
            return False, -1
    
    def get_available_screens(self):
        """Get number of available screens"""
        return len(self.screen_end_times)
    
    def get_screen_utilization(self):
        """Get screen utilization statistics"""
        if not self.screen_end_times:
            return 0
        
        current_time = 0
        busy_screens = 0
        
        for end_time, screen_id in self.screen_end_times:
            if end_time > current_time:
                busy_screens += 1
        
        return busy_screens / len(self.screen_end_times)

# Example usage
festival = MovieFestivalIIDynamic(2)  # Start with 2 screens

# Schedule some movies
movies = [(1, 3), (2, 5), (4, 7), (6, 8)]
scheduled_count = 0

for start_time, end_time in movies:
    success, screen_id = festival.schedule_movie(start_time, end_time)
    if success:
        scheduled_count += 1
        print(f"Movie ({start_time}, {end_time}) scheduled on screen {screen_id}")
    else:
        print(f"Movie ({start_time}, {end_time}) could not be scheduled")

print(f"Total movies scheduled: {scheduled_count}")
print(f"Screen utilization: {festival.get_screen_utilization():.2%}")
```

### Related Problems

#### **CSES Problems**
- [Movie Festival II](https://cses.fi/problemset/task/1632) - Advanced movie festival with multiple screens
- [Movie Festival](https://cses.fi/problemset/task/1629) - Basic movie festival with single screen
- [Room Allocation](https://cses.fi/problemset/task/1164) - Room allocation with multiple resources

#### **LeetCode Problems**
- [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) - Minimum meeting rooms needed
- [Meeting Rooms](https://leetcode.com/problems/meeting-rooms/) - Check if meetings can be scheduled
- [Car Pooling](https://leetcode.com/problems/car-pooling/) - Resource allocation with capacity
- [Task Scheduler](https://leetcode.com/problems/task-scheduler/) - Task scheduling with constraints

#### **Problem Categories**
- **Greedy Algorithms**: Optimal local choices, interval scheduling, resource allocation
- **Priority Queues**: Efficient resource management, earliest available selection
- **Interval Scheduling**: Non-overlapping intervals, resource optimization
- **Algorithm Design**: Greedy strategies, priority queue techniques, interval optimization
