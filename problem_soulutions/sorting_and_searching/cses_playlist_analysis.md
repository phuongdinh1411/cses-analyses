---
layout: simple
title: "Playlist
permalink: /problem_soulutions/sorting_and_searching/cses_playlist_analysis/"
---


# Playlist

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
```"
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

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Playlist with K Duplicates Allowed**
**Problem**: Find longest sequence where each song appears at most K times.
```python
def playlist_k_duplicates(songs, k):
    n = len(songs)
    song_count = {}
    max_length = 0
    start = 0
    
    for end in range(n):
        current_song = songs[end]
        song_count[current_song] = song_count.get(current_song, 0) + 1
        
        # Shrink window if we exceed k occurrences
        while song_count[current_song] > k:
            song_count[songs[start]] -= 1
            start += 1
        
        max_length = max(max_length, end - start + 1)
    
    return max_length
```

#### **Variation 2: Playlist with Minimum Length**
**Problem**: Find shortest sequence with exactly K unique songs.
```python
def playlist_min_length_k_unique(songs, k):
    n = len(songs)
    song_count = {}
    min_length = float('inf')
    start = 0
    
    for end in range(n):
        current_song = songs[end]
        song_count[current_song] = song_count.get(current_song, 0) + 1
        
        # Shrink window while maintaining k unique songs
        while len(song_count) > k:
            song_count[songs[start]] -= 1
            if song_count[songs[start]] == 0:
                del song_count[songs[start]]
            start += 1
        
        if len(song_count) == k:
            min_length = min(min_length, end - start + 1)
    
    return min_length if min_length != float('inf') else -1
```

#### **Variation 3: Playlist with Weighted Songs**
**Problem**: Each song has a weight. Find sequence with maximum total weight.
```python
def playlist_weighted(songs, weights):
    n = len(songs)
    song_count = {}
    max_weight = 0
    current_weight = 0
    start = 0
    
    for end in range(n):
        current_song = songs[end]
        current_weight += weights[end]
        song_count[current_song] = song_count.get(current_song, 0) + 1
        
        # Shrink window if we have duplicates
        while song_count[current_song] > 1:
            song_count[songs[start]] -= 1
            current_weight -= weights[start]
            start += 1
        
        max_weight = max(max_weight, current_weight)
    
    return max_weight
```

#### **Variation 4: Playlist with Genre Constraints**
**Problem**: Find longest sequence with at most G different genres.
```python
def playlist_genre_constraints(songs, genres, max_genres):
    n = len(songs)
    genre_count = {}
    max_length = 0
    start = 0
    
    for end in range(n):
        current_genre = genres[end]
        genre_count[current_genre] = genre_count.get(current_genre, 0) + 1
        
        # Shrink window if we exceed genre limit
        while len(genre_count) > max_genres:
            genre_count[genres[start]] -= 1
            if genre_count[genres[start]] == 0:
                del genre_count[genres[start]]
            start += 1
        
        max_length = max(max_length, end - start + 1)
    
    return max_length
```

#### **Variation 5: Playlist with Time Constraints**
**Problem**: Each song has duration. Find sequence with total duration ≤ T.
```python
def playlist_time_constraints(songs, durations, max_time):
    n = len(songs)
    song_count = {}
    current_time = 0
    max_length = 0
    start = 0
    
    for end in range(n):
        current_song = songs[end]
        current_time += durations[end]
        song_count[current_song] = song_count.get(current_song, 0) + 1
        
        # Shrink window if we exceed time or have duplicates
        while current_time > max_time or song_count[current_song] > 1:
            song_count[songs[start]] -= 1
            current_time -= durations[start]
            start += 1
        
        max_length = max(max_length, end - start + 1)
    
    return max_length
