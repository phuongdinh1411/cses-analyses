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

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Weighted Movie Festival**
**Problem**: Each movie has a weight/rating. Find maximum total weight of movies you can watch.
```python
def weighted_movie_festival(movies):
    # movies[i] = (start, end, weight)
    n = len(movies)
    movies.sort(key=lambda x: x[1])  # Sort by end time
    
    # dp[i] = max weight ending at movie i
    dp = [0] * n
    
    for i in range(n):
        # Weight of current movie
        dp[i] = movies[i][2]
        
        # Find last non-overlapping movie
        j = i - 1
        while j >= 0 and movies[j][1] > movies[i][0]:
            j -= 1
        
        if j >= 0:
            dp[i] += dp[j]
    
    return max(dp)
```

#### **Variation 2: Movie Festival with Duration Constraint**
**Problem**: You can only watch movies with duration at most D.
```python
def movie_festival_duration_constraint(movies, max_duration):
    # Filter movies by duration
    valid_movies = [(start, end) for start, end in movies if end - start <= max_duration]
    
    # Apply greedy algorithm
    valid_movies.sort(key=lambda x: x[1])  # Sort by end time
    
    count = 0
    last_end = 0
    
    for start, end in valid_movies:
        if start >= last_end:
            count += 1
            last_end = end
    
    return count
```

#### **Variation 3: Movie Festival with Multiple Theaters**
**Problem**: You have k theaters. Find maximum movies you can watch.
```python
def movie_festival_multiple_theaters(movies, k):
    # Sort by end time
    movies.sort(key=lambda x: x[1])
    
    # Track end times of k theaters
    theater_end_times = [0] * k
    
    count = 0
    for start, end in movies:
        # Find theater that becomes available earliest
        theater_idx = 0
        for i in range(1, k):
            if theater_end_times[i] < theater_end_times[theater_idx]:
                theater_idx = i
        
        # If theater is available, assign movie
        if theater_end_times[theater_idx] <= start:
            count += 1
            theater_end_times[theater_idx] = end
    
    return count
```

#### **Variation 4: Movie Festival with Break Time**
**Problem**: You need at least t minutes break between movies.
```python
def movie_festival_with_break(movies, break_time):
    movies.sort(key=lambda x: x[1])  # Sort by end time
    
    count = 0
    last_end = -break_time  # Allow first movie to start anytime
    
    for start, end in movies:
        if start >= last_end + break_time:
            count += 1
            last_end = end
    
    return count
```

#### **Variation 5: Movie Festival with Priority**
**Problem**: Some movies have higher priority. Maximize priority sum.
```python
def movie_festival_priority(movies):
    # movies[i] = (start, end, priority)
    movies.sort(key=lambda x: x[1])  # Sort by end time
    
    # Use binary search to find optimal solution
    def can_achieve_priority(target_priority):
        dp = [0] * len(movies)
        
        for i, (start, end, priority) in enumerate(movies):
            dp[i] = priority
            
            # Find last non-overlapping movie
            j = i - 1
            while j >= 0 and movies[j][1] > start:
                j -= 1
            
            if j >= 0:
                dp[i] += dp[j]
            
            if dp[i] >= target_priority:
                return True
        
        return max(dp) >= target_priority
    
    # Binary search on priority
    left, right = 0, sum(movie[2] for movie in movies)
    while left < right:
        mid = (left + right + 1) // 2
        if can_achieve_priority(mid):
            left = mid
        else:
            right = mid - 1
    
    return left
```

### 🔗 **Related Problems & Concepts**

#### **1. Interval Scheduling Problems**
- **Activity Selection**: Select maximum non-overlapping activities
- **Meeting Room Scheduling**: Assign meetings to rooms
- **Job Scheduling**: Schedule jobs on machines
- **Resource Allocation**: Allocate limited resources

#### **2. Greedy Algorithm Problems**
- **Fractional Knapsack**: Fill knapsack optimally
- **Huffman Coding**: Build optimal prefix codes
- **Dijkstra's Algorithm**: Find shortest paths
- **Kruskal's Algorithm**: Find minimum spanning tree

