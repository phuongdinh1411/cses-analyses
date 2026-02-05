---
layout: simple
title: "Sliding Window Summary"
permalink: /problem_soulutions/sliding_window/summary
---

# Sliding Window

Welcome to the Sliding Window section! This category covers efficient techniques for solving problems involving contiguous subarrays and substrings.

## Key Concepts & Techniques

### Window Management

#### Window Size Types
- **Fixed Size Windows**: Constant length windows
  - *When to use*: When window size is predetermined
  - *Time*: O(n) where n is array length
  - *Space*: O(1) additional space
  - *Applications*: Fixed-size subarray problems, window statistics
  - *Implementation*: Maintain window boundaries, slide by one position
- **Variable Size Windows**: Dynamic length windows
  - *When to use*: When window size depends on content or constraints
  - *Time*: O(n) where n is array length
  - *Space*: O(k) where k is number of distinct elements
  - *Applications*: Optimization problems, constraint satisfaction
  - *Implementation*: Expand/contract window based on conditions

#### Window Movement Techniques
- **Two Pointers**: Left and right boundaries
  - *When to use*: Most sliding window problems
  - *Time*: O(n) where n is array length
  - *Space*: O(1) additional space
  - *Applications*: Subarray problems, substring problems
  - *Implementation*: Move left/right pointers based on conditions
- **Sliding Technique**: Move window by one position
  - *When to use*: When you need to process all possible windows
  - *Time*: O(n) where n is array length
  - *Space*: O(1) additional space
  - *Applications*: Fixed-size windows, window statistics
  - *Implementation*: Remove leftmost element, add rightmost element

#### Window State Management
- **Property Maintenance**: Keep track of window properties
  - *When to use*: When you need to maintain window characteristics
  - *Time*: O(1) per update
  - *Space*: O(k) where k is number of distinct elements
  - *Applications*: Distinct elements, sum maintenance, min/max tracking
  - *Implementation*: Use hash maps, counters, or data structures
- **State Updates**: Efficiently update window state
  - *When to use*: When window content changes
  - *Time*: O(1) per update
  - *Space*: O(k) where k is number of distinct elements
  - *Applications*: Element counting, sum updates, property tracking
  - *Implementation*: Increment/decrement counters, update data structures

### Common Sliding Window Patterns

#### Two Pointers Technique
- **Opposite Direction**: Start from ends, move inward
  - *When to use*: Sorted arrays, find pairs
  - *Time*: O(n)
  - *Space*: O(1)
  - *Applications*: Two sum, palindrome checking, sorted array problems
  - *Implementation*: Move pointers based on comparison
- **Same Direction**: Both pointers move forward
  - *When to use*: Sliding window, subarray problems
  - *Time*: O(n)
  - *Space*: O(1)
  - *Applications*: Subarray sum, window problems, substring problems
  - *Implementation*: Move right pointer, adjust left pointer as needed

#### Hash Map for Counting
- **Element Frequency**: Count occurrences of elements
  - *When to use*: When you need to track element frequencies
  - *Time*: O(1) per update
  - *Space*: O(k) where k is number of distinct elements
  - *Applications*: Distinct elements, frequency-based problems
  - *Implementation*: Use hash map to store element counts
- **Character Counting**: Count characters in string windows
  - *When to use*: String problems, character-based windows
  - *Time*: O(1) per update
  - *Space*: O(26) for lowercase letters
  - *Applications*: String problems, character frequency
  - *Implementation*: Use array or hash map for character counts

#### Monotonic Queue for Min/Max
- **Minimum Queue**: Maintain minimum in window
  - *When to use*: When you need minimum element in window
  - *Time*: O(1) amortized per operation
  - *Space*: O(n) in worst case
  - *Applications*: Sliding window minimum, optimization problems
  - *Implementation*: Use deque to maintain increasing order
- **Maximum Queue**: Maintain maximum in window
  - *When to use*: When you need maximum element in window
  - *Time*: O(1) amortized per operation
  - *Space*: O(n) in worst case
  - *Applications*: Sliding window maximum, optimization problems
  - *Implementation*: Use deque to maintain decreasing order

