---
layout: simple
title: "Raab Game II - Game Theory Problem"
permalink: /problem_soulutions/counting_problems/raab_game_ii_analysis
---

# Raab Game II - Game Theory Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of game theory in combinatorial problems
- Apply counting techniques for game analysis
- Implement efficient algorithms for game counting
- Optimize game calculations for large numbers
- Handle special cases in game theory counting

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Game theory, counting techniques, mathematical formulas
- **Data Structures**: Arrays, mathematical computations, game state representation
- **Mathematical Concepts**: Game theory, combinations, permutations, modular arithmetic
- **Programming Skills**: Mathematical computations, modular arithmetic, game state analysis
- **Related Problems**: Counting Permutations (combinatorics), Counting Combinations (combinatorics), Counting Sequences (combinatorics)

## 📋 Problem Description

Given a game with n positions and k moves, count the number of winning strategies.

**Input**: 
- n: number of positions
- k: number of moves

**Output**: 
- Number of winning strategies modulo 10^9+7

**Constraints**:
- 1 ≤ n, k ≤ 10^6
- Answer modulo 10^9+7

**Example**:
```
Input:
n = 3, k = 2

Output:
6

Explanation**: 
Winning strategies with 3 positions and 2 moves:
- Strategy 1: Position 1 → Position 2
- Strategy 2: Position 1 → Position 3
- Strategy 3: Position 2 → Position 1
- Strategy 4: Position 2 → Position 3
- Strategy 5: Position 3 → Position 1
- Strategy 6: Position 3 → Position 2
Total: 6 winning strategies
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Game Solution

**Key Insights from Recursive Game Solution**:
- **Recursive Approach**: Use recursion to explore all game states
- **Complete Enumeration**: Enumerate all possible game strategies
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: Exponential time complexity

**Key Insight**: Use recursion to explore all possible game strategies and count winning ones.

**Algorithm**:
- Use recursive function to explore game states
- Count all winning strategies
- Apply modulo operation to prevent overflow

**Visual Example**:
```
n = 3, k = 2

Recursive exploration:
┌─────────────────────────────────────┐
│ Start from any position:           │
│ - Position 1: can move to 2 or 3   │
│ - Position 2: can move to 1 or 3   │
│ - Position 3: can move to 1 or 2   │
│ Total strategies: 3 × 2 = 6        │
└─────────────────────────────────────┘

Strategy enumeration:
┌─────────────────────────────────────┐
│ 1→2, 1→3                          │
│ 2→1, 2→3                          │
│ 3→1, 3→2                          │
│ Total: 6 winning strategies        │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def recursive_game_count(n, k, mod=10**9+7):
    """
    Count winning strategies using recursive approach
    
    Args:
        n: number of positions
        k: number of moves
        mod: modulo value
    
    Returns:
        int: number of winning strategies modulo mod
    """
    def count_strategies(position, moves_left):
        """Count winning strategies recursively"""
        if moves_left == 0:
            return 1  # Winning strategy found
        
        count = 0
        for next_position in range(1, n + 1):
            if next_position != position:  # Can't stay in same position
                count = (count + count_strategies(next_position, moves_left - 1)) % mod
        
        return count
    
    total_count = 0
    for start_position in range(1, n + 1):
        total_count = (total_count + count_strategies(start_position, k)) % mod
    
    return total_count

def recursive_game_count_optimized(n, k, mod=10**9+7):
    """
    Optimized recursive game counting
    
    Args:
        n: number of positions
        k: number of moves
        mod: modulo value
    
    Returns:
        int: number of winning strategies modulo mod
    """
    def count_strategies_optimized(position, moves_left):
        """Count winning strategies with optimization"""
        if moves_left == 0:
            return 1  # Winning strategy found
        
        # Each position can move to (n-1) other positions
        return ((n - 1) * count_strategies_optimized(position, moves_left - 1)) % mod
    
    # Start from any position, result is the same
    return (n * count_strategies_optimized(1, k)) % mod

# Example usage
n, k = 3, 2
result1 = recursive_game_count(n, k)
result2 = recursive_game_count_optimized(n, k)
print(f"Recursive game count: {result1}")
print(f"Optimized recursive count: {result2}")
```

**Time Complexity**: O(n^k)
**Space Complexity**: O(k)

**Why it's inefficient**: Exponential time complexity due to complete enumeration.

---

### Approach 2: Mathematical Formula Solution

**Key Insights from Mathematical Formula Solution**:
- **Mathematical Formula**: Use n × (n-1)^k formula for game strategies
- **Direct Calculation**: Calculate result directly without enumeration
- **Efficient Computation**: O(log k) time complexity
- **Optimization**: Much more efficient than recursive approach

**Key Insight**: Use the mathematical formula that each position can move to (n-1) other positions.

**Algorithm**:
- Use formula: number of strategies = n × (n-1)^k
- Calculate (n-1)^k efficiently using modular exponentiation
- Apply modulo operation throughout

**Visual Example**:
```
Mathematical formula:
┌─────────────────────────────────────┐
│ For n positions and k moves:       │
│ - Start from any of n positions    │
│ - Each move: (n-1) choices         │
│ - Total: n × (n-1) × ... × (n-1)  │
│ - Total: n × (n-1)^k              │
└─────────────────────────────────────┘

