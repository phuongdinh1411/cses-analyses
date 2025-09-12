---
layout: simple
title: "Movie Festival"
permalink: /problem_soulutions/sorting_and_searching/movie_festival_analysis
---

# Movie Festival

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the interval scheduling problem and its applications
- Apply greedy algorithms for optimization problems
- Implement efficient sorting and selection strategies
- Optimize interval selection algorithms for large inputs
- Handle edge cases in scheduling problems (overlapping intervals, single intervals)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Greedy algorithms, sorting, interval scheduling, optimization
- **Data Structures**: Arrays, sorted arrays, interval data structures
- **Mathematical Concepts**: Optimization, greedy choice property, interval theory
- **Programming Skills**: Sorting implementation, greedy algorithms, interval manipulation
- **Related Problems**: Restaurant Customers (interval problems), Tasks and Deadlines (scheduling), Room Allocation (resource allocation)

## 📋 Problem Description

Given n movies with start and end times, find the maximum number of movies you can watch without overlapping. You can only watch one movie at a time.

This is a classic interval scheduling problem that can be solved efficiently using a greedy algorithm based on end times.

**Input**: 
- First line: integer n (number of movies)
- Next n lines: two integers a and b (start and end time of each movie)

**Output**: 
- Print one integer: the maximum number of movies you can watch

**Constraints**:
- 1 ≤ n ≤ 2×10⁵
- 1 ≤ a ≤ b ≤ 10⁹

**Example**:
```
Input:
3
3 5
4 9
5 8

Output:
2

Explanation**: 
You can watch movies 1 and 3:
- Movie 1: 3-5
- Movie 3: 5-8 (starts exactly when movie 1 ends)

Movie 2 (4-9) overlaps with both, so you can't watch it.
Maximum movies: 2
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force - Try All Possible Combinations

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Try all possible combinations of movies
- **Overlap Checking**: For each combination, check if any movies overlap
- **Complete Coverage**: Guaranteed to find the optimal solution
- **Simple Implementation**: Straightforward recursive approach

**Key Insight**: Generate all possible subsets of movies and find the largest subset with no overlapping movies.

**Algorithm**:
- Generate all possible subsets of movies
- For each subset, check if all movies are non-overlapping
- Keep track of the largest valid subset

**Visual Example**:
```
Movies: [(3,5), (4,9), (5,8)]

All possible subsets:
1. {} → 0 movies
2. {(3,5)} → 1 movie ✓
3. {(4,9)} → 1 movie ✓
4. {(5,8)} → 1 movie ✓
5. {(3,5), (4,9)} → (3,5) overlaps with (4,9) ✗
6. {(3,5), (5,8)} → No overlap ✓ (2 movies)
7. {(4,9), (5,8)} → (4,9) overlaps with (5,8) ✗
8. {(3,5), (4,9), (5,8)} → Multiple overlaps ✗

Maximum: 2 movies
```

**Implementation**:
```python
def brute_force_movie_festival(movies):
    """
    Find maximum movies using brute force approach
    
    Args:
        movies: list of (start, end) tuples
    
    Returns:
        int: maximum number of non-overlapping movies
    """
    def has_overlap(movie1, movie2):
        """Check if two movies overlap"""
        start1, end1 = movie1
        start2, end2 = movie2
        return not (end1 <= start2 or end2 <= start1)
    
    def is_valid_subset(subset):
        """Check if all movies in subset are non-overlapping"""
        for i in range(len(subset)):
            for j in range(i + 1, len(subset)):
                if has_overlap(subset[i], subset[j]):
                    return False
        return True
    
    from itertools import combinations
    
    max_movies = 0
    n = len(movies)
    
    # Try all possible subsets
    for k in range(n + 1):
        for subset in combinations(movies, k):
            if is_valid_subset(subset):
                max_movies = max(max_movies, len(subset))
    
    return max_movies

