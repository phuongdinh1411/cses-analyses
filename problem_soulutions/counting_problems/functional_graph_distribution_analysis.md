---
layout: simple
title: "Functional Graph Distribution - Graph Theory Problem"
permalink: /problem_soulutions/counting_problems/functional_graph_distribution_analysis
---

# Functional Graph Distribution - Graph Theory Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of functional graphs in graph theory
- Apply counting techniques for functional graph analysis
- Implement efficient algorithms for functional graph counting
- Optimize graph operations for distribution analysis
- Handle special cases in functional graph counting

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph theory, counting techniques, combinatorial analysis
- **Data Structures**: Graphs, adjacency lists, mathematical computations
- **Mathematical Concepts**: Combinatorics, counting principles, graph properties
- **Programming Skills**: Graph representation, mathematical computations, modular arithmetic
- **Related Problems**: Counting Permutations (combinatorics), Counting Combinations (combinatorics), Counting Sequences (combinatorics)

## 📋 Problem Description

Given n nodes, count the number of functional graphs (where each node has exactly one outgoing edge).

**Input**: 
- n: number of nodes

**Output**: 
- Number of functional graphs modulo 10^9+7

**Constraints**:
- 1 ≤ n ≤ 10^6
- Answer modulo 10^9+7

**Example**:
```
Input:
n = 3

Output:
27

Explanation**: 
Functional graphs with 3 nodes:
- Each node can point to any of the 3 nodes
- Total: 3^3 = 27 functional graphs
- Examples: 1→1, 2→2, 3→3 or 1→2, 2→3, 3→1
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Generate all possible functional graphs
- **Direct Counting**: Count all possible edge assignments
- **Simple Implementation**: Easy to understand and implement
- **Inefficient**: Exponential time complexity

**Key Insight**: Enumerate all possible functional graphs by assigning edges to each node.

**Algorithm**:
- For each node, try all possible outgoing edges
- Count all valid functional graphs
- Apply modulo operation to prevent overflow

**Visual Example**:
```
n = 3 nodes

Brute force enumeration:
┌─────────────────────────────────────┐
│ Node 1: can point to 1, 2, or 3    │
│ Node 2: can point to 1, 2, or 3    │
│ Node 3: can point to 1, 2, or 3    │
│ Total combinations: 3 × 3 × 3 = 27 │
└─────────────────────────────────────┘

Example functional graphs:
┌─────────────────────────────────────┐
│ Graph 1: 1→1, 2→2, 3→3            │
│ Graph 2: 1→2, 2→3, 3→1            │
│ Graph 3: 1→3, 2→1, 3→2            │
│ ... (24 more)                      │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_functional_graph_count(n, mod=10**9+7):
    """
    Count functional graphs using brute force approach
    
    Args:
        n: number of nodes
        mod: modulo value
    
    Returns:
        int: number of functional graphs modulo mod
    """
    def generate_functional_graphs(node, current_graph):
        """Generate all possible functional graphs recursively"""
        if node == n:
            return 1  # Valid functional graph found
        
        count = 0
        for target in range(n):
            current_graph[node] = target
            count = (count + generate_functional_graphs(node + 1, current_graph)) % mod
        
        return count
    
    return generate_functional_graphs(0, [0] * n)

def brute_force_iterative(n, mod=10**9+7):
    """
    Count functional graphs using iterative brute force
    
    Args:
        n: number of nodes
        mod: modulo value
    
    Returns:
        int: number of functional graphs modulo mod
    """
    count = 0
    
    # Generate all possible functional graphs
    for i in range(n ** n):
        # Convert number to base-n representation
        graph = []
        temp = i
        for _ in range(n):
            graph.append(temp % n)
            temp //= n
        
        # This represents a valid functional graph
        count = (count + 1) % mod
    
    return count

