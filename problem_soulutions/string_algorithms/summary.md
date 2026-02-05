---
layout: simple
title: "String Algorithms Summary"
permalink: /problem_soulutions/string_algorithms/summary
---

# String Algorithms

Welcome to the String Algorithms section! This category covers fundamental and advanced algorithms for text processing and pattern matching.

## 🎯 Visual Example

### String Algorithm Techniques Overview
```
1. Pattern Matching:
   Text:    "ababcababc"
   Pattern: "ababc"
   Result:  Found at positions 0, 5

2. String Rotation:
   Original: "abacaba"
   Rotations: "bacabaa", "acabaab", "cabaaba", ...
   Minimal:   "aabacab"

3. Palindrome Detection:
   String: "racecar"
   Check:  r-a-c-e-c-a-r
   Result: True (palindrome)

4. String Compression:
   Input:  "aaabbbcc"
   Output: "a3b3c2"
```

### Algorithm Complexity Comparison
```
Algorithm          | Time    | Space   | Use Case
-------------------|---------|---------|------------------
KMP                | O(n+m)  | O(m)    | Pattern matching
Z-Algorithm        | O(n+m)  | O(n+m)  | Border detection
Manacher's         | O(n)    | O(n)    | Palindrome
Booth's            | O(n)    | O(n)    | Minimal rotation
Run-length         | O(n)    | O(n)    | Compression
```

## Key Concepts & Techniques

### Basic String Operations

#### String Comparison
- **When to use**: Lexicographic ordering, sorting strings
- **Time**: O(min(|s1|, |s2|))
- **Implementation**: Compare character by character
- **Applications**: String sorting, binary search on strings

#### Substring Operations
- **When to use**: Extracting parts of strings, pattern matching
- **Time**: O(k) for substring of length k
- **Implementation**: Use string slicing or character iteration
- **Applications**: Text processing, data extraction

#### String Concatenation
- **When to use**: Building strings from parts
- **Time**: O(|s1| + |s2|)
- **Implementation**: Use string concatenation operators
- **Applications**: String construction, text generation

#### String Rotation
- **When to use**: Cyclic shifts, finding minimal rotation
- **Time**: O(n) for rotation, O(n) for minimal rotation
- **Implementation**: Use modular arithmetic for indices
- **Applications**: String matching, lexicographic ordering

### Pattern Matching Algorithms

#### Knuth-Morris-Pratt (KMP) Algorithm
- **When to use**: Single pattern matching, finding all occurrences
- **Time**: O(n + m) where n is text length, m is pattern length
- **Space**: O(m) for failure function
- **Applications**: Text search, DNA sequence analysis
- **Implementation**: Precompute failure function, then match

#### Z Algorithm
- **When to use**: Pattern matching, finding borders, periods
- **Time**: O(n + m)
- **Space**: O(n + m)
- **Applications**: String matching, border detection
- **Implementation**: Compute Z-array using previous values

#### Rabin-Karp Algorithm
- **When to use**: Multiple pattern matching, rolling hash
- **Time**: O(n + m) average, O(nm) worst case
- **Space**: O(1) additional space
- **Applications**: Plagiarism detection, multiple pattern search
- **Implementation**: Rolling hash with collision handling

#### Boyer-Moore Algorithm
- **When to use**: Single pattern matching in long texts
- **Time**: O(n/m) best case, O(nm) worst case
- **Space**: O(m)
- **Applications**: Text editors, search engines
- **Implementation**: Bad character rule and good suffix rule

### Advanced String Techniques

#### String Hashing
- **When to use**: Fast string comparison, rolling hash
- **Time**: O(n) preprocessing, O(1) comparison
- **Space**: O(n)
- **Applications**: String matching, duplicate detection
- **Implementation**: Polynomial rolling hash with large prime

#### Suffix Array
- **When to use**: String indexing, multiple pattern matching
- **Time**: O(n log n) construction, O(m log n) per query
- **Space**: O(n)
- **Applications**: Genome analysis, text compression
- **Implementation**: Sort all suffixes, use binary search

#### Suffix Tree
- **When to use**: Multiple pattern matching, string analysis
- **Time**: O(n) construction, O(m) per query
- **Space**: O(n)
- **Applications**: Bioinformatics, text processing
- **Implementation**: Ukkonen's algorithm

#### Suffix Automaton
- **When to use**: String analysis, pattern matching
- **Time**: O(n) construction, O(m) per query
- **Space**: O(n)
- **Applications**: String processing, pattern analysis
- **Implementation**: Incremental construction

