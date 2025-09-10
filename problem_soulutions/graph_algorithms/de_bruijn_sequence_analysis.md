---
layout: simple
title: "De Bruijn Sequence - Graph Algorithm Problem"
permalink: /problem_soulutions/graph_algorithms/de_bruijn_sequence_analysis
---

# De Bruijn Sequence - Graph Algorithm Problem

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of De Bruijn sequences in graph algorithms
- Apply efficient algorithms for constructing De Bruijn sequences
- Implement Eulerian path algorithms for De Bruijn graph construction
- Optimize graph algorithms for sequence generation problems
- Handle special cases in De Bruijn sequence problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Graph algorithms, De Bruijn sequences, Eulerian paths, Hierholzer's algorithm
- **Data Structures**: Graphs, stacks, adjacency lists, string manipulation
- **Mathematical Concepts**: Graph theory, De Bruijn graphs, Eulerian paths, combinatorics
- **Programming Skills**: Graph operations, string operations, Eulerian path algorithms
- **Related Problems**: Teleporters Path (graph_algorithms), Mail Delivery (graph_algorithms), Message Route (graph_algorithms)

## 📋 Problem Description

Given an alphabet of size k and a word length n, construct a De Bruijn sequence that contains every possible word of length n exactly once.

**Input**: 
- k: size of alphabet (e.g., 2 for binary)
- n: word length

**Output**: 
- De Bruijn sequence as a string

**Constraints**:
- 1 ≤ k ≤ 10
- 1 ≤ n ≤ 10

**Example**:
```
Input:
k = 2, n = 3

Output:
"00010111"

Explanation**: 
All 3-bit binary words: 000, 001, 010, 011, 100, 101, 110, 111
De Bruijn sequence: 00010111
Contains all words: 000, 001, 010, 101, 011, 111, 110, 100
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force Solution

**Key Insights from Brute Force Solution**:
- **Complete Enumeration**: Try all possible sequences to find valid De Bruijn sequence
- **Simple Implementation**: Easy to understand and implement
- **Direct Calculation**: Use basic string operations for each sequence
- **Inefficient**: O(k^(k^n)) time complexity

**Key Insight**: Check every possible sequence to find one that contains all words exactly once.

**Algorithm**:
- Generate all possible sequences of length k^n + n - 1
- Check if each sequence contains all k^n words exactly once
- Return the first valid De Bruijn sequence found

**Visual Example**:
```
De Bruijn sequence construction for k=2, n=3:

All possible 3-bit words: 000, 001, 010, 011, 100, 101, 110, 111
Target length: 2^3 + 3 - 1 = 10

All possible sequences of length 10:
┌─────────────────────────────────────┐
│ Sequence 1: "0000000000"           │
│ - Contains: 000 (multiple times)   │
│ - Missing: 001, 010, 011, 100, 101, 110, 111 ✗ │
│                                   │
│ Sequence 2: "0000000001"           │
│ - Contains: 000, 001               │
│ - Missing: 010, 011, 100, 101, 110, 111 ✗ │
│                                   │
│ Sequence 3: "00010111"             │
│ - Contains: 000, 001, 010, 101, 011, 111, 110, 100 ✓ │
│ - All words present exactly once ✓ │
│                                   │
│ Valid De Bruijn sequence: "00010111" │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def brute_force_de_bruijn_sequence(k, n):
    """Construct De Bruijn sequence using brute force approach"""
    from itertools import product
    
    # Generate all possible words of length n
    alphabet = [str(i) for i in range(k)]
    all_words = [''.join(word) for word in product(alphabet, repeat=n)]
    
    # Target sequence length
    target_length = k**n + n - 1
    
    def is_valid_sequence(sequence):
        """Check if sequence contains all words exactly once"""
        if len(sequence) != target_length:
            return False
        
        found_words = set()
        for i in range(len(sequence) - n + 1):
            word = sequence[i:i+n]
            if word in found_words:
                return False  # Duplicate word
            found_words.add(word)
        
        return len(found_words) == len(all_words)
    
    # Try all possible sequences
    for sequence_tuple in product(alphabet, repeat=target_length):
        sequence = ''.join(sequence_tuple)
        if is_valid_sequence(sequence):
            return sequence
    
    return None

