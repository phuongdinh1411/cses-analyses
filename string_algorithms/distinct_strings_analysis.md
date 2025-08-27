# CSES Distinct Strings - Problem Analysis

## Problem Statement
Given a string, find the number of distinct substrings.

### Input
The first input line has a string s.

### Output
Print the number of distinct substrings.

### Constraints
- 1 ≤ |s| ≤ 10^5

### Example
```
Input:
abab

Output:
7
```

## Solution Progression

### Approach 1: Generate All Substrings - O(|s|³)
**Description**: Generate all possible substrings and count distinct ones.

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

### Alternative: Use Trie - O(|s|²)
**Description**: Use trie to count distinct substrings.

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
            for c in s:
                if c not in node.children:
                    node.children[c] = TrieNode()
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

## Final Optimal Solution

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

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Naive | O(|s|³) | O(|s|³) | Generate all substrings |
| Suffix Array | O(|s|² × log(|s|)) | O(|s|²) | Use suffix array |
| Suffix Automaton | O(|s|) | O(|s|) | Use suffix automaton |
| Trie | O(|s|²) | O(|s|²) | Use trie |

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
            for c in s:
                if c not in node.children:
                    node.children[c] = TrieNode()
                node = node.children[c]
            node.is_end = True
        
        def search(self, s):
            node = self.root
            for c in s:
                if c not in node.children:
                    return False
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