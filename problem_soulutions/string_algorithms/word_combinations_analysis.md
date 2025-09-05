---
layout: simple
title: "Word Combinations"
permalink: /problem_soulutions/string_algorithms/word_combinations_analysis
---


# Word Combinations

## 📋 Problem Description

Given a string and a list of words, find the number of ways to construct the string by concatenating the words.

This is a dynamic programming problem where we need to count the number of ways to build a target string using a given set of words. We can solve this using dynamic programming with memoization to avoid recalculating the same subproblems.

**Input**: 
- First line: string s (target string to construct)
- Second line: integer n (number of words)
- Next n lines: words that can be used for construction

**Output**: 
- Print one integer: the number of ways to construct the string

**Constraints**:
- 1 ≤ |s| ≤ 5000
- 1 ≤ n ≤ 100
- 1 ≤ |word| ≤ 100

**Example**:
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

**Explanation**: 
The string "ababc" can be constructed in 4 ways:
1. "ab" + "ab" + "c"
2. "ab" + "abc"
3. "ab" + "ab" + "c" (different order)
4. "abc" + "ab"

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
        
        for word in words: if i + len(word) <= n and s[
i: i + len(word)] == word:
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
            if i + length <= n: substring = s[
i: i + length]
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
        for char in word: if char not in node.
children: node.children[char] = TrieNode()
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
    
    for word in words: if i + len(word) <= len(s) and s[
i: i + len(word)] == word:
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
        
        for word in words: if i + len(word) <= n and s[
i: i + len(word)] == word:
                dp[i + len(word)] += dp[i]
    
    return dp[n]
```

### 2. **Trie Construction Pattern**
```python
def build_trie(words):
    root = TrieNode()
    for word in words:
        node = root
        for char in word: if char not in node.
children: node.children[char] = TrieNode()
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

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Word Combinations with Constraints**
**Problem**: Count ways to construct string with additional constraints (word order, length, etc.).
```python
def constrained_word_combinations(s, words, constraints):
    # constraints = {'min_words': x, 'max_words': y, 'word_order': 'ascending/descending'}
    
    n = len(s)
    dp = [0] * (n + 1)
    dp[0] = 1
    
    for i in range(n):
        if dp[i] == 0:
            continue
        
        for word in words: if i + len(word) <= n and s[
i: i + len(word)] == word:
                # Apply constraints
                if 'word_order' in constraints:
                    if constraints['word_order'] == 'ascending':
                        # Check if word is lexicographically greater than previous
                        pass  # Implementation depends on context
                    elif constraints['word_order'] == 'descending':
                        # Check if word is lexicographically smaller than previous
                        pass  # Implementation depends on context
                
                dp[i + len(word)] += dp[i]
    
    # Apply word count constraints
    if 'min_words' in constraints or 'max_words' in constraints:
        # This would require tracking word count in DP state
        pass  # More complex implementation
    
    return dp[n]
```

#### **Variation 2: Word Combinations with Costs**
**Problem**: Each word has a cost, find combinations with minimum total cost.
```python
def cost_based_word_combinations(s, words, word_costs):
    # word_costs[word] = cost of using word
    
    n = len(s)
    dp = [float('inf')] * (n + 1)
    dp[0] = 0  # Base case: 0 cost for empty string
    
    for i in range(n):
        if dp[i] == float('inf'):
            continue
        
        for word in words: if i + len(word) <= n and s[
i: i + len(word)] == word:
                cost = word_costs.get(word, 1)
                dp[i + len(word)] = min(dp[i + len(word)], dp[i] + cost)
    
    return dp[n] if dp[n] != float('inf') else -1
```

#### **Variation 3: Word Combinations with Probabilities**
**Problem**: Each word has a probability, find expected number of combinations.
```python
def probabilistic_word_combinations(s, words, word_probs):
    # word_probs[word] = probability of using word
    
    n = len(s)
    dp = [0.0] * (n + 1)
    dp[0] = 1.0  # Base case: probability 1 for empty string
    
    for i in range(n):
        if dp[i] == 0.0:
            continue
        
        for word in words: if i + len(word) <= n and s[
i: i + len(word)] == word:
                prob = word_probs.get(word, 0.1)
                dp[i + len(word)] += dp[i] * prob
    
    return dp[n]
```

