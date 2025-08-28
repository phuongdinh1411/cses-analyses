---
layout: simple
title: Raab Game I Analysis
permalink: /problem_soulutions/introductory_problems/raab_game_i_analysis/
---

# Raab Game I Analysis

## Problem Description

In the Raab game, two players take turns removing stones from piles. Each player can remove 1, 2, or 3 stones from any pile. The player who cannot make a move loses. Determine if the first player can win given the initial pile configuration.

## Key Insights

### 1. Game Theory Analysis
- **Grundy Numbers**: Each pile has a Grundy number based on its size
- **Nim Sum**: XOR of all Grundy numbers determines winner
- **Winning Strategy**: First player wins if nim sum ≠ 0

### 2. Grundy Number Pattern
- For pile size n, Grundy number = n % 4
- Pattern repeats every 4 stones
- This is because any move can be countered by opponent

### 3. Optimal Strategy
- If nim sum ≠ 0, first player can always force a win
- If nim sum = 0, second player can always force a win
- Key is to leave opponent with nim sum = 0

## Solution Approach

### Method 1: Grundy Number Calculation
```cpp
bool canFirstPlayerWin(vector<int>& piles) {
    int nim_sum = 0;
    
    // Calculate Grundy number for each pile
    for (int pile : piles) {
        nim_sum ^= (pile % 4);
    }
    
    // First player wins if nim sum is not zero
    return nim_sum != 0;
}
```

### Method 2: Dynamic Programming
```cpp
class RaabGame {
private:
    vector<int> grundy;
    
    void precomputeGrundy(int max_pile) {
        grundy.assign(max_pile + 1, 0);
        
        for (int i = 1; i <= max_pile; i++) {
            set<int> mex_values;
            
            // Try all possible moves
            for (int stones = 1; stones <= min(3, i); stones++) {
                mex_values.insert(grundy[i - stones]);
            }
            
            // Calculate MEX
            grundy[i] = 0;
            while (mex_values.count(grundy[i])) {
                grundy[i]++;
            }
        }
    }
    
public:
    bool canWin(vector<int>& piles) {
        int max_pile = *max_element(piles.begin(), piles.end());
        precomputeGrundy(max_pile);
        
        int nim_sum = 0;
        for (int pile : piles) {
            nim_sum ^= grundy[pile];
        }
        
        return nim_sum != 0;
    }
};
```

### Method 3: Mathematical Analysis
```cpp
bool canFirstPlayerWinMath(vector<int>& piles) {
    // For Raab game, Grundy number = pile_size % 4
    // This is because:
    // - Pile size 0: Grundy = 0 (terminal position)
    // - Pile size 1: Grundy = 1 (can move to 0)
    // - Pile size 2: Grundy = 2 (can move to 0 or 1)
    // - Pile size 3: Grundy = 3 (can move to 0, 1, or 2)
    // - Pile size 4: Grundy = 0 (can move to 1, 2, or 3, but opponent can counter)
    
    int nim_sum = 0;
    for (int pile : piles) {
        nim_sum ^= (pile % 4);
    }
    
    return nim_sum != 0;
}
```

## Time Complexity
- **Method 1**: O(n) - where n is number of piles
- **Method 2**: O(max_pile + n) - precomputation + calculation
- **Method 3**: O(n) - direct mathematical calculation

## Example Walkthrough

**Input**: piles = [3, 4, 5]

**Process**:
1. Calculate Grundy numbers: 3%4=3, 4%4=0, 5%4=1
2. Calculate nim sum: 3 ^ 0 ^ 1 = 2
3. Since nim sum ≠ 0, first player can win

**Output**: true

## Problem Variations

### Variation 1: Different Move Options
**Problem**: Players can remove 1 to k stones.

**Solution**: Grundy number = pile_size % (k + 1).

### Variation 2: Multiple Piles per Move
**Problem**: Players can remove stones from multiple piles.

**Approach**: Use more complex Grundy number calculations.

### Variation 3: Constrained Moves
**Problem**: Cannot remove same number of stones twice in a row.

**Solution**: Track last move in state representation.

### Variation 4: Weighted Stones
**Problem**: Each stone has a weight. Find minimum weight removal.

**Approach**: Use dynamic programming with weight tracking.

### Variation 5: Circular Piles
**Problem**: Piles are arranged in a circle with adjacency constraints.

**Solution**: Use graph theory and cycle analysis.

### Variation 6: Probabilistic Moves
**Problem**: Each move has a probability of success.

**Approach**: Use probability theory and expected values.

## Advanced Optimizations

### 1. Fast Grundy Calculation
```cpp
int fastGrundy(int pile_size, int max_move) {
    // For standard Raab game (max_move = 3)
    return pile_size % (max_move + 1);
}

int fastGrundyGeneral(int pile_size, int max_move) {
    // For general case
    if (pile_size == 0) return 0;
    if (pile_size <= max_move) return pile_size;
    return pile_size % (max_move + 1);
}
```

### 2. Winning Move Finder
```cpp
vector<pair<int, int>> findWinningMoves(vector<int>& piles) {
    vector<pair<int, int>> moves; // (pile_index, stones_to_remove)
    
    int nim_sum = 0;
    for (int pile : piles) {
        nim_sum ^= (pile % 4);
    }
    
    if (nim_sum == 0) return moves; // No winning moves
    
    // Find moves that make nim sum zero
    for (int i = 0; i < piles.size(); i++) {
        int current_grundy = piles[i] % 4;
        int target_grundy = nim_sum ^ current_grundy;
        
        if (target_grundy < current_grundy) {
            int stones_to_remove = current_grundy - target_grundy;
            if (stones_to_remove <= 3 && stones_to_remove <= piles[i]) {
                moves.push_back({i, stones_to_remove});
            }
        }
    }
    
    return moves;
}
```

### 3. State Compression
```cpp
class CompressedRaabGame {
private:
    map<vector<int>, bool> memo;
    
    bool canWinCompressed(vector<int>& piles) {
        // Sort piles for state compression
        sort(piles.begin(), piles.end());
        
        if (memo.count(piles)) {
            return memo[piles];
        }
        
        // Calculate nim sum
        int nim_sum = 0;
        for (int pile : piles) {
            nim_sum ^= (pile % 4);
        }
        
        bool result = (nim_sum != 0);
        memo[piles] = result;
        return result;
    }
};
```

## Related Problems
- [Two Sets](../two_sets_analysis/)
- [Coin Piles](../coin_piles_analysis/)
- [Apple Division](../apple_division_analysis/)

## Practice Problems
1. **CSES**: Raab Game I
2. **AtCoder**: Similar game theory problems
3. **Codeforces**: Nim game variations

## Key Takeaways
1. **Grundy numbers** are essential for impartial games
2. **Nim sum** determines the winner
3. **Mathematical patterns** can simplify calculations
4. **State compression** helps with memoization
5. **Winning strategy** involves leaving opponent with nim sum = 0
6. **Pattern recognition** is crucial for game theory
7. **Edge cases** like empty piles need special handling