### Specialized String Algorithms

#### Manacher's Algorithm
- **When to use**: Finding all palindromes, longest palindrome
- **Time**: O(n)
- **Space**: O(n)
- **Applications**: Palindrome detection, string analysis
- **Implementation**: Expand around centers with optimization

#### Aho-Corasick Algorithm
- **When to use**: Multiple pattern matching
- **Time**: O(n + m + z) where z is number of matches
- **Space**: O(m)
- **Applications**: Virus scanning, text mining
- **Implementation**: Trie with failure links

#### Trie (Prefix Tree)
- **When to use**: Prefix matching, dictionary operations
- **Time**: O(m) per operation where m is string length
- **Space**: O(ALPHABET_SIZE * N * M)
- **Applications**: Autocomplete, spell checkers
- **Implementation**: Tree with character-based edges

#### Rolling Hash
- **When to use**: Sliding window problems, string comparison
- **Time**: O(1) per update
- **Space**: O(1)
- **Applications**: Pattern matching, duplicate detection
- **Implementation**: Update hash using previous value

### String Analysis Techniques

#### Border Detection
- **When to use**: Finding string borders, period detection
- **Time**: O(n)
- **Space**: O(n)
- **Applications**: String compression, pattern analysis
- **Implementation**: Use KMP failure function or Z-array

#### Period Detection
- **When to use**: Finding repeating patterns, string compression
- **Time**: O(n)
- **Space**: O(n)
- **Applications**: Data compression, pattern recognition
- **Implementation**: Use border properties or Z-array

#### Palindrome Detection
- **When to use**: Finding palindromic substrings
- **Time**: O(n²) naive, O(n) with Manacher's
- **Space**: O(n)
- **Applications**: String analysis, text processing
- **Implementation**: Expand around centers or use Manacher's

#### String Compression
- **When to use**: Reducing string size, pattern recognition
- **Time**: O(n)
- **Space**: O(n)
- **Applications**: Data compression, text analysis
- **Implementation**: Run-length encoding or pattern-based compression

### Optimization Techniques

#### Space Optimization
- **Rolling Arrays**: When only previous values needed
  - *When to use*: DP problems on strings
  - *Example*: Edit distance with rolling array
- **In-place Processing**: Modify string in place
  - *When to use*: When original string not needed
  - *Example*: Remove duplicates in place

#### Time Optimization
- **Preprocessing**: Compute values once
  - *When to use*: Multiple queries on same string
  - *Example*: Suffix array for multiple pattern searches
- **Early Termination**: Stop when condition met
  - *When to use*: When exact match not needed
  - *Example*: Stop KMP when first match found

#### Memory Optimization
- **String Interning**: Share common strings
  - *When to use*: Many duplicate strings
  - *Example*: Dictionary with string interning
- **Lazy Evaluation**: Compute on demand
  - *When to use*: When not all values needed
  - *Example*: Lazy suffix array construction

## Problem Categories

### String Properties
- [Finding Borders](finding_borders_analysis) - Border detection in strings
- [Finding Periods](finding_periods_analysis) - Periodic patterns
- [Minimal Rotation](minimal_rotation_analysis) - Lexicographically minimal rotation

### Pattern Matching
- [String Matching](string_matching_analysis) - Basic pattern matching
- [Pattern Positions](pattern_positions_analysis) - Find all pattern occurrences
- [Longest Palindrome](longest_palindrome_analysis) - Palindrome detection

### String Construction
- [Word Combinations](word_combinations_analysis) - Dictionary-based construction
- [Repeating Substring](repeating_substring_analysis) - Finding repetitions

### Advanced String Problems
- [Distinct Strings](distinct_strings_analysis) - Counting unique strings
- [Distinct Substrings](distinct_substrings_analysis) - Counting unique substrings

## Detailed Examples and Implementations

### Classic String Algorithms with Code

