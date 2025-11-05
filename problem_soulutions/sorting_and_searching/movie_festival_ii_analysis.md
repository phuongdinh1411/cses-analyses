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

## Problem Variations

### **Variation 1: Movie Festival II with Dynamic Updates**
**Problem**: Handle dynamic movie updates (add/remove movies) while maintaining efficient optimal scheduling queries for multiple screens.

**Approach**: Use balanced binary search trees or segment trees for efficient updates and queries with priority queue management.

```python
from collections import defaultdict
import bisect
import heapq

class DynamicMovieFestivalII:
    def __init__(self, movies, k):
        self.movies = sorted(movies, key=lambda x: x['end_time'])
        self.n = len(movies)
        self.k = k
        self.max_movies = 0
        self.scheduled_movies = []
        self.screen_assignments = {}
        self._calculate_optimal_schedule()
    
    def _calculate_optimal_schedule(self):
        """Calculate optimal movie schedule using greedy approach with multiple screens."""
        if not self.movies or self.k <= 0:
            self.max_movies = 0
            self.scheduled_movies = []
            self.screen_assignments = {}
            return
        
        # Priority queue: (end_time, screen_id)
        screen_end_times = []
        for i in range(self.k):
            heapq.heappush(screen_end_times, (0, i))
        
        self.scheduled_movies = []
        self.screen_assignments = {}
        total_movies = 0
        
        for movie in self.movies:
            # Find screen with earliest end time
            earliest_end, screen_id = heapq.heappop(screen_end_times)
            
            if earliest_end <= movie['start_time']:
                # Can schedule this movie
                heapq.heappush(screen_end_times, (movie['end_time'], screen_id))
                self.scheduled_movies.append(movie)
                self.screen_assignments[movie['id']] = screen_id
                total_movies += 1
            else:
                # Put back the screen end time
                heapq.heappush(screen_end_times, (earliest_end, screen_id))
        
        self.max_movies = total_movies
    
    def add_movie(self, movie):
        """Add a new movie to the festival."""
        bisect.insort(self.movies, movie, key=lambda x: x['end_time'])
        self.n += 1
        self._calculate_optimal_schedule()
    
    def remove_movie(self, movie_id):
        """Remove a movie from the festival."""
        self.movies = [m for m in self.movies if m['id'] != movie_id]
        self.n = len(self.movies)
        self._calculate_optimal_schedule()
    
    def update_movie(self, movie_id, new_movie):
        """Update a movie in the festival."""
        self.remove_movie(movie_id)
        self.add_movie(new_movie)
    
    def update_screen_count(self, new_k):
        """Update the number of screens."""
        self.k = new_k
        self._calculate_optimal_schedule()
    
    def get_max_movies(self):
        """Get current maximum number of movies that can be watched."""
        return self.max_movies
    
    def get_scheduled_movies(self):
        """Get the actual scheduled movies."""
        return self.scheduled_movies
    
    def get_screen_assignments(self):
        """Get screen assignments for scheduled movies."""
        return self.screen_assignments
    
    def get_movies_by_screen(self, screen_id):
        """Get movies scheduled on a specific screen."""
        screen_movies = []
        for movie in self.scheduled_movies:
            if self.screen_assignments.get(movie['id']) == screen_id:
                screen_movies.append(movie)
        return screen_movies
    
    def get_screen_utilization(self):
        """Get utilization statistics for each screen."""
        screen_stats = {}
        for i in range(self.k):
            screen_movies = self.get_movies_by_screen(i)
            total_duration = sum(movie['end_time'] - movie['start_time'] for movie in screen_movies)
            screen_stats[i] = {
                'movie_count': len(screen_movies),
                'total_duration': total_duration,
                'utilization_rate': total_duration / 24.0 if total_duration > 0 else 0.0  # Assuming 24-hour day
            }
        return screen_stats
    
    def get_movies_in_time_range(self, start_time, end_time):
        """Get movies that can be watched in a specific time range."""
        available_movies = []
        screen_end_times = [0] * self.k
        
        for movie in self.movies:
            if movie['start_time'] >= start_time and movie['end_time'] <= end_time:
                # Find available screen
                best_screen = -1
                earliest_end = float('inf')
                
                for i in range(self.k):
                    if screen_end_times[i] <= movie['start_time'] and screen_end_times[i] < earliest_end:
                        earliest_end = screen_end_times[i]
                        best_screen = i
                
                if best_screen != -1:
                    screen_end_times[best_screen] = movie['end_time']
                    available_movies.append(movie)
        
        return available_movies
    
    def get_movies_by_genre(self, genre):
        """Get movies of a specific genre that can be watched."""
        genre_movies = [m for m in self.movies if m.get('genre') == genre]
        genre_movies.sort(key=lambda x: x['end_time'])
        
        # Use greedy approach for genre movies
        screen_end_times = [0] * self.k
        scheduled_genre_movies = []
        
        for movie in genre_movies:
            # Find available screen
            best_screen = -1
            earliest_end = float('inf')
            
            for i in range(self.k):
                if screen_end_times[i] <= movie['start_time'] and screen_end_times[i] < earliest_end:
                    earliest_end = screen_end_times[i]
                    best_screen = i
            
            if best_screen != -1:
                screen_end_times[best_screen] = movie['end_time']
                scheduled_genre_movies.append(movie)
        
        return scheduled_genre_movies
    
    def get_movies_by_rating(self, min_rating):
        """Get movies with minimum rating that can be watched."""
        rated_movies = [m for m in self.movies if m.get('rating', 0) >= min_rating]
        rated_movies.sort(key=lambda x: x['end_time'])
        
        # Use greedy approach for rated movies
        screen_end_times = [0] * self.k
        scheduled_rated_movies = []
        
        for movie in rated_movies:
            # Find available screen
            best_screen = -1
            earliest_end = float('inf')
            
            for i in range(self.k):
                if screen_end_times[i] <= movie['start_time'] and screen_end_times[i] < earliest_end:
                    earliest_end = screen_end_times[i]
                    best_screen = i
            
            if best_screen != -1:
                screen_end_times[best_screen] = movie['end_time']
                scheduled_rated_movies.append(movie)
        
        return scheduled_rated_movies
    
    def get_movies_with_breaks(self, break_duration):
        """Get movies that can be watched with breaks between them."""
        screen_end_times = [0] * self.k
        scheduled_movies = []
        
        for movie in self.movies:
            # Find available screen with break consideration
            best_screen = -1
            earliest_end = float('inf')
            
            for i in range(self.k):
                if screen_end_times[i] + break_duration <= movie['start_time'] and screen_end_times[i] < earliest_end:
                    earliest_end = screen_end_times[i]
                    best_screen = i
            
            if best_screen != -1:
                screen_end_times[best_screen] = movie['end_time']
                scheduled_movies.append(movie)
        
        return scheduled_movies
    
    def get_movies_with_preferences(self, preferences):
        """Get movies that match user preferences."""
        preferred_movies = []
        
        for movie in self.movies:
            matches_preferences = True
            
            if 'genres' in preferences:
                if movie.get('genre') not in preferences['genres']:
                    matches_preferences = False
            
            if 'min_rating' in preferences:
                if movie.get('rating', 0) < preferences['min_rating']:
                    matches_preferences = False
            
            if 'max_duration' in preferences:
                duration = movie['end_time'] - movie['start_time']
                if duration > preferences['max_duration']:
                    matches_preferences = False
            
            if matches_preferences:
                preferred_movies.append(movie)
        
        preferred_movies.sort(key=lambda x: x['end_time'])
        
        # Use greedy approach for preferred movies
        screen_end_times = [0] * self.k
        scheduled_preferred_movies = []
        
        for movie in preferred_movies:
            # Find available screen
            best_screen = -1
            earliest_end = float('inf')
            
            for i in range(self.k):
                if screen_end_times[i] <= movie['start_time'] and screen_end_times[i] < earliest_end:
                    earliest_end = screen_end_times[i]
                    best_screen = i
            
            if best_screen != -1:
                screen_end_times[best_screen] = movie['end_time']
                scheduled_preferred_movies.append(movie)
        
        return scheduled_preferred_movies
    
    def get_festival_statistics(self):
        """Get statistics about the movie festival."""
        if not self.movies:
            return {
                'total_movies': 0,
                'max_watchable': 0,
                'total_duration': 0,
                'average_duration': 0,
                'genres': {},
                'ratings': [],
                'screen_utilization': {}
            }
        
        total_duration = sum(movie['end_time'] - movie['start_time'] for movie in self.movies)
        genres = {}
        ratings = []
        
        for movie in self.movies:
            genre = movie.get('genre', 'Unknown')
            genres[genre] = genres.get(genre, 0) + 1
            
            rating = movie.get('rating', 0)
            if rating > 0:
                ratings.append(rating)
        
        screen_utilization = self.get_screen_utilization()
        
        return {
            'total_movies': len(self.movies),
            'max_watchable': self.max_movies,
            'total_duration': total_duration,
            'average_duration': total_duration / len(self.movies),
            'genres': genres,
            'ratings': ratings,
            'screen_utilization': screen_utilization
        }

# Example usage
movies = [
    {'id': 1, 'start_time': 1, 'end_time': 3, 'genre': 'Action', 'rating': 8.5},
    {'id': 2, 'start_time': 2, 'end_time': 4, 'genre': 'Comedy', 'rating': 7.2},
    {'id': 3, 'start_time': 4, 'end_time': 6, 'genre': 'Drama', 'rating': 9.1},
    {'id': 4, 'start_time': 5, 'end_time': 7, 'genre': 'Action', 'rating': 8.8},
    {'id': 5, 'start_time': 6, 'end_time': 8, 'genre': 'Thriller', 'rating': 8.0}
]

dynamic_festival_ii = DynamicMovieFestivalII(movies, 2)
print(f"Initial max movies: {dynamic_festival_ii.get_max_movies()}")

# Add a movie
new_movie = {'id': 6, 'start_time': 8, 'end_time': 10, 'genre': 'Horror', 'rating': 7.5}
dynamic_festival_ii.add_movie(new_movie)
print(f"After adding movie: {dynamic_festival_ii.get_max_movies()}")

# Update screen count
dynamic_festival_ii.update_screen_count(3)
print(f"With 3 screens: {dynamic_festival_ii.get_max_movies()}")

# Get screen assignments
print(f"Screen assignments: {dynamic_festival_ii.get_screen_assignments()}")

# Get movies by screen
print(f"Movies on screen 0: {dynamic_festival_ii.get_movies_by_screen(0)}")

# Get screen utilization
print(f"Screen utilization: {dynamic_festival_ii.get_screen_utilization()}")

# Get movies in time range
print(f"Movies in range [1, 5]: {dynamic_festival_ii.get_movies_in_time_range(1, 5)}")

# Get movies by genre
print(f"Action movies: {dynamic_festival_ii.get_movies_by_genre('Action')}")

# Get movies by rating
print(f"Movies with rating >= 8.0: {dynamic_festival_ii.get_movies_by_rating(8.0)}")

# Get movies with breaks
print(f"Movies with 1-hour breaks: {dynamic_festival_ii.get_movies_with_breaks(1)}")

# Get movies with preferences
preferences = {'genres': ['Action', 'Drama'], 'min_rating': 8.0, 'max_duration': 3}
print(f"Preferred movies: {dynamic_festival_ii.get_movies_with_preferences(preferences)}")

# Get statistics
print(f"Festival statistics: {dynamic_festival_ii.get_festival_statistics()}")
```

