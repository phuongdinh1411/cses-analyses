---
layout: simple
title: "Repeating Substring"
permalink: /problem_soulutions/string_algorithms/repeating_substring_analysis
---


# Repeating Substring

## 📋 Problem Description

Given a string, find the longest substring that appears at least twice.

This is a string algorithm problem where we need to find the longest substring that appears at least twice in the given string. We can solve this efficiently using suffix arrays or by checking all possible substrings with optimizations.

**Input**: 
- First line: string s (the input string)

**Output**: 
- Print the longest substring that appears at least twice, or -1 if no such substring exists

**Constraints**:
- 1 ≤ |s| ≤ 10⁵

**Example**:
```
Input:
ababab

Output:
abab
```

**Explanation**: 
In the string "ababab", the substring "abab" appears twice:
1. Starting at position 0: "abab"ab
2. Starting at position 2: ab"abab"

This is the longest substring that appears at least twice.

## 🎯 Visual Example

### Input
```
String: "ababab"
```

### Repeating Substring Detection Process
```
Step 1: Check all possible substrings
- Length 1: "a", "b" (both appear multiple times)
- Length 2: "ab", "ba" (both appear multiple times)
- Length 3: "aba", "bab" (both appear multiple times)
- Length 4: "abab" (appears twice)
- Length 5: "ababa" (appears once)

Step 2: Find longest repeating substring
- "abab" (length 4) appears twice
- This is the longest substring that appears at least twice
```

### Substring Occurrence Visualization
```
String: a b a b a b
Index:  0 1 2 3 4 5

Substring "abab" (length 4):
- First occurrence: positions 0-3
- Second occurrence: positions 2-5
- Overlap: positions 2-3

Occurrence 1: a b a b a b
            a b a b
            ✓ ✓ ✓ ✓

Occurrence 2: a b a b a b
                a b a b
                ✓ ✓ ✓ ✓
```

### Key Insight
Repeating substring detection works by:
1. Checking all possible substring lengths from longest to shortest
2. For each length, finding substrings that appear at least twice
3. Using suffix arrays for efficient detection
4. Time complexity: O(n²) for naive approach
5. Space complexity: O(n) for the algorithm

## Solution Progression

### Approach 1: Check All Substrings - O(|s|⁴)
**Description**: Check all possible substrings to find the longest one that appears at least twice.

```python
def repeating_substring_naive(s):
    n = len(s)
    max_length = 0
    result = ""
    
    for i in range(n):
        for j in range(i + 1, n + 1):
            substring = s[i:j]
            # Check if this substring appears at least twice
            count = 0
            for k in range(n - len(substring) + 1):
                if s[k: k + len(substring)] == 
substring: count += 1
                    if count >= 2:
                        break
            
            if count >= 2 and len(substring) > max_length:
                max_length = len(substring)
                result = substring
    
    return result if max_length > 0 else -1
```

**Why this is inefficient**: Quartic time complexity for large strings.

### Improvement 1: Use Suffix Array with LCP - O(|s|² × log(|s|))
**Description**: Use suffix array and longest common prefix to find repeating substrings.

```python
def repeating_substring_suffix_array(s):
    def build_suffix_array(s):
        n = len(s)
        suffixes = [(s[i:], i) for i in range(n)]
        suffixes.sort()
        return [suffix[1] for suffix in suffixes]
    
    def compute_lcp(suffix1, suffix2):
        min_len = min(len(suffix1), len(suffix2))
        for i in range(min_len):
            if suffix1[i] != suffix2[i]:
                return i
        return min_len
    
    n = len(s)
    suffix_array = build_suffix_array(s)
    
    max_length = 0
    result = ""
    
    # Check adjacent suffixes in sorted order
    for i in range(1, n):
        lcp_value = compute_lcp(s[suffix_array[i-1]:], s[suffix_array[i]:])
        if lcp_value > max_length:
            max_length = lcp_value
            result = s[suffix_array[i-1]:suffix_array[i-1] + lcp_value]
    
    return result if max_length > 0 else -1
```

**Why this improvement works**: Suffix array helps identify common prefixes efficiently.

