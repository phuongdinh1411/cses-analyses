---
layout: simple
title: "Distinct Strings - Count Unique Substrings"
permalink: /problem_soulutions/string_algorithms/distinct_strings_analysis
---

# Distinct Strings - Count Unique Substrings

## 📋 Problem Description

Given a string, find the number of distinct substrings.

This is a string algorithm problem that requires counting all unique substrings in a given string. The solution involves using efficient algorithms like suffix arrays or suffix automaton to achieve optimal time complexity.

**Input**: 
- First line: A string s

**Output**: 
- Print the number of distinct substrings

**Constraints**:
- 1 ≤ |s| ≤ 10⁵

**Example**:
```
Input:
abab

Output:
7

Explanation**: 
- String: "abab"
- All substrings: "a", "b", "a", "b", "ab", "ba", "ab", "ba", "aba", "bab", "abab"
- Distinct substrings: "a", "b", "ab", "ba", "aba", "bab", "abab"
- Count: 7 unique substrings
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
- **Goal**: Count all unique substrings in a given string
- **Key Insight**: Use suffix arrays or suffix automaton for efficiency
- **Challenge**: Handle large strings efficiently without O(|s|³) complexity

### Step 2: Initial Approach
**Generate all substrings (inefficient but correct):**

```python
def distinct_strings_naive(s):
    distinct = set()
    n = len(s)
    
    for i in range(n):
        for j in range(i + 1, n + 1):
            distinct.add(s[i:j])
    
    return len(distinct)
```

**Why this is inefficient**: Cubic time complexity and memory usage for large strings.

### Improvement 1: Use Suffix Array - O(|s|² × log(|s|))
**Description**: Use suffix array to efficiently find distinct substrings.

```python
def distinct_strings_suffix_array(s):
    def build_suffix_array(s):
        n = len(s)
        suffixes = [(s[i:], i) for i in range(n)]
        suffixes.sort()
        return [suffix[1] for suffix in suffixes]
    
    def lcp(suffix1, suffix2):
        min_len = min(len(suffix1), len(suffix2))
        for i in range(min_len):
            if suffix1[i] != suffix2[i]:
                return i
        return min_len
    
    n = len(s)
    suffix_array = build_suffix_array(s)
    
    # Count distinct substrings
    total_substrings = n * (n + 1) // 2
    duplicate_substrings = 0
    
    for i in range(1, n):
        lcp_value = lcp(s[suffix_array[i-1]:], s[suffix_array[i]:])
        duplicate_substrings += lcp_value
    
    return total_substrings - duplicate_substrings
```

**Why this improvement works**: Suffix array helps identify common prefixes efficiently.

### Improvement 2: Use Suffix Automaton - O(|s|)
**Description**: Use suffix automaton to count distinct substrings in linear time.

```python
def distinct_strings_suffix_automaton(s):
    class State:
        def __init__(self):
            self.next = {}
            self.link = -1
            self.len = 0
    
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
                    
                    while p >= 0 and self.states[p].next[c] == q:
                        self.states[p].next[c] = clone
                        p = self.states[p].link
                    
                    self.states[q].link = clone
                    self.states[curr].link = clone
            
            self.last = curr
    
    sa = SuffixAutomaton()
    for c in s:
        sa.sa_extend(c)
    
    # Count distinct substrings
    count = 0
    for i in range(1, sa.size):
        count += sa.states[i].len - sa.states[sa.states[i].link].len
    
    return count
```

**Why this improvement works**: Suffix automaton efficiently represents all substrings.

### Step 3: Optimization/Alternative
**Trie approach:**

```python
def distinct_strings_trie(s):
    class TrieNode:
        def __init__(self):
            self.children = {}
    
    class Trie:
        def __init__(self):
            self.root = TrieNode()
            self.count = 0
        
        def insert(self, s):
            node = self.root
            for c in s: if c not in node.
children: node.children[c] = TrieNode()
                    self.count += 1
                node = node.children[c]
    
    trie = Trie()
    n = len(s)
    
    for i in range(n):
        for j in range(i + 1, n + 1):
            trie.insert(s[i:j])
    
    return trie.count
```

**Why this works**: Trie efficiently stores and counts distinct substrings.

### Step 4: Complete Solution

```python
s = input().strip()

def distinct_strings_suffix_automaton(s):
    class State:
        def __init__(self):
            self.next = {}
            self.link = -1
            self.len = 0
    
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
                    
                    while p >= 0 and self.states[p].next[c] == q:
                        self.states[p].next[c] = clone
                        p = self.states[p].link
                    
                    self.states[q].link = clone
                    self.states[curr].link = clone
            
            self.last = curr
    
    sa = SuffixAutomaton()
    for c in s:
        sa.sa_extend(c)
    
    # Count distinct substrings
    count = 0
    for i in range(1, sa.size):
        count += sa.states[i].len - sa.states[sa.states[i].link].len
    
    return count