#### **Variation 4: Word Combinations with Multiple Targets**
**Problem**: Count ways to construct multiple target strings using the same word set.
```python
def multiple_target_word_combinations(targets, words):
    # targets = [s1, s2, s3, ...]
    
    results = []
    
    for s in targets:
        n = len(s)
        dp = [0] * (n + 1)
        dp[0] = 1
        
        for i in range(n):
            if dp[i] == 0:
                continue
            
            for word in words: if i + len(word) <= n and s[
i: i + len(word)] == word:
                    dp[i + len(word)] += dp[i]
        
        results.append(dp[n])
    
    return results
```

#### **Variation 5: Word Combinations with Updates**
**Problem**: Handle dynamic updates to words and recalculate combinations.
```python
def dynamic_word_combinations(s, words, updates):
    # updates = [(word, action), ...] where action is 'add' or 'remove'
    
    current_words = set(words)
    combination_history = []
    
    for word, action in updates:
        if action == 'add':
            current_words.add(word)
        elif action == 'remove':
            current_words.discard(word)
        
        # Recalculate combinations with updated word set
        n = len(s)
        dp = [0] * (n + 1)
        dp[0] = 1
        
        for i in range(n):
            if dp[i] == 0:
                continue
            
            for w in current_words: if i + len(w) <= n and s[
i: i + len(w)] == w:
                    dp[i + len(w)] += dp[i]
        
        combination_history.append(dp[n])
    
    return combination_history
```

### 🔗 **Related Problems & Concepts**

#### **1. String Construction Problems**
- **String Building**: Build strings from parts
- **String Concatenation**: Combine strings efficiently
- **String Assembly**: Assemble strings from components
- **String Generation**: Generate strings with properties

#### **2. Dynamic Programming Problems**
- **Subset Sum**: Find subsets with given sum
- **Knapsack Problems**: Pack items with constraints
- **Partition Problems**: Partition sets into subsets
- **Optimization Problems**: Optimize with constraints

#### **3. String Matching Problems**
- **Pattern Matching**: Find patterns in strings
- **Substring Search**: Search for substrings efficiently
- **Multiple Pattern Matching**: Match multiple patterns
- **Approximate String Matching**: Allow errors in matching

#### **4. Data Structure Problems**
- **Trie Construction**: Build tries for word storage
- **Hash Set Operations**: Efficient word lookup
- **Tree Traversal**: Navigate tree structures
- **Graph Problems**: Model relationships between words

#### **5. Algorithmic Techniques**
- **Dynamic Programming**: Solve optimization problems
- **Memoization**: Cache computed results
- **Greedy Algorithms**: Make locally optimal choices
- **Backtracking**: Try different combinations

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases with Different Strings**
```python
t = int(input())
for _ in range(t):
    s = input().strip()
    n_words = int(input())
    words = [input().strip() for _ in range(n_words)]
    result = dp_string_construction(s, words)
    print(result)
```

#### **2. Range Queries on Word Combinations**
```python
def range_word_combination_queries(s, queries):
    # queries = [(l, r, words), ...] - count combinations for substring s[l:r]
    
    results = []
    for l, r, words in queries: substring = s[
l: r]
        result = dp_string_construction(substring, words)
        results.append(result)
    
    return results
```

#### **3. Interactive Word Combination Problems**
```python
def interactive_word_combinations():
    while True:
        s = input("Enter target string (or 'quit' to exit): ")
        if s.lower() == 'quit':
            break
        
        n_words = int(input("Enter number of words: "))
        words = []
        for _ in range(n_words):
            word = input("Enter word: ")
            words.append(word)
        
        result = dp_string_construction(s, words)
        print(f"Target: {s}")
        print(f"Words: {words}")
        print(f"Number of combinations: {result}")
```

### 🧮 **Mathematical Extensions**

#### **1. Combinatorics**
- **String Enumeration**: Count strings with properties
- **Combination Counting**: Count combinations and permutations
- **Partition Theory**: Study of partitions
- **Generating Functions**: Algebraic approach to counting

#### **2. Probability Theory**
- **Expected Values**: Calculate expected outcomes
- **Probability Distributions**: Word probability distributions
- **Stochastic Processes**: Random word generation
- **Markov Chains**: State transitions in word sequences

#### **3. Optimization Theory**
- **Linear Programming**: Mathematical optimization
- **Integer Programming**: Discrete optimization
- **Convex Optimization**: Optimization with convex functions
- **Combinatorial Optimization**: Optimization over discrete structures

## 🔧 Implementation Details

### Time and Space Complexity
- **Time Complexity**: O(n × |s|) for dynamic programming approach
- **Space Complexity**: O(|s|) for memoization table
- **Why it works**: Dynamic programming avoids recalculating the same subproblems by storing results in a memoization table

