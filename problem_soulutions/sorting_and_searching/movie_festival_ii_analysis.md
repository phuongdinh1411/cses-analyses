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
- **[Reason 3]**: [Explanation]
- **Optimal Approach**: [Final explanation]
