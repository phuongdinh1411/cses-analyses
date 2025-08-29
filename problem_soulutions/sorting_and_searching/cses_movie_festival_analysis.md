---
layout: simple
title: "Movie Festival"
permalink: /problem_soulutions/sorting_and_searching/cses_movie_festival_analysis
---

# Movie Festival

## Problem Description

**Problem**: In a movie festival, n movies will be shown. You know the starting and ending time of each movie. What is the maximum number of movies you can watch entirely?

**Input**: 
- First line: n (number of movies)
- Next n lines: a b (starting and ending time of each movie)

**Output**: Maximum number of movies you can watch.

**Example**:
```
Input:
3
3 5
4 9
5 8

Output:
2

Explanation: You can watch movies [3,5] and [5,8] without overlap.
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Select maximum number of movies to watch
- Movies cannot overlap in time
- Must watch entire movies (not partial)
- Need to find optimal selection

**Key Observations:**
- This is an interval scheduling problem
- Greedy approach: always choose earliest ending movie
- Sort by end time for optimal solution
- Classic greedy algorithm problem

### Step 2: Greedy Approach
**Idea**: Sort movies by end time and always choose the earliest ending movie.

```python
def movie_festival_greedy(movies):
    # Sort movies by end time
    movies.sort(key=lambda x: x[1])
    
    count = 0
    last_end = 0
    
    for start, end in movies:
        # If current movie starts after last movie ends, we can watch it
        if start >= last_end:
            count += 1
            last_end = end
    
    return count
```

**Why this works:**
- Sort by end time ensures we always choose earliest ending movie
- This maximizes future opportunities
- Greedy choice is optimal for this problem

### Step 3: Optimized Solution
**Idea**: Optimize the implementation with better variable names and logic.

```python
def movie_festival_optimized(movies):
    # Sort by end time
    movies.sort(key=lambda x: x[1])
    
    selected_movies = 0
    current_end_time = 0
    
    for start_time, end_time in movies:
        if start_time >= current_end_time:
            selected_movies += 1
            current_end_time = end_time
    
    return selected_movies
```

**Why this is better:**
- Clearer variable names
- More readable logic
- Same optimal time complexity

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_movie_festival():
    n = int(input())
    movies = []
    
    for _ in range(n):
        start, end = map(int, input().split())
        movies.append((start, end))
    
    # Sort by end time
    movies.sort(key=lambda x: x[1])
    
    selected_movies = 0
    current_end_time = 0
    
    for start_time, end_time in movies:
        if start_time >= current_end_time:
            selected_movies += 1
            current_end_time = end_time
    
    print(selected_movies)

# Main execution
if __name__ == "__main__":
    solve_movie_festival()
```

**Why this works:**
- Optimal greedy approach
- Handles all edge cases
- Efficient implementation

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ([(3, 5), (4, 9), (5, 8)], 2),
        ([(1, 3), (2, 4), (3, 5)], 2),
        ([(1, 2), (2, 3), (3, 4)], 3),
        ([(1, 5), (2, 3), (4, 6)], 2),
    ]
    
    for movies, expected in test_cases:
        result = solve_test(movies)
        print(f"Movies: {movies}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(movies):
    movies.sort(key=lambda x: x[1])
    
    selected_movies = 0
    current_end_time = 0
    
    for start_time, end_time in movies:
        if start_time >= current_end_time:
            selected_movies += 1
            current_end_time = end_time
    
    return selected_movies

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n log n) - sorting movies by end time
- **Space**: O(1) - constant extra space

### Why This Solution Works
- **Greedy Choice**: Always choose earliest ending movie
- **Optimal Substructure**: Solution depends on optimal subproblems
- **Correctness**: Proven greedy strategy works for interval scheduling

## 🎯 Key Insights

### 1. **Greedy Strategy**
- Sort by end time (not start time)
- Always choose earliest ending movie
- This maximizes future opportunities
- Proven optimal for interval scheduling

### 2. **Interval Scheduling**
- Classic greedy algorithm problem
- Key insight: end time matters more than start time
- Greedy choice leads to optimal solution
- No need for dynamic programming

