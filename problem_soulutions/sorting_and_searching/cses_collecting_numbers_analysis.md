---
layout: simple
title: "Collecting Numbers"
permalink: /problem_soulutions/sorting_and_searching/cses_collecting_numbers_analysis
---

# Collecting Numbers

## Problem Description

**Problem**: You are given an array containing each number between 1…n exactly once. Collect numbers from 1 to n in increasing order. On each round, go through the array from left to right and collect as many numbers as possible in increasing order. Find the minimum number of rounds needed.

**Input**: 
- First line: n (array size)
- Second line: n integers x₁, x₂, ..., xₙ

**Output**: Minimum number of rounds needed.

**Example**:
```
Input:
5
4 2 1 5 3

Output:
3

Explanation: 
Round 1: Collect 1 (position 3)
Round 2: Collect 2 (position 2) 
Round 3: Collect 3, 4, 5 (positions 5, 1, 4)
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Collect numbers 1 to n in increasing order
- Each round: scan array from left to right
- Collect as many numbers as possible in increasing order
- Find minimum rounds needed

**Key Observations:**
- Numbers must be collected in order: 1, 2, 3, ..., n
- If we encounter a smaller number after a larger one, we need a new round
- Can track positions of each number
- Need to count "backward jumps"

### Step 2: Position Tracking Approach
**Idea**: Track positions of each number and count when we need to go backward.

```python
def collecting_numbers_positions(arr):
    n = len(arr)
    
    # Create position map: number -> position
    positions = {}
    for i, num in enumerate(arr):
        positions[num] = i
    
    rounds = 1
    current_pos = -1  # Position of last collected number
    
    for target in range(1, n + 1):
        target_pos = positions[target]
        
        # If current target comes before the last collected number,
        # we need a new round
        if target_pos < current_pos:
            rounds += 1
        
        current_pos = target_pos
    
    return rounds
```

**Why this works:**
- Track position of each number
- For each target number, check if it comes before the last collected number
- If yes, we need a new round
- This counts the minimum rounds needed

### Step 3: Optimized Solution
**Idea**: Simplify the approach with cleaner logic.

```python
def collecting_numbers_optimized(arr):
    n = len(arr)
    
    # Create position array
    pos = [0] * (n + 1)
    for i, num in enumerate(arr):
        pos[num] = i
    
    rounds = 1
    
    for i in range(2, n + 1):
        # If current number comes before previous number, need new round
        if pos[i] < pos[i - 1]:
            rounds += 1
    
    return rounds
```

**Why this is better:**
- Simpler logic: just compare consecutive positions
- More efficient: no need for current_pos tracking
- Cleaner implementation

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_collecting_numbers():
    n = int(input())
    arr = list(map(int, input().split()))
    
    # Create position array
    pos = [0] * (n + 1)
    for i, num in enumerate(arr):
        pos[num] = i
    
    rounds = 1
    
    for i in range(2, n + 1):
        # If current number comes before previous number, need new round
        if pos[i] < pos[i - 1]:
            rounds += 1
    
    print(rounds)

# Main execution
if __name__ == "__main__":
    solve_collecting_numbers()
```

