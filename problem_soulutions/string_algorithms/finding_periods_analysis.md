---
layout: simple
title: "Finding Periods"
permalink: /problem_soulutions/string_algorithms/finding_periods_analysis
---

# Finding Periods

## 📋 Problem Information

### 🎯 **Learning Objectives**
By the end of this problem, you should be able to:
- Understand the concept of string periods and their mathematical properties
- Apply KMP algorithm and failure function for period detection
- Implement efficient solutions for period finding problems with optimal complexity
- Optimize solutions for large inputs with proper complexity analysis
- Handle edge cases in period detection problems

### 📚 **Prerequisites**
Before attempting this problem, ensure you understand:
- **Algorithm Knowledge**: KMP algorithm, failure function, period detection, string matching
- **Data Structures**: Strings, failure arrays, prefix arrays
- **Mathematical Concepts**: String periods, failure function properties, period theory
- **Programming Skills**: String manipulation, KMP implementation, complexity analysis
- **Related Problems**: Finding Borders (KMP), Pattern Positions (KMP), String Matching (KMP)

## 📋 Problem Description

You are given a string s of length n. For each position i (1 ≤ i ≤ n), find the smallest period of the prefix s[1...i].

A period of a string is the smallest positive integer p such that s[i] = s[i + p] for all valid positions i.

**Input**: 
- One string s (the input string)

**Output**: 
- Print n integers: the smallest period of each prefix s[1...i]

**Constraints**:
- 1 ≤ n ≤ 10⁶
- String contains only lowercase English letters

**Example**:
```
Input:
abacaba

Output:
1 2 2 4 4 4 4

Explanation**: 
String: "abacaba"

Prefix s[1...1] = "a": period = 1
Prefix s[1...2] = "ab": period = 2 (no repetition)
Prefix s[1...3] = "aba": period = 2 (repeats "ab" + "a")
Prefix s[1...4] = "abac": period = 4 (no repetition)
Prefix s[1...5] = "abaca": period = 4 (repeats "abac" + "a")
Prefix s[1...6] = "abacab": period = 4 (repeats "abac" + "ab")
Prefix s[1...7] = "abacaba": period = 4 (repeats "abac" + "aba")
```

## 🔍 Solution Analysis: From Brute Force to Optimal

### Approach 1: Brute Force

**Key Insights from Brute Force Approach**:
- **Exhaustive Search**: [Description]
- **Complete Coverage**: [Description]
- **Simple Implementation**: [Description]

**Key Insight**: [Main insight]

**Algorithm**:
- [Step 1]
- [Step 2]
- [Step 3]

**Implementation**:
```python
def brute_force_finding_periods(text, pattern):
    """
    [Description]
    
    Args:
        text: [Description]
        pattern: [Description]
    
    Returns:
        [Description]
    """
    # Implementation will be added
    pass
```

**Time Complexity**: O([complexity])
**Space Complexity**: O([complexity])

**Why it's inefficient**: [Reason]

---

### Approach 2: Optimized

**Key Insights from Optimized Approach**:
- **Optimization Technique**: [Description]
- **Efficiency Improvement**: [Description]
- **Better Complexity**: [Description]

**Key Insight**: [Main insight]

**Algorithm**:
- [Step 1]
- [Step 2]
- [Step 3]

**Implementation**:
```python
def optimized_finding_periods(text, pattern):
    """
    [Description]
    
    Args:
        text: [Description]
        pattern: [Description]
    
    Returns:
        [Description]
    """
    # Implementation will be added
    pass
```

**Time Complexity**: O([complexity])
**Space Complexity**: O([complexity])

**Why it's better**: [Reason]

---

### Approach 3: Optimal

**Key Insights from Optimal Approach**:
- **Optimal Algorithm**: [Description]
- **Best Complexity**: [Description]
- **Efficient Implementation**: [Description]

**Key Insight**: [Main insight]

**Algorithm**:
- [Step 1]
- [Step 2]
- [Step 3]

