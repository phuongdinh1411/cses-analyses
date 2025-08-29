---
layout: simple
title: "De Bruijn Sequence"
permalink: /cses-analyses/problem_soulutions/graph_algorithms/de_bruijn_sequence_analysis
---


# De Bruijn Sequence

## Problem Statement
Given an integer n, construct a De Bruijn sequence of order n, which is a cyclic sequence of length 2^n containing all possible binary strings of length n as substrings.

### Input
The first input line has one integer n: the order of the De Bruijn sequence.

### Output
Print a De Bruijn sequence of order n.

### Constraints
- 1 ≤ n ≤ 20

### Example
```
Input:
2

Output:
0011
```

## Solution Progression
### Approach 1: Hierholzer's Algorithm on De Bruijn Graph - O(2^n)
**Description**: Use Hierholzer's algorithm on the De Bruijn graph.

```python
def de_bruijn_sequence_naive(n):
    if n == 1:
        return "01"
    
    # Build De Bruijn graph
    # Nodes are binary strings of length n-1
    # Edges represent adding a bit
    adj = {}
    
    for i in range(2**(n-1)):
        # Convert to binary string of length n-1
        node = format(i, f'0{n-1}b')
        
        # Add edges for 0 and 1
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

**Why this is inefficient**: The implementation is correct but can be optimized for clarity.

### Improvement 1: Optimized De Bruijn Graph Construction - O(2^n)
**Description**: Use optimized De Bruijn graph construction with better representation.

```python
def de_bruijn_sequence_optimized(n):
    if n == 1:
        return "01"
    
    # Build De Bruijn graph more efficiently
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

**Why this improvement works**: We use optimized De Bruijn graph construction with Hierholzer's algorithm to find De Bruijn sequence efficiently.

## Final Optimal Solution

```python
n = int(input())

def construct_de_bruijn_sequence(n):
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

result = construct_de_bruijn_sequence(n)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| De Bruijn Graph | O(2^n) | O(2^n) | Use De Bruijn graph with Hierholzer's |
| Optimized De Bruijn | O(2^n) | O(2^n) | Optimized De Bruijn graph construction |

## Key Insights for Other Problems

### 1. **De Bruijn Graph**
**Principle**: Use De Bruijn graph to represent overlapping sequences.
**Applicable to**: Sequence problems, graph problems, string problems

### 2. **Eulerian Circuit on De Bruijn Graph**
**Principle**: Use Hierholzer's algorithm on De Bruijn graph to find sequence.
**Applicable to**: De Bruijn sequence problems, circuit problems, graph problems

### 3. **Binary String Manipulation**
**Principle**: Use binary string operations to build De Bruijn graph.
**Applicable to**: String problems, bit manipulation problems, graph problems

## Notable Techniques

### 1. **De Bruijn Graph Construction**
```python
def build_de_bruijn_graph(n):
    adj = {}
    
    for i in range(2**(n-1)):
        node = format(i, f'0{n-1}b')
        next_node_0 = node[1:] + '0'
        next_node_1 = node[1:] + '1'
        
        if node not in adj:
            adj[node] = []
        adj[node].extend([next_node_0, next_node_1])
    
    return adj
```

### 2. **Binary String Operations**
```python
def binary_string_operations(n):
    # Convert integer to binary string
    binary = format(n, f'0{n}b')
    
    # Shift and add bit
    shifted = binary[1:] + '0'
    
    return binary, shifted
```

### 3. **Sequence Construction**
```python
def construct_sequence_from_circuit(circuit):
    sequence = circuit[0]
    for i in range(1, len(circuit)):
        sequence += circuit[i][-1]
    return sequence
```

## Problem-Solving Framework

1. **Identify problem type**: This is a De Bruijn sequence problem
2. **Choose approach**: Use De Bruijn graph with Hierholzer's algorithm
3. **Build graph**: Create De Bruijn graph with binary strings as nodes
4. **Find circuit**: Use Hierholzer's algorithm to find Eulerian circuit
5. **Construct sequence**: Convert circuit to De Bruijn sequence
6. **Return result**: Output the constructed sequence

---

*This analysis shows how to efficiently construct De Bruijn sequences using graph algorithms.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: De Bruijn Sequence with Different Alphabets**
**Problem**: Construct De Bruijn sequence for alphabet of size k (not just binary).
```python
def de_bruijn_sequence_k_ary(n, k):
    # Construct De Bruijn sequence for alphabet {0, 1, ..., k-1}
    
    # Build De Bruijn graph
    adj = {}
    
    for i in range(k**(n-1)):
        # Convert to k-ary string
        node = ""
        temp = i
        for _ in range(n-1):
            node = str(temp % k) + node
            temp //= k
        
        # Add edges for all k symbols
        for symbol in range(k):
            next_node = node[1:] + str(symbol)
            if node not in adj:
                adj[node] = []
            adj[node].append(next_node)
    
    # Find Eulerian circuit using Hierholzer's algorithm
    def find_eulerian_circuit():
        start = "0" * (n-1)  # Start with all zeros
        
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

