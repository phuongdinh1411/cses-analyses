---
layout: simple
title: "Playlist"
permalink: /problem_soulutions/sorting_and_searching/cses_playlist_analysis
---

# Playlist

## Problem Description

**Problem**: You are given a playlist of a radio station. What is the longest sequence of consecutive songs where each song is unique?

**Input**: 
- First line: n (number of songs)
- Second line: n integers k₁, k₂, ..., kₙ (song IDs)

**Output**: Length of the longest sequence of unique songs.

**Example**:
```
Input:
8
1 2 1 3 2 7 4 2

Output:
5

Explanation: The longest sequence of unique songs is [1, 3, 2, 7, 4] with length 5.
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

## 🔧 Implementation Details

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

## 🔗 Related Problems

- **[Longest Substring Without Repeating](/cses-analyses/problem_soulutions/sorting_and_searching/longest_substring_without_repeating_analysis)**: Similar sliding window problem
- **[Subarray Distinct Values](/cses-analyses/problem_soulutions/sorting_and_searching/subarray_distinct_values_analysis)**: Distinct value problems
- **[Sliding Window](/cses-analyses/problem_soulutions/sorting_and_searching/sliding_window_advertisement_analysis)**: Sliding window techniques

## 📚 Learning Points

1. **Sliding Window**: Efficient technique for subarray problems
2. **Two Pointers**: Maintain window boundaries efficiently
3. **Hash Maps**: Track element occurrences and positions
4. **Window Management**: Expand and contract based on constraints

---

**This is a great introduction to sliding window techniques!** 🎯 