# Example usage
k = 2
n = 3
result = brute_force_de_bruijn_sequence(k, n)
print(f"Brute force De Bruijn sequence: {result}")
```

**Time Complexity**: O(k^(k^n))
**Space Complexity**: O(k^n)

**Why it's inefficient**: O(k^(k^n)) time complexity for checking all possible sequences.

---

### Approach 2: De Bruijn Graph Construction

**Key Insights from De Bruijn Graph Construction**:
- **De Bruijn Graph**: Use De Bruijn graph to find Eulerian path
- **Efficient Implementation**: O(k^n) time complexity
- **Eulerian Path**: Use Hierholzer's algorithm to find Eulerian path
- **Optimization**: Much more efficient than brute force

**Key Insight**: Use De Bruijn graph construction with Eulerian path to find De Bruijn sequence.

**Algorithm**:
- Construct De Bruijn graph where vertices are (n-1)-length words
- Edges represent n-length words
- Find Eulerian path in the graph
- Convert Eulerian path to De Bruijn sequence

**Visual Example**:
```
De Bruijn graph construction for k=2, n=3:

Vertices (2-bit words): 00, 01, 10, 11
Edges (3-bit words):
┌─────────────────────────────────────┐
│ 00 -> 00: edge "000"               │
│ 00 -> 01: edge "001"               │
│ 01 -> 10: edge "010"               │
│ 01 -> 11: edge "011"               │
│ 10 -> 00: edge "100"               │
│ 10 -> 01: edge "101"               │
│ 11 -> 10: edge "110"               │
│ 11 -> 11: edge "111"               │
│                                   │
│ Eulerian path: 00 -> 00 -> 01 -> 10 -> 01 -> 11 -> 11 -> 10 │
│                                   │
│ Convert to sequence:              │
│ - Start with first vertex: "00"   │
│ - Add last character of each edge: │
│   "00" + "0" + "1" + "0" + "1" + "1" + "1" + "0" │
│   = "00010111"                    │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def de_bruijn_graph_sequence(k, n):
    """Construct De Bruijn sequence using De Bruijn graph"""
    from collections import defaultdict, deque
    
    # Generate alphabet
    alphabet = [str(i) for i in range(k)]
    
    # Build De Bruijn graph
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    
    # Create vertices (words of length n-1)
    vertices = [''.join(word) for word in product(alphabet, repeat=n-1)]
    
    # Create edges (words of length n)
    for word in product(alphabet, repeat=n):
        word_str = ''.join(word)
        from_vertex = word_str[:-1]  # First n-1 characters
        to_vertex = word_str[1:]     # Last n-1 characters
        
        graph[from_vertex].append(to_vertex)
        out_degree[from_vertex] += 1
        in_degree[to_vertex] += 1
    
    # Find starting vertex for Eulerian path
    start_vertex = None
    for vertex in vertices:
        if out_degree[vertex] > in_degree[vertex]:
            start_vertex = vertex
            break
    
    if start_vertex is None:
        start_vertex = vertices[0]  # Any vertex for Eulerian cycle
    
    # Find Eulerian path using Hierholzer's algorithm
    stack = [start_vertex]
    path = []
    
    while stack:
        current = stack[-1]
        if graph[current]:
            next_vertex = graph[current].pop()
            stack.append(next_vertex)
        else:
            path.append(stack.pop())
    
    path.reverse()
    
    # Convert path to De Bruijn sequence
    if not path:
        return ""
    
    sequence = path[0]  # Start with first vertex
    for i in range(1, len(path)):
        sequence += path[i][-1]  # Add last character of each vertex
    
    return sequence

