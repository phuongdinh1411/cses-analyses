---
layout: simple
title: "Counting Bishops
permalink: /problem_soulutions/counting_problems/counting_bishops_analysis/
---

# Counting Bishops

## Problem Statement
Given a chessboard of size n×n, count the number of ways to place k bishops such that no bishop attacks another bishop.

### Input
The first input line has two integers n and k: the size of the chessboard and the number of bishops to place.

### Output
Print one integer: the number of ways to place k bishops.

### Constraints
- 1 ≤ n ≤ 8
- 0 ≤ k ≤ n²

### Example
```
Input:
3 2

Output:
26
```

## Solution Progression

### Approach 1: Generate All Placements - O(n^(n²))
**Description**: Generate all possible placements of k bishops and check if they are valid.

```python
def counting_bishops_naive(n, k):
    from itertools import combinations
    
    # Generate all positions on the board
    positions = [(i, j) for i in range(n) for j in range(n)]
    
    count = 0
    
    # Try all combinations of k positions
    for bishop_positions in combinations(positions, k):
        # Check if bishops can attack each other
        valid = True
        for i in range(k):
            for j in range(i + 1, k):
                r1, c1 = bishop_positions[i]
                r2, c2 = bishop_positions[j]
                
                # Check if bishops attack each other (same diagonal)
                if abs(r1 - r2) == abs(c1 - c2):
                    valid = False
                    break
            if not valid:
                break
        
        if valid:
            count += 1
    
    return count
```

**Why this is inefficient**: We need to check all possible combinations of positions, leading to exponential time complexity.

### Improvement 1: Backtracking with Diagonal Tracking - O(n!)
**Description**: Use backtracking to place bishops one by one with diagonal tracking.

```python
def counting_bishops_backtracking(n, k):
    def can_place_bishop(row, col, diagonals):
        # Check if position is on any occupied diagonal
        for d in diagonals:
            if abs(row - d[0]) == abs(col - d[1]):
                return False
        return True
    
    def backtrack(bishops, remaining, diagonals):
        if remaining == 0:
            return 1
        
        count = 0
        start_pos = 0 if not bishops else bishops[-1][0] * n + bishops[-1][1] + 1
        
        for pos in range(start_pos, n * n):
            row, col = pos // n, pos % n
            
            if can_place_bishop(row, col, diagonals):
                bishops.append((row, col))
                diagonals.append((row, col))
                count += backtrack(bishops, remaining - 1, diagonals)
                diagonals.pop()
                bishops.pop()
        
        return count
    
    return backtrack([], k, [])
```

**Why this improvement works**: Backtracking with diagonal tracking avoids checking invalid combinations early.

## Final Optimal Solution

```python
n, k = map(int, input().split())

def count_bishop_placements(n, k):
    def can_place_bishop(row, col, diagonals):
        # Check if position is on any occupied diagonal
        for d in diagonals:
            if abs(row - d[0]) == abs(col - d[1]):
                return False
        return True
    
    def backtrack(bishops, remaining, diagonals):
        if remaining == 0:
            return 1
        
        count = 0
        start_pos = 0 if not bishops else bishops[-1][0] * n + bishops[-1][1] + 1
        
        for pos in range(start_pos, n * n):
            row, col = pos // n, pos % n
            
            if can_place_bishop(row, col, diagonals):
                bishops.append((row, col))
                diagonals.append((row, col))
                count += backtrack(bishops, remaining - 1, diagonals)
                diagonals.pop()
                bishops.pop()
        
        return count
    
    return backtrack([], k, [])

result = count_bishop_placements(n, k)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(n^(n²)) | O(k) | Generate all combinations |
| Backtracking | O(n!) | O(k) | Use backtracking with diagonal tracking |

## Key Insights for Other Problems

### 1. **Chess Piece Placement Problems**
**Principle**: Use backtracking to place chess pieces with attack checking.
**Applicable to**: Chess problems, placement problems, constraint satisfaction problems

### 2. **Diagonal Attack Checking**
**Principle**: Check diagonal attacks using the distance formula.
**Applicable to**: Chess problems, geometric problems, pattern recognition

### 3. **Backtracking with Pruning**
**Principle**: Use backtracking to avoid checking invalid combinations early.
**Applicable to**: Search problems, optimization problems, constraint problems

## Notable Techniques

### 1. **Bishop Attack Check**
```python
def can_place_bishop(row, col, bishops):
    for br, bc in bishops:
        if abs(row - br) == abs(col - bc):
            return False
    return True
