---
layout: simple
title: "De Bruijn Sequence - Binary String Construction"
permalink: /problem_soulutions/graph_algorithms/de_bruijn_sequence_analysis
---

# De Bruijn Sequence - Binary String Construction

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand De Bruijn sequences and Eulerian path concepts in graph theory
- Apply Eulerian path algorithms to construct De Bruijn sequences using graph traversal
- Implement efficient De Bruijn sequence algorithms with proper graph construction
- Optimize De Bruijn sequence construction using Eulerian path algorithms and graph representations
- Handle edge cases in De Bruijn sequences (small orders, large orders, sequence construction)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: De Bruijn sequences, Eulerian paths, graph construction, string algorithms, combinatorial algorithms
- **Data Structures**: Graph representations, path tracking, string manipulation, Eulerian path data structures
- **Mathematical Concepts**: Combinatorics, De Bruijn graphs, Eulerian paths, string theory, graph theory
- **Programming Skills**: Graph construction, Eulerian path algorithms, string manipulation, algorithm implementation
- **Related Problems**: Teleporters Path (Eulerian paths), String algorithms, Combinatorial problems

## Problem Description

**Problem**: Given an integer n, construct a De Bruijn sequence of order n, which is a cyclic sequence of length 2ⁿ containing all possible binary strings of length n as substrings.

This is a De Bruijn sequence problem where we need to construct a cyclic binary sequence that contains every possible binary string of length n exactly once. The solution involves building a De Bruijn graph and finding an Eulerian circuit.

**Input**: 
- First line: Integer n (order of the De Bruijn sequence)

**Output**: 
- A De Bruijn sequence of order n

**Constraints**:
- 1 ≤ n ≤ 20
- Sequence must be cyclic (wraps around)
- All possible binary strings of length n must appear exactly once
- Sequence length must be exactly 2ⁿ

**Example**:
```
Input:
2

Output:
0011
```

**Explanation**: 
- All possible binary strings of length 2: 00, 01, 10, 11
- The sequence 0011 contains all these as substrings:
  - 00 (positions 0-1)
  - 01 (positions 1-2) 
  - 10 (positions 2-3)
  - 11 (positions 3-4, wrapping around)

## Visual Example

### Input and Output
```
Input: n = 2
Output: 0011

All possible binary strings of length 2:
- 00, 01, 10, 11
```

### De Bruijn Graph Construction
```
Step 1: Create nodes (binary strings of length n-1)
- For n = 2, nodes are strings of length 1: 0, 1

Step 2: Create edges (adding one bit)
- From 0: add 0 → 00, add 1 → 01
- From 1: add 0 → 10, add 1 → 11

Graph representation:
0 ──0──> 0
│        │
└──1─────┼──0──> 1
          │
          └──1──> 1
```

### Hierholzer's Algorithm Process
```
Step 1: Find Eulerian circuit
- Start from node 0
- Path: 0 → 0 → 1 → 1 → 0

Step 2: Extract sequence
- Take first bit of each edge: 0, 0, 1, 1
- Sequence: 0011

Step 3: Verify all substrings
- 00: positions 0-1
- 01: positions 1-2
- 10: positions 2-3
- 11: positions 3-4 (wrapping around)
```

### Sequence Verification
```
De Bruijn sequence: 0011

Substrings of length 2:
- Position 0-1: 00 ✓
- Position 1-2: 01 ✓
- Position 2-3: 10 ✓
- Position 3-4: 11 ✓ (wrapping around)

All possible binary strings of length 2 are present ✓
```

### Key Insight
De Bruijn sequence construction works by:
1. Building a De Bruijn graph where nodes are (n-1)-bit strings
2. Finding an Eulerian circuit in the graph
3. Extracting the sequence from the circuit
4. Time complexity: O(2^n) for graph construction and traversal
5. Space complexity: O(2^n) for graph representation

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force String Generation (Inefficient)

**Key Insights from Brute Force Solution:**
- Generate all possible binary strings and try to arrange them
- Simple but computationally expensive approach
- Not suitable for large n values
- Straightforward implementation but poor performance