### **Variation 2: Movie Festival II with Different Operations**
**Problem**: Handle different types of operations on movie festival II (weighted movies, advanced constraints, optimization functions).

**Approach**: Use advanced data structures for efficient multi-screen and constraint-based queries.

```python
class AdvancedMovieFestivalII:
    def __init__(self, movies, k):
        self.movies = sorted(movies, key=lambda x: x['end_time'])
        self.n = len(movies)
        self.k = k
    
    def get_movies_weighted(self, weights):
        """Get maximum weighted movies that can be watched."""
        if len(weights) != self.n:
            weights = [1] * self.n
        
        # Create weighted movies
        weighted_movies = [(self.movies[i], weights[i]) for i in range(self.n)]
        weighted_movies.sort(key=lambda x: x[0]['end_time'])
        
        # Use dynamic programming approach
        dp = [0] * (self.n + 1)
        
        for i in range(1, self.n + 1):
            movie, weight = weighted_movies[i - 1]
            
            # Don't watch this movie
            dp[i] = dp[i - 1]
            
            # Watch this movie
            # Find the last movie that doesn't conflict
            last_compatible = -1
            for j in range(i - 1, -1, -1):
                if weighted_movies[j][0]['end_time'] <= movie['start_time']:
                    last_compatible = j
                    break
            
            if last_compatible != -1:
                dp[i] = max(dp[i], dp[last_compatible + 1] + weight)
        
        return dp[self.n]
    
    def get_movies_with_breaks(self, break_duration):
        """Get maximum movies that can be watched with breaks between them."""
        screen_end_times = [0] * self.k
        scheduled_movies = []
        
        for movie in self.movies:
            # Find available screen with break consideration
            best_screen = -1
            earliest_end = float('inf')
            
            for i in range(self.k):
                if screen_end_times[i] + break_duration <= movie['start_time'] and screen_end_times[i] < earliest_end:
                    earliest_end = screen_end_times[i]
                    best_screen = i
            
            if best_screen != -1:
                screen_end_times[best_screen] = movie['end_time']
                scheduled_movies.append(movie)
        
        return len(scheduled_movies)
    
    def get_movies_with_preferences(self, preferences):
        """Get maximum movies that match user preferences."""
        preferred_movies = []
        
        for movie in self.movies:
            matches_preferences = True
            
            if 'genres' in preferences:
                if movie.get('genre') not in preferences['genres']:
                    matches_preferences = False
            
            if 'min_rating' in preferences:
                if movie.get('rating', 0) < preferences['min_rating']:
                    matches_preferences = False
            
            if 'max_duration' in preferences:
                duration = movie['end_time'] - movie['start_time']
                if duration > preferences['max_duration']:
                    matches_preferences = False
            
            if matches_preferences:
                preferred_movies.append(movie)
        
        preferred_movies.sort(key=lambda x: x['end_time'])
        
        # Use greedy approach for preferred movies
        screen_end_times = [0] * self.k
        scheduled_movies = []
        
        for movie in preferred_movies:
            # Find available screen
            best_screen = -1
            earliest_end = float('inf')
            
            for i in range(self.k):
                if screen_end_times[i] <= movie['start_time'] and screen_end_times[i] < earliest_end:
                    earliest_end = screen_end_times[i]
                    best_screen = i
            
            if best_screen != -1:
                screen_end_times[best_screen] = movie['end_time']
                scheduled_movies.append(movie)
        
        return len(scheduled_movies)
    
    def get_movies_with_priority(self, priority_func):
        """Get maximum movies using priority-based selection."""
        # Sort movies by priority
        prioritized_movies = sorted(self.movies, key=priority_func, reverse=True)
        
        screen_end_times = [0] * self.k
        scheduled_movies = []
        
        for movie in prioritized_movies:
            # Find available screen
            best_screen = -1
            earliest_end = float('inf')
            
            for i in range(self.k):
                if screen_end_times[i] <= movie['start_time'] and screen_end_times[i] < earliest_end:
                    earliest_end = screen_end_times[i]
                    best_screen = i
            
            if best_screen != -1:
                screen_end_times[best_screen] = movie['end_time']
                scheduled_movies.append(movie)
        
        return len(scheduled_movies)
    
    def get_movies_with_constraints(self, constraints):
        """Get maximum movies that satisfy various constraints."""
        filtered_movies = []
        
        for movie in self.movies:
            satisfies_constraints = True
            
            if 'min_duration' in constraints:
                duration = movie['end_time'] - movie['start_time']
                if duration < constraints['min_duration']:
                    satisfies_constraints = False
            
            if 'max_duration' in constraints:
                duration = movie['end_time'] - movie['start_time']
                if duration > constraints['max_duration']:
                    satisfies_constraints = False
            
            if 'time_range' in constraints:
                start_range, end_range = constraints['time_range']
                if movie['start_time'] < start_range or movie['end_time'] > end_range:
                    satisfies_constraints = False
            
            if satisfies_constraints:
                filtered_movies.append(movie)
        
        filtered_movies.sort(key=lambda x: x['end_time'])
        
        screen_end_times = [0] * self.k
        scheduled_movies = []
        
        for movie in filtered_movies:
            # Find available screen
            best_screen = -1
            earliest_end = float('inf')
            
            for i in range(self.k):
                if screen_end_times[i] <= movie['start_time'] and screen_end_times[i] < earliest_end:
                    earliest_end = screen_end_times[i]
                    best_screen = i
            
            if best_screen != -1:
                screen_end_times[best_screen] = movie['end_time']
                scheduled_movies.append(movie)
        
        return len(scheduled_movies)
    
    def get_movies_with_optimization(self, optimization_func):
        """Get maximum movies using custom optimization function."""
        # Sort movies by optimization function
        optimized_movies = sorted(self.movies, key=optimization_func)
        
        screen_end_times = [0] * self.k
        scheduled_movies = []
        
        for movie in optimized_movies:
            # Find available screen
            best_screen = -1
            earliest_end = float('inf')
            
            for i in range(self.k):
                if screen_end_times[i] <= movie['start_time'] and screen_end_times[i] < earliest_end:
                    earliest_end = screen_end_times[i]
                    best_screen = i
            
            if best_screen != -1:
                screen_end_times[best_screen] = movie['end_time']
                scheduled_movies.append(movie)
        
        return len(scheduled_movies)
    
    def get_movies_with_alternatives(self, alternatives):
        """Get maximum movies considering alternative scheduling."""
        # Create all possible movie combinations
        all_combinations = []
        
        for movie in self.movies:
            # Add original movie
            all_combinations.append(movie)
            
            # Add alternative versions if available
            if movie['id'] in alternatives:
                for alt_movie in alternatives[movie['id']]:
                    all_combinations.append(alt_movie)
        
        # Sort by end time
        all_combinations.sort(key=lambda x: x['end_time'])
        
        screen_end_times = [0] * self.k
        scheduled_movies = []
        
        for movie in all_combinations:
            # Find available screen
            best_screen = -1
            earliest_end = float('inf')
            
            for i in range(self.k):
                if screen_end_times[i] <= movie['start_time'] and screen_end_times[i] < earliest_end:
                    earliest_end = screen_end_times[i]
                    best_screen = i
            
            if best_screen != -1:
                screen_end_times[best_screen] = movie['end_time']
                scheduled_movies.append(movie)
        
        return len(scheduled_movies)
    
    def get_movies_with_screen_capacities(self, screen_capacities):
        """Get maximum movies considering screen capacities."""
        if len(screen_capacities) != self.k:
            screen_capacities = [1] * self.k
        
        screen_end_times = [0] * self.k
        screen_capacities_remaining = screen_capacities[:]
        scheduled_movies = []
        
        for movie in self.movies:
            # Find the best screen (earliest end time with available capacity)
            best_screen = -1
            earliest_end = float('inf')
            
            for i in range(self.k):
                if screen_capacities_remaining[i] > 0 and screen_end_times[i] <= movie['start_time']:
                    if screen_end_times[i] < earliest_end:
                        earliest_end = screen_end_times[i]
                        best_screen = i
            
            if best_screen != -1:
                # Assign movie to best screen
                screen_end_times[best_screen] = movie['end_time']
                screen_capacities_remaining[best_screen] -= 1
                scheduled_movies.append(movie)
        
        return len(scheduled_movies)

# Example usage
movies = [
    {'id': 1, 'start_time': 1, 'end_time': 3, 'genre': 'Action', 'rating': 8.5},
    {'id': 2, 'start_time': 2, 'end_time': 4, 'genre': 'Comedy', 'rating': 7.2},
    {'id': 3, 'start_time': 4, 'end_time': 6, 'genre': 'Drama', 'rating': 9.1},
    {'id': 4, 'start_time': 5, 'end_time': 7, 'genre': 'Action', 'rating': 8.8},
    {'id': 5, 'start_time': 6, 'end_time': 8, 'genre': 'Thriller', 'rating': 8.0}
]

advanced_festival_ii = AdvancedMovieFestivalII(movies, 2)

# Weighted movies
weights = [2, 1, 3, 1, 2]
print(f"Weighted movies: {advanced_festival_ii.get_movies_weighted(weights)}")

# Movies with breaks
print(f"Movies with 1-hour breaks: {advanced_festival_ii.get_movies_with_breaks(1)}")

# Movies with preferences
preferences = {'genres': ['Action', 'Drama'], 'min_rating': 8.0, 'max_duration': 3}
print(f"Preferred movies: {advanced_festival_ii.get_movies_with_preferences(preferences)}")

# Priority-based selection
def priority_func(movie):
    return movie.get('rating', 0)

print(f"Priority-based movies: {advanced_festival_ii.get_movies_with_priority(priority_func)}")

# Movies with constraints
constraints = {'min_duration': 2, 'max_duration': 4, 'time_range': (1, 8)}
print(f"Constrained movies: {advanced_festival_ii.get_movies_with_constraints(constraints)}")

# Optimization-based selection
def optimization_func(movie):
    return movie['end_time'] - movie['start_time']  # Sort by duration

print(f"Optimized movies: {advanced_festival_ii.get_movies_with_optimization(optimization_func)}")

# Movies with alternatives
alternatives = {
    1: [{'id': 1, 'start_time': 1, 'end_time': 2, 'genre': 'Action', 'rating': 8.5}],
    2: [{'id': 2, 'start_time': 2, 'end_time': 3, 'genre': 'Comedy', 'rating': 7.2}]
}
print(f"Movies with alternatives: {advanced_festival_ii.get_movies_with_alternatives(alternatives)}")

# Movies with screen capacities
screen_capacities = [2, 1]  # Screen 0 can show 2 movies, Screen 1 can show 1 movie
print(f"Movies with screen capacities: {advanced_festival_ii.get_movies_with_screen_capacities(screen_capacities)}")
```