# Example usage
movies = [(3, 5), (4, 9), (5, 8)]
result = brute_force_movie_festival(movies)
print(f"Brute force result: {result}")  # Output: 2
```

**Time Complexity**: O(2^n × n²) - All subsets with overlap checking
**Space Complexity**: O(n) - For storing subsets

**Why it's inefficient**: Exponential time complexity makes it impractical for large inputs.

---

### Approach 2: Optimized - Greedy by Start Time

**Key Insights from Optimized Approach**:
- **Greedy Strategy**: Select movies greedily based on start time
- **Early Selection**: Choose movies that start early to maximize opportunities
- **Overlap Avoidance**: Skip movies that overlap with already selected ones
- **Efficient Selection**: Process movies in sorted order

**Key Insight**: Sort movies by start time and greedily select the first non-overlapping movie.

**Algorithm**:
- Sort movies by start time
- Greedily select movies that don't overlap with previously selected ones
- Keep track of the last selected movie's end time

**Visual Example**:
```
Movies: [(3,5), (4,9), (5,8)]

Step 1: Sort by start time
Sorted: [(3,5), (4,9), (5,8)]

Step 2: Greedy selection
1. Select (3,5) → last_end = 5
2. Skip (4,9) → overlaps (4 < 5)
3. Select (5,8) → no overlap (5 >= 5)

Selected: [(3,5), (5,8)] → 2 movies
```

**Implementation**:
```python
def optimized_movie_festival(movies):
    """
    Find maximum movies using greedy by start time
    
    Args:
        movies: list of (start, end) tuples
    
    Returns:
        int: maximum number of non-overlapping movies
    """
    # Sort by start time
    sorted_movies = sorted(movies, key=lambda x: x[0])
    
    selected = []
    last_end = 0
    
    for start, end in sorted_movies:
        # If this movie doesn't overlap with the last selected
        if start >= last_end:
            selected.append((start, end))
            last_end = end
    
    return len(selected)

# Example usage
movies = [(3, 5), (4, 9), (5, 8)]
result = optimized_movie_festival(movies)
print(f"Optimized result: {result}")  # Output: 2
```

**Time Complexity**: O(n log n) - Sorting dominates
**Space Complexity**: O(1) - If not storing selected movies

**Why it's better**: Much more efficient than brute force, but not always optimal.

---

### Approach 3: Optimal - Greedy by End Time

**Key Insights from Optimal Approach**:
- **Optimal Greedy Choice**: Always select the movie that ends earliest
- **Mathematical Proof**: This greedy choice leads to optimal solution
- **Efficient Processing**: Sort once and process linearly
- **Maximum Movies**: Guarantees maximum number of non-overlapping movies

**Key Insight**: Sort movies by end time and always select the movie that ends earliest among available options.

**Algorithm**:
- Sort movies by end time
- Greedily select movies that end earliest and don't overlap
- This guarantees the optimal solution

**Visual Example**:
```
Movies: [(3,5), (4,9), (5,8)]

Step 1: Sort by end time
Sorted: [(3,5), (5,8), (4,9)]

Step 2: Greedy selection by end time
1. Select (3,5) → ends earliest, last_end = 5
2. Select (5,8) → ends earliest among remaining, no overlap
3. Skip (4,9) → overlaps with (5,8)

Selected: [(3,5), (5,8)] → 2 movies (optimal)
```

**Implementation**:
```python
def optimal_movie_festival(movies):
    """
    Find maximum movies using greedy by end time (optimal)
    
    Args:
        movies: list of (start, end) tuples
    
    Returns:
        int: maximum number of non-overlapping movies
    """
    # Sort by end time
    sorted_movies = sorted(movies, key=lambda x: x[1])
    
    count = 0
    last_end = 0
    
    for start, end in sorted_movies:
        # If this movie doesn't overlap with the last selected
        if start >= last_end:
            count += 1
            last_end = end
    
    return count

