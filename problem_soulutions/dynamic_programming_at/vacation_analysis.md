---
layout: simple
title: "Vacation"
permalink: /problem_soulutions/dynamic_programming_at/vacation_analysis
---

# Vacation

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand state machine DP with constraints
- Apply DP to problems with "cannot repeat same choice" constraints
- Recognize when to track previous state in DP
- Implement 2D DP with state tracking
- Optimize state machine DP solutions

## 📋 Problem Description

Taro's summer vacation starts tomorrow, and he has decided to make plans for it now. The vacation consists of N days. For each i (1 ≤ i ≤ N), Taro will choose one of the following activities and do it on the i-th day:
- A: Swim in the sea. Gain a_i points of happiness.
- B: Catch bugs in the mountains. Gain b_i points of happiness.
- C: Do homework at home. Gain c_i points of happiness.

As Taro has a short temper, he gets bored if he does the same activity for two consecutive days. Find the maximum possible total points of happiness Taro gains.

**Input**: 
- First line: N (1 ≤ N ≤ 10^5)
- Next N lines: a_i, b_i, c_i (1 ≤ a_i, b_i, c_i ≤ 10^4)

**Output**: 
- Print the maximum total points of happiness

**Constraints**:
- 1 ≤ N ≤ 10^5
- 1 ≤ a_i, b_i, c_i ≤ 10^4

**Example**:
```
Input:
3
10 40 70
20 50 80
30 60 90

Output:
210

Explanation**: 
Day 1: Activity C (70 points)
Day 2: Activity B (50 points)
Day 3: Activity A (30 points)
Total: 70 + 50 + 30 = 150

Or:
Day 1: Activity C (70 points)
Day 2: Activity B (50 points)
Day 3: Activity C (90 points)
But this violates the constraint (same activity on consecutive days)

Optimal:
Day 1: Activity C (70 points)
Day 2: Activity A (20 points)
Day 3: Activity C (90 points)
Total: 70 + 20 + 90 = 180

Wait, let me recalculate:
Day 1: Activity B (40) → Day 2: Activity C (80) → Day 3: Activity A (30)
Total: 40 + 80 + 30 = 150

Actually optimal:
Day 1: Activity C (70) → Day 2: Activity A (20) → Day 3: Activity C (90)
But Day 1 and Day 3 both C, which is fine (not consecutive)

Actually, the constraint is no same activity on consecutive days.
So: C(70) → A(20) → C(90) = 180
Or: A(10) → B(50) → C(90) = 150
Or: B(40) → C(80) → A(30) = 150
Or: C(70) → B(50) → A(30) = 150

Wait, let me check: C(70) → A(20) → C(90) = 180 ✓
Or: A(10) → C(80) → B(60) = 150
Or: B(40) → C(80) → A(30) = 150

Actually the answer is 210, so:
C(70) → A(20) → C(90) = 180 ✗
C(70) → B(50) → C(90) = 210 ✓ (Day 1 C, Day 2 B, Day 3 C)
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Solution (Brute Force)

**Key Insights from Recursive Solution**:
- **Recursive Approach**: Try all possible activity sequences
- **Constraint Checking**: Ensure no two consecutive days have same activity
- **Complete Enumeration**: Explore all valid sequences
- **Inefficient**: Exponential time complexity

**Key Insight**: Use recursion to explore all possible activity sequences while respecting the constraint.

**Algorithm**:
- For each day, try all three activities
- If current activity is same as previous, skip
- Track maximum happiness

**Visual Example**:
```
Activities: [10,40,70], [20,50,80], [30,60,90]
            Day 1       Day 2       Day 3

Recursive exploration:
┌─────────────────────────────────────┐
│ Day 1: Try A(10), B(40), C(70)     │
│ Day 2: Try all except previous     │
│ Day 3: Try all except previous     │
│ ... (explores all valid sequences)  │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def vacation_recursive(n, activities):
    """
    Recursive solution for Vacation problem
    
    Args:
        n: number of days
        activities: list of tuples (a_i, b_i, c_i) for each day
    
    Returns:
        int: maximum total happiness
    """
    def max_happiness(day, last_activity):
        """Calculate maximum happiness from day to end"""
        # Base case: all days processed
        if day == n:
            return 0
        
        max_total = 0
        # Try each activity
        for activity_idx, activity_name in enumerate(['A', 'B', 'C']):
            # Skip if same as previous day
            if activity_idx == last_activity:
                continue
            
            # Current day's happiness for this activity
            if activity_idx == 0:
                happiness = activities[day][0]  # a_i
            elif activity_idx == 1:
                happiness = activities[day][1]  # b_i
            else:
                happiness = activities[day][2]  # c_i
            
            # Recurse for next day
            total = happiness + max_happiness(day + 1, activity_idx)
            max_total = max(max_total, total)
        
        return max_total
    
    # Start with no previous activity (use -1)
    return max_happiness(0, -1)

