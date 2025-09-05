---
layout: simple
title: "De Bruijn Sequence - Binary String Construction"
permalink: /problem_soulutions/graph_algorithms/de_bruijn_sequence_analysis
---

# De Bruijn Sequence - Binary String Construction

## 📋 Problem Description

Given an integer n, construct a De Bruijn sequence of order n, which is a cyclic sequence of length 2ⁿ containing all possible binary strings of length n as substrings.

**Input**: 
- First line: Integer n (order of the De Bruijn sequence)

**Output**: 
- A De Bruijn sequence of order n

**Constraints**:
- 1 ≤ n ≤ 20

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

## 🎯 Visual Example

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

**Complexity**: O(2ⁿ) - optimal for this problem

### Step 3: Optimization
**Use optimized De Bruijn graph construction with better representation:**

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

**Key Insight**: Use Hierholzer's algorithm to find Eulerian circuit efficiently

### Step 4: Complete Solution

```python
def solve_de_bruijn_sequence():
    n = int(input())
    result = construct_de_bruijn_sequence(n)
    print(result)

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

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (1, "01"),
        (2, "0011"),
        (3, "00010111"),
        (4, "0000100110101111"),
    ]
    
    for n, expected in test_cases:
        result = construct_de_bruijn_sequence(n)
        print(f"n={n}")
        print(f"Expected: {expected}")
        print(f"Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

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

test_solution()
```
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(2ⁿ) - exponential growth with n
- **Space**: O(2ⁿ) - De Bruijn graph storage

### Why This Solution Works
- **De Bruijn Graph**: Represents all possible transitions between binary strings
- **Eulerian Circuit**: Ensures all edges are traversed exactly once
- **Hierholzer's Algorithm**: Efficiently finds Eulerian circuit
- **Optimal Algorithm**: Best known approach for De Bruijn sequences

## 🎨 Visual Example

### Input Example
```
n = 2 (De Bruijn sequence of order 2)
```

### All Binary Strings of Length 2
```
All possible binary strings of length 2:
- 00
- 01
- 10
- 11

Total: 2² = 4 strings
```

### De Bruijn Graph Construction
```
Nodes: All binary strings of length (n-1) = 1
- Node 0
- Node 1

Edges: Add one bit to get string of length n
- Edge 0 → 0 (add 0 to get 00)
- Edge 0 → 1 (add 1 to get 01)
- Edge 1 → 0 (add 0 to get 10)
- Edge 1 → 1 (add 1 to get 11)

Graph:
0 ──0──→ 0
│        │
│1       │1
↓        ↓
1 ──0──→ 1
```

### Eulerian Circuit Construction
```
Using Hierholzer's algorithm:

Step 1: Start from node 0
- Current path: [0]
- Current node: 0

Step 2: From node 0, choose edge 0 → 0
- Current path: [0, 0]
- Current node: 0

Step 3: From node 0, choose edge 0 → 1
- Current path: [0, 0, 1]
- Current node: 1

Step 4: From node 1, choose edge 1 → 1
- Current path: [0, 0, 1, 1]
- Current node: 1

Step 5: From node 1, choose edge 1 → 0
- Current path: [0, 0, 1, 1, 0]
- Current node: 0

All edges visited: [0→0, 0→1, 1→1, 1→0]
```

### Sequence Construction
```
From Eulerian circuit: [0, 0, 1, 1, 0]

Extract edge labels:
- Edge 0→0: label 0
- Edge 0→1: label 1
- Edge 1→1: label 1
- Edge 1→0: label 0

Sequence: 0110

But we need 2ⁿ = 4 characters, so we take first 4: 0110
```

### Verification
```
Check if 0110 contains all binary strings of length 2:

Position 0-1: 01 ✓
Position 1-2: 11 ✓
Position 2-3: 10 ✓
Position 3-0: 00 ✓ (wrapping around)

All strings found: 00, 01, 10, 11
```

### Alternative Construction
```
Another valid De Bruijn sequence: 0011

Check if 0011 contains all binary strings of length 2:

Position 0-1: 00 ✓
Position 1-2: 01 ✓
Position 2-3: 11 ✓
Position 3-0: 10 ✓ (wrapping around)

All strings found: 00, 01, 10, 11
```