Modular exponentiation:
┌─────────────────────────────────────┐
│ (n-1)^k mod mod = ((n-1) mod mod)^k mod mod │
│ Use binary exponentiation for efficiency     │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def mathematical_game_count(n, k, mod=10**9+7):
    """
    Count winning strategies using mathematical formula
    
    Args:
        n: number of positions
        k: number of moves
        mod: modulo value
    
    Returns:
        int: number of winning strategies modulo mod
    """
    def mod_pow(base, exp, mod):
        """Calculate base^exp mod mod efficiently"""
        result = 1
        base = base % mod
        
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            exp = exp >> 1
            base = (base * base) % mod
        
        return result
    
    # Number of strategies = n × (n-1)^k
    if n == 1:
        return 0  # No valid moves from single position
    
    return (n * mod_pow(n - 1, k, mod)) % mod

def mathematical_game_count_v2(n, k, mod=10**9+7):
    """
    Alternative mathematical approach using built-in pow
    
    Args:
        n: number of positions
        k: number of moves
        mod: modulo value
    
    Returns:
        int: number of winning strategies modulo mod
    """
    if n == 1:
        return 0  # No valid moves from single position
    
    # Use built-in pow with modular arithmetic
    return (n * pow(n - 1, k, mod)) % mod

# Example usage
n, k = 3, 2
result1 = mathematical_game_count(n, k)
result2 = mathematical_game_count_v2(n, k)
print(f"Mathematical game count: {result1}")
print(f"Mathematical game count v2: {result2}")
```

**Time Complexity**: O(log k)
**Space Complexity**: O(1)

**Why it's better**: Uses mathematical formula for O(log k) time complexity.

**Implementation Considerations**:
- **Mathematical Formula**: Use n × (n-1)^k formula for game strategies
- **Modular Exponentiation**: Use efficient modular exponentiation
- **Direct Calculation**: Calculate result directly without enumeration

---

### Approach 3: Advanced Mathematical Solution (Optimal)

**Key Insights from Advanced Mathematical Solution**:
- **Advanced Mathematics**: Use advanced mathematical properties
- **Efficient Computation**: O(log k) time complexity
- **Mathematical Optimization**: Use mathematical optimizations
- **Optimal Complexity**: Best approach for game strategy counting

**Key Insight**: Use advanced mathematical properties and optimizations for efficient game strategy counting.

**Algorithm**:
- Use advanced mathematical properties
- Apply mathematical optimizations
- Calculate result efficiently

**Visual Example**:
```
Advanced mathematical properties:
┌─────────────────────────────────────┐
│ For game strategies:               │
│ - Each position has (n-1) moves    │
│ - Total number = n × (n-1)^k      │
│ - Can be calculated efficiently    │
└─────────────────────────────────────┘

Mathematical optimizations:
┌─────────────────────────────────────┐
│ - Use modular exponentiation       │
│ - Apply mathematical properties    │
│ - Optimize for large numbers       │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_mathematical_game_count(n, k, mod=10**9+7):
    """
    Count winning strategies using advanced mathematical approach
    
    Args:
        n: number of positions
        k: number of moves
        mod: modulo value
    
    Returns:
        int: number of winning strategies modulo mod
    """
    def fast_mod_pow(base, exp, mod):
        """Fast modular exponentiation with optimizations"""
        if exp == 0:
            return 1
        if exp == 1:
            return base % mod
        
        # Use binary exponentiation
        result = 1
        base = base % mod
        
        while exp > 0:
            if exp & 1:  # If exp is odd
                result = (result * base) % mod
            exp = exp >> 1  # Divide exp by 2
            base = (base * base) % mod
        
        return result
    
    # Handle edge cases
    if n == 1:
        return 0  # No valid moves from single position
    if k == 0:
        return n  # All positions are winning with 0 moves
    
    # Number of strategies = n × (n-1)^k
    return (n * fast_mod_pow(n - 1, k, mod)) % mod