# Example usage
n = 3
activities = [(10, 40, 70), (20, 50, 80), (30, 60, 90)]
result = vacation_recursive(n, activities)
print(f"Maximum happiness: {result}")  # Output: 210
```

**Time Complexity**: O(3^n)
**Space Complexity**: O(n)

**Why it's inefficient**: Exponential time complexity due to recalculating the same subproblems.

---

### Approach 2: Memoized Recursive Solution

**Key Insights from Memoized Solution**:
- **Memoization**: Store results of (day, last_activity) pairs
- **Top-Down DP**: Recursive approach with caching
- **Efficient**: O(n*3) = O(n) time complexity
- **Memory Trade-off**: O(n*3) space for memoization

**Implementation**:
```python
def vacation_memoized(n, activities):
    """
    Memoized recursive solution for Vacation problem
    
    Args:
        n: number of days
        activities: list of tuples (a_i, b_i, c_i) for each day
    
    Returns:
        int: maximum total happiness
    """
    memo = {}
    
    def max_happiness(day, last_activity):
        """Calculate maximum happiness from day to end"""
        # Check memo
        if (day, last_activity) in memo:
            return memo[(day, last_activity)]
        
        # Base case
        if day == n:
            memo[(day, last_activity)] = 0
            return 0
        
        max_total = 0
        for activity_idx in range(3):
            if activity_idx == last_activity:
                continue
            
            happiness = activities[day][activity_idx]
            total = happiness + max_happiness(day + 1, activity_idx)
            max_total = max(max_total, total)
        
        memo[(day, last_activity)] = max_total
        return max_total
    
    return max_happiness(0, -1)

# Example usage
n = 3
activities = [(10, 40, 70), (20, 50, 80), (30, 60, 90)]
result = vacation_memoized(n, activities)
print(f"Maximum happiness: {result}")  # Output: 210
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Why it's better**: Uses memoization to achieve O(n) time complexity.

---

### Approach 3: Bottom-Up Dynamic Programming (Optimal)

**Key Insights from Bottom-Up DP Solution**:
- **Bottom-Up DP**: Build solution from base cases
- **State Machine**: Track previous activity as part of state
- **Efficient**: O(n) time, O(n) or O(1) space
- **Optimal**: Best approach for this problem

**Key Insight**: Use 2D DP where dp[i][j] represents maximum happiness up to day i, ending with activity j.

#### 📌 **DP State Definition**

**What does `dp[i][j]` represent?**
- `dp[i][j]` = **maximum total happiness** up to day i (0-indexed), where day i ends with activity j
- j = 0: Activity A, j = 1: Activity B, j = 2: Activity C
- `dp[0][j]` = activities[0][j] (base case: first day)
- Final answer = max(dp[n-1][0], dp[n-1][1], dp[n-1][2])

**In plain language:**
- For each day i and each activity j, we store the maximum happiness achievable up to day i if we end with activity j
- We ensure no two consecutive days have the same activity

#### 🎯 **DP Thinking Process**

**Step 1: Identify the Subproblem**
- What are we trying to maximize? Total happiness over N days
- What information do we need? For each day, maximum happiness achievable ending with each activity

**Step 2: Define the DP State** (See DP State Definition section above)

**Step 3: Find the Recurrence Relation (State Transition)**
- How do we compute `dp[i][j]`?
- On day i, we choose activity j
- Previous day (i-1) must have chosen a different activity (not j)
- Therefore: `dp[i][j] = activities[i][j] + max(dp[i-1][k])` for all k ≠ j

**Step 4: Determine Base Cases**
- `dp[0][j] = activities[0][j]` for j in {0, 1, 2}: First day can choose any activity

**Step 5: Identify the Answer**
- The answer is `max(dp[n-1][0], dp[n-1][1], dp[n-1][2])` - maximum over all ending activities

#### 📊 **Visual DP Table Construction**

For `n = 3, activities = [(10, 40, 70), (20, 50, 80), (30, 60, 90)]`:
```
Step-by-step DP table filling:

dp[0][0] = 10  (Day 0, Activity A)
dp[0][1] = 40  (Day 0, Activity B)
dp[0][2] = 70  (Day 0, Activity C)

dp[1][0] = 20 + max(dp[0][1], dp[0][2]) = 20 + max(40, 70) = 90
dp[1][1] = 50 + max(dp[0][0], dp[0][2]) = 50 + max(10, 70) = 120
dp[1][2] = 80 + max(dp[0][0], dp[0][1]) = 80 + max(10, 40) = 120

dp[2][0] = 30 + max(dp[1][1], dp[1][2]) = 30 + max(120, 120) = 150
dp[2][1] = 60 + max(dp[1][0], dp[1][2]) = 60 + max(90, 120) = 180
dp[2][2] = 90 + max(dp[1][0], dp[1][1]) = 90 + max(90, 120) = 210

Final answer: max(150, 180, 210) = 210
```

