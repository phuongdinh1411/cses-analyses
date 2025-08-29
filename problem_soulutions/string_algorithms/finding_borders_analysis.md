---
layout: simple
title: "Finding Borders"
permalink: /cses-analyses/problem_soulutions/string_algorithms/finding_borders_analysis
---


# Finding Borders

## Problem Statement
Given a string, find all borders of the string. A border is a proper prefix that is also a proper suffix.

### Input
The first input line has a string s.

### Output
Print all borders of the string in ascending order of length.

### Constraints
- 1 ≤ |s| ≤ 10^6

### Example
```
Input:
ababab

Output:
ab
abab
```

## Solution Progression

### Approach 1: Naive Border Finding - O(|s|²)
**Description**: Check each possible prefix to see if it's also a suffix.

```python
def finding_borders_naive(s):
    borders = []
    n = len(s)
    
    for length in range(1, n):
        prefix = s[:length]
        suffix = s[n - length:]
        if prefix == suffix:
            borders.append(prefix)
    
    return borders
```

**Why this is inefficient**: Quadratic time complexity for large strings.

### Improvement 1: KMP Failure Function - O(|s|)
**Description**: Use KMP failure function to find all borders efficiently.

```python
def compute_lps(s):
    n = len(s)
    lps = [0] * n
    length = 0
    i = 1
    
    while i < n:
        if s[i] == s[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    
    return lps

def finding_borders_kmp(s):
    borders = []
    n = len(s)
    lps = compute_lps(s)
    
    # Find all borders using LPS array
    length = lps[n - 1]
    while length > 0:
        borders.append(s[:length])
        length = lps[length - 1]
    
    return borders[::-1]  # Return in ascending order
```

**Why this improvement works**: KMP failure function directly gives us border lengths in linear time.

### Improvement 2: Z-Algorithm Approach - O(|s|)
**Description**: Use Z-algorithm to find borders by comparing string with itself.

```python
def compute_z_array(s):
    n = len(s)
    z = [0] * n
    l = r = 0
    
    for i in range(1, n):
        if i > r:
            l = r = i
            while r < n and s[r - l] == s[r]:
                r += 1
            z[i] = r - l
            r -= 1
        else:
            k = i - l
            if z[k] < r - i + 1:
                z[i] = z[k]
            else:
                l = i
                while r < n and s[r - l] == s[r]:
                    r += 1
                z[i] = r - l
                r -= 1
    
    return z

def finding_borders_z_algorithm(s):
    borders = []
    n = len(s)
    z = compute_z_array(s)
    
    # Find borders using Z-array
    for i in range(1, n):
        if z[i] == n - i:
            borders.append(s[:z[i]])
    
    return borders
```

**Why this improvement works**: Z-algorithm finds all positions where string matches its own suffix.

### Alternative: Rolling Hash Approach - O(|s|)
**Description**: Use rolling hash to compare prefixes and suffixes efficiently.

```python
def finding_borders_rolling_hash(s):
    borders = []
    n = len(s)
    
    # Simple hash function
    def hash_string(s):
        hash_val = 0
        for char in s:
            hash_val = (hash_val * 31 + ord(char)) % (10**9 + 7)
        return hash_val
    
    # Check each possible border length
    for length in range(1, n):
        prefix_hash = hash_string(s[:length])
        suffix_hash = hash_string(s[n - length:])
        
        if prefix_hash == suffix_hash and s[:length] == s[n - length:]:
            borders.append(s[:length])
    
    return borders
```

**Why this works**: Rolling hash provides fast comparison of prefixes and suffixes.

## Final Optimal Solution

