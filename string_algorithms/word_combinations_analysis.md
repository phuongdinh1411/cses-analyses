# CSES Word Combinations - Problem Analysis

## Problem Statement
Given a string and a list of words, find the number of ways to construct the string by concatenating the words.

### Input
The first input line has a string s.
The second input line has an integer n: the number of words.
Then, there are n lines describing the words.

### Output
Print one integer: the number of ways to construct the string.

### Constraints
- 1 ≤ |s| ≤ 5000
- 1 ≤ n ≤ 100
- 1 ≤ |word| ≤ 100

### Example
```
Input:
ababc
4
ab
ab
c
abc

Output:
4
```

## Solution Progression

### Approach 1: Recursive Backtracking - O(n^|s|)
**Description**: Try all possible combinations of words recursively.

```python
def word_combinations_recursive(s, words):
    def backtrack(target, index):
        if index == len(target):
            return 1
        
        count = 0
        for word in words:
            if target.startswith(word, index):
                count += backtrack(target, index + len(word))
        
        return count
    
    return backtrack(s, 0)
```

**Why this is inefficient**: Exponential time complexity due to trying all possible combinations.

### Improvement 1: Dynamic Programming - O(|s| * max_word_length * n)
**Description**: Use dynamic programming to avoid recalculating subproblems.

```python
def word_combinations_dp(s, words):
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1  # Empty string has one way
    
    for i in range(n):
        if dp[i] == 0:
            continue
        
        for word in words:
            if i + len(word) <= n and s[i:i + len(word)] == word:
                dp[i + len(word)] += dp[i]
    
    return dp[n]
```

**Why this improvement works**: Dynamic programming avoids recalculating subproblems and has polynomial time complexity.

### Improvement 2: Optimized DP with Word Length Filtering - O(|s| * max_word_length * n)
**Description**: Optimize by filtering words by length and using set for faster lookups.

```python
def word_combinations_optimized_dp(s, words):
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    
    # Create a set of words for faster lookup
    word_set = set(words)
    
    # Group words by length for efficiency
    word_lengths = {}
    for word in words:
        length = len(word)
        if length not in word_lengths:
            word_lengths[length] = []
        word_lengths[length].append(word)
    
    for i in range(n):
        if dp[i] == 0:
            continue
        
        # Try words of different lengths
        for length, word_list in word_lengths.items():
            if i + length <= n:
                substring = s[i:i + length]
                if substring in word_set:
                    dp[i + length] += dp[i]
    
    return dp[n]
```

**Why this improvement works**: Grouping words by length and using set lookup improves efficiency.

### Alternative: Trie-based Approach - O(|s| * max_word_length)
**Description**: Use a trie data structure for efficient word matching.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

def build_trie(words):
    root = TrieNode()
    for word in words:
        node = root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    return root

def word_combinations_trie(s, words):
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    
    trie = build_trie(words)
    
    for i in range(n):
        if dp[i] == 0:
            continue
        
        # Traverse trie from current position
        node = trie
        j = i
        while j < n and s[j] in node.children:
            node = node.children[s[j]]
            if node.is_end:
                dp[j + 1] += dp[i]
            j += 1
    
    return dp[n]
```

**Why this works**: Trie provides efficient prefix matching and reduces the number of comparisons.

## Final Optimal Solution

```python
s = input().strip()
n = int(input())
words = [input().strip() for _ in range(n)]

# Dynamic programming solution
dp = [0] * (len(s) + 1)
dp[0] = 1  # Empty string has one way

for i in range(len(s)):
    if dp[i] == 0:
        continue
    
    for word in words:
        if i + len(word) <= len(s) and s[i:i + len(word)] == word:
            dp[i + len(word)] += dp[i]

print(dp[len(s)])
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Recursive Backtracking | O(n^|s|) | O(|s|) | Exponential due to all combinations |
| Dynamic Programming | O(|s| * max_word_length * n) | O(|s|) | Avoid recalculating subproblems |
| Optimized DP | O(|s| * max_word_length * n) | O(|s|) | Group words by length |
| Trie-based | O(|s| * max_word_length) | O(total_word_length) | Efficient prefix matching |

## Key Insights for Other Problems

### 1. **String Construction Problems**
**Principle**: Use dynamic programming to count ways to construct strings from smaller parts.
**Applicable to**:
- String construction problems
- Dynamic programming
- String algorithms
- Algorithm design

**Example Problems**:
- String construction problems
- Dynamic programming
- String algorithms
- Algorithm design

### 2. **Dynamic Programming on Strings**
**Principle**: Use DP to avoid recalculating subproblems in string construction.
**Applicable to**:
- String algorithms
- Dynamic programming
- Algorithm design
- Problem solving

**Example Problems**:
- String algorithms
- Dynamic programming
- Algorithm design
- Problem solving

### 3. **Word Matching Optimization**
**Principle**: Optimize word matching using data structures like tries or hash sets.
**Applicable to**:
- String algorithms
- Data structures
- Algorithm design
- Problem solving

**Example Problems**:
- String algorithms
- Data structures
- Algorithm design
- Problem solving

### 4. **Substring Matching**
**Principle**: Use efficient substring matching techniques for word lookup.
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

### 1. **DP String Construction Pattern**
```python
def dp_string_construction(s, words):
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    
    for i in range(n):
        if dp[i] == 0:
            continue
        
        for word in words:
            if i + len(word) <= n and s[i:i + len(word)] == word:
                dp[i + len(word)] += dp[i]
    
    return dp[n]
```

### 2. **Trie Construction Pattern**
```python
def build_trie(words):
    root = TrieNode()
    for word in words:
        node = root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    return root
```

### 3. **Word Length Grouping Pattern**
```python
def group_words_by_length(words):
    word_lengths = {}
    for word in words:
        length = len(word)
        if length not in word_lengths:
            word_lengths[length] = []
        word_lengths[length].append(word)
    return word_lengths
```

## Edge Cases to Remember

1. **Empty string**: Should return 1 (one way to construct empty string)
2. **No valid construction**: Should return 0
3. **Overlapping words**: Handle multiple ways to match at same position
4. **Long words**: Handle words longer than remaining string
5. **Duplicate words**: Count each occurrence separately

## Problem-Solving Framework

1. **Identify construction nature**: This is a string construction problem
2. **Choose approach**: Use dynamic programming for efficiency
3. **Define state**: dp[i] = ways to construct string up to index i
4. **Handle transitions**: Try all words that match at current position
5. **Return result**: Return dp[length of string]

---

*This analysis shows how to efficiently count ways to construct strings using dynamic programming.* 