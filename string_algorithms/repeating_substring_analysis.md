# CSES Repeating Substring - Problem Analysis

## Problem Statement
Given a string, find the longest substring that appears at least twice.

### Input
The first input line has a string s.

### Output
Print the longest substring that appears at least twice, or -1 if no such substring exists.

### Constraints
- 1 ≤ |s| ≤ 10^5

### Example
```
Input:
ababab

Output:
abab
```

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
                if s[k:k + len(substring)] == substring:
                    count += 1
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
            if h in seen:
                if length > max_length:
                    max_length = length
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