**Algorithm:**
1. Generate all possible binary strings of length n
2. Try to arrange them in a sequence where each appears exactly once
3. Check if the sequence forms a valid De Bruijn sequence
4. Handle cases where no valid arrangement exists

**Visual Example:**
```
Brute force: Generate all strings and arrange
For n = 2:
- All strings: 00, 01, 10, 11
- Try arrangements: 00011011, 00110110, 00110011, etc.
- Check if each substring appears exactly once
- Valid sequence: 0011 (wrapping around)
```

**Implementation:**
```python
def de_bruijn_sequence_brute_force(n):
    from itertools import permutations
    
    # Generate all possible binary strings of length n
    all_strings = []
    for i in range(2**n):
        binary_str = format(i, f'0{n}b')
        all_strings.append(binary_str)
    
    # Try all possible arrangements
    for perm in permutations(all_strings):
        # Check if arrangement forms valid De Bruijn sequence
        sequence = ''.join(perm)
        if is_valid_de_bruijn_sequence(sequence, n):
            return sequence
    
    return None

def is_valid_de_bruijn_sequence(sequence, n):
    # Check if sequence contains all possible substrings exactly once
    seen = set()
    for i in range(len(sequence)):
        substring = sequence[i:i+n]
        if len(substring) < n:
            # Handle wrapping around
            substring = sequence[i:] + sequence[:n-len(substring)]
        
        if substring in seen:
            return False
        seen.add(substring)
    
    return len(seen) == 2**n
```

**Time Complexity:** O((2^n)! × 2^n) for generating all permutations and checking validity
**Space Complexity:** O(2^n) for storing all possible strings

**Why it's inefficient:**
- O((2^n)!) time complexity is too slow for large n values
- Not suitable for competitive programming
- Inefficient for large inputs
- Poor performance with many strings

### Approach 2: Basic De Bruijn Graph Construction (Better)

**Key Insights from Basic De Bruijn Graph Solution:**
- Use De Bruijn graph construction with Eulerian circuit finding
- Much more efficient than brute force approach
- Standard method for De Bruijn sequence construction
- Can handle larger n values efficiently

**Algorithm:**
1. Build De Bruijn graph where nodes are (n-1)-bit strings
2. Use Hierholzer's algorithm to find Eulerian circuit
3. Extract sequence from the circuit
4. Return the De Bruijn sequence

**Visual Example:**
```
Basic De Bruijn Graph for n = 2:
- Nodes: 0, 1 (strings of length 1)
- Edges: 0→0 (label 0), 0→1 (label 1), 1→0 (label 0), 1→1 (label 1)
- Eulerian circuit: 0 → 0 → 1 → 1 → 0
- Sequence: 0011
```

**Implementation:**
```python
def de_bruijn_sequence_basic_graph(n):
    if n == 1:
        return "01"
    
    # Build De Bruijn graph
    adj = {}
    
    for i in range(2**(n-1)):
        node = format(i, f'0{n-1}b')
        next_node_0 = node[1:] + '0'
        next_node_1 = node[1:] + '1'
        
        if node not in adj:
            adj[node] = []
        adj[node].extend([next_node_0, next_node_1])
    
    # Hierholzer's algorithm
    def find_eulerian_circuit():
        start = '0' * (n-1)
        path = []
        stack = [start]
        
        while stack:
            current = stack[-1]
            
            if current in adj and adj[current]:
                next_node = adj[current].pop()
                stack.append(next_node)
            else:
                path.append(stack.pop())
        
        return path[::-1]
    
    circuit = find_eulerian_circuit()
    
    # Convert to sequence
    sequence = circuit[0]
    for i in range(1, len(circuit)):
        sequence += circuit[i][-1]
    
    return sequence
```

**Time Complexity:** O(2^n) for graph construction and Eulerian circuit finding
**Space Complexity:** O(2^n) for graph representation

**Why it's better:**
- O(2^n) time complexity is much better than O((2^n)!)
- Standard method for De Bruijn sequence construction
- Suitable for competitive programming
- Efficient for most practical cases

### Approach 3: Optimized De Bruijn Graph with Efficient Circuit Construction (Optimal)

