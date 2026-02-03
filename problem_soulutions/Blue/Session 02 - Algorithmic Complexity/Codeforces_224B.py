# Problem from Codeforces
# http://codeforces.com/problemset/problem/224/B
#
# Problem: Sereja and Suffixes (Distinct K Segment)
#
# Given an array of n integers and a number k, find the shortest contiguous
# segment that contains exactly k distinct values. Output the 1-based start
# and end positions of this segment.
#
# Input:
# - Line 1: n k (array size, required distinct count)
# - Line 2: n integers (array elements, values up to 100000)
#
# Output: Two integers - start and end positions (1-based), or "-1 -1" if
#         no such segment exists
#
# Approach: Sliding window - expand right until k distinct found, then
#           shrink left while maintaining k distinct

n, k = map(int, input().split())
a = list(map(int, input().split()))

current_number = -1
total_distinct = 0

start_position = 0
end_position = -1

distinct_list = [0] * 100001

for i in range(n):
    if distinct_list[a[i]] == 0:
        total_distinct += 1
    distinct_list[a[i]] += 1
    if total_distinct == k:
        end_position = i
        break

if end_position == -1:
    print('-1 -1')
else:
    while True:
        if distinct_list[a[start_position]] > 1:
            distinct_list[a[start_position]] -= 1
            start_position += 1
        else:
            break
    print(start_position + 1, end_position + 1, sep=' ')