### Improvement 2: Use Suffix Automaton - O(|s|)
**Description**: Use suffix automaton to find the longest repeating substring in linear time.

```python
def repeating_substring_suffix_automaton(s):
    class State:
        def __init__(self):
            self.next = {}
            self.link = -1
            self.len = 0
            self.cnt = 0
    
    class SuffixAutomaton:
        def __init__(self):
            self.size = 1
            self.last = 0
            self.states = [State()]
        
        def sa_extend(self, c):
            p = self.last
            curr = self.size
            self.size += 1
            self.states.append(State())
            self.states[curr].len = self.states[p].len + 1
            self.states[curr].cnt = 1
            
            while p >= 0 and c not in self.states[p].next:
                self.states[p].next[c] = curr
                p = self.states[p].link
            
            if p == -1:
                self.states[curr].link = 0
            else:
                q = self.states[p].next[c]
                if self.states[p].len + 1 == self.states[q].len:
                    self.states[curr].link = q
                else:
                    clone = self.size
                    self.size += 1
                    self.states.append(State())
                    self.states[clone].len = self.states[p].len + 1
                    self.states[clone].next = self.states[q].next.copy()
                    self.states[clone].link = self.states[q].link
                    self.states[clone].cnt = 0
                    
                    while p >= 0 and self.states[p].next[c] == q:
                        self.states[p].next[c] = clone
                        p = self.states[p].link
                    
                    self.states[q].link = clone
                    self.states[curr].link = clone
            
            self.last = curr
        
        def count_occurrences(self):
            # Count occurrences using topological sort
            count = [0] * self.size
            for i in range(self.size):
                count[self.states[i].len] += 1
            
            for i in range(self.size - 1, 0, -1):
                count[i - 1] += count[i]
            
            for i in range(self.size):
                self.states[i].cnt = count[self.states[i].len]
    
    sa = SuffixAutomaton()
    for c in s:
        sa.sa_extend(c)
    
    sa.count_occurrences()
    
    # Find the longest substring that appears at least twice
    max_length = 0
    result = ""
    
    for i in range(1, sa.size):
        if sa.states[i].cnt >= 2 and sa.states[i].len > max_length:
            max_length = sa.states[i].len
            # Reconstruct the substring
            result = s[:max_length]
    
    return result if max_length > 0 else -1
```

**Why this improvement works**: Suffix automaton efficiently represents all substrings and their occurrences.

### Alternative: Use Rolling Hash - O(|s|²)
**Description**: Use rolling hash to find repeating substrings.

```python
def repeating_substring_rolling_hash(s):
    def compute_hash(s, base=31, mod=10**9 + 7):
        n = len(s)
        hash_values = [0] * (n + 1)
        power = [1] * (n + 1)
        
        for i in range(n):
            hash_values[i + 1] = (hash_values[i] * base + ord(s[i])) % mod
            power[i + 1] = (power[i] * base) % mod
        
        return hash_values, power
    
    def get_hash(hash_values, power, mod, left, right):
        return (hash_values[right] - hash_values[left] * power[right - left]) % mod
    
    n = len(s)
    hash_values, power = compute_hash(s)
    mod = 10**9 + 7
    
    max_length = 0
    result = ""
    
    for length in range(1, n):
        seen = {}
        for i in range(n - length + 1):
            h = get_hash(hash_values, power, mod, i, i + length)
            if h in seen: if length > 
max_length: max_length = length
                    result = s[i:i + length]
                break
            seen[h] = i
    
    return result if max_length > 0 else -1
```

**Why this works**: Rolling hash efficiently checks for substring matches.

## Final Optimal Solution