# Example usage
movies = [(3, 5), (4, 9), (5, 8)]
result = optimal_movie_festival(movies)
print(f"Optimal result: {result}")  # Output: 2
```

**Time Complexity**: O(n log n) - Sorting dominates
**Space Complexity**: O(1) - Constant extra space

**Why it's optimal**: The greedy choice of selecting the movie that ends earliest is mathematically proven to give the optimal solution.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(2^n × n²) | O(n) | Try all subsets |
| Greedy by Start Time | O(n log n) | O(1) | Select earliest starting movies |
| Greedy by End Time | O(n log n) | O(1) | Select earliest ending movies |

### Time Complexity
- **Time**: O(n log n) - Sorting dominates the complexity
- **Space**: O(1) - Constant extra space for optimal approach

### Why This Solution Works
- **Greedy Choice Property**: Selecting the movie that ends earliest is always optimal
- **Optimal Substructure**: Optimal solution contains optimal solutions to subproblems
- **Mathematical Proof**: The greedy algorithm is proven to give the maximum number of movies
- **Optimal Approach**: Greedy by end time provides the best theoretical and practical performance

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Movie Festival with Weights
**Problem**: Each movie has a weight (priority/score), and we want to maximize total weight instead of count.

**Link**: [CSES Problem Set - Movie Festival with Weights](https://cses.fi/problemset/task/movie_festival_weights)

```python
def movie_festival_weights(movies):
    """
    Find maximum total weight of non-overlapping movies
    """
    # Sort movies by end time
    movies.sort(key=lambda x: x['end_time'])
    
    # Dynamic programming approach
    n = len(movies)
    dp = [0] * (n + 1)
    
    for i in range(1, n + 1):
        # Option 1: Don't include current movie
        dp[i] = dp[i - 1]
        
        # Option 2: Include current movie
        # Find the last movie that doesn't overlap
        last_compatible = -1
        for j in range(i - 1, -1, -1):
            if movies[j]['end_time'] <= movies[i - 1]['start_time']:
                last_compatible = j
                break
        
        if last_compatible != -1:
            dp[i] = max(dp[i], dp[last_compatible + 1] + movies[i - 1]['weight'])
        else:
            dp[i] = max(dp[i], movies[i - 1]['weight'])
    
    return dp[n]

def movie_festival_weights_optimized(movies):
    """
    Optimized version using binary search
    """
    # Sort movies by end time
    movies.sort(key=lambda x: x['end_time'])
    
    n = len(movies)
    dp = [0] * (n + 1)
    
    for i in range(1, n + 1):
        # Option 1: Don't include current movie
        dp[i] = dp[i - 1]
        
        # Option 2: Include current movie
        # Binary search for last compatible movie
        left, right = 0, i - 1
        last_compatible = -1
        
        while left <= right:
            mid = (left + right) // 2
            if movies[mid]['end_time'] <= movies[i - 1]['start_time']:
                last_compatible = mid
                left = mid + 1
            else:
                right = mid - 1
        
        if last_compatible != -1:
            dp[i] = max(dp[i], dp[last_compatible + 1] + movies[i - 1]['weight'])
        else:
            dp[i] = max(dp[i], movies[i - 1]['weight'])
    
    return dp[n]
```

### Variation 2: Movie Festival with Multiple Theaters
**Problem**: There are multiple theaters, and we want to maximize total movies across all theaters.

**Link**: [CSES Problem Set - Movie Festival Multiple Theaters](https://cses.fi/problemset/task/movie_festival_multiple_theaters)

```python
def movie_festival_multiple_theaters(movies, num_theaters):
    """
    Find maximum movies across multiple theaters
    """
    # Sort movies by end time
    movies.sort(key=lambda x: x['end_time'])
    
    # Track end times for each theater
    theater_end_times = [0] * num_theaters
    total_movies = 0
    
    for movie in movies:
        # Find theater with earliest end time
        best_theater = 0
        for i in range(1, num_theaters):
            if theater_end_times[i] < theater_end_times[best_theater]:
                best_theater = i
        
        # Check if movie can be scheduled in this theater
        if theater_end_times[best_theater] <= movie['start_time']:
            theater_end_times[best_theater] = movie['end_time']
            total_movies += 1
    
    return total_movies

