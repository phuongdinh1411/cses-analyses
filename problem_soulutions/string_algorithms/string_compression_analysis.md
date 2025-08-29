---
layout: simple
title: "String Compression"
permalink: /problem_soulutions/string_algorithms/string_compression_analysis
---


# String Compression

## Problem Statement
Given a string s, find the shortest compressed representation of the string. The compressed string should represent the original string using the minimum number of characters.

### Input
The first input line has a string s.

### Output
Print the compressed string.

### Constraints
- 1 ≤ |s| ≤ 10^5
- String contains only lowercase letters

### Example
```
Input:
aaabbbcc

Output:
a3b3c2
```

## Solution Progression

### Approach 1: Simple Run-Length Encoding - O(|s|)
**Description**: Use run-length encoding to compress consecutive identical characters.

```python
def string_compression_naive(s):
    if not s:
        return ""
    
    compressed = []
    current_char = s[0]
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == current_char:
            count += 1
        else:
            compressed.append(current_char)
            if count > 1:
                compressed.append(str(count))
            current_char = s[i]
            count = 1
    
    # Add the last group
    compressed.append(current_char)
    if count > 1:
        compressed.append(str(count))
    
    return ''.join(compressed)
```

**Why this is inefficient**: This is actually optimal for basic run-length encoding, but we can consider more advanced compression techniques.

### Improvement 1: Optimized Run-Length Encoding - O(|s|)
**Description**: Optimize the run-length encoding with better handling of edge cases.

```python
def string_compression_optimized(s):
    if not s:
        return ""
    
    compressed = []
    current_char = s[0]
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == current_char:
            count += 1
        else:
            compressed.append(current_char)
            if count > 1:
                compressed.append(str(count))
            current_char = s[i]
            count = 1
    
    # Add the last group
    compressed.append(current_char)
    if count > 1:
        compressed.append(str(count))
    
    return ''.join(compressed)
```

**Why this improvement works**: Better handling of edge cases and more efficient string building.

## Final Optimal Solution

```python
s = input().strip()

def compress_string(s):
    if not s:
        return ""
    
    compressed = []
    current_char = s[0]
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == current_char:
            count += 1
        else:
            compressed.append(current_char)
            if count > 1:
                compressed.append(str(count))
            current_char = s[i]
            count = 1
    
    # Add the last group
    compressed.append(current_char)
    if count > 1:
        compressed.append(str(count))
    
    return ''.join(compressed)

result = compress_string(s)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(|s|) | O(|s|) | Simple run-length encoding |
| Optimized | O(|s|) | O(|s|) | Optimized run-length encoding |

## Key Insights for Other Problems

### 1. **String Compression Problems**
**Principle**: Use run-length encoding for consecutive identical characters.
**Applicable to**: Compression problems, string encoding problems, data compression

### 2. **Run-Length Encoding**
**Principle**: Replace consecutive identical characters with character and count.
**Applicable to**: Compression algorithms, data encoding, string processing

### 3. **String Processing Patterns**
**Principle**: Process strings character by character with state tracking.
**Applicable to**: String algorithms, parsing problems, text processing

## Notable Techniques

### 1. **Run-Length Encoding**
```python
def run_length_encode(s):
    if not s:
        return ""
    
    compressed = []
    current_char = s[0]
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == current_char:
            count += 1
        else:
            compressed.append(current_char)
            if count > 1:
                compressed.append(str(count))
            current_char = s[i]
            count = 1
    
    compressed.append(current_char)
    if count > 1:
        compressed.append(str(count))
    
    return ''.join(compressed)
```

### 2. **Character Grouping**
```python
def group_consecutive_chars(s):
    groups = []
    if not s:
        return groups
    
    current_char = s[0]
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == current_char:
            count += 1
        else:
            groups.append((current_char, count))
            current_char = s[i]
            count = 1
    
    groups.append((current_char, count))
    return groups
```

### 3. **Compression Ratio Check**
```python
def compression_ratio(original, compressed):
    return len(compressed) / len(original)