```python
s = input().strip()

def repeating_substring_suffix_automaton(s):
    class State:
        def __init__(self):
            self.next = {}
            self.link = -1
            self.len = 0
            self.cnt = 0
    
    class SuffixAutomaton:
        def __init__(self):
            self.size = 1
            self.last = 0
            self.states = [State()]
        
        def sa_extend(self, c):
            p = self.last
            curr = self.size
            self.size += 1
            self.states.append(State())
            self.states[curr].len = self.states[p].len + 1
            self.states[curr].cnt = 1
            
            while p >= 0 and c not in self.states[p].next:
                self.states[p].next[c] = curr
                p = self.states[p].link
            
            if p == -1:
                self.states[curr].link = 0
            else:
                q = self.states[p].next[c]
                if self.states[p].len + 1 == self.states[q].len:
                    self.states[curr].link = q
                else:
                    clone = self.size
                    self.size += 1
                    self.states.append(State())
                    self.states[clone].len = self.states[p].len + 1
                    self.states[clone].next = self.states[q].next.copy()
                    self.states[clone].link = self.states[q].link
                    self.states[clone].cnt = 0
                    
                    while p >= 0 and self.states[p].next[c] == q:
                        self.states[p].next[c] = clone
                        p = self.states[p].link
                    
                    self.states[q].link = clone
                    self.states[curr].link = clone
            
            self.last = curr
        
        def count_occurrences(self):
            # Count occurrences using topological sort
            count = [0] * self.size
            for i in range(self.size):
                count[self.states[i].len] += 1
            
            for i in range(self.size - 1, 0, -1):
                count[i - 1] += count[i]
            
            for i in range(self.size):
                self.states[i].cnt = count[self.states[i].len]
    
    sa = SuffixAutomaton()
    for c in s:
        sa.sa_extend(c)
    
    sa.count_occurrences()
    
    # Find the longest substring that appears at least twice
    max_length = 0
    result = ""
    
    for i in range(1, sa.size):
        if sa.states[i].cnt >= 2 and sa.states[i].len > max_length:
            max_length = sa.states[i].len
            # Reconstruct the substring
            result = s[:max_length]
    
    return result if max_length > 0 else -1

result = repeating_substring_suffix_automaton(s)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(|s|⁴) | O(|s|²) | Check all substrings |
| Suffix Array | O(|s|² × log(|s|)) | O(|s|²) | Use suffix array |
| Suffix Automaton | O(|s|) | O(|s|) | Use suffix automaton |
| Rolling Hash | O(|s|²) | O(|s|) | Use rolling hash |

## Key Insights for Other Problems

### 1. **Repeating Pattern Problems**
**Principle**: Use specialized algorithms like suffix automaton for finding repeating patterns.
**Applicable to**:
- Repeating pattern problems
- String algorithms
- Pattern matching
- Algorithm design

**Example Problems**:
- Repeating pattern problems
- String algorithms
- Pattern matching
- Algorithm design

### 2. **Suffix Automaton for Counting**
**Principle**: Use suffix automaton to efficiently count substring occurrences.
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

### 3. **Suffix Array with LCP**
**Principle**: Use suffix array with longest common prefix for substring analysis.
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

### 4. **Rolling Hash Applications**
**Principle**: Use rolling hash for efficient substring comparison and matching.
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

## Notable Techniques

### 1. **Suffix Automaton with Counting Pattern**
```python
def build_suffix_automaton_with_counting(s):
    class State:
        def __init__(self):
            self.next = {}
            self.link = -1
            self.len = 0
            self.cnt = 0
    
    class SuffixAutomaton:
        def __init__(self):
            self.size = 1
            self.last = 0
            self.states = [State()]
        
        def sa_extend(self, c):
            p = self.last
            curr = self.size
            self.size += 1
            self.states.append(State())
            self.states[curr].len = self.states[p].len + 1
            self.states[curr].cnt = 1
            
            while p >= 0 and c not in self.states[p].next:
                self.states[p].next[c] = curr
                p = self.states[p].link
            
            if p == -1:
                self.states[curr].link = 0
            else:
                q = self.states[p].next[c]
                if self.states[p].len + 1 == self.states[q].len:
                    self.states[curr].link = q
                else:
                    clone = self.size
                    self.size += 1
                    self.states.append(State())
                    self.states[clone].len = self.states[p].len + 1
                    self.states[clone].next = self.states[q].next.copy()
                    self.states[clone].link = self.states[q].link
                    self.states[clone].cnt = 0
                    
                    while p >= 0 and self.states[p].next[c] == q:
                        self.states[p].next[c] = clone
                        p = self.states[p].link
                    
                    self.states[q].link = clone
                    self.states[curr].link = clone
            
            self.last = curr
        
        def count_occurrences(self):
            count = [0] * self.size
            for i in range(self.size):
                count[self.states[i].len] += 1
            
            for i in range(self.size - 1, 0, -1):
                count[i - 1] += count[i]
            
            for i in range(self.size):
                self.states[i].cnt = count[self.states[i].len]
    
    sa = SuffixAutomaton()
    for c in s:
        sa.sa_extend(c)
    
    sa.count_occurrences()
    return sa
