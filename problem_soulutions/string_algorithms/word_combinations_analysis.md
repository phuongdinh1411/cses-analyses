---
layout: simple
title: "Word Combinations"
permalink: /problem_soulutions/string_algorithms/word_combinations_analysis
---

# Word Combinations

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand word combination problems and their applications
- Apply dynamic programming and backtracking techniques for word combinations
- Implement efficient solutions for word combination problems with optimal complexity
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in word combination problems

## 📋 Problem Description

You are given a string s and a dictionary of words. Find all possible ways to break the string into words from the dictionary. Each word from the dictionary can be used multiple times.

**Input**: 
- First line: string s
- Second line: integer n (number of words in dictionary)
- Next n lines: words in the dictionary

**Output**: 
- Print all possible word combinations that form the string s

**Constraints**:
- 1 ≤ |s| ≤ 20
- 1 ≤ n ≤ 1000
- 1 ≤ |word| ≤ 20
- All strings contain only lowercase English letters

**Example**:
```
Input:
catsanddog
3
cat
cats
and
sand
dog

Output:
cat sand dog
cats and dog

Explanation**: 
String: "catsanddog"

Possible word combinations:
1. "cat" + "sand" + "dog" = "catsanddog"
2. "cats" + "and" + "dog" = "catsanddog"

All possible combinations are printed.
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(2^n × m)  
**Space Complexity**: O(n)

**Algorithm**:
1. Try all possible ways to break the string
2. For each break point, check if the substring is in the dictionary
3. Recursively solve for the remaining string
4. Collect all valid combinations

**Implementation**:
```python
def brute_force_word_combinations(s, word_dict):
    results = []
    
    def backtrack(current, remaining):
        if not remaining:
            results.append(current[:])
            return
        
        for i in range(1, len(remaining) + 1):
            word = remaining[:i]
            if word in word_dict:
                current.append(word)
                backtrack(current, remaining[i:])
                current.pop()
    
    backtrack([], s)
    return results
```

**Analysis**:
- **Time**: O(2^n × m) - Exponential time due to all possible combinations
- **Space**: O(n) - Recursion stack depth
- **Limitations**: Too slow for large inputs, exponential time complexity

### Approach 2: Optimized with Memoization
**Time Complexity**: O(n² × m)  
**Space Complexity**: O(n²)

**Algorithm**:
1. Use memoization to cache results for subproblems
2. For each position, try all possible word endings
3. Cache results to avoid redundant calculations

**Implementation**:
```python
def optimized_word_combinations(s, word_dict):
    from functools import lru_cache
    
    @lru_cache(maxsize=None)
    def dp(start):
        if start == len(s):
            return [[]]
        
        results = []
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in word_dict:
                for combination in dp(end):
                    results.append([word] + combination)
        
        return results
    
    return dp(0)
```

**Analysis**:
- **Time**: O(n² × m) - DP with memoization
- **Space**: O(n²) - Memoization cache
- **Improvement**: Much faster than brute force, avoids redundant calculations

### Approach 3: Optimal with Dynamic Programming
**Time Complexity**: O(n² × m)  
**Space Complexity**: O(n²)

**Algorithm**:
1. Use dynamic programming to find all possible combinations
2. DP[i] = list of all combinations for substring s[i:]
3. Build solutions bottom-up from the end

**Implementation**:
```python
def optimal_word_combinations(s, word_dict):
    n = len(s)
    dp = [[] for _ in range(n + 1)]
    dp[n] = [[]]  # Base case: empty string has one combination (empty)
    
    # Build DP table from right to left
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n + 1):
            word = s[i:j]
            if word in word_dict:
                for combination in dp[j]:
                    dp[i].append([word] + combination)
    
    return dp[0]
```

**Analysis**:
- **Time**: O(n² × m) - DP table construction
- **Space**: O(n²) - DP table storage
- **Optimal**: Best possible complexity for this problem

**Visual Example**:
```
String: "catsanddog"
Dictionary: {"cat", "cats", "and", "sand", "dog"}

DP Table:
dp[0] = [["cat", "sand", "dog"], ["cats", "and", "dog"]]
dp[1] = []  # No word starts at position 1
dp[2] = []  # No word starts at position 2
dp[3] = [["sand", "dog"]]  # "cat" ends at position 3
dp[4] = []  # No word starts at position 4
dp[5] = []  # No word starts at position 5
dp[6] = [["dog"]]  # "sand" ends at position 6
dp[7] = [["dog"]]  # "and" ends at position 7
dp[8] = []  # No word starts at position 8
dp[9] = []  # No word starts at position 9
dp[10] = [[]]  # Base case: empty string