```

## Problem-Solving Framework

1. **Identify problem type**: This is a string compression problem
2. **Choose approach**: Use run-length encoding for consecutive characters
3. **Process string**: Track current character and count
4. **Build result**: Append character and count to compressed string
5. **Return result**: Output the compressed string

---

*This analysis shows how to efficiently compress strings using run-length encoding.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: String Compression with Different Encodings**
**Problem**: Implement various compression algorithms (LZ77, LZ78, Huffman).
```python
def lz77_compression(s):
    # LZ77 compression with sliding window
    window_size = 4096
    lookahead_size = 64
    compressed = []
    i = 0
    
    while i < len(s):
        # Find longest match in sliding window
        start = max(0, i - window_size)
        window = s[start:i]
        lookahead = s[i:i + lookahead_size]
        
        # Find longest common prefix
        max_len = 0
        max_offset = 0
        
        for j in range(len(window)):
            k = 0
            while k < len(lookahead) and j + k < len(window) and window[j + k] == lookahead[k]:
                k += 1
            if k > max_len:
                max_len = k
                max_offset = len(window) - j
        
        if max_len > 2:
            compressed.append((max_offset, max_len, lookahead[max_len] if max_len < len(lookahead) else ''))
            i += max_len + 1
        else:
            compressed.append((0, 0, s[i]))
            i += 1
    
    return compressed
```

#### **Variation 2: String Compression with Constraints**
**Problem**: Compress strings with constraints on compression ratio or output format.
```python
def constrained_compression(s, max_ratio=0.5, min_run=2):
    # Compress with constraints on compression ratio and minimum run length
    
    compressed = []
    current_char = s[0]
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == current_char:
            count += 1
        else: if count >= 
min_run: compressed.append(current_char + str(count))
            else:
                compressed.append(current_char * count)
            current_char = s[i]
            count = 1
    
    # Handle last group
    if count >= min_run:
        compressed.append(current_char + str(count))
    else:
        compressed.append(current_char * count)
    
    result = ''.join(compressed)
    
    # Check compression ratio constraint
    if len(result) / len(s) > max_ratio:
        return s  # Return original if compression ratio is too high
    
    return result
```

#### **Variation 3: String Compression with Probabilities**
**Problem**: Compress strings with probabilistic character distributions.
```python
def probabilistic_compression(s, char_probs):
    # char_probs[c] = probability of character c
    
    # Use Huffman coding for probabilistic compression
    from heapq import heappush, heappop
    
    # Build frequency table
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    
    # Build Huffman tree
    heap = [(freq[c], c) for c in freq]
    heap.sort()
    
    while len(heap) > 1:
        f1, c1 = heap.pop(0)
        f2, c2 = heap.pop(0)
        heap.append((f1 + f2, (c1, c2)))
        heap.sort()
    
    # Build encoding table
    encoding = {}
    def build_encoding(node, code=""):
        if isinstance(node, str):
            encoding[node] = code
        else:
            build_encoding(node[0], code + "0")
            build_encoding(node[1], code + "1")
    
    if heap:
        build_encoding(heap[0][1])
    
    # Compress string
    compressed = ''.join(encoding[c] for c in s)
    return compressed, encoding
```

#### **Variation 4: String Compression with Multiple Algorithms**
**Problem**: Try multiple compression algorithms and choose the best one.
```python
def multi_algorithm_compression(s):
    # Try different compression algorithms and return the best result
    
    algorithms = [
        ("RLE", run_length_encode),
        ("LZ77", lz77_compression),
        ("Constrained", lambda x: constrained_compression(x, 0.5, 2))
    ]
    
    best_result = s
    best_ratio = 1.0
    
    for name, algorithm in algorithms: 
try: result = algorithm(s)
            ratio = len(str(result)) / len(s)
            if ratio < best_ratio:
                best_ratio = ratio
                best_result = result
        except:
            continue
    
    return best_result, best_ratio
