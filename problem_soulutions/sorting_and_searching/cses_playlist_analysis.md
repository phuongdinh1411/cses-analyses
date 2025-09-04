---
layout: simple
title: "Playlist - Longest Unique Song Sequence"
permalink: /problem_soulutions/sorting_and_searching/cses_playlist_analysis
---

# Playlist - Longest Unique Song Sequence

## 📋 Problem Description

You are given a playlist of a radio station. What is the longest sequence of consecutive songs where each song is unique?

This is a sliding window problem that requires finding the longest contiguous subarray with all unique elements. The solution involves using the two pointers technique with a frequency map to track unique elements.

**Input**: 
- First line: n (number of songs)
- Second line: n integers k₁, k₂, ..., kₙ (song IDs)

**Output**: 
- Length of the longest sequence of unique songs

**Constraints**:
- 1 ≤ n ≤ 2⋅10⁵
- 1 ≤ kᵢ ≤ 10⁹

**Example**:
```
Input:
8
1 2 1 3 2 7 4 2

Output:
5

Explanation**: 
- Song sequence: [1, 2, 1, 3, 2, 7, 4, 2]
- Longest unique sequence: [1, 3, 2, 7, 4] (positions 3-7)
- Length: 5 songs
- Cannot extend further as song 2 appears again at position 8
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find longest consecutive subarray with unique elements
- Each song ID must appear only once in the sequence
- Need to handle duplicates efficiently
- This is a sliding window problem

**Key Observations:**
- Can use two pointers technique
- Track last occurrence of each song
- Expand window until duplicate found
- Shrink window from left when duplicate encountered

### Step 2: Sliding Window Approach
**Idea**: Use two pointers to maintain a window of unique songs.

```python
def playlist_sliding_window(songs):
    n = len(songs)
    last_seen = {}  # song_id -> last_position
    max_length = 0
    start = 0
    
    for end in range(n):
        # If we've seen this song before, update start
        if songs[end] in last_seen:
            start = max(start, last_seen[songs[end]] + 1)
        
        # Update last seen position
        last_seen[songs[end]] = end
        
        # Update max length
        max_length = max(max_length, end - start + 1)
    
    return max_length
```

**Why this works:**
- Two pointers maintain window of unique songs
- Track last occurrence of each song
- Expand window until duplicate found
- Shrink window from left when needed

### Step 3: Optimized Solution
**Idea**: Optimize the implementation with better variable names and logic.

```python
def playlist_optimized(songs):
    n = len(songs)
    song_positions = {}  # song_id -> last_position
    longest_sequence = 0
    window_start = 0
    
    for window_end in range(n):
        current_song = songs[window_end]
        
        # If song already in window, move start pointer
        if current_song in song_positions:
            window_start = max(window_start, song_positions[current_song] + 1)
        
        # Update song position
        song_positions[current_song] = window_end
        
        # Update longest sequence
        current_length = window_end - window_start + 1
        longest_sequence = max(longest_sequence, current_length)
    
    return longest_sequence
```

**Why this is better:**
- Clearer variable names
- More readable logic
- Same optimal time complexity

### Step 3: Optimization/Alternative
**Alternative approaches:**
- **Brute Force**: Check all possible subarrays O(n²)
- **Sliding Window**: Two pointers with frequency map O(n)
- **Hash Map**: Track last occurrence of each element

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_playlist():
    n = int(input())
    songs = list(map(int, input().split()))
    
    # Sliding window approach
    song_positions = {}
    longest_sequence = 0
    window_start = 0
    
    for window_end in range(n):
        current_song = songs[window_end]
        
        # If song already in window, move start pointer
        if current_song in song_positions:
            window_start = max(window_start, song_positions[current_song] + 1)
        
        # Update song position
        song_positions[current_song] = window_end
        
        # Update longest sequence
        current_length = window_end - window_start + 1
        longest_sequence = max(longest_sequence, current_length)
    
    print(longest_sequence)

# Main execution
if __name__ == "__main__":
    solve_playlist()
```

