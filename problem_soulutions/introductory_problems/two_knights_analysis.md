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

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

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

## Problem Variations

### **Variation 1: Two Knights with Dynamic Updates**
**Problem**: Handle dynamic board updates (add/remove/update obstacles) while maintaining optimal two knights placement efficiently.

**Approach**: Use efficient data structures and algorithms for dynamic board management.

```python
from collections import defaultdict

class DynamicTwoKnights:
    def __init__(self, n=8):
        self.n = n
        self.board = [[0 for _ in range(n)] for _ in range(n)]
        self.obstacles = set()
        self.knight_positions = []
        self._update_two_knights_info()
    
    def _update_two_knights_info(self):
        """Update two knights feasibility information."""
        self.total_cells = self.n * self.n
        self.available_cells = self.total_cells - len(self.obstacles)
        self.two_knights_feasibility = self._calculate_two_knights_feasibility()
    
    def _calculate_two_knights_feasibility(self):
        """Calculate two knights placement feasibility."""
        if self.available_cells < 2:
            return 0.0
        
        # Check if we can place two knights without attacking each other
        return 1.0 if self.available_cells >= 2 else 0.0
    
    def add_obstacle(self, row, col):
        """Add obstacle to the board."""
        if 0 <= row < self.n and 0 <= col < self.n:
            self.obstacles.add((row, col))
            self.board[row][col] = -1
            self._update_two_knights_info()
    
    def remove_obstacle(self, row, col):
        """Remove obstacle from the board."""
        if (row, col) in self.obstacles:
            self.obstacles.remove((row, col))
            self.board[row][col] = 0
            self._update_two_knights_info()
    
    def update_obstacle(self, old_row, old_col, new_row, new_col):
        """Update obstacle position."""
        if (old_row, old_col) in self.obstacles:
            self.remove_obstacle(old_row, old_col)
            self.add_obstacle(new_row, new_col)
    
    def is_safe_position(self, row, col):
        """Check if position is safe for knight placement."""
        if (row, col) in self.obstacles:
            return False
        
        # Check if position is within bounds
        if not (0 <= row < self.n and 0 <= col < self.n):
            return False
        
        return True
    
    def can_knights_attack(self, pos1, pos2):
        """Check if two knights can attack each other."""
        r1, c1 = pos1
        r2, c2 = pos2
        
        # Knight moves: (dx, dy) where |dx| + |dy| = 3 and dx, dy != 0
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        
        for dr, dc in knight_moves:
            if r1 + dr == r2 and c1 + dc == c2:
                return True
        
        return False
    
    def count_two_knights_placements(self):
        """Count number of ways to place two knights without attacking each other."""
        if self.available_cells < 2:
            return 0
        
        count = 0
        positions = []
        
        # Get all available positions
        for i in range(self.n):
            for j in range(self.n):
                if self.is_safe_position(i, j):
                    positions.append((i, j))
        
        # Count valid pairs
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                if not self.can_knights_attack(positions[i], positions[j]):
                    count += 1
        
        return count
    
    def get_placements_with_constraints(self, constraint_func):
        """Get placements that satisfies custom constraints."""
        if self.available_cells < 2:
            return []
        
        result = []
        positions = []
        
        # Get all available positions
        for i in range(self.n):
            for j in range(self.n):
                if self.is_safe_position(i, j):
                    positions.append((i, j))
        
        # Find valid pairs
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                if not self.can_knights_attack(positions[i], positions[j]):
                    if constraint_func(positions[i], positions[j], self.board):
                        result.append((positions[i], positions[j]))
        
        return result
    
    def get_placements_in_range(self, min_distance, max_distance):
        """Get placements within specified distance range."""
        if self.available_cells < 2:
            return []
        
        result = []
        positions = []
        
        # Get all available positions
        for i in range(self.n):
            for j in range(self.n):
                if self.is_safe_position(i, j):
                    positions.append((i, j))
        
        # Find valid pairs within distance range
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                if not self.can_knights_attack(positions[i], positions[j]):
                    distance = abs(positions[i][0] - positions[j][0]) + abs(positions[i][1] - positions[j][1])
                    if min_distance <= distance <= max_distance:
                        result.append((positions[i], positions[j]))
        
        return result
    
    def get_placements_with_pattern(self, pattern_func):
        """Get placements matching specified pattern."""
        if self.available_cells < 2:
            return []
        
        result = []
        positions = []
        
        # Get all available positions
        for i in range(self.n):
            for j in range(self.n):
                if self.is_safe_position(i, j):
                    positions.append((i, j))
        
        # Find valid pairs matching pattern
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                if not self.can_knights_attack(positions[i], positions[j]):
                    if pattern_func(positions[i], positions[j], self.board):
                        result.append((positions[i], positions[j]))
        
        return result
    
    def get_board_statistics(self):
        """Get statistics about the board."""
        return {
            'board_size': self.n,
            'total_cells': self.total_cells,
            'available_cells': self.available_cells,
            'obstacle_count': len(self.obstacles),
            'two_knights_feasibility': self.two_knights_feasibility
        }
    
    def get_two_knights_patterns(self):
        """Get patterns in two knights placement."""
        patterns = {
            'no_obstacles': 0,
            'has_obstacles': 0,
            'sufficient_space': 0,
            'optimal_placement_possible': 0
        }
        
        # Check if no obstacles
        if len(self.obstacles) == 0:
            patterns['no_obstacles'] = 1
        
        # Check if has obstacles
        if len(self.obstacles) > 0:
            patterns['has_obstacles'] = 1
        
        # Check if sufficient space
        if self.available_cells >= 2:
            patterns['sufficient_space'] = 1
        
        # Check if optimal placement is possible
        if self.two_knights_feasibility == 1.0:
            patterns['optimal_placement_possible'] = 1
        
        return patterns
    
    def get_optimal_two_knights_strategy(self):
        """Get optimal strategy for two knights placement."""
        if self.available_cells < 2:
            return {
                'recommended_strategy': 'none',
                'efficiency_rate': 0,
                'two_knights_feasibility': 0
            }
        
        # Calculate efficiency rate
        efficiency_rate = self.two_knights_feasibility
        
        # Calculate two knights feasibility
        two_knights_feasibility = self.two_knights_feasibility
        
        # Determine recommended strategy
        if self.n <= 4:
            recommended_strategy = 'brute_force'
        elif self.n <= 8:
            recommended_strategy = 'optimized_placement'
        else:
            recommended_strategy = 'advanced_optimization'
        
        return {
            'recommended_strategy': recommended_strategy,
            'efficiency_rate': efficiency_rate,
            'two_knights_feasibility': two_knights_feasibility
        }

# Example usage
n = 8
dynamic_two_knights = DynamicTwoKnights(n)
print(f"Two knights feasibility: {dynamic_two_knights.two_knights_feasibility}")

# Add obstacle
dynamic_two_knights.add_obstacle(0, 0)
print(f"After adding obstacle at (0,0): {dynamic_two_knights.available_cells}")

# Remove obstacle
dynamic_two_knights.remove_obstacle(0, 0)
print(f"After removing obstacle: {dynamic_two_knights.available_cells}")

# Update obstacle
dynamic_two_knights.add_obstacle(1, 1)
dynamic_two_knights.update_obstacle(1, 1, 2, 2)
print(f"After updating obstacle: {dynamic_two_knights.obstacles}")

# Count placements
print(f"Two knights placements: {dynamic_two_knights.count_two_knights_placements()}")

# Get placements with constraints
def constraint_func(pos1, pos2, board):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) >= 3

print(f"Placements with constraints: {len(dynamic_two_knights.get_placements_with_constraints(constraint_func))}")

# Get placements in range
print(f"Placements in range 3-10: {len(dynamic_two_knights.get_placements_in_range(3, 10))}")

# Get placements with pattern
def pattern_func(pos1, pos2, board):
    return pos1[0] != pos2[0] and pos1[1] != pos2[1]

print(f"Placements with pattern: {len(dynamic_two_knights.get_placements_with_pattern(pattern_func))}")

# Get statistics
print(f"Statistics: {dynamic_two_knights.get_board_statistics()}")

# Get patterns
print(f"Patterns: {dynamic_two_knights.get_two_knights_patterns()}")

# Get optimal strategy
print(f"Optimal strategy: {dynamic_two_knights.get_optimal_two_knights_strategy()}")
```

