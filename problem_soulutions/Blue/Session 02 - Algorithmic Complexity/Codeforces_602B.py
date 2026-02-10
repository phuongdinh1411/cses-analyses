# Problem from Codeforces
# http://codeforces.com/problemset/problem/602/B
#
# Problem: Approximating a Constant Range (Almost Constant Range)
#
# Given an array of n integers, find the length of the longest contiguous
# subarray where the difference between the maximum and minimum values is
# at most 1 (i.e., max - min <= 1).
#
# Input:
# - Line 1: Integer n (array size)
# - Line 2: n integers (array elements)
#
# Output: Length of the longest "almost constant" subarray
#
# Approach: Sliding window with monotonic deques to track min/max efficiently
# - Use two deques: one for tracking maximum (decreasing), one for minimum (increasing)
# - Expand window to the right, shrink from left when max - min > 1
# - Time complexity: O(n), Space complexity: O(n)

from collections import deque

n = int(input())
a = list(map(int, input().split()))

max_deque = deque()  # Indices of elements in decreasing order (front = max)
min_deque = deque()  # Indices of elements in increasing order (front = min)
left = 0
result = 0

for right in range(n):
    # Maintain decreasing deque for maximum
    while max_deque and a[max_deque[-1]] < a[right]:
        max_deque.pop()
    max_deque.append(right)

    # Maintain increasing deque for minimum
    while min_deque and a[min_deque[-1]] > a[right]:
        min_deque.pop()
    min_deque.append(right)

    # Shrink window from left while max - min > 1
    while a[max_deque[0]] - a[min_deque[0]] > 1:
        left += 1
        # Remove elements outside the window
        if max_deque[0] < left:
            max_deque.popleft()
        if min_deque[0] < left:
            min_deque.popleft()

    result = max(result, right - left + 1)

print(result)
