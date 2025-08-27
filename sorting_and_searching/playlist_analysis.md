# CSES Playlist - Problem Analysis

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
    
    for right in range(n):
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