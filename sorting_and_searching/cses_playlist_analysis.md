# CSES Playlist - Problem Analysis

## Problem Statement
You are given a playlist of a radio station since its establishment. The playlist has a total of n songs.

What is the longest sequence of consecutive songs where each song is unique?

### Input
The first input line has an integer n: the number of songs.
The second line has n integers k1,k2,…,kn: the id number of each song.

### Output
Print one integer: the length of the longest sequence of unique songs.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ ki ≤ 10^9

### Example
```
Input:
8
1 2 1 3 2 7 4 2

Output:
5
```

## Solution Progression

### Approach 1: Brute Force - O(n³)
**Description**: Try all possible subarrays and check if they contain unique elements.

```python
def playlist_brute_force(songs):
    n = len(songs)
    max_length = 0
    
    for start in range(n):
        for end in range(start, n):
            # Check if subarray from start to end has unique elements
            unique_songs = set()
            is_unique = True
            
            for i in range(start, end + 1):
                if songs[i] in unique_songs:
                    is_unique = False
                    break
                unique_songs.add(songs[i])
            
            if is_unique:
                max_length = max(max_length, end - start + 1)
    
    return max_length
```

**Why this is inefficient**: We're checking all possible subarrays and for each one, we're checking if all elements are unique. This leads to O(n³) complexity.

### Improvement 1: Sliding Window with Set - O(n²)
**Description**: Use sliding window technique with a set to track unique elements.

```python
def playlist_sliding_window(songs):
    n = len(songs)
    max_length = 0
    
    for start in range(n):
        unique_songs = set()
        current_length = 0
        
        for end in range(start, n):
            if songs[end] in unique_songs:
                break
            unique_songs.add(songs[end])
            current_length += 1
        
        max_length = max(max_length, current_length)
    
    return max_length
```

**Why this improvement works**: Instead of checking each subarray separately, we use a sliding window approach. For each starting position, we expand the window until we encounter a duplicate, then move to the next starting position.

### Improvement 2: Optimized Sliding Window - O(n)
**Description**: Use two pointers with a hash map to track the last occurrence of each song.

```python
def playlist_optimized(songs):
    n = len(songs)
    last_seen = {}  # song_id -> last_position
    max_length = 0
    start = 0
    
    for end in range(n):
        current_song = songs[end]
        
        # If we've seen this song before, update start pointer
        if current_song in last_seen:
            start = max(start, last_seen[current_song] + 1)
        
        # Update last seen position
        last_seen[current_song] = end
        
        # Update maximum length
        max_length = max(max_length, end - start + 1)
    
    return max_length
```

**Why this improvement works**: We maintain a hash map that tracks the last position where each song was seen. When we encounter a duplicate, we move the start pointer to the position after the last occurrence of the duplicate song. This ensures we always have a window of unique songs.

### Alternative: Using Two Pointers with Set - O(n)
**Description**: Use two pointers with a set to maintain the current window of unique songs.

```python
def playlist_two_pointers(songs):
    n = len(songs)
    unique_songs = set()
    max_length = 0
    start = 0
    
    for end in range(n):
        # Remove elements from start until we can add the current element
        while songs[end] in unique_songs:
            unique_songs.remove(songs[start])
            start += 1
        
        # Add current element
        unique_songs.add(songs[end])
        
        # Update maximum length
        max_length = max(max_length, end - start + 1)
    
    return max_length
```

**Why this works**: We maintain a set of unique songs in the current window. When we encounter a duplicate, we remove elements from the start of the window until we can add the current element without duplicates.

## Final Optimal Solution

```python
n = int(input())
songs = list(map(int, input().split()))

# Optimized sliding window
last_seen = {}
max_length = 0
start = 0

for end in range(n):
    current_song = songs[end]
    
    # If we've seen this song before, update start pointer
    if current_song in last_seen:
        start = max(start, last_seen[current_song] + 1)
    
    # Update last seen position
    last_seen[current_song] = end
    
    # Update maximum length
    max_length = max(max_length, end - start + 1)

print(max_length)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n³) | O(n) | Check all subarrays |
| Sliding Window | O(n²) | O(n) | Expand window until duplicate |
| Optimized | O(n) | O(n) | Track last occurrence of each element |
| Two Pointers | O(n) | O(n) | Maintain set of unique elements |

## Key Insights for Other Problems

### 1. **Sliding Window Technique**
**Principle**: Use two pointers to maintain a window that satisfies certain conditions.
**Applicable to**:
- Subarray problems
- String problems
- Range-based problems
- Optimization problems

**Example Problems**:
- Longest substring without repeating characters
- Minimum window substring
- Subarray with given sum
- Longest subarray with k distinct elements

### 2. **Hash Map for Tracking**
**Principle**: Use hash maps to track the last occurrence or frequency of elements.
**Applicable to**:
- Duplicate detection
- Frequency counting
- Position tracking
- Caching results

**Example Problems**:
- Two sum
- Longest substring without repeating characters
- Subarray sum equals k
- Frequency counting

### 3. **Two Pointers Technique**
**Principle**: Use two pointers to efficiently process arrays or strings.
**Applicable to**:
- Subarray problems
- String manipulation
- Range queries
- Optimization problems

**Example Problems**:
- Container with most water
- Two sum in sorted array
- Remove duplicates
- Merge sorted arrays

### 4. **Unique Element Tracking**
**Principle**: Track unique elements in a window or range efficiently.
**Applicable to**:
- Duplicate detection
- Unique element counting
- Subarray problems
- String problems

**Example Problems**:
- Longest substring without repeating characters
- Count distinct elements in subarray
- Remove duplicates
- Unique element problems

## Notable Techniques

### 1. **Sliding Window Pattern**
```python
# Common sliding window pattern
start = 0
for end in range(n):
    # Add element to window
    window.add(arr[end])
    
    # Shrink window if needed
    while condition_not_met(window):
        window.remove(arr[start])
        start += 1
    
    # Update answer
    answer = max(answer, end - start + 1)
```

### 2. **Last Occurrence Tracking**
```python
# Track last occurrence of elements
last_seen = {}
for i, val in enumerate(arr):
    if val in last_seen:
        # Handle duplicate
        start = max(start, last_seen[val] + 1)
    last_seen[val] = i
```

### 3. **Two Pointers with Set**
```python
# Maintain unique elements in window
unique_elements = set()
start = 0
for end in range(n):
    while arr[end] in unique_elements:
        unique_elements.remove(arr[start])
        start += 1
    unique_elements.add(arr[end])
```

## Edge Cases to Remember

1. **Single element**: Length is 1
2. **All unique elements**: Length is n
3. **All same elements**: Length is 1
4. **Large song IDs**: Hash map handles large integers efficiently
5. **Empty array**: Handle edge case

## Problem-Solving Framework

1. **Identify subarray nature**: This is about finding longest subarray with unique elements
2. **Consider sliding window**: Natural approach for subarray problems
3. **Track unique elements**: Use hash map or set to track seen elements
4. **Handle duplicates**: Move start pointer when encountering duplicates
5. **Optimize the approach**: Use last occurrence tracking for efficiency

---

*This analysis shows how to systematically improve from O(n³) to O(n) and extracts reusable insights for sliding window problems.* 