```python
s = input().strip()

def compute_lps(s):
    n = len(s)
    lps = [0] * n
    length = 0
    i = 1
    
    while i < n:
        if s[i] == s[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    
    return lps

def finding_borders_kmp(s):
    borders = []
    n = len(s)
    lps = compute_lps(s)
    
    # Find all borders using LPS array
    length = lps[n - 1]
    while length > 0:
        borders.append(s[:length])
        length = lps[length - 1]
    
    return borders[::-1]  # Return in ascending order

borders = finding_borders_kmp(s)
for border in borders:
    print(border)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(|s|²) | O(|s|) | Simple but slow |
| KMP | O(|s|) | O(|s|) | Use failure function |
| Z-Algorithm | O(|s|) | O(|s|) | Z-array computation |
| Rolling Hash | O(|s|) | O(|s|) | Hash-based comparison |

## Key Insights for Other Problems

### 1. **Border Finding Problems**
**Principle**: Use KMP failure function or Z-algorithm to find borders efficiently.
**Applicable to**:
- Border finding problems
- String algorithms
- Pattern matching
- Algorithm design

**Example Problems**:
- Border finding problems
- String algorithms
- Pattern matching
- Algorithm design

### 2. **LPS Array Applications**
**Principle**: Use longest proper prefix that is also a suffix for border detection.
**Applicable to**:
- String algorithms
- Pattern matching
- Algorithm design
- Problem solving

**Example Problems**:
- String algorithms
- Pattern matching
- Algorithm design
- Problem solving

### 3. **Z-Array for Self-Matching**
**Principle**: Use Z-array to find positions where string matches its own suffix.
**Applicable to**:
- String algorithms
- Pattern matching
- Algorithm design
- Problem solving

**Example Problems**:
- String algorithms
- Pattern matching
- Algorithm design
- Problem solving

### 4. **Hash-based String Comparison**
**Principle**: Use rolling hash for efficient string comparison.
**Applicable to**:
- String algorithms
- Hash functions
- Algorithm design
- Problem solving

**Example Problems**:
- String algorithms
- Hash functions
- Algorithm design
- Problem solving

## Notable Techniques

### 1. **KMP Border Finding Pattern**
```python
def find_borders_kmp(s):
    def compute_lps(s):
        n = len(s)
        lps = [0] * n
        length = 0
        i = 1
        
        while i < n:
            if s[i] == s[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        
        return lps
    
    borders = []
    n = len(s)
    lps = compute_lps(s)
    
    length = lps[n - 1]
    while length > 0:
        borders.append(s[:length])
        length = lps[length - 1]
    
    return borders[::-1]
```

### 2. **Z-Algorithm Border Pattern**
```python
def find_borders_z_algorithm(s):
    def compute_z_array(s):
        n = len(s)
        z = [0] * n
        l = r = 0
        
        for i in range(1, n):
            if i > r:
                l = r = i
                while r < n and s[r - l] == s[r]:
                    r += 1
                z[i] = r - l
                r -= 1
            else:
                k = i - l
                if z[k] < r - i + 1:
                    z[i] = z[k]
                else:
                    l = i
                    while r < n and s[r - l] == s[r]:
                        r += 1
                    z[i] = r - l
                    r -= 1
        
        return z
    
    borders = []
    n = len(s)
    z = compute_z_array(s)
    
    for i in range(1, n):
        if z[i] == n - i:
            borders.append(s[:z[i]])
    
    return borders
```

### 3. **Rolling Hash Border Pattern**
```python
def find_borders_rolling_hash(s):
    def hash_string(s):
        hash_val = 0
        for char in s:
            hash_val = (hash_val * 31 + ord(char)) % (10**9 + 7)
        return hash_val
    
    borders = []
    n = len(s)
    
    for length in range(1, n):
        prefix_hash = hash_string(s[:length])
        suffix_hash = hash_string(s[n - length:])
        
        if prefix_hash == suffix_hash and s[:length] == s[n - length:]:
            borders.append(s[:length])
    
    return borders
```

## Edge Cases to Remember

1. **Empty string**: No borders
2. **Single character**: No borders
3. **All same characters**: Multiple borders
4. **No borders**: Return empty list
5. **Multiple borders**: Return all in ascending order

## Problem-Solving Framework

1. **Identify border nature**: This is a border finding problem
2. **Choose algorithm**: Use KMP failure function for efficiency
3. **Compute LPS**: Build longest proper prefix that is also a suffix array
4. **Extract borders**: Use LPS array to find all border lengths
5. **Return result**: Return borders in ascending order

---

*This analysis shows how to efficiently find borders using KMP failure function and other string algorithms.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Finding Borders with Constraints**
**Problem**: Find borders with additional constraints (length, alphabet, etc.).
```python
def constrained_finding_borders(s, constraints):
    # constraints = {'min_length': x, 'max_length': y, 'alphabet': chars}
    
    n = len(s)
    
    # Apply constraints
    if 'alphabet' in constraints:
        if not all(c in constraints['alphabet'] for c in s):
            return []
    
    # Use KMP failure function
    borders = []
    lps = compute_lps(s)
    
    length = lps[n - 1]
    while length > 0:
        # Apply length constraints
        if 'min_length' in constraints and length < constraints['min_length']:
            break
        if 'max_length' in constraints and length > constraints['max_length']:
            length = lps[length - 1]
            continue
        
        borders.append(s[:length])
        length = lps[length - 1]
    
    return borders[::-1]
```

#### **Variation 2: Finding Borders with Multiple Criteria**
**Problem**: Find borders that optimize multiple criteria (length, frequency, etc.).
```python
def multi_criteria_finding_borders(s, criteria):
    # criteria = {'length_weight': w1, 'frequency_weight': w2, 'simplicity_weight': w3}
    
    n = len(s)
    all_borders = []
    lps = compute_lps(s)
    
    length = lps[n - 1]
    while length > 0:
        all_borders.append(s[:length])
        length = lps[length - 1]
    
    # Score each border
    scored_borders = []
    for border in all_borders:
        score = 0
        
        # Length score (longer is better)
        if 'length_weight' in criteria:
            score += criteria['length_weight'] * len(border)
        
        # Frequency score (how often it appears)
        if 'frequency_weight' in criteria:
            freq = s.count(border)
            score += criteria['frequency_weight'] * freq
        
        # Simplicity score (fewer unique characters is better)
        if 'simplicity_weight' in criteria:
            unique_chars = len(set(border))
            score += criteria['simplicity_weight'] * (len(border) - unique_chars)
        
        scored_borders.append((border, score))
    
    # Return borders sorted by score
    scored_borders.sort(key=lambda x: x[1], reverse=True)
    return [border for border, _ in scored_borders]
```

#### **Variation 3: Finding Borders with Costs**
**Problem**: Each character has a cost, find borders with minimum total cost.
```python
def cost_based_finding_borders(s, char_costs):
    # char_costs[c] = cost of character c
    
    n = len(s)
    borders = []
    lps = compute_lps(s)
    
    length = lps[n - 1]
    while length > 0:
        border = s[:length]
        cost = sum(char_costs.get(c, 1) for c in border)
        borders.append((border, cost))
        length = lps[length - 1]
    
    # Sort by cost (ascending)
    borders.sort(key=lambda x: x[1])
    return [border for border, _ in borders]
```

#### **Variation 4: Finding Borders with Probabilities**
**Problem**: Characters have probabilities, find expected borders.
```python
def probabilistic_finding_borders(s, char_probs):
    # char_probs[c] = probability of character c
    
    n = len(s)
    expected_borders = []
    
    # Calculate expected borders based on character probabilities
    for length in range(1, n):
        prefix = s[:length]
        suffix = s[n - length:]
        
        # Calculate probability that prefix equals suffix
        prob_match = 1.0
        for i in range(length):
            if prefix[i] == suffix[i]:
                prob_match *= char_probs.get(prefix[i], 0.1)
            else:
                prob_match = 0
                break
        
        if prob_match >= 0.5:  # Threshold for "border"
            expected_borders.append(prefix)
    
    return expected_borders
```

#### **Variation 5: Finding Borders with Multiple Strings**
**Problem**: Find common borders across multiple strings.
```python
def multiple_string_finding_borders(strings):
    # Find borders that are common to all strings
    
    if not strings:
        return []
    
    # Find borders for each string
    all_border_sets = []
    for s in strings:
        borders = find_borders_kmp(s)
        all_border_sets.append(set(borders))
    
    # Find intersection of all border sets
    common_borders = all_border_sets[0]
    for border_set in all_border_sets[1:]:
        common_borders = common_borders.intersection(border_set)
    
    return sorted(common_borders, key=len)
```

### 🔗 **Related Problems & Concepts**

#### **1. Border Problems**
- **Border Detection**: Detect borders in strings
- **Border Analysis**: Analyze border properties
- **Border Classification**: Classify borders
- **Border Prediction**: Predict future borders

#### **2. String Analysis Problems**
- **Periodicity**: Analyze periodic properties
- **Suffix Analysis**: Analyze suffix properties
- **Prefix Analysis**: Analyze prefix properties
- **Pattern Analysis**: Analyze repeating patterns

#### **3. String Algorithms**
- **KMP Algorithm**: Efficient pattern matching
- **Z-Algorithm**: Linear time string processing
- **Failure Functions**: KMP failure function applications
- **Border Functions**: Border-based algorithms

#### **4. Optimization Problems**
- **Maximization**: Find maximum value solutions
- **Cost Optimization**: Optimize with respect to costs
- **Constrained Optimization**: Optimization with constraints
- **Multi-objective Optimization**: Optimize multiple criteria

#### **5. Algorithmic Techniques**
- **Dynamic Programming**: Solve optimization problems
- **Two Pointers**: Use two pointers for efficiency
- **Sliding Window**: Process data in windows
- **Mathematical Analysis**: Use mathematical properties

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Strings**
```python
t = int(input())
for _ in range(t):
    s = input().strip()
    borders = find_borders_kmp(s)
    print(len(borders))
    print(*borders)
```

#### **2. Range Queries on Border Finding**
```python
def range_border_finding_queries(s, queries):
    # queries = [(l, r), ...] - find borders of substring s[l:r]
    
    results = []
    for l, r in queries: substring = s[
l: r]
        borders = find_borders_kmp(substring)
        results.append(borders)
    
    return results
```

#### **3. Interactive Border Finding Problems**
```python
def interactive_border_finding():
    while True:
        s = input("Enter string (or 'quit' to exit): ")
        if s.lower() == 'quit':
            break
        
        borders = find_borders_kmp(s)
        print(f"String: {s}")
        print(f"Borders: {borders}")
        print(f"Number of borders: {len(borders)}")
```

### 🧮 **Mathematical Extensions**

#### **1. Border Theory**
- **Border Properties**: Mathematical properties of borders
- **Border Functions**: Mathematical functions on borders
- **Border Complexity**: Complexity measures for borders
- **Border Transformations**: Mathematical transformations

#### **2. Combinatorial Analysis**
- **Border Enumeration**: Count borders with properties
- **Pattern Enumeration**: Count patterns in borders
- **String Enumeration**: Count strings with border properties
- **Combinatorial Counting**: Count combinations and permutations

#### **3. String Theory**
- **String Properties**: Periodicity, borders, periods
- **String Functions**: Mathematical functions on strings
- **String Complexity**: Complexity measures for strings
- **String Transformations**: Mathematical transformations

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **String Matching**: KMP, Boyer-Moore, Rabin-Karp algorithms
- **Suffix Structures**: Suffix arrays, suffix trees, suffix automata
- **String Compression**: LZ77, LZ78, Huffman coding
- **String Parsing**: Regular expressions, context-free parsing

#### **2. Mathematical Concepts**
- **Combinatorics**: String combinatorics and counting
- **Information Theory**: Entropy, compression, encoding
- **Formal Languages**: Regular languages, context-free languages
- **Automata Theory**: Finite automata, pushdown automata

#### **3. Programming Concepts**
- **String Manipulation**: Efficient string operations
- **Algorithm Design**: Systematic approach to problem solving
- **Complexity Analysis**: Time and space complexity
- **Optimization Techniques**: Improving algorithm performance

---

*This analysis demonstrates efficient border finding techniques and shows various extensions for border analysis problems.* 