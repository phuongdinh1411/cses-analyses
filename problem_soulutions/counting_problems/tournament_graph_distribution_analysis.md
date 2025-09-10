---
layout: simple
title: "Tournament Graph Distribution - Graph Theory Problem"
permalink: /problem_soulutions/counting_problems/tournament_graph_distribution_analysis
---

# Tournament Graph Distribution - Graph Theory Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of tournament graphs in graph theory
- Apply counting techniques for tournament graph analysis
- Implement efficient algorithms for tournament graph counting
- Optimize graph operations for distribution analysis
- Handle special cases in tournament graph counting

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph theory, counting techniques, mathematical formulas
- **Data Structures**: Graphs, adjacency lists, mathematical computations
- **Mathematical Concepts**: Graph theory, combinations, permutations, modular arithmetic
- **Programming Skills**: Graph representation, mathematical computations, modular arithmetic
- **Related Problems**: Counting Permutations (combinatorics), Counting Combinations (combinatorics), Counting Sequences (combinatorics)

## 📋 Problem Description

Given n players, count the number of tournament graphs (complete directed graphs where each edge has a direction).

**Input**: 
- n: number of players

**Output**: 
- Number of tournament graphs modulo 10^9+7

**Constraints**:
- 1 ≤ n ≤ 10^6
- Answer modulo 10^9+7

**Example**:
```
Input:
n = 3

Output:
8

Explanation**: 
Tournament graphs with 3 players:
- Each pair of players has one directed edge
- Total edges: C(3,2) = 3
- Each edge can be directed in 2 ways
- Total tournaments: 2^3 = 8
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Recursive Tournament Solution

**Key Insights from Recursive Tournament Solution**:
- **Recursive Approach**: Use recursion to generate all tournament graphs
- **Complete Enumeration**: Enumerate all possible edge directions
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: Exponential time complexity

**Key Insight**: Use recursion to generate all possible tournament graphs by assigning directions to edges.

**Algorithm**:
- Use recursive function to assign directions to edges
- Count all valid tournament graphs
- Apply modulo operation to prevent overflow

**Visual Example**:
```
n = 3 players

Recursive generation:
┌─────────────────────────────────────┐
│ Edge 1: (1,2) or (2,1)            │
│ Edge 2: (1,3) or (3,1)            │
│ Edge 3: (2,3) or (3,2)            │
│ Total combinations: 2 × 2 × 2 = 8 │
└─────────────────────────────────────┘

Tournament enumeration:
┌─────────────────────────────────────┐
│ 1→2, 1→3, 2→3                     │
│ 1→2, 1→3, 3→2                     │
│ 1→2, 3→1, 2→3                     │
│ 1→2, 3→1, 3→2                     │
│ 2→1, 1→3, 2→3                     │
│ 2→1, 1→3, 3→2                     │
│ 2→1, 3→1, 2→3                     │
│ 2→1, 3→1, 3→2                     │
│ Total: 8 tournaments               │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def recursive_tournament_count(n, mod=10**9+7):
    """
    Count tournament graphs using recursive approach
    
    Args:
        n: number of players
        mod: modulo value
    
    Returns:
        int: number of tournament graphs modulo mod
    """
    def count_tournaments(edge_index, edges):
        """Count tournament graphs recursively"""
        if edge_index == len(edges):
            return 1  # Valid tournament found
        
        count = 0
        edge = edges[edge_index]
        
        # Try both directions for current edge
        for direction in [edge, (edge[1], edge[0])]:
            count = (count + count_tournaments(edge_index + 1, edges)) % mod
        
        return count
    
    # Generate all edges
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            edges.append((i, j))
    
    return count_tournaments(0, edges)

