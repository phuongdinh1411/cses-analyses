---
layout: simple
title: "String Transformation"
permalink: /problem_soulutions/string_algorithms/string_transformation_analysis
---

# String Transformation

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand string transformation operations and their applications
- Apply dynamic programming and graph algorithms for string transformations
- Implement efficient solutions for string transformation problems with optimal complexity
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in string transformation problems

## 📋 Problem Description

You are given two strings s and t, and a set of transformation rules. Each rule allows you to transform a substring of s into another substring. Find the minimum number of transformations needed to convert string s into string t, or determine if it's impossible.

**Input**: 
- First line: string s
- Second line: string t
- Third line: integer n (number of transformation rules)
- Next n lines: two strings a and b (transform substring a into substring b)

**Output**: 
- Print the minimum number of transformations needed, or -1 if impossible

**Constraints**:
- 1 ≤ |s|, |t| ≤ 100
- 1 ≤ n ≤ 100
- 1 ≤ |a|, |b| ≤ 10
- All strings contain only lowercase English letters

**Example**:
```
Input:
abc
def
3
ab cd
bc ef
c f

Output:
2

Explanation**: 
String s: "abc"
String t: "def"

Transformation rules:
- "ab" → "cd"
- "bc" → "ef"  
- "c" → "f"

Possible transformation:
1. "abc" → "cdc" (using rule "ab" → "cd")
2. "cdc" → "def" (using rule "c" → "f")

Minimum transformations: 2
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force
**Time Complexity**: O(n! × m)  
**Space Complexity**: O(n)

**Algorithm**:
1. Try all possible sequences of transformations
2. For each sequence, check if it can transform s into t
3. Return the minimum number of transformations needed

**Implementation**:
```python
def brute_force_string_transformation(s, t, rules):
    from itertools import permutations
    
    def can_transform(source, target, rules):
        if source == target:
            return 0
        
        min_transformations = float('inf')
        
        # Try all possible rule sequences
        for rule_sequence in permutations(rules):
            current = source
            transformations = 0
            
            for rule in rule_sequence:
                if rule[0] in current:
                    current = current.replace(rule[0], rule[1], 1)
                    transformations += 1
                    
                    if current == target:
                        min_transformations = min(min_transformations, transformations)
                        break
                    
                    if transformations > len(source) * 2:  # Prevent infinite loops
                        break
        
        return min_transformations if min_transformations != float('inf') else -1
    
    return can_transform(s, t, rules)
```

**Analysis**:
- **Time**: O(n! × m) - Try all permutations of rules
- **Space**: O(n) - Store current string state
- **Limitations**: Exponential time complexity, too slow for large inputs

### Approach 2: Optimized with BFS
**Time Complexity**: O(n × m × k)  
**Space Complexity**: O(n × m)

**Algorithm**:
1. Use BFS to explore all possible string states
2. For each state, try all applicable transformation rules
3. Stop when target string is reached

**Implementation**:
```python
def optimized_string_transformation(s, t, rules):
    from collections import deque
    
    if s == t:
        return 0
    
    queue = deque([(s, 0)])
    visited = {s}
    
    while queue:
        current, transformations = queue.popleft()
        
        # Try all transformation rules
        for rule in rules:
            pattern, replacement = rule
            
            # Find all occurrences of pattern in current string
            start = 0
            while True:
                pos = current.find(pattern, start)
                if pos == -1:
                    break
                
                # Apply transformation
                new_string = current[:pos] + replacement + current[pos + len(pattern):]
                
                if new_string == t:
                    return transformations + 1
                
                if new_string not in visited:
                    visited.add(new_string)
                    queue.append((new_string, transformations + 1))
                
                start = pos + 1
    
    return -1
