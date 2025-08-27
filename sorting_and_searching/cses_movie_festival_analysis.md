# CSES Movie Festival - Interview Analysis

## Problem Statement
In a movie festival, n movies will be shown. You know the starting and ending time of each movie.

What is the maximum number of movies you can watch entirely?

### Input
The first input line has an integer n: the number of movies.

After this, there are n lines that describe the movies. Each line has two integers a and b: the starting and ending time of a movie.

### Output
Print one integer: the maximum number of movies.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ a ≤ b ≤ 10^9

### Example
```
Input:
3
3 5
4 9
5 8

Output:
2
```

## Interview Approach

### Step 1: Understanding the Problem
**Interviewer**: "Can you explain what this problem is asking for?"
**Candidate**: "I need to select the maximum number of movies I can watch completely without any overlap. Each movie has a start and end time, and I can't watch two movies that overlap in time."

### Step 2: Brute Force Approach
**Interviewer**: "What's the first solution that comes to mind?"
**Candidate**: "I can try all possible combinations of movies and check which ones don't overlap."

```python
def movie_festival_brute_force(movies):
    n = len(movies)
    max_movies = 0
    
    # Try all possible subsets of movies
    for mask in range(1 << n):  # 2^n possible combinations
        selected = []
        for i in range(n):
            if mask & (1 << i):
                selected.append(movies[i])
        
        # Check if selected movies don't overlap
        if len(selected) > 1:
            selected.sort(key=lambda x: x[0])  # Sort by start time
            valid = True
            for i in range(1, len(selected)):
                if selected[i][0] < selected[i-1][1]:  # Overlap
                    valid = False
                    break
            if valid:
                max_movies = max(max_movies, len(selected))
        elif len(selected) == 1:
            max_movies = max(max_movies, 1)
    
    return max_movies

# Time Complexity: O(2^n * n log n)
# Space Complexity: O(n)
```

**Interviewer**: "What's the time complexity of this approach?"
**Candidate**: "O(2^n * n log n) because I'm trying 2^n possible combinations, and for each valid combination, I need to sort and check overlaps."

### Step 3: Dynamic Programming Approach
**Interviewer**: "Can you think of a dynamic programming solution?"
**Candidate**: "Yes! I can use DP where dp[i] represents the maximum number of movies I can watch starting from movie i."

```python
def movie_festival_dp(movies):
    n = len(movies)
    movies.sort()  # Sort by start time
    
    # dp[i] = max movies starting from movie i
    dp = [0] * (n + 1)
    
    # Fill DP from right to left
    for i in range(n - 1, -1, -1):
        # Don't include current movie
        dp[i] = dp[i + 1]
        
        # Include current movie
        # Find next movie that starts after current ends
        next_movie = i + 1
        while next_movie < n and movies[next_movie][0] < movies[i][1]:
            next_movie += 1
        
        dp[i] = max(dp[i], 1 + dp[next_movie])
    
    return dp[0]

# Time Complexity: O(n²)
# Space Complexity: O(n)
```

**Interviewer**: "What's the time complexity now?"
**Candidate**: "O(n²) because for each movie, I might need to scan through all remaining movies to find the next non-overlapping one."

### Step 4: Optimization with Binary Search
**Interviewer**: "Can you optimize the DP solution?"
**Candidate**: "Yes! I can use binary search to find the next non-overlapping movie instead of linear search."

```python
import bisect

def movie_festival_dp_optimized(movies):
    n = len(movies)
    movies.sort()  # Sort by start time
    
    # Extract start times for binary search
    start_times = [movie[0] for movie in movies]
    
    dp = [0] * (n + 1)
    
    for i in range(n - 1, -1, -1):
        # Don't include current movie
        dp[i] = dp[i + 1]
        
        # Include current movie
        # Binary search for next movie that starts after current ends
        next_movie = bisect.bisect_left(start_times, movies[i][1])
        
        dp[i] = max(dp[i], 1 + dp[next_movie])
    
    return dp[0]

# Time Complexity: O(n log n)
# Space Complexity: O(n)
```

**Interviewer**: "What's the time complexity now?"
**Candidate**: "O(n log n) because sorting takes O(n log n) and each binary search takes O(log n)."

### Step 5: Greedy Solution (Optimal)
**Interviewer**: "Can you think of a greedy approach?"
**Candidate**: "Yes! I can sort movies by ending time and always choose the movie that ends earliest."

```python
def movie_festival_greedy(movies):
    # Sort by ending time
    movies.sort(key=lambda x: x[1])
    
    selected = 0
    last_end = 0
    
    for start, end in movies:
        if start >= last_end:
            selected += 1
            last_end = end
    
    return selected

# Time Complexity: O(n log n)
# Space Complexity: O(1) if we can modify input
```

**Interviewer**: "Why does this greedy approach work?"
**Candidate**: "By always choosing the movie that ends earliest, I maximize the number of future movies I can watch. If I choose a movie that ends later, I might miss opportunities to watch other movies that could have fit in the schedule."

## Final Optimal Solution

```python
n = int(input())
movies = []

for _ in range(n):
    start, end = map(int, input().split())
    movies.append((start, end))

# Sort by ending time
movies.sort(key=lambda x: x[1])

# Greedy selection
selected = 0
last_end = 0

for start, end in movies:
    if start >= last_end:
        selected += 1
        last_end = end

print(selected)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Pros | Cons |
|----------|----------------|------------------|------|------|
| Brute Force | O(2^n * n log n) | O(n) | Guaranteed optimal | Exponential time |
| Dynamic Programming | O(n²) | O(n) | Systematic approach | Too slow for large n |
| DP + Binary Search | O(n log n) | O(n) | Efficient DP | More complex |
| Greedy | O(n log n) | O(1) | Optimal, simple | Requires proof |

## Edge Cases to Consider

1. **Single movie**: Should return 1
2. **No overlap**: All movies can be watched
3. **Complete overlap**: Only one movie can be watched
4. **Same start/end times**: Handle edge case where movies start and end at same time
5. **Large time ranges**: Algorithm works with large integers

## Interview Tips

1. **Start with brute force**: Show you understand the problem
2. **Explain DP approach**: Show systematic thinking
3. **Optimize step by step**: Demonstrate optimization skills
4. **Prove greedy correctness**: Explain why greedy works
5. **Handle edge cases**: Mention potential issues

## Follow-up Questions

**Interviewer**: "What if you want to maximize total watching time instead of number of movies?"
**Candidate**: "I'd need to modify the DP approach to track total time instead of count, and the greedy approach wouldn't work."

**Interviewer**: "What if movies have different priorities or weights?"
**Candidate**: "I'd need to use a weighted interval scheduling algorithm, which is more complex and might require different approaches."

**Interviewer**: "What if you can watch multiple movies simultaneously?"
**Candidate**: "This becomes a different problem - finding the maximum number of movies that can be watched at the same time, which is about finding maximum overlap."

---

*This analysis demonstrates the interview progression from exponential brute force through DP to optimal greedy solution with clear explanations and complexity analysis.* 