### Key Implementation Points
- Use dynamic programming with memoization to avoid exponential time complexity
- For each position in the string, try all possible words that match
- Store results to avoid recalculating the same subproblems
- Handle edge cases like empty strings and no valid combinations

## 🎨 Visual Example

### Input Example
```
Target String: "ababc"
Words: ["ab", "ab", "c", "abc"]
```

### Understanding the Problem
```
Target: a b a b c
Index:  0 1 2 3 4

Available words:
- "ab" (length 2)
- "ab" (length 2) 
- "c" (length 1)
- "abc" (length 3)

Goal: Count ways to construct "ababc" using these words
```

### All Possible Combinations
```
Combination 1: "ab" + "ab" + "c"
a b a b c
└─┘ └─┘ └┘
ab  ab  c

Combination 2: "ab" + "abc"
a b a b c
└─┘ └───┘
ab  abc

Combination 3: "abc" + "ab"
a b a b c
└───┘ └─┘
abc  ab

Combination 4: "ab" + "ab" + "c" (different order)
a b a b c
└─┘ └─┘ └┘
ab  ab  c

Total: 4 ways
```

### Dynamic Programming Approach
```
Target: a b a b c
Index:  0 1 2 3 4

DP Table: dp[i] = number of ways to construct s[0:i]

Initialization:
dp[0] = 1 (empty string has 1 way: use no words)
dp[1] = 0
dp[2] = 0
dp[3] = 0
dp[4] = 0
dp[5] = 0

Step 1: Check position 0
Words that match at position 0:
- "ab" (s[0:2] = "ab") ✓
- "abc" (s[0:3] = "abc") ✓

Update:
dp[2] += dp[0] = 1 (ways to make "ab")
dp[3] += dp[0] = 1 (ways to make "abc")

DP: [1, 0, 1, 1, 0, 0]

Step 2: Check position 1
Words that match at position 1:
- None (s[1:2] = "b", s[1:3] = "ba", s[1:4] = "bab")

DP: [1, 0, 1, 1, 0, 0]

Step 3: Check position 2
Words that match at position 2:
- "ab" (s[2:4] = "ab") ✓
- "c" (s[2:3] = "c") ✓

Update:
dp[4] += dp[2] = 1 (ways to make "abab")
dp[3] += dp[2] = 2 (ways to make "abc")

DP: [1, 0, 1, 2, 1, 0]

Step 4: Check position 3
Words that match at position 3:
- "c" (s[3:4] = "c") ✓

Update:
dp[4] += dp[3] = 3 (ways to make "ababc")

DP: [1, 0, 1, 2, 3, 0]

Step 5: Check position 4
Words that match at position 4:
- "c" (s[4:5] = "c") ✓

Update:
dp[5] += dp[4] = 3 (ways to make "ababc")

Final DP: [1, 0, 1, 2, 3, 3]

Result: dp[5] = 3 ways to construct "ababc"
```

### Step-by-Step Construction Process
```
Target: a b a b c
Index:  0 1 2 3 4

Path 1: dp[0] → dp[2] → dp[4] → dp[5]
- Start: dp[0] = 1
- Use "ab": dp[2] = 1
- Use "ab": dp[4] = 1  
- Use "c": dp[5] = 1
- Construction: "ab" + "ab" + "c"

Path 2: dp[0] → dp[3] → dp[5]
- Start: dp[0] = 1
- Use "abc": dp[3] = 1
- Use "ab": dp[5] = 1
- Construction: "abc" + "ab"

Path 3: dp[0] → dp[2] → dp[3] → dp[5]
- Start: dp[0] = 1
- Use "ab": dp[2] = 1
- Use "c": dp[3] = 2
- Use "ab": dp[5] = 2
- Construction: "ab" + "c" + "ab"

Total: 3 distinct ways
```

### Word Matching Visualization
```
Target: a b a b c
Index:  0 1 2 3 4

Word "ab" (length 2):
- Position 0: s[0:2] = "ab" ✓
- Position 1: s[1:3] = "ba" ✗
- Position 2: s[2:4] = "ab" ✓
- Position 3: s[3:5] = "bc" ✗

Word "c" (length 1):
- Position 0: s[0:1] = "a" ✗
- Position 1: s[1:2] = "b" ✗
- Position 2: s[2:3] = "a" ✗
- Position 3: s[3:4] = "b" ✗
- Position 4: s[4:5] = "c" ✓

Word "abc" (length 3):
- Position 0: s[0:3] = "abc" ✓
- Position 1: s[1:4] = "bab" ✗
- Position 2: s[2:5] = "abc" ✓
```