#### Prefix Sums for Quick Calculation
- **Range Sum**: Calculate sum of window quickly
  - *When to use*: When you need to calculate window sum frequently
  - *Time*: O(1) per query
  - *Space*: O(n) for prefix array
  - *Applications*: Subarray sum, window sum, range queries
  - *Implementation*: Precompute prefix sums, use difference for range
- **Cumulative Properties**: Track cumulative window properties
  - *When to use*: When you need cumulative window characteristics
  - *Time*: O(1) per update
  - *Space*: O(n) for prefix array
  - *Applications*: Cumulative sum, cumulative properties
  - *Implementation*: Maintain prefix array, update incrementally

### Advanced Sliding Window Techniques

#### Multiple Window Properties
- **Combined Conditions**: Multiple constraints on window
  - *When to use*: When window must satisfy multiple conditions
  - *Time*: O(n) where n is array length
  - *Space*: O(k) where k is number of distinct elements
  - *Applications*: Complex window problems, multi-constraint problems
  - *Implementation*: Maintain multiple data structures for different properties
- **Nested Windows**: Windows within windows
  - *When to use*: When you need to consider nested window structures
  - *Time*: O(n²) in worst case
  - *Space*: O(k) where k is number of distinct elements
  - *Applications*: Complex window problems, nested structures
  - *Implementation*: Use nested loops or recursive approaches

#### Optimization Techniques
- **State Compression**: Reduce memory usage
  - *When to use*: When memory is limited
  - *Time*: O(1) per update
  - *Space*: O(1) additional space
  - *Applications*: Memory-constrained problems, optimization
  - *Implementation*: Use bit manipulation or compact data structures
- **Lazy Updates**: Defer expensive operations
  - *When to use*: When updates are expensive
  - *Time*: O(1) per update, O(k) per query
  - *Space*: O(k) where k is number of distinct elements
  - *Applications*: Expensive update operations, lazy evaluation
  - *Implementation*: Use lazy evaluation, batch updates

#### Specialized Data Structures
- **Ordered Set**: Maintain sorted order
  - *When to use*: When you need sorted window elements
  - *Time*: O(log n) per operation
  - *Space*: O(n)
  - *Applications*: Sorted window problems, order statistics
  - *Implementation*: Use balanced binary search tree
- **Segment Tree**: Range queries on window
  - *When to use*: When you need range queries on window
  - *Time*: O(log n) per query/update
  - *Space*: O(n)
  - *Applications*: Range queries, window statistics
  - *Implementation*: Use segment tree for range operations

### Problem-Specific Techniques

#### Subarray Sum Problems
- **Target Sum**: Find subarray with given sum
  - *When to use*: When you need to find subarray with specific sum
  - *Time*: O(n)
  - *Space*: O(n) for hash map
  - *Applications*: Subarray sum, target sum problems
  - *Implementation*: Use hash map to store prefix sums
- **Maximum Sum**: Find subarray with maximum sum
  - *When to use*: When you need maximum sum subarray
  - *Time*: O(n)
  - *Space*: O(1)
  - *Applications*: Maximum subarray sum, optimization
  - *Implementation*: Use Kadane's algorithm or sliding window

#### Distinct Elements Problems
- **K Distinct**: Find subarray with exactly K distinct elements
  - *When to use*: When you need subarray with specific number of distinct elements
  - *Time*: O(n)
  - *Space*: O(k) where k is number of distinct elements
  - *Applications*: Distinct elements, counting problems
  - *Implementation*: Use hash map to count distinct elements
- **All Distinct**: Find subarray with all distinct elements
  - *When to use*: When you need subarray with all unique elements
  - *Time*: O(n)
  - *Space*: O(k) where k is number of distinct elements
  - *Applications*: Unique elements, string problems
  - *Implementation*: Use hash map to track element presence

#### String Window Problems
- **Character Coverage**: Find window covering all characters
  - *When to use*: When you need window covering all required characters
  - *Time*: O(n)
  - *Space*: O(26) for lowercase letters
  - *Applications*: String problems, character coverage
  - *Implementation*: Use hash map to track character coverage
- **No Repeating**: Find window with no repeating characters
  - *When to use*: When you need window with unique characters
  - *Time*: O(n)
  - *Space*: O(26) for lowercase letters
  - *Applications*: String problems, unique characters
  - *Implementation*: Use hash map to track character frequency