Final result: dp[0] = [["cat", "sand", "dog"], ["cats", "and", "dog"]]
```

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Try all possible ways to break the string into words
- **Complete Coverage**: Guarantees finding all valid combinations but inefficient
- **Simple Implementation**: Easy to understand and implement with backtracking

**Key Insights from Optimized Approach**:
- **Memoization**: Cache results for subproblems to avoid redundant calculations
- **Efficiency Improvement**: Much faster than brute force by avoiding repeated work
- **Memory Trade-off**: Use more memory to achieve better time complexity

**Key Insights from Optimal Approach**:
- **Dynamic Programming**: Build solutions bottom-up from the end of the string
- **Optimal Complexity**: Best possible complexity for this problem
- **Systematic Approach**: Process all positions systematically

## 🎯 Key Insights

### 🔑 **Core Concepts**
- **Word Break Problem**: Breaking a string into valid words from a dictionary
- **Dynamic Programming**: Finding all possible solutions using optimal substructure
- **Backtracking**: Exploring all possible combinations systematically
- **Memoization**: Caching results to avoid redundant calculations

### 💡 **Problem-Specific Insights**
- **Word Combinations**: Find all possible ways to break a string into dictionary words
- **Efficiency Optimization**: From O(2^n) brute force to O(n² × m) optimal solution
- **Solution Space**: The problem has exponential solution space in worst case

### 🚀 **Optimization Strategies**
- **Memoization**: Cache results for subproblems to improve performance
- **Bottom-up DP**: Build solutions systematically from the end
- **Early Termination**: Stop when no valid combinations are possible

## 🧠 Common Pitfalls & How to Avoid Them

### ❌ **Common Mistakes**
1. **Exponential Time**: Brute force approach has exponential time complexity
2. **Redundant Calculations**: Not using memoization leads to repeated work
3. **Memory Issues**: Storing all combinations can be memory-intensive

### ✅ **Best Practices**
1. **Use Memoization**: Cache results to avoid redundant calculations
2. **Efficient DP**: Use bottom-up approach for better performance
3. **Memory Management**: Be aware of memory usage for large inputs

## 🔗 Related Problems & Pattern Recognition

### 📚 **Similar Problems**
- **Word Break**: Check if a string can be broken into dictionary words
- **Word Break II**: Find all possible word break combinations
- **String Matching**: Finding patterns in strings

### 🎯 **Pattern Recognition**
- **Word Break Problems**: Problems involving string segmentation
- **DP Problems**: Problems requiring optimal substructure
- **Backtracking Problems**: Problems requiring exploring all possibilities

## 📈 Complexity Analysis

### ⏱️ **Time Complexity**
- **Brute Force**: O(2^n × m) - Exponential time due to all possible combinations
- **Optimized**: O(n² × m) - DP with memoization
- **Optimal**: O(n² × m) - Bottom-up DP approach

### 💾 **Space Complexity**
- **Brute Force**: O(n) - Recursion stack depth
- **Optimized**: O(n²) - Memoization cache
- **Optimal**: O(n²) - DP table storage

## 🎓 Summary

### 🏆 **Key Takeaways**
1. **Word Break Problems**: Important class of string processing problems
2. **Dynamic Programming**: Essential for finding all possible solutions efficiently
3. **Memoization**: Crucial optimization technique for avoiding redundant calculations
4. **Backtracking**: Useful for exploring all possible combinations

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Word Combinations with Dynamic Dictionary
**Problem**: Handle dynamic updates to dictionary and maintain word combination queries efficiently.

**Link**: [CSES Problem Set - Word Combinations with Dynamic Dictionary](https://cses.fi/problemset/task/word_combinations_dynamic_dict)

```python
class WordCombinationsWithDynamicDict:
    def __init__(self, s, dictionary):
        self.s = s
        self.dictionary = set(dictionary)
        self.n = len(s)
        self.dp = {}
        self.memo = {}
    
    def add_word(self, word):
        """Add new word to dictionary"""
        self.dictionary.add(word)
        self.memo.clear()  # Clear memoization cache
    
    def remove_word(self, word):
        """Remove word from dictionary"""
        if word in self.dictionary:
            self.dictionary.remove(word)
            self.memo.clear()  # Clear memoization cache
    
    def word_break(self, s):
        """Check if string can be segmented into dictionary words"""
        if s in self.memo:
            return self.memo[s]
        
        if not s:
            self.memo[s] = True
            return True
        
        for i in range(1, len(s) + 1):
            if s[:i] in self.dictionary and self.word_break(s[i:]):
                self.memo[s] = True
                return True
        
        self.memo[s] = False
        return False
    
    def get_all_combinations(self, s):
        """Get all possible word combinations"""
        if s in self.memo:
            return self.memo[s]
        
        if not s:
            return [[]]
        
        result = []
        for i in range(1, len(s) + 1):
            word = s[:i]
            if word in self.dictionary:
                for combination in self.get_all_combinations(s[i:]):
                    result.append([word] + combination)
        
        self.memo[s] = result
        return result
    
    def count_combinations(self, s):
        """Count number of possible word combinations"""
        if s in self.memo:
            return len(self.memo[s]) if isinstance(self.memo[s], list) else (1 if self.memo[s] else 0)
        
        if not s:
            return 1
        
        count = 0
        for i in range(1, len(s) + 1):
            word = s[:i]
            if word in self.dictionary:
                count += self.count_combinations(s[i:])
        
        self.memo[s] = count
        return count
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'add_word':
                self.add_word(query['word'])
                results.append(None)
            elif query['type'] == 'remove_word':
                self.remove_word(query['word'])
                results.append(None)
            elif query['type'] == 'word_break':
                result = self.word_break(query['s'])
                results.append(result)
            elif query['type'] == 'combinations':
                result = self.get_all_combinations(query['s'])
                results.append(result)
            elif query['type'] == 'count':
                result = self.count_combinations(query['s'])
                results.append(result)
        return results
