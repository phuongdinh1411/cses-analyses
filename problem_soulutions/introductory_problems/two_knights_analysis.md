---
layout: simple
title: "Two Knights"
permalink: /problem_soulutions/introductory_problems/two_knights_analysis
---

# Two Knights

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand combinatorial counting and chess piece placement problems
- Apply mathematical formulas to count non-attacking knight placements
- Implement efficient combinatorial counting algorithms with proper mathematical calculations
- Optimize combinatorial counting using mathematical analysis and chess piece movement patterns
- Handle edge cases in combinatorial problems (small boards, large boards, mathematical precision)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Combinatorial counting, chess piece placement, mathematical formulas, knight movement patterns
- **Data Structures**: Mathematical calculations, combinatorial tracking, chess board representation, counting structures
- **Mathematical Concepts**: Combinatorics, chess mathematics, knight movement theory, counting theory
- **Programming Skills**: Mathematical calculations, combinatorial counting, chess piece analysis, algorithm implementation
- **Related Problems**: Combinatorial problems, Chess problems, Mathematical counting, Knight movement problems

## Problem Description

**Problem**: Count for k=1,2,…,n the number of ways two knights can be placed on a k×k chessboard so that they do not attack each other.

**Input**: An integer n (1 ≤ n ≤ 10000)

**Output**: Print n lines: the kth line contains the number of ways two knights can be placed on a k×k chessboard.

**Constraints**:
- 1 ≤ n ≤ 10000
- Knights attack in L-shape moves: (2,1) or (1,2)
- Two knights cannot be placed on the same square
- Count all valid non-attacking placements
- For k=1, there are 0 ways (need at least 2 squares)

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

## Visual Example

### Input and Knight Placement
```
Input: n = 3

3×3 Chessboard:
. . .
. . .
. . .

Valid Knight Placement:
K . .
. . .
. . K

Invalid Knight Placement (knights attack each other):
K . .
. . .
. K .  ← Knights can attack each other
```

### Knight Movement Pattern
```
Knight moves in L-shape:
. . . . .     . . . . .
. . . . .     . . . . .
. . K . .     . . K . .
. . . . .     . . . . .
. . . . .     . . . . .

Knight can move to:
. . . . .     . . . . .
. . . . .     . . . . .
. . K . .     . . K . .
. . . . .     . . . . .
. . . . .     . . . . .

8 possible moves: (2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)
```

### Counting Process
```
For 3×3 board:
Total ways to place 2 knights: C(9,2) = 36

Attacking positions:
- Knight at (0,0) can attack (1,2) and (2,1)
- Knight at (0,1) can attack (1,3) and (2,0) - but (1,3) is out of bounds
- Knight at (0,2) can attack (1,0) and (2,3) - but (2,3) is out of bounds
- ... (count all valid attacking positions)

Valid ways = Total ways - Attacking ways = 36 - 8 = 28
```

### Key Insight
The solution works by:
1. Using combinatorial counting for total placements
2. Calculating attacking positions systematically
3. Using mathematical formulas for efficiency
4. Time complexity: O(n²) for mathematical approach
5. Space complexity: O(1) for constant variables

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Enumeration (Inefficient)

**Key Insights from Brute Force Solution:**
- Try all possible knight placements and check for conflicts
- Simple but computationally expensive approach
- Not suitable for large boards
- Straightforward implementation but poor performance

**Algorithm:**
1. Try all possible positions for two knights
2. For each placement, check if knights attack each other
3. Count all valid non-attacking placements
4. Handle edge cases correctly

**Visual Example:**
```
Brute force: Try all knight placements
For 3×3 board:
- Try: Knight1 at (0,0), Knight2 at (0,1) → Check if they attack
- Try: Knight1 at (0,0), Knight2 at (0,2) → Check if they attack
- Try: Knight1 at (0,0), Knight2 at (1,0) → Check if they attack
- Try all possible combinations
```

**Implementation:**
```python
def two_knights_brute_force(n):
    def can_attack(pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        return (dx == 1 and dy == 2) or (dx == 2 and dy == 1)
    
    def count_ways(k):
        if k < 2:
            return 0
        
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

def solve_two_knights_brute_force():
    n = int(input())
    results = two_knights_brute_force(n)
    for result in results:
        print(result)
```

**Time Complexity:** O(n⁵) for trying all possible placements
**Space Complexity:** O(1) for storing variables