def recursive_tournament_count_optimized(n, mod=10**9+7):
    """
    Optimized recursive tournament counting
    
    Args:
        n: number of players
        mod: modulo value
    
    Returns:
        int: number of tournament graphs modulo mod
    """
    def count_tournaments_optimized(edge_index, total_edges):
        """Count tournament graphs with optimization"""
        if edge_index == total_edges:
            return 1  # Valid tournament found
        
        # Each edge can be directed in 2 ways
        return (2 * count_tournaments_optimized(edge_index + 1, total_edges)) % mod
    
    # Total number of edges in complete graph
    total_edges = n * (n - 1) // 2
    
    return count_tournaments_optimized(0, total_edges)

# Example usage
n = 3
result1 = recursive_tournament_count(n)
result2 = recursive_tournament_count_optimized(n)
print(f"Recursive tournament count: {result1}")
print(f"Optimized recursive count: {result2}")
```

**Time Complexity**: O(2^(n²))
**Space Complexity**: O(n²)

**Why it's inefficient**: Exponential time complexity due to complete enumeration.

---

### Approach 2: Mathematical Formula Solution

**Key Insights from Mathematical Formula Solution**:
- **Mathematical Formula**: Use 2^(n(n-1)/2) formula for tournament graphs
- **Direct Calculation**: Calculate result directly without enumeration
- **Efficient Computation**: O(log n) time complexity
- **Optimization**: Much more efficient than recursive approach

**Key Insight**: Use the mathematical formula that each edge can be directed in 2 ways.

**Algorithm**:
- Use formula: number of tournaments = 2^(n(n-1)/2)
- Calculate 2^(n(n-1)/2) efficiently using modular exponentiation
- Apply modulo operation throughout

**Visual Example**:
```
Mathematical formula:
┌─────────────────────────────────────┐
│ For n players:                     │
│ - Number of edges: n(n-1)/2        │
│ - Each edge: 2 directions          │
│ - Total tournaments: 2^(n(n-1)/2)  │
└─────────────────────────────────────┘

Modular exponentiation:
┌─────────────────────────────────────┐
│ 2^(n(n-1)/2) mod mod               │
│ Use binary exponentiation for efficiency │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def mathematical_tournament_count(n, mod=10**9+7):
    """
    Count tournament graphs using mathematical formula
    
    Args:
        n: number of players
        mod: modulo value
    
    Returns:
        int: number of tournament graphs modulo mod
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
    
    # Number of tournaments = 2^(n(n-1)/2)
    if n <= 1:
        return 1
    
    exponent = n * (n - 1) // 2
    return mod_pow(2, exponent, mod)

def mathematical_tournament_count_v2(n, mod=10**9+7):
    """
    Alternative mathematical approach using built-in pow
    
    Args:
        n: number of players
        mod: modulo value
    
    Returns:
        int: number of tournament graphs modulo mod
    """
    if n <= 1:
        return 1
    
    # Use built-in pow with modular arithmetic
    exponent = n * (n - 1) // 2
    return pow(2, exponent, mod)

# Example usage
n = 3
result1 = mathematical_tournament_count(n)
result2 = mathematical_tournament_count_v2(n)
print(f"Mathematical tournament count: {result1}")
print(f"Mathematical tournament count v2: {result2}")
```

**Time Complexity**: O(log n)
**Space Complexity**: O(1)

**Why it's better**: Uses mathematical formula for O(log n) time complexity.

**Implementation Considerations**:
- **Mathematical Formula**: Use 2^(n(n-1)/2) formula for tournament graphs
- **Modular Exponentiation**: Use efficient modular exponentiation
- **Direct Calculation**: Calculate result directly without enumeration

---

### Approach 3: Advanced Mathematical Solution (Optimal)

**Key Insights from Advanced Mathematical Solution**:
- **Advanced Mathematics**: Use advanced mathematical properties
- **Efficient Computation**: O(log n) time complexity
- **Mathematical Optimization**: Use mathematical optimizations
- **Optimal Complexity**: Best approach for tournament graph counting

**Key Insight**: Use advanced mathematical properties and optimizations for efficient tournament graph counting.

**Algorithm**:
- Use advanced mathematical properties
- Apply mathematical optimizations
- Calculate result efficiently

**Visual Example**:
```
Advanced mathematical properties:
┌─────────────────────────────────────┐
│ For tournament graphs:             │
│ - Each edge has 2 directions       │
│ - Total number = 2^(n(n-1)/2)     │
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
def advanced_mathematical_tournament_count(n, mod=10**9+7):
    """
    Count tournament graphs using advanced mathematical approach
    
    Args:
        n: number of players
        mod: modulo value
    
    Returns:
        int: number of tournament graphs modulo mod
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
    if n <= 1:
        return 1
    
    # Number of tournaments = 2^(n(n-1)/2)
    exponent = n * (n - 1) // 2
    return fast_mod_pow(2, exponent, mod)