### Optimization Strategies

#### Time Optimization
- **Early Termination**: Stop when condition met
  - *When to use*: When exact result not needed
  - *Example*: Stop when first valid window found
- **Batch Processing**: Process multiple windows together
  - *When to use*: When you need to process multiple windows
  - *Example*: Process all windows of same size together
- **Precomputation**: Compute values once
  - *When to use*: When same calculations repeated
  - *Example*: Precompute prefix sums for range queries

#### Space Optimization
- **In-place Updates**: Modify data in place
  - *When to use*: When original data not needed
  - *Example*: In-place window updates
- **Lazy Evaluation**: Compute on demand
  - *When to use*: When not all values needed
  - *Example*: Lazy window property computation
- **Memory Pool**: Reuse allocated memory
  - *When to use*: When memory allocation is expensive
  - *Example*: Reuse hash maps for different windows

## Problem Categories

### Basic Sliding Window
- [Maximum Subarray Sum](maximum_subarray_sum_analysis) - Kadane's algorithm
- [Minimum Subarray Sum](minimum_subarray_sum_analysis) - Minimum sum window
- [Fixed Length Subarray Sum](fixed_length_subarray_sum_analysis) - Fixed size windows

### Variable Size Windows
- [Longest Subarray with Sum](longest_subarray_with_sum_analysis) - Maximum length with target
- [Shortest Subarray with Sum](shortest_subarray_with_sum_analysis) - Minimum length with target
- [Subarray with Given Sum](subarray_with_given_sum_analysis) - Find subarray with sum

### Subarray Sum Problems
- [Subarray Sums I](subarray_sums_i_analysis) - Count subarrays with sum
- [Subarray Sums II](subarray_sums_ii_analysis) - Advanced sum problems

### Distinct Elements
- [Subarray Distinct Values](subarray_distinct_values_analysis) - Count distinct elements
- [Subarray with K Distinct](subarray_with_k_distinct_analysis) - K distinct elements

### Min/Max in Window
- [Subarray Maximums](subarray_maximums_analysis) - Maximum in each window
- [Subarray Minimums](subarray_minimums_analysis) - Minimum in each window

### String Windows
- [Longest Substring Without Repeating](longest_substring_without_repeating_analysis) - Unique characters
- [Minimum Window Substring](minimum_window_substring_analysis) - Character coverage

### Advanced Applications
- [Sliding Window Advertisement](sliding_window_advertisement_analysis) - Real-world application

## Detailed Examples and Implementations

### Classic Sliding Window Patterns with Code

#### 1. Fixed Size Window Problems
```python
def max_sum_subarray_fixed_size(arr, k):
  """Find maximum sum of subarray of fixed size k"""
  if len(arr) < k:
    return 0
  
  # Calculate sum of first window
  window_sum = sum(arr[:k])
  max_sum = window_sum
  
  # Slide the window
  for i in range(k, len(arr)):
    window_sum = window_sum - arr[i - k] + arr[i]
    max_sum = max(max_sum, window_sum)
  
  return max_sum

def max_sum_subarray_fixed_size_optimized(arr, k):
  """Optimized version using prefix sums"""
  if len(arr) < k:
    return 0
  
  # Build prefix sum array
  prefix_sum = [0] * (len(arr) + 1)
  for i in range(len(arr)):
    prefix_sum[i + 1] = prefix_sum[i] + arr[i]
  
  max_sum = float('-inf')
  for i in range(len(arr) - k + 1):
    current_sum = prefix_sum[i + k] - prefix_sum[i]
    max_sum = max(max_sum, current_sum)
  
  return max_sum

def sliding_window_maximum(arr, k):
  """Find maximum element in each sliding window of size k"""
  from collections import deque
  
  dq = deque()  # Store indices
  result = []
  
  # Process first window
  for i in range(k):
    # Remove elements smaller than current element
    while dq and arr[dq[-1]] <= arr[i]:
      dq.pop()
    dq.append(i)
  
  result.append(arr[dq[0]])
  
  # Process remaining windows
  for i in range(k, len(arr)):
    # Remove elements outside current window
    while dq and dq[0] <= i - k:
      dq.popleft()
    
    # Remove elements smaller than current element
    while dq and arr[dq[-1]] <= arr[i]:
      dq.pop()
    
    dq.append(i)
    result.append(arr[dq[0]])
  
  return result

def sliding_window_minimum(arr, k):
  """Find minimum element in each sliding window of size k"""
  from collections import deque
  
  dq = deque()  # Store indices
  result = []
  
  # Process first window
  for i in range(k):
    # Remove elements larger than current element
    while dq and arr[dq[-1]] >= arr[i]:
      dq.pop()
    dq.append(i)
  
  result.append(arr[dq[0]])
  
  # Process remaining windows
  for i in range(k, len(arr)):
    # Remove elements outside current window
    while dq and dq[0] <= i - k:
      dq.popleft()
    
    # Remove elements larger than current element
    while dq and arr[dq[-1]] >= arr[i]:
      dq.pop()
    
    dq.append(i)
    result.append(arr[dq[0]])
  
  return result
```

