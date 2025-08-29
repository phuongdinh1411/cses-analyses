---
layout: simple
title: "Raab Game I Analysis"
permalink: /problem_soulutions/introductory_problems/raab_game_i_analysis
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
```python
def can_first_player_win(piles):
    nim_sum = 0
    
    # Calculate Grundy number for each pile
    for pile in piles:
        nim_sum ^= (pile % 4)
    
    # First player wins if nim sum is not zero
    return nim_sum != 0
```

### Method 2: Dynamic Programming
```python
class RaabGame:
    def __init__(self):
        self.grundy = []
    
    def precompute_grundy(self, max_pile):
        self.grundy = [0] * (max_pile + 1)
        
        for i in range(1, max_pile + 1):
            mex_values = set()
            
            # Try all possible moves
            for stones in range(1, min(4, i + 1)):
                mex_values.add(self.grundy[i - stones])
            
            # Calculate MEX
            self.grundy[i] = 0
            while self.grundy[i] in mex_values:
                self.grundy[i] += 1
    
    def can_win(self, piles):
        max_pile = max(piles)
        self.precompute_grundy(max_pile)
        
        nim_sum = 0
        for pile in piles:
            nim_sum ^= self.grundy[pile]
        
        return nim_sum != 0
```

### Method 3: Mathematical Analysis
```python
def can_first_player_win_math(piles):
    # For Raab game, Grundy number = pile_size % 4
    # This is because:
    # - Pile size 0: Grundy = 0 (terminal position)
    # - Pile size 1: Grundy = 1 (can move to 0)
    # - Pile size 2: Grundy = 2 (can move to 0 or 1)
    # - Pile size 3: Grundy = 3 (can move to 0, 1, or 2)
    # - Pile size 4: Grundy = 0 (can move to 1, 2, or 3, but opponent can counter)
    
    nim_sum = 0
    for pile in piles:
        nim_sum ^= (pile % 4)
    
    return nim_sum != 0
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
```python
def fast_grundy(pile_size, max_move):
    # For standard Raab game (max_move = 3)
    return pile_size % (max_move + 1)

def fast_grundy_general(pile_size, max_move):
    # For general case
    if pile_size == 0:
        return 0
    if pile_size <= max_move:
        return pile_size
    return pile_size % (max_move + 1)
```

### 2. Winning Move Finder
```python
def find_winning_moves(piles):
    moves = []  # (pile_index, stones_to_remove)
    
    nim_sum = 0
    for pile in piles:
        nim_sum ^= (pile % 4)
    
    if nim_sum == 0:
        return moves  # No winning moves
    
    # Find moves that make nim sum zero
    for i in range(len(piles)):
        current_grundy = piles[i] % 4
        target_grundy = nim_sum ^ current_grundy
        
        if target_grundy < current_grundy:
            stones_to_remove = current_grundy - target_grundy
            if stones_to_remove <= 3 and stones_to_remove <= piles[i]:
                moves.append((i, stones_to_remove))
    
    return moves
```

### 3. State Compression
```python
class CompressedRaabGame:
    def __init__(self):
        self.memo = {}
    
    def can_win_compressed(self, piles):
        # Sort piles for state compression
        piles_tuple = tuple(sorted(piles))
        
        if piles_tuple in self.memo:
            return self.memo[piles_tuple]
        
        # Calculate nim sum
        nim_sum = 0
        for pile in piles:
            nim_sum ^= (pile % 4)
        
        result = (nim_sum != 0)
        self.memo[piles_tuple] = result
        return result
```

## Related Problems
- [Two Sets](/cses-analyses/problem_soulutions/two_sets_analysis/)
- [Coin Piles](/cses-analyses/problem_soulutions/coin_piles_analysis/)
- [Apple Division](/cses-analyses/problem_soulutions/apple_division_analysis/)

## Practice Problems
1. ****: Raab Game I
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