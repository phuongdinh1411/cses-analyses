---
layout: simple
title: "Playlist
permalink: /problem_soulutions/sorting_and_searching/playlist_analysis/"
---


# Playlist

## Problem Statement
Given a playlist of n songs, each with a genre, find the longest continuous segment where no song appears more than once.

### Input
The first input line has an integer n: the number of songs.
The second line has n integers a1,a2,…,an: the genres of the songs.

### Output
Print one integer: the length of the longest continuous segment with unique songs.

### Constraints
- 1 ≤ n ≤ 2⋅10^5
- 1 ≤ ai ≤ 10^9

### Example
```
Input:
8
1 2 1 3 2 7 4 2

Output:
5
```

## Solution Progression

### Approach 1: Brute Force - O(n²)
**Description**: Check all possible subarrays for uniqueness.

```python
def playlist_naive(n, genres):
    max_length = 0
    
    for start in range(n):
        seen = set()
        for end in range(start, n):
            if genres[end] in seen:
                break
            seen.add(genres[end])
            max_length = max(max_length, end - start + 1)
    
    return max_length
```

**Why this is inefficient**: We check O(n²) subarrays, leading to O(n²) time complexity.

### Improvement 1: Sliding Window - O(n)
**Description**: Use sliding window technique to find the longest unique segment.

```python
def playlist_optimized(n, genres):
    max_length = 0
    left = 0
    seen = {}
    
    for right in range(n):"
        # If we've seen this genre before, move left pointer
        if genres[right] in seen and seen[genres[right]] >= left:
            left = seen[genres[right]] + 1
        
        seen[genres[right]] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

**Why this improvement works**: We maintain a sliding window where all elements are unique by tracking the last occurrence of each genre and adjusting the left pointer accordingly.

## Final Optimal Solution

```python
n = int(input())
genres = list(map(int, input().split()))

def find_longest_unique_playlist(n, genres):
    max_length = 0
    left = 0
    seen = {}
    
    for right in range(n):
        # If we've seen this genre before, move left pointer
        if genres[right] in seen and seen[genres[right]] >= left:
            left = seen[genres[right]] + 1
        
        seen[genres[right]] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length

result = find_longest_unique_playlist(n, genres)
print(result)
```

## Complexity Analysis

| Approach | Time Complexity | Space Complexity | Key Insight |
|----------|----------------|------------------|-------------|
| Brute Force | O(n²) | O(n) | Check all subarrays |
| Sliding Window | O(n) | O(n) | Maintain unique window |

## Key Insights for Other Problems

### 1. **Longest Unique Subarray**
**Principle**: Use sliding window to maintain uniqueness.
**Applicable to**: Subarray problems, uniqueness problems, window problems

### 2. **Sliding Window Technique**
**Principle**: Maintain a window that satisfies the constraint and expand/contract as needed.
**Applicable to**: Subarray problems, window problems, range problems

### 3. **Last Occurrence Tracking**
**Principle**: Track the last occurrence of each element to efficiently adjust window boundaries.
**Applicable to**: Uniqueness problems, duplicate detection, window optimization

## Notable Techniques

### 1. **Sliding Window with Hash Map**
```python
def sliding_window_unique(arr):
    max_length = 0
    left = 0
    seen = {}
    
    for right in range(len(arr)):
        if arr[right] in seen and seen[arr[right]] >= left:
            left = seen[arr[right]] + 1
        
        seen[arr[right]] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

### 2. **Window Boundary Management**
```python
def manage_window_boundaries(arr):
    left = 0
    seen = {}
    
    for right in range(len(arr)):
        # Adjust left boundary if duplicate found
        if arr[right] in seen and seen[arr[right]] >= left:
            left = seen[arr[right]] + 1
        
        seen[arr[right]] = right
    
    return left, right
```

### 3. **Unique Segment Detection**
```python
def detect_unique_segments(arr):
    segments = []
    left = 0
    seen = {}
    
    for right in range(len(arr)):
        if arr[right] in seen and seen[arr[right]] >= left:
            segments.append((left, right - 1))
            left = seen[arr[right]] + 1
        
        seen[arr[right]] = right
    
    segments.append((left, len(arr) - 1))
    return segments
```

## Problem-Solving Framework

1. **Identify problem type**: This is a longest unique subarray problem
2. **Choose approach**: Use sliding window technique
3. **Initialize variables**: Set up left pointer, hash map, and max length
4. **Expand window**: Move right pointer and track elements
5. **Contract window**: Move left pointer when duplicates found
6. **Update result**: Keep track of maximum window size
7. **Return result**: Output the longest unique segment length

