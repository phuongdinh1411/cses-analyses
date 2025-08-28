---
layout: simple
title: Grid Path Description Analysis
permalink: /problem_soulutions/introductory_problems/grid_path_description_analysis/
---

# Grid Path Description Analysis

## Problem Description

Given a grid path description (string of 'R', 'D', 'L', 'U' for right, down, left, up), find the number of different paths that can be described by this string when starting from the top-left corner of an n×n grid.

## Key Insights

### 1. Path Validation
- Check if the path stays within grid boundaries
- Ensure 0 ≤ x, y < n at each step
- Count only valid paths that don't go out of bounds

### 2. Movement Mapping
- 'R': (x, y) → (x+1, y)
- 'D': (x, y) → (x, y+1)
- 'L': (x, y) → (x-1, y)
- 'U': (x, y) → (x, y-1)

### 3. Dynamic Programming
- Use DP to count valid paths
- State: (position, current index in string)
- Transition: try each possible direction

## Solution Approach

### Method 1: Recursive with Memoization
```cpp
class Solution {
private:
    vector<vector<vector<long long>>> dp;
    string path;
    int n;
    
    long long solve(int x, int y, int idx) {
        if (idx == path.length()) {
            return 1;
        }
        
        if (dp[x][y][idx] != -1) {
            return dp[x][y][idx];
        }
        
        long long count = 0;
        char dir = path[idx];
        
        if (dir == 'R' && x + 1 < n) {
            count += solve(x + 1, y, idx + 1);
        }
        if (dir == 'D' && y + 1 < n) {
            count += solve(x, y + 1, idx + 1);
        }
        if (dir == 'L' && x - 1 >= 0) {
            count += solve(x - 1, y, idx + 1);
        }
        if (dir == 'U' && y - 1 >= 0) {
            count += solve(x, y - 1, idx + 1);
        }
        
        return dp[x][y][idx] = count;
    }
    
public:
    long long countPaths(string path_desc, int grid_size) {
        path = path_desc;
        n = grid_size;
        dp.assign(n, vector<vector<long long>>(n, vector<long long>(path.length(), -1)));
        
        return solve(0, 0, 0);
    }
};
```

### Method 2: Iterative DP
```cpp
long long countPathsIterative(string path, int n) {
    vector<vector<vector<long long>>> dp(n, vector<vector<long long>>(n, vector<long long>(path.length() + 1, 0)));
    
    dp[0][0][0] = 1;
    
    for (int idx = 0; idx < path.length(); idx++) {
        for (int x = 0; x < n; x++) {
            for (int y = 0; y < n; y++) {
                if (dp[x][y][idx] == 0) continue;
                
                char dir = path[idx];
                
                if (dir == 'R' && x + 1 < n) {
                    dp[x + 1][y][idx + 1] += dp[x][y][idx];
                }
                if (dir == 'D' && y + 1 < n) {
                    dp[x][y + 1][idx + 1] += dp[x][y][idx];
                }
                if (dir == 'L' && x - 1 >= 0) {
                    dp[x - 1][y][idx + 1] += dp[x][y][idx];
                }
                if (dir == 'U' && y - 1 >= 0) {
                    dp[x][y - 1][idx + 1] += dp[x][y][idx];
                }
            }
        }
    }
    
    return dp[0][0][path.length()];
}
```

## Time Complexity
- **Time**: O(n² × len(path)) - for each position and path index
- **Space**: O(n² × len(path)) - DP table

## Example Walkthrough

**Input**: path = "RDD", n = 3

**Process**:
1. Start at (0, 0)
2. After 'R': (1, 0)
3. After 'D': (1, 1)
4. After 'D': (1, 2) - valid path

**Alternative paths**:
- (0,0) → (1,0) → (1,1) → (2,1) - invalid (out of bounds)
- (0,0) → (1,0) → (1,1) → (0,1) - invalid (out of bounds)

**Output**: 1 (only one valid path)

## Problem Variations

### Variation 1: Multiple Paths
**Problem**: Find all valid paths that match the description.

**Approach**: Use backtracking to generate all paths.

### Variation 2: Weighted Grid
**Problem**: Each cell has a weight. Find path with maximum/minimum weight.

**Approach**: Modify DP to track path weights.

### Variation 3: Constrained Movement
**Problem**: Some directions are forbidden at certain positions.

**Solution**: Add constraints to movement validation.

### Variation 4: Cyclic Grid
**Problem**: Grid wraps around edges (toroidal).

**Approach**: Use modulo arithmetic for boundary checking.

### Variation 5: Path Optimization
**Problem**: Find shortest/longest valid path matching description.

**Approach**: Use BFS or modified DP for path length.

### Variation 6: Probability Paths
**Problem**: Each direction has a probability. Find expected number of valid paths.

**Approach**: Use probability DP with expected values.

## Advanced Optimizations

### 1. State Compression
```cpp
long long countPathsCompressed(string path, int n) {
    vector<vector<long long>> dp(n, vector<long long>(n, 0));
    dp[0][0] = 1;
    
    for (char dir : path) {
        vector<vector<long long>> new_dp(n, vector<long long>(n, 0));
        
        for (int x = 0; x < n; x++) {
            for (int y = 0; y < n; y++) {
                if (dp[x][y] == 0) continue;
                
                // Apply direction
                int nx = x, ny = y;
                if (dir == 'R') nx++;
                else if (dir == 'D') ny++;
                else if (dir == 'L') nx--;
                else if (dir == 'U') ny--;
                
                if (nx >= 0 && nx < n && ny >= 0 && ny < n) {
                    new_dp[nx][ny] += dp[x][y];
                }
            }
        }
        dp = new_dp;
    }
    
    return dp[0][0];
}
```

### 2. Matrix Exponentiation
```cpp
// For repeated patterns, use matrix exponentiation
vector<vector<long long>> matrixMultiply(vector<vector<long long>>& a, vector<vector<long long>>& b, int n) {
    vector<vector<long long>> result(n, vector<long long>(n, 0));
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n; k++) {
                result[i][j] += a[i][k] * b[k][j];
            }
        }
    }
    
    return result;
}
```

## Related Problems
- [Grid Paths](../grid_paths_analysis/)
- [Knight Moves Grid](../knight_moves_grid_analysis/)
- [Two Knights](../two_knights_analysis/)

## Practice Problems
1. **CSES**: Grid Path Description
2. **LeetCode**: Similar path counting problems
3. **AtCoder**: Grid-based DP problems

## Key Takeaways
1. **Dynamic Programming** is essential for path counting
2. **Boundary checking** prevents invalid paths
3. **State representation** affects time and space complexity
4. **Memoization** can significantly improve performance
5. **Matrix operations** help with repeated patterns
6. **State compression** reduces memory usage
7. **Path validation** is crucial for correct counting