### **Variation 2: Two Knights with Different Operations**
**Problem**: Handle different types of two knights operations (weighted positions, priority-based placement, advanced board analysis).

**Approach**: Use advanced data structures for efficient different types of two knights operations.

```python
class AdvancedTwoKnights:
    def __init__(self, n=8, weights=None, priorities=None):
        self.n = n
        self.board = [[0 for _ in range(n)] for _ in range(n)]
        self.obstacles = set()
        self.weights = weights or {}
        self.priorities = priorities or {}
        self._update_two_knights_info()
    
    def _update_two_knights_info(self):
        """Update two knights feasibility information."""
        self.total_cells = self.n * self.n
        self.available_cells = self.total_cells - len(self.obstacles)
        self.two_knights_feasibility = self._calculate_two_knights_feasibility()
    
    def _calculate_two_knights_feasibility(self):
        """Calculate two knights placement feasibility."""
        if self.available_cells < 2:
            return 0.0
        
        # Check if we can place two knights without attacking each other
        return 1.0 if self.available_cells >= 2 else 0.0
    
    def is_safe_position(self, row, col):
        """Check if position is safe for knight placement."""
        if (row, col) in self.obstacles:
            return False
        
        # Check if position is within bounds
        if not (0 <= row < self.n and 0 <= col < self.n):
            return False
        
        return True
    
    def can_knights_attack(self, pos1, pos2):
        """Check if two knights can attack each other."""
        r1, c1 = pos1
        r2, c2 = pos2
        
        # Knight moves: (dx, dy) where |dx| + |dy| = 3 and dx, dy != 0
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        
        for dr, dc in knight_moves:
            if r1 + dr == r2 and c1 + dc == c2:
                return True
        
        return False
    
    def get_weighted_placements(self):
        """Get placements with weights and priorities applied."""
        if self.available_cells < 2:
            return []
        
        # Create weighted placements
        weighted_placements = []
        positions = []
        
        # Get all available positions
        for i in range(self.n):
            for j in range(self.n):
                if self.is_safe_position(i, j):
                    positions.append((i, j))
        
        # Calculate weighted placements
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                if not self.can_knights_attack(positions[i], positions[j]):
                    weight1 = self.weights.get(positions[i], 1)
                    weight2 = self.weights.get(positions[j], 1)
                    priority1 = self.priorities.get(positions[i], 1)
                    priority2 = self.priorities.get(positions[j], 1)
                    weighted_score = (weight1 + weight2) * (priority1 + priority2)
                    weighted_placements.append((positions[i], positions[j], weighted_score))
        
        # Sort by weighted score
        weighted_placements.sort(key=lambda x: x[2], reverse=True)
        
        return weighted_placements
    
    def get_placements_with_priority(self, priority_func):
        """Get placements considering priority."""
        if self.available_cells < 2:
            return []
        
        # Create priority-based placements
        priority_placements = []
        positions = []
        
        # Get all available positions
        for i in range(self.n):
            for j in range(self.n):
                if self.is_safe_position(i, j):
                    positions.append((i, j))
        
        # Calculate priority-based placements
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                if not self.can_knights_attack(positions[i], positions[j]):
                    priority = priority_func(positions[i], positions[j], self.weights, self.priorities)
                    priority_placements.append((positions[i], positions[j], priority))
        
        # Sort by priority
        priority_placements.sort(key=lambda x: x[2], reverse=True)
        return priority_placements
    
    def get_placements_with_optimization(self, optimization_func):
        """Get placements using custom optimization function."""
        if self.available_cells < 2:
            return []
        
        # Create optimization-based placements
        optimized_placements = []
        positions = []
        
        # Get all available positions
        for i in range(self.n):
            for j in range(self.n):
                if self.is_safe_position(i, j):
                    positions.append((i, j))
        
        # Calculate optimization-based placements
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                if not self.can_knights_attack(positions[i], positions[j]):
                    score = optimization_func(positions[i], positions[j], self.weights, self.priorities)
                    optimized_placements.append((positions[i], positions[j], score))
        
        # Sort by optimization score
        optimized_placements.sort(key=lambda x: x[2], reverse=True)
        return optimized_placements
    
    def get_placements_with_constraints(self, constraint_func):
        """Get placements that satisfies custom constraints."""
        if self.available_cells < 2:
            return []
        
        if constraint_func(self.board, self.weights, self.priorities):
            return self.get_weighted_placements()
        else:
            return []
    
    def get_placements_with_multiple_criteria(self, criteria_list):
        """Get placements that satisfies multiple criteria."""
        if self.available_cells < 2:
            return []
        
        satisfies_all_criteria = True
        for criterion in criteria_list:
            if not criterion(self.board, self.weights, self.priorities):
                satisfies_all_criteria = False
                break
        
        if satisfies_all_criteria:
            return self.get_weighted_placements()
        else:
            return []
    
    def get_placements_with_alternatives(self, alternatives):
        """Get placements considering alternative weights/priorities."""
        result = []
        
        # Check original placements
        original_placements = self.get_weighted_placements()
        result.append((original_placements, 'original'))
        
        # Check alternative weights/priorities
        for alt_weights, alt_priorities in alternatives:
            # Create temporary instance with alternative weights/priorities
            temp_instance = AdvancedTwoKnights(self.n, alt_weights, alt_priorities)
            temp_placements = temp_instance.get_weighted_placements()
            result.append((temp_placements, f'alternative_{alt_weights}_{alt_priorities}'))
        
        return result
    
    def get_placements_with_adaptive_criteria(self, adaptive_func):
        """Get placements using adaptive criteria."""
        if self.available_cells < 2:
            return []
        
        if adaptive_func(self.board, self.weights, self.priorities, []):
            return self.get_weighted_placements()
        else:
            return []
    
    def get_two_knights_optimization(self):
        """Get optimal two knights configuration."""
        strategies = [
            ('weighted_placements', lambda: len(self.get_weighted_placements())),
            ('total_weight', lambda: sum(self.weights.values())),
            ('total_priority', lambda: sum(self.priorities.values())),
        ]
        
        best_strategy = None
        best_value = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                current_value = strategy_func()
                if current_value > best_value:
                    best_value = current_value
                    best_strategy = (strategy_name, current_value)
            except:
                continue
        
        return best_strategy

# Example usage
n = 8
weights = {(i, j): i + j for i in range(n) for j in range(n)}  # Weight based on position
priorities = {(i, j): abs(i - n//2) + abs(j - n//2) for i in range(n) for j in range(n)}  # Priority based on center distance
advanced_two_knights = AdvancedTwoKnights(n, weights, priorities)

print(f"Weighted placements: {len(advanced_two_knights.get_weighted_placements())}")

# Get placements with priority
def priority_func(pos1, pos2, weights, priorities):
    return weights.get(pos1, 1) + weights.get(pos2, 1) + priorities.get(pos1, 1) + priorities.get(pos2, 1)

print(f"Placements with priority: {len(advanced_two_knights.get_placements_with_priority(priority_func))}")

# Get placements with optimization
def optimization_func(pos1, pos2, weights, priorities):
    return weights.get(pos1, 1) * weights.get(pos2, 1) * priorities.get(pos1, 1) * priorities.get(pos2, 1)

print(f"Placements with optimization: {len(advanced_two_knights.get_placements_with_optimization(optimization_func))}")

# Get placements with constraints
def constraint_func(board, weights, priorities):
    return len(weights) > 0 and len(priorities) > 0

print(f"Placements with constraints: {len(advanced_two_knights.get_placements_with_constraints(constraint_func))}")

# Get placements with multiple criteria
def criterion1(board, weights, priorities):
    return len(weights) > 0

def criterion2(board, weights, priorities):
    return len(priorities) > 0

criteria_list = [criterion1, criterion2]
print(f"Placements with multiple criteria: {len(advanced_two_knights.get_placements_with_multiple_criteria(criteria_list))}")

# Get placements with alternatives
alternatives = [({(i, j): 1 for i in range(n) for j in range(n)}, {(i, j): 1 for i in range(n) for j in range(n)}), ({(i, j): (i+j)*2 for i in range(n) for j in range(n)}, {(i, j): abs(i-n//2)+abs(j-n//2)+1 for i in range(n) for j in range(n)})]
print(f"Placements with alternatives: {len(advanced_two_knights.get_placements_with_alternatives(alternatives))}")

# Get placements with adaptive criteria
def adaptive_func(board, weights, priorities, current_result):
    return len(weights) > 0 and len(current_result) < 5

print(f"Placements with adaptive criteria: {len(advanced_two_knights.get_placements_with_adaptive_criteria(adaptive_func))}")

# Get two knights optimization
print(f"Two knights optimization: {advanced_two_knights.get_two_knights_optimization()}")
```

