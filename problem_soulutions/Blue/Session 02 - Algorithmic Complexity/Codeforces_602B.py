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
# Approach: Sliding window tracking min/max values

n = int(input())
a = list(map(int, input().split()))

left, right = 0, 0
max_almost_constant_range = 1
evaluating_range = 1
range_max = a[0]
range_min = a[0]

while True:
    if right >= n - 1:
        break
    right += 1
    if a[right] > range_max and range_max - range_min >= 1:
        range_max = a[right]
        if max_almost_constant_range <= evaluating_range:
            max_almost_constant_range = evaluating_range
        evaluating_range = 1
        for i in range(right - 1, left - 1, -1):
            if a[i] == range_min:
                left = i + 1
                range_min += 1
                break
            evaluating_range += 1
    elif a[right] < range_min and range_max - range_min >= 1:
        range_min = a[right]
        if max_almost_constant_range <= evaluating_range:
            max_almost_constant_range = evaluating_range
        evaluating_range = 1
        for i in range(right - 1, left - 1, -1):
            if a[i] == range_max:
                left = i + 1
                range_max -= 1
                break
            evaluating_range += 1
    else:
        if a[right] > range_max:
            range_max = a[right]
        elif a[right] < range_min:
            range_min = a[right]
        evaluating_range += 1
        if max_almost_constant_range < evaluating_range:
            max_almost_constant_range = evaluating_range
print(max_almost_constant_range)