```

### 2. **Rolling Hash Pattern**
```python
def rolling_hash_string_matching(s, pattern):
    def compute_hash(s, base=31, mod=10**9 + 7):
        n = len(s)
        hash_values = [0] * (n + 1)
        power = [1] * (n + 1)
        
        for i in range(n):
            hash_values[i + 1] = (hash_values[i] * base + ord(s[i])) % mod
            power[i + 1] = (power[i] * base) % mod
        
        return hash_values, power
    
    def get_hash(hash_values, power, mod, left, right):
        return (hash_values[right] - hash_values[left] * power[right - left]) % mod
    
    n, m = len(s), len(pattern)
    hash_values, power = compute_hash(s)
    pattern_hash = compute_hash(pattern)[0][-1]
    mod = 10**9 + 7
    
    positions = []
    for i in range(n - m + 1):
        if get_hash(hash_values, power, mod, i, i + m) == pattern_hash:
            positions.append(i)
    
    return positions
```

### 3. **Suffix Array with LCP Pattern**
```python
def suffix_array_with_lcp(s):
    def build_suffix_array(s):
        n = len(s)
        suffixes = [(s[i:], i) for i in range(n)]
        suffixes.sort()
        return [suffix[1] for suffix in suffixes]
    
    def compute_lcp(suffix1, suffix2):
        min_len = min(len(suffix1), len(suffix2))
        for i in range(min_len):
            if suffix1[i] != suffix2[i]:
                return i
        return min_len
    
    n = len(s)
    suffix_array = build_suffix_array(s)
    lcp_array = [0] * (n - 1)
    
    for i in range(n - 1):
        lcp_array[i] = compute_lcp(s[suffix_array[i]:], s[suffix_array[i + 1]:])
    
    return suffix_array, lcp_array
```

## Edge Cases to Remember

1. **No repeating substrings**: Return -1
2. **Single character**: Return -1
3. **All same characters**: Return the entire string
4. **Empty string**: Handle appropriately
5. **Large strings**: Use efficient algorithms

## Problem-Solving Framework

1. **Identify repeating nature**: This is a longest repeating substring problem
2. **Choose algorithm**: Use suffix automaton for efficiency
3. **Build automaton**: Construct suffix automaton for the string
4. **Count occurrences**: Count substring occurrences using automaton
5. **Find longest**: Find the longest substring with at least 2 occurrences

---

*This analysis shows how to efficiently find the longest repeating substring using suffix automaton and other string algorithms.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Repeating Substring with Minimum Occurrences**
**Problem**: Find longest substring that repeats at least k times.
```python
def repeating_substring_min_occurrences(s, k):
    # Find longest substring that appears at least k times
    
    n = len(s)
    sa = SuffixAutomaton()
    for c in s:
        sa.sa_extend(c)
    
    sa.count_occurrences()
    
    max_length = 0
    max_substring = ""
    
    for i in range(sa.size):
        if sa.states[i].cnt >= k:
            # Find the substring ending at this state
            length = sa.states[i].len
            if length > max_length:
                max_length = length
                # Reconstruct substring (simplified)
                max_substring = s[:length]
    
    return max_substring if max_length > 0 else ""