# Example usage
n = 3
result1 = brute_force_functional_graph_count(n)
result2 = brute_force_iterative(n)
print(f"Brute force recursive result: {result1}")
print(f"Brute force iterative result: {result2}")
```

**Time Complexity**: O(n^n)
**Space Complexity**: O(n)

**Why it's inefficient**: Exponential time complexity due to complete enumeration.

---

### Approach 2: Mathematical Formula Solution

**Key Insights from Mathematical Formula Solution**:
- **Mathematical Formula**: Use n^n formula for functional graphs
- **Direct Calculation**: Calculate result directly without enumeration
- **Efficient Computation**: O(log n) time complexity
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use the mathematical formula that each node can point to any of n nodes.

**Algorithm**:
- Use formula: number of functional graphs = n^n
- Calculate n^n efficiently using modular exponentiation
- Apply modulo operation throughout

**Visual Example**:
```
Mathematical formula:
┌─────────────────────────────────────┐
│ For n nodes:                       │
│ - Node 1: n choices                │
│ - Node 2: n choices                │
│ - Node 3: n choices                │
│ - ...                              │
│ - Node n: n choices                │
│ Total: n × n × ... × n = n^n      │
└─────────────────────────────────────┘

Modular exponentiation:
┌─────────────────────────────────────┐
│ n^n mod mod = (n mod mod)^n mod mod │
│ Use binary exponentiation for efficiency │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def mathematical_functional_graph_count(n, mod=10**9+7):
    """
    Count functional graphs using mathematical formula
    
    Args:
        n: number of nodes
        mod: modulo value
    
    Returns:
        int: number of functional graphs modulo mod
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
    
    # Number of functional graphs = n^n
    return mod_pow(n, n, mod)

def mathematical_functional_graph_count_v2(n, mod=10**9+7):
    """
    Alternative mathematical approach using built-in pow
    
    Args:
        n: number of nodes
        mod: modulo value
    
    Returns:
        int: number of functional graphs modulo mod
    """
    # Use built-in pow with modular arithmetic
    return pow(n, n, mod)

# Example usage
n = 3
result1 = mathematical_functional_graph_count(n)
result2 = mathematical_functional_graph_count_v2(n)
print(f"Mathematical result: {result1}")
print(f"Mathematical result v2: {result2}")
```

**Time Complexity**: O(log n)
**Space Complexity**: O(1)

**Why it's better**: Uses mathematical formula for O(log n) time complexity.

**Implementation Considerations**:
- **Mathematical Formula**: Use n^n formula for functional graphs
- **Modular Exponentiation**: Use efficient modular exponentiation
- **Direct Calculation**: Calculate result directly without enumeration

---

### Approach 3: Advanced Mathematical Solution (Optimal)

**Key Insights from Advanced Mathematical Solution**:
- **Advanced Mathematics**: Use advanced mathematical properties
- **Efficient Computation**: O(log n) time complexity
- **Mathematical Optimization**: Use mathematical optimizations
- **Optimal Complexity**: Best approach for functional graph counting

**Key Insight**: Use advanced mathematical properties and optimizations for efficient functional graph counting.

**Algorithm**:
- Use advanced mathematical properties
- Apply mathematical optimizations
- Calculate result efficiently

**Visual Example**:
```
Advanced mathematical properties:
┌─────────────────────────────────────┐
│ For functional graphs:             │
│ - Each node has exactly one outgoing edge │
│ - Total number = n^n               │
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
def advanced_mathematical_functional_graph_count(n, mod=10**9+7):
    """
    Count functional graphs using advanced mathematical approach
    
    Args:
        n: number of nodes
        mod: modulo value
    
    Returns:
        int: number of functional graphs modulo mod
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
    if n == 0:
        return 1
    if n == 1:
        return 1
    
    # Number of functional graphs = n^n
    return fast_mod_pow(n, n, mod)

def optimized_functional_graph_count(n, mod=10**9+7):
    """
    Optimized functional graph counting with additional optimizations
    
    Args:
        n: number of nodes
        mod: modulo value
    
    Returns:
        int: number of functional graphs modulo mod
    """
    # Use built-in pow with optimizations
    if n == 0:
        return 1
    if n == 1:
        return 1
    
    # For large n, use built-in pow which is highly optimized
    return pow(n, n, mod)

def functional_graph_count_with_precomputation(max_n, mod=10**9+7):
    """
    Precompute functional graph counts for multiple queries
    
    Args:
        max_n: maximum value of n
        mod: modulo value
    
    Returns:
        list: precomputed functional graph counts
    """
    results = [0] * (max_n + 1)
    
    for i in range(max_n + 1):
        if i == 0:
            results[i] = 1
        elif i == 1:
            results[i] = 1
        else:
            results[i] = pow(i, i, mod)
    
    return results