result = distinct_strings_suffix_automaton(s)
print(result)
```

### Step 5: Testing Our Solution
**Test cases to verify correctness:**
- **Test 1**: Basic string (should return correct count)
- **Test 2**: Single character (should return 1)
- **Test 3**: All same characters (should return n)
- **Test 4**: Complex pattern (should return optimal count)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(|s|³) | O(|s|²) | Generate all substrings |
| Suffix Array | O(|s|² × log|s|) | O(|s|) | Use suffix array properties |
| Suffix Automaton | O(|s|) | O(|s|) | Efficient substring representation |
| Trie | O(|s|²) | O(|s|²) | Store substrings in trie |

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(|s|³) | O(|s|³) | Generate all substrings |
| Suffix Array | O(|s|² × log(|s|)) | O(|s|²) | Use suffix array |
| Suffix Automaton | O(|s|) | O(|s|) | Use suffix automaton |
| Trie | O(|s|²) | O(|s|²) | Use trie |

## 🎯 Key Insights

### Important Concepts and Patterns
- **Suffix Automaton**: Efficiently represents all substrings
- **Suffix Array**: Use suffix properties for substring counting
- **Trie**: Store and count distinct substrings
- **Linear Time**: Achieve O(|s|) complexity with suffix automaton

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Distinct Strings with Length Constraints**
```python
def distinct_strings_length_constrained(s, min_length, max_length):
    # Handle distinct strings with length constraints
    
    class State:
        def __init__(self):
            self.next = {}
            self.link = -1
            self.len = 0
    
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
                    
                    while p >= 0 and self.states[p].next[c] == q:
                        self.states[p].next[c] = clone
                        p = self.states[p].link
                    
                    self.states[q].link = clone
                    self.states[curr].link = clone
            
            self.last = curr
    
    sa = SuffixAutomaton()
    for c in s:
        sa.sa_extend(c)
    
    # Count distinct substrings with length constraints
    count = 0
    for i in range(1, sa.size):
        state_len = sa.states[i].len
        link_len = sa.states[sa.states[i].link].len
        
        # Count substrings in this state that meet length constraints
        for length in range(max(link_len + 1, min_length), min(state_len + 1, max_length + 1)):
            count += 1
    
    return count
```

#### **2. Distinct Strings with Character Constraints**
```python
def distinct_strings_character_constrained(s, allowed_chars):
    # Handle distinct strings with character constraints
    
    def is_valid_substring(substring):
        return all(char in allowed_chars for char in substring)
    
    distinct = set()
    n = len(s)
    
    for i in range(n):
        for j in range(i + 1, n + 1):
            substring = s[i:j]
            if is_valid_substring(substring):
                distinct.add(substring)
    
    return len(distinct)
```

#### **3. Distinct Strings with Dynamic Updates**
```python
def distinct_strings_dynamic(operations):
    # Handle distinct strings with dynamic string updates
    
    s = ""
    distinct_count = 0
    
    for operation in operations:
        if operation[0] == 'add':
            # Add character to string
            char = operation[1]
            s += char
            
            # Recalculate distinct count
            distinct_count = calculate_distinct_count(s)
        
        elif operation[0] == 'remove':
            # Remove last character
            if len(s) > 0:
                s = s[:-1]
                distinct_count = calculate_distinct_count(s)
        
        elif operation[0] == 'query':
            # Return current distinct count
            yield distinct_count
    
    return list(distinct_strings_dynamic(operations))

def calculate_distinct_count(s):
    if len(s) == 0:
        return 0
    
    class State:
        def __init__(self):
            self.next = {}
            self.link = -1
            self.len = 0
    
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
                    
                    while p >= 0 and self.states[p].next[c] == q:
                        self.states[p].next[c] = clone
                        p = self.states[p].link
                    
                    self.states[q].link = clone
                    self.states[curr].link = clone
            
            self.last = curr
    
    sa = SuffixAutomaton()
    for c in s:
        sa.sa_extend(c)
    
    # Count distinct substrings
    count = 0
    for i in range(1, sa.size):
        count += sa.states[i].len - sa.states[sa.states[i].link].len
    
    return count