#### **3. Dynamic Programming Problems**
- **Weighted Interval Scheduling**: Maximum weight non-overlapping intervals
- **Longest Increasing Subsequence**: Find LIS in array
- **Coin Change**: Minimum coins to make amount
- **Subset Sum**: Find subset with given sum

#### **4. Optimization Problems**
- **Linear Programming**: Formulate as LP problem
- **Integer Programming**: Discrete optimization
- **Combinatorial Optimization**: Optimize discrete structures
- **Approximation Algorithms**: Find approximate solutions

#### **5. Time Management Problems**
- **Task Scheduling**: Schedule tasks with deadlines
- **Project Planning**: Plan project timeline
- **Resource Management**: Manage limited resources
- **Capacity Planning**: Plan resource capacity

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n = int(input())
    movies = []
    for _ in range(n):
        start, end = map(int, input().split())
        movies.append((start, end))
    
    movies.sort(key=lambda x: x[1])
    
    count = 0
    last_end = 0
    
    for start, end in movies:
        if start >= last_end:
            count += 1
            last_end = end
    
    print(count)
```

#### **2. Range Queries**
```python
# Precompute maximum movies for different time ranges
def precompute_movie_ranges(movies, max_time):
    # Create timeline of events
    events = []
    for start, end in movies:
        events.append((start, 1))   # Movie starts
        events.append((end, -1))    # Movie ends
    
    events.sort()
    
    # Precompute for each time point
    timeline = [0] * (max_time + 1)
    current_movies = 0
    
    for time, event_type in events:
        if time <= max_time:
            current_movies += event_type
            timeline[time] = current_movies
    
    return timeline

# Answer queries about movie count in time range
def movie_count_query(timeline, start_time, end_time):
    return timeline[end_time] - timeline[start_time]
```

#### **3. Interactive Problems**
```python
# Interactive movie festival planner
def interactive_movie_festival():
    n = int(input("Enter number of movies: "))
    movies = []
    
    for i in range(n):
        start = int(input(f"Enter start time for movie {i+1}: "))
        end = int(input(f"Enter end time for movie {i+1}: "))
        movies.append((start, end))
    
    print(f"Movies: {movies}")
    
    # Solve using greedy algorithm
    movies.sort(key=lambda x: x[1])
    
    selected = []
    last_end = 0
    
    for start, end in movies:
        if start >= last_end:
            selected.append((start, end))
            last_end = end
            print(f"Selected movie: {start}-{end}")
    
    print(f"Total movies you can watch: {len(selected)}")
    print(f"Selected movies: {selected}")
```

### 🧮 **Mathematical Extensions**

#### **1. Optimization Theory**
- **Linear Programming**: Formulate as LP problem
- **Integer Programming**: Discrete optimization
- **Duality**: Study dual problems
- **Sensitivity Analysis**: Analyze parameter changes

#### **2. Algorithm Analysis**
- **Greedy Correctness**: Prove greedy choice property
- **Optimal Substructure**: Prove optimal substructure
- **Complexity Analysis**: Time and space complexity
- **Lower Bounds**: Establish problem lower bounds

#### **3. Scheduling Theory**
- **Interval Graphs**: Graph representation of intervals
- **Clique Cover**: Cover intervals with minimum cliques
- **Independent Set**: Find maximum independent set
- **Coloring**: Color intervals with minimum colors

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Greedy Algorithms**: Local optimal choices
- **Dynamic Programming**: Optimal substructure
- **Interval Scheduling**: Classic greedy problem
- **Binary Search**: Search for optimal solutions

#### **2. Mathematical Concepts**
- **Optimization**: Mathematical optimization theory
- **Combinatorics**: Counting and arrangement
- **Graph Theory**: Interval graphs and coloring
- **Algorithm Analysis**: Complexity and correctness

#### **3. Programming Concepts**
- **Sorting**: Custom sorting techniques
- **Data Structures**: Efficient storage and retrieval
- **Algorithm Design**: Problem-solving strategies
- **Complexity Analysis**: Performance evaluation

---

*This analysis demonstrates greedy algorithm techniques and shows various extensions for interval scheduling problems.* 