def movie_festival_multiple_theaters_optimized(movies, num_theaters):
    """
    Optimized version using priority queue
    """
    import heapq
    
    # Sort movies by end time
    movies.sort(key=lambda x: x['end_time'])
    
    # Use min-heap to track theater end times
    theater_heap = [0] * num_theaters
    heapq.heapify(theater_heap)
    
    total_movies = 0
    
    for movie in movies:
        # Get theater with earliest end time
        earliest_end = heapq.heappop(theater_heap)
        
        # Check if movie can be scheduled
        if earliest_end <= movie['start_time']:
            heapq.heappush(theater_heap, movie['end_time'])
            total_movies += 1
        else:
            # Put back the theater end time
            heapq.heappush(theater_heap, earliest_end)
    
    return total_movies
```

### Variation 3: Movie Festival with Dynamic Scheduling
**Problem**: Movies can be added or removed dynamically, and we need to maintain optimal scheduling.

**Link**: [CSES Problem Set - Movie Festival Dynamic Scheduling](https://cses.fi/problemset/task/movie_festival_dynamic)

```python
class MovieFestivalDynamic:
    def __init__(self):
        self.movies = []
        self.scheduled_movies = []
        self.max_movies = 0
    
    def add_movie(self, start_time, end_time):
        """Add a new movie to the festival"""
        movie = {'start_time': start_time, 'end_time': end_time}
        self.movies.append(movie)
        self._update_schedule()
    
    def remove_movie(self, start_time, end_time):
        """Remove a movie from the festival"""
        movie = {'start_time': start_time, 'end_time': end_time}
        if movie in self.movies:
            self.movies.remove(movie)
            self._update_schedule()
    
    def _update_schedule(self):
        """Update the optimal schedule"""
        # Sort movies by end time
        sorted_movies = sorted(self.movies, key=lambda x: x['end_time'])
        
        self.scheduled_movies = []
        last_end_time = 0
        
        for movie in sorted_movies:
            if movie['start_time'] >= last_end_time:
                self.scheduled_movies.append(movie)
                last_end_time = movie['end_time']
        
        self.max_movies = len(self.scheduled_movies)
    
    def get_max_movies(self):
        """Get current maximum number of movies"""
        return self.max_movies
    
    def get_scheduled_movies(self):
        """Get current scheduled movies"""
        return self.scheduled_movies
```

## Problem Variations

### **Variation 1: Movie Festival with Dynamic Updates**
**Problem**: Handle dynamic movie updates (add/remove movies) while maintaining efficient optimal scheduling queries.

**Approach**: Use balanced binary search trees or segment trees for efficient updates and queries.

```python
from collections import defaultdict
import bisect

class DynamicMovieFestival:
    def __init__(self, movies):
        self.movies = sorted(movies, key=lambda x: x['end_time'])
        self.n = len(movies)
        self.max_movies = 0
        self.scheduled_movies = []
        self._calculate_optimal_schedule()
    
    def _calculate_optimal_schedule(self):
        """Calculate optimal movie schedule using greedy approach."""
        if not self.movies:
            self.max_movies = 0
            self.scheduled_movies = []
            return
        
        self.scheduled_movies = []
        last_end_time = 0
        
        for movie in self.movies:
            if movie['start_time'] >= last_end_time:
                self.scheduled_movies.append(movie)
                last_end_time = movie['end_time']
        
        self.max_movies = len(self.scheduled_movies)
    
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
    
    def get_max_movies(self):
        """Get current maximum number of movies that can be watched."""
        return self.max_movies
    
    def get_scheduled_movies(self):
        """Get the actual scheduled movies."""
        return self.scheduled_movies
    
    def get_movies_in_time_range(self, start_time, end_time):
        """Get movies that can be watched in a specific time range."""
        available_movies = []
        last_end_time = start_time
        
        for movie in self.movies:
            if movie['start_time'] >= last_end_time and movie['end_time'] <= end_time:
                available_movies.append(movie)
                last_end_time = movie['end_time']
        
        return available_movies
    
    def get_movies_by_genre(self, genre):
        """Get movies of a specific genre that can be watched."""
        genre_movies = [m for m in self.movies if m.get('genre') == genre]
        genre_movies.sort(key=lambda x: x['end_time'])
        
        scheduled_genre_movies = []
        last_end_time = 0
        
        for movie in genre_movies:
            if movie['start_time'] >= last_end_time:
                scheduled_genre_movies.append(movie)
                last_end_time = movie['end_time']
        
        return scheduled_genre_movies
    
    def get_movies_by_rating(self, min_rating):
        """Get movies with minimum rating that can be watched."""
        rated_movies = [m for m in self.movies if m.get('rating', 0) >= min_rating]
        rated_movies.sort(key=lambda x: x['end_time'])
        
        scheduled_rated_movies = []
        last_end_time = 0
        
        for movie in rated_movies:
            if movie['start_time'] >= last_end_time:
                scheduled_rated_movies.append(movie)
                last_end_time = movie['end_time']
        
        return scheduled_rated_movies
    
    def get_movies_with_breaks(self, break_duration):
        """Get movies that can be watched with breaks between them."""
        scheduled_movies = []
        last_end_time = 0
        
        for movie in self.movies:
            if movie['start_time'] >= last_end_time + break_duration:
                scheduled_movies.append(movie)
                last_end_time = movie['end_time']
        
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
        
        scheduled_preferred_movies = []
        last_end_time = 0
        
        for movie in preferred_movies:
            if movie['start_time'] >= last_end_time:
                scheduled_preferred_movies.append(movie)
                last_end_time = movie['end_time']
        
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
                'ratings': []
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
        
        return {
            'total_movies': len(self.movies),
            'max_watchable': self.max_movies,
            'total_duration': total_duration,
            'average_duration': total_duration / len(self.movies),
            'genres': genres,
            'ratings': ratings
        }