**Implementation**:
```python
def optimal_finding_periods(text, pattern):
    """
    [Description]
    
    Args:
        text: [Description]
        pattern: [Description]
    
    Returns:
        [Description]
    """
    # Implementation will be added
    pass
```

**Time Complexity**: O([complexity])
**Space Complexity**: O([complexity])

**Why it's optimal**: [Reason]

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O([complexity]) | O([complexity]) | [Insight] |
| Optimized | O([complexity]) | O([complexity]) | [Insight] |
| Optimal | O([complexity]) | O([complexity]) | [Insight] |

### Time Complexity
- **Time**: O([complexity]) - [Explanation]
- **Space**: O([complexity]) - [Explanation]

### Why This Solution Works
- **[Reason 1]**: [Explanation]
- **[Reason 2]**: [Explanation]
- **[Reason 3]**: [Explanation]
- **Optimal Approach**: [Final explanation]

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

### Variation 1: Finding Periods with Dynamic Updates
**Problem**: Handle dynamic updates to string characters and maintain period information efficiently.

**Link**: [CSES Problem Set - Finding Periods with Updates](https://cses.fi/problemset/task/finding_periods_updates)

```python
class FindingPeriodsWithUpdates:
    def __init__(self, s):
        self.s = list(s)
        self.n = len(self.s)
        self.failure_function = self._build_failure_function()
        self.periods = self._calculate_periods()
    
    def _build_failure_function(self):
        """Build failure function using KMP algorithm"""
        failure = [0] * self.n
        
        for i in range(1, self.n):
            j = failure[i - 1]
            while j > 0 and self.s[i] != self.s[j]:
                j = failure[j - 1]
            if self.s[i] == self.s[j]:
                j += 1
            failure[i] = j
        
        return failure
    
    def _calculate_periods(self):
        """Calculate periods for all prefixes"""
        periods = []
        
        for i in range(self.n):
            prefix_length = i + 1
            failure_value = self.failure_function[i]
            
            if failure_value > 0 and prefix_length % (prefix_length - failure_value) == 0:
                period = prefix_length - failure_value
            else:
                period = prefix_length
            
            periods.append(period)
        
        return periods
    
    def update(self, pos, char):
        """Update character at position pos"""
        if pos < 0 or pos >= self.n:
            return
        
        self.s[pos] = char
        
        # Rebuild failure function and periods
        self.failure_function = self._build_failure_function()
        self.periods = self._calculate_periods()
    
    def get_period(self, prefix_length):
        """Get period of prefix of given length"""
        if prefix_length < 1 or prefix_length > self.n:
            return -1
        
        return self.periods[prefix_length - 1]
    
    def get_all_periods(self):
        """Get periods for all prefixes"""
        return self.periods.copy()
    
    def find_periodic_substrings(self, min_length=2):
        """Find all periodic substrings of given minimum length"""
        periodic_substrings = []
        
        for length in range(min_length, self.n + 1):
            for start in range(self.n - length + 1):
                substring = ''.join(self.s[start:start + length])
                period = self._get_substring_period(substring)
                
                if period < length:
                    periodic_substrings.append({
                        'substring': substring,
                        'start': start,
                        'length': length,
                        'period': period
                    })
        
        return periodic_substrings
    
    def _get_substring_period(self, substring):
        """Get period of a substring"""
        n = len(substring)
        failure = [0] * n
        
        for i in range(1, n):
            j = failure[i - 1]
            while j > 0 and substring[i] != substring[j]:
                j = failure[j - 1]
            if substring[i] == substring[j]:
                j += 1
            failure[i] = j
        
        if failure[n - 1] > 0 and n % (n - failure[n - 1]) == 0:
            return n - failure[n - 1]
        else:
            return n
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'update':
                self.update(query['pos'], query['char'])
                results.append(None)
            elif query['type'] == 'period':
                result = self.get_period(query['prefix_length'])
                results.append(result)
            elif query['type'] == 'all_periods':
                result = self.get_all_periods()
                results.append(result)
            elif query['type'] == 'periodic_substrings':
                result = self.find_periodic_substrings(query.get('min_length', 2))
                results.append(result)
        return results
```

### Variation 2: Finding Periods with Different Operations
**Problem**: Handle different types of operations (period, analyze, find) on period detection.

**Link**: [CSES Problem Set - Finding Periods Different Operations](https://cses.fi/problemset/task/finding_periods_operations)

```python
class FindingPeriodsDifferentOps:
    def __init__(self, s):
        self.s = list(s)
        self.n = len(self.s)
        self.failure_function = self._build_failure_function()
        self.periods = self._calculate_periods()
    
    def _build_failure_function(self):
        """Build failure function using KMP algorithm"""
        failure = [0] * self.n
        
        for i in range(1, self.n):
            j = failure[i - 1]
            while j > 0 and self.s[i] != self.s[j]:
                j = failure[j - 1]
            if self.s[i] == self.s[j]:
                j += 1
            failure[i] = j
        
        return failure
    
    def _calculate_periods(self):
        """Calculate periods for all prefixes"""
        periods = []
        
        for i in range(self.n):
            prefix_length = i + 1
            failure_value = self.failure_function[i]
            
            if failure_value > 0 and prefix_length % (prefix_length - failure_value) == 0:
                period = prefix_length - failure_value
            else:
                period = prefix_length
            
            periods.append(period)
        
        return periods
    
    def get_period(self, prefix_length):
        """Get period of prefix of given length"""
        if prefix_length < 1 or prefix_length > self.n:
            return -1
        
        return self.periods[prefix_length - 1]
    
    def get_all_periods(self):
        """Get periods for all prefixes"""
        return self.periods.copy()
    
    def find_periodic_substrings(self, min_length=2):
        """Find all periodic substrings of given minimum length"""
        periodic_substrings = []
        
        for length in range(min_length, self.n + 1):
            for start in range(self.n - length + 1):
                substring = ''.join(self.s[start:start + length])
                period = self._get_substring_period(substring)
                
                if period < length:
                    periodic_substrings.append({
                        'substring': substring,
                        'start': start,
                        'length': length,
                        'period': period
                    })
        
        return periodic_substrings
    
    def _get_substring_period(self, substring):
        """Get period of a substring"""
        n = len(substring)
        failure = [0] * n
        
        for i in range(1, n):
            j = failure[i - 1]
            while j > 0 and substring[i] != substring[j]:
                j = failure[j - 1]
            if substring[i] == substring[j]:
                j += 1
            failure[i] = j
        
        if failure[n - 1] > 0 and n % (n - failure[n - 1]) == 0:
            return n - failure[n - 1]
        else:
            return n
    
    def analyze_period_distribution(self):
        """Analyze distribution of periods by prefix length"""
        distribution = {}
        
        for i in range(self.n):
            prefix_length = i + 1
            period = self.periods[i]
            
            if period not in distribution:
                distribution[period] = {
                    'count': 0,
                    'prefix_lengths': [],
                    'ratio': 0
                }
            
            distribution[period]['count'] += 1
            distribution[period]['prefix_lengths'].append(prefix_length)
            distribution[period]['ratio'] = period / prefix_length
        
        return distribution
    
    def find_longest_periodic_prefix(self):
        """Find longest prefix that is periodic"""
        longest_periodic = None
        
        for i in range(self.n):
            prefix_length = i + 1
            period = self.periods[i]
            
            if period < prefix_length:
                if longest_periodic is None or prefix_length > longest_periodic['length']:
                    longest_periodic = {
                        'prefix': ''.join(self.s[:prefix_length]),
                        'length': prefix_length,
                        'period': period
                    }
        
        return longest_periodic
    
    def find_shortest_periodic_prefix(self):
        """Find shortest prefix that is periodic"""
        shortest_periodic = None
        
        for i in range(self.n):
            prefix_length = i + 1
            period = self.periods[i]
            
            if period < prefix_length:
                if shortest_periodic is None or prefix_length < shortest_periodic['length']:
                    shortest_periodic = {
                        'prefix': ''.join(self.s[:prefix_length]),
                        'length': prefix_length,
                        'period': period
                    }
        
        return shortest_periodic
    
    def get_period_statistics(self):
        """Get comprehensive statistics about periods"""
        distribution = self.analyze_period_distribution()
        
        total_prefixes = self.n
        periodic_prefixes = sum(1 for period in self.periods if period < self.n)
        
        return {
            'total_prefixes': total_prefixes,
            'periodic_prefixes': periodic_prefixes,
            'periodic_ratio': periodic_prefixes / total_prefixes if total_prefixes > 0 else 0,
            'distribution': distribution,
            'longest_periodic': self.find_longest_periodic_prefix(),
            'shortest_periodic': self.find_shortest_periodic_prefix(),
            'average_period': sum(self.periods) / len(self.periods) if self.periods else 0
        }
    
    def get_all_queries(self, queries):
        """Get results for multiple queries"""
        results = []
        for query in queries:
            if query['type'] == 'period':
                result = self.get_period(query['prefix_length'])
                results.append(result)
            elif query['type'] == 'all_periods':
                result = self.get_all_periods()
                results.append(result)
            elif query['type'] == 'periodic_substrings':
                result = self.find_periodic_substrings(query.get('min_length', 2))
                results.append(result)
            elif query['type'] == 'analyze':
                result = self.analyze_period_distribution()
                results.append(result)
            elif query['type'] == 'longest_periodic':
                result = self.find_longest_periodic_prefix()
                results.append(result)
            elif query['type'] == 'shortest_periodic':
                result = self.find_shortest_periodic_prefix()
                results.append(result)
            elif query['type'] == 'statistics':
                result = self.get_period_statistics()
                results.append(result)
        return results
```

### Variation 3: Finding Periods with Constraints
**Problem**: Handle period queries with additional constraints (e.g., minimum period, maximum period, frequency).

**Link**: [CSES Problem Set - Finding Periods with Constraints](https://cses.fi/problemset/task/finding_periods_constraints)

```python
class FindingPeriodsWithConstraints:
    def __init__(self, s, min_period, max_period, min_frequency):
        self.s = list(s)
        self.n = len(self.s)
        self.min_period = min_period
        self.max_period = max_period
        self.min_frequency = min_frequency
        self.failure_function = self._build_failure_function()
        self.periods = self._calculate_periods()
    
    def _build_failure_function(self):
        """Build failure function using KMP algorithm"""
        failure = [0] * self.n
        
        for i in range(1, self.n):
            j = failure[i - 1]
            while j > 0 and self.s[i] != self.s[j]:
                j = failure[j - 1]
            if self.s[i] == self.s[j]:
                j += 1
            failure[i] = j
        
        return failure
    
    def _calculate_periods(self):
        """Calculate periods for all prefixes"""
        periods = []
        
        for i in range(self.n):
            prefix_length = i + 1
            failure_value = self.failure_function[i]
            
            if failure_value > 0 and prefix_length % (prefix_length - failure_value) == 0:
                period = prefix_length - failure_value
            else:
                period = prefix_length
            
            periods.append(period)
        
        return periods
    
    def constrained_period_query(self, prefix_length):
        """Query period with constraints"""
        if prefix_length < 1 or prefix_length > self.n:
            return None
        
        period = self.periods[prefix_length - 1]
        
        # Check period constraints
        if period < self.min_period or period > self.max_period:
            return None
        
        # Check frequency constraint (how many times the period repeats)
        if period < prefix_length:
            frequency = prefix_length // period
            if frequency < self.min_frequency:
                return None
        
        return period
    
    def find_valid_periods(self):
        """Find all valid periods that satisfy constraints"""
        valid_periods = []
        
        for i in range(self.n):
            prefix_length = i + 1
            period = self.periods[i]
            
            # Check period constraints
            if period < self.min_period or period > self.max_period:
                continue
            
            # Check frequency constraint
            if period < prefix_length:
                frequency = prefix_length // period
                if frequency < self.min_frequency:
                    continue
            
            valid_periods.append({
                'prefix': ''.join(self.s[:prefix_length]),
                'prefix_length': prefix_length,
                'period': period,
                'frequency': prefix_length // period if period < prefix_length else 1
            })
        
        return valid_periods
    
    def get_longest_valid_period(self):
        """Get longest valid period that satisfies constraints"""
        valid_periods = self.find_valid_periods()
        
        if not valid_periods:
            return None
        
        longest = max(valid_periods, key=lambda x: x['prefix_length'])
        return longest
    
    def get_shortest_valid_period(self):
        """Get shortest valid period that satisfies constraints"""
        valid_periods = self.find_valid_periods()
        
        if not valid_periods:
            return None
        
        shortest = min(valid_periods, key=lambda x: x['prefix_length'])
        return shortest
    
    def get_highest_frequency_period(self):
        """Get period with highest frequency that satisfies constraints"""
        valid_periods = self.find_valid_periods()
        
        if not valid_periods:
            return None
        
        highest_frequency = max(valid_periods, key=lambda x: x['frequency'])
        return highest_frequency
    
    def get_lowest_frequency_period(self):
        """Get period with lowest frequency that satisfies constraints"""
        valid_periods = self.find_valid_periods()
        
        if not valid_periods:
            return None
        
        lowest_frequency = min(valid_periods, key=lambda x: x['frequency'])
        return lowest_frequency
    
    def count_valid_periods(self):
        """Count number of valid periods"""
        return len(self.find_valid_periods())
    
    def get_constraint_statistics(self):
        """Get statistics about valid periods"""
        valid_periods = self.find_valid_periods()
        
        if not valid_periods:
            return {
                'count': 0,
                'min_period': 0,
                'max_period': 0,
                'avg_period': 0,
                'min_frequency': 0,
                'max_frequency': 0,
                'avg_frequency': 0
            }
        
        periods = [p['period'] for p in valid_periods]
        frequencies = [p['frequency'] for p in valid_periods]
        
        return {
            'count': len(valid_periods),
            'min_period': min(periods),
            'max_period': max(periods),
            'avg_period': sum(periods) / len(periods),
            'min_frequency': min(frequencies),
            'max_frequency': max(frequencies),
            'avg_frequency': sum(frequencies) / len(frequencies)
        }

# Example usage
s = "abacaba"
min_period = 2
max_period = 4
min_frequency = 2

fp = FindingPeriodsWithConstraints(s, min_period, max_period, min_frequency)
result = fp.constrained_period_query(7)
print(f"Constrained period query result: {result}")

valid_periods = fp.find_valid_periods()
print(f"Valid periods: {valid_periods}")

longest = fp.get_longest_valid_period()
print(f"Longest valid period: {longest}")
```

### Related Problems

#### **CSES Problems**
- [Finding Periods](https://cses.fi/problemset/task/1733) - Basic finding periods problem
- [Finding Borders](https://cses.fi/problemset/task/1732) - Find borders of string
- [Pattern Positions](https://cses.fi/problemset/task/1753) - Find pattern positions

#### **LeetCode Problems**
- [Repeated String Match](https://leetcode.com/problems/repeated-string-match/) - String matching with repetition
- [Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) - Find longest common prefix
- [Wildcard Matching](https://leetcode.com/problems/wildcard-matching/) - Pattern matching with wildcards

#### **Problem Categories**
- **KMP Algorithm**: String matching, period detection, failure function
- **Pattern Matching**: KMP, Z-algorithm, string matching algorithms
- **String Processing**: Borders, periods, palindromes, string transformations
- **Advanced String Algorithms**: Suffix arrays, suffix trees, string automata