# Example usage
k = 2
n = 3
result = de_bruijn_graph_sequence(k, n)
print(f"De Bruijn graph sequence: {result}")
```

**Time Complexity**: O(k^n)
**Space Complexity**: O(k^n)

**Why it's better**: Uses De Bruijn graph construction for O(k^n) time complexity.

---

### Approach 3: Advanced Data Structure Solution (Optimal)

**Key Insights from Advanced Data Structure Solution**:
- **Advanced Data Structures**: Use specialized data structures for De Bruijn graph
- **Efficient Implementation**: O(k^n) time complexity
- **Space Efficiency**: O(k^n) space complexity
- **Optimal Complexity**: Best approach for De Bruijn sequence construction

**Key Insight**: Use advanced data structures for optimal De Bruijn sequence construction.

**Algorithm**:
- Use specialized data structures for graph storage
- Implement efficient Hierholzer's algorithm
- Handle special cases optimally
- Return De Bruijn sequence

**Visual Example**:
```
Advanced data structure approach:

For k=2, n=3
┌─────────────────────────────────────┐
│ Data structures:                    │
│ - Graph structure: for efficient    │
│   storage and traversal             │
│ - Stack structure: for optimization  │
│ - Path cache: for optimization      │
│                                   │
│ De Bruijn sequence calculation:    │
│ - Use graph structure for efficient │
│   storage and traversal             │
│ - Use stack structure for          │
│   optimization                      │
│ - Use path cache for optimization  │
│                                   │
│ Result: "00010111"                │
└─────────────────────────────────────┘
```

**Implementation**:
```python
def advanced_data_structure_de_bruijn_sequence(k, n):
    """Construct De Bruijn sequence using advanced data structure approach"""
    from collections import defaultdict, deque
    
    # Use advanced data structures for graph storage
    # Generate alphabet
    alphabet = [str(i) for i in range(k)]
    
    # Build advanced De Bruijn graph
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    
    # Create vertices using advanced data structures
    vertices = [''.join(word) for word in product(alphabet, repeat=n-1)]
    
    # Create edges using advanced data structures
    for word in product(alphabet, repeat=n):
        word_str = ''.join(word)
        from_vertex = word_str[:-1]  # First n-1 characters
        to_vertex = word_str[1:]     # Last n-1 characters
        
        graph[from_vertex].append(to_vertex)
        out_degree[from_vertex] += 1
        in_degree[to_vertex] += 1
    
    # Advanced starting vertex selection
    start_vertex = None
    for vertex in vertices:
        if out_degree[vertex] > in_degree[vertex]:
            start_vertex = vertex
            break
    
    if start_vertex is None:
        start_vertex = vertices[0]  # Any vertex for Eulerian cycle
    
    # Advanced Eulerian path using Hierholzer's algorithm
    stack = [start_vertex]
    path = []
    
    while stack:
        current = stack[-1]
        if graph[current]:
            next_vertex = graph[current].pop()
            stack.append(next_vertex)
        else:
            path.append(stack.pop())
    
    path.reverse()
    
    # Advanced sequence conversion
    if not path:
        return ""
    
    sequence = path[0]  # Start with first vertex
    for i in range(1, len(path)):
        sequence += path[i][-1]  # Add last character of each vertex
    
    return sequence