```

### 2. **Backtracking Pattern**
```python
def backtrack(bishops, remaining):
    if remaining == 0:
        return 1
    
    count = 0
    for pos in range(n * n):
        row, col = pos // n, pos % n
        
        if can_place_bishop(row, col, bishops):
            bishops.append((row, col))
            count += backtrack(bishops, remaining - 1)
            bishops.pop()
    
    return count
```

### 3. **Diagonal Tracking**
```python
def track_diagonals(bishops):
    diagonals = set()
    for row, col in bishops:
        # Add all positions on the same diagonal
        for i in range(n):
            for j in range(n):
                if abs(i - row) == abs(j - col):
                    diagonals.add((i, j))
    return diagonals
```

## Problem-Solving Framework

1. **Identify problem type**: This is a chess piece placement problem with constraints
2. **Choose approach**: Use backtracking to place bishops systematically
3. **Implement checking**: Check for bishop attacks (diagonal)
4. **Optimize**: Use diagonal tracking to avoid invalid combinations early
5. **Count results**: Count valid bishop placements

---

*This analysis shows how to efficiently count bishops that can attack each other using diagonal analysis and coordinate mapping.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Weighted Bishop Attacks**
**Problem**: Each bishop has a weight. Find the total weight of attacking bishop pairs.
```python
def weighted_bishop_attacks(n, bishops, weights):
    # weights[i] = weight of bishop i
    diagonal1 = {}  # i + j
    diagonal2 = {}  # i - j
    
    total_weight = 0
    
    for i, (r, c) in enumerate(bishops):
        d1 = r + c
        d2 = r - c
        
        # Add weight from existing bishops on same diagonals
        if d1 in diagonal1:
            for other_idx in diagonal1[d1]:
                total_weight += weights[i] * weights[other_idx]
        if d2 in diagonal2:
            for other_idx in diagonal2[d2]:
                total_weight += weights[i] * weights[other_idx]
        
        # Add current bishop to diagonals
        if d1 not in diagonal1:
            diagonal1[d1] = []
        diagonal1[d1].append(i)
        
        if d2 not in diagonal2:
            diagonal2[d2] = []
        diagonal2[d2].append(i)
    
    return total_weight
```

#### **Variation 2: Constrained Bishop Attacks**
**Problem**: Count attacks only if bishops are within a certain distance.
```python
def constrained_bishop_attacks(n, bishops, max_distance):
    diagonal1 = {}  # i + j
    diagonal2 = {}  # i - j
    
    count = 0
    
    for i, (r, c) in enumerate(bishops):
        d1 = r + c
        d2 = r - c
        
        # Check diagonal1 attacks within distance
        if d1 in diagonal1:
            for other_r, other_c in diagonal1[d1]:
                if abs(r - other_r) <= max_distance:
                    count += 1
        
        # Check diagonal2 attacks within distance
        if d2 in diagonal2:
            for other_r, other_c in diagonal2[d2]:
                if abs(r - other_r) <= max_distance:
                    count += 1
        
        # Add current bishop to diagonals
        if d1 not in diagonal1:
            diagonal1[d1] = []
        diagonal1[d1].append((r, c))
        
        if d2 not in diagonal2:
            diagonal2[d2] = []
        diagonal2[d2].append((r, c))
    
    return count
```

#### **Variation 3: Bishop Attack Groups**
**Problem**: Find the number of groups of bishops that can all attack each other.
```python
def bishop_attack_groups(n, bishops):
    diagonal1 = {}  # i + j
    diagonal2 = {}  # i - j
    
    # Group bishops by diagonals
    for r, c in bishops:
        d1 = r + c
        d2 = r - c
        
        if d1 not in diagonal1:
            diagonal1[d1] = []
        diagonal1[d1].append((r, c))
        
        if d2 not in diagonal2:
            diagonal2[d2] = []
        diagonal2[d2].append((r, c))
    
    # Count groups (each diagonal forms a group)
    groups = 0
    for diagonal in diagonal1.values():
        if len(diagonal) > 1:
            groups += 1
    
    for diagonal in diagonal2.values():
        if len(diagonal) > 1:
            groups += 1
    
    return groups