```

### 🔗 **Related Problems & Concepts**

#### **1. Sliding Window Problems**
- **Longest Substring Without Repeating**: Find substring with unique characters
- **Minimum Window Substring**: Find smallest substring containing all characters
- **Substring with Concatenation**: Find substring containing all words
- **Longest Substring with At Most K**: Find substring with at most k distinct characters

#### **2. Two Pointers Problems**
- **Two Sum**: Find pair with given sum
- **Three Sum**: Find triplet with given sum
- **Container With Most Water**: Find maximum area
- **Trapping Rain Water**: Calculate trapped water

#### **3. Hash Table Problems**
- **Hash Table Implementation**: Custom hash table design
- **Collision Resolution**: Handle hash collisions
- **Load Factor**: Optimize hash table performance
- **Hash Functions**: Design good hash functions

#### **4. String Processing Problems**
- **String Matching**: Find pattern occurrences in text
- **Anagram Detection**: Check if strings are anagrams
- **Palindrome Detection**: Check if string is palindrome
- **String Compression**: Compress repeated characters

#### **5. Array Manipulation Problems**
- **Array Rotation**: Rotate array by k positions
- **Array Partitioning**: Partition array based on conditions
- **Array Merging**: Merge sorted arrays
- **Array Sorting**: Sort array efficiently

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n = int(input())
    songs = list(map(int, input().split()))
    
    last_seen = {}
    max_length = 0
    start = 0
    
    for end in range(n):
        current_song = songs[end]
        if current_song in last_seen:
            start = max(start, last_seen[current_song] + 1)
        last_seen[current_song] = end
        max_length = max(max_length, end - start + 1)
    
    print(max_length)
```

#### **2. Range Queries**
```python
# Precompute longest unique sequences for all ranges
def precompute_unique_ranges(songs):
    n = len(songs)
    unique_lengths = [[0] * n for _ in range(n)]
    
    for i in range(n):
        song_count = {}
        for j in range(i, n):
            song_count[songs[j]] = song_count.get(songs[j], 0) + 1
            if song_count[songs[j]] == 1:
                unique_lengths[i][j] = j - i + 1
            else:
                unique_lengths[i][j] = unique_lengths[i][j-1]
    
    return unique_lengths

# Answer queries about longest unique sequences
def unique_query(unique_lengths, l, r):
    return unique_lengths[l][r]
```

#### **3. Interactive Problems**
```python
# Interactive playlist analyzer
def interactive_playlist():
    n = int(input("Enter number of songs: "))
    songs = list(map(int, input("Enter song IDs: ").split()))
    
    print(f"Playlist: {songs}")
    
    # Analyze playlist
    last_seen = {}
    max_length = 0
    start = 0
    best_start = 0
    best_end = 0
    
    for end in range(n):
        current_song = songs[end]
        if current_song in last_seen:
            start = max(start, last_seen[current_song] + 1)
        last_seen[current_song] = end
        
        if end - start + 1 > max_length:
            max_length = end - start + 1
            best_start = start
            best_end = end
    
    print(f"Longest unique sequence: {max_length}")
    print(f"Sequence: {songs[best_start:best_end+1]}")
```

### 🧮 **Mathematical Extensions**

#### **1. Probability and Statistics**
- **Expected Length**: Calculate expected length of unique sequences
- **Variance Analysis**: Analyze distribution of sequence lengths
- **Sampling Theory**: Estimate unique sequences from samples
- **Confidence Intervals**: Estimate population parameters

#### **2. Information Theory**
- **Entropy**: Calculate information content of song distribution
- **Compression**: Compress playlist data efficiently
- **Redundancy**: Measure duplicate information
- **Uniqueness**: Quantify how unique songs are

#### **3. Combinatorics**
- **Permutations**: Count arrangements of unique songs
- **Combinations**: Count selections of unique songs
- **Partitions**: Count ways to partition songs
- **Derangements**: Count arrangements with no fixed points

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Sliding Window**: Two-pointer technique
- **Hash Tables**: Efficient lookup data structures
- **Two Pointers**: Efficient array processing
- **String Algorithms**: Pattern matching techniques

#### **2. Mathematical Concepts**
- **Set Theory**: Union, intersection, difference operations
- **Combinatorics**: Counting principles and arrangements
- **Probability**: Random sampling and distributions
- **Information Theory**: Entropy and data compression

#### **3. Programming Concepts**
- **Data Structures**: Efficient storage and retrieval
- **Algorithm Analysis**: Time and space complexity
- **Memory Management**: Optimizing space usage
- **Performance Optimization**: Trade-offs between time and space

---

*This analysis demonstrates sliding window techniques and shows various extensions for sequence processing problems.* 