def optimized_game_count(n, k, mod=10**9+7):
    """
    Optimized game counting with additional optimizations
    
    Args:
        n: number of positions
        k: number of moves
        mod: modulo value
    
    Returns:
        int: number of winning strategies modulo mod
    """
    # Use built-in pow with optimizations
    if n == 1:
        return 0  # No valid moves from single position
    if k == 0:
        return n  # All positions are winning with 0 moves
    
    # For large k, use built-in pow which is highly optimized
    return (n * pow(n - 1, k, mod)) % mod

def game_count_with_precomputation(max_n, max_k, mod=10**9+7):
    """
    Precompute game counts for multiple queries
    
    Args:
        max_n: maximum value of n
        max_k: maximum value of k
        mod: modulo value
    
    Returns:
        list: precomputed game counts
    """
    results = [[0] * (max_k + 1) for _ in range(max_n + 1)]
    
    for i in range(max_n + 1):
        for j in range(max_k + 1):
            if i == 1:
                results[i][j] = 0  # No valid moves from single position
            elif j == 0:
                results[i][j] = i  # All positions are winning with 0 moves
            else:
                results[i][j] = (i * pow(i - 1, j, mod)) % mod
    
    return results

# Example usage
n, k = 3, 2
result1 = advanced_mathematical_game_count(n, k)
result2 = optimized_game_count(n, k)
print(f"Advanced mathematical game count: {result1}")
print(f"Optimized game count: {result2}")

# Precompute for multiple queries
max_n, max_k = 1000, 1000
precomputed = game_count_with_precomputation(max_n, max_k)
print(f"Precomputed result for n={n}, k={k}: {precomputed[n][k]}")
```

**Time Complexity**: O(log k)
**Space Complexity**: O(1)

**Why it's optimal**: Uses advanced mathematical properties for O(log k) time complexity.

**Implementation Details**:
- **Advanced Mathematics**: Use advanced mathematical properties
- **Efficient Computation**: Use optimized modular exponentiation
- **Mathematical Optimizations**: Apply mathematical optimizations
- **Precomputation**: Precompute results for multiple queries

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(n^k) | O(k) | Complete enumeration of all game strategies |
| Mathematical Formula | O(log k) | O(1) | Use n × (n-1)^k formula with modular exponentiation |
| Advanced Mathematical | O(log k) | O(1) | Use advanced mathematical properties and optimizations |

### Time Complexity
- **Time**: O(log k) - Use modular exponentiation for efficient calculation
- **Space**: O(1) - Use only necessary variables

### Why This Solution Works
- **Mathematical Formula**: Use n × (n-1)^k formula for game strategies
- **Modular Exponentiation**: Use efficient modular exponentiation
- **Mathematical Properties**: Leverage mathematical properties
- **Efficient Algorithms**: Use optimal algorithms for calculation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Game Count with Position Constraints**
**Problem**: Count winning strategies with position constraints.

**Key Differences**: Apply constraints to positions

**Solution Approach**: Modify counting formula to include constraints

**Implementation**:
```python
def constrained_game_count(n, k, constraints, mod=10**9+7):
    """
    Count winning strategies with position constraints
    
    Args:
        n: number of positions
        k: number of moves
        constraints: list of constraints for each position
        mod: modulo value
    
    Returns:
        int: number of constrained winning strategies modulo mod
    """
    def count_constrained_strategies(position, moves_left):
        """Count constrained winning strategies recursively"""
        if moves_left == 0:
            return 1  # Valid constrained strategy found
        
        count = 0
        for next_position in constraints[position - 1]:  # Only consider allowed positions
            if next_position != position:  # Can't stay in same position
                count = (count + count_constrained_strategies(next_position, moves_left - 1)) % mod
        
        return count
    
    total_count = 0
    for start_position in range(1, n + 1):
        total_count = (total_count + count_constrained_strategies(start_position, k)) % mod
    
    return total_count

def constrained_game_count_optimized(n, k, constraints, mod=10**9+7):
    """
    Optimized constrained game counting
    
    Args:
        n: number of positions
        k: number of moves
        constraints: list of constraints for each position
        mod: modulo value
    
    Returns:
        int: number of constrained winning strategies modulo mod
    """
    # Calculate total number of constrained strategies
    total = 0
    for i in range(n):
        total = (total + len(constraints[i])) % mod
    
    # Each move multiplies by average number of valid moves
    avg_moves = total // n
    return (n * pow(avg_moves, k, mod)) % mod

