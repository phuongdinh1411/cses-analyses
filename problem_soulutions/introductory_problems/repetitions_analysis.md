# CSES Repetitions - Problem Analysis

## Problem Statement
You are given a DNA sequence consisting of characters A, C, G, and T.

Your task is to find the longest repetition in the sequence. This is a maximum-length substring containing only one type of character.

### Input
The only input line contains a string of n characters.

### Output
Print one integer: the length of the longest repetition.

### Constraints
- 1 ≤ n ≤ 10^6

### Example
```
Input:
ATTCGGGA

Output:
3
```

## Solution Progression

### Approach 1: Brute Force - O(n³)
**Description**: Try all possible substrings and check if they contain only one character.

```python
def repetitions_brute_force(sequence):
    n = len(sequence)
    max_length = 0
    
    for start in range(n):
        for end in range(start, n):
            # Check if substring contains only one character
            substring = sequence[start:end + 1]
            if len(set(substring)) == 1:
                max_length = max(max_length, len(substring))
    
    return max_length
```

**Why this is inefficient**: We're checking all possible substrings and for each one, we're checking if all characters are the same. This leads to O(n³) complexity.

### Improvement 1: Sliding Window - O(n²)
**Description**: Use sliding window to find consecutive same characters.

```python
def repetitions_sliding_window(sequence):
    n = len(sequence)
    max_length = 0
    
    for start in range(n):
        current_char = sequence[start]
        current_length = 0
        
        for end in range(start, n):
            if sequence[end] == current_char:
                current_length += 1
            else:
                break
        
        max_length = max(max_length, current_length)
    
    return max_length
```

**Why this improvement works**: Instead of checking each substring separately, we use a sliding window approach. For each starting position, we expand the window until we encounter a different character.

### Improvement 2: Single Pass - O(n)
**Description**: Scan the sequence once and count consecutive same characters.

```python
def repetitions_single_pass(sequence):
    n = len(sequence)
    if n == 0:
        return 0
    
    max_length = 1
    current_length = 1
    
    for i in range(1, n):
        if sequence[i] == sequence[i - 1]:
            current_length += 1
        else:
            max_length = max(max_length, current_length)
            current_length = 1
    
    # Don't forget the last group
    max_length = max(max_length, current_length)
    
    return max_length
```

**Why this improvement works**: We scan the sequence once and keep track of the current length of consecutive same characters. When we encounter a different character, we update the maximum length and reset the current length.

### Alternative: Using Groupby - O(n)
**Description**: Use itertools.groupby to group consecutive same characters.

```python
from itertools import groupby

def repetitions_groupby(sequence):
    max_length = 0
    
    for char, group in groupby(sequence):
        max_length = max(max_length, len(list(group)))
    
    return max_length
```

**Why this works**: The groupby function groups consecutive same elements together, making it easy to find the longest group.

## Final Optimal Solution

```python
sequence = input().strip()

if not sequence:
    print(0)
else:
    max_length = 1
    current_length = 1
    
    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i - 1]:
            current_length += 1
        else:
            max_length = max(max_length, current_length)
            current_length = 1
    
    # Don't forget the last group
    max_length = max(max_length, current_length)
    
    print(max_length)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n³) | O(n) | Check all substrings |
| Sliding Window | O(n²) | O(1) | Expand window until different character |
| Single Pass | O(n) | O(1) | Count consecutive same characters |
| Groupby | O(n) | O(1) | Use itertools.groupby |

## Key Insights for Other Problems

### 1. **Single Pass Scanning**
**Principle**: Scan the sequence once and maintain state to solve the problem efficiently.
**Applicable to**:
- String processing
- Array processing
- Pattern recognition
- Counting problems

**Example Problems**:
- Longest consecutive sequence
- Pattern matching
- String compression
- Counting problems

### 2. **Sliding Window Technique**
**Principle**: Use two pointers to maintain a window that satisfies certain conditions.
**Applicable to**:
- Substring problems
- Array problems
- Range-based problems
- Optimization problems

**Example Problems**:
- Longest substring without repeating characters
- Minimum window substring
- Subarray problems
- Range queries

### 3. **Grouping Consecutive Elements**
**Principle**: Group consecutive same elements to simplify processing.
**Applicable to**:
- String compression
- Pattern recognition
- Data compression
- String processing

**Example Problems**:
- String compression
- Run-length encoding
- Pattern matching
- String analysis

### 4. **State Maintenance**
**Principle**: Maintain state during scanning to track important information.
**Applicable to**:
- Dynamic programming
- State machines
- Pattern recognition
- Optimization problems

**Example Problems**:
- State machine problems
- Dynamic programming
- Pattern recognition
- Optimization problems

## Notable Techniques

### 1. **Single Pass Pattern**
```python
# Scan once and maintain state
current_length = 1
max_length = 1
for i in range(1, n):
    if condition:
        current_length += 1
    else:
        max_length = max(max_length, current_length)
        current_length = 1
