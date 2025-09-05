---
layout: simple
title: "String Compression"
permalink: /problem_soulutions/string_algorithms/string_compression_analysis
---


# String Compression

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- [ ] **Objective 1**: Understand string compression problems and run-length encoding techniques
- [ ] **Objective 2**: Apply run-length encoding to compress strings by representing consecutive identical characters
- [ ] **Objective 3**: Implement efficient string compression algorithms with O(n) time complexity
- [ ] **Objective 4**: Optimize string compression using run-length encoding and character counting techniques
- [ ] **Objective 5**: Handle edge cases in string compression (single character, all different characters, empty string)

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: Run-length encoding, string compression, character counting, string processing, compression algorithms
- **Data Structures**: String data structures, character tracking, count tracking, compression tracking
- **Mathematical Concepts**: Compression theory, run-length mathematics, character frequency analysis, encoding theory
- **Programming Skills**: String manipulation, character counting, compression implementation, algorithm implementation
- **Related Problems**: String Functions (basic string operations), String algorithms, Compression problems

## 📋 Problem Description

Given a string s, find the shortest compressed representation of the string. The compressed string should represent the original string using the minimum number of characters.

This is a string algorithm problem where we need to compress a string by representing consecutive identical characters with a single character followed by its count. This is known as run-length encoding, which is a simple but effective compression technique.

**Input**: 
- First line: string s (the input string)

**Output**: 
- Print the compressed string

**Constraints**:
- 1 ≤ |s| ≤ 10⁵
- String contains only lowercase letters

**Example**:
```
Input:
aaabbbcc

Output:
a3b3c2
```

**Explanation**: 
The string "aaabbbcc" can be compressed as:
- "aaa" → "a3" (3 consecutive 'a's)
- "bbb" → "b3" (3 consecutive 'b's)
- "cc" → "c2" (2 consecutive 'c's)
- Final result: "a3b3c2"

## 🎯 Visual Example

### Input
```
String: "aaabbbcc"
```

### Compression Process
```
Step 1: Identify consecutive character groups
- Group 1: "aaa" (3 consecutive 'a's)
- Group 2: "bbb" (3 consecutive 'b's)
- Group 3: "cc" (2 consecutive 'c's)

Step 2: Compress each group
- "aaa" → "a3"
- "bbb" → "b3"
- "cc" → "c2"

Step 3: Combine results
- Final compressed string: "a3b3c2"
```

### Compression Visualization
```
Original: a a a b b b c c
Index:    0 1 2 3 4 5 6 7

Group 1: a a a
         a 3
         ✓ ✓ ✓

Group 2: b b b
         b 3
         ✓ ✓ ✓

Group 3: c c
         c 2
         ✓ ✓

Compressed: a3b3c2
```

### Key Insight
Run-length encoding works by:
1. Scanning the string from left to right
2. Counting consecutive identical characters
3. Replacing each group with character + count
4. Time complexity: O(n) for single pass
5. Space complexity: O(n) for output string

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

## 🔧 Implementation Details

### Time and Space Complexity
- **Time Complexity**: O(|s|) for run-length encoding
- **Space Complexity**: O(|s|) for storing the compressed string
- **Why it works**: Run-length encoding efficiently compresses consecutive identical characters by representing them as a single character followed by its count

### Key Implementation Points
- Iterate through the string and count consecutive identical characters
- Append the character and its count to the compressed string
- Handle edge cases like single characters and empty strings
- Optimize for strings with many consecutive identical characters

## 🎯 Key Insights

### Important Concepts and Patterns
- **Run-Length Encoding**: Simple but effective compression technique
- **String Compression**: Reducing the size of string representations
- **Character Counting**: Efficiently counting consecutive identical characters
- **Data Compression**: Techniques for reducing data size

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. String Compression with Custom Format**
```python
def string_compression_custom_format(s, format_type="standard"):
    # Compress string with different formats
    if not s:
        return ""
    
    compressed = []
    current_char = s[0]
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == current_char:
            count += 1
        else:
            if format_type == "standard":
                compressed.append(f"{current_char}{count}")
            elif format_type == "brackets":
                compressed.append(f"[{current_char}{count}]")
            elif format_type == "parentheses":
                compressed.append(f"({current_char},{count})")
            elif format_type == "colon":
                compressed.append(f"{current_char}:{count}")
            
            current_char = s[i]
            count = 1
    
    # Add the last character
    if format_type == "standard":
        compressed.append(f"{current_char}{count}")
    elif format_type == "brackets":
        compressed.append(f"[{current_char}{count}]")
    elif format_type == "parentheses":
        compressed.append(f"({current_char},{count})")
    elif format_type == "colon":
        compressed.append(f"{current_char}:{count}")
    
    return "".join(compressed)

# Example usage
s = "aaabbbcc"
formats = ["standard", "brackets", "parentheses", "colon"]
for fmt in formats:
    result = string_compression_custom_format(s, fmt)
    print(f"{fmt}: {result}")
```