# Example usage
n, k = 3, 2
constraints = [
    [2, 3],  # Position 1 can move to positions 2 or 3
    [1, 3],  # Position 2 can move to positions 1 or 3
    [1, 2]   # Position 3 can move to positions 1 or 2
]
result1 = constrained_game_count(n, k, constraints)
result2 = constrained_game_count_optimized(n, k, constraints)
print(f"Constrained game count: {result1}")
print(f"Optimized constrained count: {result2}")
```

#### **2. Game Count with Move Constraints**
**Problem**: Count winning strategies with move constraints.

**Key Differences**: Apply constraints to moves

**Solution Approach**: Use dynamic programming with move constraints

**Implementation**:
```python
def move_constrained_game_count(n, k, move_constraints, mod=10**9+7):
    """
    Count winning strategies with move constraints
    
    Args:
        n: number of positions
        k: number of moves
        move_constraints: list of move constraints for each position
        mod: modulo value
    
    Returns:
        int: number of move-constrained winning strategies modulo mod
    """
    def count_move_constrained_strategies(position, moves_left):
        """Count move-constrained winning strategies"""
        if moves_left == 0:
            return 1  # Valid move-constrained strategy found
        
        count = 0
        for next_position in range(1, n + 1):
            if next_position != position:  # Can't stay in same position
                # Check if move is allowed
                if is_move_allowed(position, next_position, moves_left, move_constraints):
                    count = (count + count_move_constrained_strategies(next_position, moves_left - 1)) % mod
        
        return count
    
    def is_move_allowed(from_pos, to_pos, moves_left, constraints):
        """Check if move is allowed"""
        # Implement move constraint logic here
        return True  # Simplified for example
    
    total_count = 0
    for start_position in range(1, n + 1):
        total_count = (total_count + count_move_constrained_strategies(start_position, k)) % mod
    
    return total_count

# Example usage
n, k = 3, 2
move_constraints = []  # Define move constraints
result = move_constrained_game_count(n, k, move_constraints)
print(f"Move constrained game count: {result}")
```

#### **3. Game Count with Multiple Players**
**Problem**: Count winning strategies for multiple players.

**Key Differences**: Handle multiple players in the game

**Solution Approach**: Use multi-player game theory

**Implementation**:
```python
def multi_player_game_count(n, k, num_players, mod=10**9+7):
    """
    Count winning strategies for multiple players
    
    Args:
        n: number of positions
        k: number of moves
        num_players: number of players
        mod: modulo value
    
    Returns:
        int: number of multi-player winning strategies modulo mod
    """
    def count_multi_player_strategies(positions, moves_left):
        """Count multi-player winning strategies"""
        if moves_left == 0:
            return 1  # Valid multi-player strategy found
        
        count = 0
        for player in range(num_players):
            current_position = positions[player]
            for next_position in range(1, n + 1):
                if next_position != current_position:  # Can't stay in same position
                    new_positions = positions.copy()
                    new_positions[player] = next_position
                    count = (count + count_multi_player_strategies(new_positions, moves_left - 1)) % mod
        
        return count
    
    # Start with all players at different positions
    initial_positions = list(range(1, num_players + 1))
    return count_multi_player_strategies(initial_positions, k)

# Example usage
n, k = 3, 2
num_players = 2
result = multi_player_game_count(n, k, num_players)
print(f"Multi-player game count: {result}")
```

### Related Problems

#### **CSES Problems**
- [Counting Permutations](https://cses.fi/problemset/task/1075) - Combinatorics
- [Counting Combinations](https://cses.fi/problemset/task/1075) - Combinatorics
- [Counting Sequences](https://cses.fi/problemset/task/1075) - Combinatorics

#### **LeetCode Problems**
- [Nim Game](https://leetcode.com/problems/nim-game/) - Game theory
- [Can I Win](https://leetcode.com/problems/can-i-win/) - Game theory
- [Predict the Winner](https://leetcode.com/problems/predict-the-winner/) - Game theory

#### **Problem Categories**
- **Game Theory**: Mathematical games, strategy counting
- **Combinatorics**: Mathematical counting, game properties
- **Mathematical Algorithms**: Modular arithmetic, number theory

## 🔗 Additional Resources

### **Algorithm References**
- [Game Theory](https://cp-algorithms.com/game_theory/game_theory.html) - Game theory algorithms
- [Combinatorics](https://cp-algorithms.com/combinatorics/binomial-coefficients.html) - Counting techniques
- [Modular Arithmetic](https://cp-algorithms.com/algebra/module-inverse.html) - Modular arithmetic

### **Practice Problems**
- [CSES Counting Permutations](https://cses.fi/problemset/task/1075) - Medium
- [CSES Counting Combinations](https://cses.fi/problemset/task/1075) - Medium
- [CSES Counting Sequences](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Game Theory](https://en.wikipedia.org/wiki/Game_theory) - Wikipedia article