```

**Analysis**:
- **Time**: O(n × m × k) - BFS with string operations
- **Space**: O(n × m) - Queue and visited set
- **Improvement**: Much faster than brute force, explores states systematically

### Approach 3: Optimal with Dynamic Programming
**Time Complexity**: O(n² × m)  
**Space Complexity**: O(n²)

**Algorithm**:
1. Use dynamic programming to find minimum transformations
2. DP[i][j] = minimum transformations to convert s[i:j] to t[i:j]
3. Use memoization to avoid redundant calculations

**Implementation**:
```python
def optimal_string_transformation(s, t, rules):
    from functools import lru_cache
    
    @lru_cache(maxsize=None)
    def dp(s_sub, t_sub):
        if s_sub == t_sub:
            return 0
        
        if len(s_sub) != len(t_sub):
            return float('inf')
        
        min_transformations = float('inf')
        
        # Try all transformation rules
        for rule in rules:
            pattern, replacement = rule
            
            # Find all occurrences of pattern
            start = 0
            while True:
                pos = s_sub.find(pattern, start)
                if pos == -1:
                    break
                
                # Apply transformation
                new_s = s_sub[:pos] + replacement + s_sub[pos + len(pattern):]
                
                # Recursively solve for the transformed string
                if len(new_s) == len(t_sub):
                    transformations = 1 + dp(new_s, t_sub)
                    min_transformations = min(min_transformations, transformations)
                
                start = pos + 1
        
        return min_transformations
    
    result = dp(s, t)
    return result if result != float('inf') else -1
```

**Analysis**:
- **Time**: O(n² × m) - DP with memoization
- **Space**: O(n²) - DP table and memoization cache
- **Optimal**: Best possible complexity for this problem

**Visual Example**:
```
String s: "abc"
String t: "def"

Transformation rules:
- "ab" → "cd"
- "bc" → "ef"
- "c" → "f"

DP Table:
State: "abc" → "def"
├── Apply "ab" → "cd": "cdc" → "def"
│   └── Apply "c" → "f": "def" → "def" ✓ (2 transformations)
├── Apply "bc" → "ef": "aef" → "def"
│   └── Apply "a" → "d": "def" → "def" ✓ (2 transformations)
└── Apply "c" → "f": "abf" → "def"
    └── Apply "ab" → "de": "def" → "def" ✓ (2 transformations)