```

#### **Variation 2: Repeating Substring with Constraints**
**Problem**: Find longest repeating substring with additional constraints.
```python
def constrained_repeating_substring(s, constraints):
    # constraints = {'alphabet': chars, 'min_length': x, 'max_length': y}
    
    n = len(s)
    
    # Apply constraints
    if 'alphabet' in constraints:
        if not all(c in constraints['alphabet'] for c in s):
            return ""
    
    if 'min_length' in constraints and n < constraints['min_length']:
        return ""
    
    if 'max_length' in constraints:
        n = min(n, constraints['max_length'])
    
    # Use suffix automaton
    sa = SuffixAutomaton()
    for c in s[:n]:
        sa.sa_extend(c)
    
    sa.count_occurrences()
    
    max_length = 0
    for i in range(sa.size):
        if sa.states[i].cnt >= 2:
            length = sa.states[i].len
            if 'min_length' in constraints:
                length = max(length, constraints['min_length'])
            max_length = max(max_length, length)
    
    return s[:max_length] if max_length > 0 else ""
```

#### **Variation 3: Repeating Substring with Costs**
**Problem**: Each character has a cost, find longest repeating substring with minimum cost.
```python
def cost_based_repeating_substring(s, char_costs):
    # char_costs[c] = cost of character c
    
    n = len(s)
    sa = SuffixAutomaton()
    for c in s:
        sa.sa_extend(c)
    
    sa.count_occurrences()
    
    max_length = 0
    min_cost = float('inf')
    best_substring = ""
    
    for i in range(sa.size):
        if sa.states[i].cnt >= 2:
            length = sa.states[i].len
            substring = s[:length]
            cost = sum(char_costs.get(c, 1) for c in substring)
            
            if length > max_length or (length == max_length and cost < min_cost):
                max_length = length
                min_cost = cost
                best_substring = substring
    
    return best_substring
```

#### **Variation 4: Repeating Substring with Probabilities**
**Problem**: Characters have probabilities, find expected longest repeating substring.
```python
def probabilistic_repeating_substring(s, char_probs):
    # char_probs[c] = probability of character c
    
    n = len(s)
    # For probabilistic strings, calculate expected repeating substring
    expected_length = 0
    
    # Calculate expected length based on character probabilities
    for length in range(1, n + 1):
        prob_repeat = 1.0
        for i in range(length):
            if i < len(s):
                prob_repeat *= char_probs.get(s[i], 0.1)
        
        if prob_repeat >= 0.5:  # Threshold for "repeating"
            expected_length = length
    
    return s[:expected_length] if expected_length > 0 else ""
```

#### **Variation 5: Repeating Substring with Multiple Strings**
**Problem**: Find longest substring that repeats in multiple strings.
```python
def multiple_string_repeating_substring(strings):
    # Find longest substring that appears in all strings
    
    if not strings:
        return ""
    
    # Find common substrings using suffix automata
    common_substrings = set()
    
    # Build suffix automaton for first string
    sa = SuffixAutomaton()
    for c in strings[0]:
        sa.sa_extend(c)
    
    # Find all substrings in first string
    for i in range(sa.size):
        if sa.states[i].cnt >= 1:
            length = sa.states[i].len
            substring = strings[0][:length]
            common_substrings.add(substring)
    
    # Check which substrings appear in all other strings
    for s in strings[1:]:
        current_common = set()
        for substring in common_substrings: if substring in 
s: current_common.add(substring)
        common_substrings = current_common
    
    # Return longest common substring
    if common_substrings:
        return max(common_substrings, key=len)
    return ""