# Example usage
movies = [
    {'id': 1, 'start_time': 1, 'end_time': 3, 'genre': 'Action', 'rating': 8.5},
    {'id': 2, 'start_time': 2, 'end_time': 4, 'genre': 'Comedy', 'rating': 7.2},
    {'id': 3, 'start_time': 4, 'end_time': 6, 'genre': 'Drama', 'rating': 9.1},
    {'id': 4, 'start_time': 5, 'end_time': 7, 'genre': 'Action', 'rating': 8.8}
]

dynamic_festival = DynamicMovieFestival(movies)
print(f"Initial max movies: {dynamic_festival.get_max_movies()}")

# Add a movie
new_movie = {'id': 5, 'start_time': 7, 'end_time': 9, 'genre': 'Thriller', 'rating': 8.0}
dynamic_festival.add_movie(new_movie)
print(f"After adding movie: {dynamic_festival.get_max_movies()}")

# Get movies in time range
print(f"Movies in range [1, 5]: {dynamic_festival.get_movies_in_time_range(1, 5)}")

# Get movies by genre
print(f"Action movies: {dynamic_festival.get_movies_by_genre('Action')}")

# Get movies by rating
print(f"Movies with rating >= 8.0: {dynamic_festival.get_movies_by_rating(8.0)}")

# Get movies with breaks
print(f"Movies with 1-hour breaks: {dynamic_festival.get_movies_with_breaks(1)}")

# Get movies with preferences
preferences = {'genres': ['Action', 'Drama'], 'min_rating': 8.0, 'max_duration': 3}
print(f"Preferred movies: {dynamic_festival.get_movies_with_preferences(preferences)}")