max_length = max(max_length, current_length)
```

### 2. **Sliding Window Pattern**
```python
# Expand window until condition is violated
for start in range(n):
    current_length = 0
    for end in range(start, n):
        if condition:
            current_length += 1
        else:
            break
    max_length = max(max_length, current_length)
```

### 3. **Groupby Pattern**
```python
# Group consecutive same elements
from itertools import groupby
for char, group in groupby(sequence):
    length = len(list(group))
    # Process group
```

## Edge Cases to Remember

1. **Empty string**: Return 0
2. **Single character**: Return 1
3. **All same characters**: Return length of string
4. **No repetitions**: Return 1 (each character is a repetition of length 1)
5. **Large strings**: Handle efficiently with single pass

## Problem-Solving Framework

1. **Identify pattern nature**: This is about finding consecutive same elements
2. **Consider single pass**: Scan once and maintain state
3. **Handle edge cases**: Empty string, single character, etc.
4. **Optimize the approach**: Use single pass for efficiency
5. **Verify correctness**: Test with examples

---

*This analysis shows how to efficiently find the longest repetition using single pass scanning.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Find All Repetitions**
**Problem**: Find all repetitions and their positions in the sequence.
```python
def find_all_repetitions(sequence):
    n = len(sequence)
    repetitions = []
    
    i = 0
    while i < n:
        char = sequence[i]
        start = i
        count = 0
        
        while i < n and sequence[i] == char:
            count += 1
            i += 1
        
        if count > 1:
            repetitions.append((char, start, count))
    
    return repetitions
```

#### **Variation 2: Minimum Repetition Length**
**Problem**: Find the minimum length of any repetition (instead of maximum).
```python
def min_repetition_length(sequence):
    n = len(sequence)
    if n == 0:
        return 0
    
    min_length = float('inf')
    current_length = 1
    
    for i in range(1, n):
        if sequence[i] == sequence[i - 1]:
            current_length += 1
        else:
            if current_length > 1:
                min_length = min(min_length, current_length)
            current_length = 1
    
    if current_length > 1:
        min_length = min(min_length, current_length)
    
    return min_length if min_length != float('inf') else 0
```

#### **Variation 3: Repetitions with Different Characters**
**Problem**: Find longest substring with at most k different characters.
```python
def longest_substring_k_chars(sequence, k):
    n = len(sequence)
    char_count = {}
    max_length = 0
    left = 0
    
    for right in range(n):
        char = sequence[right]
        char_count[char] = char_count.get(char, 0) + 1
        
        while len(char_count) > k:
            char_count[sequence[left]] -= 1
            if char_count[sequence[left]] == 0:
                del char_count[sequence[left]]
            left += 1
        
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

#### **Variation 4: Repetitions with Gaps**
**Problem**: Find longest repetition allowing at most g gaps (different characters).
```python
def repetitions_with_gaps(sequence, g):
    n = len(sequence)
    max_length = 0
    
    for char in set(sequence):
        gaps = 0
        current_length = 0
        max_current = 0
        
        for i in range(n):
            if sequence[i] == char:
                current_length += 1
            else:
                gaps += 1
                if gaps > g:
                    # Remove characters until we have <= g gaps
                    while gaps > g and current_length > 0:
                        if sequence[i - current_length] != char:
                            gaps -= 1
                        current_length -= 1
                    gaps = min(gaps, g)
            
            max_current = max(max_current, current_length)
        
        max_length = max(max_length, max_current)
    
    return max_length
```

#### **Variation 5: Weighted Repetitions**
**Problem**: Each character has a weight. Find repetition with maximum total weight.
```python
def weighted_repetitions(sequence, weights):
    n = len(sequence)
    max_weight = 0
    current_weight = 0
    current_char = None
    
    for i in range(n):
        char = sequence[i]
        weight = weights.get(char, 1)
        
        if char == current_char:
            current_weight += weight
        else:
            max_weight = max(max_weight, current_weight)
            current_weight = weight
            current_char = char
    
    max_weight = max(max_weight, current_weight)
    return max_weight
```