```

### 🔗 **Related Problems & Concepts**

#### **1. String Matching Problems**
- **Pattern Matching**: Find patterns in strings
- **Substring Search**: Search for substrings efficiently
- **Multiple Pattern Matching**: Match multiple patterns simultaneously
- **Approximate String Matching**: Allow errors in matching

#### **2. String Analysis Problems**
- **Periodicity**: Analyze periodic properties of strings
- **Border Analysis**: Find borders and periods
- **Palindrome Analysis**: Find palindromic substrings
- **Suffix Analysis**: Analyze suffix properties

#### **3. String Data Structures**
- **Suffix Arrays**: Sort all suffixes of a string
- **Suffix Trees**: Tree representation of suffixes
- **Suffix Automata**: Compact automaton for suffixes
- **Trie**: Tree for string storage and retrieval

#### **4. Optimization Problems**
- **Maximization**: Find maximum value solutions
- **Cost Optimization**: Optimize with respect to costs
- **Constrained Optimization**: Optimization with constraints
- **Multi-objective Optimization**: Optimize multiple criteria

#### **5. Algorithmic Techniques**
- **Suffix Automaton**: Efficient substring processing
- **Rolling Hash**: Hash-based string matching
- **Dynamic Programming**: Solve optimization problems
- **Sliding Window**: Process data in windows

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Strings**
```python
t = int(input())
for _ in range(t):
    s = input().strip()
    sa = SuffixAutomaton()
    for c in s:
        sa.sa_extend(c)
    sa.count_occurrences()
    
    max_length = 0
    for i in range(sa.size):
        if sa.states[i].cnt >= 2:
            max_length = max(max_length, sa.states[i].len)
    
    print(max_length if max_length > 0 else -1)
```

#### **2. Range Queries on Repeating Substrings**
```python
def range_repeating_substring_queries(s, queries):
    # queries = [(l, r), ...] - find longest repeating substring in s[l:r]
    
    results = []
    for l, r in queries: substring = s[
l: r]
        sa = SuffixAutomaton()
        for c in substring:
            sa.sa_extend(c)
        sa.count_occurrences()
        
        max_length = 0
        for i in range(sa.size):
            if sa.states[i].cnt >= 2:
                max_length = max(max_length, sa.states[i].len)
        
        results.append(max_length if max_length > 0 else -1)
    
    return results
```

#### **3. Interactive Repeating Substring Problems**
```python
def interactive_repeating_substring():
    while True:
        s = input("Enter string (or 'quit' to exit): ")
        if s.lower() == 'quit':
            break
        
        sa = SuffixAutomaton()
        for c in s:
            sa.sa_extend(c)
        sa.count_occurrences()
        
        max_length = 0
        for i in range(sa.size):
            if sa.states[i].cnt >= 2:
                max_length = max(max_length, sa.states[i].len)
        
        print(f"String: {s}")
        print(f"Longest repeating substring length: {max_length if max_length > 0 else -1}")
```

### 🧮 **Mathematical Extensions**

#### **1. String Theory**
- **String Properties**: Periodicity, borders, periods
- **String Functions**: Failure function, border array
- **String Complexity**: Kolmogorov complexity of strings
- **String Enumeration**: Count strings with certain properties

#### **2. Combinatorial Analysis**
- **String Enumeration**: Count strings with certain properties
- **Substring Enumeration**: Count substrings with properties
- **Pattern Enumeration**: Count patterns in strings
- **Repetition Analysis**: Analyze repetitions in strings

#### **3. Probability Theory**
- **Expected Values**: Calculate expected outcomes
- **Probability Distributions**: Character probability distributions
- **Stochastic Processes**: Random string generation
- **Markov Chains**: State transitions in strings

### 📚 **Learning Resources**

## 🔧 Implementation Details

### Time and Space Complexity
- **Time Complexity**: O(|s|²) for optimized approach, O(|s|⁴) for naive approach
- **Space Complexity**: O(|s|) for storing substrings and counts
- **Why it works**: We can optimize by checking substrings in decreasing order of length and stopping when we find the first repeating substring

### Key Implementation Points
- Check substrings in decreasing order of length to find the longest first
- Use efficient string matching to count occurrences
- Stop early when a repeating substring is found
- Handle edge cases like single character strings

## 🎯 Key Insights

### Important Concepts and Patterns
- **Suffix Arrays**: Efficient data structure for string analysis
- **String Matching**: Finding occurrences of substrings in strings
- **Longest Common Substring**: Finding the longest substring that appears multiple times
- **String Analysis**: Analyzing patterns and repetitions in strings

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Repeating Substring with Minimum Occurrences**
```python
def repeating_substring_min_occurrences(s, min_count):
    # Find the longest substring that appears at least min_count times
    n = len(s)
    
    # Check substrings in decreasing order of length
    for length in range(n, 0, -1):
        for i in range(n - length + 1):
            substring = s[i:i + length]
            count = 0
            
            # Count occurrences
            for j in range(n - length + 1):
                if s[j:j + length] == substring:
                    count += 1
                    if count >= min_count:
                        return substring
    
    return -1