```

### Variation 2: Word Combinations with Different Operations
**Problem**: Handle different types of operations (break, segment, optimize) on word combinations.

**Link**: [CSES Problem Set - Word Combinations Different Operations](https://cses.fi/problemset/task/word_combinations_operations)

```python
class WordCombinationsDifferentOps:
    def __init__(self, s, dictionary):
        self.s = s
        self.dictionary = set(dictionary)
        self.n = len(s)
        self.memo = {}
    
    def word_break(self, s):
        """Check if string can be segmented into dictionary words"""
        if s in self.memo:
            return self.memo[s]
        
        if not s:
            self.memo[s] = True
            return True
        
        for i in range(1, len(s) + 1):
            if s[:i] in self.dictionary and self.word_break(s[i:]):
                self.memo[s] = True
                return True
        
        self.memo[s] = False
        return False
    
    def get_all_combinations(self, s):
        """Get all possible word combinations"""
        if s in self.memo:
            return self.memo[s]
        
        if not s:
            return [[]]
        
        result = []
        for i in range(1, len(s) + 1):
            word = s[:i]
            if word in self.dictionary:
                for combination in self.get_all_combinations(s[i:]):
                    result.append([word] + combination)
        
        self.memo[s] = result
        return result
    
    def get_minimum_segments(self, s):
        """Get minimum number of segments"""
        if s in self.memo:
            return self.memo[s]
        
        if not s:
            return 0
        
        min_segments = float('inf')
        for i in range(1, len(s) + 1):
            word = s[:i]
            if word in self.dictionary:
                segments = 1 + self.get_minimum_segments(s[i:])
                min_segments = min(min_segments, segments)
        
        self.memo[s] = min_segments if min_segments != float('inf') else -1
        return self.memo[s]
    
    def get_maximum_segments(self, s):
        """Get maximum number of segments"""
        if s in self.memo:
            return self.memo[s]
        
        if not s:
            return 0
        
        max_segments = -1
        for i in range(1, len(s) + 1):
            word = s[:i]
            if word in self.dictionary:
                segments = 1 + self.get_maximum_segments(s[i:])
                max_segments = max(max_segments, segments)
        
        self.memo[s] = max_segments
        return max_segments
    
    def get_optimal_combination(self, s):
        """Get optimal word combination (minimum segments)"""
        if not s:
            return []
        
        min_segments = self.get_minimum_segments(s)
        if min_segments == -1:
            return None
        
        # Find combination with minimum segments
        for i in range(1, len(s) + 1):
            word = s[:i]
            if word in self.dictionary:
                remaining_segments = self.get_minimum_segments(s[i:])
                if remaining_segments != -1 and 1 + remaining_segments == min_segments:
                    combination = self.get_optimal_combination(s[i:])
                    if combination is not None:
                        return [word] + combination
        
        return None
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'word_break':
                result = self.word_break(query['s'])
                results.append(result)
            elif query['type'] == 'combinations':
                result = self.get_all_combinations(query['s'])
                results.append(result)
            elif query['type'] == 'min_segments':
                result = self.get_minimum_segments(query['s'])
                results.append(result)
            elif query['type'] == 'max_segments':
                result = self.get_maximum_segments(query['s'])
                results.append(result)
            elif query['type'] == 'optimal':
                result = self.get_optimal_combination(query['s'])
                results.append(result)
        return results