```

#### **Variation 4: Bishop Attack Paths**
**Problem**: Count the number of different attack paths between bishops.
```python
def bishop_attack_paths(n, bishops):
    diagonal1 = {}  # i + j
    diagonal2 = {}  # i - j
    
    paths = 0
    
    for r, c in bishops:
        d1 = r + c
        d2 = r - c
        
        # Count paths on diagonal1
        if d1 in diagonal1:
            paths += len(diagonal1[d1])
        
        # Count paths on diagonal2
        if d2 in diagonal2:
            paths += len(diagonal2[d2])
        
        # Add current bishop to diagonals
        if d1 not in diagonal1:
            diagonal1[d1] = []
        diagonal1[d1].append((r, c))
        
        if d2 not in diagonal2:
            diagonal2[d2] = []
        diagonal2[d2].append((r, c))
    
    return paths
```

#### **Variation 5: Dynamic Bishop Attacks**
**Problem**: Support adding/removing bishops and answering attack queries efficiently.
```python
class DynamicBishopCounter:
    def __init__(self, n):
        self.n = n
        self.diagonal1 = {}  # i + j
        self.diagonal2 = {}  # i - j
        self.bishops = set()
        self.attack_count = 0
    
    def add_bishop(self, r, c):
        if (r, c) in self.bishops:
            return
        
        d1 = r + c
        d2 = r - c
        
        # Count new attacks
        if d1 in self.diagonal1:
            self.attack_count += len(self.diagonal1[d1])
        if d2 in self.diagonal2:
            self.attack_count += len(self.diagonal2[d2])
        
        # Add to diagonals
        if d1 not in self.diagonal1:
            self.diagonal1[d1] = []
        self.diagonal1[d1].append((r, c))
        
        if d2 not in self.diagonal2:
            self.diagonal2[d2] = []
        self.diagonal2[d2].append((r, c))
        
        self.bishops.add((r, c))
    
    def remove_bishop(self, r, c):
        if (r, c) not in self.bishops:
            return
        
        d1 = r + c
        d2 = r - c
        
        # Remove from diagonals and update attack count
        if d1 in self.diagonal1:
            self.diagonal1[d1].remove((r, c))
            self.attack_count -= len(self.diagonal1[d1])
            if not self.diagonal1[d1]:
                del self.diagonal1[d1]
        
        if d2 in self.diagonal2:
            self.diagonal2[d2].remove((r, c))
            self.attack_count -= len(self.diagonal2[d2])
            if not self.diagonal2[d2]:
                del self.diagonal2[d2]
        
        self.bishops.remove((r, c))
    
    def get_attack_count(self):
        return self.attack_count
```

### 🔗 **Related Problems & Concepts**

#### **1. Chess Problems**
- **Chess Piece Attacks**: Analyze chess piece attacks
- **Chess Board Patterns**: Find patterns on chess boards
- **Chess Optimization**: Optimize chess strategies
- **Chess Analysis**: Analyze chess positions

#### **2. Diagonal Problems**
- **Diagonal Traversal**: Traverse diagonals efficiently
- **Diagonal Patterns**: Find diagonal patterns
- **Diagonal Optimization**: Optimize diagonal operations
- **Diagonal Analysis**: Analyze diagonal properties

#### **3. Coordinate Problems**
- **Coordinate Mapping**: Map coordinates efficiently
- **Coordinate Analysis**: Analyze coordinate patterns
- **Coordinate Optimization**: Optimize coordinate operations
- **Coordinate Systems**: Work with coordinate systems

#### **4. Attack Problems**
- **Attack Detection**: Detect attacks efficiently
- **Attack Patterns**: Find attack patterns
- **Attack Optimization**: Optimize attack algorithms
- **Attack Analysis**: Analyze attack properties

#### **5. Graph Problems**
- **Graph Traversal**: Traverse graphs efficiently
- **Graph Patterns**: Find graph patterns
- **Graph Optimization**: Optimize graph operations
- **Graph Analysis**: Analyze graph properties

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    bishops = []
    for _ in range(k):
        r, c = map(int, input().split())
        bishops.append((r, c))
    
    result = count_bishop_attacks(n, bishops)
    print(result)
```