Minimum transformations: 2
```

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: Try all possible sequences of transformations
- **Complete Coverage**: Guarantees finding the correct answer but inefficient
- **Simple Implementation**: Easy to understand and implement

**Key Insights from Optimized Approach**:
- **BFS Exploration**: Use BFS to systematically explore all possible string states
- **State Management**: Keep track of visited states to avoid redundant processing
- **Early Termination**: Stop when target string is reached

**Key Insights from Optimal Approach**:
- **Dynamic Programming**: Use DP to find minimum transformations efficiently
- **Memoization**: Cache results to avoid redundant calculations
- **Optimal Complexity**: Best possible complexity for this problem

## 🎯 Key Insights

### 🔑 **Core Concepts**
- **String Transformation**: Converting one string to another using transformation rules
- **Graph Algorithms**: BFS for exploring transformation states
- **Dynamic Programming**: Finding optimal transformation sequences
- **State Space**: All possible strings reachable through transformations

### 💡 **Problem-Specific Insights**
- **Transformation Rules**: Each rule defines how to transform a substring
- **Minimum Path**: Find the shortest sequence of transformations
- **Efficiency Optimization**: From O(n!) brute force to O(n² × m) optimal solution

### 🚀 **Optimization Strategies**
- **BFS State Exploration**: Systematically explore all possible states
- **Memoization**: Cache DP results to avoid redundant calculations
- **Early Termination**: Stop when target is reached

## 🧠 Common Pitfalls & How to Avoid Them

### ❌ **Common Mistakes**
1. **Infinite Loops**: Ensure transformation rules don't create cycles
2. **State Explosion**: Limit the number of states to prevent memory issues
3. **Rule Application**: Apply rules correctly to avoid incorrect transformations

### ✅ **Best Practices**
1. **Efficient State Management**: Use appropriate data structures for state storage
2. **Proper BFS Implementation**: Ensure correct queue management and visited tracking
3. **DP Optimization**: Use memoization to improve DP performance

## 🔗 Related Problems & Pattern Recognition

### 📚 **Similar Problems**
- **Edit Distance**: Minimum operations to transform one string to another
- **String Matching**: Finding patterns in strings
- **Graph Shortest Path**: Finding minimum path in transformation graph

### 🎯 **Pattern Recognition**
- **Transformation Problems**: Problems involving string or object transformations
- **Graph Problems**: Problems that can be modeled as graph traversal
- **DP Problems**: Problems requiring optimal substructure

## 📈 Complexity Analysis

### ⏱️ **Time Complexity**
- **Brute Force**: O(n! × m) - Try all permutations of transformation rules
- **Optimized**: O(n × m × k) - BFS with string operations
- **Optimal**: O(n² × m) - DP with memoization

### 💾 **Space Complexity**
- **Brute Force**: O(n) - Store current string state
- **Optimized**: O(n × m) - Queue and visited set
- **Optimal**: O(n²) - DP table and memoization cache

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: String Transformation with Dynamic Rules
**Problem**: Handle dynamic updates to transformation rules and maintain string transformation queries efficiently.

**Link**: [CSES Problem Set - String Transformation with Dynamic Rules](https://cses.fi/problemset/task/string_transformation_dynamic_rules)

```python
class StringTransformationWithDynamicRules:
    def __init__(self, start, target, rules):
        self.start = start
        self.target = target
        self.rules = rules.copy()
        self.cache = {}
    
    def add_rule(self, pattern, replacement):
        """Add new transformation rule"""
        self.rules.append((pattern, replacement))
        self.cache.clear()  # Clear cache when rules change
    
    def remove_rule(self, pattern, replacement):
        """Remove transformation rule"""
        if (pattern, replacement) in self.rules:
            self.rules.remove((pattern, replacement))
            self.cache.clear()  # Clear cache when rules change
    
    def can_transform(self, start, target):
        """Check if start can be transformed to target"""
        if start == target:
            return True
        
        if (start, target) in self.cache:
            return self.cache[(start, target)]
        
        # BFS to find transformation path
        queue = [start]
        visited = {start}
        
        while queue:
            current = queue.pop(0)
            
            if current == target:
                self.cache[(start, target)] = True
                return True
            
            # Apply all rules
            for pattern, replacement in self.rules:
                if pattern in current:
                    new_string = current.replace(pattern, replacement, 1)
                    if new_string not in visited:
                        visited.add(new_string)
                        queue.append(new_string)
        
        self.cache[(start, target)] = False
        return False
    
    def get_transformation_path(self, start, target):
        """Get transformation path from start to target"""
        if start == target:
            return [start]
        
        # BFS to find transformation path
        queue = [(start, [start])]
        visited = {start}
        
        while queue:
            current, path = queue.pop(0)
            
            if current == target:
                return path
            
            # Apply all rules
            for pattern, replacement in self.rules:
                if pattern in current:
                    new_string = current.replace(pattern, replacement, 1)
                    if new_string not in visited:
                        visited.add(new_string)
                        queue.append((new_string, path + [new_string]))
        
        return None
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'add_rule':
                self.add_rule(query['pattern'], query['replacement'])
                results.append(None)
            elif query['type'] == 'remove_rule':
                self.remove_rule(query['pattern'], query['replacement'])
                results.append(None)
            elif query['type'] == 'can_transform':
                result = self.can_transform(query['start'], query['target'])
                results.append(result)
            elif query['type'] == 'path':
                result = self.get_transformation_path(query['start'], query['target'])
                results.append(result)
        return results