#### 2. Variable Size Window Problems
```python
def longest_substring_without_repeating(s):
  """Find length of longest substring without repeating characters"""
  char_set = set()
  left = 0
  max_length = 0
  
  for right in range(len(s)):
    while s[right] in char_set:
      char_set.remove(s[left])
      left += 1
    
    char_set.add(s[right])
    max_length = max(max_length, right - left + 1)
  
  return max_length

def longest_substring_without_repeating_optimized(s):
  """Optimized version using hash map"""
  char_map = {}
  left = 0
  max_length = 0
  
  for right in range(len(s)):
    if s[right] in char_map and char_map[s[right]] >= left:
      left = char_map[s[right]] + 1
    
    char_map[s[right]] = right
    max_length = max(max_length, right - left + 1)
  
  return max_length

def minimum_window_substring(s, t):
  """Find minimum window in s that contains all characters in t"""
  from collections import Counter
  
  if not s or not t:
    return ""
  
  dict_t = Counter(t)
  required = len(dict_t)
  
  left = right = 0
  formed = 0
  window_counts = {}
  
  ans = float('inf'), None, None
  
  while right < len(s):
    char = s[right]
    window_counts[char] = window_counts.get(char, 0) + 1
    
    if char in dict_t and window_counts[char] == dict_t[char]:
      formed += 1
    
    while left <= right and formed == required:
      char = s[left]
      
      if right - left + 1 < ans[0]:
        ans = (right - left + 1, left, right)
      
      window_counts[char] -= 1
      if char in dict_t and window_counts[char] < dict_t[char]:
        formed -= 1
      
      left += 1
    
    right += 1
  
  return "" if ans[0] == float('inf') else s[ans[1]:ans[2] + 1]

def longest_substring_with_at_most_k_distinct(s, k):
  """Find longest substring with at most k distinct characters"""
  if not s or k == 0:
    return 0
  
  char_count = {}
  left = 0
  max_length = 0
  
  for right in range(len(s)):
    char_count[s[right]] = char_count.get(s[right], 0) + 1
    
    while len(char_count) > k:
      char_count[s[left]] -= 1
      if char_count[s[left]] == 0:
        del char_count[s[left]]
      left += 1
    
    max_length = max(max_length, right - left + 1)
  
  return max_length
```