### 3. **Sorting Strategy**
- Sort by end time, not start time
- This enables greedy selection
- Linear scan after sorting
- O(n log n) total complexity

## 🎯 Problem Variations

### Variation 1: Weighted Movie Selection
**Problem**: Each movie has a weight/rating. Maximize total weight.

```python
def weighted_movie_festival(movies):
    # movies[i] = (start, end, weight)
    movies.sort(key=lambda x: x[1])
    
    # Use dynamic programming
    n = len(movies)
    dp = [0] * n
    
    for i in range(n):
        # Don't include current movie
        dp[i] = dp[i-1] if i > 0 else 0
        
        # Include current movie
        start, end, weight = movies[i]
        
        # Find last compatible movie
        j = i - 1
        while j >= 0 and movies[j][1] > start:
            j -= 1
        
        include_weight = weight + (dp[j] if j >= 0 else 0)
        dp[i] = max(dp[i], include_weight)
    
    return dp[n-1]
```

### Variation 2: Movie Selection with Duration Constraint
**Problem**: You can only watch movies with duration at most k.

```python
def movie_festival_duration_constraint(movies, max_duration):
    # Filter movies by duration
    valid_movies = [(start, end) for start, end in movies 
                   if end - start <= max_duration]
    
    # Apply greedy algorithm
    valid_movies.sort(key=lambda x: x[1])
    
    selected_movies = 0
    current_end_time = 0
    
    for start_time, end_time in valid_movies:
        if start_time >= current_end_time:
            selected_movies += 1
            current_end_time = end_time
    
    return selected_movies
```

### Variation 3: Movie Selection with Break Time
**Problem**: You need at least k minutes break between movies.

```python
def movie_festival_with_break(movies, break_time):
    movies.sort(key=lambda x: x[1])
    
    selected_movies = 0
    current_end_time = 0
    
    for start_time, end_time in movies:
        # Check if we have enough break time
        if start_time >= current_end_time + break_time:
            selected_movies += 1
            current_end_time = end_time
    
    return selected_movies
```

### Variation 4: Movie Selection with Multiple Theaters
**Problem**: You have k theaters. Maximize total movies watched.

```python
def movie_festival_multiple_theaters(movies, k):
    movies.sort(key=lambda x: x[1])
    
    # Use k pointers to track end times of each theater
    theater_end_times = [0] * k
    total_movies = 0
    
    for start_time, end_time in movies:
        # Find theater with earliest end time
        min_end_time = min(theater_end_times)
        min_theater = theater_end_times.index(min_end_time)
        
        if start_time >= min_end_time:
            theater_end_times[min_theater] = end_time
            total_movies += 1
    
    return total_movies
```

### Variation 5: Movie Selection with Priority
**Problem**: Some movies have higher priority. Break ties by priority.

```python
def movie_festival_with_priority(movies):
    # movies[i] = (start, end, priority)
    # Sort by end time, then by priority (descending)
    movies.sort(key=lambda x: (x[1], -x[2]))
    
    selected_movies = 0
    current_end_time = 0
    
    for start_time, end_time, priority in movies:
        if start_time >= current_end_time:
            selected_movies += 1
            current_end_time = end_time
    
    return selected_movies
```

## 🔗 Related Problems

- **[Tasks and Deadlines](/cses-analyses/problem_soulutions/sorting_and_searching/tasks_and_deadlines_analysis)**: Scheduling problems
- **[Room Allocation](/cses-analyses/problem_soulutions/sorting_and_searching/room_allocation_analysis)**: Resource allocation
- **[Nested Ranges](/cses-analyses/problem_soulutions/sorting_and_searching/nested_ranges_check_analysis)**: Interval problems

## 📚 Learning Points

1. **Greedy Algorithms**: Optimal local choices lead to global optimum
2. **Interval Scheduling**: Classic greedy problem
3. **Sorting Strategy**: Sort by end time for optimal selection
4. **Resource Allocation**: Efficient resource utilization

---

**This is a great introduction to greedy algorithms and interval scheduling!** 🎯 