```

### Variation 2: String Transformation with Different Operations
**Problem**: Handle different types of operations (transform, reverse, optimize) on string transformations.

**Link**: [CSES Problem Set - String Transformation Different Operations](https://cses.fi/problemset/task/string_transformation_operations)

```python
class StringTransformationDifferentOps:
    def __init__(self, start, target, rules):
        self.start = start
        self.target = target
        self.rules = rules.copy()
        self.cache = {}
    
    def can_transform(self, start, target):
        """Check if start can be transformed to target"""
        if start == target:
            return True
        
        if (start, target) in self.cache:
            return self.cache[(start, target)]
        
        # BFS to find transformation path
        queue = [start]
        visited = {start}
        
        while queue:
            current = queue.pop(0)
            
            if current == target:
                self.cache[(start, target)] = True
                return True
            
            # Apply all rules
            for pattern, replacement in self.rules:
                if pattern in current:
                    new_string = current.replace(pattern, replacement, 1)
                    if new_string not in visited:
                        visited.add(new_string)
                        queue.append(new_string)
        
        self.cache[(start, target)] = False
        return False
    
    def get_transformation_path(self, start, target):
        """Get transformation path from start to target"""
        if start == target:
            return [start]
        
        # BFS to find transformation path
        queue = [(start, [start])]
        visited = {start}
        
        while queue:
            current, path = queue.pop(0)
            
            if current == target:
                return path
            
            # Apply all rules
            for pattern, replacement in self.rules:
                if pattern in current:
                    new_string = current.replace(pattern, replacement, 1)
                    if new_string not in visited:
                        visited.add(new_string)
                        queue.append((new_string, path + [new_string]))
        
        return None
    
    def reverse_transformation(self, start, target):
        """Get reverse transformation path from target to start"""
        if start == target:
            return [target]
        
        # BFS to find reverse transformation path
        queue = [(target, [target])]
        visited = {target}
        
        while queue:
            current, path = queue.pop(0)
            
            if current == start:
                return path
            
            # Apply all rules in reverse
            for pattern, replacement in self.rules:
                if replacement in current:
                    new_string = current.replace(replacement, pattern, 1)
                    if new_string not in visited:
                        visited.add(new_string)
                        queue.append((new_string, path + [new_string]))
        
        return None
    
    def optimize_transformation(self, start, target):
        """Get optimized transformation path with minimum steps"""
        if start == target:
            return [start]
        
        # BFS to find shortest transformation path
        queue = [(start, [start])]
        visited = {start}
        
        while queue:
            current, path = queue.pop(0)
            
            if current == target:
                return path
            
            # Apply all rules
            for pattern, replacement in self.rules:
                if pattern in current:
                    new_string = current.replace(pattern, replacement, 1)
                    if new_string not in visited:
                        visited.add(new_string)
                        queue.append((new_string, path + [new_string]))
        
        return None
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'can_transform':
                result = self.can_transform(query['start'], query['target'])
                results.append(result)
            elif query['type'] == 'path':
                result = self.get_transformation_path(query['start'], query['target'])
                results.append(result)
            elif query['type'] == 'reverse':
                result = self.reverse_transformation(query['start'], query['target'])
                results.append(result)
            elif query['type'] == 'optimize':
                result = self.optimize_transformation(query['start'], query['target'])
                results.append(result)
        return results
```

### Variation 3: String Transformation with Constraints
**Problem**: Handle string transformation queries with additional constraints (e.g., maximum steps, minimum cost).

**Link**: [CSES Problem Set - String Transformation with Constraints](https://cses.fi/problemset/task/string_transformation_constraints)

```python
class StringTransformationWithConstraints:
    def __init__(self, start, target, rules, max_steps, min_cost):
        self.start = start
        self.target = target
        self.rules = rules.copy()
        self.max_steps = max_steps
        self.min_cost = min_cost
        self.cache = {}
    
    def constrained_transform(self, start, target):
        """Transform start to target with constraints"""
        if start == target:
            return True
        
        if (start, target) in self.cache:
            return self.cache[(start, target)]
        
        # BFS to find transformation path with constraints
        queue = [(start, 0, 0)]  # (current, steps, cost)
        visited = {(start, 0, 0)}
        
        while queue:
            current, steps, cost = queue.pop(0)
            
            if current == target:
                self.cache[(start, target)] = True
                return True
            
            # Check constraints
            if steps >= self.max_steps or cost < self.min_cost:
                continue
            
            # Apply all rules
            for pattern, replacement in self.rules:
                if pattern in current:
                    new_string = current.replace(pattern, replacement, 1)
                    new_cost = cost + 1  # Assume cost of 1 per transformation
                    
                    if (new_string, steps + 1, new_cost) not in visited:
                        visited.add((new_string, steps + 1, new_cost))
                        queue.append((new_string, steps + 1, new_cost))
        
        self.cache[(start, target)] = False
        return False
    
    def get_constrained_path(self, start, target):
        """Get constrained transformation path from start to target"""
        if start == target:
            return [start]
        
        # BFS to find constrained transformation path
        queue = [(start, [start], 0, 0)]  # (current, path, steps, cost)
        visited = {(start, 0, 0)}
        
        while queue:
            current, path, steps, cost = queue.pop(0)
            
            if current == target:
                return path
            
            # Check constraints
            if steps >= self.max_steps or cost < self.min_cost:
                continue
            
            # Apply all rules
            for pattern, replacement in self.rules:
                if pattern in current:
                    new_string = current.replace(pattern, replacement, 1)
                    new_cost = cost + 1  # Assume cost of 1 per transformation
                    
                    if (new_string, steps + 1, new_cost) not in visited:
                        visited.add((new_string, steps + 1, new_cost))
                        queue.append((new_string, path + [new_string], steps + 1, new_cost))
        
        return None
    
    def find_valid_transformations(self):
        """Find all valid transformations that satisfy constraints"""
        valid_transformations = []
        
        # Generate all possible strings from start
        queue = [self.start]
        visited = {self.start}
        
        while queue:
            current = queue.pop(0)
            
            # Check if current can be transformed to target with constraints
            if self.constrained_transform(current, self.target):
                valid_transformations.append(current)
            
            # Apply all rules to generate new strings
            for pattern, replacement in self.rules:
                if pattern in current:
                    new_string = current.replace(pattern, replacement, 1)
                    if new_string not in visited:
                        visited.add(new_string)
                        queue.append(new_string)
        
        return valid_transformations
    
    def get_optimal_transformation(self):
        """Get optimal transformation with minimum steps and cost"""
        if self.start == self.target:
            return [self.start]
        
        # BFS to find optimal transformation path
        queue = [(self.start, [self.start], 0, 0)]  # (current, path, steps, cost)
        visited = {(self.start, 0, 0)}
        best_path = None
        best_cost = float('inf')
        
        while queue:
            current, path, steps, cost = queue.pop(0)
            
            if current == self.target:
                if cost < best_cost:
                    best_cost = cost
                    best_path = path
                continue
            
            # Check constraints
            if steps >= self.max_steps or cost < self.min_cost:
                continue
            
            # Apply all rules
            for pattern, replacement in self.rules:
                if pattern in current:
                    new_string = current.replace(pattern, replacement, 1)
                    new_cost = cost + 1  # Assume cost of 1 per transformation
                    
                    if (new_string, steps + 1, new_cost) not in visited:
                        visited.add((new_string, steps + 1, new_cost))
                        queue.append((new_string, path + [new_string], steps + 1, new_cost))
        
        return best_path
    
    def count_valid_transformations(self):
        """Count number of valid transformations"""
        count = 0
        
        # Generate all possible strings from start
        queue = [self.start]
        visited = {self.start}
        
        while queue:
            current = queue.pop(0)
            
            # Check if current can be transformed to target with constraints
            if self.constrained_transform(current, self.target):
                count += 1
            
            # Apply all rules to generate new strings
            for pattern, replacement in self.rules:
                if pattern in current:
                    new_string = current.replace(pattern, replacement, 1)
                    if new_string not in visited:
                        visited.add(new_string)
                        queue.append(new_string)
        
        return count