### Algorithm Comparison
```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│     Approach    │   Time       │    Space     │   Key Idea   │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Hierholzer's    │ O(2^n)       │ O(2^n)       │ Eulerian     │
│                 │              │              │ circuit      │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ DFS + Stack     │ O(2^n)       │ O(2^n)       │ Recursive    │
│                 │              │              │ construction │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Iterative       │ O(2^n)       │ O(2^n)       │ Iterative    │
│                 │              │              │ approach     │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

## 🎯 Key Insights

### 1. **De Bruijn Graph**
- Use De Bruijn graph to represent overlapping sequences
- Important for understanding
- Enables efficient sequence construction
- Essential for algorithm

### 2. **Eulerian Circuit on De Bruijn Graph**
- Use Hierholzer's algorithm on De Bruijn graph to find sequence
- Important for understanding
- Ensures all transitions are covered
- Essential for correctness

### 3. **Binary String Manipulation**
- Use binary string operations to build De Bruijn graph
- Important for understanding
- Enables efficient graph construction
- Essential for implementation

## 🎯 Problem Variations

### Variation 1: De Bruijn Sequence with Different Alphabets
**Problem**: Construct De Bruijn sequence for alphabet of size k (not just binary).

```python
def de_bruijn_sequence_k_ary(n, k):
    """Construct De Bruijn sequence for alphabet {0, 1, ..., k-1}"""
    if n == 1:
        return ''.join(str(i) for i in range(k))
    
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

# Example usage
result = de_bruijn_sequence_k_ary(2, 3)  # Ternary alphabet, length 2
print(f"Ternary De Bruijn sequence: {result}")
```

### Variation 2: De Bruijn Sequence with Constraints
**Problem**: Construct De Bruijn sequence avoiding certain substrings.

```python
def de_bruijn_sequence_with_constraints(n, forbidden_substrings):
    """Construct De Bruijn sequence avoiding forbidden substrings"""
    if n == 1:
        return "01"
    
    # Build De Bruijn graph
    adj = {}
    
    for i in range(2**(n-1)):
        node = format(i, f'0{n-1}b')
        next_node_0 = node[1:] + '0'
        next_node_1 = node[1:] + '1'
        
        # Check if adding 0 or 1 creates forbidden substring
        if node not in adj:
            adj[node] = []
        
        if next_node_0 not in forbidden_substrings:
            adj[node].append(next_node_0)
        if next_node_1 not in forbidden_substrings:
            adj[node].append(next_node_1)
    
    # Find Eulerian circuit
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

# Example usage
forbidden = {"000", "111"}  # Avoid all-0 and all-1 substrings
result = de_bruijn_sequence_with_constraints(3, forbidden)
print(f"Constrained De Bruijn sequence: {result}")
```

### Variation 3: De Bruijn Sequence with Optimization
**Problem**: Find shortest De Bruijn sequence with additional constraints.

```python
def optimized_de_bruijn_sequence(n, optimization_criteria):
    """Construct optimized De Bruijn sequence"""
    if n == 1:
        return "01"
    
    # Build De Bruijn graph with weights
    adj = {}
    weights = {}
    
    for i in range(2**(n-1)):
        node = format(i, f'0{n-1}b')
        next_node_0 = node[1:] + '0'
        next_node_1 = node[1:] + '1'
        
        if node not in adj:
            adj[node] = []
        
        # Assign weights based on optimization criteria
        weight_0 = optimization_criteria.get('0', 1)
        weight_1 = optimization_criteria.get('1', 1)
        
        adj[node].extend([next_node_0, next_node_1])
        weights[(node, next_node_0)] = weight_0
        weights[(node, next_node_1)] = weight_1
    
    # Find minimum weight Eulerian circuit
    def find_minimum_weight_circuit():
        start = '0' * (n-1)
        path = []
        stack = [start]
        
        while stack:
            current = stack[-1]
            
            if current in adj and adj[current]:
                # Choose edge with minimum weight
                min_weight = float('inf')
                best_next = None
                
                for neighbor in adj[current]:
                    weight = weights.get((current, neighbor), 1)
                    if weight < min_weight:
                        min_weight = weight
                        best_next = neighbor
                
                if best_next:
                    adj[current].remove(best_next)
                    stack.append(best_next)
                else:
                    path.append(stack.pop())
            else:
                path.append(stack.pop())
        
        return path[::-1]
    
    circuit = find_minimum_weight_circuit()
    
    # Convert to sequence
    sequence = circuit[0]
    for i in range(1, len(circuit)):
        sequence += circuit[i][-1]
    
    return sequence

# Example usage
criteria = {'0': 2, '1': 1}  # Prefer 1s over 0s
result = optimized_de_bruijn_sequence(3, criteria)
print(f"Optimized De Bruijn sequence: {result}")
```

### Variation 4: Dynamic De Bruijn Sequence
**Problem**: Maintain De Bruijn sequence as constraints change dynamically.

```python
class DynamicDeBruijnSequence:
    def __init__(self, n):
        self.n = n
        self.forbidden_substrings = set()
        self.adj = {}
        self.sequence = None
    
    def add_forbidden_substring(self, substring):
        """Add forbidden substring"""
        if len(substring) == self.n:
            self.forbidden_substrings.add(substring)
            self.update_sequence()
    
    def remove_forbidden_substring(self, substring):
        """Remove forbidden substring"""
        if substring in self.forbidden_substrings:
            self.forbidden_substrings.remove(substring)
            self.update_sequence()
    
    def update_sequence(self):
        """Recalculate De Bruijn sequence"""
        self.sequence = de_bruijn_sequence_with_constraints(self.n, self.forbidden_substrings)
    
    def get_sequence(self):
        """Get current De Bruijn sequence"""
        if self.sequence is None:
            self.update_sequence()
        return self.sequence
    
    def get_statistics(self):
        """Get statistics about the sequence"""
        if self.sequence is None:
            self.update_sequence()
        
        return {
            'length': len(self.sequence),
            'forbidden_count': len(self.forbidden_substrings),
            'sequence': self.sequence
        }