---

*This analysis shows how to efficiently find the longest continuous segment with unique elements using sliding window technique.* 

## 🎯 Problem Variations & Related Questions

### 🔄 **Variations of the Original Problem**

#### **Variation 1: Weighted Playlist**
**Problem**: Each song has a weight/rating. Find the longest continuous segment with unique songs and maximum total weight.
```python
def weighted_playlist(n, genres, weights):
    max_length = 0
    max_weight = 0
    left = 0
    seen = {}
    current_weight = 0
    
    for right in range(n):
        # If we've seen this genre before, move left pointer
        if genres[right] in seen and seen[genres[right]] >= left:
            # Remove weight of songs from left to last occurrence
            for i in range(left, seen[genres[right]] + 1):
                current_weight -= weights[i]
            left = seen[genres[right]] + 1
        
        current_weight += weights[right]
        seen[genres[right]] = right
        
        # Update result if we have better weight for same or longer length
        if right - left + 1 >= max_length:
            if right - left + 1 > max_length or current_weight > max_weight:
                max_length = right - left + 1
                max_weight = current_weight
    
    return max_length, max_weight
```

#### **Variation 2: K-Duplicate Playlist**
**Problem**: Find the longest continuous segment where no song appears more than k times.
```python
def k_duplicate_playlist(n, genres, k):
    max_length = 0
    left = 0
    freq = {}
    
    for right in range(n):
        freq[genres[right]] = freq.get(genres[right], 0) + 1
        
        # Move left pointer if frequency exceeds k
        while freq[genres[right]] > k:
            freq[genres[left]] -= 1
            if freq[genres[left]] == 0:
                del freq[genres[left]]
            left += 1
        
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

#### **Variation 3: Genre-Constrained Playlist**
**Problem**: Find the longest continuous segment with unique songs from a specific set of genres.
```python
def genre_constrained_playlist(n, genres, allowed_genres):
    max_length = 0
    left = 0
    seen = {}
    
    for right in range(n):
        # Skip songs not in allowed genres
        if genres[right] not in allowed_genres:
            left = right + 1
            seen.clear()
            continue
        
        # If we've seen this genre before, move left pointer
        if genres[right] in seen and seen[genres[right]] >= left:
            left = seen[genres[right]] + 1
        
        seen[genres[right]] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

#### **Variation 4: Minimum Length Constraint**
**Problem**: Find the longest continuous segment with unique songs that has at least L songs.
```python
def min_length_playlist(n, genres, min_length):
    max_length = 0
    left = 0
    seen = {}
    
    for right in range(n):
        # If we've seen this genre before, move left pointer
        if genres[right] in seen and seen[genres[right]] >= left:
            left = seen[genres[right]] + 1
        
        seen[genres[right]] = right
        current_length = right - left + 1
        
        # Only update if we meet minimum length requirement
        if current_length >= min_length:
            max_length = max(max_length, current_length)
    
    return max_length if max_length >= min_length else 0
```

#### **Variation 5: Circular Playlist**
**Problem**: Find the longest continuous segment with unique songs in a circular playlist.
```python
def circular_playlist(n, genres):
    # Extend array to handle circular case
    extended_genres = genres + genres
    max_length = 0
    left = 0
    seen = {}
    
    for right in range(2 * n):
        # If we've seen this genre before, move left pointer
        if extended_genres[right] in seen and seen[extended_genres[right]] >= left:
            left = seen[extended_genres[right]] + 1
        
        seen[extended_genres[right]] = right
        
        # Only count if window doesn't wrap around more than once
        if right - left + 1 <= n:
            max_length = max(max_length, right - left + 1)
    
    return max_length
```

### 🔗 **Related Problems & Concepts**

#### **1. Subarray Problems**
- **Longest Subarray with Sum**: Find longest subarray with given sum
- **Longest Subarray with XOR**: Find longest subarray with given XOR
- **Longest Subarray with Product**: Find longest subarray with given product
- **Longest Subarray with Range**: Find longest subarray in given range

#### **2. Sliding Window Problems**
- **Longest Substring Without Repeating**: Find longest substring with unique characters
- **Minimum Window Substring**: Find smallest window containing all characters
- **Subarray with K Different Integers**: Similar to original problem
- **Fruit Into Baskets**: Maximum fruits in two baskets