def optimized_tournament_count(n, mod=10**9+7):
    """
    Optimized tournament counting with additional optimizations
    
    Args:
        n: number of players
        mod: modulo value
    
    Returns:
        int: number of tournament graphs modulo mod
    """
    # Use built-in pow with optimizations
    if n <= 1:
        return 1
    
    # For large n, use built-in pow which is highly optimized
    exponent = n * (n - 1) // 2
    return pow(2, exponent, mod)

def tournament_count_with_precomputation(max_n, mod=10**9+7):
    """
    Precompute tournament counts for multiple queries
    
    Args:
        max_n: maximum value of n
        mod: modulo value
    
    Returns:
        list: precomputed tournament counts
    """
    results = [0] * (max_n + 1)
    
    for i in range(max_n + 1):
        if i <= 1:
            results[i] = 1
        else:
            exponent = i * (i - 1) // 2
            results[i] = pow(2, exponent, mod)
    
    return results

# Example usage
n = 3
result1 = advanced_mathematical_tournament_count(n)
result2 = optimized_tournament_count(n)
print(f"Advanced mathematical tournament count: {result1}")
print(f"Optimized tournament count: {result2}")

# Precompute for multiple queries
max_n = 1000
precomputed = tournament_count_with_precomputation(max_n)
print(f"Precomputed result for n={n}: {precomputed[n]}")
```

**Time Complexity**: O(log n)
**Space Complexity**: O(1)

**Why it's optimal**: Uses advanced mathematical properties for O(log n) time complexity.

**Implementation Details**:
- **Advanced Mathematics**: Use advanced mathematical properties
- **Efficient Computation**: Use optimized modular exponentiation
- **Mathematical Optimizations**: Apply mathematical optimizations
- **Precomputation**: Precompute results for multiple queries

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive | O(2^(n²)) | O(n²) | Complete enumeration of all tournament graphs |
| Mathematical Formula | O(log n) | O(1) | Use 2^(n(n-1)/2) formula with modular exponentiation |
| Advanced Mathematical | O(log n) | O(1) | Use advanced mathematical properties and optimizations |

### Time Complexity
- **Time**: O(log n) - Use modular exponentiation for efficient calculation
- **Space**: O(1) - Use only necessary variables

### Why This Solution Works
- **Mathematical Formula**: Use 2^(n(n-1)/2) formula for tournament graphs
- **Modular Exponentiation**: Use efficient modular exponentiation
- **Mathematical Properties**: Leverage mathematical properties
- **Efficient Algorithms**: Use optimal algorithms for calculation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Tournament Count with Constraints**
**Problem**: Count tournament graphs with certain constraints.

**Key Differences**: Apply constraints to tournament graphs

**Solution Approach**: Modify counting formula to include constraints

**Implementation**:
```python
def constrained_tournament_count(n, constraints, mod=10**9+7):
    """
    Count tournament graphs with constraints
    
    Args:
        n: number of players
        constraints: list of constraints for each edge
        mod: modulo value
    
    Returns:
        int: number of constrained tournament graphs modulo mod
    """
    def count_constrained_tournaments(edge_index, edges, constraints):
        """Count constrained tournament graphs recursively"""
        if edge_index == len(edges):
            return 1  # Valid constrained tournament found
        
        count = 0
        edge = edges[edge_index]
        constraint = constraints[edge_index]
        
        # Try directions allowed by constraints
        for direction in constraint:
            count = (count + count_constrained_tournaments(edge_index + 1, edges, constraints)) % mod
        
        return count
    
    # Generate all edges
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            edges.append((i, j))
    
    return count_constrained_tournaments(0, edges, constraints)