#### **Variation 2: De Bruijn Sequence with Constraints**
**Problem**: Construct De Bruijn sequence avoiding certain substrings.
```python
def constrained_de_bruijn_sequence(n, forbidden_substrings):
    # forbidden_substrings = set of substrings to avoid
    
    # Build De Bruijn graph
    adj = {}
    
    for i in range(2**(n-1)):
        node = format(i, f'0{n-1}b')
        next_node_0 = node[1:] + '0'
        next_node_1 = node[1:] + '1'
        
        # Check if adding 0 creates forbidden substring
        if node + '0' not in forbidden_substrings: if node not in 
adj: adj[node] = []
            adj[node].append(next_node_0)
        
        # Check if adding 1 creates forbidden substring
        if node + '1' not in forbidden_substrings: if node not in 
adj: adj[node] = []
            adj[node].append(next_node_1)
    
    # Find Eulerian circuit
    def find_eulerian_circuit():
        start = "0" * (n-1)
        
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
    
    return sequence if len(sequence) == 2**n else "IMPOSSIBLE"
```

#### **Variation 3: De Bruijn Sequence with Costs**
**Problem**: Each transition has a cost, find minimum cost De Bruijn sequence.
```python
def cost_based_de_bruijn_sequence(n, costs):
    # costs[(from_node, to_node)] = cost of transition
    
    # Build De Bruijn graph with costs
    adj = {}
    
    for i in range(2**(n-1)):
        node = format(i, f'0{n-1}b')
        next_node_0 = node[1:] + '0'
        next_node_1 = node[1:] + '1'
        
        if node not in adj:
            adj[node] = []
        
        cost_0 = costs.get((node, next_node_0), 0)
        cost_1 = costs.get((node, next_node_1), 0)
        
        adj[node].append((next_node_0, cost_0))
        adj[node].append((next_node_1, cost_1))
    
    # Find minimum cost Eulerian circuit
    def find_min_cost_circuit():
        start = "0" * (n-1)
        
        path = []
        stack = [start]
        total_cost = 0
        
        while stack:
            current = stack[-1]
            
            if current in adj and adj[current]:
                # Choose minimum cost edge
                min_cost_edge = min(adj[current], key=lambda x: x[1])
                next_node, cost = adj[current].pop(adj[current].index(min_cost_edge))
                stack.append(next_node)
                total_cost += cost
            else:
                path.append(stack.pop())
        
        return path[::-1], total_cost
    
    circuit, cost = find_min_cost_circuit()
    
    # Convert to sequence
    sequence = circuit[0]
    for i in range(1, len(circuit)):
        sequence += circuit[i][-1]
    
    return sequence, cost
```

#### **Variation 4: De Bruijn Sequence with Probabilities**
**Problem**: Each transition has a success probability, find most reliable De Bruijn sequence.
```python
def probabilistic_de_bruijn_sequence(n, probabilities):
    # probabilities[(from_node, to_node)] = probability of successful transition
    
    # Build De Bruijn graph with probabilities
    adj = {}
    
    for i in range(2**(n-1)):
        node = format(i, f'0{n-1}b')
        next_node_0 = node[1:] + '0'
        next_node_1 = node[1:] + '1'
        
        if node not in adj:
            adj[node] = []
        
        prob_0 = probabilities.get((node, next_node_0), 0.5)
        prob_1 = probabilities.get((node, next_node_1), 0.5)
        
        adj[node].append((next_node_0, prob_0))
        adj[node].append((next_node_1, prob_1))
    
    # Find most reliable Eulerian circuit
    def find_most_reliable_circuit():
        start = "0" * (n-1)
        
        path = []
        stack = [start]
        total_probability = 1.0
        
        while stack:
            current = stack[-1]
            
            if current in adj and adj[current]:
                # Choose maximum probability edge
                max_prob_edge = max(adj[current], key=lambda x: x[1])
                next_node, prob = adj[current].pop(adj[current].index(max_prob_edge))
                stack.append(next_node)
                total_probability *= prob
            else:
                path.append(stack.pop())
        
        return path[::-1], total_probability
    
    circuit, probability = find_most_reliable_circuit()
    
    # Convert to sequence
    sequence = circuit[0]
    for i in range(1, len(circuit)):
        sequence += circuit[i][-1]
    
    return sequence, probability
```