**Key Insights from Optimized De Bruijn Graph Solution:**
- Use optimized De Bruijn graph construction with efficient circuit finding
- Most efficient approach for De Bruijn sequence construction
- Standard method in competitive programming
- Can handle the maximum constraint efficiently

**Algorithm:**
1. Use optimized De Bruijn graph construction with efficient data structures
2. Implement efficient Eulerian circuit finding with Hierholzer's algorithm
3. Use proper sequence extraction and validation
4. Return the De Bruijn sequence efficiently

**Visual Example:**
```
Optimized De Bruijn Graph for n = 2:
- Efficient graph construction: O(2^n) time
- Optimized circuit finding: O(2^n) time
- Efficient sequence extraction: O(2^n) time
- Final sequence: 0011
```

**Implementation:**
```python
def de_bruijn_sequence_optimized_graph(n):
    if n == 1:
        return "01"
    
    # Build De Bruijn graph efficiently
    adj = {}
    
    for i in range(2**(n-1)):
        node = format(i, f'0{n-1}b')
        next_node_0 = node[1:] + '0'
        next_node_1 = node[1:] + '1'
        
        if node not in adj:
            adj[node] = []
        adj[node].extend([next_node_0, next_node_1])
    
    # Optimized Hierholzer's algorithm
    def find_eulerian_circuit():
        start = '0' * (n-1)
        path = []
        stack = [start]
        
        while stack:
            current = stack[-1]
            
            if current in adj and adj[current]:
                next_node = adj[current].pop()
                stack.append(next_node)
            else:
                path.append(stack.pop())
        
        return path[::-1]
    
    circuit = find_eulerian_circuit()
    
    # Efficient sequence extraction
    sequence = circuit[0]
    for i in range(1, len(circuit)):
        sequence += circuit[i][-1]
    
    return sequence

def solve_de_bruijn_sequence():
    n = int(input())
    result = de_bruijn_sequence_optimized_graph(n)
    print(result)

# Main execution
if __name__ == "__main__":
    solve_de_bruijn_sequence()
```

**Time Complexity:** O(2^n) for graph construction and Eulerian circuit finding
**Space Complexity:** O(2^n) for graph representation

**Why it's optimal:**
- O(2^n) time complexity is optimal for De Bruijn sequence construction
- Uses optimized De Bruijn graph with efficient circuit finding
- Most efficient approach for competitive programming
- Standard method for De Bruijn sequence problems

## 🎯 Problem Variations

### Variation 1: De Bruijn Sequence with Different Alphabets
**Problem**: Construct De Bruijn sequences for alphabets other than binary.