**Algorithm**:
- Initialize `dp[0][j] = activities[0][j]` for j in {0, 1, 2}
- For i from 1 to n-1:
  - For j in {0, 1, 2}:
    - `dp[i][j] = activities[i][j] + max(dp[i-1][k])` for all k ≠ j
- Return `max(dp[n-1][0], dp[n-1][1], dp[n-1][2])`

**Visual Example**:
```
DP table for n=3:
┌─────────────────────────────────────┐
│ Day | Activity A | Activity B | C  │
│  0  |     10     |     40     | 70 │
│  1  |     90     |    120     |120 │
│  2  |    150     |    180     |210 │
│                                     │
│ Optimal path: Day0(C=70) →         │
│              Day1(B=50) →          │
│              Day2(C=90) = 210      │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def vacation_dp(n, activities):
    """
    Bottom-up DP solution for Vacation problem
    
    Args:
        n: number of days
        activities: list of tuples (a_i, b_i, c_i) for each day
    
    Returns:
        int: maximum total happiness
    """
    # Create DP table: dp[i][j] = max happiness up to day i ending with activity j
    # j = 0: A, j = 1: B, j = 2: C
    dp = [[0] * 3 for _ in range(n)]
    
    # Base case: first day
    dp[0][0] = activities[0][0]  # Activity A
    dp[0][1] = activities[0][1]  # Activity B
    dp[0][2] = activities[0][2]  # Activity C
    
    # Fill DP table
    for i in range(1, n):
        for j in range(3):
            # Try all previous activities except j
            max_prev = 0
            for k in range(3):
                if k != j:
                    max_prev = max(max_prev, dp[i - 1][k])
            
            dp[i][j] = activities[i][j] + max_prev
    
    # Return maximum over all ending activities
    return max(dp[n - 1])

# Example usage
n = 3
activities = [(10, 40, 70), (20, 50, 80), (30, 60, 90)]
result = vacation_dp(n, activities)
print(f"Maximum happiness: {result}")  # Output: 210
```

**Time Complexity**: O(n)
**Space Complexity**: O(n)

**Why it's optimal**: Uses bottom-up DP for O(n) time and space complexity.

---

### Approach 4: Space-Optimized DP Solution

**Key Insights from Space-Optimized Solution**:
- **Space Optimization**: Only need previous day's values
- **Rolling Array**: Use 3 variables instead of n*3 array
- **Efficient**: O(n) time, O(1) space
- **Optimal Complexity**: Best space complexity

**Key Insight**: Since we only need dp[i-1] to compute dp[i], we can use just 3 variables.

**Implementation**:
```python
def vacation_space_optimized(n, activities):
    """
    Space-optimized DP solution for Vacation problem
    
    Args:
        n: number of days
        activities: list of tuples (a_i, b_i, c_i) for each day
    
    Returns:
        int: maximum total happiness
    """
    # Only need previous day's values
    prev_a = activities[0][0]
    prev_b = activities[0][1]
    prev_c = activities[0][2]
    
    for i in range(1, n):
        # Current day's values
        curr_a = activities[i][0] + max(prev_b, prev_c)
        curr_b = activities[i][1] + max(prev_a, prev_c)
        curr_c = activities[i][2] + max(prev_a, prev_b)
        
        # Update for next iteration
        prev_a, prev_b, prev_c = curr_a, curr_b, curr_c
    
    return max(prev_a, prev_b, prev_c)

# Example usage
n = 3
activities = [(10, 40, 70), (20, 50, 80), (30, 60, 90)]
result = vacation_space_optimized(n, activities)
print(f"Maximum happiness: {result}")  # Output: 210
```

**Time Complexity**: O(n)
**Space Complexity**: O(1)

**Why it's optimal**: Uses O(1) space while maintaining O(n) time complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(3^n) | O(n) | Complete enumeration of all sequences |
| Memoized | O(n) | O(n) | Cache subproblem results |
| Bottom-Up DP | O(n) | O(n) | Build solution iteratively |
| Space-Optimized DP | O(n) | O(1) | Only need previous day's values |

### Time Complexity
- **Time**: O(n) - Single pass through all days
- **Space**: O(1) - Only three variables needed for space-optimized version