#### **Variation 5: De Bruijn Sequence with Dynamic Updates**
**Problem**: Handle dynamic updates to transition costs/probabilities and find optimal sequence.
```python
def dynamic_de_bruijn_sequence(n, initial_costs, updates):
    # updates = [(edge, new_cost), ...]
    
    costs = initial_costs.copy()
    results = []
    
    for edge, new_cost in updates:
        # Update cost
        costs[edge] = new_cost
        
        # Rebuild graph with updated costs
        adj = {}
        
        for i in range(2**(n-1)):
            node = format(i, f'0{n-1}b')
            next_node_0 = node[1:] + '0'
            next_node_1 = node[1:] + '1'
            
            if node not in adj:
                adj[node] = []
            
            cost_0 = costs.get((node, next_node_0), 0)
            cost_1 = costs.get((node, next_node_1), 0)
            
            adj[node].append((next_node_0, cost_0))
            adj[node].append((next_node_1, cost_1))
        
        # Find minimum cost circuit
        def find_min_cost_circuit():
            start = "0" * (n-1)
            
            path = []
            stack = [start]
            total_cost = 0
            
            while stack:
                current = stack[-1]
                
                if current in adj and adj[current]:
                    min_cost_edge = min(adj[current], key=lambda x: x[1])
                    next_node, cost = adj[current].pop(adj[current].index(min_cost_edge))
                    stack.append(next_node)
                    total_cost += cost
                else:
                    path.append(stack.pop())
            
            return path[::-1], total_cost
        
        circuit, cost = find_min_cost_circuit()
        
        # Convert to sequence
        sequence = circuit[0]
        for i in range(1, len(circuit)):
            sequence += circuit[i][-1]
        
        results.append((sequence, cost))
    
    return results
```

### 🔗 **Related Problems & Concepts**

#### **1. Sequence Problems**
- **De Bruijn Sequences**: Sequences containing all substrings of given length
- **Gray Codes**: Sequences where adjacent elements differ by one bit
- **Lyndon Words**: Lexicographically smallest rotations
- **Necklaces**: Equivalence classes under rotation

#### **2. Graph Theory Problems**
- **Eulerian Circuits**: Circuits using each edge exactly once
- **De Bruijn Graphs**: Graphs representing overlapping sequences
- **Hamiltonian Cycles**: Cycles visiting each vertex exactly once
- **Graph Traversal**: Various graph traversal algorithms

#### **3. String Problems**
- **String Matching**: Find patterns in strings
- **String Compression**: Compress strings efficiently
- **String Generation**: Generate strings with properties
- **Substring Problems**: Problems involving substrings

#### **4. Combinatorial Problems**
- **Permutation Problems**: Problems involving permutations
- **Combination Problems**: Problems involving combinations
- **Enumeration Problems**: Enumerate objects with properties
- **Counting Problems**: Count objects with properties

#### **5. Algorithmic Techniques**
- **Hierholzer's Algorithm**: Find Eulerian circuits
- **Graph Construction**: Build graphs from problems
- **String Manipulation**: Manipulate strings efficiently
- **Bit Manipulation**: Efficient bit operations

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Lengths**
```python
t = int(input())
for _ in range(t):
    n = int(input())
    result = construct_de_bruijn_sequence(n)
    print(result)
```

#### **2. Range Queries on De Bruijn Sequences**
```python
def range_de_bruijn_queries(n_values):
    # n_values = [n1, n2, ...] - find sequences for different n values
    
    results = []
    for n in n_values:
        sequence = construct_de_bruijn_sequence(n)
        results.append(sequence)
    
    return results
```

#### **3. Interactive De Bruijn Sequence Problems**
```python
def interactive_de_bruijn_sequence():
    n = int(input("Enter n: "))
    sequence = construct_de_bruijn_sequence(n)
    print(f"De Bruijn sequence: {sequence}")
    
    # Verify the sequence
    substrings = set()
    for i in range(len(sequence) - n + 1):
        substrings.add(sequence[i:i+n])
    
    print(f"Number of unique {n}-length substrings: {len(substrings)}")
    print(f"Expected: {2**n}")
```

### 🧮 **Mathematical Extensions**

#### **1. Graph Theory**
- **De Bruijn Graph Properties**: Properties of De Bruijn graphs
- **Eulerian Graph Theory**: Theory of Eulerian graphs
- **Graph Enumeration**: Enumerate graphs with properties
- **Graph Isomorphism**: Check graph isomorphism

#### **2. Combinatorics**
- **Sequence Theory**: Mathematical theory of sequences
- **String Theory**: Theory of strings and languages
- **Enumeration Theory**: Theory of enumeration
- **Permutation Theory**: Theory of permutations

#### **3. Information Theory**
- **Coding Theory**: Theory of error-correcting codes
- **Compression Theory**: Theory of data compression
- **Entropy**: Measure of information content
- **Channel Capacity**: Maximum information transfer rate

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **De Bruijn Algorithms**: Various De Bruijn sequence algorithms
- **Graph Algorithms**: Eulerian circuit, traversal algorithms
- **String Algorithms**: String matching, compression algorithms
- **Combinatorial Algorithms**: Enumeration, counting algorithms

#### **2. Mathematical Concepts**
- **Graph Theory**: Properties and theorems about graphs
- **Combinatorics**: Combinatorial mathematics
- **Information Theory**: Mathematical theory of information
- **Number Theory**: Properties of numbers and sequences

#### **3. Programming Concepts**
- **Graph Representations**: Adjacency list vs adjacency matrix
- **String Manipulation**: Efficient string operations
- **Bit Manipulation**: Efficient bit operations
- **Algorithm Optimization**: Improving time and space complexity

---

*This analysis demonstrates efficient De Bruijn sequence techniques and shows various extensions for sequence construction problems.* 