#### 1. Knuth-Morris-Pratt (KMP) Algorithm
```python
def kmp_search(text, pattern):
  def build_failure_function(pattern):
    m = len(pattern)
    failure = [0] * m
    j = 0
    
    for i in range(1, m):
      while j > 0 and pattern[i] != pattern[j]:
        j = failure[j - 1]
      
      if pattern[i] == pattern[j]:
        j += 1
      
      failure[i] = j
    
    return failure
  
  n, m = len(text), len(pattern)
  if m == 0:
    return 0
  
  failure = build_failure_function(pattern)
  j = 0
  
  for i in range(n):
    while j > 0 and text[i] != pattern[j]:
      j = failure[j - 1]
    
    if text[i] == pattern[j]:
      j += 1
    
    if j == m:
      return i - m + 1
  
  return -1

def kmp_find_all(text, pattern):
  def build_failure_function(pattern):
    m = len(pattern)
    failure = [0] * m
    j = 0
    
    for i in range(1, m):
      while j > 0 and pattern[i] != pattern[j]:
        j = failure[j - 1]
      
      if pattern[i] == pattern[j]:
        j += 1
      
      failure[i] = j
    
    return failure
  
  n, m = len(text), len(pattern)
  if m == 0:
    return list(range(n + 1))
  
  failure = build_failure_function(pattern)
  j = 0
  matches = []
  
  for i in range(n):
    while j > 0 and text[i] != pattern[j]:
      j = failure[j - 1]
    
    if text[i] == pattern[j]:
      j += 1
    
    if j == m:
      matches.append(i - m + 1)
      j = failure[j - 1]
  
  return matches
```

#### 2. Z Algorithm
```python
def z_algorithm(text):
  n = len(text)
  z = [0] * n
  l, r = 0, 0
  
  for i in range(1, n):
    if i <= r:
      z[i] = min(r - i + 1, z[i - l])
    
    while i + z[i] < n and text[z[i]] == text[i + z[i]]:
      z[i] += 1
    
    if i + z[i] - 1 > r:
      l, r = i, i + z[i] - 1
  
  return z

def z_search(text, pattern):
  combined = pattern + '$' + text
  z = z_algorithm(combined)
  m = len(pattern)
  matches = []
  
  for i in range(m + 1, len(combined)):
    if z[i] == m:
      matches.append(i - m - 1)
  
  return matches
```

#### 3. Rabin-Karp Algorithm
```python
def rabin_karp(text, pattern, base=256, mod=10**9 + 7):
  n, m = len(text), len(pattern)
  if m == 0:
    return 0
  if m > n:
    return -1
  
  # Calculate hash of pattern and first window of text
  pattern_hash = 0
  text_hash = 0
  h = 1
  
  # Calculate h = base^(m-1) % mod
  for i in range(m - 1):
    h = (h * base) % mod
  
  # Calculate initial hashes
  for i in range(m):
    pattern_hash = (base * pattern_hash + ord(pattern[i])) % mod
    text_hash = (base * text_hash + ord(text[i])) % mod
  
  # Slide the pattern over text
  for i in range(n - m + 1):
    if pattern_hash == text_hash:
      # Check character by character
      if text[i:i+m] == pattern:
        return i
    
    if i < n - m:
      # Remove leading digit, add trailing digit
      text_hash = (base * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % mod
      if text_hash < 0:
        text_hash += mod
  
  return -1

def rabin_karp_multiple_patterns(text, patterns, base=256, mod=10**9 + 7):
  n = len(text)
  results = {}
  
  for pattern in patterns:
    m = len(pattern)
    if m == 0:
      results[pattern] = [0]
      continue
    if m > n:
      results[pattern] = []
      continue
    
    pattern_hash = 0
    text_hash = 0
    h = 1
    
    for i in range(m - 1):
      h = (h * base) % mod
    
    for i in range(m):
      pattern_hash = (base * pattern_hash + ord(pattern[i])) % mod
      text_hash = (base * text_hash + ord(text[i])) % mod
    
    matches = []
    for i in range(n - m + 1):
      if pattern_hash == text_hash:
        if text[i:i+m] == pattern:
          matches.append(i)
      
      if i < n - m:
        text_hash = (base * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % mod
        if text_hash < 0:
          text_hash += mod
    
    results[pattern] = matches
  
  return results
```