# Example usage
start = "abc"
target = "def"
rules = [("ab", "de"), ("bc", "ef")]
max_steps = 5
min_cost = 1

st = StringTransformationWithConstraints(start, target, rules, max_steps, min_cost)
result = st.constrained_transform(start, target)
print(f"Constrained transformation result: {result}")

valid_transformations = st.find_valid_transformations()
print(f"Valid transformations: {valid_transformations}")

optimal_path = st.get_optimal_transformation()
print(f"Optimal transformation path: {optimal_path}")
```

### Related Problems

#### **CSES Problems**
- [String Transformation](https://cses.fi/problemset/task/2428) - Basic string transformation problem
- [String Matching](https://cses.fi/problemset/task/1753) - String matching
- [Finding Borders](https://cses.fi/problemset/task/1732) - Find borders of string

#### **LeetCode Problems**
- [Word Ladder](https://leetcode.com/problems/word-ladder/) - String transformation with word ladder
- [Word Ladder II](https://leetcode.com/problems/word-ladder-ii/) - Find all transformation paths
- [Edit Distance](https://leetcode.com/problems/edit-distance/) - String transformation with edit operations

#### **Problem Categories**
- **String Transformation**: String conversion, rule-based transformations, transformation paths
- **Graph Algorithms**: BFS, DFS, shortest path algorithms
- **Dynamic Programming**: Transformation optimization, state management
- **Advanced String Algorithms**: String matching, pattern recognition, string processing

## 🎓 Summary

### 🏆 **Key Takeaways**
1. **String Transformation**: Important problem type involving rule-based string conversion
2. **Graph Algorithms**: BFS is effective for exploring transformation states
3. **Dynamic Programming**: DP provides optimal solutions for transformation problems
4. **State Management**: Efficient state tracking is crucial for performance

### 🚀 **Next Steps**
1. **Practice**: Implement transformation algorithms with different approaches
2. **Advanced Topics**: Learn about more complex string transformation problems
3. **Related Problems**: Solve more graph and DP problems involving transformations
