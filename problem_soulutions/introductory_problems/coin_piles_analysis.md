---
layout: simple
title: "Coin Piles"
permalink: /problem_soulutions/introductory_problems/coin_piles_analysis
---

# Coin Piles

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand mathematical modeling and constraint satisfaction problems
- Apply linear algebra and system of equations to solve constraint problems
- Implement efficient mathematical solution algorithms with proper constraint validation
- Optimize mathematical problems using algebraic manipulation and constraint analysis
- Handle edge cases in mathematical problems (large numbers, impossible constraints, boundary conditions)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Mathematical modeling, constraint satisfaction, linear algebra, system of equations
- **Data Structures**: Basic arithmetic operations, constraint tracking, mathematical calculations
- **Mathematical Concepts**: Linear algebra, system of equations, constraint satisfaction, modular arithmetic
- **Programming Skills**: Mathematical calculations, constraint validation, algorithm implementation
- **Related Problems**: Mathematical problems, Constraint satisfaction, Linear algebra, System of equations

## Problem Description

**Problem**: You have two coin piles containing a and b coins. On each move, you can either remove 1 coin from the left pile and 2 coins from the right pile, or remove 2 coins from the left pile and 1 coin from the right pile. Determine if it's possible to empty both piles.

**Input**: 
- First line: t (number of test cases)
- Next t lines: two integers a and b (1 ≤ a, b ≤ 10⁹)

**Output**: For each test case, print "YES" if possible, "NO" otherwise.

**Example**:
```
Input:
3
2 1
2 2
3 3

Output:
NO
YES
YES
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Start with two piles: a coins in left, b coins in right
- Each move: remove (1,2) or (2,1) coins from (left, right)
- Goal: empty both piles completely
- Determine if this is possible

**Key Observations:**
- Each move removes exactly 3 coins total (1+2 or 2+1)
- Total coins removed must be divisible by 3
- We need to find if we can reach (0,0) from (a,b)

### Step 2: Mathematical Analysis
**Idea**: Analyze the conditions mathematically.

**Key Insights:**
- Total coins = a + b must be divisible by 3
- After each move: (a-1, b-2) or (a-2, b-1)
- We need to reach (0,0)
- This means we need moves that can reduce both piles to 0

**Conditions for possibility:**
1. (a + b) % 3 == 0 (total divisible by 3)
2. Both a and b must be reachable by the moves

### Step 3: Finding the Pattern
**Idea**: Let's see what moves we can make.

**Move Analysis:**
- Move 1: (a-1, b-2)
- Move 2: (a-2, b-1)

**Key Insight:**
- If we make x moves of type 1 and y moves of type 2
- Final state: (a - x - 2y, b - 2x - y)
- We need: a - x - 2y = 0 and b - 2x - y = 0

**Solving the equations:**
- a = x + 2y
- b = 2x + y
- Adding: a + b = 3x + 3y = 3(x + y)
- So (a + b) must be divisible by 3

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_coin_piles():
    t = int(input())
    
    for _ in range(t):
        a, b = map(int, input().split())
        
        # Check if total is divisible by 3
        if (a + b) % 3 != 0:
            print("NO")
            continue
        
        # Check if both piles can be emptied
        # We need: a ≤ 2b and b ≤ 2a
        if a > 2 * b or b > 2 * a:
            print("NO")
        else:
            print("YES")

# Main execution
if __name__ == "__main__":
    solve_coin_piles()
```

**Why this works:**
- If total not divisible by 3, impossible
- If one pile is more than twice the other, impossible
- Otherwise, it's possible to empty both

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (2, 1, False),   # Total=3, but 2 > 2*1
        (2, 2, True),    # Total=4, not divisible by 3
        (3, 3, True),    # Total=6, both ≤ 2*other
        (1, 1, False),   # Total=2, not divisible by 3
        (4, 2, True),    # Total=6, both ≤ 2*other
    ]
    
    for a, b, expected in test_cases:
        result = solve_test(a, b)
        print(f"a={a}, b={b}")
        print(f"Expected: {'YES' if expected else 'NO'}")
        print(f"Got: {result}")
        print(f"{'✓ PASS' if result == ('YES' if expected else 'NO') else '✗ FAIL'}")
        print()

def solve_test(a, b):
    if (a + b) % 3 != 0:
        return "NO"
    if a > 2 * b or b > 2 * a:
        return "NO"
    return "YES"

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Per Test Case**: O(1) - just a few arithmetic operations
- **Total**: O(t) where t is number of test cases

### Space Complexity
- O(1) - we only use a few variables

### Why This Solution Works
- **Mathematical**: Based on solving the system of equations
- **Complete**: Handles all possible cases
- **Efficient**: Constant time per test case

## 🎨 Visual Example

### Input Example
```
3 test cases:
Case 1: a=2, b=1
Case 2: a=2, b=2  
Case 3: a=3, b=3
```