```

#### **Variation 5: String Compression with Updates**
**Problem**: Handle dynamic updates to the string and maintain compression.
```python
def dynamic_compression(s, updates):
    # updates = [(pos, new_char), ...]
    
    s = list(s)  # Convert to list for updates
    compressed_history = []
    
    for pos, new_char in updates:
        s[pos] = new_char
        # Recompress after each update
        compressed = run_length_encode(''.join(s))
        compressed_history.append(compressed)
    
    return compressed_history
```

### 🔗 **Related Problems & Concepts**

#### **1. Compression Algorithms**
- **Run-Length Encoding**: Simple compression for repeated characters
- **LZ77/LZ78**: Dictionary-based compression
- **Huffman Coding**: Variable-length encoding
- **Arithmetic Coding**: Advanced entropy coding

#### **2. String Processing**
- **String Matching**: Find patterns in strings
- **String Analysis**: Analyze string properties
- **String Transformation**: Transform strings efficiently
- **String Encoding**: Encode strings in different formats

#### **3. Data Compression**
- **Lossless Compression**: Preserve all information
- **Lossy Compression**: Allow some information loss
- **Entropy Coding**: Optimal encoding based on probabilities
- **Dictionary Compression**: Use repeated patterns

#### **4. Information Theory**
- **Entropy**: Measure of information content
- **Compression Ratio**: Ratio of compressed to original size
- **Redundancy**: Repeated or unnecessary information
- **Coding Theory**: Theory of efficient encoding

#### **5. Algorithmic Techniques**
- **Greedy Algorithms**: Make locally optimal choices
- **Dynamic Programming**: Solve optimization problems
- **Tree Structures**: Huffman trees, suffix trees
- **Hash Functions**: Fast string hashing

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Strings**
```python
t = int(input())
for _ in range(t):
    s = input().strip()
    compressed = run_length_encode(s)
    print(compressed)
```

#### **2. Compression Ratio Queries**
```python
def compression_ratio_queries(strings):
    results = []
    for s in strings:
        compressed = run_length_encode(s)
        ratio = len(compressed) / len(s)
        results.append((s, compressed, ratio))
    return results
```

#### **3. Interactive Compression Problems**
```python
def interactive_compression():
    while True:
        s = input("Enter string to compress (or 'quit' to exit): ")
        if s.lower() == 'quit':
            break
        
        compressed = run_length_encode(s)
        ratio = len(compressed) / len(s)
        print(f"Original: {s}")
        print(f"Compressed: {compressed}")
        print(f"Compression ratio: {
ratio: .2f}")
```

### 🧮 **Mathematical Extensions**

#### **1. Information Theory**
- **Shannon Entropy**: Theoretical limit of compression
- **Kolmogorov Complexity**: Algorithmic complexity of strings
- **Compression Bounds**: Lower bounds on compression
- **Coding Theory**: Optimal encoding schemes

#### **2. Compression Theory**
- **Universal Compression**: Compress without knowing source
- **Adaptive Compression**: Adapt to changing data
- **Context Compression**: Use context for better compression
- **Multi-dimensional Compression**: Compress multi-dimensional data

#### **3. Advanced Compression**
- **Burrows-Wheeler Transform**: String transformation for compression
- **Move-to-Front**: Adaptive encoding technique
- **Delta Encoding**: Encode differences between values
- **Predictive Compression**: Predict next values

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Compression Algorithms**: RLE, LZ77, LZ78, Huffman, Arithmetic
- **String Algorithms**: KMP, Boyer-Moore, Rabin-Karp
- **Data Structures**: Trees, heaps, hash tables
- **Encoding Schemes**: ASCII, Unicode, Base64

#### **2. Mathematical Concepts**
- **Information Theory**: Entropy, mutual information, channel capacity
- **Probability Theory**: Probability distributions, expected values
- **Combinatorics**: Counting, permutations, combinations
- **Number Theory**: Prime numbers, modular arithmetic

#### **3. Programming Concepts**
- **Memory Management**: Efficient storage and retrieval
- **Algorithm Optimization**: Improving compression performance
- **Error Handling**: Dealing with compression failures
- **Data Validation**: Ensuring compressed data integrity

---

*This analysis demonstrates efficient string compression techniques and shows various extensions for data compression problems.* 