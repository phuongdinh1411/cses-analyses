---
layout: simple
title: Grid Coloring I Analysis
permalink: /problem_soulutions/introductory_problems/grid_coloring_i_analysis/
---

# Grid Coloring I Analysis

## Problem Description

Given an n×n grid, color each cell with one of k colors such that no two adjacent cells (sharing an edge) have the same color. Find the number of valid colorings.

## Key Insights

### 1. Graph Coloring Problem
- Each cell is a vertex in the graph
- Adjacent cells are connected by edges
- Need to color vertices so no adjacent vertices have same color
- This is a classic graph coloring problem

### 2. Chromatic Number
- Minimum number of colors needed: 2 (for grid)
- Maximum number of colors: n² (each cell different color)
- For k colors, count all valid colorings

### 3. Dynamic Programming
- Use DP with state: (current position, color configuration)
- Track colors of cells that affect current cell
- Use bit manipulation for efficient state representation

## Solution Approach

### Method 1: Recursive with Memoization
```cpp
class Solution {
private:
    vector<vector<vector<long long>>> dp;
    int n, k;
    
    long long solve(int row, int col, int prev_colors) {
        if (row == n) return 1;
        if (col == n) return solve(row + 1, 0, 0);
        
        int state = (row * n + col) * k + prev_colors;
        if (dp[row][col][prev_colors] != -1) {
            return dp[row][col][prev_colors];
        }
        
        long long count = 0;
        
        // Try each color
        for (int color = 0; color < k; color++) {
            bool valid = true;
            
            // Check left neighbor
            if (col > 0 && ((prev_colors >> (col - 1)) & 1) == color) {
                valid = false;
            }
            
            // Check top neighbor
            if (row > 0 && ((prev_colors >> (n + col)) & 1) == color) {
                valid = false;
            }
            
            if (valid) {
                int new_prev = prev_colors;
                new_prev |= (color << col);
                count += solve(row, col + 1, new_prev);
            }
        }
        
        return dp[row][col][prev_colors] = count;
    }
    
public:
    long long countColorings(int grid_size, int num_colors) {
        n = grid_size;
        k = num_colors;
        dp.assign(n, vector<vector<long long>>(n, vector<long long>(1 << (2 * n), -1)));
        
        return solve(0, 0, 0);
    }
};
```

### Method 2: Iterative DP
```cpp
long long countColoringsIterative(int n, int k) {
    vector<vector<long long>> dp(n * n + 1, vector<long long>(1 << n, 0));
    dp[0][0] = 1;
    
    for (int pos = 0; pos < n * n; pos++) {
        int row = pos / n;
        int col = pos % n;
        
        for (int mask = 0; mask < (1 << n); mask++) {
            if (dp[pos][mask] == 0) continue;
            
            for (int color = 0; color < k; color++) {
                bool valid = true;
                
                // Check left neighbor
                if (col > 0 && ((mask >> (col - 1)) & 1) == color) {
                    valid = false;
                }
                
                // Check top neighbor (stored in different part of mask)
                if (row > 0 && ((mask >> (n + col)) & 1) == color) {
                    valid = false;
                }
                
                if (valid) {
                    int new_mask = mask;
                    new_mask |= (color << col);
                    dp[pos + 1][new_mask] += dp[pos][mask];
                }
            }
        }
    }
    
    return dp[n * n][0];
}
```

## Time Complexity
- **Time**: O(n² × k × 2^n) - for each position, color, and state
- **Space**: O(n² × 2^n) - DP table

## Example Walkthrough

**Input**: n = 2, k = 3

**Process**:
1. Start with empty grid
2. Color (0,0) with color 0
3. Color (0,1) with color 1 (different from left)
4. Color (1,0) with color 1 (different from top)
5. Color (1,1) with color 0 (different from left and top)

**Valid colorings**:
```
0 1    0 2    1 0    1 2    2 0    2 1
1 0    1 2    0 1    0 2    1 2    1 0
```

**Output**: 6 valid colorings

## Problem Variations

### Variation 1: Fixed Colors
**Problem**: Some cells have pre-assigned colors.

**Approach**: Modify DP to respect fixed colors.

### Variation 2: Weighted Coloring
**Problem**: Each color has a weight. Find minimum/maximum weight coloring.

**Approach**: Track total weight in DP state.

### Variation 3: Connectivity Constraints
**Problem**: Cells of same color must form connected components.

**Approach**: Use union-find to track connectivity.

### Variation 4: Circular Grid
**Problem**: Grid wraps around edges (toroidal).

**Solution**: Modify boundary checking for circular adjacency.

### Variation 5: Diagonal Constraints
**Problem**: Diagonal cells cannot have same color.

**Approach**: Add diagonal checking to validation.

### Variation 6: Color Frequency
**Problem**: Each color must appear exactly k times.

**Approach**: Track color frequencies in DP state.

## Advanced Optimizations

### 1. Symmetry Breaking
```cpp
long long countColoringsSymmetry(int n, int k) {
    // Use symmetry to reduce search space
    // Only consider canonical colorings
    vector<vector<long long>> dp(n * n + 1, vector<long long>(1 << n, 0));
    
    // Start with canonical first row
    for (int color = 0; color < k; color++) {
        dp[n][1 << color] = 1;
    }
    
    // Continue with rest of grid...
}
```

### 2. Inclusion-Exclusion
```cpp
long long countColoringsInclusionExclusion(int n, int k) {
    long long total = 1;
    for (int i = 0; i < n * n; i++) {
        total *= k;
    }
    
    // Subtract invalid colorings using inclusion-exclusion
    for (int mask = 1; mask < (1 << (n * n)); mask++) {
        // Count colorings violating edges in mask
        // Add/subtract based on parity
    }
    
    return total;
}
```

### 3. Matrix Tree Theorem
```cpp
// For special cases, use matrix tree theorem
// Count spanning trees in dual graph
long long countColoringsMatrixTree(int n, int k) {
    // Construct Laplacian matrix
    // Count spanning trees
    // Multiply by k^(number of components)
}
```

## Related Problems
- [Grid Coloring II](../grid_coloring_ii_analysis/)
- [Chessboard and Queens](../chessboard_and_queens_analysis/)
- [Two Knights](../two_knights_analysis/)

## Practice Problems
1. **CSES**: Grid Coloring I
2. **LeetCode**: Similar graph coloring problems
3. **AtCoder**: Constraint satisfaction problems

## Key Takeaways
1. **Graph coloring** is a fundamental algorithmic problem
2. **Dynamic Programming** with state compression is essential
3. **Bit manipulation** helps represent color configurations efficiently
4. **Symmetry breaking** can significantly reduce search space
5. **Inclusion-exclusion** provides alternative counting approach
6. **Matrix operations** help with special cases
7. **Constraint validation** must be carefully implemented
