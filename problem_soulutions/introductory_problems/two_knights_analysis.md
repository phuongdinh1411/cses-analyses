---
layout: simple
title: "Two Knights"
permalink: /problem_soulutions/introductory_problems/two_knights_analysis
---

# Two Knights

## Problem Description

**Problem**: Count for k=1,2,…,n the number of ways two knights can be placed on a k×k chessboard so that they do not attack each other.

**Input**: An integer n (1 ≤ n ≤ 10000)

**Output**: Print n lines: the kth line contains the number of ways two knights can be placed on a k×k chessboard.

**Example**:
```
Input: 8

Output:
0
6
28
96
252
550
1056
1848
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Place two knights on a k×k chessboard
- Count ways where knights don't attack each other
- Do this for all board sizes from 1 to n

**Key Observations:**
- Knights attack in L-shape: (2,1) or (1,2) moves
- Total ways = C(k², 2) = k² × (k²-1) / 2
- Attacking ways = positions where knights can attack each other
- Valid ways = Total ways - Attacking ways

### Step 2: Brute Force Approach
**Idea**: Try all possible positions and check if knights attack each other.

```python
def two_knights_brute_force(n):
    def can_attack(pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)
    
    def count_ways(k):
        total_positions = k * k
        ways = 0
        
        for i in range(total_positions):
            for j in range(i + 1, total_positions):
                pos1 = (i // k, i % k)
                pos2 = (j // k, j % k)
                if not can_attack(pos1, pos2):
                    ways += 1
        
        return ways
    
    results = []
    for k in range(1, n + 1):
        results.append(count_ways(k))
    
    return results
```

**Why this doesn't work:**
- O(k⁴) complexity for each board size
- O(n⁵) total complexity
- Too slow for large n

### Step 3: Mathematical Formula
**Idea**: Use mathematical formulas to calculate directly.

```python
def two_knights_math(n):
    def count_ways(k):
        if k < 2:
            return 0
        
        # Total ways to place two knights
        total_ways = (k * k) * (k * k - 1) // 2
        
        # Ways where knights attack each other
        attacking_ways = 0
        
        # Count attacking positions
        for i in range(k):
            for j in range(k):
                # Check all 8 possible knight moves
                moves = [
                    (i-2, j-1), (i-2, j+1),
                    (i-1, j-2), (i-1, j+2),
                    (i+1, j-2), (i+1, j+2),
                    (i+2, j-1), (i+2, j+1)
                ]
                
                for ni, nj in moves:
                    if 0 <= ni < k and 0 <= nj < k:
                        attacking_ways += 1
        
        # Each attacking pair is counted twice, so divide by 2
        attacking_ways //= 2
        
        return total_ways - attacking_ways
    
    results = []
    for k in range(1, n + 1):
        results.append(count_ways(k))
    
    return results
```

**Why this works:**
- Calculate total ways using combination formula
- Count attacking positions systematically
- Subtract to get valid positions

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_two_knights():
    n = int(input())
    
    for k in range(1, n + 1):
        if k < 2:
            print(0)
            continue
        
        # Total ways to place two knights
        total_ways = (k * k) * (k * k - 1) // 2
        
        # Ways where knights attack each other
        attacking_ways = 0
        
        # Count attacking positions
        for i in range(k):
            for j in range(k):
                # Check all 8 possible knight moves
                moves = [
                    (i-2, j-1), (i-2, j+1),
                    (i-1, j-2), (i-1, j+2),
                    (i+1, j-2), (i+1, j+2),
                    (i+2, j-1), (i+2, j+1)
                ]
                
                for ni, nj in moves:
                    if 0 <= ni < k and 0 <= nj < k:
                        attacking_ways += 1
        
        # Each attacking pair is counted twice, so divide by 2
        attacking_ways //= 2
        
        print(total_ways - attacking_ways)

# Main execution
if __name__ == "__main__":
    solve_two_knights()
```

**Why this works:**
- Efficient mathematical approach
- Handles all board sizes correctly
- Uses combination formula for total ways

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (1, [0]),
        (2, [0, 6]),
        (3, [0, 6, 28]),
        (4, [0, 6, 28, 96]),
    ]
    
    for n, expected in test_cases:
        result = solve_test(n)
        print(f"n = {n}")
        print(f"Expected: {expected}")
        print(f"Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n):
    results = []
    for k in range(1, n + 1):
        if k < 2:
            results.append(0)
            continue
        
        total_ways = (k * k) * (k * k - 1) // 2
        attacking_ways = 0
        
        for i in range(k):
            for j in range(k):
                moves = [
                    (i-2, j-1), (i-2, j+1),
                    (i-1, j-2), (i-1, j+2),
                    (i+1, j-2), (i+1, j+2),
                    (i+2, j-1), (i+2, j+1)
                ]
                
                for ni, nj in moves:
                    if 0 <= ni < k and 0 <= nj < k:
                        attacking_ways += 1
        
        attacking_ways //= 2
        results.append(total_ways - attacking_ways)
    
    return results

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n × k²) - for each board size, check each position
- **Space**: O(1) - constant space

### Why This Solution Works
- **Mathematical**: Uses combination formula for total ways
- **Systematic**: Counts attacking positions systematically
- **Correct**: Handles all edge cases properly

## 🎯 Key Insights

### 1. **Knight Movement**
- Knights move in L-shape: (2,1) or (1,2) moves
- 8 possible attacking positions from each square

### 2. **Combination Formula**
- Total ways to place two knights: C(k², 2) = k² × (k²-1) / 2
- This gives us all possible positions

### 3. **Attacking Positions**
- Count positions where knights can attack each other
- Each attacking pair is counted twice, so divide by 2

## 🎯 Problem Variations

### Variation 1: Three Knights
**Problem**: Count ways to place three knights without attacking each other.

```python
def three_knights(n):
    def count_ways(k):
        if k < 3:
            return 0
        
        # Total ways to place three knights
        total_ways = (k * k) * (k * k - 1) * (k * k - 2) // 6
        
        # Ways where knights attack each other
        attacking_ways = 0
        
        # Count all attacking configurations
        for i in range(k):
            for j in range(k):
                moves = [
                    (i-2, j-1), (i-2, j+1),
                    (i-1, j-2), (i-1, j+2),
                    (i+1, j-2), (i+1, j+2),
                    (i+2, j-1), (i+2, j+1)
                ]
                
                for ni, nj in moves:
                    if 0 <= ni < k and 0 <= nj < k:
                        # Count configurations with this attacking pair
                        attacking_ways += (k * k - 2)
        
        return total_ways - attacking_ways // 2
    
    return [count_ways(k) for k in range(1, n + 1)]
```

### Variation 2: Different Pieces
**Problem**: Count ways to place a knight and a bishop without attacking.

```python
def knight_bishop(n):
    def count_ways(k):
        if k < 2:
            return 0
        
        # Total ways to place knight and bishop
        total_ways = k * k * (k * k - 1)
        
        # Ways where they attack each other
        attacking_ways = 0
        
        for i in range(k):
            for j in range(k):
                # Knight moves
                knight_moves = [
                    (i-2, j-1), (i-2, j+1),
                    (i-1, j-2), (i-1, j+2),
                    (i+1, j-2), (i+1, j+2),
                    (i+2, j-1), (i+2, j+1)
                ]
                
                # Bishop moves (diagonal)
                for di in range(1, k):
                    bishop_moves = [
                        (i+di, j+di), (i+di, j-di),
                        (i-di, j+di), (i-di, j-di)
                    ]
                    
                    for ni, nj in bishop_moves:
                        if 0 <= ni < k and 0 <= nj < k:
                            attacking_ways += 1
        
        return total_ways - attacking_ways
    
    return [count_ways(k) for k in range(1, n + 1)]
```

### Variation 3: Weighted Positions
**Problem**: Each position has a weight. Find maximum total weight.

```python
def weighted_knights(n, weights):
    # weights[i][j] = weight of position (i, j)
    def count_ways(k):
        if k < 2:
            return 0
        
        max_weight = 0
        
        for i in range(k):
            for j in range(k):
                for ni in range(k):
                    for nj in range(k):
                        if (i, j) != (ni, nj):
                            # Check if knights attack each other
                            dx = abs(i - ni)
                            dy = abs(j - nj)
                            if not ((dx == 1 and dy == 2) or (dx == 2 and dy == 1)):
                                weight = weights[i][j] + weights[ni][nj]
                                max_weight = max(max_weight, weight)
        
        return max_weight
    
    return [count_ways(k) for k in range(1, n + 1)]
```

### Variation 4: Circular Board
**Problem**: Board wraps around (toroidal surface).

```python
def circular_knights(n):
    def count_ways(k):
        if k < 2:
            return 0
        
        total_ways = (k * k) * (k * k - 1) // 2
        attacking_ways = 0
        
        for i in range(k):
            for j in range(k):
                # Knight moves with wraparound
                moves = [
                    ((i-2) % k, (j-1) % k),
                    ((i-2) % k, (j+1) % k),
                    ((i-1) % k, (j-2) % k),
                    ((i-1) % k, (j+2) % k),
                    ((i+1) % k, (j-2) % k),
                    ((i+1) % k, (j+2) % k),
                    ((i+2) % k, (j-1) % k),
                    ((i+2) % k, (j+1) % k)
                ]
                
                for ni, nj in moves:
                    attacking_ways += 1
        
        attacking_ways //= 2
        return total_ways - attacking_ways
    
    return [count_ways(k) for k in range(1, n + 1)]
```

## 🔗 Related Problems

- **[Chessboard and Queens](/cses-analyses/problem_soulutions/introductory_problems/chessboard_and_queens_analysis)**: Chess piece placement
- **[Two Sets](/cses-analyses/problem_soulutions/introductory_problems/two_sets_analysis)**: Counting problems
- **[Grid Coloring I](/cses-analyses/problem_soulutions/introductory_problems/grid_coloring_i_analysis)**: Constraint satisfaction

## 📚 Learning Points

1. **Mathematical Counting**: Using combination formulas
2. **Chess Piece Movement**: Understanding knight movement patterns
3. **Systematic Counting**: Counting attacking positions systematically
4. **Optimization**: Avoiding brute force approaches

---

**This is a great introduction to mathematical counting and chess piece problems!** 🎯 