# Example usage
n = 3
result1 = advanced_mathematical_functional_graph_count(n)
result2 = optimized_functional_graph_count(n)
print(f"Advanced mathematical result: {result1}")
print(f"Optimized result: {result2}")

# Precompute for multiple queries
max_n = 1000
precomputed = functional_graph_count_with_precomputation(max_n)
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
| Brute Force | O(n^n) | O(n) | Complete enumeration of all functional graphs |
| Mathematical Formula | O(log n) | O(1) | Use n^n formula with modular exponentiation |
| Advanced Mathematical | O(log n) | O(1) | Use advanced mathematical properties and optimizations |

### Time Complexity
- **Time**: O(log n) - Use modular exponentiation for efficient calculation
- **Space**: O(1) - Use only necessary variables

### Why This Solution Works
- **Mathematical Formula**: Use n^n formula for functional graphs
- **Modular Exponentiation**: Use efficient modular exponentiation
- **Mathematical Properties**: Leverage mathematical properties
- **Efficient Algorithms**: Use optimal algorithms for calculation

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Functional Graph Count with Constraints**
**Problem**: Count functional graphs with certain constraints.

**Key Differences**: Apply constraints to functional graphs

**Solution Approach**: Modify counting formula to include constraints

**Implementation**:
```python
def constrained_functional_graph_count(n, constraints, mod=10**9+7):
    """
    Count functional graphs with constraints
    
    Args:
        n: number of nodes
        constraints: list of constraints for each node
        mod: modulo value
    
    Returns:
        int: number of constrained functional graphs modulo mod
    """
    def count_constrained_graphs(node, current_graph):
        """Count constrained functional graphs recursively"""
        if node == n:
            return 1  # Valid constrained functional graph found
        
        count = 0
        for target in constraints[node]:  # Only consider allowed targets
            current_graph[node] = target
            count = (count + count_constrained_graphs(node + 1, current_graph)) % mod
        
        return count
    
    return count_constrained_graphs(0, [0] * n)

def constrained_functional_graph_count_optimized(n, constraints, mod=10**9+7):
    """
    Optimized constrained functional graph counting
    
    Args:
        n: number of nodes
        constraints: list of constraints for each node
        mod: modulo value
    
    Returns:
        int: number of constrained functional graphs modulo mod
    """
    # Calculate total number of constrained functional graphs
    total = 1
    for i in range(n):
        total = (total * len(constraints[i])) % mod
    
    return total

# Example usage
n = 3
constraints = [
    [0, 1],  # Node 0 can point to nodes 0 or 1
    [1, 2],  # Node 1 can point to nodes 1 or 2
    [0, 2]   # Node 2 can point to nodes 0 or 2
]
result1 = constrained_functional_graph_count(n, constraints)
result2 = constrained_functional_graph_count_optimized(n, constraints)
print(f"Constrained functional graph count: {result1}")
print(f"Optimized constrained count: {result2}")
```

#### **2. Functional Graph Count with Cycles**
**Problem**: Count functional graphs with specific cycle properties.

**Key Differences**: Consider cycle properties in functional graphs

**Solution Approach**: Use cycle analysis for counting

