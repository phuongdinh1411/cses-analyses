---
layout: simple
title: Creating Strings Analysis
permalink: /problem_soulutions/introductory_problems/creating_strings_analysis/
---

# Creating Strings Analysis

## Problem Description

Given a string, find all distinct strings that can be created by reordering its characters. Output the number of distinct strings and list them in lexicographical order.

## Key Insights

### 1. Permutation Generation
- **Distinct permutations**: Handle duplicate characters correctly
- **Lexicographical order**: Generate permutations in sorted order
- **Efficiency**: Avoid generating duplicate permutations

### 2. Mathematical Formula
- **Total permutations**: n! / (f1! × f2! × ... × fk!)
- Where n is string length and fi is frequency of character i
- **Distinct count**: Use multinomial coefficient

### 3. Implementation Strategy
- Use next_permutation for lexicographical generation
- Handle duplicates by sorting first
- Count distinct permutations efficiently

## Solution Approach

### Method 1: Using next_permutation
```cpp
vector<string> createStrings(string s) {
    vector<string> result;
    
    // Sort string to get lexicographically smallest permutation
    sort(s.begin(), s.end());
    
    // Generate all permutations
    do {
        result.push_back(s);
    } while (next_permutation(s.begin(), s.end()));
    
    return result;
}

int countDistinctStrings(string s) {
    // Count character frequencies
    vector<int> freq(26, 0);
    for (char c : s) {
        freq[c - 'a']++;
    }
    
    // Calculate multinomial coefficient
    int n = s.length();
    long long result = 1;
    
    // Calculate n!
    for (int i = 2; i <= n; i++) {
        result *= i;
    }
    
    // Divide by factorial of each frequency
    for (int f : freq) {
        if (f > 1) {
            for (int i = 2; i <= f; i++) {
                result /= i;
            }
        }
    }
    
    return result;
}
```

### Method 2: Recursive Generation
```cpp
class StringCreator {
private:
    vector<string> result;
    string current;
    vector<int> freq;
    
    void generate(int pos, int n) {
        if (pos == n) {
            result.push_back(current);
            return;
        }
        
        for (int i = 0; i < 26; i++) {
            if (freq[i] > 0) {
                freq[i]--;
                current[pos] = 'a' + i;
                generate(pos + 1, n);
                freq[i]++;
            }
        }
    }
    
public:
    vector<string> createStringsRecursive(string s) {
        // Count frequencies
        freq.assign(26, 0);
        for (char c : s) {
            freq[c - 'a']++;
        }
        
        current = s;
        generate(0, s.length());
        return result;
    }
};
```

### Method 3: Iterative with Duplicate Handling
```cpp
vector<string> createStringsIterative(string s) {
    vector<string> result;
    
    // Sort to handle duplicates correctly
    sort(s.begin(), s.end());
    
    // Generate permutations and skip duplicates
    do {
        result.push_back(s);
        
        // Skip duplicate permutations
        while (next_permutation(s.begin(), s.end()) && 
               result.back() == s) {
            // Skip duplicates
        }
    } while (next_permutation(s.begin(), s.end()));
    
    return result;
}
```

## Time Complexity
- **Method 1**: O(n! × n) - generate all permutations
- **Method 2**: O(n! × n) - recursive generation
- **Method 3**: O(n! × n) - iterative with duplicate handling

## Example Walkthrough

**Input**: "aab"

**Process**:
1. Sort string: "aab"
2. Generate permutations:
   - "aab" (original)
   - "aba" (swap b with second a)
   - "baa" (swap b with first a)
3. All are distinct

**Output**: 3 distinct strings: ["aab", "aba", "baa"]

## Problem Variations

### Variation 1: K-th Permutation
**Problem**: Find k-th lexicographical permutation.

**Solution**: Use mathematical approach or binary search.

### Variation 2: Constrained Permutations
**Problem**: Some characters must maintain relative order.

**Approach**: Use topological sorting or constraint satisfaction.

### Variation 3: Weighted Permutations
**Problem**: Each permutation has a weight. Find minimum/maximum weight.

**Solution**: Use dynamic programming or greedy approach.

### Variation 4: Circular Permutations
**Problem**: Consider rotations as equivalent.

**Approach**: Use Burnside's lemma or group theory.

### Variation 5: Partial Permutations
**Problem**: Generate permutations of length k from string of length n.

**Solution**: Use combination generation with permutation.

### Variation 6: Probabilistic Permutations
**Problem**: Each character has a probability. Find expected number of distinct permutations.

**Approach**: Use probability theory and expected values.

## Advanced Optimizations

### 1. Efficient Duplicate Handling
```cpp
vector<string> createStringsEfficient(string s) {
    vector<string> result;
    
    // Sort to get lexicographically smallest
    sort(s.begin(), s.end());
    
    // Use set to automatically handle duplicates
    set<string> unique_permutations;
    
    do {
        unique_permutations.insert(s);
    } while (next_permutation(s.begin(), s.end()));
    
    // Convert set to vector
    result.assign(unique_permutations.begin(), unique_permutations.end());
    return result;
}
```

### 2. Mathematical Counting
```cpp
long long countPermutations(string s) {
    vector<int> freq(26, 0);
    for (char c : s) {
        freq[c - 'a']++;
    }
    
    int n = s.length();
    long long numerator = 1;
    long long denominator = 1;
    
    // Calculate n!
    for (int i = 2; i <= n; i++) {
        numerator *= i;
    }
    
    // Calculate product of factorials of frequencies
    for (int f : freq) {
        if (f > 1) {
            for (int i = 2; i <= f; i++) {
                denominator *= i;
            }
        }
    }
    
    return numerator / denominator;
}
```

### 3. Memory Efficient Generation
```cpp
class MemoryEfficientStringCreator {
private:
    vector<string> result;
    string s;
    
    void generatePermutations(int start) {
        if (start == s.length() - 1) {
            result.push_back(s);
            return;
        }
        
        set<char> used;
        for (int i = start; i < s.length(); i++) {
            if (used.count(s[i])) continue;
            used.insert(s[i]);
            
            swap(s[start], s[i]);
            generatePermutations(start + 1);
            swap(s[start], s[i]);
        }
    }
    
public:
    vector<string> createStrings(string input) {
        s = input;
        sort(s.begin(), s.end());
        generatePermutations(0);
        return result;
    }
};
```

### 4. Parallel Generation
```cpp
vector<string> createStringsParallel(string s) {
    // For large strings, use parallel processing
    // Divide permutation space and process in parallel
    // Merge results
    
    // Implementation for parallel processing...
    return vector<string>();
}
```

## Related Problems
- [String Reorder](../string_reorder_analysis/)
- [Palindrome Reorder](../palindrome_reorder_analysis/)
- [Permutations](../permutations_analysis/)

## Practice Problems
1. **CSES**: Creating Strings
2. **LeetCode**: Similar permutation problems
3. **AtCoder**: String manipulation problems

## Key Takeaways
1. **next_permutation** is efficient for lexicographical generation
2. **Mathematical counting** helps avoid generating all permutations
3. **Duplicate handling** is crucial for correct results
4. **Memory efficiency** is important for large strings
5. **Lexicographical order** requires initial sorting
6. **Mathematical formulas** provide exact counts
7. **Optimization techniques** depend on problem constraints