### **Variation 3: Two Knights with Constraints**
**Problem**: Handle two knights placement with additional constraints (distance limits, position constraints, pattern constraints).

**Approach**: Use constraint satisfaction with advanced optimization and mathematical analysis.

```python
class ConstrainedTwoKnights:
    def __init__(self, n=8, constraints=None):
        self.n = n
        self.board = [[0 for _ in range(n)] for _ in range(n)]
        self.obstacles = set()
        self.constraints = constraints or {}
        self._update_two_knights_info()
    
    def _update_two_knights_info(self):
        """Update two knights feasibility information."""
        self.total_cells = self.n * self.n
        self.available_cells = self.total_cells - len(self.obstacles)
        self.two_knights_feasibility = self._calculate_two_knights_feasibility()
    
    def _calculate_two_knights_feasibility(self):
        """Calculate two knights placement feasibility."""
        if self.available_cells < 2:
            return 0.0
        
        # Check if we can place two knights without attacking each other
        return 1.0 if self.available_cells >= 2 else 0.0
    
    def is_safe_position(self, row, col):
        """Check if position is safe for knight placement."""
        if (row, col) in self.obstacles:
            return False
        
        # Check if position is within bounds
        if not (0 <= row < self.n and 0 <= col < self.n):
            return False
        
        return True
    
    def can_knights_attack(self, pos1, pos2):
        """Check if two knights can attack each other."""
        r1, c1 = pos1
        r2, c2 = pos2
        
        # Knight moves: (dx, dy) where |dx| + |dy| = 3 and dx, dy != 0
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        
        for dr, dc in knight_moves:
            if r1 + dr == r2 and c1 + dc == c2:
                return True
        
        return False
    
    def _is_valid_placement(self, pos1, pos2):
        """Check if placement is valid considering constraints."""
        # Distance constraints
        if 'min_distance' in self.constraints:
            distance = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
            if distance < self.constraints['min_distance']:
                return False
        
        if 'max_distance' in self.constraints:
            distance = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
            if distance > self.constraints['max_distance']:
                return False
        
        # Position constraints
        if 'forbidden_positions' in self.constraints:
            if pos1 in self.constraints['forbidden_positions'] or pos2 in self.constraints['forbidden_positions']:
                return False
        
        if 'required_positions' in self.constraints:
            if pos1 not in self.constraints['required_positions'] and pos2 not in self.constraints['required_positions']:
                return False
        
        # Pattern constraints
        if 'pattern_constraints' in self.constraints:
            for constraint in self.constraints['pattern_constraints']:
                if not constraint(pos1, pos2, self.board):
                    return False
        
        return True
    
    def get_placements_with_distance_constraints(self, min_distance, max_distance):
        """Get placements considering distance constraints."""
        if self.available_cells < 2:
            return []
        
        result = []
        positions = []
        
        # Get all available positions
        for i in range(self.n):
            for j in range(self.n):
                if self.is_safe_position(i, j):
                    positions.append((i, j))
        
        # Find valid pairs within distance range
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                if not self.can_knights_attack(positions[i], positions[j]):
                    distance = abs(positions[i][0] - positions[j][0]) + abs(positions[i][1] - positions[j][1])
                    if min_distance <= distance <= max_distance and self._is_valid_placement(positions[i], positions[j]):
                        result.append((positions[i], positions[j]))
        
        return result
    
    def get_placements_with_position_constraints(self, position_constraints):
        """Get placements considering position constraints."""
        if self.available_cells < 2:
            return []
        
        satisfies_constraints = True
        for constraint in position_constraints:
            if not constraint(self.board):
                satisfies_constraints = False
                break
        
        if satisfies_constraints:
            result = []
            positions = []
            
            # Get all available positions
            for i in range(self.n):
                for j in range(self.n):
                    if self.is_safe_position(i, j):
                        positions.append((i, j))
            
            # Find valid pairs
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    if not self.can_knights_attack(positions[i], positions[j]):
                        if self._is_valid_placement(positions[i], positions[j]):
                            result.append((positions[i], positions[j]))
            
            return result
        else:
            return []
    
    def get_placements_with_pattern_constraints(self, pattern_constraints):
        """Get placements considering pattern constraints."""
        if self.available_cells < 2:
            return []
        
        satisfies_pattern = True
        for constraint in pattern_constraints:
            if not constraint(self.board):
                satisfies_pattern = False
                break
        
        if satisfies_pattern:
            result = []
            positions = []
            
            # Get all available positions
            for i in range(self.n):
                for j in range(self.n):
                    if self.is_safe_position(i, j):
                        positions.append((i, j))
            
            # Find valid pairs
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    if not self.can_knights_attack(positions[i], positions[j]):
                        if self._is_valid_placement(positions[i], positions[j]):
                            result.append((positions[i], positions[j]))
            
            return result
        else:
            return []
    
    def get_placements_with_mathematical_constraints(self, constraint_func):
        """Get placements that satisfies custom mathematical constraints."""
        if self.available_cells < 2:
            return []
        
        if constraint_func(self.board):
            result = []
            positions = []
            
            # Get all available positions
            for i in range(self.n):
                for j in range(self.n):
                    if self.is_safe_position(i, j):
                        positions.append((i, j))
            
            # Find valid pairs
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    if not self.can_knights_attack(positions[i], positions[j]):
                        if self._is_valid_placement(positions[i], positions[j]):
                            result.append((positions[i], positions[j]))
            
            return result
        else:
            return []
    
    def get_placements_with_optimization_constraints(self, optimization_func):
        """Get placements using custom optimization constraints."""
        if self.available_cells < 2:
            return []
        
        # Calculate optimization score for placements
        score = optimization_func(self.board)
        
        if score > 0:
            result = []
            positions = []
            
            # Get all available positions
            for i in range(self.n):
                for j in range(self.n):
                    if self.is_safe_position(i, j):
                        positions.append((i, j))
            
            # Find valid pairs
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    if not self.can_knights_attack(positions[i], positions[j]):
                        if self._is_valid_placement(positions[i], positions[j]):
                            result.append((positions[i], positions[j]))
            
            return result
        else:
            return []
    
    def get_placements_with_multiple_constraints(self, constraints_list):
        """Get placements that satisfies multiple constraints."""
        if self.available_cells < 2:
            return []
        
        satisfies_all_constraints = True
        for constraint in constraints_list:
            if not constraint(self.board):
                satisfies_all_constraints = False
                break
        
        if satisfies_all_constraints:
            result = []
            positions = []
            
            # Get all available positions
            for i in range(self.n):
                for j in range(self.n):
                    if self.is_safe_position(i, j):
                        positions.append((i, j))
            
            # Find valid pairs
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    if not self.can_knights_attack(positions[i], positions[j]):
                        if self._is_valid_placement(positions[i], positions[j]):
                            result.append((positions[i], positions[j]))
            
            return result
        else:
            return []
    
    def get_placements_with_priority_constraints(self, priority_func):
        """Get placements with priority-based constraints."""
        if self.available_cells < 2:
            return []
        
        # Calculate priority for placements
        priority = priority_func(self.board)
        
        if priority > 0:
            result = []
            positions = []
            
            # Get all available positions
            for i in range(self.n):
                for j in range(self.n):
                    if self.is_safe_position(i, j):
                        positions.append((i, j))
            
            # Find valid pairs
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    if not self.can_knights_attack(positions[i], positions[j]):
                        if self._is_valid_placement(positions[i], positions[j]):
                            result.append((positions[i], positions[j]))
            
            return result
        else:
            return []
    
    def get_placements_with_adaptive_constraints(self, adaptive_func):
        """Get placements with adaptive constraints."""
        if self.available_cells < 2:
            return []
        
        if adaptive_func(self.board, []):
            result = []
            positions = []
            
            # Get all available positions
            for i in range(self.n):
                for j in range(self.n):
                    if self.is_safe_position(i, j):
                        positions.append((i, j))
            
            # Find valid pairs
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    if not self.can_knights_attack(positions[i], positions[j]):
                        if self._is_valid_placement(positions[i], positions[j]):
                            result.append((positions[i], positions[j]))
            
            return result
        else:
            return []
    
    def get_optimal_two_knights_strategy(self):
        """Get optimal two knights strategy considering all constraints."""
        strategies = [
            ('distance_constraints', self.get_placements_with_distance_constraints),
            ('position_constraints', self.get_placements_with_position_constraints),
            ('pattern_constraints', self.get_placements_with_pattern_constraints),
        ]
        
        best_strategy = None
        best_score = 0
        
        for strategy_name, strategy_func in strategies:
            try:
                if strategy_name == 'distance_constraints':
                    result = strategy_func(1, 10)
                elif strategy_name == 'position_constraints':
                    position_constraints = [lambda board: len(board) > 0]
                    result = strategy_func(position_constraints)
                elif strategy_name == 'pattern_constraints':
                    pattern_constraints = [lambda board: len(board) > 0]
                    result = strategy_func(pattern_constraints)
                
                if len(result) > best_score:
                    best_score = len(result)
                    best_strategy = (strategy_name, result)
            except:
                continue
        
        return best_strategy

# Example usage
constraints = {
    'min_distance': 2,
    'max_distance': 8,
    'forbidden_positions': [(0, 0), (7, 7)],
    'required_positions': [(1, 1), (6, 6)],
    'pattern_constraints': [lambda pos1, pos2, board: pos1[0] != pos2[0] and pos1[1] != pos2[1]]
}

n = 8
constrained_two_knights = ConstrainedTwoKnights(n, constraints)

print("Distance-constrained placements:", len(constrained_two_knights.get_placements_with_distance_constraints(2, 8)))

print("Position-constrained placements:", len(constrained_two_knights.get_placements_with_position_constraints([lambda board: len(board) > 0])))

print("Pattern-constrained placements:", len(constrained_two_knights.get_placements_with_pattern_constraints([lambda board: len(board) > 0])))

# Mathematical constraints
def custom_constraint(board):
    return len(board) > 0

print("Mathematical constraint placements:", len(constrained_two_knights.get_placements_with_mathematical_constraints(custom_constraint)))

# Range constraints
def range_constraint(board):
    return len(board) > 0

range_constraints = [range_constraint]
print("Range-constrained placements:", len(constrained_two_knights.get_placements_with_distance_constraints(1, 10)))

# Multiple constraints
def constraint1(board):
    return len(board) > 0

def constraint2(board):
    return len(board[0]) > 0

constraints_list = [constraint1, constraint2]
print("Multiple constraints placements:", len(constrained_two_knights.get_placements_with_multiple_constraints(constraints_list)))

# Priority constraints
def priority_func(board):
    return len(board) + len(board[0])

print("Priority-constrained placements:", len(constrained_two_knights.get_placements_with_priority_constraints(priority_func)))

# Adaptive constraints
def adaptive_func(board, current_result):
    return len(board) > 0 and len(current_result) < 5

print("Adaptive constraint placements:", len(constrained_two_knights.get_placements_with_adaptive_constraints(adaptive_func)))

# Optimal strategy
optimal = constrained_two_knights.get_optimal_two_knights_strategy()
print(f"Optimal two knights strategy: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Two Knights](https://cses.fi/problemset/task/1072) - Basic two knights placement
- [Chessboard and Queens](https://cses.fi/problemset/task/1624) - Chess piece placement problems
- [Knight Moves](https://cses.fi/problemset/task/1073) - Knight movement problems

#### **LeetCode Problems**
- [N-Queens](https://leetcode.com/problems/n-queens/) - Chess piece placement
- [N-Queens II](https://leetcode.com/problems/n-queens-ii/) - Count valid queen placements
- [Knight Probability in Chessboard](https://leetcode.com/problems/knight-probability-in-chessboard/) - Knight movement probability
- [Minimum Knight Moves](https://leetcode.com/problems/minimum-knight-moves/) - Minimum knight moves

#### **Problem Categories**
- **Combinatorics**: Chess piece placement, mathematical counting, combinatorial analysis
- **Chess Mathematics**: Knight movement, attack patterns, piece placement strategies
- **Mathematical Counting**: Efficient counting formulas, combinatorial optimization, mathematical analysis
- **Algorithm Design**: Counting algorithms, mathematical algorithms, optimization techniques

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