**Why this works:**
- Optimal sliding window approach
- Handles all edge cases
- Efficient implementation

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        ([1, 2, 1, 3, 2, 7, 4, 2], 5),
        ([1, 2, 3, 4, 5], 5),
        ([1, 1, 1, 1], 1),
        ([1, 2, 1, 2, 1, 2], 2),
        ([1], 1),
    ]
    
    for songs, expected in test_cases:
        result = solve_test(songs)
        print(f"Songs: {songs}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(songs):
    n = len(songs)
    song_positions = {}
    longest_sequence = 0
    window_start = 0
    
    for window_end in range(n):
        current_song = songs[window_end]
        
        if current_song in song_positions:
            window_start = max(window_start, song_positions[current_song] + 1)
        
        song_positions[current_song] = window_end
        
        current_length = window_end - window_start + 1
        longest_sequence = max(longest_sequence, current_length)
    
    return longest_sequence

test_solution()
```

### Step 5: Testing Our Solution
**Test cases to verify correctness:**
- **Test 1**: Basic unique sequence (should return correct length)
- **Test 2**: All unique songs (should return n)
- **Test 3**: All same songs (should return 1)
- **Test 4**: Complex pattern (should return optimal length)

## 🔧 Implementation Details

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(1) | Check all possible subarrays |
| Sliding Window | O(n) | O(n) | Two pointers with frequency map |
| Hash Map | O(n) | O(n) | Track last occurrence positions |

### Time Complexity
- **Time**: O(n) - single pass through array
- **Space**: O(n) - hash map storage

### Why This Solution Works
- **Sliding Window**: Maintains window of unique elements
- **Hash Map**: Tracks last occurrence efficiently
- **Two Pointers**: Efficiently expands and contracts window

## 🎯 Key Insights

### 1. **Sliding Window Technique**
- Use two pointers to maintain window
- Expand window until constraint violated
- Contract window from left when needed
- Track maximum valid window size

### 2. **Hash Map for Tracking**
- Store last occurrence of each element
- O(1) lookup and update time
- Enables efficient window adjustment
- Handles duplicates correctly

### 3. **Window Management**
- Start pointer moves when duplicate found
- End pointer always moves forward
- Window always contains unique elements
- Track maximum window size

## 🎯 Problem Variations

### Variation 1: Longest Substring with At Most K Distinct Characters
**Problem**: Find longest substring with at most k distinct characters.

```python
def longest_substring_k_distinct(s, k):
    n = len(s)
    char_count = {}
    longest_substring = 0
    window_start = 0
    
    for window_end in range(n):
        current_char = s[window_end]
        char_count[current_char] = char_count.get(current_char, 0) + 1
        
        # Shrink window if too many distinct characters
        while len(char_count) > k:
            start_char = s[window_start]
            char_count[start_char] -= 1
            if char_count[start_char] == 0:
                del char_count[start_char]
            window_start += 1
        
        longest_substring = max(longest_substring, window_end - window_start + 1)
    
    return longest_substring
```

### Variation 2: Longest Subarray with Sum At Most K
**Problem**: Find longest subarray with sum at most k.

```python
def longest_subarray_sum_at_most_k(arr, k):
    n = len(arr)
    current_sum = 0
    longest_subarray = 0
    window_start = 0
    
    for window_end in range(n):
        current_sum += arr[window_end]
        
        # Shrink window if sum exceeds k
        while current_sum > k:
            current_sum -= arr[window_start]
            window_start += 1
        
        longest_subarray = max(longest_subarray, window_end - window_start + 1)
    
    return longest_subarray
```

### Variation 3: Longest Subarray with Exactly K Distinct Elements
**Problem**: Find longest subarray with exactly k distinct elements.

```python
def longest_subarray_exactly_k_distinct(arr, k):
    n = len(arr)
    element_count = {}
    longest_subarray = 0
    window_start = 0
    
    for window_end in range(n):
        current_element = arr[window_end]
        element_count[current_element] = element_count.get(current_element, 0) + 1
        
        # Shrink window if too many distinct elements
        while len(element_count) > k:
            start_element = arr[window_start]
            element_count[start_element] -= 1
            if element_count[start_element] == 0:
                del element_count[start_element]
            window_start += 1
        
        # Check if we have exactly k distinct elements
        if len(element_count) == k:
            longest_subarray = max(longest_subarray, window_end - window_start + 1)
    
    return longest_subarray
```

### Variation 4: Longest Subarray with Balanced Parentheses
**Problem**: Find longest subarray with balanced parentheses.

```python
def longest_balanced_parentheses(s):
    n = len(s)
    stack = [-1]  # Initialize with -1 to handle edge case
    max_length = 0
    
    for i in range(n):
        if s[i] == '(':
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                max_length = max(max_length, i - stack[-1])
    
    return max_length
```

### Variation 5: Longest Subarray with Target Sum
**Problem**: Find longest subarray with sum equal to target.

```python
def longest_subarray_with_target_sum(arr, target):
    n = len(arr)
    prefix_sum = {0: -1}  # sum -> first occurrence
    current_sum = 0
    max_length = 0
    
    for i in range(n):
        current_sum += arr[i]
        
        # Check if we've seen current_sum - target before
        if current_sum - target in prefix_sum:
            max_length = max(max_length, i - prefix_sum[current_sum - target])
        
        # Only update if this is the first occurrence
        if current_sum not in prefix_sum:
            prefix_sum[current_sum] = i
    
    return max_length
```

## 🎯 Key Insights

### Important Concepts and Patterns
- **Sliding Window**: Two pointers technique for contiguous subarrays
- **Hash Map**: Track frequency or last occurrence of elements
- **Unique Elements**: Maintain window with all unique elements
- **Two Pointers**: Efficient technique for subarray problems

## 🚀 Problem Variations

### Extended Problems with Detailed Code Examples

#### **1. Playlist with K Duplicates Allowed**
```python
def playlist_k_duplicates(songs, k):
    # Handle playlist where each song can appear at most k times
    
    song_count = {}
    longest_sequence = 0
    window_start = 0
    
    for window_end in range(len(songs)):
        current_song = songs[window_end]
        
        # Add current song to window
        song_count[current_song] = song_count.get(current_song, 0) + 1
        
        # Shrink window if any song appears more than k times
        while song_count[current_song] > k:
            song_count[songs[window_start]] -= 1
            if song_count[songs[window_start]] == 0:
                del song_count[songs[window_start]]
            window_start += 1
        
        # Update longest sequence
        current_length = window_end - window_start + 1
        longest_sequence = max(longest_sequence, current_length)
    
    return longest_sequence
```

#### **2. Playlist with Weighted Songs**
```python
def playlist_weighted(songs, weights):
    # Handle playlist with weighted songs
    
    song_positions = {}
    longest_sequence = 0
    window_start = 0
    current_weight = 0
    
    for window_end in range(len(songs)):
        current_song = songs[window_end]
        
        # If song already in window, move start pointer
        if current_song in song_positions:
            # Remove weight of songs before the duplicate
            for i in range(window_start, song_positions[current_song] + 1):
                current_weight -= weights[i]
            window_start = song_positions[current_song] + 1
        
        # Add current song weight
        current_weight += weights[window_end]
        song_positions[current_song] = window_end
        
        # Update longest sequence (by weight)
        longest_sequence = max(longest_sequence, current_weight)
    
    return longest_sequence
```

#### **3. Playlist with Dynamic Updates**
```python
def playlist_dynamic(operations):
    # Handle playlist with dynamic song additions/removals
    
    songs = []
    longest_sequence = 0
    
    for operation in operations:
        if operation[0] == 'add':
            # Add new song
            song = operation[1]
            songs.append(song)
            
            # Recalculate longest unique sequence
            longest_sequence = calculate_longest_unique(songs)
        
        elif operation[0] == 'remove':
            # Remove song at index
            index = operation[1]
            if 0 <= index < len(songs):
                songs.pop(index)
                longest_sequence = calculate_longest_unique(songs)
        
        elif operation[0] == 'query':
            # Return current longest sequence
            yield longest_sequence
    
    return list(playlist_dynamic(operations))

def calculate_longest_unique(songs):
    song_positions = {}
    longest_sequence = 0
    window_start = 0
    
    for window_end in range(len(songs)):
        current_song = songs[window_end]
        
        if current_song in song_positions:
            window_start = max(window_start, song_positions[current_song] + 1)
        
        song_positions[current_song] = window_end
        
        current_length = window_end - window_start + 1
        longest_sequence = max(longest_sequence, current_length)
    
    return longest_sequence
```

## 🔗 Related Problems

### Links to Similar Problems
- **Sliding Window**: Subarray problems with constraints
- **Two Pointers**: Array problems with two pointers
- **Hash Map**: Frequency counting problems
- **Unique Elements**: Problems with distinct values

## 📚 Learning Points

1. **Sliding Window**: Efficient technique for subarray problems
2. **Two Pointers**: Maintain window boundaries efficiently
3. **Hash Maps**: Track element occurrences and positions
4. **Window Management**: Expand and contract based on constraints

---

**This is a great introduction to sliding window techniques!** 🎯 