#### 3. Subarray Sum Problems
```python
def subarray_sum_equals_k(nums, k):
  """Find total number of subarrays with sum equal to k"""
  count = 0
  prefix_sum = 0
  sum_count = {0: 1}  # Initialize with sum 0 appearing once
  
  for num in nums:
    prefix_sum += num
    
    # If (prefix_sum - k) exists, then there's a subarray with sum k
    if prefix_sum - k in sum_count:
      count += sum_count[prefix_sum - k]
    
    # Update count of current prefix sum
    sum_count[prefix_sum] = sum_count.get(prefix_sum, 0) + 1
  
  return count

def subarray_sum_equals_k_positive_only(nums, k):
  """Find subarray with sum k (positive numbers only)"""
  left = 0
  current_sum = 0
  
  for right in range(len(nums)):
    current_sum += nums[right]
    
    while current_sum > k and left <= right:
      current_sum -= nums[left]
      left += 1
    
    if current_sum == k:
      return nums[left:right + 1]
  
  return []

def maximum_size_subarray_sum_equals_k(nums, k):
  """Find maximum size subarray with sum equal to k"""
  prefix_sum = 0
  sum_index = {0: -1}  # Initialize with sum 0 at index -1
  max_length = 0
  
  for i, num in enumerate(nums):
    prefix_sum += num
    
    if prefix_sum - k in sum_index:
      max_length = max(max_length, i - sum_index[prefix_sum - k])
    
    if prefix_sum not in sum_index:
      sum_index[prefix_sum] = i
  
  return max_length

def subarray_sum_closest_to_target(nums, target):
  """Find subarray with sum closest to target"""
  prefix_sum = 0
  sum_index = {0: -1}
  min_diff = float('inf')
  result = []
  
  for i, num in enumerate(nums):
    prefix_sum += num
    
    # Check current prefix sum
    diff = abs(prefix_sum - target)
    if diff < min_diff:
      min_diff = diff
      result = nums[0:i + 1]
    
    # Check all previous prefix sums
    for prev_sum, prev_index in sum_index.items():
      diff = abs(prefix_sum - prev_sum - target)
      if diff < min_diff:
        min_diff = diff
        result = nums[prev_index + 1:i + 1]
    
    sum_index[prefix_sum] = i
  
  return result
```

### Advanced Sliding Window Techniques

#### 1. Multiple Window Properties
```python
def longest_substring_with_at_most_k_distinct_and_no_repeats(s, k):
  """Find longest substring with at most k distinct characters and no repeats"""
  char_count = {}
  left = 0
  max_length = 0
  
  for right in range(len(s)):
    char_count[s[right]] = char_count.get(s[right], 0) + 1
    
    # Shrink window if we have more than k distinct chars or any repeats
    while len(char_count) > k or max(char_count.values()) > 1:
      char_count[s[left]] -= 1
      if char_count[s[left]] == 0:
        del char_count[s[left]]
      left += 1
    
    max_length = max(max_length, right - left + 1)
  
  return max_length

def subarray_with_sum_and_length_constraints(nums, target_sum, min_length, max_length):
  """Find subarray with specific sum and length constraints"""
  prefix_sum = 0
  sum_indices = {0: [-1]}  # Store all indices for each sum
  result = []
  
  for i, num in enumerate(nums):
    prefix_sum += num
    
    # Check if we can form target sum with valid length
    if prefix_sum - target_sum in sum_indices:
      for prev_index in sum_indices[prefix_sum - target_sum]:
        length = i - prev_index
        if min_length <= length <= max_length:
          result.append(nums[prev_index + 1:i + 1])
    
    # Store current prefix sum index
    if prefix_sum not in sum_indices:
      sum_indices[prefix_sum] = []
    sum_indices[prefix_sum].append(i)
  
  return result

def sliding_window_with_multiple_conditions(arr, conditions):
  """Generic sliding window with multiple conditions"""
  left = 0
  window_properties = {}
  valid_windows = []
  
  for right in range(len(arr)):
    # Update window properties
    element = arr[right]
    window_properties[element] = window_properties.get(element, 0) + 1
    
    # Check if all conditions are satisfied
    while not all(condition(window_properties) for condition in conditions):
      # Shrink window from left
      window_properties[arr[left]] -= 1
      if window_properties[arr[left]] == 0:
        del window_properties[arr[left]]
      left += 1
    
    # Current window satisfies all conditions
    valid_windows.append(arr[left:right + 1])
  
  return valid_windows
```

