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