### 🔗 **Related Problems & Concepts**

#### **1. String Processing Problems**
- **Longest Common Substring**: Find longest common substring between strings
- **Palindrome Detection**: Check if string is palindrome
- **Anagram Detection**: Check if strings are anagrams
- **String Compression**: Compress repeated characters

#### **2. Sliding Window Problems**
- **Longest Substring Without Repeating**: Find substring with unique characters
- **Minimum Window Substring**: Find smallest substring containing all characters
- **Substring with Concatenation**: Find substring containing all words
- **Longest Substring with At Most K**: Find substring with at most k distinct characters

#### **3. Pattern Recognition Problems**
- **Regular Expression Matching**: Match patterns in strings
- **String Matching**: Find pattern occurrences in text
- **Sequence Alignment**: Align sequences optimally
- **Motif Finding**: Find common patterns in sequences

#### **4. Bioinformatics Problems**
- **DNA Sequence Analysis**: Analyze genetic sequences
- **Protein Sequence Matching**: Match protein sequences
- **Genome Assembly**: Assemble genome fragments
- **Sequence Motif Discovery**: Find regulatory motifs

#### **5. Data Compression Problems**
- **Run-Length Encoding**: Compress repeated characters
- **Huffman Coding**: Optimal prefix coding
- **LZ77/LZ78**: Dictionary-based compression
- **Burrows-Wheeler Transform**: String transformation

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    sequence = input().strip()
    
    max_length = 1
    current_length = 1
    
    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i - 1]:
            current_length += 1
        else:
            max_length = max(max_length, current_length)
            current_length = 1
    
    max_length = max(max_length, current_length)
    print(max_length)
```

#### **2. Range Queries**
```python
# Precompute repetition lengths for all positions
def precompute_repetitions(sequence):
    n = len(sequence)
    repetition_lengths = [1] * n
    
    for i in range(1, n):
        if sequence[i] == sequence[i - 1]:
            repetition_lengths[i] = repetition_lengths[i - 1] + 1
    
    return repetition_lengths

# Answer queries about repetition lengths
def repetition_query(repetition_lengths, l, r):
    return max(repetition_lengths[l:r + 1])
```

#### **3. Interactive Problems**
```python
# Interactive sequence analysis
def interactive_repetitions():
    sequence = input("Enter DNA sequence: ")
    print(f"Sequence length: {len(sequence)}")
    
    while True:
        query = input("Enter query (max/min/all/quit): ")
        if query.lower() == 'quit':
            break
        elif query.lower() == 'max':
            result = repetitions_single_pass(sequence)
            print(f"Maximum repetition length: {result}")
        elif query.lower() == 'min':
            result = min_repetition_length(sequence)
            print(f"Minimum repetition length: {result}")
        elif query.lower() == 'all':
            result = find_all_repetitions(sequence)
            print(f"All repetitions: {result}")
```

### 🧮 **Mathematical Extensions**

#### **1. Combinatorics**
- **Counting Repetitions**: Count number of repetitions of each length
- **Probability of Repetitions**: Calculate probability of repetitions in random sequences
- **Expected Length**: Find expected length of longest repetition
- **Variance Analysis**: Analyze distribution of repetition lengths

#### **2. Information Theory**
- **Entropy**: Calculate information content of sequences
- **Compression Ratio**: Measure how well sequences can be compressed
- **Redundancy**: Measure repetitive patterns in sequences
- **Complexity**: Analyze sequence complexity

#### **3. Statistical Analysis**
- **Frequency Analysis**: Analyze character frequencies
- **Correlation**: Find correlations between different positions
- **Markov Chains**: Model sequence as Markov process
- **Random Walks**: Analyze sequence as random walk

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **String Algorithms**: KMP, Boyer-Moore, suffix arrays
- **Compression Algorithms**: Run-length encoding, Huffman coding
- **Pattern Matching**: Regular expressions, finite automata
- **Sequence Analysis**: Dynamic programming for sequences

#### **2. Mathematical Concepts**
- **Combinatorics**: Counting and probability
- **Information Theory**: Entropy and compression
- **Statistics**: Frequency analysis and correlation
- **Probability**: Random processes and Markov chains

#### **3. Programming Concepts**
- **String Manipulation**: Efficient string operations
- **Sliding Window**: Two-pointer technique
- **Dynamic Programming**: Optimal substructure
- **Data Structures**: Efficient storage and retrieval

---

*This analysis demonstrates efficient string processing techniques and shows various extensions for pattern recognition problems.* 