### Move Types
```
Two possible moves:
Move Type 1: Remove 1 from left, 2 from right
Move Type 2: Remove 2 from left, 1 from right

Each move removes exactly 3 coins total.
```

### Case Analysis
```
Case 1: a=2, b=1
Initial: [2, 1]
Total coins: 2 + 1 = 3 ✓ (divisible by 3)

Try Move Type 1: [2-1, 1-2] = [1, -1] ✗ (negative coins)
Try Move Type 2: [2-2, 1-1] = [0, 0] ✓

Result: YES (possible with 1 move of type 2)

Case 2: a=2, b=2
Initial: [2, 2]
Total coins: 2 + 2 = 4 ✗ (not divisible by 3)

Result: NO (impossible)

Case 3: a=3, b=3
Initial: [3, 3]
Total coins: 3 + 3 = 6 ✓ (divisible by 3)

Try Move Type 1: [3-1, 3-2] = [2, 1]
Then Move Type 2: [2-2, 1-1] = [0, 0] ✓

Result: YES (possible with 2 moves)
```

### Mathematical Analysis
```
Let x = number of moves of type (1,2)
Let y = number of moves of type (2,1)

System of equations:
a = x + 2y  (coins removed from left pile)
b = 2x + y  (coins removed from right pile)

Solving:
x = (2a - b) / 3
y = (2b - a) / 3

For valid solution:
- x ≥ 0 and y ≥ 0 (non-negative moves)
- x and y must be integers
```

### Constraint Verification
```
Constraint: No pile can be more than twice the other

Case 1: a=2, b=1
- 2 ≤ 2×1 ✓ (2 ≤ 2)
- 1 ≤ 2×2 ✓ (1 ≤ 4)

Case 2: a=2, b=2  
- 2 ≤ 2×2 ✓ (2 ≤ 4)
- 2 ≤ 2×2 ✓ (2 ≤ 4)

Case 3: a=3, b=3
- 3 ≤ 2×3 ✓ (3 ≤ 6)
- 3 ≤ 2×3 ✓ (3 ≤ 6)
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Mathematical    │ O(1)         │ O(1)         │ Solve        │
│                 │              │              │ equations    │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Simulation      │ O(a+b)       │ O(1)         │ Try all      │
│                 │              │              │ moves        │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ BFS             │ O(a+b)       │ O(a+b)       │ State        │
│                 │              │              │ exploration  │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **Total Divisibility**
- Each move removes 3 coins total
- So (a + b) must be divisible by 3

### 2. **Pile Size Constraints**
- No pile can be more than twice the other
- Otherwise, we can't empty both

### 3. **Mathematical Equations**
- Let x = moves of type (1,2)
- Let y = moves of type (2,1)
- Solve: a = x + 2y, b = 2x + y

## 🔗 Related Problems

- **[Two Sets](/cses-analyses/problem_soulutions/introductory_problems/two_sets_analysis)**: Division problems
- **[Apple Division](/cses-analyses/problem_soulutions/introductory_problems/apple_division_analysis)**: Optimization problems
- **[Increasing Array](/cses-analyses/problem_soulutions/introductory_problems/increasing_array_analysis)**: Array manipulation

## 🎯 Problem Variations

### Variation 1: Three Piles
**Problem**: You have three piles with a, b, c coins. Can you empty all three?

```python
def three_piles(a, b, c):
    # Each move removes 3 coins total
    total = a + b + c
    if total % 3 != 0:
        return False
    
    # Check if any pile is too large
    max_pile = max(a, b, c)
    if max_pile > (a + b + c) // 2:
        return False
    
    return True
```

### Variation 2: Different Move Types
**Problem**: You can remove (1,1,1) or (2,1,0) or (1,0,2) coins from piles.

```python
def different_moves(a, b, c):
    # More complex system of equations
    # Need to solve: a = x + 2y + z, b = x + y, c = x + 2z
    # Where x, y, z are non-negative integers
    pass
```

### Variation 3: Minimum Moves
**Problem**: Find the minimum number of moves to empty the piles.

```python
def minimum_moves(a, b, c):
    if not three_piles(a, b, c):
        return -1  # Impossible
    
    # Each move removes 3 coins
    return (a + b + c) // 3
```

### Variation 4: Weighted Coins
**Problem**: Each coin has a weight. Find minimum total weight removed.

```python
def weighted_coins(a, b, weights_a, weights_b):
    # Similar to original but track weights
    # Need to minimize total weight while emptying piles
    pass
```

## 📚 Learning Points

1. **Mathematical Analysis**: Converting problems to equations
2. **System of Equations**: Solving multiple constraints
3. **Divisibility**: Using modulo arithmetic
4. **Problem Constraints**: Understanding what makes solutions possible

---

**This is a great introduction to mathematical problem-solving!** 🎯