### Algorithm Flowchart
```
                    Start
                      │
                      ▼
              ┌─────────────────┐
              │ Input: string s,│
              │ words[]         │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Initialize DP   │
              │ dp[0] = 1       │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ For each        │
              │ position i      │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ For each word   │
              │ in words[]      │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Does word match │
              │ at position i?  │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Update DP:      │
              │ dp[i+len] +=    │
              │ dp[i]           │
              └─────────────────┘
                      │
                      ▼
              ┌─────────────────┐
              │ Return dp[n]    │
              └─────────────────┘
                      │
                      ▼
                    End
```

## 🎯 Key Insights

### Important Concepts and Patterns
- **Dynamic Programming**: Essential for avoiding exponential time complexity
- **String Matching**: Efficiently check if a word matches at a given position
- **Memoization**: Store results of subproblems to avoid recalculation
- **Word Combinations**: Count ways to construct strings using given words

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Word Combinations with Minimum Cost**
```python
def word_combinations_minimum_cost(s, words, costs):
    # Find minimum cost to construct the string
    n = len(s)
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    
    for i in range(n + 1):
        if dp[i] != float('inf'):
            for word, cost in zip(words, costs):
                if i + len(word) <= n and s[i:i+len(word)] == word:
                    dp[i + len(word)] = min(dp[i + len(word)], dp[i] + cost)
    
    return dp[n] if dp[n] != float('inf') else -1

# Example usage
s = "ababc"
words = ["ab", "abc", "c"]
costs = [2, 3, 1]
result = word_combinations_minimum_cost(s, words, costs)
print(f"Minimum cost: {result}")
```

#### **2. Word Combinations with Maximum Length**
```python
def word_combinations_maximum_length(s, words):
    # Find maximum length of constructed string
    n = len(s)
    dp = [0] * (n + 1)
    
    for i in range(n + 1):
        if dp[i] > 0 or i == 0:
            for word in words:
                if i + len(word) <= n and s[i:i+len(word)] == word:
                    dp[i + len(word)] = max(dp[i + len(word)], dp[i] + len(word))
    
    return max(dp)

# Example usage
s = "ababc"
words = ["ab", "abc", "c"]
result = word_combinations_maximum_length(s, words)
print(f"Maximum length: {result}")
```

#### **3. Word Combinations with All Solutions**
```python
def word_combinations_all_solutions(s, words):
    # Find all possible ways to construct the string
    n = len(s)
    dp = [[] for _ in range(n + 1)]
    dp[0] = [[]]  # Empty combination for empty string
    
    for i in range(n + 1):
        if dp[i]:
            for word in words:
                if i + len(word) <= n and s[i:i+len(word)] == word:
                    for combination in dp[i]:
                        dp[i + len(word)].append(combination + [word])
    
    return dp[n]

# Example usage
s = "ababc"
words = ["ab", "abc", "c"]
result = word_combinations_all_solutions(s, words)
print(f"All solutions: {result}")
```

#### **4. Word Combinations with Constraints**
```python
def word_combinations_with_constraints(s, words, max_words, max_length):
    # Find combinations with constraints on number of words and total length
    n = len(s)
    dp = [[0] * (max_words + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    
    for i in range(n + 1):
        for j in range(max_words + 1):
            if dp[i][j] > 0:
                for word in words:
                    if (i + len(word) <= n and 
                        j + 1 <= max_words and 
                        i + len(word) <= max_length and
                        s[i:i+len(word)] == word):
                        dp[i + len(word)][j + 1] += dp[i][j]
    
    return sum(dp[n])

# Example usage
s = "ababc"
words = ["ab", "abc", "c"]
max_words = 3
max_length = 10
result = word_combinations_with_constraints(s, words, max_words, max_length)
print(f"Combinations with constraints: {result}")
```

## 🔗 Related Problems

### Links to Similar Problems
- **String Algorithms**: String matching, Pattern matching
- **Dynamic Programming**: Coin change, Subset sum
- **Combinatorics**: Counting problems, Permutations
- **String Construction**: String building, Word formation

## 📚 Learning Points

### Key Takeaways
- **Dynamic programming** is essential for avoiding exponential time complexity
- **String matching** can be optimized using efficient algorithms
- **Memoization** helps avoid recalculating the same subproblems
- **Word combinations** is a fundamental string construction problem

---

*This analysis demonstrates efficient word combination techniques and shows various extensions for string construction problems.* 