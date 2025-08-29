---
layout: simple
title: "Raab Game I"
permalink: /problem_soulutions/introductory_problems/raab_game_i_analysis
---

# Raab Game I

## Problem Description

**Problem**: In the Raab game, two players take turns removing stones from piles. Each player can remove 1, 2, or 3 stones from any pile. The player who cannot make a move loses. Determine if the first player can win given the initial pile configuration.

**Input**: 
- First line: n (number of piles)
- Second line: n integers (pile sizes)

**Output**: "FIRST" if first player can win, "SECOND" otherwise.

**Example**:
```
Input:
3
1 2 3

Output:
FIRST

Explanation: First player can win by removing 2 stones from pile 2, leaving piles [1,0,3].
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Two players take turns removing stones
- Each can remove 1, 2, or 3 stones from any pile
- Player who cannot move loses
- Determine if first player can force a win

**Key Observations:**
- This is a game theory problem
- We can use Grundy numbers (Nim game theory)
- Each pile has a Grundy number based on its size
- XOR of all Grundy numbers determines winner

### Step 2: Game Theory Analysis
**Idea**: Use Grundy numbers to determine winning strategy.

```python
def can_first_player_win_grundy(piles):
    nim_sum = 0
    
    # Calculate Grundy number for each pile
    for pile in piles:
        nim_sum ^= (pile % 4)
    
    # First player wins if nim sum is not zero
    return nim_sum != 0
```

**Why this works:**
- Grundy number for pile size n is n % 4
- Pattern repeats every 4 stones
- XOR of all Grundy numbers determines winner
- If nim sum ≠ 0, first player can force a win

### Step 3: Mathematical Analysis
**Idea**: Understand why Grundy number = n % 4.

```python
def understand_grundy_numbers():
    # Let's analyze why Grundy number = n % 4
    
    # Pile size 0: Grundy = 0 (terminal position)
    # Pile size 1: Grundy = 1 (can move to 0)
    # Pile size 2: Grundy = 2 (can move to 0 or 1)
    # Pile size 3: Grundy = 3 (can move to 0, 1, or 2)
    # Pile size 4: Grundy = 0 (can move to 1, 2, or 3, but opponent can counter)
    
    # Pattern repeats every 4 stones
    for i in range(10):
        grundy = i % 4
        print(f"Pile size {i}: Grundy = {grundy}")
```

**Why this pattern exists:**
- From pile size 4, any move can be countered by opponent
- This creates a cycle of length 4
- Hence Grundy number = n % 4

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_raab_game():
    n = int(input())
    piles = list(map(int, input().split()))
    
    # Calculate nim sum using Grundy numbers
    nim_sum = 0
    for pile in piles:
        nim_sum ^= (pile % 4)
    
    # First player wins if nim sum is not zero
    if nim_sum != 0:
        print("FIRST")
    else:
        print("SECOND")

# Main execution
if __name__ == "__main__":
    solve_raab_game()
```