# Example usage
s = "ababab"
min_count = 3
result = repeating_substring_min_occurrences(s, min_count)
print(f"Longest substring with {min_count} occurrences: {result}")
```

#### **2. Repeating Substring with Non-Overlapping**
```python
def repeating_substring_non_overlapping(s):
    # Find the longest substring that appears at least twice without overlapping
    n = len(s)
    
    # Check substrings in decreasing order of length
    for length in range(n // 2, 0, -1):
        for i in range(n - length + 1):
            substring = s[i:i + length]
            
            # Check for non-overlapping occurrences
            positions = []
            for j in range(n - length + 1):
                if s[j:j + length] == substring:
                    positions.append(j)
            
            # Check if we have at least 2 non-overlapping occurrences
            if len(positions) >= 2:
                # Check for non-overlapping
                for k in range(len(positions)):
                    for l in range(k + 1, len(positions)):
                        if positions[l] >= positions[k] + length:
                            return substring
    
    return -1

# Example usage
s = "ababab"
result = repeating_substring_non_overlapping(s)
print(f"Longest non-overlapping repeating substring: {result}")
```

#### **3. Repeating Substring with Maximum Frequency**
```python
def repeating_substring_max_frequency(s):
    # Find the substring with maximum frequency
    n = len(s)
    max_frequency = 0
    result = ""
    
    # Check all possible substrings
    for i in range(n):
        for j in range(i + 1, n + 1):
            substring = s[i:j]
            count = 0
            
            # Count occurrences
            for k in range(n - len(substring) + 1):
                if s[k:k + len(substring)] == substring:
                    count += 1
            
            # Update result if frequency is higher
            if count > max_frequency:
                max_frequency = count
                result = substring
    
    return result, max_frequency

# Example usage
s = "ababab"
result, frequency = repeating_substring_max_frequency(s)
print(f"Substring with max frequency: {result} (frequency: {frequency})")
```

#### **4. Repeating Substring with Suffix Array**
```python
def build_suffix_array(s):
    # Build suffix array for efficient string analysis
    n = len(s)
    suffixes = []
    
    for i in range(n):
        suffixes.append((s[i:], i))
    
    suffixes.sort()
    return [suffix[1] for suffix in suffixes]

def repeating_substring_suffix_array(s):
    # Find longest repeating substring using suffix array
    n = len(s)
    suffix_array = build_suffix_array(s)
    
    max_length = 0
    result = ""
    
    # Compare adjacent suffixes
    for i in range(n - 1):
        suffix1 = s[suffix_array[i]:]
        suffix2 = s[suffix_array[i + 1]:]
        
        # Find common prefix length
        common_length = 0
        min_len = min(len(suffix1), len(suffix2))
        
        for j in range(min_len):
            if suffix1[j] == suffix2[j]:
                common_length += 1
            else:
                break
        
        # Update result if common prefix is longer
        if common_length > max_length:
            max_length = common_length
            result = suffix1[:common_length]
    
    return result if max_length > 0 else -1

# Example usage
s = "ababab"
result = repeating_substring_suffix_array(s)
print(f"Longest repeating substring (suffix array): {result}")
```

## 🔗 Related Problems

### Links to Similar Problems
- **String Algorithms**: String matching, Pattern matching
- **Suffix Arrays**: String analysis, String processing
- **String Compression**: Repetitive patterns, String optimization
- **String Analysis**: Pattern detection, String statistics

## 📚 Learning Points

### Key Takeaways
- **Suffix arrays** are efficient for string analysis and pattern detection
- **String matching** can be optimized using various algorithms
- **Longest common substring** is a fundamental string analysis problem
- **String analysis** helps identify patterns and repetitions in text

---

*This analysis demonstrates efficient repeating substring techniques and shows various extensions for string analysis problems.* 