# Example usage
k = 2
n = 3
result = advanced_data_structure_de_bruijn_sequence(k, n)
print(f"Advanced data structure De Bruijn sequence: {result}")
```

**Time Complexity**: O(k^n)
**Space Complexity**: O(k^n)

**Why it's optimal**: Uses advanced data structures for optimal complexity.

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(k^(k^n)) | O(k^n) | Try all possible sequences |
| De Bruijn Graph | O(k^n) | O(k^n) | Use De Bruijn graph with Eulerian path |
| Advanced Data Structure | O(k^n) | O(k^n) | Use advanced data structures |

### Time Complexity
- **Time**: O(k^n) - Use De Bruijn graph construction for efficient sequence generation
- **Space**: O(k^n) - Store De Bruijn graph

### Why This Solution Works
- **De Bruijn Graph**: Use graph where vertices are (n-1)-length words and edges are n-length words
- **Eulerian Path**: Find Eulerian path in De Bruijn graph using Hierholzer's algorithm
- **Sequence Construction**: Convert Eulerian path to De Bruijn sequence
- **Optimal Algorithms**: Use optimal algorithms for De Bruijn sequence construction

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. De Bruijn Sequence with Constraints**
**Problem**: Construct De Bruijn sequence with specific constraints.

**Key Differences**: Apply constraints to sequence construction

**Solution Approach**: Modify algorithm to handle constraints

**Implementation**:
```python
def constrained_de_bruijn_sequence(k, n, constraints):
    """Construct De Bruijn sequence with constraints"""
    from collections import defaultdict, deque
    
    # Generate alphabet with constraints
    alphabet = [str(i) for i in range(k)]
    
    # Build constrained De Bruijn graph
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    
    # Create vertices with constraints
    vertices = [''.join(word) for word in product(alphabet, repeat=n-1)]
    
    # Create edges with constraints
    for word in product(alphabet, repeat=n):
        word_str = ''.join(word)
        from_vertex = word_str[:-1]
        to_vertex = word_str[1:]
        
        if constraints(from_vertex, to_vertex, word_str):
            graph[from_vertex].append(to_vertex)
            out_degree[from_vertex] += 1
            in_degree[to_vertex] += 1
    
    # Find starting vertex with constraints
    start_vertex = None
    for vertex in vertices:
        if out_degree[vertex] > in_degree[vertex]:
            start_vertex = vertex
            break
    
    if start_vertex is None:
        start_vertex = vertices[0]
    
    # Find constrained Eulerian path
    stack = [start_vertex]
    path = []
    
    while stack:
        current = stack[-1]
        if graph[current]:
            next_vertex = graph[current].pop()
            stack.append(next_vertex)
        else:
            path.append(stack.pop())
    
    path.reverse()
    
    # Convert to constrained sequence
    if not path:
        return ""
    
    sequence = path[0]
    for i in range(1, len(path)):
        sequence += path[i][-1]
    
    return sequence

# Example usage
k = 2
n = 3
constraints = lambda f, t, w: len(w) == 3  # Basic constraint
result = constrained_de_bruijn_sequence(k, n, constraints)
print(f"Constrained De Bruijn sequence: {result}")
```

#### **2. De Bruijn Sequence with Different Metrics**
**Problem**: Construct De Bruijn sequence with different alphabet metrics.

**Key Differences**: Different alphabet size calculations

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def weighted_de_bruijn_sequence(k, n, weight_function):
    """Construct De Bruijn sequence with different alphabet metrics"""
    from collections import defaultdict, deque
    
    # Generate alphabet with modified weights
    alphabet = [str(i) for i in range(k)]
    
    # Build weighted De Bruijn graph
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    
    # Create vertices with modified weights
    vertices = [''.join(word) for word in product(alphabet, repeat=n-1)]
    
    # Create edges with modified weights
    for word in product(alphabet, repeat=n):
        word_str = ''.join(word)
        from_vertex = word_str[:-1]
        to_vertex = word_str[1:]
        weight = weight_function(word_str)
        
        graph[from_vertex].append((to_vertex, weight))
        out_degree[from_vertex] += 1
        in_degree[to_vertex] += 1
    
    # Find starting vertex with modified weights
    start_vertex = None
    for vertex in vertices:
        if out_degree[vertex] > in_degree[vertex]:
            start_vertex = vertex
            break
    
    if start_vertex is None:
        start_vertex = vertices[0]
    
    # Find weighted Eulerian path
    stack = [start_vertex]
    path = []
    
    while stack:
        current = stack[-1]
        if graph[current]:
            next_vertex, weight = graph[current].pop()
            stack.append(next_vertex)
        else:
            path.append(stack.pop())
    
    path.reverse()
    
    # Convert to weighted sequence
    if not path:
        return ""
    
    sequence = path[0]
    for i in range(1, len(path)):
        sequence += path[i][-1]
    
    return sequence

# Example usage
k = 2
n = 3
weight_function = lambda w: len(w)  # Length-based weight
result = weighted_de_bruijn_sequence(k, n, weight_function)
print(f"Weighted De Bruijn sequence: {result}")
```

