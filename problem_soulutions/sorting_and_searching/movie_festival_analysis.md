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