**Why this works:**
- Efficient mathematical approach
- Uses game theory principles
- Handles all cases correctly

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ([1, 2, 3], "FIRST"),
        ([1, 1, 1], "FIRST"),
        ([2, 2, 2], "SECOND"),
        ([1], "FIRST"),
        ([4], "SECOND"),
    ]
    
    for piles, expected in test_cases:
        result = solve_test(piles)
        print(f"Piles: {piles}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(piles):
    nim_sum = 0
    for pile in piles:
        nim_sum ^= (pile % 4)
    
    return "FIRST" if nim_sum != 0 else "SECOND"

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - where n is number of piles
- **Space**: O(1) - constant space

### Why This Solution Works
- **Game Theory**: Uses Grundy numbers and nim sum
- **Mathematical**: Direct calculation using modulo
- **Correct**: Based on proven game theory principles

## 🎯 Key Insights

### 1. **Grundy Numbers**
- Each pile has a Grundy number based on its size
- For Raab game: Grundy number = pile_size % 4
- Pattern repeats every 4 stones

### 2. **Nim Sum**
- XOR of all Grundy numbers determines winner
- If nim sum ≠ 0, first player can force a win
- If nim sum = 0, second player can force a win

### 3. **Winning Strategy**
- If nim sum ≠ 0, make a move that leaves opponent with nim sum = 0
- This ensures opponent cannot force a win

## 🎯 Problem Variations

### Variation 1: Different Move Options
**Problem**: Players can remove 1, 2, 3, or 4 stones.

```python
def raab_game_extended(piles):
    # For moves 1,2,3,4, Grundy number = pile_size % 5
    nim_sum = 0
    for pile in piles:
        nim_sum ^= (pile % 5)
    
    return "FIRST" if nim_sum != 0 else "SECOND"
```

### Variation 2: Multiple Piles per Move
**Problem**: Players can remove stones from multiple piles in one move.

```python
def multi_pile_raab_game(piles):
    # This is more complex - need to analyze each possible move
    # For simplicity, assume players can remove from up to 2 piles
    
    def can_win(piles):
        if all(pile == 0 for pile in piles):
            return False
        
        # Try all possible moves
        for i in range(len(piles)):
            for stones in range(1, min(4, piles[i] + 1)):
                new_piles = piles.copy()
                new_piles[i] -= stones
                if not can_win(new_piles):
                    return True
        
        return False
    
    return "FIRST" if can_win(piles) else "SECOND"
```

### Variation 3: Weighted Stones
**Problem**: Each stone has a weight. Players want to maximize total weight collected.

```python
def weighted_raab_game(piles, weights):
    # weights[i][j] = weight of j-th stone in pile i
    # This becomes a more complex optimization problem
    
    def max_weight_difference(piles, weights, player):
        if all(pile == 0 for pile in piles):
            return 0
        
        if player == 1:  # First player
            max_diff = float('-inf')
            for i in range(len(piles)):
                for stones in range(1, min(4, piles[i] + 1)):
                    new_piles = piles.copy()
                    new_piles[i] -= stones
                    weight_gained = sum(weights[i][piles[i] - j - 1] for j in range(stones))
                    diff = weight_gained + max_weight_difference(new_piles, weights, 2)
                    max_diff = max(max_diff, diff)
            return max_diff
        else:  # Second player
            min_diff = float('inf')
            for i in range(len(piles)):
                for stones in range(1, min(4, piles[i] + 1)):
                    new_piles = piles.copy()
                    new_piles[i] -= stones
                    weight_gained = sum(weights[i][piles[i] - j - 1] for j in range(stones))
                    diff = weight_gained + max_weight_difference(new_piles, weights, 1)
                    min_diff = min(min_diff, diff)
            return min_diff
    
    diff = max_weight_difference(piles, weights, 1)
    return "FIRST" if diff > 0 else "SECOND"
```

### Variation 4: Constrained Moves
**Problem**: Players can only remove stones from piles with even/odd sizes.

```python
def constrained_raab_game(piles, constraint):
    # constraint = "even" or "odd"
    # Players can only remove from piles with even/odd sizes
    
    def can_win(piles, constraint):
        if all(pile == 0 for pile in piles):
            return False
        
        for i in range(len(piles)):
            # Check if pile satisfies constraint
            if constraint == "even" and piles[i] % 2 != 0:
                continue
            if constraint == "odd" and piles[i] % 2 != 1:
                continue
            
            for stones in range(1, min(4, piles[i] + 1)):
                new_piles = piles.copy()
                new_piles[i] -= stones
                if not can_win(new_piles, constraint):
                    return True
        
        return False
    
    return "FIRST" if can_win(piles, constraint) else "SECOND"
```

### Variation 5: Circular Piles
**Problem**: Piles are arranged in a circle, players can only remove from adjacent piles.

```python
def circular_raab_game(piles):
    # Piles are in a circle, can only remove from adjacent piles
    # This creates a more complex constraint
    
    def can_win(piles, last_move):
        if all(pile == 0 for pile in piles):
            return False
        
        for i in range(len(piles)):
            # Can only remove from piles adjacent to last move
            if last_move is not None:
                if i != (last_move - 1) % len(piles) and i != (last_move + 1) % len(piles):
                    continue
            
            for stones in range(1, min(4, piles[i] + 1)):
                new_piles = piles.copy()
                new_piles[i] -= stones
                if not can_win(new_piles, i):
                    return True
        
        return False
    
    return "FIRST" if can_win(piles, None) else "SECOND"
```

## 🔗 Related Problems

- **[Two Sets](/cses-analyses/problem_soulutions/introductory_problems/two_sets_analysis)**: Mathematical analysis problems
- **[Apple Division](/cses-analyses/problem_soulutions/introductory_problems/apple_division_analysis)**: Subset problems
- **[Coin Piles](/cses-analyses/problem_soulutions/introductory_problems/coin_piles_analysis)**: Mathematical problems

## 📚 Learning Points

1. **Game Theory**: Understanding Grundy numbers and nim sum
2. **Mathematical Patterns**: Recognizing repeating patterns
3. **Optimal Strategy**: Finding winning strategies
4. **Modular Arithmetic**: Using modulo for pattern recognition

---

**This is a great introduction to game theory and mathematical patterns!** 🎯