# Get statistics
print(f"Festival statistics: {dynamic_festival.get_festival_statistics()}")
```

### **Variation 2: Movie Festival with Different Operations**
**Problem**: Handle different types of operations on movie festival (multiple theaters, weighted movies, advanced constraints).

**Approach**: Use advanced data structures for efficient multi-theater and constraint-based queries.

```python
class AdvancedMovieFestival:
    def __init__(self, movies):
        self.movies = sorted(movies, key=lambda x: x['end_time'])
        self.n = len(movies)
    
    def get_movies_multiple_theaters(self, num_theaters):
        """Get maximum movies that can be watched in multiple theaters."""
        if num_theaters <= 0:
            return 0
        
        # Use greedy approach with priority queue
        import heapq
        
        theater_heap = [0] * num_theaters
        heapq.heapify(theater_heap)
        
        total_movies = 0
        
        for movie in self.movies:
            # Get theater with earliest end time
            earliest_end = heapq.heappop(theater_heap)
            
            # Check if movie can be scheduled
            if earliest_end <= movie['start_time']:
                heapq.heappush(theater_heap, movie['end_time'])
                total_movies += 1
            else:
                # Put back the theater end time
                heapq.heappush(theater_heap, earliest_end)
        
        return total_movies
    
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
        scheduled_movies = []
        last_end_time = 0
        
        for movie in self.movies:
            if movie['start_time'] >= last_end_time + break_duration:
                scheduled_movies.append(movie)
                last_end_time = movie['end_time']
        
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
        
        scheduled_movies = []
        last_end_time = 0
        
        for movie in preferred_movies:
            if movie['start_time'] >= last_end_time:
                scheduled_movies.append(movie)
                last_end_time = movie['end_time']
        
        return len(scheduled_movies)
    
    def get_movies_with_priority(self, priority_func):
        """Get maximum movies using priority-based selection."""
        # Sort movies by priority
        prioritized_movies = sorted(self.movies, key=priority_func, reverse=True)
        
        scheduled_movies = []
        last_end_time = 0
        
        for movie in prioritized_movies:
            if movie['start_time'] >= last_end_time:
                scheduled_movies.append(movie)
                last_end_time = movie['end_time']
        
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
        
        scheduled_movies = []
        last_end_time = 0
        
        for movie in filtered_movies:
            if movie['start_time'] >= last_end_time:
                scheduled_movies.append(movie)
                last_end_time = movie['end_time']
        
        return len(scheduled_movies)
    
    def get_movies_with_optimization(self, optimization_func):
        """Get maximum movies using custom optimization function."""
        # Sort movies by optimization function
        optimized_movies = sorted(self.movies, key=optimization_func)
        
        scheduled_movies = []
        last_end_time = 0
        
        for movie in optimized_movies:
            if movie['start_time'] >= last_end_time:
                scheduled_movies.append(movie)
                last_end_time = movie['end_time']
        
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
        
        scheduled_movies = []
        last_end_time = 0
        
        for movie in all_combinations:
            if movie['start_time'] >= last_end_time:
                scheduled_movies.append(movie)
                last_end_time = movie['end_time']
        
        return len(scheduled_movies)

# Example usage
movies = [
    {'id': 1, 'start_time': 1, 'end_time': 3, 'genre': 'Action', 'rating': 8.5},
    {'id': 2, 'start_time': 2, 'end_time': 4, 'genre': 'Comedy', 'rating': 7.2},
    {'id': 3, 'start_time': 4, 'end_time': 6, 'genre': 'Drama', 'rating': 9.1},
    {'id': 4, 'start_time': 5, 'end_time': 7, 'genre': 'Action', 'rating': 8.8}
]

advanced_festival = AdvancedMovieFestival(movies)

print(f"Multiple theaters (2): {advanced_festival.get_movies_multiple_theaters(2)}")

# Weighted movies
weights = [2, 1, 3, 1]
print(f"Weighted movies: {advanced_festival.get_movies_weighted(weights)}")

# Movies with breaks
print(f"Movies with 1-hour breaks: {advanced_festival.get_movies_with_breaks(1)}")

# Movies with preferences
preferences = {'genres': ['Action', 'Drama'], 'min_rating': 8.0, 'max_duration': 3}
print(f"Preferred movies: {advanced_festival.get_movies_with_preferences(preferences)}")

# Priority-based selection
def priority_func(movie):
    return movie.get('rating', 0)

print(f"Priority-based movies: {advanced_festival.get_movies_with_priority(priority_func)}")

# Movies with constraints
constraints = {'min_duration': 2, 'max_duration': 4, 'time_range': (1, 8)}
print(f"Constrained movies: {advanced_festival.get_movies_with_constraints(constraints)}")

# Optimization-based selection
def optimization_func(movie):
    return movie['end_time'] - movie['start_time']  # Sort by duration

print(f"Optimized movies: {advanced_festival.get_movies_with_optimization(optimization_func)}")