#### 4. Manacher's Algorithm for Palindromes
```python
def manacher_algorithm(text):
  # Transform string to handle even-length palindromes
  transformed = '#'.join('^{}$'.format(text))
  n = len(transformed)
  p = [0] * n
  center, right = 0, 0
  
  for i in range(1, n - 1):
    # Mirror index
    mirror = 2 * center - i
    
    if i < right:
      p[i] = min(right - i, p[mirror])
    
    # Try to expand palindrome centered at i
    try:
      while transformed[i + (1 + p[i])] == transformed[i - (1 + p[i])]:
        p[i] += 1
    except IndexError:
      pass
    
    # Update center and right if palindrome extends beyond right
    if i + p[i] > right:
      center, right = i, i + p[i]
  
  # Find maximum length and center
  max_len = 0
  center_index = 0
  for i in range(1, n - 1):
    if p[i] > max_len:
      max_len = p[i]
      center_index = i
  
  start = (center_index - max_len) // 2
  return text[start:start + max_len]

def find_all_palindromes(text):
  transformed = '#'.join('^{}$'.format(text))
  n = len(transformed)
  p = [0] * n
  center, right = 0, 0
  palindromes = []
  
  for i in range(1, n - 1):
    mirror = 2 * center - i
    
    if i < right:
      p[i] = min(right - i, p[mirror])
    
    try:
      while transformed[i + (1 + p[i])] == transformed[i - (1 + p[i])]:
        p[i] += 1
    except IndexError:
      pass
    
    if i + p[i] > right:
      center, right = i, i + p[i]
    
    # Store palindrome if length > 1
    if p[i] > 0:
      start = (i - p[i]) // 2
      length = p[i]
      palindromes.append((start, start + length))
  
  return palindromes
```

### Advanced String Data Structures

#### 1. Suffix Array Construction
```python
def build_suffix_array(text):
  n = len(text)
  k = 1
  c = [ord(text[i]) for i in range(n)]
  sa = list(range(n))
  
  while k < n:
    # Sort suffixes by first k characters
    sa.sort(key=lambda x: (c[x], c[x + k]) if x + k < n else (c[x], -1))
    
    # Update equivalence classes
    new_c = [0] * n
    new_c[sa[0]] = 0
    
    for i in range(1, n):
      curr = (c[sa[i]], c[sa[i] + k]) if sa[i] + k < n else (c[sa[i]], -1)
      prev = (c[sa[i-1]], c[sa[i-1] + k]) if sa[i-1] + k < n else (c[sa[i-1]], -1)
      
      if curr == prev:
        new_c[sa[i]] = new_c[sa[i-1]]
      else:
        new_c[sa[i]] = new_c[sa[i-1]] + 1
    
    c = new_c
    k *= 2
  
  return sa

def build_lcp_array(text, sa):
  n = len(text)
  lcp = [0] * n
  rank = [0] * n
  
  for i in range(n):
    rank[sa[i]] = i
  
  k = 0
  for i in range(n):
    if rank[i] == n - 1:
      k = 0
      continue
    
    j = sa[rank[i] + 1]
    while i + k < n and j + k < n and text[i + k] == text[j + k]:
      k += 1
    
    lcp[rank[i]] = k
    if k > 0:
      k -= 1
  
  return lcp
```

#### 2. Trie Implementation
```python
class TrieNode:
  def __init__(self):
    self.children = {}
    self.is_end_of_word = False
    self.count = 0

class Trie:
  def __init__(self):
    self.root = TrieNode()
  
  def insert(self, word):
    node = self.root
    for char in word:
      if char not in node.children:
        node.children[char] = TrieNode()
      node = node.children[char]
      node.count += 1
    node.is_end_of_word = True
  
  def search(self, word):
    node = self.root
    for char in word:
      if char not in node.children:
        return False
      node = node.children[char]
    return node.is_end_of_word
  
  def starts_with(self, prefix):
    node = self.root
    for char in prefix:
      if char not in node.children:
        return False
      node = node.children[char]
    return True
  
  def count_prefix(self, prefix):
    node = self.root
    for char in prefix:
      if char not in node.children:
        return 0
      node = node.children[char]
    return node.count
  
  def delete(self, word):
    def delete_helper(node, word, index):
      if index == len(word):
        if not node.is_end_of_word:
          return False
        node.is_end_of_word = False
        return len(node.children) == 0
      
      char = word[index]
      if char not in node.children:
        return False
      
      should_delete = delete_helper(node.children[char], word, index + 1)
      
      if should_delete:
        del node.children[char]
        return len(node.children) == 0 and not node.is_end_of_word
      
      return False
    
    delete_helper(self.root, word, 0)
```