```

## 🔗 Related Problems

### Links to Similar Problems
- **String Algorithms**: Suffix array, suffix automaton problems
- **Substring Problems**: String substring analysis
- **Counting Problems**: String counting algorithms
- **Data Structures**: Trie, suffix tree problems

## 📚 Learning Points

### Key Takeaways
- **Suffix automaton** provides optimal O(|s|) solution
- **Suffix arrays** are useful for substring problems
- **Trie** is intuitive for substring storage
- **Linear time** algorithms are crucial for large strings

## Key Insights for Other Problems

### 1. **Substring Problems**
**Principle**: Use specialized data structures like suffix automaton for substring problems.
**Applicable to**:
- Substring problems
- String algorithms
- Pattern matching
- Algorithm design

**Example Problems**:
- Substring problems
- String algorithms
- Pattern matching
- Algorithm design

### 2. **Suffix Automaton**
**Principle**: Use suffix automaton to efficiently represent all substrings of a string.
**Applicable to**:
- String algorithms
- Substring problems
- Algorithm design
- Problem solving

**Example Problems**:
- String algorithms
- Substring problems
- Algorithm design
- Problem solving

### 3. **Suffix Array Applications**
**Principle**: Use suffix array for efficient substring analysis and pattern matching.
**Applicable to**:
- String algorithms
- Substring problems
- Algorithm design
- Problem solving

**Example Problems**:
- String algorithms
- Substring problems
- Algorithm design
- Problem solving

### 4. **Trie Data Structure**
**Principle**: Use trie for efficient string storage and prefix matching.
**Applicable to**:
- String algorithms
- Substring problems
- Algorithm design
- Problem solving

**Example Problems**:
- String algorithms
- Substring problems
- Algorithm design
- Problem solving

## Notable Techniques

### 1. **Suffix Automaton Pattern**
```python
def build_suffix_automaton(s):
    class State:
        def __init__(self):
            self.next = {}
            self.link = -1
            self.len = 0
    
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
                    
                    while p >= 0 and self.states[p].next[c] == q:
                        self.states[p].next[c] = clone
                        p = self.states[p].link
                    
                    self.states[q].link = clone
                    self.states[curr].link = clone
            
            self.last = curr
    
    sa = SuffixAutomaton()
    for c in s:
        sa.sa_extend(c)
    
    return sa
```

### 2. **Suffix Array Pattern**
```python
def build_suffix_array(s):
    n = len(s)
    suffixes = [(s[i:], i) for i in range(n)]
    suffixes.sort()
    return [suffix[1] for suffix in suffixes]

def lcp(suffix1, suffix2):
    min_len = min(len(suffix1), len(suffix2))
    for i in range(min_len):
        if suffix1[i] != suffix2[i]:
            return i
    return min_len
```

### 3. **Trie Pattern**
```python
def build_trie(strings):
    class TrieNode:
        def __init__(self):
            self.children = {}
            self.is_end = False
    
    class Trie:
        def __init__(self):
            self.root = TrieNode()
        
        def insert(self, s):
            node = self.root
            for c in s: if c not in node.
children: node.children[c] = TrieNode()
                node = node.children[c]
            node.is_end = True
        
        def search(self, s):
            node = self.root
            for c in s: if c not in node.
children: return False
                node = node.children[c]
            return node.is_end
    
    trie = Trie()
    for s in strings:
        trie.insert(s)
    
    return trie
```

## Edge Cases to Remember

1. **Empty string**: Return 0
2. **Single character**: Return 1
3. **All same characters**: Return n
4. **No repeated characters**: Return n*(n+1)/2
5. **Large strings**: Use efficient algorithms

## Problem-Solving Framework

1. **Identify substring nature**: This is a distinct substring counting problem
2. **Choose algorithm**: Use suffix automaton for efficiency
3. **Build automaton**: Construct suffix automaton for the string
4. **Count substrings**: Count distinct substrings using automaton properties
5. **Return result**: Return the count of distinct substrings

---

*This analysis shows how to efficiently count distinct substrings using suffix automaton and other string algorithms.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Distinct Substrings with Length Constraints**
**Problem**: Count distinct substrings with specific length constraints.
```python
def distinct_substrings_length_constraints(s, min_length, max_length):
    # Count distinct substrings with length between min_length and max_length
    
    n = len(s)
    sa = SuffixAutomaton()
    for c in s:
        sa.sa_extend(c)
    
    count = 0
    for i in range(sa.size):
        length = sa.states[i].len
        if min_length <= length <= max_length:
            # Count distinct substrings ending at this state
            count += length - sa.states[i].link
    
    return count
```

#### **Variation 2: Distinct Substrings with Alphabet Constraints**
**Problem**: Count distinct substrings using only specific characters.
```python
def distinct_substrings_alphabet_constraints(s, alphabet):
    # Count distinct substrings using only characters in alphabet
    
    n = len(s)
    
    # Filter string to only include allowed characters
    filtered_s = ''.join(c for c in s if c in alphabet)
    
    if not filtered_s:
        return 0
    
    sa = SuffixAutomaton()
    for c in filtered_s:
        sa.sa_extend(c)
    
    count = 0
    for i in range(sa.size):
        count += sa.states[i].len - sa.states[i].link
    
    return count