def constrained_tournament_count_optimized(n, constraints, mod=10**9+7):
    """
    Optimized constrained tournament counting
    
    Args:
        n: number of players
        constraints: list of constraints for each edge
        mod: modulo value
    
    Returns:
        int: number of constrained tournament graphs modulo mod
    """
    # Calculate total number of constrained tournaments
    total = 1
    for constraint in constraints:
        total = (total * len(constraint)) % mod
    
    return total

# Example usage
n = 3
constraints = [
    [(0, 1), (1, 0)],  # Edge 0-1 can be directed either way
    [(0, 2)],          # Edge 0-2 must be directed from 0 to 2
    [(1, 2), (2, 1)]   # Edge 1-2 can be directed either way
]
result1 = constrained_tournament_count(n, constraints)
result2 = constrained_tournament_count_optimized(n, constraints)
print(f"Constrained tournament count: {result1}")
print(f"Optimized constrained count: {result2}")
```

#### **2. Tournament Count with Weighted Edges**
**Problem**: Count tournament graphs with weighted edges.

**Key Differences**: Edges have weights that affect counting

**Solution Approach**: Modify counting formula to include weights

**Implementation**:
```python
def weighted_tournament_count(n, weights, mod=10**9+7):
    """
    Count tournament graphs with weighted edges
    
    Args:
        n: number of players
        weights: list of weights for each edge
        mod: modulo value
    
    Returns:
        int: number of weighted tournament graphs modulo mod
    """
    def count_weighted_tournaments(edge_index, edges, weights, current_weight):
        """Count weighted tournament graphs recursively"""
        if edge_index == len(edges):
            return current_weight % mod  # Return weighted count
        
        count = 0
        edge = edges[edge_index]
        weight = weights[edge_index]
        
        # Try both directions for current edge
        for direction in [edge, (edge[1], edge[0])]:
            new_weight = (current_weight * weight) % mod
            count = (count + count_weighted_tournaments(edge_index + 1, edges, weights, new_weight)) % mod
        
        return count
    
    # Generate all edges
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            edges.append((i, j))
    
    return count_weighted_tournaments(0, edges, weights, 1)

# Example usage
n = 3
weights = [2, 3, 1]  # Weights for edges 0-1, 0-2, 1-2
result = weighted_tournament_count(n, weights)
print(f"Weighted tournament count: {result}")
```

#### **3. Tournament Count with Multiple Tournaments**
**Problem**: Count tournament graphs across multiple tournaments.

**Key Differences**: Handle multiple tournaments simultaneously

**Solution Approach**: Combine results from multiple tournaments

**Implementation**:
```python
def multi_tournament_count(tournaments, mod=10**9+7):
    """
    Count tournament graphs across multiple tournaments
    
    Args:
        tournaments: list of tournament sizes
        mod: modulo value
    
    Returns:
        int: number of tournament graphs modulo mod
    """
    def count_single_tournament(n):
        """Count tournaments for single tournament"""
        return optimized_tournament_count(n, mod)
    
    # Count tournaments for each tournament
    total_count = 1
    for n in tournaments:
        tournament_count = count_single_tournament(n)
        total_count = (total_count * tournament_count) % mod
    
    return total_count