#### **2. Range Queries**
```python
# Precompute attack counts for different board regions
def precompute_attack_counts(n, bishops):
    # Precompute for all possible board regions
    attack_counts = {}
    
    for start_r in range(n):
        for start_c in range(n):
            for end_r in range(start_r, n):
                for end_c in range(start_c, n):
                    region_bishops = []
                    for r, c in bishops:
                        if start_r <= r <= end_r and start_c <= c <= end_c:
                            region_bishops.append((r, c))
                    
                    count = count_bishop_attacks(end_r - start_r + 1, region_bishops)
                    attack_counts[(start_r, start_c, end_r, end_c)] = count
    
    return attack_counts

# Answer range queries efficiently
def range_query(attack_counts, start_r, start_c, end_r, end_c):
    return attack_counts.get((start_r, start_c, end_r, end_c), 0)
```

#### **3. Interactive Problems**
```python
# Interactive bishop analyzer
def interactive_bishop_analyzer():"
    n = int(input("Enter board size: "))
    k = int(input("Enter number of bishops: "))
    bishops = []
    
    print("Enter bishop positions:")
    for i in range(k):
        r, c = map(int, input(f"Bishop {i+1}: ").split())
        bishops.append((r, c))
    
    print("Bishops:", bishops)
    
    while True:
        query = input("Enter query (attacks/weighted/constrained/groups/paths/dynamic/exit): ")
        if query == "exit":
            break
        
        if query == "attacks":
            result = count_bishop_attacks(n, bishops)
            print(f"Attack pairs: {result}")
        elif query == "weighted":
            weights = list(map(int, input("Enter weights: ").split()))
            result = weighted_bishop_attacks(n, bishops, weights)
            print(f"Weighted attacks: {result}")
        elif query == "constrained":
            max_dist = int(input("Enter max distance: "))
            result = constrained_bishop_attacks(n, bishops, max_dist)
            print(f"Constrained attacks: {result}")
        elif query == "groups":
            result = bishop_attack_groups(n, bishops)
            print(f"Attack groups: {result}")
        elif query == "paths":
            result = bishop_attack_paths(n, bishops)
            print(f"Attack paths: {result}")
        elif query == "dynamic":
            counter = DynamicBishopCounter(n)
            for r, c in bishops:
                counter.add_bishop(r, c)
            print(f"Dynamic attack count: {counter.get_attack_count()}")
```

### 🧮 **Mathematical Extensions**

#### **1. Combinatorics**
- **Bishop Combinations**: Count bishop combinations
- **Attack Arrangements**: Arrange attacks on board
- **Diagonal Partitions**: Partition board into diagonals
- **Inclusion-Exclusion**: Count using inclusion-exclusion

#### **2. Number Theory**
- **Chess Patterns**: Mathematical patterns in chess
- **Diagonal Sequences**: Sequences of diagonal positions
- **Modular Arithmetic**: Chess operations with modular arithmetic
- **Number Sequences**: Sequences in chess counting

#### **3. Optimization Theory**
- **Chess Optimization**: Optimize chess operations
- **Attack Optimization**: Optimize attack counting
- **Algorithm Optimization**: Optimize algorithms
- **Complexity Analysis**: Analyze algorithm complexity

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Chess Algorithms**: Efficient chess algorithms
- **Diagonal Traversal**: Diagonal traversal algorithms
- **Coordinate Mapping**: Coordinate mapping algorithms
- **Dynamic Programming**: For optimization problems

#### **2. Mathematical Concepts**
- **Combinatorics**: Foundation for counting problems
- **Chess Theory**: Mathematical properties of chess
- **Diagonal Theory**: Properties of diagonals
- **Optimization**: Mathematical optimization techniques

#### **3. Programming Concepts**
- **Data Structures**: Efficient storage and retrieval
- **Algorithm Design**: Problem-solving strategies
- **Chess Processing**: Efficient chess processing techniques
- **Attack Analysis**: Attack analysis techniques

---

*This analysis demonstrates efficient bishop attack counting techniques and shows various extensions for chess and diagonal problems.* 