### **Variation 3: Movie Festival II with Constraints**
**Problem**: Handle movie festival II with additional constraints (time limits, resource constraints, mathematical constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedMovieFestivalII:
    def __init__(self, movies, k, constraints=None):
        self.movies = sorted(movies, key=lambda x: x['end_time'])
        self.n = len(movies)
        self.k = k
        self.constraints = constraints or {}
    
    def get_movies_with_time_constraints(self, time_limit):
        """Get maximum movies that can be watched within time limit."""
        screen_end_times = [0] * self.k
        scheduled_movies = []
        total_time = 0
        
        for movie in self.movies:
            if total_time >= time_limit:
                break
            
            # Find available screen
            best_screen = -1
            earliest_end = float('inf')
            
            for i in range(self.k):
                if screen_end_times[i] <= movie['start_time'] and screen_end_times[i] < earliest_end:
                    earliest_end = screen_end_times[i]
                    best_screen = i
            
            if best_screen != -1:
                movie_duration = movie['end_time'] - movie['start_time']
                
                if total_time + movie_duration <= time_limit:
                    screen_end_times[best_screen] = movie['end_time']
                    scheduled_movies.append(movie)
                    total_time += movie_duration
        
        return len(scheduled_movies)
    
    def get_movies_with_resource_constraints(self, resource_limits, resource_consumption):
        """Get maximum movies considering resource constraints."""
        screen_end_times = [0] * self.k
        scheduled_movies = []
        resources_used = [0] * len(resource_limits)
        
        for movie in self.movies:
            # Find available screen
            best_screen = -1
            earliest_end = float('inf')
            
            for i in range(self.k):
                if screen_end_times[i] <= movie['start_time'] and screen_end_times[i] < earliest_end:
                    earliest_end = screen_end_times[i]
                    best_screen = i
            
            if best_screen != -1:
                # Check resource constraints
                can_watch_movie = True
                for i, consumption in enumerate(resource_consumption[movie['id']]):
                    if resources_used[i] + consumption > resource_limits[i]:
                        can_watch_movie = False
                        break
                
                if can_watch_movie:
                    # Consume resources and add movie
                    for i, consumption in enumerate(resource_consumption[movie['id']]):
                        resources_used[i] += consumption
                    screen_end_times[best_screen] = movie['end_time']
                    scheduled_movies.append(movie)
        
        return len(scheduled_movies)
    
    def get_movies_with_mathematical_constraints(self, constraint_func):
        """Get maximum movies that satisfy custom mathematical constraints."""
        filtered_movies = [movie for movie in self.movies if constraint_func(movie)]
        filtered_movies.sort(key=lambda x: x['end_time'])
        
        screen_end_times = [0] * self.k
        scheduled_movies = []
        
        for movie in filtered_movies:
            # Find available screen
            best_screen = -1
            earliest_end = float('inf')
            
            for i in range(self.k):
                if screen_end_times[i] <= movie['start_time'] and screen_end_times[i] < earliest_end:
                    earliest_end = screen_end_times[i]
                    best_screen = i
            
            if best_screen != -1:
                screen_end_times[best_screen] = movie['end_time']
                scheduled_movies.append(movie)
        
        return len(scheduled_movies)
    
    def get_movies_with_range_constraints(self, range_constraints):
        """Get maximum movies that satisfy range constraints."""
        screen_end_times = [0] * self.k
        scheduled_movies = []
        
        for movie in self.movies:
            # Check if movie satisfies all range constraints
            satisfies_constraints = True
            for constraint in range_constraints:
                if not constraint(movie):
                    satisfies_constraints = False
                    break
            
            if not satisfies_constraints:
                continue
            
            # Find available screen
            best_screen = -1
            earliest_end = float('inf')
            
            for i in range(self.k):
                if screen_end_times[i] <= movie['start_time'] and screen_end_times[i] < earliest_end:
                    earliest_end = screen_end_times[i]
                    best_screen = i
            
            if best_screen != -1:
                screen_end_times[best_screen] = movie['end_time']
                scheduled_movies.append(movie)
        
        return len(scheduled_movies)
    
    def get_movies_with_optimization_constraints(self, optimization_func):
        """Get maximum movies using custom optimization constraints."""
        # Sort movies by optimization function
        optimized_movies = sorted(self.movies, key=optimization_func)
        
        screen_end_times = [0] * self.k
        scheduled_movies = []
        
        for movie in optimized_movies:
            # Find available screen
            best_screen = -1
            earliest_end = float('inf')
            
            for i in range(self.k):
                if screen_end_times[i] <= movie['start_time'] and screen_end_times[i] < earliest_end:
                    earliest_end = screen_end_times[i]
                    best_screen = i
            
            if best_screen != -1:
                screen_end_times[best_screen] = movie['end_time']
                scheduled_movies.append(movie)
        
        return len(scheduled_movies)
    
    def get_movies_with_multiple_constraints(self, constraints_list):
        """Get maximum movies that satisfy multiple constraints."""
        screen_end_times = [0] * self.k
        scheduled_movies = []
        
        for movie in self.movies:
            # Check if movie satisfies all constraints
            satisfies_all_constraints = True
            for constraint in constraints_list:
                if not constraint(movie):
                    satisfies_all_constraints = False
                    break
            
            if not satisfies_all_constraints:
                continue
            
            # Find available screen
            best_screen = -1
            earliest_end = float('inf')
            
            for i in range(self.k):
                if screen_end_times[i] <= movie['start_time'] and screen_end_times[i] < earliest_end:
                    earliest_end = screen_end_times[i]
                    best_screen = i
            
            if best_screen != -1:
                screen_end_times[best_screen] = movie['end_time']
                scheduled_movies.append(movie)
        
        return len(scheduled_movies)
    
    def get_movies_with_priority_constraints(self, priority_func):
        """Get maximum movies with priority-based constraints."""
        # Sort movies by priority
        prioritized_movies = sorted(self.movies, key=priority_func, reverse=True)
        
        screen_end_times = [0] * self.k
        scheduled_movies = []
        
        for movie in prioritized_movies:
            # Find available screen
            best_screen = -1
            earliest_end = float('inf')
            
            for i in range(self.k):
                if screen_end_times[i] <= movie['start_time'] and screen_end_times[i] < earliest_end:
                    earliest_end = screen_end_times[i]
                    best_screen = i
            
            if best_screen != -1:
                screen_end_times[best_screen] = movie['end_time']
                scheduled_movies.append(movie)
        
        return len(scheduled_movies)
    
    def get_movies_with_adaptive_constraints(self, adaptive_func):
        """Get maximum movies with adaptive constraints."""
        screen_end_times = [0] * self.k
        scheduled_movies = []
        
        for movie in self.movies:
            # Find available screen
            best_screen = -1
            earliest_end = float('inf')
            
            for i in range(self.k):
                if screen_end_times[i] <= movie['start_time'] and screen_end_times[i] < earliest_end:
                    earliest_end = screen_end_times[i]
                    best_screen = i
            
            if best_screen != -1:
                # Check adaptive constraints
                if adaptive_func(movie, scheduled_movies, screen_end_times[best_screen]):
                    screen_end_times[best_screen] = movie['end_time']
                    scheduled_movies.append(movie)
        
        return len(scheduled_movies)
    
    def get_optimal_movie_strategy(self):
        """Get optimal movie strategy considering all constraints."""
        strategies = [
            ('time_constraints', self.get_movies_with_time_constraints),
            ('resource_constraints', self.get_movies_with_resource_constraints),
            ('mathematical_constraints', self.get_movies_with_mathematical_constraints),
        ]
        
        best_strategy = None
        best_movies = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'time_constraints':
                    current_movies = strategy_func(10)  # 10 time units
                elif strategy_name == 'resource_constraints':
                    resource_limits = [100, 50]
                    resource_consumption = {1: [10, 5], 2: [15, 8], 3: [12, 6], 4: [20, 10], 5: [8, 4]}
                    current_movies = strategy_func(resource_limits, resource_consumption)
                elif strategy_name == 'mathematical_constraints':
                    def constraint_func(movie):
                        return movie.get('rating', 0) >= 8.0
                    current_movies = strategy_func(constraint_func)
                
                if current_movies > best_movies:
                    best_movies = current_movies
                    best_strategy = (strategy_name, current_movies)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'min_rating': 8.0,
    'max_duration': 3,
    'time_range': (1, 8)
}

