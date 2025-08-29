---
layout: simple
title: "Playlist"
permalink: /problem_soulutions/sorting_and_searching/playlist_analysis
---

# Playlist

## Problem Description

**Problem**: Given a playlist of n songs, each with a genre, find the longest continuous segment where no song appears more than once.

**Input**: 
- First line: n (number of songs)
- Second line: n integers a₁, a₂, ..., aₙ (genres of the songs)

**Output**: Length of the longest continuous segment with unique songs.

**Example**:
```
Input:
8
1 2 1 3 2 7 4 2

Output:
5

Explanation: 
The longest segment with unique genres is [1, 3, 2, 7, 4] starting from position 3.
Segment: [1, 3, 2, 7, 4] has length 5 and all genres are unique.
```

## 🎯 Solution Progression

### Step 1: Understanding the Problem
**What are we trying to do?**
- Find longest continuous subarray with unique elements
- No duplicate genres allowed in the segment
- Return the length of such segment

**Key Observations:**
- This is a classic sliding window problem
- Need to track last occurrence of each genre
- When we encounter a duplicate, move left pointer
- Maintain maximum length seen so far

### Step 2: Brute Force Approach
**Idea**: Check all possible subarrays for uniqueness.

```python
def playlist_brute_force(n, genres):
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

**Why this works:**
- Checks all possible subarrays
- Uses set to track seen genres
- Simple to understand and implement
- O(n²) time complexity

### Step 3: Sliding Window Optimization
**Idea**: Use sliding window technique to find the longest unique segment.

```python
def playlist_sliding_window(n, genres):
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

**Why this is better:**
- O(n) time complexity
- Uses sliding window optimization
- Much more efficient
- Handles large constraints

### Step 4: Complete Solution
**Putting it all together:**

```python
def solve_playlist():
    n = int(input())
    genres = list(map(int, input().split()))
    
    max_length = 0
    left = 0
    seen = {}
    
    for right in range(n):
        # If we've seen this genre before, move left pointer
        if genres[right] in seen and seen[genres[right]] >= left:
            left = seen[genres[right]] + 1
        
        seen[genres[right]] = right
        max_length = max(max_length, right - left + 1)
    
    print(max_length)

# Main execution
if __name__ == "__main__":
    solve_playlist()
```

**Why this works:**
- Optimal sliding window approach
- Handles all edge cases
- Efficient implementation
- Clear and readable code

### Step 5: Testing Our Solution
**Let's verify with examples:**

```python
def test_solution():
    test_cases = [
        (8, [1, 2, 1, 3, 2, 7, 4, 2], 5),
        (5, [1, 2, 3, 4, 5], 5),
        (5, [1, 1, 1, 1, 1], 1),
        (3, [1, 2, 1], 2),
        (4, [1, 2, 3, 1], 3),
    ]
    
    for n, genres, expected in test_cases:
        result = solve_test(n, genres)
        print(f"n={n}, genres={genres}")
        print(f"Expected: {expected}, Got: {result}")
        print(f"{'✓ PASS' if result == expected else '✗ FAIL'}")
        print()

def solve_test(n, genres):
    max_length = 0
    left = 0
    seen = {}
    
    for right in range(n):
        if genres[right] in seen and seen[genres[right]] >= left:
            left = seen[genres[right]] + 1
        
        seen[genres[right]] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length

test_solution()
```

## 🔧 Implementation Details

### Time Complexity
- **Time**: O(n) - single pass through array
- **Space**: O(n) - hash map to track last occurrences

### Why This Solution Works
- **Sliding Window**: Maintains window with unique elements
- **Hash Map**: Tracks last occurrence of each genre
- **Pointer Movement**: Moves left pointer when duplicate found
- **Optimal Approach**: Each element processed at most twice

## 🎯 Key Insights

### 1. **Sliding Window Technique**
- Maintains window with unique elements
- Expands window to the right
- Contracts window from left when needed
- Key insight for optimization

### 2. **Hash Map Usage**
- Tracks last occurrence of each genre
- Enables O(1) lookup and update
- Essential for efficient window management
- Crucial for understanding

### 3. **Pointer Management**
- Right pointer always moves forward
- Left pointer moves when duplicate found
- Window always contains unique elements
- Important for correctness

## 🎯 Problem Variations