```

#### **Variation 3: Distinct Substrings with Costs**
**Problem**: Each character has a cost, find distinct substrings with minimum total cost.
```python
def cost_based_distinct_substrings(s, char_costs, budget):
    # Find distinct substrings with total cost within budget
    
    n = len(s)
    sa = SuffixAutomaton()
    for c in s:
        sa.sa_extend(c)
    
    distinct_substrings = set()
    total_cost = 0
    
    for i in range(sa.size):
        length = sa.states[i].len
        # Generate all substrings ending at this state
        for j in range(sa.states[i].link + 1, length + 1):
            substring = s[:j]
            cost = sum(char_costs.get(c, 1) for c in substring)
            
            if substring not in distinct_substrings and total_cost + cost <= budget:
                distinct_substrings.add(substring)
                total_cost += cost
    
    return len(distinct_substrings)
```

#### **Variation 4: Distinct Substrings with Probabilities**
**Problem**: Characters have probabilities, find expected number of distinct substrings.
```python
def probabilistic_distinct_substrings(s, char_probs):
    # char_probs[c] = probability of character c
    
    n = len(s)
    # For probabilistic strings, calculate expected distinct substrings
    expected_count = 0
    
    # Calculate expected count based on character probabilities
    for length in range(1, n + 1):
        for start in range(n - length + 1):
            prob_substring = 1.0
            for i in range(start, start + length):
                if i < len(s):
                    prob_substring *= char_probs.get(s[i], 0.1)
            expected_count += prob_substring
    
    return expected_count
```

#### **Variation 5: Distinct Substrings with Multiple Strings**
**Problem**: Count distinct substrings across multiple strings.
```python
def multiple_string_distinct_substrings(strings):
    # Count distinct substrings across all strings
    
    all_substrings = set()
    
    for s in strings:
        n = len(s)
        sa = SuffixAutomaton()
        for c in s:
            sa.sa_extend(c)
        
        # Add all substrings from this string
        for i in range(sa.size):
            length = sa.states[i].len
            for j in range(sa.states[i].link + 1, length + 1):
                substring = s[:j]
                all_substrings.add(substring)
    
    return len(all_substrings)
```

### 🔗 **Related Problems & Concepts**

#### **1. String Counting Problems**
- **Substring Counting**: Count substrings with specific properties
- **Pattern Counting**: Count occurrences of patterns
- **Palindrome Counting**: Count palindromic substrings
- **Anagram Counting**: Count anagrams of strings

#### **2. String Analysis Problems**
- **Periodicity**: Analyze periodic properties of strings
- **Border Analysis**: Find borders and periods
- **Suffix Analysis**: Analyze suffix properties
- **Prefix Analysis**: Analyze prefix properties

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
- **Dynamic Programming**: Solve optimization problems
- **Sliding Window**: Process data in windows
- **Two Pointers**: Use two pointers for efficiency

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Strings**
```python
t = int(input())
for _ in range(t):
    s = input().strip()
    sa = SuffixAutomaton()
    for c in s:
        sa.sa_extend(c)
    
    count = 0
    for i in range(sa.size):
        count += sa.states[i].len - sa.states[i].link
    
    print(count)
```

#### **2. Range Queries on Distinct Substrings**
```python
def range_distinct_substring_queries(s, queries):
    # queries = [(l, r), ...] - count distinct substrings in s[l:r]
    
    results = []
    for l, r in queries: substring = s[
l: r]
        sa = SuffixAutomaton()
        for c in substring:
            sa.sa_extend(c)
        
        count = 0
        for i in range(sa.size):
            count += sa.states[i].len - sa.states[i].link
        
        results.append(count)
    
    return results
```

#### **3. Interactive Distinct Substring Problems**
```python
def interactive_distinct_substrings():
    while True:
        s = input("Enter string (or 'quit' to exit): ")
        if s.lower() == 'quit':
            break
        
        sa = SuffixAutomaton()
        for c in s:
            sa.sa_extend(c)
        
        count = 0
        for i in range(sa.size):
            count += sa.states[i].len - sa.states[i].link
        
        print(f"String: {s}")
        print(f"Number of distinct substrings: {count}")
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
- **Combinatorial Counting**: Count combinations and permutations

#### **3. Probability Theory**
- **Expected Values**: Calculate expected outcomes
- **Probability Distributions**: Character probability distributions
- **Stochastic Processes**: Random string generation
- **Markov Chains**: State transitions in strings

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
- **String Representations**: Character arrays, string objects
- **Memory Management**: Efficient string storage and manipulation
- **Algorithm Optimization**: Improving string algorithm performance
- **Error Handling**: Dealing with invalid inputs and edge cases

---

*This analysis demonstrates efficient distinct substring counting techniques and shows various extensions for string analysis problems.* 