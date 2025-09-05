---
layout: simple
title: "Movie Festival - Maximum Non-Overlapping Movies"
permalink: /problem_soulutions/sorting_and_searching/cses_movie_festival_analysis
---

# Movie Festival - Maximum Non-Overlapping Movies

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand interval scheduling problems and greedy selection strategies
- [ ] **Objective 2**: Apply greedy algorithms with earliest end time selection to maximize non-overlapping intervals
- [ ] **Objective 3**: Implement efficient interval scheduling algorithms with O(n log n) time complexity
- [ ] **Objective 4**: Optimize interval scheduling using sorting and greedy selection techniques
- [ ] **Objective 5**: Handle edge cases in interval scheduling (overlapping intervals, single interval, no valid selection)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Greedy algorithms, interval scheduling, sorting algorithms, non-overlapping intervals, optimization problems
- **Data Structures**: Arrays, sorting, interval tracking, selection tracking, time tracking
- **Mathematical Concepts**: Interval mathematics, scheduling theory, optimization problems, time analysis
- **Programming Skills**: Sorting implementation, greedy algorithm implementation, interval processing, algorithm implementation
- **Related Problems**: Room Allocation (interval scheduling), Greedy algorithm problems, Interval problems

## 📋 Problem Description

In a movie festival, n movies will be shown. You know the starting and ending time of each movie. What is the maximum number of movies you can watch entirely?

This is a classic interval scheduling problem that requires finding the maximum number of non-overlapping intervals. The solution involves using a greedy algorithm that always selects the movie with the earliest end time.

**Input**: 
- First line: n (number of movies)
- Next n lines: a b (starting and ending time of each movie)

**Output**: 
- Maximum number of movies you can watch entirely

**Constraints**:
- 1 ≤ n ≤ 2⋅10⁵
- 1 ≤ a < b ≤ 10⁹

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
- Movie 1: [3, 5] - ends at time 5
- Movie 2: [4, 9] - ends at time 9  
- Movie 3: [5, 8] - ends at time 8
- Optimal selection: Movies [3,5] and [5,8] (2 movies)
- Cannot watch movie [4,9] as it overlaps with both others
```

## 📊 Visual Example

### Input Movies
```
Movie 1: [3, 5] - ends at 5
Movie 2: [4, 9] - ends at 9
Movie 3: [5, 8] - ends at 8
```

### Timeline Visualization
```
Time:  0  1  2  3  4  5  6  7  8  9  10
       |  |  |  |  |  |  |  |  |  |  |
Movie 1:    [=====]
Movie 2:       [=========]
Movie 3:          [=====]

Overlap Analysis:
- Movie 1 [3,5] and Movie 2 [4,9]: Overlap at time 4-5
- Movie 1 [3,5] and Movie 3 [5,8]: Touch at time 5 (no overlap)
- Movie 2 [4,9] and Movie 3 [5,8]: Overlap at time 5-8
```

### Greedy Algorithm Process
```
Step 1: Sort movies by end time
Original: [3,5], [4,9], [5,8]
Sorted:   [3,5], [5,8], [4,9] (by end time: 5, 8, 9)

Step 2: Greedy selection
┌─────────────────────────────────────┐
│ Selected: []                        │
│ Last end time: -∞                   │
└─────────────────────────────────────┘

Movie 1 [3,5]: start=3 ≥ last_end=-∞ ✓
┌─────────────────────────────────────┐
│ Selected: [[3,5]]                   │
│ Last end time: 5                    │
└─────────────────────────────────────┘

Movie 3 [5,8]: start=5 ≥ last_end=5 ✓
┌─────────────────────────────────────┐
│ Selected: [[3,5], [5,8]]            │
│ Last end time: 8                    │
└─────────────────────────────────────┘

Movie 2 [4,9]: start=4 < last_end=8 ✗
┌─────────────────────────────────────┐
│ Selected: [[3,5], [5,8]] (unchanged)│
│ Last end time: 8                    │
└─────────────────────────────────────┘

Final Result: 2 movies
```

### Why Greedy Works
```
Key Insight: Always pick the movie that ends earliest

If we don't pick the earliest ending movie:
- We might block future movies that could fit
- The earliest ending movie doesn't block any more movies than necessary
- This gives us the maximum number of non-overlapping movies
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