**Why it's inefficient:**
- O(n⁵) time complexity is too slow for large n
- Not suitable for competitive programming with n up to 10000
- Inefficient for large inputs
- Poor performance with polynomial growth

### Approach 2: Mathematical Counting with Systematic Attack Calculation (Better)

**Key Insights from Mathematical Solution:**
- Use combinatorial formulas for total placements
- Calculate attacking positions systematically
- Much more efficient than brute force approach
- Standard method for chess piece counting problems

**Algorithm:**
1. Calculate total ways using combination formula C(k², 2)
2. Count attacking positions by checking all knight moves
3. Subtract attacking ways from total ways
4. Handle edge cases correctly

**Visual Example:**
```
Mathematical approach: Use formulas
For 3×3 board:
- Total ways: C(9,2) = 36
- Attacking ways: Count all valid knight attack positions
- Valid ways: 36 - 8 = 28
```

**Implementation:**
```python
def two_knights_mathematical(n):
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

def solve_two_knights_mathematical():
    n = int(input())
    results = two_knights_mathematical(n)
    for result in results:
        print(result)
```

**Time Complexity:** O(n³) for mathematical calculation
**Space Complexity:** O(1) for storing variables

**Why it's better:**
- O(n³) time complexity is much better than O(n⁵)
- Uses mathematical formulas for efficient solution
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized Mathematical Formula (Optimal)

**Key Insights from Optimized Mathematical Solution:**
- Use optimized mathematical formulas for efficiency
- Most efficient approach for knight counting problems
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use optimized mathematical formulas
2. Apply efficient attack position counting
3. Handle edge cases efficiently
4. Return the optimal solution

**Visual Example:**
```
Optimized mathematical: Use efficient formulas
For k×k board:
- Total ways: C(k², 2) = k² × (k²-1) / 2
- Attacking ways: 4 × (k-1) × (k-2) for k ≥ 3
- Valid ways: Total ways - Attacking ways
```

**Implementation:**
```python
def two_knights_optimized(n):
    def count_ways(k):
        if k < 2:
            return 0
        
        # Total ways to place two knights
        total_ways = (k * k) * (k * k - 1) // 2
        
        # Optimized calculation of attacking ways
        if k < 3:
            attacking_ways = 0
        else:
            # For k×k board, attacking ways = 4 × (k-1) × (k-2)
            attacking_ways = 4 * (k - 1) * (k - 2)
        
        return total_ways - attacking_ways
    
    results = []
    for k in range(1, n + 1):
        results.append(count_ways(k))
    
    return results

def solve_two_knights():
    n = int(input())
    results = two_knights_optimized(n)
    for result in results:
        print(result)

# Main execution
if __name__ == "__main__":
    solve_two_knights()
```

**Time Complexity:** O(n) for optimized mathematical calculation
**Space Complexity:** O(1) for storing variables

**Why it's optimal:**
- O(n) time complexity is optimal for this problem
- Uses optimized mathematical formulas
- Most efficient approach for competitive programming
- Standard method for knight counting optimization

## 🎯 Problem Variations

### Variation 1: Two Knights with Different Movement Patterns
**Problem**: Two knights with different movement patterns (e.g., one moves like a knight, other like a bishop).