#### **3. Uniqueness Problems**
- **Distinct Elements**: Count distinct elements in array
- **Unique Pairs**: Find pairs with unique values
- **Unique Triplets**: Find triplets with unique values
- **Unique Subsequences**: Find subsequences with unique elements

#### **4. Frequency Problems**
- **Most Frequent Element**: Find most frequent element in subarray
- **Frequency Queries**: Answer frequency-based queries
- **Mode in Subarray**: Find mode of subarray
- **Frequency Distribution**: Analyze frequency distribution

#### **5. Optimization Problems**
- **Maximum Subarray**: Find subarray with maximum sum
- **Minimum Subarray**: Find subarray with minimum sum
- **Optimal Subarray**: Find subarray optimizing given criteria
- **Constrained Subarray**: Find subarray satisfying constraints

### 🎯 **Competitive Programming Variations**

#### **1. Multiple Test Cases**
```python
t = int(input())
for _ in range(t):
    n = int(input())
    genres = list(map(int, input().split()))
    
    result = find_longest_unique_playlist(n, genres)
    print(result)
```

#### **2. Range Queries**
```python
# Precompute for different ranges
def precompute_playlist_lengths(genres):
    n = len(genres)
    # Precompute for all possible ranges
    dp = {}
    
    for start in range(n):
        for end in range(start, n):
            subarray = genres[start:end+1]
            length = find_longest_unique_playlist(len(subarray), subarray)
            dp[(start, end)] = length
    
    return dp

# Answer range queries efficiently
def playlist_query(dp, start, end):
    return dp.get((start, end), 0)
```

#### **3. Interactive Problems**
```python
# Interactive playlist analyzer
def interactive_playlist_analyzer():
    n = int(input("Enter number of songs: "))
    genres = []
    
    for i in range(n):
        genre = int(input(f"Enter genre for song {i+1}: "))
        genres.append(genre)
    
    print("Playlist:", genres)
    
    while True:
        query = input("Enter query (longest/weighted/k_duplicate/circular/exit): ")
        if query == "exit":
            break
        
        if query == "longest":
            result = find_longest_unique_playlist(n, genres)
            print(f"Longest unique segment: {result}")
        elif query == "weighted":
            weights = []
            for i in range(n):
                weight = int(input(f"Enter weight for song {i+1}: "))
                weights.append(weight)
            length, weight = weighted_playlist(n, genres, weights)
            print(f"Longest weighted segment: {length}, Weight: {weight}")
        elif query == "k_duplicate":
            k = int(input("Enter k: "))
            result = k_duplicate_playlist(n, genres, k)
            print(f"Longest segment with at most {k} duplicates: {result}")
        elif query == "circular":
            result = circular_playlist(n, genres)
            print(f"Longest circular unique segment: {result}")
```

### 🧮 **Mathematical Extensions**

#### **1. Combinatorics**
- **Permutations**: Arrangements of unique songs
- **Combinations**: Combinations of songs
- **Partitions**: Ways to partition playlist
- **Inclusion-Exclusion**: Count using inclusion-exclusion

#### **2. Probability Theory**
- **Expected Value**: Expected length of unique segments
- **Probability Distribution**: Distribution of segment lengths
- **Random Sampling**: Sampling segments randomly
- **Statistical Analysis**: Statistical properties of playlists

#### **3. Number Theory**
- **Prime Factorization**: Prime factors in song genres
- **GCD/LCM**: Greatest common divisor and least common multiple
- **Modular Arithmetic**: Playlists with modular properties
- **Number Sequences**: Special sequences in playlists

### 📚 **Learning Resources**

#### **1. Related Algorithms**
- **Sliding Window Algorithm**: Core technique for subarray problems
- **Two Pointers Technique**: Efficient array traversal
- **Hash Maps**: Efficient frequency tracking
- **Dynamic Programming**: Alternative approach for some variations

#### **2. Mathematical Concepts**
- **Set Theory**: Understanding unique elements as sets
- **Combinatorics**: Counting principles and techniques
- **Optimization**: Finding optimal subarrays
- **Complexity Analysis**: Time and space complexity analysis

#### **3. Programming Concepts**
- **Hash Maps**: Efficient frequency tracking
- **Dynamic Programming**: Alternative approach for some variations
- **Binary Search**: For optimization problems
- **Data Structures**: Efficient storage and retrieval

---

*This analysis demonstrates efficient playlist analysis techniques and shows various extensions for subarray problems.* 