#### 3. Aho-Corasick Algorithm
```python
class AhoCorasickNode:
  def __init__(self):
    self.children = {}
    self.failure = None
    self.output = []
    self.is_end = False

class AhoCorasick:
  def __init__(self):
    self.root = AhoCorasickNode()
  
  def add_pattern(self, pattern):
    node = self.root
    for char in pattern:
      if char not in node.children:
        node.children[char] = AhoCorasickNode()
      node = node.children[char]
    node.is_end = True
    node.output.append(pattern)
  
  def build_failure_links(self):
    queue = []
    
    # Initialize failure links for first level
    for char, child in self.root.children.items():
      child.failure = self.root
      queue.append(child)
    
    # Build failure links for remaining levels
    while queue:
      current = queue.pop(0)
      
      for char, child in current.children.items():
        queue.append(child)
        failure = current.failure
        
        while failure is not None and char not in failure.children:
          failure = failure.failure
        
        if failure is not None:
          child.failure = failure.children[char]
        else:
          child.failure = self.root
        
        # Merge output sets
        child.output.extend(child.failure.output)
  
  def search(self, text):
    results = []
    current = self.root
    
    for i, char in enumerate(text):
      # Follow failure links until we find a match or reach root
      while current is not None and char not in current.children:
        current = current.failure
      
      if current is not None:
        current = current.children[char]
      else:
        current = self.root
      
      # Collect all matches at current position
      for pattern in current.output:
        results.append((i - len(pattern) + 1, pattern))
    
    return results
```

### String Processing Techniques

#### 1. Rolling Hash Implementation
```python
class RollingHash:
  def __init__(self, text, base=256, mod=10**9 + 7):
    self.text = text
    self.base = base
    self.mod = mod
    self.n = len(text)
    self.powers = [1] * (self.n + 1)
    
    # Precompute powers
    for i in range(1, self.n + 1):
      self.powers[i] = (self.powers[i-1] * base) % mod
    
    # Precompute prefix hashes
    self.prefix_hashes = [0] * (self.n + 1)
    for i in range(self.n):
      self.prefix_hashes[i+1] = (self.prefix_hashes[i] * base + ord(text[i])) % mod
  
  def get_hash(self, start, end):
    if start >= end:
      return 0
    
    hash_value = (self.prefix_hashes[end] - 
          self.prefix_hashes[start] * self.powers[end - start]) % self.mod
    
    return hash_value if hash_value >= 0 else hash_value + self.mod
  
  def get_substring_hash(self, start, length):
    return self.get_hash(start, start + length)
```

#### 2. String Compression
```python
def run_length_encoding(text):
  if not text:
    return ""
  
  result = []
  current_char = text[0]
  count = 1
  
  for i in range(1, len(text)):
    if text[i] == current_char:
      count += 1
    else:
      result.append(f"{count}{current_char}")
      current_char = text[i]
      count = 1
  
  result.append(f"{count}{current_char}")
  return "".join(result)

def run_length_decoding(encoded):
  if not encoded:
    return ""
  
  result = []
  i = 0
  
  while i < len(encoded):
    # Extract count
    count_str = ""
    while i < len(encoded) and encoded[i].isdigit():
      count_str += encoded[i]
      i += 1
    
    if i < len(encoded):
      char = encoded[i]
      count = int(count_str)
      result.append(char * count)
      i += 1
  
  return "".join(result)

def lz77_compression(text, window_size=4096, lookahead_size=18):
  compressed = []
  i = 0
  
  while i < len(text):
    # Find longest match in sliding window
    best_match = (0, 0)  # (offset, length)
    
    # Search in sliding window
    start = max(0, i - window_size)
    for j in range(start, i):
      match_length = 0
      while (match_length < lookahead_size and 
         i + match_length < len(text) and
         j + match_length < i and
         text[j + match_length] == text[i + match_length]):
        match_length += 1
      
      if match_length > best_match[1]:
        best_match = (i - j, match_length)
    
    if best_match[1] > 0:
      # Encode as (offset, length, next_char)
      next_char = text[i + best_match[1]] if i + best_match[1] < len(text) else ""
      compressed.append((best_match[0], best_match[1], next_char))
      i += best_match[1] + 1
    else:
      # Encode as literal
      compressed.append((0, 0, text[i]))
      i += 1
  
  return compressed
```

### Advanced String Analysis