#### 2. String Processing with Sliding Window
```python
def find_all_anagrams(s, p):
  """Find all starting indices of anagrams of p in s"""
  if len(s) < len(p):
    return []
  
  p_count = {}
  for char in p:
    p_count[char] = p_count.get(char, 0) + 1
  
  window_count = {}
  result = []
  
  # Initialize window
  for i in range(len(p)):
    window_count[s[i]] = window_count.get(s[i], 0) + 1
  
  if window_count == p_count:
    result.append(0)
  
  # Slide window
  for i in range(len(p), len(s)):
    # Add new character
    window_count[s[i]] = window_count.get(s[i], 0) + 1
    
    # Remove old character
    window_count[s[i - len(p)]] -= 1
    if window_count[s[i - len(p)]] == 0:
      del window_count[s[i - len(p)]]
    
    # Check if current window is an anagram
    if window_count == p_count:
      result.append(i - len(p) + 1)
  
  return result

def longest_repeating_character_replacement(s, k):
  """Find longest substring with same character after at most k replacements"""
  char_count = {}
  left = 0
  max_length = 0
  max_freq = 0
  
  for right in range(len(s)):
    char_count[s[right]] = char_count.get(s[right], 0) + 1
    max_freq = max(max_freq, char_count[s[right]])
    
    # If window size - max_freq > k, we need to shrink
    if right - left + 1 - max_freq > k:
      char_count[s[left]] -= 1
      left += 1
    
    max_length = max(max_length, right - left + 1)
  
  return max_length

def permutation_in_string(s1, s2):
  """Check if s1 is a permutation of any substring in s2"""
  if len(s1) > len(s2):
    return False
  
  s1_count = {}
  for char in s1:
    s1_count[char] = s1_count.get(char, 0) + 1
  
  window_count = {}
  
  # Initialize window
  for i in range(len(s1)):
    window_count[s2[i]] = window_count.get(s2[i], 0) + 1
  
  if window_count == s1_count:
    return True
  
  # Slide window
  for i in range(len(s1), len(s2)):
    # Add new character
    window_count[s2[i]] = window_count.get(s2[i], 0) + 1
    
    # Remove old character
    window_count[s2[i - len(s1)]] -= 1
    if window_count[s2[i - len(s1)]] == 0:
      del window_count[s2[i - len(s1)]]
    
    if window_count == s1_count:
      return True
  
  return False
```

#### 3. Advanced Data Structures with Sliding Window
```python
class SlidingWindowMedian:
  """Maintain median in sliding window using two heaps"""
  def __init__(self, k):
    self.k = k
    self.small = []  # Max heap (negated values)
    self.large = []  # Min heap
    self.window = []
    self.balance = 0
  
  def add(self, num):
    self.window.append(num)
    
    if len(self.window) > self.k:
      # Remove oldest element
      old_num = self.window.pop(0)
      self.remove_from_heaps(old_num)
    
    # Add new element
    if not self.small or num <= -self.small[0]:
      heapq.heappush(self.small, -num)
      self.balance += 1
    else:
      heapq.heappush(self.large, num)
      self.balance -= 1
    
    self.rebalance()
  
  def remove_from_heaps(self, num):
    if self.small and num <= -self.small[0]:
      self.small.remove(-num)
      heapq.heapify(self.small)
      self.balance -= 1
    else:
      self.large.remove(num)
      heapq.heapify(self.large)
      self.balance += 1
    
    self.rebalance()
  
  def rebalance(self):
    if self.balance > 1:
      val = -heapq.heappop(self.small)
      heapq.heappush(self.large, val)
      self.balance -= 2
    elif self.balance < -1:
      val = heapq.heappop(self.large)
      heapq.heappush(self.small, -val)
      self.balance += 2
  
  def get_median(self):
    if len(self.window) < self.k:
      return None
    
    if self.k % 2 == 1:
      return -self.small[0] if self.balance > 0 else self.large[0]
    else:
      return (-self.small[0] + self.large[0]) / 2

def sliding_window_median(nums, k):
  """Find median in each sliding window of size k"""
  import heapq
  
  swm = SlidingWindowMedian(k)
  medians = []
  
  for num in nums:
    swm.add(num)
    if len(swm.window) == k:
      medians.append(swm.get_median())
  
  return medians

class SlidingWindowOrderedSet:
  """Maintain ordered set in sliding window"""
  def __init__(self, k):
    self.k = k
    self.window = []
    self.sorted_elements = []
  
  def add(self, num):
    self.window.append(num)
    
    if len(self.window) > self.k:
      # Remove oldest element
      old_num = self.window.pop(0)
      self.sorted_elements.remove(old_num)
    
    # Add new element in sorted order
    import bisect
    bisect.insort(self.sorted_elements, num)
  
  def get_kth_smallest(self, k):
    if k <= len(self.sorted_elements):
      return self.sorted_elements[k - 1]
    return None
  
  def get_range(self, start, end):
    return self.sorted_elements[start:end]
```