#### **2. String Compression with Threshold**
```python
def string_compression_with_threshold(s, threshold=2):
    # Only compress if count is above threshold
    if not s:
        return ""
    
    compressed = []
    current_char = s[0]
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == current_char:
            count += 1
        else:
            if count >= threshold:
                compressed.append(f"{current_char}{count}")
            else:
                # Add characters individually if below threshold
                compressed.append(current_char * count)
            
            current_char = s[i]
            count = 1
    
    # Add the last character
    if count >= threshold:
        compressed.append(f"{current_char}{count}")
    else:
        compressed.append(current_char * count)
    
    return "".join(compressed)

# Example usage
s = "aaabbbcc"
thresholds = [1, 2, 3, 4]
for threshold in thresholds:
    result = string_compression_with_threshold(s, threshold)
    print(f"Threshold {threshold}: {result}")
```

#### **3. String Compression with Decompression**
```python
def string_compression_with_decompression(s):
    # Compress and then decompress to verify
    def compress(s):
        if not s:
            return ""
        
        compressed = []
        current_char = s[0]
        count = 1
        
        for i in range(1, len(s)):
            if s[i] == current_char:
                count += 1
            else:
                compressed.append(f"{current_char}{count}")
                current_char = s[i]
                count = 1
        
        compressed.append(f"{current_char}{count}")
        return "".join(compressed)
    
    def decompress(compressed):
        if not compressed:
            return ""
        
        result = []
        i = 0
        
        while i < len(compressed):
            char = compressed[i]
            i += 1
            
            # Extract count
            count_str = ""
            while i < len(compressed) and compressed[i].isdigit():
                count_str += compressed[i]
                i += 1
            
            count = int(count_str) if count_str else 1
            result.append(char * count)
        
        return "".join(result)
    
    compressed = compress(s)
    decompressed = decompress(compressed)
    
    return compressed, decompressed, s == decompressed

# Example usage
s = "aaabbbcc"
compressed, decompressed, is_valid = string_compression_with_decompression(s)
print(f"Original: {s}")
print(f"Compressed: {compressed}")
print(f"Decompressed: {decompressed}")
print(f"Valid: {is_valid}")
```

#### **4. String Compression with Statistics**
```python
def string_compression_with_statistics(s):
    # Compress string and provide compression statistics
    if not s:
        return "", {"original_length": 0, "compressed_length": 0, "compression_ratio": 0}
    
    compressed = []
    current_char = s[0]
    count = 1
    
    for i in range(1, len(s)):
        if s[i] == current_char:
            count += 1
        else:
            compressed.append(f"{current_char}{count}")
            current_char = s[i]
            count = 1
    
    compressed.append(f"{current_char}{count}")
    compressed_str = "".join(compressed)
    
    # Calculate statistics
    original_length = len(s)
    compressed_length = len(compressed_str)
    compression_ratio = compressed_length / original_length if original_length > 0 else 0
    
    statistics = {
        "original_length": original_length,
        "compressed_length": compressed_length,
        "compression_ratio": compression_ratio,
        "space_saved": original_length - compressed_length,
        "compression_percentage": (1 - compression_ratio) * 100
    }
    
    return compressed_str, statistics

# Example usage
s = "aaabbbcc"
compressed, stats = string_compression_with_statistics(s)
print(f"Compressed: {compressed}")
print(f"Statistics: {stats}")
```

## 🔗 Related Problems

### Links to Similar Problems
- **String Algorithms**: String manipulation, String processing
- **Data Compression**: Run-length encoding, Huffman coding
- **String Analysis**: Character frequency, String statistics
- **String Optimization**: String efficiency, String performance

## 📚 Learning Points

### Key Takeaways
- **Run-length encoding** is a simple but effective compression technique
- **String compression** can significantly reduce storage requirements
- **Character counting** is essential for efficient compression
- **Data compression** is important for optimizing storage and transmission

---

*This analysis demonstrates efficient string compression techniques and shows various extensions for data compression problems.* 