#### 1. Period Detection
```python
def find_period(text):
  n = len(text)
  
  # Check all possible periods
  for period in range(1, n + 1):
    if n % period != 0:
      continue
    
    is_period = True
    for i in range(period, n):
      if text[i] != text[i % period]:
        is_period = False
        break
    
    if is_period:
      return period
  
  return n

def find_all_periods(text):
  n = len(text)
  periods = []
  
  for period in range(1, n + 1):
    if n % period != 0:
      continue
    
    is_period = True
    for i in range(period, n):
      if text[i] != text[i % period]:
        is_period = False
        break
    
    if is_period:
      periods.append(period)
  
  return periods

def border_array(text):
  n = len(text)
  border = [0] * n
  j = 0
  
  for i in range(1, n):
    while j > 0 and text[i] != text[j]:
      j = border[j - 1]
    
    if text[i] == text[j]:
      j += 1
    
    border[i] = j
  
  return border
```

#### 2. String Rotation and Cyclic Shifts
```python
def is_rotation(s1, s2):
  if len(s1) != len(s2):
    return False
  
  return s2 in s1 + s1

def find_rotation_point(text):
  n = len(text)
  left, right = 0, n - 1
  
  while left < right:
    mid = (left + right) // 2
    
    if text[mid] > text[right]:
      left = mid + 1
    else:
      right = mid
  
  return left

def lexicographically_minimal_rotation(text):
  n = len(text)
  text = text + text  # Double the string
  i, j = 0, 1
  
  while j < n:
    k = 0
    while k < n and text[i + k] == text[j + k]:
      k += 1
    
    if text[i + k] > text[j + k]:
      i = max(i + k + 1, j)
      j = i + 1
    else:
      j = j + k + 1
  
  return text[i:i + n]
```

## Tips for Success

1. **Master Basic Operations**: String manipulation
2. **Understand KMP**: Essential for pattern matching
3. **Learn Hashing**: Fast string comparison
4. **Practice Implementation**: Code common algorithms
5. **Study Data Structures**: Trie, Suffix Array, etc.
6. **Handle Edge Cases**: Empty strings, single characters

## Common Pitfalls to Avoid

1. **Time Limits**: With naive algorithms
2. **Memory Usage**: With large strings
3. **Hash Collisions**: In string hashing
4. **Edge Cases**: Empty strings, single characters
5. **Index Errors**: Off-by-one mistakes
6. **Unicode Issues**: Multi-byte characters

## Advanced Topics

### String Data Structures
- **Suffix Array**: String searching
- **Suffix Tree**: Pattern matching
- **Trie**: Prefix matching
- **Aho-Corasick**: Multiple pattern matching

### Optimization Techniques
- **Rolling Hash**: Fast comparison
- **Z Algorithm**: Linear time matching
- **Suffix Links**: Fast transitions
- **Failure Functions**: Pattern matching

### Special Cases
- **Palindromes**: Symmetric strings
- **Periodic Strings**: Repeating patterns
- **Rotations**: Cyclic shifts
- **Substrings**: Continuous subsequences

## Algorithm Complexities

### Pattern Matching
- **Naive Algorithm**: O(nm) time
- **KMP Algorithm**: O(n+m) time
- **Z Algorithm**: O(n+m) time
- **Rabin-Karp**: O(n+m) average time

### String Processing
- **String Hashing**: O(n) preprocessing
- **Suffix Array**: O(n log n) construction
- **Trie**: O(n) construction
- **Manacher's**: O(n) palindrome finding

## 📚 **Additional Learning Resources**

### **LeetCode Pattern Integration**
For interview preparation and pattern recognition, complement your CSES learning with these LeetCode resources:

- **[Awesome LeetCode Resources](https://github.com/ashishps1/awesome-leetcode-resources)** - Comprehensive collection of LeetCode patterns, templates, and curated problem lists
- **[15 LeetCode Patterns](https://github.com/ashishps1/awesome-leetcode-resources#-patterns)** - Essential patterns including Sliding Window, Two Pointers, and String Manipulation
- **[String Algorithm Patterns](https://github.com/ashishps1/awesome-leetcode-resources#-must-read-leetcode-articles)** - Specific string processing templates and techniques

### **Related LeetCode Problems**
Practice these LeetCode problems to reinforce string algorithm concepts:

- **Sliding Window Pattern**: [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/), [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/)
- **Two Pointers Pattern**: [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/), [Reverse String](https://leetcode.com/problems/reverse-string/)
- **String Hashing**: [Repeated String Match](https://leetcode.com/problems/repeated-string-match/), [Rabin-Karp Pattern Matching](https://leetcode.com/problems/implement-strstr/)

---

Ready to start? Begin with [Finding Borders](finding_borders_analysis) and work your way through the problems in order of difficulty!