# Example usage
tournaments = [3, 2, 4]  # Three tournaments of sizes 3, 2, 4
result = multi_tournament_count(tournaments)
print(f"Multi-tournament count: {result}")
```

### Related Problems

#### **CSES Problems**
- [Counting Permutations](https://cses.fi/problemset/task/1075) - Combinatorics
- [Counting Combinations](https://cses.fi/problemset/task/1075) - Combinatorics
- [Counting Sequences](https://cses.fi/problemset/task/1075) - Combinatorics

#### **LeetCode Problems**
- [Course Schedule](https://leetcode.com/problems/course-schedule/) - Graph theory
- [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/) - Graph theory
- [Redundant Connection](https://leetcode.com/problems/redundant-connection/) - Graph theory

#### **Problem Categories**
- **Graph Theory**: Tournament graphs, directed graphs
- **Combinatorics**: Mathematical counting, graph properties
- **Mathematical Algorithms**: Modular arithmetic, number theory

## 🔗 Additional Resources

### **Algorithm References**
- [Graph Theory](https://cp-algorithms.com/graph/basic-graph-algorithms.html) - Graph algorithms
- [Combinatorics](https://cp-algorithms.com/combinatorics/binomial-coefficients.html) - Counting techniques
- [Modular Arithmetic](https://cp-algorithms.com/algebra/module-inverse.html) - Modular arithmetic

### **Practice Problems**
- [CSES Counting Permutations](https://cses.fi/problemset/task/1075) - Medium
- [CSES Counting Combinations](https://cses.fi/problemset/task/1075) - Medium
- [CSES Counting Sequences](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Introduction to Algorithms](https://mitpress.mit.edu/books/introduction-algorithms) - CLRS textbook
- [Competitive Programming](https://cp-algorithms.com/) - Algorithm reference
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article

---

## 📝 Implementation Checklist

When applying this template to a new problem, ensure you:

### **Content Requirements**
- [x] **Problem Description**: Clear, concise with examples
- [x] **Learning Objectives**: 5 specific, measurable goals
- [x] **Prerequisites**: 5 categories of required knowledge
- [x] **3 Approaches**: Brute Force → Greedy → Optimal
- [x] **Key Insights**: 4-5 insights per approach at the beginning
- [x] **Visual Examples**: ASCII diagrams for each approach
- [x] **Complete Implementations**: Working code with examples
- [x] **Complexity Analysis**: Time and space for each approach
- [x] **Problem Variations**: 3 variations with implementations
- [x] **Related Problems**: CSES and LeetCode links

### **Structure Requirements**
- [x] **No Redundant Sections**: Remove duplicate Key Insights
- [x] **Logical Flow**: Each approach builds on the previous
- [x] **Progressive Complexity**: Clear improvement from approach to approach
- [x] **Educational Value**: Theory + Practice in each section
- [x] **Complete Coverage**: All important concepts included

### **Quality Requirements**
- [x] **Working Code**: All implementations are runnable
- [x] **Test Cases**: Examples with expected outputs
- [x] **Edge Cases**: Handle boundary conditions
- [x] **Clear Explanations**: Easy to understand for students
- [x] **Visual Learning**: Diagrams and examples throughout

---

## 🎯 **Template Usage Instructions**

### **Step 1: Replace Placeholders**
- Replace `[Problem Name]` with actual problem name
- Replace `[category]` with the problem category folder
- Replace `[problem_name]` with the actual problem filename
- Replace all `[placeholder]` text with actual content

### **Step 2: Customize Approaches**
- **Approach 1**: Usually brute force or naive solution
- **Approach 2**: Optimized solution (DP, greedy, etc.)
- **Approach 3**: Optimal solution (advanced algorithms)

### **Step 3: Add Visual Examples**
- Use ASCII art for diagrams
- Show step-by-step execution
- Use actual data in examples

### **Step 4: Implement Working Code**
- Write complete, runnable implementations
- Include test cases and examples
- Handle edge cases properly

### **Step 5: Add Problem Variations**
- Create 3 meaningful variations
- Provide implementations for each
- Link to related problems

### **Step 6: Quality Check**
- Ensure no redundant sections
- Verify all code works
- Check that complexity analysis is correct
- Confirm educational value is high

This template ensures consistency across all problem analyses while maintaining high educational value and practical implementation focus.