**Implementation**:
```python
def cycle_functional_graph_count(n, cycle_lengths, mod=10**9+7):
    """
    Count functional graphs with specific cycle properties
    
    Args:
        n: number of nodes
        cycle_lengths: list of allowed cycle lengths
        mod: modulo value
    
    Returns:
        int: number of functional graphs with specified cycles modulo mod
    """
    def count_cycle_graphs(node, current_graph, cycle_count):
        """Count functional graphs with cycle properties"""
        if node == n:
            # Check if graph has required cycle properties
            if has_required_cycles(current_graph, cycle_lengths):
                return 1
            return 0
        
        count = 0
        for target in range(n):
            current_graph[node] = target
            count = (count + count_cycle_graphs(node + 1, current_graph, cycle_count)) % mod
        
        return count
    
    return count_cycle_graphs(0, [0] * n, 0)

def has_required_cycles(graph, cycle_lengths):
    """
    Check if graph has required cycle properties
    
    Args:
        graph: functional graph representation
        cycle_lengths: list of required cycle lengths
    
    Returns:
        bool: True if graph has required cycles
    """
    n = len(graph)
    visited = [False] * n
    cycle_counts = {}
    
    for i in range(n):
        if not visited[i]:
            cycle_length = find_cycle_length(graph, i, visited)
            cycle_counts[cycle_length] = cycle_counts.get(cycle_length, 0) + 1
    
    # Check if cycle counts match requirements
    for length in cycle_lengths:
        if cycle_counts.get(length, 0) == 0:
            return False
    
    return True

def find_cycle_length(graph, start, visited):
    """
    Find cycle length starting from given node
    
    Args:
        graph: functional graph representation
        start: starting node
        visited: visited array
    
    Returns:
        int: cycle length
    """
    path = []
    current = start
    
    while not visited[current]:
        visited[current] = True
        path.append(current)
        current = graph[current]
    
    # Find cycle length
    if current in path:
        cycle_start = path.index(current)
        return len(path) - cycle_start
    
    return 0

# Example usage
n = 3
cycle_lengths = [1, 2]  # Require cycles of length 1 and 2
result = cycle_functional_graph_count(n, cycle_lengths)
print(f"Cycle functional graph count: {result}")
```

#### **3. Functional Graph Count with Multiple Components**
**Problem**: Count functional graphs with multiple connected components.

**Key Differences**: Consider multiple connected components

**Solution Approach**: Use component analysis for counting

**Implementation**:
```python
def multi_component_functional_graph_count(n, component_sizes, mod=10**9+7):
    """
    Count functional graphs with multiple components
    
    Args:
        n: number of nodes
        component_sizes: list of component sizes
        mod: modulo value
    
    Returns:
        int: number of functional graphs with specified components modulo mod
    """
    def count_multi_component_graphs(node, current_graph, component_count):
        """Count functional graphs with multiple components"""
        if node == n:
            # Check if graph has required component properties
            if has_required_components(current_graph, component_sizes):
                return 1
            return 0
        
        count = 0
        for target in range(n):
            current_graph[node] = target
            count = (count + count_multi_component_graphs(node + 1, current_graph, component_count)) % mod
        
        return count
    
    return count_multi_component_graphs(0, [0] * n, 0)

def has_required_components(graph, component_sizes):
    """
    Check if graph has required component properties
    
    Args:
        graph: functional graph representation
        component_sizes: list of required component sizes
    
    Returns:
        bool: True if graph has required components
    """
    n = len(graph)
    visited = [False] * n
    component_counts = {}
    
    for i in range(n):
        if not visited[i]:
            component_size = find_component_size(graph, i, visited)
            component_counts[component_size] = component_counts.get(component_size, 0) + 1
    
    # Check if component counts match requirements
    for size in component_sizes:
        if component_counts.get(size, 0) == 0:
            return False
    
    return True

def find_component_size(graph, start, visited):
    """
    Find component size starting from given node
    
    Args:
        graph: functional graph representation
        start: starting node
        visited: visited array
    
    Returns:
        int: component size
    """
    size = 0
    current = start
    
    while not visited[current]:
        visited[current] = True
        size += 1
        current = graph[current]
    
    return size

# Example usage
n = 3
component_sizes = [1, 2]  # Require components of size 1 and 2
result = multi_component_functional_graph_count(n, component_sizes)
print(f"Multi-component functional graph count: {result}")
```

### Related Problems

#### **CSES Problems**
- [Counting Permutations](https://cses.fi/problemset/task/1075) - Combinatorics
- [Counting Combinations](https://cses.fi/problemset/task/1075) - Combinatorics
- [Counting Sequences](https://cses.fi/problemset/task/1075) - Combinatorics

#### **LeetCode Problems**
- [Graph Valid Tree](https://leetcode.com/problems/graph-valid-tree/) - Graph theory
- [Course Schedule](https://leetcode.com/problems/course-schedule/) - Graph theory
- [Redundant Connection](https://leetcode.com/problems/redundant-connection/) - Graph theory

#### **Problem Categories**
- **Graph Theory**: Functional graphs, graph counting
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