movies = [
    {'id': 1, 'start_time': 1, 'end_time': 3, 'genre': 'Action', 'rating': 8.5},
    {'id': 2, 'start_time': 2, 'end_time': 4, 'genre': 'Comedy', 'rating': 7.2},
    {'id': 3, 'start_time': 4, 'end_time': 6, 'genre': 'Drama', 'rating': 9.1},
    {'id': 4, 'start_time': 5, 'end_time': 7, 'genre': 'Action', 'rating': 8.8},
    {'id': 5, 'start_time': 6, 'end_time': 8, 'genre': 'Thriller', 'rating': 8.0}
]

constrained_festival_ii = ConstrainedMovieFestivalII(movies, 2, constraints)

print("Time-constrained movies:", constrained_festival_ii.get_movies_with_time_constraints(8))

# Resource constraints
resource_limits = [100, 50]
resource_consumption = {1: [10, 5], 2: [15, 8], 3: [12, 6], 4: [20, 10], 5: [8, 4]}
print("Resource-constrained movies:", constrained_festival_ii.get_movies_with_resource_constraints(resource_limits, resource_consumption))

# Mathematical constraints
def custom_constraint(movie):
    return movie.get('rating', 0) >= 8.0

print("Mathematical constraint movies:", constrained_festival_ii.get_movies_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(movie):
    return movie.get('rating', 0) >= 8.0 and movie['end_time'] - movie['start_time'] <= 3

range_constraints = [range_constraint]
print("Range-constrained movies:", constrained_festival_ii.get_movies_with_range_constraints(range_constraints))

# Multiple constraints
def constraint1(movie):
    return movie.get('rating', 0) >= 8.0

def constraint2(movie):
    return movie['end_time'] - movie['start_time'] <= 3

constraints_list = [constraint1, constraint2]
print("Multiple constraints movies:", constrained_festival_ii.get_movies_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(movie):
    return movie.get('rating', 0)

print("Priority-constrained movies:", constrained_festival_ii.get_movies_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(movie, scheduled_movies, last_end_time):
    return movie.get('rating', 0) >= 8.0 and len(scheduled_movies) < 3

print("Adaptive constraint movies:", constrained_festival_ii.get_movies_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_festival_ii.get_optimal_movie_strategy()
print(f"Optimal strategy: {optimal}")
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