#### 4. Optimization Techniques
```python
def sliding_window_optimized_memory(arr, k, operation):
  """Sliding window with optimized memory usage"""
  if len(arr) < k:
    return []
  
  # Use single variable for window sum instead of array
  window_sum = sum(arr[:k])
  result = [operation(window_sum)]
  
  for i in range(k, len(arr)):
    window_sum = window_sum - arr[i - k] + arr[i]
    result.append(operation(window_sum))
  
  return result

def batch_sliding_window(arr, k, batch_size):
  """Process multiple sliding windows in batches"""
  results = []
  
  for batch_start in range(0, len(arr) - k + 1, batch_size):
    batch_end = min(batch_start + batch_size, len(arr) - k + 1)
    batch_results = []
    
    for i in range(batch_start, batch_end):
      window = arr[i:i + k]
      batch_results.append(sum(window))
    
    results.extend(batch_results)
  
  return results

def lazy_sliding_window(arr, k, lazy_condition):
  """Sliding window with lazy evaluation"""
  window = []
  result = []
  
  for i, num in enumerate(arr):
    window.append(num)
    
    if len(window) > k:
      window.pop(0)
    
    if len(window) == k:
      # Only compute if lazy condition is met
      if lazy_condition(window):
        result.append(sum(window))
      else:
        result.append(None)  # Lazy evaluation placeholder
  
  return result
```

## Tips for Success

1. **Master Two Pointers**: Essential technique
2. **Understand Window Properties**: What to maintain
3. **Learn State Management**: Efficient updates
4. **Practice Implementation**: Code common patterns
5. **Study Advanced Techniques**: Multiple properties, optimization
6. **Handle Edge Cases**: Empty windows, boundary conditions

## Common Pitfalls to Avoid

1. **Window Boundaries**: Off-by-one errors
2. **State Updates**: Missing updates
3. **Memory Usage**: Inefficient storage
4. **Time Complexity**: Slow operations

## Advanced Topics

### Window Types
- **Fixed Size**: Constant length
- **Variable Size**: Dynamic length
- **Multiple Properties**: Combined conditions
- **Nested Windows**: Windows within windows

### Data Structures
- **Deque**: Efficient min/max
- **Hash Map**: Element counting
- **Segment Tree**: Range queries
- **Monotonic Queue**: Order maintenance

### Special Cases
- **Empty Windows**: Edge cases
- **Single Element**: Minimal windows
- **Full Array**: Maximum windows
- **No Solution**: Invalid cases

## Algorithm Complexities

### Basic Operations
- **Window Sliding**: O(1) per slide
- **Property Update**: O(1) typical
- **State Maintenance**: O(1) amortized
- **Result Calculation**: O(1) per window

### Advanced Operations
- **Distinct Counting**: O(1) amortized
- **Min/Max Maintenance**: O(1) amortized
- **Sum Calculation**: O(1) with prefix
- **String Processing**: O(1) per character

## 📚 **Additional Learning Resources**

### **LeetCode Pattern Integration**
For interview preparation and pattern recognition, complement your CSES learning with these LeetCode resources:

- **[Awesome LeetCode Resources](https://github.com/ashishps1/awesome-leetcode-resources)** - Comprehensive collection of LeetCode patterns, templates, and curated problem lists
- **[Sliding Window Pattern](https://github.com/ashishps1/awesome-leetcode-resources#-patterns)** - Essential sliding window techniques and templates
- **[Sliding Window Template](https://github.com/ashishps1/awesome-leetcode-resources#-must-read-leetcode-articles)** - Specific sliding window templates and optimization strategies

### **Related LeetCode Problems**
Practice these LeetCode problems to reinforce sliding window concepts:

- **Fixed Window Pattern**: [Maximum Average Subarray I](https://leetcode.com/problems/maximum-average-subarray-i/), [Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/)
- **Variable Window Pattern**: [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/), [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/)
- **Two Pointers Pattern**: [Container With Most Water](https://leetcode.com/problems/container-with-most-water/), [3Sum](https://leetcode.com/problems/3sum/)
- **Prefix Sum Pattern**: [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/), [Continuous Subarray Sum](https://leetcode.com/problems/continuous-subarray-sum/)

---

Ready to start? Begin with [Maximum Subarray Sum](maximum_subarray_sum_analysis) and work your way through the problems in order of difficulty!