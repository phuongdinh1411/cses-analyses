---
layout: simple
title: "Chessboard and Queens Analysis"
permalink: /problem_soulutions/introductory_problems/chessboard_and_queens_analysis
---


# Chessboard and Queens Analysis

## Problem Description

Place 8 queens on an 8×8 chessboard so that no two queens threaten each other. Some squares are blocked and cannot be used.

## Key Insights

### 1. Backtracking Approach
- Use recursive backtracking to try all valid queen placements
- For each row, try placing a queen in each valid column
- Check if the placement is valid (no conflicts with previous queens)

### 2. Conflict Detection
- **Row conflicts**: Only one queen per row (handled by placing one per row)
- **Column conflicts**: Check if column is already occupied
- **Diagonal conflicts**: Check both main diagonal and anti-diagonal
- **Blocked squares**: Cannot place queens on blocked squares

### 3. Optimization Techniques
- Use bit manipulation for faster conflict checking
- Early termination when no valid placement is possible
- Symmetry breaking for faster enumeration

## Solution Approach

```python
class Solution:
    def __init__(self):
        self.blocked = []
        self.col = []
        self.diag1 = []
        self.diag2 = []
        self.count = 0
    
    def backtrack(self, row):
        if row == 8:
            self.count += 1
            return
        
        for c in range(8):
            if self.blocked[row][c]:
                continue
            if self.col[c] or self.diag1[row + c] or self.diag2[row - c + 7]:
                continue
            
            self.col[c] = self.diag1[row + c] = self.diag2[row - c + 7] = True
            self.backtrack(row + 1)
            self.col[c] = self.diag1[row + c] = self.diag2[row - c + 7] = False
    
    def solve(self, blocked_squares):
        self.blocked = blocked_squares
        self.col = [False] * 8
        self.diag1 = [False] * 15  # row + col
        self.diag2 = [False] * 15  # row - col + 7
        self.count = 0
        self.backtrack(0)
        return self.count
```

## Time Complexity
- **Time**: O(8!) - in worst case, we try all permutations
- **Space**: O(8) - recursion depth + arrays for conflict checking

## Example Walkthrough

**Input**: 8×8 grid with some blocked squares
```
........
........
........
........
........
........
........
........
```

**Process**:
1. Place queen in row 0, column 0
2. Check conflicts for row 1
3. Continue until all 8 queens placed
4. Count valid configurations

## Problem Variations

### Variation 1: N-Queens Problem
**Problem**: Place N queens on N×N board without conflicts.

**Solution**: Same approach but with variable board size.

### Variation 2: Weighted Queens
**Problem**: Each square has a weight. Find placement with maximum total weight.

**Approach**: Modify backtracking to track current weight and update maximum.

### Variation 3: Minimum Queens
**Problem**: Find minimum queens needed to attack all squares.

**Approach**: Use greedy or dynamic programming approach.

### Variation 4: Queens with Constraints
**Problem**: Queens can only move in certain directions or have limited range.

**Approach**: Modify conflict detection based on new rules.

### Variation 5: Multiple Piece Types
**Problem**: Place queens, rooks, bishops, and knights without conflicts.

**Approach**: Track different piece types and their movement patterns.

## Advanced Optimizations

### 1. Bit Manipulation
```python
def backtrack(self, row, col_mask, diag1_mask, diag2_mask):
    if row == 8:
        self.count += 1
        return
    
    available = ((1 << 8) - 1) & ~col_mask & ~diag1_mask & ~diag2_mask
    while available:
        col = (available & -available).bit_length() - 1  # Get least significant bit
        if not self.blocked[row][col]:
            self.backtrack(row + 1, 
                          col_mask | (1 << col),
                          (diag1_mask | (1 << (row + col))) << 1,
                          (diag2_mask | (1 << (row - col + 7))) << 1)
        available &= available - 1
```

### 2. Symmetry Breaking
- Use rotational and reflectional symmetries
- Only count unique configurations up to symmetry

### 3. Constraint Propagation
- Use advanced constraint satisfaction techniques
- Forward checking and arc consistency

## Related Problems
- [Permutations](../permutations_analysis/)
- [Creating Strings](../creating_strings_analysis/)
- [Two Knights](../two_knights_analysis/)

## Practice Problems
1. ****: Chessboard and Queens
2. **LeetCode**: N-Queens, N-Queens II
3. **AtCoder**: Similar backtracking problems

## Key Takeaways
1. **Backtracking** is essential for constraint satisfaction problems
2. **Conflict detection** must be efficient for good performance
3. **Bit manipulation** can significantly speed up operations
4. **Symmetry** can be exploited to reduce search space
5. **Early termination** is crucial for performance
6. **State representation** affects both time and space complexity