### Step 3: Optimization/Alternative
**Alternative approaches:**
- **Sort by Start Time**: Less optimal, may miss better solutions
- **Dynamic Programming**: O(n²) approach for weighted intervals
- **Greedy by End Time**: Optimal O(n log n) approach

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

### Step 5: Testing Our Solution
**Test cases to verify correctness:**
- **Test 1**: Basic overlapping movies (should return optimal count)
- **Test 2**: No overlapping movies (should return all movies)
- **Test 3**: All movies overlap (should return 1)
- **Test 4**: Complex overlapping pattern (should return optimal selection)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Greedy by End Time | O(n log n) | O(1) | Sort by end time, always choose earliest ending |
| Greedy by Start Time | O(n log n) | O(1) | Less optimal, may miss better solutions |
| Dynamic Programming | O(n²) | O(n) | For weighted intervals |

## 🎯 Key Insights

### Important Concepts and Patterns
- **Greedy Algorithm**: Always choose the locally optimal choice
- **Interval Scheduling**: Classic problem with proven greedy solution
- **Sorting**: Sort by end time for optimal results
- **Non-overlapping Intervals**: Maximize number of compatible intervals

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Movie Festival with Weights**
```python
def movie_festival_weighted(n, movies):
    # Handle movies with different weights/priorities
    
    # Sort by end time
    movies.sort(key=lambda x: x[1])
    
    # DP approach for weighted intervals
    dp = [0] * (n + 1)
    
    for i in range(1, n + 1):
        start, end, weight = movies[i-1]
        
        # Don't take current movie
        dp[i] = dp[i-1]
        
        # Take current movie - find last compatible movie
        last_compatible = -1
        for j in range(i-1, -1, -1):
            if movies[j][1] <= start:
                last_compatible = j
                break
        
        if last_compatible != -1:
            dp[i] = max(dp[i], dp[last_compatible + 1] + weight)
    
    return dp[n]
```

#### **2. Movie Festival with Multiple Theaters**
```python
def movie_festival_multiple_theaters(n, movies, num_theaters):
    # Handle movies across multiple theaters
    
    # Sort by end time
    movies.sort(key=lambda x: x[1])
    
    # Track end times for each theater
    theater_end_times = [0] * num_theaters
    total_movies = 0
    
    for start, end in movies:
        # Find theater with earliest end time
        best_theater = 0
        for i in range(1, num_theaters):
            if theater_end_times[i] < theater_end_times[best_theater]:
                best_theater = i
        
        # Check if movie can be scheduled in best theater
        if start >= theater_end_times[best_theater]:
            theater_end_times[best_theater] = end
            total_movies += 1
    
    return total_movies
```

#### **3. Movie Festival with Dynamic Updates**
```python
def movie_festival_dynamic(n, operations):
    # Handle movies with dynamic additions/removals
    
    movies = []
    total_movies = 0
    
    for operation in operations:
        if operation[0] == 'add':
            # Add new movie
            start, end = operation[1], operation[2]
            movies.append((start, end))
            
            # Recalculate optimal schedule
            movies.sort(key=lambda x: x[1])
            total_movies = 0
            current_end_time = 0
            
            for movie_start, movie_end in movies:
                if movie_start >= current_end_time:
                    total_movies += 1
                    current_end_time = movie_end
        
        elif operation[0] == 'remove':
            # Remove movie
            start, end = operation[1], operation[2]
            if (start, end) in movies:
                movies.remove((start, end))
                
                # Recalculate optimal schedule
                movies.sort(key=lambda x: x[1])
                total_movies = 0
                current_end_time = 0
                
                for movie_start, movie_end in movies:
                    if movie_start >= current_end_time:
                        total_movies += 1
                        current_end_time = movie_end
        
        elif operation[0] == 'query':
            # Return current maximum movies
            yield total_movies
    
    return list(movie_festival_dynamic(n, operations))
```

## 🔗 Related Problems

### Links to Similar Problems
- **Interval Scheduling**: Activity selection problems
- **Greedy Algorithms**: Problems with optimal local choices
- **Sorting**: Problems requiring data preprocessing
- **Scheduling**: Resource allocation problems

## 📚 Learning Points

### Key Takeaways
- **Greedy strategy** works for interval scheduling
- **End time sorting** is crucial for optimal solutions
- **Local optimal choices** lead to global optimum
- **Interval problems** often have greedy solutions
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