```

### Variation 3: Word Combinations with Constraints
**Problem**: Handle word combination queries with additional constraints (e.g., maximum segments, minimum word length).

**Link**: [CSES Problem Set - Word Combinations with Constraints](https://cses.fi/problemset/task/word_combinations_constraints)

```python
class WordCombinationsWithConstraints:
    def __init__(self, s, dictionary, max_segments, min_word_length):
        self.s = s
        self.dictionary = set(dictionary)
        self.n = len(s)
        self.max_segments = max_segments
        self.min_word_length = min_word_length
        self.memo = {}
    
    def constrained_word_break(self, s, segments_used):
        """Check if string can be segmented with constraints"""
        if (s, segments_used) in self.memo:
            return self.memo[(s, segments_used)]
        
        if not s:
            self.memo[(s, segments_used)] = True
            return True
        
        if segments_used >= self.max_segments:
            self.memo[(s, segments_used)] = False
            return False
        
        for i in range(self.min_word_length, len(s) + 1):
            word = s[:i]
            if word in self.dictionary and self.constrained_word_break(s[i:], segments_used + 1):
                self.memo[(s, segments_used)] = True
                return True
        
        self.memo[(s, segments_used)] = False
        return False
    
    def get_constrained_combinations(self, s, segments_used):
        """Get all possible word combinations with constraints"""
        if (s, segments_used) in self.memo:
            return self.memo[(s, segments_used)]
        
        if not s:
            return [[]]
        
        if segments_used >= self.max_segments:
            return []
        
        result = []
        for i in range(self.min_word_length, len(s) + 1):
            word = s[:i]
            if word in self.dictionary:
                for combination in self.get_constrained_combinations(s[i:], segments_used + 1):
                    result.append([word] + combination)
        
        self.memo[(s, segments_used)] = result
        return result
    
    def find_valid_combinations(self):
        """Find all valid combinations that satisfy constraints"""
        return self.get_constrained_combinations(self.s, 0)
    
    def get_optimal_constrained_combination(self):
        """Get optimal combination with minimum segments under constraints"""
        min_segments = float('inf')
        best_combination = None
        
        for combination in self.find_valid_combinations():
            if len(combination) < min_segments:
                min_segments = len(combination)
                best_combination = combination
        
        return best_combination
    
    def count_valid_combinations(self):
        """Count number of valid combinations"""
        return len(self.find_valid_combinations())
    
    def get_combination_statistics(self):
        """Get statistics about valid combinations"""
        combinations = self.find_valid_combinations()
        if not combinations:
            return {
                'count': 0,
                'min_segments': 0,
                'max_segments': 0,
                'avg_segments': 0
            }
        
        segment_counts = [len(combo) for combo in combinations]
        return {
            'count': len(combinations),
            'min_segments': min(segment_counts),
            'max_segments': max(segment_counts),
            'avg_segments': sum(segment_counts) / len(segment_counts)
        }

# Example usage
s = "catsanddog"
dictionary = ["cat", "cats", "and", "sand", "dog"]
max_segments = 3
min_word_length = 2

wc = WordCombinationsWithConstraints(s, dictionary, max_segments, min_word_length)
result = wc.constrained_word_break(s, 0)
print(f"Constrained word break result: {result}")

valid_combinations = wc.find_valid_combinations()
print(f"Valid combinations: {valid_combinations}")

optimal = wc.get_optimal_constrained_combination()
print(f"Optimal constrained combination: {optimal}")
```

### Related Problems

#### **CSES Problems**
- [Word Combinations](https://cses.fi/problemset/task/1731) - Basic word combinations problem
- [String Matching](https://cses.fi/problemset/task/1753) - String matching
- [Finding Borders](https://cses.fi/problemset/task/1732) - Find borders of string

#### **LeetCode Problems**
- [Word Break](https://leetcode.com/problems/word-break/) - Check if string can be segmented
- [Word Break II](https://leetcode.com/problems/word-break-ii/) - Find all possible combinations
- [Concatenated Words](https://leetcode.com/problems/concatenated-words/) - Find concatenated words

#### **Problem Categories**
- **Dynamic Programming**: Word break, string segmentation, combination counting
- **Backtracking**: All possible combinations, recursive exploration
- **String Processing**: Dictionary matching, word segmentation, string analysis
- **Advanced String Algorithms**: String matching, pattern recognition, string processing

## 🚀 Key Takeaways

- **Word Break Algorithm**: Essential for string segmentation problems
- **Dynamic Programming**: Essential for finding all possible solutions efficiently
- **Memoization**: Crucial optimization technique for avoiding redundant calculations
- **Backtracking**: Useful for exploring all possible combinations