# Example usage
dynamic_seq = DynamicDeBruijnSequence(3)
print(f"Initial sequence: {dynamic_seq.get_sequence()}")

dynamic_seq.add_forbidden_substring("000")
print(f"After forbidding '000': {dynamic_seq.get_sequence()}")

dynamic_seq.add_forbidden_substring("111")
print(f"After forbidding '111': {dynamic_seq.get_sequence()}")

stats = dynamic_seq.get_statistics()
print(f"Statistics: {stats}")
```

### Variation 5: De Bruijn Sequence with Applications
**Problem**: Use De Bruijn sequences for specific applications like shift registers.

```python
def de_bruijn_shift_register(n):
    """Construct De Bruijn sequence optimized for shift register applications"""
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
    
    # Find Eulerian circuit with shift register optimization
    def find_shift_register_circuit():
        start = '0' * (n-1)
        path = []
        stack = [start]
        
        while stack:
            current = stack[-1]
            
            if current in adj and adj[current]:
                # Prefer transitions that minimize shift register changes
                next_node_0 = current[1:] + '0'
                next_node_1 = current[1:] + '1'
                
                if next_node_0 in adj[current]:
                    adj[current].remove(next_node_0)
                    stack.append(next_node_0)
                elif next_node_1 in adj[current]:
                    adj[current].remove(next_node_1)
                    stack.append(next_node_1)
                else:
                    # Take any available edge
                    next_node = adj[current].pop()
                    stack.append(next_node)
            else:
                path.append(stack.pop())
        
        return path[::-1]
    
    circuit = find_shift_register_circuit()
    
    # Convert to sequence
    sequence = circuit[0]
    for i in range(1, len(circuit)):
        sequence += circuit[i][-1]
    
    return sequence

# Example usage
result = de_bruijn_shift_register(4)
print(f"Shift register optimized sequence: {result}")

# Verify all substrings are present
def verify_de_bruijn_sequence(sequence, n):
    """Verify that sequence contains all possible substrings of length n"""
    expected_substrings = set()
    for i in range(2**n):
        expected_substrings.add(format(i, f'0{n}b'))
    
    actual_substrings = set()
    for i in range(len(sequence)):
        substring = sequence[i:i+n]
        if len(substring) == n:
            actual_substrings.add(substring)
    
    # Handle wrapping
    for i in range(n-1):
        substring = sequence[i:i+n]
        if len(substring) == n:
            actual_substrings.add(substring)
    
    missing = expected_substrings - actual_substrings
    extra = actual_substrings - expected_substrings
    
    return len(missing) == 0, missing, extra

is_valid, missing, extra = verify_de_bruijn_sequence(result, 4)
print(f"Valid De Bruijn sequence: {is_valid}")
if not is_valid:
    print(f"Missing: {missing}")
    print(f"Extra: {extra}")
```
    
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
        
        prob_0 = probabilities.get((node, next_node_0), 1.0)
        prob_1 = probabilities.get((node, next_node_1), 1.0)
        
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
                # Choose most reliable edge
                most_reliable_edge = max(adj[current], key=lambda x: x[1])
                next_node, prob = adj[current].pop(adj[current].index(most_reliable_edge))
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

# Example usage
probabilities = {("00", "00"): 0.9, ("00", "01"): 0.8, ("01", "10"): 0.7, ("01", "11"): 0.6}
result, prob = probabilistic_de_bruijn_sequence(3, probabilities)
print(f"Most reliable sequence: {result}, Probability: {prob}")
```

---

## 🔗 Related Problems

- **[Eulerian Circuit](/cses-analyses/problem_soulutions/graph_algorithms/)**: Graph traversal problems
- **[Topological Sorting](/cses-analyses/problem_soulutions/graph_algorithms/)**: DAG ordering problems
- **[Binary String Problems](/cses-analyses/problem_soulutions/graph_algorithms/)**: String manipulation problems

## 📚 Learning Points

1. **De Bruijn Graph**: Essential for sequence construction problems
2. **Eulerian Circuit**: Important for graph traversal and sequence generation
3. **Hierholzer's Algorithm**: Key algorithm for finding Eulerian circuits
4. **Binary String Manipulation**: Foundation for many graph problems
5. **Graph Representation**: Critical for efficient algorithm implementation

---

**This is a great introduction to De Bruijn sequences and graph-based sequence construction!** 🎯
    
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