**Why this works:**
- Efficient position tracking
- Simple comparison logic
- Handles all cases correctly

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ([4, 2, 1, 5, 3], 3),
        ([1, 2, 3, 4, 5], 1),
        ([5, 4, 3, 2, 1], 5),
        ([3, 1, 2], 2),
    ]
    
    for arr, expected in test_cases:
        result = solve_test(arr)
        print(f"Array: {arr}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(arr):
    n = len(arr)
    
    # Create position array
    pos = [0] * (n + 1)
    for i, num in enumerate(arr):
        pos[num] = i
    
    rounds = 1
    
    for i in range(2, n + 1):
        if pos[i] < pos[i - 1]:
            rounds += 1
    
    return rounds

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through array
- **Space**: O(n) - position array

### Why This Solution Works
- **Position Tracking**: Efficiently track where each number is
- **Simple Logic**: Count backward jumps
- **Optimal**: Linear time complexity

## 🎯 Key Insights

### 1. **Position Mapping**
- Map each number to its position in array
- Enables efficient position comparison
- Key insight: track positions instead of simulating rounds

### 2. **Backward Jump Counting**
- Count when we need to go backward in array
- Each backward jump requires a new round
- Simple comparison: pos[i] < pos[i-1]

### 3. **Greedy Collection**
- Always collect numbers in order 1, 2, 3, ..., n
- No need to simulate actual collection process
- Just count the minimum rounds needed

## 🎯 Problem Variations

### Variation 1: Collecting in Different Orders
**Problem**: Collect numbers in different orders (e.g., descending, custom order).

```python
def collecting_custom_order(arr, order):
    n = len(arr)
    
    # Create position array
    pos = [0] * (n + 1)
    for i, num in enumerate(arr):
        pos[num] = i
    
    rounds = 1
    
    for i in range(1, len(order)):
        # If current number comes before previous number, need new round
        if pos[order[i]] < pos[order[i - 1]]:
            rounds += 1
    
    return rounds

# Example: collect in descending order
def collecting_descending(arr):
    n = len(arr)
    order = list(range(n, 0, -1))  # n, n-1, ..., 1
    return collecting_custom_order(arr, order)
```

### Variation 2: Multiple Collections per Round
**Problem**: Each round can collect up to k numbers.

```python
def collecting_with_limit(arr, k):
    n = len(arr)
    
    # Create position array
    pos = [0] * (n + 1)
    for i, num in enumerate(arr):
        pos[num] = i
    
    rounds = 1
    collected_in_round = 1
    
    for i in range(2, n + 1):
        if pos[i] < pos[i - 1]:
            # Need new round
            rounds += 1
            collected_in_round = 1
        else:
            collected_in_round += 1
            if collected_in_round > k:
                # Current round is full, need new round
                rounds += 1
                collected_in_round = 1
    
    return rounds
```

### Variation 3: Weighted Collection
**Problem**: Each number has a weight. Minimize total weight of rounds.

```python
def collecting_weighted(arr, weights):
    n = len(arr)
    
    # Create position array
    pos = [0] * (n + 1)
    for i, num in enumerate(arr):
        pos[num] = i
    
    # Dynamic programming approach
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    
    for i in range(1, n + 1):
        # Try starting a new round at position i
        for j in range(i):
            if pos[i] > pos[j]:
                dp[i] = min(dp[i], dp[j] + weights[i])
    
    return dp[n]
```

### Variation 4: Circular Collection
**Problem**: Array is circular. Collect numbers in circular order.

```python
def collecting_circular(arr):
    n = len(arr)
    
    # Create position array
    pos = [0] * (n + 1)
    for i, num in enumerate(arr):
        pos[num] = i
    
    rounds = 1
    
    for i in range(2, n + 1):
        # Handle circular case
        prev_pos = pos[i - 1]
        curr_pos = pos[i]
        
        # Check if we need to wrap around
        if curr_pos < prev_pos:
            # Check if it's a small wrap or large wrap
            if curr_pos + n - prev_pos < prev_pos - curr_pos:
                # Small wrap, might not need new round
                pass
            else:
                rounds += 1
    
    return rounds
```

### Variation 5: Dynamic Updates
**Problem**: Support adding/removing numbers dynamically.

```python
class DynamicCollectingNumbers:
    def __init__(self):
        self.arr = []
        self.pos = {}
        self.n = 0
    
    def add_number(self, num):
        self.arr.append(num)
        self.pos[num] = self.n
        self.n += 1
        return self.get_rounds()
    
    def remove_number(self, num):
        if num in self.pos:
            # Remove and update positions
            idx = self.pos[num]
            self.arr.pop(idx)
            del self.pos[num]
            
            # Update positions for remaining numbers
            for i in range(idx, len(self.arr)):
                self.pos[self.arr[i]] = i
            
            self.n -= 1
            return self.get_rounds()
        return self.get_rounds()
    
    def get_rounds(self):
        if self.n <= 1:
            return 1
        
        rounds = 1
        for i in range(2, self.n + 1):
            if i in self.pos and i-1 in self.pos:
                if self.pos[i] < self.pos[i-1]:
                    rounds += 1
        
        return rounds
```

## 🔗 Related Problems

- **[Collecting Numbers II](/cses-analyses/problem_soulutions/sorting_and_searching/collecting_numbers_ii_analysis)**: Advanced collecting problems
- **[Distinct Numbers](/cses-analyses/problem_soulutions/sorting_and_searching/cses_distinct_numbers_analysis)**: Array processing
- **[Array Division](/cses-analyses/problem_soulutions/sorting_and_searching/array_division_analysis)**: Array manipulation

## 📚 Learning Points

1. **Position Tracking**: Efficient way to track element positions
2. **Greedy Algorithms**: Optimal local choices
3. **Array Processing**: Efficient array manipulation techniques
4. **Problem Simplification**: Convert complex simulation to simple counting

---

**This is a great introduction to position tracking and greedy algorithms!** 🎯 