### Variation 1: Longest Substring Without Repeating Characters
**Problem**: Find longest substring with unique characters.

```python
def longest_unique_substring(s):
    max_length = 0
    left = 0
    seen = {}
    
    for right in range(len(s)):
        if s[right] in seen and seen[s[right]] >= left:
            left = seen[s[right]] + 1
        
        seen[s[right]] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

### Variation 2: Longest Subarray with At Most K Duplicates
**Problem**: Find longest subarray where each element appears at most k times.

```python
def longest_subarray_k_duplicates(n, arr, k):
    max_length = 0
    left = 0
    count = {}
    
    for right in range(n):
        count[arr[right]] = count.get(arr[right], 0) + 1
        
        # Shrink window if we have more than k duplicates
        while count[arr[right]] > k:
            count[arr[left]] -= 1
            left += 1
        
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

### Variation 3: Longest Subarray with Unique Elements and Sum ≤ Target
**Problem**: Find longest subarray with unique elements and sum ≤ target.

```python
def longest_unique_subarray_with_sum_limit(n, arr, target):
    max_length = 0
    left = 0
    current_sum = 0
    seen = {}
    
    for right in range(n):
        # If we've seen this element before, move left pointer
        if arr[right] in seen and seen[arr[right]] >= left:
            # Remove elements from left until we remove the duplicate
            while left <= seen[arr[right]]:
                current_sum -= arr[left]
                left += 1
        
        seen[arr[right]] = right
        current_sum += arr[right]
        
        # Shrink window if sum exceeds target
        while current_sum > target:
            current_sum -= arr[left]
            left += 1
        
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

### Variation 4: Longest Subarray with Unique Elements and Minimum Length
**Problem**: Find longest subarray with unique elements and minimum length k.

```python
def longest_unique_subarray_min_length(n, arr, k):
    max_length = 0
    left = 0
    seen = {}
    
    for right in range(n):
        if arr[right] in seen and seen[arr[right]] >= left:
            left = seen[arr[right]] + 1
        
        seen[arr[right]] = right
        
        # Only consider subarrays with length >= k
        if right - left + 1 >= k:
            max_length = max(max_length, right - left + 1)
    
    return max_length
```

### Variation 5: Dynamic Playlist Management
**Problem**: Support adding/removing songs dynamically and finding longest unique segment.

```python
class DynamicPlaylist:
    def __init__(self):
        self.genres = []
        self.max_length = 0
        self.left = 0
        self.seen = {}
    
    def add_song(self, genre):
        self.genres.append(genre)
        right = len(self.genres) - 1
        
        if genre in self.seen and self.seen[genre] >= self.left:
            self.left = self.seen[genre] + 1
        
        self.seen[genre] = right
        self.max_length = max(self.max_length, right - self.left + 1)
        
        return self.max_length
    
    def remove_song(self, index):
        if 0 <= index < len(self.genres):
            removed_genre = self.genres.pop(index)
            
            # Recalculate if the removed song was in our current window
            if index >= self.left:
                # Rebuild the window
                self.max_length = 0
                self.left = 0
                self.seen = {}
                
                for i, genre in enumerate(self.genres):
                    if genre in self.seen and self.seen[genre] >= self.left:
                        self.left = self.seen[genre] + 1
                    
                    self.seen[genre] = i
                    self.max_length = max(self.max_length, i - self.left + 1)
        
        return self.max_length
    
    def get_max_length(self):
        return self.max_length
```

## 🔗 Related Problems

- **[Longest Substring Without Repeating Characters](/cses-analyses/problem_soulutions/sliding_window/longest_substring_without_repeating_analysis)**: String version of this problem
- **[Subarray with K Distinct Elements](/cses-analyses/problem_soulutions/sliding_window/subarray_with_k_distinct_analysis)**: K distinct elements variation
- **[Minimum Window Substring](/cses-analyses/problem_soulutions/sliding_window/minimum_window_substring_analysis)**: Minimum window problems

## 📚 Learning Points

1. **Sliding Window**: Powerful technique for subarray problems
2. **Hash Map Tracking**: Efficient way to track element occurrences
3. **Two Pointers**: Manage window boundaries efficiently
4. **Unique Element Problems**: Common pattern in competitive programming

---

**This is a great introduction to sliding window techniques and unique element problems!** 🎯 