### Why This Solution Works
- **Optimal Substructure**: Maximum happiness up to day i depends on maximum happiness up to day i-1 with different activity
- **State Machine**: Track previous activity to enforce constraint
- **DP Optimization**: Bottom-up approach avoids redundant calculations

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Vacation - Path Reconstruction**
**Problem**: Find maximum happiness and reconstruct the optimal activity sequence.

**Implementation**:
```python
def vacation_with_path(n, activities):
    """
    DP solution with path reconstruction for Vacation problem
    
    Args:
        n: number of days
        activities: list of tuples (a_i, b_i, c_i) for each day
    
    Returns:
        tuple: (maximum happiness, optimal activity sequence)
    """
    dp = [[0] * 3 for _ in range(n)]
    parent = [[-1] * 3 for _ in range(n)]
    
    # Base case
    dp[0][0] = activities[0][0]
    dp[0][1] = activities[0][1]
    dp[0][2] = activities[0][2]
    
    for i in range(1, n):
        for j in range(3):
            max_prev = -1
            best_prev = -1
            for k in range(3):
                if k != j and dp[i - 1][k] > max_prev:
                    max_prev = dp[i - 1][k]
                    best_prev = k
            
            dp[i][j] = activities[i][j] + max_prev
            parent[i][j] = best_prev
    
    # Find best ending activity
    best_end = max(range(3), key=lambda x: dp[n - 1][x])
    max_happiness = dp[n - 1][best_end]
    
    # Reconstruct path
    path = []
    current = best_end
    for i in range(n - 1, -1, -1):
        activity_names = ['A', 'B', 'C']
        path.append(activity_names[current])
        if i > 0:
            current = parent[i][current]
    
    path.reverse()
    return max_happiness, path

# Example usage
n = 3
activities = [(10, 40, 70), (20, 50, 80), (30, 60, 90)]
happiness, path = vacation_with_path(n, activities)
print(f"Maximum happiness: {happiness}")
print(f"Optimal path: {path}")
```

#### **2. Vacation - Multiple Activities**
**Problem**: Extend to k activities instead of 3.

**Implementation**:
```python
def vacation_k_activities(n, k, activities):
    """
    DP solution for Vacation with k activities
    
    Args:
        n: number of days
        k: number of activities
        activities: list of lists, activities[i][j] = happiness for day i, activity j
    
    Returns:
        int: maximum total happiness
    """
    dp = [[0] * k for _ in range(n)]
    
    # Base case
    for j in range(k):
        dp[0][j] = activities[0][j]
    
    for i in range(1, n):
        for j in range(k):
            max_prev = 0
            for prev_j in range(k):
                if prev_j != j:
                    max_prev = max(max_prev, dp[i - 1][prev_j])
            
            dp[i][j] = activities[i][j] + max_prev
    
    return max(dp[n - 1])

# Example usage
n, k = 3, 3
activities = [[10, 40, 70], [20, 50, 80], [30, 60, 90]]
result = vacation_k_activities(n, k, activities)
print(f"Maximum happiness: {result}")
```

### Related Problems

#### **LeetCode Problems**
- [House Robber](https://leetcode.com/problems/house-robber/) - Similar constraint pattern
- [House Robber II](https://leetcode.com/problems/house-robber-ii/) - Circular constraint
- [Paint House](https://leetcode.com/problems/paint-house/) - Almost identical problem
- [Paint House II](https://leetcode.com/problems/paint-house-ii/) - Extension with k colors

#### **AtCoder Problems**
- [Frog 1](https://atcoder.jp/contests/dp/tasks/dp_a) - Similar DP pattern
- [Frog 2](https://atcoder.jp/contests/dp/tasks/dp_b) - Similar structure

#### **Problem Categories**
- **State Machine DP**: Problems with state constraints
- **2D DP with Constraints**: Tracking previous state
- **Maximum Optimization**: Finding optimal sequences with constraints

## 🔗 Additional Resources

### **Algorithm References**
- [Dynamic Programming Introduction](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html) - DP fundamentals
- [State Machine DP](https://cp-algorithms.com/dynamic_programming/state-transitions.html) - State machine techniques

### **Practice Problems**
- [AtCoder DP Contest Problem C](https://atcoder.jp/contests/dp/tasks/dp_c) - Original problem
- [LeetCode Paint House](https://leetcode.com/problems/paint-house/) - Similar problem
- [LeetCode House Robber](https://leetcode.com/problems/house-robber/) - Similar constraint pattern

### **Further Reading**
- [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/books/introduction-algorithms) - Dynamic Programming chapter
- [Competitive Programming Handbook](https://cses.fi/book/book.pdf) - DP section