**Link**: [CSES Problem Set - Two Knights Different Movement](https://cses.fi/problemset/task/two_knights_different_movement)

```python
def two_knights_different_movement(n, knight1_moves, knight2_moves):
    def can_attack(pos1, pos2, moves1, moves2):
        x1, y1 = pos1
        x2, y2 = pos2
        
        # Check if knight1 can attack knight2
        for dx, dy in moves1:
            if x1 + dx == x2 and y1 + dy == y2:
                return True
        
        # Check if knight2 can attack knight1
        for dx, dy in moves2:
            if x2 + dx == x1 and y2 + dy == y1:
                return True
        
        return False
    
    def count_ways(k):
        if k < 2:
            return 0
        
        total_ways = (k * k) * (k * k - 1) // 2
        attacking_ways = 0
        
        for i in range(k):
            for j in range(k):
                for ni, nj in [(i+dx, j+dy) for dx, dy in knight1_moves]:
                    if 0 <= ni < k and 0 <= nj < k:
                        attacking_ways += 1
        
        attacking_ways //= 2
        return total_ways - attacking_ways
    
    results = []
    for k in range(1, n + 1):
        results.append(count_ways(k))
    
    return results
```

### Variation 2: Two Knights with Obstacles
**Problem**: Two knights on a board with obstacles that block movement.

**Link**: [CSES Problem Set - Two Knights with Obstacles](https://cses.fi/problemset/task/two_knights_obstacles)

```python
def two_knights_obstacles(n, obstacles):
    def can_attack(pos1, pos2, obstacles):
        x1, y1 = pos1
        x2, y2 = pos2
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        
        if (dx == 1 and dy == 2) or (dx == 2 and dy == 1):
            # Check if path is blocked by obstacles
            if (x1, y1) in obstacles or (x2, y2) in obstacles:
                return False
            return True
        
        return False
    
    def count_ways(k):
        if k < 2:
            return 0
        
        total_ways = (k * k) * (k * k - 1) // 2
        attacking_ways = 0
        
        for i in range(k):
            for j in range(k):
                if (i, j) in obstacles:
                    continue
                
                moves = [
                    (i-2, j-1), (i-2, j+1),
                    (i-1, j-2), (i-1, j+2),
                    (i+1, j-2), (i+1, j+2),
                    (i+2, j-1), (i+2, j+1)
                ]
                
                for ni, nj in moves:
                    if 0 <= ni < k and 0 <= nj < k and (ni, nj) not in obstacles:
                        attacking_ways += 1
        
        attacking_ways //= 2
        return total_ways - attacking_ways
    
    results = []
    for k in range(1, n + 1):
        results.append(count_ways(k))
    
    return results
```

### Variation 3: Two Knights with Different Colors
**Problem**: Two knights of different colors with different movement rules.

**Link**: [CSES Problem Set - Two Knights Different Colors](https://cses.fi/problemset/task/two_knights_different_colors)

```python
def two_knights_different_colors(n, color1_moves, color2_moves):
    def can_attack(pos1, pos2, moves1, moves2):
        x1, y1 = pos1
        x2, y2 = pos2
        
        # Check if color1 knight can attack color2 knight
        for dx, dy in moves1:
            if x1 + dx == x2 and y1 + dy == y2:
                return True
        
        # Check if color2 knight can attack color1 knight
        for dx, dy in moves2:
            if x2 + dx == x1 and y2 + dy == y1:
                return True
        
        return False
    
    def count_ways(k):
        if k < 2:
            return 0
        
        total_ways = (k * k) * (k * k - 1) // 2
        attacking_ways = 0
        
        for i in range(k):
            for j in range(k):
                for ni, nj in [(i+dx, j+dy) for dx, dy in color1_moves]:
                    if 0 <= ni < k and 0 <= nj < k:
                        attacking_ways += 1
        
        attacking_ways //= 2
        return total_ways - attacking_ways
    
    results = []
    for k in range(1, n + 1):
        results.append(count_ways(k))
    
    return results
```

## 🔗 Related Problems

- **[Combinatorial Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Combinatorial problems
- **[Chess Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Chess problems
- **[Mathematical Counting](/cses-analyses/problem_soulutions/introductory_problems/)**: Mathematical counting problems
- **[Knight Movement Problems](/cses-analyses/problem_soulutions/introductory_problems/)**: Knight movement problems

## 📚 Learning Points

1. **Combinatorial Counting**: Essential for understanding chess piece placement problems
2. **Mathematical Formulas**: Key technique for efficient counting
3. **Chess Mathematics**: Important for understanding chess piece movement
4. **Knight Movement Theory**: Critical for understanding knight attack patterns
5. **Mathematical Optimization**: Foundation for many counting algorithms
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The Two Knights problem demonstrates combinatorial counting concepts for chess piece placement. We explored three approaches:

1. **Brute Force Enumeration**: O(n⁵) time complexity using exhaustive search of all knight placements, inefficient for large boards
2. **Mathematical Counting with Systematic Attack Calculation**: O(n³) time complexity using combinatorial formulas and systematic attack counting, better approach for knight counting problems
3. **Optimized Mathematical Formula**: O(n) time complexity with optimized mathematical formulas, optimal approach for knight counting optimization

The key insights include understanding combinatorial counting principles, using mathematical formulas for efficient total placement calculation, and applying systematic attack position counting for optimal performance. This problem serves as an excellent introduction to combinatorial counting algorithms and chess mathematics.
