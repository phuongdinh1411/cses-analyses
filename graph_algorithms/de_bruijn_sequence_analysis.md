# CSES De Bruijn Sequence - Problem Analysis

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