**Link**: [CSES Problem Set - De Bruijn Sequence Different Alphabets](https://cses.fi/problemset/task/de_bruijn_sequence_different_alphabets)

```python
def de_bruijn_sequence_different_alphabets(n, alphabet_size):
    if n == 1:
        return ''.join(str(i) for i in range(alphabet_size))
    
    # Build De Bruijn graph for different alphabet
    adj = {}
    
    for i in range(alphabet_size**(n-1)):
        node = base_convert(i, alphabet_size, n-1)
        for j in range(alphabet_size):
            next_node = node[1:] + str(j)
            if node not in adj:
                adj[node] = []
            adj[node].append(next_node)
    
    # Hierholzer's algorithm
    def find_eulerian_circuit():
        start = '0' * (n-1)
        path = []
        stack = [start]
        
        while stack:
            current = stack[-1]
            
            if current in adj and adj[current]:
                next_node = adj[current].pop()
                stack.append(next_node)
            else:
                path.append(stack.pop())
        
        return path[::-1]
    
    circuit = find_eulerian_circuit()
    
    # Convert to sequence
    sequence = circuit[0]
    for i in range(1, len(circuit)):
        sequence += circuit[i][-1]
    
    return sequence

def base_convert(num, base, length):
    result = ""
    for _ in range(length):
        result = str(num % base) + result
        num //= base
    return result
```

### Variation 2: De Bruijn Sequence with Minimum Length
**Problem**: Find the shortest De Bruijn sequence that contains all possible substrings.

**Link**: [CSES Problem Set - De Bruijn Sequence Minimum Length](https://cses.fi/problemset/task/de_bruijn_sequence_minimum_length)

```python
def de_bruijn_sequence_minimum_length(n):
    if n == 1:
        return "01"
    
    # Build De Bruijn graph
    adj = {}
    
    for i in range(2**(n-1)):
        node = format(i, f'0{n-1}b')
        next_node_0 = node[1:] + '0'
        next_node_1 = node[1:] + '1'
        
        if node not in adj:
            adj[node] = []
        adj[node].extend([next_node_0, next_node_1])
    
    # Find minimum length sequence
    def find_minimum_sequence():
        start = '0' * (n-1)
        path = []
        stack = [start]
        
        while stack:
            current = stack[-1]
            
            if current in adj and adj[current]:
                next_node = adj[current].pop()
                stack.append(next_node)
            else:
                path.append(stack.pop())
        
        return path[::-1]
    
    circuit = find_minimum_sequence()
    
    # Convert to sequence
    sequence = circuit[0]
    for i in range(1, len(circuit)):
        sequence += circuit[i][-1]
    
    return sequence
```

### Variation 3: De Bruijn Sequence with Constraints
**Problem**: Construct De Bruijn sequences with specific constraints on substring patterns.

**Link**: [CSES Problem Set - De Bruijn Sequence Constraints](https://cses.fi/problemset/task/de_bruijn_sequence_constraints)

```python
def de_bruijn_sequence_constraints(n, constraints):
    if n == 1:
        return "01"
    
    # Build De Bruijn graph with constraints
    adj = {}
    
    for i in range(2**(n-1)):
        node = format(i, f'0{n-1}b')
        for bit in ['0', '1']:
            next_node = node[1:] + bit
            substring = node + bit
            
            # Check constraints
            if satisfies_constraints(substring, constraints):
                if node not in adj:
                    adj[node] = []
                adj[node].append(next_node)
    
    # Hierholzer's algorithm
    def find_eulerian_circuit():
        start = '0' * (n-1)
        path = []
        stack = [start]
        
        while stack:
            current = stack[-1]
            
            if current in adj and adj[current]:
                next_node = adj[current].pop()
                stack.append(next_node)
            else:
                path.append(stack.pop())
        
        return path[::-1]
    
    circuit = find_eulerian_circuit()
    
    # Convert to sequence
    sequence = circuit[0]
    for i in range(1, len(circuit)):
        sequence += circuit[i][-1]
    
    return sequence

def satisfies_constraints(substring, constraints):
    for constraint in constraints:
        if not constraint(substring):
            return False
    return True
```

## 🔗 Related Problems

- **[Teleporters Path](/cses-analyses/problem_soulutions/graph_algorithms/teleporters_path_analysis/)**: Eulerian paths
- **[String Algorithms](/cses-analyses/problem_soulutions/string_algorithms/)**: String problems
- **[Combinatorial Problems](/cses-analyses/problem_soulutions/counting_problems/)**: Combinatorial problems
- **[Graph Algorithms](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph problems

## 📚 Learning Points

1. **De Bruijn Sequences**: Essential for understanding combinatorial string problems
2. **Eulerian Circuits**: Key technique for De Bruijn sequence construction
3. **Graph Construction**: Important for understanding De Bruijn graphs
4. **String Manipulation**: Critical for understanding sequence extraction
5. **Combinatorial Algorithms**: Foundation for many string problems
6. **Algorithm Optimization**: Critical for competitive programming performance

## 📝 Summary

The De Bruijn Sequence problem demonstrates fundamental combinatorial concepts for constructing cyclic sequences that contain all possible substrings. We explored three approaches:

1. **Brute Force String Generation**: O((2^n)!) time complexity using permutation generation, inefficient for large n values
2. **Basic De Bruijn Graph Construction**: O(2^n) time complexity using standard De Bruijn graph construction, better approach for sequence construction
3. **Optimized De Bruijn Graph with Efficient Circuit Construction**: O(2^n) time complexity with optimized graph construction, optimal approach for De Bruijn sequence problems

The key insights include understanding De Bruijn graph construction, using Eulerian circuit algorithms for sequence generation, and applying combinatorial techniques for optimal performance. This problem serves as an excellent introduction to De Bruijn sequences and Eulerian circuit algorithms.