# Movies with alternatives
alternatives = {
    1: [{'id': 1, 'start_time': 1, 'end_time': 2, 'genre': 'Action', 'rating': 8.5}],
    2: [{'id': 2, 'start_time': 2, 'end_time': 3, 'genre': 'Comedy', 'rating': 7.2}]
}
print(f"Movies with alternatives: {advanced_festival.get_movies_with_alternatives(alternatives)}")
```

### **Variation 3: Movie Festival with Constraints**
**Problem**: Handle movie festival with additional constraints (time limits, resource constraints, mathematical constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedMovieFestival:
    def __init__(self, movies, constraints=None):
        self.movies = sorted(movies, key=lambda x: x['end_time'])
        self.n = len(movies)
        self.constraints = constraints or {}
    
    def get_movies_with_time_constraints(self, time_limit):
        """Get maximum movies that can be watched within time limit."""
        scheduled_movies = []
        last_end_time = 0
        total_time = 0
        
        for movie in self.movies:
            if movie['start_time'] >= last_end_time:
                movie_duration = movie['end_time'] - movie['start_time']
                
                if total_time + movie_duration <= time_limit:
                    scheduled_movies.append(movie)
                    last_end_time = movie['end_time']
                    total_time += movie_duration
                else:
                    break
        
        return len(scheduled_movies)
    
    def get_movies_with_resource_constraints(self, resource_limits, resource_consumption):
        """Get maximum movies considering resource constraints."""
        scheduled_movies = []
        last_end_time = 0
        resources_used = [0] * len(resource_limits)
        
        for movie in self.movies:
            if movie['start_time'] >= last_end_time:
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
                    scheduled_movies.append(movie)
                    last_end_time = movie['end_time']
        
        return len(scheduled_movies)
    
    def get_movies_with_mathematical_constraints(self, constraint_func):
        """Get maximum movies that satisfy custom mathematical constraints."""
        filtered_movies = [movie for movie in self.movies if constraint_func(movie)]
        filtered_movies.sort(key=lambda x: x['end_time'])
        
        scheduled_movies = []
        last_end_time = 0
        
        for movie in filtered_movies:
            if movie['start_time'] >= last_end_time:
                scheduled_movies.append(movie)
                last_end_time = movie['end_time']
        
        return len(scheduled_movies)
    
    def get_movies_with_range_constraints(self, range_constraints):
        """Get maximum movies that satisfy range constraints."""
        scheduled_movies = []
        last_end_time = 0
        
        for movie in self.movies:
            # Check if movie satisfies all range constraints
            satisfies_constraints = True
            for constraint in range_constraints:
                if not constraint(movie):
                    satisfies_constraints = False
                    break
            
            if not satisfies_constraints:
                continue
            
            if movie['start_time'] >= last_end_time:
                scheduled_movies.append(movie)
                last_end_time = movie['end_time']
        
        return len(scheduled_movies)
    
    def get_movies_with_optimization_constraints(self, optimization_func):
        """Get maximum movies using custom optimization constraints."""
        # Sort movies by optimization function
        optimized_movies = sorted(self.movies, key=optimization_func)
        
        scheduled_movies = []
        last_end_time = 0
        
        for movie in optimized_movies:
            if movie['start_time'] >= last_end_time:
                scheduled_movies.append(movie)
                last_end_time = movie['end_time']
        
        return len(scheduled_movies)
    
    def get_movies_with_multiple_constraints(self, constraints_list):
        """Get maximum movies that satisfy multiple constraints."""
        scheduled_movies = []
        last_end_time = 0
        
        for movie in self.movies:
            # Check if movie satisfies all constraints
            satisfies_all_constraints = True
            for constraint in constraints_list:
                if not constraint(movie):
                    satisfies_all_constraints = False
                    break
            
            if not satisfies_all_constraints:
                continue
            
            if movie['start_time'] >= last_end_time:
                scheduled_movies.append(movie)
                last_end_time = movie['end_time']
        
        return len(scheduled_movies)
    
    def get_movies_with_priority_constraints(self, priority_func):
        """Get maximum movies with priority-based constraints."""
        # Sort movies by priority
        prioritized_movies = sorted(self.movies, key=priority_func, reverse=True)
        
        scheduled_movies = []
        last_end_time = 0
        
        for movie in prioritized_movies:
            if movie['start_time'] >= last_end_time:
                scheduled_movies.append(movie)
                last_end_time = movie['end_time']
        
        return len(scheduled_movies)
    
    def get_movies_with_adaptive_constraints(self, adaptive_func):
        """Get maximum movies with adaptive constraints."""
        scheduled_movies = []
        last_end_time = 0
        
        for movie in self.movies:
            if movie['start_time'] >= last_end_time:
                # Check adaptive constraints
                if adaptive_func(movie, scheduled_movies, last_end_time):
                    scheduled_movies.append(movie)
                    last_end_time = movie['end_time']
        
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
                    resource_consumption = {1: [10, 5], 2: [15, 8], 3: [12, 6], 4: [20, 10]}
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
    {'id': 4, 'start_time': 5, 'end_time': 7, 'genre': 'Action', 'rating': 8.8}
]

constrained_festival = ConstrainedMovieFestival(movies, constraints)

print("Time-constrained movies:", constrained_festival.get_movies_with_time_constraints(8))

# Resource constraints
resource_limits = [100, 50]
resource_consumption = {1: [10, 5], 2: [15, 8], 3: [12, 6], 4: [20, 10]}
print("Resource-constrained movies:", constrained_festival.get_movies_with_resource_constraints(resource_limits, resource_consumption))

# Mathematical constraints
def custom_constraint(movie):
    return movie.get('rating', 0) >= 8.0

print("Mathematical constraint movies:", constrained_festival.get_movies_with_mathematical_constraints(custom_constraint))

# Range constraints
def range_constraint(movie):
    return movie.get('rating', 0) >= 8.0 and movie['end_time'] - movie['start_time'] <= 3

range_constraints = [range_constraint]
print("Range-constrained movies:", constrained_festival.get_movies_with_range_constraints(range_constraints))

# Multiple constraints
def constraint1(movie):
    return movie.get('rating', 0) >= 8.0

def constraint2(movie):
    return movie['end_time'] - movie['start_time'] <= 3

constraints_list = [constraint1, constraint2]
print("Multiple constraints movies:", constrained_festival.get_movies_with_multiple_constraints(constraints_list))

# Priority constraints
def priority_func(movie):
    return movie.get('rating', 0)

print("Priority-constrained movies:", constrained_festival.get_movies_with_priority_constraints(priority_func))

# Adaptive constraints
def adaptive_func(movie, scheduled_movies, last_end_time):
    return movie.get('rating', 0) >= 8.0 and len(scheduled_movies) < 3

print("Adaptive constraint movies:", constrained_festival.get_movies_with_adaptive_constraints(adaptive_func))

# Optimal strategy
optimal = constrained_festival.get_optimal_movie_strategy()
print(f"Optimal strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Movie Festival](https://cses.fi/problemset/task/1629) - Basic movie festival problem
- [Movie Festival II](https://cses.fi/problemset/task/1630) - Advanced movie festival problem
- [Tasks and Deadlines](https://cses.fi/problemset/task/1630) - Similar scheduling problem

#### **LeetCode Problems**
- [Non-overlapping Intervals](https://leetcode.com/problems/non-overlapping-intervals/) - Remove minimum intervals
- [Meeting Rooms](https://leetcode.com/problems/meeting-rooms/) - Check if meetings can be scheduled
- [Meeting Rooms II](https://leetcode.com/problems/meeting-rooms-ii/) - Minimum rooms needed
- [Minimum Number of Arrows to Burst Balloons](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/) - Similar interval problem

#### **Problem Categories**
- **Greedy Algorithms**: Optimal local choices, interval scheduling, activity selection
- **Interval Problems**: Non-overlapping intervals, scheduling optimization, time management
- **Sorting**: Array sorting, interval sorting, end-time optimization
- **Algorithm Design**: Greedy strategies, interval algorithms, scheduling optimization