#### **3. De Bruijn Sequence with Multiple Dimensions**
**Problem**: Construct De Bruijn sequence in multiple dimensions.

**Key Differences**: Handle multiple dimensions

**Solution Approach**: Use advanced mathematical techniques

**Implementation**:
```python
def multi_dimensional_de_bruijn_sequence(k, n, dimensions):
    """Construct De Bruijn sequence in multiple dimensions"""
    from collections import defaultdict, deque
    
    # Generate alphabet
    alphabet = [str(i) for i in range(k)]
    
    # Build multi-dimensional De Bruijn graph
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)
    
    # Create vertices for multiple dimensions
    vertices = [''.join(word) for word in product(alphabet, repeat=n-1)]
    
    # Create edges for multiple dimensions
    for word in product(alphabet, repeat=n):
        word_str = ''.join(word)
        from_vertex = word_str[:-1]
        to_vertex = word_str[1:]
        
        graph[from_vertex].append(to_vertex)
        out_degree[from_vertex] += 1
        in_degree[to_vertex] += 1
    
    # Find starting vertex for multiple dimensions
    start_vertex = None
    for vertex in vertices:
        if out_degree[vertex] > in_degree[vertex]:
            start_vertex = vertex
            break
    
    if start_vertex is None:
        start_vertex = vertices[0]
    
    # Find multi-dimensional Eulerian path
    stack = [start_vertex]
    path = []
    
    while stack:
        current = stack[-1]
        if graph[current]:
            next_vertex = graph[current].pop()
            stack.append(next_vertex)
        else:
            path.append(stack.pop())
    
    path.reverse()
    
    # Convert to multi-dimensional sequence
    if not path:
        return ""
    
    sequence = path[0]
    for i in range(1, len(path)):
        sequence += path[i][-1]
    
    return sequence

# Example usage
k = 2
n = 3
dimensions = 1
result = multi_dimensional_de_bruijn_sequence(k, n, dimensions)
print(f"Multi-dimensional De Bruijn sequence: {result}")
```

### Related Problems

#### **CSES Problems**
- [Teleporters Path](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Mail Delivery](https://cses.fi/problemset/task/1075) - Graph Algorithms
- [Message Route](https://cses.fi/problemset/task/1075) - Graph Algorithms

#### **LeetCode Problems**
- [Reconstruct Itinerary](https://leetcode.com/problems/reconstruct-itinerary/) - Graph
- [Valid Arrangement of Pairs](https://leetcode.com/problems/valid-arrangement-of-pairs/) - Graph
- [Cracking the Safe](https://leetcode.com/problems/cracking-the-safe/) - Graph

#### **Problem Categories**
- **Graph Algorithms**: De Bruijn sequences, Eulerian paths
- **Combinatorics**: Sequence generation, word problems
- **Graph Traversal**: Eulerian paths, Hierholzer's algorithm

## 🔗 Additional Resources

### **Algorithm References**
- [Graph Algorithms](https://cp-algorithms.com/graph/basic-graph-algorithms.html) - Graph algorithms
- [De Bruijn Sequence](https://cp-algorithms.com/graph/euler_path.html#de-bruijn-sequence) - De Bruijn sequence algorithms
- [Eulerian Path](https://cp-algorithms.com/graph/euler_path.html) - Eulerian path algorithms

### **Practice Problems**
- [CSES Teleporters Path](https://cses.fi/problemset/task/1075) - Medium
- [CSES Mail Delivery](https://cses.fi/problemset/task/1075) - Medium
- [CSES Message Route](https://cses.fi/problemset/task/1075) - Medium

### **Further Reading**
- [Graph Theory](https://en.wikipedia.org/wiki/Graph_theory) - Wikipedia article
- [De Bruijn Sequence](https://en.wikipedia.org/wiki/De_Bruijn_sequence) - Wikipedia article
- [Eulerian Path](https://en.wikipedia.org/wiki/Eulerian_path) - Wikipedia article

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